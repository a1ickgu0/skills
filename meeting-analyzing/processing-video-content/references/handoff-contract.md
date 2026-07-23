# Pipeline handoff contract

## Stage graph

`authorized media -> video-to-text -> validated transcript -> analyzing-video-transcripts -> validated analysis`

An existing validated transcript may enter at the middle node.

## Stage 1 acceptance

Required files:

- `transcript.md`
- `transcription-manifest.json`

The transcription manifest must declare `audio_coverage_percent` of 100. The transcript must declare authorization, duration, full coverage, source language, model information, and timestamped content.

## Stage 2 acceptance

Required files:

- `video-analysis.md`
- `analysis-manifest.json`

The analysis manifest must identify and hash the transcript and transcription manifest, list analytical lenses, and hash `video-analysis.md`.

## Recovery

Manifests are checkpoints. If Stage 1 is valid, do not retranscribe merely because Stage 2 failed. If an input hash changes, invalidate and rerun every downstream stage that depended on it.

## Pipeline status

`pipeline-status.json` must contain:

- `input_route`: `media` or `transcript`;
- `stages.transcription` and `stages.analysis`: `complete` at final acceptance;
- `validators`: a non-empty array of validator names or commands;
- `audio_coverage_percent`: 100;
- `outputs`: all four stage deliverables.
