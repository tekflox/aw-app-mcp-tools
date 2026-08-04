#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp_tools_app import installer  # noqa: E402


class McpToolsInstallerTest(unittest.TestCase):
    @patch("mcp_tools_app.installer.subprocess.run")
    def test_install_playwright_mcp_runs_script_with_cdp_endpoint(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Playwright MCP config installed at /home/test/.aw-workspace/data/mcp-tools/mcp.json\n",
            stderr="",
        )

        out = installer.install_playwright_mcp("http://localhost:9223")

        self.assertIn("mcp.json", out)
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0][-1], str(installer.SCRIPTS_DIR / "install_playwright_mcp.sh"))
        self.assertEqual(kwargs["env"]["AW_PLAYWRIGHT_CDP_ENDPOINT"], "http://localhost:9223")

    @patch("mcp_tools_app.installer.subprocess.run")
    def test_install_playwright_mcp_raises_on_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="boom")

        with self.assertRaises(installer.InstallError):
            installer.install_playwright_mcp()

    @patch("mcp_tools_app.installer.subprocess.run")
    def test_uninstall_playwright_mcp_runs_uninstall_script(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        installer.uninstall_playwright_mcp()

        args, _ = mock_run.call_args
        self.assertEqual(args[0][-1], str(installer.SCRIPTS_DIR / "uninstall.sh"))


if __name__ == "__main__":
    unittest.main()
