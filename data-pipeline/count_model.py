"""Counts-only research utilities. Missing evidence is never an observed zero."""
import math
import numpy as np
from scipy.stats import spearmanr

BANDS = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24']

# Only equivalences explicitly printed together in the 2024 source headers.
# These mappings do not imply all IPC/BNS definitions or year totals are equal.
LEGAL_HEADS = {'Sec.376 IPC': 'rape', 'Sec 64-68,70-71 BNS': 'rape',
               'Sec 304B IPC': 'dowry_deaths', 'Sec 80 BNS': 'dowry_deaths',
               'Sec 498-A IPC': 'cruelty_husband_relatives', 'Sec 85 BNS': 'cruelty_husband_relatives'}


def normalise_head(source_label):
    return LEGAL_HEADS.get(source_label)  # Unknown categories require review.


def count(value):
    if value is None or str(value).strip() in ('', '-', 'NA', 'N/A'):
        return None
    number = float(value)
    if not math.isfinite(number) or number < 0 or not number.is_integer():
        raise ValueError('A recorded count must be a nonnegative integer')
    return int(number)


def assert_split(train, test, *, spatial=True):
    if train.empty or test.empty:
        raise ValueError('Empty validation partition')
    if not (train.feature_year < train.year).all() or not (test.feature_year < test.year).all():
        raise ValueError('Target year leaked into history')
    if spatial and set(train.unit_id) & set(test.unit_id):
        raise ValueError('Held-out reporting areas overlap training areas')
    if not spatial and train.year.max() >= test.year.min():
        raise ValueError('Temporal target years overlap')


def smooth_history(values, adjacency, alpha=0.2):
    """Adjacency must come from matching reviewed police boundaries, not names."""
    if not 0 <= alpha <= 1:
        raise ValueError('Invalid smoothing weight')
    result = {}
    for key, value in values.items():
        neighbours = adjacency.get(key, [])
        if value is None or any(values.get(n) is None for n in neighbours):
            result[key] = None
        else:
            result[key] = (1-alpha)*value + alpha*np.mean([values[n] for n in neighbours]) if neighbours else float(value)
    return result


def downscale(total, zones):
    """Allocate exactly using independently measured nonnegative weights.

    Required inputs: reviewed district crosswalk, density, road density and
    built-up fraction. Missing inputs reject allocation rather than invent it.
    Expected counts are fractional estimates; residual correction conserves sum.
    """
    if count(total) is None or not zones:
        raise ValueError('Missing reported total or neighbourhoods')
    if len({z['id'] for z in zones}) != len(zones):
        raise ValueError('Duplicate neighbourhood')
    districts = {z.get('district_id') for z in zones}
    if None in districts or len(districts) != 1:
        raise ValueError('Cross-border or missing district identity')
    for z in zones:
        if not z.get('crosswalk_verified'):
            raise ValueError('Unverified police-district crosswalk')
        for field in ('density', 'road_density', 'built_up'):
            value = z.get(field)
            if value is None or not math.isfinite(value) or value < 0:
                raise ValueError('Missing or invalid allocation context')
    # Each component is normalized inside the district, avoiding mixed units.
    weights = np.zeros(len(zones))
    for field in ('density', 'road_density', 'built_up'):
        component = np.array([z[field] for z in zones], dtype=float)
        if component.sum() <= 0:
            raise ValueError('Uninformative allocation component')
        weights += component/component.sum()/3
    values = weights*total
    values[-1] = total-float(values[:-1].sum())
    return [{'id': z['id'], 'district_id': z['district_id'], 'estimated_cases': float(v),
             'data_type': 'estimated', 'total_reported_cases': None,
             'district_total_reported_cases': total} for z, v in zip(zones, values)]


def night_context(components, *, inventory_complete):
    """One documented proxy; never infer absent OSM tags are observed absence.

    Components are audited 0..1 indices: isolation, dead ends, transit,
    explicit late-open POIs, built-up activity. This formula is assumed,
    not a validated relationship between environments and crime.
    """
    names = ('isolation', 'dead_ends', 'transit', 'late_open', 'built_up_activity')
    if not inventory_complete or any(components.get(n) is None for n in names):
        return None
    if any(not math.isfinite(components[n]) or not 0 <= components[n] <= 1 for n in names):
        raise ValueError('Context components must be within [0,1]')
    return sum([components['isolation'], components['dead_ends'],
                1-components['transit'], 1-components['late_open'],
                1-components['built_up_activity']])/5


def bucket(score):
    if score is None:
        return 'unknown'
    if not math.isfinite(score) or not 0 <= score <= 100:
        raise ValueError('Invalid percentile')
    return 'Low' if score < 25 else 'Moderate' if score < 50 else 'High' if score < 75 else 'Very High'


def evidence_confidence(*, history, context, geometry, time_observed, source_count):
    """Explicit completeness heuristic, never a calibrated safety probability."""
    if not history:
        return 0.0
    if source_count < 0:
        raise ValueError('Invalid source count')
    diversity = min(max(source_count-1, 0)/2, 1)
    return .25 + .25*bool(context) + .25*bool(geometry) + .15*bool(time_observed) + .1*diversity


def scores(expected, confidence, threshold=0.6):
    """Percentiles exclude unknown entries; singleton rank is unknown."""
    from scipy.stats import rankdata
    if len(expected) != len(confidence) or any(not math.isfinite(c) or not 0 <= c <= 1 for c in confidence):
        raise ValueError('Invalid confidence vector')
    eligible = [i for i, v in enumerate(expected) if v is not None and math.isfinite(v)
                and v >= 0 and confidence[i] >= threshold]
    output = [None]*len(expected)
    if len(eligible) > 1:
        for i, rank in zip(eligible, rankdata([expected[i] for i in eligible], method='average')):
            output[i] = float(100*(rank-1)/(len(eligible)-1))
    return output


def time_values(baseline, adjustment, factors):
    if baseline is None or adjustment is None:
        return []
    if not math.isfinite(baseline) or baseline < 0 or not math.isfinite(adjustment) or adjustment <= 0:
        raise ValueError('Invalid case index')
    result = []
    for day in ('weekday', 'weekend'):
        if len(factors[day]) != 6:
            raise ValueError('Expected six bands')
        for band, factor in zip(BANDS, factors[day]):
            if not math.isfinite(factor) or factor <= 0:
                raise ValueError('Invalid time multiplier')
            result.append({'day_type': day, 'time_band': band, 'expected_case_index': baseline*factor*adjustment,
                           'time_factor': factor, 'time_data_type': 'assumed'})
    return result


def metrics(actual, predicted):
    actual, predicted = np.array(actual, dtype=float), np.array(predicted, dtype=float)
    if not len(actual) or not np.isfinite(predicted).all() or (predicted < 0).any():
        raise ValueError('Invalid evaluation values')
    k = max(1, math.ceil(len(actual)*0.2))
    corr = spearmanr(actual, predicted).statistic if len(actual) > 1 and np.ptp(actual) and np.ptp(predicted) else None
    bins = np.array_split(np.argsort(predicted, kind='stable'), min(4, len(actual)))
    return {'n': len(actual), 'mae': float(np.abs(actual-predicted).mean()),
            'rmse': float(np.sqrt(((actual-predicted)**2).mean())),
            'spearman': float(corr) if corr is not None and math.isfinite(corr) else None,
            'top_k': k, 'hotspot_hit_rate': len(set(np.argsort(actual)[-k:]) & set(np.argsort(predicted)[-k:]))/k,
            'calibration_ratio_predicted_to_observed': float(predicted.sum()/actual.sum()) if actual.sum() else None,
            'calibration_bins': [{'n': len(b), 'mean_observed': float(actual[b].mean()),
                                  'mean_predicted': float(predicted[b].mean())} for b in bins]}


def validate_export(record):
    required = ('id', 'year', 'source_list', 'data_type', 'confidence', 'risk_score', 'level',
                'total_reported_cases', 'top_windows', 'time_bands')
    if any(k not in record for k in required) or not record['source_list']:
        raise ValueError('Incomplete export')
    if record['data_type'] not in ('real', 'estimated', 'assumed', 'unknown'):
        raise ValueError('Invalid provenance')
    if not 0 <= record['confidence'] <= 1:
        raise ValueError('Invalid confidence')
    if record['level'] != bucket(record['risk_score']):
        raise ValueError('Score and level disagree')
    if record['confidence'] < .6 and (record['risk_score'] is not None or record['top_windows']):
        raise ValueError('Low confidence must remain unknown')
    if record['data_type'] == 'estimated' and record['total_reported_cases'] is not None:
        raise ValueError('Downscaled values are not observed neighbourhood cases')
    count(record['total_reported_cases'])
    if len(record['time_bands']) not in (0, 12):
        raise ValueError('Export requires twelve bands or explicitly absent observations')
    keys = set()
    for band in record['time_bands']:
        key = (band['day_type'], band['time_band'])
        if key in keys or key[0] not in ('weekday', 'weekend') or key[1] not in BANDS:
            raise ValueError('Invalid or duplicate time band')
        keys.add(key)
        if band['level'] != bucket(band['risk_score']):
            raise ValueError('Invalid band risk level')
        if record['confidence'] < .6 and band['risk_score'] is not None:
            raise ValueError('Low confidence time band must stay unknown')
