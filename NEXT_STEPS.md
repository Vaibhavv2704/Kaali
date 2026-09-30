# Kaali: what happens next

## Work I can continue in this workspace

- Collect permitted public reports; review locality/date/time associations and deduplicate events.
- Keep source references, aggregate crime context and adult conviction profiles visible with their limitations.
- Finish region geometry, population crosswalks, Hindi copy and responsive map checks.
- Maintain and test training, validation and static prediction export. Train only after inputs and runtime are ready.

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

Production red zones require usable labels and exposure, reviewed boundaries, successful spatial/city/temporal evaluation and calibrated scores. Until then, sample shading stays explicitly labelled. No additional paid API, deployment or new account is required for the current work.
