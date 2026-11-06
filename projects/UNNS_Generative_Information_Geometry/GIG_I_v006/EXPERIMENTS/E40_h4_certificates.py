"""E40 (v006-8) -- explicit cycle/cochain certificates for the E38 arithmetic H_4 hits (identity role map, GF(2)).
For each hit: the 4-cycle L2 in P_8 (as faces), the admissible set A(m), and a cochain phi with phi(L2)=1, phi o d = 0 on all admitted 5-faces; checked by an independent verifier (no elimination)."""
import json, os, time
import _path
import cert
from E30_arith import denominators
import E37_h3_to_h4 as E37
P8 = E37.P8

if __name__ == "__main__":
    hits = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E38_h4_arithmetic.json")))["hits"]
    out = []
    for h in hits:
        t = time.time()
        (a, b), (i, j) = h["pair"], h["fill"]
        l2, _, _ = E37.second_lift((a, b), i, j)
        D = denominators(h["content"])
        K = int(h["m"])
        A = sum(1 << s for s in range(1, 256) if K % D[s] == 0)
        phi = cert.solve(P8, A, 4, l2)
        ok, msg = (False, "no cochain") if phi is None else cert.verify_certificate(P8, A, 4, l2, phi)
        rec = {"content": h["content"], "m": h["m"], "pair": h["pair"], "fill": h["fill"], "cycle_faces": bin(l2).count("1"), "admitted_5faces": sum(1 for i5 in range(len(P8.FS)) if P8.DIM[i5] == 5 and not P8.PM[i5] & ~A),
               "phi_support": None if phi is None else len(phi), "verified": ok, "verifier_msg": msg, "seconds": round(time.time() - t, 1)}
        out.append(rec)
        print(rec, flush=True)
        if phi is not None and ok and len(out) == 1:
            json.dump({"content": h["content"], "m": h["m"], "pair": h["pair"], "fill": h["fill"], "cycle": [[list(B) for B in P8.FS[g]] for g in range(len(P8.FS)) if l2 >> g & 1],
                       "cochain": [[list(B) for B in P8.FS[g]] for g in phi]}, open(os.path.join(_path.ROOT, "CERTIFICATES", "h4_certificate_first_hit.json"), "w"))
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E40_h4_certificates.json"), "w"), indent=1)
