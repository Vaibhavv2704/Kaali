import {describe,it,expect} from 'vitest';
import input from '../../public/data/delhi-district-crime.json';
import {loadDistrictCrime,formatCases} from './district-crime';
describe('historical district records',()=>{
 it('keeps police districts, administrative names and special units separate',()=>{
  const data=loadDistrictCrime(input);
  expect(data.records.filter(r=>r.unit_type==='geographic_police_district')).toHaveLength(15);
  expect(data.records.filter(r=>r.unit_type==='special_unit')).toHaveLength(8);
  const dwarka=data.records.find(r=>r.registration_circles==='Dwarka')!;
  expect(dwarka.source_administrative_district_name).toBe('Shahdara');
  expect(dwarka.district_name).toBe('Dwarka');expect(dwarka.boundary).toBeNull();
 });
 it('preserves the unresolved official comparison and reproduces Rohini subtotals',()=>{
  const data=loadDistrictCrime(input),row=data.records.find(r=>r.district_name==='Rohini')!;
  expect(row.calculated.calculated_recorded_heads_subtotal).toBe(879);
  expect(row.calculated.calculated_pocso_girl_child_subtotal).toBe(98);
  expect(data.validation.mirrorCombinedSubtotal).toBe(13295);
  expect(data.validation.ncrbTotal).toBe(13396);
  expect(data.validation.status).toBe('unresolved_discrepancy');
  expect(formatCases(null)).toBe('Not published');expect(formatCases(0)).toBe('0');
 });
 it('rejects altered formulas, district identities, inferred boundaries and inconsistent aggregates',()=>{
  const change=(mutate:(copy:typeof input)=>void)=>{const copy=structuredClone(input);mutate(copy);expect(()=>loadDistrictCrime(copy)).toThrow()};
  change(copy=>copy.formulas.calculated_rape_subtotal.push('rape_women'));
  change(copy=>copy.records[0].district_name='Other district');
  change(copy=>copy.records[0].calculated.calculated_recorded_heads_subtotal++);
  change(copy=>copy.validation.mirrorCombinedSubtotal++);
  change(copy=>(copy.records[0].missing_fields as string[]).push('rape_women'));
  expect(()=>loadDistrictCrime({...input,records:[...input.records,input.records[0]]})).toThrow();
  expect(()=>loadDistrictCrime({...input,records:input.records.map(r=>({...r,boundary:{type:'Polygon'}}))})).toThrow();
 });
});
