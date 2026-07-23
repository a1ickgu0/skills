"""FasterWhisper provider — CTranslate2 backend, CUDA GPU or CPU."""

from __future__ import annotations

import os
from typing import Any

from .base import AbstractTranscriptionProvider, ProviderCapabilities, TunedConfig


class FasterWhisperProvider(AbstractTranscriptionProvider):
    @property
    def name(self) -> str:
        return "faster_whisper"

    def probe(self) -> ProviderCapabilities:
        caps = ProviderCapabilities(
            name="faster_whisper",
            supports_gpu=False,
            gpu_backend="cuda",
            supports_cpu=True,
            platform_restrictions=[],
        )
        try:
            import torch  # type: ignore
            caps.supports_gpu = torch.cuda.is_available()
        except ImportError:
            pass
        return caps

    def auto_tune(self, caps: ProviderCapabilities) -> TunedConfig:
        cpu_count = os.cpu_count() or 4
        cpu_workers = max(1, cpu_count - 2)

        if caps.supports_gpu:
            memory_gb: float = 4
            try:
                import torch  # type: ignore
                props = torch.cuda.get_device_properties(0)
                memory_gb = props.total_memory / (1024**3)
            except Exception:
                pass

            if memory_gb >= 16:
                return TunedConfig(
                    model="large-v3",
                    review_model="large-v3",
                    gpu_workers=1,
                    cpu_workers=cpu_workers,
                    chunk_seconds=900,
                    overlap_seconds=5,
                )
            if memory_gb >= 8:
                return TunedConfig(
                    model="large-v3-turbo",
                    review_model="large-v3",
                    gpu_workers=1,
                    cpu_workers=cpu_workers,
                    chunk_seconds=600,
                    overlap_seconds=5,
                )
            return TunedConfig(
                model="medium",
                review_model="large-v3-turbo",
                gpu_workers=1,
                cpu_workers=cpu_workers,
                chunk_seconds=300,
                overlap_seconds=5,
            )

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
        from faster_whisper import WhisperModel  # type: ignore

        compute_type = kwargs.pop("compute_type", "float16")
        device = kwargs.pop("device", "cuda" if self.probe().supports_gpu else "cpu")
        cpu_threads = kwargs.pop("cpu_threads", os.cpu_count() or 4)

        fw_model = WhisperModel(model, device=device, compute_type=compute_type, cpu_threads=cpu_threads)
        segments, info = fw_model.transcribe(
            audio_path,
            language=language,
            initial_prompt=initial_prompt,
            word_timestamps=word_timestamps,
            **kwargs,
        )

        result_segments: list[dict[str, Any]] = []
        for segment in segments:
            words = []
            if segment.words:
                for w in segment.words:
                    words.append({
                        "word": w.word,
                        "start": w.start,
                        "end": w.end,
                        "probability": w.probability,
                    })
            result_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": words,
                "compression_ratio": getattr(segment, "compression_ratio", None),
                "avg_logprob": getattr(segment, "avg_logprob", None),
                "no_speech_prob": getattr(segment, "no_speech_prob", None),
            })

        return {
            "text": " ".join(s["text"] for s in result_segments),
            "segments": result_segments,
            "language": info.language,
            "language_probability": info.language_probability,
        }
