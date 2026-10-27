# Project Development Runbook

## Current state

The repository contains a deterministic synthetic browser prototype and a Flask frontend that serves the dashboard and a story outline. It does not contain a source database, approved analysis dataset, Tableau workbook, or published Tableau view. Do not treat demo output as health evidence.

## Local setup

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment: `py -m venv .venv`, then `\.venv\Scripts\Activate.ps1` on Windows (or `source .venv/bin/activate` on macOS/Linux). If `py` is unavailable, use `python -m venv .venv`.
3. Install dependencies: `python -m pip install -r requirements.txt`.
4. Optionally copy `.env.example` to `.env`; Flask reads its simple `KEY=VALUE` settings automatically. Leave Tableau URLs empty to use the Flask dashboard and story outline.
5. Run locally with `python app.py`, then open `http://127.0.0.1:5000`. Choose Dashboard to open the working synthetic prototype or Story outline to see the planned narrative. The built-in Flask server is for local development only.
6. Download the matching Tableau demo file from `http://127.0.0.1:5000/demo-data.csv` or the home page. In Tableau Desktop, connect to this CSV and build/publish the views. To embed them in Flask, paste the dashboard/story **Share > Copy Link** URLs into `TABLEAU_DASHBOARD_URL` / `TABLEAU_STORY_URL` in `.env`, then restart Flask. Use HTTPS view URLs. Leave either variable blank to keep the corresponding Flask fallback page.

## Approved database extraction

1. Obtain source-owner, privacy, and security approval; confirm minimum required fields and an approved read-only database account.
2. Install the optional extractor dependency with `python -m pip install -r requirements-data.txt`, plus the SQLAlchemy dialect/driver appropriate for the approved database. Drivers are source-specific and are not included because the source database is unknown.
3. Set `DATABASE_URL`, `SOURCE_QUERY`, and `EXTRACTION_APPROVED=true` in a restricted shell/session. The query utility allows one SELECT or read-only CTE query, but database-side read-only permissions remain mandatory.
4. Choose a destination outside source control and protected by the approved storage controls. Run `python scripts/extract_database.py --output <restricted-path>`.
5. Record extraction metadata, row counts, columns, and approval reference without putting credentials or patient data in project documentation.

## Data preparation

1. Copy `config/field_mapping.example.json` to a restricted mapping file and map canonical field names to the approved source headers. Omit fields that are unavailable; never map direct identifiers.
2. The three outcome fields are required for the current project scope. If the approved source does not include all three, obtain stakeholder approval to revise the scope before changing the script's required outcomes.
3. Run `python scripts/prepare_dataset.py --input <restricted-input.csv> --mapping <restricted-mapping.json> --output <restricted-prepared.csv>`.
4. Review the adjacent `.quality.json` report, resolve invalid values, check missingness and duplicate counts, and independently reconcile the row counts and outcome denominators. The script writes only whitelisted canonical fields and does not silently remove incomplete rows.
5. Confirm age/BMI categories, thresholds, units, time coverage, bias, and small-cell privacy with the data owner/domain reviewer. Document the decisions before Tableau analysis.

## Tableau construction and integration

Follow `docs/tableau_spec.md` for the planned calculated fields, eight visualization types, dashboard interactions, and four-scene story. The synthetic CSV lets you try the Tableau connection before an approved real dataset exists; label it as synthetic in every view. Validate calculations against prepared data and publish only to an approved Tableau site with approved permissions and refresh behavior. Tableau embedding uses the hosted Embedding API v3 and the URL variables above; Tableau controls authentication and view permissions.

## Performance, publishing, and handoff

Complete `docs/performance_test_plan.md` with actual measurements. Choose numeric acceptance thresholds with the project owner for the target environment. Deploy Flask with a production WSGI server, HTTPS, approved access controls, and secret management; do not use Flask's development server in production. Verify authorized and unauthorized access before release and record the version and rollback procedure.

Use `docs/demo_video_script.md` for the demonstration. Deliver the data dictionary, extraction/preparation log, calculation inventory, visualization/story inventory, performance results, source limitations, operating instructions, and video transcript with the project.
