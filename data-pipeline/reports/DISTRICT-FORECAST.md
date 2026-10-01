# Experimental recorded-case forecast — 1 October 2026

This run trained a real LightGBM Poisson regression on **131 source-backed annual recorded-rape observations**, yielding 93 lagged examples, across 19 geographic reporting units: 15 Delhi police districts and Gurugram, Faridabad, Gautambudh Nagar and Ghaziabad. Check the JSON's `examples` field for the exact executable count; it is the authoritative run output. Sources are the hash-checked India Data Portal 2017–2022 and 2024 CSVs documented in the Delhi extraction receipt. This is a **secondary-source recorded-case forecast**, not a neighbourhood safety model.

Target: annual adult + girl rape heads recorded under IPC/BNS. Other categories and POCSO heads are not silently added. Input features are only past counts, their mean and trend, forecast horizon and reporting city. No exposure denominator, neighbourhood environment, incident time or validated geography has been invented. No 0–100 risk score is produced.

`python data-pipeline/train_district_forecast.py` reproduces the model, lag-feature CSV and evaluation under ignored `data-pipeline/artifacts/district-forecast/`. Original hashes must match before training. `reports/DISTRICT-FORECAST.json` retains actual evaluation results and held-out predictions. Joblib artifacts are local and never loaded from an external source.

The temporal test trained on pre-2024 target rows and held out all 19 available 2024 district targets. 2023 is absent, so these are two-year forecasts from 2022 history. Training horizons before this test are one year: the test also evaluates extrapolation to a previously unseen horizon, and cannot establish calibration of other horizons. Mean absolute error (MAE) is the average absolute difference in recorded cases, not a safety accuracy percentage.

| Temporal scope | Targets | Model MAE | Last-recorded-count baseline MAE |
| --- | ---: | ---: | ---: |
| All held-out reporting units | 19 | 19.07 | 22.11 |
| Delhi | 15 | 16.79 | 15.33 |
| Faridabad | 1 | 45.74 | 60.00 |
| Gautam Buddh Nagar | 1 | 59.22 | 42.00 |
| Ghaziabad | 1 | 2.79 | 40.00 |
| Gurugram | 1 | 2.70 | 48.00 |

Five-fold whole-reporting-unit and leave-one-city-out checks use only pre-2024 labels; exact fold and per-city results are in the JSON. Held-out units retain their known past history as inputs, but their target rows are excluded from model fitting. These grouped tests measure generalization across units; they are separate from the prospective temporal test. They do not establish performance for unseen neighbourhoods.

The overall model beats this simple temporal baseline, but **does not beat it for Delhi or Gautam Buddh Nagar**. Four city summaries each have only one held-out target. Reporting changes, under-reporting, POCSO/IPC classification, the 2024 BNS transition, missing 2023 and unverified reporting-unit boundary continuity limit interpretation. No intervals or calibrated probabilities are available.

**Production neighbourhood/time-risk release remains false.** The trained artifact and metrics are research work, and are not inserted into the public neighbourhood file or used to colour risk polygons. Future predictions are not published. Real unsafe-time or neighbourhood predictions require observed target cells, exposure, reviewed boundaries, environment joins and further validation.

## Historical map references

The new red markers use the separate 2024 **historical recorded-head subtotal**, not this model's rape predictions. All have a fixed marker size; no danger radius or district polygon is drawn. Explicit point sources come from the existing OSM snapshot:

- Central: [mapped DCP district office](https://www.openstreetmap.org/node/12441175891).
- Shahdara: [mapped DCP district office](https://www.openstreetmap.org/node/12596382943).
- Dwarka: [mapped police station](https://www.openstreetmap.org/node/2408446621), an approximate locality reference, not a claim that it is the district headquarters.

These are approximate district reference points, **not crime locations or verified boundaries**. OSM locations are not field-verified. The remaining 12 Delhi districts have no new map reference point in this release. Their absence does not mean lower volume or lower risk. `publish_district_points.py` verifies each explicit OSM ID/name pair before emitting the points, retains source links, and never uses inconsistent LGD names to geocode a police unit.

Map messages and marker dialogs disclose the annual reporting year, reference-point status, recorded-volume meaning and the unresolved 101-case Delhi stalking discrepancy. Annual markers do not change with the time slider; selecting an unsupported crime/year filter hides them. Synthetic neighbourhood polygons remain opt-in and separately labelled.
