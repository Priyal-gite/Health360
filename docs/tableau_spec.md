# Tableau Build Specification

This is the build specification for the Tableau deliverable. No Tableau workbook is included yet because this workspace has no approved dataset or Tableau environment.

## Data source and fields

Use only the approved prepared dataset. Confirm field definitions, reporting period, units, refresh mode, and row counts with the data owner. The preparation utility accepts these canonical fields when available:

`age`, `bmi`, `systolic_bp`, `cholesterol`, `glucose`, `smoker`, `alcohol_use`, `exercise_level`, `fatigue`, `chest_pain`, `dizziness`, `heart_disease`, `diabetes`, `stroke`, and `observation_date`.

Map only approved source columns in `config/field_mapping.example.json`. Do not add direct identifiers to the analysis extract. Confirm the definitions and handling of missing values before building rates.

## Calculated field inventory (planned)

| Field | Definition to implement | Validation |
|---|---|---|
| Age group | `18–39`, `40–54`, `55–69`, `70+` using the documented age boundaries | Compare counts to independent grouped counts |
| BMI category | Categories and cutoffs approved by the data owner/domain reviewer | Compare counts to independent grouped counts |
| Condition flag | Source outcome normalized to a documented Boolean/category | Compare positive/negative/missing counts to prepared data |
| Factor group | Documented categories for each source lifestyle, clinical, or symptom field | Confirm categories and denominators |
| Population denominator | Count of eligible records for the current filters and view | Reconcile to filtered source row count |
| Condition numerator | Eligible records with the selected condition | Reconcile to prepared condition counts |
| Prevalence rate | Condition numerator divided by eligible denominator; null when denominator is zero | Independently recompute for selected filter combinations |
| Observation period | Approved date or period grain, only if repeated dated observations are valid | Confirm period coverage and duplicates |

Keep a field-level inventory with the final Tableau formula, owner, decision, and validation status. Do not interpret these descriptive measures as causal estimates.

## Eight planned visualizations

1. KPI cards: eligible population, condition prevalence, and selected condition count.
2. Condition prevalence by age group.
3. Condition prevalence by BMI category.
4. Clinical indicator comparisons by condition (distributions or threshold shares supported by the source).
5. Lifestyle comparisons by condition.
6. Symptom comparisons by condition.
7. Factor-condition heatmap comparing clearly defined groups, with denominator tooltips.
8. Privacy-reviewed cohort/segment table; omit row-level details if approval does not permit them.

Add a dated trend only when approved repeated observations support a valid comparison. A single cross-sectional row per person does not establish a trend.

## Dashboard and story layout

- Dashboard filters: condition, age group, BMI category, lifestyle; provide a reset action and visible current state.
- Show source, coverage period, refresh date, missingness caveats, denominator definitions, and non-diagnostic wording.
- Design desktop and narrow-screen layouts; validate legibility, overflow, keyboard use, color contrast, and filter interactions at each supported size.
- Story scene 1: data coverage and population.
- Story scene 2: age and BMI comparisons.
- Story scene 3: clinical, lifestyle, symptom, and factor comparisons.
- Story scene 4: segments for qualified follow-up and open questions.
- Use takeaway titles and captions. Revise scenes to match approved source coverage and suppress unsafe small cells.
