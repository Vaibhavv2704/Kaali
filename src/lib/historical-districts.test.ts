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
  const copy=structuredClone(loadHistoricalDistricts(data));copy.records[0].categories[0].count=null;
  copy.records[0].missingColumns=[3];
  copy.records[0].categoryMismatches.push({column:3,label:'Rape (Total a+b)',reported_parent:null,child_sum:copy.records[0].categories[1].count!+copy.records[0].categories[2].count!,difference:null});
  expect(loadHistoricalDistricts(copy).records[0].categories[0].count).toBeNull();
  copy.records[0].missingColumns=[];expect(()=>loadHistoricalDistricts(copy)).toThrow();
 });
 it('rejects missing, altered and duplicate discrepancy disclosures',()=>{
  for(const mutate of [
   (r:ReturnType<typeof loadHistoricalDistricts>['records'][number])=>{r.categoryMismatches=[]},
   (r:ReturnType<typeof loadHistoricalDistricts>['records'][number])=>{r.categoryMismatches[0].child_sum=0},
   (r:ReturnType<typeof loadHistoricalDistricts>['records'][number])=>{r.categoryMismatches[0].difference=0},
   (r:ReturnType<typeof loadHistoricalDistricts>['records'][number])=>{r.categoryMismatches.push({...r.categoryMismatches[0]})}
  ]){
   const copy=structuredClone(loadHistoricalDistricts(data));mutate(copy.records.find(r=>r.id==='Rohini')!);
   expect(()=>loadHistoricalDistricts(copy)).toThrow();
  }
 });
 it('rejects substituting a special unit for a geographic police district',()=>{
  const copy=structuredClone(data);copy.records[0].id='Railway';copy.records[0].name='Railway';
  expect(()=>loadHistoricalDistricts(copy)).toThrow();
 });
 it('never styles malformed numbers as a recorded-case band',()=>{
  for(const value of [NaN,Infinity,-1]){expect(()=>districtBand(value)).toThrow();expect(()=>districtDiameter(value)).toThrow()}
 });
 it('keeps published category inconsistencies without fixing either side',()=>{
  const rohini=loadHistoricalDistricts(data).records.find(r=>r.name==='Rohini')!;
  expect(rohini.categoryMismatches.find(c=>c.column===23)?.reported_parent).toBe(6);
  expect(rohini.categoryMismatches.find(c=>c.column===23)?.child_sum).toBe(2);
  expect(rohini.count).toBe(883);
 });
});
