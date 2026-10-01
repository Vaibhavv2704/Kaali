import {useEffect,useMemo,useRef,useState} from 'react';
import Map,{Marker,AttributionControl,type MapRef} from 'react-map-gl/maplibre';
import maplibregl from 'maplibre-gl';
import {useReducedMotion} from 'framer-motion';
import {Plus,Minus,LocateFixed} from 'lucide-react';
import {Button,Glass} from './ui';
import {baseStyle} from '../lib/map-state';
import {districtBand,districtDiameter,type HistoricalDistrict} from '../lib/historical-districts';
import type {Bounds} from '../types';
import 'maplibre-gl/dist/maplibre-gl.css';

export default function HistoricalMapCanvas({districts,selectedId,theme,onSelect,bounds,center,openPanel}:{districts:HistoricalDistrict[];selectedId:string|null;theme:string;onSelect:(id:string)=>void;bounds:Bounds;center:{lat:number;lng:number};openPanel:'districts'|'details'|'legend'|null}){
 const ref=useRef<MapRef>(null),reduce=useReducedMotion();const [ready,setReady]=useState(false),[error,setError]=useState('');
 const key=import.meta.env.VITE_MAPTILER_KEY??'';const style=useMemo(()=>baseStyle(theme,key),[theme,key]);
 const padding=()=>window.innerWidth>760?{top:200,bottom:150,left:openPanel==='districts'?335:48,right:openPanel==='details'?365:48}:{top:180,bottom:openPanel==='details'||openPanel==='legend'?Math.min(window.innerHeight*.4+148,window.innerHeight-200):200,left:24,right:24};
 const recenter=()=>{ref.current?.fitBounds([[bounds.west,bounds.south],[bounds.east,bounds.north]],{padding:padding(),duration:reduce?0:700});};
 useEffect(()=>{const map=ref.current?.getMap();if(!map||!ready)return;const resize=()=>{map.resize();map.jumpTo({padding:padding()});};resize();const observer=new ResizeObserver(resize);observer.observe(map.getContainer());return()=>observer.disconnect();},[ready,openPanel]);
 useEffect(()=>{if(!ready)return;const record=districts.find(r=>r.id===selectedId);if(record)ref.current?.flyTo({center:record.reference.coordinates,zoom:11.8,padding:padding(),duration:reduce?0:650});},[selectedId,ready,reduce]);
 return <><Map ref={ref} mapLib={maplibregl} initialViewState={{longitude:center.lng,latitude:center.lat,zoom:10}} mapStyle={style} attributionControl={false} maxBounds={[bounds.west-.15,bounds.south-.15,bounds.east+.15,bounds.north+.15]} onLoad={()=>{setReady(true);recenter();}} onError={()=>setError('Some base-map tiles could not load. District records remain available.')}>
 {districts.map(d=>{const diameter=districtDiameter(d.count);return <Marker key={d.id} longitude={d.reference.coordinates[0]} latitude={d.reference.coordinates[1]} anchor="center" style={{zIndex:selectedId===d.id?2:1}}><button className={`historical-marker ${selectedId===d.id?'is-selected':''}`} aria-label={`${d.name} police district, ${d.count===null?'total missing':`${d.count} recorded cases`}, ${d.year}; approximate reference`} aria-pressed={selectedId===d.id} onClick={e=>{e.stopPropagation();onSelect(d.id);}} title={`${d.name} · ${d.count??'Not published'} cases · ${d.year}`}>
 <span className={`historical-circle band-${districtBand(d.count)}`} style={{width:diameter??24,height:diameter??24}}>{d.count===null?'?':d.count.toLocaleString('en-IN')}</span><span className="historical-marker-label">{d.name}</span></button></Marker>})}
 <AttributionControl position="bottom-right" compact={false} customAttribution="© MapTiler © OpenStreetMap contributors"/>
 </Map>{key&&<a className="historical-maptiler-logo" href="https://www.maptiler.com/" target="_blank" rel="noreferrer"><img src="https://api.maptiler.com/resources/logo.svg" alt="MapTiler" width="85" height="25"/></a>}<Glass className="historical-map-controls"><Button size="icon" variant="ghost" aria-label="Zoom in" onClick={()=>ref.current?.zoomIn({duration:reduce?0:250})}><Plus size={18}/></Button><Button size="icon" variant="ghost" aria-label="Zoom out" onClick={()=>ref.current?.zoomOut({duration:reduce?0:250})}><Minus size={18}/></Button><Button size="icon" variant="ghost" aria-label="Recenter on Delhi" onClick={recenter}><LocateFixed size={18}/></Button></Glass>{(!key||error)&&<p className="historical-tile-note glass" role="status">{!key?'Configure MapTiler to show the street basemap. Circles use geographic reference coordinates.':error}</p>}</>;
}
