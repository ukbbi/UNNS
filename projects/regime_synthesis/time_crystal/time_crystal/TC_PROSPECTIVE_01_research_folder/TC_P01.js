(function(){
  "use strict";

  const DATA=window.TC_P01_DATA||{campaign:{},records:[],documents:[]};
  const state={selected:null,role:"",stage:"",verdict:""};

  const $=sel=>document.querySelector(sel);
  const esc=x=>String(x??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[m]));
  const fmt=(v,n=6)=>{
    if(v===null||v===undefined||v==="")return "—";
    if(typeof v==="number")return Number.isInteger(v)?String(v):v.toFixed(n);
    return String(v);
  };
  const statusBadge=s=>{
    const status=s||"—";const cls=status==="N/A"?"NA":status;
    return `<span class="badge ${esc(cls)}">${esc(status)}</span>`;
  };

  function temporal(r){return r.sectors?.temporal||{}}
  function metric(r,k){
    const t=temporal(r);
    return t.metrics?.[k] ?? t[k] ?? null;
  }

  function filtered(){
    return DATA.records.filter(r=>
      (!state.role||r.role===state.role)&&
      (!state.stage||r.stage===state.stage)&&
      (!state.verdict||r.verdict===state.verdict)
    );
  }

  function renderStats(){
    const c=DATA.campaign||{};
    const stats=[
      ["Candidates",c.candidate_count??0],
      ["Controls",c.control_count??0],
      ["Closed",c.closed_count??0],
      ["Blind locked",c.blind_locked_count??0],
      ["Locked records",c.record_count??0],
    ];
    $("#stats").innerHTML=stats.map(([lab,n])=>
      `<div class="stat"><div class="n">${esc(n)}</div><div class="lab">${esc(lab)}</div></div>`
    ).join("");
    $("#principle").textContent=c.principle||"Analyze first, lock second, reveal third, interpret fourth.";
    $("#generatedAt").textContent=c.generated_at?`Data refresh: ${c.generated_at}`:"";
  }

  function renderProgress(){
    const candidates=DATA.records.filter(r=>r.role==="CANDIDATE");
    $("#progressTrack").innerHTML=candidates.map(r=>{
      const q=metric(r,"q0");
      return `<div class="progress-item">
        <div class="pid">${esc(r.id)}</div>
        <div class="sub">${esc(r.verdict)} · q₀=${esc(q??"—")}</div>
        <div class="stage stage-${esc(r.stage)}">${esc(r.stage)}</div>
      </div>`;
    }).join("") || `<div class="muted">No prospective candidates found under locked_runs.</div>`;
  }

  function initFilters(){
    [...new Set(DATA.records.map(r=>r.verdict))].sort().forEach(v=>{
      const o=document.createElement("option");o.value=v;o.textContent=v;$("#verdictFilter").appendChild(o);
    });
    $("#roleFilter").addEventListener("change",e=>{state.role=e.target.value;syncSelection();});
    $("#stageFilter").addEventListener("change",e=>{state.stage=e.target.value;syncSelection();});
    $("#verdictFilter").addEventListener("change",e=>{state.verdict=e.target.value;syncSelection();});
  }

  function syncSelection(){
    const rows=filtered();
    if(!rows.some(r=>r.id===state.selected))state.selected=rows[0]?.id||null;
    renderTable();
    const r=rows.find(r=>r.id===state.selected);
    if(r)renderDetail(r); else renderEmpty();
  }

  function renderTable(){
    const tb=$("#registryTable tbody");tb.innerHTML="";
    filtered().forEach(r=>{
      const tr=document.createElement("tr");
      if(r.id===state.selected)tr.classList.add("active");
      const s=r.sectors||{};
      tr.innerHTML=`
        <td><b>${esc(r.id)}</b><br><span class="muted small">${esc(r.domain)}</span></td>
        <td class="role-${esc(r.role)}"><b>${esc(r.role)}</b></td>
        <td><span class="stage stage-${esc(r.stage)}">${esc(r.stage)}</span></td>
        <td>${esc(metric(r,"q0")??"—")}</td>
        <td>${esc(fmt(metric(r,"closure")))}</td>
        <td>${esc(fmt(metric(r,"family_contrast")))}</td>
        <td>${esc(fmt(metric(r,"shuffle_p")))}</td>
        <td>${statusBadge(s.temporal?.status)}</td>
        <td>${statusBadge(s.rigidity?.status)}</td>
        <td>${statusBadge(s.collective?.status)}</td>
        <td>${statusBadge(s.spectral?.status)}</td>
        <td><span class="verdict v-${esc(r.verdict)}">${esc(r.verdict)}</span></td>`;
      tr.addEventListener("click",()=>{state.selected=r.id;renderTable();renderDetail(r)});
      tb.appendChild(tr);
    });
  }

  function sectorCard(name,obj){
    obj=obj||{};
    const metrics=obj.metrics||{};
    const entries=[];
    for(const [k,v] of Object.entries(metrics))entries.push([k,v]);
    if(name==="Temporal"){
      for(const key of ["q0","closure","family_contrast","shuffle_p"]){
        if(obj[key]!==undefined && !entries.some(([k])=>k===key))entries.push([key,obj[key]]);
      }
    }
    if(obj.basis)entries.push(["basis",obj.basis]);
    if(obj.missing?.length)entries.push(["missing",obj.missing.join("; ")]);
    if(obj.reasons?.length)entries.push(["reasons",obj.reasons.join("; ")]);
    return `<div class="sector">
      <h3>${esc(name)}</h3>
      ${statusBadge(obj.status)}
      <div class="kv">${entries.map(([k,v])=>
        `<div class="k">${esc(k)}</div><div class="v">${esc(typeof v==="number"?fmt(v):v)}</div>`
      ).join("")}</div>
    </div>`;
  }

  function compareControl(r){
    if(r.role!=="CANDIDATE")return null;
    let ctrl=DATA.records.find(x=>x.id===`${r.id}_CTRL`);
    if(!ctrl && r.id.endsWith("C001"))ctrl=DATA.records.find(x=>x.id.includes("NRCTRL"));
    return ctrl||null;
  }

  function renderDetail(r){
    const s=r.sectors||{};
    const post=r.posthoc;
    const ctrl=compareControl(r);
    const revealClass=post?`<span class="reveal-done">${esc(r.reveal_status)}</span>`:
      `<span class="reveal-locked">BLIND LOCKED — NOT REVEALED</span>`;

    const linkItems=Object.entries(r.links||{}).filter(([,href])=>href);
    $("#detail").innerHTML=`
      <div class="detail-head">
        <div>
          <div class="eyebrow">${esc(r.role)} · ${esc(r.stage)}</div>
          <h2>${esc(r.id)}</h2>
          <div class="detail-meta">
            <span class="pill">${esc(r.domain)}</span>
            <span class="pill">Level ${esc(r.level??"—")}</span>
            <span class="pill">q₀ ${esc(metric(r,"q0")??"—")}</span>
          </div>
        </div>
        <div>
          <div class="verdict v-${esc(r.verdict)}">${esc(r.verdict)}</div>
          <div class="small" style="margin-top:6px">${revealClass}</div>
        </div>
      </div>

      <div class="sectors">
        ${sectorCard("Temporal",s.temporal)}
        ${sectorCard("Rigidity",s.rigidity)}
        ${sectorCard("Collective",s.collective)}
        ${sectorCard("Spectral",s.spectral)}
      </div>

      <div class="detail-grid">
        <div class="block">
          <h3>Blind analysis lock</h3>
          <div class="kv">
            <div class="k">mode</div><div>${esc(r.lock?.mode||"—")}</div>
            <div class="k">evidence SHA</div><div class="hash">${esc(r.lock?.candidate_evidence_sha256||"—")}</div>
            <div class="k">metric SHA</div><div class="hash">${esc(r.lock?.frozen_metric_sha256||"—")}</div>
            <div class="k">protocol SHA</div><div class="hash">${esc(r.lock?.protocol_sha256||"—")}</div>
            <div class="k">analysis lock</div><div class="hash">${esc(r.lock?.analysis_lock_sha256||"—")}</div>
          </div>
        </div>

        <div class="block">
          <h3>Reveal / comparison</h3>
          ${post?`
            <div class="kv">
              <div class="k">status</div><div>${esc(post.status||"—")}</div>
              <div class="k">physical class</div><div>${esc(post.physical_class||"—")}</div>
              <div class="k">expected verdict</div><div>${esc(post.expected_verdict??"None")}</div>
              <div class="k">blind verdict</div><div>${esc(post.observed_blind_verdict||r.verdict)}</div>
              <div class="k">match</div><div>${esc(post.verdict_match??"N/A")}</div>
            </div>`:
            `<div class="reveal-locked"><b>Ground truth not revealed.</b></div>
             <p class="muted small">The campaign shell does not read ground_truth directly. Reveal data appears here only after posthoc_comparison.json exists.</p>`
          }
        </div>

        <div class="block">
          <h3>Verdict path</h3>
          ${(r.path?.length)?`<ol>${r.path.map(x=>`<li>${esc(x)}</li>`).join("")}</ol>`:
            `<div class="muted small">No verdict path recorded.</div>`}
        </div>

        <div class="block">
          <h3>${ctrl?"Matched control":"Record files"}</h3>
          ${ctrl?`
            <div class="kv">
              <div class="k">control</div><div>${esc(ctrl.id)}</div>
              <div class="k">verdict</div><div class="verdict v-${esc(ctrl.verdict)}">${esc(ctrl.verdict)}</div>
              <div class="k">q₀</div><div>${esc(metric(ctrl,"q0")??"—")}</div>
              <div class="k">F</div><div>${esc(fmt(metric(ctrl,"family_contrast")))}</div>
              <div class="k">shuffle p</div><div>${esc(fmt(metric(ctrl,"shuffle_p")))}</div>
            </div>`:""}
          <div class="links" style="margin-top:10px">
            ${linkItems.map(([k,href])=>`<a href="${esc(href)}">${esc(k)}</a>`).join("")}
          </div>
        </div>
      </div>`;
  }

  function renderEmpty(){
    $("#detail").innerHTML=`<h2>No records match the current filters.</h2>`;
  }

  function renderDocs(){
    $("#docs").innerHTML=(DATA.documents||[]).map(d=>
      `<a class="doc-card" href="${esc(d.href)}"><b>${esc(d.label)}</b><span>${esc(d.href)}</span></a>`
    ).join("");
  }

  function csvCell(v){
    const s=String(v??"");return /[",\r\n]/.test(s)?`"${s.replace(/"/g,'""')}"`:s;
  }
  function toCsv(rows){
    const h=["id","role","stage","domain","q0","closure","family_contrast","shuffle_p",
      "temporal","rigidity","collective","spectral","verdict","level","reveal_status","analysis_lock"];
    const lines=[h.join(",")];
    rows.forEach(r=>{
      const s=r.sectors||{};
      const a=[
        r.id,r.role,r.stage,r.domain,metric(r,"q0"),metric(r,"closure"),metric(r,"family_contrast"),
        metric(r,"shuffle_p"),s.temporal?.status,s.rigidity?.status,s.collective?.status,
        s.spectral?.status,r.verdict,r.level,r.reveal_status,r.lock?.analysis_lock_sha256
      ];
      lines.push(a.map(csvCell).join(","));
    });
    return "\uFEFF"+lines.join("\r\n");
  }
  function download(name,text,mime){
    const blob=new Blob([text],{type:`${mime};charset=utf-8`});
    const url=URL.createObjectURL(blob);const a=document.createElement("a");
    a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),900);
  }

  $("#exportCampaign").addEventListener("click",()=>download(
    "TC_P01_campaign.json",JSON.stringify(DATA,null,2),"application/json"
  ));
  $("#exportCsv").addEventListener("click",()=>download(
    "TC_P01_visible.csv",toCsv(filtered()),"text/csv"
  ));

  renderStats();renderProgress();initFilters();renderDocs();
  const first=DATA.records.find(r=>r.role==="CANDIDATE")||DATA.records[0];
  state.selected=first?.id||null;
  renderTable();
  if(first)renderDetail(first);else renderEmpty();
})();