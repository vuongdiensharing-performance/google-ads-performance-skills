"""Unit tests for the read-only GA4 MCP adapter."""

from __future__ import annotations

import unittest

from integrations.google_analytics.adapter import (
    EVIDENCE_TYPES,
    GA4AdapterError,
    GoogleAnalyticsMCPAdapter,
    canonical_request_fingerprint,
)


class FakeClient:
    def __init__(self, result: dict) -> None:
        self.result = result
        self.calls: list[tuple[str, dict]] = []

    def call_tool(self, name: str, arguments: dict) -> dict:
        self.calls.append((name, arguments))
        return self.result


class GA4ReadOnlyAdapterTests(unittest.TestCase):
    COMMIT = "a8ca729d4a8fa99bffe87962c17c0539c6aa9da7"

    def adapter(self, result: dict | None = None) -> tuple[GoogleAnalyticsMCPAdapter, FakeClient]:
        client = FakeClient(result or {"structuredContent": {"ok": True}})
        return GoogleAnalyticsMCPAdapter(client, provider_version="0.7.0", provider_commit=self.COMMIT), client

    def test_allowlist_maps_all_upstream_tools(self) -> None:
        adapter, _ = self.adapter()
        for tool, evidence_type in EVIDENCE_TYPES.items():
            request = {} if tool == "get_account_summaries" else {"property_id": "properties/123"}
            contract = adapter.call(tool, request)
            self.assertEqual(contract["evidence_type"], evidence_type)
            self.assertFalse(contract["provenance"]["inference_used"])

    def test_write_or_unknown_tool_is_rejected(self) -> None:
        adapter, client = self.adapter()
        with self.assertRaises(GA4AdapterError):
            adapter.call("delete_property", {})
        self.assertEqual(client.calls, [])

    def test_property_id_is_required_for_scoped_tools(self) -> None:
        adapter, client = self.adapter()
        with self.assertRaises(GA4AdapterError):
            adapter.call("run_report", {})
        self.assertEqual(client.calls, [])

    def test_property_id_format_is_strict(self) -> None:
        adapter, client = self.adapter()
        with self.assertRaises(GA4AdapterError):
            adapter.call("get_property_details", {"property_id": "properties/not-a-number"})
        self.assertEqual(client.calls, [])

    def test_fingerprint_matches_contract_semantics(self) -> None:
        adapter, _ = self.adapter()
        request = {
            "property_id": "properties/123",
            "date_range": {"start_date": "2026-08-01", "end_date": "2026-08-10"},
            "dimensions": ["sessionCampaignName"],
            "metrics": ["sessions", "conversions"],
        }
        contract = adapter.run_report("properties/123", request)
        expected_request = {"property_id": "properties/123", **request}
        self.assertEqual(
            contract["provenance"]["request_fingerprint"],
            canonical_request_fingerprint("run_report", expected_request),
        )

    def test_structured_content_is_preserved(self) -> None:
        adapter, _ = self.adapter({"structuredContent": {"rows": [{"sessions": 10}]}})
        contract = adapter.get_property_details("properties/123")
        self.assertEqual(contract["result"]["data"]["rows"][0]["sessions"], 10)


if __name__ == "__main__":
    unittest.main()
