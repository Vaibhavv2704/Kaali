import {describe,it,expect} from 'vitest';
import raw from '../../public/data/ncr-historical-districts.json';
import {loadNcrDistricts} from './ncr-districts';
import {contextScenario,mappedTransitNearby} from './context-scenario';
import type {HelpFeature} from '../types';
describe('NCR recorded data and assumed scenarios',()=>{
 it('preserves nineteen source reporting units and the selected-unit subtotal',()=>{
  const data=loadNcrDistricts(raw);expect(data.records).toHaveLength(19);expect(data.ncrRecordedSubtotal).toBe(18778);
  expect(data.records.find(r=>r.id==='Gautambudh Nagar')?.count).toBe(431);
  expect(data.records.some(r=>r.id==='Noida'||r.id==='Greater Noida')).toBe(false);
 });
 it('rejects an invented city split and misassigned state',()=>{
  const a=structuredClone(raw);a.records.find(r=>r.name==='Gautambudh Nagar')!.id='Noida';expect(()=>loadNcrDistricts(a)).toThrow();
  const b=structuredClone(raw);b.records.find(r=>r.name==='Gurugram')!.stateName='Uttar Pradesh';expect(()=>loadNcrDistricts(b)).toThrow();
 });
 it('rejects altered aggregate checks, history and omitted source discrepancies',()=>{
  const a=structuredClone(raw);a.ncrRecordedSubtotal++;expect(()=>loadNcrDistricts(a)).toThrow();
  const b=structuredClone(raw);b.records[0].history.find(h=>h.year===2024)!.count++;expect(()=>loadNcrDistricts(b)).toThrow();
  const c=structuredClone(raw);c.records.find(r=>r.name==='Rohini')!.categoryMismatches=[];expect(()=>loadNcrDistricts(c)).toThrow();
 });
 it('returns unknown when activity/history is missing rather than assuming quiet means safe',()=>{
  expect(contextScenario(null,[1,2],5,0)).toBeNull();expect(contextScenario(1,[1,2],0,0)).toBeNull();expect(contextScenario(1,[1],4,0)).toBeNull();expect(contextScenario(1,[1,2],4,6)).toBeNull();
 });
 it('keeps judgement factors separate and does not mutate recorded cases',()=>{
  const counts=[100,500,1000];const day=contextScenario(500,counts,10,2)!,night=contextScenario(500,counts,10,5)!;
  expect(night.score).toBeGreaterThan(day.score);expect(night.dataType).toBe('assumed-scenario');expect(night.confidence).toBe('low');expect(counts).toEqual([100,500,1000]);
 });
 it('uses proximity to mapped transit as a proxy, excluding hospitals and distant stops',()=>{
  const features:HelpFeature[]=[['bus',77.2,28.6],['metro',78,29],['hospital',77.2,28.6]].map(([kind,lng,lat],i)=>({type:'Feature',geometry:{type:'Point',coordinates:[Number(lng),Number(lat)]},properties:{id:String(i),name:'Fixture',kind:kind as HelpFeature['properties']['kind'],cityId:'',source:'https://example.org',lastVerified:'2026-10-02'}}));
  expect(mappedTransitNearby([77.2,28.6],features)).toBe(1);
 });
});
