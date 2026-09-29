import fs from 'node:fs';
const path='src/data/helplines.json',data=JSON.parse(fs.readFileSync(path,'utf8'));
const report=[];const cache=new Map();
for(const e of data.entries){try{let body=cache.get(e.source);if(!body){const response=await fetch(e.source,{signal:AbortSignal.timeout(18000),headers:{'User-Agent':'AegisHelplineVerification/0.1','Accept':'text/html'}});if(!response.ok)throw Error(`HTTP ${response.status}`);body=await response.text();cache.set(e.source,body);}const found=new RegExp(`(?<![0-9])${e.number}(?![0-9])`).test(body);report.push({id:e.id,url:e.source,number:e.number,status:found?'number-present-manual-context-review-needed':'number-not-found',checkedAt:new Date().toISOString()});}catch(error){report.push({id:e.id,url:e.source,status:'unavailable',reason:error.message,checkedAt:new Date().toISOString()})}}
for(const r of data.resources){try{const response=await fetch(r.url,{signal:AbortSignal.timeout(15000),headers:{'User-Agent':'AegisHelplineVerification/0.1'}});report.push({url:r.url,status:response.ok?'reachable':'unavailable',httpStatus:response.status})}catch{report.push({url:r.url,status:'unavailable'})}}
fs.mkdirSync('public/data/reports',{recursive:true});fs.writeFileSync('public/data/reports/helpline-verification.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report.map(({id,url,status})=>({id:id??url,status})),null,2));
// Never automatically update lastVerified on reachability alone.
if(report.some(x=>x.status==='unavailable'||x.status==='number-not-found'))process.exitCode=1;
