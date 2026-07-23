---
name: video-to-text
description: Use when authorized video or audio must be converted into a complete timestamped source-language transcript, with Chinese translation for non-Chinese speech, cross-platform GPU/CPU acceleration, checkpoint recovery, terminology correction, and coverage validation.
---

# Video to Text

## Core Principles

This skill is responsible only for media-to-text conversion — no thematic, strategic, or competitive analysis. Verify completeness by media time ranges; verbatim content, translations, runtime manifest, and anomaly records must all be traceable.

## Required Reading

Read in full before starting:

- `references/transcription-runtime.md`: cross-platform provider selection, auto-tuning, chunking, and recovery rules.
- `references/output-contract.md`: formal transcript and manifest contract.

Use `assets/transcript-template.md` to create the formal transcript.

## Provider Model

Transcription uses a pluggable provider architecture. The system auto-selects the best available provider:

| Provider | Backend | GPU | Platforms |
|---|---|---|---|
| `mlx` | MLX Whisper | Metal | Apple Silicon (arm64) |
| `faster_whisper` | CTranslate2 | CUDA | macOS, Linux, Windows |
| `cpu` | openai-whisper | None | All |

Run `python scripts/probe_runtime.py` to see which providers are available on the current machine. Use `--require-gpu` to require GPU acceleration, or omit it to allow CPU providers.

## Workflow

1. Record media source, authorization basis, source language, target translation language, and terminology glossary. Ask before proceeding if authorization is unclear.
2. Check for official transcript and player-embedded subtitle tracks; prefer them when available and verify completeness.
3. Run `python scripts/probe_runtime.py` to inspect available providers and hardware. The auto-tuned defaults (model, chunk size, worker count) are based on detected hardware tier.
4. Use `scripts/transcribe_local.py` to extract audio, chunk in parallel, transcribe via the selected provider, review anomalies, checkpoint, and deduplicate overlaps. Defaults are auto-tuned; override with `--provider`, `--model`, `--chunk-seconds`, etc. as needed.
5. Confirm 100% coverage from 0 seconds to media end by the union of chunk intervals; repair download, extraction, or decoding gaps.
6. Correct names, product names, model numbers, digits, and abbreviations using the glossary, visuals, and authorized references. When uncertain, retain `[inaudible HH:MM:SS]` or `[uncertain: candidate]`.
7. For non-Chinese media: write `Original` and `中文` blocks per chunk. For Chinese media: write `原文（中文）` blocks only. Never insert summaries or inferences into the transcript.
8. Run `python scripts/validate_transcript.py <output_dir>`. Only hand off to downstream analysis after all checks pass.

## Stop Conditions

- Do not bypass login, DRM, region locks, or access controls.
- When GPU is unavailable and `--require-gpu` was given, troubleshoot the provider installation before falling back to CPU.
- Do not claim completion when audio gaps, duration mismatches, or transcript validation failures exist.
