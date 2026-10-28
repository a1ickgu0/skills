"""Check the skill's minimal research contract; no network or factual verification."""

import argparse
from datetime import date
import json
from pathlib import Path
import sys


COLLECTIONS = {
    "products": ("id", "sku", "name", "kind"),
    "configurations": ("id", "product_id", "basis", "description"),
    "sources": ("id", "url", "kind", "title", "version", "accessed_at"),
    "evidence": ("id", "source_id", "locator", "excerpt", "applicability"),
    "claims": ("id", "product_id", "configuration_id", "field", "value", "unit",
               "value_state", "method", "conflict", "evidence_ids", "importance", "rationale"),
    "research_tasks": ("id", "claim_id", "reason", "priority", "status", "attempts",
                       "hypotheses", "next_action", "stop_reason"),
    "coverage": ("id", "segment", "source_ids", "candidate_product_ids", "status", "gaps"),
    "changes": ("product_id", "field", "old_value", "new_value", "reason", "evidence_ids"),
}


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["root must be an object"]

    def require(obj, fields, label):
        for field in fields:
            if field not in obj:
                errors.append(f"{label}: missing {field}")

    def choice(obj, field, values, label):
        if obj.get(field) not in values:
            errors.append(f"{label}: invalid {field}")

    def check_date(value, label):
        try:
            if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{label}: invalid date")

    require(data, ("schema_version", "dataset_id", "revision", "scope"), "root")
    if data.get("schema_version") != "1.0":
        errors.append("unsupported schema_version")
    for key in ("dataset_id", "revision"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key}: expected nonempty string")
    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
    else:
        require(scope, ("vendor", "category", "region", "as_of", "lifecycle_target", "defaults"), "scope")
        check_date(scope.get("as_of"), "scope.as_of")
        if not isinstance(scope.get("defaults"), list):
            errors.append("scope.defaults must be an array")

    rows, indexes = {}, {}
    for name, fields in COLLECTIONS.items():
        values = data.get(name)
        if not isinstance(values, list):
            errors.append(f"{name} must be an array")
            values = []
        rows[name], indexes[name] = [], {}
        for number, item in enumerate(values):
            label = f"{name}[{number}]"
            if not isinstance(item, dict):
                errors.append(f"{label}: expected object")
                continue
            rows[name].append(item)
            require(item, fields, label)
            if "id" in fields:
                ident = item.get("id")
                if not isinstance(ident, str) or not ident.strip():
                    errors.append(f"{label}: invalid id")
                elif ident in indexes[name]:
                    errors.append(f"{label}: duplicate id {ident}")
                else:
                    indexes[name][ident] = item

    def ref(value, target, label):
        if not isinstance(value, str) or value not in indexes[target]:
            errors.append(f"{label}: invalid reference to {target}")
            return None
        return indexes[target][value]

    def refs(item, field, target, label):
        values = item.get(field)
        if not isinstance(values, list):
            errors.append(f"{label}.{field}: expected array")
            return []
        return [found for value in values if (found := ref(value, target, label)) is not None]

    skus = set()
    for item in rows["products"]:
        sku = item.get("sku")
        vendor = item.get("vendor", scope.get("vendor") if isinstance(scope, dict) else None)
        key = (str(vendor), str(sku))
        if not isinstance(vendor, str) or not vendor.strip() or vendor == "multiple":
            errors.append("product: explicit vendor required for multi-vendor research")
        if not isinstance(sku, str) or not sku.strip():
            errors.append("product: invalid sku")
        elif key in skus:
            errors.append("product: duplicate sku within scoped vendor")
        else:
            skus.add(key)
    for item in rows["configurations"]:
        ref(item.get("product_id"), "products", "configuration")
        choice(item, "basis", ("standard", "maximum", "specified"), "configuration")
    for item in rows["sources"]:
        choice(item, "kind", ("official", "secondary", "user", "synthetic"), "source")
        check_date(item.get("accessed_at"), "source.accessed_at")
        if item.get("kind") == "synthetic" and not (isinstance(scope, dict) and scope.get("synthetic") is True):
            errors.append("synthetic source requires scope.synthetic=true")
    for item in rows["evidence"]:
        ref(item.get("source_id"), "sources", "evidence")

    current, graph = set(), {}
    for item in rows["claims"]:
        label = f"claim {item.get('id')}"
        ref(item.get("product_id"), "products", label)
        config = ref(item.get("configuration_id"), "configurations", label)
        if config and config.get("product_id") != item.get("product_id"):
            errors.append(f"{label}: configuration belongs to another product")
        key = tuple(str(item.get(k)) for k in ("product_id", "configuration_id", "field"))
        if key in current:
            errors.append(f"{label}: duplicate current claim")
        current.add(key)
        choice(item, "value_state", ("known", "unknown", "not_applicable"), label)
        choice(item, "method", ("official_direct", "official_derived", "name_inferred", "secondary", "user_asserted", "unestablished"), label)
        choice(item, "conflict", ("none", "unresolved", "explained"), label)
        choice(item, "importance", ("critical", "normal"), label)
        state = item.get("value_state")
        if state in ("unknown", "not_applicable") and item.get("value") is not None:
            errors.append(f"{label}: unknown/not_applicable value must be null")
        if state == "known" and item.get("value") is None:
            errors.append(f"{label}: known value cannot be null")
        evidence = refs(item, "evidence_ids", "evidence", label)
        if state == "known" and item.get("method") != "user_asserted" and not evidence:
            errors.append(f"{label}: known value requires evidence")
        if state == "known" and item.get("method") == "unestablished":
            errors.append(f"{label}: known value cannot be unestablished")
        if state == "known" and item.get("method") in ("official_direct", "official_derived"):
            if not any(isinstance(e.get("source_id"), str) and indexes["sources"].get(e["source_id"], {}).get("kind") == "official" for e in evidence):
                errors.append(f"{label}: official method requires official evidence")
        if item.get("method") in ("official_derived", "name_inferred"):
            derivation = item.get("derivation")
            if not isinstance(derivation, dict):
                errors.append(f"{label}: missing derivation")
            else:
                require(derivation, ("input_claim_ids", "rule", "calculation", "conditions", "limitations"), label)
                inputs = refs(derivation, "input_claim_ids", "claims", label)
                graph[str(item.get("id"))] = [str(i.get("id")) for i in inputs]
                if any(i.get("value_state") != "known" or i.get("conflict") == "unresolved" for i in inputs):
                    errors.append(f"{label}: derivation has uncertain input")

    visiting, visited = set(), set()

    def visit(node):
        if node in visiting:
            errors.append(f"claim {node}: derivation cycle")
            return
        if node in visited:
            return
        visiting.add(node)
        for child in graph.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)

    active_tasks = set()
    for item in rows["research_tasks"]:
        label = f"task {item.get('id')}"
        claim = ref(item.get("claim_id"), "claims", label)
        choice(item, "reason", ("not_searched", "applicability_unclear", "conflicting", "configuration_dependent", "access_blocked", "not_found_in_checked_sources"), label)
        choice(item, "status", ("open", "blocked", "exhausted", "resolved"), label)
        choice(item, "priority", ("high", "normal"), label)
        status = item.get("status")
        if status != "resolved" and isinstance(item.get("claim_id"), str):
            active_tasks.add(item["claim_id"])
        if status in ("open", "blocked") and not item.get("next_action"):
            errors.append(f"{label}: next_action required")
        if status in ("blocked", "exhausted") and not item.get("stop_reason"):
            errors.append(f"{label}: stop_reason required")
        attempts = item.get("attempts")
        if not isinstance(attempts, list):
            errors.append(f"{label}: attempts must be array")
            attempts = []
        needs_attempt = claim and (claim.get("importance") == "critical" or claim.get("conflict") == "unresolved")
        if (needs_attempt or status == "resolved") and not attempts and status != "blocked":
            errors.append(f"{label}: at least one attempt required")
        for attempt in attempts:
            if not isinstance(attempt, dict):
                errors.append(f"{label}: invalid attempt")
                continue
            require(attempt, ("action", "source_ids", "result"), label)
            for field in ("action", "result"):
                if not isinstance(attempt.get(field), str) or not attempt[field].strip():
                    errors.append(f"{label}: attempt {field} must be nonempty")
            refs(attempt, "source_ids", "sources", label)
        if not isinstance(item.get("hypotheses"), list):
            errors.append(f"{label}: hypotheses must be array")
        if status == "resolved" and claim and (claim.get("value_state") == "unknown" or claim.get("conflict") == "unresolved"):
            errors.append(f"{label}: resolved task still has unresolved claim")
    for item in rows["claims"]:
        if ((item.get("importance") == "critical" and item.get("value_state") == "unknown") or item.get("conflict") == "unresolved") and item.get("id") not in active_tasks:
            errors.append(f"claim {item.get('id')}: unresolved claim requires task")
    for item in rows["coverage"]:
        refs(item, "source_ids", "sources", "coverage")
        refs(item, "candidate_product_ids", "products", "coverage")
        choice(item, "status", ("complete", "partial", "blocked"), "coverage")
    for item in rows["changes"]:
        ref(item.get("product_id"), "products", "change")
        refs(item, "evidence_ids", "evidence", "change")
        user_value = item.get("origin") == "user" or any(
            c.get("product_id") == item.get("product_id") and c.get("field") == item.get("field")
            and c.get("method") == "user_asserted" for c in rows["claims"])
        if user_value and not item.get("user_resolution"):
            errors.append("change: user_resolution required for user value")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        print(f"Cannot read research JSON: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print("PASS: minimal research contract (not factual verification)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
