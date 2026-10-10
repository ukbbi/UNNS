#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v006 -- target-blind structural nulls by rewiring grammar incidence.

The physical patch, Hamiltonian, nominal space and target sets are never touched; only the incidence list
inc[v] = [(island, sigma) x4] is rewired. Nulls are NOT selected by preservation performance: the only rejections are
structural (malformed / identical-to-real / empty-grammar) and are logged with reasons.

Families
  DEGREE_PRESERVING_SWAP : repeated swaps of (island, sigma) between incidences of two different vertices.
        Preserves vertex count, vertex arity (4), every island's degree and every island's multiset of sigma.
  FREE_RANDOM_4SET       : each vertex receives 4 distinct random islands with random sigma.
        Preserves vertex count and arity only (island degrees are NOT preserved) -- a weaker, more adversarial null.
Controls: UNCHANGED (0 swaps; must reproduce the real grammar) and PERTURBED (one sigma flipped; must differ).
"""
import random
from collections import Counter
from energy_windows_v006 import compile_masks

MASTER_SEED = 20261010


def rng_for(family, idx):
    return random.Random("%d|%s|%d" % (MASTER_SEED, family, idx))


def valid_structure(inc_n, inc_real):
    """Structural validity: same vertex count, arity 4, distinct islands per vertex."""
    if len(inc_n) != len(inc_real):
        return False, "vertex count changed"
    for ent in inc_n:
        if len(ent) != 4:
            return False, "arity changed"
        if len({i for i, _ in ent}) != 4:
            return False, "duplicate island at a vertex"
    return True, ""


def degree_profile(inc):
    d = Counter(); sg = {}
    for ent in inc:
        for i, s in ent:
            d[i] += 1; sg.setdefault(i, []).append(s)
    return dict(d), {i: sorted(v) for i, v in sg.items()}


def swap_null(inc_real, rng, n_swaps=None):
    """Return (incidence, move_attempts, move_rejections)."""
    inc = [list(e) for e in inc_real]
    slots = [(v, k) for v, e in enumerate(inc) for k in range(len(e))]
    n_swaps = n_swaps if n_swaps is not None else 10 * len(slots)
    done = att = rej = 0
    while done < n_swaps and att < 50 * n_swaps + 100:
        att += 1
        (v1, k1), (v2, k2) = rng.sample(slots, 2)
        if v1 == v2:
            rej += 1; continue
        a, b = inc[v1][k1], inc[v2][k2]
        if any(i == b[0] for i, _ in inc[v1]) or any(i == a[0] for i, _ in inc[v2]):
            rej += 1; continue                    # would put the same island twice at one vertex
        inc[v1][k1], inc[v2][k2] = b, a
        done += 1
    return inc, att, rej


def free_null(inc_real, n_islands, rng):
    out = []
    for _ in inc_real:
        isl = rng.sample(range(n_islands), 4)
        out.append([(i, rng.choice((-1, 1))) for i in isl])
    return out


def unchanged_control(inc_real):
    return [list(e) for e in inc_real]


def perturbed_control(inc_real):
    inc = [list(e) for e in inc_real]
    i, s = inc[0][0]
    inc[0][0] = (i, -s)
    return inc


def survivors(n, inc):
    masks = compile_masks(inc)
    return [all(((s ^ nm) & im).bit_count() == 2 for im, nm in masks) for s in range(1 << n)]


def generate(family, inc_real, n, count, max_tries=None):
    """Generate `count` valid nulls. Returns (list of dicts, log). Each null: idx, seed_label, inc, surv."""
    nulls, log = [], Counter()
    real_key = frozenset(frozenset(e) for e in inc_real)
    real_prof = degree_profile(inc_real)
    tries = 0
    max_tries = max_tries or 20 * count
    while len(nulls) < count and tries < max_tries:
        idx = tries; tries += 1
        rng = rng_for(family, idx)
        if family == "DEGREE_PRESERVING_SWAP":
            inc, att, rej = swap_null(inc_real, rng)
            log["move_attempts"] += att; log["move_rejections"] += rej
        elif family == "FREE_RANDOM_4SET":
            inc = free_null(inc_real, n, rng)
        else:
            raise ValueError(family)
        ok, why = valid_structure(inc, inc_real)
        if not ok:
            log["rejected:" + why] += 1; continue
        if family == "DEGREE_PRESERVING_SWAP" and degree_profile(inc) != real_prof:
            log["rejected:degree profile changed (implementation error)"] += 1; continue
        if frozenset(frozenset(e) for e in inc) == real_key:
            log["rejected:identical to real incidence"] += 1; continue
        surv = survivors(n, inc)
        if not any(surv):
            log["rejected:empty grammar (no surviving configuration)"] += 1; continue
        nulls.append(dict(idx=idx, seed="%d|%s|%d" % (MASTER_SEED, family, idx), inc=inc, surv=surv))
    log["tries"] = tries; log["accepted"] = len(nulls)
    return nulls, dict(log)
