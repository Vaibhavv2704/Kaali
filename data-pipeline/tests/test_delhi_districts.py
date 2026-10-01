"""Synthetic parsing tests plus optional checks against downloaded research files."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from extract_delhi_districts import (ROOT, GEOGRAPHIC, SPECIAL, PDF_COLUMNS, FORMULAS,
    checked_file, complete_sum, extract, official_values, parse_count, reconcile)


class DelhiDistrictTests(unittest.TestCase):
    def test_blank_is_missing_and_zero_is_observed(self):
        self.assertIsNone(parse_count(' '))
        self.assertIsNone(parse_count(None))
        self.assertEqual(parse_count('0.0'), 0)
        self.assertEqual(parse_count('63.0'), 63)
        for invalid in ['-1', '2.5', 'NaN', 'Infinity']:
            with self.assertRaises(ValueError):
                parse_count(invalid)

    def test_partial_subtotal_is_unavailable(self):
        self.assertIsNone(complete_sum({'a': 2, 'b': None}, ['a', 'b']))
        self.assertEqual(complete_sum({'a': 2, 'b': 0}, ['a', 'b']), 2)
        with self.assertRaises(ValueError):
            complete_sum({'a': 2}, ['a', 'a'])

    def test_only_leaf_fields_in_grand_subtotal(self):
        self.assertEqual(set(FORMULAS['calculated_recorded_heads_subtotal']), set(PDF_COLUMNS))
        self.assertFalse(any(f.startswith('calculated_') for f in FORMULAS['calculated_recorded_heads_subtotal']))
        self.assertNotIn('kidnap_abduct_inducing_women_compel_marriage', FORMULAS['calculated_kidnapping_abduction_subtotal'])
        self.assertEqual(len(FORMULAS['calculated_pocso_girl_child_subtotal']), 5)

    def fixture(self, path):
        with path.open('w', newline='', encoding='utf-8') as stream:
            keys = ['id', 'year', 'state_name', 'state_code', 'district_name', 'district_code', 'registration_circles']+list(PDF_COLUMNS)
            writer = csv.DictWriter(stream, fieldnames=keys)
            writer.writeheader()
            for i, unit in enumerate(sorted(GEOGRAPHIC | SPECIAL)):
                row = dict.fromkeys(keys, '0')
                row.update(id=str(i), year='2024', state_name='Delhi', district_name='Synthetic broader district', registration_circles=unit)
                row['rape_women'] = '' if unit == 'Rohini' else '1'
                writer.writerow(row)

    def test_reporting_circles_not_administrative_grouping(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'fixture.csv'
            self.fixture(path)
            records, _ = extract(path, 2024)
            self.assertEqual(len(records), 23)
            self.assertEqual(sum(r['unit_type'] == 'special_unit' for r in records), 8)
            rohini = next(r for r in records if r['district_name'] == 'Rohini')
            self.assertEqual(rohini['missing_fields'], ['rape_women'])
            self.assertIsNone(rohini['calculated']['calculated_recorded_heads_subtotal'])
            self.assertEqual(rohini['source_administrative_district_name'], 'Synthetic broader district')
            text = path.read_text(encoding='utf-8')
            path.write_text(text+text.splitlines()[1]+'\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                extract(path, 2024)

    def test_source_hash_required(self):
        with self.assertRaises(ValueError):
            checked_file({'localPath': 'extract_delhi_districts.py', 'sha256': '0'*64, 'bytes': 1})

    @unittest.skipUnless((ROOT/'raw/ncrb/vol1-crimeinindia2024.pdf').exists(), 'Original research files not downloaded')
    def test_original_files_and_all_category_reconciliation(self):
        sources = {s['id']: s for s in json.loads((ROOT/'sources/delhi-district-2024-receipt.json').read_text())['sources']}
        records, fields = extract(checked_file(sources['idp-2024']), 2024)
        self.assertEqual(len(fields), 49)
        official, total = official_values(checked_file(sources['ncrb-2024-volume-1']))
        validation = reconcile(records, official, total)
        self.assertEqual(total, 13396)
        self.assertEqual(validation['mirrorCombinedSubtotal'], 13295)
        self.assertEqual(list(validation['discrepancies']), ['stalking_women'])
        self.assertEqual(validation['ncrbMinusMirror'], 101)
        rohini = next(r for r in records if r['district_name'] == 'Rohini')
        self.assertEqual(rohini['calculated']['calculated_recorded_heads_subtotal'], 879)
        self.assertEqual(rohini['calculated']['calculated_pocso_girl_child_subtotal'], 98)
        self.assertFalse(rohini['trainingEligible'])
        older, _ = extract(checked_file(sources['idp-candidate-2017-2022']), 2022, False)
        self.assertTrue(all(r['counts']['kidnapping_for_ransom'] is None for r in older))


if __name__ == '__main__':
    unittest.main()
