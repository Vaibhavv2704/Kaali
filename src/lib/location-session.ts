import type {UserPosition} from '../types';

type GeoService=Pick<Geolocation,'watchPosition'|'clearWatch'>;
/** A stopped watch must never revive location state through an already queued callback. */
export function locationSession(service:GeoService,receive:(position:UserPosition|null)=>void,failed:()=>void){
  let watch:number|null=null;
  let generation=0;
  const stop=()=>{generation++;if(watch!==null)service.clearWatch(watch);watch=null;receive(null)};
  return {
    stop,
    start(){
      if(watch!==null)return;
      const token=++generation;
      const error=()=>{if(token!==generation)return;stop();failed()};
      try{
        const id=service.watchPosition(result=>{
          if(token!==generation)return;
          const {latitude:lat,longitude:lng,accuracy}=result.coords;
          if(![lat,lng,accuracy].every(Number.isFinite)||Math.abs(lat)>90||Math.abs(lng)>180||accuracy<0){error();return}
          receive({lat,lng,accuracy});
        },error,{enableHighAccuracy:false,maximumAge:15000,timeout:12000});
        if(token===generation)watch=id;else service.clearWatch(id);
      }catch{error()}
    },
  };
}
