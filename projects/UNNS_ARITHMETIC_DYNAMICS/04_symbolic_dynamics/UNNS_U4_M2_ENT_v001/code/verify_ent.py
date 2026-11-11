"""Verifier for UNNS_U4_M2_ENT_v001 (relative paths). python3 code/verify_ent.py"""
import os,sys,json,hashlib,subprocess,tempfile
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
sha=lambda p:hashlib.sha256(open(p,"rb").read()).hexdigest()
rep={};ok=True
def chk(n,c,i=""):
    global ok;ok&=bool(c);rep[n]=dict(passed=bool(c),info=i);print("PASS " if c else "FAIL ",n,i)
reg=json.load(open(R+"/data/ent_registration.json"))
for f,h in reg.items(): chk("hash "+f,sha(R+"/"+f)==h)
t=tempfile.mkdtemp()+"/r.json";subprocess.run([sys.executable,"-W","ignore",R+"/code/ent_verify.py",t],check=True,stdout=subprocess.DEVNULL)
A=json.load(open(t));S=json.load(open(R+"/reports/ent_raw.json"))
chk("E1 rerun passed",A["passed"]);chk("E1 reproduces stored report",A==S)
chk("inherited STAGE2 zip hash recorded (NOT_RERUN)",open(R+"/inherited/STAGE2_zip_sha256.txt").read().startswith("1b68eb08bcc8c99f708ab2c986d43c6d0f0fdad3cb9e453cd51d9022aeb2eada"))
rep["ALL_PASSED"]=ok;json.dump(rep,open(R+"/reports/verify_ent_report.json","w"),indent=1);print("ALL_PASSED" if ok else "FAILED");sys.exit(not ok)
