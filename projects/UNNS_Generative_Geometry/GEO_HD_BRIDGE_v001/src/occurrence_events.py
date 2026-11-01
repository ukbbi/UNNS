"""HD-C3/C4: occurrence membership d in D(m) iff v_p(m) >= 2 a_p; incidence sequences, variation V_d, reduced event churn chi_d."""
from prime_geometry import factor, vp


def in_D(d, m):
    return d >= 2 and all(vp(m, p) >= 2 * a for p, a in factor(d).items())


def occ_set(m):
    """D(m): divisors >= 2 of s(m)"""
    divs = [1]
    for p, e in factor(m).items(): divs = [d * p ** i for d in divs for i in range(e // 2 + 1)]
    return sorted(d for d in divs if d >= 2)


def incidence(d, states): return [1 if in_D(d, m) else 0 for m in states]


def variation(rho): return sum(abs(rho[j] - rho[j - 1]) for j in range(1, len(rho)))


def churn(rho):
    V = variation(rho)
    assert (V - abs(rho[-1] - rho[0])) % 2 == 0
    return (V - abs(rho[-1] - rho[0])) // 2


def history_churn(d, m, w):
    st = [m]
    for N in w:
        m = m // N * (N + 1) ** 2; st.append(m)
    return churn(incidence(d, st))
