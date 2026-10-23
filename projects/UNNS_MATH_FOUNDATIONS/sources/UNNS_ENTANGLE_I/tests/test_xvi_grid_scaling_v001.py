"""Program integrity and finite candidate diagnostics; not a Born or physical theorem."""
from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
from src import xvi_grid_scaling_v001 as m
from src import xvi_tau_evolution_v001 as tau

class GridScalingAuditV001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=m.build_report()

    def test_01_uploaded_tau_bytes_locked(self):
        x=m.baseline_lock()
        self.assertTrue(x['pass'])
        self.assertEqual(x['frozen_primary_verdict'],'FULL_TAU_CERTIFICATION_NOT_ESTABLISHED')
        self.assertEqual(x['checks']['uploaded_tau']['actual_sha256'],
           '8ed0d7afcdaba90cddcd5a51e8468f09c60dd634d85d7cc41048ef25986caab9')

    def test_02_original_html_unmodified(self):
        x=m.baseline_lock()
        self.assertTrue(x['checks']['canonical_html']['pass'])

    def test_03_previous_failure_not_relabelled(self):
        r=self.r
        self.assertEqual(r['old_T4_remains'],'FAIL_OR_NONCONVERGENT')
        self.assertEqual(r['old_full_tau_verdict'],'FULL_TAU_CERTIFICATION_NOT_ESTABLISHED')
        self.assertEqual(r['original_negative_gates']['T2_repaired_flux_each_closure'],'FAIL')
        self.assertEqual(r['original_negative_gates']['T4_grid_refinement'],'FAIL_OR_NONCONVERGENT')
        self.assertFalse(r['full_canonical_tau_certified'])

    def test_04_tampered_baseline_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for x in ('config/XVI_GRID_LOCK_v001.json','docs/frozen/XVI_TAU_EVOLUTION_v001.json',
                      'docs/sources/XVI_ENGINE_v084.html','docs/frozen/XVI_PROJECTION_REPAIR_v001.json'):
                dest=root/x;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((m.ROOT/x).read_bytes())
            self.assertTrue(m.baseline_lock(root)['pass'])
            with (root/'docs/frozen/XVI_TAU_EVOLUTION_v001.json').open('ab') as f: f.write(b'\n')
            self.assertFalse(m.baseline_lock(root)['pass'])

    def test_05_grid_geometry_ratios(self):
        for r in self.r['physical_geometry_audit']:
            self.assertAlmostEqual(r['source_to_physical_center_gradient_ratio'],2*np.pi/r['N'],places=14)
            self.assertAlmostEqual(r['continuum_dx']*r['N'],2*np.pi,places=12)

    def test_06_fixed_physical_time_with_grid_cfl(self):
        for row in self.r['physical_candidate_runs']:
            self.assertAlmostEqual(row['final_physical_time'],m.CANDIDATE['T'],places=12)
            self.assertAlmostEqual(row['dt']*row['steps'],m.CANDIDATE['T'],places=12)
        s41=[r for r in self.r['physical_candidate_runs'] if r['seed']==41]
        self.assertEqual([r['N'] for r in s41],[64,128,256])
        self.assertGreater(s41[2]['steps'],s41[1]['steps'])

    def test_07_candidate_projection_reliability(self):
        for row in self.r['physical_candidate_runs']:
            w=row['max_projector_residuals']
            self.assertLess(w['post_rel'],1e-10)
            self.assertLess(w['scaled_idempotence'],1e-10)
            self.assertLess(w['energy_rel'],1e-10)
            self.assertEqual(row['status'],'COMPLETED')

    def test_08_coupled_grid_space_time_cauchy(self):
        for d in self.r['physical_grid_cauchy']:
            self.assertTrue(d['decreasing'])
            self.assertLess(d['error_128_to_256'],.1)

    def test_09_fixed_dt_spatial_mesh_control(self):
        for d in self.r['fixed_dt_mesh_cauchy']:
            self.assertTrue(d['decreasing'])
            self.assertEqual(d['steps'],100)
            self.assertLess(d['error_128_to_256'],.1)

    def test_10_temporal_refinement_independent(self):
        for d in self.r['timestep_refinement']:
            self.assertAlmostEqual(d['dt']/d['half_dt'],2.,places=12)
            self.assertLess(d['field_rel_error'],.01)

    def test_11_retains_nontrivial_spatial_structure(self):
        for row in self.r['physical_candidate_runs']:
            self.assertGreater(row['std_retention'],.65)
            self.assertGreater(row['final']['low_mode_power_fraction'],.8)

    def test_12_closure_ablation_not_inert(self):
        self.assertGreater(self.r['nontrivial_closure_ablation']['field_rel_difference'],.001)

    def test_13_near_zero_relative_metric_flag(self):
        samples=self.r['conditioning']
        self.assertEqual([x['relative_interpretable'] for x in samples],[True,True,False,False])
        self.assertTrue(all(np.isfinite(x['absolute_P2_P_residual']) for x in samples))

    def test_14_forbid_invalid_resolution(self):
        with self.assertRaises(ValueError): m.run_candidate(127,41)

    def test_15_new_result_never_claims_canonical_or_born(self):
        self.assertEqual(self.r['born_rule'],'NOT_DERIVED')
        self.assertFalse(self.r['full_canonical_tau_certified'])
        self.assertIn('OPEN',self.r['gates']['S6'])
        self.assertEqual(self.r['gates']['S7'],'NOT_DERIVED_OBSERVABLE_MEASURE')

    def test_16_reproducible_seed_small_grid(self):
        a=m.run_candidate(64,41);b=m.run_candidate(64,41)
        self.assertEqual(a,b)

    def test_17_source_truth_never_overwritten(self):
        record=json.loads((m.ROOT/'docs/frozen/XVI_TAU_EVOLUTION_v001.json').read_text('utf-8'))
        self.assertNotEqual(record['gates']['T4_grid_refinement'],'PASS')
        self.assertNotEqual(self.r['gates']['S3'],'PASS_CANONICAL_T4')

if __name__=='__main__': unittest.main()
