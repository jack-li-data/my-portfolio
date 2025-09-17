from __future__ import annotations

from pathlib import Path

from app import create_app, load_projects
from flask import render_template

BASE_DIR = Path(__file__).parent.resolve()
DIST_DIR = BASE_DIR / "dist"


def build() -> Path:
    app = create_app()
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with app.app_context():
        html = render_template("index.html", projects=load_projects())
    out_file = DIST_DIR / "index.html"
    out_file.write_text(html, encoding="utf-8")
    return out_file


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out} ({out.stat().st_size} bytes)")
