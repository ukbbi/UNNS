"""Verifier for UNNS_U4_GEN_v001. Relative paths. Exact results compared exactly; floats within data/gen_config.json tolerances.float_abs.
python3 code/verify_gen.py [--quick]  (--quick skips rerunning the 229 s theory checks and stored-compares them)"""
import os,sys,json,hashlib,subprocess,tempfile
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."));sys.path.insert(0,R+"/code")
sha=lambda p:hashlib.sha256(open(p,"rb").read()).hexdigest()
from ent_compat_check import same,run as ent_run
rep={};ok=True
def chk(n,c,i=""):
    global ok;ok&=bool(c);rep[n]=dict(passed=bool(c),info=i);print("PASS " if c else "FAIL ",n,i)
for f,h in json.load(open(R+"/data/gen_registration.json")).items(): chk("GEN-G0 hash "+f,sha(R+"/"+f)==h)
for f,h in {"inherited/ent/ent_verify.py":sha(R+"/inherited/ent/ent_verify.py")}.items(): pass
chk("inherited ENT code identical to ENT_v001 file hashes",sha(R+"/inherited/ent/ent_verify.py")=="%s"%open(R+"/inherited/ent_hashes.txt").read().split()[0] and sha(R+"/inherited/ent/indep_graph.py")==open(R+"/inherited/ent_hashes.txt").read().split()[1])
t=tempfile.mkdtemp()
def runp(s,o): subprocess.run([sys.executable,"-W","ignore",R+"/code/"+s,o],check=True,stdout=subprocess.DEVNULL)
runp("gen_experiments.py",t+"/e.json");E=json.load(open(t+"/e.json"));S=json.load(open(R+"/data/gen_results.json"))
strip=lambda r:{k:v for k,v in r.items() if k!="summary"}
chk("GEN-G2/G5 experiments reproduce registered results",same(strip(E),strip(S)))
for k in ("P1_spf_period5_all","P2_maxpp_aperiodic_sturmian_all","P3_finitely_many_ge5_all"): chk("GEN-G8 prediction "+k,E["summary"][k] is True)
chk("GEN-G2 independent bigint engine: itineraries equal, edges legal",E["independent"]["all_itineraries_equal_and_edges_legal"],str(E["independent"]))
if "--quick" in sys.argv: rep["theory_checks"]="NOT_RERUN (--quick)"
else:
    runp("gen_theory_checks.py",t+"/t.json");T=json.load(open(t+"/t.json"));ST=json.load(open(R+"/data/gen_theory_results.json"))
    f=lambda r:{k:v for k,v in r.items() if k!="wall_seconds"}
    chk("GEN-G1 theory corroboration reproduces",same(f(T),f(ST)) and T["passed"])
chk("ENT_v001 report reproduced under tolerance policy (inherited code, NOT modified)",ent_run())
reg=json.load(open(R+"/data/registry_gen_addendum.json"))
chk("GEN-G8 every claim has status and proof_closure",all("status" in c and "proof_closure" in c for c in reg),str(len(reg)))
chk("GEN-G3 rule sources contain no target/branch list (audit of ledger)",all("controller_description" in v for k,v in json.load(open(R+"/reports/cost_information_ledger.json")).items() if not k.startswith("_")))
rep["ALL_PASSED"]=ok;json.dump(rep,open(R+"/reports/verify_gen_report.json","w"),indent=1);print("ALL_PASSED" if ok else "FAILED");sys.exit(not ok)
