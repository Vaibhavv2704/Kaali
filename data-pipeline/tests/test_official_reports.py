import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from import_haryana_police import normalize
from import_parliament import parse_table


class OfficialReportTests(unittest.TestCase):
    def test_women_column_not_sum_of_populations(self):
        text = '4220 2026 As reported by Delhi Police elderly person '
        text += '2023 1,234 200 100 2024 2,345 300 200 2025 3,456 400 300'
        rows = parse_table(text)
        self.assertEqual([r['count'] for r in rows], [1234, 2345, 3456])
        self.assertEqual(rows[1]['periodDays'], 366)
        self.assertTrue(all(r['trainingEligible'] is False for r in rows))
        with self.assertRaises(ValueError):
            parse_table(text + ' 2025 3,456 400 300')

    def test_transcribed_columns_keep_district_identity(self):
        review = {'districts': ['Faridabad', 'Gurugram'], 'sourceUrl': 'https://example.org/fixture.pdf',
                  'rows': [{'category': str(i), 'page': 16, 'sourceLabel': 'synthetic',
                            'legalSection': 'fixture', 'counts': [1, 2]} for i in range(4)]}
        rows = normalize(review)
        self.assertEqual([(r['sourceGeography'], r['count']) for r in rows[:2]],
                         [('Faridabad', 1), ('Gurugram', 2)])
        review['districts'].reverse()
        with self.assertRaises(ValueError):
            normalize(review)


if __name__ == '__main__':
    unittest.main()
