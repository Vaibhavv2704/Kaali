# Aegis data contract · v1

Hierarchy: region → city → neighbourhood. All identifiers are stable strings. WGS84 GeoJSON uses longitude, latitude; metric area and distances use a suitable projected CRS selected in regional source configuration. Bounding rectangles are camera extents only, never jurisdiction classifiers.

## Incident input (private staging; never serve raw microdata)

`event_id`, `source_id`, `source_url`, `headline` (privacy-reviewed), `region_id`, `city_id`, `jurisdiction`, `category`, `date`, `time_band` (0–5 or null), `day_type` (weekday/weekend or null), `longitude`, `latitude`, `location_precision`, `period_start`, `period_end`, `count`, `estimated`, `origin` (official/news/crowdsourced).

Reject names, identities of victims/families, residential addresses, narratives, photos, and records without reviewed locality precision. Extract text in memory only; retain only URL and a redacted, human-approved headline for news. Never export precise incident coordinates. Unknown time is null, never randomly allocated. Same-event corroborating sources are separate provenance entries, not extra incidents. Deduplication uses publisher IDs, canonical URL and a locality/date/category fingerprint with manual review of ambiguous collisions.

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
