# Kaali

## Delhi historical police-district records

The map now has three red **historical volume reference markers** for Central, Shahdara and Dwarka, anchored to explicitly identified locations in the OSM snapshot. These are approximate reference points, not crime locations, district boundaries or danger radii. Click for reporting-year/source details. Filters can hide this layer; it does not change with the time slider. Other districts remain unmapped until a matching reference or boundary is reviewed. Reproduce with `python data-pipeline/publish_district_points.py`.

An experimental annual recorded-rape forecast can be trained with `python data-pipeline/train_district_forecast.py`. It trains LightGBM on source-backed district counts, runs whole-unit/city and temporal evaluations against a last-observation baseline, and saves its artifact privately. See `data-pipeline/reports/DISTRICT-FORECAST.md` for actual results and limitations. It does not produce neighbourhood safety scores or unsafe-time forecasts and does not colour risk polygons.

Home → **Explore police districts**, or `/evidence` → Delhi, displays the sourced 2024 reporting-circle extract: 15 geographic police districts and eight separately grouped special units. Selecting a unit shows its calculated recorded-head subtotal, selected category groups and all 49 original head counts. Missing values remain unavailable, never zero. The screen retains the 13,295 mirror versus 13,396 NCRB reconciliation and its 101 adult-stalking difference; these are historical recorded volumes, not safety scores. No district count is assigned to a map neighbourhood.

Reproduce the research files with `python data-pipeline/extract_delhi_districts.py`, then the app feed with `python data-pipeline/publish_delhi_districts.py`. Both require the original hash-matching CSV/PDF downloads documented in `data-pipeline/reports/delhi-districts/METHODOLOGY.md`. The full India downloads stay in ignored raw storage. The Delhi-only factual feed keeps source attribution and the mirror's **No License Provided** disclosure.

To configure another city's reviewed district feed, add `districtCrimeFile` to that city's entry in `public/data/regions.json`. Its JSON must pass `loadDistrictCrime` and match the configured region/city IDs. Page components read the configured path; no city-name code change is required. Run the publication validator and tests before use. This configuration does not establish police boundaries or make a dataset eligible for risk modelling.

Neighbourhood safety awareness for Delhi NCR. React + Vite + TypeScript, Tailwind v4, locally owned shadcn-style Radix primitives, Framer Motion, Lucide and lazy Recharts. The map uses **MapLibre GL JS through react-map-gl**, MapTiler vector styles, Turf client-side geometry and optional static PMTiles.

See [BUILD_STATUS.md](BUILD_STATUS.md) for the current milestone and next steps.

## Current delivery status

- Runnable glass UI: map, neighbourhood sheet, location consent/messages, nearby help, helplines, methodology, design-system gallery.
- Region/city configuration includes Delhi, Gurugram, Noida, Greater Noida, Faridabad and Ghaziabad. Optional fringes are not covered.
- **No validated production risk model or neighbourhood crime estimates.** Production data is intentionally empty. 18 clearly labelled synthetic cells exercise time bands, filters, charts and selection. They are never used for location advice.
- Real OSM snapshot: **3,733** service/road features, fetched 2026-09-29 UTC (retrieval date is stored in the file). These are mapped, not field-verified. All city assignments remain empty until verified jurisdiction boundaries are supplied. They display under All NCR; a city-filtered layer excludes unassigned records.
- Four sourced adult conviction records, with geographic match withheld. No case cards are attached to fabricated neighbourhoods. Additional seed cases are deferred until conviction/locality evidence has been reviewed.
- Helplines researched against official pages. The direct build-time access report contains blocked/unavailable pages; **not every URL check passed**. See `public/data/reports/helpline-verification.json`. Phone services have not been test-called.
- MapTiler key is not supplied. The app renders interactive MapLibre sample geometry over a neutral background, explicitly labelled **No basemap**. No production basemap, paid geocoding or domain restrictions have been end-to-end verified without a key.

## Run

Requires Node 22+ and pnpm (lockfile included), or npm to install the same manifest. Python 3.11+ is needed only for data processing.

```sh
pnpm install
cp .env.example .env.local
# Add your domain-restricted VITE_MAPTILER_KEY to .env.local
pnpm dev
pnpm test
pnpm validate:data
pnpm build
```

Routes: `/`, `/helplines`, `/about`, `/design-system`. The dev server prints its actual port. Static hosting must route unknown application paths to `index.html` while serving JSON, GeoJSON and PMTiles as actual files. No backend is required for precomputed predictions.

## Environment and map setup

| Variable | Purpose |
|---|---|
| `VITE_MAPTILER_KEY` | Browser MapTiler key. Restrict allowed domains in MapTiler Cloud; include only intended local/production origins. |
| `VITE_MAPTILER_LIGHT_STYLE` | Default `dataviz-v4-light`; may be your own muted style ID. |
| `VITE_MAPTILER_DARK_STYLE` | Default `dataviz-v4-dark`. |
| `VITE_PHOTON_URL` | Default public Photon demo endpoint. Use a self-hosted endpoint or controlled proxy for production scale. |
| `VITE_FEEDBACK_URL` | Owner-managed corrections/removal/city suggestion link. Not configured in preview. Avoid collecting personal data. |

Vite embeds `VITE_*` variables in browser assets. The map key is deliberately browser-visible: use domain restrictions and quota limits, not secrecy, to protect it. Do not put private credentials in Vite variables.

`MapView` accepts region, layer data, selected ID, time band, theme, camera targets, location and event callbacks. Pages contain no provider-specific map calls. Theme changes replace the style on the existing MapLibre instance, preserve camera, then restore risk sources/layers and selection on `style.load`. Risk scores animate via feature-state without replacing GeoJSON on each time change. Glow uses a blurred line; high-risk cells get a hatch pattern; 3D uses fill extrusion. All controls use the shared glass primitives. Reduced-motion settings disable interpolation and camera animations.

### Pricing / terms checked 2026-09-29

Primary sources: [MapTiler pricing](https://www.maptiler.com/cloud/pricing/), [Cloud terms](https://www.maptiler.com/terms/cloud/), [sessions versus requests](https://docs.maptiler.com/guides/account/sessions-vs-requests/), [geocoding API](https://docs.maptiler.com/cloud/api/geocoding/).

The public page describes a $0 free plan for testing/personal/non-commercial use and a $30/month Flex plan. Its numeric free traffic quotas were not exposed in the retrieved dynamic pricing table. **The numeric quota remains unverified; confirm the current limits in the account dashboard before launch.** Do not reuse historical 100k/25k quotas as current facts. Third-party MapLibre use is request-metered, unlike SDK session assumptions. Free service can pause when quota is exhausted. Free-plan use requires MapTiler logo and attribution; both are wired into the map when the key is present. Commercial deployment must use an eligible plan.

### Search behaviour and policies

550ms debounce, 3-character minimum, bounding-box restriction from region config, 100-query in-memory cache, stale-request cancellation. MapTiler is primary; empty/error results fall back to Photon. Photon calls are serialized and spaced at least 1.1 seconds apart **per browser**, not globally across all visitors. The public demo has no uptime guarantee or fixed published quota. Its [usage policy](https://github.com/komoot/photon#public-demo-server) permits reasonable use and warns of throttling. A production deployment with material traffic needs a self-hosted Photon instance or centralized throttled proxy; browser-local pacing is not a global rate limit.

Public Nominatim is **not used**: its [policy](https://operations.osmfoundation.org/policies/nominatim/) forbids client autocomplete, beyond its 1 request/second maximum. Typed search text goes to the chosen geocoder. Recent selected addresses (up to five) stay in localStorage and can be cleared from the search dropdown. GPS coordinates are never reverse-geocoded or saved. No analytics or accounts.

## Data pipeline and retraining

```sh
python -m venv .venv
# Activate the venv for your shell
python -m pip install -r data-pipeline/requirements.txt
python data-pipeline/overpass.py --region delhi-ncr
python data-pipeline/train.py --input data-pipeline/private/reviewed-features.csv
python data-pipeline/predict.py --region delhi-ncr \
  --model data-pipeline/artifacts/model.joblib \
  --features data-pipeline/private/prediction-features.csv \
  --boundaries data-pipeline/private/neighbourhoods.geojson \
  --release-review data-pipeline/private/release-review.json
pnpm validate:data
```

Read [schema](data-pipeline/schema.md), [sources](data-pipeline/SOURCES.md), [model card](data-pipeline/MODEL_CARD.md), and per-city reports in `public/data/reports/`. Training is blocked on sufficient reviewed observations, real exposure and leakage-free history. It uses LightGBM Poisson regression; validates spatial neighbourhood groups, held-out cities and a final future period; writes per-city metrics to ignored staging. Estimated allocated counts cannot be target truth. Scores are relative estimated reported-incident intensity, not the probability of crime or victimization. The training environment was not installed/run for this delivery because no admissible training input exists; no accuracy numbers are invented.

Source collector defaults deny requests until licence/terms approval, checks robots, identifies itself and rate-limits. News payloads are never published; retaining even a headline requires manual privacy review. `geography.py` provides clipped H3 resolution 8/9, point assignment and conservative aggregate-allocation weights. Complex IPC/BNS mapping needs source-specific reviewed adapters. `environment.py` derives OSM POI and explicit 24/7 tags as limited proxies; it does not claim measured footfall or parse every opening_hours expression.

Overpass runs one bounded request, at most weekly by default, preserving the previous snapshot on failure. No browser makes Overpass requests. The GitHub Actions workflow schedules a weekly **review artifact**, not an automatic public release. It becomes active when this repository is hosted in GitHub with Actions enabled; no remote repository has been configured here. Supply verified city boundaries before populating `cityId`. Missing `lit` tags mean unknown; `lit=yes` is contributor evidence, not a safety guarantee. Service distance is straight-line, not routing or a response-time promise.

### Generate PMTiles

Install [Tippecanoe](https://github.com/felt/tippecanoe) and the [PMTiles CLI](https://docs.protomaps.com/pmtiles/cli) through their official installation instructions (WSL/Linux is convenient on Windows).

```sh
python data-pipeline/tiles.py --input public/data/delhi-ncr/neighbourhoods.json \
  --output public/data/delhi-ncr/neighbourhoods.pmtiles
```

The script creates per-zoom simplified vector tiles (zooms 7–15) through Tippecanoe → MBTiles → PMTiles, preserving all features. Set `pmtiles` to `/data/delhi-ncr/neighbourhoods.pmtiles` and `sourceLayer` to `neighbourhoods` in the region entry. IDs are string `id` properties promoted for feature-state. The static host must support HTTP Range requests and appropriate CORS. JSON metadata is still loaded for panels; for very large datasets, a metadata index/sharding pass will be needed. No production tile archive was generated from absent geometry. 60fps on physical mid-range phones remains a measurement target, not a verified claim.

## Add a region or city

1. Supply licensed WGS84 region and city boundary FeatureCollections. Rectangular camera extents must not classify jurisdiction.
2. Add a `regions.json` region/city entry with IDs, names, center, bounds, boundary files, neighbourhood/sample/help files, sources, helpline set, languages, timezone and quality report.
3. Supply reviewed neighbourhood polygons or H3 cells clipped at jurisdiction borders, matching female population and period-specific observations. Avoid mixing census/ward vintages.
4. Add source adapters/configuration and helpline data; verify source access and data licences. Refresh OSM help data.
5. Retrain, review held-out metrics, publish static predictions, optionally generate PMTiles. Compute real coverage; never set it merely because a city exists in config.

The UI reads configuration, not city-specific branches. Additional languages require translations; no new renderer code is required.

## Add a convicted-offender record

Add only a verified adult conviction to `public/data/offenders.json`. The Zod schema rejects missing court, conviction date or HTTPS source, juveniles, unreviewed entries, unexpected fields, and unrecognized verdict/status. Use no victim/family identifiers, homes, graphic text or unlicensed photos. Current schema deliberately supports placeholder silhouettes only. Set locality/neighbourhood IDs only after a reviewed spatial match; otherwise leave null and `locationVerified=false`. Recheck appeals/status and lastVerified manually. Run `pnpm validate:data` and `pnpm test`. Schema checks cannot replace factual or privacy review.

## Verification and remaining gates

- 31 unit tests cover data bounds/missingness, schema gates, geographic holes/borders, jurisdiction-safe nearest lookup, style restoration, selection state, time updates, geocoder fallback/cache/abort, sheet snapping, camera padding, and real MapLibre style validation.
- Mobile details support pointer dragging and arrow/Home/End resizing through peek, half and full heights. The map remains non-modal and adjusts camera padding. City filters apply to all risk layers, including PMTiles and empty results; style replacement reapplies them. Renderer failures offer a labelled geometry overview and retry.
- Live UI checks and light/dark desktop/mobile captures are in `artifacts/screenshots/` when generated.
- Helpline check: `pnpm verify:helplines`. It checks reachability and number presence; only manual context review advances lastVerified. Some official pages rejected/timed out direct requests despite being available through research search. Report stays visible; verification failures are not silently ignored.
- Public launch still needs a MapTiler key/eligible plan, configured feedback channel, verified jurisdiction geometry, reviewed data and a validated model. Hindi covers key navigation/location messages; full translation of all explanatory text remains incomplete.

## Attribution / licences

Map tiles: © MapTiler under Cloud terms. Open data: © OpenStreetMap contributors, ODbL 1.0; observe attribution and derived-database share-alike requirements. Photon data derives from OSM. MapLibre BSD-3-Clause; react-map-gl MIT; Turf MIT; PMTiles JS BSD-3-Clause. Inter and Space Grotesk are locally hosted under SIL Open Font License. Dependency licences are distributed in their packages. Court/news facts are linked, with no article bodies or source photographs republished.

## Branding changelog

Formerly Aegis. Renamed to Kaali; Know your area. Walk with awareness.

Logo variants are in public/brand. The abstract mark uses no figurative or religious imagery. Existing browser preferences and recent searches migrate once to the new storage prefix. No factual datasets, licence text, third-party attribution, API credentials or external project identifiers change. App routes and manifest scope remain at the root, so no URL redirects are needed.

Manual branding follow-ups: choose a domain and social handles, perform a trademark/name availability search, and update display names in the hosting, source repository and MapTiler consoles if applicable. No remote or deployed domain is configured in this checkout.

### Pipeline validation and collection status (2026-09-30)

Run `.venv/Scripts/python.exe -m unittest discover -s data-pipeline/tests -v` on Windows (or `.venv/bin/python` on Unix). Fixtures are synthetic and remain under tests; passing these checks is not evidence of model accuracy. Training imports its ML libraries only when needed. This Windows host currently blocks scikit-learn’s `_libsvm` binary under Application Control; use an approved ML environment without weakening that policy.

The [source register](data-pipeline/SOURCES.md) records official aggregate tables, date/geography caveats and access/reuse gates. No aggregate has been silently allocated into time bands or neighbourhood risk. MapTiler light and dark style endpoints accepted the locally configured key; browser rendering, account limits and domain restrictions require separate verification.

Location messages search the next 24 hours using the region’s timezone and each future window’s weekday/weekend scores. Upcoming windows include a calendar date; missing scores never imply lower risk.

### Historical crime data and reading links

`/evidence` shows annual 2020–2022 Delhi City and Ghaziabad counts from the explicitly public-domain OpenCity transcription of NCRB 2022. Download the exact CSV linked in `data-pipeline/SOURCES.md` with its stated crawl delay, place it in ignored staging, then run `python data-pipeline/import_metro_context.py --input <csv>`. The importer checks SHA256; changed files require review. This context never becomes neighbourhood training labels. Rates are withheld until female-population exposure is verified.

`public/data/news.json` stores only curated reading-link metadata and neutral editorial headlines. Article copyright remains with the publisher. No bodies, photos or identifying narratives are retained; news counts are not added to official totals. Case cards reuse validated adult-conviction profiles and are not placed on the map without verified localities.


### News-derived context

Public news text can be processed in memory for reviewed facts. See [news extraction workflow](data-pipeline/NEWS.md). The first Delhi adapter extracts nine annual category counts and records provenance without retaining article bodies or victim details. `/evidence` labels these separately from official context; they are not neighbourhood/time-band training labels.

### Delhi input audit

Run `python data-pipeline/phase1.py --stage-existing` to verify and stage collected inputs. See [raw input paths and Census provenance](data-pipeline/RAW_INPUTS.md). The audit publishes data-readiness details, not predictions; optional environmental staging requires a working pyproj runtime.

### Reproduce Delhi city boundary and help assignments

Delhi city detection uses the OSM community state boundary, not the historical ward candidates. Attribution: © OpenStreetMap contributors, ODbL 1.0. The original help snapshot stays unchanged in raw inputs. With both checksum-reviewed raw files present:

```sh
python data-pipeline/osm_boundary.py --input data-pipeline/raw/osm/delhi-boundary-1942586.json --relation 1942586 --iso IN-DL --city delhi --output public/data/delhi-ncr/delhi-boundary.geojson --help-input data-pipeline/raw/osm/help-2026-09-29.geojson --help-output public/data/delhi-ncr/help.geojson
python data-pipeline/phase1.py
```

Review refreshed source bytes before replacing the pinned manifest hash. The converter rejects incomplete rings, wrong administrative identity and conflicting help assignments. This command regenerates the original Delhi-only assignment snapshot; preserve later city assignments when refreshing. City detection is available even without neighbourhood observations; it does not create risk predictions.

### Red-zone preview and training validation

The map overview offers **Preview red zones · sample**. This explicitly enables existing synthetic cells; it does not enable production predictions. Select a cell or change the time band to inspect the interaction. Exit returns to evidence-backed coverage.

Before fitting, run `python data-pipeline/train.py --input PATH_TO_REVIEWED_CSV --validate-only`. See `data-pipeline/schema.md` for documented observation-coverage and exposure requirements. City annual totals and missing news reports are not neighbourhood training labels.

### Stage model predictions

Use `python data-pipeline/predict.py --region delhi-ncr --model MODEL.joblib --features FEATURES.csv --boundaries BOUNDARIES.geojson --release-review REVIEW.json`. The review binds file hashes as described in MODEL_CARD.md. Output stays in ignored staging; it never overwrites public risk data. Complete model evaluation, calibration, source review and publication-schema validation before copying the result into the configured region file. No production model is currently available.

See [next steps and your input](NEXT_STEPS.md) for the current handoff. Runtime checks now pass; real observation/exposure data remain the main prediction blocker.

### Delhi historical district map

The primary route `/` displays 15 Delhi police districts' **2024 recorded totals**, with district search on the left and selected categories/source notes on the right. On mobile, selection opens a non-modal details sheet. `/methodology` explains the scope; `/helplines` retains official emergency contacts. The previous neighbourhood experience remains available at `/neighbourhoods`, and `/evidence` retains its separate mirror extracts.

Circle diameter is `22 + sqrt(caseCount / 1500) * 30` screen pixels. Under 500 cases is pale red, 500–999 medium red and 1,000+ strong red. These are display choices, not NCRB danger classifications. Counts describe historical reporting, not current safety, victims, incident coordinates or neighbourhood forecasts.

The new feed uses the existing original-titled NCRB 2024 workbook's explicit total column: geographic police districts **13,230**, separately reported special units **166**, combined Delhi UT **13,396**. It preserves all 64 source heads/components and blanks. Parent totals and components are never added into the headline total. Stalking inconsistencies remain visible. The earlier mirror's calculated subtotals are not interchangeable with these original total cells.

Reproduce the feed, with the checksum-reviewed local inputs present:

```sh
python data-pipeline/publish_historical_map.py
```

Inputs and receipts: `data-pipeline/config/counts-v1.json`, `data-pipeline/config/phase1-inputs.json`, `data-pipeline/sources/delhi-district-2024-receipt.json`, the reviewed OSM help snapshot and Delhi NCT outline. Output: `public/data/delhi-historical-districts.json`. The publisher checks workbook and OSM hashes, original-report state totals, reference identities/geometry, and whether references lie within Delhi NCT. The client rejects missing category scope or inconsistent totals; tests verify the exact diameter/bands and missing-value handling.

Matching police-district boundaries are unavailable. Each circle uses an approximate public-place reference from OSM linked to a station/locality in the [Delhi Police directory](https://yuva.delhipolice.gov.in/contact-us.html), reviewed 2026-10-01. These are not verified district centroids, 2024 boundary assignments or danger radii. © OpenStreetMap contributors (ODbL); © MapTiler. The original workbook's acquisition URL/date are unknown and its redistribution terms need review before publishing; the independently downloaded report's receipt remains available. No new crime download or source licence is claimed for this map integration.

## Delhi NCR map update — 2026-10-02

The primary map now covers 19 reporting units: 15 Delhi police districts plus Gurugram, Faridabad, Gautambudh Nagar (Noida/Greater Noida combined) and Ghaziabad. The 2024 selected-unit subtotal is 18,778 recorded cases, not an official whole-NCR total. Rebuild with `python data-pipeline/publish_ncr_map.py`; outputs are validated by `npm run validate:data`.

Help nearby defaults on, with clustered police/hospital/metro/bus markers and per-category filters. These reuse the partial OSM snapshot; no fire-station records are available. Facilities and hours are unconfirmed. A fresh Overpass attempt was blocked by robots policy; its receipt is saved. No additional API key is required.

Map filters offer detailed streets (light/dark), muted vector and satellite with labels. Streets use `streets-v4` / `streets-v4-dark`; satellite uses `hybrid`. All three styles returned HTTP 200 with the configured key. Street/shop labels depend on provider coverage and zoom. Camera and overlays are retained when switching layouts. See https://docs.maptiler.com/sdk-js/api/map-styles/ and https://docs.maptiler.com/cloud/api/maps/ for additional outdoor/terrain styles. Domain restriction and account quotas apply; this update makes no claim of changed free-tier allowances. © MapTiler © OpenStreetMap contributors; OSM data remains ODbL.

An optional time/activity scenario uses disclosed judgement factors and mapped transit proximity. It is low-confidence, not a trained neighbourhood safety prediction. Missing context is unknown. Real recorded totals remain unchanged. The formula, exact references, provenance, missing boundaries and acquisition limits are documented in `data-pipeline/NCR_MAP_METHODOLOGY.md`. Neighbourhood estimates remain gated on a verified police-geography crosswalk and context weights.

Convicted-person details are removed. Our approach navigation is removed; old `/about` and `/methodology` links redirect to `/evidence`, which retains crime sources and data limitations.

## Supplied traffic and population integration

Reproduce with `python data-pipeline/prepare_locality_context.py`. Reads the three supplied CSVs and twenty Aug 11–30, 2024 road-probe files; originals are not edited. Corrects swapped headings in memory; preserves 153 locality references, 78 with traffic matches, six density matches and 73 population matches. No crime counts invented. Source hashes/coverage: data-pipeline/sources/supplied-locality-context.json. See data-pipeline/SUPPLIED_CONTEXT_REPORT.md for joins, scoring rules and reuse limits.

Main-map location is consent-only, with a blue device dot, accuracy circle, native sharing and an on-device awareness summary. No GPS is sent to a server/geocoder/AI service. Advice uses local rules, not live LLM inference. Square emergency pins/clusters differ from risk circles. Transparent H3 reference-cell colours are an assumed activity scenario; not locality boundaries or a calibrated crime forecast.

Layout picker includes 43 public MapTiler catalogue variants plus three presets; provider/account availability can vary. Refresh with `python data-pipeline/refresh_map_catalog.py`. Source/hash: src/data/map-catalog.json. Original supplied CSV/probe licences and population year/units remain unverified; confirm before redistribution. Large raw traffic files are not committed or copied to the public app.
