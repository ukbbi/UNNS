"""GIG-INFO v003 -- vectorised local geometry of the legal-swap graph of an arrangement set (rank-permutations of 6 labels, 720-bit mask).
d(w) degree, q(w) # commuting-swap squares through w, s(w)=sum_{u~w}(d(u)-1), |B2(w)| = 1 + d + s - q  (Theorem T1, proved in THEORY),  hexagons = braid faces.
All outputs are exact integers."""
import itertools
import numpy as np

K = 6
PERMS = list(itertools.permutations(range(K)))
IDX = {p: i for i, p in enumerate(PERMS)}
M = len(PERMS)
SW = np.array([[IDX[p[:j] + (p[j + 1], p[j]) + p[j + 2:]] for j in range(K - 1)] for p in PERMS], dtype=np.int32)  # SW[w,j]: swap positions j,j+1
PAIRS = [(j, l) for j in range(K - 1) for l in range(j + 2, K - 1)]
TRI = []  # hexagon: positions a..a+2 permuted
for a in range(K - 2):
    rows = []
    for p in PERMS:
        base = p[a:a + 3]
        rows.append([IDX[p[:a] + t + p[a + 3:]] for t in itertools.permutations(sorted(base))])
    TRI.append(np.array(rows, dtype=np.int32))
ASC = [np.array([p[a] < p[a + 1] < p[a + 2] for p in PERMS]) for a in range(K - 2)]


def unpack(masks):
    """list of python ints -> (R,720) bool"""
    nb = (M + 7) // 8
    raw = np.frombuffer(b"".join(m.to_bytes(nb, "little") for m in masks), dtype=np.uint8).reshape(len(masks), nb)
    return np.unpackbits(raw, axis=1, bitorder="little")[:, :M].astype(bool)


def features(masks):
    a = unpack(masks)
    R = a.shape[0]
    nbm = np.stack([a & a[:, SW[:, j]] for j in range(K - 1)], axis=2)  # (R,720,5): edge w--SW[w,j]
    d = nbm.sum(2).astype(np.int32)
    q = np.zeros((R, M), dtype=np.int32)
    for j, l in PAIRS:
        wj = SW[:, j]
        q += (nbm[:, :, j] & nbm[:, :, l] & a[:, SW[wj, l]]).astype(np.int32)
    s = np.zeros((R, M), dtype=np.int32)
    for j in range(K - 1):
        s += nbm[:, :, j] * (d[:, SW[:, j]] - 1)
    B2 = np.where(a, 1 + d + s - q, 0).astype(np.int32)
    hx = np.zeros(R, dtype=np.int64)
    for t in range(K - 2):
        full = a[:, TRI[t]].all(axis=2) & ASC[t][None, :]
        hx += full.sum(1)
    N = a.sum(1).astype(np.int64)
    dd, qq, bb = d.astype(np.int64), q.astype(np.int64), B2.astype(np.int64)
    out = dict(N=N, E=dd.sum(1) // 2, sq=qq.sum(1) // 4, hx=hx, Sd2=(dd ** 2).sum(1), Sd3=(dd ** 3).sum(1), Sq2=(qq ** 2).sum(1), SB2=bb.sum(1), SB22=(bb ** 2).sum(1),
               dmax=np.where(a, d, -1).max(1), dmin=np.where(a, d, 99).min(1), bmax=bb.max(1), bmin=np.where(a, B2, 999).min(1),
               Ss=(s.astype(np.int64)).sum(1), Ss2=(s.astype(np.int64) ** 2).sum(1), Sds=(dd * s).sum(1), Sdq=(dd * qq).sum(1), Ssq=(s.astype(np.int64) * qq).sum(1))
    # histograms
    out["hd"] = np.stack([(a & (d == v)).sum(1) for v in range(K)], axis=1).astype(np.int32)
    out["hq"] = np.stack([(a & (q == v)).sum(1) for v in range(11)], axis=1).astype(np.int32)
    bm = int(bb.max()) + 1
    out["hb"] = np.stack([(a & (B2 == v)).sum(1) for v in range(40)], axis=1).astype(np.int32)
    assert bm <= 40
    # joint (d,q) histogram: degree-correlation proxy
    out["hdq"] = np.stack([(a & (d == u) & (q == v)).sum(1) for u in range(K) for v in range(11)], axis=1).astype(np.int32)
    return out
