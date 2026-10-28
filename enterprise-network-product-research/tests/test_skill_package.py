import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_local_markdown_links_exist(self):
        for path in [ROOT / "SKILL.md", *list((ROOT / "references").glob("*.md"))]:
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" not in target and not target.startswith("#"):
                    with self.subTest(path=path.name, target=target):
                        self.assertTrue((path.parent / target.split("#")[0]).exists())

    def test_fixture_cli_passes(self):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts/validate_research.py"),
             str(ROOT / "tests/fixtures/research.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("not factual verification", result.stdout)

    def test_fixture_is_explicitly_synthetic(self):
        data = json.loads((ROOT / "tests/fixtures/research.json").read_text())
        self.assertTrue(data["scope"]["synthetic"])
        self.assertTrue(all(s["kind"] == "synthetic" for s in data["sources"]))

    def test_expert_activation_is_in_runtime_entry(self):
        skill = (ROOT / "SKILL.md").read_text()
        self.assertIn("必须激活数通/交换机产品专家角色", skill)
        self.assertIn("references/expert-review.md#专家字段判定是必经步骤", skill)
        rules = (ROOT / "references/expert-review.md").read_text()
        for requirement in ("领域推导", "条件结论", "真正未知", "name_inferred", "official_derived"):
            self.assertIn(requirement, rules)

    def test_panorama_reference_is_aruba_only(self):
        import xml.etree.ElementTree as ET
        path = ROOT / "references/panorama_masked.svg"
        root = ET.parse(path).getroot()
        text = " ".join(root.itertext())
        self.assertIn("Aruba CX", text)
        self.assertIn("非全量官方核验", text)
        self.assertNotRegex(text, r"XW-\d+|版本\s*[12]\.0|降本|场景款|共\s*27\s*款")
        for element in root.iter():
            self.assertNotIn(element.tag.split("}")[-1], ("image", "script", "foreignObject"))
        data = json.loads((ROOT / "references/panorama-example.json").read_text())
        items = [item for lane in data["lanes"] for item in lane["items"]]
        self.assertEqual(len(items), 8)
        self.assertTrue(all(item["sku"] in text and item["source_url"].startswith("https://buy.hpe.com/") for item in items))
        self.assertTrue((ROOT / "references/panorama_masked.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_historical_csv_remains_input_not_answer(self):
        skill = (ROOT / "SKILL.md").read_text()
        self.assertIn("不是标准答案", skill)
        self.assertTrue((ROOT / "references/aruba-example-notes.md").exists())


if __name__ == "__main__":
    unittest.main()
