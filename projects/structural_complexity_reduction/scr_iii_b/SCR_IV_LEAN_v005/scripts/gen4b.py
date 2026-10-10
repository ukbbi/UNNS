#!/usr/bin/env python3
"""IV-4B gate 1: UNTRUSTED certificate generator for the frozen 4x4 instance (exact integers only; no floating-point search, no incumbent).
usage: gen4b.py ROOT OBJ(ground|nong) D0 OUTDIR
Writes OUTDIR/cert_<OBJ>_D<D0>.txt (line b = certificate integer of frontier prefix b), stats json. Nothing here is trusted: Lean re-checks every certificate."""
import sys, json, hashlib, pathlib, time
sys.set_int_max_str_digits(0); sys.setrecursionlimit(10000)
from fractions import Fraction
ROOT = pathlib.Path(sys.argv[1]); OBJ = sys.argv[2]; D0 = int(sys.argv[3]); OUT = pathlib.Path(sys.argv[4]); OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT/"scripts")); 
t = (ROOT/"data/real_4x4.txt").read_text().split(); n = 40; c = 2
K = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(i+1, n):
        fr = Fraction(float(t[c])) * (1 << 70); assert fr.denominator == 1; K[i][j] = int(fr); c += 1
vt = t[c:]; VERTS = [(int(vt[2*v]), int(vt[2*v+1])) for v in range(16)]
R = [[K[d][j] for j in range(d+1, n)] for d in range(n)]
sabs = lambda l: sum(abs(x) for x in l)
def H(b):
    s = [1 if (b >> i) & 1 else -1 for i in range(n)]
    return sum(K[i][j]*s[i]*s[j] for i in range(n) for j in range(i+1, n))
def leafGrammar(b):
    return all(sum(1 for i in range(n) if (m >> i) & 1 and (((b >> i) & 1) == ((p >> i) & 1))) == 2 for m, p in VERTS)
G_ID, N_ID = 711243241830, 161487427942
if OBJ == "ground": U = H(G_ID); leafOK = lambda b: False
elif OBJ == "nong": U = H(N_ID); leafOK = leafGrammar; assert not leafGrammar(N_ID) and leafGrammar(G_ID)
elif OBJ == "nongT": U = H(711243241766); leafOK = leafGrammar; assert not leafGrammar(711243241766)   # exact minimum found by scripts/diag_nong.py
else: raise SystemExit("OBJ")
nodes = [0]
def gen(d, acc, F, T, bits, out):
    nodes[0] += 1
    if U <= acc - sabs(F) - T: out.append(0); return
    if d == n:
        assert leafOK(bits), ("INVALID: leaf below U", bits)   # untrusted generator refuses to emit an unprovable certificate
        out.append(2); return
    out.append(1); f = F[0]; fs = F[1:]; row = R[d]; Tn = T - sabs(row)
    gen(d+1, acc - f, [a - r for a, r in zip(fs, row)], Tn, bits, out)
    gen(d+1, acc + f, [a + r for a, r in zip(fs, row)], Tn, bits | (1 << d), out)
def encode(tok):
    cc = 0
    for k, x in enumerate(tok): cc |= x << (2*k)
    return cc | (1 << (2*len(tok)))
certs = [None]*(1 << D0); ntok = [0]*(1 << D0); shallow = [0]
def top(d, acc, F, T, bits):
    if d < D0 and U <= acc - sabs(F) - T:       # shallow prune: all 2^(D0-d) descendants get the one-token certificate (monotone bound)
        for b in range(bits, bits + (1 << d) * (1 << (D0 - d)), 1 << d): certs[b] = 4; ntok[b] = 1
        shallow[0] += 1; nodes[0] += 1; return
    if d == D0:
        tok = []; gen(d, acc, F, T, bits, tok); certs[bits] = encode(tok); ntok[bits] = len(tok); return
    nodes[0] += 1; f = F[0]; fs = F[1:]; row = R[d]; Tn = T - sabs(row)
    top(d+1, acc - f, [a - r for a, r in zip(fs, row)], Tn, bits)
    top(d+1, acc + f, [a + r for a, r in zip(fs, row)], Tn, bits | (1 << d))
t0 = time.time(); top(0, 0, [0]*n, sum(sabs(r) for r in R), 0)
assert all(x is not None for x in certs)
# note: prefixes pruned above get certificate 4 = token 0 + sentinel; the Lean checker recomputes the bound at depth D0 (>= the shallower bound), so it accepts.
body = "\n".join(str(x) for x in certs) + "\n"
fn = OUT/f"cert_{OBJ}_D{D0}.txt"; fn.write_text(body)
st = dict(obj=OBJ, D0=D0, U=U, prefixes=len(certs), total_tokens=sum(ntok), max_tokens=max(ntok), argmax=ntok.index(max(ntok)),
          hist={k: sum(1 for x in ntok if lo <= x < hi) for k, (lo, hi) in {"1":(1,2),"2-99":(2,100),"100-999":(100,1000),"1000-2499":(1000,2500),"2500-9999":(2500,10000),"10000+":(10000,10**9)}.items()},
          gen_seconds=round(time.time()-t0, 1), cert_file=fn.name, cert_sha256=hashlib.sha256(body.encode()).hexdigest(), cert_bytes=len(body), ntok=ntok)
(OUT/f"stats_{OBJ}_D{D0}.json").write_text(json.dumps(st))
print({k: v for k, v in st.items() if k != "ntok"})
