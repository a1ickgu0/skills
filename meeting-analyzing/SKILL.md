---
name: meeting-analyzing
description: Route video/audio media or transcripts through a three-stage analysis pipeline (transcribe, analyze, domain overlay) orchestrated by a fourth component, with independently invocable stages. Use when the user wants end-to-end processing or needs to enter the pipeline at any intermediate stage.
---

# Meeting Analyzing

Convert authorized video/audio into timestamped transcripts, evidence-traceable content analysis, and optional domain-specific research overlays. Each stage is independently invocable — run the full pipeline or enter at any intermediate stage.

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

This skill is a routing entry point. It describes what the pipeline can do and which sub-skill handles each stage. For detailed orchestration logic — stage gating, manifest validation, recovery — see `processing-video-content/SKILL.md`.

## Usage modes

Each mode is triggered by what the user provides. All modes produce validated, manifest-tracked outputs that can resume from the last valid stage.

### 1. Full pipeline (media → domain analysis)

**User has**: an authorized video or audio file
**Trigger**: "Analyze this video", "Process this conference recording"
**Delegates to**: `processing-video-content`

Stages: transcribe → generic analysis → domain overlay. Use `--skip-domain` to stop after generic analysis.

### 2. Transcription only

**User has**: media, needs only a transcript
**Trigger**: "Transcribe this video"
**Delegates to**: `video-to-text`

Produces `transcript.md` + `transcription-manifest.json`. The output directory is ready for downstream analysis later.

### 3. Analysis from existing transcript

**User has**: a validated transcript directory (`transcript.md` + `transcription-manifest.json`)
**Trigger**: "Analyze this transcript"
**Delegates to**: `analyzing-video-transcripts` (or `processing-video-content` for full downstream pipeline including domain overlay)

Validates the existing transcript, then runs generic analysis. Optionally chain with domain overlay afterward.

### 4. Domain overlay only

**User has**: a validated `video-analysis.md` + a domain profile
**Trigger**: "Apply HPE Discover profile to this analysis"
**Delegates to**: `domain-analyzer`

Select the profile from `domain-analyzer/profiles/`, then apply domain-specific sections, vocabulary, evidence rules, and Task 1 delta analysis.

### 5. Cross-SKILL orchestration

**Caller**: another SKILL that produces media or transcripts
**Interface**: `processing-video-content` reads `references/handoff-contract.md` for stage contracts
**Trigger**: delegate to `processing-video-content` with media or transcript input
**Delegates to**: `processing-video-content`

Each stage declares its required inputs and outputs. Downstream stages validate upstream manifests before starting. Recovery resumes from the first invalid or missing stage.

## Sub-skill summary

| Skill | Role | Inputs | Outputs |
|-------|------|--------|---------|
| `video-to-text` | Transcribe media to timestamped transcript | Video/audio file | `transcript.md`, `transcription-manifest.json` |
| `analyzing-video-transcripts` | Generic evidence-traceable content analysis | Validated transcript + manifest | `video-analysis.md`, `analysis-manifest.json` |
| `domain-analyzer` | Vendor/event-specific research overlay | Validated generic analysis + YAML profile | Domain-annotated analysis |
| `processing-video-content` | Orchestration, stage gating, recovery | Media or existing transcript | Full pipeline with `pipeline-status.json` |

## Provider support matrix (video-to-text)

| Provider | Backend | Apple Silicon | CUDA GPU | CPU-only |
|----------|---------|---------------|----------|----------|
| `mlx` | Metal (Apple Silicon GPU) | Yes | No | No |
| `faster_whisper` | CTranslate2 (CUDA/CPU) | Yes | Yes | Yes |
| `cpu` | openai-whisper (fp32) | Yes | Yes | Yes |

Provider auto-selection: probe → pick best available → auto-tune model/workers/chunk size based on hardware.

## Adding a new domain profile

1. Copy an existing profile: `cp domain-analyzer/profiles/hpe-discover-networking.yaml domain-analyzer/profiles/my-event.yaml`
2. Fill in `meta`, `corpus`, `tracks`, `sections`, vocabulary lists, and `terminology`
3. Use it: `domain-analyzer` reads the profile and applies its rules
4. Validate: `python domain-analyzer/scripts/validate_domain_analysis.py --profile domain-analyzer/profiles/my-event.yaml <analysis.md>`

## Boundaries

- Do not bypass login, DRM, region locks, or access controls on media.
- Do not add vendor- or event-specific interpretation unless a domain profile supplies it as an explicit lens.
- Do not conceal missing coverage or substitute summaries for a verbatim transcript.
- Keep stage outputs so work can resume without re-running valid stages.
- Treat roadmap statements as future-looking; do not convert into current availability.
- Do not manufacture availability, performance, causality, intent, or competitive conclusions.
