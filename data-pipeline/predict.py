"""Stage static predictions; validate exact joins and reviewed artifact identities."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlparse
import numpy as np
import pandas as pd
from shapely.geometry import shape
from train import NUM,CAT


def positive(value):
    return type(value) in (int,float) and math.isfinite(value) and value>0


def validate_review(review):
    required=['metricsReviewed','privacyReviewed','licencesReviewed','boundariesReviewed','exposureReviewed']
    if not all(review.get(k) is True for k in required):raise ValueError('Complete release review required')
    if not positive(review.get('rateScale')) or not positive(review.get('periodDays')):
        raise ValueError('Finite positive calibrated rateScale and periodDays required')
    if type(review.get('year')) is not int or not 1900<=review['year']<=2100:raise ValueError('Invalid reporting year')
    if review.get('confidence') not in ('low','medium','high'):raise ValueError('Reviewed confidence required')
    sources=review.get('sources')
    if not isinstance(sources,list) or not sources:raise ValueError('Sources required')
    for source in sources:
        if set(source)!={'label','url'} or not source['label']:raise ValueError('Invalid source')
        url=urlparse(source['url'])
        if url.scheme!='https' or not url.hostname:raise ValueError('HTTPS source required')


def verify_artifacts(review,paths):
    expected=review.get('artifactSha256',{})
    for name,path in paths.items():
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected.get(name):
            raise ValueError(f'{name}: bytes differ from reviewed artifact')


def validate_inputs(frame,geo,region):
    required=set(NUM+CAT+['neighbourhood_id'])
    if required-set(frame.columns):raise ValueError('Missing prediction features')
    if frame.empty:raise ValueError('No prediction features')
    if geo.get('type')!='FeatureCollection' or not geo.get('features'):raise ValueError('No boundary features')
    features={};cities={c['id'] for c in region['cities']}
    for feature in geo['features']:
        prop=feature['properties'];key=prop.get('id')
        if not isinstance(key,str) or not key or key in features:raise ValueError('Missing or duplicate boundary ID')
        if prop.get('cityId') not in cities or prop.get('boundaryStatus')!='verified':raise ValueError('Unreviewed boundary jurisdiction')
        if not prop.get('name') or not positive(prop.get('femalePopulation')):raise ValueError('Missing name or female exposure')
        geom=shape(feature['geometry'])
        if geom.geom_type not in ('Polygon','MultiPolygon') or geom.is_empty or not geom.is_valid:
            raise ValueError('Invalid neighbourhood geometry')
        if not (-180<=geom.bounds[0]<=geom.bounds[2]<=180 and -90<=geom.bounds[1]<=geom.bounds[3]<=90):
            raise ValueError('Geometry outside WGS84 bounds')
        features[key]=feature
    if set(frame.neighbourhood_id)!=set(features):raise ValueError('Feature/boundary IDs must match exactly; no silent omissions')
    if not frame.day_type.isin(['weekday','weekend']).all() or not frame.time_band.isin(range(6)).all():
        raise ValueError('Invalid time dimensions')
    for key,rows in frame.groupby('neighbourhood_id'):
        if not rows.city_id.eq(features[key]['properties']['cityId']).all():raise ValueError('Feature jurisdiction differs from boundary')
        for day in ['weekday','weekend']:
            if sorted(rows.loc[rows.day_type==day,'time_band'].tolist())!=list(range(6)):
                raise ValueError('Each neighbourhood needs exactly six bands for each day type')
    for col in CAT:
        if frame[col].isna().any() or frame[col].astype(str).str.strip().eq('').any():raise ValueError('Missing categorical feature')
    for col in NUM:
        values=pd.to_numeric(frame[col],errors='raise')
        if np.isinf(values).any() or (values.dropna()<0).any():raise ValueError('Invalid numeric feature')
    if (frame.lighting.dropna()>1).any():raise ValueError('Invalid lighting fraction')
    return features


def build_records(frame,predictions,geo,region,review):
    validate_review(review);features=validate_inputs(frame,geo,region)
    pred=np.asarray(predictions,dtype=float)
    if pred.shape!=(len(frame),) or not np.isfinite(pred).all() or (pred<0).any():
        raise ValueError('Invalid model rates; do not silently clip or replace predictions')
    df=frame.copy();df['score']=np.rint(-100*np.expm1(-pred/review['rateScale'])).astype(int)
    records=[]
    for key,feature in features.items():
        prop=feature['properties'];rows=df[df.neighbourhood_id==key]
        scores={f'{day}:all':rows[rows.day_type==day].sort_values('time_band').score.tolist() for day in ['weekday','weekend']}
        records.append({'id':key,'name':prop['name'],'cityId':prop['cityId'],'regionId':region['id'],
            'geometry':feature['geometry'],'boundaryStatus':'verified','provenance':'model','confidence':review['confidence'],
            'sources':review['sources'],'scores':scores,'incidents':None,'trend':None,'year':review['year'],
            'femalePopulation':prop['femalePopulation'],'periodDays':review['periodDays'],'estimated':True})
    return records


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--region',required=True)
    for name in ['model','features','boundaries','release-review']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--output',type=Path,default=Path(__file__).parent/'artifacts/predictions.json')
    a=p.parse_args();root=Path(__file__).resolve().parents[1]
    if a.output.resolve().is_relative_to((root/'public').resolve()):raise ValueError('Stage outside public/; validate and review before copying for release')
    region=next(r for r in json.loads((root/'public/data/regions.json').read_text()) if r['id']==a.region)
    review=json.loads(a.release_review.read_text());validate_review(review)
    verify_artifacts(review,{'model':a.model,'features':a.features,'boundaries':a.boundaries})
    frame=pd.read_csv(a.features);geo=json.loads(a.boundaries.read_text());validate_inputs(frame,geo,region)
    # Load only trusted local artifacts whose exact bytes were reviewed. Joblib is executable.
    import joblib
    model=joblib.load(a.model)
    records=build_records(frame,model.predict(frame[NUM+CAT]),geo,region,review)
    payload=json.dumps(records,indent=2,allow_nan=False)+'\n'
    a.output.parent.mkdir(parents=True,exist_ok=True)
    temp=a.output.with_suffix(a.output.suffix+'.tmp');temp.write_text(payload,encoding='utf-8');temp.replace(a.output)
    print('Predictions staged. Review and validate before copying to the configured public neighbourhood file.')


if __name__=='__main__':main()
