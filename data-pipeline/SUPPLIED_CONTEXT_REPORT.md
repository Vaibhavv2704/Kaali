# Supplied locality, population and traffic context — 2026-10-02

## Inputs and preparation

The three CSV copies supplied under `data-pipeline/` and `new_delhi_traffic_dataset/` are preserved. Their Desktop paths were absent. `prepare_locality_context.py` reads these originals and saves SHA-256/byte-size receipts in `sources/supplied-locality-context.json`. No download or official provenance is asserted for these inputs. Licences/source URLs and population dates were not supplied; redistribution requires review. The traffic README attributes the collection to Ryan Madhuwala (RAW), Garudex Labs. Road-export metadata contains sampled probe counts; these are not counts of all vehicles, people or crime.

Of 185 locality rows, 153 have numeric coordinates inside configured NCR bounds. Missing/out-of-bounds coordinates are rejected with original row IDs; no coordinates guessed. Names/coordinates remain unverified references, including possible plausible-but-wrong coordinates inside the bounds. A nearest-reference name is not a verified GPS locality match. Administrative borough names are not joined to police districts.

Population CSV 1 has `Longitude` values around 28 and `latitude` values around 77. The importer corrects this reversal in memory. Unique normalised name matches must also lie within 2 km and satisfy population/area=density: six density matches survive. Population CSV 2 supplies ward population without area/geometry; 67 additional unique name-only population matches are retained as context, yielding 73 population records overall. They are explicitly not spatial ward matches. No density inferred from this second file. Population/density dates and units remain unverified. Scheduled-caste counts are not used.

Twenty traffic files cover 11–30 August 2024. Metadata is checked for one actual reporting date per file and 24 hourly time sets. Segment coordinates are averaged for a reference-assignment point; each segment goes only to its nearest supplied reference within 1 km, using a local planar distance approximation. Counts are aggregated as mean sampled probes per segment-hour, separately for weekday/weekend and six four-hour bands. 78 locality references have traffic matches. Repeated segments/dates are observations, not independent people. Missing values remain missing; observed zeros are preserved. Segment sets/counts and per-file assignment coverage are recorded in the receipt. Festival/monsoon sampling and collection coverage limit extrapolation. Data do not represent current traffic, congestion, measured footfall or all NCR roads.

Run: `python data-pipeline/prepare_locality_context.py`. Export: `public/data/delhi-ncr/locality-context.json`. Original large road files are not copied to the app or committed.

## Transparent map cells and assumptions

H3 resolution-8 cells surround supplied reference coordinates; they are not locality boundaries, police units or danger radii. Cells do not cover all neighbourhoods. The map's separate recorded police-district circles keep their original totals and band rules. No district total is assigned to a locality; all locality `reportedCases` values remain null.

The activity illustration is not a fitted crime model. For observed mean probes `p`, activity term = `1/(1+log(1+p))`; assumed night weights for the six bands are `[0.8,0.5,0.2,0.2,0.4,1]`. Index = `100 × (0.55 × night + 0.45 × activity)`, rounded. When source density is matched and at least two matched densities exist, multiply by `1 − 0.1 × density rank / number of matched densities`. This weak adjustment assumes density might reflect activity; it is not causal protection. Missing density has no adjustment, never a guessed value. Missing road observations yield unknown/grey cells. Pale rose through crimson encode this assumed index, not probability or validated Low/High danger classifications. Population is shown in the summary but is not used as measured street activity. No performance metrics, retrained crime model or calibrated neighbourhood forecast are claimed.

## Location and advice

The main map requests geolocation only after consent. A high-accuracy device watch supplies a blue glowing dot and an accuracy circle. Device readings are estimates, not exact positions. Position stays in component memory; stop/unmount clears it and ignores queued callbacks. No GPS coordinates go to a geocoder, server, analytics or AI service. Viewed map tiles disclose the viewport to MapTiler. Native sharing sends coordinates only after pressing Share location.

The on-device summary changes with IST, weekday/weekend, nearest supplied reference and historical traffic/population context. It uses locally written rules, not live LLM inference. It explicitly states unknown local crime risk; advice suggests route/pickup planning, licensed transport when useful, voluntary sharing and 112. It never orders a person to stay indoors or claims a prediction establishes their safety. The nearest police label uses the mapped OSM snapshot and straight-line distance, not an operational dispatch directory.

## Layout catalogue

`refresh_map_catalog.py` downloads the public MapTiler client style metadata with policy checks and a hash. `src/data/map-catalog.json` contains 43 variants without an explicit active `deprecated: true` flag, plus three theme-following presets in the app. Official source URL/hash are stored; account entitlement/HTTP availability of every variant is not asserted. Explicit variants retain their selected style; automatic streets/muted presets follow theme. Custom/private account styles are outside this public catalogue. Unsupported styles show the existing tile error while records remain available. Sources/markers/icons are restored on style events. Catalogue reference: https://docs.maptiler.com/sdk-js/api/map-styles/ . MapTiler/OSM attribution remains intact.

## Remaining model evidence

These files improve activity context but add no observed locality crime labels or matching police boundaries. They cannot support honest supervised neighbourhood-crime training by themselves. Existing counts-only research remains unchanged; neighbourhood count downscaling awaits a reviewed police-to-locality crosswalk with allocation weights. Genuine time-of-occurrence labels would replace assumed time factors. Before publishing, confirm original CSV/probe source URLs, licence, sampling method, density units/date, ward vintage and reference coordinates.

References sharing a cell are merged into 129 distinct polygons, averaging available assumed indices rather than stacking fill opacity. The location summary also shows the actual recorded regional subtotal/year separately from unknown locality counts. Outside-reference positions receive no locality assignment; GPS can still be shown outside the configured region.
