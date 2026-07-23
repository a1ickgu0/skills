#!/usr/bin/env python3
"""Validate generic transcript-analysis deliverables."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "Executive summary", "Scope and evidence", "Full chronology",
    "Themes and argument", "Mechanisms and process",
    "Entities, claims, and metrics", "Demonstrations and cases",
    "Evidence and status ledger", "Requested analytical lenses",
    "Contradictions and uncertainties", "Unanswered questions",
    "Method and sources",
]
REQUIRED_LABELS = [
    "speech-only", "slide-only", "demo", "customer-claim",
    "official-cross-check", "analysis-inference", "uncertain", "future-looking",
]
TIME_BLOCK = re.compile(r"^### \[\d{2}:\d{2}:\d{2}[–-]\d{2}:\d{2}:\d{2}\]", re.MULTILINE)
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(directory: Path) -> list[str]:
    errors: list[str] = []
    transcript = directory / "transcript.md"
    transcription_manifest = directory / "transcription-manifest.json"
    analysis = directory / "video-analysis.md"
    analysis_manifest = directory / "analysis-manifest.json"
    for path in (transcript, transcription_manifest, analysis, analysis_manifest):
        if not path.is_file():
            errors.append(f"missing file: {path.name}")
    if errors:
        return errors

    text = analysis.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+(?:\d+\.\s+)?{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"analysis missing section: {section}")
    if not TIME_BLOCK.search(text):
        errors.append("Full chronology has no timestamped segment")
    for label in REQUIRED_LABELS:
        if f"`{label}`" not in text:
            errors.append(f"analysis missing evidence/status label: {label}")
    if re.search(r"TODO|TBD|PLACEHOLDER", text, re.IGNORECASE):
        errors.append("placeholder text remains in analysis")

    try:
        source_manifest = json.loads(transcription_manifest.read_text(encoding="utf-8"))
        if float(source_manifest.get("audio_coverage_percent", 0)) < 100:
            errors.append("transcription manifest audio coverage is below 100%")
    except (json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid transcription manifest: {exc}")

    try:
        manifest = json.loads(analysis_manifest.read_text(encoding="utf-8"))
        for key in ("schema_version", "generated_at", "inputs", "analytical_lenses", "output"):
            if key not in manifest:
                errors.append(f"analysis manifest missing field: {key}")
        inputs = manifest.get("inputs", [])
        if not isinstance(inputs, list) or not inputs:
            errors.append("analysis manifest inputs must be a non-empty array")
        else:
            roles = set()
            for item in inputs:
                rel = item.get("path", "")
                sha = item.get("sha256", "")
                roles.add(item.get("role"))
                path = directory / rel
                if not path.is_file():
                    errors.append(f"manifest input does not exist: {rel}")
                elif not SHA256.fullmatch(sha) or digest(path) != sha:
                    errors.append(f"manifest input hash mismatch: {rel}")
            if not {"transcript", "transcription-manifest"}.issubset(roles):
                errors.append("analysis manifest must include transcript and transcription-manifest roles")
        output = manifest.get("output", {})
        if output.get("path") != "video-analysis.md" or output.get("sha256") != digest(analysis):
            errors.append("analysis manifest output path or hash mismatch")
        if not isinstance(manifest.get("analytical_lenses"), list):
            errors.append("analytical_lenses must be an array")
    except (json.JSONDecodeError, AttributeError) as exc:
        errors.append(f"invalid analysis manifest: {exc}")
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
    print("PASS: video analysis and manifests satisfy the generic contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
