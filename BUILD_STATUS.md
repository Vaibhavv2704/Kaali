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

Production neighbourhood records are empty. The 18 synthetic sample cells are software fixtures only. The existing 3,733 OSM features are real retrieved map data with unverified city assignment. No production model, metrics, jurisdiction geometry or new case matches were created. No data source was fetched or newly verified in this UI milestone.

## Latest data/pipeline milestone

- Installed the Python requirements in ignored .venv. Four synthetic-only validation tests pass; no fixture is published or used to claim model performance.
- Reject unknown estimated flags, non-finite exposure/counts, fractional observed counts, missing source URLs/identifiers and reversed periods. Allocation now rejects infinity.
- Training dependencies load when training is invoked so data validation can run independently. Actual scikit-learn execution is blocked by Windows Application Control on its _libsvm binary; no policy was changed. A permitted training environment is required.
- Expanded both source registers with exact official table URLs, geography, partial-year caveats, reuse restrictions, access failures and all six city gaps. Corrected the stale OSM collection status. OpenCity robots disallows its API; do not retry that route.
- No new incident counts, boundaries, model scores or metrics were published.

## Next independent work

1. Audit location lifecycle: asynchronous boundary arrival, region changes, city detection independent of available risk records, and clearing all location UI on stop/error. Add tests without sending or retaining user coordinates.
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

Latest result: lint, TypeScript, 36 unit tests, publication-schema validation and production build passed. The build retains the existing large lazy MapLibre chunk warning. Browser checks used the keyless basemap fallback and labelled synthetic cells; live MapTiler services and physical-phone frame rate remain unverified.

`pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm validate:data`, `pnpm build`.

Use the workspace’s installed tooling. On this Windows host, pnpm is available at `C:/Users/vaibh/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/pnpm.cmd`. Vite/esbuild checks may require the normal approved execution outside the filesystem sandbox because they inspect ancestor directories. Keep screenshots in `artifacts/screenshots/`; do not commit private credentials or local browser storage.
