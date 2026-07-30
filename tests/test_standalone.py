from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mcp_tools_app.__main__ import SLUG, UI_DIST, build_standalone_app  # noqa: E402


def test_standalone_app_boots_and_mounts_api():
    client = TestClient(build_standalone_app())
    resp = client.get(f"/api/apps/{SLUG}/status")
    assert resp.status_code == 200
    assert resp.json()["app"] == "mcp-tools"


def test_standalone_serves_ui_dist_when_built():
    if not UI_DIST.is_dir():
        return
    client = TestClient(build_standalone_app())
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
