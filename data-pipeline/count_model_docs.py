"""Generate documentation and receipts from actual counts-v1 run results."""
import csv
import json
from pathlib import Path
import numpy as np


def update_manifest(path, entries):
    """Refresh reproducible input receipts without erasing later acquisitions."""
    previous = []
    fields = list(entries[0])
    if path.exists():
        with path.open(encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream)
            previous = list(reader)
            fields = list(dict.fromkeys([*(reader.fieldnames or []), *fields]))
    def key(row):
        return row.get('path', ''), row.get('download_url', '')
    replacements = {key(row): row for row in entries}
    merged = []
    for row in previous:
        new = replacements.pop(key(row), None)
        # Preserve free-form annotations and supplied metadata when the
        # generated receipt has no known value. Do not invent verification.
        merged.append({**row, **{k: v for k, v in (new or {}).items() if v != ''}})
    merged.extend(replacements.values())
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader(); writer.writerows(merged)


def write_docs(root, rows, report, config):
    analysis = root.parent/'analysis'
    analysis.mkdir(exist_ok=True)
    compare = report['spatial']['district']
    table = '| Model (count-only) | District holdout MAE | RMSE | Spearman | Top-20% hit rate |\n|---|---:|---:|---:|---:|\n'
    for name, entry in compare.items():
        m = entry['metrics']
        table += f'| {name} | {m["mae"]:.2f} | {m["rmse"]:.2f} | {m["spearman"]:.3f} | {m["hotspot_hit_rate"]:.0%} |\n'
    card = f'''# Kaali model card — counts-v1

## Purpose and status

Research forecasting of **recorded annual total crimes against women**, not individual safety or current danger. This counts-only study supersedes the earlier selected-rape-head experiment for the latest task. No UI or public app data is changed. Modelled and assumed values are never measured facts.

**Selected model: historical-count persistence.** Actual Poisson GLM and LightGBM artifacts were trained and saved, but are count-only ablations because complete night context is missing. A complete three-input neighbourhood risk model has **not** been validated or published.

## Data and label strategy

Two existing local NCRB-titled district workbooks, reporting years **2022 and 2024**, provide {len(rows)} actual total-count observations: 15 Delhi police districts plus Gurugram, Faridabad, Gautambudh Nagar and Ghaziabad. GBN remains one reporting area; Noida and Greater Noida are not invented separate labels. The original workbook download URLs, acquisition dates and independent publisher receipts are unavailable. File hashes, header identities and reconciliation are retained in config/counts-v1.json and manifest.csv. Verify original acquisition and reuse terms before publishing.

Targets use only the explicit total column (2022 column 54; 2024 column 67). No parent-plus-child sums, rates per population, blank-to-zero conversions or estimated neighbourhood labels are training targets. All reporting units, including special units, sum exactly to the workbook Delhi/Haryana/UP state total in both years. Special units are excluded from geographic modelling. Delhi total is 14,247 in 2022 and 13,396 in 2024, consistent with the previously downloaded NCRB 2024 report Table 3A.1. This check validates workbook totals, not district boundary continuity or every category cell.

The 2024 workbook itself has stalking parent/child inconsistencies. Delhi parent stalking total is 178 while adult/girl children sum to 77. Those discrepancies also explain why the earlier mirror leaf-sum extract differed from the explicit total. The underlying cause is unknown. The new pipeline audits all printed adjacent adult/girl subtotal identities and records every selected-district mismatch without repairing source values. Rohini's explicit total is **883**; the earlier mirror-derived leaf subtotal was 879. These are different source calculations and are not silently substituted in the app.

IPC/BNS transitions remain a comparability limitation. Explicit paired legal labels from the 2024 header are mapped conservatively in count_model.py; unreviewed categories stay unmapped. Totals are retained as each year's published definition, including newly introduced categories. No assertion of identical legal scope across years is made.

## Exactly three intended inputs

1. Previous observed annual total cases, optionally smoothed using reviewed matching police-district adjacency: 0.8 own count + 0.2 neighbouring mean. **Current run is unsmoothed:** matching adjacency is unavailable. Revenue names, ward boundaries and approximate reference points are not police geography.
2. Six four-hour bands and weekday/weekend. There are no observed time labels. config/time_factors.yaml uses neutral **assumed** multipliers of 1. No time model is trained and no preferred risky window is invented.
3. One night-context score from reviewed OSM/open context. Missing for every training example. The current OSM file is a help-only inventory (not complete land use/roads/isolation/transit/late-open density), and is from 2026, after the validation target. It cannot be disguised as historical context. Optional reviewed historical context inputs are documented in reports/counts-v1/README.md.

Future work only: socio-economic predictors, CCTV, police-station distance and other excluded inputs. Density may support place context/allocation; it is never a target-rate denominator.

## Formula, confidence and export

`expected_case_index = annual baseline × time factor × place-context adjustment`.

The adjustment is unavailable, rather than fabricated as a fitted coefficient. The count-only research baseline can be inspected separately. A time multiplier on an annual index does not create measured four-hour case counts. Common within-band factors cannot change percentile area ordering.

The scoring utility implements percentile rank × 100 within eligible areas, tie-average ranks, and 25/50/75 bucket thresholds. Low confidence (<0.6), missing context, missing geometry and singleton comparisons remain **unknown**. Export's 0.25 completeness score is a conservative heuristic, not calibrated probability. Real district totals are retained alongside unknown risk entries in all twelve day/band combinations. No synthetic data is trained; synthetic unit fixtures are separate.

The tested downscale allocator requires measured density, road density and built-up weights and a verified complete district partition. Normalized weights sum back to each district total, with a floating-point residual correction. Counts are labelled estimated; observed neighbourhood totals remain null. No real downscaling has been performed because a matching crosswalk and inputs are missing. The versioned GeoJSON is empty with an explicit reason. **PMTiles is not generated from missing geometry.**

## Validation and comparison

{table}

Five whole-reporting-district folds and five leave-city-out folds use the 2024 targets and only 2022 count features. They test cross-area transfer, not future forecasting. No random observation splits. Persisted fold training IDs and tests prove train/test areas are disjoint and feature cutoff precedes target year.

Temporal persistence backtest: 2022 counts predict 2024 totals over a two-year gap, MAE **{report['temporal']['historical_count']['mae']:.2f}**, RMSE **{report['temporal']['historical_count']['rmse']:.2f}**, Spearman **{report['temporal']['historical_count']['spearman']:.3f}**. No 2023 interpolation. Learned models cannot be independently temporally tested: only one complete lag/target pair exists per district. They would need earlier complete targets to train before 2024. This is why persistence remains the selected baseline, rather than claiming the spatial fit is a temporal safety validation.

City holdout MAE: GLM {report['spatial']['city']['poisson_glm']['metrics']['mae']:.2f}, LightGBM {report['spatial']['city']['lightgbm_poisson']['metrics']['mae']:.2f}. Per-city temporal persistence MAE: Delhi 82.47 (15 districts), Faridabad 24, Gurugram 17, GBN 509, Ghaziabad 802 (each outside Delhi has one target). Singleton rank metrics are unavailable; their top-k hit rate is trivial and cannot validate hotspots.

Calibration bins, predicted/observed total ratios, per-city metrics, held-out permutation importance and seeds 7/42/103 are in evaluation.json. Seed outputs are identical for the current deterministic settings; this does not imply data stability. No hyperparameter search was performed on the held-out data.

## Uncertainty, sensitivity and bias

Reporting-unit bootstrap of temporal persistence errors, fixed seed 42, 1,000 draws: MAE 95% interval **{report['uncertainty']['mae_95_percent_interval'][0]:.2f}–{report['uncertainty']['mae_95_percent_interval'][1]:.2f}** cases. Absolute-error 90th quantile {report['uncertainty']['absolute_error_90_percent_quantile']:.2f}. These describe this small retrospective error sample; they are not calibrated future per-neighbourhood prediction intervals. No false quantile coverage claim.

District research exports also carry **estimated 2026 annual persistence forecasts** and exploratory 90% intervals from 10,000 resampled pooled signed 2022→2024 errors. This uses the same two-year horizon and assumes stable, exchangeable district errors. The assumption is not validated, and pooled errors do not capture missing place/time inputs or jurisdiction differences. Forecasts are distinct from the 2024 measured total, carry low confidence and no risk score, and are not written to app feeds.

Sensitivity scenarios multiply an illustrative baseline index (100, explicitly a scenario constant) by 0.75/1/1.25. They are not crime observations and are not trained. Missing history makes outputs unknown; missing context suppresses risk but retains historical-count research. No time observations means neutral factors and no time learning.

Population/area correlations and Moran's I are **unavailable**, since matched police-unit population, area and adjacency are missing. Administrative geography must not be used as a substitute. Whole-city results reveal poor transfer to UP reporting areas, but neither establish causes nor identify reporting-rate differences. Counts inherently depend on jurisdiction size, population, police recording practices and reporting willingness. Under-reporting and affluent/low-reporting area differences remain unresolved. Low observed volume never establishes safety.

## Sources, licences and next evidence

NCRB workbook provenance/redistribution terms need confirmation; downloaded original report via OpenCity is attributed to NCRB (mirror declares Other/Public Domain). India Data Portal mirrors declare no licence and are not used as total-count labels here. OSM: ODbL 1.0, © OpenStreetMap contributors; evaluate derivative-database obligations. Historical DataMeet wards: CC BY-SA 2.5 India; boundary vintage/crosswalk unverified. Census government table is Central Delhi 2011 only, not all police districts; no added open-licence claim. No login, paywall or robots restriction was bypassed.

Next: earlier original total-count workbooks for honest temporal learned-model testing; reviewed matching police geography plus complete context for downscaling; RTI for finer aggregate counts and observed time bands; SafeCity/Safetipin for separately reviewed crowd reports/environment audits. These are acquisition steps, not fabricated inputs. Exact gaps and intended local destinations are in MANUAL_DOWNLOADS.md. No new API key is needed to reproduce this run.
'''
    card_path = root/'MODEL_CARD.md'
    if card_path.exists() and not card_path.read_text(encoding='utf-8').startswith('# Kaali model card — counts-v1'):
        legacy = root/'reports/MODEL_CARD_PRE_COUNTS.md'
        if not legacy.exists(): legacy.write_text(card_path.read_text(encoding='utf-8'), encoding='utf-8')
    card_path.write_text(card, encoding='utf-8')
    values = np.array([r['count'] for r in rows])
    q1, q3 = np.quantile(values, [.25, .75]); limit = q3+1.5*(q3-q1)
    outliers = [(r['unit'], r['year'], r['count']) for r in rows if r['count'] > limit]
    eda = f'''# Counts-v1 exploratory data analysis

Source-backed observations: {len(rows)}, 19 reporting units, years 2022 and 2024. Latest usable local original district workbook year: 2024. Special units are reconciled separately, not modelled. No 2023 or time-band observations are invented.

## Distributions, two-year changes and outliers

Across the two-year panel: min {values.min()}, median {np.median(values):.1f}, mean {values.mean():.1f}, max {values.max()} total recorded cases. Tukey upper fence {limit:.1f}; flagged rows {outliers}. These are descriptive outliers, not errors or danger classifications.

![2024 recorded district totals](figures/recorded-counts-2024.svg)

![2022 versus 2024 totals](figures/two-year-counts.svg)

GBN changes from 940 to 431; Ghaziabad from 1,597 to 2,399. The available files do not establish whether this reflects crime incidence, reporting, recording, legal scope or geography changes. Two observations do not constitute a reliable annual trend. Delhi's geographic districts must be kept separate from special-unit totals and NCRB metropolitan tables.

## Missingness

| Input | Missing among 38 district/year observations | Consequence |
|---|---:|---|
| Explicit annual total | 0 | Usable recorded-count labels |
| Observed four-hour/day-type counts | 38 | Assumed neutral factors only |
| Complete historical night context | 38 | Count-only ablations |
| Matching verified police-district boundary | 38 | No downscaling or district area |
| Matched district population | 38 | No population bias correlation |

![Input missingness](figures/missingness.svg)

Blank raw values stay missing. Source adult/girl stalking columns disagree with parent stalking totals in all 19 selected 2024 districts; category differences are saved in evaluation.json. Explicit reported annual totals, not the inconsistent child sums, are labels. All six state/year sums equal the original workbook state total. This is reconciliation, not independent verification of every source case.

## Correlations and spatial autocorrelation

Temporal count-order Spearman (2022 versus 2024): {report['temporal']['historical_count']['spearman']:.3f}. Correlation with police-district area: unavailable. Correlation with matched police-district population: unavailable. Moran's I: unavailable without matching boundaries/adjacency. Assigning revenue districts or guessed points would create misleading spatial statistics. None are reported as zero.

## Validation interpretation

{table}

The learned fits are whole-district retrospective transfer tests. Persistence has a genuine 2022→2024 forecast comparison; learned models do not have an earlier independent temporal fit. One observation per non-Delhi city makes city-specific claims weak. Cross-state counts are not normalized rates and should not be interpreted as comparable individual danger. See MODEL_CARD.md and evaluation.json for calibration, uncertainty, limitations and exact fold identities.
'''
    (analysis/'EDA.md').write_text(eda, encoding='utf-8')
    bars = ''.join(f'<text x="18" y="{60+i*46}">{name}</text><rect x="295" y="{43+i*46}" width="{missing*8}" height="24" fill="#a72e49"/><text x="615" y="{60+i*46}">{missing}/38 missing</text>' for i, (name, missing) in enumerate([('Annual totals', 0), ('Time observations', 38), ('Historical night context', 38), ('Matching police boundaries', 38), ('Matched population', 38)]))
    (analysis/'figures/missingness.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="780" height="290"><rect width="780" height="290" fill="white"/><g font-family="sans-serif" font-size="14" fill="#20242a"><text x="18" y="24">Observed input completeness (district/year panel)</text>'+bars+'</g></svg>', encoding='utf-8')

    manifest = root/'manifest.csv'
    entries = []
    for s in config['sources']:
        entries.append({'path': s['path'], 'source_url': '', 'download_url': '', 'retrieval_date': '',
                        'observed_local_date': s['discovered_local_date'], 'sha256': s['sha256'],
                        'licence': s['licence'], 'status': 'existing_local_original_receipt_missing',
                        'usage': 'counts-v1 labels, header/source-total checked'})
    # Include existing audited context inputs; no new acquisition dates claimed.
    for s in json.loads((root/'config/phase1-inputs.json').read_text())['inputs']:
        entries.append({'path': s['path'], 'source_url': s['sourceUrl'], 'download_url': '',
                        'retrieval_date': s['retrievedAt'], 'observed_local_date': '', 'sha256': s['sha256'],
                        'licence': s['licence'], 'status': 'existing_audited_input',
                        'usage': 'inspected; not counts-v1 model labels or matched context'})
    receipt = json.loads((root/'sources/delhi-district-2024-receipt.json').read_text())
    s = next(s for s in receipt['sources'] if s['id'] == 'ncrb-2024-volume-1')
    entries.append({'path': s['localPath'], 'source_url': s['resourceUrl'], 'download_url': s['downloadUrl'],
                    'retrieval_date': s['retrievedAt'], 'observed_local_date': '', 'sha256': s['sha256'],
                    'licence': s['licenceDeclared'], 'status': 'previous_automatic_download',
                    'usage': 'independent state/UT total reconciliation, Table 3A.1'})
    update_manifest(manifest, entries)


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    write_docs(root, json.loads((root/'reports/counts-v1/observations.json').read_text()),
               json.loads((root/'reports/counts-v1/evaluation.json').read_text()),
               json.loads((root/'config/counts-v1.json').read_text()))
