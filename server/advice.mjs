import http from 'node:http';
import {pathToFileURL} from 'node:url';
export function contextOnly(input){
 const allowed={index:['unknown','lower','middle','higher'],time:['day','night'],activity:['unknown','lower','higher'],population:['unknown','available']};
 if(!input||typeof input!=='object'||Array.isArray(input)||Object.keys(input).length!==4||Object.keys(input).some(k=>!Object.hasOwn(allowed,k))||Object.entries(allowed).some(([k,values])=>!values.includes(input[k])))throw Error('Only anonymous context categories are accepted');
 return input;
}
export function advicePrompt(context){contextOnly(context);return `Write 2 short calm travel-awareness sentences in English. Input: ${JSON.stringify(context)}. The index comes from an experimental annual recorded-case ML model, with assumed spatial/time/activity adjustments. Local crime risk, live traffic and individual safety are unknown. Never assert current danger, safety, crime probability, blame, stranger stereotypes or tell someone to stay indoors. Suggest one practical voluntary action appropriate to night/day and sampled activity. Do not invent names, numbers, locations or operational facility details. Reply JSON with exactly one key: advice.`;}
export function acceptAdvice(value){const text=value?.advice;if(typeof text!=='string'||text.length<20||text.length>600||/<|https?:|\b\d{2,}\b|stay (at )?(home|indoors)|avoid going outdoors|don't trust|do not trust|safe area|area is safe|area is unsafe|area is dangerous|area is risky|high risk area|definitely|guarantee|will be attacked|victim|rape|murder/i.test(text))throw Error('Unacceptable generated advice');return text;}
export function createAdviceServer(){return http.createServer(async(req,res)=>{
 const origin=req.headers.origin??'';
 if(!/^http:\/\/(127\.0\.0\.1|localhost):\d+$/.test(origin)){res.writeHead(403);res.end();return;}
 res.setHeader('Access-Control-Allow-Origin',origin);res.setHeader('Vary','Origin');res.setHeader('Cache-Control','no-store');
 if(req.method==='OPTIONS'){res.setHeader('Access-Control-Allow-Methods','POST');res.setHeader('Access-Control-Allow-Headers','Content-Type');res.writeHead(204);res.end();return;}
 if(req.method!=='POST'||req.url!=='/api/advice'){res.writeHead(404);res.end();return;}
 try{
  let body='';for await(const chunk of req){body+=chunk;if(body.length>1024)throw Error('Oversized context');}
  const context=contextOnly(JSON.parse(body));
  const model=process.env.KAALI_OLLAMA_MODEL;if(!model){res.writeHead(503,{'Content-Type':'application/json'});res.end(JSON.stringify({error:'Configure KAALI_OLLAMA_MODEL for an installed local Ollama model.'}));return;}
  const result=await fetch('http://127.0.0.1:11434/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,system:'You provide cautious awareness tips, not safety predictions.',prompt:advicePrompt(context),format:'json',stream:false,options:{temperature:.2,num_predict:180}}),signal:AbortSignal.timeout(30000)});
  if(!result.ok)throw Error('Local generation unavailable');const answer=await result.json();const advice=acceptAdvice(JSON.parse(answer.response));
  res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({advice,source:'local-ollama'}));
 }catch{res.writeHead(503,{'Content-Type':'application/json'});res.end(JSON.stringify({error:'AI advice is unavailable; the on-device summary remains available.'}));}
 });}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){createAdviceServer().listen(5175,'127.0.0.1',()=>process.stdout.write('Kaali local advice service on port 5175\n'));}
