"""Convert one reviewed OSM administrative relation; reject incomplete ring geometry."""
import argparse
import hashlib
import json
import math
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
from shapely.geometry import LineString,mapping,shape
from shapely.ops import polygonize_full,unary_union


def relation_polygon(data,relation_id,iso):
    if data.get('remark'):raise ValueError('Partial Overpass response')
    matches=[r for r in data['elements'] if r.get('type')=='relation' and r['id']==relation_id]
    if len(matches)!=1:raise ValueError('Missing or duplicate relation')
    relation=matches[0];tags=relation.get('tags',{})
    if tags.get('ISO3166-2')!=iso or tags.get('boundary')!='administrative' or tags.get('admin_level')!='4':
        raise ValueError('Unexpected administrative identity')
    rings={'outer':[],'inner':[]};seen=set()
    for member in relation['members']:
        role=member.get('role')
        if role not in rings:
            if (member['type'],role) in [('node','admin_centre'),('node','label'),('relation','subarea')]:continue
            raise ValueError('Unreviewed relation member role')
        if member['type']!='way' or not member.get('geometry'):raise ValueError('Missing boundary way geometry')
        if member['ref'] in seen:raise ValueError('Duplicate boundary way')
        seen.add(member['ref'])
        coords=[(p['lon'],p['lat']) for p in member['geometry']]
        if len(coords)<2 or any(not math.isfinite(x) or not math.isfinite(y) or not -180<=x<=180 or not -90<=y<=90 for x,y in coords):raise ValueError('Invalid coordinates')
        rings[role].append(LineString(coords))
    if not rings['outer']:raise ValueError('No outer boundary')
    polygons={}
    for role,lines in rings.items():
        faces,cuts,dangles,invalid=polygonize_full(lines)
        if not cuts.is_empty or not dangles.is_empty or not invalid.is_empty:raise ValueError('Incomplete or invalid ring topology')
        polygons[role]=unary_union(faces)
    outer=polygons['outer'];inner=polygons['inner']
    if not inner.is_empty and not outer.contains(inner):raise ValueError('Hole outside outer boundary')
    result=outer.difference(inner)
    if result.is_empty or not result.is_valid or result.geom_type not in ('Polygon','MultiPolygon'):raise ValueError('Invalid administrative polygon')
    return result,len(seen)


def assign_help(data,boundary,city_id):
    result=deepcopy(data);assigned=0
    for feature in result['features']:
        geometry=shape(feature['geometry'])
        # Exclude edge points and roads that touch/cross the boundary.
        inside=boundary.contains(geometry) and boundary.boundary.disjoint(geometry)
        previous=feature['properties'].get('cityId','')
        if inside:
            if previous and previous!=city_id:raise ValueError('Existing jurisdiction conflicts with reviewed boundary')
            feature['properties']['cityId']=city_id;assigned+=1
        elif previous==city_id:raise ValueError('Existing city assignment outside reviewed boundary')
    return result,assigned


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--relation',type=int,required=True);parser.add_argument('--iso',required=True)
    parser.add_argument('--city',required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--help-input',type=Path);parser.add_argument('--help-output',type=Path)
    a=parser.parse_args();raw=a.input.read_bytes();data=json.loads(raw)
    polygon,ways=relation_polygon(data,a.relation,a.iso)
    source=f'https://www.openstreetmap.org/relation/{a.relation}'
    output={'type':'FeatureCollection','attribution':'© OpenStreetMap contributors','license':'ODbL-1.0',
            'source':source,'sourceTimestamp':data.get('osm3s',{}).get('timestamp_osm_base'),
            'reviewedAt':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(raw).hexdigest(),
            'review':'OSM community administrative boundary; topology and identity checked, not a legal survey.',
            'features':[{'type':'Feature','properties':{'cityId':a.city,'source':source},'geometry':mapping(polygon)}]}
    if bool(a.help_input)!=bool(a.help_output):raise ValueError('Both help paths are required')
    if a.help_input:
        help_data,assigned=assign_help(json.loads(a.help_input.read_text(encoding='utf-8')),polygon,a.city)
        help_data['jurisdictionAssignment']={'cityId':a.city,'boundarySource':source,'assignedCount':assigned,
                                            'reviewedAt':output['reviewedAt'],'method':'Whole feature strictly inside OSM boundary'}
    # Validate every input and assignment before changing either published file.
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(output,ensure_ascii=False)+'\n',encoding='utf-8')
    if a.help_input:
        a.help_output.parent.mkdir(parents=True,exist_ok=True)
        a.help_output.write_text(json.dumps(help_data,ensure_ascii=False)+'\n',encoding='utf-8')
        print(f'Assigned {assigned} help features; other jurisdictions unchanged.')
    print(f'Validated {ways} boundary ways; bounds {polygon.bounds}. No risk observations generated.')


if __name__=='__main__':main()
