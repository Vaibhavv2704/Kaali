# Kaali ML annual-volume model — ml-volume-v1

## Actual fitted model

Regularised **Poisson regression**, trained on real NCRB annual total crimes-against-women labels. The training feature is `log1p(previous observed annual total)`. The pooled sample contains **109** matched named reporting units across Delhi, Haryana and Uttar Pradesh: 2022 features → 2024 targets. Auxiliary units outside NCR are included for training, never presented as NCR map areas. No synthetic counts, estimated neighbourhood labels, population rates, or invented occurrence-time observations are used.

Special units (Delhi non-geographic branches, GRP, Irrigation & Power) are excluded. Three commissionerate labels with unmatched related rural/outer labels are conservatively excluded. Missing/unmatched years have no paired example. Names are source identities, not verified boundary-continuity evidence. Other unobserved jurisdiction changes remain a limitation. Both source files retain frozen SHA-256 in config/counts-v1.json; all six state/year totals, including the units excluded from modelling, reconcile with original NCRB Table 3A.1. Original workbook acquisition URL/date and reuse receipts remain unknown. No new crime download is claimed.

## Measured retrospective results

Five disjoint reporting-unit folds; no random observation split, no overlapping train/test units. Feature years precede target years. Fixed model settings, no hyperparameter search.

| Candidate | OOF MAE (cases) | RMSE | Spearman |
|---|---:|---:|---:|
| Previous-count persistence | 165.55 | 256.97 | 0.8993 |
| Poisson GLM | **160.99** | **250.28** | 0.8933 |
| LightGBM Poisson | 180.71 | 260.61 | 0.8724 |

Poisson is selected for the lowest pooled count MAE. The mean improvement is **4.57 cases**, only about 2.8%; its rank correlation is slightly worse than persistence. Paired reporting-unit bootstrap interval and calibration/top-20% metrics are saved in evaluation.json. Model selection used these same folds; there is no untouched final test. Do not claim significant general improvement or hotspot validation.

Whole-NCR-city holdouts train on the remaining pooled units. ML MAE: Delhi **81.91**, Faridabad **126.28**, GBN **471.11**, Ghaziabad **983.76**, Gurugram **126.62** cases. Delhi has 15 test units; each other city has one. Combined NCR city-holdout MAE is about **154.55**, worse than persistence (136.26). Per-city baselines, RMSE, rank/hotspot/calibration metrics, unit IDs and split evidence are in evaluation.json. Singleton rank metrics are unavailable and hotspot hits trivial. This model must not be promoted as a validated NCR safety model.

Only one complete lag/target cohort exists. **Learned future-year validation is unavailable**, not replaced by random splits or interpolation. The separate old counts-v1 persistence backtest is not validation of this newly pooled model. Fitting the 2022→2024 relationship and applying it to 2024 to estimate 2026 is an explicitly unvalidated two-year extrapolation. Seeds 7/42/103 and runtime/model hashes are recorded. Exploratory intervals use pooled out-of-area residual 5th/95th percentiles; they are not calibrated future/neighbourhood confidence intervals.

## Model-dependent map scenario

NCR export has 19 district annual forecasts, original 2024 recorded totals in separate fields, and percentile ranks of forecasted volume. It does not infer individual safety. References retain their original approximate OSM-place coordinates, never incident locations or verified centroids.

For supplied locality reference points inside the reviewed Delhi NCT outline, interpolate the three nearest Delhi forecast-volume ranks using inverse squared distance, floored at 0.5 km and capped at a 12 km nearest-reference distance. This is **assumed display interpolation**, not a police-district assignment, neighbourhood count, official boundary or supervised spatial prediction. Outside Delhi, mapping remains unknown because corresponding geometry is not verified. 152 reference points have an annual interpolated index; missing traffic/context can still suppress the final display.

The final cell index multiplies that interpolated rank by `0.75 + 0.5 × activityScenario/100`, capped at 100 and rounded. ActivityScenario is the separately documented assumed time/historical-probe/source-density illustration in SUPPLIED_CONTEXT_REPORT.md. Traffic and population are not fitted crime coefficients: they have no reviewed police crosswalk, complete historical exposure or real crime time labels. Mean indices are merged for references sharing one H3 cell, avoiding opacity stacking. Pale rose through crimson encode this index; grey means unknown. It is not a within-time-band percentile or calibrated risk probability.

All neighbourhood `reportedCases` and actual `riskScore` values remain **null**; the separate display `annualVolumeIndex`/ML scenario index is estimated with assumed mapping and low confidence. No district total has been downscaled, no danger radius invented, and no PMTiles generated from verified neighbourhood boundaries. The reference-cell GeoJSON is exported as an assumed display artifact, not factual locality geometry.

## Advice

Location summaries report the model scenario and context with uncertainty. Optional genuine generative wording uses a locally installed Ollama model through server/advice.mjs. The endpoint accepts only anonymous index/time/activity/population categories; no GPS, locality names, counts, raw prompts or identifiers. It binds to loopback, does not log/store requests, uses bounded generation and rejects unsupported dramatic claims. No model is installed/running in the current machine check, so live generation remains an external runtime setup gate; rule-generated summaries continue to work. Mocked endpoint/privacy tests are not evidence that an actual LLM ran.

## Bias, licences and gaps

Counts reflect population/area size, reporting practices, under-reporting and legal-definition changes (IPC/BNS). Police-unit area/population/adjacency are unverified, so area/density correlations and Moran's I are not invented. The poor transfer in several NCR holdouts is visible; no causal interpretation is asserted. Matching neighbourhood crime labels, police geography, historical context, earlier annual totals and occurrence-time labels remain the strongest next evidence.

NCRB government publication reuse receipts remain unresolved; user-supplied locality/population/probe licence and source provenance need review before redistribution. OSM reference attribution/ODbL and MapTiler service attribution remain required. No victim data, accounts, tracking, offender profiles or residential addresses are used.

## Reproduce and artifacts

`python data-pipeline/train_ml_volume.py`

Trained estimator/config: `data-pipeline/artifacts/ml-volume-v1/` (local, Git ignored). Training rows, OOF/city metrics/folds, exclusions, hashes and reference-cell GeoJSON: this report directory. App JSON: `public/data/delhi-ncr/ml-volume.json`. Existing counts-v1 model artifacts/reports and measured feeds remain unchanged.
