import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from public_download import allowed, download, validate_payload
from import_delhi_police import CATEGORIES, parse_table
from import_up_police import parse_districts


class AcquisitionTests(unittest.TestCase):
    def test_district_categories_do_not_include_general_crime_total(self):
        text = 'TABLE - 8 DURING 2012 WOMEN & GIRLS '
        text += 'GHAZIABAD 1 2 3 4 5 6 7 8 9 10 55 '
        text += 'G.B. NAGAR 1 2 3 4 5 6 7 8 9 10 55'
        rows = parse_districts(text)
        self.assertEqual([row['count'] for row in rows], [2, 5, 6, 2, 5, 6])
        self.assertTrue(all(row['periodDays'] == 366 for row in rows))
        with self.assertRaises(ValueError):
            parse_districts(text.replace('10 55', '10 56'))

    def test_rejects_error_page_disguised_as_data(self):
        for suffix in ['.pdf', '.xlsx', '.csv', '.json']:
            with self.assertRaises(ValueError):
                validate_payload(b'<html>Access denied</html>', suffix)

    def test_robots_denial_stops_before_download(self):
        session = Mock()
        session.get.return_value = Mock(status_code=200, text='User-agent: *\nDisallow: /')
        with self.assertRaisesRegex(ValueError, 'disallows'):
            allowed(session, 'https://example.org/report.pdf')
        self.assertEqual(session.get.call_count, 1)

    def test_raw_path_cannot_escape(self):
        with patch('public_download.requests.Session') as session:
            with self.assertRaises(ValueError):
                download({'path': '../../outside.pdf', 'url': 'https://example.org/x'})
            session.assert_not_called()

    def test_partial_years_are_separate_and_not_training_labels(self):
        # Synthetic counts; this fixture is not public crime data.
        text = '* UPTO 15TH JULY CRIME HEAD 2012 2013 2014 2015 2016 '
        for _, label in CATEGORIES:
            text += label.replace('\\', '') + ' ' + ' '.join(['1']*12) + ' '
        rows = parse_table(text)
        self.assertEqual(len(rows), 96)
        full, partial = rows[9], rows[10]
        self.assertEqual(full['periodEnd'], '2021-12-31')
        self.assertEqual(partial['periodEnd'], '2021-07-15')
        self.assertEqual(partial['periodDays'], 196)
        self.assertFalse(partial['trainingEligible'])
        self.assertIsNone(partial['neighbourhoodId'])
        with self.assertRaises(ValueError):
            parse_table(text.replace('* UPTO 15TH JULY', ''))


if __name__ == '__main__':
    unittest.main()
