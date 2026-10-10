import unittest, sys
from pathlib import Path
SCRII=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRII))
from nulls.controls import frozen_symbol_permutations, frozen_transition_permutations, permuted_transitions
from grammar.route_grammar import DEFAULT_TRANSITIONS

class NullTests(unittest.TestCase):
    def test_fixed_counts(self):
        self.assertEqual(len(frozen_symbol_permutations()),12)
        self.assertEqual(len(frozen_transition_permutations()),12)

    def test_transition_outdegree_preserved(self):
        for m in frozen_transition_permutations():
            tr=permuted_transitions(m)
            self.assertEqual({k:len(v) for k,v in tr.items()},{k:len(v) for k,v in DEFAULT_TRANSITIONS.items()})
