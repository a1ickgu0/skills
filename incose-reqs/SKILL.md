---
name: incose-reqs
description: "Analyze customer proposals, user stories, interview notes, pilot reports, product feedback, and acceptance materials using INCOSE requirements development; derive stakeholder and system requirements, business buying factors, verification methods, traceability, risks, and evidence-backed review conclusions."
metadata:
  short-description: "INCOSE requirements development and traceability"
  version: "0.3.2"
---

# INCOSE Requirements Engineering

## Output-language policy (mandatory)

The SKILL instructions are written in English, but the analysis output must use the customer's local language:

1. If the customer or source document has an explicit language, use that language.
2. If the source is multilingual, use the language of the primary audience or the language explicitly requested by the user.
3. If no language is specified, infer it from the dominant source language and customer context; ask only when the choice would materially affect acceptance or review.
4. Preserve short original-language quotations exactly, and add a concise translation only when the report language differs from the quotation language.
5. Do not translate product names, model numbers, identifiers, requirement IDs, URLs, or technical tokens.
6. This policy governs every user-facing part of the deliverable: the three-dimension key summary, executive close, all tables, requirement statements, verification plans, conclusions, and generated filenames.

The output-language decision must be stated in the opening summary, for example: `Output language: Chinese (customer/source language)`. The worked sample in `references/requirements-schema.md` §-1 is an English rendering of a Chinese-customer case; real output always follows the policy above.

## Generated filename convention

When the analysis is saved as a file, the filename must start with the skill-name prefix rendered in the output language (see Output-language policy): `INCOSE 需求工程分析：` for Chinese output, `INCOSE Requirements Engineering Analysis:` for English output, or the equivalent translation for any other output language. Append a concise customer or source-document title and the appropriate extension, for example: `INCOSE 需求工程分析：<customer-or-document-title>.docx` or `INCOSE Requirements Engineering Analysis: <customer-or-document-title>.docx`. Keep the prefix uniform across reports in the same language, including its spacing and colon style (full-width colon for Chinese, half-width for English). Sanitize only characters that are invalid for the target filesystem; do not remove or reorder the prefix, and do not mix languages within it.

## Opening executive close (leads the report body)

The executive close must be a standalone, citation-ready paragraph covering scope, core business buying factors, key requirements, evidence coverage, unresolved risks, and recommended action. It directly follows the three-dimension key summary. It must not introduce facts absent from the body and must include at least two original-language key quotations with precise locations, formatted as: `"Original quotation" — Source: section/subsection/table`.

## Three-dimension key summary

Always produce a concise, decision-oriented three-dimension key summary for sales, presales, and customer decision makers. It is the mandatory first section of every report and precedes the executive close. It may also be produced standalone when the user asks for only a summary, snapshot, or brief.

The summary must explain the customer's business situation, not merely restate technical facts. Build each bullet through this chain where evidence permits: **customer/business context → concrete operating scenario → observed problem or change → business impact → customer need or decision implication**. Do not force every bullet to contain every link, but do not leave technical symptoms without explaining whom or what business outcome they affect.

The three dimensions, in fixed order:

1. **Customer background** — describe the customer's business identity and operating model: what the organization does, which customer segments or users matter, what service or business promise they must deliver, the scale and quantified context that affects demand, how operations are staffed or outsourced, and what current business initiative raises the stakes. Preserve decision-relevant numbers, dates, durations, capacities, locations, and response times. Do not reduce them to vague qualitative terms.
2. **Business needs** — explain what the customer needs to change in the business or operating experience. Connect concrete current-state conditions to affected users, scenarios, and consequences: for example, an observed service interruption to a customer-facing experience, a capacity limit to an expansion constraint, or a slow support response to operational exposure. State the desired business or operational result. Technical facts may appear as evidence, but the bullet must not stop at a device, topology, or feature description.
3. **Buying factors** — explain why the customer would buy now and how the customer will judge value. State the business outcome protected or created, the risk/cost avoided or decision pressure, the concrete evidence or metric that makes it material, and any important trade-off or evolution requirement. If a product, architecture, or model is mentioned, present it only as a solution mapping to the buying factor, never as the buying factor itself. Rank only when the source or explicit analysis supports the ranking; otherwise mark priority as to be confirmed.

### Conciseness and evidence rules

- Use 2–4 compact bullets per dimension when the evidence supports them; do not force a fixed total if doing so would remove a material fact or business causal link.
- Keep each bullet focused on one business thread. Use a short, information-dense sentence or two short linked clauses rather than a vague slogan.
- Preserve source quantities exactly, including units, ranges, dates, counts, locations, durations, costs, thresholds, and response times. Never replace a decision-relevant quantity with a qualitative adjective.
- Every bullet must include an inline source quotation and precise location, for example: `("Original quotation" — Source: Section 2/Table 1)`. If the content is derived or uncertain, label it `Derived` or `To be confirmed` beside the evidence.
- Do not use a table, requirement ID, or separate citation block in this opening summary. Detailed traceability belongs in later sections.
- Keep the customer's own wording for pain points and business outcomes where possible. Do not invent complaints, revenue loss, churn, reviews, savings, service levels, or other business consequences that the source does not state; mark them as derived or to be confirmed.

### Desensitization note

The worked sample in [`references/requirements-schema.md`](references/requirements-schema.md) §-1 is desensitized (generic terms in place of the real name, model, and price); that applies to the sample only. The real report must preserve customer names, model numbers, prices, and locations exactly as in the source — do not desensitize actual output.

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

1. Three-dimension key summary (mandatory first section);
2. Executive close (always present; first prose section after the key summary);
3. Scope, sources, evidence levels, and output-language decision;
4. Customer-business core buying factors;
5. Stakeholders and role–goal–pain points;
6. Baseline and ConOps scenarios;
7. Candidate stakeholder requirements;
8. Derived system requirements;
9. Requirement–solution–verification traceability;
10. Verification/validation plan and acceptance gaps;
11. Conflicts, risks, assumptions, issues, decisions, and priorities;
12. Requirements quality review;
13. Original-source validation record;
14. Conclusion and next actions.

If the user asks for analysis only, label requirements as `candidate` or `to be baselined`; never present them as approved requirements.

## Completion gate

Before claiming completion, confirm that the report:

- uses the correct local output language and states the language decision;
- uses a filename whose prefix matches the output language (`INCOSE 需求工程分析：` for Chinese, `INCOSE Requirements Engineering Analysis:` for English) whenever a file is generated;
- opens with the mandatory three-dimension key summary: exactly three sections in order, concise but quantitatively faithful, traceable to source, and NOT desensitized;
- follows it with the citation-ready executive close;
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
