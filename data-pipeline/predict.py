"""Export static risk records from a reviewed model and six-band feature matrix."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from train import NUM,CAT

def main():
    p=argparse.ArgumentParser();p.add_argument('--region',required=True);p.add_argument('--model',type=Path,required=True);p.add_argument('--features',type=Path,required=True);p.add_argument('--boundaries',type=Path,required=True);p.add_argument('--release-review',type=Path,required=True);a=p.parse_args()
    root=Path(__file__).resolve().parents[1];region=next(r for r in json.loads((root/'public/data/regions.json').read_text()) if r['id']==a.region)
    review=json.loads(a.release_review.read_text());required=['metricsReviewed','privacyReviewed','licencesReviewed','boundariesReviewed','exposureReviewed']
    if not all(review.get(k) is True for k in required) or not review.get('sources') or review.get('rateScale',0)<=0:raise ValueError('Release review and positive calibrated rateScale required')
    df=pd.read_csv(a.features);model=joblib.load(a.model);pred=np.maximum(model.predict(df[NUM+CAT]),0);df['score']=np.clip(100*(1-np.exp(-pred/review['rateScale'])),0,100).round().astype(int)
    records=[];geo=json.loads(a.boundaries.read_text())
    for feature in geo['features']:
        prop=feature['properties'];id=prop['id'];rows=df[df.neighbourhood_id==id]
        if rows.empty:continue
        scores={}
        for day in ['weekday','weekend']:
            values=rows[rows.day_type==day].sort_values('time_band')
            if list(values.time_band)!=list(range(6)):raise ValueError(f'{id}: incomplete or duplicate six-band observations')
            scores[f'{day}:all']=values.score.tolist()
        if prop['cityId'] not in {c['id'] for c in region['cities']}:raise ValueError('Unconfigured city')
        records.append({'id':id,'name':prop['name'],'cityId':prop['cityId'],'regionId':region['id'],'geometry':feature['geometry'],'boundaryStatus':'verified','provenance':'model','confidence':review.get('confidence','low'),'sources':review['sources'],'scores':scores,'incidents':None,'trend':None,'year':int(review['year']),'femalePopulation':float(prop['femalePopulation']),'periodDays':float(review['periodDays']),'estimated':True})
    if not records:raise ValueError('No publishable predictions')
    output=root/'public'/region['neighbourhoodFile'].lstrip('/');output.write_text(json.dumps(records,indent=2));print('Static predictions written. Run pnpm validate:data and review city coverage before publishing.')

if __name__=='__main__':main()
