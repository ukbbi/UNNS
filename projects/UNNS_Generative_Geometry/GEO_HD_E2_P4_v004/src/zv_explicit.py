"""v004: explicit form of the zero-vertex condition (P4-Z2) and structure of 'hard' cells.
For a cell C = P(u; g_1..g_j) (corners in the box, all >= 0): coordinatewise minimum corner m(C) = u + sum_i min(g_i,0).
P4-Z2: a zero-vertex decomposition exists  <=>  m(C) = 0  and  g_i^- in Lambda' for every i   (g^- = componentwise min(g,0)).
Over all 2^j representations (base corner / generator signs):  C is robustly flagged  <=>  m(C) = 0 and g_i^+ and g_i^- in Lambda' for all i."""
from itertools import product


def neg(g):
    return tuple(min(x, 0) for x in g)


def pos(g):
    return tuple(max(x, 0) for x in g)


def min_corner(base, gens):
    return tuple(base[c] + sum(min(g[c], 0) for g in gens) for c in range(len(base)))


def zv_explicit(base, gens, inLp):
    return all(x == 0 for x in min_corner(base, gens)) and all(inLp(neg(g)) for g in gens)


def robustly_flagged(base, gens, inLp):
    return all(x == 0 for x in min_corner(base, gens)) and all(inLp(neg(g)) and inLp(pos(g)) for g in gens)
