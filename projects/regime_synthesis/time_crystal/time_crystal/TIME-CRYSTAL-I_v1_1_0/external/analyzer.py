from __future__ import annotations
import importlib.util, json, hashlib, math
from pathlib import Path
from itertools import combinations
import numpy as np

from .bundle import Bundle, matrix_csv, long_values, status_entry

EXPECTED_SHA = "06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553"

def load_frozen_metric(chamber_root):
    p = Path(chamber_root) / "frozen" / "tc_closure.py"
    data = p.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != EXPECTED_SHA:
        raise RuntimeError(f"Frozen temporal metric hash mismatch: {got}")
    spec = importlib.util.spec_from_file_location("tci110_frozen_closure", p)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module, got

def load_protocol(chamber_root):
    return json.loads((Path(chamber_root)/"protocols"/"external_quantum_dtc.json").read_text(encoding="utf-8"))

def _universality(vals):
    a=np.asarray(vals,dtype=float)
    mean=float(np.mean(a))
    sd=float(np.std(a,ddof=1)) if len(a)>1 else 0.0
    cv=sd/abs(mean) if abs(mean)>1e-15 else float("inf")
    return {"mean":mean,"sd":sd,"CV":cv,"U":float(np.clip(1-cv,0,1))}

def _basin_area(rows,boundary,seed_n=5):
    x=np.asarray([float(r["perturbation"]) for r in rows],dtype=float)
    y=np.asarray([float(r["family_contrast"]) for r in rows],dtype=float)
    order=np.argsort(x);x=x[order];y=y[order]
    mask=x<=boundary+1e-12;x=x[mask];y=y[mask]
    if len(x)<2 or boundary<=x[0]:
        return float("nan")
    xn=(x-x[0])/(boundary-x[0])
    base=float(np.median(y[:min(seed_n,len(y))]))
    if abs(base)<1e-15:
        return float("nan")
    return float(np.trapezoid(y/base,xn))

def analyze_bundle(bundle_path, chamber_root, blind=True):
    bundle=Bundle(bundle_path)
    manifest=bundle.read_json("manifest.json")
    protocol=load_protocol(chamber_root)
    tc,metric_sha=load_frozen_metric(chamber_root)

    candidate_id=str(manifest["candidate_id"])
    domain=str(manifest.get("domain","unknown"))
    label=candidate_id if blind else str(manifest.get("label",candidate_id))
    reasons=[]
    audit={}

    # ---------- Temporal ----------
    temporal_file="temporal/trajectories.csv"
    if bundle.exists(temporal_file):
        _,X,_=matrix_csv(bundle.read_csv(temporal_file))
        ok=np.ones(X.shape[1],dtype=bool)
        spec,_,_=tc.closure_spectrum(X,ok,qmax=int(protocol["temporal"]["qmax"]))
        qdet=tc.detect_fundamental_q(spec)
        fam=tc.family_contrast(spec,qdet["q0"])
        null=tc.shuffle_null(X,ok,qdet["q0"])
        C=float(next(r["closure"] for r in spec if r["q"]==qdet["q0"]))
        F=float(fam["family_contrast"]); p=float(null["empirical_p_ge"])
        passed=(C>=protocol["temporal"]["minimum_closure"]
                and F>=protocol["temporal"]["minimum_family_contrast"]
                and p<=protocol["temporal"]["maximum_shuffle_p"])
        temporal=status_entry(
            "SUPPORTED" if passed else "NOT_SUPPORTED",
            "calculated from temporal/trajectories.csv with the frozen TC_CLOSURE metric",
            metrics={"q0":int(qdet["q0"]),"closure":C,"family_contrast":F,"shuffle_p":p},
            reasons=[] if passed else ["temporal thresholds not all satisfied"]
        )
        temporal["q0"]=int(qdet["q0"])
        temporal["closure"]=C; temporal["family_contrast"]=F; temporal["shuffle_p"]=p
        audit["temporal"]={"file":temporal_file,"present":True,"status":temporal["status"],"metrics":temporal["metrics"]}
    else:
        temporal=status_entry("NOT_TESTED","required trajectory evidence absent",missing=[temporal_file])
        temporal["q0"]=None
        audit["temporal"]={"file":temporal_file,"present":False,"status":"NOT_TESTED"}

    # ---------- Rigidity ----------
    rig_metrics={}
    rig_evidence=False
    rig_pass=False
    rig_reasons=[]
    init_file="rigidity/initial_state_trajectories.csv"
    if bundle.exists(init_file):
        rig_evidence=True
        _,X,names=matrix_csv(bundle.read_csv(init_file))
        pair_F=[]; pair_p=[]; pair_rows=[]
        for i,j in combinations(range(X.shape[1]),2):
            P=X[:,[i,j]]
            ok=np.ones(2,dtype=bool)
            spec,_,_=tc.closure_spectrum(P,ok,qmax=int(protocol["temporal"]["qmax"]))
            qd=tc.detect_fundamental_q(spec)
            fam=tc.family_contrast(spec,qd["q0"])
            null=tc.shuffle_null(P,ok,qd["q0"])
            pair_F.append(float(fam["family_contrast"]))
            pair_p.append(float(null["empirical_p_ge"]))
            pair_rows.append({"pair":f"{names[i]}|{names[j]}","q0":int(qd["q0"]),
                              "family_contrast":pair_F[-1],"shuffle_p":pair_p[-1]})
        uni=_universality(pair_F)
        sig=sum(p<=protocol["rigidity"]["maximum_pair_shuffle_p"] for p in pair_p)
        frac=sig/len(pair_p) if pair_p else 0.0
        pass_init=(len(pair_p)>=protocol["rigidity"]["initial_state_min_pair_count"]
                   and uni["U"]>=protocol["rigidity"]["minimum_universality"]
                   and frac>=protocol["rigidity"]["minimum_significant_pair_fraction"])
        rig_pass |= pass_init
        rig_metrics["initial_state"]={"pair_count":len(pair_p),"significant_pairs":sig,
                                      "significant_fraction":frac,"universality":uni,
                                      "pairs":pair_rows,"pass":pass_init}
        if not pass_init:
            rig_reasons.append("initial-state universality/significance gate not satisfied")

    scan_file="rigidity/perturbation_scan.csv"
    if bundle.exists(scan_file):
        rig_evidence=True
        scan=bundle.read_csv(scan_file)
        basin=tc.plateau_exit_boundary(
            scan,key="family_contrast",
            seed_n=int(protocol["rigidity"]["basin_seed_n"]),
            sigma_mult=float(protocol["rigidity"]["basin_sigma_mult"]),
            consecutive=int(protocol["rigidity"]["basin_consecutive"])
        )
        b=float(basin["boundary_epsilon"]) if basin["boundary_epsilon"] is not None else float("nan")
        area=_basin_area(scan,b,int(protocol["rigidity"]["basin_seed_n"])) if np.isfinite(b) else float("nan")
        pass_basin=bool(np.isfinite(area) and area>=protocol["rigidity"]["minimum_normalized_basin_area"])
        rig_pass |= pass_basin
        rig_metrics["basin"]={"boundary":b if np.isfinite(b) else None,"normalized_area":area if np.isfinite(area) else None,
                              "pass":pass_basin}
        if not pass_basin:
            rig_reasons.append("perturbation-basin gate not satisfied")

    if not rig_evidence:
        rigidity=status_entry("NOT_TESTED","no standardized rigidity evidence supplied",
                              missing=[init_file,scan_file])
    else:
        rigidity=status_entry("SUPPORTED" if rig_pass else "NOT_SUPPORTED",
                              "calculated from standardized rigidity evidence",
                              metrics=rig_metrics,reasons=rig_reasons)

    audit["rigidity"]={"files":{
        init_file:bundle.exists(init_file),scan_file:bundle.exists(scan_file)},
        "status":rigidity["status"],"metrics":rig_metrics}

    # ---------- Collective ----------
    if domain!="quantum_many_body":
        collective=status_entry("N/A","collective quantum-many-body gate not imposed outside quantum_many_body domain")
        audit["collective"]={"status":"N/A","domain":domain}
    else:
        size_file="collective/size_scaling.csv"
        state_file="collective/initial_state_order.csv"
        pert_file="collective/perturbation_profile.csv"
        have_size=bundle.exists(size_file); have_state=bundle.exists(state_file)
        cm={}
        size_pass=False; state_pass=False
        if have_size:
            rows=bundle.read_csv(size_file)
            L=np.asarray([float(r["size"]) for r in rows],dtype=float)
            y=np.asarray([abs(float(r["order"])) for r in rows],dtype=float)
            good=(L>0)&(y>0)
            alpha=float(np.polyfit(np.log(L[good]),np.log(y[good]),1)[0]) if good.sum()>=2 else float("nan")
            size_pass=bool(np.isfinite(alpha) and alpha>protocol["collective"]["minimum_size_exponent"])
            cm["size_scaling"]={"alpha_log_size":alpha if np.isfinite(alpha) else None,"pass":size_pass}
        if have_state:
            vals=np.asarray([abs(float(r["order"])) for r in bundle.read_csv(state_file)],dtype=float)
            mean=float(np.mean(vals)); sd=float(np.std(vals,ddof=1)) if len(vals)>1 else 0.0
            cv=sd/mean if mean>0 else float("inf")
            state_pass=(mean>=protocol["collective"]["minimum_state_mean_abs"]
                        and cv<=protocol["collective"]["maximum_state_CV"])
            cm["initial_state_order"]={"mean_abs":mean,"sd_abs":sd,"CV":cv,"n":len(vals),"pass":state_pass}
        if bundle.exists(pert_file):
            vals=np.asarray([abs(float(r["response"])) for r in bundle.read_csv(pert_file)],dtype=float)
            prob=vals/(vals.sum()+1e-15)
            ipr=float(np.sum(prob*prob))
            cm["perturbation_profile"]={"IPR":ipr,"N_eff":float(1/ipr),
                                        "note":"supporting evidence only; not sufficient by itself"}
        if have_size and have_state:
            if size_pass and state_pass:
                cs="SUPPORTED"
            elif size_pass or state_pass:
                cs="PARTIAL"
            else:
                cs="NOT_SUPPORTED"
            collective=status_entry(cs,"calculated from finite-size order and broad initial-state order",
                                    metrics=cm,reasons=[] if cs=="SUPPORTED" else ["collective default gates not all satisfied"])
        elif have_size or have_state or bundle.exists(pert_file):
            collective=status_entry("PARTIAL","some collective evidence present but required evidence pair is incomplete",
                                    metrics=cm,missing=[f for f,present in [(size_file,have_size),(state_file,have_state)] if not present])
        else:
            collective=status_entry("NOT_TESTED","required collective evidence absent",missing=[size_file,state_file])
        audit["collective"]={"files":{size_file:have_size,state_file:have_state,pert_file:bundle.exists(pert_file)},
                             "status":collective["status"],"metrics":cm}

    # ---------- Spectral / typicality ----------
    if domain!="quantum_many_body":
        spectral=status_entry("N/A","Hilbert-space typicality is not assigned to an ordinary classical/generic domain")
        audit["spectral"]={"status":"N/A","domain":domain}
    else:
        spec_file="spectral/typicality.csv"
        if bundle.exists(spec_file):
            groups=long_values(bundle.read_csv(spec_file),"K","value")
            ks=sorted(groups)
            k0,k1=ks[0],ks[-1]
            init=float(np.mean(np.abs(groups[k0]))); final=float(np.mean(np.abs(groups[k1])))
            retention=final/init if init>0 else float("nan")
            passed=(final>=protocol["spectral"]["minimum_final_typicality_mean_abs"]
                    and retention>=protocol["spectral"]["minimum_typicality_retention"])
            spectral=status_entry("SUPPORTED" if passed else "NOT_SUPPORTED",
                                  "calculated from spectral/typicality.csv",
                                  metrics={"K_min":k0,"K_max":k1,"initial_mean_abs":init,
                                           "final_mean_abs":final,"retention":retention},
                                  reasons=[] if passed else ["spectral typicality thresholds not all satisfied"])
            audit["spectral"]={"file":spec_file,"present":True,"status":spectral["status"],
                               "metrics":spectral["metrics"]}
        else:
            spectral=status_entry("NOT_TESTED","required typicality evidence absent",missing=[spec_file])
            audit["spectral"]={"file":spec_file,"present":False,"status":"NOT_TESTED"}

    record={
        "id":candidate_id,
        "label":label,
        "domain":domain,
        "expected_physics_class":None if blind else manifest.get("expected_physics_class"),
        "sectors":{
            "temporal":temporal,
            "rigidity":rigidity,
            "collective":collective,
            "spectral":spectral
        },
        "provenance":[f"External bundle SHA256 {bundle.evidence_hash()}",
                      "TIME-CRYSTAL-I external_quantum_dtc protocol v1.1.0",
                      f"Frozen TC_CLOSURE metric {metric_sha}"]
    }

    return {
        "manifest":{"candidate_id":candidate_id,"domain":domain,
                    "protocol":manifest.get("protocol","quantum_dtc_v1_1_0"),
                    "blind_label_suppressed":bool(blind)},
        "record":record,
        "audit":audit,
        "evidence_sha256":bundle.evidence_hash(),
        "metric_sha256":metric_sha,
        "protocol":protocol
    }
