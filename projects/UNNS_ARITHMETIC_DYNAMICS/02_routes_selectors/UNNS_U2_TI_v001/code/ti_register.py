"""Pre-registration: writes data/ti_config.json and data/registration.json (SHA-256 of config, language and recognizer sources) BEFORE any registered run."""
import json,hashlib,os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import ti_lang as G
cfg=dict(version="U2-TI v001",
  grammar=G.GRAMMAR, rules_F=G.rules_F(), rules_M=G.rules_M(),
  starts=[1,2,3,4,5,6,7,8,9,10,12,16,24,36], horizon_T=400, escape_ESC=10**18,
  recognizers=dict(sequences=["V (vertex sequence; pre-periodic part if cyclic)","R (record sequence: successive strict maxima)"],
     linear_recurrence="Berlekamp-Massey over Q, order<=4, n>=4r+6, verified on every term; min length V:22, R:10; analysis window = first 60 terms of each sequence (amendment A1)",
     families=["naturals","squares","cubes","triangular","powers_of_2","powers_of_3","fibonacci","factorials","primes"],
     family_tests="subset: >=8 distinct terms all in family; consecutive: 8 successive terms are consecutive members in increasing order"),
  amendments=['A1: recognizer analysis window limited to first 60 terms (performance of Berlekamp-Massey on large integers); made after a timing test of a single rule and before any complete run; the only orbit endpoints inspected were those of one rule during that test'],
  success_criterion="orbit status in {escape,horizon} AND (linrec_V or linrec_R present OR family consecutive hit on V or R). 'Fibonacci-like': family fibonacci consecutive on V or R, or linear recurrence a_n=a_{n-1}+a_{n-2}.",
  target_blindness=dict(
    TB1="a selector is a rule tuple of the predeclared grammar; one interpreter; no per-sequence code",
    TB2="reads only X, H (window<=2), NB(X); class M additionally the visited set (unbounded memory; reference class, not finite control)",
    TB3="no step counter, target, index or external table; horizon and escape bound act outside the selector; recognizers have no feedback",
    TB4="the registered rule set, starts and horizon are the same for every sequence family and were fixed before the registered run; rules added after seeing results are labelled exploratory",
    TB5="audit: channel-read log, locality re-execution from (x,H) alone, brute-force cross-check of NB for small x"))
os.makedirs(HERE+"/../data",exist_ok=True)
txt=json.dumps(cfg,indent=1,sort_keys=True)
open(HERE+"/../data/ti_config.json","w").write(txt)
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
reg=dict(config_sha256=sha(HERE+"/../data/ti_config.json"),ti_lang_sha256=sha(HERE+"/ti_lang.py"),ti_recog_sha256=sha(HERE+"/ti_recog.py"),n_rules_F=len(cfg["rules_F"]),n_rules_M=len(cfg["rules_M"]),n_starts=len(cfg["starts"]))
json.dump(reg,open(HERE+"/../data/registration.json","w"),indent=1)
print(reg)
