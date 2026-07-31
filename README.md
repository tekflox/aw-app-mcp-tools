# aw-app-mcp-tools

AW decoupled app that installs MCP helper tools into a workspace.

The first tool bundle is Playwright MCP:

- `mcp.json` contributes a `playwright` stdio server that runs `npx -y @playwright/mcp@0.0.77` from the MCP Gateway container.
- The contributed Playwright server connects to the shared AW Browser CDP endpoint at `http://aw-app-browser:9223`.
- `aw-playwright-mcp` is still installed into the workspace bin for local/manual use.
- `mcp.json` is bundled in the repo and installed to `$AW_WORKSPACE_HOME/apps/mcp-tools/mcp.json`.

The installed config is scanned by `aw-app-mcp-gateway`:

```json
{
  "mcpServers": {
    "playwright": {
      "enabled": true,
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@0.0.77",
        "--cdp-endpoint",
        "http://aw-app-browser:9223"
      ]
    }
  }
}
```

The checked-in `mcp.json` is the same file the installer copies into the
workspace app data directory, so updates to the bundled MCP config travel
through normal app releases.

## Development

```bash
python -m pytest tests -q
cd ui && npm run build
python -m mcp_tools_app
```

Pushes to `master` call `tekflox/aw-marketplace`'s reusable app release
workflow, which validates the manifest/tests, tags a release, and opens the
marketplace sync PR.
