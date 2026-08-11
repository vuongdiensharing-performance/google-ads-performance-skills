"""Minimal stdio MCP JSON-RPC client used by the GA4 read-only adapter.

The client intentionally exposes only request/response transport primitives. It
never interprets analytics data and it never exposes a write-capable MCP tool.
"""

from __future__ import annotations

import json
import os
import subprocess
from typing import Any, Sequence


class MCPClientError(RuntimeError):
    """Raised when the MCP transport or protocol fails."""


class MCPToolError(MCPClientError):
    """Raised when the MCP server returns a JSON-RPC/tool error."""


class StdioMCPClient:
    """Small synchronous MCP stdio client for one long-lived server process."""

    def __init__(
        self,
        command: Sequence[str],
        *,
        env: dict[str, str] | None = None,
        timeout_seconds: float = 30.0,
        protocol_version: str | None = None,
    ) -> None:
        if not command:
            raise ValueError("MCP command must not be empty")
        self.command = list(command)
        self.timeout_seconds = timeout_seconds
        self.protocol_version = protocol_version or os.getenv(
            "GA4_MCP_PROTOCOL_VERSION", "2025-06-18"
        )
        self.env = env
        self._process: subprocess.Popen[str] | None = None
        self._next_id = 1
        self.server_info: dict[str, Any] = {}

    def start(self) -> None:
        if self._process is not None:
            return
        self._process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            env={**os.environ, **self.env} if self.env else None,
            bufsize=1,
        )
        response = self._request(
            "initialize",
            {
                "protocolVersion": self.protocol_version,
                "capabilities": {},
                "clientInfo": {"name": "google-ads-performance-skills", "version": "0.1.0"},
            },
        )
        self.server_info = response.get("serverInfo", {})
        self._notify("notifications/initialized", {})

    def close(self) -> None:
        process = self._process
        self._process = None
        if process is None:
            return
        if process.stdin:
            try:
                process.stdin.close()
            except OSError:
                pass
        try:
            process.terminate()
            process.wait(timeout=2)
        except (OSError, subprocess.TimeoutExpired):
            try:
                process.kill()
            except OSError:
                pass

    def __enter__(self) -> "StdioMCPClient":
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.start()
        response = self._request("tools/call", {"name": name, "arguments": arguments})
        if response.get("isError") is True:
            raise MCPToolError(f"MCP tool {name!r} returned isError=true")
        return response

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        process = self._require_process()
        if process.stdin is None:
            raise MCPClientError("MCP stdin is unavailable")
        process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method, "params": params}) + "\n")
        process.stdin.flush()

    def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        process = self._require_process()
        if process.stdin is None or process.stdout is None:
            raise MCPClientError("MCP stdio streams are unavailable")
        request_id = self._next_id
        self._next_id += 1
        process.stdin.write(
            json.dumps(
                {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
                separators=(",", ":"),
            )
            + "\n"
        )
        process.stdin.flush()

        while True:
            line = process.stdout.readline()
            if line == "":
                raise MCPClientError("MCP server closed stdout before replying")
            if not line.strip():
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                continue
            if message.get("id") != request_id:
                continue
            if "error" in message:
                error = message["error"]
                raise MCPToolError(f"MCP JSON-RPC error: {error}")
            result = message.get("result")
            if not isinstance(result, dict):
                raise MCPClientError("MCP response result must be an object")
            return result

    def _require_process(self) -> subprocess.Popen[str]:
        if self._process is None or self._process.poll() is not None:
            raise MCPClientError("MCP client is not running")
        return self._process
