import {describe,it,expect} from 'vitest';
import raw from '../../public/data/delhi-ncr/ml-volume.json';
import contextRaw from '../../public/data/delhi-ncr/locality-context.json';
import {mlVolumeSchema,mlIndex,mlCells,modelRiskLevel} from './ml-volume';
import {localitySchema} from './locality-context';
describe('trained count-volume scenario',()=>{
 const model=mlVolumeSchema.parse(raw),context=localitySchema.parse(contextRaw);
 it('encodes four display levels while preserving unknown',()=>{
  expect([0,24,25,49,50,74,75,100].map(modelRiskLevel)).toEqual(['Low','Low','Medium','Medium','High','High','Very high','Very high']);
  expect([null,NaN,-1,101].map(modelRiskLevel)).toEqual(['Unknown','Unknown','Unknown','Unknown']);
 });
 it('keeps learned forecasts separate from real totals and missing local cases',()=>{expect(model.model).toBe('poisson_glm');expect(model.anchors).toHaveLength(19);expect(model.anchors.some(a=>a.expectedAnnualCases!==a.recordedCases)).toBe(true);expect(model.localities.every(r=>r.reportedCases===null&&r.riskScore===null)).toBe(true);});
 it('requires both learned reference influence and activity before shading',()=>{const r=context.records.find(r=>r.traffic.weekday[5]!==null)!;expect(mlIndex(null,r,5,'weekday',context.records)).toBeNull();expect(mlIndex(model,r,5,'weekday',context.records)).not.toBeNull();const missing=context.records.find(r=>r.traffic.weekday[5]===null)!;expect(mlIndex(model,missing,5,'weekday',context.records)).toBeNull();});
 it('deduplicates cells and keeps model indices bounded',()=>{const cells=mlCells(model,context.records,5,'weekday');expect(cells.features).toHaveLength(129);for(const f of cells.features)if(f.properties.score!==null){expect(f.properties.score).toBeGreaterThanOrEqual(0);expect(f.properties.score).toBeLessThanOrEqual(100);}expect(()=>mlVolumeSchema.parse({...raw,localities:[{...raw.localities[0],reportedCases:44}]})).toThrow();});
});
