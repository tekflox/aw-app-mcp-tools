from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mcp_tools_app.plugin import McpToolsAppPlugin, build_mcp_servers, write_mcp_json  # noqa: E402


def test_build_mcp_servers_both_tools_enabled_by_default():
    servers = build_mcp_servers({})
    assert set(servers) == {"playwright", "mcp-tools-echo"}
    assert servers["playwright"]["command"] == "npx"
    assert "http://aw-app-browser:9223" in servers["playwright"]["args"]
    assert servers["mcp-tools-echo"]["command"] == "python3"
    assert servers["mcp-tools-echo"]["args"] == ["-m", "mcp_tools_app.echo_server"]


def test_build_mcp_servers_playwright_disabled():
    servers = build_mcp_servers({"tool_playwright_enabled": False})
    assert "playwright" not in servers
    assert "mcp-tools-echo" in servers


def test_build_mcp_servers_echo_disabled():
    servers = build_mcp_servers({"tool_echo_enabled": False})
    assert "playwright" in servers
    assert "mcp-tools-echo" not in servers


def test_build_mcp_servers_both_disabled_yields_no_servers():
    servers = build_mcp_servers({"tool_playwright_enabled": False, "tool_echo_enabled": False})
    assert servers == {}


def test_build_mcp_servers_uses_custom_cdp_endpoint():
    servers = build_mcp_servers({"playwright_cdp_endpoint": "http://custom:9999"})
    assert "http://custom:9999" in servers["playwright"]["args"]


def test_write_mcp_json_writes_package_dir_mcp_json(tmp_path):
    write_mcp_json(str(tmp_path), {"tool_echo_enabled": False})
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
    ctx = _fake_ctx(tmp_path, {"tool_echo_enabled": False})
    _async(plugin.activate(ctx))
    written = json.loads((tmp_path / "mcp.json").read_text())
    assert set(written["mcpServers"]) == {"playwright"}


def test_on_config_saved_rewrites_mcp_json_to_match_new_config(tmp_path):
    plugin = McpToolsAppPlugin()
    ctx = _fake_ctx(tmp_path, {})
    _async(plugin.activate(ctx))
    assert set(json.loads((tmp_path / "mcp.json").read_text())["mcpServers"]) == \
        {"playwright", "mcp-tools-echo"}

    ctx.config = {"tool_playwright_enabled": False}
    _async(plugin.on_config_saved(ctx))
    written = json.loads((tmp_path / "mcp.json").read_text())
    assert set(written["mcpServers"]) == {"mcp-tools-echo"}
