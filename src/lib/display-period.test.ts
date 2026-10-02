import {it,expect} from 'vitest';
import {displayPeriod,historicalCopy} from './display-period';
it('hides the requested reporting year only in presentation',()=>{
 expect(displayPeriod(2024)).toBe('Historical period');
 expect(displayPeriod('2024-08-11')).toBe('Historical period');
 expect(displayPeriod(2022)).toBe('2022');
 expect(historicalCopy('Recorded in 2024; 500 cases')).toBe('Recorded in the reporting period; 500 cases');
 const source={year:2024,count:2024};displayPeriod(source.year);expect(source).toEqual({year:2024,count:2024});
});
