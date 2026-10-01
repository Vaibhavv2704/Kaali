# Missing evidence for counts-v1

No download URL below is guessed. These gaps do not prevent the included counts-only run. They prevent claiming a validated complete neighbourhood/time risk model.

| Required evidence | Public starting point / status | Intended local destination |
|---|---|---|
| Original acquisition receipts for the existing NCRB 2022 and 2024 district workbooks | [NCRB](https://ncrb.gov.in/), Crime in India district annexures. Exact original workbook URLs and retrieval dates are unknown. Preserve the current files and their hashes. | `data-pipeline/sources/` receipt with exact URL, year, hash and acquisition date |
| Earlier original district **TOTAL** tables, preferably 2020 and 2021 | [NCRB](https://ncrb.gov.in/) and [data.gov.in district crimes against women catalogue](https://www.data.gov.in/catalog/district-wise-crimes-committed-against-women). No verified direct original URL located; prior automated robots restrictions retained. Do not treat incomplete mirror leaf sums as totals. | `data-pipeline/raw/ncrb/` (retain actual downloaded filename; no server filename inferred) |
| Police-district polygons with reporting-year continuity and complete ward/H3 crosswalk | Published jurisdiction geography from the relevant authority. [DataMeet municipal data](https://github.com/datameet/Municipal_Spatial_Data) wards alone are not matching police boundaries. No authoritative NCR police partition currently found. | `data-pipeline/raw/boundaries/`; reviewed crosswalk and adjacency in `data-pipeline/interim/counts-v1/` |
| Complete night context: roads/classes/dead ends/isolation, land use, transit and opening_hours POIs | [Overpass](https://overpass-api.de/) or [Geofabrik India extracts](https://download.geofabrik.de/asia/india.html), subject to service limits/ODbL. Existing help extract is incomplete. Need source timestamp, query/extract coverage and matching geometry. Historical backtests need historical snapshots. | `data-pipeline/raw/osm/`; reviewed `night-context.json` in `data-pipeline/interim/counts-v1/` |
| Density / built-up allocation weights and bias denominators matched to police districts | [Census](https://censusindia.gov.in/), WorldPop/GHSL with checked product licence and reporting geography. Existing Central Delhi PCA alone is insufficient. | `data-pipeline/raw/population/`; reviewed context/crosswalk in interim |
| Finer aggregate crime and actual time-band counts | Public statistical releases if available; otherwise RTI per jurisdiction. Never raw FIRs or victim identifiers. SafeCity reports and Safetipin audits require separate provenance review when supplied. | `raw/rti/aggregate-counts.json`, `raw/safecity/aggregate-counts.json`, `raw/safetipin/` (environment audits, not assumed crime counts) |

The free-form filenames above are local destinations, not claims that particular files exist on a server. No fabricated download attempts, CAPTCHA bypass or purchased access. Annual aggregate counts cannot supply observed four-hour distributions.

### Verified failed link (2026-10-01 follow-up)

The indexed 2021 Volume I link `https://data.opencity.in/dataset/09182f51-d3da-4aa6-b4fe-2b9f636e39d8/resource/b3bbdf99-4679-444c-9d49-880f509141e1/download/cii_2021volume-1.pdf` returned HTTP 404. Its intended local destination was `raw/ncrb/cii-2021-volume-1.pdf`; that file does not exist. The current [2021 catalogue](https://data.opencity.in/dataset/national-crime-data-2021) and [Volume I resource](https://data.opencity.in/dataset/national-crime-data-2021/resource/c14b3e6b-825a-460d-8b3f-03a3f3bf917e) surfaced in discovery but returned 403 to the web reader. Their current download URL was not guessed. A volume report alone may still lack district totals; acquisition would be for primary category/aggregate verification, not automatic model labels.

## NCR emergency refresh — 2026-10-02

Automatic collection from https://overpass-api.de/api/interpreter was blocked by robots policy. If a permitted open OSM export is supplied, place the original file and source/licence/date receipt under data-pipeline/raw/osm/ for parser review. Do not bypass policy or claim an absent refresh. Existing mapped help remains available; fire records are missing. No specific downloadable file URL was verified, so none is guessed.
