import json,hashlib,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rn_lang as G
H=os.path.dirname(os.path.abspath(__file__));D=H+"/../data"
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
cfg=dict(rules=G.grammar(),starts=[1,2,3,4,5,6,7,8,9,10,12,16,24,36],horizon_T=400,escape_ESC=10**18,
 mr_bound=3317044064679887385961981,
 undefined_rank_policy="stuck; no substitution",
 certification_policy="orbit flagged certified only if every factorization used has every prime factor deterministically certified (n<3.317e24) ; otherwise flagged uncertified and reported separately",
 preregistered_checks=["P-A: for each rule in PROVED_LAWS the engine orbit equals the closed-form orbit exactly (starts 1..2000 and the 14 starts)",
   "P-B: every orbit ends cyclic/stuck/escape/horizon; counts reported; no success criterion is defined (this is a classification study)",
   "P-C: distinct primes visited per orbit are counted; no orbit-level claim of 'infinitely many primes' is made from a finite run",
   "P-D: Tier-A theorems verified against definition-level neighbour engine for x<=20000"],
 amendments=[])
json.dump(cfg,open(D+"/rn_config.json","w"),indent=1,sort_keys=True)
reg=dict(config_sha256=sha(D+"/rn_config.json"),**{f+"_sha256":sha(H+"/"+f+".py") for f in("rn_core","rn_lang","rn_closed","rn_naive","rn_analyse")},n_rules=len(cfg["rules"]),n_starts=len(cfg["starts"]))
json.dump(reg,open(D+"/rn_registration.json","w"),indent=1,sort_keys=True);print(reg)
