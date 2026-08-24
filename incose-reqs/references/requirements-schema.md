# INCOSE Requirements Analysis Output Schema

## -1. Three-dimension key summary — mandatory first section, precedes the executive close

Always produce this section; never skip it. Three sections in fixed order: Customer background, Pain points / problems, Buying factors. Target 9–12 bullets total, one sentence each. No tables, no IDs, no citation block. Keep the customer's own phrasing for pain points. Buying factors must express the business essence of why the customer buys (business outcome / risk removed / strategic position) from the customer's perspective, not the products purchased. Do NOT desensitize real output — the sample below is desensitized for the SKILL only.

### Worked sample (desensitized)

**Customer background:**
- An upscale hotel in a tourist city, opened in recent years, several dozen rooms; guests are mainly long-stay business travelers and digital nomads with a hard requirement for stable, high-speed network.
- No dedicated IT staff; network operations long outsourced on a monthly fee, with slow daytime response and next-day handling of nighttime failures.
- Currently converting the public lounge into a co-working space as a differentiating selling point.

**Pain points:** Current network is gigabit copper + WiFi 5 with one AP serving every two rooms; problems are prominent
- Uneven room coverage and no corridor APs cause roaming drops; frequent disconnect/reconnect in the lobby under high concurrency
- Access-switch ports exhausted, no room to expand
- Operations depend on outsourcing, with slow response

**Buying factors:**
- Protect guest reputation and revenue: guests complain, post negative reviews, and check out over poor network, directly hitting hotel income
- Escape passive dependence on outsourced operations: fault response shifts from next-day to controllable and self-managed
- Pave the way for the differentiating selling point: the co-working space needs a network foundation strong enough for the future guest base

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

