"""Read-only adapter from Google Analytics MCP tool results to GA4 Evidence Contract."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Protocol


EVIDENCE_TYPES: dict[str, str] = {
    "get_account_summaries": "GA4_IDENTITY",
    "get_property_details": "GA4_IDENTITY",
    "list_google_ads_links": "GA4_LINKAGE",
    "run_report": "GA4_REPORT",
    "run_funnel_report": "GA4_FUNNEL",
    "get_custom_dimensions_and_metrics": "GA4_METADATA",
    "run_realtime_report": "GA4_REALTIME",
}

READ_ONLY_TOOLS = frozenset(EVIDENCE_TYPES)


class MCPToolCaller(Protocol):
    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]: ...


class GA4AdapterError(RuntimeError):
    """Raised when a GA4 request cannot safely become evidence."""


def canonical_request_fingerprint(tool: str, request: dict[str, Any]) -> str:
    """Return the exact fingerprint required by the GA4 Evidence Contract."""
    payload = {"tool": tool, "request": request}
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _extract_data(result: dict[str, Any]) -> dict[str, Any]:
    structured = result.get("structuredContent")
    if isinstance(structured, dict):
        return structured

    content = result.get("content")
    if isinstance(content, list):
        parsed: list[Any] = []
        for item in content:
            if not isinstance(item, dict):
                parsed.append(item)
                continue
            text = item.get("text")
            if isinstance(text, str):
                try:
                    parsed.append(json.loads(text))
                except json.JSONDecodeError:
                    parsed.append(text)
            else:
                parsed.append(item)
        return {"content": parsed}

    return {"raw": result}


class GoogleAnalyticsMCPAdapter:
    """Expose only upstream read-only GA4 tools and emit evidence envelopes."""

    def __init__(self, client: MCPToolCaller, *, provider_version: str, provider_commit: str) -> None:
        self.client = client
        self.provider_version = provider_version
        self.provider_commit = provider_commit

    def call(self, tool: str, request: dict[str, Any]) -> dict[str, Any]:
        if tool not in READ_ONLY_TOOLS:
            raise GA4AdapterError(f"Tool is outside the GA4 read-only allowlist: {tool}")
        self._validate_request(tool, request)
        raw_result = self.client.call_tool(tool, request)
        if not isinstance(raw_result, dict):
            raise GA4AdapterError("MCP tool result must be an object")

        property_id = request.get("property_id")
        source: dict[str, Any] = {
            "provider": "google_analytics",
            "transport": "mcp",
            "tool": tool,
        }
        if property_id is not None:
            source["property_id"] = property_id

        return {
            "contract_version": "1.1.0",
            "evidence_type": EVIDENCE_TYPES[tool],
            "source": source,
            "request": request,
            "result": {"data": _extract_data(raw_result), "metadata": {"mcp_result": raw_result}},
            "provenance": {
                "retrieved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "source_verified": True,
                "inference_used": False,
                "provider_version": self.provider_version,
                "provider_commit": self.provider_commit,
                "request_fingerprint": canonical_request_fingerprint(tool, request),
            },
        }

    def get_account_summaries(self, request: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.call("get_account_summaries", request or {})

    def get_property_details(self, property_id: str) -> dict[str, Any]:
        return self.call("get_property_details", {"property_id": property_id})

    def list_google_ads_links(self, property_id: str) -> dict[str, Any]:
        return self.call("list_google_ads_links", {"property_id": property_id})

    def run_report(self, property_id: str, request: dict[str, Any]) -> dict[str, Any]:
        return self.call("run_report", {"property_id": property_id, **request})

    def run_funnel_report(self, property_id: str, request: dict[str, Any]) -> dict[str, Any]:
        return self.call("run_funnel_report", {"property_id": property_id, **request})

    def get_custom_dimensions_and_metrics(self, property_id: str) -> dict[str, Any]:
        return self.call("get_custom_dimensions_and_metrics", {"property_id": property_id})

    def run_realtime_report(self, property_id: str, request: dict[str, Any]) -> dict[str, Any]:
        return self.call("run_realtime_report", {"property_id": property_id, **request})

    @staticmethod
    def _validate_request(tool: str, request: dict[str, Any]) -> None:
        if not isinstance(request, dict):
            raise GA4AdapterError("MCP request must be an object")
        if tool != "get_account_summaries":
            property_id = request.get("property_id")
            if not isinstance(property_id, str) or not property_id.isdigit() is False:
                if not isinstance(property_id, str) or not property_id.startswith("properties/"):
                    raise GA4AdapterError("property_id is required and must match properties/<numeric_id>")
            suffix = property_id.removeprefix("properties/")
            if not suffix.isdigit():
                raise GA4AdapterError("property_id must match properties/<numeric_id>")
