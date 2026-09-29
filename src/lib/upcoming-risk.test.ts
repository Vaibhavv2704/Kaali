import {describe, expect, it} from 'vitest';
import {loadRisk} from './risk';
import {nextHigherWindow} from './upcoming-risk';
import samples from '../../public/data/delhi-ncr/sample.json';

const record = () => ({...loadRisk(samples)[0], scores: {
  'weekday:all': [10, 10, 10, 10, 10, 10] as number[] | null,
  'weekend:all': [60, 10, 10, 10, 10, 10] as number[] | null,
}});
describe('upcoming location risk windows', () => {
  it('uses weekend scores after Friday midnight in the region', () => {
    expect(nextHigherWindow(record(), 'Asia/Kolkata', new Date('2026-09-25T18:00:00Z')))
      .toMatchObject({band: 0, day: 'weekend', score: 60});
  });
  it('uses weekday scores after Sunday midnight', () => {
    const r = record(); r.scores['weekday:all']![0] = 70;
    expect(nextHigherWindow(r, 'Asia/Kolkata', new Date('2026-09-27T18:00:00Z')))
      .toMatchObject({band: 0, day: 'weekday', score: 70});
  });
  it('does not infer a comparison when current scores are missing', () => {
    const r = record(); r.scores['weekday:all'] = null;
    expect(nextHigherWindow(r, 'Asia/Kolkata', new Date('2026-09-25T18:00:00Z'))).toBeNull();
  });
  it('skips missing future scores and returns null without a higher window', () => {
    const r = record(); r.scores['weekend:all'] = null;
    expect(nextHigherWindow(r, 'Asia/Kolkata', new Date('2026-09-25T18:00:00Z'))).toBeNull();
  });
  it('includes tomorrow’s same band when the day type changes', () => {
    const r = record(); r.scores['weekend:all'] = [10, 10, 10, 10, 10, 80];
    expect(nextHigherWindow(r, 'Asia/Kolkata', new Date('2026-09-25T18:00:00Z')))
      .toMatchObject({band: 5, day: 'weekend', score: 80});
  });
});
