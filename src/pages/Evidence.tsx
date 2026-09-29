import {useEffect,useState} from 'react';
import {Database,UserRound,ArrowUpRight} from 'lucide-react';
import type {Region} from '../types';
import {loadOffenders,type Offender} from '../lib/offenders';
import {loadCrimeContext,type CrimeContext} from '../lib/crime-context';
import {loadNews,type NewsReference} from '../lib/news';
import {Card,Skeleton} from '../components/ui';

export default function Evidence({region}:{region:Region}){
  const [city,setCity]=useState(region.cities[0]?.id??'');
  const [context,setContext]=useState<CrimeContext|null>(null);
  const [offenders,setOffenders]=useState<Offender[]>([]);
  const [news,setNews]=useState<NewsReference[]>([]);
  const [error,setError]=useState('');
  useEffect(()=>{const controller=new AbortController();
    const fetchJSON=async(url:string)=>{const response=await fetch(url,{signal:controller.signal});if(!response.ok)throw Error('Evidence could not be loaded. Please reload to try again.');return response.json()};
    Promise.all([fetchJSON('/data/crime-context.json').then(loadCrimeContext),fetchJSON('/data/offenders.json').then(loadOffenders),fetchJSON('/data/news.json').then(loadNews)])
      .then(([data,cases,coverage])=>{setContext(data);setOffenders(cases);setNews(coverage)})
      .catch(e=>{if(e.name!=='AbortError')setError(e.message)});
    return()=>controller.abort();
  },[]);
  const selected=region.cities.some(c=>c.id===city)?city:region.cities[0]?.id;
  const rows=context?.records.filter(r=>r.regionId===region.id&&r.cityId===selected)??[];
  const cases=offenders.filter(o=>o.regionId===region.id&&o.cityId===selected);
  return <main className="page" id="main"><p className="eyebrow">SOURCES & PUBLIC RECORDS</p><h1>Evidence, in context.</h1>
    <p className="lead">Historical crime statistics and documented adult convictions. These records do not predict anyone’s safety or indicate where a person lives.</p>
    <label className="evidence-city">City <select value={selected} onChange={e=>setCity(e.target.value)}>{region.cities.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}</select></label>
    {error?<p role="alert">{error}</p>:!context?<Skeleton/>:<>
    <div className="method-grid" style={{marginTop:24}}><Card className="method-card full"><Database size={24}/><h2>Reported crime · historical totals</h2>
      {rows.length?<><p>{rows[0].reportingArea} · {rows[0].geography}. {rows[0].category}.</p>
      <table className="coverage-table"><caption>Full calendar years; counts of registered cases</caption><thead><tr><th scope="col">Year</th><th scope="col">Reported cases</th></tr></thead><tbody>{rows.map(r=><tr key={r.id}><th scope="row">{r.year}</th><td className="stat-number">{r.count.toLocaleString('en-IN')}</td></tr>)}</tbody></table></>:<p>No admissible city statistics have been imported for this city. This means missing data, not an absence of crime.</p>}
      <p>No neighbourhood or time-of-day estimates can be derived from this table alone. No rate or cross-city ranking is shown while female-population exposure is unverified.</p>
      <a className="text-link" href={context.sourceUrl} target="_blank" rel="noreferrer">NCRB / OpenCity source <ArrowUpRight size={14}/></a><p className="page-footnote">Retrieved {context.retrievedAt}. {context.licence}.</p>
      <details><summary>Data limitations</summary><ul>{context.limitations.map(text=><li key={text}>{text}</li>)}</ul></details>
    </Card></div>
    <h2 style={{marginTop:32}}>News coverage</h2>
    <p>News-derived figures and curated links with neutral editorial headlines. Publisher articles may contain sensitive details. Figures retain the publisher’s category labels; legal classifications have not been harmonised. These reports are not added to official totals, conviction profiles or model labels.</p>
    <div className="bento-grid">{news.filter(n=>n.regionId===region.id&&n.cityId===selected).map(n=><Card key={n.id}><h3><a href={n.url} target="_blank" rel="noreferrer">{n.headline} ↗</a></h3><p>{n.publisher} · {n.publishedAt}</p>
      {'facts' in n&&<><table className="coverage-table"><caption>News-reported counts · city-wide, full calendar years</caption><thead><tr><th scope="col">Category</th><th scope="col">Year</th><th scope="col">Cases</th></tr></thead><tbody>{n.facts.map(f=><tr key={`${f.category}:${f.year}`}><th scope="row">{f.category}</th><td>{f.year}</td><td>{f.count.toLocaleString('en-IN')}</td></tr>)}</tbody></table><p className="page-footnote">No neighbourhood or incident-time data. These figures do not establish risk levels. {n.licence}</p></>}
      <small>Aggregate reporting · reviewed {n.reviewedAt}</small></Card>)}</div>
    {!news.some(n=>n.regionId===region.id&&n.cityId===selected)&&<p>No reviewed news links are available for this city yet.</p>}
    <h2 style={{marginTop:32}}>Convicted offenders / notable cases</h2>
    <p>Only reviewed adult convictions are listed. A case appears on the map only after its crime locality is verified against a neighbourhood boundary. This list is not a neighbourhood incident census.</p>
    <div className="bento-grid">{cases.map(o=><Card className="method-card" key={o.id}><UserRound size={28} aria-hidden="true"/><h3>{o.name}</h3><p>{o.caseName} · {o.year}</p><dl><dt>Court</dt><dd>{o.court}</dd><dt>Verdict</dt><dd>{o.verdict} · {o.convictionDate}</dd><dt>Sentence</dt><dd>{o.sentence}</dd><dt>Status</dt><dd>{o.status}</dd><dt>Crime locality</dt><dd>{o.locationVerified?o.crimeLocality:'Not verified for map placement'}</dd></dl><p>Neighbourhood incident total: unavailable.</p><p className="page-footnote">Last verified {o.lastVerified}</p>{o.sources.map((url,i)=><a className="resource-link" href={url} key={url} target="_blank" rel="noreferrer">Source {i+1} <ArrowUpRight size={12}/></a>)}</Card>)}</div>
    {!cases.length&&<Card><p>No reviewed conviction profiles are available for this city. This is not evidence of an absence of crime.</p></Card>}
    <p><a className="text-link" href="/about#corrections">Report an error / request removal</a></p></>}
  </main>;
}
