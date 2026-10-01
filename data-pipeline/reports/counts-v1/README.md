# Counts-only model research

Retrain from the repository root:

```powershell
.venv/Scripts/python.exe data-pipeline/train_count_model.py
.venv/Scripts/python.exe -m unittest discover -s data-pipeline/tests
```

The command hashes and parses the actual 2022/2024 NCRB workbooks, uses the explicit **Total Crime against Women** column, checks all Delhi/Haryana/UP reporting-unit sums against workbook state totals, saves the reviewed name mapping, fits Poisson GLM and LightGBM count-only ablations, and compares them against last-observation persistence. No UI or app feed is modified.

`observations.csv/json` contains source-backed total counts, reporting years, source worksheet rows/hashes and source category inconsistencies. `evaluation.json` contains whole-district and whole-city holdout predictions, per-city metrics, temporal persistence results, calibration bins, bootstrap error uncertainty, seed comparisons and held-out permutation importance. Model files and training/config snapshots are under `data-pipeline/artifacts/counts-v1/` (ignored by Git). JSON never uses NaN for unavailable metrics.

`district-research-export.json` contains factual district totals and unknown risk entries for all twelve day/band combinations. Its annual persistence value is an **estimate**, not a new measured total. `neighbourhoods.geojson` is deliberately empty because matching police boundaries, a ward/H3 crosswalk and allocation context are not available. No PMTiles archive can honestly be generated from missing geometry. Existing `tiles.py` can tile reviewed app-schema geometries once they exist; it is not run here.

The separate `annual_count_forecast` object is for 2026: persistence from 2024 and exploratory pooled-bootstrap intervals over a matching two-year horizon. It is estimated research output, not a calibrated prediction of safety. Its reporting year is separate from the observed source year. The model card states the interval assumptions.

## Inputs to add when available

No placeholder observations are trained. SafeCity, Safetipin and RTI remain optional raw inputs under `raw/safecity/`, `raw/safetipin/` and `raw/rti/`; the counts-v1 run does not consume them until their schemas, privacy and reporting units have been reviewed.

Historical context may be supplied in `data-pipeline/interim/counts-v1/night-context.json` as a list with `unit_id`, `year`, `night_context` (0–1), `inventory_complete`, `boundary_verified` and `source_list`. Only a context snapshot whose year equals the feature cutoff is allowed into a historical backtest. A 2026 OSM snapshot must not be disguised as 2022 context. Incomplete scores stay missing; training includes context only when every example has reviewed evidence.

`police-adjacency.json` has `boundary_verified`, `source_list`, `valid_years` and an `adjacency` dictionary keyed by reporting-unit ID. Unverified adjacency is rejected; unknown neighbours are rejected rather than silently filled with zero. The smoothing formula is 80% own previous count plus 20% neighbouring mean. Without matching boundaries, smoothing remains unavailable, rather than guessed from revenue district names.

`count_model.downscale` provides a tested allocator for a complete reviewed district partition. Each zone requires a unique `id`, one `district_id`, `crosswalk_verified`, measured `density`, `road_density` and `built_up`. It equally combines the three within-district normalized weights, corrects floating-point residuals, and returns **estimated** fractional counts whose sum equals the reported district total. It rejects missing values, zero-information weights and mixed jurisdictions. This utility does not manufacture geometry, nor does its existence mean any real neighbourhood allocation has been performed.

`config/time_factors.yaml` is JSON-compatible YAML with neutral factors. All time outputs are assumed; no four-hour observed count, night hotspot or weekday/weekend difference is asserted. `count_model.scores` implements percentile ranking and unknown handling, but production neighbourhood ranks are not emitted until supporting inputs and validation exist.

## Deliberate limits

Two complete annual observations per district support one two-year persistence backtest. They do **not** support training a learned model on earlier lag/target pairs and testing it on 2024. Whole-city tests have one district each outside Delhi. The count-only learned ablations are retrospective transfer experiments, not validated three-input risk models. No random train/test splits are used.

Population rates, socio-economic variables, CCTV, police distance and other prohibited predictors are absent. Population/density can later support allocation and night context; it is not a target denominator. Export confidence is a completeness heuristic, not a probability that an individual will experience crime.
