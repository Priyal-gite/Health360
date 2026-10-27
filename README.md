# Health360

## Start the app

In PowerShell, from this project folder, run this one command:

```powershell
.\run-health360.bat
```

On first run it creates the Python environment and installs Flask. Then open `http://127.0.0.1:5000`. Keep the terminal window open; press **Ctrl+C** there to stop the app.

If the app was already running before you updated the project, stop the old server with **Ctrl+C** in its terminal, then run the command above again. The old server does not load new routes until restarted. This fixes the `/demo-data.csv` not found issue.

## Use Tableau (optional)

1. Start Flask using the command above. Download the synthetic Tableau-ready CSV from the home page or open `http://127.0.0.1:5000/demo-data.csv`.
2. In Tableau Desktop, open that downloaded CSV and create/publish the dashboard or story. In Tableau, copy the published view's **Share → Copy Link** URL.
3. Copy `.env.example` to `.env`, paste the URL into `TABLEAU_DASHBOARD_URL` and, if you publish a story, `TABLEAU_STORY_URL`. Restart Flask. It will embed the published views automatically. Leave a URL blank to use the working Flask page for that view.

The CSV contains 320 deterministic **synthetic** records that match the browser prototype. They are for interface testing only, not health evidence. Tableau account sign-in, workbook authoring, and publishing still happen in Tableau; Flask needs no Tableau configuration until you have a published URL.

## More detail

- [End-to-end project plan](/D:/Health360/Health360/plan.md)
- [Step-by-step runbook](/D:/Health360/Health360/docs/project_runbook.md)
- [Tableau workbook specification](/D:/Health360/Health360/docs/tableau_spec.md)
- [Performance measurement plan](/D:/Health360/Health360/docs/performance_test_plan.md)
- [Demo video outline](/D:/Health360/Health360/docs/demo_video_script.md)

Database extraction is optional. It requires approved database access and is documented in the runbook.
