# INCOSE Requirements Analysis Output Schema

## -1. Three-dimension key summary — mandatory first section, precedes the executive close

Always produce this section; never skip it. It is a concise, decision-oriented summary for sales, presales, and customer decision makers. Use three sections in fixed order: Customer background, Business needs, and Buying factors — always rendered in the output language. Build each bullet from the customer's business context and concrete operating scenarios, then connect the observed condition to the affected user/business outcome and the decision implication where evidence permits. Use 2–4 compact bullets per section when supported by the source; do not force a fixed total that removes material facts. No tables, IDs, or separate citation block. Every bullet must contain an inline original quotation and precise location. Preserve quantities, units, dates, durations, costs, capacities, locations, and response times exactly. Do not desensitize real output; any worked sample in this file must use generic labels and must not expose identifying details.

If the report is saved as a file, its filename must start with the skill-name prefix in the output language — `INCOSE 需求工程分析：` for Chinese, `INCOSE Requirements Engineering Analysis:` for English — followed by a concise customer or source-document title and the appropriate extension.

### Worked sample structure (desensitized; English rendering of a Chinese-customer case; quotation text is a placeholder — real output follows the output-language policy)

**Customer background:**
- `Explicit` An upscale hotel in a tourist city has 80+ guest rooms across multiple floors; its main guests are long-stay travelers, remote workers, and business travelers with average stays measured in weeks, so a stable network is part of the continuous stay and work experience. ("[desensitized original quotation]" — Source: [customer background section])
- `Explicit` The hotel has no dedicated IT staff and relies on an external service provider for network operations; daytime fault response takes about 1–2 hours, and overnight faults usually wait until the next day. ("[desensitized original quotation]" — Source: [current operations section])
- `Explicit` The hotel is renovating its public lounge and pool areas to introduce shared-office scenarios, so the network load will expand from guest internet access to office users and higher-concurrency services. ("[desensitized original quotation]" — Source: [business planning section])

**Business needs:**
- `Explicit` Uneven room coverage and missing corridor access points cause roaming disconnections when guests move between floors; the hotel needs to turn "signal exists" into continuously available connectivity across rooms and movement paths. ("[desensitized original quotation]" — Source: [current network problems section])
- `Explicit` Under high concurrency in public areas, disconnections and reconnections occur within about 20 minutes; the hotel needs to reduce the risk of concentrated network outages during check-in and public-area usage. ("[desensitized original quotation]" — Source: [current network problems section])
- `Explicit` Access switch ports are exhausted, so the current network cannot directly support new office spaces and device connections; the hotel needs to restore expandable access capacity. ("[desensitized original quotation]" — Source: [expansion limits section])

**Buying factors:**
- `Explicit` Guest WiFi experience is tied to the hotel's reputation and revenue; the goal is full coverage with fewer complaints, and the solution's value shows first in improved guest experience rather than in more devices. ("[desensitized original quotation]" — Source: [buying factors section])
- `Explicit` The hotel needs unified cloud-based operations to shorten the problem-detection and handling chain, reducing the operational exposure of having no dedicated IT staff and depending on external service providers. ("[desensitized original quotation]" — Source: [buying factors section])
- `Explicit` The network architecture must support the shared-office space and later expansion; dual-core, 10G interconnection, and all-optical access are solution constraints supporting that evolution goal, not the buying motive itself. ("[desensitized original quotation]" — Source: [buying factors section])

## 0. Executive close — first prose section, after the key summary

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
