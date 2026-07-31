from __future__ import annotations

import json
import logging
import os

from . import routes as routes_mod

log = logging.getLogger("aw_apps.mcp_tools")


class McpToolsAppPlugin:
    async def activate(self, ctx) -> None:
        with open(os.path.join(ctx.package_dir, "aw-app.json"), encoding="utf-8") as f:
            manifest = json.load(f)

        cdp_endpoint = (
            (getattr(ctx, "config", {}) or {}).get("playwright_cdp_endpoint")
            or "http://aw-app-browser:9223"
        )
        os.environ["AW_PLAYWRIGHT_CDP_ENDPOINT"] = str(cdp_endpoint)

        installed = []
        for cli in manifest.get("contributes", {}).get("system_clis", []):
            ctx.commands.install_system_cli(
                cli["name"], cli["installer"], uninstall="scripts/uninstall.sh"
            )
            installed.append(cli["name"])

        ctx.routes.register(routes_mod.build_routes())

        log.info(
            "aw-app-mcp-tools activated: installed %s (cdp_endpoint=%s), routes mounted",
            installed,
            cdp_endpoint,
        )

    async def deactivate(self) -> None:
        log.info("aw-app-mcp-tools deactivated")
