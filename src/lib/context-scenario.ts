import {distance,point} from '@turf/turf';
import type {HelpFeature} from '../types';
// Editable judgement factors, not learned occurrence-time probabilities.
export const assumedTimeFactors=[1.2,0.9,0.9,1,1.1,1.35] as const;
export const scenarioBands=['00:00–04:00','04:00–08:00','08:00–12:00','12:00–16:00','16:00–20:00','20:00–24:00'];
export function mappedTransitNearby(coordinates:[number,number],help:HelpFeature[]){
 return help.filter(f=>f.geometry.type==='Point'&&(f.properties.kind==='metro'||f.properties.kind==='bus')&&distance(point(coordinates),point(f.geometry.coordinates),{units:'kilometers'})<=1).length;
}
export function contextScenario(count:number|null,allCounts:(number|null)[],transit:number,band:number){
 if(count===null||!Number.isFinite(count)||count<0||!Number.isInteger(band)||band<0||band>5||!Number.isFinite(transit)||transit<=0)return null;
 const available=allCounts.filter((n):n is number=>n!==null&&Number.isFinite(n)&&n>=0);
 if(available.length<2)return null;
 // Annual reporting volume rank, not estimated neighbourhood cases or probability.
 const rank=(available.filter(n=>n<count).length+available.filter(n=>n===count).length/2)/available.length;
 const activityAdjustment=1-Math.min(transit,20)/100;
 return {score:Math.round(Math.min(100,rank*100*assumedTimeFactors[band]*activityAdjustment)),historyRank:rank,timeFactor:assumedTimeFactors[band],activityAdjustment,transit,confidence:'low' as const,dataType:'assumed-scenario' as const};
}
