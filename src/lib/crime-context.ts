import {z} from 'zod';
const row = z.object({
  id:z.string(), regionId:z.string(), cityId:z.string(), reportingArea:z.string(),
  geography:z.string(), category:z.string(), year:z.number().int(), count:z.number().int().nonnegative(),
  periodStart:z.string(), periodEnd:z.string(), neighbourhoodId:z.null(), timeBand:z.null(),
  femalePopulation:z.null(), normalizedRate:z.null(), eligibleForTraining:z.literal(false),
}).strict();
export const contextSchema=z.object({schemaVersion:z.literal(1), retrievedAt:z.string(),
  sourceUrl:z.string().url(), downloadUrl:z.string().url(), sha256:z.string().regex(/^[a-f0-9]{64}$/),
  publisher:z.string(), licence:z.string(), limitations:z.array(z.string()).min(1),records:z.array(row),
}).strict();
export type CrimeContext=z.infer<typeof contextSchema>;
export function loadCrimeContext(data:unknown){
  const result=contextSchema.parse(data);
  if(new Set(result.records.map(r=>r.id)).size!==result.records.length)throw Error('Duplicate context IDs');
  return result;
}
