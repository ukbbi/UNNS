"""shared, in-process cache of the censuses used by several experiments."""
import _path  # noqa: F401
import realizability as rz

_CENSUS = {}
_CLASSES = {}


def census(k, L):
    if (k, L) not in _CENSUS:
        _CENSUS[(k, L)] = rz.census(k, L)
    return _CENSUS[(k, L)]


def classes(k, L):
    if (k, L) not in _CLASSES:
        found, _ = census(k, L)
        _CLASSES[(k, L)] = rz.iso_classes(found, k)
    return _CLASSES[(k, L)]
