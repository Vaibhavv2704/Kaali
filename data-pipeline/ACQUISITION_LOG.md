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
