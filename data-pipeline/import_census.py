"""Import reviewed Central Delhi PCA 2011 population, without a modern boundary join."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
KEYS=['State','District','Subdistt','Town/Village','Ward']
POP=['TOT_P','TOT_M','TOT_F']


def normalize(rows):
    required=set(KEYS+POP+['Level','Name','TRU'])
    seen=set()
    for row in rows:
        if not required.issubset(row):raise ValueError('Missing Census columns')
        if row['State']!='07' or row['District']!='095':raise ValueError('Unexpected reporting district')
        if any(type(row[k]) is not int or row[k]<0 for k in POP):raise ValueError('Missing or invalid population')
        if row['TOT_P']!=row['TOT_M']+row['TOT_F']:raise ValueError('Sex totals do not reconcile')
        key=tuple(row[k] for k in KEYS)+ (row['Level'],row['TRU'])
        if key in seen:raise ValueError('Duplicate Census reporting unit')
        seen.add(key)
    district=[r for r in rows if r['Level']=='DISTRICT' and r['TRU']=='Total']
    wards=[r for r in rows if r['Level']=='WARD' and r['TRU']=='Urban']
    towns=[r for r in rows if r['Level']=='TOWN' and r['TRU']=='Urban']
    if len(district)!=1 or not wards:raise ValueError('Missing district total or ward rows')
    if any(sum(r[k] for r in wards)!=district[0][k] for k in POP):raise ValueError('Ward totals do not reconcile to district')
    for town in towns:
        children=[r for r in wards if all(r[k]==town[k] for k in KEYS[:4])]
        if not children or any(sum(r[k] for r in children)!=town[k] for k in POP):raise ValueError('Ward parts do not reconcile to town')
    town_keys={tuple(r[k] for k in KEYS[:4]) for r in towns}
    if any(tuple(r[k] for k in KEYS[:4]) not in town_keys for r in wards):raise ValueError('Ward missing parent town')
    return {'district':{'name':district[0]['Name'],'totalPopulation':district[0]['TOT_P'],
                        'malePopulation':district[0]['TOT_M'],'femalePopulation':district[0]['TOT_F']},
            'records':[{'id':':'.join(r[k] for k in KEYS),'stateCode':r['State'],'districtCode':r['District'],
                        'subdistrictCode':r['Subdistt'],'townCode':r['Town/Village'],'wardCode':r['Ward'],
                        'name':r['Name'],'totalPopulation':r['TOT_P'],'malePopulation':r['TOT_M'],
                        'femalePopulation':r['TOT_F'],'year':2011,'boundaryMatched':False} for r in wards]}


def convert(path, expected_hash):
    import openpyxl
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected_hash:raise ValueError('Workbook changed; re-review required')
    book=openpyxl.load_workbook(path,read_only=True,data_only=False)
    try:
        if book.sheetnames!=['EB-0706']:raise ValueError('Unexpected workbook sheets')
        sheet=book.worksheets[0]
        values=iter(sheet.values);headers=next(values)
        if len(set(headers))!=len(headers):raise ValueError('Duplicate headers')
        rows=[dict(zip(headers,r)) for r in values if any(v is not None for v in r)]
        result=normalize(rows)
    finally:book.close()
    return {'schemaVersion':1,'regionId':'delhi-ncr','cityId':'delhi','year':2011,
            'sourceUrl':'https://censusindia.gov.in/nada/index.php/catalog/6286/study-description',
            'publisher':'Office of the Registrar General & Census Commissioner, India',
            'acquisition':'User-supplied local workbook; catalog metadata matched, remote bytes not independently compared',
            'reviewedAt':'2026-09-30','sha256':expected_hash,'sample':False,'eligibleForTraining':False,
            'limitations':['Central district only, according to 2011 Census geography.',
                           'Rows are ward parts within subdistricts/towns; ward number alone is not a unique key.',
                           'Historical female population is not a current exposure estimate.',
                           'No boundary crosswalk or crime geography join has been verified.'],**result}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True);args=parser.parse_args()
    manifest=json.loads((ROOT/'config/phase1-inputs.json').read_text(encoding='utf-8'))
    entry=next(e for e in manifest['inputs'] if e['id']=='census-central-pca-2011')
    result=convert(args.input,entry['sha256'])
    (ROOT.parent/'public/data/census-central-2011.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'Imported {len(result["records"])} historical Census ward-part rows; no current crime rates or boundary matches.')
