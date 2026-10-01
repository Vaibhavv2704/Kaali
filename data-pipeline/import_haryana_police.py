"""Normalize visually reviewed cells from an immutable scanned government report."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def normalize(review):
    if review['districts'] != ['Faridabad', 'Gurugram']:
        raise ValueError('Reviewed district column order changed')
    records, seen = [], set()
    for row in review['rows']:
        if row['category'] in seen or row['page'] not in (16, 17, 18):
            raise ValueError('Duplicate category or unreviewed page')
        seen.add(row['category'])
        if len(row['counts']) != 2 or any(type(n) is not int or n < 0 for n in row['counts']):
            raise ValueError('Expected two nonnegative integer counts')
        for district, count in zip(review['districts'], row['counts'], strict=True):
            records.append({
                'sourceGeography': district, 'geographyLevel': 'police district',
                'boundaryVintage': '2022; no current neighbourhood crosswalk',
                'category': row['category'], 'sourceCategory': row['sourceLabel'],
                'legalSection': row['legalSection'], 'count': count, 'unit': 'registered cases',
                'periodStart': '2022-01-01', 'periodEnd': '2022-12-31', 'periodDays': 365,
                'sourcePage': row['page'], 'sourceUrl': review['sourceUrl'],
                'estimated': False, 'sample': False, 'trainingEligible': False,
                'neighbourhoodId': None, 'timeBand': None,
            })
    if len(records) != 8:
        raise ValueError('Expected four reviewed categories for two districts')
    return records


def main():
    review = json.loads((ROOT/'config/haryana-2022-reviewed.json').read_text(encoding='utf-8'))
    source = ROOT/'raw'/review['sourcePath']
    if hashlib.sha256(source.read_bytes()).hexdigest() != review['sourceSha256']:
        raise ValueError('Source changed; scanned cells require fresh review')
    result = {k: review[k] for k in ['sourceUrl', 'sourceSha256', 'reviewedAt', 'extraction']}
    result['limitations'] = ['Four selected categories, not total crime against women.',
                            'District geography is not city limits or individual neighbourhoods.',
                            'No female exposure, time-of-day observations or prediction labels.']
    result['records'] = normalize(review)
    output = ROOT/'raw/normalized/haryana-ncr-districts-2022.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Staged {len(result["records"])} reviewed district/category rows at {output}')


if __name__ == '__main__':
    main()
