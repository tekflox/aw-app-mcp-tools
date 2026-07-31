#!/usr/bin/env bash
set -euo pipefail

AW_HOME="${AW_WORKSPACE_HOME:-$HOME/.aw-workspace}"
AW_BIN_DIR="$AW_HOME/bin"
APP_DATA_DIR="$AW_HOME/apps/mcp-tools"

rm -f "$AW_BIN_DIR/aw-playwright-mcp"
rm -f "$APP_DATA_DIR/mcp.json"
rmdir "$APP_DATA_DIR" 2>/dev/null || true
