"""Abstract base class and data structures for transcription providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ProviderCapabilities:
    name: str
    supports_gpu: bool = False
    gpu_backend: str | None = None  # "metal", "cuda", "vulkan"
    supports_cpu: bool = True
    platform_restrictions: list[str] = field(default_factory=list)  # "darwin-arm64", etc.


@dataclass
class TunedConfig:
    model: str
    review_model: str | None
    gpu_workers: int = 1
    cpu_workers: int = 4
    chunk_seconds: int = 900
    overlap_seconds: int = 5


class AbstractTranscriptionProvider(ABC):
    """Provider interface for local transcription backends."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def probe(self) -> ProviderCapabilities:
        """Detect whether this provider is available on the current system."""
        ...

    @abstractmethod
    def auto_tune(self, caps: ProviderCapabilities) -> TunedConfig:
        """Select model and concurrency settings based on hardware capabilities."""
        ...

    @abstractmethod
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
        """Run transcription on a single audio file. Returns the raw result dict."""
        ...
