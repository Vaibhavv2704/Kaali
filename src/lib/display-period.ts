// Presentation only. Source reporting years and request/filter values stay intact.
export function displayPeriod(value:string|number|null|undefined){
 if(value===null||value===undefined)return 'Historical period';
 return /^2024(?:$|-)/.test(String(value))?'Historical period':String(value);
}
export function historicalCopy(value:string){return value.replace(/\b2024\b/g,'the reporting period');}
