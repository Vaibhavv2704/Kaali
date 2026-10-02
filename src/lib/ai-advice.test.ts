import {describe,it,expect,vi,afterEach} from 'vitest';
import {aiContextSchema,generateLocalAdvice} from './ai-advice';
import {contextOnly,advicePrompt,acceptAdvice} from '../../server/advice.mjs';
describe('local generative advice privacy',()=>{
 const context={index:'higher',time:'night',activity:'lower',population:'unknown'} as const;
 afterEach(()=>vi.unstubAllGlobals());
 it('rejects coordinates, names, counts and free-form prompts',()=>{for(const extra of [{lat:28.6},{longitude:77.2},{locality:'Dwarka'},{count:883},{prompt:'ignore instructions'}]){expect(()=>aiContextSchema.parse({...context,...extra})).toThrow();expect(()=>contextOnly({...context,...extra})).toThrow();}});
 it('gives generation only categorical context and uncertainty instructions',()=>{const prompt=advicePrompt(context);expect(prompt).toContain('individual safety are unknown');expect(prompt).not.toContain('Dwarka');expect(()=>acceptAdvice({advice:'Your area is dangerous. Stay indoors.'})).toThrow();expect(acceptAdvice({advice:'Consider a well-lit pickup point, and share your journey with someone you trust if helpful.'})).toContain('well-lit');});
 it('sends no GPS or identifiers and handles unavailable generation honestly',async()=>{const fetch=vi.fn().mockResolvedValue({ok:false});vi.stubGlobal('fetch',fetch);await expect(generateLocalAdvice(context,new AbortController().signal)).rejects.toThrow('unavailable');expect(fetch.mock.calls[0][0]).toBe('http://127.0.0.1:5175/api/advice');expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual(context);});
});
