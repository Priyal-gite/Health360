# Health360 Project Plan

## Project Objective
Explore patterns in heart disease, diabetes, and stroke by analyzing demographic, clinical, symptom, and lifestyle factors. The intended outcome is an interactive Tableau dashboard that helps healthcare teams recognize higher-risk population segments, monitor health patterns, inform preventive-care planning, support clinical review, and guide public-health resource allocation.

This project supports population-level exploration. It is not a diagnostic system, an individual clinical risk calculator, or a substitute for professional medical judgment.

## Users and Scenarios
- **Dr. Michael Carter, Clinical Risk Assessment Officer:** Review patient segments and indicators such as BMI, blood pressure, cholesterol, and glucose; spot potential high-risk cases for timely clinical follow-up.
- **Emily Rodriguez, Healthcare Data Analyst:** Compare disease prevalence with smoking, alcohol consumption, and exercise; investigate relationships using comparative charts, trend views, and heatmaps.
- **Dr. Priya Nair, Public Health Researcher:** Compare age groups, BMI categories, exercise patterns, and symptom prevalence; identify population segments for further study and prevention initiatives.

## Analysis Questions
- How does heart disease, diabetes, and stroke prevalence vary by age group and BMI category?
- How are blood pressure, cholesterol, glucose, and BMI distributions associated with each condition?
- How do smoking, alcohol use, and exercise patterns differ between groups with and without reported conditions?
- How do fatigue, chest pain, and dizziness reports vary across conditions and population segments?
- Which factors show the strongest observed associations with each condition, and which groups warrant further investigation?
- Where do prevalence patterns change over time, when the source data includes suitable dates and repeated observations?

## Data Requirements
Use an approved, de-identified dataset with documented definitions, provenance, coverage, and time period. Relevant fields include:
- **Demographics:** age or age group.
- **Clinical indicators:** BMI, blood pressure, cholesterol, and glucose.
- **Lifestyle:** smoking, alcohol consumption, and exercise level.
- **Symptoms:** fatigue, chest pain, and dizziness.
- **Outcomes:** heart disease, diabetes, and stroke indicators.
- **Time:** observation date or period, when available and appropriate for trend analysis.

Generated demo records are for interface testing only. Do not use them to estimate real prevalence, validate medical hypotheses, or make care decisions. Protect patient privacy and review data quality, missingness, bias, and category definitions before analysis.

## Dashboard Requirements
- Provide overview KPIs for population size, condition prevalence, and relevant high-risk segments.
- Compare the three conditions across age groups and BMI categories.
- Present clinical and lifestyle comparisons, with symptom views and heatmaps for exploring factor-condition relationships.
- Include time trends only when the data supports valid temporal comparisons.
- Provide coordinated filters for condition, age, BMI, and lifestyle, plus an appropriate patient or cohort review view.
- Make charts interpretable with clear denominators, labels, accessible color choices, and visible data-source caveats.
- Deliver the analytical dashboard in Tableau. A browser prototype may be used for interaction and layout development, but is not a substitute for the Tableau deliverable.

## Intended Use and Outcomes
- Support earlier review of potentially higher-risk individuals by qualified clinical staff.
- Help teams monitor population health patterns and target preventive-care strategies.
- Inform clinical decision-making and resource planning without presenting associations as causes.
- Help researchers identify vulnerable segments for follow-up study, awareness programs, and public-health policy development.
- Contribute to better prevention and treatment planning; improved patient outcomes are an intended long-term goal, not a result this prototype can claim.

## End-to-End Implementation Plan

### 1. Data Collection and Database Extraction
- Identify the source database, data owner, approved tables/views, observation period, and refresh cadence.
- Obtain data-owner and privacy/security approval before accessing or extracting any records. Use the minimum fields and rows needed for the population-level analysis.
- Document the source, extraction date, query or extraction procedure, field definitions, inclusion criteria, and record counts.
- Extract through an approved read-only connection into a restricted project location. Do not put credentials, direct identifiers, or patient-level data in source control, the Flask app, or public Tableau content.
- Confirm the permitted de-identification method and retain only the approved analysis dataset. If no eligible source is approved, keep the synthetic demo data clearly labeled and do not report real-world findings.

### 2. Data Preparation
- Profile schema, types, duplicates, missingness, invalid values, coverage, and category definitions.
- De-identify or aggregate as approved; remove direct identifiers and review small-cell disclosure risk before sharing results.
- Standardize units, labels, date handling, and categories. Derive age groups and BMI categories using documented rules; define clinical thresholds with a qualified stakeholder or an approved source.
- Record cleaning decisions, exclusions, missing-value handling, and known bias/coverage limitations in a data dictionary and preparation log.
- Reconcile source, prepared, and Tableau row counts and validate key condition counts and denominators against an independent calculation.

### 3. Tableau Data Connection and Calculations
- Connect Tableau to the approved database view or a governed extract. Select live connection versus extract based on source policy, refresh needs, and measured performance.
- Keep credentials in an approved credential store and configure least-privilege access. Document refresh and failure handling.
- Create and document calculated fields for age group, BMI category, condition flags, factor groups, prevalence numerator, prevalence denominator, and prevalence rate. Add a time-period field only if valid dated repeated observations exist.
- Validate each calculation against the prepared data before publishing. Maintain a calculation inventory with field name, formula, definition, and validation result.

### 4. Data Visualizations
- Build and review a target of **8 unique visualization types** (final count may change with supported source fields):
  1. KPI cards for population size and condition prevalence.
  2. Condition prevalence by age group.
  3. Condition prevalence by BMI category.
  4. Clinical indicator comparison by condition.
  5. Lifestyle comparison by condition.
  6. Symptom comparison by condition.
  7. Factor-condition heatmap with clear group definitions and denominators.
  8. Cohort or segment review table with privacy-safe fields.
- Add a time trend only where observation dates and repeated observations support a valid comparison; otherwise document why it is omitted.
- Provide titles, units, denominators, accessible color choices, tooltips, missing-data treatment, and source/limitation notes. Present associations as descriptive, not causal.

### 5. Tableau Dashboard Design and Responsiveness
- Compose the visualizations into a Tableau dashboard for desktop and supported smaller screens; define the supported viewport sizes during implementation.
- Add coordinated filters for condition, age group, BMI category, and lifestyle, plus reset behavior and clear filter state.
- Use dashboard actions only when their effect is clear and consistent. Check labels, overflow, legends, contrast, keyboard focus, and readable text at each supported size.
- Include the data period, source, last refresh, synthetic/real-data status, and non-diagnostic caveat on the dashboard.

### 6. Tableau Story
- Create a **4-scene story** (adjust if approved data cannot support a scene):
  1. Population and data coverage: source, period, population size, and limitations.
  2. Demographic patterns: condition prevalence by age and BMI.
  3. Clinical, lifestyle, symptom, and factor-condition comparisons.
  4. Population segments for further qualified review, with caveats and next questions.
- Give each scene a takeaway title and explanatory caption. Do not imply causation, diagnosis, or treatment advice.

### 7. Performance Testing
- Test with representative small, expected, and upper-bound data volumes; record the number of rows and columns loaded, extract/live mode, refresh duration, workbook size, and environment.
- Measure initial dashboard load time and filter/action response time. Record the test machine/browser, Tableau version, data source, network conditions, and repetitions so results can be reproduced.
- Exercise each filter alone and in combination, reset behavior, each calculated field, every visualization, and each story scene. Check for empty-result handling and correct denominators.
- Inventory the number of calculated fields and the number of worksheets/visualizations used by the dashboard and story. Review slow calculations, high-cardinality fields, excess marks, and redundant views.
- Capture baseline and final measurements and document issues and fixes. Set numeric pass thresholds with the project owner after the target deployment environment and expected data volume are known.

### 8. Web Integration with Flask
- Build a Flask application that serves the project landing page and embeds the published Tableau dashboard and story using Tableau's supported embedding approach.
- Configure the published content URL, authentication, authorization, and session handling for the intended audience. Keep secrets in environment-specific secret storage; never commit them.
- Make the embed container responsive, provide a useful loading/error state, and verify dashboard filters and story navigation work within the page.
- Apply access controls and privacy review before exposing the page. Do not publicly embed patient-level data or rely on hidden UI elements as access control.

### 9. Publishing and Release
- Publish the Tableau data source, workbook/dashboard, and story to the approved Tableau environment with the intended permissions and refresh schedule.
- Publish/deploy the Flask application to an approved environment; configure production settings, HTTPS, logging without sensitive values, and required access controls.
- Verify the published Tableau links and Flask embed as an authorized user and an unauthorized user. Record release version, owner, refresh date, and rollback procedure.
- Do not publish until dataset approval, calculation validation, privacy review, and stakeholder review are complete.

### 10. Demonstration and Documentation
- Record an end-to-end project demonstration video covering the data source and extraction, preparation and quality checks, Tableau connection, calculated fields, visualizations, dashboard filters/responsive layouts, story scenes, Flask embed, and published result.
- Use synthetic or approved de-identified data in the recording; do not show credentials, direct identifiers, or restricted records. Add captions or a transcript and note known limitations.
- Write step-by-step project documentation covering prerequisites, approved data access, extraction, preparation, Tableau connection, calculations, worksheet/dashboard/story construction, performance test procedure/results, Flask setup, configuration, publishing, troubleshooting, and maintenance.
- Include a data dictionary, calculation inventory, visualization/story inventory, privacy and limitations notes, and screenshots or links to approved deliverables.

## Current Prototype and Scaffolding Status
- [x] Standalone browser dashboard implemented in `index.html` using deterministic synthetic demo data.
- [x] Overview KPIs, prevalence by age group, clinical/lifestyle factor summaries, and a searchable, paginated synthetic cohort review implemented.
- [x] README features and instructions for opening the browser prototype added.
- [x] Add condition prevalence comparisons across BMI categories in the browser prototype.
- [x] Add a descriptive factor-condition prevalence heatmap comparing records with and without each factor. These are group comparisons in synthetic records, not correlation estimates or causal findings.
- [x] Add a simple Flask frontend serving the working browser dashboard and the four-scene story outline on the homepage; the app runs with no Tableau configuration.
- [x] Provide a deterministic synthetic CSV download matching the prototype cohort for Tableau connection and embed setup.
- [x] Add optional Tableau Embedding API v3 integration configured with published dashboard/story share URLs in `.env`; native Flask views remain available when URLs are blank.
- [x] Verify Flask landing, dashboard, story, health, synthetic CSV, and configured Tableau embed routes with a local Flask test client.
- [x] Add guarded single-query SQL extraction and canonical-field CSV preparation utilities with aggregate quality reporting.
- [x] Add Tableau build specification, performance measurement template, project runbook, and end-to-end demo video script.
- [ ] Add time-trend analysis if a suitable dated dataset is available. The current prototype has no dates or repeated observations.
- [ ] Replace demo data with an approved, de-identified dataset before reporting real-world findings. None is present in this workspace.
- [ ] Build, validate, and publish the Tableau dashboard when the dataset and Tableau environment are available. The current deliverable remains a browser prototype.

The prototype's focus-condition selector now updates the age and BMI prevalence views and scopes the cohort review to records reporting that condition. Age, BMI, and lifestyle filters update the population metrics and comparisons. The cohort review includes search and pagination and does not rank synthetic records by a fabricated clinical risk score.

### End-to-End Delivery Checklist
- [ ] Confirm source database, data owner approval, privacy constraints, analysis period, and refresh cadence.
- [ ] Extract the approved dataset and document provenance, extraction steps, and source record counts.
- [ ] Prepare and validate the analysis dataset; complete the data dictionary, cleaning log, and privacy review.
- [ ] Connect Tableau to the approved source or governed extract; document refresh behavior and access controls.
- [ ] Build and validate the documented calculation fields and target visualization inventory.
- [ ] Complete the responsive Tableau dashboard and coordinated filters.
- [ ] Complete the four-scene Tableau story, revising scenes to match fields supported by the approved data.
- [ ] Run performance tests and report data volume loaded, filter/action response, calculated-field count, visualization count, and story/dashboard results.
- [ ] Validate Tableau authentication, authorization, responsive behavior, and error/loading states against the published views in the target deployment.
- [ ] Publish Tableau assets and Flask application to approved environments after data, privacy, and stakeholder reviews.
- [ ] Record the end-to-end demonstration video using only synthetic or approved de-identified data.
- [ ] Deliver step-by-step project documentation, inventories, test results, limitations, and maintenance instructions.

## Acceptance Criteria
- The Tableau dashboard covers all three conditions and the requested demographic, clinical, lifestyle, and symptom factors supported by the source data.
- Users can compare disease prevalence by age group and BMI category and explore factor-condition patterns using clearly labeled views.
- Supported time trends, filters, and cohort comparisons use documented definitions and valid denominators.
- Findings distinguish observed association from causation and state data limitations; synthetic data is never presented as clinical evidence.
- Healthcare and public-health stakeholders can use the dashboard to identify segments for further review without treating it as an automated diagnosis or treatment recommendation.
- The source dataset, extraction procedure, preparation decisions, data dictionary, privacy review, and row-count reconciliation are documented.
- Tableau connection, refresh approach, calculated fields, and their validation are documented and reproducible.
- The final visualization and story-scene counts are inventoried; the dashboard responds correctly to coordinated filters and supported viewport sizes.
- Performance results include data volume, load and interaction measurements, calculation-field count, visualization count, test environment, and any unresolved issues.
- The Flask page embeds the authorized Tableau dashboard and story, handles loading/errors, and enforces access through authentication and authorization.
- Tableau assets and the Flask application are published to approved environments with release details and rollback steps.
- An end-to-end demonstration video and step-by-step development, setup, publishing, and maintenance documentation are delivered.

## Current Limitations
The workspace contains the standalone HTML prototype, data-pipeline scaffolding, a matching synthetic CSV download, and a Flask frontend with optional Tableau embedding. It still has no approved database connection, real dataset, published Tableau workbook/story, deployment environment, or measured performance results. The app has not been run against a real source. Generated records demonstrate interface behavior only; real prevalence, correlations, trends, clinical utility, and patient outcome improvements cannot be concluded until suitable data is analyzed and results are reviewed by qualified stakeholders.

## Plan Completion Audit

**Overall: partially complete.** The local synthetic-data prototype and supporting scaffolding exist; the full approved-data and Tableau deliverables are not complete.

| Workstream | Status | Evidence / remaining work |
|---|---|---|
| Browser prototype and Flask frontend | Complete for demo use | Filters, charts, cohort review, demo CSV, and homepage storyline are implemented. |
| Data collection and extraction | Scaffold only | A guarded extraction script exists. No approved source, access approval, or extracted real dataset is present. |
| Data preparation | Scaffold only | A mapping template and quality-report script exist. No approved dataset has been prepared or reconciled. |
| Tableau data connection and calculated fields | Not complete | The synthetic CSV can be opened in Tableau, but there is no Tableau workbook or documented/validated Tableau calculation inventory. |
| Tableau visualizations, dashboard, and story | Not complete | The eight-view specification and four-scene storyline are plans. No Tableau workbook, dashboard, or story is present. The Flask homepage displays the storyline outline. |
| Performance testing | Not complete | A test matrix exists, but dashboard/data-volume measurements have not been recorded. |
| Flask and Tableau integration | Partial | Flask frontend and optional Embedding API v3 routes are implemented. No Tableau URLs are configured, so the app currently serves its native Flask dashboard and homepage storyline. |
| Publishing and release | Not complete | No Tableau assets or Flask deployment have been published. |
| Demonstration and documentation | Partial | Runbook, build specification, performance plan, and video script exist. The end-to-end video and measured release documentation remain outstanding. |

The Tableau dashboard and story are **not currently being used**. The app has optional code to embed them after published HTTPS view URLs are configured, but neither `TABLEAU_DASHBOARD_URL` nor `TABLEAU_STORY_URL` is configured in this workspace. The current dashboard and storyline are served by Flask using synthetic data.
