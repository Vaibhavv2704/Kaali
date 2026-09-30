"""Reproducible Delhi input audit and historical environmental staging.

No network, model fitting or production risk publication occurs in this command.
Missing inputs are explicit. Changed bytes require source review, never guessing.
"""
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def read_verified(root, entry):
    path = (root / entry['path']).resolve()
    if not path.is_relative_to((root / 'raw').resolve()):
        raise ValueError('Input must remain within raw/')
    if not path.is_file():
        return None
    raw = path.read_bytes()
    if not entry.get('sha256'):
        raise ValueError('New input needs schema/vintage review before importing')
    if hashlib.sha256(raw).hexdigest() != entry['sha256']:
        raise ValueError(f"Changed source bytes: {entry['id']}; review before use")
    return path


def audit(root=ROOT):
    from shapely.geometry import shape
    from import_metro_context import convert
    manifest = json.loads((root / 'config/phase1-inputs.json').read_text(encoding='utf-8'))
    result = {'regionId':'delhi-ncr','cityId':'delhi','checkedAt':datetime.now(timezone.utc).isoformat(),
              'inputs':[], 'productionModelReady':False, 'productionNeighbourhoodObservations':0,
              'blockers':['No reviewed neighbourhood/time-band observations or observation coverage denominator.',
                          'Current female exposure and a reviewed historical-to-current boundary crosswalk are unavailable.',
                          'Current jurisdiction boundaries are not verified.',
                          'Held-out model evaluation has not been performed.'], 'sample':False}
    for entry in manifest['inputs']:
        item = {k:entry[k] for k in ('id','path','sourceUrl','licence','retrievedAt','sha256')}
        path = read_verified(root, entry)
        item['status'] = 'present' if path else 'missing'
        if path and entry['id']=='opencity-metros-2022':
            context=convert(path)
            item['delhiAnnualRows']=len([r for r in context['records'] if r['cityId']=='delhi'])
            item['eligibleForTraining']=False
        elif path and entry['id']=='datameet-delhi-wards':
            data=json.loads(path.read_text(encoding='utf-8'))
            geoms=[shape(f['geometry']) for f in data['features']]
            item.update(featureCount=len(geoms),invalidGeometryCount=sum(not g.is_valid for g in geoms),
                        emptyGeometryCount=sum(g.is_empty for g in geoms),currentBoundaryVerified=False,
                        vintage='Unverified historical wards; publisher issue #57 reports outdated geometry')
        elif path and entry['id']=='osm-help':
            data=json.loads(path.read_text(encoding='utf-8'))
            item.update(featureCount=len(data['features']),cityAssignment='Unverified',
                        completeRoadInventory=False,footfallObserved=False)
        elif path and entry['id']=='census-central-pca-2011':
            item.update(geography='Central district, 2011',currentExposureVerified=False,
                        boundaryCrosswalkVerified=False,acquisition=entry.get('acquisition'))
        result['inputs'].append(item)
    return result


def stage_environment():
    import pyproj  # Fail before processing if required CRS support is unavailable.
    import geopandas as gpd
    from environment import environmental_features
    manifest=json.loads((ROOT/'config/phase1-inputs.json').read_text(encoding='utf-8'))
    paths={e['id']:read_verified(ROOT,e) for e in manifest['inputs']}
    if not paths['datameet-delhi-wards'] or not paths['osm-help']:
        raise ValueError('Boundary candidate and OSM snapshot required')
    # GeoJSON is ordinary JSON; no GDAL file driver is needed for these inputs.
    zones=gpd.GeoDataFrame.from_features(json.loads(paths['datameet-delhi-wards'].read_text(encoding='utf-8'))['features'],crs=4326)
    zones['id']='historical-delhi-ward:'+zones['Ward_No'].astype(str)
    if zones['id'].duplicated().any() or not zones.is_valid.all() or zones.is_empty.any():
        raise ValueError('Invalid or duplicate boundary candidates')
    features=gpd.GeoDataFrame.from_features(json.loads(paths['osm-help'].read_text(encoding='utf-8'))['features'],crs=4326)
    table=environmental_features(zones,features[features.geometry.type=='Point'],
                                 features[features.geometry.type=='LineString'],'EPSG:32643')
    table['boundaryStatus']='historical-unverified'
    table['eligibleForTraining']=False
    table['poiScope']='Mapped help amenities only; not total POIs or observed footfall'
    table['roadScope']='Mapped lit main roads only; distances omit unmapped/unlit roads'
    table['femalePopulation']=None
    table['crimeCount']=None
    output=ROOT/'private/phase1'
    output.mkdir(parents=True,exist_ok=True)
    # Pandas maps missing numerical features to null rather than JSON NaN.
    (output/'historical-environment.json').write_text(table.to_json(orient='records',indent=2),encoding='utf-8')
    return len(table)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage-existing',action='store_true')
    parser.add_argument('--environment',action='store_true')
    args=parser.parse_args()
    if args.stage_existing:
        pairs=[(ROOT/'private/research/metros-2022.csv',ROOT/'raw/opencity/metros-2022.csv'),
               (ROOT/'private/research/delhi-wards-candidate.geojson',ROOT/'raw/datameet/Delhi_Wards.geojson'),
               (REPO/'public/data/delhi-ncr/help.geojson',ROOT/'raw/osm/help-2026-09-29.geojson')]
        for source,target in pairs:
            if source.is_file() and not target.exists():
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source,target)
    report=audit()
    if args.environment:
        try:
            report['historicalEnvironmentRows']=stage_environment()
        except ImportError:
            report['environmentStatus']='Unavailable: required geospatial runtime failed to import. No environment rows generated.'
    output=REPO/'public/data/reports/delhi-phase1.json'
    output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Delhi audit written. Production predictions remain unavailable; no sample scores published.')


if __name__=='__main__':main()
