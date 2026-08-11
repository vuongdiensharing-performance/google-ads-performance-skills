import unittest
from pathlib import Path

import yaml

from scripts.validate_ga4_query import (
    REGISTRY_PATH,
    SCHEMA_PATH,
    load_json,
    load_mapping,
    validate,
)


ROOT = Path(__file__).resolve().parents[1]


class GA4QueryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_json(SCHEMA_PATH)
        cls.registry = load_mapping(REGISTRY_PATH)

    def fixture(self, name):
        return load_mapping(ROOT / "evals/ga4" / name)

    def test_valid_conversion_query(self):
        errors, canonical = validate(
            self.fixture("ga4_query_contract.yaml"), self.schema, self.registry
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(canonical)
        self.assertEqual(canonical["query_id"], "GA4-CV-001")
        self.assertEqual(canonical["tool"], "run_report")
        self.assertEqual(canonical["request"]["dimensions"], ["sessionCampaignName"])
        self.assertEqual(canonical["request"]["metrics"], ["sessions", "conversions"])
        self.assertRegex(canonical["request_fingerprint"], r"^sha256:[0-9a-f]{64}$")

    def test_arbitrary_metric_is_rejected(self):
        errors, canonical = validate(
            self.fixture("ga4_query_contract_invalid_metric.yaml"), self.schema, self.registry
        )
        self.assertTrue(errors)
        self.assertIsNone(canonical)
        self.assertTrue(any("additional properties" in error for error in errors))

    def test_unknown_filter_is_rejected(self):
        errors, canonical = validate(
            self.fixture("ga4_query_contract_invalid_filter.yaml"), self.schema, self.registry
        )
        self.assertTrue(errors)
        self.assertIsNone(canonical)
        self.assertTrue(any("additional properties" in error for error in errors))

    def test_unknown_query_id_is_rejected(self):
        contract = self.fixture("ga4_query_contract.yaml")
        contract["query_id"] = "GA4-UNKNOWN-999"
        errors, canonical = validate(contract, self.schema, self.registry)
        self.assertTrue(errors)
        self.assertIsNone(canonical)
        self.assertTrue(any("exactly one registered query" in error for error in errors))

    def test_date_range_is_deterministic(self):
        contract = self.fixture("ga4_query_contract.yaml")
        first_errors, first = validate(contract, self.schema, self.registry)
        second_errors, second = validate(contract, self.schema, self.registry)
        self.assertEqual(first_errors, second_errors, [])
        self.assertEqual(first["request_fingerprint"], second["request_fingerprint"])


if __name__ == "__main__":
    unittest.main()
