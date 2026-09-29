import {describe,it,expect} from 'vitest';
import {nearestSnap,sheetHeights,stepSnap} from './sheet';
describe('mobile details sheet',()=>{
  it('keeps full details below the header on short and tall viewports',()=>{
    for(const viewport of [480,640,844,1000]){const h=sheetHeights(viewport);expect(h.peek).toBeLessThanOrEqual(h.half);expect(h.half).toBeLessThanOrEqual(h.full);expect(h.full).toBeLessThanOrEqual(viewport-170)}
  });
  it('snaps a drag to its nearest height rather than skipping the half position',()=>{
    expect(nearestSnap(190,844)).toBe('peek');expect(nearestSnap(450,844)).toBe('half');expect(nearestSnap(900,844)).toBe('full');expect(nearestSnap(-100,844)).toBe('peek');
  });
  it('clamps keyboard movement at each end',()=>{expect(stepSnap('peek',-1)).toBe('peek');expect(stepSnap('peek',1)).toBe('half');expect(stepSnap('full',-1)).toBe('half');expect(stepSnap('full',1)).toBe('full')});
});
