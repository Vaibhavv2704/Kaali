import {z} from 'zod';
const reference=z.object({id:z.string(),regionId:z.string(),cityId:z.string(),
  headline:z.string().min(1).max(180),publisher:z.string(),publishedAt:z.string(),
  url:z.string().url().refine(s=>s.startsWith('https://')),reviewedAt:z.string(),
  privacyReviewed:z.literal(true),kind:z.literal('aggregate-report'),eligibleForTraining:z.literal(false),
}).strict();
const extracted=reference.extend({
  facts:z.array(z.object({category:z.enum(['rape','molestation','eve-teasing']),year:z.number().int().min(1900),count:z.number().int().nonnegative()}).strict()).min(1),
  origin:z.literal('news'),neighbourhoodId:z.null(),timeBand:z.null(),
  sha256:z.string().regex(/^[a-f0-9]{64}$/),retrievedAt:z.string().datetime({offset:true}),licence:z.string().min(1),
}).strict().superRefine((r,ctx)=>{
  const keys=r.facts.map(f=>`${f.category}:${f.year}`);
  if(new Set(keys).size!==keys.length)ctx.addIssue({code:'custom',message:'Duplicate news category/year'});
  if(r.facts.some(f=>f.year>=Number(r.publishedAt.slice(0,4))))ctx.addIssue({code:'custom',message:'Only reviewed complete calendar years supported'});
});
const schema=z.array(z.union([reference,extracted]));
export function loadNews(data:unknown){
  const rows=schema.parse(data);
  const urls=rows.map(r=>{const u=new URL(r.url);u.hash='';u.search='';return u.toString()});
  if(new Set(urls).size!==rows.length||new Set(rows.map(r=>r.id)).size!==rows.length)throw Error('Duplicate news reference');
  return rows;
}
export type NewsReference=ReturnType<typeof loadNews>[number];
