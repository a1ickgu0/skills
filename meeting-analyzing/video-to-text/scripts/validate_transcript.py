#!/usr/bin/env python3
"""Validate complete bilingual transcript and transcription manifest outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TIME_BLOCK = re.compile(r"^### \[(\d{2}):(\d{2}):(\d{2})[–-](\d{2}):(\d{2}):(\d{2})\]", re.MULTILINE)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"\'')
    return result


def to_seconds(parts: tuple[str, ...], offset: int) -> int:
    return int(parts[offset]) * 3600 + int(parts[offset + 1]) * 60 + int(parts[offset + 2])


def validate(directory: Path) -> list[str]:
    errors: list[str] = []
    transcript_path = directory / "transcript.md"
    manifest_path = directory / "transcription-manifest.json"
    for path in (transcript_path, manifest_path):
        if not path.is_file():
            errors.append(f"missing file: {path.name}")
    if errors:
        return errors

    transcript = transcript_path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(transcript)
    required = [
        "media_id", "source_locator", "source_language", "translation_language",
        "authorization_basis", "duration_seconds", "coverage_start_seconds",
        "coverage_end_seconds", "transcription_model", "review_model", "generated_at",
    ]
    for key in required:
        if not metadata.get(key):
            errors.append(f"missing transcript metadata: {key}")
    authorization = metadata.get("authorization_basis", "").lower()
    VALID_AUTH = {"user-confirmed", "user-confirmed-rights", "licensed", "owned", "public-domain"}
    if authorization not in VALID_AUTH:
        errors.append("authorization_basis must record confirmed rights")
    try:
        duration = float(metadata.get("duration_seconds", "nan"))
        start = float(metadata.get("coverage_start_seconds", "nan"))
        end = float(metadata.get("coverage_end_seconds", "nan"))
        if start != 0 or end + 0.5 < duration:
            errors.append("transcript metadata does not declare full media coverage")
    except ValueError:
        errors.append("duration and coverage metadata must be numeric")

    blocks = TIME_BLOCK.findall(transcript)
    if not blocks:
        errors.append("transcript has no timestamp blocks")
    else:
        last_start = -1
        for block in blocks:
            start, end = to_seconds(block, 0), to_seconds(block, 3)
            if end < start or start < last_start:
                errors.append("transcript timestamp blocks are out of order")
                break
            last_start = start

    language = metadata.get("source_language", "").lower()
    chinese = language.startswith(("zh", "chinese", "中文"))
    if chinese:
        if "**原文（中文）**" not in transcript:
            errors.append("Chinese transcript must contain 原文（中文） blocks")
        if metadata.get("translation_language") != "none":
            errors.append("Chinese transcript translation_language must be none")
    else:
        if "**Original**" not in transcript or "**中文**" not in transcript:
            errors.append("non-Chinese transcript must contain Original and 中文 blocks")
        if metadata.get("translation_language") != "zh-CN":
            errors.append("non-Chinese transcript translation_language must be zh-CN")
    if re.search(r"TODO|TBD|SOURCE-LANGUAGE VERBATIM TEXT|中文翻译。", transcript):
        errors.append("placeholder text remains in transcript")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if float(manifest.get("audio_coverage_percent", 0)) < 100:
            errors.append("manifest audio coverage is below 100%")
        for key in ("device", "cpu_workers", "model", "review_model", "chunks", "realtime_factor"):
            if key not in manifest:
                errors.append(f"manifest missing runtime field: {key}")
    except (json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid manifest: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    errors = validate(args.directory)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("PASS: transcript and transcription manifest satisfy the contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

