"""One bounded Overpass emergency snapshot, with source/robots receipt; no browser requests."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
import requests
from public_download import allowed,USER_AGENT
ROOT=Path(__file__).resolve().parent
URL='https://overpass-api.de/api/interpreter'
def main():
 region=json.loads((ROOT.parent/'public/data/regions.json').read_text())[0]
 b=region['bounds'];query=f"[out:json][timeout:50][maxsize:33554432];nwr[amenity~\"^(police|hospital|fire_station)$\"]({b['south']},{b['west']},{b['north']},{b['east']});out center;"
 path=ROOT/'raw/osm/ncr-emergency-2026-10-02.json';receipt=ROOT/'sources/ncr-emergency-2026-10-02.json'
 if path.exists():
  previous=json.loads(receipt.read_text());raw=path.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=previous['sha256']:raise ValueError('Changed snapshot')
  data=json.loads(raw)
 else:
  session=requests.Session();session.headers.update({'User-Agent':USER_AGENT,'Accept':'application/json'})
  audit={'sourceUrl':URL,'query':query,'licence':'ODbL-1.0','attribution':'© OpenStreetMap contributors','attemptedAt':datetime.now(timezone.utc).isoformat()}
  try:
   audit['robots']=allowed(session,URL)
   response=session.post(URL,data={'data':query},timeout=(15,65));response.raise_for_status()
   if len(response.content)>33554432:raise ValueError('Oversized response')
   data=response.json()
   if data.get('remark') or 'elements' not in data:raise ValueError('Partial response')
   raw=response.content;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
   audit.update(status='downloaded',retrievedAt=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),path=str(path.relative_to(ROOT)))
  except Exception as e:
   audit.update(status='failed',reason=str(e));receipt.write_text(json.dumps(audit,indent=2)+'\n');print('Emergency acquisition failed: '+str(e));return
  receipt.write_text(json.dumps(audit,indent=2)+'\n');previous=audit
 features=[]
 for e in data['elements']:
  tags=e.get('tags',{});center=e.get('center',e)
  if 'lon' not in center or 'lat' not in center:continue
  kind={'police':'police','hospital':'hospital','fire_station':'fire'}.get(tags.get('amenity'))
  if not kind:continue
  identity=f"{e['type']}/{e['id']}"
  features.append({'type':'Feature','id':identity,'geometry':{'type':'Point','coordinates':[center['lon'],center['lat']]},'properties':{'id':identity,'kind':kind,'name':tags.get('name:en',tags.get('name',f'Mapped {kind} facility')),'cityId':'','source':'https://www.openstreetmap.org/'+identity,'lastVerified':previous['retrievedAt'][:10],'verification':'OSM snapshot; not field-verified','opening_hours':tags.get('opening_hours')}})
 output={'type':'FeatureCollection','license':'ODbL-1.0','attribution':'© OpenStreetMap contributors','retrievedAt':previous['retrievedAt'],'features':features}
 (ROOT.parent/'public/data/delhi-ncr/emergency.geojson').write_text(json.dumps(output,ensure_ascii=False)+'\n',encoding='utf-8')
 print('Published mapped emergency places: '+str(len(features)))
if __name__=='__main__':main()
