"""Hash-checked Delhi police registration-circle extraction. No network or imputation.

Run: .venv/Scripts/python.exe data-pipeline/extract_delhi_districts.py
Original files and their public download URLs are listed in the source receipt.
"""
import argparse
import csv
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / 'sources/delhi-district-2024-receipt.json'
IDENTITY = ['id', 'year', 'state_name', 'state_code', 'district_name',
            'district_code', 'registration_circles']
GEOGRAPHIC = {'Central', 'East', 'New Delhi', 'Outer North', 'North', 'North-East',
              'North-West', 'Outer', 'Rohini', 'Dwarka', 'Shahdara', 'South',
              'South-East', 'South-West', 'West'}
SPECIAL = {'Eow', 'Igi Airport', 'Railway', 'Spuwac', 'Vigilance', 'Crime Branch',
           'Metro', 'Spl Cell'}
UNIT_ALIASES = {'Economic Offences Wing': 'Eow'}
# PDF page (one-based), offset in the Delhi row after its name. Select registered
# cases (I/IPC+BNS Total), never victims (V), rates (R), or parent totals.
PDF_COLUMNS = {
    'rape_women': (328, 7), 'rape_girls': (329, 2),
    'sexual_intercourse_employing_deceitful_means': (329, 7),
    'murder_rape_gang': (330, 2),
    'attempt_commit_rape_women': (331, 2), 'attempt_commit_rape_girls': (331, 7),
    'assault_outrage_modesty_women': (332, 7),
    'assault_women_outrage_modesty_girls': (333, 2),
    'sexual_harassment_women': (334, 2), 'sexual_harassment_girls': (334, 7),
    'assault_criminal_force_disrobe_women': (335, 7),
    'assault_criminal_force_disrobe_girls': (336, 2),
    'voyeurism_women': (337, 2), 'voyeurism_girls': (337, 7),
    'stalking_women': (338, 7), 'stalking_girls': (339, 2),
    'insult_modesty_women': (340, 2), 'insult_modesty_women_girls': (340, 7),
    'dowry_deaths': (341, 2), 'cruelty_husband_relatives': (341, 7),
    'kidnap_abduct_inducing_women_compel_marriage': (342, 7),
    'kidnap_abduct_inducing_girls_compel_marriage': (343, 2),
    'miscarriage': (343, 7), 'procuration_minor_girls': (344, 2),
    'selling_girls_prostitution': (344, 7), 'buying_girls_prostitution': (345, 2),
    'abetment_suicides_women': (345, 7), 'acid_attack': (346, 2),
    'attempt_acid_attack': (346, 7), 'kidnapping_abduction_women': (347, 7),
    'kidnapping_abduction_women_murder': (348, 2), 'kidnapping_ransom': (348, 7),
    'importation_girls_foreign_country': (348, 12), 'women_others': (349, 2),
    'dowry_prohibition': (350, 0), 'procuring_inducing_children_prostitution': (350, 6),
    'detaining_premises_where_prostitution_is_carried': (350, 9),
    'prostitution_vicinity_public_places': (351, 0),
    'seducing_soliciting_prostitution': (351, 3), 'other_itp': (351, 6),
    'protection_women_domestic_violence': (352, 0),
    'publish_transmit_sexually_explicit_mtrl': (352, 6),
    'other_women_centric_cyber_crimes': (352, 9),
    'protection_children_sexual_violence_pocso': (353, 3), 'pocso_10': (353, 6),
    'pocso_12': (354, 0), 'pocso_14_15': (354, 3), 'pocso_17_22': (354, 6),
    'indecent_representation_women': (355, 0),
}
FORMULAS = {
    'calculated_rape_subtotal': ['rape_women', 'rape_girls'],
    'calculated_attempted_rape_subtotal': ['attempt_commit_rape_women', 'attempt_commit_rape_girls'],
    'calculated_assault_outrage_modesty_subtotal': ['assault_outrage_modesty_women', 'assault_women_outrage_modesty_girls'],
    'calculated_sexual_harassment_subtotal': ['sexual_harassment_women', 'sexual_harassment_girls'],
    'calculated_assault_related_subtotal': ['assault_outrage_modesty_women', 'assault_women_outrage_modesty_girls',
        'sexual_harassment_women', 'sexual_harassment_girls', 'assault_criminal_force_disrobe_women',
        'assault_criminal_force_disrobe_girls', 'voyeurism_women', 'voyeurism_girls', 'stalking_women', 'stalking_girls'],
    'calculated_kidnapping_abduction_subtotal': ['kidnapping_abduction_women', 'kidnapping_abduction_women_murder',
        'kidnapping_ransom', 'importation_girls_foreign_country', 'women_others'],
    'calculated_compelled_marriage_subtotal': ['kidnap_abduct_inducing_women_compel_marriage',
        'kidnap_abduct_inducing_girls_compel_marriage'],
    'calculated_pocso_girl_child_subtotal': ['protection_children_sexual_violence_pocso',
        'pocso_10', 'pocso_12', 'pocso_14_15', 'pocso_17_22'],
}
FORMULAS['calculated_recorded_heads_subtotal'] = list(PDF_COLUMNS)


def parse_count(value):
    if value is None or not value.strip():
        return None
    number = Decimal(value.strip())
    if not number.is_finite() or number < 0 or number != number.to_integral_value():
        raise ValueError(f'Invalid case count: {value!r}')
    return int(number)


def complete_sum(counts, fields):
    if len(fields) != len(set(fields)):
        raise ValueError('Duplicate component would double count')
    values = [counts[f] for f in fields]
    return None if any(v is None for v in values) else sum(values)


def checked_file(source):
    path = ROOT / source['localPath']
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != source['sha256']:
        raise ValueError(f'Source changed; review required: {path}')
    if len(payload) != source['bytes']:
        raise ValueError('Source size changed')
    return path


def extract(path, year, validate_schema=True):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields = [f for f in reader.fieldnames if f not in IDENTITY]
        if validate_schema and set(fields) != set(PDF_COLUMNS):
            raise ValueError('Unreviewed category schema')
        records, seen = [], set()
        for row in reader:
            if row['state_name'].strip().casefold() != 'delhi' or parse_count(row['year']) != year:
                continue
            unit = row['registration_circles'].strip()
            canonical_unit = UNIT_ALIASES.get(unit, unit)
            if canonical_unit in seen or canonical_unit not in GEOGRAPHIC | SPECIAL:
                raise ValueError(f'Duplicate or unreviewed reporting unit: {unit}')
            seen.add(canonical_unit)
            counts = {f: parse_count(row[f]) for f in fields}
            record = {
                'district_name': unit, 'year': year,
                'unit_type': 'geographic_police_district' if canonical_unit in GEOGRAPHIC else 'special_unit',
                'source_row_id': row['id'], 'source_state_code': row['state_code'],
                'source_administrative_district_name': row['district_name'],
                'source_administrative_district_code': row['district_code'],
                'registration_circles': unit, 'counts': counts,
                'missing_fields': [f for f, value in counts.items() if value is None],
                'calculated': {name: complete_sum(counts, components) for name, components in FORMULAS.items()}
                    if validate_schema else {},
                'sample': False, 'estimated': False, 'trainingEligible': False,
                'boundary': None, 'neighbourhoodId': None,
            }
            records.append(record)
    if seen != GEOGRAPHIC | SPECIAL:
        raise ValueError('Expected 15 geographic police districts and eight special units')
    return sorted(records, key=lambda r: (r['unit_type'], r['district_name'])), fields


def official_values(path):
    from pypdf import PdfReader
    pdf = PdfReader(path)
    cache = {}
    def value(page, offset):
        if page not in cache:
            text = pdf.pages[page-1].extract_text()
            rows = re.findall(r'^32\s+Delhi\s+([^\n]+)', text, re.MULTILINE)
            if len(rows) != 1:
                raise ValueError(f'Unreviewed Delhi PDF row on page {page}')
            cache[page] = rows[0].split()
        return parse_count(cache[page][offset])
    categories = {field: value(*cell) for field, cell in PDF_COLUMNS.items()}
    total = value(327, 2)
    if total != value(355, 6) or sum(categories.values()) != total:
        raise ValueError('Official category hierarchy does not reconcile to the official total')
    return categories, total


def reconcile(records, official, official_total):
    totals = {field: complete_sum({str(i): r['counts'][field] for i, r in enumerate(records)},
                                [str(i) for i in range(len(records))]) for field in PDF_COLUMNS}
    differences = {f: {'mirror': totals[f], 'ncrb': official[f],
                       'ncrb_minus_mirror': None if totals[f] is None else official[f]-totals[f],
                       'pdf_page': PDF_COLUMNS[f][0]}
                   for f in PDF_COLUMNS if totals[f] != official[f]}
    subtotals = {kind: complete_sum({str(i): r['calculated']['calculated_recorded_heads_subtotal']
                                   for i, r in enumerate(records) if r['unit_type'] == kind},
                                  [str(i) for i, r in enumerate(records) if r['unit_type'] == kind])
                for kind in ['geographic_police_district', 'special_unit']}
    combined = complete_sum(subtotals, list(subtotals))
    return {'reportingYear': 2024, 'officialGeography': 'Delhi UT',
            'ncrbTotal': official_total, 'mirrorSubtotalsByUnitType': subtotals,
            'mirrorCombinedSubtotal': combined,
            'ncrbMinusMirror': None if combined is None else official_total-combined,
            'categoryComparisons': {f: {'mirror': totals[f], 'ncrb': official[f]} for f in PDF_COLUMNS},
            'discrepancies': differences,
            'status': 'matches' if combined == official_total and not differences else 'unresolved_discrepancy',
            'limitation': 'Aggregate agreement cannot validate individual district cells, boundaries or completeness. Do not distribute the discrepancy to districts.'}


def write_outputs(output, year, records, fields, metadata):
    output.mkdir(parents=True, exist_ok=True)
    stem = output / f'delhi-police-district-women-{year}'
    stem.with_suffix('.json').write_text(json.dumps({**metadata, 'records': records}, indent=2)+'\n', encoding='utf-8')
    fixed = ['district_name', 'year', 'unit_type', 'registration_circles', 'source_row_id',
             'source_state_code', 'source_administrative_district_name', 'source_administrative_district_code']
    calculated = list(FORMULAS) if year == 2024 else []
    with stem.with_suffix('.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fixed+fields+calculated+['missing_fields', 'sample', 'estimated'])
        writer.writeheader()
        for record in records:
            writer.writerow({**{f: record[f] for f in fixed}, **record['counts'], **record['calculated'],
                             'missing_fields': '|'.join(record['missing_fields']), 'sample': False, 'estimated': False})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'reports/delhi-districts')
    args = parser.parse_args()
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    sources = {source['id']: source for source in receipt['sources']}
    records, fields = extract(checked_file(sources['idp-2024']), 2024)
    official, total = official_values(checked_file(sources['ncrb-2024-volume-1']))
    validation = reconcile(records, official, total)
    write_outputs(args.output, 2024, records, fields, {
        'reportingYear': 2024, 'retrievalDate': receipt['retrievalDate'], 'sources': receipt['sources'],
        'formulas': FORMULAS, 'validation': validation,
        'categoryNotes': {'kidnapping_abduction_women': 'Section 137/138 BNS or 363 IPC leaf, not the parent total.',
                          'protection_children_sexual_violence_pocso': 'Sections 4 & 6 leaf, not total POCSO.',
                          'pocso_10': 'Source shorthand for sections 8 & 10.',
                          'assault_outrage_modesty_women': 'Section 74 BNS / 354 IPC adult leaf; separate from harassment, disrobing, voyeurism and stalking.'},
        'limitations': receipt['limitations']})
    older, older_fields = extract(checked_file(sources['idp-candidate-2017-2022']), 2022, validate_schema=False)
    write_outputs(args.output, 2022, older, older_fields, {
        'reportingYear': 2022, 'retrievalDate': receipt['retrievalDate'],
        'source': sources['idp-candidate-2017-2022'],
        'limitations': ['Candidate verification supplement: original category cells and blanks retained. No 2022 category hierarchy or total reconciliation asserted.']})
    print(json.dumps({'output': str(args.output), 'records': len(records), 'validation': validation['status'],
                      'mirrorSubtotal': validation['mirrorCombinedSubtotal'], 'ncrbTotal': total}, indent=2))


if __name__ == '__main__':
    main()
