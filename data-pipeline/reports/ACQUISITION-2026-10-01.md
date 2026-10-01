# Public-source acquisition — 1 October 2026

Six original government PDFs were downloaded unchanged. `acquisition-2026-10-01.json` records actual retrieval timestamps, URLs, byte sizes, SHA-256 hashes, HTTP metadata and robots checks. Raw files are private/ignored; no personal case records were extracted.

## Reviewed counts

| Source | File under raw/ | Finest reviewed geography | Extracted records |
| --- | --- | --- | --- |
| Delhi Police crimes against women | delhi-police/caw-2013-2022.pdf | Whole Delhi Police coverage | 96 category/period rows: 8 categories × 12 periods |
| Delhi Police general crime | delhi-police/crime-2011-2022.pdf | Whole Delhi | Preserved; overlapping counts not added |
| Delhi Police historical general crime | delhi-police/crime-2001-2010.pdf | Whole Delhi | Preserved; not imported |
| UP SCRB Crime in Uttar Pradesh 2012 | up-police/crime-in-up-2012.pdf | Historical police districts | 6 rows: 3 categories each for Ghaziabad and G.B. Nagar |
| Haryana Police Annual Administrative Report 2022 | haryana-police/annual-admin-2022.pdf | Pending scanned-table inspection | Preserved; no counts imported |
| Rajya Sabha question 4220, 1 April 2026 | parliament/rs-4220-2026.pdf | Whole Delhi Police coverage | Preserved; 2023–2025 totals identified, not yet normalized |

Delhi table page 1 was visually checked: full years **2012–2021**, then separate **1 January–15 July 2021 and 2022**. The source download-page title is not the reporting period. Never sum full and partial periods, or duplicate the general-crime table. Legal categories remain source-specific, including combined 498-A/406.

UP PDF page 25 / printed page 18 / Table 8 was visually checked. Ghaziabad has 41 dowry-death cases, 31 rape cases and 220 kidnapping/abduction cases concerning women and girls. G.B. Nagar has 17, 19 and 115 respectively. These are selected categories, not total crimes against women. Row-wide sums reconcile against the printed general crime-against-body totals. Geography is from 2012; no current district/commissionerate crosswalk has been asserted. G.B. Nagar is not duplicated into Noida and Greater Noida.

The UP report also contains state-level annual categories and range-level monthly tables (printed pages 210–213). A range is not a police district, and a month is not a time-of-day band. Further extraction is queued with these distinctions intact. Haryana's report is image-based in the inspected pages and needs visual/OCR table review.

## Reproduce

Run from the repository root with the project Python environment:

```powershell
python data-pipeline/public_download.py data-pipeline/config/public-downloads-2026-10-01.json
python data-pipeline/public_download.py data-pipeline/config/additional-downloads-2026-10-01.json
python data-pipeline/import_delhi_police.py
python data-pipeline/import_up_police.py
python -m unittest discover -s data-pipeline/tests
```

Existing raw files are reused only if their saved acquisition checksum matches. Changed files require review. Normalized outputs remain in `raw/normalized/`, with provenance, period length, source geography and `trainingEligible: false`.

## Remaining acquisition work

- NCRB latest published report identified as 2024; obtain permitted report files for 2020–2024. Live robots policy disallows automated access. Do not work around that restriction.
- data.gov.in catalog identifies police-district annual data, but the live robots policy disallows automated access. No CSV bytes obtained in this pass.
- More recent district tables for Delhi, Haryana and UP remain sought; no police-station series found in this pass. Haryana scanned report review remains useful independent work.
- Delhi Assembly searches returned debates/staffing rather than the required statistical annexure; no unrelated figures imported.
- Existing DataMeet historical wards, OSM Delhi boundary/help features and Central Delhi Census workbook retained; they do not establish a current neighbourhood/population crosswalk. Census catalog access failed again in the web tool.
- Delhi Open Transit bus/DMRC static downloads request name, email, purpose and terms acceptance. No form submitted, identity invented or gated endpoint used. OSM transit inventory remains available.

## Video review

Reviewed all 26 sampled seconds of the user's local video visually, including captions. It shows glowing red map spots and a case sidebar and cites NCRB generally. It gives no table IDs, source files, geographic allocation method or model validation. No audio transcription was performed. It is a design reference, not crime evidence; no identities or numeric claims were imported from it.

## Model implications

This pass adds genuine historical district data, but still no neighbourhood/time-band observations, matched female exposure or complete reporting coverage. No model metrics, current red-zone scores or neighbourhood counts were invented. Annual aggregates cannot directly supervise six daily time bands.
