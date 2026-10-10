#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v006 -- energy-window analysis, target-blind grammar, constructive enumeration.

Uses the FROZEN v005 evaluator (physical_energy_v005.py) read-only through an importlib adapter; nothing in v005 is modified.

Grammar (target-blind): built ONLY from vertex incidence and spin orientation.
    incidence[v] = [(island_index, sigma), ...]   (4 entries per vertex)
    sigma = sign((vertex - island_centre) . u_island): the arrow s*u points TOWARD the vertex ("in") iff s*sigma = +1.
    G(s) = 1  <=>  every vertex has exactly two 'in' arrows.
No energy, ground-state label or target membership enters this module's grammar.
"""
import importlib.util, pathlib, sys, time
from math import sqrt

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
V005_DIR = PROJECT / "scr_iii_b" / "reference_check"

T_REF = 792.0                 # K, v005 reference temperature (ordering is T-invariant, B(T)=0)
LEVEL_TOL_REL = 1e-9          # degeneracy tolerance on |E - E'| / max|E| (normalized units); roundoff is ~1e-16
A_LAT = 260.0


def load_v005():
    """Import the frozen v005 evaluator read-only (no bytecode written next to frozen files)."""
    path = V005_DIR / "physical_energy_v005.py"
    if not path.exists():
        raise FileNotFoundError(str(path))
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("physical_energy_v005_frozen", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = old
    return mod


# ---------------------------------------------------------------- patch, incidence, grammar
def build_patch(pe, L):
    isl = pe.source_geometry(L)
    pairs = pe.K_pairs(isl)
    vpos = pe.vertex_positions(L)
    return isl, pairs, vpos


def build_incidence(pe, isl, vpos):
    """Real-incidence grammar from geometry alone: per vertex 4 (island, sigma) plus ENWS role index of each island."""
    inc, roles = [], []
    for (vx, vy) in vpos:
        ent, rl = [], {}
        for i, p in enumerate(isl):
            d = sqrt((p.x - vx) ** 2 + (p.y - vy) ** 2)
            if 1e-9 < d < 0.5 * A_LAT + 1e-9:
                dot = (vx - p.x) * p.ux + (vy - p.y) * p.uy
                ent.append((i, 1 if dot > 0 else -1))
                if p.uy == 0:                      # horizontal island: E if centre right of vertex, else W
                    rl[i] = 0 if p.x > vx else 2
                else:                              # vertical island: N if centre above vertex, else S
                    rl[i] = 1 if p.y > vy else 3
        inc.append(ent); roles.append(rl)
    return inc, roles


def compile_masks(inc):
    """Per vertex (island_mask, negmask): in-bits = (state ^ negmask) & island_mask, state bit 1 <=> s=+1."""
    out = []
    for ent in inc:
        im = nm = 0
        for i, sg in ent:
            im |= 1 << i
            if sg < 0:
                nm |= 1 << i
        out.append((im, nm))
    return out


def in_counts(state_id, masks):
    return [((state_id ^ nm) & im).bit_count() for im, nm in masks]


def violated_vertices(state_id, masks):
    return [v for v, c in enumerate(in_counts(state_id, masks)) if c != 2]


def grammar_set(n, masks):
    """Brute-force survivor flags over the nominal space."""
    return [all(((s ^ nm) & im).bit_count() == 2 for im, nm in masks) for s in range(1 << n)]


# source vertex typing (independent re-implementation; E,N,W,S -> bits 0..3, bit=1 for s=+1)
TYPE_OF_ENWS = {}
for _c in range(16):
    if _c in (3, 12): TYPE_OF_ENWS[_c] = 1
    elif _c in (0, 5, 10, 15): TYPE_OF_ENWS[_c] = 2
    elif _c in (6, 9): TYPE_OF_ENWS[_c] = 4
    else: TYPE_OF_ENWS[_c] = 3


def vertex_types(state_id, inc, roles):
    res = []
    for ent, rl in zip(inc, roles):
        code = 0
        for i, _sg in ent:
            if (state_id >> i) & 1:
                code |= 1 << rl[i]
        res.append(TYPE_OF_ENWS[code])
    return res


# ---------------------------------------------------------------- levels and windows
def group_levels(En, tol_rel=LEVEL_TOL_REL):
    """Cluster numerically degenerate energies (normalized units). Returns (level_of_state, levels) with
    levels[k] = dict(E_min, E_max, members)."""
    sc = max(abs(e) for e in En) or 1.0
    order = sorted(range(len(En)), key=lambda i: (En[i], i))
    levels, lv = [], [0] * len(En)
    cur = [order[0]]
    for a, b in zip(order, order[1:]):
        if En[b] - En[a] <= tol_rel * sc:
            cur.append(b)
        else:
            levels.append(cur); cur = [b]
    levels.append(cur)
    out = []
    for k, mem in enumerate(levels):
        for s in mem:
            lv[s] = k
        out.append(dict(E_min=min(En[s] for s in mem), E_max=max(En[s] for s in mem), members=sorted(mem)))
    gaps = [out[k + 1]["E_min"] - out[k]["E_max"] for k in range(len(out) - 1)]
    return lv, out, (min(gaps) / sc if gaps else None), sc


def window_metrics(n, level_of, n_levels, surv, k):
    """Metrics for the window that admits exactly levels 0..k."""
    N0 = 1 << n
    SG = sum(surv)
    ST = [s for s in range(N0) if level_of[s] <= k]
    kept = sum(1 for s in ST if surv[s])
    fn = len(ST) - kept
    return dict(nominal=N0, grammar=SG, target=len(ST), surviving_targets=kept, false_exclusions=fn,
                preservation=kept / len(ST), contraction=1 - SG / N0, target_density=len(ST) / N0,
                grammar_target_density=kept / SG if SG else float("nan"),
                capacity_L_over_m=SG / len(ST), capacity_ok=(SG >= len(ST)) if fn == 0 else None)


# ---------------------------------------------------------------- constructive grammar enumeration
def constructive_enumerate(inc, n, vertex_order=None):
    """Backtracking generation of S_G (no energy). Returns (set_of_ids, nodes_visited). Islands are assigned in the order
    in which vertices become complete, and each completed vertex is tested immediately."""
    order_v = list(range(len(inc))) if vertex_order is None else list(vertex_order)
    assigned_order, seen = [], set()
    check_after = {}                       # position in assignment order -> vertex to check once assigned
    for v in order_v:
        for i, _ in inc[v]:
            if i not in seen:
                seen.add(i); assigned_order.append(i)
        check_after.setdefault(len(assigned_order) - 1, []).append(v)
    for i in range(n):
        if i not in seen:
            seen.add(i); assigned_order.append(i)
    masks = compile_masks(inc)
    found, nodes = [], [0]

    def rec(pos, state):
        if pos == len(assigned_order):
            found.append(state); return
        isl = assigned_order[pos]
        for bit in (0, 1):
            st = state | (bit << isl)
            nodes[0] += 1
            ok = True
            for v in check_after.get(pos, ()):
                im, nm = masks[v]
                if ((st ^ nm) & im).bit_count() != 2:
                    ok = False; break
            if ok:
                rec(pos + 1, st)
    rec(0, 0)
    return set(found), nodes[0]
