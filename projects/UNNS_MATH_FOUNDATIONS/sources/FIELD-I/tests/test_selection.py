import unittest
from itertools import product
from src.nest import value, next_occurrence
from src.selection import joint_low, joint_high, joint_covariant, nonselection_witness


class TestSelection(unittest.TestCase):
    def test_witness_distinct(self):
        w=nonselection_witness()
        self.assertEqual(w['input_value'],'225/2')
        self.assertNotEqual(w['low']['route'],w['high']['route'])
        self.assertNotEqual(w['low']['value'],w['high']['value'])

    def test_commutativity(self):
        B=list(product(range(1,8),range(1,6)))
        for op in (joint_low,joint_high):
            for a in B:
                for b in B:
                    self.assertEqual(op(a,b),op(b,a))

    def test_associativity(self):
        B=list(product(range(1,5),range(1,5)))
        for op in (joint_low,joint_high):
            for a in B:
                for b in B:
                    for c in B:
                        self.assertEqual(op(op(a,b),c),op(a,op(b,c)))

    def test_idempotence(self):
        for op in (joint_low,joint_high):
            for a in product(range(1,30),range(1,20)):
                self.assertEqual(op(a,a),a)

    def test_joint_unary_covariance(self):
        for op in (joint_low,joint_high):
            for a in product(range(1,16),range(1,10)):
                for b in [(1,1),(3,2),(10,5),(15,8)]:
                    self.assertTrue(joint_covariant(op,a,b))

    def test_same_nest_agreement(self):
        for op in (joint_low,joint_high):
            for N in range(1,15):
                for M in range(1,20):
                    for Mp in range(1,10):
                        self.assertEqual(op((M,N),(Mp,N)),(max(M,Mp),N))

    def test_not_selected_by_labelled_successor(self):
        a,b=(25,2),(18,4)
        self.assertEqual(value(*a),value(*b))
        self.assertNotEqual(joint_low(a,b),joint_high(a,b))

    def test_invalid_occurrence(self):
        for op in (joint_low,joint_high):
            with self.assertRaises(ValueError): op((0,2),(1,2))
