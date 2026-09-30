import {describe,it,expect} from 'vitest';
import {loadRisk} from './risk';
import {rankRedZones} from './red-zones';
import samples from '../../public/data/delhi-ncr/sample.json';

const records=loadRisk(samples);
describe('red-zone ranking',()=>{
  it('ranks the selected time band and keeps unsupported filters unknown',()=>{
    const morning=rankRedZones(records,0,'weekday','all','all');
    const evening=rankRedZones(records,5,'weekday','all','all');
    expect(morning.ranked.length).toBe(records.length);
    expect(evening.ranked.map(zone=>zone.score)).not.toEqual(morning.ranked.map(zone=>zone.score));
    expect(evening.ranked.every((zone,index)=>index===0||zone.score<=evening.ranked[index-1].score)).toBe(true);
    expect(evening.high.every(zone=>zone.score>=50)).toBe(true);
    const unsupported=rankRedZones(records,5,'weekday','rape','all');
    expect(unsupported.ranked).toEqual([]);
    expect(unsupported.unknown).toBe(records.length);
  });
  it('does not promote missing scores to lower risk',()=>{
    const zone={...records[0],scores:{'weekday:all':null}};
    const result=rankRedZones([zone],3,'weekday','all','all');
    expect(result).toEqual({ranked:[],high:[],unknown:1});
  });
});
