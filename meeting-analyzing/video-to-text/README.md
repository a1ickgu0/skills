# video-to-text

Cross-platform media transcription with dynamic hardware adaptation. Auto-detects the best available provider and tunes model size, workers, and chunking to the hardware.

## Platform support

| Provider | Backend | Platforms | GPU | CPU |
|----------|---------|-----------|-----|-----|
| `mlx` | Metal | macOS arm64 | Yes | No |
| `faster_whisper` | CTranslate2 | macOS, Linux, Windows | CUDA | Yes |
| `cpu` | openai-whisper | macOS, Linux, Windows | No | Yes |

## Quick start

```bash
# Auto-detect best provider
python scripts/transcribe_local.py input.mp4 output_dir/

# Require GPU-capable provider
python scripts/transcribe_local.py --require-gpu input.mp4 output_dir/

# Explicit provider
python scripts/transcribe_local.py --provider faster_whisper input.mp4 output_dir/

# Optional speaker diarization (post-processing)
python scripts/speaker_diarize.py output_dir/ input.mp4 --hf-token <token>

# Validate transcript
python scripts/validate_transcript.py output_dir/
```

## Auto-tuning

Hardware tier determines model and chunk size automatically:

| Tier | Condition | Model | Chunk |
|------|-----------|-------|-------|
| High GPU | ≥16 GB VRAM | large-v3 | 900s |
| Mid GPU | ≥8 GB VRAM | large-v3-turbo | 600s |
| Low GPU | <8 GB VRAM | medium | 300s |
| CPU only | No GPU | small | 300s |

## Output structure

```
output_dir/
├── transcript.md                  # Timestamp-blocked transcript
├── transcription-manifest.json    # Model, coverage, provider metadata
```

## References

- [transcription-runtime.md](references/transcription-runtime.md) — Provider selection and auto-tuning details
- [output-contract.md](references/output-contract.md) — Manifest and transcript format specification
