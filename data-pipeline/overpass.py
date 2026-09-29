"""Fetch one bounded OSM snapshot per region; never query Overpass from browsers."""
import argparse
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ENDPOINT=os.environ.get('OVERPASS_URL','https://overpass-api.de/api/interpreter')

def query_for(region):
    b=region['bounds'];box=f"{b['south']},{b['west']},{b['north']},{b['east']}"
    return f'''[out:json][timeout:50][maxsize:67108864];(
      nwr[amenity~"^(police|hospital)$"]({box});
      node[railway=station]({box});
      node[highway=bus_stop]({box});
      way[highway~"^(primary|secondary|trunk)$"][lit=yes]({box});
    );out center geom;'''

def city_for(lng,lat,region):
    # No rectangular/nearest-city jurisdiction guesses. Missing geometry stays unassigned.
    for city in region['cities']:
        if not city.get('boundaryFile'): continue
        from shapely.geometry import shape, Point
        data=json.loads((ROOT/'public'/city['boundaryFile'].lstrip('/')).read_text())
        if any(shape(f['geometry']).contains(Point(lng,lat)) for f in data['features']): return city['id']
    return ''

def transform(data,region):
    features=[];now=datetime.now(timezone.utc).date().isoformat()
    for e in data.get('elements',[]):
        tags=e.get('tags',{});kind=tags.get('amenity')
        if kind not in ('police','hospital'):
            if tags.get('railway')=='station':
                # Keep only subway / light rail station evidence, not every railway station.
                if not (tags.get('station') in ('subway','light_rail') or tags.get('subway')=='yes' or tags.get('light_rail')=='yes'): continue
                kind='metro'
            elif tags.get('highway')=='bus_stop':kind='bus'
            elif tags.get('lit')=='yes':kind='road'
            else:continue
        center=e.get('center',e);lng=center.get('lon');lat=center.get('lat')
        if lng is None or lat is None:continue
        geometry={'type':'Point','coordinates':[lng,lat]}
        if kind=='road':
            coords=[[p['lon'],p['lat']] for p in e.get('geometry',[]) if 'lon' in p]
            if len(coords)<2:continue
            geometry={'type':'LineString','coordinates':coords}
        features.append({'type':'Feature','id':f"{e['type']}/{e['id']}",'geometry':geometry,'properties':{'id':f"{e['type']}/{e['id']}",'name':tags.get('name:en',tags.get('name',{'police':'Mapped police station','hospital':'Mapped hospital','metro':'Mapped metro station','bus':'Mapped bus stop','road':'OSM lit=yes main road'}[kind])),'kind':kind,'cityId':city_for(lng,lat,region),'source':f"https://www.openstreetmap.org/{e['type']}/{e['id']}",'lastVerified':now,'verification':'OSM snapshot; not field-verified','opening_hours':tags.get('opening_hours'),'lit':tags.get('lit')}})
    return {'type':'FeatureCollection','license':'ODbL-1.0','attribution':'© OpenStreetMap contributors','retrievedAt':now,'features':features}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--region',default='delhi-ncr');ap.add_argument('--input',type=Path);ap.add_argument('--force',action='store_true');a=ap.parse_args()
    region=next(r for r in json.loads((ROOT/'public/data/regions.json').read_text()) if r['id']==a.region)
    output=ROOT/'public'/region['helpFile'].lstrip('/')
    if output.exists() and not a.force:
        old=json.loads(output.read_text());date=old.get('retrievedAt')
        if date and (datetime.now(timezone.utc).date()-datetime.fromisoformat(date).date()).days<7:raise SystemExit('Snapshot under 7 days old; using cache. --force only for deliberate refresh.')
    if a.input:data=json.loads(a.input.read_text())
    else:
        request=urllib.request.Request(ENDPOINT,data=urllib.parse.urlencode({'data':query_for(region)}).encode(),headers={'User-Agent':'KaaliResearch/0.1 (weekly static NCR snapshot)','Accept':'application/json'})
        with urllib.request.urlopen(request,timeout=60) as response:data=json.load(response)
    if data.get('remark'):raise ValueError('Overpass partial/error response; preserving previous snapshot: '+data['remark'])
    result=transform(data,region);temporary=output.with_suffix('.tmp');temporary.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8');temporary.replace(output)
    print(f"Saved {len(result['features'])} OSM features. Unassigned city IDs remain unassigned, not guessed.")

if __name__=='__main__':main()
