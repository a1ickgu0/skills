---
name: incose-reqs
description: "Analyze customer proposals, user stories, interview notes, pilot reports, product feedback, and acceptance materials using INCOSE requirements development; derive stakeholder and system requirements, business buying factors, verification methods, traceability, risks, and evidence-backed review conclusions."
metadata:
  short-description: "INCOSE requirements development and traceability"
  version: "0.2.0"
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

## Three-dimension key summary (三维度关键综述)

Optionally produce a concise, scannable three-dimension key summary — a one-screen executive snapshot for sales / presales / decision context. Produce it when the user asks for a summary, snapshot, or brief; otherwise skip it. It may stand alone or precede the full report.

The three dimensions, in fixed order:

1. **客户背景 (Customer background)** — who the customer is and their operating context: industry/type and scale; key customer segments and their defining need; IT staffing / operating model and its constraint; any strategic initiative that raises the stakes. 2–4 bullets, one fact-cluster per bullet.
2. **问题诉求 (Pain points / problems)** — the as-is state and gap, made concrete. First state what the current situation IS (existing equipment, current architecture, current operating/outsourcing model, current coverage or performance), then point out the specific problem each condition produces. Do NOT stop at abstract environment parameters (e.g. "high racks, 8m ceiling", "long corridors") — name the concrete pain each produces (coverage holes, roaming drops, port exhaustion, slow response). Describe problems, not solutions. 2–4 bullets.
3. **购买要素 (Buying factors)** — the business essence of WHY the customer buys, stated from the customer's own business perspective: what business outcome, risk removed, cost avoided, or strategic position the customer is really purchasing — not what products/boxes they bought. Each bullet carries a concrete, checkable fact. 2–4 bullets, ranked by customer value and decision impact. Ban empty rhetoric: no phrases like "这是命脉", "最痛的一环", "重中之重", or any wording that adds emphasis without information — every bullet must state a real business motivation.

### Conciseness rules

- Target 9–12 bullets total; one sentence per bullet; strip adjectives and repetition.
- No tables, no requirement IDs, no citation block.
- Every bullet must be traceable to the source material; keep the customer's own phrasing for pain points, lightly normalized.

### Desensitization note

The worked sample below is desensitized (generic terms in place of the real name, model, and price). This applies only to the sample embedded in this SKILL. The real report must preserve customer names, model numbers, prices, and locations exactly as in the source — do not desensitize actual output.

### Worked sample (desensitized)

**客户背景：**
- 某旅游城市一家近年开业的高端酒店，数十间客房，客群以长住商务与数字游民为主，对稳定高速网络有刚性需求。
- 无专职 IT，网络运维长期外包（月费制），白天响应慢、夜间故障次日处理。
- 正将公共休息区改造为共享办公空间，作为差异化卖点。

**问题诉求：** 现网为千兆铜缆 + WiFi 5「一拖二房」，问题突出
- 房间覆盖不均、走廊无 AP 导致漫游断连，大堂高并发下频繁断线重连
- 接入交换机端口耗尽，无法扩容
- 运维依赖外包，响应迟缓

**购买要素：**
- 保住住客口碑与营收：住客因网络差而投诉、差评、退房，直接影响酒店收入
- 摆脱对外包运维的被动依赖：故障响应从「次日」变为可掌控、可自运维
- 为差异化卖点铺路：共享办公空间需要一张撑得起未来客群的网络底盘

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

1. Three-dimension key summary (optional, when requested; if produced, it precedes the executive close);
2. Executive close (first, always present);
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
- if a three-dimension key summary is produced: it has exactly three sections in order, stays within ~12 bullets, is traceable to source, and is NOT desensitized;
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
