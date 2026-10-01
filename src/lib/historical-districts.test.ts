import {describe,it,expect} from 'vitest';
import data from '../../public/data/delhi-historical-districts.json';
import {districtBand,districtDiameter,loadHistoricalDistricts} from './historical-districts';
describe('historical district display',()=>{
 it('uses precisely the requested display bands, never danger labels',()=>{
  expect([null,0,499,500,999,1000,1500].map(districtBand)).toEqual(['unknown','pale','pale','medium','medium','strong','strong']);
 });
 it('uses the smooth pixel-diameter formula and preserves unknowns',()=>{
  expect(districtDiameter(0)).toBe(22);expect(districtDiameter(1500)).toBe(52);
  expect(districtDiameter(500)).toBeCloseTo(22+Math.sqrt(500/1500)*30);
  expect(districtDiameter(null)).toBeNull();expect(()=>districtDiameter(-1)).toThrow();
 });
 it('validates all 15 recorded totals separately from special units',()=>{
  const result=loadHistoricalDistricts(data);expect(result.records).toHaveLength(15);
  expect(result.geographicTotal!+result.specialUnitTotal!).toBe(13396);
  expect(result.records.find(r=>r.name==='Rohini')?.count).toBe(883);
  expect(result.records.every(r=>r.countType==='recorded_total'&&r.reference.status==='approximate_reference')).toBe(true);
 });
 it('rejects identity, totals and category omissions',()=>{
  expect(()=>loadHistoricalDistricts({...data,geographicTotal:0})).toThrow();
  expect(()=>loadHistoricalDistricts({...data,records:[data.records[0],...data.records.slice(1).map(()=>data.records[0])]})).toThrow();
  const copy=structuredClone(data);copy.records[0].categories.pop();expect(()=>loadHistoricalDistricts(copy)).toThrow();
 });
 it('preserves missing category values without converting them to zero',()=>{
  const copy=structuredClone(data);copy.records[0].categories[0].count=null as unknown as number;
  copy.records[0].missingColumns=[3] as never[];
  expect(loadHistoricalDistricts(copy).records[0].categories[0].count).toBeNull();
  copy.records[0].missingColumns=[];expect(()=>loadHistoricalDistricts(copy)).toThrow();
 });
 it('keeps published category inconsistencies without fixing either side',()=>{
  const rohini=loadHistoricalDistricts(data).records.find(r=>r.name==='Rohini')!;
  expect(rohini.categoryMismatches.find(c=>c.column===23)?.reported_parent).toBe(6);
  expect(rohini.categoryMismatches.find(c=>c.column===23)?.child_sum).toBe(2);
  expect(rohini.count).toBe(883);
 });
});
