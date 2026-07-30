from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mcp_tools_app.routes import build_routes  # noqa: E402


def test_status():
    client = TestClient(build_routes())
    resp = client.get("/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["app"] == "mcp-tools"
    assert body["tools"] == ["playwright", "playwright-local"]
    assert body["config"]["mcpServers"]["playwright"]["command"] == "aw-playwright-mcp"


def test_mcp_json():
    client = TestClient(build_routes())
    resp = client.get("/mcp.json")
    assert resp.status_code == 200
    assert "playwright-local" in resp.json()["mcpServers"]
