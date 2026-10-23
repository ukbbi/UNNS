"""Independent joint-route grammar; does not import quantum states or Born probabilities.

Mathematical status: constructive representation, NOT a uniquely derived physical law.
"""
from __future__ import annotations
from math import isfinite
from typing import Callable

KERNEL = Callable[[float, float], float]
OUTCOMES = (-1, 1)


def parity_stationary(c: float) -> dict[int, float]:
    if not isfinite(c) or not (-1 <= c <= 1):
        raise ValueError('correlation parameter must be finite and in [-1,1]')
    return {s: (1 + s*c)/2 for s in OUTCOMES}


def parity_transition(old_z: int, new_z: int, c: float, refresh: float) -> float:
    if old_z not in OUTCOMES or new_z not in OUTCOMES:
        raise ValueError('parity must be ±1')
    if not isfinite(refresh) or not (0 < refresh <= 1):
        raise ValueError('refresh must satisfy 0<r<=1')
    return (1-refresh)*float(old_z == new_z) + refresh * parity_stationary(c)[new_z]


def evolve_parity(initial: dict[int,float], c: float, refresh: float, steps: int) -> dict[int,float]:
    if steps < 0 or not isinstance(steps,int):
        raise ValueError('steps must be a nonnegative integer')
    if any(s not in initial for s in OUTCOMES) or any(initial[s] < 0 for s in OUTCOMES) or abs(sum(initial.values())-1)>1e-12:
        raise ValueError('invalid initial parity distribution')
    result=dict(initial)
    for _ in range(steps):
        result={new:sum(result[old]*parity_transition(old,new,c,refresh) for old in OUTCOMES) for new in OUTCOMES}
    return result


def joint_probabilities(a:float,b:float,kernel:KERNEL)->dict[tuple[int,int],float]:
    """Draw common unbiased g, parity z from the stationary kernel; A=g and B=gz."""
    c=kernel(a,b)
    pi=parity_stationary(c)
    return {(A,B):0.5*pi[A*B] for A in OUTCOMES for B in OUTCOMES}


def expectation(p:dict[tuple[int,int],float])->float:
    return sum(A*B*prob for (A,B),prob in p.items())


def marginals(p:dict[tuple[int,int],float]):
    return ({A:sum(p[(A,B)] for B in OUTCOMES) for A in OUTCOMES},
            {B:sum(p[(A,B)] for A in OUTCOMES) for B in OUTCOMES})


def chsh(kernel:KERNEL, a:float, ap:float, b:float, bp:float)->float:
    return (expectation(joint_probabilities(a,b,kernel))+
            expectation(joint_probabilities(a,bp,kernel))+
            expectation(joint_probabilities(ap,b,kernel))-
            expectation(joint_probabilities(ap,bp,kernel)))
