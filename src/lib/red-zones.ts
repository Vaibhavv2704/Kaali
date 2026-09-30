import type {RiskRecord} from '../types';
import {getScore} from './risk';

export type RankedZone={record:RiskRecord;score:number};

// Unknown scores are excluded. An absent observation must never become a low-risk zone.
export function rankRedZones(records:RiskRecord[],band:number,day:string,crime:string,year:string){
  const ranked:RankedZone[]=records.flatMap(record=>{
    const score=getScore(record,band,day,crime,year);
    return score===null?[]:[{record,score}];
  }).sort((a,b)=>b.score-a.score||a.record.name.localeCompare(b.record.name));
  return {
    ranked,
    high:ranked.filter(zone=>zone.score>=50),
    unknown:records.length-ranked.length,
  };
}
