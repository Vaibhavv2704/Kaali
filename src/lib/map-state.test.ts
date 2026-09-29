import {describe,it,expect,vi} from 'vitest';
import type {Map as GLMap} from 'maplibre-gl';
import {restoreRisk,selectFeature,applyScores,filterRisk,riskLayers} from './map-state';
import {loadRisk} from './risk';
import regions from '../../public/data/regions.json';
import samples from '../../public/data/delhi-ncr/sample.json';
const region=regions[0],records=loadRisk(samples);
function fakeMap(){const sources=new Set<string>(),layers=new Set<string>(),images=new Set<string>();return {getSource:vi.fn((id:string)=>sources.has(id)),addSource:vi.fn((id:string)=>sources.add(id)),hasImage:vi.fn((id:string)=>images.has(id)),addImage:vi.fn((id:string)=>images.add(id)),getLayer:vi.fn((id:string)=>layers.has(id)),addLayer:vi.fn((l:{id:string})=>layers.add(l.id)),setFeatureState:vi.fn(),setFilter:vi.fn(),clearStyle:()=>{sources.clear();layers.clear();images.clear()},layers};}
describe('map style lifecycle',()=>{it('restores all risk layers after theme style replacement without touching camera',()=>{const m=fakeMap();restoreRisk(m as unknown as GLMap,region,records,true);expect([...m.layers]).toEqual(riskLayers);restoreRisk(m as unknown as GLMap,region,records,true);expect(m.addSource).toHaveBeenCalledTimes(1);m.clearStyle();restoreRisk(m as unknown as GLMap,region,records,true);expect([...m.layers]).toEqual(riskLayers);expect(m.addSource).toHaveBeenCalledTimes(2)});it('clears previous selection and sets next feature state',()=>{const m=fakeMap();selectFeature(m as unknown as GLMap,region,true,'old','new');expect(m.setFeatureState.mock.calls).toEqual([[{source:'kaali-risk',id:'old'},{selected:false}],[{source:'kaali-risk',id:'new'},{selected:true}]])});it('updates scores without replacing source or layer',()=>{const m=fakeMap();applyScores(m as unknown as GLMap,region,records,true,0,'weekday','all','all');expect(m.setFeatureState).toHaveBeenCalledTimes(records.length);expect(m.addSource).not.toHaveBeenCalled();expect(m.addLayer).not.toHaveBeenCalled()})});

describe('risk layer filtering',()=>{
 it('filters every visual layer to selected records, including after style replacement',()=>{
  const m=fakeMap();restoreRisk(m as unknown as GLMap,region,records,true);
  const selected=records.slice(0,2);filterRisk(m as unknown as GLMap,selected);
  expect(m.setFilter.mock.calls).toEqual(riskLayers.map(id=>[id,['in',['get','id'],['literal',selected.map(r=>r.id)]]]));
  m.clearStyle();restoreRisk(m as unknown as GLMap,region,records,true);m.setFilter.mockClear();filterRisk(m as unknown as GLMap,selected);
  expect(m.setFilter).toHaveBeenCalledTimes(riskLayers.length);
 });
 it('hides all layers for a city without matching records',()=>{
  const m=fakeMap();restoreRisk(m as unknown as GLMap,region,records,true);filterRisk(m as unknown as GLMap,[]);
  expect(m.setFilter.mock.calls).toEqual(riskLayers.map(id=>[id,['==',['literal',1],0]]));
 });
 it('does not mutate layers while a replacement style has not loaded',()=>{
  const m=fakeMap();filterRisk(m as unknown as GLMap,records);expect(m.setFilter).not.toHaveBeenCalled();
 });
});
