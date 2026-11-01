"""HD-1D v004 builder: occurrence events along histories of possibly different lengths.
Comparison method that stays meaningful for unequal lengths: compare *event words* (per-step birth/loss counts, read in order), the multiset of
indices that ever occur, their survival intervals and reappearances -- never time-aligned signatures."""
from select_history import fibre


def states(m0, w):
    out = [m0]; m = m0
    for N in w:
        assert m % N == 0
        m = m // N * (N + 1) ** 2; out.append(m)
    return out


def fibre_sequence(m0, w): return [frozenset(fibre(m)) for m in states(m0, w)]


def event_word(m0, w):
    seq = fibre_sequence(m0, w)
    return tuple((len(seq[j] - seq[j - 1]), len(seq[j - 1] - seq[j])) for j in range(1, len(seq)))


def summary(m0, w):
    seq = fibre_sequence(m0, w); ev = event_word(m0, w)
    ds = set().union(*seq) if seq else set()
    reappear = 0; intervals = {}
    for d in ds:
        pat = [int(d in F) for F in seq]
        runs = sum(1 for j in range(len(pat)) if pat[j] and (j == 0 or not pat[j - 1]))
        if runs > 1: reappear += 1
        intervals[d] = runs
    return {"length": len(w), "births": sum(b for b, _ in ev), "losses": sum(l for _, l in ev), "event_word": ev,
            "distinct_indices": len(ds), "reappearing_indices": reappear, "max_fibre": max(len(F) for F in seq)}
