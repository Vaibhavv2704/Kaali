import {describe,it,expect} from 'vitest';
import {migrateStorage,LEGACY_PREFIXES} from './storage-migration';
class MemoryStorage implements Storage{data=new Map<string,string>();get length(){return this.data.size}clear(){this.data.clear()}getItem(key:string){return this.data.get(key)??null}key(i:number){return [...this.data.keys()][i]??null}removeItem(key:string){this.data.delete(key)}setItem(key:string,value:string){this.data.set(key,value)}}
// Legacy literals are confined to the deliberate migration implementation.
const legacy=LEGACY_PREFIXES[0].slice(0,-1);
describe('brand storage migration',()=>{
  it('preserves theme, language and recent searches, then removes old keys',()=>{const s=new MemoryStorage();s.setItem(`${legacy}-theme`,'dark');s.setItem(`${legacy}:language`,'hi');s.setItem(`${legacy}-searches`,'[]');s.setItem('other-app','keep');migrateStorage(s);expect(s.getItem('kaali-theme')).toBe('dark');expect(s.getItem('kaali:language')).toBe('hi');expect(s.getItem('kaali-searches')).toBe('[]');expect(s.getItem(`${legacy}-theme`)).toBeNull();expect(s.getItem(`${legacy}:language`)).toBeNull();expect(s.getItem('other-app')).toBe('keep')});
  it('retains a newer preference and is idempotent',()=>{const s=new MemoryStorage();s.setItem(`${legacy}-theme`,'dark');s.setItem('kaali-theme','light');migrateStorage(s);migrateStorage(s);expect(s.getItem('kaali-theme')).toBe('light');expect(s.getItem(`${legacy}-theme`)).toBeNull()});
  it('keeps the old value if copying fails',()=>{const s=new MemoryStorage();s.setItem(`${legacy}-theme`,'dark');s.setItem=()=>{throw Error('Storage full')};expect(()=>migrateStorage(s)).not.toThrow();expect(s.getItem(`${legacy}-theme`)).toBe('dark');expect(s.getItem('kaali:storage-migrated-v1')).toBeNull()});
});
