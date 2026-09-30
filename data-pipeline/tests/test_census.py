import sys
import unittest
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from import_census import normalize


def fixture():
    base={'State':'07','District':'095','Subdistt':'00001','Town/Village':'000001','Ward':'0001',
          'Name':'Synthetic fixture','Level':'WARD','TRU':'Urban','TOT_P':10,'TOT_M':4,'TOT_F':6}
    return [base,base|{'Level':'TOWN','Ward':'0000'},
            base|{'Level':'DISTRICT','TRU':'Total','Subdistt':'00000','Town/Village':'000000','Ward':'0000'}]


class CensusTests(unittest.TestCase):
    def test_selects_ward_rows_without_counting_parents_twice(self):
        result=normalize(fixture())
        self.assertEqual(len(result['records']),1)
        self.assertEqual(result['records'][0]['femalePopulation'],6)
        self.assertFalse(result['records'][0]['boundaryMatched'])

    def test_rejects_duplicates_and_inconsistent_population(self):
        rows=fixture()
        with self.assertRaises(ValueError):normalize(rows+[deepcopy(rows[0])])
        rows[0]['TOT_F']=5
        with self.assertRaises(ValueError):normalize(rows)

    def test_rejects_missing_ward_and_wrong_district(self):
        with self.assertRaises(ValueError):normalize(fixture()[1:])
        rows=fixture();rows[0]['District']='094'
        with self.assertRaises(ValueError):normalize(rows)


if __name__=='__main__':unittest.main()
