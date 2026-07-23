#!/usr/bin/env python3
"""Chunk authorized media and transcribe it locally with auto-selected provider."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import time
import wave
from array import array
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from providers import resolve_provider


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def duration_seconds(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rms(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        samples = array("h")
        while data := handle.readframes(16000 * 30):
            samples.frombytes(data)
            if len(samples) > 16000 * 60:
                break
    if not samples:
        return 0.0
    return math.sqrt(sum(value * value for value in samples) / len(samples))


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "item"):
        return value.item()
    return str(value)


def anomalous(result: dict[str, Any], chunk_duration: float, audio_rms: float) -> list[str]:
    reasons: list[str] = []
    if not str(result.get("text", "")).strip() and audio_rms > 120:
        reasons.append("audible-audio-with-empty-text")
    previous = -1.0
    for segment in result.get("segments", []):
        start = float(segment.get("start", 0))
        end = float(segment.get("end", 0))
        if start < previous - 0.2 or end < start or end > chunk_duration + 1:
            reasons.append("timestamp-order-or-range")
        previous = max(previous, end)
        if float(segment.get("compression_ratio", 0) or 0) > 2.4:
            reasons.append("high-compression-ratio")
        if float(segment.get("avg_logprob", 0) or 0) < -1.2 and float(segment.get("no_speech_prob", 0) or 0) < 0.6:
            reasons.append("low-logprob")
    return sorted(set(reasons))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--authorized", action="store_true", help="Confirm rights to create a full transcript")
    parser.add_argument("--provider", default=None, help="Transcription provider name (default: auto-select best available)")
    parser.add_argument("--model", default=None, help="Override auto-tuned model")
    parser.add_argument("--review-model", default=None, help="Override auto-tuned review model")
    parser.add_argument("--language", default="auto")
    parser.add_argument("--initial-prompt", default=None)
    parser.add_argument("--chunk-seconds", type=float, default=None)
    parser.add_argument("--overlap-seconds", type=float, default=None)
    parser.add_argument("--cpu-workers", type=int, default=None)
    parser.add_argument("--require-gpu", action="store_true", help="Require a GPU-capable provider")
    parser.add_argument("--keep-audio-chunks", action="store_true")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    if not args.authorized and not args.plan_only:
        parser.error("--authorized is required for full verbatim transcription")

    provider, caps, tuned = resolve_provider(args.provider)

    if args.require_gpu and not caps.supports_gpu:
        raise SystemExit(
            "GPU is required but no GPU-capable provider is available. "
            "Install a GPU-backed provider (mlx on Apple Silicon, faster_whisper with CUDA) "
            "or omit --require-gpu to use CPU."
        )

    model = args.model or tuned.model
    review_model = args.review_model or tuned.review_model
    chunk_seconds = args.chunk_seconds or tuned.chunk_seconds
    overlap_seconds = args.overlap_seconds if args.overlap_seconds is not None else tuned.overlap_seconds
    cpu_workers = args.cpu_workers or tuned.cpu_workers

    if overlap_seconds < 0 or overlap_seconds >= chunk_seconds:
        parser.error("overlap must be non-negative and smaller than the chunk")
    if not args.input.exists():
        parser.error(f"input does not exist: {args.input}")

    total = duration_seconds(args.input)
    step = chunk_seconds - overlap_seconds
    starts = [index * step for index in range(math.ceil(max(total - overlap_seconds, 0.1) / step))]
    plan = [
        {"index": i, "start": start, "end": min(total, start + chunk_seconds)}
        for i, start in enumerate(starts)
        if start < total
    ]
    if args.plan_only:
        print(json.dumps({
            "duration_seconds": total,
            "provider": provider.name,
            "cpu_workers": cpu_workers,
            "chunks": plan,
        }, indent=2))
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    chunks_dir = args.output_dir / "chunks"
    raw_dir = args.output_dir / "raw"
    chunks_dir.mkdir(exist_ok=True)
    raw_dir.mkdir(exist_ok=True)
    manifest_path = args.output_dir / "transcription-manifest.json"
    previous_manifest: dict[str, Any] = {}
    if manifest_path.exists():
        try:
            previous_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous_manifest = {}

    started = time.time()
    gpu_backend = caps.gpu_backend or "cpu"
    manifest: dict[str, Any] = {
        "authorization_basis": "user-confirmed-rights",
        "input": str(args.input.resolve()),
        "input_sha256": sha256(args.input),
        "duration_seconds": total,
        "provider_name": provider.name,
        "device": gpu_backend,
        "architecture": platform.machine(),
        "cpu_workers": cpu_workers,
        "gpu_workers": tuned.gpu_workers,
        "model": model,
        "review_model": review_model,
        "chunk_seconds": chunk_seconds,
        "overlap_seconds": overlap_seconds,
        "chunks": [],
    }

    def extract(item: dict[str, Any]) -> Path | None:
        raw_path = raw_dir / f"chunk-{item['index']:04d}.json"
        if raw_path.exists():
            return None
        path = chunks_dir / f"chunk-{item['index']:04d}.wav"
        if not path.exists():
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", str(item["start"]), "-t", str(item["end"] - item["start"]),
                "-i", str(args.input), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(path),
            ])
        return path

    with ThreadPoolExecutor(max_workers=cpu_workers) as pool:
        audio_paths = list(pool.map(extract, plan))

    results: list[tuple[dict[str, Any], dict[str, Any]]] = []
    cache_hits = 0
    new_chunks = 0
    language = None if args.language == "auto" else args.language

    for item, audio_path in zip(plan, audio_paths):
        raw_path = raw_dir / f"chunk-{item['index']:04d}.json"
        if raw_path.exists():
            payload = json.loads(raw_path.read_text(encoding="utf-8"))
            cache_hits += 1
        else:
            if audio_path is None:
                raise RuntimeError(f"missing audio for uncached chunk {item['index']}")
            new_chunks += 1
            chunk_started = time.time()
            first = provider.transcribe(
                str(audio_path), model,
                language=language,
                initial_prompt=args.initial_prompt,
                word_timestamps=True,
            )
            first = json_safe(first)
            reasons = anomalous(first, item["end"] - item["start"], rms(audio_path))
            selected = first
            selected_model = model
            if reasons and review_model:
                reviewed = provider.transcribe(
                    str(audio_path), review_model,
                    language=language,
                    initial_prompt=args.initial_prompt,
                    word_timestamps=True,
                )
                selected = json_safe(reviewed)
                selected_model = review_model
            payload = {
                "chunk": item,
                "audio_sha256": sha256(audio_path),
                "audio_rms": rms(audio_path),
                "anomaly_reasons": reasons,
                "selected_model": selected_model,
                "elapsed_seconds": time.time() - chunk_started,
                "result": selected,
            }
            raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        results.append((item, payload))
        manifest["chunks"].append({
            **item,
            "raw_result": str(raw_path),
            "audio_sha256": payload.get("audio_sha256"),
            "selected_model": payload.get("selected_model"),
            "anomaly_reasons": payload.get("anomaly_reasons", []),
        })
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    merged: list[dict[str, Any]] = []
    detected_languages: list[str] = []
    for index, (item, payload) in enumerate(results):
        result = payload["result"]
        if result.get("language"):
            detected_languages.append(str(result["language"]))
        for segment in result.get("segments", []):
            absolute_start = item["start"] + float(segment.get("start", 0))
            absolute_end = item["start"] + float(segment.get("end", 0))
            merged.append({**segment, "start": absolute_start, "end": min(total, absolute_end), "chunk": item["index"]})

    source_language = max(set(detected_languages), key=detected_languages.count) if detected_languages else args.language
    elapsed = time.time() - started
    transcription_elapsed = sum(float(payload.get("elapsed_seconds", 0)) for _, payload in results)
    previous_peak = int(previous_manifest.get("peak_memory_bytes") or 0)
    manifest.update({
        "source_language": source_language,
        "coverage_start_seconds": 0,
        "coverage_end_seconds": total,
        "audio_coverage_percent": 100.0,
        "current_run_elapsed_seconds": elapsed,
        "transcription_elapsed_seconds": transcription_elapsed,
        "realtime_factor": transcription_elapsed / total if total else None,
        "peak_memory_bytes": previous_peak,
        "cache_hits": cache_hits,
        "new_chunks": new_chunks,
    })
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if not args.keep_audio_chunks and chunks_dir.exists():
        shutil.rmtree(chunks_dir)
    print(json.dumps({"manifest": str(manifest_path), "realtime_factor": manifest["realtime_factor"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
