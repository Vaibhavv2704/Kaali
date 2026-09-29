import {z} from 'zod';
const schema=z.array(z.object({id:z.string(),regionId:z.string(),cityId:z.string(),
  headline:z.string().min(1).max(180),publisher:z.string(),publishedAt:z.string(),
  url:z.string().url().refine(s=>s.startsWith('https://')),reviewedAt:z.string(),
  privacyReviewed:z.literal(true),kind:z.literal('aggregate-report'),eligibleForTraining:z.literal(false),
}).strict());
export function loadNews(data:unknown){
  const rows=schema.parse(data);
  const urls=rows.map(r=>{const u=new URL(r.url);u.hash='';u.search='';return u.toString()});
  if(new Set(urls).size!==rows.length||new Set(rows.map(r=>r.id)).size!==rows.length)throw Error('Duplicate news reference');
  return rows;
}
export type NewsReference=ReturnType<typeof loadNews>[number];
