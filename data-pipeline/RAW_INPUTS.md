# Delhi Phase 1 inputs

Run from the repository root:

```powershell
.venv/Scripts/python.exe data-pipeline/phase1.py --stage-existing
.venv/Scripts/python.exe data-pipeline/phase1.py --environment
```

The first run copies previously downloaded files into ignored `data-pipeline/raw/` without overwriting existing files. The checked-in manifest `config/phase1-inputs.json` pins their SHA256 hashes, sources, licences and retrieval dates. Subsequent audits use those exact bytes. Missing inputs stay missing; changed files require review. `public/data/reports/delhi-phase1.json` is the generated quality report. These commands do not publish risk predictions.

| File under raw/ | Use | Status |
| --- | --- | --- |
| `opencity/metros-2022.csv` | Three Delhi annual NCRB context rows | Retrieved, hash pinned |
| `datameet/Delhi_Wards.geojson` | 290 historical boundary candidates | Retrieved; current vintage unverified |
| `osm/help-2026-09-29.geojson` | 3,733 NCR help features | Retrieved; individual city assignment unverified |
| `census/DDW_PCA0706_2011_MDDS with UI.xlsx` | Central Delhi 2011 ward population candidate | Supplied locally; 21 ward-part rows imported and reconciled |

## Census workbook received and reviewed

The requested workbook is now present. Its 21 urban ward-part rows reconcile to the district and town totals. Only population and geographic identifiers are imported; caste, employment and other columns are excluded. The checksum is pinned in the input manifest.

```powershell
python data-pipeline/import_census.py --input "data-pipeline/raw/census/DDW_PCA0706_2011_MDDS with UI.xlsx"
```

The importer requires openpyxl from requirements.txt. This run used the bundled Python environment. Output is `public/data/census-central-2011.json`. Original workbook bytes remain unchanged and ignored by Git. Acquisition is labelled user-supplied: the official catalog metadata matches, but remote bytes could not be independently compared. The original download timestamp is unknown; 2026-09-30 is the local review/receipt date.

This is Central district only, according to 2011 geography. Composite state/district/subdistrict/town/ward keys preserve split ward parts. No current neighbourhood boundary join or current crime-rate denominator is claimed. No further manual file is requested at this milestone.

## Environmental preprocessing

`--environment` can stage observed OSM feature summaries for the historical candidate geometries under `private/phase1/` on a working geospatial runtime. It never joins crime counts or publishes risk. Both files retain their independent provenance. The OSM help snapshot selects only help amenities and lit main roads, so it cannot estimate total POI density, footfall or the fraction of all roads that are lit. Lighting stays null without a complete inventory and explicit lighting tags. Distance features refer only to the mapped subset.

On this Windows host, Application Control blocks pyproj's transformer DLL as well as the previously identified scikit-learn binary. The audit still runs; environmental staging is reported unavailable. No security policy was altered and no geographic approximation substituted. Use an allowed Python environment with `requirements.txt` for geospatial preprocessing and eventual training; real training labels are still missing.

## Deferred inputs

SafeCity, Safetipin, private police/RTI datasets remain unavailable stubs. Delhi Open Transit currently presents a download form requiring identity and terms acceptance; no form has been submitted. Existing OSM transit features remain available. Public news extraction is enabled separately in NEWS.md under the user's latest instruction.

## Runtime recovery — 2026-09-30

Fresh project-runtime checks now pass for tables, geometry, projection, news extraction and a tiny synthetic LightGBM fit. Installed the already-declared openpyxl dependency. No Application Control setting was changed. Earlier runtime-blocker statements are superseded by this successful check; the reason host behavior changed is unknown.

`phase1.py --environment` now stages 290 historical candidate environmental rows privately. Boundaries remain historical/unverified, lighting fraction remains unknown for the incomplete inventory, and crime/exposure joins remain absent. No production model or metrics generated. 27 Python tests pass. Runtime readiness does not fix missing labels or coverage.
