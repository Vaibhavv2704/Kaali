"""Synthetic software fixtures only; no real predictions or metrics generated."""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from predict import build_records,verify_artifacts
from train import NUM


def fixture():
    frame=pd.DataFrame([dict.fromkeys(NUM,1)|{'neighbourhood_id':'fixture','city_id':'city',
        'jurisdiction':'fixture','land_use':'fixture','day_type':day,'time_band':band}
        for day in ['weekday','weekend'] for band in range(6)])
    geo={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'id':'fixture',
        'cityId':'city','name':'Synthetic fixture','femalePopulation':1000,'boundaryStatus':'verified'},
        'geometry':{'type':'Polygon','coordinates':[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}}]}
    region={'id':'fixture','cities':[{'id':'city'}]}
    review=dict.fromkeys(['metricsReviewed','privacyReviewed','licencesReviewed','boundariesReviewed','exposureReviewed'],True)
    review.update(rateScale=10,periodDays=365,year=2025,confidence='low',sources=[{'label':'Test only','url':'https://example.invalid/fixture'}])
    return frame,geo,region,review


class PredictionTests(unittest.TestCase):
    def test_valid_mapping_preserves_input_and_unknown_incidents(self):
        frame,geo,region,review=fixture();original=frame.copy(deep=True)
        rows=build_records(frame,np.arange(12),geo,region,review)
        self.assertEqual(len(rows[0]['scores']['weekday:all']),6)
        self.assertEqual(rows[0]['scores']['weekday:all'][0],0)
        self.assertIsNone(rows[0]['incidents']);pd.testing.assert_frame_equal(frame,original)

    def test_invalid_rates_are_not_clipped(self):
        frame,geo,region,review=fixture()
        for value in [np.nan,np.inf,-1]:
            rates=np.ones(12);rates[0]=value
            with self.assertRaises(ValueError):build_records(frame,rates,geo,region,review)
        with self.assertRaises(ValueError):build_records(frame,np.ones(11),geo,region,review)

    def test_missing_bands_extra_ids_and_cross_city_rows_rejected(self):
        frame,geo,region,review=fixture()
        for bad in [frame.iloc[:-1],pd.concat([frame,frame.iloc[[0]]]),frame.assign(neighbourhood_id='unknown'),frame.assign(city_id='other')]:
            with self.assertRaises(ValueError):build_records(bad,np.ones(len(bad)),geo,region,review)
        duplicate=copy.deepcopy(geo);duplicate['features']*=2
        with self.assertRaises(ValueError):build_records(frame,np.ones(12),duplicate,region,review)

    def test_review_and_boundary_requirements(self):
        frame,geo,region,review=fixture()
        for key,value in [('rateScale',np.inf),('periodDays',0),('confidence','certain'),('metricsReviewed',False)]:
            with self.assertRaises(ValueError):build_records(frame,np.ones(12),geo,region,review|{key:value})
        geo['features'][0]['properties']['boundaryStatus']='sample'
        with self.assertRaises(ValueError):build_records(frame,np.ones(12),geo,region,review)

    def test_artifact_bytes_must_match_review(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'model';path.write_bytes(b'test-only')
            with self.assertRaises(ValueError):verify_artifacts({}, {'model':path})


if __name__=='__main__':unittest.main()
