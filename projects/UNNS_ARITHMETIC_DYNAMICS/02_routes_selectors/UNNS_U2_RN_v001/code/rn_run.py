import json,os,sys,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H);D=H+"/../data"
import hashlib
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
reg=json.load(open(D+"/rn_registration.json"))
for f in("rn_core","rn_lang","rn_closed","rn_naive","rn_analyse"): assert reg[f+"_sha256"]==sha(H+"/"+f+".py"),f
assert reg["config_sha256"]==sha(D+"/rn_config.json")
import rn_lang as G,rn_analyse as A
cfg=json.load(open(D+"/rn_config.json"));res=[];t=time.time()
for ri,rule in enumerate(cfg["rules"]):
    for x0 in cfg["starts"]:
        o=G.run(rule,x0,cfg["horizon_T"],cfg["escape_ESC"]);a=A.analyse(o,cfg["escape_ESC"])
        res.append(dict(rule_index=ri,rule=rule,start=x0,analysis=a,prefix=o["seq"][:40],labels=o["labels"][:12],cost=o["cost"],steps=len(o["labels"])))
json.dump(res,open(D+"/rn_results.json","w"),default=str)
print(len(res),round(time.time()-t,1))
