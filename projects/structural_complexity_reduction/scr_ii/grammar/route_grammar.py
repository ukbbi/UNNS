from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterable, Mapping, Sequence, Tuple

ALPHABET = ("A", "B", "C", "D")
DEFAULT_TRANSITIONS = {
    "A": ("A", "B"),
    "B": ("B", "C"),
    "C": ("A", "D"),
    "D": ("C", "D"),
}
PHASE_MODULUS = 3

@dataclass(frozen=True)
class StructuralState:
    symbol: str
    phase: int
    last_discontinuities: Tuple[int, ...] = ()

def initial_state(instance: Mapping) -> StructuralState:
    return StructuralState(
        symbol=str(instance["initial_symbol"]),
        phase=int(instance["initial_phase"]),
        last_discontinuities=(),
    )

def phase_ok(prev: int, nxt: int) -> bool:
    return ((nxt - prev) % PHASE_MODULUS) in (0, 1)

def persistence_ok(history: Sequence[int], new_flag: int) -> bool:
    window = tuple(history[-3:]) + (int(new_flag),)
    return sum(window) <= 1

def advance_state(state: StructuralState, option: Mapping) -> StructuralState:
    hist = (state.last_discontinuities + (int(option["discontinuity"]),))[-3:]
    return StructuralState(str(option["symbol"]), int(option["phase"]), hist)

@lru_cache(maxsize=None)
def _abstract_reachable(symbol: str, phase: int, history: Tuple[int, ...], remaining: int,
                        transition_key: Tuple[Tuple[str, Tuple[str, ...]], ...]) -> bool:
    # The frozen v001 preregistration does not name a restricted terminal structural subset.
    # Therefore every structurally valid terminal state is accepting.
    if remaining <= 0:
        return True
    transitions = dict(transition_key)
    for ns in transitions.get(symbol, ()):
        for delta in (0, 1):
            np = (phase + delta) % 3
            for disc in (0, 1):
                if not persistence_ok(history, disc):
                    continue
                nh = (history + (disc,))[-3:]
                if _abstract_reachable(ns, np, nh, remaining - 1, transition_key):
                    return True
    return False

def suffix_reachable(state: StructuralState, remaining_depth: int,
                     transitions: Mapping[str, Iterable[str]] | None = None) -> bool:
    tr = transitions or DEFAULT_TRANSITIONS
    key = tuple(sorted((k, tuple(v)) for k, v in tr.items()))
    return _abstract_reachable(state.symbol, state.phase, state.last_discontinuities, int(remaining_depth), key)

def evaluate_gates(state: StructuralState, option: Mapping, remaining_depth: int,
                   transitions: Mapping[str, Iterable[str]] | None = None):
    tr = transitions or DEFAULT_TRANSITIONS
    gates = {}
    gates["G1"] = str(option["symbol"]) in tuple(tr.get(state.symbol, ()))
    if not gates["G1"]:
        return False, "G1", gates, None

    gates["G2"] = phase_ok(state.phase, int(option["phase"]))
    if not gates["G2"]:
        return False, "G2", gates, None

    proposed = advance_state(state, option)
    gates["G3"] = suffix_reachable(proposed, remaining_depth, tr)
    if not gates["G3"]:
        return False, "G3", gates, None

    gates["G4"] = persistence_ok(state.last_discontinuities, int(option["discontinuity"]))
    if not gates["G4"]:
        return False, "G4", gates, None

    return True, None, gates, proposed
