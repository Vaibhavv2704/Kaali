"""Check an approved Python runtime without fitting models or changing policies."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

CHECKS={
    'tables':'import pandas, numpy, openpyxl',
    'geometry':'from shapely.geometry import Point; assert Point(0,0).is_valid',
    'projection':'from pyproj import Transformer; Transformer.from_crs(4326,32643,always_xy=True).transform(77.2,28.6)',
    'ml':'from sklearn.model_selection import GroupKFold; from lightgbm import LGBMRegressor; import joblib; import numpy as np; x=np.arange(40).reshape(20,2); model=LGBMRegressor(n_estimators=2,min_child_samples=2,verbosity=-1,n_jobs=1).fit(x,np.arange(20)%3); assert np.isfinite(model.predict(x)).all()',
    'news':'import requests, bs4, trafilatura',
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();results={}
    for name,code in CHECKS.items():
        try:
            result=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True,timeout=45)
            # Do not publish local paths or environment values from traceback output.
            reason='Import/execution failed; inspect this interpreter locally.'
            if 'application control' in result.stderr.lower():reason='Windows Application Control blocked a required binary.'
            elif 'no module named' in result.stderr.lower():reason='A required package is missing.'
            results[name]={'available':result.returncode==0,'reason':None if result.returncode==0 else reason}
        except subprocess.TimeoutExpired:
            results[name]={'available':False,'reason':'Runtime check exceeded 45 seconds.'}
    report={'checks':results,'runtimeReady':all(x['available'] for x in results.values()),
            'modelTrained':False,'note':'Runtime availability does not establish data readiness or model validity.'}
    text=json.dumps(report,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text+'\n',encoding='utf-8')
    print(text)
    return 0 if report['runtimeReady'] else 1


if __name__=='__main__':sys.exit(main())
