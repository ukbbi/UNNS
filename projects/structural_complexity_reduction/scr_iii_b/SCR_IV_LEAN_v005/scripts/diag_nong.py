#!/usr/bin/env python3
"""DIAGNOSTIC (untrusted, exact integers): exact minimum of H over NON-grammar states, by branch-and-bound with strict-improvement pruning.
Purpose: IV-4B gate 1 found a non-grammar leaf below the frozen claimedNonGNum. This script finds the exact minimum value + one minimiser.
Seeded with the known one-flip state (an upper bound) so that the search is short. Not a re-run of SCR-III; does not touch any frozen file."""
import sys, pathlib, time
sys.set_int_max_str_digits(0); sys.setrecursionlimit(10000)
src = open(pathlib.Path(sys.argv[1])/"scripts/gen4b.py").read().split("nodes = [0]")[0]
sys.argv = ['gen4b', sys.argv[1], 'nong', '12', '/tmp/claude-0/w4/gen_diag']
exec(src)
best = [H(711243241766), 711243241766]; cnt = [0]; ties = []
def dfs(d, acc, F, T, bits):
    cnt[0] += 1
    B = acc - sabs(F) - T
    if B > best[0]: return
    if B == best[0] and d < n: ties.append(0)
    if d == n:
        if not leafGrammar(bits):
            if B < best[0]: best[0] = B; best[1] = bits
        return
    f = F[0]; fs = F[1:]; row = R[d]; Tn = T - sabs(row)
    dfs(d+1, acc - f, [a - r for a, r in zip(fs, row)], Tn, bits)
    dfs(d+1, acc + f, [a + r for a, r in zip(fs, row)], Tn, bits | (1 << d))
t0 = time.time(); dfs(0, 0, [0]*n, sum(sabs(r) for r in R), 0)
print("nodes", cnt[0], "sec", round(time.time()-t0, 1))
print("exact nonG min (num/2^70):", best[0], " minimiser id:", best[1], " grammar:", leafGrammar(best[1]), " recomputed H:", H(best[1]))
print("frozen claimedNonG:", H(161487427942), " diff (frozen - true):", H(161487427942)-best[0], " in A units:", (H(161487427942)-best[0])/2**70)
print("ground:", H(711243241830), " true gap num:", best[0]-H(711243241830), " frozen gap num:", H(161487427942)-H(711243241830))
