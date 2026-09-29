import type * as GeoJSON from 'geojson';
export type Bounds = {north:number;south:number;east:number;west:number};
export type City = {id:string;name:string;state:string;helplineSet:string;center:{lat:number;lng:number};bounds:Bounds;boundaryFile:string|null;coverage:number;status:string;qualityReport:string};
export type Region = {id:string;name:string;center:{lat:number;lng:number};bounds:Bounds;cities:City[];boundaryFile:string|null;neighbourhoodFile:string;sampleFile:string;sources:string[];helplineSet:string;languages:string[];timezone:string;helpFile:string;optionalCities:string[];pmtiles?:string;sourceLayer?:string};
export type Level = 'Low'|'Moderate'|'High'|'Very High';
export type RiskRecord = {id:string;name:string;cityId:string;regionId:string;geometry:GeoJSON.Polygon|GeoJSON.MultiPolygon;provenance:'sample'|'model'|'unavailable';boundaryStatus:'sample'|'verified';confidence:'low'|'medium'|'high';sources:{label:string;url:string}[];scores:Record<string,number[]|null>;incidents:{category:string;count:number}[]|null;trend:{year:number;count:number}[]|null;year:number|null;femalePopulation:number|null;periodDays:number|null;estimated:boolean};
export type HelpFeature = GeoJSON.Feature<GeoJSON.Point|GeoJSON.LineString,{id:string;name:string;kind:'police'|'hospital'|'metro'|'bus'|'road';cityId:string;source:string;lastVerified:string}>;
export type UserPosition={lat:number;lng:number;accuracy:number};
