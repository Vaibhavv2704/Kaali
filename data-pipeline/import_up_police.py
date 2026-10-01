"""Extract reviewed historical NCR district categories from UP SCRB Table 8."""
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SHA256 = 'fcb05ab8c92b363874f870ff45f845eba5a927eb317052f93545d2b4d622949b'
URL = 'https://uppolice.gov.in/writereaddata/uploaded-content/Web_Page/21_11_2013_12_23_50_Crime%20in%20UP-2012.pdf'


def parse_districts(text):
    text = ' '.join(text.split())
    if not all(token in text for token in ['TABLE - 8', 'DURING 2012', 'WOMEN & GIRLS']):
        raise ValueError('Reviewed table headers missing')
    records = []
    for district in ['GHAZIABAD', 'G.B. NAGAR']:
        matches = list(re.finditer(re.escape(district)+r'\s+((?:\d+\s+){10}\d+)(?=\s|$)', text))
        if len(matches) != 1:
            raise ValueError('Missing or duplicate district row')
        counts = [int(n) for n in matches[0].group(1).split()]
        if sum(counts[:10]) != counts[10]:
            raise ValueError('District row does not reconcile with source total')
        # Table 8 has other crime heads. Its total is NOT a crimes-against-women total.
        for category, index in [('dowry-death', 1), ('rape', 4), ('kidnapping-abduction-women-girls', 5)]:
            records.append({
                'sourceGeography': district, 'geographyLevel': 'police district',
                'boundaryVintage': '2012; not crosswalked to present jurisdictions',
                'category': category, 'count': counts[index], 'unit': 'registered cases',
                'periodStart': '2012-01-01', 'periodEnd': '2012-12-31', 'periodDays': 366,
                'sourceUrl': URL, 'sourcePage': 25, 'printedPage': 18, 'sourceTable': '8',
                'estimated': False, 'sample': False, 'trainingEligible': False,
                'neighbourhoodId': None, 'timeBand': None,
            })
    return records


def main():
    path = ROOT/'raw/up-police/crime-in-up-2012.pdf'
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError('Changed source requires review')
    records = parse_districts(PdfReader(path).pages[24].extract_text())
    output = ROOT/'raw/normalized/up-ncr-districts-2012.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        'sourceSha256': SHA256, 'reviewedAt': '2026-10-01',
        'limitations': ['Historical district counts, not current locality observations.',
                        'Three selected categories only; no total crime-against-women count inferred.',
                        'Do not allocate G.B. Nagar totals separately to Noida and Greater Noida.',
                        'No female exposure or time-of-day observations.'],
        'records': records,
    }, indent=2), encoding='utf-8')
    print(f'Staged {len(records)} sourced district/category rows at {output}')


if __name__ == '__main__':
    main()
