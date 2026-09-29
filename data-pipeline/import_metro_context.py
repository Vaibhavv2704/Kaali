"""Import the reviewed OpenCity NCRB transcription as historical context, never model labels."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

SHA256 = '93a7596163c46f6acf303905f6b9cbb251d7e2f7eb6a0d228db67d82f72cb162'
SOURCE = 'https://data.opencity.in/dataset/crime-in-india-2022/resource/a4496020-4d71-4533-9041-d18e3bedb911'
DOWNLOAD = SOURCE + '/download/2176f9d3-19ea-4280-9b82-e643cfb5255d.csv'


def convert(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError('Source changed: review the new file and licence before importing')
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    result = []
    for name, city in [('Delhi City', 'delhi'), ('Ghaziabad', 'ghaziabad')]:
        matches = [r for r in rows if r['Cities'] == name]
        if len(matches) != 1:
            raise ValueError('Missing or duplicate reporting geography')
        row = matches[0]
        for year in (2020, 2021, 2022):
            count = int(row[str(year)])
            if count < 0:
                raise ValueError('Negative count')
            result.append({'id': f'ncrb-{city}-{year}', 'regionId': 'delhi-ncr', 'cityId': city,
                           'reportingArea': name, 'geography': 'NCRB metropolitan reporting area',
                           'category': 'Crime against women (IPC and SLL)', 'year': year,
                           'count': count, 'periodStart': f'{year}-01-01', 'periodEnd': f'{year}-12-31',
                           'neighbourhoodId': None, 'timeBand': None, 'femalePopulation': None,
                           'normalizedRate': None, 'eligibleForTraining': False})
    return {'schemaVersion': 1, 'retrievedAt': '2026-09-30', 'sourceUrl': SOURCE,
            'downloadUrl': DOWNLOAD, 'sha256': SHA256, 'publisher': 'NCRB, transcribed by OpenCity',
            'licence': 'Other (Public Domain), as declared by OpenCity on this resource',
            'limitations': [
                'Historical annual totals, not current alerts or neighbourhood predictions.',
                'Metropolitan reporting areas do not imply current municipal or police jurisdiction boundaries.',
                'The transcription population heading does not explicitly identify female exposure. Rates are withheld until denominator review.',
                'No locality, incident time, crime-category breakdown or individual record is available in this file.',
                'Counts are not comparable safety rankings; recording practices and under-reporting differ.',
                'Other NCR cities are absent from this resource, not zero-crime areas.'
            ], 'records': result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / 'public/data/crime-context.json'
    output.write_text(json.dumps(convert(args.input), indent=2) + '\n', encoding='utf-8')
    print('Published six historical city/year context rows; no model labels or risk scores.')
