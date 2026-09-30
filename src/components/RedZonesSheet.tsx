import {Info,MapPin} from 'lucide-react';
import type {RiskRecord} from '../types';
import {bands,displayLevel,riskColor} from '../lib/risk';
import {rankRedZones} from '../lib/red-zones';
import {Sheet} from './ui';

type Props={open:boolean;onOpenChange:(open:boolean)=>void;records:RiskRecord[];sample:boolean;band:number;day:string;crime:string;year:string;onSelect:(record:RiskRecord)=>void};

export default function RedZonesSheet({open,onOpenChange,records,sample,band,day,crime,year,onSelect}:Props){
  const {ranked,high,unknown}=rankRedZones(records,band,day,crime,year);
  return <Sheet open={open} onOpenChange={onOpenChange} title={sample?'Sample red zones':'Red zones'} description="Zones ranked for the selected time and filters. Unknown scores are excluded.">
    <p className="red-zone-context">{bands[band]} · {day==='weekday'?'Weekday':'Weekend'}{crime!=='all'?` · ${crime.replace('-', ' ')}`:''}{year!=='all'?` · ${year}`:''}</p>
    {sample&&<p className="red-zone-warning"><Info size={16}/> Synthetic sample cells and scores. These are not observed crime data or real risk predictions.</p>}
    {ranked.length?<>
      <div className="red-zone-totals"><div><strong>{high.length}</strong><span>High or very high {sample?'sample':'estimated'} risk</span></div><div><strong>{ranked.length}</strong><span>Zones with scores</span></div><div><strong>{unknown}</strong><span>Insufficient data</span></div></div>
      <p className="red-zone-note">{sample?'These synthetic scores demonstrate the interaction only.':'Scores compare model estimates within this view; they do not predict anyone’s safety.'} Areas without scores are not lower risk.</p>
      <div className="red-zone-results">{ranked.map(({record,score})=><button type="button" className="zone-row" key={record.id} onClick={()=>{onSelect(record);onOpenChange(false)}}><span className="zone-symbol" style={{background:riskColor(score),color:score>=50?'#fff':'#202431'}}>{score}</span><span><strong>{record.name}</strong><small>{record.cityId.replace('-', ' ')} · {displayLevel(score)}{sample?' · Sample':''}</small></span><MapPin size={16}/></button>)}</div>
    </>:<p className="red-zone-empty">No neighbourhood scores are available for this view. Official city totals and individual news references do not establish neighbourhood red zones. Try another filter or explore the clearly labelled sample preview.</p>}
  </Sheet>;
}
