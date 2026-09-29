import {describe,it,expect} from 'vitest';
import {loadNews} from './news';
import data from '../../public/data/news.json';
describe('news references',()=>{
  it('keeps reading links separate from training observations',()=>{expect(loadNews(data).every(n=>!n.eligibleForTraining&&n.privacyReviewed)).toBe(true)});
  it('rejects article bodies and URL duplicates including tracking variants',()=>{
    expect(()=>loadNews([{...data[0],body:'Do not store article bodies'}])).toThrow();
    expect(()=>loadNews([data[0],{...data[0],id:'duplicate',url:data[0].url+'?utm_source=test'}])).toThrow();
  });
});
