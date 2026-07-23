#!/usr/bin/env python3
"""Optional speaker diarization post-processing for transcripts.

Integrates pyannote.audio to assign speaker labels to transcript segments.
When pyannote is unavailable, degrades gracefully with a clear message.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_segments(transcript_path: Path) -> list[dict[str, Any]]:
    """Parse timestamp blocks from a transcript.md into segment dicts."""
    import re
    text = transcript_path.read_text(encoding="utf-8")
    TIME_BLOCK = re.compile(
        r"^### \[(\d{2}):(\d{2}):(\d{2})[–-](\d{2}):(\d{2}):(\d{2})\](.*)$",
        re.MULTILINE,
    )
    segments: list[dict[str, Any]] = []
    blocks = list(TIME_BLOCK.finditer(text))
    for i, match in enumerate(blocks):
        h1, m1, s1, h2, m2, s2 = map(int, match.groups()[:6])
        start = h1 * 3600 + m1 * 60 + s1
        end = h2 * 3600 + m2 * 60 + s2
        speaker_label = match.group(6).strip()
        # Extract text between this block and the next
        block_end = blocks[i + 1].start() if i + 1 < len(blocks) else len(text)
        body = text[match.end():block_end].strip()
        segments.append({
            "start": start,
            "end": end,
            "speaker_label": speaker_label,
            "text": body,
        })
    return segments


def diarize(audio_path: str, segments: list[dict[str, Any]], hf_token: str | None = None) -> list[dict[str, Any]]:
    """Run pyannote speaker diarization and assign labels to segments."""
    try:
        from pyannote.audio import Pipeline
    except ImportError:
        print(
            "pyannote.audio is not installed. Install it with: "
            "pip install pyannote.audio",
            file=sys.stderr,
        )
        return segments

    token = hf_token or None
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=token,
    )
    diarization = pipeline(audio_path)

    speaker_map: dict[int, str] = {}
    next_speaker = 0

    for segment in segments:
        mid = (segment["start"] + segment["end"]) / 2
        best_speaker = None
        best_overlap = 0.0
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            overlap = min(turn.end, segment["end"]) - max(turn.start, segment["start"])
            if overlap > best_overlap:
                best_overlap = overlap
                best_speaker = speaker
        if best_speaker is not None and best_overlap > 0:
            if best_speaker not in speaker_map:
                speaker_map[best_speaker] = f"SPEAKER_{next_speaker:02d}"
                next_speaker += 1
            segment["speaker_id"] = speaker_map[best_speaker]

    return segments


def update_transcript(transcript_path: Path, segments: list[dict[str, Any]]) -> None:
    """Rewrite transcript.md with speaker_id annotations in timestamp headers."""
    import re
    text = transcript_path.read_text(encoding="utf-8")

    TIME_BLOCK = re.compile(
        r"^(### \[(\d{2}):(\d{2}):(\d{2})[–-](\d{2}):(\d{2}):(\d{2})\]).*$",
        re.MULTILINE,
    )

    seg_index = 0

    def replace_header(match: re.Match) -> str:
        nonlocal seg_index
        if seg_index < len(segments):
            speaker_id = segments[seg_index].get("speaker_id", "")
            seg_index += 1
            if speaker_id:
                return f"{match.group(1)} {speaker_id}"
        return match.group(1)

    updated = TIME_BLOCK.sub(replace_header, text)
    transcript_path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Optional speaker diarization for transcripts")
    parser.add_argument("transcript_dir", type=Path, help="Directory containing transcript.md and transcription-manifest.json")
    parser.add_argument("audio_input", type=Path, help="Original audio/video file for diarization")
    parser.add_argument("--hf-token", default=None, help="HuggingFace token for pyannote model access")
    parser.add_argument("--dry-run", action="store_true", help="Print speaker assignments without modifying files")
    args = parser.parse_args()

    transcript_path = args.transcript_dir / "transcript.md"
    manifest_path = args.transcript_dir / "transcription-manifest.json"

    if not transcript_path.is_file():
        print(f"ERROR: transcript.md not found in {args.transcript_dir}", file=sys.stderr)
        return 1

    segments = load_segments(transcript_path)
    if not segments:
        print("ERROR: no timestamp blocks found in transcript.md", file=sys.stderr)
        return 1

    segments = diarize(str(args.audio_input), segments, args.hf_token)

    if args.dry_run:
        for seg in segments:
            sid = seg.get("speaker_id", "unknown")
            print(f"[{seg['start']:.1f}s–{seg['end']:.1f}s] {sid}")
        return 0

    update_transcript(transcript_path, segments)

    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["diarization"] = {
            "model": "pyannote/speaker-diarization-3.1",
            "speaker_count": len(set(s.get("speaker_id", "") for s in segments)),
            "per_segment": [
                {"start": s["start"], "end": s["end"], "speaker_id": s.get("speaker_id", "")}
                for s in segments
            ],
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
