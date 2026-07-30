from __future__ import annotations

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import build_routes

SLUG = "mcp-tools"
DEFAULT_PORT = 9406

APP_ROOT = Path(__file__).resolve().parent.parent
UI_DIST = APP_ROOT / "ui" / "dist"


def build_standalone_app() -> FastAPI:
    app = FastAPI(title="mcp-tools (standalone)")
    app.mount(f"/api/apps/{SLUG}", build_routes())

    if UI_DIST.is_dir():
        app.mount("/", StaticFiles(directory=UI_DIST, html=True), name="ui")

    return app


app = build_standalone_app()


def main() -> None:
    if not UI_DIST.is_dir():
        print(f"NOTE: {UI_DIST} not built yet - run `npm run build` in ui/ first.")
    port = int(os.environ.get("PORT", str(DEFAULT_PORT)))
    host = os.environ.get("AW_APP_HOST", "127.0.0.1")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
