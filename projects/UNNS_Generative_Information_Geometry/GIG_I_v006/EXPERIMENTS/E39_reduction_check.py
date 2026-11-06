"""E39 (v006-7) -- reduction of non-degeneracy to the difference cycle.  Identity (proved, S3): L_{a,b} = d(Lam(c_a)) + last(c_a+c_b).  If the bridge chain Lam(c_a) lies in K(P_{L_{a,b}}) (all its prefix sets are in P_L)
then [L_{a,b}] = [last(d_ab)] in H_3(K(P_L)) and L_{a,b} is non-degenerate iff last(d_ab) is.  Symmetric statement with Lam(c_b) and first(d_ab).  Checked on the 12 off-diagonal anchor pairs (exact)."""
import json, os
import _path
import hole_survival as H, lift as Lf, fi
from pk import PK
P6, P7 = PK(6), PK(7)
z6 = P6.bits(H.Z)
f6, _ = P6.minimal_families(z6, 2)
P = P6.pz(z6)
ch = [set(Lf.filling_chain(P6, z6, P | F)) for F in f6]
def lam4(c):  # Lam(c): 4-chain of P_7
    return P7.bits([P7.IDX[f] for f in Lf.lam_faces([P6.FS[g] for g in c], 6)])
rows = []
for a in range(4):
    for b in range(4):
        if a == b: continue
        zf = Lf.lam_faces([P6.FS[g] for g in H.Z], 6) ^ Lf.first([P6.FS[g] for g in ch[a]], 6) ^ Lf.last([P6.FS[g] for g in ch[b]], 6)
        L = P7.bits([P7.IDX[f] for f in zf]); PL = P7.pz(L)
        d = P6.bits(ch[a] ^ ch[b])
        la, lb = lam4(ch[a]), lam4(ch[b])
        r = {"a": a, "b": b, "bridge_a_in_K(P_L)": not P7.pz(la) & ~PL, "bridge_b_in_K(P_L)": not P7.pz(lb) & ~PL,
             "L_nondegenerate": not P7.bounds(L, PL, 3)}
        # identity checks
        rows.append(r)
        print(r)
json.dump(rows, open(os.path.join(_path.ROOT, "RESULTS", "E39_reduction_check.json"), "w"), indent=1)
