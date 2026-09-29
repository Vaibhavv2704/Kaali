import {describe,it,expect} from 'vitest';
import {mapPadding} from './map-layout';
describe('map camera padding',()=>{
  it('leaves at least 140px of interactive map above an expanded mobile sheet',()=>{
    for(const height of [480,640,844]){const p=mapPadding(390,height,1000);expect(height-p.top-p.bottom).toBeGreaterThanOrEqual(140)}
  });
  it('restores desktop padding after mobile resizing',()=>{
    expect(mapPadding(1440,1000,600)).toEqual(mapPadding(1440,1000,0));
    expect(mapPadding(390,844,180).bottom).toBeGreaterThan(mapPadding(390,844,0).bottom);
  });
});
