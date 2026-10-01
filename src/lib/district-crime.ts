import {z} from 'zod';

const count=z.number().int().nonnegative().nullable();
const record=z.object({district_name:z.string(),year:z.number().int(),
 unit_type:z.enum(['geographic_police_district','special_unit']),registration_circles:z.string(),
 source_row_id:z.string(),source_state_code:z.string(),source_administrative_district_name:z.string(),
 source_administrative_district_code:z.string(),counts:z.record(count),missing_fields:z.array(z.string()),
 calculated:z.record(count),sample:z.literal(false),estimated:z.literal(false),trainingEligible:z.literal(false),
 boundary:z.null(),neighbourhoodId:z.null()}).strict();
const schema=z.object({schemaVersion:z.literal(1),regionId:z.string(),cityId:z.string(),year:z.number().int(),
 retrievedAt:z.string(),sourceUrl:z.string().url(),downloadUrl:z.string().url(),officialUrl:z.string().url(),
 sha256:z.string().regex(/^[a-f0-9]{64}$/),licence:z.string(),formulas:z.record(z.array(z.string()).min(1)),
 records:z.array(record).min(1),validation:z.object({reportingYear:z.number().int(),officialGeography:z.string(),
 ncrbTotal:count,mirrorSubtotalsByUnitType:z.record(count),mirrorCombinedSubtotal:count,ncrbMinusMirror:z.number().int().nullable(),
 categoryComparisons:z.record(z.object({mirror:count,ncrb:count}).strict()),
 discrepancies:z.record(z.object({mirror:count,ncrb:count,ncrb_minus_mirror:z.number().int().nullable(),pdf_page:z.number().int()}).strict()),
 status:z.enum(['matches','unresolved_discrepancy']),limitation:z.string()}).strict()}).strict();
export type DistrictCrime=z.infer<typeof schema>;
export function formatCases(value:number|null|undefined){return value==null?'Not published':value.toLocaleString('en-IN')}
export function loadDistrictCrime(input:unknown){
 const data=schema.parse(input),seen=new Set<string>();
 const heads=data.formulas.calculated_recorded_heads_subtotal;
 if(!heads||new Set(heads).size!==heads.length||data.validation.reportingYear!==data.year)throw Error('Invalid recorded-head scope');
 if(Object.keys(data.validation.categoryComparisons).length!==heads.length||heads.some(f=>!(f in data.validation.categoryComparisons)))throw Error('Incomplete category comparisons');
 for(const row of data.records){
  if(seen.has(row.registration_circles)||row.district_name!==row.registration_circles||row.year!==data.year)throw Error('Invalid district identity');
  seen.add(row.registration_circles);
  if(Object.keys(row.counts).length!==heads.length||heads.some(f=>!(f in row.counts)))throw Error('Incomplete recorded-head subtotal');
  const missing=Object.keys(row.counts).filter(f=>row.counts[f]===null).sort();
  if(JSON.stringify(missing)!==JSON.stringify([...row.missing_fields].sort()))throw Error('Missing fields mismatch');
  if(Object.keys(row.calculated).length!==Object.keys(data.formulas).length)throw Error('Unexpected subtotal');
  for(const [name,fields] of Object.entries(data.formulas)){
   if(new Set(fields).size!==fields.length||fields.some(f=>!(f in row.counts)))throw Error('Invalid subtotal components');
   const expected=fields.some(f=>row.counts[f]===null)?null:fields.reduce((sum,f)=>sum+row.counts[f]!,0);
   if(row.calculated[name]!==expected)throw Error('Subtotal mismatch');
  }
 }
 const subtotal=(kind:string)=>{const rows=data.records.filter(r=>r.unit_type===kind);return !rows.length||rows.some(r=>r.calculated.calculated_recorded_heads_subtotal==null)?null:rows.reduce((sum,r)=>sum+r.calculated.calculated_recorded_heads_subtotal!,0)};
 const geographic=subtotal('geographic_police_district'),special=subtotal('special_unit');
 if(data.validation.mirrorSubtotalsByUnitType.geographic_police_district!==geographic||data.validation.mirrorSubtotalsByUnitType.special_unit!==special)throw Error('Reporting scope mismatch');
 const combined=geographic===null||special===null?null:geographic+special;
 if(combined!==data.validation.mirrorCombinedSubtotal||data.validation.ncrbMinusMirror!==(combined===null||data.validation.ncrbTotal===null?null:data.validation.ncrbTotal-combined))throw Error('Reconciliation mismatch');
 for(const [field,comparison] of Object.entries(data.validation.categoryComparisons)){
  if(data.records.some(r=>!(field in r.counts)))throw Error('Unknown comparison category');
  const sum=data.records.some(r=>r.counts[field]===null)?null:data.records.reduce((sum,r)=>sum+r.counts[field]!,0);
  if(sum!==comparison.mirror)throw Error('Category comparison mismatch');
  const difference=data.validation.discrepancies[field];
  if(comparison.mirror!==comparison.ncrb&&(!difference||difference.mirror!==sum||difference.ncrb!==comparison.ncrb||difference.ncrb_minus_mirror!==(sum===null||comparison.ncrb===null?null:comparison.ncrb-sum)))throw Error('Unreported category discrepancy');
  if(comparison.mirror===comparison.ncrb&&difference)throw Error('Spurious category discrepancy');
 }
 if(Object.keys(data.validation.discrepancies).some(f=>!(f in data.validation.categoryComparisons)))throw Error('Unknown discrepancy category');
 if(data.validation.status==='matches'&&(combined!==data.validation.ncrbTotal||Object.keys(data.validation.discrepancies).length))throw Error('Incorrect validation status');
 return data;
}

export const headlineCategories=[
 ['calculated_rape_subtotal','Rape'],['calculated_assault_related_subtotal','Assault-related heads'],
 ['calculated_kidnapping_abduction_subtotal','Kidnapping / abduction'],['dowry_deaths','Dowry deaths'],
 ['cruelty_husband_relatives','Cruelty by husband / relatives'],['calculated_pocso_girl_child_subtotal','POCSO · girl-child heads'],
] as const;
const labels:Record<string,string>={
 protection_children_sexual_violence_pocso:'POCSO sections 4 & 6 · girl children',pocso_10:'POCSO sections 8 & 10 · girl children',
 pocso_12:'POCSO section 12 · girl children',pocso_14_15:'POCSO sections 14 & 15 · girl children',pocso_17_22:'POCSO sections 17–22 · girl children',
 kidnapping_abduction_women:'Kidnapping / abduction · basic section component',women_others:'Kidnapping / abduction · other component',
 rape_women:'Rape · women aged 18+',rape_girls:'Rape · girls under 18',murder_rape_gang:'Murder with rape / gang rape',
 stalking_women:'Stalking · women aged 18+',stalking_girls:'Stalking · girls under 18',
};
export function categoryLabel(field:string){return labels[field]??field.replaceAll('_',' ').replace(/^./,c=>c.toUpperCase())}
