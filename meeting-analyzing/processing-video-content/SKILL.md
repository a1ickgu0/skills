---
name: processing-video-content
description: Orchestrate an authorized video or an existing validated transcript through reusable transcription and content-analysis stages. Use when the user wants an end-to-end, restartable media-to-transcript-to-analysis workflow with explicit stage contracts and validation.
---

# Processing Video Content

## Overview

Route inputs through the generic video-content pipeline. This skill owns orchestration, stage boundaries, recovery, and final validation; it does not duplicate transcription or analytical logic.

## Usage modes

Each stage is independently invocable. Combine them for a full pipeline or run a single stage in isolation:

1. **Full pipeline (media → domain analysis)**: Run Stage 1 + Stage 2 + optional domain overlay.
2. **Transcription only**: Run Stage 1 — produces `transcript.md` + `transcription-manifest.json`.
3. **Analysis only**: Start from an existing validated transcript — skip Stage 1.
4. **Domain overlay only**: Apply `domain-analyzer` with a profile to an existing validated analysis.

Use `--skip-domain` to run only the generic pipeline (transcribe + analyze) without a domain overlay.

## Route the input

- For video or audio input, run both stages in order.
- For an existing transcript, validate it and start at analysis.
- For a partially completed output directory, inspect manifests and resume from the first invalid or missing stage.

Read [references/handoff-contract.md](references/handoff-contract.md) before starting.

## Stage 1: transcript

**REQUIRED SUB-SKILL:** Use video-to-text

Require user-confirmed authorization before processing media. Stage 1 must finish with validated `transcript.md` and `transcription-manifest.json`. For non-Chinese speech, preserve original verbatim text and add Chinese translation; for Chinese speech, keep Chinese only.

Do not start analysis when Stage 1 coverage is below 100% or its validator fails.

## Stage 2: analysis

**REQUIRED SUB-SKILL:** Use analyzing-video-transcripts

Pass the validated transcript, transcription manifest, any optional OCR/background inputs, and the user's requested analytical lenses. Stage 2 must finish with validated `video-analysis.md` and `analysis-manifest.json`.

## Domain overlay (optional)

**SUB-SKILL:** Use domain-analyzer with a profile from `domain-analyzer/profiles/`

Apply a vendor/event-specific research lens on top of the generic analysis. Select the appropriate profile (e.g., `domain-analyzer/profiles/hpe-discover-networking.yaml`) and delegate to `domain-analyzer`. Skip this stage with `--skip-domain` when only generic analysis is needed.

## Final gate

Write `pipeline-status.json` with the input route, both stage states, validators run, audio coverage, and output paths. Run `scripts/validate_pipeline.py OUTPUT_DIR`. Repair the earliest failing stage and rerun downstream validation.

## Boundaries

- Do not add vendor- or event-specific interpretation unless a calling domain skill supplies it as an explicit lens and source set.
- Do not fetch or download protected media through bypass techniques.
- Do not conceal missing coverage or substitute summaries for a verbatim transcript.
- Keep stage outputs so work can resume without retranscribing valid chunks.
