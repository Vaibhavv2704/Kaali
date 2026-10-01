# NCR map and optional context scenario — 2026-10-02

## Recorded data

`publish_ncr_map.py` republishes existing hash-frozen NCRB 2022/2024 workbook rows. No new crime download is claimed. The 2024 map has 15 Delhi police districts plus Gurugram, Faridabad, Gautambudh Nagar and Ghaziabad. Explicit annual TOTAL cells are used, never a sum of overlapping category headings. Blank cells and original category inconsistencies remain unchanged. The selected geographic units sum to **18,778** recorded cases: Delhi 13,230; Gurugram 1,377; Faridabad 1,341; Gautambudh Nagar 431; Ghaziabad 2,399. This calculated subtotal is not an official whole-NCR total. Noida and Greater Noida are not artificially split. Special Delhi units remain outside the geographic map subtotal.

All Delhi/Haryana/UP state sums for both years reconcile with the corresponding workbook and independently downloaded NCRB Table 3A.1. This aggregate check does not prove individual cells or continuity of police boundaries. Original workbook retrieval URL/date remain unknown; hashes and the existing report receipt are retained in counts-v1 config/manifest. Government publication reuse must be reviewed before redistribution.

## Geography

Circles use named public-place coordinates from the existing hash-checked OSM snapshot, not incident coordinates, district boundaries, centroids or danger radii. New references are Millennium City Centre Gurugram (`node/7018316590`), Police chowki NIT 3 (`node/1575177481`), Noida Sector 18 (`node/6537285486`) and Police Station Sahibabad (`node/3245675051`). Government locality context links are saved with each record. A chowki reference is not asserted to be identical to a full police station in the directory. Delhi points are checked against the existing NCT outline; other cities do not have verified police polygons.

## Optional assumed scenario

Recorded-case colours remain the default. The optional scenario is a judgement illustration, separate from the trained counts-only research model and its reported evaluation. It has no measured time-band labels or validated safety probabilities.

For each selected district reference:

1. Rank annual recorded counts across all 19 units, using average ranks for ties divided by 19.
2. Multiply by the assumed four-hour factor: 00–04 **1.2**, 04–08 **0.9**, 08–12 **0.9**, 12–16 **1.0**, 16–20 **1.1**, 20–24 **1.35**. These choices illustrate a user's night-awareness hypothesis; no evidence establishes these multipliers. No weekday/weekend difference is claimed.
3. Count mapped bus/metro points within 1 km of the approximate reference. Multiply by `1 - min(mappedTransit, 20) / 100`. The assumed 0.8–1 adjustment illustrates activity, not actual footfall, open hours or causal protection. A district reference's surroundings are not representative of its entire district.
4. Scale to 100, cap at 100, round. Missing counts, fewer than two available comparison counts, invalid bands or no mapped transit input produce **unknown**, not low risk. All outputs have low confidence and `assumed-scenario` data type.

Rules are reproducible in `src/lib/context-scenario.ts`. Hiding help layers does not change the full snapshot used for this calculation; search does not change the comparison population. Changing a time factor can change colour/index but never a recorded case total. Clipping can create ties. This index is not a calibrated or within-band percentile prediction. No evaluation metrics from the counts-only model apply to it.

## Emergency places, layouts and gaps

Default help layers reuse the existing partial OSM snapshot: 167 police, 931 hospitals, 284 metro and 2,351 bus points. Counts describe mapped features, not complete operational directories. Fire-station records are absent rather than fabricated. A bounded Overpass refresh was stopped by robots policy before querying; receipt: `sources/ncr-emergency-2026-10-02.json`. No alternative endpoint or policy bypass was attempted. Availability/hours remain unconfirmed. OSM: ODbL, © OpenStreetMap contributors.

Detailed MapTiler light/dark streets, muted vector styles and satellite-with-labels are offered. All three detailed/hybrid styles responded HTTP 200 using the configured key on 2026-10-02. Place/street/shop labels depend on zoom and provider coverage. © MapTiler; account/domain restrictions and current plan terms still apply.

Neighbourhood counts and model outputs remain unavailable: no matching police-boundary-to-ward/sector/H3 crosswalk has been verified. Administrative boundaries must not substitute for police units. The existing tested downscaler can conserve district totals once that mapping and context weights are supplied; no invented neighbourhood allocation is exported now. Real occurrence-time observations, historical busyness/context and additional earlier totals are the next model inputs. Lower reporting can reflect under-reporting; counts also track reporting practices and area size. Neither circles nor assumed indices establish current individual safety.

Convicted-person cards and records have been removed from the product at the user's request. The former About/methodology routes redirect to the crime-data page; source and limitation notes remain with the data.
