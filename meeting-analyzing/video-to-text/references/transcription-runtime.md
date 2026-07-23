# Local Transcription Runtime Specification

## 1. Objective

Maximize utilization of local GPU, CPU, and memory without sacrificing accuracy. Acceptance criteria: the selected provider is actually active, models are reused across chunks, CPU/GPU pipelining is parallel, realtime factor and peak memory are recorded. Blind pursuit of multiple GPU processes or 100% utilization is not the goal.

## 2. Provider Selection

The system auto-selects the best available provider by probing each candidate:

1. **MLX** (`mlx`): Apple Silicon only (darwin-arm64). Uses Metal GPU via `mlx_whisper`. Selected when `import mlx` and `import mlx_whisper` succeed and a Metal GPU device is detected.
2. **FasterWhisper** (`faster_whisper`): Cross-platform. Uses CTranslate2 with CUDA GPU when available, falls back to CPU. Selected when `import faster_whisper` succeeds.
3. **CPU** (`cpu`): Universal fallback. Uses `openai-whisper` with `fp16=False`. Always available as last resort.

Run `python scripts/probe_runtime.py` to see which providers are available:

```bash
python scripts/probe_runtime.py --pretty
```

Use `--require-gpu` to fail when no GPU-capable provider is available:

```bash
python scripts/probe_runtime.py --require-gpu
```

When a GPU-capable provider is unavailable and the task requires GPU, troubleshoot the provider installation before falling back. CPU is a first-class path — no user confirmation needed for CPU transcription when `--require-gpu` is not set.

## 3. Auto-Tuned Defaults

Hardware tiers are defined in `scripts/provider_config.yaml`. The provider's `auto_tune()` picks the best tier based on available resources:

| Tier | Condition | Model | Review Model | Chunk |
|---|---|---|---|---|
| High GPU | ≥ 16 GB VRAM/unified | large-v3 | large-v3 | 900 s |
| Mid GPU | ≥ 8 GB | large-v3-turbo | large-v3 | 600 s |
| Low GPU | ≥ 4 GB | medium | large-v3-turbo | 300 s |
| CPU Only | N/A | small | none | 300 s |

All tiers use 5-second chunk overlap. CPU workers default to `max(1, cpu_count - 2)`. GPU workers default to 1 (avoids contention). Model names may vary by provider; the actual value is recorded in the manifest.

Override any auto-tuned value with the corresponding CLI flag: `--model`, `--review-model`, `--chunk-seconds`, `--overlap-seconds`, `--cpu-workers`.

## 4. CPU/GPU Pipeline

1. CPU workers extract and normalize audio chunks in parallel.
2. A single GPU process holds the model and transcribes chunks sequentially; the provider reuses loaded models across chunks.
3. CPU workers inspect completed JSON, timestamps, duplicates, terminology, and anomaly metrics while GPU processes subsequent chunks.
4. Anomalous chunks are queued for GPU review with the review model — no second parallel model instance is started.
5. The manifest is atomically updated after each chunk, enabling resume from interruption.

## 5. Anomalies and Review

Review is triggered when any of these conditions is met:

- Audible audio but empty text output;
- Timestamps out of order, out of range, or anomalously overlapping;
- `compression_ratio > 2.4`;
- `avg_logprob < -1.2` with non-silence;
- Consecutive repeated phrases indicating model looping;
- Model numbers, names, digits conflicting with official materials or visuals;
- Chunk boundary unclosed sentences with inconsistent overlap results.

Review uses the higher-precision review model. When a provider has no review model (e.g., CPU tier), anomalous chunks are flagged but not re-transcribed. When still uncertain after review, write `uncertain` — do not substitute plausible-seeming words.

## 6. Completeness

- Check coverage by the union of audio chunk intervals, not by ASR text presence.
- Coverage must span from 0 seconds to total media duration; the final partial chunk is acceptable.
- No positive gaps between chunks; overlap regions are deduplicated by timestamp and text similarity.
- Download gaps, corrupt chunks, and re-run segments are logged with reason and resolution.

## 7. Runtime Record

The manifest records at minimum: provider name, device backend, CPU workers, GPU workers, model, review model, chunk seconds, overlap seconds, total duration, wall-clock elapsed, realtime factor, peak memory, re-run chunks, and audio coverage percentage.
