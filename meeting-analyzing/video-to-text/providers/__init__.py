"""Provider registry and auto-selection."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .base import AbstractTranscriptionProvider, ProviderCapabilities, TunedConfig
from .cpu_provider import CPUProvider
from .faster_whisper_provider import FasterWhisperProvider
from .mlx_provider import MLXProvider

_ALL_PROVIDERS: list[AbstractTranscriptionProvider] = [
    MLXProvider(),
    FasterWhisperProvider(),
    CPUProvider(),
]


def get_available_providers() -> list[tuple[AbstractTranscriptionProvider, ProviderCapabilities]]:
    """Return all providers that pass probe(), ordered by preference (GPU first, then CPU)."""
    available: list[tuple[AbstractTranscriptionProvider, ProviderCapabilities]] = []
    for provider in _ALL_PROVIDERS:
        caps = provider.probe()
        if caps.supports_gpu or caps.supports_cpu:
            available.append((provider, caps))
    # Sort: GPU-capable first, then CPU-only
    available.sort(key=lambda pair: (pair[1].supports_gpu, pair[0].name), reverse=True)
    return available


def resolve_provider(name: str | None = None) -> tuple[AbstractTranscriptionProvider, ProviderCapabilities, TunedConfig]:
    """Resolve a provider by name, or auto-select the best available.

    Returns (provider, capabilities, tuned_config).
    """
    available = get_available_providers()
    if not available:
        raise RuntimeError("No transcription provider is available on this system.")

    if name:
        for provider, caps in available:
            if provider.name == name:
                return provider, caps, provider.auto_tune(caps)
        raise ValueError(
            f"Provider '{name}' is not available. Available: {[p.name for p, _ in available]}"
        )

    # Auto-select: first available (already sorted by preference)
    provider, caps = available[0]
    return provider, caps, provider.auto_tune(caps)
