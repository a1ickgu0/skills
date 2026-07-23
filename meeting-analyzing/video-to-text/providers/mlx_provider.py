"""MLX Whisper provider — Apple Silicon GPU (Metal) only."""

from __future__ import annotations

import os
import platform
from typing import Any

from .base import AbstractTranscriptionProvider, ProviderCapabilities, TunedConfig


class MLXProvider(AbstractTranscriptionProvider):
    @property
    def name(self) -> str:
        return "mlx"

    def probe(self) -> ProviderCapabilities:
        caps = ProviderCapabilities(
            name="mlx",
            supports_gpu=False,
            gpu_backend="metal",
            supports_cpu=False,
            platform_restrictions=["darwin-arm64"],
        )
        if platform.system() != "Darwin" or platform.machine() != "arm64":
            return caps
        try:
            import mlx.core as mx  # type: ignore
            device = str(mx.default_device())
            probe = mx.array([1.0, 2.0]) * 2
            mx.eval(probe)
            caps.supports_gpu = "gpu" in device.lower()
        except Exception:
            pass
        return caps

    def auto_tune(self, caps: ProviderCapabilities) -> TunedConfig:
        memory_gb: float = 16
        try:
            import mlx.core as mx  # type: ignore
            get_peak = getattr(mx, "get_peak_memory", None)
            if get_peak:
                memory_gb = float(get_peak()) / (1024**3)
        except Exception:
            pass
        try:
            total_mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
            memory_gb = max(memory_gb, total_mem / (1024**3))
        except Exception:
            pass

        cpu_count = os.cpu_count() or 4
        cpu_workers = max(1, cpu_count - 2)

        if memory_gb >= 16:
            return TunedConfig(
                model="mlx-community/whisper-large-v3-turbo",
                review_model="mlx-community/whisper-large-v3-mlx",
                gpu_workers=1,
                cpu_workers=min(cpu_workers, 6),
                chunk_seconds=900,
                overlap_seconds=5,
            )
        if memory_gb >= 8:
            return TunedConfig(
                model="mlx-community/whisper-large-v3-turbo",
                review_model="mlx-community/whisper-large-v3-mlx",
                gpu_workers=1,
                cpu_workers=min(cpu_workers, 4),
                chunk_seconds=600,
                overlap_seconds=5,
            )
        return TunedConfig(
            model="mlx-community/whisper-medium-mlx",
            review_model="mlx-community/whisper-large-v3-turbo",
            gpu_workers=1,
            cpu_workers=min(cpu_workers, 2),
            chunk_seconds=300,
            overlap_seconds=5,
        )

    def transcribe(
        self,
        audio_path: str,
        model: str,
        *,
        language: str | None = None,
        initial_prompt: str | None = None,
        word_timestamps: bool = True,
        verbose: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        import mlx_whisper  # type: ignore
        return mlx_whisper.transcribe(
            audio_path,
            path_or_hf_repo=model,
            language=language,
            initial_prompt=initial_prompt,
            word_timestamps=word_timestamps,
            verbose=verbose,
            **kwargs,
        )
