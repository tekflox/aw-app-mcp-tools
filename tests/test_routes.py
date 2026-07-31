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
    assert body["tools"] == ["playwright"]
    assert body["config"]["mcpServers"]["playwright"]["command"] == "npx"
    assert "http://aw-app-browser:9223" in body["config"]["mcpServers"]["playwright"]["args"]


def test_mcp_json():
    client = TestClient(build_routes())
    resp = client.get("/mcp.json")
    assert resp.status_code == 200
    assert "playwright" in resp.json()["mcpServers"]
    assert "playwright-local" not in resp.json()["mcpServers"]
