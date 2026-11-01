"""G2-A/B: geometry along SELECT-II histories of integer states.
Edge m --N--> m(N+1)^2/N ; coordinates q_p = floor(v_p/2).  Transport law (B2-T2): for p not dividing N,
q_p' = q_p + v_p(N+1); for p | N, q_p' = q_p - l_p with l_p = floor(n/2) (v_p(m) odd) or ceil(n/2) (v_p(m) even), n=v_p(N)."""
import _paths  # noqa
from collections import Counter
from functools import lru_cache
from geo_snapshots import qvec, vp, closed_form
from geo1lib import factor


def step(m, N):
    return None if m % N else m * (N + 1) ** 2 // N


def states(m, labels):
    out = [m]
    for N in labels:
        m = step(m, N)
        if m is None:
            return None
        out.append(m)
    return out


def edge_transport(m, N):
    """predicted dq_p for every prime p involved (dict p -> change in q_p); used to test the transport law."""
    ds = {}
    ps = set(factor(N)) | set(factor(N + 1))
    for p in ps:
        n, w = vp(N, p), vp(N + 1, p)
        if n:
            e = vp(m, p)
            ds[p] = -((n // 2) if e % 2 else (n + 1) // 2)
        else:
            ds[p] = w
    return ds


def gain_loss(m, labels):
    """per-prime accounting along a history: G_p = sum v_p(N_i+1) (gain content), Lambda_p = total loss, dq_p = net change,
    and the list of steps at which q_p strictly decreases.  Telescoping: dq_p = G_p - Lambda_p."""
    path = states(m, labels)
    assert path is not None
    primes = set()
    for s in path:
        primes |= set(qvec(s))
    for N in labels:
        primes |= set(factor(N + 1)) | set(factor(N))
    G = Counter(); Lam = Counter(); steps = {p: [] for p in primes}
    for i, N in enumerate(labels):
        a, b = qvec(path[i]), qvec(path[i + 1])
        for p in primes:
            dq = b.get(p, 0) - a.get(p, 0)
            if dq < 0:
                Lam[p] += -dq; steps[p].append(i)
        for p in factor(N + 1):
            G[p] += vp(N + 1, p)
    net = {p: qvec(path[-1]).get(p, 0) - qvec(path[0]).get(p, 0) for p in primes}
    return {'G': dict(G), 'Lambda': dict(Lam), 'net': net, 'loss_steps': steps, 'path': path,
            'balance_ok': all(net[p] == G.get(p, 0) - Lam.get(p, 0) for p in primes)}


def predicted_loss_steps(content, m, p):
    """Theorem B2-T4: if every label N in the content has v_p(N) <= 1, the number of steps at which q_p decreases is
    floor(c/2) (v_p(m) odd) or ceil(c/2) (v_p(m) even), c = number of labels divisible by p -- independent of the order."""
    if any(vp(N, p) > 1 for N in content):
        return None
    c = sum(1 for N in content if N % p == 0)
    return c // 2 if vp(m, p) % 2 else (c + 1) // 2


def arrangements(m, content):
    """all distinct admissible orderings of the multiset `content` from m, as (labels, states)."""
    cnt = Counter(content); out = []
    def rec(z, labs, path):
        if not any(cnt.values()):
            out.append((tuple(labs), tuple(path))); return
        for N in sorted(cnt):
            if cnt[N] == 0:
                continue
            t = step(z, N)
            if t is None:
                continue
            cnt[N] -= 1; rec(t, labs + [N], path + [t]); cnt[N] += 1
    rec(m, [], [m])
    return out


def ambient_profile(path):
    return [len(qvec(s)) for s in path]


def both_active(path, p=2, r=3):
    """does some state have q_p >= 1 and q_r >= 1 (the mixed index p*r is in D, so K contains the unit square)?"""
    return any(qvec(s).get(p, 0) >= 1 and qvec(s).get(r, 0) >= 1 for s in path)


@lru_cache(None)
def avoids_square(v2, v3, a, b):
    """exists an admissible completion (a labels 2, b labels 3 left) that never has v2>=2 and v3>=2?  (valuation DP on (v2,v3))"""
    if v2 >= 2 and v3 >= 2:
        return False
    if a == 0 and b == 0:
        return True
    if a > 0 and v2 >= 1 and avoids_square(v2 - 1, v3 + 2, a - 1, b):
        return True
    if b > 0 and v3 >= 1 and avoids_square(v2 + 4, v3 - 1, a, b - 1):
        return True
    return False


@lru_cache(None)
def feasible(v2, v3, a, b):
    if a == 0 and b == 0:
        return True
    return (a > 0 and v2 >= 1 and feasible(v2 - 1, v3 + 2, a - 1, b)) or (b > 0 and v3 >= 1 and feasible(v2 + 4, v3 - 1, a, b - 1))


def benchmark_B3():
    """the 4 -> 65536 pair: 1^7 versus (2,2,3,3,3,3): complete geometric trajectories (closed form + frozen engine)."""
    from geo_snapshots import state_record
    out = {}
    for name, labs in (('1^7', (1,) * 7), ('2,2,3,3,3,3', (2, 2, 3, 3, 3, 3))):
        path = states(4, labs)
        out[name] = {'labels': list(labs), 'states': path, 'records': [state_record(s) for s in path],
                     'gain_loss': {k: v for k, v in gain_loss(4, labs).items() if k != 'path'}}
    return out
