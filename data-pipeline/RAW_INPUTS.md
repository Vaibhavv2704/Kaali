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
| `census/DDW_PCA0706_2011_MDDS with UI.xlsx` | Central Delhi 2011 ward population candidate | Missing; official catalog/download access failed |

## One file needed next

Download **DDW_PCA0706_2011_MDDS with UI.xlsx** from the [official Census catalog, PC11_PCA-TV-0706](https://censusindia.gov.in/nada/index.php/catalog/6286/study-description) and place it at:

`data-pipeline/raw/census/DDW_PCA0706_2011_MDDS with UI.xlsx`

The official site returned SSL errors through Python and 502 through web access on 2026-09-30. Certificate checks were not disabled. Once supplied, the workbook needs column, geographic-code, licence and vintage review before adding its checksum and parser. The manifest deliberately refuses to import an unreviewed file. This is Central district only; it is a starting input, not all-Delhi coverage. Ward numbers alone are not unique join keys and 2011 geography must not be treated as current boundaries.

## Environmental preprocessing

`--environment` can stage observed OSM feature summaries for the historical candidate geometries under `private/phase1/` on a working geospatial runtime. It never joins crime counts or publishes risk. Both files retain their independent provenance. The OSM help snapshot selects only help amenities and lit main roads, so it cannot estimate total POI density, footfall or the fraction of all roads that are lit. Lighting stays null without a complete inventory and explicit lighting tags. Distance features refer only to the mapped subset.

On this Windows host, Application Control blocks pyproj's transformer DLL as well as the previously identified scikit-learn binary. The audit still runs; environmental staging is reported unavailable. No security policy was altered and no geographic approximation substituted. Use an allowed Python environment with `requirements.txt` for geospatial preprocessing and eventual training; real training labels are still missing.

## Deferred inputs

SafeCity, Safetipin, private police/RTI datasets remain unavailable stubs. Delhi Open Transit currently presents a download form requiring identity and terms acceptance; no form has been submitted. Existing OSM transit features remain available. Public news extraction is enabled separately in NEWS.md under the user's latest instruction.
