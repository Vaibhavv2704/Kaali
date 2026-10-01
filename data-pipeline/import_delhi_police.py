"""Reproduce reviewed Delhi Police aggregate counts; never neighbourhood labels."""
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://delhipolice.gov.in/Images/HTMLfiles/CAW(10).pdf'
REVIEWED_SHA256 = '52471388a8d93a7e96ed2c4998c398e20a5922ae5a604f48d74c20152e32194f'
CATEGORIES = [
    ('rape', r'RAPE\(376 IPC\)'),
    ('assault-to-modesty', r'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY \(354 IPC\)'),
    ('insult-to-modesty', r'INSULT TO THE MODESTY OF WOMEN \(509 IPC\)'),
    ('kidnapping', r'KIDNAPPING OF WOMEN'),
    ('abduction', r'ABDUCTION OF WOMEN'),
    ('cruelty-498a-406', r'498-A/406 IPC \(CRUELTY BY HUSBAND AND IN LAWS\)'),
    ('dowry-death', r'DOWRY DEATH \(304B\)'),
    ('dowry-prohibition-act', r'DOWRY PROHIBITION ACT'),
]


def parse_table(text):
    text = ' '.join(text.split())
    if '* UPTO 15TH JULY' not in text or 'CRIME HEAD 2012 2013 2014 2015 2016' not in text:
        raise ValueError('Reviewed period headers missing')
    periods = [(year, 12, 31) for year in range(2012, 2022)] + [(2021, 7, 15), (2022, 7, 15)]
    records = []
    for category, label in CATEGORIES:
        matches = list(re.finditer(label + r'\s+((?:\d+\s+){11}\d+)', text))
        if len(matches) != 1:
            raise ValueError(f'Expected one 12-column row: {category}')
        counts = [int(value) for value in matches[0].group(1).split()]
        for (year, month, day), count in zip(periods, counts, strict=True):
            start, end = date(year, 1, 1), date(year, month, day)
            records.append({
                'category': category, 'sourceCategory': re.sub(r'\\([()])', r'\1', label),
                'periodStart': start.isoformat(), 'periodEnd': end.isoformat(),
                'periodDays': (end-start).days+1, 'partialYear': month != 12,
                'count': count, 'unit': 'registered cases',
                'geography': 'Delhi Police coverage', 'geographyLevel': 'city-wide police coverage',
                'estimated': False, 'sample': False, 'sourcePage': 1,
                'sourceUrl': SOURCE, 'trainingEligible': False,
                'timeBand': None, 'neighbourhoodId': None,
            })
    return records


def main():
    source = ROOT/'raw/delhi-police/caw-2013-2022.pdf'
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != REVIEWED_SHA256:
        raise ValueError('Source changed; review table layout and periods before importing')
    reader = PdfReader(source)
    if len(reader.pages) != 1:
        raise ValueError('Unexpected page count')
    records = parse_table(reader.pages[0].extract_text())
    result = {
        'sourceUrl': SOURCE, 'sourceSha256': digest, 'reviewedAt': '2026-10-01',
        'limitations': [
            'Download-page title differs from the table: full years 2012–2021, plus Jan 1–July 15 of 2021 and 2022.',
            'Do not add partial and complete periods or overlapping general-crime tables.',
            'No district/station/locality breakdown, female exposure, or time-of-day observations.',
            'Original legal categories retained; 498-A/406 not silently equated with 498-A alone.',
        ],
        'records': records,
    }
    output = ROOT/'raw/normalized/delhi-police-caw.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Staged {len(records)} sourced aggregate rows at {output}')


if __name__ == '__main__':
    main()
