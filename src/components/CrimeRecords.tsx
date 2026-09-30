import {useEffect,useState} from 'react';
import type {Region} from '../types';
import {loadCrimeContext,type CrimeContext} from '../lib/crime-context';
import {loadNews,type NewsReference} from '../lib/news';
import {bands} from '../lib/risk';
import {Button,Sheet} from './ui';

export default function CrimeRecords({region,city}:{region:Region;city:string}){
 const [context,setContext]=useState<CrimeContext|null>(null),[news,setNews]=useState<NewsReference[]>([]),[open,setOpen]=useState(false),[locality,setLocality]=useState<string|null>(null),[error,setError]=useState(false);
 useEffect(()=>{const abort=new AbortController();const read=async(url:string)=>{const r=await fetch(url,{signal:abort.signal});if(!r.ok)throw Error();return r.json()};Promise.all([read('/data/crime-context.json').then(loadCrimeContext),read('/data/news.json').then(loadNews)]).then(([c,n])=>{setContext(c);setNews(n)}).catch(e=>{if(e.name!=='AbortError')setError(true)});return()=>abort.abort()},[]);
 useEffect(()=>setLocality(null),[city,region.id]);
 const matches=(r:{regionId:string;cityId:string})=>r.regionId===region.id&&(city==='all'||r.cityId===city);
 const rows=context?.records.filter(matches)??[];
 const latest=rows.filter(r=>!rows.some(other=>other.cityId===r.cityId&&other.year>r.year));
 const reports=news.filter(matches);
 const localities=[...new Set(reports.flatMap(r=>'event' in r?[r.event.locality]:[]))];
 const events=reports.filter(r=>'event' in r&&r.event.locality===locality);
 return <section className="home-crime-records" aria-label="Available crime records"><h2>Available crime records</h2>
 {latest.map(r=><p key={r.id}><strong>{r.count.toLocaleString('en-IN')}</strong> reported cases<br/><small>{r.reportingArea} · {r.year} · NCRB</small></p>)}
 {!latest.length&&<p>{error?'Records could not load. Try reloading the page.':context?'Coverage expanding for this city.':'Loading records…'}</p>}
 <Button variant="secondary" onClick={()=>setOpen(true)}>Crime breakdown & localities</Button>
 <Sheet open={open} onOpenChange={setOpen} title="Available crime records">
 <p>Published reporting areas and years are shown below. City totals describe the whole reporting area; they are not locality counts.</p>
 {latest.map(r=><section key={r.id}><h3>{r.reportingArea} · {r.year}</h3><p><strong>{r.count.toLocaleString('en-IN')}</strong> registered cases · {r.category}</p><a href={context!.sourceUrl} target="_blank" rel="noreferrer">NCRB / OpenCity source ↗</a></section>)}
 <h3>Category breakdown · published news figures</h3>
 {reports.filter(r=>'facts' in r).map(r=>'facts' in r&&<section key={r.id}><p>{region.cities.find(c=>c.id===r.cityId)?.name} · {r.publisher}</p><table className="coverage-table"><thead><tr><th>Category</th><th>Year</th><th>Reported cases</th></tr></thead><tbody>{r.facts.map(f=><tr key={`${f.category}-${f.year}`}><td>{f.category}</td><td>{f.year}</td><td>{f.count.toLocaleString('en-IN')}</td></tr>)}</tbody></table><a href={r.url} target="_blank" rel="noreferrer">Read source ↗</a></section>)}
 {!reports.some(r=>'facts' in r)&&<p>Category coverage is expanding. Available city records are listed above.</p>}
 <p>Category figures retain source wording and are not added to overlapping official totals.</p>
 <h3>Explore locality records</h3>
 {localities.map(name=><Button key={name} variant="secondary" aria-pressed={locality===name} onClick={()=>setLocality(name)}>{name}</Button>)}
 {!localities.length&&<p>Locality coverage is expanding.</p>}
 {locality&&<section aria-live="polite"><h3>{locality}</h3><p>{events.length} reviewed event reference{events.length===1?'':'s'}. This is the collection count, not the locality’s total crimes.</p>{events.map(r=>'event' in r&&<article key={r.id}><h4>{r.event.category} · reported allegation</h4><p>{r.event.date??'Date unspecified'} · {r.event.timeBand===null?'Time unspecified':bands[r.event.timeBand]+' IST'}</p>{r.event.dateBasis==='day-month-with-publication-year'&&<small>Year inferred from publication context.</small>}<p><a href={r.url} target="_blank" rel="noreferrer">{r.headline} ↗</a></p></article>)}</section>}
 <p><a href="/evidence">All sources and notable cases ↗</a></p>
 </Sheet></section>;
}
