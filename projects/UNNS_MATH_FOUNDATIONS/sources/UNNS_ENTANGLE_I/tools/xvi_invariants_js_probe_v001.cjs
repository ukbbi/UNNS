'use strict';
// Optional comparison of source calculations on shared 64² fields. Original HTML unchanged.
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'docs/sources/XVI_ENGINE_v084.html'),'utf8');
const lock=JSON.parse(fs.readFileSync(path.join(root,'config/XVI_INVARIANTS_LOCK_v001.json')));
const digest=crypto.createHash('sha256').update(html).digest('hex');
if(digest!==lock.inputs.html.sha256)throw new Error('Canonical HTML source integrity failure');
const begin=html.indexOf('class TauFieldEngineN {');const end=html.indexOf('</script>',begin);
if(begin<0||end<0)throw new Error('Original engine class missing');
const ctx={console:{log:()=>{}},module:{exports:{}},Math,Float64Array,performance:{now:()=>0}};
vm.runInNewContext(html.slice(begin,end),ctx);
const Engine=ctx.module.exports;
const inp=JSON.parse(fs.readFileSync(path.join(root,'output/XVI_INVARIANTS_JS_FIXTURE_v001.json')));
const report=[];
for(const entry of inp.cases){
 const eng=new Engine({grid_width:entry.N,operator_mode:'XVI',init_mode:'zero',lambda:0.1,beta:0.000002,
                    alpha_c:0.01,gamma_closure:0.00001,closure_interval:6,laplacian_mode:'fft',seed:41});
 eng.fields[0].tau.set(entry.values);
 let bestMu=1.618,bestDelta=Infinity;
 for(let mu=1.600;mu<=1.640;mu+=0.001){const x=eng.computeScaleInvariants(mu).Delta_scale;
   if(x<bestDelta){bestMu=mu;bestDelta=x;}}
 eng.captureSpectrum();const s=eng.getLatestSpectrum();const H=eng.computeEntropy();
 report.push({name:entry.name,mu_star:bestMu,delta_scale:bestDelta,
   p:Number.isFinite(s.p)?s.p:null,r2:Number.isFinite(s.r2)?s.r2:null,n:s.n,
   entropy:Number.isFinite(H)?H:null});
}
const out={protocol:'XVI_INVARIANTS_JS_SOURCE_PARITY_v001',unmodified_html:true,
  source_sha256:digest,cases:report};
fs.writeFileSync(path.join(root,'output/XVI_INVARIANTS_JS_WITNESS_v001.json'),JSON.stringify(out,null,2)+'\n');
console.log('WROTE output/XVI_INVARIANTS_JS_WITNESS_v001.json');
