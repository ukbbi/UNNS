let activeJob = null;
let currentRun = null;

const $ = id => document.getElementById(id);
const fmt = v => (v===null || v===undefined || Number.isNaN(Number(v))) ? "—" :
  (Math.abs(Number(v)) < 0.001 && Number(v)!==0 ? Number(v).toExponential(3) : Number(v).toFixed(4));

function setStatus(cls, text){
  const el=$("statusTag"); el.className="htag "+cls; el.textContent=text;
}
function stat(k,v){
  return `<div class="stat"><div class="k">${k}</div><div class="v">${v}</div></div>`;
}
function setStats(id, rows){
  $(id).innerHTML=rows.map(([k,v])=>stat(k,v)).join("");
}
function log(msg){ $("runLog").textContent=msg; }

async function start(url, options={}){
  setStatus("running","RUNNING");
  partialRendered=false;
  $("provisionalBanner").style.display="none";
  $("nullLiveStats").innerHTML="";
  $("downloadBtn").disabled=true;
  currentRun=null;
  const r=await fetch(url, options);
  if(!r.ok){ const t=await r.text(); throw new Error(t); }
  const j=await r.json(); activeJob=j.job_id; poll();
}
async function runFixture(name){
  try{ await start(`/api/fixture/${name}`,{method:"POST"}); }
  catch(e){ setStatus("error","ERROR"); log(e.message); }
}
$("filesForm").addEventListener("submit", async e=>{
  e.preventDefault();
  try{ await start("/api/run-files",{method:"POST",body:new FormData(e.target)}); }
  catch(err){ setStatus("error","ERROR"); log(err.message); }
});
$("bundleForm").addEventListener("submit", async e=>{
  e.preventDefault();
  try{ await start("/api/run-bundle",{method:"POST",body:new FormData(e.target)}); }
  catch(err){ setStatus("error","ERROR"); log(err.message); }
});

let partialRendered=false;

function fmtTime(sec){
  if(sec===null || sec===undefined || !isFinite(sec)) return "—";
  sec=Math.max(0,Math.round(sec));
  const m=Math.floor(sec/60), s=sec%60;
  return m ? `${m}m ${s}s` : `${s}s`;
}

async function poll(){
  if(!activeJob)return;
  const r=await fetch(`/api/status/${activeJob}`);
  const j=await r.json();
  log(`${(100*(j.progress||0)).toFixed(1)}% · ${j.phase||""}\n${j.message||""}`);

  if(j.partial_result && !partialRendered){
    renderStructure(j.partial_result,true);
    partialRendered=true;
  }
  if(j.null_progress){
    const p=j.null_progress;
    setStats("nullLiveStats",[
      ["NULL",`${p.null_index}/${p.null_count}`],
      ["ACCEPTED SWAPS",p.accepted_swaps_current],
      ["CURRENT MOBILITY",fmt(p.mobility_current)],
      ["MEAN MOBILITY",fmt(p.mean_mobility_so_far)],
      ["ELAPSED",fmtTime(p.elapsed_seconds)],
      ["ETA",fmtTime(p.eta_seconds)]
    ]);
  }

  if(j.status==="COMPLETE"){
    setStatus("done","COMPLETE"); currentRun=j.run_id; render(j.result);
    $("downloadBtn").disabled=false; activeJob=null; partialRendered=false; return;
  }
  if(j.status==="ERROR"){
    setStatus("error","ERROR"); log(j.error||j.message||"Unknown error");
    activeJob=null; partialRendered=false; return;
  }
  setTimeout(poll,500);
}
$("downloadBtn").addEventListener("click",()=>{
  if(currentRun) window.location=`/api/download/${encodeURIComponent(currentRun)}`;
});

function renderStructure(r, provisional=false){
  const inp=r.input, s=r.structure.scale, t=r.structure.time, st=r.structure.stitch;
  $("provisionalBanner").style.display=provisional?"":"none";
  setStats("inputStats",[
    ["OBJECTS",inp.n_objects],["RELATIONS SUPPLIED",inp.n_relations_supplied],
    ["RELATIONS ELIGIBLE",inp.n_relations_eligible],["SCALE LAYERS",inp.scale_layers],["TIME LAYERS",inp.time_layers]
  ]);
  setStats("scaleStats",[
    ["SOURCE PERSISTENCE",fmt(s.persistence_mean_sources)],["P90 PERSISTENCE",fmt(s.persistence_p90_sources)],
    ["ROUTE ENTROPY",fmt(s.entropy_mean_sources)],["SOURCE N",s.source_nodes]
  ]);
  setStats("timeStats",[
    ["SOURCE PERSISTENCE",fmt(t.persistence_mean_sources)],["P90 PERSISTENCE",fmt(t.persistence_p90_sources)],
    ["ROUTE ENTROPY",fmt(t.entropy_mean_sources)],["SOURCE N",t.source_nodes]
  ]);
  setStats("scaleBranch",[
    ["BRANCH FRACTION",fmt(s.branch_fraction_all)],["MERGE FRACTION",fmt(s.merge_fraction_all)],
    ["MEAN OUT DEG",fmt(s.mean_out_degree_sources)],["CONSERVATION",fmt(s.conservation_mean)]
  ]);
  setStats("timeBranch",[
    ["BRANCH FRACTION",fmt(t.branch_fraction_all)],["MERGE FRACTION",fmt(t.merge_fraction_all)],
    ["MEAN OUT DEG",fmt(t.mean_out_degree_sources)],["CONSERVATION",fmt(t.conservation_mean)]
  ]);
  setStats("stitchStats",[
    ["ELIGIBLE SOURCES",st.eligible_sources],["CELLS",st.cells],["MEAN D□",fmt(st.mean_defect)],
    ["P90 D□",fmt(st.p90_defect)],["MAX D□",fmt(st.max_defect)]
  ]);

  const nq=r.null_quality||{};
  setStats("nullStats",[
    ["SWAP ATTEMPTS",nq.swap_attempts_total??"—"],
    ["SWAPS ACCEPTED",nq.swap_accepted_total??"—"],
    ["MEAN MOBILITY",fmt(nq.mean_mobility_fraction)],
    ["UNIQUE NULLS",nq.unique_graphs??"—"],
    ["UNIQUE FRACTION",fmt(nq.unique_graph_fraction)],
    ["REAL MATCH FRACTION",fmt(nq.real_graph_match_fraction)]
  ]);
  $("nullFlags").innerHTML=(nq.flags||[]).map(x=>`<span class="tag">${x}</span>`).join("");

  drawAxis("scaleCanvas",s,"SCALE");
  drawAxis("timeCanvas",t,"TIME");
  drawMetricCanvas(r);

  if(provisional){
    const ve=$("verdict");
    ve.textContent="PENDING NULL ENSEMBLE";
    ve.className="verdict under";
    $("tags").innerHTML='<span class="tag">REAL_METRICS_AVAILABLE</span>';
    return;
  }
}

function render(r){
  renderStructure(r,false);

  const tb=$("evidenceTable").querySelector("tbody"); tb.innerHTML="";
  for(const [name,test] of Object.entries(r.evidence.tests)){
    if(!test) continue;
    const tr=document.createElement("tr");
    tr.innerHTML=`<td>${name}</td><td>${fmt(test.real)}</td><td>${fmt(test.null_mean)}</td>
      <td>${fmt(test.null_std)}</td><td>${fmt(test.favorable_z)}</td>
      <td>${fmt(test.p_favorable)}</td><td>${fmt(test.p_opposing)}</td><td>${test.direction}</td>`;
    tb.appendChild(tr);
  }
  for(const [name,item] of Object.entries(r.evidence.descriptive_only||{})){
    const tr=document.createElement("tr");
    tr.title=item.reason||"";
    tr.innerHTML=`<td>${name} · DESCRIPTIVE</td><td>${fmt(item.real)}</td>
      <td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>non-inferential</td>`;
    tb.appendChild(tr);
  }
  const v=r.verdict.class, ve=$("verdict");
  ve.textContent=v; ve.className="verdict "+
    (v==="CONSTRAINED_ROUTING"?"constrained":v==="MIXED_ROUTING"?"mixed":
     v==="NULL_LIKE_ROUTING"?"null":"under");
  $("tags").innerHTML=(r.verdict.tags||[]).map(x=>`<span class="tag">${x}</span>`).join("");
}

function baseCanvas(id,title){
  const c=$(id), dpr=window.devicePixelRatio||1, W=Math.max(500,c.clientWidth), H=parseInt(c.getAttribute("height"));
  c.width=W*dpr;c.height=H*dpr;const x=c.getContext("2d");x.scale(dpr,dpr);
  x.clearRect(0,0,W,H);x.fillStyle="#5a7a96";x.font="10px Consolas";x.fillText(title,12,16);
  return {x,W,H};
}
function drawBars(id,vals,title){
  const {x,W,H}=baseCanvas(id,title), pad=36, bw=(W-2*pad)/Math.max(1,vals.length);
  vals.forEach((q,i)=>{
    let v=q[1]; if(v===null||v===undefined||!isFinite(v))v=0;
    v=Math.max(0,Math.min(1,Number(v)));
    const h=v*(H-70), xx=pad+i*bw+bw*.18, y=H-30-h;
    x.fillStyle="#00c8f088";x.fillRect(xx,y,bw*.64,h);
    x.fillStyle="#a8bfd0";x.font="9px Consolas";x.textAlign="center";
    x.fillText(q[0],xx+bw*.32,H-12);x.fillText(v.toFixed(3),xx+bw*.32,y-5);
  }); x.textAlign="left";
}
function drawAxis(id,s,title){
  drawBars(id,[
    ["PERSIST",s.persistence_mean_sources],
    ["ENTROPY",s.entropy_mean_sources],
    ["BRANCH",s.branch_fraction_all],
    ["MERGE",s.merge_fraction_all]
  ],title+" ROUTE PROFILE");
}
function drawMetricCanvas(r){
  drawBars("metricCanvas",[
    ["S PERSIST",r.structure.scale.persistence_mean_sources],
    ["T PERSIST",r.structure.time.persistence_mean_sources],
    ["S ENTROPY",r.structure.scale.entropy_mean_sources],
    ["T ENTROPY",r.structure.time.entropy_mean_sources],
    ["STITCH",r.structure.stitch.mean_defect]
  ],"ROUTE METRIC VECTOR · no composite score");
}
