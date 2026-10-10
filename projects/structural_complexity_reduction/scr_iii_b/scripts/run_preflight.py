from pathlib import Path
import hashlib,json,sys,unittest,time
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'models'))
from physical_energy import enumerate_patch
A=BASE/'output/acquisition';V=BASE/'output/validation';A.mkdir(parents=True,exist_ok=True);V.mkdir(parents=True,exist_ok=True)
sources=['references/square_ice_model/Dryad_README.md','references/public_code/hotspice_reference.txt','references/public_code/Hotspice-main.zip','references/public_code/MMC_Code.zip','references/public_code/SPMMC_Code.zip','data/raw/mean_200nm_300K_50x50_verteximage.npz']
manifest=[]
for s in sources:
 p=BASE/s
 manifest.append({'path':s,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
(A/'ACQUISITION_MANIFEST_v001.json').write_text(json.dumps({'sources':manifest,'dryad_doi':'10.5061/dryad.cz8w9gjk0','zenodo_doi':'10.5281/zenodo.15548088','hotspice_url':'https://github.com/mumax/Hotspice','notes':'Original source archives preserved; Dryad code v1.00 templates, not publication-specific v1.01'},indent=2)+'\n')
checks=[]
for L in (1,2):
 start=time.perf_counter();r=enumerate_patch(L);r['elapsed_seconds']=time.perf_counter()-start;checks.append(r)
(V/'SIZE_BENCHMARK_v001.json').write_text(json.dumps({'exhaustive':checks,'proposed_3x3':{'spins':24,'states':2**24,'status':'not_executed_cost_not_benchmarked'}},indent=2)+'\n')
loader=unittest.defaultTestLoader.discover(str(BASE/'tests'),pattern='test_energy.py');result=unittest.TextTestRunner(verbosity=2).run(loader)
report={'verdict':'PREFLIGHT_PARTIAL','tests_run':result.testsRun,'tests_failures':len(result.failures),'tests_errors':len(result.errors),'source_to_independent_numerical_comparison':'NOT_RUN','independent_exact_target_checks':'NOT_RUN','objective':'Verify geometry and normalized dumbbell coupling algebra, source acquisition and small-patch enumeration','caveats':['Interaction coefficients reproduce a formula independently but have not been compared with reference C++ numerical output','Normalized interaction energy uses a chosen sign consistent with field flip identities; physical normalization and absolute energy not established','3x3 exact performance unmeasured','No energy window or primary protocol frozen']}
(V/'ENERGY_CHECK_v001.json').write_text(json.dumps(report,indent=2)+'\n')
(V/'PREFLIGHT_RESULT_v001.md').write_text('# SCR-III-B Hamiltonian feasibility preflight v001\n\n**Verdict: PREFLIGHT_PARTIAL**\n\nSmall-patch enumeration and internal algebra checks were run. No numerical C++ reference cross-check, full physical energy normalization, exact solver comparison, or 3x3 benchmark yet. Do not freeze SCR-III-B SPEC.\n\n'+json.dumps(checks,indent=2)+'\n')
print(json.dumps({'verdict':report['verdict'],'tests':result.testsRun,'failures':len(result.failures),'sizes':checks},indent=2))
if not result.wasSuccessful():sys.exit(1)
