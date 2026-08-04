# aw-app-mcp-tools

AW decoupled app that installs MCP helper tools into a workspace. Ships with
**`playwright`** pre-configured — runs `npx -y @playwright/mcp@0.0.77` from
the MCP Gateway container, connected to the shared AW Browser CDP endpoint
(`http://aw-app-browser:9223`).

`mcp_tools_app/echo_server.py` is a trivial `echo` tool kept around as an
example of a second stdio server — not enabled by default, add it back via
the settings JSON (see below) if you want to exercise it.

## Settings is a raw JSON editor over mcpServers — no fixed tool list

This app's config schema has exactly one field, `mcpServers` — the literal
`mcpServers` object this app's `mcp.json` will contain. The Apps view gear
icon opens a raw JSON editor (`JsonConfigEditor` in aw-workspace-ui) over
this field, not a generated toggle form — so you can add, remove, or edit
*any* MCP server definition, not just flip booleans on a fixed set shipped
by this app.

`mcp.json` (what `aw-mcp-gateway`'s app-scan reads directly —
`contributes.mcp.reload_on_save: true` in `aw-app.json`) is **regenerated
from config**, not a fixed file:

- `McpToolsAppPlugin.activate()` writes it on install/start.
- `McpToolsAppPlugin.on_config_saved()` rewrites it every time this app's
  settings are saved — `build_mcp_servers(config)` just returns
  `config["mcpServers"]` verbatim (see `tests/test_plugin.py`).
- Right after `on_config_saved` returns, aw-workspace's `save_app_config`
  route calls the installed `mcp-gateway` app's `POST /reload` (its
  internal container address, not the public route) so the change takes
  effect immediately — no gateway restart, see aw-workspace's
  `_reload_mcp_gateway`.

The checked-in root `mcp.json` mirrors the config schema's default (just
`playwright`) so a fresh checkout — before the plugin ever activates — still
has a working file to scan.

## Development

```bash
python -m pytest tests -q
cd ui && npm run build
python -m mcp_tools_app
```

Pushes to `master` call `tekflox/aw-marketplace`'s reusable app release
workflow, which validates the manifest/tests, tags a release, and opens the
marketplace sync PR.
