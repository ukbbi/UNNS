"""E31 (S3-5) -- exact verification of the E30 predictions on the full 7-label regime complexes (cell_boundary, 4-cell boundaries):
 positives : every content with a predicted hole regime (first listed pattern; all patterns for the first 25 contents) -> the lifted cycle z3 is present in X(K_P),
             is NOT a boundary (no 4-chain fills it), beta_3 >= 1, and a cochain phi with phi(z3)=1, phi o d4 = 0 is produced and verified;
 negatives : random (content, pattern) pairs predicted to have NO hole at K_P (some family admissible) -> z3 present and IS a boundary (fill chain found, boundary verified)."""
import json, os, random, sys, time
import multiprocessing as mp
import _path
import cell_boundary as cb
import threshold_closure as tc
import E30_arithmetic_census as E30  # noqa: F401  (loads patterns)
from pk import PK
LM = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 30
P7 = PK(7)
R = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E30_arithmetic_census_L%d.json" % LM)))
PAT = {"%d%d" % (p["a"], p["b"]): p for p in E30.PAIRS}


def check(job):
    C, name, K, expect = job
    t = time.time()
    p = PAT[name]
    cx = cb.Complex(tc.source_mask(tuple(C), K), 7)
    pos = {g: j for j, g in enumerate(cx.dims[3])}
    ids = p["z3_faces"]
    rec = {"content": list(C), "pattern": name, "K": str(K), "expect_hole": expect, "arrangements": cx.f()[0], "z3_present": all(g in pos for g in ids)}
    if not rec["z3_present"]:
        rec["ok"] = False
        return rec
    z = sum(1 << pos[g] for g in ids)
    fc = cb.fill_chain(cx, 3, z)
    rec["z3_bounds"] = fc is not None
    if fc is not None:
        acc = cb.boundary_of_chain(cx, 4, fc)
        rec["fill_verified"] = acc == z
    else:
        reps, piv = cb.homology_representatives(cx, 3)
        phi = cb.cocycle_certificate(cx, 3, z, piv)
        v = cb.verify_cocycle(cx, 3, z, phi)
        rec["cocycle_verified"] = bool(v["z_is_cycle"] and v["phi_kills_all_boundaries"] and v["phi_of_z"] == 1)
        rec["beta3"] = cx.betti()[3]
        rec["phi_weight"] = phi.bit_count()
    rec["ok"] = (not rec["z3_bounds"] and rec.get("cocycle_verified", False)) if expect else (rec["z3_bounds"] and rec.get("fill_verified", False))
    rec["seconds"] = round(time.time() - t, 1)
    return rec


if __name__ == "__main__":
    rnd = random.Random(31)
    jobs = []
    for n, r in enumerate(R["records"]):
        pats = r["patterns"] if n < 25 else r["patterns"][:1]
        for name, K in pats:
            jobs.append((r["content"], name, int(K), True))
    # negatives: contents with labels <= 20 (not in hit list) -- the pattern is present at K_P but a family is admissible
    hit = {tuple(r["content"]) for r in R["records"]}
    import itertools
    from math import lcm
    negs = []
    pool = [c for c in itertools.combinations(range(2, 21), 7) if c not in hit]
    rnd.shuffle(pool)
    for C in pool[:30000]:
        D = E30.denominators(list(C))
        name = rnd.choice(sorted(PAT))
        ok, K = E30.exists(D, PAT[name]["Pset"], PAT[name]["fam_masks"])
        if not ok and K < 400000:
            negs.append((list(C), name, K, False))
        if len(negs) >= 100:
            break
    jobs += negs
    t0 = time.time()
    with mp.get_context("fork").Pool(2) as pool_:
        res = []
        for i, r in enumerate(pool_.imap_unordered(check, jobs, chunksize=1)):
            res.append(r)
            if i % 25 == 0:
                print(i, len(jobs), round(time.time() - t0), flush=True)
    out = {"Lmax": LM, "positives": sum(1 for r in res if r["expect_hole"]), "positives_ok": sum(1 for r in res if r["expect_hole"] and r["ok"]),
           "negatives": sum(1 for r in res if not r["expect_hole"]), "negatives_ok": sum(1 for r in res if not r["expect_hole"] and r["ok"]),
           "beta3_hist": {}, "failures": [r for r in res if not r["ok"]], "seconds": round(time.time() - t0, 1), "records": res}
    for r in res:
        if r.get("beta3") is not None:
            out["beta3_hist"][r["beta3"]] = out["beta3_hist"].get(r["beta3"], 0) + 1
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E31_verify_regimes_L%d.json" % LM), "w"), indent=1)
    print({k: v for k, v in out.items() if k not in ("records",)})
