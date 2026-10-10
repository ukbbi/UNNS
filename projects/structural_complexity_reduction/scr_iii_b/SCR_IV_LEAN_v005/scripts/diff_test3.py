#!/usr/bin/env python3
"""IV-3 differential test (EVIDENCE, NOT PROOF). usage: diff_test3.py ROOT  (run with `lake` on PATH)
 (a) Python transcription of solver_v010.cpp::bound/dfs-accumulator in exact integers  vs  Lean `solverBound`/`pathAcc`/`Bnd` (#eval), and
 (b) the bound vs BRUTE-FORCE minimum over all completions of deep prefixes (d>=30: at most 1024 completions; never 2^40), and
 (c) random small instances (n<=9) with EVERY prefix and EVERY completion.
The 2^40 space is not enumerated."""
import sys, random, subprocess, pathlib, re, ast, itertools
from fractions import Fraction
ROOT = pathlib.Path(sys.argv[1]); sys.dont_write_bytecode = True
t = (ROOT/"data/real_4x4.txt").read_text().split(); n = 40; c = 2
K = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(i+1, n):
        fr = Fraction(float(t[c])) * (1 << 70); assert fr.denominator == 1; K[i][j] = int(fr); c += 1
def cpp_bound(n, d, K, s):
    acc = 0
    for dd in range(d):                      # dfs accumulator
        field = 0
        for i in range(dd): field += K[i][dd]*s[i]
        acc += s[dd]*field
    l = acc                                  # bound(d, acc), same loop order
    for j in range(d, n):
        field = 0
        for i in range(d): field += K[i][j]*s[i]
        l -= abs(field)
        for h in range(j+1, n): l -= abs(K[j][h])
    return l
def H(n, K, s): return sum(K[i][j]*s[i]*s[j] for i in range(n) for j in range(i+1, n))
sp = lambda p, m: [1 if (p >> i) & 1 else -1 for i in range(m)]
rng = random.Random(20261011)
# (c) small random instances: every prefix, every completion
bad_c = 0; cnt_c = 0
for trial in range(40):
    m = rng.randint(2, 9); Ks = [[rng.randint(-50, 50) if j > i else 0 for j in range(m)] for i in range(m)]
    for d in range(m+1):
        for pre in itertools.product([1, -1], repeat=d):
            b = cpp_bound(m, d, Ks, list(pre)+[0]*(m-d))
            mn = min(H(m, Ks, list(pre)+list(rest)) for rest in itertools.product([1, -1], repeat=m-d))
            cnt_c += 1
            if not b <= mn or (d == m and b != mn): bad_c += 1
# (a),(b) real instance
cases = []
for d in (30, 31, 32, 34, 36, 38, 40):
    for _ in range(4): cases.append((rng.getrandbits(40), d))
cases += [(711243241830, 32), (161487427942, 32), (711243241830, 40), (161487427942, 40)]
src = "import SCR_IV_Prune\nopen SCR_IV\n#eval [%s].map (fun (p, d) => (solverBound 40 d kAt (sigmaAt p) (pathAcc kAt (sigmaAt p) d), Bnd 40 d kAt (sigmaAt p)))\n" % ", ".join("(%d, %d)" % x for x in cases)
(ROOT/"tests/_Diff3.lean").write_text(src)
out = subprocess.run(["lake", "env", "lean", "tests/_Diff3.lean"], cwd=ROOT, capture_output=True, text=True).stdout
res = ast.literal_eval(out.strip()); assert len(res) == len(cases), out[:200]
bad_a = bad_b = 0; minslack = None
for (p, d), (lb, lbnd) in zip(cases, res):
    s = sp(p, 40); pb = cpp_bound(40, d, K, s)
    if pb != lb or pb != lbnd: bad_a += 1
    mn = min(H(40, K, s[:d] + sp(r, 40-d)) for r in range(1 << (40-d)))
    if not pb <= mn: bad_b += 1
    sl = mn - pb; minslack = sl if minslack is None else min(minslack, sl)
    if d == 40 and pb != H(40, K, s): bad_b += 1
print("(c) small random instances, all prefixes x completions:", cnt_c, "checks, violations:", bad_c)
print("(a) python-vs-Lean bound mismatches on real instance:", bad_a, "of", len(cases), " (b) bound>min-completion violations:", bad_b, " min slack (scaled 2^-70 A):", minslack)
sys.exit(0 if bad_a == 0 and bad_b == 0 and bad_c == 0 else 1)
