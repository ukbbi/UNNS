#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v009 -- deterministic seed registry and structural-null machinery (target-blind).

Seed derivation (domain separated by family and draw index, identical to the frozen v006 derivation):
    label(family, idx) = "<master>|<family>|<idx>"        master = 20261010  (PROPOSED, not frozen)
    rng(family, idx)   = random.Random(label)              (CPython seeds str via SHA-512: platform independent)
    seed_sha256        = SHA-256(label)                    (registry fingerprint)
Nulls are NEVER ranked or selected using physical-target performance; the only rejections are structural / counting rejections, logged with reasons.
Survivor counts come from the grammar-only constructive counter (no Hamiltonian is evaluated).
"""
import hashlib, importlib.util, json, pathlib, random, sys
from collections import Counter

MASTER_SEED = 20261010
FAMILIES = {"N1": "DEGREE_PRESERVING_SWAP", "N2": "FREE_RANDOM_4SET"}      # N1 degree-preserving, N2 free incidence (v006 families)


def load_v006_nulls(feas_dir):
    p = pathlib.Path(feas_dir) / "grammar_nulls_v006.py"
    sys.path.insert(0, str(feas_dir))
    old = sys.dont_write_bytecode; sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("grammar_nulls_v006_frozen", p)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = old
    return mod


def label(family, idx, master=MASTER_SEED):
    return "%d|%s|%d" % (master, family, idx)


def seed_sha256(family, idx, master=MASTER_SEED):
    return hashlib.sha256(label(family, idx, master).encode()).hexdigest()


def rng_for(family, idx, master=MASTER_SEED):
    return random.Random(label(family, idx, master))


def canon_key(inc):
    """Order-insensitive canonical form of an incidence (vertex order and slot order carry no meaning for the grammar)."""
    return tuple(sorted(tuple(sorted((int(i), int(s)) for i, s in ent)) for ent in inc))


def inc_sha256(inc):
    return hashlib.sha256(json.dumps(canon_key(inc)).encode()).hexdigest()


def well_formed(inc, inc_real, n_islands, family, v6):
    """Structural well-formedness only (no Hamiltonian, no target)."""
    if len(inc) != len(inc_real):
        return False, "vertex count changed"
    for ent in inc:
        if len(ent) != 4:
            return False, "arity changed"
        if len({i for i, _ in ent}) != 4:
            return False, "duplicate island at a vertex"
        if any((not (0 <= i < n_islands)) or s not in (-1, 1) for i, s in ent):
            return False, "island index or sigma out of range"
    if family == FAMILIES["N1"]:
        if v6.degree_profile(inc) != v6.degree_profile(inc_real):
            return False, "degree/sigma profile changed (implementation error)"
    return True, ""


def draw(family, idx, inc_real, n_islands, v6):
    rng = rng_for(family, idx)
    if family == FAMILIES["N1"]:
        inc, att, rej = v6.swap_null(inc_real, rng)
        return inc, att, rej
    return v6.free_null(inc_real, n_islands, rng), 0, 0


def generate(family, inc_real, n_islands, count, survivors_fn, v6, max_tries=None):
    """Deterministic generation with full accounting.  survivors_fn(inc) -> int (grammar-only survivor count) or None if the cap was hit.
    Returns (nulls, accounting).  accounting: attempted (draws consumed), accepted, duplicate, rejected-by-reason, exhausted."""
    max_tries = max_tries if max_tries is not None else 5 * count
    nulls, seen, acc = [], set(), Counter()
    real_key = canon_key(inc_real); idx = 0
    while len(nulls) < count and idx < max_tries:
        inc, att, rej = draw(family, idx, inc_real, n_islands, v6)
        acc["move_attempts"] += att; acc["move_rejections"] += rej
        ok, why = well_formed(inc, inc_real, n_islands, family, v6)
        key = canon_key(inc)
        if not ok:
            acc["rejected:" + why] += 1
        elif key == real_key:
            acc["rejected:identical to real incidence"] += 1
        elif key in seen:
            acc["duplicate"] += 1
        else:
            cnt = survivors_fn(inc)
            if cnt is None:
                acc["rejected:survivor-count cap hit (more than the declared cap)"] += 1
            elif cnt == 0:
                acc["rejected:empty grammar (no surviving configuration)"] += 1
            else:
                seen.add(key)
                nulls.append(dict(idx=idx, label=label(family, idx), seed_sha256=seed_sha256(family, idx), inc=inc, inc_sha256=inc_sha256(inc), survivors=cnt))
        idx += 1
    acc["attempted"] = idx; acc["accepted"] = len(nulls); acc["exhausted"] = len(nulls) < count
    return nulls, dict(acc)


def registry_digest(entries):
    h = hashlib.sha256()
    for e in entries:
        h.update(("%s|%d|%s|%s|%d\n" % (e["family"], e["idx"], e["seed_sha256"], e["inc_sha256"], e["survivors"])).encode())
    return h.hexdigest()
