"""Standard-library exact graph / Fourier admissibility kernel for CIB-I."""
from fractions import Fraction
from math import pi, sin
from collections import Counter


def graph(name, limit):
    edges = []
    if name == 'SQUARE':
        for m in range(1, limit + 1):
            k = 2
            while k * k * m <= limit:
                edges.append((m, k*k*m, k))
                k += 1
    else:
        delta = {'UNNS':0, 'NEAR_MINUS':-1, 'NEAR_PLUS':1}[name]
        # Same N|m gate for all three admissible-grammar variants.
        for n in range(1, limit+1):
            t = 1
            while t*(n*n+(2+delta)*n+1) <= limit:
                m = n*t
                y = t*(n*n+(2+delta)*n+1)
                edges.append((m,y,n))
                t += 1
    return sorted(edges)


def unns_step(m,n):
    if n < 1 or m % n:
        return None
    return m//n*(n+1)**2


def q_shift(edge):
    return edge[1] - edge[0]


def dielectric_hat_power(q, duty):
    """|u_hat(q)|^2 for u=1_[0,2pi D]-D; q != 0."""
    assert q > 0
    return (sin(pi*q*float(duty)) / (pi*q))**2


def exact_nonzero(q, duty):
    # D reduced Fraction(a,b), q>0.
    return q % duty.denominator != 0


def scramble_sources(edges, limit):
    """Preserve every q, move source labels by a q-specific cyclic permutation."""
    shifted=[]
    for m,y,label in edges:
        q=y-m
        available=limit-q
        if available < 2:
            new_m=m
        else:
            shift=1+((7*q+11)%(available-1))
            new_m=1+((m-1+shift)%available)
        shifted.append((new_m,new_m+q,label))
    return sorted(shifted)


def profile_scores(edges,duty,limit):
    e=len(edges)
    nonzero=sum(exact_nonzero(q_shift(x),duty) for x in edges)
    mean_power=sum(dielectric_hat_power(q_shift(x),duty) for x in edges)/e if e else 0
    # All possible positive-index directed pairs in the same window.
    base_denom=limit*(limit-1)//2
    base_num=sum((limit-q) for q in range(1,limit) if exact_nonzero(q,duty))
    base=base_num/base_denom
    return {'edges':e,'nonzero_edges':nonzero,'nonzero_fraction':nonzero/e if e else None,
            'mean_fourier_power':mean_power,'background_nonzero_fraction':base,
            'enrichment':(nonzero/e)/base if e and base else None}


def diamond(duty):
    A=(6,28) # 2 -> 8 -> 36
    B=(7,27) # 2 -> 9 -> 36
    def hit(qs):return [exact_nonzero(q,duty) for q in qs]
    return {'duty':f'{duty.numerator}/{duty.denominator}', 'A_shifts':list(A),
            'A_first_order_edges':hit(A),'A_all_first_order':all(hit(A)),
            'B_shifts':list(B),'B_first_order_edges':hit(B),'B_all_first_order':all(hit(B))}
