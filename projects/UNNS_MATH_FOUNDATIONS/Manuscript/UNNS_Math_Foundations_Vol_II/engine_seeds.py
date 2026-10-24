"""Seed generators for the experiments of Volume II (reset states of prime-g orbits)."""
import random
from engine import *
GS = [p for p in range(11, 260) if is_prime(p)]
def congruent_prime(r, g):
    for k in range(0, 600):
        u = r + k * g
        if u > 1 and is_prime(u) and u != g: return u
def gen_reset(rng):
    """random reset state (gamma=1) with G=g exactly, g prime <200; returns (g, E)."""
    g = rng.choice([x for x in GS if x < 200]); Es = {}
    for p in rng.sample([2, 3, 5, 7, 11, 13], rng.randint(1, 4)):
        if g % p: Es[p] = rng.randint(1, 6)
    for _ in range(rng.randint(0, 2)):
        r = rng.randint(2, g - 1); u = congruent_prime(r, g)
        if u and u not in Es: Es[u] = rng.randint(1, max(1, min(8, ordmod(r, g))))
    n = normalise(g, 1, Es)
    if n is None or n[0] != 1 or not n[1]: return None
    return g, n[1]
