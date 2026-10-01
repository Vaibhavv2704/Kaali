import {describe,it,expect} from 'vitest';
import {readFileSync} from 'node:fs';
const points=JSON.parse(readFileSync(new URL('../../public/data/delhi-ncr/district-reference-points.geojson',import.meta.url),'utf8'));
import records from '../../public/data/delhi-district-crime.json';
import {loadDistrictPoints} from './district-points';
describe('historical map references',()=>{
 it('retains historical subtotals and source-backed points without assigning boundaries',()=>{
  const data=loadDistrictPoints(points);expect(data.features).toHaveLength(3);
  for(const f of data.features){expect(f.properties.pointStatus).toBe('approximate_reference');
   expect(f.properties.count).toBe(records.records.find(r=>r.registration_circles===f.id)?.calculated.calculated_recorded_heads_subtotal);
   expect(f.properties.source).toContain('openstreetmap.org/node/');expect(f.geometry.type).toBe('Point');}
 });
 it('rejects danger polygons and duplicate reference identities',()=>{
  expect(()=>loadDistrictPoints({...points,features:[...points.features,points.features[0]]})).toThrow();
  expect(()=>loadDistrictPoints({...points,features:[{...points.features[0],geometry:{type:'Polygon',coordinates:[]}}]})).toThrow();
 });
});
