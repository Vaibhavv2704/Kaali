import {distance,point} from '@turf/turf';
import type {Locality} from './locality-context';
import {mlCells,mlIndex,modelRiskLevel,type MLVolume} from './ml-volume';
export type AdvisoryLevel='Low'|'Medium'|'High'|'Very high';
const levels:AdvisoryLevel[]=['Low','Medium','High','Very high'];
export function localHour(now=new Date(),timezone='Asia/Kolkata'){return Number(new Intl.DateTimeFormat('en-GB',{timeZone:timezone,hour:'numeric',hourCycle:'h23'}).format(now));}
export function advisoryLevel(score:number|null,hour:number,outer=false,lowerDensity=false):AdvisoryLevel{
 if(!Number.isInteger(hour)||hour<0||hour>23)throw Error('Invalid local hour');
 const base=modelRiskLevel(score);
 if(base==='Unknown')return hour>=20||hour<6?'High':hour<10||hour>=17?'Medium':'Low';
 let rank=levels.indexOf(base);
 if(hour>=22||hour<6){if(rank<2)rank++;if(outer||lowerDensity)rank=Math.max(rank,2);}
 return levels[rank];
}
export function referenceFlags(r:Locality,references:Locality[],center:{lng:number;lat:number}){
 const densities=references.map(x=>x.density).filter((x):x is number=>x!==null).sort((a,b)=>a-b);
 // Explicit display assumptions: outer = >20 km from configured regional centre;
 // lower density = below median of available supplied density values, never inferred from missingness.
 return {outer:distance(point(r.coordinates),point([center.lng,center.lat]))>20,lowerDensity:r.density!==null&&densities.length>1&&r.density<densities[Math.floor(densities.length/2)]};
}
export function referenceAdvisory(model:MLVolume|null,r:Locality,band:number,day:string,hour:number,references:Locality[],center:{lng:number;lat:number}){const flags=referenceFlags(r,references,center);return advisoryLevel(mlIndex(model,r,band,day,references),hour,flags.outer,flags.lowerDensity);}
export function advisoryCells(model:MLVolume|null,records:Locality[],band:number,day:string,hour:number,center:{lng:number;lat:number}){
 const cells=mlCells(model,records,band,day);
 for(const f of cells.features){const group=records.filter(r=>r.cellId===records.find(r=>r.id===f.properties.id)?.cellId);const rank=Math.max(...group.map(r=>levels.indexOf(referenceAdvisory(model,r,band,day,hour,records,center))));f.properties.score=[12,37,62,87][rank];}
 return cells;
}
export function precaution(level:AdvisoryLevel){const tip={Low:'Choose a familiar route and check your destination and pickup point before setting out. Keep your phone accessible and enough charge for the journey. If using a cab, check the vehicle and driver details against your booking. You can share your expected arrival time with someone you trust.',Medium:'Prefer well-lit main roads and pickup points where other people are present. Check the route before travelling and consider a licensed ride instead of an unfamiliar shortcut. Verify the vehicle and driver against your booking, and consider sharing your journey or expected arrival time with someone you trust. Keep your phone charged and accessible.',High:'For your journey, consider well-lit main roads and a licensed ride, especially if a route looks quiet or unfamiliar. Wait for your pickup at a visible, active location and verify the vehicle and driver against your booking. Consider sharing your journey and arranging a check-in with someone you trust. Keep your phone charged; if you feel uncomfortable, you can change your route or move toward a staffed public place.', 'Very high':'Plan your route and pickup before setting out, choosing visible, well-lit main roads where possible. Consider a licensed ride or travelling with someone you trust, and verify the vehicle and driver against your booking. Share your journey or arrange a check-in if helpful, and keep your phone charged and within reach. If something feels uncomfortable, consider moving toward a staffed public place and seeking assistance.'}[level];return `${tip} This is advice only; stay aware of your surroundings and take care. Keep 112 handy for emergencies.`;}
