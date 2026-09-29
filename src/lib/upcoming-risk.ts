import type {RiskRecord} from '../types';
import {getScore, timeContext} from './risk';

/** Search the next 24 hours using each future instant's regional calendar. */
export function nextHigherWindow(record: RiskRecord, timezone: string, now: Date) {
  const current = timeContext(timezone, now);
  const score = getScore(record, current.band, current.day);
  if (score === null) return null;
  const calendar = new Intl.DateTimeFormat('en-CA', {timeZone: timezone, year: 'numeric', month: '2-digit', day: '2-digit'});
  let previous = `${calendar.format(now)}:${current.band}`;
  for (let hour = 1; hour <= 24; hour++) {
    const instant = new Date(now.getTime() + hour * 3_600_000);
    const context = timeContext(timezone, instant);
    const window = `${calendar.format(instant)}:${context.band}`;
    if (window === previous) continue;
    previous = window;
    const futureScore = getScore(record, context.band, context.day);
    if (futureScore !== null && futureScore > score) {
      return {...context, score: futureScore, date: instant};
    }
  }
  return null;
}
