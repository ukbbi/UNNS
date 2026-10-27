"""GEO-I v007, Programme B: classification of shared-centre collisions of the binary 0/1 box complex.

Collision of two distinct cells A=P(x;S_1..S_r), B=P(y;T_1..T_t), r,t>=1  <=>  same union U and x=y outside U (Theorem B2 of v006, re-proved independently here
through the coset description).  Types: (r,t) with r<=t; 'full' if U=[n].
FACTS (proved in BINARY_RANK.md, machine re-checked here):
  F1  segment-segment and segment-multicircuit collisions do not exist (r=1 forces S_1=U=T-union, hence t=1 and the two cells are the same coset or both
      span(S)=2 elements: A=B).  Hence r,t>=2 for every collision.
  F2  in a minimal non-embedded box every collision has x = 1 on [n]\\U  (otherwise the collision survives the deletion of a coordinate where x=0).
  F3  full-support collision  =>  nullity n-rank(M) >= 3   (two distinct cells with union [n]: either two distinct nonzero cosets of one span, dim C>=r+2>=4,
      or two partitions, span(S)+span(T) has dim>=3).
Also records, per collision: (r,t,|U|,rank of generators, rank with delta)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binary_01 as B, binary_circuits as BC


def collisions(cols):
    byc, C, circ = B.cells_01(cols)
    out = []
    for cen, lst in byc.items():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                out.append((cen, lst[a], lst[b]))
    return out


def collision_type(n, cen, a, b):
    U, xo = cen
    return {'r': len(a[2]), 't': len(b[2]), 'U': bin(U).count('1'), 'full': U == (1 << n) - 1, 'x_outside_ones': bin(xo).count('1') == bin((1 << n) - 1 & ~U).count('1')}


def check_facts(cols):
    """returns dict of booleans for F1,F3 on this box (F2 is only meaningful for minimal boxes)."""
    n = len(cols); cs = collisions(cols); res = {'F1': all(len(a[2]) >= 2 and len(b[2]) >= 2 for _, a, b in cs)}
    res['F3'] = all(BC.nullity(cols) >= 3 for cen, a, b in cs if cen[0] == (1 << n) - 1)
    # coset description agrees with cells_01 on full-support cells
    fs = BC.full_support_cells(cols); byc, C, circ = B.cells_01(cols)
    cells01 = {frozenset(k) for (U, xo), lst in byc.items() if U == (1 << n) - 1 for (k, x, S) in lst}
    res['coset_description'] = cells01 == {co for p, co in fs}
    return res
