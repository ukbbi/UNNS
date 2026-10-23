"""Phase XVI nonlinear tau audit tests; scientific no-pass cannot be hidden."""
import json
import unittest
from pathlib import Path
import numpy as np
from src import xvi_tau_evolution_v001 as m
from src import xvi_projection_repair_v001 as repair


class TauEvolutionAuditV001(unittest.TestCase):
    def test_01_lock(self):
        self.assertTrue(m.source_lock()['pass'])

    def test_02_frozen_report_checksum(self):
        x=json.loads((m.ROOT/'config/XVI_TAU_LOCK_v001.json').read_text('utf-8'))
        self.assertEqual(m.sha(m.ROOT/x['inputs']['frozen_repair']['path']),
                         '875cdce0399a97a8a645c0df063d67bd1ff589bece3ee87c8415d976f9d95a6c')

    def test_03_original_source_unchanged(self):
        src=(m.ROOT/'docs/sources/XVI_ENGINE_v084.html').read_text('utf-8')
        for snippet in ('this.evolveField(field_idx);', 'this.applyClosure(field_idx);',
                        'this.computeFlux(field_idx);', 'tau[i] -= this.alpha_c * psi[i]'):
            self.assertIn(snippet,src)

    def test_04_frozen_js_witness(self):
        j=json.loads((m.ROOT/'output/XVI_TAU_JS_WITNESS_v001.json').read_text('utf-8'))
        self.assertTrue(j['all_pass']); self.assertEqual(len(j['results']),2)
        self.assertLess(max(x['relative_final_tau_error'] for x in j['results']),1e-10)
        self.assertEqual(j['source_sha256'],m.sha(m.ROOT/'docs/sources/XVI_ENGINE_v084.html'))

    def test_05_deterministic_init(self):
        a=m.init_tau(64,41)
        self.assertTrue(np.array_equal(a,m.init_tau(64,41)))
        self.assertFalse(np.array_equal(a,m.init_tau(64,137)))

    def test_06_consistent_initial_grid(self):
        a=m.init_tau(64,41);b=m.init_tau(128,41)
        self.assertLess(float(np.max(np.abs(a-b[::2,::2]))),1e-12)

    def test_07_first_step_is_evolution_only(self):
        z=m.init_tau(64,41)
        expected=z+0.1*np.sin(np.roll(z,-1,axis=1)-z)-2e-6*m.laplacian_source(z)
        out,c=m.step_tau(z,0,'original_emulation',m.DEFAULT)
        self.assertIsNone(c)
        self.assertLess(float(np.max(np.abs(expected-out))),1e-13)

    def test_08_closure_schedule(self):
        z=m.init_tau(64,41)
        self.assertIsNone(m.step_tau(z,5,'forward_volume',m.DEFAULT)[1])
        self.assertIsNotNone(m.step_tau(z,6,'forward_volume',m.DEFAULT)[1])

    def test_09_source_projection_failure_preserved(self):
        jx,jy=repair.source_flux(64,41)
        px,py,_=m.source_original_project(jx,jy)
        pre=m.rms(repair.divergence(jx,jy,'central_source'))
        post=m.rms(repair.divergence(px,py,'central_source'))
        self.assertGreater(post/pre,0.5)

    def test_10_matched_source_repair(self):
        jx,jy=repair.source_flux(64,41)
        px,py,_=m.p_flux(jx,jy,'central_source')
        self.assertLess(m.rms(repair.divergence(px,py,'central_source')),1e-12)

    def test_11_finite_volume_repair(self):
        jx,jy=repair.source_flux(64,41)
        px,py,_=m.p_flux(jx,jy,'forward_volume')
        self.assertLess(m.rms(repair.divergence(px,py,'forward_volume')),1e-12)

    def test_12_composite_closure_finite(self):
        r=m.run_case(64,41,'forward_volume',params={'steps':24})
        self.assertEqual(r['status'],'FINITE_WINDOW_COMPLETED')
        self.assertEqual(r['closures_observed'],3)

    def test_13_random_stress_finite_smoke(self):
        r=m.run_case(64,137,'central_source',corpus='random',params={'steps':24})
        self.assertEqual(r['status'],'FINITE_WINDOW_COMPLETED')

    def test_14_noise_not_silently_enabled(self):
        with self.assertRaises(ValueError):
            m.run_case(64,41,'forward_volume',params={'steps':10,'sigma':0.02})

    def test_15_zero_field_fixed_for_one_step(self):
        z=np.zeros((64,64))
        for method in m.METHODS:
            a,_=m.step_tau(z,6,method,m.DEFAULT)
            self.assertTrue(np.all(a==0))

    def test_16_precomputed_scientific_verdict_not_faked(self):
        report=json.loads((m.ROOT/'output/XVI_TAU_EVOLUTION_v001.json').read_text('utf-8'))
        self.assertEqual(report['primary_verdict'],'FULL_TAU_CERTIFICATION_NOT_ESTABLISHED')
        self.assertEqual(report['gates']['T7_born_rule'],'NOT_DERIVED')
        self.assertNotEqual(report['gates']['T2_repaired_flux_each_closure'],'PASS_TESTED')

    def test_17_grid_cauchy_fail_preserved(self):
        report=json.loads((m.ROOT/'output/XVI_TAU_EVOLUTION_v001.json').read_text('utf-8'))
        self.assertEqual(report['gates']['T4_grid_refinement'],'FAIL_OR_NONCONVERGENT')


if __name__=='__main__': unittest.main()
