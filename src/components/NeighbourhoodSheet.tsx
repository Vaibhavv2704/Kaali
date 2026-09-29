import {useEffect,useRef,useState,type ReactNode} from 'react';
import {motion,useReducedMotion} from 'framer-motion';
import {nearestSnap,sheetHeights,stepSnap,type SheetSnap} from '../lib/sheet';

/** Non-modal details: the exposed map stays usable while the sheet is open. */
export default function NeighbourhoodSheet({name,children,onClose,onHeightChange}:{
  name:string;children:ReactNode;onClose:()=>void;onHeightChange:(height:number)=>void;
}) {
  const reduce=useReducedMotion();
  const panel=useRef<HTMLElement>(null), close=useRef(onClose);
  close.current=onClose;
  const [viewport,setViewport]=useState(()=>({mobile:matchMedia('(max-width:760px)').matches,height:window.innerHeight}));
  const [snap,setSnap]=useState<SheetSnap>('half'),[dragHeight,setDragHeight]=useState<number|null>(null);
  const gesture=useRef<{y:number;height:number;moved:boolean}|null>(null), suppressClick=useRef(false);
  const heights=sheetHeights(viewport.height), height=dragHeight??heights[snap];

  useEffect(()=>{
    const update=()=>setViewport({mobile:matchMedia('(max-width:760px)').matches,height:window.visualViewport?.height??window.innerHeight});
    window.addEventListener('resize',update);window.visualViewport?.addEventListener('resize',update);
    update();return()=>{window.removeEventListener('resize',update);window.visualViewport?.removeEventListener('resize',update)};
  },[]);
  useEffect(()=>{
    const before=document.activeElement as HTMLElement|null;
    panel.current?.focus({preventScroll:true});
    const key=(e:KeyboardEvent)=>{if(e.key==='Escape')close.current()};
    window.addEventListener('keydown',key);
    return()=>{window.removeEventListener('keydown',key);if(before?.isConnected)before.focus({preventScroll:true})};
  },[]);
  useEffect(()=>{
    if(!panel.current)return;
    const observer=new ResizeObserver(()=>onHeightChange(viewport.mobile?panel.current!.getBoundingClientRect().height:0));
    observer.observe(panel.current);return()=>{observer.disconnect();onHeightChange(0)};
  },[viewport.mobile,onHeightChange]);

  return <motion.aside ref={panel} tabIndex={-1} aria-label={`${name} details`}
    className="glass detail" data-snap={snap} data-dragging={dragHeight!==null}
    style={viewport.mobile?{height}:undefined}
    initial={reduce?false:{opacity:0,y:viewport.mobile?20:0,x:viewport.mobile?0:24}}
    animate={{opacity:1,x:0,y:0}} transition={{type:'spring',stiffness:260,damping:28}}>
    <button className="sheet-handle" aria-label={`Resize details sheet: ${snap}. Arrow up to expand, arrow down to collapse.`}
      onKeyDown={e=>{if(['ArrowUp','ArrowDown','Home','End'].includes(e.key)){e.preventDefault();setSnap(e.key==='Home'?'peek':e.key==='End'?'full':stepSnap(snap,e.key==='ArrowUp'?1:-1))}}}
      onClick={()=>{if(suppressClick.current){suppressClick.current=false;return}setSnap(snap==='full'?'peek':stepSnap(snap,1))}}
      onPointerDown={e=>{if(e.button!==0)return;suppressClick.current=false;gesture.current={y:e.clientY,height,moved:false};e.currentTarget.setPointerCapture(e.pointerId)}}
      onPointerMove={e=>{const g=gesture.current;if(!g)return;const delta=g.y-e.clientY;if(Math.abs(delta)>6)g.moved=true;if(g.moved)setDragHeight(Math.max(heights.peek,Math.min(heights.full,g.height+delta)))}}
      onPointerUp={e=>{const g=gesture.current;if(!g)return;if(g.moved){suppressClick.current=true;setSnap(nearestSnap(g.height+g.y-e.clientY,viewport.height))}gesture.current=null;setDragHeight(null);if(e.currentTarget.hasPointerCapture(e.pointerId))e.currentTarget.releasePointerCapture(e.pointerId)}}
      onPointerCancel={()=>{gesture.current=null;suppressClick.current=true;setDragHeight(null)}}>
      <span aria-hidden="true"/>Drag or tap · {snap}
    </button>
    <div className="detail-content">{children}</div>
  </motion.aside>;
}
