"""Synthetic article fixtures only; no real narrative or identities."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from news_extract import extract_reviewed, validate_review


class NewsExtractionTests(unittest.TestCase):
    def setUp(self):
        self.review = json.loads((ROOT / 'config/news-delhi-review.json').read_text())
        self.review['access'].pop('articleSelector', None)

    def test_unknown_or_personal_fields_rejected(self):
        self.review['facts'][0]['victim'] = 'synthetic sentinel'
        with self.assertRaises(ValueError):
            validate_review(self.review)

    def test_duplicate_category_year_rejected(self):
        self.review['facts'].append(deepcopy(self.review['facts'][0]))
        with self.assertRaises(ValueError):
            validate_review(self.review)

    def test_partial_year_and_missing_body_rejected(self):
        self.review['facts'][0]['year'] = 2026
        with self.assertRaises(ValueError):
            validate_review(self.review)
        self.review['facts'][0]['year'] = 2023
        with self.assertRaises(ValueError):
            extract_reviewed('<html><body></body></html>', self.review)

    def test_extract_keeps_no_body_and_no_model_label(self):
        self.review['facts'] = [{'category': 'rape', 'year': 2023, 'count': 2141}]
        html = '<html><body><article><p>Synthetic test report only: 2,141 rape cases were reported in 2023. This paragraph exists only to exercise the extractor and is never a real observation. The fixture contains no names or addresses. It checks that source prose stays in memory and that only deliberately reviewed structured fields are returned to the caller.</p></article></body></html>'
        result = extract_reviewed(html, self.review)
        self.assertEqual(result['facts'], self.review['facts'])
        self.assertFalse(result['eligibleForTraining'])
        self.assertIsNone(result['timeBand'])
        self.assertNotIn('Synthetic test report', json.dumps(result))

    def test_changed_count_requires_review(self):
        self.review['facts'] = [{'category': 'rape', 'year': 2023, 'count': 99}]
        with self.assertRaises(ValueError):
            extract_reviewed('<article><p>Synthetic report of rape in 2023. No reviewed count is present in this fixture paragraph.</p></article>', self.review)


if __name__ == '__main__':
    unittest.main()
