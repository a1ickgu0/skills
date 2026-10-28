import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_research.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def dataset():
    return {
        "schema_version": "1.0", "dataset_id": "synthetic-test", "revision": "1",
        "scope": {"vendor": "Example", "category": "switch", "region": "global",
                  "as_of": "2026-10-27", "lifecycle_target": "unknown", "defaults": [],
                  "synthetic": True},
        "products": [{"id": "example:SW1", "sku": "SW1", "name": "Test switch", "kind": "fixed"}],
        "configurations": [{"id": "standard", "product_id": "example:SW1",
                            "basis": "standard", "description": "No optional modules"}],
        "sources": [{"id": "s1", "url": "https://example.invalid/spec", "kind": "synthetic",
                     "title": "Synthetic fixture", "version": None, "accessed_at": "2026-10-27"}],
        "evidence": [{"id": "e1", "source_id": "s1", "locator": "fixture row 1",
                      "excerpt": "24 concurrent ports", "applicability": "SW1 standard"}],
        "claims": [{"id": "c1", "product_id": "example:SW1", "configuration_id": "standard",
                    "field": "concurrent_port_count", "value": 24, "unit": "ports",
                    "value_state": "known", "method": "secondary", "conflict": "none",
                    "evidence_ids": ["e1"], "importance": "critical", "rationale": "Test only"}],
        "research_tasks": [], "coverage": [], "changes": []}


def task():
    return {"id": "t1", "claim_id": "c1", "reason": "not_found_in_checked_sources",
            "priority": "high", "status": "open", "attempts": [
                {"action": "Read fixture", "source_ids": ["s1"], "result": "No CPU data"}],
            "hypotheses": [], "next_action": "Check hardware guide", "stop_reason": None}


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = dataset()

    def reject(self, text):
        self.assertTrue(any(text in error for error in validator.validate(self.data)))

    def test_valid_known(self):
        self.assertEqual(validator.validate(self.data), [])

    def test_missing_collection(self):
        del self.data["evidence"]
        self.reject("evidence")

    def test_duplicate_id(self):
        self.data["products"] *= 2
        self.reject("duplicate")

    def test_dangling_evidence(self):
        self.data["claims"][0]["evidence_ids"] = ["missing"]
        self.reject("reference")

    def test_unknown_cannot_be_zero(self):
        self.data["claims"][0]["value_state"] = "unknown"
        self.reject("null")

    def test_known_needs_evidence(self):
        self.data["claims"][0]["evidence_ids"] = []
        self.reject("evidence")

    def test_official_needs_official_source(self):
        self.data["claims"][0]["method"] = "official_direct"
        self.reject("official")

    def test_critical_unknown_needs_task(self):
        self.data["claims"][0].update(value=None, value_state="unknown", method="unestablished")
        self.reject("task")

    def test_progressed_unknown(self):
        self.data["claims"][0].update(value=None, value_state="unknown", method="unestablished")
        self.data["research_tasks"] = [task()]
        self.assertEqual(validator.validate(self.data), [])

    def test_unattempted_unknown_rejected(self):
        self.data["claims"][0].update(value=None, value_state="unknown", method="unestablished")
        item = task()
        item["attempts"] = []
        self.data["research_tasks"] = [item]
        self.reject("attempt")

    def test_conflict_needs_task_even_when_normal(self):
        self.data["claims"][0].update(conflict="unresolved", importance="normal")
        self.reject("task")

    def test_configuration_must_match_product(self):
        self.data["products"].append({"id": "example:SW2", "sku": "SW2", "name": "Other", "kind": "fixed"})
        self.data["configurations"][0]["product_id"] = "example:SW2"
        self.reject("configuration")

    def test_duplicate_current_claim(self):
        other = copy.deepcopy(self.data["claims"][0])
        other["id"] = "c2"
        self.data["claims"].append(other)
        self.reject("duplicate current")

    def test_derivation_cannot_reference_itself(self):
        self.data["claims"][0].update(method="name_inferred", derivation={
            "input_claim_ids": ["c1"], "rule": "test", "calculation": "test",
            "conditions": "test", "limitations": "test"})
        self.reject("cycle")

    def test_blocked_requires_reason_and_next_action(self):
        item = task()
        item.update(status="blocked", attempts=[], next_action=None)
        self.data["research_tasks"] = [item]
        self.reject("stop_reason")
        self.reject("next_action")

    def test_malformed_root_reports_error(self):
        self.assertTrue(validator.validate([]))

    def test_empty_attempt_does_not_count_as_progress(self):
        self.data["claims"][0].update(value=None, value_state="unknown", method="unestablished")
        item = task()
        item["attempts"] = [{"action": "", "source_ids": [], "result": ""}]
        self.data["research_tasks"] = [item]
        self.reject("nonempty")

    def test_malformed_reference_reports_error_not_crash(self):
        self.data["claims"][0]["method"] = "official_direct"
        self.data["evidence"][0]["source_id"] = []
        self.assertTrue(validator.validate(self.data))

    def test_same_sku_across_vendors_is_allowed(self):
        self.data["products"][0]["vendor"] = "Example"
        self.data["products"].append({"id": "other:SW1", "vendor": "Other", "sku": "SW1", "name": "Other switch", "kind": "fixed"})
        self.assertEqual(validator.validate(self.data), [])

    def test_user_change_requires_resolution(self):
        self.data["claims"][0]["method"] = "user_asserted"
        self.data["changes"] = [{"product_id": "example:SW1", "field": "concurrent_port_count",
                                 "old_value": 24, "new_value": 24, "reason": "Keep user value",
                                 "evidence_ids": ["e1"]}]
        self.reject("user_resolution")

    def test_bad_date(self):
        self.data["scope"]["as_of"] = "2026-02-30"
        self.reject("date")


if __name__ == "__main__":
    unittest.main()
