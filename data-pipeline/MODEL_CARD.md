# Kaali model card — counts-v1

## Purpose and status

Research forecasting of **recorded annual total crimes against women**, not individual safety or current danger. This counts-only study supersedes the earlier selected-rape-head experiment for the latest task. No UI or public app data is changed. Modelled and assumed values are never measured facts.

**Selected model: historical-count persistence.** Actual Poisson GLM and LightGBM artifacts were trained and saved, but are count-only ablations because complete night context is missing. A complete three-input neighbourhood risk model has **not** been validated or published.

## Data and label strategy

Two existing local NCRB-titled district workbooks, reporting years **2022 and 2024**, provide 38 actual total-count observations: 15 Delhi police districts plus Gurugram, Faridabad, Gautambudh Nagar and Ghaziabad. GBN remains one reporting area; Noida and Greater Noida are not invented separate labels. The original workbook download URLs, acquisition dates and independent publisher receipts are unavailable. File hashes, header identities and reconciliation are retained in config/counts-v1.json and manifest.csv. Verify original acquisition and reuse terms before publishing.

Targets use only the explicit total column (2022 column 54; 2024 column 67). No parent-plus-child sums, rates per population, blank-to-zero conversions or estimated neighbourhood labels are training targets. All reporting units, including special units, sum exactly to the workbook Delhi/Haryana/UP state total in both years. Special units are excluded from geographic modelling. Delhi total is 14,247 in 2022 and 13,396 in 2024, consistent with the previously downloaded NCRB 2024 report Table 3A.1. This check validates workbook totals, not district boundary continuity or every category cell.

The 2024 workbook itself has stalking parent/child inconsistencies. Delhi parent stalking total is 178 while adult/girl children sum to 77. Those discrepancies also explain why the earlier mirror leaf-sum extract differed from the explicit total. The underlying cause is unknown. The new pipeline audits all printed adjacent adult/girl subtotal identities and records every selected-district mismatch without repairing source values. Rohini's explicit total is **883**; the earlier mirror-derived leaf subtotal was 879. These are different source calculations and are not silently substituted in the app.

IPC/BNS transitions remain a comparability limitation. Explicit paired legal labels from the 2024 header are mapped conservatively in count_model.py; unreviewed categories stay unmapped. Totals are retained as each year's published definition, including newly introduced categories. No assertion of identical legal scope across years is made.

## Exactly three intended inputs

1. Previous observed annual total cases, optionally smoothed using reviewed matching police-district adjacency: 0.8 own count + 0.2 neighbouring mean. **Current run is unsmoothed:** matching adjacency is unavailable. Revenue names, ward boundaries and approximate reference points are not police geography.
2. Six four-hour bands and weekday/weekend. There are no observed time labels. config/time_factors.yaml uses neutral **assumed** multipliers of 1. No time model is trained and no preferred risky window is invented.
3. One night-context score from reviewed OSM/open context. Missing for every training example. The current OSM file is a help-only inventory (not complete land use/roads/isolation/transit/late-open density), and is from 2026, after the validation target. It cannot be disguised as historical context. Optional reviewed historical context inputs are documented in reports/counts-v1/README.md.

Future work only: socio-economic predictors, CCTV, police-station distance and other excluded inputs. Density may support place context/allocation; it is never a target-rate denominator.

## Formula, confidence and export

`expected_case_index = annual baseline × time factor × place-context adjustment`.

The adjustment is unavailable, rather than fabricated as a fitted coefficient. The count-only research baseline can be inspected separately. A time multiplier on an annual index does not create measured four-hour case counts. Common within-band factors cannot change percentile area ordering.

The scoring utility implements percentile rank × 100 within eligible areas, tie-average ranks, and 25/50/75 bucket thresholds. Low confidence (<0.6), missing context, missing geometry and singleton comparisons remain **unknown**. Export's 0.25 completeness score is a conservative heuristic, not calibrated probability. Real district totals are retained alongside unknown risk entries in all twelve day/band combinations. No synthetic data is trained; synthetic unit fixtures are separate.

The tested downscale allocator requires measured density, road density and built-up weights and a verified complete district partition. Normalized weights sum back to each district total, with a floating-point residual correction. Counts are labelled estimated; observed neighbourhood totals remain null. No real downscaling has been performed because a matching crosswalk and inputs are missing. The versioned GeoJSON is empty with an explicit reason. **PMTiles is not generated from missing geometry.**

## Validation and comparison

| Model (count-only) | District holdout MAE | RMSE | Spearman | Top-20% hit rate |
|---|---:|---:|---:|---:|
| historical_count | 136.26 | 238.33 | 0.916 | 75% |
| poisson_glm | 157.65 | 264.72 | 0.891 | 75% |
| lightgbm_poisson | 242.57 | 398.75 | 0.604 | 25% |


Five whole-reporting-district folds and five leave-city-out folds use the 2024 targets and only 2022 count features. They test cross-area transfer, not future forecasting. No random observation splits. Persisted fold training IDs and tests prove train/test areas are disjoint and feature cutoff precedes target year.

Temporal persistence backtest: 2022 counts predict 2024 totals over a two-year gap, MAE **136.26**, RMSE **238.33**, Spearman **0.916**. No 2023 interpolation. Learned models cannot be independently temporally tested: only one complete lag/target pair exists per district. They would need earlier complete targets to train before 2024. This is why persistence remains the selected baseline, rather than claiming the spatial fit is a temporal safety validation.

City holdout MAE: GLM 347.67, LightGBM 514.54. Per-city temporal persistence MAE: Delhi 82.47 (15 districts), Faridabad 24, Gurugram 17, GBN 509, Ghaziabad 802 (each outside Delhi has one target). Singleton rank metrics are unavailable; their top-k hit rate is trivial and cannot validate hotspots.

Calibration bins, predicted/observed total ratios, per-city metrics, held-out permutation importance and seeds 7/42/103 are in evaluation.json. Seed outputs are identical for the current deterministic settings; this does not imply data stability. No hyperparameter search was performed on the held-out data.

## Uncertainty, sensitivity and bias

Reporting-unit bootstrap of temporal persistence errors, fixed seed 42, 1,000 draws: MAE 95% interval **59.68–245.71** cases. Absolute-error 90th quantile 289.00. These describe this small retrospective error sample; they are not calibrated future per-neighbourhood prediction intervals. No false quantile coverage claim.

District research exports also carry **estimated 2026 annual persistence forecasts** and exploratory 90% intervals from 10,000 resampled pooled signed 2022→2024 errors. This uses the same two-year horizon and assumes stable, exchangeable district errors. The assumption is not validated, and pooled errors do not capture missing place/time inputs or jurisdiction differences. Forecasts are distinct from the 2024 measured total, carry low confidence and no risk score, and are not written to app feeds.

Sensitivity scenarios multiply an illustrative baseline index (100, explicitly a scenario constant) by 0.75/1/1.25. They are not crime observations and are not trained. Missing history makes outputs unknown; missing context suppresses risk but retains historical-count research. No time observations means neutral factors and no time learning.

Population/area correlations and Moran's I are **unavailable**, since matched police-unit population, area and adjacency are missing. Administrative geography must not be used as a substitute. Whole-city results reveal poor transfer to UP reporting areas, but neither establish causes nor identify reporting-rate differences. Counts inherently depend on jurisdiction size, population, police recording practices and reporting willingness. Under-reporting and affluent/low-reporting area differences remain unresolved. Low observed volume never establishes safety.

## Sources, licences and next evidence

NCRB workbook provenance/redistribution terms need confirmation; downloaded original report via OpenCity is attributed to NCRB (mirror declares Other/Public Domain). India Data Portal mirrors declare no licence and are not used as total-count labels here. OSM: ODbL 1.0, © OpenStreetMap contributors; evaluate derivative-database obligations. Historical DataMeet wards: CC BY-SA 2.5 India; boundary vintage/crosswalk unverified. Census government table is Central Delhi 2011 only, not all police districts; no added open-licence claim. No login, paywall or robots restriction was bypassed.

Next: earlier original total-count workbooks for honest temporal learned-model testing; reviewed matching police geography plus complete context for downscaling; RTI for finer aggregate counts and observed time bands; SafeCity/Safetipin for separately reviewed crowd reports/environment audits. These are acquisition steps, not fabricated inputs. Exact gaps and intended local destinations are in MANUAL_DOWNLOADS.md. No new API key is needed to reproduce this run.
