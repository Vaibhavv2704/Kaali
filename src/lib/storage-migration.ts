/** One-time brand migration. Never overwrite a newer preference or remove an uncopied value. */
export const LEGACY_PREFIXES=['aegis-','aegis:','aegis_'];
const MARKER='kaali:storage-migrated-v1';
export function migrateStorage(storage:Storage){
  try{
    if(storage.getItem(MARKER)==='1')return;
    const keys=Array.from({length:storage.length},(_,i)=>storage.key(i)).filter((key):key is string=>key!==null);
    for(const key of keys){
      const prefix=LEGACY_PREFIXES.find(p=>key.startsWith(p));
      if(!prefix)continue;
      const destination=`kaali${prefix.slice(-1)}${key.slice(prefix.length)}`;
      const value=storage.getItem(key);
      if(value===null)continue;
      if(storage.getItem(destination)===null)storage.setItem(destination,value);
      storage.removeItem(key);
    }
    storage.setItem(MARKER,'1');
  }catch{/* Restricted/full browser storage: retain any untransferred preference and retry later. */}
}
export function migrateBrandStorage(){
  for(const name of ['localStorage','sessionStorage'] as const){try{migrateStorage(window[name])}catch{/* Storage is optional. */}}
}
