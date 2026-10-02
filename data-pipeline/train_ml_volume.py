"""Train real count-label ML; export explicitly assumed spatial scenarios separately."""
import hashlib,json,sys
from pathlib import Path
from importlib.metadata import version
import joblib,numpy as np,pandas as pd
from sklearn.linear_model import PoissonRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold
from lightgbm import LGBMRegressor
from train_count_model import workbook_rows,independent_report_check,observations
from count_model import metrics,assert_split
from extract_delhi_districts import GEOGRAPHIC
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'reports/ml-volume-v1';ART=ROOT/'artifacts/ml-volume-v1'
SEEDS=[7,42,103]
def write(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def build_pool(config):
 rows=[];checks=[];excluded=[]
 for source in config['sources']:
  data,state_checks=workbook_rows(source);checks+=state_checks
  for r in data:
   name=r['source_name']
   if (r['state']=='Delhi' and name.replace('-',' ') not in {n.replace('-',' ') for n in GEOGRAPHIC}) or name in {'GRP','Irrigation & Power'}:
    excluded.append({'state':r['state'],'name':name,'year':r['year'],'reason':'special reporting unit'});continue
   # These explicit labels occur alongside unmatched rural/outer units in 2022.
   if name in {'Kanpur Commissionarate','Lucknow Commissionarate','Varanasi Commissionarate'}:
    excluded.append({'state':r['state'],'name':name,'year':r['year'],'reason':'unmatched related labels across years; boundary continuity not established'});continue
   rows.append({**r,'unit_id':r['state']+':'+name.replace('-',' '),'feature_year':r['year']})
 independent_report_check(checks)
 if any(c['difference']!=0 or c['independent_difference']!=0 for c in checks):raise ValueError('Source totals do not reconcile')
 frame=[]
 for r in rows:
  previous=[p for p in rows if p['unit_id']==r['unit_id'] and p['year']<r['year'] and p['count'] is not None]
  if previous and r['count'] is not None:
   p=max(previous,key=lambda x:x['year']);frame.append({**r,'history_count':p['count'],'feature_year':p['year']})
 return pd.DataFrame(frame),checks,excluded
def models(seed=42):
 return {'poisson_glm':make_pipeline(StandardScaler(),PoissonRegressor(alpha=1,max_iter=3000)),
 'lightgbm_poisson':LGBMRegressor(objective='poisson',n_estimators=80,num_leaves=7,min_child_samples=10,learning_rate=.04,reg_lambda=10,random_state=seed,verbosity=-1,n_jobs=1,deterministic=True,force_col_wise=True)}
def features(frame):return np.log1p(frame.history_count.to_numpy()).reshape(-1,1)
def influence(coordinates,anchors):
 """Reference interpolation only: no district assignment or neighbourhood case count."""
 distances=np.array([np.hypot((coordinates[0]-a['coordinates'][0])*97.6,(coordinates[1]-a['coordinates'][1])*111.2) for a in anchors])
 indices=np.argsort(distances)[:3]
 if not len(indices) or distances[indices[0]]>12:return None,[]
 weights=1/np.maximum(distances[indices],.5)**2;weights/=weights.sum()
 return float(sum(anchors[i]['volume_index']*w for i,w in zip(indices,weights))),[{'id':anchors[i]['id'],'weight':float(w),'distanceKm':float(distances[i])} for i,w in zip(indices,weights)]
def main():
 config=json.loads((ROOT/'config/counts-v1.json').read_text());frame,checks,excluded=build_pool(config)
 if frame.unit_id.duplicated().any() or len(frame)<30:raise ValueError('Expected independent lagged district examples')
 X=features(frame);y=frame['count'].to_numpy();predictions={name:np.zeros(len(frame)) for name in ['persistence',*models()]};folds=[]
 for train,test in GroupKFold(5).split(X,y,frame.unit_id):
  assert_split(frame.iloc[train],frame.iloc[test]);predictions['persistence'][test]=frame.iloc[test].history_count
  folds.append({'train':frame.iloc[train].unit_id.tolist(),'test':frame.iloc[test].unit_id.tolist(),'feature_year':2022,'target_year':2024})
  for name,model in models().items():model.fit(X[train],y[train]);predictions[name][test]=model.predict(X[test])
 comparison={name:metrics(y,p) for name,p in predictions.items()}
 chosen=min(models(),key=lambda name:comparison[name]['mae'])
 fitted=models()[chosen];fitted.fit(X,y)
 ncr=json.loads((ROOT.parent/'public/data/ncr-historical-districts.json').read_text());context=json.loads((ROOT.parent/'public/data/delhi-ncr/locality-context.json').read_text())
 city_evaluation={};ncr_errors=[]
 for city in sorted({r['cityId'] for r in ncr['records']}):
  ids={r['stateName']+':'+r['name'].replace('-',' ') for r in ncr['records'] if r['cityId']==city}
  mask=frame.unit_id.isin(ids).to_numpy();train=np.where(~mask)[0];test=np.where(mask)[0]
  if not len(test):raise ValueError('Missing NCR validation unit')
  assert_split(frame.iloc[train],frame.iloc[test]);model=models()[chosen];model.fit(X[train],y[train]);p=model.predict(X[test]);ncr_errors.extend((y[test]-p).tolist())
  city_evaluation[city]={'model':metrics(y[test],p),'persistence':metrics(y[test],frame.iloc[test].history_count),'train_ids':frame.iloc[train].unit_id.tolist(),'test_ids':frame.iloc[test].unit_id.tolist()}
 forecasts=np.maximum(0,fitted.predict(np.log1p([r['count'] for r in ncr['records']]).reshape(-1,1)))
 errors=y-predictions[chosen];lo,hi=np.quantile(errors,[.05,.95]);anchors=[]
 for r,p in zip(ncr['records'],forecasts):
  rank=(float(np.sum(forecasts<p))+.5*float(np.sum(forecasts==p)))/len(forecasts)*100
  anchors.append({'id':r['id'],'name':r['name'],'state':r['stateName'],'coordinates':r['reference']['coordinates'],'recordedYear':2024,'recordedCases':r['count'],'forecastYear':2026,'expectedAnnualCases':float(p),'volume_index':rank,'interval':[max(0,float(p+lo)),max(0,float(p+hi))],'intervalStatus':'pooled out-of-area residual range; uncalibrated future coverage','dataType':'model-estimate','confidence':'low','referenceStatus':'approximate_reference'})
 outline=json.loads((ROOT.parent/'public/data/delhi-ncr/delhi-boundary.geojson').read_text())
 from shapely.geometry import shape,Point
 from shapely.ops import unary_union
 delhi=unary_union([shape(f['geometry']) for f in outline['features']])
 local=[]
 for r in context['records']:
  eligible=[a for a in anchors if a['state']=='Delhi'] if delhi.covers(Point(r['coordinates'])) else []
  score,weights=influence(r['coordinates'],eligible)
  local.append({'id':r['id'],'annualVolumeIndex':score,'influenceReferences':weights,'riskScore':None,'reportedCases':None,'status':'model-reference-interpolation' if score is not None else 'unknown','confidence':'low','spatialMapping':'assumed proximity; no police/locality membership assigned'})
 stability={}
 for seed in SEEDS:
  model=models(seed)[chosen];model.fit(X,y);values=model.predict(np.log1p([r['count'] for r in ncr['records']]).reshape(-1,1));stability[str(seed)]={'max_abs_difference_vs_seed42':float(np.max(np.abs(values-forecasts)))}
 ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
 joblib.dump(fitted,ART/'model.joblib');frame.to_csv(OUT/'training-examples.csv',index=False)
 model_config={'version':'ml-volume-v1','chosen_model':chosen,'features':['log1p_previous_observed_annual_cases'],'seed':42,'seeds':SEEDS,'training_feature_year':2022,'training_target_year':2024,'forecast_origin_year':2024,'forecast_horizon_years':2,'night_context':'separate historical/assumed scenario; never trained as invented crime labels','sources':config['sources']}
 write(ART/'config.json',model_config)
 report={'version':'ml-volume-v1','examples':len(frame),'comparison':comparison,'chosen_learned_model':chosen,'best_overall':min(comparison,key=lambda name:comparison[name]['mae']),'city_evaluation':city_evaluation,'folds':folds,'source_total_checks':checks,'excluded':excluded,'seed_stability':stability,'temporal_ml_validation':None,'temporal_limitation':'Only one lag/target cohort; learned models cannot be honestly validated on later unseen target years. Spatial tests are retrospective transfer, not future prediction validation.','features':model_config['features'],'runtime':{p:version(p) for p in ['scikit-learn','lightgbm','numpy','joblib']}}
 rng=np.random.default_rng(42);paired=np.abs(y-predictions['persistence'])-np.abs(y-predictions[chosen])
 draws=rng.integers(0,len(frame),size=(2000,len(frame)))
 report['paired_mae_improvement']={'mean_cases':float(paired.mean()),'bootstrap_95_interval':np.quantile(paired[draws].mean(axis=1),[.025,.975]).tolist(),'basis':'reporting-unit bootstrap of retrospective OOF errors; model selected on these folds, no untouched final test'}
 write(OUT/'evaluation.json',report);write(OUT/'artifact-hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ART.iterdir() if p.is_file()})
 export={'version':'ml-volume-v1','model':chosen,'trainedOn':'real 2022→2024 police reporting-unit annual totals; pooled Delhi/Haryana/UP auxiliary units','forecastYear':2026,'notASafetyProbability':True,'forecastStatus':'experimental; future-year validation unavailable','comparison':{n:{k:v for k,v in m.items() if k in ['mae','rmse','spearman']} for n,m in comparison.items()},'anchors':anchors,'localities':local,'sourceHashes':{s['path']:s['sha256'] for s in config['sources']},'modelSha256':hashlib.sha256((ART/'model.joblib').read_bytes()).hexdigest(),'assumptions':['Two-year count relationship remains applicable from 2024 to 2026','Same reporting-unit name does not verify boundary continuity','Proximity interpolation is a display assumption, not police jurisdiction or neighbourhood cases','Historical traffic/density adjust the display separately, not learned crime occurrence probabilities'],'limitations':['No measured neighbourhood crime labels','No crime time-of-day labels','Incomplete current activity context and no live traffic','Reporting bias and IPC/BNS definition changes','Pooled residual intervals have no validated future coverage']}
 write(ROOT.parent/'public/data/delhi-ncr/ml-volume.json',export);write(OUT/'export.json',export)
 by_id={r['id']:r for r in local}
 write(OUT/'reference-cells.geojson',{'type':'FeatureCollection','metadata':{'version':'ml-volume-v1','status':'assumed spatial display','notLocalityBoundaries':True,'noNeighbourhoodCaseAllocation':True},'features':[{'type':'Feature','geometry':r['geometry'],'properties':{'id':r['id'],'name':r['name'],'annualVolumeIndex':by_id[r['id']]['annualVolumeIndex'],'reportedCases':None,'riskScore':None,'confidence':'low','dataType':'model-estimate-with-assumed-spatial-mapping'}} for r in context['records']]})
 print(json.dumps({'examples':len(frame),'chosen':chosen,'best_overall':report['best_overall'],'comparison':{n:{k:v for k,v in m.items() if k in ['mae','rmse','spearman']} for n,m in comparison.items()},'spatial_scenarios':sum(r['annualVolumeIndex'] is not None for r in local)},indent=2))
if __name__=='__main__':main()
