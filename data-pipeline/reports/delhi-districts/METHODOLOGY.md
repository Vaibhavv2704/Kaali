# Delhi police-district crimes against women: 2024 research extract

Retrieved **1 October 2026**. Reporting period: **calendar year 2024**. This is the newest usable Delhi district year found in the downloaded resources. NCRB's latest report identified in this search was *Crime in India 2024*. A newer Delhi Police city-wide 2025 total exists, but it does not supply district category records and is not substituted here.

## Files and provenance

- `delhi-police-district-women-2024.csv` and `.json`: 23 reporting-unit records, all 49 source category columns and nine explicitly calculated subtotals. Fifteen units are geographic police districts; eight are special units.
- `delhi-police-district-women-2022.csv` and `.json`: verification supplement for the user's original candidate. All 42 original category cells per Delhi unit are preserved; no unverified 2022 combined total is asserted.
- Reproduction: `data-pipeline/extract_delhi_districts.py`. Source receipt: `data-pipeline/sources/delhi-district-2024-receipt.json`. Each input must match its recorded SHA-256 and size before extraction. Raw downloads remain under `data-pipeline/raw/`, excluded from Git.

The original candidate is [India Data Portal resource c8d3ea7e](https://ckandev.indiadataportal.com/dataset/crime-statistics/resource/c8d3ea7e-4855-45f3-9c26-557419e93b6a). Its **actual CSV** has 5,322 rows for 2017–2022, including 23 Delhi registration circles in 2022. It does not contain 2024 observations. Its catalog's dates do not consistently describe the rows, so row years determine coverage.

The same catalog links [resource d8bda878](https://ckandev.indiadataportal.com/dataset/crime-statistics/resource/d8bda878-37a7-4320-8413-36d741bd9b27). Its actual CSV has 964 rows, all for 2024, including 23 Delhi registration circles. Both resources attribute extraction to NCRB. This verifies declared provenance, **not** a complete audit of each secondary-source district cell against an original NCRB district workbook.

The validation source is the actual 602-page *NCRB Crime in India 2024, Volume I* PDF, obtained from an [OpenCity resource](https://data.opencity.in/dataset/crime-in-india-2024/resource/46f760f4-dcf4-4f95-85c9-2225e2f7bbe8). Publisher and title are visible in the downloaded report. Table 3A.1 is printed page 281 / PDF page 327. Table 3A.2 is printed pages 282–309 / PDF pages 328–355. Numbers are extracted from those files, **not search snippets**. The total, stalking and POCSO pages were also rendered and visually checked.

NCRB and data.gov.in were investigated first. Their live automated-access checks prevented direct file acquisition in this environment. The public India Data Portal Download buttons worked in the browser without login or bypass. Automated requests to that mirror returned access errors; those failures are not treated as a licence prohibition. The OpenCity PDF download passed a live robots check with its ten-second crawl delay. No permission document, account or API key was required.

### Exact downloads and SHA-256

1. Candidate, saved at `data-pipeline/raw/india-data-portal/districtwise-crime-against-women-2017-onwards.csv` (788,976 bytes):
   [Download CSV](https://ckandev.indiadataportal.com/dataset/e311a510-ce48-4f4c-baf6-0ec5f9278285/resource/c8d3ea7e-4855-45f3-9c26-557419e93b6a/download/districtwise-crime-against-women-2017-onwards.csv)
   SHA-256: `cc18f80b56b4555c15f96d17f0aef3ab1acaecbd87b7533de4a56683107c66cc`.
2. Newer mirror, saved at `data-pipeline/raw/india-data-portal/districtwise-crime-against-women-2024-onwards.csv` (154,697 bytes):
   [Download CSV](https://ckandev.indiadataportal.com/dataset/e311a510-ce48-4f4c-baf6-0ec5f9278285/resource/d8bda878-37a7-4320-8413-36d741bd9b27/download/districtwise-crime-against-women-2024-onwards.csv)
   SHA-256: `9e2743fe8a40c08bb36dfa805834d785b5124a271f60b2d0a572e87677bb324f`.
3. Original report, saved at `data-pipeline/raw/ncrb/vol1-crimeinindia2024.pdf` (17,795,140 bytes):
   [Download NCRB PDF from OpenCity](https://data.opencity.in/dataset/7d883875-921a-4820-b298-713c6219bd90/resource/46f760f4-dcf4-4f95-85c9-2225e2f7bbe8/download/vol1-crimeinindia2024.pdf)
   SHA-256: `75b827bdcfcd5e641984d7fb549aaa2f3cdf030caace2d93853e450ee236bb4c`.

All were retrieved on 2026-10-01 UTC. The receipt distinguishes browser file-creation timestamps from HTTP retrieval timestamps. India Data Portal declares **No License Provided**; do not infer the Government Open Data Licence from its attribution to NCRB. OpenCity declares **Other (Public Domain)** for its report resource. These are attributed research outputs, not a new public-app feed; the mirror's redistribution licence remains unconfirmed.

## Filtering and reporting units

Select `state_name = Delhi` and `year = 2024`. Use **`registration_circles` as the reporting unit**. Keep `district_name` and `district_code` verbatim in `source_administrative_district_*` fields; they are not a verified police-boundary crosswalk.

For example, Rohini is grouped under North West in the administrative field. Dwarka is grouped under **Shahdara in the 2024 mirror**, whereas the 2022 candidate groups it under South West. This inconsistency is preserved and flagged here; Dwarka's police registration-circle row is never merged into Shahdara. Outer North likewise carries New Delhi in the administrative field. No location or boundary correction is guessed.

Geographic units: Central, East, New Delhi, North, North-East, North-West, Outer, Outer North, Rohini, Dwarka, Shahdara, South, South-East, South-West and West.

Special units remain separate: Eow, Igi Airport, Railway, Spuwac, Vigilance, Crime Branch, Metro and Spl Cell. `Economic Offences Wing` in the 2022 file is recognized as the Eow classification alias, while its original spelling is retained. Unknown or duplicated circles stop extraction; the script expects 15 geographic units and eight special units. Special-unit counts are included only in the explicitly labelled combined reconciliation, never attached to a geographic district.

## Categories, missing values and calculations

Counts are nonnegative integers. Integral source values such as `15.0` become 15; blanks become JSON `null` and empty CSV cells. `missing_fields` names every absent cell. A formula requiring any missing component returns `null`, not a partial sum masquerading as complete. All 2024 Delhi category cells are populated; **all 23 Delhi 2022 ransom cells are blank**. These remain missing.

The 2024 PDF distinguishes cases (`I`, or IPC+BNS **Total**) from victims (`V`), rates (`R`) and parent totals. The extractor selects case counts only. Its `PDF_COLUMNS` dictionary specifies the original PDF page and Delhi-row cell offset for every category; JSON `categoryComparisons` retains the independent state/UT checks.

- Rape subtotal: adult + girl rape fields. Attempted rape and murder with rape remain separate heads.
- Assault under section 74 BNS / 354 IPC is separate from sexual harassment, disrobing, voyeurism and stalking. The broad `calculated_assault_related_subtotal` adds these five adult/girl head pairs; it is our grouping, not an NCRB district total.
- `kidnapping_abduction_women` is the **section 137/138 BNS / 363 IPC component**, not the kidnapping parent total. Its subtotal adds that component, murder-purpose kidnapping, ransom, foreign importation and `women_others` (the other-kidnapping component). The separate compelled-marriage head is reported separately, matching the 2024 table hierarchy.
- `protection_children_sexual_violence_pocso` is the **sections 4 & 6 component**, not total POCSO. `pocso_10` is source shorthand for **sections 8 & 10**. Add those and sections 12, 14 & 15, and 17–22 once. This table covers **girl-child victims only**, not all POCSO cases.
- Dowry deaths and cruelty by husband/relatives are preserved directly, alongside dowry-prohibition cases and other published legal heads.
- `calculated_recorded_heads_subtotal` sums the 49 raw mutually exclusive recorded heads once. It **does not add any of our calculated subtotals** to those fields. It is not labelled an official district total because the secondary-source series has an unresolved aggregate discrepancy.

NCRB's Principal Offence Rule records a case under the primary/most serious offence. These figures are not all allegations, all affected people or all events. The 2024 IPC/BNS transition and changed schema prevent automatic comparability with the 2022 headings. No missing field absent from a year's schema is invented.

## Reconciliation

| 2024 reporting scope | Case count |
| --- | ---: |
| Mirror, 15 geographic police districts, calculated heads subtotal | 13,131 |
| Mirror, eight special units, calculated heads subtotal | 164 |
| Mirror, both groups combined | **13,295** |
| NCRB Table 3A.1, Delhi UT | **13,396** |
| NCRB minus mirror | **101** |

The script independently extracts and sums the 49 NCRB leaf cells: they equal 13,396 and match Table 3A.1 and Table 3A.2's grand total. Across all 23 mirror units, **48 category sums match** the corresponding NCRB Delhi UT cells. Only adult stalking differs: **77 in the CSV versus 178 in NCRB**, with girl stalking zero in both. That numerical difference accounts for the whole 101-case gap. Its cause and district distribution are unknown. This is not evidence that a particular district should receive additional cases; no adjustment is made.

This check uses the full Delhi registration-circle series against the Delhi **UT** table, not the metropolitan-city table (which has a different reporting scope). Even perfect aggregate agreement would not prove each district cell correct, unchanged police boundaries, absence of revisions, or complete reporting. Here it establishes a specific secondary-source inconsistency that must accompany use of these subtotals.

For additional context only, the separately downloaded [Rajya Sabha answer 4220, 1 April 2026](https://sansad.in/getFile/annex/270/AU4220_M31fhO.pdf?source=pqars) reports Delhi Police's 2024 city-wide total as **13,195**. That is 100 below this mirror subtotal and 201 below NCRB's UT total. Its category/geography/revision equivalence has not been established; it is not used to overwrite or force-match either series. The existing importer and acquisition audit retain that document's original checksum.

## Worked Rohini example

The 2024 Rohini registration-circle row has the following nonzero heads; all other supplied heads are observed zero:

| Head or explicitly calculated group | Calculation | Cases |
| --- | --- | ---: |
| Rape | 63 adult + 0 girl | 63 |
| Deceitful sexual intercourse | direct cell | 1 |
| Assault-related grouping | 54 assault + 17 harassment + 18 disrobing + 1 voyeurism + 2 stalking; girl counterparts zero | 92 |
| Insult to modesty | 14 adult + 0 girl | 14 |
| Dowry deaths | direct cell | 10 |
| Cruelty by husband/relatives | direct cell | 332 |
| Miscarriage | direct cell | 1 |
| Abetment of suicide | direct cell | 4 |
| Attempted acid attack | direct cell | 2 |
| Kidnapping/abduction grouping | 257 basic + 0 murder + 0 ransom + 0 importation + 2 other | 259 |
| Sexually explicit cyber material | direct cell | 3 |
| POCSO girl-child grouping | 75 sections 4/6 + 22 sections 8/10 + 1 section 12 + 0 sections 14/15 + 0 sections 17–22 | 98 |
| **Calculated recorded-head subtotal** | **63 + 1 + 92 + 14 + 10 + 332 + 1 + 4 + 2 + 259 + 3 + 98** | **879** |

The 92 assault grouping and 98 POCSO grouping substitute for their component cells in this worked explanation; they are not added again. **879 is the mirror-derived subtotal, not a confirmed official Rohini total.** In particular, the unresolved Delhi stalking discrepancy may affect district subtotals, but its allocation is unknown. No correction is inferred.

## Reproduce and limitations

From the repository root, put the three unchanged downloads at the exact raw paths above, install `data-pipeline/requirements.txt`, then run:

```powershell
.venv/Scripts/python.exe data-pipeline/extract_delhi_districts.py
.venv/Scripts/python.exe -m unittest discover -s data-pipeline/tests -p test_delhi_districts.py
```

Use `--output <directory>` to choose another output folder. A changed hash, changed category schema, invalid count, duplicate/unknown unit or failed official PDF hierarchy check stops extraction. Output is deterministic and local; no web scraping, victim information or imputation occurs during extraction.

These are historical recorded volumes, affected by reporting, registration practice, legal definitions and coverage. They do not establish current danger, a neighbourhood rate, individual safety, or a predictive target at neighbourhood/time-band resolution. No offender, photo or incident location is derived from aggregate tables.

**No map data has been prepared from this extract.** Neither the LGD administrative names nor existing Delhi municipal wards establish matching police-district boundaries. If a later map uses approximate district reference points, it must label them as approximate and label red symbols as historical recorded case volume—not validated safety scores or danger radii. The current extract contains no coordinates or fabricated polygons.
