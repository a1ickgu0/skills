# Meeting Analyzing

Pipeline for transcribing, analyzing, and applying domain-specific research frameworks to conference videos and transcripts. Supports HPE Discover, Cisco Live, IETF Meeting, and any other event via configurable YAML profiles.

```
authorized media
       │
       ▼
┌─────────────────┐
│  video-to-text  │  →  transcript.md + transcription-manifest.json
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  analyzing-video-     │  →  video-analysis.md + analysis-manifest.json
│  transcripts          │
└────────┬─────────────┘
         │
         ▼ (optional)
┌─────────────────┐
│ domain-analyzer │  →  domain-specific overlay on top of generic analysis
└─────────────────┘

        orchestrated by
┌──────────────────────────┐
│ processing-video-content │
└──────────────────────────┘
```

## Sub-skill summary

| Skill | Role | Inputs | Outputs |
|-------|------|--------|---------|
| `video-to-text` | Transcribe media to timestamped transcript | Video/audio file | `transcript.md`, `transcription-manifest.json` |
| `analyzing-video-transcripts` | Generic evidence-traceable content analysis | Validated transcript + manifest | `video-analysis.md`, `analysis-manifest.json` |
| `domain-analyzer` | Vendor/event-specific research overlay | Validated generic analysis + YAML profile | Domain-annotated analysis |
| `processing-video-content` | Orchestration, stage gating, recovery | Media or existing transcript | Full pipeline with `pipeline-status.json` |

## Usage modes

1. **Full pipeline**: `processing-video-content` orchestrates media → transcript → analysis → domain overlay
2. **Transcription only**: `video-to-text` produces transcript + manifest from media
3. **Analysis only**: `analyzing-video-transcripts` from an existing validated transcript
4. **Domain overlay only**: `domain-analyzer` with a profile applied to existing analysis

## Provider support matrix (video-to-text)

| Provider | Backend | Apple Silicon | CUDA GPU | CPU-only |
|----------|---------|---------------|----------|----------|
| `mlx` | Metal (Apple Silicon GPU) | Yes | No | No |
| `faster_whisper` | CTranslate2 (CUDA/CPU) | Yes | Yes | Yes |
| `cpu` | openai-whisper (fp32) | Yes | Yes | Yes |

Provider auto-selection: probe → pick best available → auto-tune model/workers/chunk size based on hardware.

## Adding a new domain profile

1. Copy the example profile: `cp domain-analyzer/profiles/hpe-discover-networking.yaml domain-analyzer/profiles/my-event.yaml`
2. Fill in `meta`, `corpus`, `tracks`, `sections`, vocabulary lists, and `terminology`
3. Use it: `domain-analyzer` reads the profile and applies its rules
4. Validate: `validate_domain_analysis.py --profile domain-analyzer/profiles/my-event.yaml <analysis.md>`
