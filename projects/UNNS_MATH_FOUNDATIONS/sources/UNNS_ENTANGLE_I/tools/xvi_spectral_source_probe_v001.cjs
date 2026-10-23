'use strict';
/** Read-only extraction of the ORIGINAL class into Node VM, no edits to canonical HTML. */
const fs=require('fs'),path=require('path'),crypto=require('crypto'),vm=require('vm');
const root=path.resolve(__dirname,'..');
const source=path.join(root,'docs/sources/XVI_ENGINE_v084.html');
const html=fs.readFileSync(source,'utf8');
const sha=crypto.createHash('sha256').update(html).digest('hex');
const lock=JSON.parse(fs.readFileSync(path.join(root,'config/XVI_SPECTRAL_LOCK_v001.json'),'utf8'));
if(sha!==lock.inputs.canonical_html.sha256)throw Error('canonical SHA-256 mismatch');
const start=html.indexOf('class TauFieldEngineN {');const end=html.indexOf('</script>',start);
if(start<0||end<0)throw Error('Original engine class not found');
const ctx={console:{log:()=>{}},module:{exports:{}},Math,Float64Array,performance:{now:()=>0}};
vm.runInNewContext(html.slice(start,end),ctx,{timeout:15000});
const Engine=ctx.module.exports;
const cases=[];
for(const N of [64,128])for(const seed of [41]){
 const E=new Engine({grid_width:N,operator_mode:'XVI',init_mode:'random',lambda:0.1,beta:0.000002,
  alpha_c:0.01,gamma_closure:0.00001,closure_interval:6,laplacian_mode:'fft',seed});
 // original constructor uses config.sigma || 0.02; explicit assignment avoids stochastic evolution
 E.sigma=0; E.anneal_sigma=0;
 for(const step of [0,24]){
   while(E.step_count<step)E.step();
   E.captureSpectrum();const s=E.getLatestSpectrum();
   const tau=Array.from(E.getField());
   const Pk=Array.from(s.Pk); const k=Array.from(s.k);
   cases.push({name:`original_engine_N${N}_seed${seed}_step${step}`,N,seed,step,
     tau,original_js:{k,Pk,p:Number.isFinite(s.p)?s.p:null,r2:Number.isFinite(s.r2)?s.r2:null,n:s.n}});
 }
}
const out={protocol:'XVI_SPECTRAL_SOURCE_RAW_v001',source_sha256:sha,source_unmodified:true,
 scope:'New source-executed fields, NOT historical export fields',
 evolution_settings:{operator_mode:'XVI',init_mode:'random',sigma:0,anneal_sigma:0,closure_interval:6,lambda:0.1,beta:2e-6,alpha_c:0.01,gamma_closure:1e-5},cases};
const dest=path.join(root,'output/XVI_SPECTRAL_SOURCE_RAW_v001.json');
fs.writeFileSync(dest,JSON.stringify(out)+'\n');
console.log('WROTE '+path.relative(root,dest)+' ('+cases.length+' original-engine field snapshots)');
