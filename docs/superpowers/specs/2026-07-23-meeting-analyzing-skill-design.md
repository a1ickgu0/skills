# Meeting Analyzing SKILL — Design Spec

## Overview

Create the top-level `meeting-analyzing/SKILL.md` that serves as a thin routing entry point into the existing four-stage video-content analysis pipeline. The skill describes what the pipeline can do and which sub-skill handles each stage, without duplicating the orchestration logic already defined in `processing-video-content/SKILL.md`.

## Architecture

```
meeting-analyzing/SKILL.md  ← NEW (routing entry point)
    │
    ├── video-to-text/SKILL.md
    ├── analyzing-video-transcripts/SKILL.md
    ├── domain-analyzer/SKILL.md
    └── processing-video-content/SKILL.md  (orchestration owner)
```

**Key decision**: `meeting-analyzing/SKILL.md` is a routing facade. It does NOT duplicate stage gating, manifest validation, or recovery logic. Users needing orchestration details are directed to `processing-video-content/SKILL.md`.

## Content structure

| Section | Purpose |
|---------|---------|
| Frontmatter + overview | Skill identity, pipeline diagram, routing disclaimer |
| Usage modes (5) | Each mode: user context, trigger phrases, delegation target |
| Sub-skill summary table | Quick reference: skill, role, inputs, outputs |
| Provider support matrix | Hardware/provider compatibility for transcription |
| Adding a new domain profile | 4-step guide |
| Boundaries | Non-negotiable constraints (cross-cutting across all stages) |

## Usage modes covered

1. **Full pipeline** — media → transcript → analysis → domain overlay (delegates to `processing-video-content`)
2. **Transcription only** — media → transcript (delegates to `video-to-text`)
3. **Analysis from existing transcript** — transcript → generic analysis → optional domain overlay (delegates to `analyzing-video-transcripts` or `processing-video-content`)
4. **Domain overlay only** — existing analysis + profile → domain-annotated analysis (delegates to `domain-analyzer`)
5. **Cross-SKILL orchestration** — called by another SKILL via `processing-video-content`'s handoff contract

## Design principles

- **No logic duplication**: Routing only; orchestration lives in `processing-video-content`
- **Self-describing entries**: Each mode states what the user has, what triggers it, and which sub-skill handles it
- **Independent stages**: Every stage is independently invocable; outputs are manifest-tracked for resume
- **Consistent conventions**: Follows existing repo structure (frontmatter, table format, ASCII diagrams)

## What this does NOT include

- Stage gating, manifest validation, or recovery rules (owned by `processing-video-content`)
- Transcription provider implementation details (owned by `video-to-text`)
- Evidence rules or analysis templates (owned by `analyzing-video-transcripts`)
- Domain profile schema or terminology rules (owned by `domain-analyzer`)
