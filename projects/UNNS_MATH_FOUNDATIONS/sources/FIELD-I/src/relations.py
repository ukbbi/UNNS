"""Separation-vs-label-leakage controls for original fixed-nest dynamics."""
from fractions import Fraction
from .fibres import occurrences
from .successor import next_options, reconstruct_consecutive
from .nest import index_number


def successor_separation(x: Fraction) -> dict:
    """All pairwise distinct next values are equivalent to distinct nest labels."""
    opts = next_options(x)
    return {
        'value': str(Fraction(x)),
        'occurrences': len(opts),
        'successors_unique': len({y for _, y in opts}) == len(opts),
        'label_recovery': all(reconstruct_consecutive(Fraction(x), y) == occ for occ, y in opts),
        'explanation': 'next-current is index_number(N), an injective encoding of the already-present N label',
    }


def scalar_successor_well_defined(x: Fraction) -> bool:
    """Whether a function of x alone can match every fixed-nest next value."""
    return len({y for _, y in next_options(x)}) <= 1


def possible_increment_labels(x: Fraction) -> tuple[Fraction, ...]:
    return tuple(sorted({index_number(N) for _, N in occurrences(x)}))
