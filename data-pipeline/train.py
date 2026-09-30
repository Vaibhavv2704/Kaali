"""Train only on reviewed observations; emit validation evidence before release."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

NUM=['historical_density','lighting','poi_density','open_late_density','distance_police','distance_metro','distance_main_road','population_density','time_band']
CAT=['land_use','city_id','jurisdiction','day_type']

def estimator():
    from lightgbm import LGBMRegressor
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
    prep=ColumnTransformer([('num',SimpleImputer(strategy='median',add_indicator=True),NUM),('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),CAT)])
    return Pipeline([('prep',prep),('model',LGBMRegressor(objective='poisson',n_estimators=120,num_leaves=15,learning_rate=.04,verbosity=-1,random_state=42,n_jobs=2))])

def validate_frame(df):
    df = df.copy()
    required=set(NUM+CAT+['neighbourhood_id','period_start','period_end','feature_cutoff','count','female_population','period_days','estimated','provenance','source_url','observation_coverage','coverage_source_url','boundary_status','exposure_source_url'])
    missing=required-set(df.columns)
    if missing: raise ValueError(f'Missing columns: {sorted(missing)}')
    if len(df)<100 or df.neighbourhood_id.nunique()<5 or df.city_id.nunique()<2: raise ValueError('Need 100+ observations, 5+ neighbourhoods and 2+ cities for validation')
    if not df.provenance.eq('observed').all() or not df.estimated.astype(str).str.lower().isin(['false','0']).all(): raise ValueError('Synthetic/allocated or unknown counts cannot be training ground truth')
    if not df.observation_coverage.eq('complete').all(): raise ValueError('Target cells need documented complete observation coverage; missing news reports are not zero counts')
    if not df.boundary_status.eq('verified').all(): raise ValueError('Training requires reviewed neighbourhood boundaries')
    for col in ['count','female_population','period_days']:
        df[col] = pd.to_numeric(df[col], errors='raise')
        if not np.isfinite(df[col]).all(): raise ValueError(f'Non-finite {col}')
    if not (df['count'] % 1 == 0).all(): raise ValueError('Observed counts must be integers')
    if (df.female_population<=0).any() or (df.period_days<=0).any() or (df['count']<0).any(): raise ValueError('Invalid exposure/count')
    if not df.time_band.isin(range(6)).all() or not df.day_type.isin(['weekday','weekend']).all(): raise ValueError('Invalid time dimensions')
    for col in ['period_start','period_end','feature_cutoff']: df[col]=pd.to_datetime(df[col],errors='raise')
    if not (df.period_end >= df.period_start).all(): raise ValueError('Reversed reporting period')
    for col in ['period_start','period_end']:
        if not df[col].eq(df[col].dt.normalize()).all(): raise ValueError('Reporting periods must use whole inclusive calendar dates')
    # Exposure counts only matching weekdays/weekends in the inclusive period.
    # Each row covers one four-hour band; the rate remains band-specific.
    for row in df.itertuples():
        dates=pd.date_range(row.period_start,row.period_end,freq='D')
        expected=sum((d.dayofweek<5)==(row.day_type=='weekday') for d in dates)
        if row.period_days!=expected: raise ValueError('period_days does not match the observed day-type calendar')
    for col in CAT + ['neighbourhood_id']:
        if df[col].isna().any() or df[col].astype(str).str.strip().eq('').any(): raise ValueError(f'Missing {col}')
    if not (df.feature_cutoff<df.period_start).all(): raise ValueError('Historical features must predate labels to prevent leakage')
    if df.duplicated(['neighbourhood_id','period_start','time_band','day_type']).any(): raise ValueError('Duplicate target cells')
    for _,group in df.groupby(['neighbourhood_id','time_band','day_type']):
        ordered=group.sort_values('period_start')
        if (ordered.period_start.iloc[1:].to_numpy()<=ordered.period_end.cummax().iloc[:-1].to_numpy()).any():
            raise ValueError('Overlapping target periods would double-count observations')
    for col in ['source_url','coverage_source_url','exposure_source_url']:
        if not df[col].fillna('').str.match(r'^https://[^/\s]+(?:/|$)').all(): raise ValueError(f'Missing source provenance: {col}')
    for col in NUM:
        df[col]=pd.to_numeric(df[col],errors='raise')
        if np.isinf(df[col]).any() or (df[col].dropna()<0).any(): raise ValueError(f'Invalid feature: {col}')
    if (df.lighting.dropna()>1).any(): raise ValueError('Lighting must be a fraction or missing')
    return df

def metrics(y,pred,cities):
    from sklearn.metrics import mean_absolute_error, mean_poisson_deviance
    def score(mask): return {'mae':float(mean_absolute_error(y[mask],pred[mask])),'poisson_deviance':float(mean_poisson_deviance(y[mask],np.maximum(pred[mask],1e-8))),'rows':int(mask.sum())}
    return {'overall':score(np.ones(len(y),dtype=bool)),'cities':{city:score(np.array(cities)==city) for city in sorted(set(cities))}}

def train(path,out):
    df=validate_frame(pd.read_csv(path))
    from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
    x=df[NUM+CAT];exposure=df.female_population*df.period_days/365.25/100000;y=(df['count']/exposure).to_numpy();weights=exposure.to_numpy();reports={}
    for name,splitter,groups in [('spatial',GroupKFold(min(5,df.neighbourhood_id.nunique())),df.neighbourhood_id),('held_out_city',LeaveOneGroupOut(),df.city_id)]:
        folds=[]
        for train_idx,test_idx in splitter.split(x,y,groups):
            model=estimator();model.fit(x.iloc[train_idx],y[train_idx],model__sample_weight=weights[train_idx]);pred=model.predict(x.iloc[test_idx]);folds.append(metrics(y[test_idx],pred,df.city_id.iloc[test_idx].to_numpy()))
        reports[name]=folds
    dates=sorted(df.period_start.unique())
    if len(dates)<3: raise ValueError('Need at least three distinct periods for temporal validation')
    cutoff=dates[-1];tr=np.flatnonzero(df.period_end.to_numpy()<cutoff);te=np.flatnonzero(df.period_start.to_numpy()>=cutoff)
    if not len(tr) or not len(te): raise ValueError('Overlapping temporal periods prevent validation')
    model=estimator();model.fit(x.iloc[tr],y[tr],model__sample_weight=weights[tr]);reports['temporal']=metrics(y[te],model.predict(x.iloc[te]),df.city_id.iloc[te].to_numpy())
    out.mkdir(parents=True,exist_ok=True);(out/'metrics.json').write_text(json.dumps(reports,indent=2));model.fit(x,y,model__sample_weight=weights);joblib.dump(model,out/'model.joblib');print('Staging model and validation evidence written. Manual release review required.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path(__file__).parent/'artifacts')
    ap.add_argument('--validate-only',action='store_true',help='Check evidence and exposure without loading the ML runtime or fitting a model')
    args=ap.parse_args()
    if args.validate_only:
        frame=validate_frame(pd.read_csv(args.input))
        print(f'{len(frame)} input rows passed structural checks. Source review and model evaluation still required. No model trained.')
    else:train(args.input,args.output)
