# Source register

Research began **2026-09-29** (IST); dated updates below extend this log. Dates mean researched/access attempted, not a claim that underlying observations are current. Public accessibility is not a reuse licence. No victim data, article bodies, or incident microdata were downloaded into the public dataset. Search previews are discovery evidence, not dataset ingestion. Sources without verified reuse terms are blocked in `config/sources.json`.

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

## Imported historical context and news — 2026-09-30

- **OpenCity / NCRB Crime in India 2022:** [resource and licence](https://data.opencity.in/dataset/crime-in-india-2022/resource/a4496020-4d71-4533-9041-d18e3bedb911), [CSV download](https://data.opencity.in/dataset/crime-in-india-2022/resource/a4496020-4d71-4533-9041-d18e3bedb911/download/2176f9d3-19ea-4280-9b82-e643cfb5255d.csv). Resource metadata explicitly declares Other (Public Domain); credit OpenCity, original source NCRB. The permitted download returned HTTP 200 after respecting robots and its ten-second delay; dataset HTML still returns 403. No API used. SHA256: `93a7596163c46f6acf303905f6b9cbb251d7e2f7eb6a0d228db67d82f72cb162`. Imported six rows (Delhi City and Ghaziabad, 2020–2022) into `crime-context.json`, separate from neighbourhood records. The CSV’s population heading does not explicitly identify female exposure, so rates remain withheld. The importer refuses changed bytes pending review.
- **DataMeet Delhi ward candidate:** [publisher provenance and CC BY-SA 2.5 India licence](https://github.com/datameet/Municipal_Spatial_Data/tree/master/Delhi), [geometry](https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/refs/heads/master/Delhi/Delhi_Wards.geojson). Downloaded privately and checked: 290 features/unique IDs, no empty or invalid polygons. Current vintage is unresolved; not approved for production location classification. See public `reports/delhi-boundary-candidate.json`. No geometry redistributed or marked current.
- **News references:** `news.json` contains three manually reviewed URL references with neutral editorial headlines, publisher/date metadata and no bodies, photos or personal narratives. Copyright remains with publishers; these are reading links, not a republished news dataset. No bulk crawler or training use enabled. [Gurugram, Times of India, 23 January 2025](https://timesofindia.indiatimes.com/city/gurgaon/gurgaon-records-rise-in-reports-on-crime-against-women-but-it-has-no-shelter/articleshow/117466959.cms); [Ghaziabad, Hindustan Times, 25 November 2025](https://www.hindustantimes.com/cities/noida-news/ghaziabad-27-decline-in-crime-against-women-heinous-crimes-reduced-by-17-since-2024-101764097834838.html); [Delhi, Hindustan Times, 23 January 2026](https://www.hindustantimes.com/cities/delhi-news/crimes-in-delhi-went-down-in-2025-delhi-police-101769106398499.html). These aggregate reports are not incident records; no counts extracted or added to official totals. A Faridabad TOI page failed to open and was not added.
- **Safecity research corpus:** [authors’ repository](https://github.com/swkarlekar/safecity) explicitly requires contacting Safecity for permission and limits use to research. No narratives downloaded. User reports having access, but the specific dataset/path and permission evidence have not yet been supplied.

The earlier audit remains a dated record; this successful CSV import supersedes the earlier statement that no aggregate counts had been imported. It does not change neighbourhood coverage or model readiness.

## Additional source families — checked 2026-09-30

| Source | Intended role | Evidence and remaining gate |
|---|---|---|
| [GDELT DOC API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) and [time-range update](https://blog.gdeltproject.org/doc-geo-2-0-api-updates-full-year-searching-and-more/) | Discover article references | Publisher article rights remain separate. Mentioned locations and GDELT event codes are not verified local crime labels. One bounded 25-result, one-month API request failed with HTTPError; no response records retained. Audit: `/data/reports/gdelt-discovery.json`. |
| [Jagori baseline survey](https://www.jagori.org/sites/jagori/files/ResearchReportpdf/Safe%20Cities%20Free%20of%20Violence%20Against%20Women%20and%20Girls%20Initiative.pdf) / [Safer Cities](https://www.jagori.org/safer-cities-initiative) | Historical audit methodology and reporting-bias context | Delhi baseline is from 2010. No current incident labels or granular audit licence established; no narratives imported. |
| [WorldPop India age/sex 2020](https://hub.worldpop.org/geodata/summary?id=81562) | Candidate female-population exposure | DOI 10.5258/SOTON/WP00841, R2025A v1; estimated 100m grid counts, not census observations. Full collection is 41.2GB. No full download; choose female age bands, verify licence and align year/boundaries before a clipped extract. Do not use only childbearing-age women as an all-female denominator. |
| [Central RTI portal](https://www.rtionline.gov.in/) / [guidelines](https://rtionline.gov.in/guidelines.php?appeal=&pageid=cfcd208495d565ef66e7dff9f98764da) | Request existing aggregate records | State authorities require the appropriate state route. Drafts in DATA_REQUESTS.md; applicant details, authority and fees unresolved. Nothing filed or sent. |

Census ward/town tables, NFHS-5, GHSL, Delhi Economic Survey, Open Transit Data, municipal streetlights, Survey of India/Bhuvan, Breakthrough, UN Women and academic papers remain queued for resource-level review. They have not been claimed as downloaded or licensed. NFHS prevalence and NCW complaints must remain separate from police incidence. Google News, social-media feeds and Kaggle mirrors are discovery candidates only; no automated scraping enabled or licence assumed.


## News extraction resumed - 2026-09-30

The user's latest instruction explicitly includes public news text for factual extraction, superseding the preceding news-text exclusion. No article bodies are retained. No extra permission document is requested for public factual research.

- Source: The Tribune, Rahul Gahlawat, Delhi police annual figures for 2023-2025; published 2026-01-22.
- URL: https://www.tribuneindia.com/news/delhi/delhi-saw-dip-in-crime-snatching-extortion-least-solved-cases/
- Robots: https://www.tribuneindia.com/robots.txt returned 200 and allows all paths. Live requests respected a two-second minimum delay.
- Licence: publisher copyright; no open-text licence or article-republication right claimed. Only reviewed factual fields and an editorial headline are retained, with attribution/link. No restriction was found on the accessed article/footer; a guessed terms-and-conditions route was unavailable. This review covers one article, not bulk crawling.
- Retrieval: 2026-09-30; exact UTC timestamp and decoded-HTML SHA256 are in public/data/news.json and ignored raw/news/4da9308a5bd296b3.facts.json.
- Extracted nine category/year counts. These are news-reported Delhi city aggregates, not directly imported police records. Categories retain publisher wording. No geographic/time allocation, denominator, rate, risk score or model label was inferred.
- HTML adaptation: the article lives inside #story-detail and a form wrapper that the generic extractor omitted. A reviewed selector reads that container only; missing containers/tokens fail closed. Bodies are processed in memory and discarded.
- Access audit: the initial sandbox socket attempt failed; authorized network execution succeeded. Automatic review first cited the superseded news exclusion, then allowed the request after the latest user authorization was made explicit.


## Delhi Phase 1 reproducibility audit - 2026-09-30

- Existing OpenCity, DataMeet and OSM files copied into ignored raw/ with SHA256 manifests; no re-download or new crime observations. Run phase1.py to recreate the public Delhi input audit.
- DataMeet issue https://github.com/datameet/Municipal_Spatial_Data/issues/57 explicitly flags Delhi ward geometry outdated (opened 2023-08-05). The 290 valid polygons remain historical candidates, not current jurisdiction boundaries.
- Census source https://censusindia.gov.in/nada/index.php/catalog/6286/study-description identifies PC11_PCA-TV-0706, DDW_PCA0706_2011_MDDS with UI.xlsx, ORGI Census 2011, Central Delhi. No workbook retrieved. Python robots/catalog requests failed SSLError; web catalog 913 returned 502. No TLS bypass, guessed download token, population values or denominator imported. Publication: government census; workbook-specific terms and metadata await retrieval. Exact manual path is in RAW_INPUTS.md.
- OSM snapshot selection bias: help query includes only lit=yes major roads. A lighting fraction from these roads would be invalid; environmental preprocessing now requires a complete road inventory with known yes/no tags, otherwise null. Help amenity density is not a total POI or footfall measurement.
- Two additional public Tribune incident candidates were discovered through search, but web article fetches failed (cache miss / unexpected status). No incident fact, body or person entity was imported. Discovery URLs: https://www.tribuneindia.com/news/delhi-police-files-case-after-woman-alleges-threats-by-roommates-male-guests-in-dwarka/ and https://www.tribuneindia.com/news/delhi/british-woman-raped-by-social-media-friend-in-delhi-hotel-2-arrested/ . Publisher copyright; no further reuse/access decision based on snippets alone.


## Census workbook receipt - 2026-09-30

The previously requested DDW_PCA0706_2011_MDDS with UI.xlsx is now present at raw/census/. Acquisition: user-supplied local file, original download date unknown. The official catalog https://censusindia.gov.in/nada/index.php/catalog/6286/study-description names the matching PC11_PCA-TV-0706 workbook; remote bytes were not independently verified. Publisher: ORGI, Census of India 2011. Public government population table, attribution retained; no additional open licence claimed.

Imported 21 ward-part rows using the complete geographic key, excluding parent summary rows and unrelated demographic columns. Female/male/total population reconciles for each row, each parent town and the Central district total. Output includes source URL, checksum, receipt/review date and historical limitations. No current boundary match, projection or crime-rate denominator was inferred. Source workbook preserved unchanged.

## Delhi administrative boundary — 2026-09-30

- Source: OpenStreetMap relation 1942586, https://www.openstreetmap.org/relation/1942586 ; retrieved 2026-09-30 via https://overpass-api.de/api/interpreter with bounded query `[out:json][timeout:50][maxsize:33554432];relation(1942586);out body geom;`.
- Licence: Open Database Licence (ODbL) 1.0, https://www.openstreetmap.org/copyright . Attribution: © OpenStreetMap contributors.
- Raw file: `data-pipeline/raw/osm/delhi-boundary-1942586.json`; SHA-256 `1d6df2cf5cd50e0b61e6cf61964bb003de42a4d34450dd929c8c914f47a96e0d`. The raw Overpass timestamp is preserved in the public GeoJSON.
- Reviewed ISO3166-2 IN-DL / admin_level 4 identity, all 119 outer ways and closed-ring topology. One valid polygon, no dangling edges or invalid rings. Delhi centre falls inside; configured centres of the other five NCR cities fall outside.
- Community mapping, not a legal survey or verified neighbourhood geography. Used for city detection and help assignment only. Whole features must lie strictly inside; boundary-touching/crossing features remain unassigned. 2,916 of 3,733 help features assigned Delhi; 817 remain unassigned. No population tags, crime labels or model scores inferred.
- OpenCity boundary catalog remained inaccessible (HTTP 403); historical DataMeet wards remain unverified for current use. No access restriction bypassed.

## Delhi incident report import — 2026-09-30

Source: The Tribune / PTI, https://www.tribuneindia.com/news/delhi/delhi-2-northeastern-women-assaulted-molested-outside-nehru-place-hotel/ (published 2026-05-11). Retrieved 2026-09-30T15:06:21.988241+00:00; decoded HTML SHA-256 `6b2bca19385382b9b701ef42e47e4fcf4f2fd8270c42b531e9c4cc244e72ce9b`. Publisher copyright; linked factual extraction only, no open-text licence claimed. Existing single-article access review applied; live robots and canonical article requests returned HTTP 200. Body processed in memory and discarded.

One reviewed reported event in Nehru Place on May 10, with 2026 inferred from publication context; reported 06:30 maps to band 04:00–08:00. Source label molestation retained, no legal code mapping asserted. Retained no victim/accused names, age, ethnicity, venue address, imagery or narrative. Police-station location is not used as incident locality. No exact coordinates, polygon assignment, coverage denominator or training eligibility. Reports from other outlets about the same event must not become extra events.

Excluded NDTV from automated collection after its linked terms page explicitly prohibited scraping/data mining: https://www.ndtv.com/convergence/ndtv/new/TermsAndConditions.aspx (reviewed 2026-09-30). Robots allowing a path does not override terms. Also rejected a Tribune August 2025 party-report locality candidate because the article supplied a residence rather than incident locality. No values from either candidate added to model inputs.

## Official-file acquisition — 2026-10-01

Visit order: NCRB, data.gov.in, Delhi Police, Haryana/UP Police, Parliament/Assembly, boundaries/population, transit. See reports/ACQUISITION-2026-10-01.md and reports/acquisition-2026-10-01.json for original-file checksums, exact retrieval timestamps and geographic limitations.

| Source URL | Result | Licence / terms |
| --- | --- | --- |
| https://www.ncrb.gov.in/crime-in-india.html and https://www.ncrb.gov.in/crime-in-india-all-previous-publications.html | Latest report identified as 2024; English/Hindi navigation inspected. Runtime robots disallows all automated paths; no report files downloaded | Government publications; no resource licence asserted without file review |
| https://www.data.gov.in/catalog/district-wise-crimes-committed-against-women | Catalog identifies annual police-district resources; live robots disallows automated paths; no CSV downloaded | Catalog shows Government Open Data Licence–India; police districts must not be equated with revenue districts |
| https://delhipolice.gov.in/statistics | Three original PDFs downloaded: https://delhipolice.gov.in/Images/HTMLfiles/CAW(10).pdf ; https://delhipolice.gov.in/Images/HTMLfiles/Crime%20In%20Delhi(2).pdf ; https://delhipolice.gov.in/Images/HTMLfiles/CRIME_RATE_2001_2010%20(1).pdf | Government statistical publications; no separate open licence asserted. Private research staging, source attribution retained. Robots returned 404 |
| https://haryanapolice.gov.in/PDF/Annual_Admin_Report_2022.pdf | 111-page report downloaded, scanned table review pending | Government publication; no separate open licence asserted; private staging. Robots returned 404 on successful retry |
| https://haryanapolice.gov.in/RTI/rtipart14 | Search identified current state crime chart; no values imported | Government page; resource terms not yet reviewed |
| https://uppolice.gov.in/writereaddata/uploaded-content/Web_Page/21_11_2013_12_23_50_Crime%20in%20UP-2012.pdf | Original report downloaded. Table 8 page 25 provides historical NCR police-district figures; six selected category rows normalized | UP Police SCRB government publication; no separate open licence asserted; private research staging. Robots returned 404 |
| https://sansad.in/getFile/annex/270/AU4220_M31fhO.pdf?source=pqars | Downloaded answer dated 1 April 2026: Delhi Police annual 2023–2025 totals, no district detail | Parliamentary government answer; no separate open licence asserted; private research staging. Robots returned 404 |
| https://sansad.in/getFile/loksabhaquestions/annex/174/AU1021.pdf?source=pqals | Web reviewed; refers Rajasthan district question back to NCRB; excluded from NCR data | Government answer; not downloaded or imported |
| https://delhiassembly.delhi.gov.in/sites/default/files/dlas/universal/29_june_2015.pdf | Search found staffing proposals, not requested district crime counts; excluded | Government proceedings; no dataset imported |
| https://github.com/datameet/Municipal_Spatial_Data | Revisited repository; existing Delhi historical ward file retained without duplicating downloads | Delhi folder states CC BY-SA 2.5 India; historical-vintage caveat still applies |
| https://censusindia.gov.in/nada/index.php/catalog/6286/study-description | Web access failed; previously received Central Delhi workbook preserved | ORGI government Census 2011 table; no additional licence asserted |
| https://www.openstreetmap.org/relation/1942586 | Existing downloaded boundary/help inventory reused; no new retrieval claimed | ODbL 1.0; © OpenStreetMap contributors |
| https://otd.delhi.gov.in/data/static/ and https://otd.delhi.gov.in/data/staticDMRC/ | Public pages visited; downloads require identity/purpose form. No form submitted or file downloaded | https://otd.delhi.gov.in/terms reviewed: DoT terms apply, attribution required; not a blanket open-data licence. No invented identity or access bypass |

All six successful file acquisitions occurred on 2026-10-01 UTC. Download Last-Modified headers are retained as server metadata, not used as the report year. The Haryana/UP/Parliament first sandbox attempts failed on socket permissions; authorized network execution succeeded without disabling TLS or access checks.

## Haryana district and Parliament table review — 2026-10-01

The already-downloaded Haryana Annual Administrative Report 2022 contains a scanned Hindi district-by-IPC table on PDF/printed pages 16–18. Rendered and rotated these pages to inspect the district header and cells. Four selected categories transcribed for Faridabad / Gurugram respectively: cruelty under 498A (286 / 418), dowry death under 304B (20 / 15), insult to modesty under 509 (13 / 84), and rape under 376–376E (167 / 194). These eight records do not constitute total crimes against women. Source: https://haryanapolice.gov.in/PDF/Annual_Admin_Report_2022.pdf ; original retrieval/checksum unchanged from the acquisition audit. Government publication, private research staging; no new licence claim or download. Explicit transcription and district column order are recorded in config/haryana-2022-reviewed.json. No neighbourhood allocation or current-boundary equivalence is asserted.

Visually reviewed page 1 of Rajya Sabha answer 4220 (1 April 2026), https://sansad.in/getFile/annex/270/AU4220_M31fhO.pdf?source=pqars . Extracted Delhi Police crimes-against-women annual totals: 13,208 (2023), 13,195 (2024), 12,458 (2025). The adjacent children and elderly columns are not added. These form a separate reporting series from the older NCRB metropolitan table; category definitions and boundaries have not been proved identical. Retrieval/checksum unchanged; government parliamentary publication, private research staging. No rates or model labels derived.

## Delhi registration-circle extraction — 2026-10-01

Model/reference follow-up on the same downloaded files: `train_district_forecast.py` uses actual annual rape-head cells for Delhi and four NCR reporting units, with original file hashes checked. No new download date is claimed. Evaluation is experimental recorded-volume research and is not a neighbourhood safety prediction. `publish_district_points.py` uses the existing 2026-09-28 OSM snapshot for explicit Central/Shahdara DCP office references and a Dwarka police-station reference; IDs and source links are retained in the generated point file. These are approximate district reference points, not verified boundaries or crime locations. OSM ODbL attribution remains required; the Delhi mirror's unspecified-licence disclosure remains unchanged.

Actual public browser downloads from India Data Portal: [candidate 2017–2022 resource](https://ckandev.indiadataportal.com/dataset/crime-statistics/resource/c8d3ea7e-4855-45f3-9c26-557419e93b6a) and [2024 resource](https://ckandev.indiadataportal.com/dataset/crime-statistics/resource/d8bda878-37a7-4320-8413-36d741bd9b27). Both declare NCRB extraction provenance and **No License Provided**. No licence inferred from the primary publisher. No login or access bypass; automated mirror requests had returned access errors. Candidate file covers 2017–2022 despite inconsistent catalog metadata. New file contains 2024 only. Each year's Delhi rows comprise 15 geographic police districts and eight special units.

Downloaded the original *NCRB Crime in India 2024, Volume I* from [OpenCity](https://data.opencity.in/dataset/crime-in-india-2024/resource/46f760f4-dcf4-4f95-85c9-2225e2f7bbe8); the catalog declares Other (Public Domain). This permitted mirror acquisition supplements the earlier unsuccessful direct NCRB download, rather than changing that audit. Live robots check and crawl delay respected.

Exact download URLs, byte sizes, UTC receipt timestamps and SHA-256 for all three files: **sources/delhi-district-2024-receipt.json**. Filtering, original PDF cell references, calculations, validation and Rohini worked example: **reports/delhi-districts/METHODOLOGY.md**. Raw files remain ignored; research CSV/JSON derivatives are tracked and not loaded into the public app. Mirror redistribution terms remain unconfirmed.

Subsequent app integration: `publish_delhi_districts.py` now exports a Delhi-only factual extract into `public/data/delhi-district-crime.json`, with source links, the unspecified mirror licence and the unresolved comparison retained. No full India source CSV, coordinates or model scores are published. Home and Evidence views display the historical reporting year and distinguish geographic police districts from special units.

The 2024 mirror's 49 category sums total 13,295 versus the original NCRB Delhi UT total of 13,396. Forty-eight category sums match; adult stalking is 77 versus 178, accounting numerically for the 101 gap. Cause and district allocation remain unresolved. Registration circles preserved separately from LGD administrative fields; the mirror's 2024 Dwarka administrative name is Shahdara, an inconsistent crosswalk never used to locate or merge the police unit. No neighbourhood estimates, boundaries, time bands, offender records or safety scores inferred.
# Counts-v1 local workbook audit — 2026-10-01

Earlier-history follow-up attempted an exact publicly indexed NCRB 2021 Volume I link via OpenCity; HTTP 404, no file retrieved or numeric evidence imported. Catalogue pages returned 403 to the web reader. Attempt URL/date and licence uncertainty are in `reports/counts-v1/acquisition-followup.json` and `manifest.csv`; no hash or retrieval date was invented. No training-label changes. Retraining now preserves acquisition-log additions and annotations.

Current total-count model input receipt is `config/counts-v1.json` and `manifest.csv`. Existing local `raw/ncrb/17016840143DistrictwiseCrimeagainstWomen2022.xlsx` and `raw/ncrb/3DistrictwiseCrimeagainstWomen2024.xlsx` have NCRB district-table titles, explicit total columns and exact Delhi/Haryana/UP state reconciliations. Original download URL/date is **unknown**; local observation date is 2026-10-01. No added licence or retrieval-date claim. Government-publication redistribution terms and original acquisition should be checked before release. SHA-256 hashes are frozen in the receipt and manifest.

This audit found parent/child inconsistencies within the 2024 workbook's stalking heads. It uses the explicit published annual total, not a reconstructed sum of those children. The independently downloaded NCRB 2024 Volume I via OpenCity remains the Delhi UT reconciliation source (exact URL/hash in `sources/delhi-district-2024-receipt.json`). No new source was downloaded for this run, and no values were extracted solely from search snippets. Existing DataMeet/OSM/Census inputs were inspected but are not matching police-district context labels. Acquisition and missing-evidence logs: `ACQUISITION_LOG.md`, `MANUAL_DOWNLOADS.md`.

## Historical map reference review — 2026-10-01

Visited the full public [Delhi Police Yuva district directory](https://yuva.delhipolice.gov.in/contact-us.html) on 2026-10-01 to match named stations/localities to all 15 Delhi police-district reporting names. Used public place facts only; staff names, personal phone numbers and page bodies are not retained. No open licence is asserted for the directory. This is a current directory, not a source of historical police-district polygons. Exact OSM IDs/names and assignment URL are saved in `publish_historical_map.py` and the generated feed. OSM coordinates reuse the pinned original help snapshot (ODbL, © OpenStreetMap contributors); no new OSM retrieval claimed.

The primary map feed `public/data/delhi-historical-districts.json` uses the original-titled 2024 workbook's explicit total cells and all 64 category columns. Workbook SHA-256: `cf04a114bff10d9b712b326eda40a91eefa46f45aa1de6d8dcd4870d978895fb`; acquisition URL/date remain unknown, as in the counts-v1 receipt. Fifteen geographic units sum to 13,230; special units add 166, reconciling to the independently downloaded NCRB report's Delhi UT total 13,396. No child totals are summed into headline totals. Reference points are checked against their original OSM geometry and Delhi NCT outline, **not** against unverified police-district boundaries. Current anchors are approximate display references only. Government-workbook redistribution/provenance remains a launch review item.

## Unused geography candidate — 2026-10-02

Public ESRI layer metadata reviewed at https://livingatlas.esri.in/server1/rest/services/NCRB/District_Wise_Crime_Against_Women_2022/MapServer/0 . The URL says 2022 while category fields refer to 2024. Polygon geometry and LGD/Census identifiers do not establish matching Delhi police reporting districts, year continuity or an open redistribution licence. ArcGIS item https://www.arcgis.com/home/item.html?id=15807229ed3342939bfabd8c9606f25e and the two exact item metadata attempts are recorded in ACQUISITION_LOG.md. Reuse metadata could not be verified through the web reader. No file downloaded, receipt hash assigned, numeric record imported or map geometry replaced. Candidate remains excluded rather than being labelled a verified police boundary.

## NCR map source review — 2026-10-02

Reused existing hash-frozen NCRB 2022/2024 workbook TOTAL rows and independently downloaded original report. No new crime file retrieval. NCR publisher verifies all six state/year reconciliations and retains existing acquisition/redistribution limitations. Source hashes/URLs remain in config/counts-v1.json and the existing manifest; output is public/data/ncr-historical-districts.json.

Government locality-context pages reviewed, no statistical files downloaded: https://gurugram.gov.in/ ; https://faridabad.nic.in/public-utility/police-station-nit-faridabad/ ; https://gbnagar.nic.in/contact-us/ ; https://ghaziabad.nic.in/en/police/ . Licence: public government pages, open redistribution licence not asserted. Facts used only for approximate named-place locality context; no verified 2024 district boundary claim. Coordinate data reuse: existing OSM snapshot, ODbL, © OpenStreetMap contributors.

Overpass endpoint https://overpass-api.de/api/interpreter: bounded NCR emergency-facility collection stopped by robots policy before query. No file downloaded; no retrieval date/hash asserted. Receipt sources/ncr-emergency-2026-10-02.json records UTC attempts (local 2026-10-02). Existing partial OSM help snapshot reused, no imaginary fire-station records.

Map style documentation: https://docs.maptiler.com/sdk-js/api/map-styles/ ; https://docs.maptiler.com/cloud/api/maps/ . Reviewed 2026-10-02. MapTiler proprietary service terms/account quotas apply, © MapTiler; styles are not redistributed as open datasets. Detailed light/dark streets and hybrid styles returned HTTP 200 with the locally configured key, which is never stored in audit files.

### Police-jurisdiction candidate review — 2026-10-02

Source: https://dmsouthwest.delhi.gov.in/jurisdiction-maps-of-district/ . Government District South West Delhi page, public reader review only, headings West/South West/Dwarka. Licence: government website, open reuse licence not asserted. Page update September 1, 2026 is not the geometry's effective date. Policy-aware HTML acquisition failed because robots policy was unreadable; no retrieved file, SHA-256 or matching police polygon asserted. Candidate not used in map/allocation.

## Supplied context — 2026-10-02

User-provided local copies: delhi_neighbour.csv; population density wardwise 1.csv; population density wardwise 2.csv; new_delhi_traffic_dataset/probe_counts/geojson/ (20 August 2024 daily files). External source URL, licence and retrieval date not supplied; no official/population year provenance inferred. Exact 23 original-file SHA-256/byte sizes are recorded in sources/supplied-locality-context.json. Traffic README attribution: Ryan Madhuwala (RAW), Garudex Labs. Sampling is road probes, not pedestrians/live traffic/crime. Full joins and limits: SUPPLIED_CONTEXT_REPORT.md. Redistribution terms require review.

MapTiler client metadata: https://raw.githubusercontent.com/maptiler/maptiler-client-js/refs/heads/main/src/mapstyle.ts ; retrieved through policy-aware downloader on local 2026-10-02. Raw acquisition receipt saves UTC timestamp/hash; src/data/map-catalog.json retains URL/hash and 43 variants. Metadata only; proprietary map-service terms/account access still apply. Documentation: https://docs.maptiler.com/sdk-js/api/map-styles/ . No tile bulk download or entitlement to every private/custom style asserted.

## ML volume source reuse — 2026-10-02

ml-volume-v1 reuses the existing 2022/2024 NCRB district workbooks, original report-total PDF check, supplied locality/probe/population context, Delhi NCT outline and approximate OSM references listed above and in manifest.csv. No additional crime data was downloaded. The exact model source hashes and exclusions are saved in reports/ml-volume-v1/export.json and evaluation.json. Original workbook acquisition date/URL and supplied-file reuse terms remain unresolved; model fitting does not resolve them.

Optional advice implementation references official Ollama documentation https://docs.ollama.com/api/generate (reviewed 2026-10-02); no model or model licence is bundled. No victim information or live location is included in any model dataset or advice request.
