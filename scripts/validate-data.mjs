import {build} from 'esbuild';
import fs from 'node:fs';
try{
const result=await build({stdin:{contents:"export {loadOffenders} from './src/lib/offenders'; export {loadRisk} from './src/lib/risk'; export {loadCrimeContext} from './src/lib/crime-context'; export {loadNews} from './src/lib/news'; export {loadDistrictCrime} from './src/lib/district-crime'; export {loadDistrictPoints} from './src/lib/district-points'; export {loadHistoricalDistricts} from './src/lib/historical-districts'; export {loadNcrDistricts} from './src/lib/ncr-districts';",resolveDir:process.cwd()},bundle:true,write:false,platform:'node',format:'esm'});
const validators=await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`);
validators.loadCrimeContext(JSON.parse(fs.readFileSync('public/data/crime-context.json','utf8')));
validators.loadDistrictCrime(JSON.parse(fs.readFileSync('public/data/delhi-district-crime.json','utf8')));
validators.loadHistoricalDistricts(JSON.parse(fs.readFileSync('public/data/delhi-historical-districts.json','utf8')));
validators.loadNcrDistricts(JSON.parse(fs.readFileSync('public/data/ncr-historical-districts.json','utf8')));
const local=await build({stdin:{contents:"export {localitySchema} from './src/lib/locality-context';",resolveDir:process.cwd()},bundle:true,write:false,platform:'node',format:'esm'});
const locality=await import(`data:text/javascript;base64,${Buffer.from(local.outputFiles[0].text).toString('base64')}`);
locality.localitySchema.parse(JSON.parse(fs.readFileSync('public/data/delhi-ncr/locality-context.json','utf8')));
validators.loadNews(JSON.parse(fs.readFileSync('public/data/news.json','utf8')));
validators.loadOffenders(JSON.parse(fs.readFileSync('public/data/offenders.json','utf8')));
for(const r of JSON.parse(fs.readFileSync('public/data/regions.json','utf8'))){for(const path of [r.neighbourhoodFile,r.sampleFile]){const list=validators.loadRisk(JSON.parse(fs.readFileSync(`public${path}`,'utf8')));if(path===r.neighbourhoodFile&&list.some(x=>x.provenance==='sample'))throw Error('Sample data in production file');if(list.some(x=>x.regionId!==r.id||!r.cities.some(c=>c.id===x.cityId)))throw Error('Unknown region or city');}}
for(const r of JSON.parse(fs.readFileSync('public/data/regions.json','utf8'))){if(r.districtReferenceFile){const points=validators.loadDistrictPoints(JSON.parse(fs.readFileSync(`public${r.districtReferenceFile}`,'utf8')));if(points.features.some(f=>!r.cities.some(c=>c.id===f.properties.cityId)))throw Error('Unknown reference city');}}
console.log('Offender, neighbourhood, historical context, recorded district totals, district references and news publication schemas passed.');
}catch(error){console.error(error instanceof Error?error.message:'Publication validation failed');process.exitCode=1;}
