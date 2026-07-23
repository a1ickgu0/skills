#!/usr/bin/env python3
"""Report local CPU, memory, GPU and provider availability as JSON — cross-platform."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def run_text(command: list[str]) -> str | None:
    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
        return completed.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def total_memory_bytes() -> int | None:
    """Cross-platform total physical memory detection."""
    try:
        import psutil
        mem = psutil.virtual_memory()
        return mem.total
    except ImportError:
        pass
    # Fallbacks
    system = platform.system()
    try:
        if system == "Darwin":
            result = run_text(["sysctl", "-n", "hw.memsize"])
            if result and result.isdigit():
                return int(result)
        elif system == "Linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        return int(line.split()[1]) * 1024
        elif system == "Windows":
            result = run_text(["wmic", "computersystem", "get", "totalphysicalmemory"])
            if result:
                lines = result.strip().splitlines()
                if len(lines) > 1:
                    return int(lines[1].strip())
    except Exception:
        pass
    return None


def gpu_info() -> dict[str, object]:
    """Probe available GPU backends without importing heavy libraries upfront."""
    info: dict[str, object] = {
        "metal": probe_metal(),
        "cuda": probe_cuda(),
    }
    return info


def _is_apple_silicon() -> bool:
    """Return True on Apple Silicon hardware, even when Python runs under Rosetta 2."""
    if platform.system() != "Darwin":
        return False
    # sysctl hw.optional.arm64 returns 1 on native arm64 hardware regardless of
    # whether this process is translated via Rosetta 2.
    result = run_text(["sysctl", "-n", "hw.optional.arm64"])
    return result == "1"


def probe_metal() -> dict[str, object]:
    result: dict[str, object] = {"available": False}
    if not _is_apple_silicon():
        return result
    try:
        import mlx  # type: ignore # noqa: F401
        import mlx.core as mx  # type: ignore
        device = str(mx.default_device())
        probe = mx.array([1.0, 2.0]) * 2
        mx.eval(probe)
        result["available"] = "gpu" in device.lower()
        result["device"] = device
        get_peak = getattr(mx, "get_peak_memory", None)
        if get_peak:
            result["peak_memory_bytes"] = int(get_peak())
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def probe_cuda() -> dict[str, object]:
    result: dict[str, object] = {"available": False}
    try:
        import torch  # type: ignore
        result["torch_version"] = getattr(torch, "__version__", "unknown")
        result["available"] = torch.cuda.is_available()
        if result["available"]:
            result["device_count"] = torch.cuda.device_count()
            props = torch.cuda.get_device_properties(0)
            result["device_name"] = props.name
            result["total_memory_bytes"] = props.total_memory
    except ImportError:
        pass
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def probe_providers() -> dict[str, object]:
    """Probe which transcription providers are available."""
    result: dict[str, object] = {}
    # Add providers directory to path for import
    providers_dir = Path(__file__).resolve().parent.parent / "providers"
    if str(providers_dir.parent) not in sys.path:
        sys.path.insert(0, str(providers_dir.parent))
    try:
        from providers import get_available_providers
        available = get_available_providers()
        for provider, caps in available:
            result[provider.name] = {
                "available": True,
                "supports_gpu": caps.supports_gpu,
                "gpu_backend": caps.gpu_backend,
                "supports_cpu": caps.supports_cpu,
                "platform_restrictions": caps.platform_restrictions,
            }
        # Fill in known providers that didn't probe successfully
        known = {"mlx", "faster_whisper", "cpu"}
        for name in known:
            if name not in result:
                result[name] = {"available": False}
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-gpu", action="store_true", help="Exit non-zero if no GPU-capable provider is available")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    ffmpeg_version = run_text([ffmpeg, "-version"]) if ffmpeg else None
    mem_bytes = total_memory_bytes()
    runtime: dict[str, object] = {
        "platform": platform.platform(),
        "system": platform.system(),
        "architecture": platform.machine(),
        "cpu_logical": os.cpu_count(),
        "memory_bytes": mem_bytes,
        "memory_gb": round(mem_bytes / (1024**3), 1) if mem_bytes else None,
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "ffmpeg": {
            "path": ffmpeg,
            "version": ffmpeg_version.splitlines()[0] if ffmpeg_version else None,
        },
        "gpu": gpu_info(),
        "providers": probe_providers(),
    }
    try:
        runtime["disk_free_bytes"] = shutil.disk_usage(Path.cwd()).free
    except Exception:
        runtime["disk_free_bytes"] = None

    print(json.dumps(runtime, ensure_ascii=False, indent=2 if args.pretty else None))

    if args.require_gpu:
        has_gpu = False
        providers = runtime.get("providers", {})
        for info in providers.values():
            if isinstance(info, dict) and info.get("supports_gpu"):
                has_gpu = True
                break
        if not has_gpu:
            print(
                "GPU is required but no GPU-capable provider is available. "
                "Install a GPU-backed provider (mlx on Apple Silicon, faster_whisper with CUDA) "
                "or omit --require-gpu to use CPU.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
