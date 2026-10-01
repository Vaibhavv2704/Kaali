import {useEffect,useState} from 'react';
import {Database,ArrowUpRight} from 'lucide-react';
import type {Region} from '../types';
import {loadCrimeContext,type CrimeContext} from '../lib/crime-context';
import {loadNews,type NewsReference} from '../lib/news';
import {Card,Skeleton} from '../components/ui';
import {bands} from '../lib/risk';
import {loadNcrDistricts,type NcrDistricts} from '../lib/ncr-districts';

export default function Evidence({region}:{region:Region}){
  const [regional,setRegional]=useState<NcrDistricts|null>(null);
  const [context,setContext]=useState<CrimeContext|null>(null);
  const [news,setNews]=useState<NewsReference[]>([]);
  const [error,setError]=useState('');
  useEffect(()=>{const controller=new AbortController();
    const fetchJSON=async(url:string)=>{const response=await fetch(url,{signal:controller.signal});if(!response.ok)throw Error('Evidence could not be loaded. Please reload to try again.');return response.json()};
    Promise.all([fetchJSON('/data/crime-context.json').then(loadCrimeContext),fetchJSON('/data/news.json').then(loadNews),fetchJSON('/data/ncr-historical-districts.json').then(loadNcrDistricts)])
      .then(([data,coverage,ncr])=>{setContext(data);setNews(coverage);setRegional(ncr)})
      .catch(e=>{if(e.name!=='AbortError')setError(e.message)});
    return()=>controller.abort();
  },[]);
  const rows=context?.records.filter(r=>r.regionId===region.id)??[];
  return <main className="page" id="main"><p className="eyebrow">DELHI NCR · SOURCE RECORDS</p><h1>Crime data, in context.</h1>
    <p className="lead">Historical crime statistics and reviewed news coverage for Delhi NCR. Recorded cases do not establish current safety.</p>
    {regional&&<Card className="method-card full" style={{marginTop:24}}><h2>Delhi NCR · {regional.year} recorded district totals</h2><p>{regional.records.length} geographic reporting units · combined subtotal {regional.ncrRecordedSubtotal?.toLocaleString('en-IN')}. This is a calculated sum of the selected units' published totals, not an official whole-NCR series. Noida and Greater Noida remain one Gautam Buddh Nagar reporting unit.</p>{regional.records.map(r=><details key={r.id} className="ncr-evidence-record"><summary>{r.name} · {r.count?.toLocaleString('en-IN')??'Not published'} cases</summary><p>{r.stateName} · {r.year} · Recorded total, not a current safety classification.</p><table className="coverage-table"><caption>Selected source groups; parent categories and children must not be added together</caption><tbody>{r.categories.filter(c=>c.highlight).map(c=><tr key={c.column}><th scope="row">{c.highlight}</th><td>{c.count?.toLocaleString('en-IN')??'Not published'}</td></tr>)}</tbody></table>{r.categoryMismatches.map(c=><p key={c.column}>{c.label}: parent {c.reported_parent??'Missing'}, children {c.child_sum??'Missing'}. Retained as published.</p>)}</details>)}<a className="text-link" href={regional.sourceUrl} target="_blank" rel="noreferrer">NCRB source catalogue ↗</a><p className="page-footnote">{regional.provenanceNote}</p></Card>}
    {error?<p role="alert">{error}</p>:!context?<Skeleton/>:<>
    <div className="method-grid" style={{marginTop:24}}><Card className="method-card full"><Database size={24}/><h2>Reported crime · historical totals</h2>
      {rows.length?<><p>{rows[0].reportingArea} · {rows[0].geography}. {rows[0].category}.</p>
      <table className="coverage-table"><caption>Full calendar years; counts of registered cases</caption><thead><tr><th scope="col">Reporting area</th><th scope="col">Year</th><th scope="col">Reported cases</th></tr></thead><tbody>{rows.map(r=><tr key={r.id}><th scope="row">{r.reportingArea}</th><td>{r.year}</td><td className="stat-number">{r.count.toLocaleString('en-IN')}</td></tr>)}</tbody></table></>:<p>No admissible city statistics have been imported for this city. This means missing data, not an absence of crime.</p>}
      <p>No neighbourhood or time-of-day estimates can be derived from this table alone. No rate or cross-city ranking is shown while female-population exposure is unverified.</p>
      <a className="text-link" href={context.sourceUrl} target="_blank" rel="noreferrer">NCRB / OpenCity source <ArrowUpRight size={14}/></a><p className="page-footnote">Retrieved {context.retrievedAt}. {context.licence}.</p>
      <details><summary>Data limitations</summary><ul>{context.limitations.map(text=><li key={text}>{text}</li>)}</ul></details>
    </Card></div>
    <h2 style={{marginTop:32}}>News coverage</h2>
    <p>News-derived figures and curated links with neutral editorial headlines. Publisher articles may contain sensitive details. Figures retain the publisher’s category labels; legal classifications have not been harmonised. These reports are not added to official totals or model labels.</p>
    <div className="bento-grid">{news.filter(n=>n.regionId===region.id).map(n=><Card key={n.id}><h3><a href={n.url} target="_blank" rel="noreferrer">{n.headline} ↗</a></h3><p>{n.publisher} · {n.publishedAt}</p>
      {'facts' in n&&<><table className="coverage-table"><caption>News-reported counts · city-wide, full calendar years</caption><thead><tr><th scope="col">Category</th><th scope="col">Year</th><th scope="col">Cases</th></tr></thead><tbody>{n.facts.map(f=><tr key={`${f.category}:${f.year}`}><th scope="row">{f.category}</th><td>{f.year}</td><td>{f.count.toLocaleString('en-IN')}</td></tr>)}</tbody></table><p className="page-footnote">No neighbourhood or incident-time data. These figures do not establish risk levels. {n.licence}</p></>}
      {'event' in n&&<><dl><dt>Reported incident locality</dt><dd>{n.event.locality}</dd><dt>Incident date</dt><dd>{n.event.date??'Unknown'}{n.event.dateBasis==='day-month-with-publication-year'?' (year inferred from publication context)':''}</dd><dt>Reported time band</dt><dd>{n.event.timeBand===null?'Unknown':`${bands[n.event.timeBand]} IST`}</dd><dt>Source category</dt><dd>{n.event.category}</dd></dl><p>Reported allegation, not a conviction. One event reference; not a count of all crimes in this locality. No verified polygon match or training label.</p></>}
      <small>{n.kind==='incident-report'?'Incident reporting':'Aggregate reporting'} · reviewed {n.reviewedAt}</small></Card>)}</div>
    {!news.some(n=>n.regionId===region.id)&&<p>No reviewed news links are available for Delhi NCR yet.</p>}
    </>}
  </main>;
}
