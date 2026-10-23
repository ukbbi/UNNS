import unittest
from fractions import Fraction
from src.relations import successor_separation, scalar_successor_well_defined, possible_increment_labels
from src.fibres import occurrences
from src.nest import value


class TestRelations(unittest.TestCase):
    def test_label_leakage_72(self):
        rec = successor_separation(72)
        self.assertEqual(rec['occurrences'],3)
        self.assertTrue(rec['successors_unique'])
        self.assertTrue(rec['label_recovery'])
        self.assertFalse(scalar_successor_well_defined(72))

    def test_label_leakage_rational(self):
        rec = successor_separation(Fraction(225,2))
        self.assertEqual(rec['occurrences'],3)
        self.assertTrue(rec['successors_unique'])
        self.assertTrue(rec['label_recovery'])
        self.assertFalse(scalar_successor_well_defined(Fraction(225,2)))

    def test_singleton_has_successor(self):
        self.assertTrue(scalar_successor_well_defined(4))
        self.assertEqual(possible_increment_labels(4),(Fraction(4),))

    def test_no_occurrences(self):
        self.assertTrue(scalar_successor_well_defined(1))
        self.assertEqual(possible_increment_labels(1),())

    def test_all_competing_nests_reconstructed(self):
        checked = 0
        for x in {value(M,N) for M in range(1,75) for N in range(1,30)}:
            if len(occurrences(x)) > 1:
                rec = successor_separation(x)
                self.assertTrue(rec['successors_unique'] and rec['label_recovery'])
                checked += 1
        self.assertGreater(checked, 0)
