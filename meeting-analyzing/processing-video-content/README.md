# processing-video-content

Orchestrates the full media-to-analysis pipeline with explicit stage boundaries, validation gating, and recovery support. Delegates transcription and analysis to sub-skills; owns only orchestration and handoff validation.

## Stage graph

```
┌──────────┐     ┌──────────────────────┐     ┌──────────┐
│  Media   │ ──▶ │  Stage 1: transcript │ ──▶ │  Stage 2 │ ──▶ Domain
│  or      │     │  (video-to-text)     │     │  analysis│     overlay
│  existing │     └──────────────────────┘     │  (analy- │     (domain-
│  transcript│                                  │  zing-   │     analyzer)
└──────────┘                                   │  video-  │
                                                │  trans-  │
                                                │  cripts) │
                                                └──────────┘
```

## Recovery rules

- **Stage 1 valid, Stage 2 failed**: Do not retranscribe. Fix analysis and rerun Stage 2 validation.
- **Input hash changed**: Invalidate and rerun every downstream stage.
- **Partial output directory**: Inspect manifests, resume from first invalid/missing stage.

## Pipeline status schema

```json
{
  "input_route": "media | transcript",
  "stages": {
    "transcription": "complete",
    "analysis": "complete"
  },
  "validators": ["validate_transcript.py", "validate_video_analysis.py"],
  "audio_coverage_percent": 100,
  "outputs": ["transcript.md", "transcription-manifest.json", "video-analysis.md", "analysis-manifest.json"]
}
```

## References

- [handoff-contract.md](references/handoff-contract.md) — Full stage acceptance criteria and recovery
