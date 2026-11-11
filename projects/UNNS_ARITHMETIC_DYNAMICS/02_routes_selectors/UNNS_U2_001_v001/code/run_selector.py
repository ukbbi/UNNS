import sys
from u2_selector import *
from u1_bnd_lib import fwd, inv, is_edge
def run(K):
    x, q, steps = 1, READY, 0
    nxt = 2; maxlen = 0; cur = 0
    seen_ready = []
    while nxt <= K + 1:
        s, N, q2 = sigma(x, q)
        y = fwd(x, N) if s == "+" else inv(x, N)   # raises if illegal
        assert is_edge(x, y)
        x, q = y, q2; steps += 1; cur += 1
        if q == READY:
            assert x == nxt, (x, nxt)
            maxlen = max(maxlen, cur); cur = 0; nxt += 1
    return steps, maxlen
if __name__ == "__main__":
    K = int(sys.argv[1])
    print(run(K))
