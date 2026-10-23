import json
import hashlib
import math
import unittest
from pathlib import Path

from src.gct_joint_core_v002 import (parity_stationary,parity_transition,evolve_parity,
     joint_probabilities,expectation,marginals,chsh)
from src.gct_countermodels_v002 import local_shared_route,saturated_joint_route
from src.gct_quantum_comparator_v002 import singlet_reference
from src.gct_joint_origin_v002 import freeze_check,main

KERNELS=(local_shared_route,singlet_reference,saturated_joint_route)
SETTINGS=(0.,math.pi/2,math.pi/4,-math.pi/4)

class GCTJointV002(unittest.TestCase):
    def test_01_frozen_v001_checksums(self):
        self.assertTrue(freeze_check()['all_pass'])

    def test_02_probability_normalization_and_nonnegative(self):
        for f in KERNELS:
            for a in (0.,.2,1.4,math.pi):
                for b in (-.4,0.,.7,2.2):
                    p=joint_probabilities(a,b,f)
                    self.assertAlmostEqual(sum(p.values()),1.,places=12)
                    self.assertTrue(all(0<=v<=1 for v in p.values()))

    def test_03_flip_symmetry(self):
        for f in KERNELS:
            p=joint_probabilities(.2,1.7,f)
            self.assertAlmostEqual(p[(1,1)],p[(-1,-1)],places=12)
            self.assertAlmostEqual(p[(1,-1)],p[(-1,1)],places=12)

    def test_04_no_signalling_marginals(self):
        for f in KERNELS:
            for a in (0.,.4,2.4):
                for b in (0.,1.2,1.9):
                    pa,pb=marginals(joint_probabilities(a,b,f))
                    for m in (*pa.values(),*pb.values()): self.assertAlmostEqual(m,.5,places=12)

    def test_05_covariance_under_common_rotation(self):
        for f in KERNELS:
            c1=expectation(joint_probabilities(.1,.4,f))
            c2=expectation(joint_probabilities(1.1,1.4,f))
            self.assertAlmostEqual(c1,c2,places=12)

    def test_06_swap_symmetry(self):
        for f in KERNELS:
            self.assertAlmostEqual(f(.37,1.22),f(1.22,.37),places=12)

    def test_07_aligned_anticorrelation(self):
        for f in KERNELS:
            self.assertAlmostEqual(f(.31,.31),-1.,places=12)
            p=joint_probabilities(.31,.31,f)
            self.assertAlmostEqual(p[(1,1)]+p[(-1,-1)],0.,places=12)

    def test_08_axis_reversal(self):
        for f in KERNELS:
            self.assertAlmostEqual(f(.31+math.pi,.8),-f(.31,.8),places=12)

    def test_09_triangle_local_bound(self):
        self.assertAlmostEqual(chsh(local_shared_route,*SETTINGS),-2.,places=12)

    def test_10_reference_tsirelson(self):
        self.assertAlmostEqual(abs(chsh(singlet_reference,*SETTINGS)),2*math.sqrt(2),places=12)

    def test_11_smooth_superquantum(self):
        s=abs(chsh(saturated_joint_route,*SETTINGS))
        self.assertGreater(s,2*math.sqrt(2))
        self.assertLess(s,4.)
        self.assertAlmostEqual(s,3.998397592390445,places=11)

    def test_12_generic_support_identical(self):
        supports=[]
        for f in KERNELS:
            p=joint_probabilities(0.,math.pi/8,f)
            supports.append(set(k for k,v in p.items() if v>1e-12))
        self.assertTrue(all(s==supports[0] for s in supports))
        self.assertEqual(len(supports[0]),4)

    def test_13_nonunique_weights_same_support(self):
        ps=[joint_probabilities(0.,math.pi/8,f)[(1,1)] for f in KERNELS]
        self.assertGreater(max(ps)-min(ps),.1/4)

    def test_14_stationary_parity_invariant(self):
        for c in (-1.,-.5,0.,.7,1.):
            pi=parity_stationary(c)
            for s in (-1,1):
                new=sum(pi[z]*parity_transition(z,s,c,.3) for z in (-1,1))
                self.assertAlmostEqual(new,pi[s],places=12)

    def test_15_stationary_attracting(self):
        pi=parity_stationary(-.6)
        p=evolve_parity({-1:1.,1:0.},-.6,.3,100)
        for s in (-1,1):self.assertAlmostEqual(p[s],pi[s],places=12)

    def test_16_exact_contraction(self):
        c=-.3; r=.2
        pi=parity_stationary(c)
        p0={-1:1.,1:0.}
        p5=evolve_parity(p0,c,r,5)
        for s in (-1,1):
            self.assertAlmostEqual(p5[s]-pi[s],(1-r)**5*(p0[s]-pi[s]),places=12)

    def test_17_invalid_kernel_rejected(self):
        for c in (-1.1,1.1,float('nan')):
            with self.assertRaises(ValueError): parity_stationary(c)

    def test_18_invalid_refresh_rejected(self):
        with self.assertRaises(ValueError):parity_transition(1,1,0.,0.)
        with self.assertRaises(ValueError):parity_transition(1,1,0.,1.1)

    def test_19_nontrivial_recursion_not_forced_singlet(self):
        # A shared route and an attractive stationary law do not select c_Q.
        c_l=local_shared_route(0.,math.pi/8)
        c_q=singlet_reference(0.,math.pi/8)
        self.assertNotAlmostEqual(c_l,c_q,places=4)

    def test_20_report_does_not_claim_born_rule(self):
        data=main()
        self.assertEqual(data['scientific_verdict'],'UNDERDETERMINED_NONLOCAL_GENERATIVE_RULE')
        self.assertEqual(data['gates']['J8'],'NOT_DERIVED_BORN_RULE')
        self.assertEqual(data['previous_v001']['verdict'],'NO_GO_WITH_LOCAL_FACTORIZATION')

if __name__=='__main__':unittest.main()
