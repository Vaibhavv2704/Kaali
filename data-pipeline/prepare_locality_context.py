"""Audit supplied context; never allocate district crime totals to reference cells."""
import csv, hashlib, json, math, re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
import h3
import numpy as np
from scipy.spatial import cKDTree

ROOT=Path(__file__).resolve().parent
def normal(value): return re.sub(r'[^a-z0-9]', '', value.lower())
def probe_metadata(data):
    features=data.get('features',[])
    if not features or features[0].get('geometry') is not None:raise ValueError('Missing leading probe metadata')
    metadata=features[0].get('properties',{})
    days=metadata.get('dateRanges',[])
    if len(days)!=1 or days[0].get('from')!=days[0].get('to') or '@id' not in days[0]:raise ValueError('Expected one actual date per probe file')
    day=date.fromisoformat(days[0]['from'])
    if not date(2024,8,11)<=day<=date(2024,8,30):raise ValueError('Probe date outside declared sample period')
    times={}; hours=[]
    for t in metadata.get('timeSets',[]):
        match=re.fullmatch(r'(\d{1,2}):00-(\d{1,2}):00',t.get('name',''))
        if not match:raise ValueError('Expected whole-hour probe time set')
        hour,end=map(int,match.groups())
        if hour<0 or hour>23 or end!=(hour+1)%24 and end!=hour+1:raise ValueError('Invalid hourly range')
        if t['@id'] in times:raise ValueError('Duplicate time-set identifier')
        hours.append(hour);times[t['@id']]=hour//4
    if len(hours)!=24 or set(hours)!=set(range(24)):raise ValueError('Incomplete or duplicated probe hours')
    return day,days[0]['@id'],times
def corrected_population_coordinates(row):
    # Original source headers are reversed. Never change the supplied bytes.
    lat,lon=float(row['Longitude']),float(row['latitude'])
    if not(28.27<=lat<=28.91 and 76.81<=lon<=77.75):raise ValueError('Population coordinates outside configured NCR bounds')
    return lat,lon
def main():
    inputs=[]
    def audit(path):
        inputs.append({'path':str(path.relative_to(ROOT)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes':path.stat().st_size, 'source':'user-supplied', 'licence':'not supplied', 'retrievalDate':None})
    points=[]; rejected=[]
    source=ROOT/'delhi_neighbour.csv'; audit(source)
    for i,r in enumerate(csv.DictReader(source.open(encoding='utf-8-sig'))):
        if not r['latitude'] or not r['longitude']: rejected.append({'row':i,'reason':'missing coordinates'}); continue
        lat,lon=float(r['latitude']),float(r['longitude'])
        if not(28.27<=lat<=28.91 and 76.81<=lon<=77.75): rejected.append({'row':i,'reason':'outside configured NCR bounds'}); continue
        points.append({'id':f'locality-reference-{i}', 'name':r['Neighborhood'], 'sourceBorough':r['Borough'], 'coordinates':[lon,lat], 'population':None,'density':None,'populationYear':None,'reportedCases':None,'referenceStatus':'user-supplied-unverified'})
    pop=ROOT/'population density wardwise 1.csv';audit(pop)
    population=list(csv.DictReader(pop.open(encoding='utf-8-sig')))
    for p in points:
        matches=[r for r in population if normal(r['City'])==normal(p['name'])]
        if len(matches)==1:
            r=matches[0]; lat,lon=corrected_population_coordinates(r)
            # Swapped source headings retained in audit; never edit original CSV.
            km=math.hypot((lon-p['coordinates'][0])*97.6,(lat-p['coordinates'][1])*111.2)
            if 28.27<=lat<=28.91 and 76.81<=lon<=77.75 and km<=2:
                density=float(r['Density']); population_count=float(r['Population']); area=float(r['Area'])
                if area>0 and abs(population_count/area-density)<0.02:
                    p.update(population=population_count,density=density,populationMatch='exact normalised name and within 2 km; density units/year unverified')
    ward=ROOT/'population density wardwise 2.csv'; audit(ward)
    ward_rows=list(csv.DictReader(ward.open(encoding='utf-8-sig')))
    # No ward geometry/area: do not convert population to density or infer spatial join.
    for p in points:
        matches=[r for r in ward_rows if normal(r['ward'])==normal(p['name'])]
        if p['population'] is None and len(matches)==1 and matches[0]['total_population']:
            p['population']=float(matches[0]['total_population'])
            p['populationMatch']='exact unique ward-name match only; ward vintage/boundary unverified, not a spatial match'
    tree=cKDTree(np.array([[p['coordinates'][0]*97.6,p['coordinates'][1]*111.2] for p in points]))
    aggregates=defaultdict(lambda:[0.0,0]); segment_sets=defaultdict(set); file_notes=[]
    files=sorted((ROOT/'new_delhi_traffic_dataset/probe_counts/geojson').glob('*.geojson'))
    if len(files)!=20:raise ValueError('Expected all 20 daily traffic files; refusing incomplete publication')
    observed_dates=set()
    for path in files:
        audit(path); data=json.loads(path.read_text());day,date_id,times=probe_metadata(data)
        if day in observed_dates:raise ValueError('Duplicate probe reporting date')
        observed_dates.add(day);daytype='weekend' if day.weekday()>=5 else 'weekday'
        valid=0; assigned=0
        for f in data['features'][1:]:
            g=f.get('geometry');props=f.get('properties',{})
            if not g or g['type']!='LineString' or not g['coordinates']:continue
            valid+=1; coords=g['coordinates'];lon=sum(c[0] for c in coords)/len(coords);lat=sum(c[1] for c in coords)/len(coords)
            km,index=tree.query([lon*97.6,lat*111.2])
            if km>1:continue
            assigned+=1; segment_sets[int(index)].add(str(props['segmentId']))
            for obs in props.get('segmentProbeCounts',[]):
                if obs.get('dateRange')!=date_id:raise ValueError('Probe references an unexpected date range')
                value=obs.get('probeCount'); band=times.get(obs.get('timeSet'))
                if band is None or value is None:continue
                if not isinstance(value,(int,float)) or not math.isfinite(value) or value<0:raise ValueError('Invalid probe count')
                a=aggregates[(int(index),daytype,band)];a[0]+=value;a[1]+=1
        file_notes.append({'path':path.name,'date':str(day),'roadSegments':valid,'assignedSegments':assigned})
    if observed_dates!={date(2024,8,11)+timedelta(days=i) for i in range(20)}:raise ValueError('Incomplete declared traffic period')
    for i,p in enumerate(points):
        p['traffic']={day:[round(aggregates[(i,day,b)][0]/aggregates[(i,day,b)][1],4) if aggregates[(i,day,b)][1] else None for b in range(6)] for day in ['weekday','weekend']}
        p['trafficSegments']=len(segment_sets[i])
        cell=h3.latlng_to_cell(p['coordinates'][1],p['coordinates'][0],8)
        ring=[[lon,lat] for lat,lon in h3.cell_to_boundary(cell)];ring.append(ring[0])
        p['geometry']={'type':'Polygon','coordinates':[ring]};p['cellId']=cell
    result={'schemaVersion':1,'regionId':'delhi-ncr','trafficPeriod':'2024-08-11 to 2024-08-30','trafficMeaning':'mean sampled probes per road-segment-hour; nearest supplied reference within 1 km, not vehicles, people, congestion or live conditions','populationNote':'Source headings swapped in file 1; only unique name matches within 2 km retained. Population year/density units unverified. File 2 has no area or geometry; not used for density.','licence':'User-supplied input licence/provenance not supplied; review before redistribution','geometryNote':'H3 resolution 8 reference cells, not locality or police boundaries; supplied names/coordinates unverified','records':points}
    dest=ROOT.parent/'public/data/delhi-ncr/locality-context.json';dest.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    receipt={'inputs':inputs,'rejectedLocalityRows':rejected,'trafficFiles':file_notes,'wardPopulationRowsNotSpatiallyJoined':len(ward_rows),'densityMatches':sum(p['density'] is not None for p in points),'populationMatches':sum(p['population'] is not None for p in points),'records':len(points),'crimeAllocation':'none; neighbourhood counts remain unknown'}
    (ROOT/'sources/supplied-locality-context.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:receipt[k] for k in ['records','populationMatches','wardPopulationRowsNotSpatiallyJoined']}))
if __name__=='__main__':main()
