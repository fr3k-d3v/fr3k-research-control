// FR3K dynamic UI independent host reference fixture, 2026-11-27.
// SIMULATION ONLY. Viewport dimensions are synthetic test profiles, not hardware verification.
// This is not an A2UI implementation, production validator, authenticated transport or native renderer.
// One data model -> separate device surfaces -> SVG preview -> bounded action intent.
// Run: node research/fixtures/dynamic-ui-reference-2026-11-27.mjs
function generate(profile, state) {
  const w=profile.width,h=profile.height;
  const compact=h<200, wide=w>=600;
  const pad=compact?6:12, gap=compact?4:8, top=compact?24:48, foot=compact?27:46;
  const bodyH=h-top-foot-pad*2;
  const columns=wide?2:1, rows=wide?2:4;
  const cellW=Math.floor((w-pad*2-gap*(columns-1))/columns);
  const cellH=Math.floor((bodyH-gap*(rows-1))/rows);
  const items=[["online","Online"],["total","Registered"],["jobs","Active jobs"],["alerts","Alerts"]];
  const widgets=items.map(([key,label],i)=>({id:key,type:"metric",label,value:String(state[key]),x:pad+(i%columns)*(cellW+gap),y:top+Math.floor(i/columns)*(cellH+gap),w:cellW,h:cellH}));
  widgets.push({id:"refresh",type:"button",label:"Refresh fleet",action:"fleet.read.status",x:pad,y:h-foot,w:w-pad*2,h:foot-pad});
  return {schema:"fr3k.ui.fixture.v1",device:profile.id,width:w,height:h,revision:state.revision,widgets};
}
function patch(state, update) {
  if(update.base!==state.revision || update.revision!==state.revision+1) throw Error("stale revision");
  const values=update.values;
  for(const [key,value] of Object.entries(values)){
    if(!["online","total","jobs","alerts"].includes(key)||!Number.isSafeInteger(value)||value<0) throw Error("invalid data");
  }
  const next={...state,...values,revision:update.revision};
  if(next.online>next.total) throw Error("invalid counts");
  return next;
}
function validate(surface) {
  const ids=new Set();
  if(surface.schema!=="fr3k.ui.fixture.v1"||!Number.isSafeInteger(surface.revision)||surface.widgets.length>16) throw Error("invalid surface");
  for(const a of surface.widgets){
    if(ids.has(a.id)||!["metric","button"].includes(a.type)) throw Error("invalid widget");
    ids.add(a.id);
    if(![a.x,a.y,a.w,a.h].every(Number.isSafeInteger)||a.x<0||a.y<0||a.w<=0||a.h<=0||a.x+a.w>surface.width||a.y+a.h>surface.height) throw Error("bounds");
    if(a.type==="button"&&a.action!=="fleet.read.status") throw Error("action not allowed");
  }
  for(let i=0;i<surface.widgets.length;i++)for(let j=i+1;j<surface.widgets.length;j++){
    const a=surface.widgets[i],b=surface.widgets[j];
    if(a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y)throw Error("overlap");
  }
  return true;
}
function preview(s) {
  validate(s);
  const esc=x=>String(x).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${s.width}" height="${s.height}" viewBox="0 0 ${s.width} ${s.height}"><rect width="100%" height="100%" fill="#08151b"/><text x="8" y="16" font-family="monospace" font-size="12" fill="#5eead4">FR3K / FLEET</text>`+s.widgets.map(a=>`<rect x="${a.x}" y="${a.y}" width="${a.w}" height="${a.h}" rx="3" fill="#17333b"/><text x="${a.x+4}" y="${a.y+Math.min(a.h-2,Math.max(9,Math.floor(a.h*.65)))}" font-family="monospace" font-size="${Math.min(18,Math.max(8,Math.floor(a.h*.5)))}" fill="white">${esc(a.label)}${a.type==="metric"?": "+esc(a.value):""}</text>`).join("")+"</svg>";
}
function event(surface, message) {
  validate(surface);
  if(message.revision!==surface.revision||message.device!==surface.device) throw Error("stale/wrong target");
  const widget=surface.widgets.find(a=>a.id===message.widget);
  if(!widget||widget.type!=="button"||widget.action!=="fleet.read.status") throw Error("invalid action");
  return {kind:"action_intent",device:surface.device,revision:surface.revision,action:widget.action,requiresGatewayAuthorization:true};
}
function selftest(){
  const profiles=[{id:"tab5",width:1280,height:720},{id:"cardputer",width:240,height:135},{id:"watch-ultra",width:410,height:502},{id:"watch-s3",width:240,height:240},{id:"k10",width:320,height:240},{id:"k230",width:800,height:480},{id:"t-deck-plus",width:320,height:240},{id:"android",width:720,height:1280}];
  let passed=0;
  const assert=(v)=>{if(!v)throw Error("assertion");passed++};
  const reject=(fn)=>{let threw=false;try{fn()}catch{threw=true}assert(threw)};
  const s={online:2,total:10,jobs:3,alerts:1,revision:1};
  const n=patch(s,{base:1,revision:2,values:{online:4,alerts:0}});
  const examples=[];
  for(const p of profiles){
    const a=generate(p,s), b=generate(p,n);
    assert(validate(a));assert(validate(b));
    assert(preview(b).includes("Online: 4"));
    assert(event(b,{revision:2,device:p.id,widget:"refresh"}).requiresGatewayAuthorization);
    reject(()=>event(b,{revision:1,device:p.id,widget:"refresh"}));
    reject(()=>event(b,{revision:2,device:"wrong",widget:"refresh"}));
    const bad={...b,widgets:b.widgets.map(w=>w.type==="button"?{...w,action:"shell.execute"}:w)};
    reject(()=>validate(bad));
    reject(()=>validate({...b,widgets:b.widgets.map((w,i)=>i===0?{...w,w:p.width+1}:w)}));
    examples.push({profile:p.id,viewport:[p.width,p.height],widgets:b.widgets.length,svg:preview(b)});
  }
  reject(()=>patch(n,{base:1,revision:2,values:{online:3}}));
  reject(()=>patch(n,{base:2,revision:3,values:{online:99}}));
  reject(()=>patch(n,{base:2,revision:3,values:{command:1}}));
  return {passed,profiles:examples.map(({svg,...e})=>e),examples};
}
const result=selftest(); console.log(JSON.stringify(result,null,2));
