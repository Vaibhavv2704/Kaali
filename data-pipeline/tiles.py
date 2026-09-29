"""Static vector tile build; requires tippecanoe and pmtiles CLIs in PATH."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    records=json.loads(a.input.read_text());features=[]
    for r in records:
        if r['provenance']=='sample':raise ValueError('Do not publish sample geometries as production vector tiles')
        if r['boundaryStatus']!='verified':raise ValueError('Boundary review required')
        features.append({'type':'Feature','geometry':r['geometry'],'properties':{'id':r['id'],'name':r['name'],'cityId':r['cityId']}})
    if not features:raise ValueError('No verified geometry to tile')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        src=Path(temp)/'zones.geojson';mb=Path(temp)/'zones.mbtiles';src.write_text(json.dumps({'type':'FeatureCollection','features':features}))
        # Tippecanoe's default per-zoom simplification retained; no dropping of zones.
        subprocess.run(['tippecanoe','-o',str(mb),'-l','neighbourhoods','-Z','7','-z','15','--no-tile-size-limit','--no-feature-limit',str(src)],check=True)
        subprocess.run(['pmtiles','convert',str(mb),str(a.output)],check=True)
    print('Tiles built. Set region.pmtiles and sourceLayer=neighbourhoods after QA; server must support HTTP Range + CORS.')

if __name__=='__main__':main()
