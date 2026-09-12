(function(){
  "use strict";

  const DATA = window.TIME_CRYSTAL_I_DATA || {chamber:{status:"NO DATA"},results:[]};

  function verdict(record){
    const s=record.sectors||{};
    const t=s.temporal||{}, r=s.rigidity||{}, c=s.collective||{}, p=s.spectral||{};
    const domain=record.domain;

    if(t.status!=="SUPPORTED") return {verdict:"NO_TEMPORAL_ORDER",level:0,path:["temporal recurrence/order not supported"],missing:[]};

    const path=[`temporal recurrence supported at q0=${t.q0}`];

    if(domain!=="quantum_many_body"){
      if(r.status==="SUPPORTED"){
        path.push("rigidity supported","many-body spectral admissibility not applicable to this domain");
        return {verdict:"RIGID_RECURRENCE",level:2,path,missing:[]};
      }
      path.push("higher recurrence rigidity not established");
      return {verdict:"TEMPORAL_RECURRENCE",level:1,path,missing:[]};
    }

    if(r.status!=="SUPPORTED"){
      path.push("quantum recurrence rigidity not supported");
      return {verdict:"TEMPORAL_RECURRENCE",level:1,path,missing:[]};
    }

    path.push("quantum recurrence rigidity supported");
    const missing=[];
    if(["NOT_TESTED","N/A"].includes(c.status)) missing.push("collective");
    if(["NOT_TESTED","N/A"].includes(p.status)) missing.push("spectral");

    if(missing.length){
      path.push("required quantum many-body sector evidence is missing");
      return {verdict:"INSUFFICIENT_DOMAIN_EVIDENCE",level:2,path,missing};
    }

    if(c.status!=="SUPPORTED"){
      path.push("collective many-body order not fully supported");
      return {verdict:"RIGID_RECURRENCE",level:2,path,missing};
    }

    path.push("collective many-body order supported");
    if(p.status!=="SUPPORTED"){
      path.push("many-body spectral/eigenstate breadth not fully supported");
      return {verdict:"COLLECTIVE_TEMPORAL_ORDER",level:3,path,missing};
    }

    path.push("many-body spectral/eigenstate breadth supported","all TIME-CRYSTAL-I quantum gates satisfied");
    return {verdict:"MANY_BODY_TIME_CRYSTAL_ADMISSIBLE",level:4,path,missing};
  }

  const state={results:DATA.results||[],selected:null,filter:""};

  const statusEl=document.getElementById("chamberStatus");
  statusEl.innerHTML=`<div class="big">${escapeHtml(DATA.chamber?.status||"UNKNOWN")}</div>
    <div class="small">TIME-CRYSTAL-I ${escapeHtml(DATA.chamber?.version||"1.1.0")}</div>`;
  document.getElementById("principle").textContent=DATA.chamber?.principle||"Temporal recurrence is necessary but not sufficient.";
  document.getElementById("corpusCount").textContent=` · ${state.results.length} records`;

  const filter=document.getElementById("verdictFilter");
  [...new Set(state.results.map(x=>x.verdict))].sort().forEach(v=>{
    const o=document.createElement("option");o.value=v;o.textContent=v;filter.appendChild(o);
  });
  filter.addEventListener("change",()=>{
    state.filter=filter.value;
    const shown=getVisibleResults();
    if(!shown.some(r=>r.id===state.selected)){
      state.selected=shown[0]?.id||null;
    }
    renderTable();
    if(shown.length) renderDetail(shown.find(r=>r.id===state.selected)||shown[0]);
    else renderEmptyDetail();
  });

  document.getElementById("candidateFile").addEventListener("change",ev=>{
    const file=ev.target.files?.[0]; if(!file)return;
    const reader=new FileReader();
    reader.onload=()=>{
      try{
        const loaded=JSON.parse(reader.result);
        let result;
        if(loaded && loaded.result && loaded.result.record){
          result={...loaded.result,browser_evaluated:true,external_loaded:true};
        }else if(loaded && loaded.record && loaded.verdict){
          result={...loaded,browser_evaluated:true};
        }else{
          const record=loaded;
          const e=verdict(record);
          result={id:record.id||"local",label:record.label||file.name,domain:record.domain||"unknown",
            ...e,record,browser_evaluated:true};
        }
        state.results=[result,...state.results.filter(x=>!x.browser_evaluated)];
        state.filter="";
        filter.value="";
        state.selected=result.id;
        document.getElementById("corpusCount").textContent=` · ${state.results.length} records`;
        renderTable();renderDetail(result);
      }catch(err){alert("Could not load candidate JSON: "+err.message);}
    };
    reader.readAsText(file);
  });

  const exportButton=document.getElementById("exportButton");
  const exportMenu=document.getElementById("exportMenu");
  exportButton.addEventListener("click",ev=>{
    ev.stopPropagation();
    exportMenu.hidden=!exportMenu.hidden;
  });
  document.addEventListener("click",()=>{exportMenu.hidden=true;});
  exportMenu.addEventListener("click",ev=>{
    ev.stopPropagation();
    const action=ev.target?.dataset?.export;
    if(!action)return;
    exportMenu.hidden=true;
    handleExport(action);
  });

  function getVisibleResults(){
    return state.results.filter(r=>!state.filter||r.verdict===state.filter);
  }

  function currentResult(){
    return state.results.find(r=>r.id===state.selected)||getVisibleResults()[0]||null;
  }

  function renderTable(){
    const tbody=document.querySelector("#corpusTable tbody");tbody.innerHTML="";
    const shown=getVisibleResults();
    shown.forEach(r=>{
      const s=r.record.sectors;const tr=document.createElement("tr");
      if(state.selected===r.id)tr.classList.add("active");
      tr.innerHTML=`
        <td><strong>${escapeHtml(r.label)}</strong><br><span class="muted">${escapeHtml(r.record.expected_physics_class||"")}</span></td>
        <td>${escapeHtml(r.domain)}</td>
        <td>${s.temporal.q0??"—"}</td>
        <td>${badge(s.temporal.status)}</td>
        <td>${badge(s.rigidity.status)}</td>
        <td>${badge(s.collective.status)}</td>
        <td>${badge(s.spectral.status)}</td>
        <td><span class="verdict v-${r.verdict}">${escapeHtml(r.verdict)}</span></td>`;
      tr.addEventListener("click",()=>{state.selected=r.id;renderTable();renderDetail(r);});
      tbody.appendChild(tr);
    });
  }

  function renderDetail(r){
    const rec=r.record,s=rec.sectors;
    const browser=verdict(rec);
    const parity=browser.verdict===r.verdict;
    const detail=document.getElementById("detail");
    detail.innerHTML=`
      <div class="detail-head">
        <div><h2>${escapeHtml(r.label)}</h2>
          <div class="muted">${escapeHtml(rec.expected_physics_class||"")} · ${escapeHtml(r.domain)}</div></div>
        <div><div class="verdict v-${r.verdict}">${escapeHtml(r.verdict)}</div>
          <div class="muted">JS/Python verdict parity: ${parity?"PASS":"MISMATCH"}</div>
          <div class="export-note">Use Export ▾ above to save this result for outside analysis.</div></div>
      </div>
      <div class="sectors">
        ${sectorCard("Temporal",s.temporal)}
        ${sectorCard("Rigidity",s.rigidity)}
        ${sectorCard("Collective",s.collective)}
        ${sectorCard("Spectral",s.spectral)}
      </div>
      <div class="path"><strong>Verdict path</strong><ol>${(r.path||browser.path).map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ol></div>
      <div class="path"><strong>Provenance</strong><ul>${(rec.provenance||[]).map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul></div>`;
  }

  function renderEmptyDetail(){
    document.getElementById("detail").innerHTML="<h2>No records in this filter</h2><p class='muted'>Choose another verdict filter.</p>";
  }

  function sectorCard(name,obj){
    const entries=Object.entries(obj).filter(([k])=>k!=="status");
    return `<div class="sector"><h3>${escapeHtml(name)}</h3>${badge(obj.status)}
      <div class="kv" style="margin-top:10px">${entries.map(([k,v])=>`<div class="k">${escapeHtml(k)}</div><div>${escapeHtml(format(v))}</div>`).join("")}</div></div>`;
  }

  function handleExport(action){
    const selected=currentResult();
    if(action==="selected-json"){
      if(!selected)return alert("No selected result to export.");
      const payload={
        export_type:"TIME-CRYSTAL-I selected result",
        chamber:DATA.chamber,
        exported_at:new Date().toISOString(),
        result:selected
      };
      downloadText(`${safeName(selected.id)}_TCI_result.json`,JSON.stringify(payload,null,2),"application/json");
      return;
    }

    if(action==="selected-md"){
      if(!selected)return alert("No selected result to export.");
      downloadText(`${safeName(selected.id)}_TCI_report.md`,resultMarkdown(selected),"text/markdown");
      return;
    }

    if(action==="filtered-csv"){
      const rows=getVisibleResults();
      downloadText(`TIME-CRYSTAL-I_visible_${safeName(state.filter||"all")}.csv`,resultsCsv(rows),"text/csv");
      return;
    }

    if(action==="all-json"){
      const payload={
        export_type:"TIME-CRYSTAL-I full chamber results",
        chamber:DATA.chamber,
        dependencies:DATA.dependencies||{},
        exported_at:new Date().toISOString(),
        results:state.results
      };
      downloadText("TIME-CRYSTAL-I_results.json",JSON.stringify(payload,null,2),"application/json");
      return;
    }

    if(action==="all-csv"){
      downloadText("TIME-CRYSTAL-I_corpus.csv",resultsCsv(state.results),"text/csv");
    }
  }

  function resultMarkdown(r){
    const rec=r.record,s=rec.sectors;
    const lines=[
      `# TIME-CRYSTAL-I — ${r.label}`,
      "",
      `- Chamber version: ${DATA.chamber?.version||"1.1.0"}`,
      `- Record ID: \`${r.id}\``,
      `- Domain: \`${r.domain}\``,
      `- Expected physics class: ${rec.expected_physics_class||"—"}`,
      `- Verdict: **${r.verdict}**`,
      `- Level: ${r.level}`,
      "",
      "## Sectors",
      ""
    ];
    for(const [name,obj] of Object.entries(s)){
      lines.push(`### ${capitalize(name)}`,`Status: **${obj.status}**`,"");
      for(const [k,v] of Object.entries(obj)){
        if(k==="status")continue;
        lines.push(`- ${k}: ${format(v)}`);
      }
      lines.push("");
    }
    lines.push("## Verdict path","",...(r.path||verdict(rec).path).map((x,i)=>`${i+1}. ${x}`),"");
    lines.push("## Provenance","",...(rec.provenance||[]).map(x=>`- ${x}`),"");
    lines.push(`Exported: ${new Date().toISOString()}`);
    return lines.join("\n");
  }

  function resultsCsv(rows){
    const headers=[
      "id","label","domain","expected_physics_class","q0",
      "temporal_status","rigidity_status","collective_status","spectral_status",
      "verdict","level","browser_evaluated"
    ];
    const out=[headers.join(",")];
    rows.forEach(r=>{
      const s=r.record.sectors;
      const vals=[
        r.id,r.label,r.domain,r.record.expected_physics_class||"",
        s.temporal.q0??"",
        s.temporal.status,s.rigidity.status,s.collective.status,s.spectral.status,
        r.verdict,r.level,r.browser_evaluated?true:false
      ];
      out.push(vals.map(csvCell).join(","));
    });
    return "\uFEFF"+out.join("\r\n");
  }

  function downloadText(filename,text,mime){
    const blob=new Blob([text],{type:`${mime};charset=utf-8`});
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;a.download=filename;
    document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }

  function csvCell(v){
    const s=String(v??"");
    return /[",\r\n]/.test(s)?`"${s.replace(/"/g,'""')}"`:s;
  }
  function safeName(v){
    return String(v||"export").replace(/[^A-Za-z0-9._-]+/g,"_").slice(0,80);
  }
  function capitalize(v){return v.charAt(0).toUpperCase()+v.slice(1)}
  function badge(status){
    const cls=status==="N/A"?"NA":status;
    return `<span class="badge ${cls}">${escapeHtml(status)}</span>`;
  }
  function format(v){
    if(typeof v==="number")return Number.isInteger(v)?String(v):v.toFixed(6);
    if(typeof v==="boolean")return v?"true":"false";
    if(Array.isArray(v))return v.join(", ");
    if(v&&typeof v==="object")return JSON.stringify(v);
    return String(v??"—");
  }
  function escapeHtml(x){
    return String(x).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[m]));
  }

  renderTable();
  if(state.results.length){
    state.selected=state.results[0].id;
    renderTable();
    renderDetail(state.results[0]);
  }else{
    renderEmptyDetail();
  }
})();
