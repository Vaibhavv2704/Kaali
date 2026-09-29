# Source register

Research date: **2026-09-29** (IST). Dates below mean researched/access attempted, not a claim that underlying observations are current. Public accessibility is not a reuse licence. No victim data, article bodies, or incident microdata were downloaded into the public dataset. Search previews are discovery evidence, not dataset ingestion. Sources without verified reuse terms are blocked in `config/sources.json`.

| Source / URL | Use and access outcome | Licence / terms | Retrieved or checked |
|---|---|---|---|
| [OGD / NCRB Crime in India 2022](https://www.data.gov.in/catalog/crime-india-2022) | Official catalog located; granular six-band NCR data not imported. No counts inferred from catalog snippets. | Check GODL at resource level; not assumed | 2026-09-29 |
| [Delhi Police](https://delhipolice.gov.in/index) | Official 112, 1091, 1930 confirmed; no station-level dataset imported | Government site; bulk-data reuse unverified | 2026-09-29 |
| [Haryana Police Women Safety Cell](https://www.haryanapolice.gov.in/Women%20Safety%20Cell) | 1091 procedure found; no Gurugram/Faridabad granular incident dataset imported | No bulk reuse permission verified | 2026-09-29 |
| [UP Police WCSO](https://uppolice.gov.in/article/en/about-us-mahila-samman-prakostha) | 1090 confirmed active on official page; no Noida/Ghaziabad observations imported | No bulk reuse permission verified | 2026-09-29 |
| [OpenCity Delhi wards](https://data.opencity.in/dataset/delhi-wards-information) | Boundary catalog identified; geometry/vintage/licence QA pending | Resource-specific licence must be checked | 2026-09-29 |
| [OpenCity Delhi census female population](https://data.opencity.in/dataset/delhi-census-2011-data/resource/372c35ad-ae9e-418f-a2e6-faa3351de767) | Ward population resource found; 2011 vintage not silently joined to later wards | Resource-specific terms pending | 2026-09-29 |
| [Safetipin Delhi reports](https://safetipin.com/report/delhi/) | Public audit summaries; not a crime incidence measure | Copyright; detailed data access permission required | 2026-09-29 |
| [World Bank reproducibility record](https://reproducibility.worldbank.org/catalog/565) | Explicitly describes request-only NCR Safetipin dataset | Third-party dataset access restricted | 2026-09-29 |
| [Safecity / Red Dot Foundation](https://www.safecity.in/) | Candidate crowdsourced source; no raw records collected | Permission and privacy review required | 2026-09-29 |
| [OpenStreetMap](https://www.openstreetmap.org/copyright) | 3,733 features retrieved 2026-09-29 via Overpass; city assignments remain unverified | ODbL 1.0; © OpenStreetMap contributors; derived DB obligations | 2026-09-29 |
| [ERSS](https://112.gov.in/) / [integration](https://www.112.gov.in/about) | 112 and legacy integration guidance | Official reference, factual numbers only | 2026-09-29 |
| [WCD](https://wcd.gov.in/women/help) | 181 / child-helpline navigation | Official reference, factual numbers only | 2026-09-29 |
| [Ghaziabad district helplines](https://ghaziabad.nic.in/en/helpline/) | 1098, 1091, 100, 102, 108 confirmed; coverage must not be generalized | Official reference, factual numbers only | 2026-09-29 |
| [Haryana government](https://www.haryana.gov.in/) | 1091 confirmed | Official reference, factual numbers only | 2026-09-29 |
| [Supreme Court review judgment](https://api.sci.gov.in/supremecourt/2017/35383/35383_2017_Judgement_09-Jul-2018.pdf) | Conviction research; no judgment text republished | Public judicial record; link only | 2026-09-29 |
| [Reuters syndicated report](https://www.brecorder.com/news/581827/india-executes-four-men-convicted-in-2012-delhi-gang-rape-murder-case) | Execution status corroboration; names and facts only; no victim identifiers retained | Reuters copyright; link only, no images/text copied | 2026-09-29 |

## Gaps / deferred collection


Optional Sonipat, Bahadurgarh and Meerut fringe are explicitly not covered. The UI's sample dataset is generated software test material, not an observation from any source above.

## Follow-up source audit — 2026-09-29

These are research outcomes, not imported incident records. No per-neighbourhood or time-band counts were inferred.

| Source | Scope and access evidence | Reuse / next action |
|---|---|---|
| [Delhi Police women-crime table](https://delhipolice.gov.in/Images/HTMLfiles/CAW%2810%29.pdf) | Annual 2012–2021 columns followed by partial-year 2021/2022 columns through 15 July; city-wide categories, no locality or time bands | [Copyright policy](https://delhipolice.gov.in/PrivacyPolicy) requires permission review; not imported |
| [Haryana Police RTI statistics](https://www.haryanapolice.gov.in/RTI/rtipart14) | Statewide 2025 table, not Gurugram/Faridabad city observations | Reuse permission unresolved; internal server links are not public collection endpoints |
| [UP Police 2015 district table](https://uppolice.gov.in/writereaddata/uploaded-content/Web_Page/13_7_2016_12_17_26_Table_5_1.pdf) | Historic district incidence and Census 2011 female population in lakhs; district boundaries are not current municipal boundaries | [Copyright policy](https://uppolice.gov.in/article/en/copyright-policy) distinguishes document downloads from other reuse; not imported |
| [MHA parliamentary answer, 4 August 2021](https://www.mha.gov.in/MHA1/Par2017/pdfs/par2021-pdfs/RS04082021/1803.pdf) | Metropolitan totals for 2017–2019 include Delhi City and Ghaziabad; Delhi UT totals are a different geography | [Website policy](https://www.mha.gov.in/en/page/website-policy) requires permission for reproduction; no public table copied |
| [OGD city/category resource](https://up.data.gov.in/resource/crime-head-wise-and-city-wise-indian-penal-code-ipc-crimes-and-special-and-local-laws-sll) | Resource discovered; direct retrieval timed out; no machine-readable payload obtained | GODL applicability must be confirmed on the actual resource; a catalog title is not an import |
| [OpenCity robots policy](https://data.opencity.in/robots.txt) | Retrieved successfully; disallows `/api/`, requires 10-second crawl delay. Dataset page access failed; metadata API attempt returned 404 | Do not retry the API. Resource-level licence and geometry vintage remain unresolved |
| [NCW annual report 2023–24](https://cdn.ncw.gov.in/wp-content/uploads/2025/03/NCWAnnualReport20232024Eng.pdf) | Complaint statistics are not police-recorded incidence; no case narratives collected | Separate complaint context only after reuse/privacy review; never add to police counts |
| [Safetipin Delhi](https://safetipin.com/report/delhi/) | Public report index accessible; granular audit observations not obtained | Permission required for detailed data; audits are environmental evidence, not crime labels |
| [Safecity](https://www.safecity.in/) | Access attempt unsuccessful; no raw records obtained | Permission, privacy and deduplication review still required |

### City-specific availability

- **Delhi:** official aggregate source found, but no reusable neighbourhood/time-band labels or aligned exposure imported.
- **Gurugram and Faridabad:** Haryana statewide totals cannot be attributed to either city. City/station observations and boundary pairs remain missing.
- **Noida and Greater Noida:** Gautam Buddh Nagar district statistics cannot be split between these municipalities without matching geography and exposure.
- **Ghaziabad:** metropolitan and historic district statistics use different units; neither supports neighbourhood timing estimates.
- **All six cities:** OSM environmental features are available, but municipal assignment awaits reviewed boundaries. Production risk coverage remains zero, indicating missing evidence rather than low risk.

No news article bodies, victim details or private complaint records were retained. Reputable news remains a candidate for manually reviewed URL/headline evidence; it cannot substitute for an incident census. Commission and NGO access requests have not been sent.
