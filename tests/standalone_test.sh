#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

AW_HOME="${AW_WORKSPACE_HOME:-$HOME/.aw-workspace}"
AW_BIN_DIR="$AW_HOME/bin"
APP_DATA_DIR="$AW_HOME/apps/mcp-tools"

echo "== install_playwright_mcp.sh =="
bash scripts/install_playwright_mcp.sh

echo "== wrapper resolution =="
export PATH="$AW_BIN_DIR:$PATH"
which aw-playwright-mcp

echo "== config =="
test -f "$APP_DATA_DIR/mcp.json"
grep -q '"playwright"' "$APP_DATA_DIR/mcp.json"
grep -q '"npx"' "$APP_DATA_DIR/mcp.json"
grep -q '"http://aw-app-browser:9223"' "$APP_DATA_DIR/mcp.json"

echo "== idempotency re-run =="
bash scripts/install_playwright_mcp.sh

echo "OK: Playwright MCP wrappers and mcp.json installed"
