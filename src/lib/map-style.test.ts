import {createRequire} from 'node:module';
import {describe,it,expect} from 'vitest';
import type {Map as GLMap} from 'maplibre-gl';
import {filterRisk,restoreRisk} from './map-state';
import regions from '../../public/data/regions.json';
import samples from '../../public/data/delhi-ncr/sample.json';
import {loadRisk} from './risk';

// Use the validator bundled with our installed renderer, so syntax is checked
// against the same style-spec version the browser actually uses.
const require=createRequire(import.meta.url);
const rendererRequire=createRequire(require.resolve('maplibre-gl/package.json'));
const {validateStyleMin}=rendererRequire('@maplibre/maplibre-gl-style-spec');
describe('renderer style validation',()=>{
  it('accepts every risk layer with populated and empty city filters',()=>{
    const sources:Record<string,unknown>={},layers:Record<string,unknown>[]=[],images=new Set<string>();
    const map={getSource:(id:string)=>sources[id],addSource:(id:string,source:unknown)=>{sources[id]=source},
      getLayer:(id:string)=>layers.find(l=>l.id===id),addLayer:(layer:Record<string,unknown>)=>layers.push(layer),
      hasImage:(id:string)=>images.has(id),addImage:(id:string)=>images.add(id),
      setFilter:(id:string,filter:unknown)=>{layers.find(l=>l.id===id)!.filter=filter}} as unknown as GLMap;
    const records=loadRisk(samples);
    restoreRisk(map,regions[0],records,true);
    for(const selection of [records,records.slice(0,3),[]]){
      filterRisk(map,selection);
      expect(validateStyleMin({version:8,sources,layers}).map((e:{message:string})=>e.message)).toEqual([]);
    }
  });
});
