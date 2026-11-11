import json,os,csv
H=os.path.dirname(os.path.abspath(__file__));D=H+"/../data"
reg=json.load(open(D+"/registry_spec_v001.json"))
PC_OK="Proof written (docs/PROOFS.md); verifier-corroborated; external review pending"
PC_NO="Not closed: proof obligation remains; no proof written in this release"
upd={"U4.3-T2":("Proved (author-level)",PC_OK),"U4.3-T3":("Proved (author-level), memory-one only",PC_OK),
"U4.3-T4":("Proved (author-level), radius one, k>=3",PC_OK),"U4.2-T4":("Proved (author-level), loop hypothesis required",PC_OK)}
for c in reg:
    c["version_added"]=c.get("version_added","SPEC_v001")
    c["proof_closure"]=PC_NO if c["status"].startswith("Sketch") else ("n/a (definition, import, standard or open)" if c["status"] not in [] else "")
    if c["id"] in upd:
        c["status_spec_v001"]=c["status"];c["status"],c["proof_closure"]=upd[c["id"]]
        c["falsification_gate"]=c.get("falsification_gate","")+" [S2: see PROOFS.md falsification condition]"
    if c["id"]=="U4.3-X1":
        c["status_spec_v001"]=c["status"];c["status"]="Assembled; rests on proved T2,T3,T4 (author-level) and standard T5";c["proof_closure"]="Follows from closed items; external review pending"
    if c["id"] in ("U4.1-T2","U4.1-T4","U4.1-T5","U4.4-T1","U4.4-T2","U4.5-S2d"):
        c["proof_closure"]=PC_NO+" (bounded verifier passes, where any, do not upgrade the status)"
    if c["id"] in ("U4.6-TU","U4.6-TO","U4.6-TB"):
        c["proof_closure"]="Assembled statements; components U4.1-T2,T4,T5 (TU), U4.5-S2d (TO) remain unclosed"
def N(i,title,kind,status,st,hyp,fals,notdo,proof,deps=()):
    reg.append(dict(id=i,stage="S2",title=title,kind=kind,statement=st,hypotheses=hyp,origin="NEW_ELEMENTARY",status=status,info_class="structural",deps=list(deps),falsification_gate=fals,proof_note=notdo,probe="reports/",proof_closure=proof,version_added="STAGE2_v001"))
N("U4.3-L1","Lemma M1-P2: nonempty memory-1 metric shift has a point of period <=2","Lemma","Proved (author-level)","Symmetry of the pair rule gives (ab)^Z or a^Z.","memory 1, metric-only","nonempty memory-1 rule with no period<=2 point","memory 1 only",PC_OK)
N("U4.3-X2","Degree-augmented rule realises golden mean on {p,4p}","Proposition","Proved by exhibition; exact check","Repeat allowed iff deg=2; other transitions need d=1.","p prime","failure of the exhibited matrix","shows T2 is a metric-only statement",PC_OK,["U4.3-T2"])
N("U4-M2","Memory-two non-backtracking shift Y_NB","Theorem","Proved (author-level), items 1-6","Equivalence with non-backtracking walks; no periods 1,2,3; periods 4,5 present and infinitely many orbits; vertex 1 is a dead end; not conjugate to a memory-1 metric shift; non-real window spectra.","triangle-freeness, N(1)={4}, injective scaling homomorphism (frozen U3/U3-COR)","points of period 1,2,3 or containing 1; failed period-4/5 distances","entropy of infinite Y_NB open; not a generator; no universality",PC_OK,["U4.3-L1","U4.3-T3"])
N("U4-M2-E","Topological entropy of Y_NB (infinite alphabet)","Conjecture","Open","Hashimoto window lower bounds 2.81/3.69/5.21 on hubs 12/60/360 are observations only.","","","",
  "Open")
N("U4.2C-O1","Memory-two survey (registered observation)","Observation","Registered observation","94,352 memory-2 rules over 10 windows: 68,364 non-real, 6,422 nonempty with no period<=2 point, 0 fixed-point violations, 42,615 signatures; golden mean and directed 3-cycle with loops not found.","survey windows only","","'not found' is not 'impossible'","n/a (observation)")
N("U4.2D-O1","Selector experiment (registered observation)","Observation","Registered observation","Deterministic target-independent selectors; state-only vs one-previous-state NB memory; 432 runs, all neighbourhoods certified.","18 starts, horizon 400, escape 1e18","","finite prime visits are observations; selectors are not generators","n/a (observation)")
json.dump(reg,open(D+"/registry_stage2.json","w"),indent=1)
cols=["id","stage","kind","status","proof_closure","origin","title"]
w=csv.writer(open(D+"/registry_stage2.csv","w",newline=""));w.writerow(cols)
[w.writerow([c.get(k,"") for k in cols]) for c in reg]
print(len(reg))
