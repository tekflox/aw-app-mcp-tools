from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from . import routes as routes_mod

log = logging.getLogger("aw_apps.mcp_tools")

DEFAULT_CDP_ENDPOINT = "http://aw-app-browser:9223"


def build_mcp_servers(config: dict) -> dict:
    """The ``mcpServers`` object this app's own root mcp.json should
    contain, computed from config — the per-tool enable/disable toggles
    (``tool_<name>_enabled``) plus playwright_cdp_endpoint. This exact file
    is what aw-mcp-gateway's app-scan reads directly (ADR "aw-app-mcp-tools
    contributes mcp.json"), so disabling a tool here means it's gone from
    the gateway's tools/list after the next reload — not just hidden."""
    config = config or {}
    servers: dict = {}

    if config.get("tool_playwright_enabled", True):
        cdp_endpoint = config.get("playwright_cdp_endpoint") or DEFAULT_CDP_ENDPOINT
        servers["playwright"] = {
            "enabled": True,
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@playwright/mcp@0.0.77", "--cdp-endpoint", str(cdp_endpoint)],
        }

    if config.get("tool_echo_enabled", True):
        servers["mcp-tools-echo"] = {
            "enabled": True,
            "type": "stdio",
            "command": "python3",
            "args": ["-m", "mcp_tools_app.echo_server"],
        }

    return servers


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
        cdp_endpoint = config.get("playwright_cdp_endpoint") or DEFAULT_CDP_ENDPOINT
        os.environ["AW_PLAYWRIGHT_CDP_ENDPOINT"] = str(cdp_endpoint)

        installed = []
        for cli in manifest.get("contributes", {}).get("system_clis", []):
            ctx.commands.install_system_cli(
                cli["name"], cli["installer"], uninstall="scripts/uninstall.sh"
            )
            installed.append(cli["name"])

        mcp_doc = write_mcp_json(ctx.package_dir, config)

        ctx.routes.register(routes_mod.build_routes())

        log.info(
            "aw-app-mcp-tools activated: installed %s (cdp_endpoint=%s), "
            "mcp.json servers=%s, routes mounted",
            installed, cdp_endpoint, list(mcp_doc["mcpServers"]),
        )

    async def on_config_saved(self, ctx) -> None:
        """Regenerate mcp.json from the newly-saved config (tool toggles /
        CDP endpoint). aw-workspace's save_app_config calls this BEFORE
        telling the MCP Gateway to /reload — see this app's
        contributes.mcp.reload_on_save — so the gateway always scans the
        file this write just produced, never a stale one."""
        config = getattr(ctx, "config", {}) or {}
        cdp_endpoint = config.get("playwright_cdp_endpoint") or DEFAULT_CDP_ENDPOINT
        os.environ["AW_PLAYWRIGHT_CDP_ENDPOINT"] = str(cdp_endpoint)
        mcp_doc = write_mcp_json(ctx.package_dir, config)
        log.info("aw-app-mcp-tools config saved: mcp.json servers=%s", list(mcp_doc["mcpServers"]))

    async def deactivate(self) -> None:
        log.info("aw-app-mcp-tools deactivated")
