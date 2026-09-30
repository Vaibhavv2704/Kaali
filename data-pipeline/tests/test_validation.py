"""Synthetic in-memory fixtures only; never exported as observations or metrics."""
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from geography import allocate
from train import NUM, validate_frame


def fixture():
    rows = []
    for zone in range(5):
        for period in range(20):
            start = datetime(2020, 1, 1) + timedelta(days=period * 7)
            rows.append(dict.fromkeys(NUM, 1) | {
                'neighbourhood_id': f'test-{zone}', 'city_id': f'test-city-{zone % 2}',
                'jurisdiction': 'test-only', 'land_use': 'test-only', 'day_type': 'weekday',
                'period_start': start, 'period_end': start + timedelta(days=6),
                'feature_cutoff': start - timedelta(days=1), 'count': 2,
                'female_population': 1000, 'period_days': 5, 'estimated': False,
                'provenance': 'observed', 'source_url': 'https://example.invalid/test-only',
                'observation_coverage':'complete','boundary_status':'verified',
                'coverage_source_url':'https://example.invalid/coverage',
                'exposure_source_url':'https://example.invalid/exposure',
            })
    return pd.DataFrame(rows)


class ValidationTests(unittest.TestCase):
    def test_valid_shape_and_no_mutation(self):
        frame = fixture()
        original = frame.copy(deep=True)
        self.assertEqual(len(validate_frame(frame)), 100)
        pd.testing.assert_frame_equal(frame, original)

    def test_rejects_unknown_or_invalid_evidence(self):
        for col, value in [('estimated', None), ('estimated', True), ('provenance', 'sample'),
                           ('count', np.nan), ('count', np.inf), ('count', 0.5),
                           ('female_population', 0), ('period_days', np.inf),
                           ('source_url', None), ('source_url', 'https://'),
                           ('city_id', None), ('time_band', 6)]:
            with self.subTest(col=col, value=value):
                frame = fixture().astype({col: object})
                frame.loc[0, col] = value
                with self.assertRaises(ValueError):
                    validate_frame(frame)

    def test_rejects_leakage_reversed_period_and_duplicates(self):
        for col, value in [('feature_cutoff', '2021-01-01'), ('period_end', '2019-01-01')]:
            frame = fixture()
            frame.loc[0, col] = pd.Timestamp(value)
            with self.assertRaises(ValueError):
                validate_frame(frame)
        frame = fixture()
        with self.assertRaises(ValueError):
            validate_frame(pd.concat([frame, frame.iloc[[0]]], ignore_index=True))

    def test_allocation_preserves_total_and_rejects_infinity(self):
        cells = pd.DataFrame({'area': [1.0, 2.0], 'female_population': [0, 0], 'road_length': [2, 1]})
        self.assertAlmostEqual(float(allocate(17, cells).sum()), 17)
        for count in [np.nan, np.inf, -1]:
            with self.assertRaises(ValueError):
                allocate(count, cells)
        cells.loc[0, 'area'] = np.inf
        with self.assertRaises(ValueError):
            allocate(17, cells)

    def test_rejects_unobserved_cells_and_wrong_exposure(self):
        for col,value in [('observation_coverage','unknown'),('boundary_status','sample'),
                          ('coverage_source_url',None),('exposure_source_url',None),
                          ('period_days',7),('lighting',1.5),('distance_police',-1),
                          ('poi_density',np.inf)]:
            with self.subTest(col=col):
                frame=fixture().astype({col:object});frame.loc[0,col]=value
                with self.assertRaises(ValueError):validate_frame(frame)

    def test_rejects_overlapping_periods_with_different_start_dates(self):
        frame=fixture()
        frame.loc[1,'period_start']=frame.loc[0,'period_start']+timedelta(days=1)
        frame.loc[1,'feature_cutoff']=frame.loc[1,'period_start']-timedelta(days=1)
        dates=pd.date_range(frame.loc[1,'period_start'],frame.loc[1,'period_end'])
        frame.loc[1,'period_days']=sum(d.dayofweek<5 for d in dates)
        with self.assertRaisesRegex(ValueError,'Overlapping'):validate_frame(frame)


if __name__ == '__main__':
    unittest.main()
