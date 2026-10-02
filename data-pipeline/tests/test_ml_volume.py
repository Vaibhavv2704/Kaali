import sys,unittest,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from train_ml_volume import influence,build_pool,ROOT
class MLVolumeTests(unittest.TestCase):
 def test_reference_interpolation_is_bounded_and_not_case_allocation(self):
  anchors=[{'id':'a','coordinates':[77.2,28.6],'volume_index':20},{'id':'b','coordinates':[77.22,28.6],'volume_index':80}]
  index,refs=influence([77.21,28.6],anchors);self.assertAlmostEqual(index,50);self.assertAlmostEqual(sum(r['weight'] for r in refs),1)
  self.assertEqual(influence([72.8,19],anchors),(None,[]));self.assertEqual(influence([77.2,28.6],[]),(None,[]))
 def test_real_pool_excludes_special_units_and_future_features(self):
  frame,checks,excluded=build_pool(json.loads((ROOT/'config/counts-v1.json').read_text()))
  self.assertEqual(len(frame),109);self.assertFalse(frame.unit_id.duplicated().any());self.assertTrue((frame.feature_year<frame.year).all())
  self.assertTrue(all(c['difference']==0 and c['independent_difference']==0 for c in checks));self.assertTrue(any(r['name']=='GRP' for r in excluded));self.assertFalse(frame.source_name.isin(['GRP','Crime Branch']).any())
 def test_saved_folds_have_no_area_leakage(self):
  report=json.loads((ROOT/'reports/ml-volume-v1/evaluation.json').read_text())
  for fold in report['folds']:
   self.assertFalse(set(fold['train'])&set(fold['test']));self.assertLess(fold['feature_year'],fold['target_year'])
  self.assertIsNone(report['temporal_ml_validation'])
if __name__=='__main__':unittest.main()
