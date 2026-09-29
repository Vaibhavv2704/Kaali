export type SheetSnap = 'peek' | 'half' | 'full';
export const sheetSnaps: SheetSnap[] = ['peek', 'half', 'full'];

export function sheetHeights(viewportHeight: number): Record<SheetSnap, number> {
  const full = Math.max(180, Math.min(viewportHeight * .8, viewportHeight - 170));
  return {peek: Math.min(180, full), half: Math.min(viewportHeight * .52, full), full};
}

export function nearestSnap(height: number, viewportHeight: number): SheetSnap {
  const heights = sheetHeights(viewportHeight);
  return sheetSnaps.reduce((best, snap) =>
    Math.abs(heights[snap] - height) < Math.abs(heights[best] - height) ? snap : best);
}

export function stepSnap(snap: SheetSnap, direction: number): SheetSnap {
  return sheetSnaps[Math.max(0, Math.min(2, sheetSnaps.indexOf(snap) + direction))];
}
