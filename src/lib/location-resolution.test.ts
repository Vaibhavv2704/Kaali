import {describe,it,expect} from 'vitest';
import type {FeatureCollection} from 'geojson';
import type {Region} from '../types';
import config from '../../public/data/regions.json';
import {resolveLocation} from './location-resolution';

const region={...config[0],boundaryFile:null,cities:[{...config[0].cities[0],boundaryFile:'/city.geojson'}]} as Region;
const boundary:FeatureCollection={type:'FeatureCollection',features:[{type:'Feature',properties:{},geometry:{type:'Polygon',coordinates:[[[0,0],[4,0],[4,4],[0,4],[0,0]]]}}]};
const p={lat:2,lng:2,accuracy:10};
describe('location resolution',()=>{
  it('can resolve city and helplines with no risk observations',()=>{
    const result=resolveLocation([region],[],new Map([['/city.geojson',boundary]]),p);
    expect(result.city?.helplineSet).toBe('delhi');expect(result.neighbourhood).toBeNull();
  });
  it('recomputes correctly when boundaries arrive after the GPS fix',()=>{
    expect(resolveLocation([region],[],new Map(),p).city).toBeNull();
    expect(resolveLocation([region],[],new Map([['/city.geojson',boundary]]),p).city?.id).toBe('delhi');
  });
  it('rejects border points and overlapping city jurisdictions',()=>{
    const cache=new Map([['/city.geojson',boundary]]);
    expect(resolveLocation([region],[],cache,{...p,lat:0,lng:0}).city).toBeNull();
    const overlap={...region,cities:[...region.cities,{...region.cities[0],id:'other'}]};
    expect(resolveLocation([overlap],[],cache,p).status).toBe('ambiguous');
  });
});
