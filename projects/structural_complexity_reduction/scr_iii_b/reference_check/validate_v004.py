#!/usr/bin/env python3
"""Additive SCR-III-B v004: verbatim original-source pair function probe."""
import hashlib, json, math, pathlib, subprocess, sys
HERE=pathlib.Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
sys.path.insert(0,str(PROJECT/'scr_iii_b'/'models'))
from physical_energy import pair_coupling, energy, ice_ok
sys.path.insert(0,str(PROJECT/'scr_iii_b'/'reference_check'))
from validate_v002 import geometry, vertices
DEST=PROJECT/'scr_iii_b'/'output'/'validation'/'v004'
DEST.mkdir(parents=True,exist_ok=True)
BIN=DEST/'original_source_probe.bin'
REPORT=DEST/'REFERENCE_RUN_v004.json'

def run():
 rec={'version':'v004','source_kind':'verbatim functions extracted from original Dryad SPMMC v1.00','full_original_simulator_executed':False,'physical_reference_status':'PARTIAL','verdict':'PARTIAL','cases':[],'tolerance':1e-12}
 try:
  p=subprocess.run(['g++','-std=c++17','-O2',str(HERE/'source_probe_v004.cpp'),'-o',str(BIN)],capture_output=True,text=True)
  if p.returncode: raise RuntimeError('compile: '+p.stderr[-3000:])
  for L in (1,2,3):
   p=subprocess.run([str(BIN),str(L)],capture_output=True,text=True,check=True)
   es=geometry(L)
   pairs=[(int(i),int(j),float(k)) for i,j,k in (line.split() for line in p.stdout.splitlines())]
   maxerr=max(abs(pair_coupling(es[i],es[j])-k) for i,j,k in pairs)
   r={'L':L,'spins':len(es),'pairs':len(pairs),'max_python_vs_verbatim_cpp_coupling_error':maxerr}
   if L<=2:
    vs=vertices(L); best=float('inf'); ground=[]; icecount=0; minice=float('inf'); minbad=float('inf')
    for b in range(1<<len(es)):
     s=[1 if (b>>i)&1 else -1 for i in range(len(es))]
     e=energy(s,pairs); ok=ice_ok(s,vs); icecount+=ok
     if ok:minice=min(minice,e)
     else:minbad=min(minbad,e)
     if e<best-1e-13:best=e; ground=[s]
     elif abs(e-best)<=1e-13:ground.append(s)
    r.update(states=1<<len(es),ice_states=icecount,ground_count=len(ground),ground_all_ice=all(ice_ok(s,vs) for s in ground),ground_energy_normalized=best,min_ice_energy_normalized=minice,min_nonice_energy_normalized=minbad)
   rec['cases'].append(r)
  if all(x['max_python_vs_verbatim_cpp_coupling_error']<rec['tolerance'] for x in rec['cases']):rec['verdict']='ORIGINAL_SOURCE_PAIR_FUNCTION_PASS_PHYSICAL_REFERENCE_PARTIAL'
  else:rec['verdict']='FAIL'
 except Exception as exc:rec['verdict']='FAIL';rec['error']=repr(exc)
 REPORT.write_text(json.dumps(rec,indent=2)+'\n')
 (DEST/'REFERENCE_RUN_v004.md').write_text('# Original-source pair preflight v004\n\nVerdict: `'+rec['verdict']+'`\n\nThis is original-source **function** agreement, not a full Dryad engine / physical energy reference lock. The finite-patch total energy and sign remain modeled separately; MMC vs SPMMC geometry and finite-boundary validation, source field/ΔE sign, physical scaling and temperature, published v1.01 parameters, and physical target preservation remain pending.\n\n```json\n'+json.dumps(rec,indent=2)+'\n```\n')
 print(json.dumps(rec,indent=2));return 0 if rec['verdict'].startswith('ORIGINAL_SOURCE_PAIR_FUNCTION_PASS') else 1
if __name__=='__main__':sys.exit(run())
