# Performance Test Plan and Results

Run this plan after the Tableau workbook is connected to representative data and published to a test environment. Do not fill in expected results before measuring them.

## Test setup

Record the test date, tester, Tableau Server/Cloud version, browser/version, machine, network, source database, live/extract mode, extract refresh time, workbook size, and repeat count. Use approved test data with direct identifiers removed.

## Measurement matrix

| Scenario | Rows loaded | Columns loaded | Calculated fields | Worksheets / unique visualizations | Dashboard/story scenes | Initial load (s) | Filter/action response (s) | Result / notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Small representative volume | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Pending approved data |
| Expected production volume | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Pending source estimate |
| Upper-bound volume | TBD | TBD | TBD | TBD | TBD | TBD | Pending source estimate |

## Procedure

1. Record actual rows and columns in the prepared source and Tableau data model; record extract size and refresh duration if using an extract.
2. Measure initial dashboard load in a clean browser session at least five times; record median and range.
3. Measure each filter separately, all filters together, reset, and each dashboard action at least five times. Record median and range.
4. Open all eight planned visualization types and all supported story scenes; verify no broken views, slow calculations, misleading empty states, or incorrect denominators.
5. Repeat at each supported dashboard viewport and with the expected and upper-bound data volumes.
6. Record calculated-field count, worksheets, unique visualization types, marks/row counts where relevant, issues, changes, and post-change results.
7. Have the project owner approve numeric performance thresholds for the target environment before declaring a pass.

## Result status

Not run: there is no approved dataset, Tableau workbook, or deployment environment in this workspace yet.
