import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from train_district_forecast import examples


class DistrictForecastTests(unittest.TestCase):
    def test_no_future_counts_in_lag_features(self):
        # Synthetic fixture, never used in training artifacts or published data.
        rows=[{'unit':'fixture','city':'fixture','year':year,'count':count,'source':'synthetic'}
              for year,count in [(2017,10),(2018,20),(2019,500),(2021,30)]]
        data=examples(rows)
        self.assertEqual(data[0]['last_count'],20)
        self.assertEqual(data[0]['past_mean'],15)
        self.assertTrue(all(r['feature_cutoff']<r['year'] for r in data))
        self.assertEqual(data[1]['horizon'],2)  # No invented missing year.

    def test_same_named_reporting_units_do_not_mix_cities(self):
        rows=[{'unit':'fixture','city':city,'year':year,'count':count,'source':'synthetic'}
              for city,count in [('a',10),('b',100)] for year in [2017,2018,2019]]
        data=examples(rows)
        self.assertEqual([r['last_count'] for r in data],[10,100])


if __name__=='__main__':unittest.main()
