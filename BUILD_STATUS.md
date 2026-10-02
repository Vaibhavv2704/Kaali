# Kaali build status

Updated 2026-09-30. Read this with README.md and the user’s requirements before continuing.

## Latest design preference

The header uses the Kaali wordmark alone. The user requested removal of the standalone red K mark beside it; preserve this in both themes and the monochrome wordmark.

## Completed in the latest milestone

- Non-modal mobile neighbourhood sheet: continuous pointer drag, peek/half/full snap positions, fixed handle, independently scrolling content, arrow/Home/End controls, reduced-motion support and stable focus restoration.
- Camera padding responds to sheet size and viewport changes. The underlying map remains interactive.
- All five risk layers filter by metadata IDs for both GeoJSON and PMTiles, including empty results and restored styles. Scores still update through feature state without source replacement.
- Renderer failures have an error boundary, labelled geometry fallback and retry control. Tile failures keep details and helplines available.
- Mobile selection hides the overview and duplicate time slider; the detail panel retains time controls. Attribution and awareness labels are retained. Nearby-help control has an accessible name at narrow widths.
- Added real MapLibre style validation alongside state, sheet and layout regressions. A browser check caught and corrected an invalid empty-filter expression.
- Browser checks: sample selection, city filter, time change, light/dark selection preservation, 390px mobile resizing, pointer drag from half to peek, keyboard return to half. Screenshots are local artifacts, not evidence of real risk.

## Data remains unchanged

Historical city context is now available on /evidence: six real rows from the OpenCity NCRB 2022 transcription for Delhi City and Ghaziabad (2020–2022), plus three curated news references and the four existing conviction profiles. Production neighbourhood records are empty. The 18 synthetic sample cells are software fixtures only. The existing 3,733 OSM features are real retrieved map data with unverified city assignment. No production model, metrics, jurisdiction geometry or new case matches were created. The earlier UI milestone did not fetch sources; the 2026-09-30 evidence milestone subsequently fetched the aggregate CSV and a private boundary candidate.

## Latest data/pipeline milestone

- Installed the Python requirements in ignored .venv. Four synthetic-only validation tests pass; no fixture is published or used to claim model performance.
- Reject unknown estimated flags, non-finite exposure/counts, fractional observed counts, missing source URLs/identifiers and reversed periods. Allocation now rejects infinity.
- Training dependencies load when training is invoked so data validation can run independently. Actual scikit-learn execution is blocked by Windows Application Control on its _libsvm binary; no policy was changed. A permitted training environment is required.
- Expanded both source registers with exact official table URLs, geography, partial-year caveats, reuse restrictions, access failures and all six city gaps. Corrected the stale OSM collection status. OpenCity robots disallows its API; do not retry that route.
- No new incident counts, boundaries, model scores or metrics were published.

## Next independent work

1. Completed in 2004f9e: location lifecycle, late boundary arrival, independent city detection, and clearing location UI on stop/error; six regression tests added without transmitting coordinates.
2. Completed: upcoming windows now use future regional day types across midnight, show calendar dates, include tomorrow’s same band within 24 hours and preserve missing scores as unknown. Five regression tests cover these cases.
3. Complete English/Hindi translation coverage across map controls, detail panels, traveller messaging and helplines, preserving factual content.
4. Exercise Python preprocessing and publication gates with explicitly synthetic test fixtures kept separate from public production output. Do not claim model performance from fixtures.
5. Continue legitimate boundary/data research. Record source permissions, exact retrieval dates, granularity and unresolved jurisdiction issues; do not turn camera bounding boxes into legal city boundaries.
6. Finish all-page responsive/accessibility checks, production-key map/geocoder verification and physical-device performance measurements when their prerequisites exist.

## External launch gates

- MapTiler key configured in ignored .env.local; both configured style endpoints returned HTTP 200. Domain restrictions, account quota and full browser rendering still need verification.
- Reviewed region/city/neighbourhood boundaries and admissible, normalized incident/exposure data.
- Real training inputs, validated model evaluation and reviewed release approval.
- Feedback/corrections destination, outstanding official helpline URL verification and current case-status review.
- PMTiles generation requires verified geometry plus Tippecanoe/PMTiles CLI; no production archive exists.

## Continuation

An hourly heartbeat named “Continue Kaali build after usage reset” is active in this chat. It checks usage availability, continues the next unfinished milestone, and should remain quiet when nothing actionable changed. It must preserve edits, update this file and README after verified milestones, and never publish or manufacture data to clear a gate. There is no exact usage-reset event trigger in this setup.

## Verification commands

Latest result: lint, TypeScript, 40 unit tests, publication-schema validation and production build passed. The build retains the existing large lazy MapLibre chunk warning. Browser checks used the keyless basemap fallback and labelled synthetic cells; live MapTiler services and physical-phone frame rate remain unverified.

`pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm validate:data`, `pnpm build`.

Use the workspace’s installed tooling. On this Windows host, pnpm is available at `C:/Users/vaibh/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/pnpm.cmd`. Vite/esbuild checks may require the normal approved execution outside the filesystem sandbox because they inspect ancestor directories. Keep screenshots in `artifacts/screenshots/`; do not commit private credentials or local browser storage.

## Evidence page milestone — 2026-09-30

- `/evidence`: city-filtered historical annual counts, curated news links and existing verified adult conviction profiles; linked from desktop navigation and About. No victim identities, news bodies or imagery retained.
- Reproducible checksum-pinned context importer, strict context/news validators and duplicate-URL checks.
- Downloaded and assessed 290 DataMeet Delhi ward polygons privately. Geometry validity passes, but current vintage is unverified; no production boundaries activated.
- Live MapTiler basemap renders with configured key. Evidence page browser check confirms Delhi/Ghaziabad filters and conviction cards. Light/dark screenshots stored locally. Desktop navigation and city filtering checked in browser; a final 390px check remains.
- User supplied a broad source list and authorized news collection. Specific granular dataset/path and reuse evidence remain unavailable. Prepared unsubmitted jurisdiction-specific police/NGO request drafts in data-pipeline/DATA_REQUESTS.md. GDELT bounded discovery returned HTTPError; no raw records retained.


## News extraction milestone - 2026-09-30

- Latest user steering explicitly reinstates public media/article text extraction, superseding the earlier Phase 1 exclusion of news text. Start with Delhi. Do not ask for a permission document for public factual research. Robots, access restrictions, copyright and victim privacy still apply.
- Added a reproducible single-article extractor and reviewed Tribune adapter. Live robots and article requests succeeded. Nine real annual category counts (2023-2025) are published separately as news-derived context on /evidence, with retrieval timestamp, hash and source link.
- Article bodies are processed only in memory; ignored raw/news staging contains structured facts only. No victim identifiers, residential addresses, photos, incident coordinates or inferred time bands retained. No crime score, model metric or synthetic observation added.
- Initial automatic approval rejection cited the superseded exclusion. Retried with the user's explicit latest authorization and approved; no remaining approval blocker.
- Verification: 47 frontend unit tests, nine Python tests, lint, TypeScript through build, publication validation and production build passed. Known lazy MapLibre chunk size warning remains. Browser checked the real nine-row table at mobile width; screenshot artifacts/screenshots/news-facts-mobile-dark.png. Restored viewport override afterward.
- No API key or user file is needed for this completed milestone.

### Next data work

1. Continue public Delhi article discovery with source-specific access checks; obtain actual event locality/date/time evidence, keeping publication time separate. Build reviewed incident adapters and deduplication; do not use city aggregates as neighbourhood targets.
2. Finish the Phase 1 raw input manifest/orchestrator for existing OpenCity, OSM and DataMeet inputs. DataMeet old Delhi wards remain a historical candidate (repo issue 57 flags them outdated), not current jurisdiction geometry.
3. Fetch Census ward female-population exposure and reconcile geography vintage. Delhi Open Transit download forms require identity/terms acceptance; retain the OSM transit fallback until an anonymously usable input exists.
4. Fit/evaluate only when admissible labels and exposure exist, using an environment where sklearn is allowed. Windows Application Control and missing granular labels still prevent a production model. Never manufacture risk scores to clear this gate.

## Delhi raw-input milestone - 2026-09-30

- Added checksum-pinned raw-input manifest and reproducible phase1.py audit; staged the three existing downloaded datasets without overwrites. Public report lists actual counts and missing inputs, with no sample or predicted crime values.
- Corrected environmental lighting fraction: the lit-roads-only OSM help snapshot cannot provide its denominator. Missing tags/incomplete inventories return null. Regression tests cover this.
- Verified DataMeet publisher issue 57 marks the boundary candidates outdated. Current geometry remains unverified.
- Census catalog/robots requests fail SSL validation; no certificate bypass. One exact manual input requested in RAW_INPUTS.md: Central Delhi PCA2011 workbook. No data assumed from a missing workbook.
- Additional runtime blocker identified: Windows Application Control blocks pyproj transformer DLL. Optional environment staging records unavailable and creates no feature rows. The audit and 11 Python tests pass. Existing frontend unchanged (47 tests/build passed previous milestone).
- Next: review the Census workbook when supplied, acquire current boundary/exposure crosswalk, continue permitted incident extraction. Model fitting still requires real granular observations plus a permitted geospatial/ML runtime.

## Location Hindi milestone - 2026-09-30

- Completed English/Hindi location consent, provider privacy explanation, status/error messages, sharing controls, risk labels and traveller tips in a typed copy module. Shared dialog supports translated close labels and descriptions.
- Outside-coverage suggestion now depends on location state rather than searching English message text. Delayed geolocation errors use the currently selected language.
- Verified Hindi consent dialog and search fallback in browser without requesting GPS or sharing coordinates. Screenshot: artifacts/screenshots/location-consent-hindi.png.
- Lint, TypeScript/production build and 47 frontend tests pass. Known lazy MapLibre size warning remains. Other map/page translation work remains. No factual datasets changed in this UI milestone.

## Census input milestone - 2026-09-30

- Found the requested Central Delhi PCA2011 workbook locally; previous request is fulfilled. Workbook preserved unchanged. Acquisition is user-supplied; official catalog metadata matches, remote bytes not independently compared. Original download time unknown.
- Imported 21 historical urban ward-part population rows with complete geographic keys. Sex totals reconcile per row, parent town and district. Excluded parent summaries from the detail output and all unrelated demographic columns.
- Public census-central-2011.json includes source, checksum, historical scope and explicit no-boundary-match/no-training labels. No current population projection, normalized crime rate or new risk score created.
- 14 Python tests pass; live workbook import and refreshed phase1 audit succeed using bundled Python for openpyxl. requirements.txt now includes openpyxl. No additional manual file requested.
- Next: verify historical/current boundary crosswalk before exposure joins; continue permitted Delhi incident sourcing, then other cities. Census import resolves one missing input, not the missing neighbourhood/time labels or blocked ML/geospatial runtime.

## Delhi city-boundary milestone — 2026-09-30

- Retrieved OSM Delhi state relation 1942586 through bounded public Overpass requests. Checked administrative identity and closed topology of all 119 ways; activated this community boundary for city location/helpline matching. It is not a legal survey or neighbourhood geometry.
- Assigned 2,916 of 3,733 OSM help features strictly within Delhi. Other 817 remain unassigned. Confirmed all original feature geometry and factual properties preserved; only cityId changed. Original raw snapshot and pinned checksum preserved.
- Added reproducible converter, source hash/provenance, config path, input-audit entry and quality-report updates. No crime data, exposure estimates or risk scores created. OpenCity boundary catalog remains inaccessible (403); historical DataMeet wards remain unverified for current use.
- Verification: 17 Python tests, 48 frontend tests, lint, publication validation and TypeScript/production build pass. Regression covers real Delhi and surrounding city centres, absent risk records, incomplete rings, holes and boundary-crossing help features. Existing lazy MapLibre chunk warning remains. No new GPS/browser check performed in this milestone.
- Next: continue permitted Delhi incident sourcing and reviewed locality/date/time extraction; obtain historical Census geography crosswalk and remaining NCR city boundaries. Production training still lacks neighbourhood/time observations and exposure coverage, and this host blocks required sklearn/pyproj DLLs. No additional API key or manual file requested now.

## Red-zone preview and training-input validation — 2026-09-30

- Added prominent Preview red zones · sample control near the top of the map overview and a Sample risk scale legend. Preview remains opt-in, uses existing synthetic cells and never enters location matching or production training. No crime records or scores changed.
- Hardened training prerequisites: documented complete observation coverage, reviewed boundary flag, exposure/source references, matching weekday/weekend calendar exposure, non-overlapping target periods and valid numeric features. Validate-only CLI runs without loading the blocked ML runtime; structural checks do not substitute for source review.
- Verification: 19 Python tests, 48 frontend tests, lint and TypeScript/production build pass. Existing large lazy MapLibre chunk warning remains. Browser confirmed the preview toggle and patterned red polygons on live dark basemap; screenshot artifacts/screenshots/red-zone-preview-dark.png. Data validation required normal esbuild filesystem access after sandbox denial.
- Still no trained production model: neighbourhood/time labels and matched observation/exposure coverage are missing, and host policy blocks sklearn. Next: permitted Delhi event sourcing/review and historical geography crosswalk; do not turn city totals or absent news reports into neighbourhood labels. No new API key requested.

## First locality/time news event — 2026-09-30

- Imported one real Tribune/PTI event reference with reported Nehru Place locality and 04:00–08:00 band. Event date May 10 uses publication-year inference, disclosed in the UI. One event reference, not victim count or neighbourhood census. No people, ethnicity, exact address, coordinates or article body retained.
- Added bounded incident extractor, reviewed source config, strict publication schema and duplicate-event checks. Evidence page renders locality, date basis, time band and allegation status separately from conviction profiles. No training label or risk score generated.
- NDTV terms prohibit scraping/data mining, so no collector/import added. A different Tribune article gave only residence locality and was rejected for spatial assignment. Source reviews and actual extraction hash/time recorded in SOURCES.md.
- 22 Python and 49 frontend tests, lint, publication validation passed. Browser confirms new reference on /evidence. Production build checked in this milestone; existing lazy map size warning remains.
- Next: continue source collection and deduplication, finish reviewed prediction-export gates, remaining city geometry and translations. Training remains blocked by incomplete neighbourhood labels/exposure and ML runtime policy. All requested work is not complete.

## Prediction export milestone — 2026-09-30

- Replaced permissive model export with exact feature/boundary/city joins, complete 12-cell checks, valid geometry/exposure, finite nonnegative prediction checks and reviewed artifact hashes. No silent clipping or unmatched-row omission. Output is staged atomically outside public/ for publication review.
- Added five synthetic in-memory export tests covering invalid rates, missing/duplicate cells, mismatched jurisdictions, review failures and changed artifacts. All 27 Python tests pass. Frontend remains at 49 passing tests with lint/data validation/production build passed in the preceding milestone.
- No model fitted, scores published or crime counts invented. Original data blockers remain: one real event reference is insufficient for training; city totals do not establish neighbourhood/time targets. Windows policy blocks sklearn/pyproj. Existing four adult conviction profiles and historical official/news counts remain accessible.

## Runtime recovery — 2026-09-30

Fresh project-runtime checks now pass for tables, geometry, projection, news extraction and a tiny synthetic LightGBM fit. Installed the already-declared openpyxl dependency. No Application Control setting was changed. Earlier runtime-blocker statements are superseded by this successful check; the reason host behavior changed is unknown.

`phase1.py --environment` now stages 290 historical candidate environmental rows privately. Boundaries remain historical/unverified, lighting fraction remains unknown for the incomplete inventory, and crime/exposure joins remain absent. No production model or metrics generated. 27 Python tests pass. Runtime readiness does not fix missing labels or coverage.

## Home crime records — 2026-09-30

- Added home-screen available crime records card filtered by city chips. Shows latest imported NCRB total separately for each reporting area; no cross-city sum.
- Opens a sheet with source-linked category/year tables and selectable locality references. Nehru Place shows the existing reviewed event, allegation status, time band and inferred-year disclosure. Collection reference count is not represented as total locality crimes.
- Neutral coverage-expanding copy used for unpopulated sections. No factual records changed and no production risk labels added. Publication schema validation passes; lint and production build run for this change.
- Remaining: browser layout checks for this new sheet; broader source acquisition and real model labels. Home summary does not substitute city statistics for selected map neighbourhood counts.

- Follow-up verification (2026-10-01): pending production build completed successfully; lint and publication validation passed. Browser confirmed home totals, category tables and Nehru Place selection. Fixed shared dialog viewport overflow with bounded internal scrolling. Screenshot artifacts/screenshots/home-locality-records.png. A basemap network-error toast appeared during this check; data interactions remained functional. Map-click linkage to real locality records remains unfinished.

## Home records resilience — 2026-10-01

- Official context and news now load independently; one feed failure preserves the other. Cancelled loads do not update component state. A fetch failure is distinguished from expanding coverage.
- Extracted city/region selection with regression checks for separate latest totals, absent cities, cross-region exclusion and partial feed failure. No factual dataset or prediction changed.
- All 53 frontend tests, lint and TypeScript checks pass. Next: link verified locality records to map selection once matching geography is available, and continue public data acquisition.

## Red-zone explorer — 2026-10-01

- Added a time-aware red-zone summary and ranked sheet, available from the overview and floating map controls. Selecting a row opens its map neighbourhood panel. The list follows city, search, day type, crime type, year, and time-band selections.
- Unknown scores remain excluded from rankings and count separately. Glow and hatch layers now require a known score, so changing to an unsupported filter cannot briefly present a stale high-risk visual. Existing sample cells remain opt-in and prominently labelled synthetic.
- Browser checked the dark MapTiler map: the evening slider updated sample values, ranked sheet showed 9 high/very-high sample cells, and selecting a cell opened its detail panel and flew the map. All 56 frontend tests, lint, TypeScript check, and production build passed. The build still reports a large lazy MapLibre chunk.
- No real neighbourhood red zones are published: current NCRB values are annual city totals and the single reviewed news event does not establish complete neighbourhood/time observations. Continue public Delhi sourcing, boundary/exposure crosswalk work, then train and validate before publishing model scores.
- Public-source follow-up found [data.gov.in NCRB police-district annual tables](https://www.data.gov.in/catalog/district-wise-crimes-committed-against-women) and a [public Esri India district map service](https://livingatlas.esri.in/server1/rest/services/NCRB/District_Wise_Crime_Against_Women_2022/MapServer/0) exposing 2022–2024 category fields. Neither supplies neighbourhood or time-of-day observations. The Esri item licence and district-boundary provenance remain to be checked before any redistribution; the runtime could not reach its item metadata endpoint. No values from that service were imported.

## Official-source acquisition — 2026-10-01

- Reviewed the user's video visuals/captions; it contains no verifiable dataset or model method. No facts imported from it.
- Downloaded six original official PDFs: three Delhi Police statistics files, Haryana 2022 annual report, UP SCRB 2012 report and Rajya Sabha 4220/2026. Tracked acquisition manifest records timestamps, bytes and SHA-256 hashes; raw originals remain ignored/private.
- Reproducible reviewed importers stage 96 Delhi category/period records and six historical NCR police-district/category records. Delhi full/partial-year periods are separate. UP Table 8 geography/category columns and totals visually checked; G.B. Nagar is not split into Noida/Greater Noida. No neighbourhood labels or model outputs produced.
- Added policy-aware bounded downloader, signature checks, immutable raw-file reuse checks, and regression tests. All 32 Python tests pass. Frontend unchanged; preceding 56-test/build verification remains applicable.
- NCRB/data.gov.in automated collection stopped at live robots restrictions. Delhi transit static downloads require an identity/purpose form; left untouched. Existing OSM/DataMeet/Census inputs retained. No new key needed.
- Next: inspect Haryana scanned tables; normalize the Parliament totals with geography separation; extract remaining UP historical categories/range-month tables without treating them as neighbourhood/time bands; continue permitted recent district-source discovery and geography/exposure crosswalk. Production model training still requires granular labels and observed coverage.

## Haryana district extraction and recent Delhi totals — 2026-10-01

- Visually reviewed rotated Haryana 2022 district table, pages 16–18. Added explicit source transcription and hash-checked importer for eight cells: Faridabad/Gurugram × four source legal categories. District headers and page references retained; selected categories are not presented as total crimes against women.
- Visually reviewed Parliament answer 4220/2026 page 1. New importer extracts Delhi Police totals for 2023–2025 independently of NCRB metropolitan totals, excludes adjacent children/elderly columns and preserves leap-year period length.
- Normalized source-backed aggregate records now total 113 across four staged importers. No UI counts, neighbourhood model labels or scores changed. All 34 Python tests pass; frontend unchanged.
- Next: a validated multi-source aggregate publication/feed that preserves source, geography, category and period identity, then show district records as historical context in the home/evidence views. Continue remaining UP category extraction, recent district discovery and boundary/exposure matching. Never merge Delhi Police and NCRB metropolitan series without a documented crosswalk.

## Delhi police-district research deliverable — 2026-10-01

- Downloaded actual India Data Portal candidate CSV (2017–2022), its newer 2024 resource, and original NCRB 2024 Volume I PDF through OpenCity. Source receipt tracks exact links, hashes, byte sizes, retrieval date and declared licences. No key, login or permission document required.
- Extracted 2024's 15 Delhi geographic police districts and eight separate special units, including Rohini, Dwarka and Shahdara. All 49 raw categories and explicitly calculated leaf-only subtotals exported to CSV/JSON under data-pipeline/reports/delhi-districts. The 2022 verification supplement preserves 23 blank ransom cells as missing. No fabricated data or model training labels.
- Independently checked each category sum against original NCRB Table 3A.2 and the Delhi UT total against Table 3A.1: mirror subtotal 13,295, NCRB 13,396. Adult stalking alone differs (77 vs 178), accounting for the 101 gap; no district correction guessed. Rohini's mirror subtotal is 879, not a confirmed official district total. Its worked example and reproduction instructions are in METHODOLOGY.md.
- Administrative names are retained verbatim but excluded as police-boundary crosswalks; Dwarka's 2024 mirror mapping to Shahdara is flagged. No district map geometry or reference points manufactured. Mirror licence unspecified; outputs remain attributed research extracts outside the app feed.
- Verification: all 40 pipeline tests pass, including six new parsing/identity/reconciliation tests. Re-running extraction gives byte-identical CSV/JSON, and every CSV category cell matches its JSON counterpart, including blanks. Frontend unchanged by this research deliverable.
- Next for publication: establish rights/source district workbook, resolve or explicitly retain the stalking discrepancy, obtain matching police geography before any district symbols. Annual district volumes do not supply neighbourhood/time-band labels for the requested predictive model.

## Delhi district records in the app — 2026-10-01

- Added a home-screen entry and an independent Evidence-page district explorer for the real 2024 Delhi extract. Select Rohini, Dwarka, Shahdara or another reporting circle; see category cards, all 49 raw heads, source links and downloadable audit JSON. Geographic police districts and special units have separate selector groups. Historical volumes are not called risk scores.
- Home highlights the 13,131 calculated geographic-district heads separately from eight special units (164) and the earlier metropolitan series. The expanded explorer shows the combined 13,295 mirror subtotal, NCRB 13,396 comparison and adult stalking discrepancy (77 vs 178). No values changed or redistributed to districts.
- Added a hash-checked publisher and strict client loader with identity, missing-field, formula and reconciliation checks. The Delhi-only factual feed retains the mirror's unspecified-licence disclosure. Original all-India downloads remain private; map polygons and predictions unchanged.
- Browser visual testing was blocked by the browser tool's URL policy when binding the existing localhost tab. No browser bypass attempted. Local preview started on port 5174; visual/mobile checks still need completion in an accessible browser session.
- Verification: 59 frontend tests pass; lint, TypeScript, publication validation and production build pass. Final district tests rerun after the reporting-area guard. Production JSON is byte-identical to the publisher output, and the region-config diff changes only the optional city feed path. Existing large lazy MapLibre-chunk warning remains. No new API key required.

## District feed integrity follow-up — 2026-10-01

- Client loader now refuses omitted category comparisons, incomplete recorded-head scope, mismatched validation years and unknown/spurious discrepancy categories. An entirely absent special-unit series is missing, not an observed zero. Public crime figures unchanged.
- Five district regression tests, TypeScript, lint, publication validation and production build pass. Existing MapLibre chunk warning persists; browser visual checks remain pending under the previously recorded URL-policy block.
- Next acquisition milestone can reuse the already hash-checked 2024 India Data Portal CSV: actual rows exist for Haryana `Gurugram` and `Faridabad`, and UP `Gautambudh Nagar` and `Ghaziabad`. These rows were inspected for identity only; no new counts or totals published yet. Extract their 49 heads, retain source administrative names, and reconcile each full state's mirror series with original NCRB PDF rows 8 (Haryana) and 26 (UP). GBN must remain one district, without inventing a Noida/Greater Noida split. These annual district rows still do not supply neighbourhood/time-band prediction labels.

## Experimental district model and historical red references — 2026-10-01

- Trained actual LightGBM annual registered-rape-head model from 131 secondary-source observations (93 lagged examples), across 19 reporting units and five city groups, using hash-checked CSV inputs. No fabricated counts, 2023 gap fill, victim data, population rates or neighbourhood/time labels. Private artifact and reproducible training script; tracked evaluation includes whole-unit/city folds and 2024 temporal predictions.
- Temporal MAE 19.07 cases versus 22.11 for last observation. Delhi and GBN are worse than their baselines; other city summaries have one held-out target each. Report documents unseen two-year horizon, reporting changes and boundary-continuity uncertainty. Experimental recorded-volume forecast is not a production safety model; no future predictions or risk JSON released.
- Added source-backed red historical-volume markers for Central, Shahdara and Dwarka using explicit OSM ID/name pairs. Fixed-size approximate reference points, not district polygons, crime sites or danger radii. Marker click flies to reference and opens source/year/context sheet. Other 12 districts not assigned guessed coordinates. Sources/geometry reproduced by publisher; reference file configured in regions.json.
- Annual markers are independent of time bands, hidden in sample mode and unsupported crime/year filters; layer can be hidden/re-enabled. MapLibre markers survive theme changes and a geometry fallback also renders them with its existing schematic disclosure. Neighbourhood polygon predictions remain unchanged/empty.
- Verification: 42 Python tests and 63 frontend tests pass; lint and TypeScript checks pass. Browser visual verification remains pending due the previously recorded URL-policy block. Final production build check recorded below once complete. Next: source/reconcile remaining full-state district categories; obtain finer observed labels, denominators and matching geometry before neighbourhood/time predictions.
- Final production build and publication/reference validation passed. Existing large lazy MapLibre-chunk warning persists. No screenshots or browser interaction verification claimed for this change.

## Historical map filter follow-up — 2026-10-01

- Historical reference years now appear in the year selector even when production neighbourhood scores are empty; 2024 remains selectable without creating model scores. Sample-mode years exclude historical reference data.
- Closing/hiding a historical layer or choosing an unsupported filter also closes its selected reference dialog, preventing stale district context from remaining open.
- Three reference-filter tests, TypeScript, lint and production build pass. No crime data, model metrics or geometry changed. Existing MapLibre bundle warning and browser visual-check limitation persist. Next source/validation milestone remains the full-state Haryana/UP district extraction recorded above.
## Counts-only model milestone — 2026-10-01

- Latest task restricted work to ML/data preparation; no app UI, public crime feed or map geometry changed.
- Found existing local 2022/2024 NCRB district workbooks with explicit annual TOTAL columns. Preserved raw files, froze hashes and retained unknown original download URLs/dates. Extracted 38 real totals across 19 NCR police reporting districts. All six Delhi/Haryana/UP state/year sums reconcile to the workbook and independently to original NCRB Table 3A.1.
- Audited 2024 parent/child heads: stalking discrepancies are present in the original workbook, not just the mirror. Explicit annual totals are labels; no missing child cell repair. Saved reporting-unit mapping; no revenue/police boundary substitution.
- Trained regularised Poisson GLM and LightGBM Poisson count-only ablations; saved actual artifacts, runtime versions, seeds and hashes. Whole-district holdout MAE: persistence 136.26, GLM 157.65, boosted 242.57 cases. Persistence selected. Temporal 2022→2024 baseline backtest plus whole-city tests, calibration, bootstrap error/forecast uncertainty, seed and held-out permutation reports included. Learned models lack earlier complete lag/target pairs for honest temporal testing.
- Added tested exact-total downscaling, reviewed historical-context/adjacency readers, percentile/unknown handling, separate assumed time factors and local-only unavailable-source stubs. Neutral time factors assert no riskier window. Complete historical OSM context and matching police geography are missing, so no neighbourhood allocations or validated risk scores emitted. Versioned district research export separates real 2024 totals from estimated 2026 persistence and unknown time-band risk; neighbourhood GeoJSON explicitly empty, PMTiles deferred.
- Model card, source/acquisition manifest, missing-evidence list, EDA with three SVG figures and one-command retraining are recorded under data-pipeline and analysis. Prior model card retained as a legacy report. No new automatic download claimed for this run; previous downloaded PDF receipt reused for independent checks.
- Next: original older total workbooks and receipts, matching police boundary/crosswalk with historical context, then temporal comparison and neighbourhood allocation. Population/area correlations and Moran's I remain unavailable rather than invented. No new key is needed to reproduce current research.
- Verification: 56 pipeline tests pass. Full retraining produced identical SHA-256 hashes for all five saved artifacts; all six original-report reconciliation checks match. Versioned research export validates 19 districts × 12 unknown day/band entries. No frontend file changed. Raw files and existing untracked artifacts preserved.

## Model source-discovery follow-up — 2026-10-01

- Capacity available; inspected clean tracked Git state and the latest counts-only milestone. Continued earlier-total source discovery without changing UI scope.
- An exact indexed OpenCity NCRB 2021 Volume I download returned HTTP 404 through the policy-aware downloader; catalogue/resource pages returned 403 to the web reader. No bypass, guessed replacement URL, new file or numeric label. Exact attempt/failure recorded in the acquisition receipt, manifest and manual-download notes. Existing model data and outputs unchanged.
- Corrected manifest generation to retain subsequent acquisition rows and user annotations across retraining. All 57 pipeline tests pass. Full retraining preserves all nine manifest rows and produces identical hashes for all five saved model artifacts. This maintenance does not resolve the already reported geography/context/history evidence gaps.

## Primary historical Delhi map — 2026-10-01

- Latest task authorizes a historical map UI. `/` now has MapLibre basemap, left district search/list and right selected-district details; mobile uses horizontal district controls and a non-modal details sheet. Light/dark theme, zoom, pan, recenter, fly-to, keyboard-selectable symbols and official helplines retained. Previous neighbourhood features moved to `/neighbourhoods`; `/about` and `/evidence` preserved. `/methodology` explains sources, display choices and limitations.
- All 15 Delhi police districts use the original 2024 workbook's explicit annual total cells: geographic total 13,230, special units 166, combined Delhi UT 13,396. No parent/child double-counting, blank-to-zero repair, safety score or neighbourhood allocation. All 64 category columns and source discrepancies retained. Earlier mirror subtotals remain separately labelled in Evidence.
- Named public OSM references matched to the live Delhi Police directory. Coordinates checked against pinned raw OSM geometry and Delhi NCT outline. Matching police-district boundaries remain unavailable; circles are labelled approximate references, never incident locations, historical centroids or danger radii. Colour bands and exact screen-pixel diameter formula are display choices.
- Source hash, acquisition uncertainty, licences, regeneration command and route changes documented. No new crime-file retrieval claimed. Government-workbook original download URL/date and redistribution review remain unresolved.
- Verification: 70 frontend tests pass, lint and TypeScript pass, production build passes with the existing large lazy MapLibre chunk warning. Browser visual interaction/screenshots remain unverified under the previously recorded URL-policy block; no bypass attempted. Source-backed pipeline publication runs successfully; all 57 pipeline tests pass. Existing local port 5174 serves the new 2024/15-district feed; preserved its running server instead of restarting it.

## Historical source integrity follow-up — 2026-10-02

- District loader now recomputes source parent/child checks only to validate discrepancy disclosures: it refuses omitted, duplicated or altered comparisons, special units substituted for geographic districts, and invalid numeric display bands. It never repairs measured category values or headline totals. Missing values remain missing.
- Reviewed public ESRI NCRB layer metadata; LGD/Census district fields and polygon geometry do not prove matching police reporting units. Item reuse metadata was unavailable through the reader. Candidate excluded; exact reviewed URLs and limitations in ACQUISITION_LOG.md. No new crime file, boundary, licence or data value asserted.
- Updated NEXT_STEPS.md to distinguish the completed historical circles and trained counts-only research from still-unavailable neighbourhood/time safety estimates. Nine targeted district tests, lint, TypeScript and production build pass. Existing lazy MapLibre chunk warning persists. Browser visual QA remains pending under the recorded URL-policy restriction. No app layout or measured data changed.

## Publication validation coverage — 2026-10-02

- Included the new historical district feed in the existing `validate:data` command, using the same client loader and discrepancy checks. The publication gate now covers recorded district totals as well as the older mirror extract, risk, news, offenders and district references.
- Full publication validation and script lint pass. No crime values, model artifacts, map geometry or UI changed; existing untracked artifacts preserved. Source-provenance, matching geography/context and browser visual-review gaps remain unchanged.

## Collapsible historical map controls — 2026-10-02

- District controls now start as a glass capsule showing the recorded total and year. Click to expand search and the full district card; click again or press Escape to collapse. Legend uses the same disclosure pattern. Only one card expands at a time, with hidden content removed from keyboard navigation.
- Removed the empty right-hand details card. Selecting a district opens its details; the header collapses it to a name/count capsule. Clear-selection remains available. Mobile cards use bounded scrolling and avoid competing expanded sheets.
- Zoom/recenter controls are anchored in a separate bottom-right capsule, independent of district/card height. Camera padding follows the open card, with resize/padding applied before selection fly-to. Attribution stays visible above mobile navigation.
- Crime counts, categories, references, marker colours/diameters and model artifacts unchanged. Lint, TypeScript and production build pass; browser visual interaction remains unverified under the existing tool URL-policy restriction. User screenshots were used to identify the overlapping controls.

## NCR scope and map layers — 2026-10-02

- Expanded primary map to 19 reporting units: 15 Delhi plus Gurugram, Faridabad, Gautambudh Nagar and Ghaziabad. Existing hash-frozen original NCRB total cells yield a calculated selected-unit subtotal of 18,778 for 2024. GBN remains one district; no Noida/Greater Noida split. All six state/year reconciliations match original-report totals. Blanks, all 64 category columns and discrepancies are preserved. New public-place references reuse actual OSM geometry and government locality context; no police boundary invented.
- Default clustered help layers use the existing partial OSM snapshot (3,733 features). Per-category filters hide/show police, hospitals, metro and buses. Fire-station records remain absent. Bounded emergency refresh was blocked by robots policy before query; receipt/source/manifest/manual notes recorded, no bypass or fake update.
- Added detailed light/dark streets and satellite-with-labels alongside muted map. Configured MapTiler styles responded HTTP 200; no new key needed. Place/shop labels depend on zoom/provider coverage. Source/layer restoration and camera preservation retained through react-map-gl and style icon recreation; visual interaction remains unverified under the existing browser URL-policy block.
- Added optional low-confidence assumed time/activity illustration; count-rank, judgement time factors and mapped-transit adjustment are disclosed, missing inputs are unknown. This is separate from trained research; no validation claims or measured time values. Recorded counts remain unchanged. Neighbourhood estimates still require matching police boundary/crosswalk and context weights, so none invented/exported.
- Removed convicted-person UI/cards and emptied the public offender feed. Removed Our approach navigation; old About/methodology routes redirect to the crime-data page, which retains source/limitation notes. Existing historical model artifacts and all original raw inputs preserved.
- Verification: all 79 frontend tests, lint, TypeScript and publication validation pass. Production build result recorded below. Next: permitted refreshed OSM export, matching police geography/context and actual occurrence-time observations; complete visual QA when browser access is available. Existing untracked artifacts preserved.
- Final production build passes. Existing large lazy MapLibre chunk warning persists; no browser screenshots/interaction claims. Full Python regression result recorded after completion.
- All 57 Python pipeline regression tests pass. New publisher reproduced the NCR feed with source/reconciliation checks intact.

## Police-geography discovery follow-up — 2026-10-02

- Usage available; tracked working tree clean, existing artifacts preserved. Reviewed government South West police-jurisdiction page with West/South West/Dwarka headings. Page-update date does not verify geometry vintage or correspondence to 2024 records. Policy-aware HTML acquisition stopped because robots policy could not be read; no file, polygon, coordinate or model input added. Exact URL, failure and reuse caveats recorded in source/acquisition/manual notes and manifest.
- Matching neighbourhood allocation remains gated on reviewed police geography/context. No new user action or changed blocker; app/data/model untouched. Documentation-only follow-up; no repeat tests needed.

## Supplied context and location milestone — 2026-10-02

- Imported supplied locality, population and 20 daily traffic files with original hashes and reproducible parser. Swapped coordinate headings corrected in memory. Missing/out-of-NCR references rejected; 153 retained, 78 with road-probe observations, six source-density matches, 73 population matches (67 ward-name-only). All locality crime totals remain unknown; no fabricated police crosswalk or retraining metrics.
- Transparent H3 reference-cell shading uses separate assumed time/activity rules with optional source-density rank adjustment; historical probes, not live traffic/footfall. No neighbourhood boundaries or calibrated safety scores asserted. Matched population is shown as context. Original datasets and large untracked traffic folder preserved.
- Square facility pins and square clusters distinguish help from recorded red circles. Main-map GPS is consent-only, high-accuracy requested, blue glowing device dot plus accuracy circle, cleared on stop/unmount. On-device rule-generated awareness summary uses IST/day/time and historical traffic/population, voluntary native sharing and nearest mapped police reference. No location transmission/storage or live LLM claim.
- Added 43 documented MapTiler catalogue variants plus three presets; catalogue fetched with policy checks/hash. No claim of account availability for every style. Automatic streets/muted follow theme; explicit variant choices retain their style. Source/licence/reuse gaps documented in SUPPLIED_CONTEXT_REPORT.md.
- Verification: initial full suite 86 tests passed; final consent/density regressions pass in the 12-test targeted suite. TypeScript, lint, publication validation and production build pass; existing lazy MapLibre chunk warning persists. Browser visual QA remains pending under the existing URL-policy block. No API key needed for local advice; no measured crime values/model artifacts changed.
- Final full frontend suite passes: 89 tests. Shared reference cells are merged into 129 polygons to avoid unintended opacity stacking. Density and location-consent regressions pass. A final source-date-range guard and production build are checked before commit. Regional crime background is shown separately from unknown locality counts.
- Final type-check, lint, publication validation and production build pass after GPS outside-coverage handling. Parser rerun validates each probe date-range reference and reproduces 153/78/6/73 counts. All 89 frontend tests pass; no visual QA claim. Original user files remain untracked and untouched.

## Supplied traffic validation follow-up — 2026-10-02

- Usage available; inspected tracked state and preserved the supplied untracked CSV/traffic files and artifacts. Tightened traffic importer to require all 20 distinct dates in the declared August 11–30, 2024 interval, leading metadata, one date range, and exactly 24 distinct whole-hour time sets/IDs. It refuses incomplete/misdated sources instead of silently retaining the full-period label.
- Added regression coverage for missing/duplicated/partial hours, wrong reporting periods, missing metadata and correction of swapped population coordinate headings without altering input rows. Full pipeline suite: 61 tests pass. Complete source-data rerun produces a byte-identical public context export with unchanged 153/78/6/73 coverage. No app, crime counts, model or source files changed. No new user action or evidence gap.

## Trained ML and model-aware shading/advice — 2026-10-02

- Fitted and compared persistence, regularised Poisson GLM and LightGBM Poisson using 109 real matched 2022/2024 reporting units across Delhi/Haryana/UP. All six state/year totals reconcile independently with NCRB report totals. No invented labels, time observations or neighbourhood counts. Saved five disjoint-unit folds, whole-city holdouts, calibration/rank/hotspot metrics, paired bootstrap, seeds and artifact hashes.
- Selected Poisson on pooled MAE 160.99 vs persistence 165.55 and LightGBM 180.71 cases. Improvement is small; its paired bootstrap interval includes zero. Combined NCR transfer MAE 154.55 is worse than persistence 136.26. Only one cohort exists; future-year validation and reviewed police geography remain unavailable. Exported 19 explicitly experimental 2026 forecasts separately from recorded 2024 totals, local estimator/config and assumed reference-cell GeoJSON. Old counts-v1 artifacts preserved.
- Main-map transparent reference-cell shades now depend on learned annual-volume ranks plus explicitly assumed spatial interpolation and time/activity/density adjustments. Grey means unknown; locality reportedCases/riskScore remain null. District details show the separate model forecast. GPS summary reports experimental context rather than declaring current danger.
- Added optional genuine generative advice via loopback Ollama service. Strict anonymous categorical request schema refuses GPS/name/count/prompt fields; no logging/storage/cloud calls. User-triggered generation, abort/stale-response handling and rule fallback retained. Ollama is not installed/running here, so live generation needs local runtime/model setup and is not claimed tested. No API key needed.
- Verification: 95 frontend tests, 64 Python pipeline tests, TypeScript, lint, publication validation and production build pass. Existing lazy MapLibre chunk warning remains. Browser screenshots/visual interaction remain unverified under the existing URL-policy restriction. Supplied originals and untracked artifacts preserved.

## Simplified polygon levels and Help nearby — 2026-10-02

- Removed both scenario checkboxes and the alternate assumed district-circle mode. Model cell shading is automatic; historical district circles retain recorded-count colours/diameters. Clicking a cell shows its supplied reference name(s) and one of Low / Medium / High / Very high; missing or invalid estimates remain Unknown. Display cut-offs are 25, 50 and 75 on the experimental index; corresponding four red shades match the popup levels. Legend retains the model-estimate and approximate-cell disclosures; these are not verified ward polygons or official risk classifications.
- Help nearby capsule defaults to police stations and hospitals only. Metro is an optional unchecked category; bus/fire overlays are removed from this screen's selectable categories. Layout and time controls remain available. No source records or model outputs changed.
- Type-check, lint, four model-display regressions and publication validation pass. Browser visual QA remains unverified under the existing URL-policy restriction. Production build result recorded after completion.
- Production build passes with the existing large lazy MapLibre chunk warning. No crime/model/source data changed.

## Local-time advisory and automatic location — 2026-10-02

- Added user-requested time-only advisory fallback: 20:00–06:00 High, 06:00–10:00 Medium, 10:00–17:00 Low, 17:00–20:00 Medium. For available model indices at 22:00–06:00, Low upgrades to Medium and Medium to High; High/Very high never downgrade. Outer or lower-density references have a High minimum then. Outer is explicitly assumed >20 km from configured region centre; lower density means below the median of available supplied density values. Missing density is never interpreted as low. Rules are not learned or measured risk facts.
- Polygon shades/popups and GPS advice use the same categorical rules. Hourly time selector includes Current time, refreshed each minute using the configured timezone. The model's unknown/null values remain unchanged in exported data; display fallback is labelled advisory. Existing measured crime feeds and trained model artifacts untouched.
- Replaced long missing-data narrative with a short level badge and calm practical advice, plus the requested reminder to remain aware/careful. Evidence and limitations stay in expandable context and the legend. Added restrained entry animation, sticky close header, readable copy, bounded scrolling and reduced-motion support.
- Already-granted browser geolocation permission resumes the client-only watch automatically on mount and centers/zooms when its first position arrives. New permission retains consent flow; Stop and unmount clear GPS. No location storage. Privacy/AI requests remain anonymous categories only.
- Type-check, lint, 14 targeted advisory/model/privacy/location regressions and publication validation pass. Visual QA remains pending under the existing browser URL-policy block; no screenshot claims. Production build result recorded after completion.
- Production build passes with the existing large lazy MapLibre chunk warning. Changes committed separately from the preserved supplied raw datasets.

## Detailed automatic advice card — 2026-10-02

- Removed How this advice is formed and Generate AI advice locally from the location card, including all AI request state/calls and runtime setup text in this component. Existing optional server/library remains available for future work but the card makes no generation request. Automatic on-device wording is not described as live AI.
- Expanded each advisory level's precautions with route/pickup planning, booking verification, phone readiness, optional journey sharing/check-ins and practical responses to discomfort. Retained awareness/care reminder, emergency contact, short estimate disclaimer, auto-location and explicit native share. Crime/model/source data unchanged.
- Type-check and lint pass. Targeted advisory/location tests and production build are verified before commit. Browser visual QA remains pending under the existing URL-policy block.
- Seven targeted tests and production build passed before the advice-card commit; the existing lazy MapLibre chunk warning remains.

## Unified map location control and wordmark — 2026-10-02

- Removed the standalone Locate me button. The control beside zoom +/− now triggers the existing consent flow or flies to the device position when location is enabled; it previously recentered the whole NCR region. The capsule remains anchored in the existing position. Automatic zoom for previously granted permission is retained.
- Header now renders Kaali directly as text, using the existing brand typography and theme text colour. Public SVG variants remain preserved. No model/crime/source records changed.
- Type-check and lint pass. Relevant location/advisory tests and production build are verified before commit; visual browser QA remains pending under the existing URL-policy restriction.
- Seven relevant tests and production build pass. Existing large lazy MapLibre chunk warning remains; no runtime browser verification claimed.

## Handoff consistency — 2026-10-02

- Usage available; tracked checkout clean, supplied untracked datasets/artifacts preserved. Updated NEXT_STEPS.md to match the latest ML cohort, automatic advisory shading, simplified advice, single location control and help-layer defaults. Removed stale statements about optional scenario switches and persistence being the selected latest model; retained the distinct older cohort and all evidence/visual-review gates. Documentation only; no app/source/model changes or repeated runtime checks.

## Collapsible surroundings capsule — 2026-10-02

- Your surroundings now collapses/reopens through an accessible disclosure header. Collapsed capsule keeps the current advisory level visible; hidden advice/actions are removed from keyboard navigation. Collapsing preserves the GPS watch, position and map dot. Separate Stop location remains inside the expanded card and still clears GPS. Chevron motion respects reduced-motion preference.
- Type-check and lint pass. Production build is checked before commit; visual browser QA remains pending under the recorded URL-policy block. No crime/model/advisory rules or supplied files changed.
