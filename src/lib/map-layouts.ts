import {baseStyle} from './map-state';
import catalog from '../data/map-catalog.json';
export type BasemapLayout=string;
export const mapLayouts=[{id:'streets',label:'Detailed streets · automatic theme'},{id:'muted',label:'Muted map · automatic theme'},{id:'satellite',label:'Satellite with labels'},...catalog.styles];
export function detailedBasemap(theme:string,key:string,layout:BasemapLayout){
 if(!key||layout==='muted')return baseStyle(theme,key);
 const style=layout==='satellite'?'hybrid':layout==='streets'?(theme==='dark'?'streets-v4-dark':'streets-v4'):catalog.styles.some(s=>s.id===layout)?layout:'streets-v4';
 return `https://api.maptiler.com/maps/${style}/style.json?key=${encodeURIComponent(key)}`;
}
