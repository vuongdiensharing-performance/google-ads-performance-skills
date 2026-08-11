#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

from rule_engine import run

ROOT = Path(__file__).resolve().parents[1]


class RuleEngineSmokeTest(unittest.TestCase):
    def test_broad_match_rule_matches(self):
        context = json.loads((ROOT / "examples/rule-engine/context.json").read_text(encoding="utf-8"))
        result = run(ROOT / "rules", context)
        ids = {item["rule_id"] for item in result["matched"]}
        self.assertIn("KW-BROAD-001", ids)

    def test_missing_evidence_is_not_a_finding(self):
        context = {"evidence": {"business_context_available": True}}
        result = run(ROOT / "rules", context)
        self.assertTrue(result["insufficient_evidence"])


if __name__ == "__main__":
    unittest.main()
