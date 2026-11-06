"""exact (Fraction) conditional entropy for a finite uniform ensemble; logs via the v001 decimal routine."""
from collections import Counter, defaultdict
from decimal import Decimal
from fractions import Fraction
import _vpath  # noqa: F401
from information import shannon, fmt


def H_counts(counts):
    t = sum(counts)
    return shannon([Fraction(c, t) for c in counts]) if t else Decimal(0)


def profile(samples):
    """samples: iterable of (y, signature) with uniform weight.  Returns dict with H(Y), H(Y|O), I, #classes, #mixed classes, #positives in mixed classes."""
    by = defaultdict(Counter)
    n = 0
    ycount = Counter()
    for y, s in samples:
        by[s][y] += 1
        ycount[y] += 1
        n += 1
    HY = H_counts(list(ycount.values()))
    HYO = Decimal(0)
    mixed = pos_mixed = 0
    for s, c in by.items():
        if len(c) > 1:
            mixed += 1
            pos_mixed += c[1]
            HYO += Decimal(sum(c.values())) / Decimal(n) * H_counts(list(c.values()))
    return {"size": n, "positives": ycount[1], "classes": len(by), "mixed_classes": mixed, "positives_in_mixed_classes": pos_mixed,
            "H(Y)": fmt(HY, 30), "H(Y|O)": fmt(HYO, 30), "I(Y;O)": fmt(HY - HYO, 30)}
