import {describe,it,expect} from 'vitest';
import {neighbourhoodAt,nearestPolice} from './geo';
import {loadRisk} from './risk';
import samples from '../../public/data/delhi-ncr/sample.json';
import type {RiskRecord,HelpFeature} from '../types';
const zone={...loadRisk(samples)[0],provenance:'unavailable',boundaryStatus:'verified',geometry:{type:'Polygon',coordinates:[[[0,0],[4,0],[4,4],[0,4],[0,0]],[[1,1],[2,1],[2,2],[1,2],[1,1]]]}} as RiskRecord;
describe('local spatial lookup',()=>{it('respects polygon holes and excludes boundary ambiguity',()=>{expect(neighbourhoodAt([zone],{lat:3,lng:3})?.id).toBe(zone.id);expect(neighbourhoodAt([zone],{lat:1.5,lng:1.5})).toBeNull();expect(neighbourhoodAt([zone],{lat:0,lng:0})).toBeNull()});it('rejects overlapping jurisdictions and sample matches',()=>{expect(neighbourhoodAt([zone,{...zone,id:'overlap'}],{lat:3,lng:3})).toBeNull();expect(neighbourhoodAt([{...zone,provenance:'sample'}],{lat:3,lng:3})).toBeNull()});it('filters nearest police by verified jurisdiction',()=>{const f=(id:string,cityId:string,lng:number):HelpFeature=>({type:'Feature',geometry:{type:'Point',coordinates:[lng,0]},properties:{id,cityId,kind:'police',name:id,source:'https://openstreetmap.org',lastVerified:'2026-09-29'}});expect(nearestPolice([f('wrong','other',.001),f('correct','delhi',.01)],{lat:0,lng:0},'delhi')?.feature.properties.id).toBe('correct')})});
