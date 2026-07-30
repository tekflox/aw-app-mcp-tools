# aw-app-mcp-tools

AW decoupled app that installs MCP helper tools into a workspace.

The first tool bundle is Playwright MCP:

- `aw-playwright-mcp` runs `@playwright/mcp@0.0.77` against the shared AW browser CDP endpoint, defaulting to `http://localhost:9223`.
- `aw-playwright-local-mcp` runs `@playwright/mcp@0.0.77 --isolated`.
- `mcp.json` is bundled in the repo and installed to `$AW_WORKSPACE_HOME/apps/mcp-tools/mcp.json`.

The installed config uses the wrapper commands, so clients can add:

```json
{
  "mcpServers": {
    "playwright": {
      "enabled": true,
      "type": "stdio",
      "command": "aw-playwright-mcp",
      "args": []
    },
    "playwright-local": {
      "enabled": true,
      "type": "stdio",
      "command": "aw-playwright-local-mcp",
      "args": []
    }
  }
}
```

## Development

```bash
python -m pytest tests -q
cd ui && npm run build
python -m mcp_tools_app
```

The release workflow is inherited from `aw-app-template`: pushes to `master`
call `tekflox/aw-marketplace`'s reusable app release workflow, which validates
the manifest/tests, tags a release, and opens the marketplace sync PR.
