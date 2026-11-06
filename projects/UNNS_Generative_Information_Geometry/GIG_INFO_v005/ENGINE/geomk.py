"""GIG-INFO v003 -- the same local-geometry features for any number k of distinct labels (k=6 reproduces geom.py; k=7 used in the transfer test)."""
import itertools
import numpy as np


class Geom:
    def __init__(self, K):
        self.K = K
        self.PERMS = list(itertools.permutations(range(K)))
        self.IDX = {p: i for i, p in enumerate(self.PERMS)}
        self.M = len(self.PERMS)
        self.SW = np.array([[self.IDX[p[:j] + (p[j + 1], p[j]) + p[j + 2:]] for j in range(K - 1)] for p in self.PERMS], dtype=np.int32)
        self.PAIRS = [(j, l) for j in range(K - 1) for l in range(j + 2, K - 1)]
        self.TRI, self.ASC = [], []
        for a in range(K - 2):
            self.TRI.append(np.array([[self.IDX[p[:a] + t + p[a + 3:]] for t in itertools.permutations(sorted(p[a:a + 3]))] for p in self.PERMS], dtype=np.int32))
            self.ASC.append(np.array([p[a] < p[a + 1] < p[a + 2] for p in self.PERMS]))

    def unpack(self, masks):
        nb = (self.M + 7) // 8
        raw = np.frombuffer(b"".join(m.to_bytes(nb, "little") for m in masks), dtype=np.uint8).reshape(len(masks), nb)
        return np.unpackbits(raw, axis=1, bitorder="little")[:, :self.M].astype(bool)

    def features(self, masks):
        K, M, SW = self.K, self.M, self.SW
        a = self.unpack(masks)
        R = a.shape[0]
        nbm = np.stack([a & a[:, SW[:, j]] for j in range(K - 1)], axis=2)
        d = nbm.sum(2).astype(np.int32)
        q = np.zeros((R, M), dtype=np.int32)
        for j, l in self.PAIRS:
            q += (nbm[:, :, j] & nbm[:, :, l] & a[:, SW[SW[:, j], l]]).astype(np.int32)
        s = np.zeros((R, M), dtype=np.int32)
        for j in range(K - 1):
            s += nbm[:, :, j] * (d[:, SW[:, j]] - 1)
        B2 = np.where(a, 1 + d + s - q, 0).astype(np.int32)
        hx = np.zeros(R, dtype=np.int64)
        for t in range(K - 2):
            hx += (a[:, self.TRI[t]].all(axis=2) & self.ASC[t][None, :]).sum(1)
        dd, qq, bb = d.astype(np.int64), q.astype(np.int64), B2.astype(np.int64)
        out = dict(N=a.sum(1).astype(np.int64), E=dd.sum(1) // 2, sq=qq.sum(1) // 4, hx=hx, Sd2=(dd ** 2).sum(1), Sd3=(dd ** 3).sum(1), Sq2=(qq ** 2).sum(1), SB2=bb.sum(1), SB22=(bb ** 2).sum(1),
                   dmax=np.where(a, d, -1).max(1), dmin=np.where(a, d, 99).min(1), bmax=bb.max(1), bmin=np.where(a, B2, 999).min(1),
               Ss=(s.astype(np.int64)).sum(1), Ss2=(s.astype(np.int64) ** 2).sum(1), Sds=(dd * s).sum(1), Sdq=(dd * qq).sum(1), Ssq=(s.astype(np.int64) * qq).sum(1))
        out["hd"] = np.stack([(a & (d == v)).sum(1) for v in range(K)], axis=1).astype(np.int32)
        out["hq"] = np.stack([(a & (q == v)).sum(1) for v in range(len(self.PAIRS) + 1)], axis=1).astype(np.int32)
        nbmax = int(bb.max()) + 1
        out["hb"] = np.stack([(a & (B2 == v)).sum(1) for v in range(max(nbmax, 40))], axis=1).astype(np.int32)
        return out
