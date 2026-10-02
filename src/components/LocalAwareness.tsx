import {useEffect,useMemo,useRef,useState} from 'react';
import {Link} from 'react-router-dom';
import {Share2,X} from 'lucide-react';
import {distance,point} from '@turf/turf';
import {Button,Glass,Sheet} from './ui';
import {locationSession} from '../lib/location-session';
import {currentPeriod,nearestReference,type LocalityContext} from '../lib/locality-context';
import type {UserPosition,HelpFeature} from '../types';
import {advisoryLevel,referenceAdvisory,localHour,precaution} from '../lib/advisory-risk';
import {type MLVolume} from '../lib/ml-volume';
export default function LocalAwareness({context,help,user,onPosition,onLocate,ml,center,timezone,locateRequest}:{locateRequest:number;center:{lat:number;lng:number};timezone:string;context:LocalityContext|null;help:HelpFeature[];user:UserPosition|null;onPosition:(u:UserPosition|null)=>void;onLocate:()=>void;regional:{year:number;count:number|null}|null;ml:MLVolume|null}){
 const [consent,setConsent]=useState(false),[enabled,setEnabled]=useState(false),[error,setError]=useState(''),[now,setNow]=useState(new Date());

 const session=useRef<ReturnType<typeof locationSession>|null>(null);
 useEffect(()=>{if(!navigator.geolocation)return;let mounted=true;session.current=locationSession(navigator.geolocation,onPosition,()=>{setEnabled(false);setError('Location was unavailable. You can still explore the map manually.');},{enableHighAccuracy:true,maximumAge:5000,timeout:20000});if(navigator.permissions)navigator.permissions.query({name:'geolocation'}).then(permission=>{if(mounted&&permission.state==='granted'){setEnabled(true);session.current?.start();}}).catch(()=>{});return()=>{mounted=false;session.current?.stop()}},[onPosition]);
 useEffect(()=>{const timer=setInterval(()=>setNow(new Date()),60000);return()=>clearInterval(timer)},[]);
 const nearest=useMemo(()=>user&&context?nearestReference(user,context.records):null,[user,context]);
 const police=useMemo(()=>{if(!user)return null;return help.filter(f=>f.properties.kind==='police'&&f.geometry.type==='Point').map(f=>({name:f.properties.name,km:distance(point([user.lng,user.lat]),point(f.geometry.coordinates as [number,number]),{units:'kilometers'})})).sort((a,b)=>a.km-b.km)[0]??null},[help,user]);
 const period=currentPeriod(now),r=nearest?.record;

 const hour=localHour(now,timezone),level=r?referenceAdvisory(ml,r,period.band,period.day,hour,context?.records??[],center):advisoryLevel(null,hour);
 const lastLocateRequest=useRef(0);
 useEffect(()=>{if(locateRequest===lastLocateRequest.current)return;lastLocateRequest.current=locateRequest;if(enabled)onLocate();else setConsent(true)},[locateRequest,enabled,onLocate]);
 const share=async()=>{if(!user)return;try{if(!navigator.share){setError('Use your device’s location-sharing app; native sharing is unavailable here.');return;}await navigator.share({title:'My current location',text:`My device location (approximately ±${Math.round(user.accuracy)} m): https://www.openstreetmap.org/?mlat=${user.lat}&mlon=${user.lng}#map=17/${user.lat}/${user.lng}`});}catch{setError('Location sharing was cancelled or unavailable.')}};
 return <><Sheet open={consent} onOpenChange={setConsent} title="Your location, on this device"><p>Show your device’s reported position and an awareness summary. Coordinates stay in memory here and are cleared when you stop. We do not send GPS to a geocoder or AI service. Map tiles reveal the viewed area to the map provider.</p><p>The blue dot is your device’s estimate; its accuracy circle is not a guarantee of an exact position.</p><Button onClick={()=>{setConsent(false);setError('');if(!session.current){setError('Location is unavailable in this browser.');return;}setEnabled(true);session.current.start();}}>Allow location</Button><Button variant="ghost" onClick={()=>setConsent(false)}>Continue without location</Button></Sheet>
 {enabled&&<Glass className="historical-location-card" aria-label="On-device location awareness"><div className="location-card-heading"><strong>{user?'Your surroundings':'Finding your location…'}</strong><Button size="icon" variant="ghost" aria-label="Stop location and clear position" onClick={()=>{session.current?.stop();setEnabled(false)}}><X size={18}/></Button></div>{user&&<><div className={`location-risk-badge risk-${level.toLowerCase().replace(' ','-')}`}>{level} · advisory level</div>{r&&<p className="location-reference-name">Near {r.name}</p>}<p className="location-advice-copy">{precaution(level)}</p><p className="historical-small">Model estimate with time-based advisory rules; not a guarantee of safety.</p><small>{new Intl.DateTimeFormat('en-IN',{timeZone:timezone,hour:'numeric',minute:'2-digit'}).format(now)} IST · GPS accuracy ±{Math.round(user.accuracy)} m</small>{police&&<p className="historical-small">Nearest mapped police reference: {police.name} · {police.km.toFixed(1)} km straight-line; availability unconfirmed.</p>}<div className="location-card-actions"><a href="tel:112">Call 112</a><Button size="small" variant="ghost" onClick={share}><Share2 size={16}/>Share location</Button><Link to="/helplines">Helplines</Link></div></>}</Glass>}{error&&<Glass className="historical-location-error" role="status">{error}<Button variant="ghost" size="small" onClick={()=>setError('')}>Dismiss</Button></Glass>}</>;
}
