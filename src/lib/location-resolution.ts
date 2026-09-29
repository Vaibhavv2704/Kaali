import {booleanPointInPolygon,point} from '@turf/turf';
import type {FeatureCollection,Polygon,MultiPolygon,Feature} from 'geojson';
import type {Region,RiskRecord,UserPosition} from '../types';
import {neighbourhoodAt} from './geo';

export type BoundaryCache=ReadonlyMap<string,FeatureCollection>;
function inside(data:FeatureCollection|undefined,p:Pick<UserPosition,'lat'|'lng'>){
  if(!data||data.type!=='FeatureCollection'||!Array.isArray(data.features))return false;
  try{return data.features.some(f=>(f.geometry?.type==='Polygon'||f.geometry?.type==='MultiPolygon')&&booleanPointInPolygon(point([p.lng,p.lat]),f as Feature<Polygon|MultiPolygon>,{ignoreBoundary:true}))}catch{return false}
}

/** Configured, reviewed boundaries determine jurisdiction; viewport rectangles never do. */
export function resolveLocation(regions:Region[],records:RiskRecord[],boundaries:BoundaryCache,p:UserPosition){
  const neighbourhood=neighbourhoodAt(records,p);
  const cities=regions.flatMap(region=>region.cities.filter(city=>city.boundaryFile&&inside(boundaries.get(city.boundaryFile),p)).map(city=>({region,city})));
  const matches=regions.filter(region=>(region.boundaryFile&&inside(boundaries.get(region.boundaryFile),p))||cities.some(c=>c.region.id===region.id)||neighbourhood?.regionId===region.id);
  if(matches.length!==1||cities.length>1)return {region:null,city:null,neighbourhood:null,status:matches.length>1||cities.length>1?'ambiguous' as const:'unknown' as const};
  const region=matches[0];
  const record=neighbourhood?.regionId===region.id?neighbourhood:null;
  const recordCity=region.cities.find(c=>c.id===record?.cityId&&!c.boundaryFile);
  const city=cities.find(c=>c.region.id===region.id)?.city??recordCity??null;
  if(record&&city&&record.cityId!==city.id)return {region,city:null,neighbourhood:null,status:'ambiguous' as const};
  return {region,city,neighbourhood:record,status:'matched' as const};
}
