"""Re-runs the inherited ENT_v001 verifier code (copied unchanged to inherited/ent/, hash-checked) and compares its report to the stored one
with the tolerance policy: exact for ints/strings/lists/bools, float_abs for floats. (Addresses the strict-float-comparison reproducibility issue; ENT_v001 itself is unchanged.)"""
import os,sys,json,subprocess,tempfile
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
TOL=json.load(open(R+"/data/gen_config.json"))["tolerances"]["float_abs"]
def same(a,b,path=""):
    if isinstance(a,dict) and isinstance(b,dict):
        return a.keys()==b.keys() and all(same(a[k],b[k],path+"/"+k) for k in a)
    if isinstance(a,list) and isinstance(b,list):
        return len(a)==len(b) and all(same(x,y,path) for x,y in zip(a,b))
    if isinstance(a,float) or isinstance(b,float):
        try: return abs(float(a)-float(b))<=TOL*max(1.0,abs(float(b)))
        except Exception: return False
    return a==b
def run():
    t=tempfile.mkdtemp()+"/r.json"
    subprocess.run([sys.executable,"-W","ignore",R+"/inherited/ent/ent_verify.py",t],check=True,stdout=subprocess.DEVNULL)
    return same(json.load(open(t)),json.load(open(R+"/inherited/ent/ent_raw.json")))
if __name__=="__main__": print(run())
