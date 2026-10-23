"""Adversarial witnesses: unary fixed-nest generation underdetermines binary joins."""
from .nest import positive, next_occurrence, value


def _validate(r: tuple[int, int]) -> None:
    if not isinstance(r, tuple) or len(r) != 2:
        raise ValueError('an occurrence must be a pair (M,N)')
    positive(r[0], 'M'); positive(r[1], 'N')


def joint_low(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    """One additional, explicitly proposed binary operation (not derived)."""
    _validate(a); _validate(b)
    return max(a[0], b[0]), min(a[1], b[1])


def joint_high(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    """A distinct proposed operation satisfying the same specified unary axioms."""
    _validate(a); _validate(b)
    return max(a[0], b[0]), max(a[1], b[1])


def joint_covariant(op, a, b) -> bool:
    """Simultaneous unary successor covariance: J(Ua,Ub)=U(J(a,b))."""
    return op(next_occurrence(*a), next_occurrence(*b)) == next_occurrence(*op(a, b))


def nonselection_witness() -> dict:
    a, b = (25, 2), (18, 4)  # both generate 225/2
    x = value(*a)
    low, high = joint_low(a, b), joint_high(a, b)
    return {
        'input_value': str(x), 'inputs': [list(a), list(b)],
        'low': {'route': list(low), 'value': str(value(*low))},
        'high': {'route': list(high), 'value': str(value(*high))},
        'status': 'constructive nonselection under CAI, same-nest agreement and simultaneous U-covariance',
    }
