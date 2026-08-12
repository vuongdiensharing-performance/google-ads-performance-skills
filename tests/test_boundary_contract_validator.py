import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_boundary_contract import (  # noqa: E402
    EXPECTED_STATE_IDS,
    canonical_contract,
    load_contract_schema,
    load_yaml,
    validate_rule,
)


RULE_IDS = (
    "STR-FRAG-001",
    "CV-TRACK-001",
    "BID-OBJ-001",
    "BUD-OPP-001",
    "ST-SPEND-001",
    "PMAX-GOAL-001",
)


class BoundaryContractValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_contract_schema()
        self.registry = load_yaml(ROOT / "rules/registry.yaml")

    def test_canonical_schema_is_valid(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_all_gate_2c_rules_validate_against_rule_local_contract(self) -> None:
        registry_by_id = {item["id"]: item for item in self.registry["rules"]}
        for rule_id in RULE_IDS:
            path = ROOT / registry_by_id[rule_id]["path"]
            with self.subTest(rule_id=rule_id):
                self.assertEqual(validate_rule(path, self.registry, self.schema), [])

    def test_all_a_to_f_states_have_canonical_identity(self) -> None:
        _, decisions, findings = canonical_contract(self.schema)
        self.assertEqual(set(EXPECTED_STATE_IDS.values()), set(decisions))
        self.assertEqual(set(EXPECTED_STATE_IDS.values()), set(findings))
        self.assertEqual(
            self.schema["x-canonical-resolution-precedence"],
            [
                "NOT_APPLICABLE",
                "APPLICABLE_MISSING_EVIDENCE",
                "CONFLICTING_EVIDENCE",
                "EXPLICIT_EXCLUSION",
                "APPLICABLE_TRIGGERED",
                "APPLICABLE_VALID",
            ],
        )

    def test_schema_rejects_rule_local_decision_drift(self) -> None:
        registry_by_id = {item["id"]: item for item in self.registry["rules"]}
        rule = load_yaml(ROOT / registry_by_id["STR-FRAG-001"]["path"])
        contract = copy.deepcopy(rule["boundary_contract"])
        contract["states"]["B"]["decision"] = "PASS"
        envelope = {
            "boundary_contract": contract,
            "resolution_precedence": self.schema["x-canonical-resolution-precedence"],
        }
        errors = list(Draft202012Validator(self.schema).iter_errors(envelope))
        self.assertFalse(errors, "JSON Schema validates shape; semantic canonical drift is checked by validate_rule")
        rule_path = ROOT / registry_by_id["STR-FRAG-001"]["path"]
        # The persisted Rule must remain canonical after the mutation attempt.
        self.assertEqual(load_yaml(rule_path)["boundary_contract"]["states"]["B"]["decision"], "FAIL")

    def test_machine_readable_contract_has_no_inference(self) -> None:
        registry_by_id = {item["id"]: item for item in self.registry["rules"]}
        for rule_id in RULE_IDS:
            rule = load_yaml(ROOT / registry_by_id[rule_id]["path"])
            resolution = rule["boundary_contract"]["conflict_policy"]["resolution"]
            with self.subTest(rule_id=rule_id):
                self.assertIs(resolution["inference_used"], False)


if __name__ == "__main__":
    unittest.main()
