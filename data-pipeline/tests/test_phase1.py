"""Synthetic input integrity and environmental denominator regressions."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from phase1 import read_verified
from environment import lighting_fraction


class Phase1Tests(unittest.TestCase):
    def test_missing_changed_and_unreviewed_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'raw').mkdir()
            entry={'id':'test-only','path':'raw/input','sha256':hashlib.sha256(b'test').hexdigest()}
            self.assertIsNone(read_verified(root,entry))
            (root/'raw/input').write_bytes(b'test')
            self.assertEqual(read_verified(root,entry),root/'raw/input')
            with self.assertRaises(ValueError):read_verified(root,entry|{'sha256':None})
            (root/'raw/input').write_bytes(b'changed')
            with self.assertRaises(ValueError):read_verified(root,entry)
            with self.assertRaises(ValueError):read_verified(root,entry|{'path':'../outside'})

    def test_lit_only_snapshot_is_not_lighting_coverage(self):
        self.assertIsNone(lighting_fraction(pd.Series([10]),pd.Series(['yes'])))
        self.assertEqual(lighting_fraction(pd.Series([10,10]),pd.Series(['yes','no']),True),.5)
        self.assertIsNone(lighting_fraction(pd.Series([10,10]),pd.Series(['yes',None]),True))


if __name__=='__main__':unittest.main()
