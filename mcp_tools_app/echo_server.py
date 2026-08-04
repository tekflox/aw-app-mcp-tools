"""Minimal stdio MCP server — a trivial "echo" tool demonstrating a second
entry in this app's settings ``mcpServers`` JSON. Not enabled by default;
add ``"mcp-tools-echo": {"command": "python3", "args": ["-m",
"mcp_tools_app.echo_server"]}`` back into the settings JSON to try it.

Same shape as aw-mcp-gateway's own bundled ``gateway/examples/echo_server.py``
(deliberately — one obviously-correct reference implementation for a
minimal stdio MCP server), server-named differently (``mcp-tools-echo`` in
mcp.json, not ``example-echo``) so the two never collide once aggregated.
"""

from __future__ import annotations

import json
import sys

PROTOCOL = "2024-11-05"

TOOLS = [{
    "name": "echo",
    "description": "Echo back the given text.",
    "inputSchema": {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
    },
}]


def _write(msg: dict) -> None:
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        req_id = req.get("id")

        if method == "initialize":
            _write({"jsonrpc": "2.0", "id": req_id, "result": {
                "protocolVersion": PROTOCOL, "capabilities": {"tools": {}},
                "serverInfo": {"name": "mcp-tools-echo", "version": "1.0.0"}}})
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            _write({"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}})
        elif method == "tools/call":
            args = (req.get("params") or {}).get("arguments") or {}
            text = args.get("text", "")
            _write({"jsonrpc": "2.0", "id": req_id, "result": {
                "content": [{"type": "text", "text": text}], "isError": False}})
        else:
            _write({"jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"}})


if __name__ == "__main__":
    main()
