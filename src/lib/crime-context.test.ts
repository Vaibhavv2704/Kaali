import {describe,it,expect} from 'vitest';
import {loadCrimeContext} from './crime-context';
import data from '../../public/data/crime-context.json';
describe('historical crime context',()=>{
  it('retains annual reporting geography without inventing neighbourhood labels',()=>{
    const result=loadCrimeContext(data);
    expect(result.records).toHaveLength(6);
    expect(result.records.every(r=>r.timeBand===null&&r.neighbourhoodId===null&&!r.eligibleForTraining)).toBe(true);
  });
  it('rejects negative counts, duplicate records and training eligibility',()=>{
    for(const changes of [{count:-1},{eligibleForTraining:true},{neighbourhoodId:'invented'}]){
      const copy=structuredClone(data);Object.assign(copy.records[0],changes);
      expect(()=>loadCrimeContext(copy)).toThrow();
    }
    expect(()=>loadCrimeContext({...data,records:[...data.records,data.records[0]]})).toThrow();
  });
});
