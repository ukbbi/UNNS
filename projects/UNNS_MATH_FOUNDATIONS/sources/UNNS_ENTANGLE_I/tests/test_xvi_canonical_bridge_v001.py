"""Source-lock and operator counterexample audit; does not require Node.js or NumPy."""
import json
import math
import unittest
from pathlib import Path
from src import xvi_canonical_bridge_v001 as m

class XVIActualSourceAudit(unittest.TestCase):
    def test_01_all_source_and_phase3_baselines_locked(self):
        a=m.verify_lock();self.assertTrue(a['all_pass'],a)
    def test_02_source_formulas_verbatim(self):
        a=m.source_audit();self.assertTrue(all(a.values()),a)
    def test_03_counterexample_64(self):
        self.assertAlmostEqual(m.longitudinal_mode(64)['original_divergence_ratio_after_before'],0.9019828596704393,places=12)
    def test_04_counterexample_128(self):
        self.assertAlmostEqual(m.longitudinal_mode(128)['original_divergence_ratio_after_before'],0.950932325672582,places=12)
    def test_05_counterexample_256(self):
        self.assertAlmostEqual(m.longitudinal_mode(256)['original_divergence_ratio_after_before'],0.9754587714770877,places=12)
    def test_06_residual_worsens_with_refinement(self):
        a=[m.longitudinal_mode(N)['original_divergence_ratio_after_before'] for N in (64,128,256)]
        self.assertTrue(a[0]<a[1]<a[2])
    def test_07_original_operator_not_idempotent(self):
        a=m.longitudinal_mode(64);self.assertGreater(a['relative_projection_idempotence_defect'],0.05)
    def test_08_original_energy_decomposition_fails(self):
        a=m.longitudinal_mode(64);self.assertGreater(a['relative_L2_energy_decomposition_defect'],0.1)
    def test_09_matched_spectral_comparator_only(self):
        for N in (64,128,256):self.assertEqual(m.longitudinal_mode(N)['ideal_spectral_comparator_divergence_ratio'],0)
    def test_10_zero_mean_div_not_zero_rms(self):
        a=m.longitudinal_mode(64);self.assertTrue(a['original_divergence_mean_is_zero']);self.assertGreater(a['original_divergence_ratio_after_before'],0.9)
    def test_11_original_exports_preserved(self):
        runs=m.summarize_exports();self.assertEqual(len(runs),4)
        self.assertEqual({r['config']['grid'] for r in runs},{64,128,256})
        self.assertTrue(all(r['export_version']=='0.8.0' for r in runs))
        self.assertTrue(all(r['timeline_count']>0 for r in runs))
    def test_12_gates_refuse_born_rule_claim(self):
        r=m.build_report();self.assertEqual(r['gates']['B5'],'BLOCKED_NO_OBSERVABLE_EVENT_BRIDGE')
        self.assertEqual(r['gates']['B6'],'NOT_DERIVED_BORN_RULE')
        self.assertEqual(r['primary_verdict'],'CANONICAL_IMPLEMENTATION_OBSTRUCTION')
    def test_13_invalid_modes_rejected(self):
        for N,m0 in [(2,1),(64,0),(64,32)]:
            with self.assertRaises(ValueError):m.longitudinal_mode(N,m0)
    def test_14_frozen_phase3_scientific_status(self):
        j=json.loads((m.PROJECT/'docs/frozen/MEASURE_REP_PHASE3_v001.json').read_text(encoding='utf-8'))
        self.assertEqual(j['gates']['R5'],'BLOCKED_NOT_DERIVED')
        self.assertTrue(j['phase2c_integrity_pass'])

if __name__=='__main__':unittest.main()
