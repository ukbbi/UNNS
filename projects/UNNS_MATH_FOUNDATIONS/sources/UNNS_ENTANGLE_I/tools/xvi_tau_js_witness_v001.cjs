'use strict';
// Optional source-JS witness, NOT required for the Python/NumPy research runs.
// Usage from project root: node tools/xvi_tau_js_witness_v001.cjs
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'docs/sources/XVI_ENGINE_v084.html'),'utf8');
const lock=JSON.parse(fs.readFileSync(path.join(root,'config/XVI_TAU_LOCK_v001.json'),'utf8'));
const hash=crypto.createHash('sha256').update(source).digest('hex');
if(hash!==lock.inputs.canonical_engine.sha256)throw new Error('Source lock mismatch');
const a=source.indexOf('class TauFieldEngineN {');
const b=source.indexOf('</script>',a);
if(a<0||b<0)throw new Error('Missing class');
const ctx={console:{log:()=>{}},module:{exports:{}},Math,Float64Array,performance:{now:()=>0}};
vm.runInNewContext(source.slice(a,b),ctx);
const Engine=ctx.module.exports;
const fixture=JSON.parse(fs.readFileSync(path.join(root,'output/XVI_TAU_JS_INPUT_v001.json'),'utf8'));
function rmsErr(a,b){let num=0,den=0;for(let i=0;i<a.length;i++){let e=a[i]-b[i];num+=e*e;den+=b[i]*b[i];}return Math.sqrt(num/(den+1e-40));}
const results=[];
for(const c of fixture.cases){
 const eng=new Engine({grid_width:c.N,operator_mode:'XVI',init_mode:'zero',lambda:c.params.lam,
   beta:c.params.beta,alpha_c:c.params.alpha_c,gamma_closure:c.params.gamma,
   closure_interval:c.params.interval,laplacian_mode:'fft',seed:c.seed});
 eng.sigma=0;eng.anneal_sigma=0; // mandatory: HTML config.sigma || 0.02 cannot set 0 through constructor
 eng.fields[0].tau.set(c.initial_tau);
 for(let s=0;s<c.params.steps;s++)eng.step();
 const rel=rmsErr(eng.fields[0].tau,c.python_final_tau);
 results.push({N:c.N,seed:c.seed,steps:c.params.steps,relative_final_tau_error:rel,
  source_JS_version:eng.version,pass:rel<1e-10});
}
const verdict={protocol:'XVI_TAU_JS_WITNESS_v001',source_sha256:hash,
                original_engine_unmodified:true,results,all_pass:results.every(x=>x.pass),
                note:'Pass checks controlled deterministic zero-noise full nonlinear source vs Python translation; not representative of noisy original UI runs.'};
const dest=path.join(root,'output/XVI_TAU_JS_WITNESS_v001.json');
fs.writeFileSync(dest,JSON.stringify(verdict,null,2)+'\n');
console.log('WROTE output/XVI_TAU_JS_WITNESS_v001.json',verdict.all_pass?'PASS':'FAIL');
if(!verdict.all_pass)process.exitCode=1;
