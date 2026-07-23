# domain-analyzer

Applies a domain-specific research lens on top of generic video analysis. Configured via YAML profiles for any vendor/event — HPE Discover, Cisco Live, IETF Meeting, etc.

## Available profiles

| Profile | Event | Vendor |
|---------|-------|--------|
| `hpe-discover-networking.yaml` | HPE Discover | HPE |

## Profile format

Each profile YAML configures:

- `meta` — skill name, display name, event name, vendor
- `corpus` — item ID pattern, directory structure, output path template
- `tracks` — research track names
- `sections` — required analysis section headers
- `availability_vocabulary` — capability classification terms
- `delta_statuses` — page-layer comparison terms
- `evidence_labels` — evidence classification terms
- `mandatory_extensions` — required analysis extensions
- `template` — frontmatter field defaults
- `terminology` — brand names and naming rules
- `additional_rules` — evidence separation, metrics precision, etc.

## Adding a new domain

```bash
# Copy the example profile
cp profiles/hpe-discover-networking.yaml profiles/cisco-live.yaml

# Edit: change meta, corpus paths, tracks, sections, terminology
# Validate against your analysis with the new profile:
python scripts/validate_domain_analysis.py --profile profiles/cisco-live.yaml item-analysis.md
```

## Validation

```bash
python scripts/validate_domain_analysis.py --profile profiles/<profile>.yaml <analysis.md>
```

Checks: frontmatter fields, all configured sections present, all vocabulary terms used, all tracks covered, customer/demo separation, no placeholder text, timestamped chronology present.

## References

- [domain-research-contract.md](references/domain-research-contract.md) — Generic analysis extension framework
- [domain-terminology.md](references/domain-terminology.md) — Terminology normalization rules
