# analyzing-video-transcripts

Generic evidence-traceable video content analysis. Turns a validated timestamped transcript into a complete content report with chronology, themes, mechanisms, claims, demonstrations, and uncertainties — without vendor- or event-specific assumptions.

## Input requirements

- `transcript.md` — ordered timestamp blocks with complete source-language coverage
- `transcription-manifest.json` — declaring 100% audio coverage

## Output

```
output_dir/
├── video-analysis.md             # Full analysis with evidence labels
├── analysis-manifest.json        # Input hashes, lenses, output hash
```

## Evidence labels

| Label | Meaning |
|-------|---------|
| `speech-only` | Claim from spoken word only |
| `slide-only` | Claim from slides only |
| `demo` | Demonstration evidence |
| `customer-claim` | Customer-reported claim |
| `official-cross-check` | Verified against official source |
| `analysis-inference` | Analyst interpretation |
| `uncertain` | Ambiguous or unclear |
| `future-looking` | Roadmap or forward-looking statement |

## Analysis lenses

Apply user-requested lenses only after the source-grounded analysis exists. The analysis framework supports thematic, competitive, technical, strategic, and temporal lenses without coupling to any specific vendor or event.

## References

- [analysis-contract.md](references/analysis-contract.md) — Analysis requirements and structure
- [evidence-rules.md](references/evidence-rules.md) — Evidence classification and attribution rules
