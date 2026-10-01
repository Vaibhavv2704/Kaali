# Counts-v1 acquisition log — 2026-10-01

This run used existing files, and downloaded **no new crime or context file**. Acquisition date is not inferred from a filesystem timestamp. Prior automated downloads and exact URLs are in `reports/acquisition-2026-10-01.json`, `reports/ACQUISITION-2026-10-01.md`, `sources/delhi-district-2024-receipt.json` and SOURCES.md.

| Action | Result |
|---|---|
| Inspect raw NCRB directory | Found existing 2022/2024 district workbooks with explicit total columns. Original download receipts unavailable. Frozen SHA-256 in config/counts-v1.json and manifest.csv. |
| Inspect reporting units and all state/year totals | 38 NCR geographic observations; Delhi/Haryana/UP sums reconcile in both years. Special units counted in reconciliation but excluded from modelling. |
| Inspect adjacent adult/girl category subtotals | 2024 stalking parent/child inconsistencies retained and exported. Explicit total labels not recomputed from inconsistent children. |
| Search public web for original 2020/2021 district workbooks | No verified direct original download URL located by the search. Mirrors surfaced, but snippets supplied no training numbers. No guessed download attempted. |
| Reuse existing India Data Portal CSVs | Not used for TOTAL labels: older Delhi leaves include missing cells; latest child sum differs from original totals. Mirrors have unspecified licence. |
| Inspect existing OSM/DataMeet/Census evidence | Help-only 2026 inventory, historical administrative wards and Central Delhi 2011 Census do not provide matching historical police context/adjacency/population. No new interpretation of absence as zero. |
| Training and export | Counts-only models run on genuine totals. Risk stays unknown; no neighbourhood geometry, current danger or time-of-day counts fabricated. |

Previously recorded direct NCRB/data.gov.in automated collection encountered robots restrictions; India Data Portal automated requests returned 403. The earlier browser-mediated mirror downloads are recorded separately. This run did not bypass those restrictions. Delhi Open Transit static downloads previously required an identity/purpose form and were left untouched. SafeCity, Safetipin and RTI are unavailable; local-only aggregate reader stubs added without external requests.

## Evidence still required

See MANUAL_DOWNLOADS.md. No extra API key or paid service is required to reproduce the completed counts-only experiment. Missing source URLs remain blank in the manifest, not invented. Reuse/publication clearance and matching geography are separate from ability to train a retrospective count ablation.

## Earlier-year discovery follow-up — 2026-10-01

- Public discovery found an exact older OpenCity NCRB 2021 Volume I PDF link and a current National Crime Data 2021 catalogue. The catalogue/resource pages returned HTTP 403 through the web reader. No login or access-control workaround attempted.
- The previously indexed, explicit PDF URL was tested using the existing bounded, robots-aware downloader at `2026-10-01T15:47:20.329253+00:00`; it returned HTTP 404. No PDF was retrieved, no SHA-256/retrieval date assigned, and no numbers taken from search snippets. Exact attempted URL, failure and declared licence caveat are retained in `reports/counts-v1/acquisition-followup.json`, `config/counts-history-downloads.json` and `manifest.csv`.
- Searches did not reveal a verified original 2020/2021 district-total workbook URL. Existing incomplete mirror heads remain excluded from total-count labels. Training inputs, metrics, risk exports and app files unchanged.
- Fixed receipt maintenance so retraining preserves later successful/failed acquisition rows and free-form manifest annotations rather than overwriting the log. Regression test added.

## Historical map integration — 2026-10-01

- Read the actual public Delhi Police district directory at https://yuva.delhipolice.gov.in/contact-us.html through the web reader. Matched public station/locality names to district labels. No staff contact data or page body retained; no new downloaded file or file hash assigned to this page review. Directory terms/open licence not established.
- Reused frozen original 2024 district workbook, independently downloaded NCRB report and original OSM help snapshot. No new crime file downloaded, no new acquisition date inferred. The publisher verifies hashes, original-report reconciliation, all 15 identities, reference geometry and Delhi NCT containment.
- Published 2024 recorded totals/category cells and approximate district reference places. Geographic total 13,230 plus separately excluded special units 166 equals Delhi UT 13,396. These are historical recorded volumes, without safety scores, inferred neighbourhood counts, danger radii or fabricated district polygons.

## Geography discovery follow-up — 2026-10-02

- Reviewed the actual public layer metadata at https://livingatlas.esri.in/server1/rest/services/NCRB/District_Wise_Crime_Against_Women_2022/MapServer/0 . Despite its URL suffix, fields include 2024 crime categories, district names, LGD codes and Census codes. This does not establish correspondence to all Delhi police registration circles or historical police boundaries. No crime figures were imported from the page or search results.
- Discovery item: https://www.arcgis.com/home/item.html?id=15807229ed3342939bfabd8c9606f25e . The page reader returned no usable content. Exact metadata endpoints https://www.arcgis.com/sharing/rest/content/items/15807229ed3342939bfabd8c9606f25e?f=pjson and https://www.arcgis.com/sharing/rest/content/items/cf2747ea37fd4daf9152ffd87f71519f?f=pjson were not accessible through the web tool. No alternate access attempt, download, invented receipt or licence claim.
- Candidate excluded from app/model geography pending reporting-unit correspondence, year continuity and reuse verification. Existing recorded counts, OSM reference coordinates and model outputs unchanged.

## 2026-10-02 NCR map extension

Reused original local NCRB 2022/2024 workbooks and existing original-report PDF, with hash validation and six state/year reconciliation checks. No new crime download. Added four public-place NCR references from existing OSM snapshot using government locality-context pages listed in SOURCES.md; police boundaries are not asserted. See NCR_MAP_METHODOLOGY.md.

Emergency refresh: https://overpass-api.de/api/interpreter, bounded query and receipt in sources/ncr-emergency-2026-10-02.json. Robots policy disallowed automated download before the data request. No file/hash, alternative-host bypass or synthetic facility record. Existing 3,733-feature help snapshot retained. Detailed streets and hybrid MapTiler styles returned HTTP 200; credentials excluded from logs.

## Police-jurisdiction source discovery — 2026-10-02

Reviewed https://dmsouthwest.delhi.gov.in/jurisdiction-maps-of-district/ through the web reader. The District South West government page explicitly labels maps for Police District West, South West and Dwarka, and reports a page update of September 1, 2026. That date does not establish the maps' reporting year or compatibility with NCRB 2024 units. The reader exposed headings but no geometry/download links. A policy-aware attempt to obtain the HTML for exact image/link discovery stopped because robots policy could not be read. No file or geometry was acquired; no alternative-host bypass attempted. Byte-acquisition audit: raw/acquisition-audits/ (URL-hash receipt). Candidate remains unverified for allocation, and no app/map data changed.

## Supplied-context preparation — 2026-10-02

Read original workspace locality/population/traffic files, preserving originals; Desktop paths absent. Exact 23 hashes/byte sizes and 20 traffic-date/coverage summaries in sources/supplied-locality-context.json. Swapped coordinates corrected in memory. 153 accepted locality references; 78 with historical probe matches, six density matches, 73 population matches. Ward name matches are not spatial joins. No local crime label or district allocation added. No new crime download.

Policy-aware MapTiler public client mapstyle.ts download succeeded; original raw receipt stores retrieval timestamp/hash under raw/acquisition-audits. Parsed 43 metadata variants without explicit active deprecation flags. Full methodology: SUPPLIED_CONTEXT_REPORT.md.
