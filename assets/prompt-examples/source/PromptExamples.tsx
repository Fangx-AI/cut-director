// SPDX-License-Identifier: AGPL-3.0-or-later
// CutDirector by Fangx-AI. Local Remotion examples, not ChatCut exports.
import React from 'react';
import {AbsoluteFill,Composition,Easing,interpolate,useCurrentFrame,useVideoConfig,registerRoot} from 'remotion';

const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const ease={...clamp,easing:Easing.bezier(.16,1,.3,1)};
export type StyleProps={background:string;foreground:string;accent:string;fontFamily:string};
const styleDefaults:StyleProps={background:'#0a1019',foreground:'#f4f6f8',accent:'#c9f578',fontFamily:'Microsoft YaHei, sans-serif'};
type HeadlineProps=StyleProps & {announcement:string;count:number;unit:string;question:string};
type BoardProps=StyleProps & {title:string;columns:[string,string,string];tasks:[string,string,string]};
export const headlineDefaults:HeadlineProps={...styleDefaults,announcement:'新工具发布',count:12,unit:'种实用方法',question:'哪一个，你能用上？'};
export const boardDefaults:BoardProps={...styleDefaults,title:'积压任务，逐项推进',columns:['待处理','处理中','已完成'],tasks:['整理材料','检查内容','完成交付']};

const Canvas:React.FC<React.PropsWithChildren<StyleProps>>=({children,...p})=>{
 const {width,height}=useVideoConfig();const scale=Math.min(width/1280,height/720);
 return <AbsoluteFill style={{background:p.background,color:p.foreground,fontFamily:p.fontFamily,overflow:'hidden'}}><div style={{position:'absolute',width:1280,height:720,left:(width-1280*scale)/2,top:(height-720*scale)/2,transform:`scale(${scale})`,transformOrigin:'top left'}}>{children}</div></AbsoluteFill>;
};
export const Headline:React.FC<HeadlineProps>=(p)=>{
 const f=useCurrentFrame();const {durationInFrames}=useVideoConfig();
 const phase=Math.min(2,Math.floor(f/(durationInFrames/3)));const t=f-phase*durationInFrames/3;
 const enter=interpolate(t,[0,12],[0,1],ease);
 const value=phase===0?p.announcement:phase===1?String(Math.round(interpolate(t,[0,16],[Math.max(0,p.count-5),p.count],ease))):p.question;
 return <Canvas {...p}>
  <div style={{position:'absolute',left:65,top:45,fontSize:22,letterSpacing:4,color:p.accent}}>三段式数字片头</div>
  {[0,1,2].map(i=><div key={i} style={{position:'absolute',width:390+i*115,height:390+i*115,left:445-i*57.5,top:165-i*57.5,border:`1px solid ${p.accent}35`,borderRadius:'50%',scale:interpolate(f,[0,durationInFrames-1],[.9,1.08],clamp)}}/>)}
  <div style={{position:'absolute',left:70,right:70,top:phase===1?155:270,textAlign:'center',fontSize:phase===1?240:phase===2?85:100,lineHeight:1.15,fontWeight:900,color:phase===1?p.accent:p.foreground,opacity:enter,translate:`${phase===2?(1-enter)*150:0}px ${(1-enter)*45}px`,scale:phase===1?interpolate(t,[0,16],[1.25,1],ease):1}}>{value}</div>
  {phase===1&&<div style={{position:'absolute',top:442,left:0,right:0,textAlign:'center',fontSize:58,fontWeight:800}}>{p.unit}</div>}
  <div style={{position:'absolute',top:560,left:250,width:780,height:4,background:p.accent,scale:`${interpolate(t,[0,20],[0,1],ease)} 1`}}/>
  <div style={{position:'absolute',bottom:65,left:65,right:65,display:'flex',gap:12}}>{[0,1,2].map(i=><div key={i} style={{height:4,flex:1,background:i===phase?p.accent:'#344251'}}/>)}</div>
 </Canvas>;
};

export const Board:React.FC<BoardProps>=(p)=>{
 const f=useCurrentFrame();const {durationInFrames}=useVideoConfig();const t=f*180/durationInFrames;
 return <Canvas {...p}>
  <div style={{position:'absolute',left:65,top:40,fontSize:51,fontWeight:800}}>{p.title}</div>
  <div style={{position:'absolute',right:65,top:58,fontSize:23,color:'#9eafbf'}}>流程示意</div>
  {p.columns.map((c,i)=><div key={i} style={{position:'absolute',left:65+i*390,top:150,width:365,height:455,borderRadius:16,background:'#182330',border:`1px solid ${i===2?p.accent+'66':'#344251'}`,padding:22,fontSize:32,boxSizing:'border-box',color:i===2?p.accent:p.foreground}}>{c}</div>)}
  {p.tasks.map((task,i)=>{
   const start=20+i*26;
   const x=interpolate(t,[start,start+20,start+43,start+66],[0,390,390,780],ease);
   const done=t>=start+66;
   return <div key={i} style={{position:'absolute',left:86+x,top:225+i*109,width:323,height:86,borderRadius:12,boxSizing:'border-box',padding:'21px 18px',background:done?p.accent:'#34485e',color:done?'#15220c':p.foreground,fontSize:30,fontWeight:700,boxShadow:'0 10px 24px #0004'}}>{done?'✓':'↗'}　{task}</div>;
  })}
  <div style={{position:'absolute',left:65,bottom:55,fontSize:28,color:'#a4b4c5'}}>同一张卡片，沿状态推进</div>
 </Canvas>;
};
export const PromptCompositions=()=> <><Composition id="Prompt010" component={Headline} defaultProps={headlineDefaults} width={1280} height={720} fps={30} durationInFrames={180}/><Composition id="Prompt011" component={Board} defaultProps={boardDefaults} width={1280} height={720} fps={30} durationInFrames={180}/></>;
registerRoot(PromptCompositions);
