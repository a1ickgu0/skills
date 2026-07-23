#!/usr/bin/env python3
"""Validate the handoff and completion of the generic video pipeline."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


SHA256 = re.compile(r"^[0-9a-f]{64}$")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(directory: Path) -> list[str]:
    errors: list[str] = []
    files = {
        name: directory / name for name in (
            "transcript.md", "transcription-manifest.json",
            "video-analysis.md", "analysis-manifest.json", "pipeline-status.json",
        )
    }
    for name, path in files.items():
        if not path.is_file():
            errors.append(f"missing pipeline output: {name}")
    if errors:
        return errors

    try:
        transcription = json.loads(files["transcription-manifest.json"].read_text(encoding="utf-8"))
        if float(transcription.get("audio_coverage_percent", 0)) < 100:
            errors.append("Stage 1 audio coverage is below 100%")
    except (json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid Stage 1 manifest: {exc}")

    try:
        analysis = json.loads(files["analysis-manifest.json"].read_text(encoding="utf-8"))
        inputs = analysis.get("inputs", [])
        roles = {item.get("role") for item in inputs if isinstance(item, dict)}
        if not {"transcript", "transcription-manifest"}.issubset(roles):
            errors.append("Stage 2 manifest lacks required Stage 1 input roles")
        for item in inputs:
            rel = item.get("path", "")
            path = directory / rel
            sha = item.get("sha256", "")
            if not path.is_file() or not SHA256.fullmatch(sha) or digest(path) != sha:
                errors.append(f"Stage 2 input handoff mismatch: {rel}")
        output = analysis.get("output", {})
        if output.get("path") != "video-analysis.md" or output.get("sha256") != digest(files["video-analysis.md"]):
            errors.append("Stage 2 output hash mismatch")
    except (json.JSONDecodeError, AttributeError, TypeError) as exc:
        errors.append(f"invalid Stage 2 manifest: {exc}")

    try:
        status = json.loads(files["pipeline-status.json"].read_text(encoding="utf-8"))
        if status.get("input_route") not in {"media", "transcript"}:
            errors.append("pipeline status input_route must be media or transcript")
        stages = status.get("stages", {})
        if stages.get("transcription") != "complete" or stages.get("analysis") != "complete":
            errors.append("pipeline stages are not both complete")
        if float(status.get("audio_coverage_percent", 0)) < 100:
            errors.append("pipeline status audio coverage is below 100%")
        if not status.get("validators"):
            errors.append("pipeline status has no validator record")
        required_outputs = set(files) - {"pipeline-status.json"}
        if not required_outputs.issubset(set(status.get("outputs", []))):
            errors.append("pipeline status output list is incomplete")
    except (json.JSONDecodeError, AttributeError, TypeError, ValueError) as exc:
        errors.append(f"invalid pipeline status: {exc}")
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
    print("PASS: both pipeline stages and their handoff are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
