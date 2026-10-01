import {describe,it,expect} from 'vitest';
import {detailedBasemap,mapLayouts} from './map-layouts';
describe('layout catalogue',()=>{
 it('keeps theme-following presets and catalogue ids without credentials',()=>{expect(mapLayouts.length).toBeGreaterThan(40);expect(new Set(mapLayouts.map(l=>l.id)).size).toBe(mapLayouts.length);expect(mapLayouts.every(l=>/^[a-z0-9-]+$/.test(l.id))).toBe(true);expect(detailedBasemap('dark','test','streets')).toContain('streets-v4-dark');expect(detailedBasemap('light','test','outdoor-v4')).toContain('/outdoor-v4/');});
 it('has a keyless fallback and refuses undocumented style path injection',()=>{expect(detailedBasemap('dark','','streets')).toMatchObject({version:8});expect(detailedBasemap('dark','test','../../private')).toContain('/streets-v4/');});
});
