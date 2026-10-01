"""Experimental annual recorded-rape-head forecasting, NOT a safety model.

Uses actual mirror cells. No disaggregation, time bands, population rates or risk
scores. Backtests hold out years and whole reporting units/cities. Artifacts stay
private. Run with the project's Python runtime.
"""
import json
from pathlib import Path
import csv
from extract_delhi_districts import ROOT, RECEIPT, GEOGRAPHIC, checked_file, parse_count


def observations():
    sources={s['id']:s for s in json.loads(RECEIPT.read_text())['sources']}
    result=[];seen=set()
    other={'Gurugram':('Haryana','gurugram'),'Faridabad':('Haryana','faridabad'),
           'Gautambudh Nagar':('Uttar Pradesh','gautam-buddh-nagar'), 'Ghaziabad':('Uttar Pradesh','ghaziabad')}
    for source_id,fields in [('idp-candidate-2017-2022',('rape_women_above_18','rape_girls_below_18')),
                             ('idp-2024',('rape_women','rape_girls'))]:
        with checked_file(sources[source_id]).open(encoding='utf-8-sig',newline='') as stream:
            for row in csv.DictReader(stream):
                unit=row['registration_circles'];state=row['state_name']
                city='delhi' if state=='Delhi' and unit in GEOGRAPHIC else other.get(unit,(None,None))[1] if other.get(unit,(None,None))[0]==state else None
                if city is None:continue
                year=parse_count(row['year']);counts=[parse_count(row[f]) for f in fields]
                if None in counts:continue  # Missing is never observed zero.
                key=(city,unit,year)
                if key in seen:raise ValueError('Duplicate reporting unit/year')
                seen.add(key)
                result.append({'unit':unit,'city':city,'year':year,'count':sum(counts),'source':source_id})
    return result


def examples(rows):
    result=[]
    for row in rows:
        history=sorted([r for r in rows if r['unit']==row['unit'] and r['city']==row['city'] and r['year']<row['year']],key=lambda r:r['year'])
        if len(history)<2:continue
        last,prior=history[-1],history[-2]
        result.append({**row,'last_count':last['count'],'prior_count':prior['count'],
                       'past_mean':sum(r['count'] for r in history)/len(history),
                       'trend':(last['count']-prior['count'])/(last['year']-prior['year']),
                       'horizon':row['year']-last['year'],'feature_cutoff':last['year']})
    return result


def model():
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.pipeline import Pipeline
    from lightgbm import LGBMRegressor
    return Pipeline([('features',ColumnTransformer([('numeric','passthrough',['last_count','prior_count','past_mean','trend','horizon']),
        ('city',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['city'])])),
        ('model',LGBMRegressor(objective='poisson',n_estimators=80,num_leaves=7,min_child_samples=5,learning_rate=.04,random_state=42,n_jobs=2,verbosity=-1))])


def evaluate(train,test):
    from sklearn.metrics import mean_absolute_error
    import numpy as np
    if train.empty or test.empty:raise ValueError('Empty evaluation split')
    fitted=model().fit(train,train['count']);pred=fitted.predict(test)
    if not np.isfinite(pred).all() or (pred<0).any():raise ValueError('Invalid model output')
    def score(mask):return {'rows':int(mask.sum()),'model_mae':float(mean_absolute_error(test['count'].to_numpy()[mask],pred[mask])),
                           'last_observation_mae':float(mean_absolute_error(test['count'].to_numpy()[mask],test.last_count.to_numpy()[mask]))}
    return {'overall':score(np.ones(len(test),dtype=bool)),
            'cities':{c:score(test.city.to_numpy()==c) for c in sorted(set(test.city))}},[
                {'unit':r.unit,'city':r.city,'year':int(r.year),'observed':int(r.count),'predicted':float(p),
                 'last_observation':int(r.last_count),'horizon':int(r.horizon)} for r,p in zip(test.itertuples(),pred)]


def main():
    import pandas as pd
    import joblib
    from sklearn.model_selection import GroupKFold,LeaveOneGroupOut
    rows=observations();frame=pd.DataFrame(examples(rows))
    if not (frame.feature_cutoff<frame.year).all():raise ValueError('Feature leakage')
    latest=int(frame.year.max());past=frame[frame.year<latest]
    temporal,heldout=evaluate(past,frame[frame.year==latest])
    # Spatial/city evaluations use only pre-latest labels. Held-out units retain
    # their known lag history as input, never their target labels as training rows.
    grouped={}
    for name,splitter,groups in [('reporting_unit',GroupKFold(5),past.city+':'+past.unit),('city',LeaveOneGroupOut(),past.city)]:
        grouped[name]=[evaluate(past.iloc[tr],past.iloc[te])[0] for tr,te in splitter.split(past,groups=groups)]
    report={'target':'Annual registered rape heads (adult + girl IPC/BNS), police reporting unit',
            'status':'experimental_research_only','safetyModelEligible':False,'observations':len(rows),'examples':len(frame),
            'observedYears':sorted(set(r['year'] for r in rows)),'temporalHoldoutYear':latest,
            'temporal':temporal,'groupedValidation':grouped,'heldoutPredictions':heldout,
            'releaseGate':{'beat_last_observation_temporal':temporal['overall']['model_mae']<temporal['overall']['last_observation_mae'],
                           'neighbourhood_time_risk_release':False},
            'limitations':['No neighbourhood/time-band targets, exposure rates or safety probabilities.',
              '2023 is absent; 2024 forecasts have a two-year horizon. No invented 2023 values.',
              'Secondary-source cells and reporting-unit continuity are not independently verified for every historical year.',
              'IPC/BNS and POCSO registration practices can change the recorded rape-head series.',
              'Grouped tests hold out target rows; lag features use known history of held-out units.',
              'GBN is one district, not separate Noida/Greater Noida counts.'],
            'sources':json.loads(RECEIPT.read_text())['sources']}
    output=ROOT/'artifacts/district-forecast';output.mkdir(parents=True,exist_ok=True)
    (output/'evaluation.json').write_text(json.dumps(report,indent=2)+'\n')
    frame.to_csv(output/'training-examples.csv',index=False)
    joblib.dump(model().fit(frame,frame['count']),output/'model.joblib')
    # Small tracked evaluation report; no model scores are put into public risk JSON.
    path=ROOT/'reports/DISTRICT-FORECAST.json';path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'observations':len(rows),'temporal':temporal,'releaseGate':report['releaseGate']},indent=2))


if __name__=='__main__':main()
