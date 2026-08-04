from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from . import routes as routes_mod

log = logging.getLogger("aw_apps.mcp_tools")

DEFAULT_CDP_ENDPOINT = "http://aw-app-browser:9223"

# Mirrors aw-app.json's config_schema.properties.mcpServers.default. That
# JSON-Schema default is only applied by aw-workspace's API-response layer
# (config_with_defaults in list_apps/get_app_config) — ctx.config at
# activate() time is the raw stored config, un-defaulted. Without this
# fallback, a fresh install (config == {}) writes an EMPTY mcp.json until
# the user opens settings and hits Save once — found live 2026-08-04.
DEFAULT_MCP_SERVERS = {
    "playwright": {
        "enabled": True,
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@playwright/mcp@0.0.77", "--cdp-endpoint", DEFAULT_CDP_ENDPOINT],
    },
}


def build_mcp_servers(config: dict) -> dict:
    """The ``mcpServers`` object this app's own root mcp.json should
    contain — taken verbatim from ``config["mcpServers"]`` when present,
    else the schema default. This app's settings panel IS a raw JSON
    editor over this exact object (see JsonConfigEditor in
    aw-workspace-ui), so whatever the user adds, removes, or edits there is
    what aw-mcp-gateway's app-scan reads on the next reload (ADR
    "aw-app-mcp-tools contributes mcp.json") — not just a fixed
    enable/disable toggle over a hardcoded tool set."""
    config = config or {}
    servers = config.get("mcpServers")
    if servers is None:
        return dict(DEFAULT_MCP_SERVERS)
    return dict(servers) if isinstance(servers, dict) else {}


def write_mcp_json(package_dir: str, config: dict) -> dict:
    """Regenerate this app's own root mcp.json from config and write it to
    disk — the file aw-mcp-gateway scans directly. Returns the full
    {"mcpServers": ...} document written, for callers (routes.py's
    /status) that want it without a re-read."""
    doc = {"mcpServers": build_mcp_servers(config)}
    path = Path(package_dir) / "mcp.json"
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return doc


class McpToolsAppPlugin:
    async def activate(self, ctx) -> None:
        with open(os.path.join(ctx.package_dir, "aw-app.json"), encoding="utf-8") as f:
            manifest = json.load(f)

        config = getattr(ctx, "config", {}) or {}

        installed = []
        for cli in manifest.get("contributes", {}).get("system_clis", []):
            ctx.commands.install_system_cli(
                cli["name"], cli["installer"], uninstall="scripts/uninstall.sh"
            )
            installed.append(cli["name"])

        mcp_doc = write_mcp_json(ctx.package_dir, config)

        ctx.routes.register(routes_mod.build_routes())

        log.info(
            "aw-app-mcp-tools activated: installed %s, mcp.json servers=%s, routes mounted",
            installed, list(mcp_doc["mcpServers"]),
        )

    async def on_config_saved(self, ctx) -> None:
        """Regenerate mcp.json from the newly-saved config (the raw
        mcpServers JSON the settings panel edits). aw-workspace's
        save_app_config calls this BEFORE telling the MCP Gateway to
        /reload — see this app's contributes.mcp.reload_on_save — so the
        gateway always scans the file this write just produced, never a
        stale one."""
        config = getattr(ctx, "config", {}) or {}
        mcp_doc = write_mcp_json(ctx.package_dir, config)
        log.info("aw-app-mcp-tools config saved: mcp.json servers=%s", list(mcp_doc["mcpServers"]))

    async def deactivate(self) -> None:
        log.info("aw-app-mcp-tools deactivated")
