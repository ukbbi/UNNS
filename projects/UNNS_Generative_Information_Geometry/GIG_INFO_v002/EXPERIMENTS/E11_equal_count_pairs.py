"""E11 -- equal history count, different second homology: the census search and the information-recovery profile.
Y(X)=1 iff beta_2>0.  Observables (each a function of the system):  O0=N;  OE=(N,f_1);  OF=f-vector;  OX=(N,Euler characteristic);  O1a=(N,h1);  O1b=(N,h2);  O1=(N,h1,h2);  [O2 (graph class), O2f, O3 (labelled set)
refine O1 and are therefore zero-residual wherever O1 is: O1 is a function of the isomorphism class, and Y is a function of the labelled set.]
Ensembles (uniform): E_all = all 346,859 regimes; E_band = regimes whose N occurs among the beta_2>0 regimes; E_distinct = one system per distinct labelled arrangement set."""
import csv, gzip, json, os, sys, time
from collections import Counter, defaultdict
import _path
import census as cs
import ent

if __name__ == "__main__":
    t0 = time.time()
    REGS = cs.enumerate_regimes()
    rows = []
    with gzip.open(os.path.join(_path.ROOT, "RESULTS", "census_regimes.csv.gz"), "rt") as f:
        rd = csv.reader(f)
        next(rd)
        for r in rd:
            rows.append((tuple(map(int, r[3:9])), tuple(map(int, r[9:15]))))
    assert len(rows) == len(REGS)
    Y = [1 if b[2] > 0 else 0 for b, _ in rows]
    posN = Counter(REGS[i][2] for i in range(len(REGS)) if Y[i])
    out = {"regimes": len(REGS), "positives": sum(Y), "distinct_N_among_positives": len(posN)}
    # --- pair statistics
    negN = Counter(REGS[i][2] for i in range(len(REGS)) if not Y[i] and REGS[i][2] in posN)
    out["cross_pairs_equal_N_different_Y"] = sum(posN[n] * negN[n] for n in posN)
    bycont = defaultdict(list)
    for i, r in enumerate(REGS):
        bycont[r[0]].append(i)
    same = []
    for C, ids in bycont.items():
        ps = [i for i in ids if Y[i]]
        if not ps:
            continue
        for i in ps:
            for j in ids:
                if not Y[j] and REGS[j][2] == REGS[i][2]:
                    same.append((i, j))
    out["same_content_pairs_equal_N_different_Y"] = len(same)
    out["positives_with_a_same_content_partner"] = len({i for i, _ in same})
    # --- band signatures (O1) exact
    band = [i for i in range(len(REGS)) if REGS[i][2] in posN]
    out["band_regimes"] = len(band)
    sig1 = {}
    for k, i in enumerate(band):
        sig1[i] = cs.ball_histograms(cs.adjacency(REGS[i][3]))
        if k == 3000:
            print("eta", round((time.time() - t0) / 3000 * len(band)), "s", flush=True)
    chi = lambda fv: sum((-1) ** d * c for d, c in enumerate(fv))

    def observables(i):
        N, (b, fv) = REGS[i][2], rows[i]
        o = {"O0": (N,), "OE": (N, fv[1]), "OF": fv, "OX": (N, chi(fv))}
        if i in sig1:
            h1, h2 = sig1[i]
            o.update({"O1a": (N, h1), "O1b": (N, h2), "O1": (N, h1, h2)})
        else:  # outside the band N alone identifies Y=0: any refinement is constant on the N-class together with N
            o.update({"O1a": (N,), "O1b": (N,), "O1": (N,)})
        return o
    OBS = [observables(i) if True else None for i in range(len(REGS))]
    LEV = ["O0", "OE", "OF", "OX", "O1a", "O1b", "O1"]
    seen = {}
    distinct = []
    for i, r in enumerate(REGS):
        if r[3] not in seen:
            seen[r[3]] = i
            distinct.append(i)
    ens = {"E_all": list(range(len(REGS))), "E_band": band, "E_distinct": distinct}
    out["ensembles"] = {}
    for en, ids in ens.items():
        out["ensembles"][en] = {lev: ent.profile((Y[i], OBS[i][lev]) for i in ids) for lev in LEV}
        print(en, {l: (v["H(Y|O)"][:9], v["mixed_classes"]) for l, v in out["ensembles"][en].items()}, flush=True)
    # --- per-positive isolation: number of equal-N negatives and how many survive each refinement
    iso_tab = []
    negs_by_N = defaultdict(list)
    for i in band:
        if not Y[i]:
            negs_by_N[REGS[i][2]].append(i)
    for i in band:
        if not Y[i]:
            continue
        cnt = {"N": len(negs_by_N[REGS[i][2]])}
        for lev in LEV[1:]:
            cnt[lev] = sum(1 for j in negs_by_N[REGS[i][2]] if OBS[j][lev] == OBS[i][lev])
        iso_tab.append({"content": list(REGS[i][0]), "L": REGS[i][1], "N": REGS[i][2], "beta2": rows[i][0][2], "equal_N_negatives": cnt})
    out["positives_vs_negatives_remaining"] = {lev: sum(1 for x in iso_tab if x["equal_N_negatives"][lev] > 0) for lev in ["N"] + LEV[1:]}
    out["positives_table"] = iso_tab
    # --- representative pairs
    reps = []
    for (i, j) in same[:5]:
        reps.append({"content": list(REGS[i][0]), "L_pos": REGS[i][1], "L_neg": REGS[j][1], "N": REGS[i][2], "h1_pos": sig1[i][0], "h1_neg": sig1[j][0], "h2_pos": sig1[i][1], "h2_neg": sig1[j][1],
                     "betti_pos": list(rows[i][0]), "betti_neg": list(rows[j][0]), "f_pos": list(rows[i][1]), "f_neg": list(rows[j][1])})
    out["same_content_examples"] = reps
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E11_equal_count_pairs.json"), "w"), indent=1, default=list)
    print({k: v for k, v in out.items() if k not in ("positives_table", "ensembles", "same_content_examples")})
