"""Synthetic article fixtures; no victim data or publication metrics."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from incident_extract import extract

class IncidentTests(unittest.TestCase):
    def setUp(self):
        self.review=json.loads((Path(__file__).resolve().parents[1]/'config/news-nehru-place-review.json').read_text())

    def test_changed_evidence_rejected(self):
        with self.assertRaises(ValueError):extract('<html><p>No relevant evidence</p></html>',self.review)

    def test_personal_fields_and_invalid_time_rejected(self):
        for field,value in [('name','test'),('timeBand',6),('status','convicted')]:
            review=json.loads(json.dumps(self.review));review['event'][field]=value
            with self.assertRaises(ValueError):extract('',review)

    def test_publication_date_never_used_as_event_date(self):
        self.review['event']['date']='2026-05-12'
        with self.assertRaises(ValueError):extract('',self.review)

if __name__=='__main__':unittest.main()
