"""Verifier for UNNS_U4_STAGE2_v001. Relative paths only. Usage: python3 code/verify_stage2.py [--quick]
--quick skips re-running the 340 s memory-two survey and compares stored results only."""
import os,sys,json,hashlib,subprocess,tempfile,time
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
ok=True;rep={}
def chk(n,c,info=""):
    global ok;ok&=bool(c);rep[n]=dict(passed=bool(c),info=info);print(("PASS " if c else "FAIL "),n,info)
reg=json.load(open(R+"/data/stage2_registration.json"))
for rel,h in reg.items():
    p=R+"/"+(rel if "/" in rel else ("code/"+rel if rel!="stage2_config.json" else "data/"+rel))
    chk("S2-G7 hash "+rel,sha(p)==h)
tmp=tempfile.mkdtemp()
def run(script,out):
    t=time.time();subprocess.run([sys.executable,"-W","ignore",R+"/code/"+script,out],check=True,stdout=subprocess.DEVNULL);return time.time()-t
a=tmp+"/a.json";run("stage2a_checks.py",a);A=json.load(open(a));S=json.load(open(R+"/reports/stage2a_raw.json"))
for k in ("U4.3-T2","U4.3-T3","U4.3-T4","U4.2-T4"): chk("S2-G1 "+k+" rerun passed",A[k]["passed"] and A[k]["passed"]==S[k]["passed"])
m=tmp+"/m.json";run("m2_checks.py",m);M=json.load(open(m));S2=json.load(open(R+"/reports/m2_raw.json"))
for k,v in M.items(): chk("S2-G2/G5 "+k,v["passed"])
s=tmp+"/s.json";run("selector_exp.py",s);X=json.load(open(s));S3=json.load(open(R+"/data/selector_results.json"))
key=lambda r:(r["key"],r["rank"],r["memory"],r["start"])
strip=lambda rows:{key(r):{k:v for k,v in r.items() if k not in("requests",)} for r in rows}
chk("S2-G4 selector rows reproduce registered results",strip(X["rows"])==strip(S3["rows"]))
chk("S2-G5 all neighbourhoods certified",X["all_neighbourhoods_certified"] and S3["all_neighbourhoods_certified"])
if "--quick" not in sys.argv:
    v=tmp+"/v.json";run("m2_survey.py",v);V=json.load(open(v));S4=json.load(open(R+"/data/m2_survey_results.json"))
    chk("S2-G3 survey reproduces registered aggregate",V["aggregate"]==S4["aggregate"] and V["targets_seen"]==S4["targets_seen"])
else:
    S4=json.load(open(R+"/data/m2_survey_results.json"));rep["survey"]="NOT_RERUN (--quick); stored aggregate sha256 "+hashlib.sha256(json.dumps(S4["aggregate"],sort_keys=True).encode()).hexdigest()
chk("S2-G3 no fixed-point violations in survey",all(S4["aggregate"][k]["fixed_point_violations"]==0 for k in S4["aggregate"]))
reg2=json.load(open(R+"/data/registry_stage2.json"))
chk("S2-G6 every claim has proof_closure",all("proof_closure" in c for c in reg2),str(len(reg2))+" claims")
chk("S2-G6 no Sketch upgraded without proof",all(c["proof_closure"].startswith("Not closed") for c in reg2 if c["status"].startswith("Sketch")))
rep["ALL_PASSED"]=ok;print("ALL_PASSED" if ok else "FAILED")
json.dump(rep,open(R+"/reports/verify_stage2_report.json","w"),indent=1)
sys.exit(0 if ok else 1)
