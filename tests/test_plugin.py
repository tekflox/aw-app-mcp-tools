from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mcp_tools_app.plugin import McpToolsAppPlugin, build_mcp_servers, write_mcp_json  # noqa: E402

PLAYWRIGHT_DEFAULT = {
    "playwright": {
        "enabled": True,
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@playwright/mcp@0.0.77", "--cdp-endpoint", "http://aw-app-browser:9223"],
    },
}


def test_build_mcp_servers_returns_config_mcp_servers_verbatim():
    servers = build_mcp_servers({"mcpServers": PLAYWRIGHT_DEFAULT})
    assert servers == PLAYWRIGHT_DEFAULT


def test_build_mcp_servers_missing_key_falls_back_to_default():
    # ctx.config at activate() time is un-defaulted (config_with_defaults is
    # an API-response-layer concern) — a fresh install's config is {}, so
    # this fallback is what keeps a first install from shipping empty.
    assert build_mcp_servers({}) == PLAYWRIGHT_DEFAULT


def test_build_mcp_servers_explicit_empty_object_yields_no_servers():
    # An explicit {} (the user cleared every server) is respected, distinct
    # from a missing key.
    assert build_mcp_servers({"mcpServers": {}}) == {}


def test_build_mcp_servers_lets_user_add_an_arbitrary_tool():
    config = {
        "mcpServers": {
            **PLAYWRIGHT_DEFAULT,
            "my-custom-tool": {"type": "stdio", "command": "my-tool", "args": []},
        }
    }
    servers = build_mcp_servers(config)
    assert set(servers) == {"playwright", "my-custom-tool"}


def test_write_mcp_json_writes_package_dir_mcp_json(tmp_path):
    write_mcp_json(str(tmp_path), {"mcpServers": PLAYWRIGHT_DEFAULT})
    written = json.loads((tmp_path / "mcp.json").read_text())
    assert set(written["mcpServers"]) == {"playwright"}


def _async(coro):
    return asyncio.run(coro)


def _fake_ctx(tmp_path, config):
    (tmp_path / "aw-app.json").write_text(json.dumps({"contributes": {}}))
    return SimpleNamespace(
        package_dir=str(tmp_path),
        config=config,
        commands=SimpleNamespace(install_system_cli=lambda *a, **k: None),
        routes=SimpleNamespace(register=lambda *a, **k: None),
    )


def test_activate_writes_mcp_json_from_config(tmp_path):
    plugin = McpToolsAppPlugin()
    ctx = _fake_ctx(tmp_path, {"mcpServers": PLAYWRIGHT_DEFAULT})
    _async(plugin.activate(ctx))
    written = json.loads((tmp_path / "mcp.json").read_text())
    assert set(written["mcpServers"]) == {"playwright"}


def test_activate_with_fresh_empty_config_still_ships_playwright(tmp_path):
    # Regression: a fresh install's ctx.config is {} (un-defaulted) — must
    # not write an empty mcp.json.
    plugin = McpToolsAppPlugin()
    ctx = _fake_ctx(tmp_path, {})
    _async(plugin.activate(ctx))
    written = json.loads((tmp_path / "mcp.json").read_text())
    assert set(written["mcpServers"]) == {"playwright"}


def test_on_config_saved_rewrites_mcp_json_to_match_new_config(tmp_path):
    plugin = McpToolsAppPlugin()
    ctx = _fake_ctx(tmp_path, {"mcpServers": PLAYWRIGHT_DEFAULT})
    _async(plugin.activate(ctx))
    assert set(json.loads((tmp_path / "mcp.json").read_text())["mcpServers"]) == {"playwright"}

    ctx.config = {
        "mcpServers": {
            **PLAYWRIGHT_DEFAULT,
            "extra": {"type": "stdio", "command": "extra-tool", "args": []},
        }
    }
    _async(plugin.on_config_saved(ctx))
    written = json.loads((tmp_path / "mcp.json").read_text())
    assert set(written["mcpServers"]) == {"playwright", "extra"}
