#!/usr/bin/env python3
"""Validate domain-specific video-analysis content against a YAML profile."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def load_profile(path: Path) -> dict:
    if yaml is None:
        print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
        raise SystemExit(2)
    if not path.is_file():
        print(f"ERROR: profile not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


TIME_BLOCK = re.compile(r"^### \[\d{2}:\d{2}:\d{2}[–-]\d{2}:\d{2}:\d{2}\]", re.MULTILINE)


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result


def validate(path: Path, profile: dict) -> list[str]:
    if not path.is_file():
        return [f"missing analysis file: {path}"]

    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)

    # --- Frontmatter checks ---
    corpus = profile.get("corpus", {})
    item_id_pattern = corpus.get("item_id_pattern", "")
    if item_id_pattern:
        if not re.fullmatch(item_id_pattern, meta.get("item_id", "")):
            errors.append(f"item_id must match pattern: {item_id_pattern}")

    task1 = meta.get("task1_file", "")
    task1_dir = corpus.get("task1_dir", "")
    if task1_dir and not task1.startswith(task1_dir):
        errors.append(f"task1_file must be under {task1_dir}")

    official_source = meta.get("official_source_url", "")
    if not official_source.startswith(("http://", "https://")):
        errors.append("official_source_url must be an explicit URL")

    if meta.get("analysis_coverage") != "full-video":
        errors.append("analysis_coverage must be full-video")

    # --- Section checks ---
    sections = profile.get("sections", [])
    for section in sections:
        if not re.search(rf"^##\s+\d+\.\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"missing analysis section: {section}")

    # --- Chronology check ---
    if not TIME_BLOCK.search(text):
        errors.append("full chronology has no timestamped segment")

    # --- Vocabulary checks ---
    for label in profile.get("evidence_labels", []):
        if f"`{label}`" not in text:
            errors.append(f"missing required evidence label: {label}")

    for term in profile.get("availability_vocabulary", []):
        if f"`{term}`" not in text:
            errors.append(f"missing required availability term: {term}")

    for status in profile.get("delta_statuses", []):
        if f"`{status}`" not in text:
            errors.append(f"missing required delta status: {status}")

    # --- Track coverage ---
    tracks = profile.get("tracks", [])
    if tracks and not all(track in text for track in tracks):
        errors.append("track assessment is incomplete")

    # --- Customer/demo separation ---
    if not re.search(r"客户.*(?:演示|demo)|(?:演示|demo).*客户", text, re.DOTALL | re.IGNORECASE):
        errors.append("customer claims and demonstrations are not explicitly separated")

    # --- Placeholder check ---
    if re.search(r"TODO|TBD|PLACEHOLDER|NXX|00:00:00–00:00:00", text, re.IGNORECASE):
        errors.append("placeholder text remains")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate domain analysis against a profile")
    parser.add_argument("analysis", type=Path, help="Path to the analysis markdown file")
    parser.add_argument("--profile", type=Path, required=True, help="Path to the domain profile YAML")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    errors = validate(args.analysis, profile)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    event_name = profile.get("meta", {}).get("event_name", "domain")
    print(f"PASS: {event_name} analysis satisfies the domain contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
