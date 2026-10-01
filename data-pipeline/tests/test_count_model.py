"""Synthetic fixtures test logic only; never used as training observations."""
import sys
import json
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from count_model import (count, assert_split, downscale, scores, bucket,
                         smooth_history, night_context, time_values, normalise_head, validate_export, evidence_confidence)
from train_count_model import ROOT, observations, examples, independent_report_check, bootstrap_forecast_intervals, prepare_features


class CountModelTests(unittest.TestCase):
    def test_blank_is_missing_and_zero_is_observed(self):
        self.assertIsNone(count(''))
        self.assertIsNone(count(None))
        self.assertEqual(count(0), 0)
        for invalid in (-1, .3, float('inf')):
            with self.assertRaises(ValueError): count(invalid)

    def test_explicit_source_totals_reconcile(self):
        config = json.loads((ROOT/'config/counts-v1.json').read_text())
        rows, checks, mapping = observations(config)
        self.assertEqual(len(rows), 38)
        self.assertTrue(all(c['difference'] == 0 for c in checks))
        self.assertEqual([c['workbook_state_total'] for c in checks if c['state'] == 'Delhi'], [14247, 13396])
        self.assertEqual(next(r['count'] for r in rows if r['unit'] == 'Rohini' and r['year'] == 2024), 883)
        self.assertFalse(any('Metro' in r['unit_id'] for r in rows))
        self.assertTrue(all(not r['boundary_verified'] for r in mapping))
        independent_report_check(checks)
        self.assertTrue(all(c['independent_difference'] == 0 for c in checks))

    def test_category_normalisation_is_explicit(self):
        self.assertEqual(normalise_head('Sec.376 IPC'), normalise_head('Sec 64-68,70-71 BNS'))
        self.assertIsNone(normalise_head('unreviewed legal head'))

    def test_conservation_and_cross_border_rejection(self):
        zones = [{'id': str(i), 'district_id': 'fixture', 'crosswalk_verified': True,
                  'density': i+1, 'road_density': 3-i, 'built_up': .4} for i in range(3)]
        result = downscale(101, zones)
        self.assertAlmostEqual(sum(r['estimated_cases'] for r in result), 101, places=12)
        self.assertTrue(all(r['total_reported_cases'] is None for r in result))
        zones[-1]['district_id'] = 'other'
        with self.assertRaises(ValueError): downscale(101, zones)

    def test_missing_context_rejects_allocation(self):
        with self.assertRaises(ValueError): downscale(100, [{'id': 'fixture', 'district_id': 'fixture',
                                                           'crosswalk_verified': True, 'density': None}])
        self.assertIsNone(night_context({}, inventory_complete=False))

    def test_percentile_unknown_handling_and_buckets(self):
        self.assertEqual(scores([0, 50, 100, None], [1, .1, 1, 1]), [0, None, 100, None])
        self.assertEqual(scores([7], [1]), [None])
        self.assertEqual([bucket(v) for v in [None, 0, 25, 50, 75, 100]],
                         ['unknown', 'Low', 'Moderate', 'High', 'Very High', 'Very High'])

    def test_completeness_drops_with_missing_inputs_and_few_sources(self):
        full = dict(history=True, context=True, geometry=True, time_observed=True, source_count=3)
        self.assertAlmostEqual(evidence_confidence(**full), 1)
        for field in ('history', 'context', 'geometry', 'time_observed'):
            self.assertLess(evidence_confidence(**{**full, field: False}), 1)
        self.assertLess(evidence_confidence(**{**full, 'source_count': 1}), 1)

    def test_smoothing_uses_only_supplied_adjacency(self):
        self.assertEqual(smooth_history({'a': 10, 'b': 30}, {'a': ['b']})['a'], 14)
        self.assertIsNone(smooth_history({'a': 10}, {'a': ['unknown']})['a'])

    def test_no_area_or_future_leakage(self):
        train = pd.DataFrame([{'unit_id': 'a', 'year': 2022, 'feature_year': 2021}])
        test = pd.DataFrame([{'unit_id': 'a', 'year': 2024, 'feature_year': 2022}])
        with self.assertRaises(ValueError): assert_split(train, test)
        assert_split(train, test, spatial=False)
        test.loc[0, 'feature_year'] = 2024
        with self.assertRaises(ValueError): assert_split(train, test, spatial=False)

    def test_history_does_not_fill_missing_years(self):
        result = examples([{'unit_id': 'fixture', 'year': y, 'count': v} for y, v in [(2022, 10), (2024, 20)]])
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0].feature_year, 2022)

    def test_modern_context_cannot_leak_into_historical_validation(self):
        frame = pd.DataFrame([{'unit_id': 'fixture', 'year': 2024, 'feature_year': 2022, 'history_count': 10}])
        with tempfile.TemporaryDirectory() as folder, patch('train_count_model.INTERIM', Path(folder)):
            path = Path(folder)/'night-context.json'
            item = {'unit_id': 'fixture', 'year': 2026, 'night_context': .8,
                    'inventory_complete': True, 'boundary_verified': True, 'source_list': ['synthetic fixture']}
            path.write_text(json.dumps([item]))
            self.assertTrue(prepare_features(frame)[0].night_context.isna().all())
            item['year'] = 2022
            path.write_text(json.dumps([item]))
            self.assertEqual(prepare_features(frame)[0].iloc[0].night_context, .8)

    def test_time_factors_are_separate_assumptions(self):
        result = time_values(100, 1, {'weekday': [1]*6, 'weekend': [1]*6})
        self.assertEqual(len(result), 12)
        self.assertTrue(all(r['time_data_type'] == 'assumed' for r in result))
        self.assertEqual(time_values(100, None, {}), [])

    def test_bootstrap_is_reproducible_and_exploratory(self):
        a = bootstrap_forecast_intervals([10, 30, 80], [20, 20, 20])
        self.assertEqual(a, bootstrap_forecast_intervals([10, 30, 80], [20, 20, 20]))
        self.assertEqual(a['status'], 'exploratory_not_calibrated')

    def test_export_never_claims_low_confidence_is_low_risk(self):
        r = {'id': 'fixture', 'year': 2024, 'source_list': ['fixture'], 'data_type': 'estimated',
             'confidence': .2, 'risk_score': None, 'level': 'unknown', 'total_reported_cases': None,
             'top_windows': [], 'time_bands': []}
        validate_export(r)
        r.update(risk_score=0, level='Low')
        with self.assertRaises(ValueError): validate_export(r)


if __name__ == '__main__':
    unittest.main()
