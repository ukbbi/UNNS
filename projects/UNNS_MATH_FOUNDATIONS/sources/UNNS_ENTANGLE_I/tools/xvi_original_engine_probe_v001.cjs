'use strict';
// Executes the original, byte-frozen TauFieldEngineN.projectFlux method.
// Requires Node.js; Python test suite does NOT require Node.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');
const root = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(root,'docs','sources','XVI_ENGINE_v084.html'),'utf8');
const lock = JSON.parse(fs.readFileSync(path.join(root,'config','XVI_BRIDGE_LOCK_v001.json'),'utf8'));
const hash = crypto.createHash('sha256').update(Buffer.from(src,'utf8')).digest('hex');
if(hash!==lock.inputs.engine.sha256) throw Error('SOURCE HASH MISMATCH');
const begin = src.indexOf('class TauFieldEngineN {');
const end = src.indexOf('</script>',begin);
if(begin<0||end<0) throw Error('Original engine class not found');
const context={console:{log:()=>{}},module:{exports:{}},Float64Array,Math};
vm.runInNewContext(src.slice(begin,end),context);
const Engine=context.module.exports;
if(typeof Engine!=='function') throw Error('Engine export not available');
function rms(a){let sum=0;for(const x of a) sum+=x*x;return Math.sqrt(sum/a.length);}
function dot(a,b){let sum=0;for(let i=0;i<a.length;i++)sum+=a[i]*b[i];return sum/a.length;}
function divN(J,N){const d = new Float64Array(J.length);for(let y=0;y<N;y++)for(let x=0;x<N;x++){
 let i=x+y*N;d[i]=(J[(x+1)%N+y*N]-J[(x+N-1)%N+y*N])*Math.PI/N;
}return d;}
const results=[];
for(const N of [64,128,256]) {
 const eng=new Engine({grid_width:N,operator_mode:'XVI',init_mode:'zero',alpha_c:0.03,seed:41});
 for(let y=0;y<N;y++)for(let x=0;x<N;x++)eng.closure.Jx[x+y*N]=Math.sin(2*Math.PI*x/N);
 const before=Float64Array.from(eng.closure.Jx), preDiv=rms(divN(before,N));
 eng.projectFlux();
 const after=Float64Array.from(eng.closure.Jx), correction=Float64Array.from(eng.closure.gradPsiX);
 const predicted=1-Math.sin(2*Math.PI/N);
 const actual=rms(after)/rms(before);
 const divRatio=rms(divN(after,N))/preDiv;
 const cross=dot(after,correction)/dot(before,before);
 const eDef=(dot(before,before)-dot(after,after)-dot(correction,correction))/dot(before,before);
 if(Math.abs(actual-predicted)>1e-8||Math.abs(divRatio-predicted)>1e-8) throw Error('ENGINE/FORMULA MISMATCH '+N);
 eng.projectFlux();
 results.push({N,mode:1,source_engine_version:eng.version,
     predicted_divergence_residual:predicted,actual_field_residual:actual,
     actual_divergence_residual:divRatio, normalized_orthogonality_cross:cross,
     normalized_energy_decomposition_defect:eDef,
     second_projection_ratio:rms(eng.closure.Jx)/rms(before)});
}
process.stdout.write(JSON.stringify({protocol:'XVI_ORIGINAL_ENGINE_PROBE_v001',sha256:hash,source_unmodified:true,results},null,2)+'\n');
