#!/usr/bin/env bash
set -euo pipefail

APP_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AW_HOME="${AW_WORKSPACE_HOME:-$HOME/.aw-workspace}"
AW_BIN_DIR="$AW_HOME/bin"
APP_DATA_DIR="$AW_HOME/apps/mcp-tools"
MCP_CONFIG="$APP_DATA_DIR/mcp.json"

mkdir -p "$AW_BIN_DIR" "$APP_DATA_DIR"
cp "$APP_ROOT/mcp.json" "$MCP_CONFIG"

cat > "$AW_BIN_DIR/aw-playwright-mcp" <<'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail
exec npx -y @playwright/mcp@0.0.77 --cdp-endpoint "${AW_PLAYWRIGHT_CDP_ENDPOINT:-http://aw-app-browser:9223}" "$@"
SCRIPT

chmod +x "$AW_BIN_DIR/aw-playwright-mcp"

echo "Playwright MCP config installed at $MCP_CONFIG"
