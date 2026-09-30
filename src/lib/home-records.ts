import {loadCrimeContext,type CrimeContext} from './crime-context';
import {loadNews,type NewsReference} from './news';

/** Independent feeds: a failed news response must not hide official context. */
export async function fetchHomeRecords(read:(url:string)=>Promise<unknown>){
 const [context,news]=await Promise.allSettled([
  read('/data/crime-context.json').then(loadCrimeContext),
  read('/data/news.json').then(loadNews),
 ]);
 return {context:context.status==='fulfilled'?context.value:null,
  news:news.status==='fulfilled'?news.value:[],
  contextError:context.status==='rejected',newsError:news.status==='rejected'};
}

export function homeRecords(context:CrimeContext|null,news:NewsReference[],regionId:string,cityId:string){
 const matches=(r:{regionId:string;cityId:string})=>r.regionId===regionId&&(cityId==='all'||r.cityId===cityId);
 const rows=context?.records.filter(matches)??[];
 // Preserve each reporting geography/category separately, never sum them.
 const latest=rows.filter(r=>!rows.some(other=>other.cityId===r.cityId&&
  other.reportingArea===r.reportingArea&&other.geography===r.geography&&other.category===r.category&&other.year>r.year));
 return {latest,reports:news.filter(matches)};
}
