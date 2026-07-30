from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI

APP_ROOT = Path(__file__).resolve().parent.parent
MCP_CONFIG = APP_ROOT / "mcp.json"


def build_routes() -> FastAPI:
    app = FastAPI(title="mcp-tools")

    @app.get("/status")
    async def status() -> dict:
        return {
            "app": "mcp-tools",
            "tools": ["playwright", "playwright-local"],
            "config": json.loads(MCP_CONFIG.read_text(encoding="utf-8")),
        }

    @app.get("/mcp.json")
    async def mcp_json() -> dict:
        return json.loads(MCP_CONFIG.read_text(encoding="utf-8"))

    return app
