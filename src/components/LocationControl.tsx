import {nextHigherWindow} from '../lib/upcoming-risk';
import {useEffect,useMemo,useRef,useState} from 'react';
import {createPortal} from 'react-dom';
import {motion} from 'framer-motion';
import {Navigation,ShieldCheck,Share2,Phone,X} from 'lucide-react';
import type {Region,RiskRecord,HelpFeature,UserPosition} from '../types';
import {nearestPolice} from '../lib/geo';
import {timeContext,getScore,bands,displayLevel} from '../lib/risk';
import {locationSession} from '../lib/location-session';
import {resolveLocation} from '../lib/location-resolution';
import {Button,Glass,Sheet} from './ui';

type Props={region:Region;regions:Region[];onRegion:(id:string)=>void;records:RiskRecord[];onJurisdiction:(id:string)=>void;onFocus:(p:{lat:number;lng:number})=>void;onSelect:(r:RiskRecord)=>void;lang:string;onMessage:(s:string)=>void;helpFeatures:HelpFeature[];onPosition:(p:UserPosition|null)=>void;onClear:()=>void};
export default function LocationControl(props:Props){
 const {region,regions,records,onJurisdiction,onFocus,lang,onMessage,helpFeatures}=props;
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
 const status=!position?'':resolved?.status==='ambiguous'?'Boundary overlap prevents a reliable jurisdiction match. National helpline 112 remains available.':!resolved?.region?(inViewport?'Verified boundaries are not available here yet. We cannot confirm your neighbourhood or jurisdiction.':"We don’t cover your area yet. Helplines are still available."):!city?'Your region is covered, but your city jurisdiction could not be verified.':!neighbourhood?'Your city is identified. Neighbourhood risk estimates are not available yet.':'';
 useEffect(()=>{onJurisdiction(city?.helplineSet??'national')},[city,onJurisdiction]);
 useEffect(()=>{
   if(resolved?.region&&resolved.region.id!==region.id)latest.current.onRegion(resolved.region.id);
   if(neighbourhood&&neighbourhood.id!==lastSelected.current){lastSelected.current=neighbourhood.id;latest.current.onSelect(neighbourhood)}
   if(!neighbourhood&&lastSelected.current){lastSelected.current=null;latest.current.onClear()}
 },[resolved,region.id,neighbourhood]);
 const stop=()=>{session.current?.stop();session.current=null;setConsent(false)};
 const start=()=>{
   setConsent(false);
   if(!navigator.geolocation){onMessage('Location is unavailable in this browser. Search for a locality instead.');return}
   if(position){onFocus(position);setVisible(true);return}
   if(!session.current)session.current=locationSession(navigator.geolocation,p=>{
     latest.current.onPosition(p);
     if(!mounted.current)return;
     setPosition(p);setLocating(false);setVisible(Boolean(p));
     if(p){setClock(new Date());latest.current.onFocus(p)}
     else{lastSelected.current=null;latest.current.onClear();latest.current.onJurisdiction('national')}
   },()=>{if(mounted.current)latest.current.onMessage('Location was unavailable or denied. You can search for a locality instead.')});
   setLocating(true);session.current.start();
 };
 const share=async()=>{if(!position)return;const url=`https://www.openstreetmap.org/?mlat=${position.lat}&mlon=${position.lng}#map=16/${position.lat}/${position.lng}`;try{if(navigator.share)await navigator.share({title:'My current location',text:'My current location, shared from Kaali.',url});else onMessage('Native sharing is unavailable in this browser. Use your device’s location sharing app.')}catch(e){if((e as Error).name!=='AbortError')onMessage('Sharing could not be opened.')}};
 const card=<motion.div className="glass location-card" initial={{opacity:0,y:10}} animate={{opacity:1,y:0}}><div className="detail-title"><p className="eyebrow"><ShieldCheck size={14}/>YOUR SURROUNDINGS</p><Button variant="ghost" size="icon" aria-label="Hide location card" onClick={()=>setVisible(false)}><X size={16}/></Button></div><h2>{city?`${lang==='hi'?'आप यहाँ हैं':'You’re in'} ${neighbourhood?neighbourhood.name+', ':''}${city.name}.`:lang==='hi'?'आपकी जगह, आपकी निजता।':'Your location. Your privacy.'}</h2><span className="badge">{displayLevel(score)}</span><p>{status||`${next?`${lang==='hi'?'अगला अधिक अनुमानित जोखिम वाला समय':'Next higher estimated window'}: ${new Intl.DateTimeFormat(lang==='hi'?'hi-IN':'en-IN',{timeZone:timezone,weekday:'short',day:'numeric',month:'short'}).format(next.date)}, ${bands[next.band]}. `:''}${lang==='hi'?'मुख्य और रोशनी वाली सड़कों का विकल्प रखें। ज़रूरत पड़ने पर 112 पर कॉल करें।':score!==null&&score>=50?'Consider well-lit main roads, and share your plans with someone you trust. Keep 112 handy.':'Stay aware of your surroundings, keep a trusted contact handy, and choose a route that feels comfortable.'}`}</p>{police&&<p>Nearest mapped police station: {police.feature.properties.name} · {police.km.toFixed(1)} km straight-line distance.</p>}<p>{lang==='hi'?'यात्रियों के लिए: लाइसेंस प्राप्त टैक्सी चुनें और अपनी यात्रा की जानकारी साझा करें।':'Visitor tip: choose licensed cabs and well-lit routes. Check your pickup point before travelling.'}</p><div className="location-actions"><Button asChild><a href="tel:112"><Phone size={14}/>Call 112</a></Button><Button variant="secondary" onClick={share}><Share2 size={14}/>Share location</Button><Button variant="help" asChild><a href="/helplines">Helplines</a></Button></div>{status.includes('cover')&&<a className="text-link" href="/about#suggest">Suggest a city</a>}<button className="text-link" onClick={stop}>Turn location off & clear</button></motion.div>;
 return <><Glass><Button variant="ghost" onClick={()=>position?start():setConsent(true)} aria-label="Locate me" disabled={locating}><Navigation size={18}/><span className="action-label">{locating?'Locating…':lang==='hi'?'मेरी जगह':'Locate me'}</span></Button></Glass><Sheet open={consent} onOpenChange={setConsent} title={lang==='hi'?'अपनी जगह जानें':'A little context, just for you'}><p>{lang==='hi'?'आपकी अनुमति से, आपकी जगह का मिलान इसी डिवाइस पर होगा।':'With your permission, Kaali matches your location to neighbourhood boundaries on this device. Coordinates are never stored or sent to our servers.'}</p><p>Map providers receive the map viewport when tiles load. Your exact GPS coordinates are not sent to the geocoder. Sharing sends your location only when you choose “Share location”.</p><div className="sheet-actions"><Button onClick={start}>{lang==='hi'?'स्थान की अनुमति दें':'Allow location'}</Button><Button variant="ghost" onClick={()=>setConsent(false)}>Use search instead</Button></div></Sheet>{visible&&position&&document.getElementById('main')&&createPortal(card,document.getElementById('main')!)}</>;
}

