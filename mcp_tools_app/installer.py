from __future__ import annotations

import subprocess
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = APP_ROOT / "scripts"
MCP_CONFIG = APP_ROOT / "mcp.json"


class InstallError(RuntimeError):
    pass


def _run_script(script: str, *, env_overrides: dict[str, str] | None = None) -> str:
    import os

    path = SCRIPTS_DIR / script
    env = dict(os.environ)
    if env_overrides:
        env.update(env_overrides)
    result = subprocess.run(
        ["bash", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    if result.returncode != 0:
        raise InstallError(
            f"{script} failed (exit {result.returncode}): {result.stderr.strip()}"
        )
    return result.stdout.strip()


def install_playwright_mcp(cdp_endpoint: str = "http://localhost:9223") -> str:
    return _run_script(
        "install_playwright_mcp.sh",
        env_overrides={"AW_PLAYWRIGHT_CDP_ENDPOINT": cdp_endpoint},
    )


def uninstall_playwright_mcp() -> None:
    _run_script("uninstall.sh")
