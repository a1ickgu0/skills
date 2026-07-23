# Analysis contract

## Required report structure

The analysis must contain these sections, even when a section records that the source supplied no evidence:

1. Executive summary
2. Scope and evidence
3. Full chronology
4. Themes and argument
5. Mechanisms and process
6. Entities, claims, and metrics
7. Demonstrations and cases
8. Evidence and status ledger
9. Requested analytical lenses
10. Contradictions and uncertainties
11. Unanswered questions
12. Method and sources

## Completeness

`Full chronology` is the coverage spine. Use ordered timestamp ranges from the transcript and account for every material section. Summaries may compress greetings, transitions, and repeated wording, but must not silently remove claims, qualifications, counterexamples, or changes in topic.

## Analysis manifest

`analysis-manifest.json` must contain:

- `schema_version`
- `generated_at`
- `inputs`: a non-empty array of objects with `path`, `role`, and lowercase SHA-256 `sha256`
- `analytical_lenses`: an array, empty when none were requested
- `output`: an object with `path` and SHA-256 `sha256`

Input roles may include `transcript`, `transcription-manifest`, `ocr`, and `background`.
