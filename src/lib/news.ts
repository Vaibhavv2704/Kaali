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
const incident=reference.extend({kind:z.literal('incident-report'),origin:z.literal('news'),
  neighbourhoodId:z.null(),observationCoverage:z.literal('unknown'),
  sha256:z.string().regex(/^[a-f0-9]{64}$/),retrievedAt:z.string().datetime({offset:true}),licence:z.string().min(1),
  event:z.object({id:z.string().min(1),locality:z.string().min(1),date:z.string().date().nullable(),
    dateBasis:z.enum(['explicit','day-month-with-publication-year','unknown']),
    timeBand:z.number().int().min(0).max(5).nullable(),category:z.enum(['molestation','rape','harassment','sexual-assault']),
    status:z.literal('reported-allegation')}).strict(),
}).strict().superRefine((r,c)=>{
  if((r.event.date===null)!==(r.event.dateBasis==='unknown'))c.addIssue({code:'custom',message:'Event date basis mismatch'});
  if(r.event.date&&r.event.date>r.publishedAt)c.addIssue({code:'custom',message:'Event after publication'});
});
const schema=z.array(z.union([reference,extracted,incident]));
export function loadNews(data:unknown){
  const rows=schema.parse(data);
  const urls=rows.map(r=>{const u=new URL(r.url);u.hash='';u.search='';return u.toString()});
  if(new Set(urls).size!==rows.length||new Set(rows.map(r=>r.id)).size!==rows.length)throw Error('Duplicate news reference');
  const events=rows.flatMap(r=>'event' in r?[r.event.id]:[]);
  if(new Set(events).size!==events.length)throw Error('Duplicate event; merge corroborating sources before publication');
  return rows;
}
export type NewsReference=ReturnType<typeof loadNews>[number];
