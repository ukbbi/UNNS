import hashlib
import math
import unittest

import numpy as np

from src import xvi_projection_repair_v001 as mod


class ProjectionRepairV001(unittest.TestCase):
    def test_locked_inputs(self):
        self.assertTrue(mod.source_lock()['all_pass'])

    def test_source_divergence_is_exactly_reproduced(self):
        for n in (64, 128, 256):
            jx,jy=mod.source_flux(n,41)
            spatial=mod.central_divergence_spatial(jx,jy)
            spectral=mod.divergence(jx,jy,'central_source')
            self.assertLess(mod.rms(spatial-spectral)/(mod.rms(spatial)+1e-30),1e-11)

    def test_matched_central_projection(self):
        for n in mod.N_LIST:
            for seed in mod.SEED_LIST:
                with self.subTest(n=n,seed=seed):
                    self.assertTrue(mod.certify_case(n,seed,'central_source')['pass'])

    def test_matched_finite_volume_projection(self):
        for n in mod.N_LIST:
            for seed in mod.SEED_LIST:
                with self.subTest(n=n,seed=seed):
                    self.assertTrue(mod.certify_case(n,seed,'forward_volume')['pass'])

    def test_adjoint_and_energy_orthogonality(self):
        for kind in ('central_source','forward_volume'):
            self.assertLess(mod.adjoint_defect(64,kind,41),1e-11)
            result=mod.certify_case(64,137,kind)
            self.assertLess(result['orthogonality_relative'],1e-11)
            self.assertLess(result['energy_identity_relative'],1e-11)

    def test_source_nullspace_is_finite_difference_nullspace(self):
        item=mod.nyquist_test()
        self.assertLess(item['central_divergence'],1e-12)
        self.assertLess(item['central_preserves_invisible_checkerboard'],1e-12)
        self.assertGreater(item['forward_divergence'],1.)
        self.assertLess(item['forward_removes_checkerboard'],1e-12)

    def test_repair_does_not_change_constants(self):
        for kind in ('central_source','forward_volume'):
            x=np.full((64,64),2.1);y=np.full((64,64),-3.7)
            px,py,_=mod.project(x,y,kind)
            self.assertLess(mod.vnorm(px-x,py-y),1e-12)

    def test_zero_field_is_fixed(self):
        for kind in ('central_source','forward_volume'):
            x=np.zeros((64,64));px,py,pot=mod.project(x,x,kind)
            self.assertEqual(mod.vnorm(px,py),0)
            self.assertEqual(mod.rms(pot),0)

    def test_grid_refinement_to_spectral_low_mode_reference(self):
        e=[mod.continuum_grid_error(n) for n in mod.N_LIST]
        self.assertTrue(e[0]>e[1]>e[2])
        self.assertLess(e[-1],0.001)
        self.assertGreater(e[0]/e[1],3)

    def test_unmodified_early_bridge_retains_failure(self):
        x=mod.ROOT/'docs/frozen/XVI_CANONICAL_BRIDGE_v001.json'
        d=__import__('json').loads(x.read_text())
        self.assertEqual(d['primary_verdict'],'CANONICAL_IMPLEMENTATION_OBSTRUCTION')
        self.assertEqual(d['gates']['B6'],'NOT_DERIVED_BORN_RULE')
        self.assertGreater(d['fourier_mode_analytic'][0]['original_divergence_ratio_after_before'],0.9)

    def test_same_mode_direct_original_js_vs_candidate(self):
        for item in mod.single_mode_original_vs_repair():
            self.assertTrue(item['pass'])
            self.assertGreater(item['original_js_residual'],0.9)
            self.assertLess(item['candidate_residual'],1e-10)

    def test_nonuniqueness_of_measure_from_projector(self):
        c=mod.measure_counterexample()
        self.assertLess(c['projected_invariance_relative'],1e-12)
        self.assertAlmostEqual(c['orthogonality_uv'],0)
        self.assertAlmostEqual(c['outcome_weights']['1']['A'],3/7)
        self.assertAlmostEqual(c['outcome_weights']['2']['A'],0.36)
        self.assertGreater(abs(c['outcome_weights']['1']['A']-c['outcome_weights']['2']['A']),0.01)

    def test_input_validation(self):
        with self.assertRaises(ValueError):mod.project(np.ones((3,4)),np.ones((3,4)))
        with self.assertRaises(ValueError):mod.project(np.ones((7,7)),np.ones((7,7)))
        with self.assertRaises(ValueError):mod.project(np.full((64,64),np.nan),np.zeros((64,64)))
        with self.assertRaises(ValueError):mod.project(np.ones((64,64)),np.ones((64,64)),'unknown')

    def test_report_gates_match_scope(self):
        r=mod.build_report()
        for key in ('L0','L1','L2','L3','L4','L5'):
            self.assertTrue(r['gates'][key].startswith(('PASS','NO_GO')))
        self.assertEqual(r['gates']['L6'],'UNPROVED_OBSERVABLE_EVENT_BRIDGE')
        self.assertEqual(r['gates']['L7'],'UNTESTED_FULL_TAU_EVOLUTION')
        self.assertEqual(r['born_rule'],'NOT_DERIVED')
        self.assertFalse(r['original_html_modified'])


if __name__=='__main__':unittest.main()
