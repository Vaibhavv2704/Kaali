"""Extract only the women column from reviewed Rajya Sabha answer 4220/2026."""
import hashlib
import json
import re
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SHA256 = '716d1c2c351a006a05878d8f815eaf47023ef164d5b3aac222b745954f2159d3'
URL = 'https://sansad.in/getFile/annex/270/AU4220_M31fhO.pdf?source=pqars'


def parse_table(text):
    text = ' '.join(text.split())
    if not all(t in text for t in ['4220', '2026', 'As reported by Delhi Police', 'elderly person']):
        raise ValueError('Missing reviewed source/table headings')
    records = []
    for year in range(2023, 2026):
        rows = re.findall(rf'\b{year}\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)', text)
        if len(rows) != 1:
            raise ValueError('Missing or duplicate annual row')
        count = int(rows[0][0].replace(',', ''))
        records.append({
            'sourceGeography': 'Delhi Police coverage', 'geographyLevel': 'city-wide police coverage',
            'category': 'Crime against women', 'count': count, 'unit': 'registered cases',
            'periodStart': f'{year}-01-01', 'periodEnd': f'{year}-12-31',
            'periodDays': 366 if year == 2024 else 365,
            'sourceUrl': URL, 'sourcePage': 1, 'estimated': False, 'sample': False,
            'trainingEligible': False, 'neighbourhoodId': None, 'timeBand': None,
        })
    return records


def main():
    source = ROOT/'raw/parliament/rs-4220-2026.pdf'
    if hashlib.sha256(source.read_bytes()).hexdigest() != SHA256:
        raise ValueError('Source changed; review required')
    result = {'sourceUrl': URL, 'sourceSha256': SHA256, 'reviewedAt': '2026-10-01',
              'limitations': ['Delhi Police annual totals; not NCRB metropolitan series or district counts.',
                              'Women, children and elderly columns may overlap; never add them.',
                              'No neighbourhood counts, exposure or time-band observations.'],
              'records': parse_table(PdfReader(source).pages[0].extract_text())}
    output = ROOT/'raw/normalized/parliament-delhi-2023-2025.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(f'Staged {len(result["records"])} sourced annual totals at {output}')


if __name__ == '__main__':
    main()
