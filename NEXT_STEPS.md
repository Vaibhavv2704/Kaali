# Kaali: what happens next

## Work I can continue in this workspace

- Collect permitted public reports; review locality/date/time associations and deduplicate events.
- Keep source references and aggregate crime context visible with their limitations. Convicted-person profiles have been removed at your request.
- Finish region geometry, population crosswalks, Hindi copy and responsive map checks.
- Maintain the fitted annual-volume model and its disjoint-area/city evaluation. Obtain another complete historical cohort before claiming temporal validation. Replace assumed neighbourhood mapping/time rules with measured evidence when available.

## Current completed milestones

- The home screen is the 2024 historical Delhi NCR map: 15 Delhi police districts plus Gurugram, Faridabad, Gautambudh Nagar and Ghaziabad. Its 18,778 recorded-case subtotal is calculated for these selected units. Symbols are approximate references, not district boundaries or danger radii. Detailed streets, satellite with labels and other catalogue layouts remain available. Police stations/hospitals default on; metro is optional in Help nearby. Convicted-person details and Our approach navigation are removed.
- Latest ML volume model fits 109 real 2022→2024 reporting-unit examples across Delhi/Haryana/UP. Poisson pooled held-out MAE is 160.99 cases versus persistence 165.55, but combined NCR city transfer is worse than persistence. Its 2026 estimates remain experimental. The earlier counts-v1 persistence report covers a different cohort and remains preserved. See `data-pipeline/reports/ml-volume-v1/MODEL_CARD.md` for the latest comparison, fold identities, limitations and reproducible exports.
- Supplied traffic/population/locality files are imported without altering originals. Corrected swapped coordinate headings, retained missing values and kept historical August 2024 probes separate from live traffic. Transparent reference-cell levels use model-volume interpolation plus explicit assumed time/activity rules. Missing model inputs use the requested time-only advisory, without filling crime/model nulls. These cells are not verified ward boundaries.
- Detailed automatic advice uses on-device wording, with no explanation disclosure or local AI generation button. No AI request is made by the current location card. Already-granted browser permission resumes GPS and zoom automatically; the single location control is beside +/−. Stop/unmount clears GPS. Header renders Kaali directly as text.
- Source-backed totals are available, but the original local workbooks' download receipts, matching police boundaries and complete historical place context remain missing. Additional API keys do not fill those evidence gaps.

## What you can do to unblock real predictions

### 1. Runtime setup: handled here

A fresh check on 2026-09-30 found ML and projection libraries loading successfully, superseding the earlier Windows-policy blocker. The missing openpyxl package has been installed in the project environment. No machine move or security-policy change is requested. The diagnostic includes a tiny in-memory synthetic fit, which produces no production model or metrics.

```sh
.venv/Scripts/python.exe data-pipeline/check_runtime.py
```

### 2. Obtain a statistical crime export, if you have access

Most useful: anonymised counts by locality or police station, reporting period, crime category and occurrence-time band. Include boundary IDs/maps, data definitions, missing/suppressed-cell flags and collection coverage. Unknown time should remain unknown. Police-station totals alone cannot establish neighbourhood-level observations.

Do not send raw FIRs, victim details, names, exact residential addresses or personal coordinates. Place statistical exports in `data-pipeline/raw/provided/` and tell me the filename and source URL. Existing public licence/source information is enough for public datasets; no separate permission document is requested. For non-public exports, include the provider's permitted-use terms.

If you do not have an export, the drafts in `data-pipeline/DATA_REQUESTS.md` can help you request one. They have not been sent or filed. You handle contacts, applicant details and any submission or fee. News evidence collection can continue meanwhile, but news absence cannot become zero-crime labels.

## Already supplied — no need to send again

- MapTiler key is configured locally.
- Central Delhi 2011 Census workbook is received and imported; its current-geography crosswalk remains unfinished.

## Completion criteria

The historical red circles are complete as recorded-volume symbols; they do not assert danger. Transparent advisory-cell shading and the fitted experimental annual-volume model are implemented. Validated neighbourhood risk estimates still require usable labels, matching geometry/context and successful spatial/city/temporal evaluation. Actual time-band predictions require occurrence-time observations; user-requested time rules remain assumptions. The count-based model uses total counts rather than population rates. Browser visual QA/screenshots remain pending under the recorded tool URL-policy block; no bypass has been attempted. Review unresolved source receipts/reuse terms before redistribution. No additional paid API, deployment or new account is required for the current work.
