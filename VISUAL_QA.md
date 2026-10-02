# Early-access visual checks

Checked on 2 October 2026 in the Codex in-app browser: desktop CSS viewport 1440×900 and mobile CSS viewport 360×800, light and dark themes.

| Page | Desktop | Mobile | Interactions checked |
| --- | --- | --- | --- |
| Map | Light/dark | Light/dark | Theme/layers, district search and Rohini selection, collapsible controls, help filters, hourly time selector |
| Helplines | Light/dark | Light/dark | Four jurisdiction tabs, UP/1090 search, tap-to-call link presence (not test-called) |
| Crime data | Light/dark | Light/dark | Navigation, readable source cards, table wrapping |

Fixed mobile helpline tabs to a 2×2 grid, kept the emergency header fixed while scrolling, compacted duplicate attribution, and separated mobile expanded panels from bottom controls. DOM measurements showed no horizontal page overflow at the tested widths. Browser console checks on the map returned no errors.

Local screenshots are in `artifacts/visual-qa/` (excluded from Git). The browser's viewport capture exhibited scaling/compositing artifacts and stalled once; screenshots are review evidence, not a claim of physical-device GPU performance. Live deployment will be checked separately. Precise GPS screenshots are not published.

Not covered: real-phone 60fps measurements, live GPS grant/movement, screen-reader audit, every MapTiler catalogue style or long-running provider outages.
