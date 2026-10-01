import {baseStyle} from './map-state';
export type BasemapLayout='streets'|'muted'|'satellite';
export function detailedBasemap(theme:string,key:string,layout:BasemapLayout){
 if(!key||layout==='muted')return baseStyle(theme,key);
 const style=layout==='satellite'?'hybrid':theme==='dark'?'streets-v4-dark':'streets-v4';
 return `https://api.maptiler.com/maps/${style}/style.json?key=${encodeURIComponent(key)}`;
}
