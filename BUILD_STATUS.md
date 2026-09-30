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
