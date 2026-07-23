---
name: domain-analyzer
description: Apply a domain-specific research lens on top of generic video analysis. Use when you need vendor/event-specific product, strategy, availability, customer, demo, evidence, and page-layer delta analysis. Configure via profiles in profiles/ for your event (HPE Discover, Cisco Live, IETF Meeting, etc.).
---

# Domain Analyzer

## Overview

Apply a domain-specific research framework to video analysis content while preserving generic transcription and evidence contracts. This skill owns domain interpretation — vendor/product terminology, research tracks, availability classification, and page-layer delta analysis — not media transcription or generic analysis mechanics.

## How to use

### For a full pipeline run

Delegate transcription and generic analysis to `processing-video-content`, then apply the domain overlay by invoking this skill with the appropriate profile:

1. Select the profile matching your event/vendor from `profiles/` (e.g., `profiles/hpe-discover-networking.yaml`).
2. Read the profile to understand the corpus structure, tracks, sections, vocabulary, and rules.
3. For each item, read the corresponding Task 1 page record and track files.
4. Apply the domain overlay to the generic video analysis, adding profile-configured sections.

### For domain overlay on existing analysis

If you already have a validated generic video analysis, apply the domain overlay directly:

1. Select the appropriate profile from `profiles/`.
2. Read the existing `video-analysis.md` and its manifest.
3. Add the profile-configured sections, vocabulary, and delta analysis.
4. Validate with `scripts/validate_domain_analysis.py --profile <profile.yaml> <analysis.md>`.

## Required source set

For each item, read the profile to determine the corpus structure. Typically:

1. Map the item to its identifier in the corpus (e.g., `N01`–`N22` for HPE Discover Networking).
2. Read the corresponding Task 1 page record completely.
3. Read the relevant track and analysis files from the configured directories.
4. Use official event/vendor sources for cross-checking; record every source.

Read [references/domain-research-contract.md](references/domain-research-contract.md) and [references/domain-terminology.md](references/domain-terminology.md) for the generic framework. The profile supplies the concrete vocabulary, tracks, and sections.

## Domain-specific rules (profile-driven)

The profile configures:

- **Sections**: The required analysis section headers.
- **Tracks**: Research tracks to assess (applicable / not applicable / unsupported).
- **Availability vocabulary**: Terms for classifying capability availability.
- **Delta statuses**: Terms for comparing video against the page layer.
- **Evidence labels**: Labels for classifying evidence type.
- **Terminology**: Brand names, naming conventions, and spelling rules.
- **Additional rules**: Evidence separation, customer/demo separation, metrics precision, future-looking treatment, etc.

Core rules that apply across all profiles:

- Separate what the speaker says from official cross-checks and analyst inference.
- Classify each capability independently using the profile's availability vocabulary.
- Keep customer production claims separate from demonstrations and hypothetical examples.
- Preserve exact qualifiers, dates, units, denominators, and scope for metrics.
- Compare video against the page layer explicitly using the profile's delta statuses.
- Cover all applicable research tracks and explicitly mark non-applicable tracks.
- Treat roadmap statements as future-looking; do not convert into current availability.

## Output and validation

For new runs, store output in the directory configured by the profile's `corpus.output_dir_pattern`. Keep all transcript and analysis artifacts together.

Run `scripts/validate_domain_analysis.py --profile <profile.yaml> <ANALYSIS_MD>`. Repair every validation error before marking the item complete.
