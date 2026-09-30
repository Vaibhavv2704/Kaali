import {locationCopy,locationRiskLabel} from '../lib/location-copy';
import {nextHigherWindow} from '../lib/upcoming-risk';
import {useEffect,useMemo,useRef,useState} from 'react';
import {createPortal} from 'react-dom';
import {motion} from 'framer-motion';
import {Navigation,ShieldCheck,Share2,Phone,X} from 'lucide-react';
import type {Region,RiskRecord,HelpFeature,UserPosition} from '../types';
import {nearestPolice} from '../lib/geo';
import {timeContext,getScore,bands} from '../lib/risk';
import {locationSession} from '../lib/location-session';
import {resolveLocation} from '../lib/location-resolution';
import {Button,Glass,Sheet} from './ui';

type Props={region:Region;regions:Region[];onRegion:(id:string)=>void;records:RiskRecord[];onJurisdiction:(id:string)=>void;onFocus:(p:{lat:number;lng:number})=>void;onSelect:(r:RiskRecord)=>void;lang:string;onMessage:(s:string)=>void;helpFeatures:HelpFeature[];onPosition:(p:UserPosition|null)=>void;onClear:()=>void};
export default function LocationControl(props:Props){
 const {region,regions,records,onJurisdiction,onFocus,lang,onMessage,helpFeatures}=props;
 const copy=locationCopy(lang);
 const [consent,setConsent]=useState(false),[position,setPosition]=useState<UserPosition|null>(null),[locating,setLocating]=useState(false),[visible,setVisible]=useState(false),[clock,setClock]=useState(new Date());
 const [boundaries,setBoundaries]=useState(new Map<string,GeoJSON.FeatureCollection>());
 const latest=useRef(props);latest.current=props;
 const session=useRef<ReturnType<typeof locationSession>|null>(null),mounted=useRef(true),lastSelected=useRef<string|null>(null);
 useEffect(()=>{mounted.current=true;const timer=setInterval(()=>setClock(new Date()),60000);return()=>{mounted.current=false;clearInterval(timer);session.current?.stop();session.current=null}},[]);
 useEffect(()=>{
   const controller=new AbortController();
   const paths=[...new Set(regions.flatMap(r=>[r.boundaryFile,...r.cities.map(c=>c.boundaryFile)]).filter((v):v is string=>Boolean(v)))];
   for(const path of paths)fetch(path,{signal:controller.signal}).then(r=>{if(!r.ok)throw Error('Boundary unavailable');return r.json()}).then(data=>{
     if(!controller.signal.aborted&&data.type==='FeatureCollection'&&Array.isArray(data.features))setBoundaries(old=>new Map(old).set(path,data));
   }).catch(()=>{});
   return()=>controller.abort();
 },[regions]);
 const resolved=useMemo(()=>position?resolveLocation(regions,records,boundaries,position):null,[position,regions,records,boundaries]);
 const neighbourhood=resolved?.neighbourhood??null,city=resolved?.city??null;
 const timezone=resolved?.region?.timezone??region.timezone;
 const current=timeContext(timezone,clock),score=neighbourhood?getScore(neighbourhood,current.band,current.day):null;
 const next=neighbourhood?nextHigherWindow(neighbourhood,timezone,clock):null;
 const police=position&&city?nearestPolice(helpFeatures,position,city.id):null;
 const inViewport=position&&regions.some(r=>position.lat<=r.bounds.north&&position.lat>=r.bounds.south&&position.lng>=r.bounds.west&&position.lng<=r.bounds.east);
 const outside=Boolean(position&&!resolved?.region&&!inViewport&&resolved?.status!=='ambiguous');
 const status=!position?'':resolved?.status==='ambiguous'?copy.overlap:!resolved?.region?(inViewport?copy.boundaries:copy.outside):!city?copy.cityUnknown:!neighbourhood?copy.riskUnknown:'';
 useEffect(()=>{onJurisdiction(city?.helplineSet??'national')},[city,onJurisdiction]);
 useEffect(()=>{
   if(resolved?.region&&resolved.region.id!==region.id)latest.current.onRegion(resolved.region.id);
   if(neighbourhood&&neighbourhood.id!==lastSelected.current){lastSelected.current=neighbourhood.id;latest.current.onSelect(neighbourhood)}
   if(!neighbourhood&&lastSelected.current){lastSelected.current=null;latest.current.onClear()}
 },[resolved,region.id,neighbourhood]);
 const stop=()=>{session.current?.stop();session.current=null;setConsent(false)};
 const start=()=>{
   setConsent(false);
   if(!navigator.geolocation){onMessage(copy.unavailable);return}
   if(position){onFocus(position);setVisible(true);return}
   if(!session.current)session.current=locationSession(navigator.geolocation,p=>{
     latest.current.onPosition(p);
     if(!mounted.current)return;
     setPosition(p);setLocating(false);setVisible(Boolean(p));
     if(p){setClock(new Date());latest.current.onFocus(p)}
     else{lastSelected.current=null;latest.current.onClear();latest.current.onJurisdiction('national')}
   },()=>{if(mounted.current)latest.current.onMessage(locationCopy(latest.current.lang).denied)});
   setLocating(true);session.current.start();
 };
 const share=async()=>{if(!position)return;const url=`https://www.openstreetmap.org/?mlat=${position.lat}&mlon=${position.lng}#map=16/${position.lat}/${position.lng}`;try{if(navigator.share)await navigator.share({title:copy.shareTitle,text:copy.shareText,url});else onMessage(copy.shareUnavailable)}catch(e){if((e as Error).name!=='AbortError')onMessage(copy.shareError)}};
 const card=<motion.div className="glass location-card" initial={{opacity:0,y:10}} animate={{opacity:1,y:0}}>
   <div className="detail-title"><p className="eyebrow"><ShieldCheck size={14}/>{copy.surroundings}</p><Button variant="ghost" size="icon" aria-label={copy.hide} onClick={()=>setVisible(false)}><X size={16}/></Button></div>
   <h2>{city?`${copy.greeting} ${neighbourhood?neighbourhood.name+', ':''}${city.name}.`:copy.privacy}</h2>
   <span className="badge">{locationRiskLabel(score,lang)}</span>
   <p>{status||`${next?`${copy.next}: ${new Intl.DateTimeFormat(lang==='hi'?'hi-IN':'en-IN',{timeZone:timezone,weekday:'short',day:'numeric',month:'short'}).format(next.date)}, ${bands[next.band]}. `:''}${score!==null&&score>=50?copy.higherTip:copy.lowerTip}`}</p>
   {score!==null&&<p className="page-footnote">{copy.estimate}</p>}
   {police&&<p>{copy.police}: {police.feature.properties.name} · {police.km.toLocaleString(lang==='hi'?'hi-IN':'en-IN',{minimumFractionDigits:1,maximumFractionDigits:1})} {copy.distance}</p>}
   <p>{copy.visitor}</p>
   <div className="location-actions"><Button asChild><a href="tel:112"><Phone size={14}/>{copy.call}</a></Button><Button variant="secondary" onClick={share}><Share2 size={14}/>{copy.share}</Button><Button variant="help" asChild><a href="/helplines">{copy.helplines}</a></Button></div>
   {outside&&<a className="text-link" href="/about#suggest">{copy.suggest}</a>}<button className="text-link" onClick={stop}>{copy.stop}</button>
 </motion.div>;
 return <><Glass><Button variant="ghost" onClick={()=>position?start():setConsent(true)} aria-label={copy.locate} disabled={locating}><Navigation size={18}/><span className="action-label">{locating?copy.locating:copy.locate}</span></Button></Glass>
   <Sheet open={consent} onOpenChange={setConsent} title={copy.title} closeLabel={lang==='hi'?'बंद करें':'Close'} description={copy.consent}><p>{copy.consent}</p><p>{copy.providers}</p><div className="sheet-actions"><Button onClick={start}>{copy.allow}</Button><Button variant="ghost" onClick={()=>setConsent(false)}>{copy.search}</Button></div></Sheet>
   {visible&&position&&document.getElementById('main')&&createPortal(card,document.getElementById('main')!)}
 </>;
}
