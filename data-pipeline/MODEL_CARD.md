# Aegis model card

## Release status

**No production model is trained or published.** Verified neighbourhood labels, exposure, environmental features and validation evidence are not yet available. Production JSON is empty and UI confidence is limited. The sample map is synthetic software test material, not a prediction, probability or empirical crime dataset.

## Intended task

Estimate relative intensity of reported crimes against women by neighbourhood, six four-hour bands and weekday/weekend. Scores 0–100 are a monotonic display transformation of a predicted annualized reported-incident rate, **not the probability of a crime or an individual's safety**. Thresholds require calibration before a production release. Labels: Low (UI: lower estimated risk), Moderate, High, Very High.

## Proposed model / executable training path

`train.py` uses LightGBM regression with Poisson objective and female-person-year exposure weights. Required lagged historical density must predate every row's label window. Inputs include lighting, OSM POI density, opening_hours-derived late-opening indicators, police/metro/road distance, land use, population density, city, jurisdiction, band and day type. Estimated aggregate allocations may be features, never ground-truth labels. Source quality is tracked separately from risk.

Validation: GroupKFold by entire neighbourhood; leave-one-city-out; final reporting period held out temporally. Preprocessing is fitted within each fold. Each split reports overall and per-city MAE / mean Poisson deviance. Any folds with missing denominators or insufficient cities fail. Model artifacts and metrics stay in ignored staging until reviewed. Static predictions can be exported without a backend once release gates pass.

| City | Observed training rows | Spatial validation | Temporal validation | Release |
|---|---:|---|---|---|
| Delhi | 0 | Not run | Not run | Blocked by evidence |
| Gurugram | 0 | Not run | Not run | Blocked by evidence |
| Noida / Greater Noida | 0 | Not run | Not run | Blocked by evidence |
| Faridabad | 0 | Not run | Not run | Blocked by evidence |
| Ghaziabad | 0 | Not run | Not run | Blocked by evidence |

## Limitations and bias

Reporting rates differ between the three police systems and between affluent, visible neighbourhoods and low-reporting areas. News and crowdsourcing are selection-biased. Missing lighting tags do not mean no lighting. OSM opening_hours are not measured footfall. Census denominators may be stale or geographically incompatible. Station/district allocations are ecological estimates and cannot establish street-level incident risk. H3 cells are analytical units, not legal jurisdictions. Distance to police does not guarantee response or availability. A higher estimated score does not imply that residents are dangerous.

## Privacy / responsible use

No victim identities or addresses. No individual-level prediction. No surveillance, policing allocation or denial of services based on scores. Location stays in volatile browser memory; explicit share action is the only user-triggered location export. Feedback endpoint must be configured before public release.

Last updated: 2026-09-29.
