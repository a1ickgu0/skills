---
name: analyzing-video-transcripts
description: Analyze a validated, timestamped video transcript into a complete evidence-traceable content report. Use after transcription when the user needs chronology, themes, mechanisms, claims, demonstrations, uncertainties, or requested analytical lenses without adding event- or vendor-specific assumptions.
---

# Analyzing Video Transcripts

## Language

All analysis instructions and templates are in English. Output language matches the user's language unless the user requests otherwise.

# Analyzing Video Transcripts

## Overview

Turn a complete validated transcript into a source-grounded analysis. Preserve the full chronology, distinguish speech from interpretation, and record the exact inputs used.

## Required inputs

Require:

- `transcript.md`, with ordered timestamp blocks and complete source-language coverage;
- `transcription-manifest.json`, declaring 100% audio coverage;
- optional OCR, background documents, and user-requested analytical lenses.

If the transcript or manifest fails its originating transcription contract, stop and return it for repair. Do not infer missing video content.

Read [references/analysis-contract.md](references/analysis-contract.md) and [references/evidence-rules.md](references/evidence-rules.md) before analysis.

## Workflow

1. Verify transcript coverage, timestamps, language, and manifest.
2. Hash every input used so the analysis can be reproduced.
3. Read the entire transcript before drafting conclusions.
4. Build the full chronology first; ensure every material segment appears.
5. Extract arguments, mechanisms, entities, named claims, metrics, demos, cases, uncertainties, and unanswered questions.
6. Apply evidence/status labels to every non-trivial claim.
7. Apply user-requested lenses only after the source-grounded analysis exists.
8. Write `video-analysis.md` using [assets/video-analysis-template.md](assets/video-analysis-template.md).
9. Write `analysis-manifest.json` with input paths, SHA-256 hashes, analytical lenses, generated time, and output hash.
10. Run `scripts/validate_video_analysis.py OUTPUT_DIR` and repair every error.

## Non-negotiable boundaries

- Do not treat analysis inference as speaker fact.
- Do not merge slide, demo, customer, or external-source evidence into speech without labels.
- Do not omit inconvenient, repetitive-but-material, uncertain, or contradictory portions.
- Do not manufacture availability, performance, causality, intent, or competitive conclusions.
- Preserve the source language in quoted evidence; translate only when useful and label translations.

## Outputs

Produce exactly:

- `video-analysis.md`
- `analysis-manifest.json`

This skill does not download media, transcribe audio, or impose a vendor-specific research framework.
