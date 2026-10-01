import copy
import sys
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from prepare_locality_context import probe_metadata, corrected_population_coordinates

def metadata():
    return {'features':[{'geometry':None,'properties':{'dateRanges':[{'@id':1,'from':'2024-08-11','to':'2024-08-11'}], 'timeSets':[{'@id':h+2,'name':f'{h}:00-{h+1}:00'} for h in range(24)]}}]}

class SuppliedContextTests(unittest.TestCase):
    def test_hour_mapping_preserves_real_reporting_date(self):
        day,identity,bands=probe_metadata(metadata())
        self.assertEqual(day,date(2024,8,11));self.assertEqual(identity,1)
        self.assertEqual([bands[h+2] for h in range(24)],[h//4 for h in range(24)])
    def test_duplicate_or_missing_hours_are_not_valid_coverage(self):
        for change in ['duplicate_hour','duplicate_id','missing_hour','partial_hour']:
            data=metadata();times=data['features'][0]['properties']['timeSets']
            if change=='duplicate_hour':times[23]['name']='22:00-23:00'
            if change=='duplicate_id':times[23]['@id']=2
            if change=='missing_hour':times.pop()
            if change=='partial_hour':times[0]['name']='0:30-1:30'
            with self.assertRaises(ValueError):probe_metadata(data)
    def test_period_and_metadata_identity_must_match(self):
        for change in ['outside','span','missing_metadata']:
            data=copy.deepcopy(metadata());properties=data['features'][0]['properties']
            if change=='outside':properties['dateRanges'][0].update({'from':'2025-08-11','to':'2025-08-11'})
            if change=='span':properties['dateRanges'][0]['to']='2024-08-12'
            if change=='missing_metadata':data['features'][0]['geometry']={'type':'Point','coordinates':[77,28]}
            with self.assertRaises(ValueError):probe_metadata(data)
    def test_swapped_population_headings_are_corrected_without_mutation(self):
        row={'Longitude':'28.513960270583976','latitude':'77.30840347358063'};original=dict(row)
        self.assertEqual(corrected_population_coordinates(row),(28.513960270583976,77.30840347358063));self.assertEqual(row,original)
        with self.assertRaises(ValueError):corrected_population_coordinates({'Longitude':'77.3','latitude':'28.5'})

if __name__=='__main__':unittest.main()
