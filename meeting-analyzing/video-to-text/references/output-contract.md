# Video to Text Output Contract

Each media output directory must contain at minimum:

```text
<media-id>/
├── transcript.md
├── transcription-manifest.json
└── raw/*.json
```

## transcript.md

Frontmatter must include: `media_id`, `source_locator`, `source_language`, `translation_language`, `authorization_basis`, `duration_seconds`, `coverage_start_seconds`, `coverage_end_seconds`, `transcription_model`, `review_model`, `generated_at`.

For non-Chinese media, each chunk uses:

```markdown
### [00:00:00–00:00:20] Speaker

**Original**

Source-language verbatim text.

**中文**

中文翻译。
```

For Chinese media, each chunk uses `**原文（中文）**` and `translation_language` must be `none`.

The transcript must cover all meaningful speech. Translations preserve numbers, qualifiers, and tone. Summaries, factual corrections, and analytical inferences must not appear in the transcript body.

## transcription-manifest.json

Required fields: `provider_name`, `device` (one of `"metal"`, `"cuda"`, `"cpu"`), `architecture`, `input_sha256`, `duration_seconds`, `cpu_workers`, `gpu_workers`, `model`, `review_model`, `chunk_seconds`, `overlap_seconds`, per-chunk status with anomaly review records, `cache_hits`, `new_chunks`, `transcription_elapsed_seconds`, `realtime_factor`, `peak_memory_bytes`, `coverage_start_seconds`, `coverage_end_seconds`, and `audio_coverage_percent: 100`.

Optional fields: `diarization` (when speaker diarization was applied — records the diarization model and per-segment speaker labels).

Downstream consumers must only read transcripts after `validate_transcript.py` passes.
