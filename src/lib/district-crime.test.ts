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
 it('rejects omitted comparison heads, subtotal components and inconsistent reporting years',()=>{
  const missingComparison=structuredClone(input);
  delete (missingComparison.validation.categoryComparisons as Record<string,unknown>).stalking_women;
  expect(()=>loadDistrictCrime(missingComparison)).toThrow('Incomplete category comparisons');
  const missingHead=structuredClone(input);
  missingHead.formulas.calculated_recorded_heads_subtotal.pop();
  expect(()=>loadDistrictCrime(missingHead)).toThrow();
  expect(()=>loadDistrictCrime({...input,validation:{...input.validation,reportingYear:2022}})).toThrow('Invalid recorded-head scope');
  expect(()=>loadDistrictCrime({...input,validation:{...input.validation,discrepancies:{...input.validation.discrepancies,
   invented:{mirror:1,ncrb:2,ncrb_minus_mirror:1,pdf_page:1}}}})).toThrow('Unknown discrepancy category');
 });
 it('does not present an absent special-unit series as an observed zero',()=>{
  const data=structuredClone(input);
  data.records=data.records.filter(r=>r.unit_type==='geographic_police_district');
  data.validation.mirrorSubtotalsByUnitType.special_unit=0;
  data.validation.mirrorCombinedSubtotal=data.validation.mirrorSubtotalsByUnitType.geographic_police_district;
  data.validation.ncrbMinusMirror=data.validation.ncrbTotal-data.validation.mirrorCombinedSubtotal;
  expect(()=>loadDistrictCrime(data)).toThrow('Reporting scope mismatch');
 });
});
