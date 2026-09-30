import {describe,it,expect} from 'vitest';
import {fetchHomeRecords,homeRecords} from './home-records';
import {loadCrimeContext} from './crime-context';
import {loadNews} from './news';
import contextData from '../../public/data/crime-context.json';
import newsData from '../../public/data/news.json';
const context=loadCrimeContext(contextData),news=loadNews(newsData);
describe('home records',()=>{
 it('keeps latest city totals separate and excludes other regions',()=>{
  expect(homeRecords(context,news,'delhi-ncr','all').latest.map(r=>r.count)).toEqual([14158,1063]);
  expect(homeRecords(context,news,'delhi-ncr','delhi').latest.map(r=>r.cityId)).toEqual(['delhi']);
  expect(homeRecords(context,news,'another-region','all')).toEqual({latest:[],reports:[]});
 });
 it('does not treat missing city records as zero counts or attach Delhi events elsewhere',()=>{
  const result=homeRecords(context,news,'delhi-ncr','noida');
  expect(result.latest).toEqual([]);expect(result.reports).toEqual([]);
 });
 it('retains official records when news fails',async()=>{
  const result=await fetchHomeRecords(async url=>{if(url.includes('news'))throw Error('offline');return contextData});
  expect(result.context?.records).toHaveLength(6);expect(result.newsError).toBe(true);expect(result.contextError).toBe(false);
 });
 it('retains news when official context is malformed',async()=>{
  const result=await fetchHomeRecords(async url=>url.includes('news')?newsData:{});
  expect(result.context).toBeNull();expect(result.news.length).toBe(news.length);expect(result.contextError).toBe(true);
 });
});
