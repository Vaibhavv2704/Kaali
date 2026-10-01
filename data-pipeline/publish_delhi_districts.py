"""Publish the attributed Delhi factual extract; never publish geography or scores."""
import json
from pathlib import Path
from extract_delhi_districts import ROOT, checked_file, extract, official_values, reconcile, RECEIPT, FORMULAS


def main():
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    sources = {s['id']: s for s in receipt['sources']}
    records, _ = extract(checked_file(sources['idp-2024']), 2024)
    official, total = official_values(checked_file(sources['ncrb-2024-volume-1']))
    data = {'schemaVersion': 1, 'regionId': 'delhi-ncr', 'cityId': 'delhi', 'year': 2024,
            'retrievedAt': receipt['retrievalDate'], 'sourceUrl': sources['idp-2024']['resourceUrl'],
            'downloadUrl': sources['idp-2024']['downloadUrl'], 'sha256': sources['idp-2024']['sha256'],
            'officialUrl': sources['ncrb-2024-volume-1']['downloadUrl'],
            'licence': 'India Data Portal: No License Provided. NCRB report mirror: Other (Public Domain).',
            'formulas': FORMULAS, 'validation': reconcile(records, official, total), 'records': records}
    output = ROOT.parent/'public/data/delhi-district-crime.json'
    output.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    print(f'Published {len(records)} historical registration-circle records; no map scores.')


if __name__ == '__main__':
    main()
