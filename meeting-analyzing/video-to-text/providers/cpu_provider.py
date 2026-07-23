"""Pure CPU provider — openai-whisper with fp16=False. Works everywhere, no GPU required."""

from __future__ import annotations

import os
from typing import Any

from .base import AbstractTranscriptionProvider, ProviderCapabilities, TunedConfig


class CPUProvider(AbstractTranscriptionProvider):
    @property
    def name(self) -> str:
        return "cpu"

    def probe(self) -> ProviderCapabilities:
        caps = ProviderCapabilities(
            name="cpu",
            supports_gpu=False,
            gpu_backend=None,
            supports_cpu=True,
            platform_restrictions=[],
        )
        try:
            import whisper  # type: ignore # noqa: F401
        except ImportError:
            pass  # will still be available — probe is best-effort
        return caps

    def auto_tune(self, caps: ProviderCapabilities) -> TunedConfig:
        cpu_count = os.cpu_count() or 4
        cpu_workers = max(1, cpu_count - 2)
        return TunedConfig(
            model="small",
            review_model=None,
            gpu_workers=0,
            cpu_workers=cpu_workers,
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
        import whisper  # type: ignore

        whisper_model = whisper.load_model(model)
        result = whisper_model.transcribe(
            audio_path,
            language=language,
            initial_prompt=initial_prompt,
            word_timestamps=word_timestamps,
            verbose=verbose,
            fp16=False,
            **kwargs,
        )
        return result
