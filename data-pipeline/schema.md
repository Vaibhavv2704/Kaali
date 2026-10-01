# Kaali data contract · v1

Hierarchy: region → city → neighbourhood. All identifiers are stable strings. WGS84 GeoJSON uses longitude, latitude; metric area and distances use a suitable projected CRS selected in regional source configuration. Bounding rectangles are camera extents only, never jurisdiction classifiers.

## Incident input (private staging; never serve raw microdata)

`event_id`, `source_id`, `source_url`, `headline` (privacy-reviewed), `region_id`, `city_id`, `jurisdiction`, `category`, `date`, `time_band` (0–5 or null), `day_type` (weekday/weekend or null), `longitude`, `latitude`, `location_precision`, `period_start`, `period_end`, `count`, `estimated`, `origin` (official/news/crowdsourced).

Reject names, identities of victims/families, residential addresses, narratives, photos, and records without reviewed locality precision. Extract text in memory only; retain only URL and a redacted, human-approved headline for news. Never export precise incident coordinates. Unknown time is null, never randomly allocated. Same-event corroborating sources are separate provenance entries, not extra incidents. Deduplication uses publisher IDs, canonical URL and a locality/date/category fingerprint with manual review of ambiguous collisions.

News aggregate context may additionally retain reviewed category/year/count facts and a content hash/retrieval timestamp, with `origin=news`, `eligibleForTraining=false`, `neighbourhoodId=null` and `timeBand=null`. This is factual extraction, not storage of article prose. See NEWS.md. Publication timestamps must never substitute for incident timestamps.

## Categories and normalization

| Canonical category | Legacy coding example | Mapping rule |
|---|---|---|
| sexual-assault | IPC 354 family | Retain subsection; exclude nonmatching offences |
| rape | IPC 376 family | Keep attempted/completed and adult/child distinctions in private aggregation |
| harassment | IPC 509; verified stalking/harassment categories | Do not double-count overlap with 354 |
| trafficking | Relevant verified trafficking provisions | Include only women-related subset with evidence |
| other | Unmapped official category | Never silently force into another category |

IPC/BNS changes require a versioned, reviewed crosswalk by effective date. No automated IPC→BNS equivalence is claimed. NCR systems differ: Delhi Police, Haryana Police and UP commissionerates. Units, municipal/census/police boundaries and reporting periods must be aligned before comparison. Missing offences are missing, not zero.

Annualized rate = reported count / female population × 100000 × 365.25 / reporting days. A rate is unavailable when exposure is missing. Time-band rates need band-specific observation exposure. Do not add overlapping periods or official aggregates to their component news events. News/audit/crowd sources are features or separately labelled layers, not extra official counts.

For aggregate allocation, intersect verified reporting-unit and neighbourhood polygons in metric CRS. Within that reporting unit only: weight = 0.2 × normalized intersection area + 0.6 × normalized female population + 0.2 × normalized road length. Renormalize available weights, record which denominators were missing and preserve source totals. Fractional allocated counts are `estimated=true`, never official neighbourhood counts. Do not allocate temporal bands from an annual total.

## Public neighbourhoods

See `src/lib/risk.ts` runtime validator. `geometry` must be closed Polygon/MultiPolygon; real geometry requires `boundaryStatus=verified`. `provenance`: `sample`, `model`, `unavailable`. `scores` keys `weekday:all`, `weekend:all` and supported `day:category`; six 0–100 values or null. Missing category/year lookup returns null. Model scores describe relative estimated reported-incident intensity, **not probability of victimization**. Unknown scores never become zero. `incidents` and `trend` are null if unsupported. `year`, `femalePopulation`, `periodDays`, `estimated`, `sources`, `confidence` mandatory. No unsupported official-looking precision.

Confidence: high requires ≥3 independent source families, verified geometry and exposure, adequate current observations and held-out validation; medium requires ≥2 and valid exposure; otherwise low. This is evidence coverage, not model certainty. Production release requires manual review of these thresholds. City coverage is the fraction of valid neighbourhood-time cells supported by admissible observed data (0 when none); it is not a safety score.

## Region additions

`public/data/regions.json` declares all files, cities, map extents, IANA timezone, languages and helpline sets. Supply verified region/city boundaries and neighbourhood polygons (or jurisdiction-clipped H3 cells at resolution 8/9). Grid cells intersecting a border are clipped separately and given jurisdiction-specific IDs. Do not use nearest-city or rectangle membership for jurisdiction. Holes and MultiPolygons must be respected.

## Training input checks — 2026-09-30

Target rows now require `observation_coverage=complete`, a `coverage_source_url`, `boundary_status=verified` and an `exposure_source_url`. These declarations need source review; passing schema checks does not verify their truth. News-only absence cannot be converted to observed zero counts. Reporting dates are inclusive whole days. `period_days` must equal the number of weekdays or weekend days matching `day_type` in that interval. Each row describes one four-hour band; rates are band-specific annualized reported counts, not individual probabilities. Overlapping periods within the same neighbourhood/band/day type are rejected. Numeric features allow missing values but reject infinity, negative values and lighting outside 0–1.

Run `python data-pipeline/train.py --input PATH_TO_REVIEWED_CSV --validate-only` to check evidence structure before loading the ML runtime. It writes no model or metrics. No admissible production training CSV currently exists. Test fixtures remain synthetic, in memory and excluded from published data. Production training is still blocked by missing observations/exposure and the host ML runtime policy.

## Prediction export checks — 2026-09-30

`predict.py` now stages to ignored `data-pipeline/artifacts/predictions.json` by default and refuses direct output under public/. It checks exact feature/boundary ID agreement, one row per six bands and two day types, city agreement, reviewed boundary flags, valid polygon topology and positive exposure. Invalid/negative/non-finite model rates are rejected rather than silently clipped. A review must bind the exact local model, feature CSV and boundary file with `artifactSha256` keys `model`, `features`, `boundaries`. Never load untrusted joblib files; hashes bind reviewed bytes but do not make an untrusted model safe. Sources, confidence, finite calibration scale and reporting metadata are mandatory.

This is an export implementation with synthetic in-memory unit tests, not a trained or calibrated model. After a real model passes review, validate staged records with the frontend schema before copying to the region's configured neighbourhood file. Unsupported incident counts and trend remain null.
# Counts-v1 total-count research schema

Latest counts-only task is isolated from the earlier app/model schema below. `reports/counts-v1/observations.csv/json` records `unit_id`, original `source_name`, police reporting `unit`, `city`, `state`, `year`, explicit total `count`, `source_path`, `source_sha256`, `source_row`, and `category_mismatches`. Blank input cells remain null; zero is retained only when recorded. Mapping retains source names and unresolved `boundary_id:null`, `boundary_verified:false`. Special reporting units enter state reconciliation but not the geographic training panel.

Model features use historical TOTAL count, optional reviewed night-context scalar, and separate observed-or-assumed time/day factors. No population-normalized target. IPC/BNS mappings are explicit source-header pairs; unreviewed heads stay unmapped, and totals retain original year definitions. Adjacency and zone allocation require independently reviewed police geography, not `district_name` from mirrors.

Versioned district export has `id`, `year`, `source_list`, `data_type`, `confidence`, `total_reported_cases`, `risk_score`, `level`, `top_windows`, and `time_bands` (six bands × two day types). Current risk entries are null/unknown. Factual observed district totals stay separate from estimated annual persistence and assumed time factors. Downscaled neighbourhoods must have `total_reported_cases:null`, `district_total_reported_cases`, `estimated_cases`, `data_type:estimated`, reviewed geometry and a conserved district sum. No synthetic training/output record enters counts-v1. The current neighbourhood GeoJSON is empty with missing-evidence metadata; no PMTiles export is claimed.

Confidence is a completeness heuristic, not safety probability. Missing/low confidence can never become a Low or High risk label. Empty top windows explicitly mean no supported ranking; equal neutral factors do not establish three riskiest windows. Reports remain private/research outputs outside public app feeds.
