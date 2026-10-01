import {z} from 'zod';
const feature=z.object({type:z.literal('Feature'),id:z.string(),geometry:z.object({type:z.literal('Point'),coordinates:z.tuple([z.number().min(-180).max(180),z.number().min(-90).max(90)])}).strict(),
 properties:z.object({id:z.string(),name:z.string(),cityId:z.string(),year:z.number().int(),count:z.number().int().nonnegative(),referenceName:z.string(),source:z.string().url(),crimeSource:z.string().url(),pointStatus:z.literal('approximate_reference'),meaning:z.string(),lastVerified:z.string()}).strict()}).strict();
const schema=z.object({type:z.literal('FeatureCollection'),features:z.array(feature)}).strict();
export type DistrictPoints=z.infer<typeof schema>;
export function loadDistrictPoints(input:unknown){const data=schema.parse(input);if(new Set(data.features.map(f=>f.id)).size!==data.features.length||data.features.some(f=>f.id!==f.properties.id))throw Error('Invalid reference identity');return data}
/** Historical reference years remain selectable without neighbourhood scores. */
export function mapRecordYears(records:{year:number|null}[],points:DistrictPoints,sample:boolean){
 return [...new Set([...records.flatMap(r=>r.year===null?[]:[r.year]),...(sample?[]:points.features.map(f=>f.properties.year))])].sort((a,b)=>b-a);
}
