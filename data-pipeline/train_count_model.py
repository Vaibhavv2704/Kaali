"""Reproduce NCRB total-count research without modifying the app or its feeds.

Run: .venv/Scripts/python.exe data-pipeline/train_count_model.py
Optional audited inputs belong in interim/counts-v1; absent evidence stays missing.
"""
import csv
import hashlib
import json
import re
import sys
from importlib.metadata import version
from pathlib import Path

import joblib
import numpy as np
import openpyxl
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from count_model import assert_split, count, metrics, smooth_history, time_values, validate_export, BANDS, evidence_confidence
from extract_delhi_districts import GEOGRAPHIC, RECEIPT, checked_file

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'reports'/'counts-v1'
ART = ROOT/'artifacts'/'counts-v1'
INTERIM = ROOT/'interim'/'counts-v1'
STATES = ('Delhi', 'Haryana', 'Uttar Pradesh')
OTHER = {'Gurugram': ('Haryana', 'gurugram'), 'Faridabad': ('Haryana', 'faridabad'),
         'Gautambudh Nagar': ('Uttar Pradesh', 'gautam-buddh-nagar'), 'Ghaziabad': ('Uttar Pradesh', 'ghaziabad')}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def workbook_rows(source):
    path = ROOT/source['path']
    if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
        raise ValueError('Source changed: '+str(path))
    sheet = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    headers = list(sheet.values)[2]
    column = source['total_column']-1
    if not str(sheet.cell(2, column+1).value).startswith('Total Crime against Women'):
        raise ValueError('Total column header changed')
    state = None
    rows, totals = [], {}
    for index, row in enumerate(sheet.values, 1):
        if isinstance(row[0], str) and row[0].startswith(('State:', 'UT:')):
            state = row[0].split(':', 1)[1].strip()
            continue
        if state not in STATES or not isinstance(row[1], str):
            continue
        name = row[1].strip()
        if name.startswith('Total Districts'):
            totals[state] = count(row[column])
        elif isinstance(row[0], (int, float)):
            category_checks = []
            if source['year'] == 2024:
                # Audit adjacent adult/girl subtotals printed in the source.
                # Do not replace source totals when the published hierarchy disagrees.
                for i, label in enumerate(headers):
                    if isinstance(label, str) and '(Total a+b)' in label:
                        children = [count(row[i+1]), count(row[i+2])]
                        parent = count(row[i])
                        computed = None if None in children else sum(children)
                        if computed != parent:
                            category_checks.append({'column': i+1, 'label': label.strip(),
                                                    'reported_parent': parent, 'child_sum': computed,
                                                    'difference': None if computed is None or parent is None else parent-computed})
            rows.append({'state': state, 'source_name': name, 'year': source['year'],
                         'count': count(row[column]), 'source_row': index,
                         'source_path': source['path'], 'source_sha256': source['sha256'],
                         'category_mismatches': category_checks})
    comparisons = []
    for state in STATES:
        values = [r['count'] for r in rows if r['state'] == state]
        subtotal = None if None in values else sum(values)
        official = totals.get(state)
        comparisons.append({'state': state, 'year': source['year'], 'units': len(values),
                            'sum_units': subtotal, 'workbook_state_total': official,
                            'difference': None if subtotal is None or official is None else subtotal-official})
    return rows, comparisons


def observations(config):
    result, checks, mapping = [], [], []
    for source in config['sources']:
        rows, comparisons = workbook_rows(source)
        checks.extend(comparisons)
        for row in rows:
            name, state = row['source_name'], row['state']
            canonical = name.replace('-', ' ')
            delhi_names = {n.replace('-', ' '): n for n in GEOGRAPHIC}
            if state == 'Delhi' and canonical in delhi_names:
                city, unit = 'delhi', delhi_names[canonical]
            elif name in OTHER and OTHER[name][0] == state:
                city, unit = OTHER[name][1], name
            else:
                continue  # Special units are included in reconciliation, never geographic modelling.
            unit_id = city+':'+unit
            result.append({**row, 'unit': unit, 'city': city, 'unit_id': unit_id})
            mapping.append({'source_name': name, 'unit_id': unit_id, 'year': source['year'],
                            'reporting_unit': 'police district/registration circle',
                            'boundary_id': None, 'boundary_verified': False})
    if len({(r['unit_id'], r['year']) for r in result}) != len(result):
        raise ValueError('Duplicate reporting-unit/year')
    return result, checks, mapping


def independent_report_check(checks):
    """Original NCRB Table 3A.1, not search snippets or mirror category sums."""
    from pypdf import PdfReader
    receipt = json.loads(RECEIPT.read_text())
    source = next(s for s in receipt['sources'] if s['localPath'].endswith('vol1-crimeinindia2024.pdf'))
    text = PdfReader(checked_file(source)).pages[326].extract_text()
    if 'TABLE 3A.1' not in text or '2022-2024' not in text:
        raise ValueError('Independent report table changed')
    for entry in checks:
        match = re.search(r'^\d+ '+re.escape(entry['state'])+r' (\d+) (\d+) (\d+) ', text, re.M)
        if not match:
            raise ValueError('State missing from independent report')
        official = int(match.group(1 if entry['year'] == 2022 else 3))
        entry.update({'independent_report_total': official,
                      'independent_difference': None if entry['sum_units'] is None else entry['sum_units']-official,
                      'independent_source': source['localPath'], 'independent_pdf_page': 327,
                      'independent_table': '3A.1'})


def examples(rows):
    result = []
    for row in rows:
        history = sorted([r for r in rows if r['unit_id'] == row['unit_id'] and r['year'] < row['year']
                          and r['count'] is not None], key=lambda r: r['year'])
        if history and row['count'] is not None:
            result.append({**row, 'history_count': history[-1]['count'], 'feature_year': history[-1]['year']})
    return pd.DataFrame(result)


def features(frame):
    columns = [np.log1p(frame.history_count.to_numpy())]
    if 'night_context' in frame and frame.night_context.notna().all():
        columns.append(frame.night_context.to_numpy())
    return np.column_stack(columns)


def prepare_features(frame):
    """Read reviewed evidence if supplied, otherwise retain explicit unknowns.

    Modern OSM snapshots cannot enter historical validation as if they were
    observed in 2022. Source year and matching geography are mandatory.
    """
    frame = frame.copy()
    frame['night_context'] = None
    path = INTERIM/'night-context.json'
    if path.exists():
        entries = json.loads(path.read_text())
        seen = set()
        for entry in entries:
            key = (entry['unit_id'], entry['year'])
            if key in seen:
                raise ValueError('Duplicate context observation')
            seen.add(key)
            if not entry.get('inventory_complete') or not entry.get('boundary_verified') or not entry.get('source_list'):
                continue
            value = entry.get('night_context')
            if value is None:
                continue
            if not np.isfinite(value) or not 0 <= value <= 1:
                raise ValueError('Invalid night score')
            mask = (frame.unit_id == entry['unit_id']) & (frame.feature_year == entry['year'])
            frame.loc[mask, 'night_context'] = value
    adjacency_path = INTERIM/'police-adjacency.json'
    smoothing = 'unavailable: no reviewed matching police-district adjacency'
    if adjacency_path.exists():
        evidence = json.loads(adjacency_path.read_text())
        if not evidence.get('boundary_verified') or not evidence.get('source_list'):
            raise ValueError('Adjacency lacks matching reviewed geometry provenance')
        for year, group in frame.groupby('feature_year'):
            if year not in evidence.get('valid_years', []):
                continue
            history = dict(zip(group.unit_id, group.history_count))
            values = smooth_history(history, evidence['adjacency'])
            for index in group.index:
                value = values[frame.loc[index, 'unit_id']]
                if value is None:
                    raise ValueError('Smoothing requires observed history for every neighbour')
                frame.loc[index, 'history_count'] = value
            smoothing = 'estimated adjacency-weighted history (alpha=0.2); source count labels unchanged'
    return frame, smoothing


def estimator(name, seed):
    if name == 'poisson_glm':
        return make_pipeline(StandardScaler(), PoissonRegressor(alpha=1, max_iter=2000))
    return LGBMRegressor(objective='poisson', n_estimators=40, num_leaves=3, min_child_samples=4,
                         learning_rate=.04, random_state=seed, n_jobs=2, verbosity=-1)


def folds(frame, grouping, seed):
    group = frame.unit_id if grouping == 'district' else frame.city
    splitter = GroupKFold(min(5, group.nunique())) if grouping == 'district' else LeaveOneGroupOut()
    records = {name: [] for name in ('historical_count', 'poisson_glm', 'lightgbm_poisson')}
    for train_idx, test_idx in splitter.split(frame, groups=group):
        train, test = frame.iloc[train_idx], frame.iloc[test_idx]
        assert_split(train, test)
        if grouping == 'city' and set(train.city) & set(test.city):
            raise ValueError('City leakage')
        for name in records:
            prediction = test.history_count.to_numpy() if name == 'historical_count' else estimator(name, seed).fit(features(train), train['count']).predict(features(test))
            for row, value in zip(test.itertuples(), prediction):
                records[name].append({'unit_id': row.unit_id, 'city': row.city, 'year': row.year,
                                      'observed': row.count, 'predicted': float(value),
                                      'training_units': sorted(set(train.unit_id))})
    return {name: {'metrics': metrics([r['observed'] for r in rec], [r['predicted'] for r in rec]),
                   'per_city': {city: metrics([r['observed'] for r in rec if r['city'] == city],
                                              [r['predicted'] for r in rec if r['city'] == city]) for city in sorted(set(frame.city))},
                   'predictions': rec} for name, rec in records.items()}


def bootstrap_mae(actual, prediction, seed=42):
    rng = np.random.default_rng(seed)
    errors = np.abs(np.array(actual)-np.array(prediction))
    means = [float(rng.choice(errors, size=len(errors), replace=True).mean()) for _ in range(1000)]
    return {'method': 'Reporting-unit bootstrap of temporal persistence errors; tiny sample, no prospective coverage guarantee',
            'mae_95_percent_interval': np.quantile(means, [.025, .975]).tolist(),
            'absolute_error_90_percent_quantile': float(np.quantile(errors, .9))}


def bootstrap_forecast_intervals(actual, prediction, seed=42):
    # Empirical residual resampling, not synthetic training labels. Transferring
    # pooled 2022→2024 errors to 2024→2026 assumes stationarity/exchangeability.
    rng = np.random.default_rng(seed)
    errors = np.asarray(actual)-np.asarray(prediction)
    draws = rng.choice(errors, size=10000, replace=True)
    return {'method': 'Empirical bootstrap of pooled signed two-year count errors',
            'residual_5_95_quantiles': np.quantile(draws, [.05, .95]).tolist(),
            'status': 'exploratory_not_calibrated',
            'assumptions': 'Same two-year horizon; errors exchangeable across districts and stable in time. Neither assumption validated. No neighbourhood uncertainty claim.'}


def figures(rows, checks):
    """Standalone SVG figures: no plotting dependency, no invented observations."""
    target = ROOT.parent/'analysis'/'figures'
    target.mkdir(parents=True, exist_ok=True)
    from html import escape
    latest = sorted([r for r in rows if r['year'] == 2024], key=lambda r: r['count'])
    scale = max(r['count'] for r in latest)
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="650" viewBox="0 0 960 650"><rect width="960" height="650" fill="#fff"/><g font-family="sans-serif" font-size="13" fill="#20242a"><text x="24" y="30" font-size="20">NCRB 2024 recorded total cases by police reporting district</text>']
    for i, row in enumerate(latest):
        y = 65+i*29
        parts.append(f'<text x="24" y="{y+14}">{escape(row["unit"])}</text><rect x="230" y="{y}" width="{560*row["count"]/scale:.1f}" height="18" fill="#a72e49"/><text x="{240+560*row["count"]/scale:.1f}" y="{y+14}">{row["count"]}</text>')
    parts.append('</g></svg>')
    (target/'recorded-counts-2024.svg').write_text(''.join(parts), encoding='utf-8')
    by_id = {r['unit_id']: r for r in rows if r['year'] == 2022}
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="700" height="650"><rect width="700" height="650" fill="white"/><g font-family="sans-serif" fill="#20242a"><text x="30" y="28">2022 vs 2024 recorded counts (not an annual trend series)</text><path d="M70 65V570H650" stroke="#333" fill="none"/><text x="270" y="615">2022 total cases</text><text x="12" y="55">2024</text>']
    upper = max(max(r['count'] for r in latest), max(r['count'] for r in by_id.values()))
    for row in latest:
        x, y = 70+550*by_id[row['unit_id']]['count']/upper, 570-490*row['count']/upper
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#a72e49"><title>{escape(row["unit"])}: {by_id[row["unit_id"]]["count"]} → {row["count"]}</title></circle>')
    parts.append('</g></svg>')
    (target/'two-year-counts.svg').write_text(''.join(parts), encoding='utf-8')


def main():
    config = json.loads((ROOT/'config/counts-v1.json').read_text())
    factors = json.loads((ROOT.parent/'config/time_factors.yaml').read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    rows, checks, mapping = observations(config)
    independent_report_check(checks)
    dump(OUT/'observations.json', rows)
    pd.DataFrame(rows).to_csv(OUT/'observations.csv', index=False)
    dump(OUT/'source-total-checks.json', checks)
    dump(OUT/'reporting-unit-mapping.json', mapping)
    frame = examples(rows)
    # Existing help-only OSM extract is not a complete place-context inventory.
    # Adjacency cannot be derived from administrative names or reference points.
    frame, smoothing_status = prepare_features(frame)
    frame.to_csv(ART/'training.csv', index=False)
    spatial = {name: folds(frame, name, config['seed']) for name in ('district', 'city')}
    stability = {str(seed): {name: folds(frame, 'district', seed)[name]['metrics']
                            for name in ('poisson_glm', 'lightgbm_poisson')} for seed in config['seeds']}
    actual, pred = frame['count'].to_numpy(), frame.history_count.to_numpy()
    temporal = {'test_year': 2024, 'feature_year': 2022, 'horizon_years': 2,
                'historical_count': metrics(actual, pred),
                'per_city': {city: metrics(f['count'], f.history_count) for city, f in frame.groupby('city')},
                'learned_models': 'Not testable temporally: no earlier complete district-total lag/target pairs. Spatial fits use 2024 labels and are not temporal validation.'}
    uncertainty = bootstrap_mae(actual, pred)
    uncertainty['forecast_intervals'] = bootstrap_forecast_intervals(actual, pred)
    # Save actual trained ablations separately. Missing context means these are
    # count-only research candidates, not the requested complete context models.
    importance = {}
    for name in ('poisson_glm', 'lightgbm_poisson'):
        fitted = estimator(name, config['seed']).fit(features(frame), frame['count'])
        joblib.dump(fitted, ART/(name+'.joblib'))
        # Importance estimated on held-out districts, never in-sample.
        rng = np.random.default_rng(config['seed'])
        differences = []
        for tr, te in GroupKFold(5).split(frame, groups=frame.unit_id):
            fitted_fold = estimator(name, config['seed']).fit(features(frame.iloc[tr]), frame.iloc[tr]['count'])
            x = features(frame.iloc[te]); y = frame.iloc[te]['count'].to_numpy()
            base = metrics(y, fitted_fold.predict(x))['mae']
            for _ in range(20):
                shuffled = x.copy(); rng.shuffle(shuffled[:, 0])
                differences.append(metrics(y, fitted_fold.predict(shuffled))['mae']-base)
        importance[name] = {'log1p_history_count_permutation_mae_increase': float(np.mean(differences)),
                            'context': None, 'time': None}
    release = {'version': 'counts-v1', 'chosen_model': 'historical_count',
               'reason': 'Simplest valid temporal baseline. Learned candidates lack earlier lag/target pairs for temporal comparison; night context and matching geography are missing.',
               'formula': 'expected_case_index = last_observed_annual_total * time_factor * place_adjustment',
               'feature_list': ['total_recorded_history', 'time_band_and_day_type', 'night_place_context'],
               'implemented_training_features': ['log1p_total_recorded_history'] +
                    (['night_context'] if frame.night_context.notna().all() else []),
               'time_factors': factors, 'place_adjustment': None,
               'smoothing': {'status': smoothing_status},
               'seeds': config['seeds'], 'source_hashes': config['sources'],
               'last_observed_counts': {r['unit_id']: r['count'] for r in rows if r['year'] == 2024},
               'production_eligible': False}
    joblib.dump(release, ART/'model.joblib')
    dump(ART/'config.json', release)
    report = {'version': 'counts-v1', 'observations': len(rows), 'lagged_examples': len(frame),
              'runtime': {'python': sys.version, 'packages': {p: version(p) for p in
                          ('numpy', 'pandas', 'scipy', 'scikit-learn', 'lightgbm', 'openpyxl', 'joblib')}},
              'reporting_years': [2022, 2024], 'source_totals': checks,
              'category_mismatches': [{'unit_id': r['unit_id'], 'year': r['year'], 'checks': r['category_mismatches']}
                                      for r in rows if r['category_mismatches']],
              'temporal': temporal, 'spatial': spatial, 'uncertainty': uncertainty,
              'seed_stability': stability, 'heldout_permutation_importance': importance,
              'chosen_model': release['chosen_model'], 'reason': release['reason'],
              'bias': {'population_correlation': None, 'area_correlation': None, 'morans_i': None,
                       'reason': 'No matched police-district population, area or verified adjacency. Administrative wards are not interchangeable with police districts.',
                       'jurisdiction_check': 'See city holdouts and per-city temporal metrics; one district per Haryana/UP city, no reporting-rate identification.'},
              'sensitivity': {'missing_history': 'unknown', 'missing_context': 'unknown risk; annual persistence retained as historical research index',
                              'missing_time_labels': 'neutral assumed factors, no time training',
                              'factor_scenarios': {str(f): time_values(100, 1, {'weekday': [f]*6, 'weekend': [f]*6})
                                                   for f in (.75, 1, 1.25)},
                              'percentile_effect': 'Common time multipliers change volume indices but do not change within-band area ordering.'}}
    dump(OUT/'evaluation.json', report)
    exports = []
    for r in rows:
        if r['year'] != 2024:
            continue
        item = {'id': r['unit_id'], 'reporting_unit': 'police district', 'year': 2024,
                'source_list': [r['source_path']], 'data_type': 'real' if r['count'] is not None else 'unknown',
                'confidence': evidence_confidence(history=r['count'] is not None, context=False,
                    geometry=False, time_observed=False, source_count=1),
                'confidence_basis': 'Heuristic completeness score, not calibrated model probability; context/geography/time evidence absent.',
                'total_reported_cases': r['count'], 'risk_score': None, 'level': 'unknown',
                'top_windows': [], 'time_bands': [{'time_band': band, 'day_type': day,
                    'risk_score': None, 'level': 'unknown', 'time_factor': factors[day][i],
                    'time_data_type': 'assumed', 'expected_case_index': None}
                    for day in ('weekday', 'weekend') for i, band in enumerate(BANDS)],
                'expected_annual_cases_baseline': r['count'],
                'baseline_data_type': 'estimated', 'neighbourhood_outputs': 'unavailable: missing reviewed crosswalk/context'}
        low, high = uncertainty['forecast_intervals']['residual_5_95_quantiles']
        item['annual_count_forecast'] = {'year': 2026, 'expected_cases': r['count'],
             'data_type': 'estimated', 'model': 'historical_count_persistence',
             'exploratory_90_percent_interval': None if r['count'] is None else [max(0, r['count']+low), max(0, r['count']+high)],
             'interval_status': 'pooled_bootstrap_not_calibrated; excludes missing place/time effects',
             'not_a_safety_score': True}
        validate_export(item)
        exports.append(item)
    dump(OUT/'district-research-export.json', {'version': 'counts-v1', 'records': exports})
    dump(OUT/'neighbourhoods.geojson', {'type': 'FeatureCollection', 'features': [],
         'metadata': {'status': 'unknown', 'reason': 'No matching police boundaries or reviewed ward/H3 crosswalk; no polygons invented.'}})
    figures(rows, checks)
    dump(OUT/'artifact-hashes.json', {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in sorted(ART.iterdir()) if p.is_file()})
    from count_model_docs import write_docs
    write_docs(ROOT, rows, report, config)
    print(json.dumps({'observations': len(rows), 'examples': len(frame),
                      'temporal_baseline': temporal['historical_count'],
                      'district_holdout_comparison': {n: x['metrics'] for n, x in spatial['district'].items()},
                      'state_total_mismatches': [c for c in checks if c['difference'] != 0]}, indent=2))


if __name__ == '__main__':
    main()
