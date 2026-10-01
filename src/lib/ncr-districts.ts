import {z} from 'zod';
import {historicalRecordSchema,loadHistoricalDistricts,validateCategoryChecks} from './historical-districts';
const number=z.number().int().nonnegative().nullable();
const record=historicalRecordSchema.extend({reference:historicalRecordSchema.shape.reference.extend({coordinates:z.tuple([z.number().min(76.81).max(77.75),z.number().min(28.27).max(28.91)])}),cityId:z.string(),stateName:z.string(),history:z.array(z.object({year:z.number().int(),count:number})).min(1)});
const schema=z.object({schemaVersion:z.literal(2),regionId:z.literal('delhi-ncr'),year:z.number().int(),sourceUrl:z.string().url(),reportUrl:z.string().url(),workbookSha256:z.string().regex(/^[a-f0-9]{64}$/),provenanceNote:z.string(),stateTotal:number,geographicTotal:number,specialUnitTotal:number,ncrRecordedSubtotal:number,referenceNote:z.string(),stateChecks:z.array(z.object({state:z.string(),year:z.number().int(),sum_units:number,workbook_state_total:number,difference:z.literal(0),independent_report_total:number,independent_difference:z.literal(0)})).length(3),records:z.array(record).length(19)});
export type NcrDistrict=z.infer<typeof record>;
export type NcrDistricts=z.infer<typeof schema>;
const extra:Record<string,[string,string]>={'Gurugram':['gurugram','Haryana'],'Faridabad':['faridabad','Haryana'],'Gautambudh Nagar':['gautam-buddh-nagar','Uttar Pradesh'],'Ghaziabad':['ghaziabad','Uttar Pradesh']};
export function loadNcrDistricts(input:unknown){
 const data=schema.parse(input);
 const delhi=data.records.filter(r=>r.cityId==='delhi');
 loadHistoricalDistricts({...data,schemaVersion:1,records:delhi});
 if(new Set(data.records.map(r=>r.id)).size!==19)throw Error('Duplicate NCR reporting unit');
 for(const r of data.records){
  if(r.cityId==='delhi'){if(r.stateName!=='Delhi')throw Error('Wrong jurisdiction');}
  else if(!extra[r.id]||extra[r.id][0]!==r.cityId||extra[r.id][1]!==r.stateName||r.name!==r.id)throw Error('Wrong NCR reporting unit');
  if(r.year!==data.year||r.categories.length!==64||new Set(r.categories.map(c=>c.column)).size!==64||r.categories.some(c=>c.column<3||c.column>66))throw Error('Incomplete NCR scope');
  if(JSON.stringify(r.categories.filter(c=>c.count===null).map(c=>c.column).sort((a,b)=>a-b))!==JSON.stringify([...r.missingColumns].sort((a,b)=>a-b)))throw Error('Invalid NCR missing fields');
  if(new Set(r.history.map(h=>h.year)).size!==r.history.length||r.history.some(h=>h.year>r.year)||r.history.find(h=>h.year===r.year)?.count!==r.count)throw Error('Invalid observed history');
  validateCategoryChecks(r);
 }
 const total=data.records.some(r=>r.count===null)?null:data.records.reduce((sum,r)=>sum+r.count!,0);
 if(total!==data.ncrRecordedSubtotal)throw Error('Invalid NCR combined subtotal');
 if(new Set(data.stateChecks.map(c=>c.state)).size!==3||data.stateChecks.some(c=>!['Delhi','Haryana','Uttar Pradesh'].includes(c.state)||c.year!==data.year||c.sum_units!==c.workbook_state_total||c.sum_units!==c.independent_report_total))throw Error('Invalid state source comparison');
 return data;
}
