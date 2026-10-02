# Kaali 0.1.0: Delhi NCR early access

Release scope: Delhi NCR awareness map, historical recorded-case display, experimental locality advisories, emergency resources and client-only location. The software scope is complete for early access; this does not certify neighbourhood safety predictions.

Includes light/dark themes, MapTiler layouts, collapsible glass controls, district search/breakdowns, police/hospital overlays (metro optional), automatic location after prior consent, blue accuracy marker, and detailed on-device precautions. No offender profiles or cloud AI requests in the location flow.

Release checks: 100 frontend tests and 64 pipeline tests pass, along with lint, TypeScript, static-data validation and production build. Desktop/mobile browser checks cover theme switches, district selection/search, help filters, helpline tabs/search and evidence navigation. GPS permission/grant and physical-phone frame rate were not independently verified in this release check.

The recorded counts are historical. Locality cells are approximate reference geometry; time and context adjustments are assumed. Traffic samples are historical road probes. Advice is precautionary guidance, not real-time danger detection. Source licences, matched police boundaries, additional temporal cohorts and measured locality/time-band labels remain research work.

Deployment uses Render Static Sites, with the MapTiler client key supplied through the build environment. Local secrets, original supplied CSV/traffic files and raw inputs are excluded from Git.
