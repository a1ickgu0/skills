# INCOSE Requirements Analysis Output Schema

## -1. Three-dimension key summary — optional, precedes executive close

Produce only when requested. Three sections in fixed order: 客户背景 (customer background), 问题诉求 (pain points / problems), 购买要素 (buying factors). Target 9–12 bullets total, one sentence each. No tables, no IDs, no citation block. Keep the customer's own phrasing for pain points. 购买要素 must express the business essence of why the customer buys (business outcome / risk removed / strategic position) from the customer's perspective, not the products purchased. Do NOT desensitize real output — the sample in SKILL.md is desensitized for the SKILL only.

## 0. Executive close — first section

Write one standalone paragraph covering scope, output language, core buying factors, key requirements, evidence coverage, unresolved risks, and recommended action. Include at least two original-language quotations with locations.

## 1. Scope, sources, and evidence level

| Field | Content | Original key quotation |
|---|---|---|
| Source | Title, link/file, revision/date | |
| System boundary | In-scope and out-of-scope system elements | |
| Lifecycle phase | Plan, procure, deploy, operate, maintain, retire | |
| Output language | Local/customer language and selection rationale | |
| Evidence limits | Unread attachments, missing metrics, conflicts | |
| Evidence level | A=explicit source; B=source data/test; C=reasoned derivation; D=to-be-confirmed assumption | |

## 2. Customer-business core buying factors

| ID | Buying factor | Business goal/value | Pain/trigger | Decision impact | Metrics | Solution mapping | Status | Original key quotation |
|---|---|---|---|---|---|---|---|---|

Status: `explicit`, `derived from pain`, or `to be confirmed`. Do not simply list product models.

## 3. Stakeholders

| ID | Role/organization | Context and goal | Pain/constraint | Influence | Original key quotation |
|---|---|---|---|---|---|

## 4. ConOps scenarios

| Scenario ID | Trigger | Participants/entities | Main flow | Expected result | Exception/recovery | Original key quotation |
|---|---|---|---|---|---|---|

## 5. Requirements

| ID | Level | Requirement statement | Source role | Type | Priority | Original key quotation/location | Status |
|---|---|---|---|---|---|---|---|

Types may include function, performance, availability, interface, operations, deployment/migration, security, constraint, and quality attribute. Status may be candidate, verified, partially verified, to be clarified, or conflicting.

## 6. Traceability matrix

| Stakeholder requirement | System requirement | Solution/component | Verification evidence | Coverage conclusion | Original key quotation |
|---|---|---|---|---|---|

Coverage conclusions: covered, partially covered, not covered, or indeterminate.

## 7. Verification plan

| VER ID | Related requirement | Method | Conditions/environment | Measurement and threshold | Sample/duration | Pass criteria | Current evidence | Original key quotation |
|---|---|---|---|---|---|---|---|---|

## 8. Issues and decisions

| ID | Category | Content | Impact | Recommended action | Owner role | Closure condition | Original key quotation |
|---|---|---|---|---|---|---|---|

Categories: conflict, risk, assumption, gap, decision, or technical debt.

## 9. Requirements quality review

For key requirements, state pass/fail/to-confirm for necessity, singularity, clarity, feasibility, verifiability, completeness, consistency, and traceability. Attach an original key quotation to every judgment.

## 10. Original-source validation record

| Validation object | Original key quotation | Source location | Result | Revision note |
|---|---|---|---|---|

Results: passed, corrected, deleted, or not directly verifiable. Cover the executive close, buying factors, each requirement class, traceability conclusions, verification claims, risks/assumptions, and final conclusion.

## 11. Conclusion

Summarize baselinable requirements, requirements not ready for baseline, critical verification gaps, customer decisions, and next clarification actions. End with an original key quotation.

