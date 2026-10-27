"""Local Flask frontend for the Health360 browser prototype."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, Response, redirect, render_template, send_from_directory, url_for

from demo_data import csv_text


def load_local_env() -> None:
    """Load simple KEY=VALUE settings from .env without an extra dependency."""
    env_file = Path(__file__).with_name(".env")
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if value[:1] in ("'", '"') and value[-1:] == value[:1]:
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)


load_local_env()


def _tableau_view(view_env: str) -> dict[str, str] | None:
    view_url = os.environ.get(view_env, "").strip()
    if not view_url:
        return None
    parsed = urlparse(view_url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.port not in (None, 443)
    ):
        raise ValueError(f"{view_env} must be an HTTPS Tableau Share > Copy Link URL.")
    origin = f"https://{parsed.hostname}"
    return {
        "url": view_url,
        "origin": origin,
        "api_url": f"{origin}/javascripts/api/tableau.embedding.3.latest.min.js",
    }


app = Flask(__name__)
TABLEAU_VIEWS = {
    "dashboard": _tableau_view("TABLEAU_DASHBOARD_URL"),
    "story": _tableau_view("TABLEAU_STORY_URL"),
}
TABLEAU_ORIGINS = sorted({view["origin"] for view in TABLEAU_VIEWS.values() if view})


@app.context_processor
def template_settings():
    return {"tableau_views": TABLEAU_VIEWS}


@app.after_request
def security_headers(response):
    sources = " ".join(TABLEAU_ORIGINS)
    frame_sources = sources if sources else "'none'"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        f"script-src 'self' 'unsafe-inline' {sources}; "
        f"style-src 'self' 'unsafe-inline' {sources}; "
        f"frame-src {frame_sources}; "
        f"connect-src 'self' {sources}; "
        "img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'self'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.get("/")
def index():
    return render_template("home.html")


@app.get("/dashboard")
def dashboard():
    view = TABLEAU_VIEWS["dashboard"]
    if view:
        return render_template("tableau.html", title="Interactive dashboard", view=view)
    return send_from_directory(app.root_path, "index.html")


@app.get("/prototype")
def prototype():
    return send_from_directory(app.root_path, "index.html")


@app.get("/story")
def story():
    return redirect(url_for("index") + "#storyline")


@app.get("/demo-data.csv")
def download_demo_data():
    return Response(
        csv_text(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=health360_synthetic_demo.csv"},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
    )
