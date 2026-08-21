---
name: incose-reqs
description: "Analyze customer proposals, user stories, interview notes, pilot reports, product feedback, and acceptance materials using INCOSE requirements development; derive stakeholder and system requirements, business buying factors, verification methods, traceability, risks, and evidence-backed review conclusions."
metadata:
  short-description: "INCOSE requirements development and traceability"
  version: "0.1.0"
---

# INCOSE Requirements Engineering

## Output-language policy (mandatory)

The SKILL instructions are written in English, but the analysis output must use the customer's local language:

1. If the customer or source document has an explicit language, use that language.
2. If the source is multilingual, use the language of the primary audience or the language explicitly requested by the user.
3. If no language is specified, infer it from the dominant source language and customer context; ask only when the choice would materially affect acceptance or review.
4. Preserve short original-language quotations exactly, and add a concise translation only when the report language differs from the quotation language.
5. Do not translate product names, model numbers, identifiers, requirement IDs, URLs, or technical tokens.

The output-language decision must be stated in the opening summary, for example: `Output language: Chinese (customer/source language)`. The Chinese Emoi Hotel sample remains Chinese because its customer report and review context are Chinese.

## Opening executive close (must come first)

The first paragraph must be a standalone, citation-ready executive close covering scope, core business buying factors, key requirements, evidence coverage, unresolved risks, and recommended action. It must not introduce facts absent from the body and must include at least two original-language key quotations with precise locations, formatted as: `"Original quotation" — Source: section/subsection/table`.

## Purpose and boundaries

Convert natural-language customer material into requirements development results that are understandable, verifiable, traceable, and conservative about inference. Applicable inputs include customer proposals, user stories, interview notes, pilot summaries, bids, product feedback, and acceptance records. The SKILL analyzes and models; it does not approve a baseline, edit source documents, or contact external parties unless separately authorized.

## Input handling

Support pasted text, Markdown, extracted PDF text, local documents, Feishu Docx/Wiki links, and existing structured extraction results. Preserve the source title, link, revision/date, and stable location markers such as page, paragraph, heading, table, or block ID.

For documents containing images, tables, video, or embedded documents, use readable text first. If an artifact cannot be directly inspected, mark it as `not directly verifiable`; never treat an inferred image/video description as an original fact or fabricate a quotation.

## Evidence classification

Classify each statement before deriving a requirement:

| Code | Meaning | Treatment |
|---|---|---|
| OBS | Current state, measurement, or observed problem | Baseline/problem evidence |
| NEED | Explicit stakeholder need, goal, or constraint | Candidate stakeholder requirement |
| SOL | Product, architecture, model, configuration, or implementation | Design/solution constraint; not automatically a requirement |
| VER | Test, demonstration, operating data, or acceptance result | Verification evidence; assess coverage and limits |
| ISSUE | Pilot defect, failure, workaround, or known limitation | Risk, gap, or change candidate |
| ASSUMP | Analyst assumption or interpretation | Isolate and request confirmation |

Do not rewrite a model, topology, or cloud-management choice as a mandatory requirement unless the source explicitly makes it non-negotiable. Derive the underlying capability requirement and preserve the solution mapping.

## Mandatory original-quotation evidence

Every analytical statement must have source evidence. This includes the opening summary, table rows, scenarios, requirements, derivations, traceability conclusions, verification conclusions, risks, assumptions, priorities, and final conclusion.

- Every table must include an `Original key quotation` column; every row needs a short quotation and precise location.
- Put a quotation immediately after each paragraph-level conclusion. Mark derived content as `Derived` and cite the supporting source.
- Keep quotations faithful to the source. Do not present analyst paraphrases as quotations.
- For non-output-language sources, preserve the original quotation and add a concise translation.
- Quantities, thresholds, roles, and claims of verification must cite the source text containing that quantity or claim.
- If a conclusion depends on multiple sources, cite the 1–3 most material quotations.

## INCOSE requirements-development workflow

1. **Set scope and operational context**: record source, system boundary, organization/site, lifecycle phase, analysis date, output language, and decision question.
2. **Identify stakeholders and problem context**: distinguish users, operators, maintainers, decision makers, installers, service providers, affected people, and regulatory/safety roles.
3. **Build the baseline and ConOps threads**: describe trigger, action, system state, result, exception, and recovery for normal operation, deployment/migration, failure/recovery, and maintenance/upgrade when relevant.
4. **Extract stakeholder needs**: convert NEED/OBS/ISSUE into atomic candidate requirements while preserving uncertainty and quotations.
5. **Derive system requirements**: derive capability, performance, interface, constraint, operations, availability, security, and migration requirements; every derived requirement must trace upward.
6. **Separate solutions and decisions**: keep SOL content distinct, map requirement–solution–evidence, and identify design lock-in, open decisions, and technical debt.
7. **Define verification and acceptance**: select inspection, analysis, demonstration, or test; define object, conditions, thresholds, duration, sample, and pass criteria. If missing, create a verification question.
8. **Analyze business buying factors**: explain why the customer buys, the business value sought, the buying trigger, acceptable trade-offs, decision impact, metrics, solution mapping, and evidence. Rank by customer value and decision impact; distinguish explicit, derived, and to-be-confirmed factors.
9. **Run quality and completeness checks**: assess necessity, singularity, clarity, feasibility, verifiability, completeness, consistency, and traceability. Do not invent metrics, roles, boundaries, or compliance conclusions.
10. **Perform source validation after drafting**: return to the source and check every quotation, number, role, scenario, requirement source, coverage conclusion, risk, assumption, and final claim. Correct or remove unsupported content and record the result.
11. **Close the review**: state baseline candidates, unresolved gaps, risks, assumptions, decisions, customer questions, and next actions.

## Requirement-writing rules

Prefer: `The system shall/must + one capability or constraint + object/condition + verifiable threshold.` Each requirement expresses one primary claim. Convert vague terms such as better, stable, fast, seamless, convenient, or significant into confirmation questions; do not invent thresholds.

Use stable IDs: `BUY-xxx` (business buying factor), `SR-xxx` (stakeholder requirement), `SYS-xxx` (system requirement), `VER-xxx` (verification item), `ISS-xxx` (issue/risk), and `ASM-xxx` (assumption).

## Required output order

Follow [`references/requirements-schema.md`](references/requirements-schema.md) in this order:

1. Executive close (first);
2. Scope, sources, evidence levels, and output-language decision;
3. Customer-business core buying factors;
4. Stakeholders and role–goal–pain points;
5. Baseline and ConOps scenarios;
6. Candidate stakeholder requirements;
7. Derived system requirements;
8. Requirement–solution–verification traceability;
9. Verification/validation plan and acceptance gaps;
10. Conflicts, risks, assumptions, issues, decisions, and priorities;
11. Requirements quality review;
12. Original-source validation record;
13. Conclusion and next actions.

If the user asks for analysis only, label requirements as `candidate` or `to be baselined`; never present them as approved requirements.

## Completion gate

Before claiming completion, confirm that the report:

- uses the correct local output language and states the language decision;
- starts with a citation-ready executive close;
- includes business buying factors distinct from product models;
- separates NEED, SOL, VER, ISSUE, and ASSUMP;
- gives every analytical row/paragraph an original key quotation and location;
- gives every requirement a unique ID, source, and upstream trace;
- preserves test conditions, duration, sample, units, and thresholds for quantities;
- does not turn a pilot result into proof of full-system satisfaction;
- identifies uncovered roles, exception paths, interfaces, migration, and operations;
- includes the completed source-validation record;
- has no unsupported number, conclusion, priority, risk, or verification claim.

If source validation is incomplete, mark the report `Draft — source validation incomplete` and do not claim the analysis is complete.
