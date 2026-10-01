import {useEffect,useId,useState} from 'react';
import {Button,Card,Sheet,Skeleton} from './ui';
import {categoryLabel,formatCases,headlineCategories,loadDistrictCrime,type DistrictCrime} from '../lib/district-crime';

export default function DistrictRecords({compact=false,file,cityName,regionId,cityId}:{compact?:boolean;file:string;cityName:string;regionId:string;cityId:string}){
 const [data,setData]=useState<DistrictCrime|null>(null),[error,setError]=useState(false),[retry,setRetry]=useState(0);
 const [open,setOpen]=useState(false),[selected,setSelected]=useState('Rohini');
 const selectId=useId();
 useEffect(()=>{const controller=new AbortController();setError(false);setData(null);
  fetch(file,{signal:controller.signal}).then(r=>{if(!r.ok)throw Error();return r.json()}).then(loadDistrictCrime)
   .then(result=>{if(result.regionId!==regionId||result.cityId!==cityId)throw Error('Wrong reporting area');if(!controller.signal.aborted)setData(result)}).catch(()=>{if(!controller.signal.aborted)setError(true)});
  return()=>controller.abort();
 },[retry,file,regionId,cityId]);
 if(error)return <section className="home-crime-records"><h2>{cityName} police-district records</h2><p role="status">Records could not load.</p><Button variant="secondary" onClick={()=>setRetry(n=>n+1)}>Try again</Button></section>;
 if(!data||data.cityId!==cityId||data.regionId!==regionId)return <Skeleton/>;
 const row=data.records.find(r=>r.registration_circles===selected)??data.records[0];
 const details=<div className="district-records">
  <p>Calendar year {data.year} · historical registered cases. Police districts are reporting areas; these counts do not describe individual localities or current danger.</p>
  <div className="district-reconciliation" role="note"><h3>Source comparison</h3><p>Downloaded district heads: <b>{formatCases(data.validation.mirrorCombinedSubtotal)}</b> across all reporting units. NCRB {data.validation.officialGeography} total: <b>{formatCases(data.validation.ncrbTotal)}</b>.</p>{data.validation.status==='unresolved_discrepancy'?<><p>Difference: {formatCases(data.validation.ncrbMinusMirror)} cases. Its district distribution is unknown. Values below retain the downloaded cells.</p>{Object.entries(data.validation.discrepancies).map(([field,d])=><p key={field}>{categoryLabel(field)}: district mirror {formatCases(d.mirror)}; NCRB {formatCases(d.ncrb)}.</p>)}</>:<p>The combined category counts match the published total; this does not independently verify every district cell.</p>}</div>
  <label className="district-picker" htmlFor={selectId}>Choose a police reporting unit<select id={selectId} value={row.registration_circles} onChange={e=>setSelected(e.target.value)}>
   <optgroup label="Geographic police districts">{data.records.filter(r=>r.unit_type==='geographic_police_district').map(r=><option key={r.registration_circles}>{r.registration_circles}</option>)}</optgroup>
   <optgroup label="Special units · separate from districts">{data.records.filter(r=>r.unit_type==='special_unit').map(r=><option key={r.registration_circles}>{r.registration_circles}</option>)}</optgroup>
  </select></label>
  <section aria-live="polite" aria-atomic="true" className="district-selected"><h3>{row.district_name} · {data.year}</h3><p>{row.unit_type==='special_unit'?'Special police unit · not a geographic district':'Geographic police district'}</p>
   <div className="district-total"><strong>{formatCases(row.calculated.calculated_recorded_heads_subtotal)}</strong><span>Calculated recorded-head subtotal<br/>Mirror-derived; not a confirmed official district total</span></div>
   <div className="district-category-grid">{headlineCategories.map(([key,label])=><div className="district-category" key={key}><span>{label}</span><b>{formatCases(key in row.calculated?row.calculated[key]:row.counts[key])}</b></div>)}</div>
   <p className="page-footnote">Selected categories only. Subtotals group their component heads; do not add them again to the recorded-head subtotal. POCSO here covers girl children only.</p>
   {row.missing_fields.length>0&&<p>Not published: {row.missing_fields.map(categoryLabel).join(', ')}. Missing cells are not zero.</p>}
  </section>
  <details className="district-all-heads"><summary>All {Object.keys(row.counts).length} recorded crime heads</summary><table className="coverage-table"><caption>{row.district_name} · {data.year} · original category cells</caption><thead><tr><th scope="col">Crime head</th><th scope="col">Registered cases</th></tr></thead><tbody>{Object.entries(row.counts).map(([field,value])=><tr key={field}><th scope="row">{categoryLabel(field)}</th><td>{formatCases(value)}</td></tr>)}</tbody></table></details>
  <details><summary>Reporting geography and calculation notes</summary><p>The source administrative name is “{row.source_administrative_district_name}”. It is retained for audit and is not used to place this police unit on the map. {cityId==='delhi'&&row.registration_circles==='Dwarka'&&'Dwarka’s 2024 administrative mapping is inconsistent with the older file.'}</p><p>Kidnapping’s basic field and POCSO sections 4/6 are components, not parent totals. Calculations use raw heads once. NCRB applies the Principal Offence Rule, so these counts do not enumerate all allegations or victims. No verified police-district boundary is attached.</p></details>
  <div className="district-sources"><a href={data.sourceUrl} target="_blank" rel="noreferrer">District CSV source ↗</a><a href={data.officialUrl} target="_blank" rel="noreferrer">Original NCRB {data.year} report ↗</a><a href={file} download>Download counts & source audit</a></div>
  <p className="page-footnote">Retrieved {data.retrievedAt}. {data.licence} These figures are an attributed extract from a secondary NCRB mirror with the discrepancy disclosed above.</p>
 </div>;
 if(compact)return <section className="home-crime-records" aria-label={`${cityName} police-district crime records`}><h2>{cityName} police-district records · {data.year}</h2><p><strong>{formatCases(data.validation.mirrorSubtotalsByUnitType.geographic_police_district)}</strong><br/><small>Calculated heads across {data.records.filter(r=>r.unit_type==='geographic_police_district').length} geographic police districts</small></p><p>Historical recorded volume · source comparison included</p><Button variant="secondary" onClick={()=>setOpen(true)}>Explore police districts</Button><Sheet title={`${cityName} police-district crime records`} open={open} onOpenChange={setOpen}>{details}</Sheet></section>;
 return <Card className="method-card full"><h2>{cityName} police-district records · {data.year}</h2>{details}</Card>;
}
