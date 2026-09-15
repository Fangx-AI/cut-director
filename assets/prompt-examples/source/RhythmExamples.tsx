// SPDX-License-Identifier: AGPL-3.0-or-later
// Original abstract demonstrations by CutDirector / Fangx-AI, not product recordings.
import React from 'react';
import {AbsoluteFill, Composition, Easing, interpolate, registerRoot, useCurrentFrame} from 'remotion';

const ease = {extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const,easing:Easing.bezier(.16,1,.3,1)};
type Props = {accent:string; fontFamily:string; label:string};
const defaults:Props={accent:'#CBF66F',fontFamily:'Microsoft YaHei, sans-serif',label:'CUTDIRECTOR / ORIGINAL STUDY'};
const Ink='#F5F3EC';
const Frame:React.FC<React.PropsWithChildren<Props & {number:string;title:string}>>=({children,number,title,...p})=><AbsoluteFill style={{background:'#101419',color:Ink,fontFamily:p.fontFamily,padding:64,overflow:'hidden'}}>
 <div style={{display:'flex',justifyContent:'space-between',fontSize:17,letterSpacing:3,color:'#a2aab5'}}><span>{p.label}</span><span>{number} / {title}</span></div>{children}
 <div style={{position:'absolute',bottom:35,left:64,right:64,display:'flex',justifyContent:'space-between',fontSize:17,color:'#a2aab5'}}><span>独立结构演示 · 非产品实录</span><span>Fangx-AI / CutDirector</span></div>
</AbsoluteFill>;

const Accent:React.FC<Props>=(p)=>{
 const f=useCurrentFrame(); const beat=Math.floor(f/45); const local=f%45;
 const labels=['先给一个理由','让关键动作','与音乐一起','落稳。'];
 const x=interpolate(local,[0,13],[24,0],ease); const pulse=interpolate(local,[0,18],[1.2,1],ease);
 return <Frame {...p} number="012" title="语义重音">
  <div style={{position:'absolute',top:175,left:64,width:760}}><div style={{fontSize:19,color:p.accent,letterSpacing:6}}>ONE IDEA. ONE ACCENT.</div><div style={{fontWeight:900,fontSize:92,marginTop:25,translate:`0 ${x}px`,opacity:interpolate(local,[0,6],[.3,1],ease)}}>{labels[Math.min(beat,3)]}</div><div style={{fontSize:26,color:'#a2aab5',marginTop:28}}>主动作在重音落下，下一句自然接上。</div></div>
  <div style={{position:'absolute',right:95,top:220,width:205,height:205,borderRadius:'50%',background:p.accent,scale:pulse,display:'grid',placeItems:'center',color:'#101419',fontSize:78,fontWeight:900}}>{String(beat+1).padStart(2,'0')}</div>
  <div style={{position:'absolute',left:64,right:64,bottom:125,display:'flex',gap:12,alignItems:'end',height:85}}>{Array.from({length:24},(_,i)=><div key={i} style={{flex:1,height:i%6===0?75:25+(i%3)*12,background:f>=i*7.5?p.accent:'#2c343d',borderRadius:4}}/>)}</div>
 </Frame>;
};

const Stack:React.FC<Props>=(p)=>{
 const f=useCurrentFrame(); const text=['先看见问题','再看懂变化','最后记住结果'];
 return <Frame {...p} number="013" title="短句累积">
 <div style={{position:'absolute',top:137,left:70,width:690}}>{text.map((t,i)=>{const reveal=i===0?1:interpolate(f,[i*33,i*33+15],[0,1],ease);return <div key={t} style={{display:'flex',alignItems:'center',gap:25,height:112,opacity:reveal,translate:`${(1-reveal)*45}px 0`}}><span style={{fontSize:22,color:p.accent,border:`1px solid ${p.accent}`,borderRadius:'50%',width:49,height:49,display:'grid',placeItems:'center'}}>{i+1}</span><span style={{fontSize:51,fontWeight:800}}>{t}</span></div>})}</div>
 <div style={{position:'absolute',left:815,top:172,width:3,height:294,background:'#34404b'}}/>
 <div style={{position:'absolute',left:815,top:172,width:3,height:interpolate(f,[0,99],[0,294],ease),background:p.accent}}/>
 <div style={{position:'absolute',right:67,top:252,width:310,opacity:interpolate(f,[96,115],[0,1],ease),translate:`0 ${interpolate(f,[96,115],[25,0],ease)}px`}}><div style={{fontSize:20,color:p.accent}}>三步，形成一个完整解释</div><div style={{fontSize:68,fontWeight:900,marginTop:20}}>看懂了。</div></div>
 <div style={{position:'absolute',bottom:116,left:72,color:'#a2aab5',fontSize:23}}>前面的意思还在，新的信息继续向前。</div>
 </Frame>;
};

const Tiles:React.FC<{aligned:boolean;accent:string}> = ({aligned,accent})=><div style={{position:'absolute',inset:0}}>{Array.from({length:6},(_,i)=>{const x=aligned?90+(i%3)*155:95+(i%3)*158+((i%2)?30:-20);const y=aligned?60+Math.floor(i/3)*110:60+Math.floor(i/3)*105+((i%3)-1)*20;return <div key={i} style={{position:'absolute',left:x,top:y,width:127,height:78,background:aligned?accent:'#596573',rotate:aligned?'0deg':`${(i%3-1)*13}deg`,borderRadius:12,color:aligned?'#12171c':Ink,fontSize:27,display:'grid',placeItems:'center',fontWeight:800}}>{String(i+1).padStart(2,'0')}</div>})}</div>;
const Compare:React.FC<Props>=(p)=>{
 const f=useCurrentFrame();const wipe=interpolate(f,[39,99],[0,100],ease);
 return <Frame {...p} number="014" title="同构图对比"><div style={{marginTop:40,fontWeight:900,fontSize:47}}>对象不变，变化一眼看见。</div>
 <div style={{position:'absolute',top:232,left:160,width:960,height:330,background:'#1c242d',borderRadius:18,overflow:'hidden'}}><div style={{position:'absolute',left:140,top:17,width:680,height:300}}><Tiles aligned={false} accent={p.accent}/></div><div style={{position:'absolute',inset:0,background:'#263529',clipPath:`inset(0 ${100-wipe}% 0 0)`}}><div style={{position:'absolute',left:140,top:17,width:680,height:300}}><Tiles aligned accent={p.accent}/></div></div>{wipe>0&&wipe<100&&<div style={{position:'absolute',left:`${wipe}%`,top:0,bottom:0,width:3,background:Ink}}/>}</div>
 <div style={{position:'absolute',top:193,left:162,color:f<70?'#a2aab5':p.accent,fontSize:22}}>{f<70?'BEFORE / 散乱':'AFTER / 对齐'}</div></Frame>;
};

const Relay:React.FC<Props>=(p)=>{
 const f=useCurrentFrame();const scene=Math.min(2,Math.floor(f/60));const t=f-scene*60;
 const titles=['选择目标','完成操作','展示结果'];
 return <Frame {...p} number="015" title="演示接力">
 <div style={{display:'flex',gap:15,marginTop:42}}>{titles.map((v,i)=><div key={v} style={{flex:1,borderTop:`3px solid ${i<=scene?p.accent:'#39404a'}`,paddingTop:15,color:i===scene?Ink:'#828d99',fontSize:24}}>{i+1} / {v}</div>)}</div>
 <div style={{position:'absolute',left:65,top:245,width:420,fontSize:71,fontWeight:900,lineHeight:1.3}}>{titles[scene]}<div style={{fontSize:23,fontWeight:400,color:'#a2aab5',marginTop:27}}>动作完成，直接交接。</div></div>
 <div style={{position:'absolute',left:600,right:85,top:230,bottom:117,display:'flex',gap:18,alignItems:'center',justifyContent:'center'}}>
 {scene===0&&[0,1,2].map(i=><div key={i} style={{width:130,height:155,borderRadius:17,border:`2px solid ${i===1&&t>15?p.accent:'#536071'}`,background:i===1&&t>15?p.accent:'#222d37',color:i===1&&t>15?'#101419':Ink,translate:`0 ${i===1?interpolate(t,[15,35],[0,-20],ease):0}px`,display:'grid',placeItems:'center',fontSize:49,fontWeight:800}}>{i+1}</div>)}
 {scene===1&&<div style={{width:380}}><div style={{fontSize:23,marginBottom:25}}>让一个变化完整发生</div><div style={{height:28,borderRadius:14,background:'#34404d',overflow:'hidden'}}><div style={{height:'100%',width:`${interpolate(t,[0,35],[0,100],ease)}%`,background:p.accent}}/></div><div style={{marginTop:23,fontSize:62,color:p.accent,fontWeight:900}}>{Math.round(interpolate(t,[0,35],[0,100],ease))}%</div></div>}
 {scene===2&&<div style={{width:205,height:205,borderRadius:'50%',background:p.accent,color:'#17231b',fontSize:112,display:'grid',placeItems:'center',scale:interpolate(t,[0,12],[.86,1],ease)}}>✓</div>}
 </div></Frame>;
};
const Root=()=> <>{[Accent,Stack,Compare,Relay].map((C,i)=><Composition key={i} id={`Prompt0${12+i}`} component={C} width={1280} height={720} fps={30} durationInFrames={180} defaultProps={defaults}/>)}</>;
registerRoot(Root);
