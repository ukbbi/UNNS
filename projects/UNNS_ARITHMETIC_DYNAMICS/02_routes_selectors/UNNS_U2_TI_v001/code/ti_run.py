"""Registered run of U2-TI: all registered rules x starts.  usage: ti_run.py OUT.json"""
import sys,os,json,time,hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import ti_lang as G, ti_recog as R
cfg=json.load(open(HERE+"/../data/ti_config.json")); reg=json.load(open(HERE+"/../data/registration.json"))
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
assert reg["config_sha256"]==sha(HERE+"/../data/ti_config.json") and reg["ti_lang_sha256"]==sha(HERE+"/ti_lang.py") and reg["ti_recog_sha256"]==sha(HERE+"/ti_recog.py"),"registered files changed"
out=[]; t0=time.time()
for cls,rules in (("F",cfg["rules_F"]),("M",cfg["rules_M"])):
    for ri,rule in enumerate(rules):
        for x0 in cfg["starts"]:
            res=G.run(rule,x0,cfg["horizon_T"],cfg["escape_ESC"]); a=R.analyse(res)
            out.append(dict(cls=cls,rule_index=ri,rule=rule,start=x0,analysis=a,prefix=res["seq"][:60],moves=len(res["moves"]),cand=res["cand"],channels=res["channels"]))
        print(cls,ri,round(time.time()-t0),flush=True)
json.dump(out,open(sys.argv[1],"w"),default=str)
print("done",len(out),round(time.time()-t0))
