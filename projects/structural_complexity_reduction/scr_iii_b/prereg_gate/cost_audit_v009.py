#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v009 -- cost accounting, timing protocol and the H-C uncertainty rule (PROPOSED, not frozen).

C_total = C_setup + C_generation + C_filter + C_energy + C_other, each operation charged exactly once.
Phase timers come from the solver binaries; the bucket mapping below is documentary (G2/B1/E2 interleave generation and incremental energy
inseparably) -- the compared quantity is the TOTAL charged wall time plus the operation counters.

Timing protocol (proposed): 1 thread, 3 warm-up rounds, 15 timed rounds, deterministic balanced interleaving (cyclic Latin-square rotation of the
solver order, round r rotated by r), median and dispersion.  H-C uncertainty: PAIRED per-round ratios t_B0/t_arm (common machine noise cancels
within a round), and a decision rule on the lower end of a 95% interval of the median/geometric-mean ratio.
"""
import math, statistics, subprocess, time
import numpy as np

BUCKETS = {
    "b0": dict(setup="t_preprocess_s", generation=None, filter=None, energy="t_traverse_s", other="t_finalize_s"),
    "g1": dict(setup="t_preprocess_s", generation=None, filter="t_grammar_s", energy="t_energy_s", other="t_finalize_s"),
    "g2": dict(setup="t_preprocess_s", generation="t_traverse_s", filter=None, energy=None, other="t_finalize_s"),
    "b1": dict(setup="t_preprocess_s", generation="t_traverse_s", filter=None, energy=None, other="t_finalize_s"),
    "e2": dict(setup="t_preprocess_s", generation=None, filter="t_traverse_s", energy=None, other="t_finalize_s"),
    "cert_b0": dict(setup="t_preprocess_s", generation=None, filter=None, energy="t_traverse_s", other="t_finalize_s"),
    "cert_b1": dict(setup="t_preprocess_s", generation="t_traverse_s", filter=None, energy=None, other="t_finalize_s"),
}
NUMERIC_KEYS = ["wall_s", "cpu_s", "t_preprocess_s", "t_traverse_s", "t_grammar_s", "t_energy_s", "t_finalize_s", "t_serialize_s", "t_read_input_s", "maxrss_kb",
                "states_visited", "nodes", "leaves", "grammar_checks", "vertex_checks", "full_energy_evals", "field_updates", "pair_ops", "bound_evals", "pruned",
                "materialized", "candidates_kept", "comparisons", "resyncs", "scan_certain_in", "scan_certain_out", "direct_fallbacks", "hp_evals",
                "unresolved_boundary", "cert_rejects", "cert_accepts", "e2_fallbacks", "z2_expansions", "ref_checks", "target_count"]


def parse_kv(text):
    return dict(l.split("=", 1) for l in text.splitlines() if "=" in l)


def numeric(kv):
    out = {}
    for k in NUMERIC_KEYS:
        if k in kv:
            out[k] = float(kv[k]) if ("." in kv[k] or "e" in kv[k].lower()) else int(kv[k])
    return out


def charged(solver, num):
    """Buckets and the charged total.  total = phases + serialisation + input parsing (+ unattributed remainder of the wall time)."""
    m = BUCKETS[solver]; b = {}
    for name, key in m.items():
        b[name] = num.get(key, 0.0) if key else 0.0
    b["other"] += num.get("t_serialize_s", 0.0)
    b["setup"] += num.get("t_read_input_s", 0.0)
    attributed = sum(b.values()) - num.get("t_read_input_s", 0.0) - num.get("t_serialize_s", 0.0)
    b["unattributed"] = max(0.0, num.get("wall_s", 0.0) - attributed)
    b["total_charged"] = sum(b.values())
    return b


def schedule(solvers, rounds):
    k = len(solvers)
    return [[solvers[(i + r) % k] for i in range(k)] for r in range(rounds)]


def run_protocol(run_fn, solvers, warmups=3, repeats=15):
    """run_fn(solver) -> (kv_dict, external_wall).  Warm-up rounds are executed and discarded."""
    rec = {s: [] for s in solvers}; order_log = []
    for r, order in enumerate(schedule(solvers, warmups + repeats)):
        for s in order:
            kv, ext = run_fn(s)
            if r >= warmups:
                num = numeric(kv); num["external_wall_s"] = ext; num["round"] = r - warmups
                rec[s].append(num)
        order_log.append(order)
    return rec, order_log


def disp(xs):
    xs = sorted(xs); med = statistics.median(xs)
    mad = statistics.median([abs(x - med) for x in xs])
    q = lambda p: xs[min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))]
    return dict(median=med, mad=mad, rel_mad=(mad / med if med else None), min=xs[0], max=xs[-1], q25=q(0.25), q75=q(0.75), rel_range=((xs[-1] - xs[0]) / med if med else None), n=len(xs))


# ---------------------------------------------------------------- H-C uncertainty rule
def hc_intervals(t_ref, t_arm, n_boot=10000, seed=20261010, block=3):
    """Paired rounds: ratio_r = t_ref[r]/t_arm[r].  Returns the median ratio with a percentile interval from a CIRCULAR MOVING-BLOCK bootstrap
    (block length 3 ~ R^(1/3); consecutive rounds are autocorrelated) and a log-scale Student-t interval for the geometric-mean ratio."""
    r = np.asarray(t_ref, float) / np.asarray(t_arm, float); R = len(r)
    rng = np.random.default_rng(seed); nb = -(-R // block)
    starts = rng.integers(0, R, size=(n_boot, nb))
    idx = ((starts[:, :, None] + np.arange(block)[None, None, :]) % R).reshape(n_boot, nb * block)[:, :R]
    meds = np.median(r[idx], axis=1)
    boot = (float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5)))
    lr = np.log(r); m = lr.mean(); se = lr.std(ddof=1) / math.sqrt(R)
    from math import exp
    tq = _t975(R - 1)
    tint = (exp(m - tq * se), exp(m + tq * se))
    return dict(median_ratio=float(np.median(r)), geo_mean_ratio=exp(m), bootstrap95=boot, t95=tint, rounds=R)


def _t975(df):
    table = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145,
             15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 24: 2.064, 29: 2.045, 30: 2.042}
    if df in table:
        return table[df]
    keys = sorted(table)
    for a, b in zip(keys, keys[1:]):
        if a < df < b:
            return table[a] + (table[b] - table[a]) * (df - a) / (b - a)
    return 1.96


def hc_decision(intervals, threshold=1.2, P_pass=False, output_complete_certified=False, which="bootstrap95"):
    """Decision table for H-C (proposed):  needs P PASS and certified complete output, else NOT_ELIGIBLE (conditional performance only).
    PASS if the lower end of the 95% interval >= threshold; FAIL if the upper end < threshold; otherwise INCONCLUSIVE."""
    if not (P_pass and output_complete_certified):
        return "NOT_ELIGIBLE_COMPLETE_TASK_NOT_CERTIFIED"
    lo, hi = intervals[which]
    if lo >= threshold:
        return "CHARGED_GAIN_PASS"
    if hi < threshold:
        return "CHARGED_GAIN_FAIL"
    return "CHARGED_GAIN_INCONCLUSIVE"


def coverage_simulation(true_ratios=(1.0, 1.1, 1.2, 1.5, 2.0), sims=600, rounds=15, n_boot=1000, sigma_common=0.15, sigma_ind=0.05, phi=0.3, seed=20261011, threshold=1.2):
    """Synthetic paired timings with a common per-round machine factor (cancels in the paired ratio) and AR(1)-correlated individual noise.
    Reports how often each interval contains the true ratio and how often the decision rule says PASS / FAIL (power / false-pass rates)."""
    rng = np.random.default_rng(seed); out = {}
    for rho in true_ratios:
        cov_b = cov_t = 0; dec = {"CHARGED_GAIN_PASS": 0, "CHARGED_GAIN_FAIL": 0, "CHARGED_GAIN_INCONCLUSIVE": 0}; dec_t = dict(dec)
        for _ in range(sims):
            common = np.exp(rng.normal(0, sigma_common, rounds))
            def ar():
                e = np.zeros(rounds); e[0] = rng.normal(0, sigma_ind)
                for i in range(1, rounds):
                    e[i] = phi * e[i - 1] + math.sqrt(1 - phi * phi) * rng.normal(0, sigma_ind)
                return np.exp(e)
            t_ref = 1.0 * common * ar(); t_arm = (1.0 / rho) * common * ar()
            iv = hc_intervals(t_ref, t_arm, n_boot=n_boot, seed=int(rng.integers(1, 2 ** 31)))
            cov_b += iv["bootstrap95"][0] <= rho <= iv["bootstrap95"][1]; cov_t += iv["t95"][0] <= rho <= iv["t95"][1]
            dec[hc_decision(iv, threshold, True, True, "bootstrap95")] += 1; dec_t[hc_decision(iv, threshold, True, True, "t95")] += 1
        out["%.2f" % rho] = dict(coverage_bootstrap=cov_b / sims, coverage_t_log=cov_t / sims, decisions_bootstrap={k: v / sims for k, v in dec.items()},
                                 decisions_t_log={k: v / sims for k, v in dec_t.items()})
    return out
