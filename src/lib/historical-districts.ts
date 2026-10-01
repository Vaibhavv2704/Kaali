import {z} from 'zod';
const value=z.number().int().nonnegative().nullable();
const record=z.object({id:z.string(),name:z.string(),year:z.number().int(),count:value,countType:z.literal('recorded_total'),sourceRow:z.number().int(),categories:z.array(z.object({column:z.number().int(),label:z.string(),count:value,kind:z.enum(['subtotal','source_heading']),highlight:z.string().nullable()})),missingColumns:z.array(z.number().int()),categoryMismatches:z.array(z.object({column:z.number().int(),label:z.string(),reported_parent:value,child_sum:value,difference:z.number().nullable()})),reference:z.object({coordinates:z.tuple([z.number().min(76.8).max(77.4),z.number().min(28.4).max(28.9)]),name:z.string(),kind:z.string(),source:z.string().url(),assignmentSource:z.string().url(),status:z.literal('approximate_reference'),reviewedAt:z.string()})});
const schema=z.object({schemaVersion:z.literal(1),year:z.number().int(),sourceUrl:z.string().url(),reportUrl:z.string().url(),workbookSha256:z.string().regex(/^[a-f0-9]{64}$/),provenanceNote:z.string(),stateTotal:value,geographicTotal:value,specialUnitTotal:value,referenceNote:z.string(),records:z.array(record).length(15)});
export type HistoricalDistrict=z.infer<typeof record>;
export type HistoricalDistricts=z.infer<typeof schema>;
const districtNames=new Set(['Central','East','New Delhi','North','North-East','North-West','Outer','Outer North','Rohini','Dwarka','Shahdara','South','South-East','South-West','West']);

function validateCategoryChecks(district:HistoricalDistrict){
 const byColumn=new Map(district.categories.map(c=>[c.column,c]));
 const expected=district.categories.flatMap(parent=>{
  if(!parent.label.includes('(Total a+b)'))return [];
  const a=byColumn.get(parent.column+1),b=byColumn.get(parent.column+2);
  if(!a||!b)throw Error('Incomplete source hierarchy');
  const sum=a.count===null||b.count===null?null:a.count+b.count;
  return sum===parent.count?[]:[{column:parent.column,parent:parent.count,sum,difference:sum===null||parent.count===null?null:parent.count-sum}];
 });
 if(new Set(district.categoryMismatches.map(c=>c.column)).size!==district.categoryMismatches.length||district.categoryMismatches.length!==expected.length)throw Error('Incomplete category discrepancy disclosure');
 for(const check of expected){
  const declared=district.categoryMismatches.find(c=>c.column===check.column);
  if(!declared||declared.reported_parent!==check.parent||declared.child_sum!==check.sum||declared.difference!==check.difference)throw Error('Invalid category discrepancy');
 }
}

export function loadHistoricalDistricts(input:unknown){
 const data=schema.parse(input);
 if(new Set(data.records.map(r=>r.id)).size!==15||data.records.some(r=>!districtNames.has(r.id)||r.id!==r.name||r.year!==data.year))throw Error('Invalid district identity');
 if(data.records.some(r=>r.categories.length!==64||new Set(r.categories.map(c=>c.column)).size!==64||r.categories.some(c=>c.column<3||c.column>66)||JSON.stringify(r.categories.filter(c=>c.count===null).map(c=>c.column).sort((a,b)=>a-b))!==JSON.stringify([...r.missingColumns].sort((a,b)=>a-b))))throw Error('Invalid category scope');
 data.records.forEach(validateCategoryChecks);
 const total=data.records.some(r=>r.count===null)?null:data.records.reduce((n,r)=>n+r.count!,0);
 if(total!==data.geographicTotal||(total!==null&&data.specialUnitTotal!==null&&total+data.specialUnitTotal!==data.stateTotal))throw Error('Invalid reconciliation');
 return data;
}
function validCount(count:number){if(!Number.isFinite(count)||count<0)throw Error('Invalid count');}
export function districtDiameter(count:number|null){if(count===null)return null;validCount(count);return 22+Math.sqrt(count/1500)*30}
export function districtBand(count:number|null){if(count===null)return 'unknown';validCount(count);return count<500?'pale':count<1000?'medium':'strong'}
