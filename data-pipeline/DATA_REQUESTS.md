# Data-access drafts for Kaali

Prepared 2026-09-30. These drafts have **not been sent or filed**. Fill applicant/contact details privately, confirm the current public authority and official filing route, and review any fee before submission. Do not put identities or credentials in the repository.

## Police reporting data

Prepare separate requests for Delhi Police, Gurugram Police, Faridabad Police, Gautam Buddh Nagar Commissionerate (Noida and Greater Noida), and Ghaziabad Commissionerate. A state-wide request is not a substitute for the relevant reporting unit.

### Draft text

Subject: Existing anonymised statistical records on crimes against women, 2021–2025

Please provide existing electronic statistical records for your jurisdiction for calendar years 2021–2025, preferably CSV/XLSX, containing counts of registered cases under crimes against women by police station, month, offence category and occurrence-time band where already held. Requested time bands are 00–04, 04–08, 08–12, 12–16, 16–20 and 20–24; if these bands are not held, please provide the existing time grouping and its definitions. Please distinguish occurrence time from registration time and identify unknown-time records separately.

Please provide existing records documenting:

1. Definitions and IPC/BNS category mappings, effective dates and whether counts represent cases, offences, complaints or persons.
2. Police station identifiers, jurisdiction maps or boundary files, changes of boundaries and effective dates.
3. The reporting-period coverage, partial periods, missing/suppressed cells, revisions and recording-system changes.
4. Any population denominators used in published rates, their sex/age scope, year, source and geographic unit.
5. Published terms or instructions governing attribution, reuse and redistribution of these statistical records.

No FIR text, names, case narratives, victim/family information, exact incident addresses, phone numbers, identifiers or individual coordinates are requested. Please retain applicable suppression and privacy protections. If a requested breakdown is not maintained, please identify the available existing aggregate instead; creation of a new analysis is not requested. If records are publicly available, please provide the exact download location.

### Filing routes to verify

- The [central RTI portal](https://www.rtionline.gov.in/) explicitly excludes state-government authorities, including GNCT Delhi. Do not use it for Haryana/UP departments or assume that a Delhi-based authority is a GNCT department. Check the actual authority in the [available-authority directory](https://rtionline.gov.in/request/allpa.php).
- For Haryana and UP police, identify the official state route and relevant PIO before filing.
- Portal instructions, eligibility, applicant identity, fee and any CAPTCHA must be handled at submission time. No application or payment has been made by this project.

## Safecity / Red Dot Foundation request draft

We are building Kaali, an awareness tool for Delhi NCR. Could you provide a licensed, privacy-preserving aggregate export for Delhi, Gurugram, Faridabad, Noida, Greater Noida and Ghaziabad? We seek locality or coarse-cell counts by month, harassment category and broad time band, including unknown values and suppression rules. We do not seek narratives, names, exact points or identifying details.

Please describe collection coverage, deduplication, moderation, reporting bias, permitted uses (including model training and public aggregate display), attribution, licence duration, redistribution limits and any fees. We will keep crowdsourced observations separate from police-recorded counts and will not describe low reporting as safety.

## Safetipin request draft

Could you provide NCR safety-audit observations or privacy-preserving aggregates, with a reuse licence covering feature engineering and public derived estimates? Requested environmental fields are audit date, locality/coarse geography, lighting, visibility, crowd/public presence, transport access and audit methodology/version. We do not seek user identities or exact personal travel traces.

Please specify spatial/temporal coverage, sampling design, repeat-audit handling, redistribution and attribution requirements. Audit scores will be treated as environmental evidence, not crime incidence labels.

## Why these records matter

Annual metropolitan totals now displayed in Kaali cannot identify incident timing or neighbourhood differences. News discovery and population rasters cannot recover those missing labels. Any resulting model must be evaluated on independently observed, geographically and temporally held-out data before its scores become production red zones.
