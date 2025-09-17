from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Dict

from flask import Flask, render_template


# Paths
BASE_DIR = Path(__file__).parent.resolve()
PROJECTS_JSON = BASE_DIR / "projects.json"


def load_projects() -> List[Dict[str, Any]]:
    """Load projects from the local JSON file.

    Returns an empty list if the file is missing or invalid.
    """
    try:
        with PROJECTS_JSON.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except FileNotFoundError:
        print("Warning: projects.json not found. Showing empty project list.")
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse projects.json: {e}")
    return []


def create_app() -> Flask:
    """Application factory (Flask 3+)"""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.update(TEMPLATES_AUTO_RELOAD=True)

    @app.get("/")
    def index():
        projects = load_projects()
        return render_template("index.html", projects=projects)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    # Support running via `python app.py` in addition to `flask --app app run`.
    app = create_app()
    app.run(debug=True)
