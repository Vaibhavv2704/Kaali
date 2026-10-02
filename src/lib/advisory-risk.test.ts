import {describe,it,expect} from 'vitest';
import {advisoryLevel,localHour,precaution} from './advisory-risk';
describe('explicit local-time advisory rules',()=>{
 it('uses exact fallback boundaries',()=>{expect([0,5,6,9,10,16,17,19,20,23].map(h=>advisoryLevel(null,h))).toEqual(['High','High','Medium','Medium','Low','Low','Medium','Medium','High','High']);});
 it('upgrades known night levels without downgrading high or very high',()=>{expect([12,37,62,87].map(s=>advisoryLevel(s,22))).toEqual(['Medium','High','High','Very high']);expect(advisoryLevel(12,6)).toBe('Low');expect(advisoryLevel(12,21)).toBe('Low');expect(advisoryLevel(12,5,true)).toBe('High');expect(advisoryLevel(12,5,false,true)).toBe('High');});
 it('uses IST irrespective of browser timezone and gives calm advice',()=>{expect(localHour(new Date('2026-10-02T00:30:00Z'))).toBe(6);expect(precaution('High')).toContain('advice only');expect(precaution('Low')).not.toContain('unknown');expect(()=>advisoryLevel(null,24)).toThrow();});
});
