"""Local-only partner/RTI aggregate readers; never scrape unavailable sources."""
import json
from pathlib import Path
from count_model import count

ROOT = Path(__file__).resolve().parent


def read_unreviewed_aggregates(source):
    if source not in ('safecity', 'safetipin', 'rti'):
        raise ValueError('Unsupported pending source')
    path = ROOT/'raw'/source/'aggregate-counts.json'
    if not path.exists():
        return {'status': 'not_supplied', 'records': [], 'path': str(path)}
    records = json.loads(path.read_text(encoding='utf-8'))
    allowed = {'area_id', 'year', 'total_reported_cases', 'source_url', 'reporting_unit',
               'time_band', 'day_type', 'licence'}
    for row in records:
        if not set(row) <= allowed:
            raise ValueError('Only aggregate fields are accepted; no personal data')
        if not all(row.get(k) is not None for k in ('area_id', 'year', 'source_url', 'reporting_unit')):
            raise ValueError('Missing aggregate provenance')
        count(row.get('total_reported_cases'))
    # Review is mandatory before these can become training labels. Safetipin
    # audits in particular are environment observations, not crime counts.
    return {'status': 'supplied_unreviewed_not_training', 'records': records, 'path': str(path)}
