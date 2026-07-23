#!/usr/bin/env python3
"""Tests for cross-platform probe_runtime.py hardware detection."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROBE_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "probe_runtime.py"


def run_probe(*args: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(PROBE_SCRIPT), *args],
        capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def test_probe_outputs_required_keys():
    runtime = run_probe()
    for key in ("platform", "system", "architecture", "cpu_logical", "memory_bytes",
                "python", "ffmpeg", "gpu", "providers"):
        assert key in runtime, f"missing key: {key}"


def test_gpu_section_has_metal_and_cuda():
    runtime = run_probe()
    gpu = runtime["gpu"]
    assert "metal" in gpu, "missing gpu.metal"
    assert "cuda" in gpu, "missing gpu.cuda"


def test_providers_section_populated():
    runtime = run_probe()
    providers = runtime["providers"]
    assert isinstance(providers, dict), "providers must be a dict"
    # At least the cpu provider should be reported
    assert len(providers) >= 1, "expected at least one provider"


def test_cpu_provider_reported():
    runtime = run_probe()
    providers = runtime["providers"]
    assert "cpu" in providers, "cpu provider must always be reported"


def test_memory_bytes_is_positive():
    runtime = run_probe()
    assert runtime["memory_bytes"] is None or runtime["memory_bytes"] > 0


def test_cpu_logical_is_positive():
    runtime = run_probe()
    assert runtime["cpu_logical"] is not None
    assert runtime["cpu_logical"] > 0


def test_probe_pretty_flag():
    result = subprocess.run(
        [sys.executable, str(PROBE_SCRIPT), "--pretty"],
        capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    assert "providers" in data


def test_probe_require_gpu_reports_status():
    result = subprocess.run(
        [sys.executable, str(PROBE_SCRIPT), "--require-gpu"],
        capture_output=True, text=True,
    )
    # Exit code 0 means GPU found; exit code 2 means no GPU (still valid output)
    assert result.returncode in (0, 2), f"unexpected exit code: {result.returncode}"
    if result.returncode == 0:
        data = json.loads(result.stdout)
        providers = data.get("providers", {})
        has_gpu = any(
            isinstance(info, dict) and info.get("supports_gpu")
            for info in providers.values()
        )
        assert has_gpu, "require-gpu passed but no GPU-capable provider found"


def test_system_is_darwin():
    runtime = run_probe()
    assert runtime["system"] == "Darwin", "expected macOS (Darwin)"
