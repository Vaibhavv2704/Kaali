"""Historical volume at explicitly approximate OSM reference points, not zones."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    data=json.loads((ROOT/'public/data/delhi-district-crime.json').read_text())
    help_data=json.loads((ROOT/'public/data/delhi-ncr/help.geojson').read_text())
    # Explicit reviewed name/ID pairs; never geocode police units from LGD names.
    anchors={'Central':('node/12441175891','Office Of The Deputy Commissioner Of Police Central District'),
             'Shahdara':('node/12596382943','DCP Shahdara District Office'),
             'Dwarka':('node/2408446621','Dwarka Police Station')}
    features=[]
    for unit,(key,name) in anchors.items():
        matches=[f for f in help_data['features'] if f['properties']['id']==key and f['properties']['name']==name]
        if len(matches)!=1:raise ValueError('Reference point changed; review required')
        point=matches[0];record=next(r for r in data['records'] if r['registration_circles']==unit)
        if record['unit_type']!='geographic_police_district':raise ValueError('Special unit cannot be assigned geography')
        features.append({'type':'Feature','id':unit,'geometry':point['geometry'],
          'properties':{'id':unit,'name':unit,'cityId':'delhi','year':2024,
            'count':record['calculated']['calculated_recorded_heads_subtotal'],
            'referenceName':name,'source':point['properties']['source'],'crimeSource':data['sourceUrl'],
            'pointStatus':'approximate_reference','meaning':'Historical recorded-head subtotal; not a safety score or danger radius',
            'lastVerified':point['properties']['lastVerified']}})
    output=ROOT/'public/data/delhi-ncr/district-reference-points.geojson'
    output.write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2)+'\n')
    print('Published three approximate district reference points; no district polygons or crime locations.')


if __name__=='__main__':main()
