"""Verification tests. Scientific FAIL gates are intentionally preserved and asserted."""
import json
import math
import unittest
from pathlib import Path
import numpy as np
from src import xvi_invariants_audit_v001 as audit

ROOT=Path(__file__).resolve().parents[1]

class InvariantsV001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((ROOT/'output/XVI_INVARIANTS_AUDIT_v001.json').read_text('utf8'))

    def test_01_exact_uploaded_baseline_lock(self):
        self.assertTrue(audit.locked()['all_pass'])

    def test_02_previous_negative_canonical_verdict_not_reversed(self):
        self.assertTrue(audit.locked()['prior_negative_preserved'])
        self.assertFalse(self.report['full_canonical_XVI_invariant_certified'])

    def test_03_sources_locked(self):
        self.assertEqual(len(audit.locked()['checks']),6)
        self.assertTrue(all(v['pass'] for v in audit.locked()['checks'].values()))

    def test_04_full_source_mu_grid_includes_phi_by_design(self):
        mu=audit.mu_values()
        self.assertGreaterEqual(len(mu),40)
        self.assertAlmostEqual(mu[0],1.6)
        self.assertLessEqual(mu[-1],1.64000000000001)
        self.assertTrue(1.6<1.618<1.64)

    def test_05_mu_sampling_exact_constant(self):
        a=np.full((8,8),1.4)
        self.assertAlmostEqual(audit.scaled_delta(a,1.618),0.0)
        self.assertTrue(audit.scale_invariant(a)['at_search_edge'])

    def test_06_entropy_source_histogram_two_equal_populations(self):
        a=np.tile([0.,1.],(8,4))
        self.assertAlmostEqual(audit.entropy_source(a)['H_r'],1.0)

    def test_07_constant_entropy_undefined_not_fabricated(self):
        self.assertIsNone(audit.entropy_source(np.ones((8,8)))['H_r'])

    def test_08_spectrum_constant_not_faked_valid(self):
        a=np.ones((16,16))
        self.assertNotEqual(audit.spectrum_source(a)['status'],'SOURCE_FIT_NUMERICALLY_FINITE')

    def test_09_four_export_source_fields_unavailable(self):
        self.assertEqual(len(self.report['original_chamber_exports']),4)
        for r in self.report['original_chamber_exports']:
            self.assertFalse(r['raw_tau_field_exported'])
            self.assertFalse(r['field_based_recalculation_possible'])

    def test_10_all_original_exports_failed_C2(self):
        self.assertTrue(all(not e['reported_criteria']['C_invariants'] for e in self.report['original_chamber_exports']))

    def test_11_js_source_mu_entropy_parity(self):
        p=audit.source_js_parity_witness()
        self.assertTrue(p['all_scale_and_entropy_parity'])

    def test_12_js_spectral_parity_failure_recorded(self):
        p=audit.source_js_parity_witness()
        self.assertFalse(p['all_spectral_parity'])
        self.assertEqual(self.report['gates']['I12'],'FAIL_STRICT_SPECTRAL_JS_PARITY')

    def test_13_grid_seeds_controls_complete(self):
        self.assertEqual({(r['N'],r['seed']) for r in self.report['experiments']},
                         {(n,seed) for n in (64,128,256) for seed in (41,137)})
        self.assertTrue(all(set(r['runs'])=={'candidate','advection_diffusion','diffusion_only'}
                            for r in self.report['experiments']))

    def test_14_field_variation_retained_only_finite(self):
        self.assertTrue(all(r['runs']['candidate']['std_retention']>=.65 for r in self.report['experiments']))
        self.assertEqual(self.report['gates']['I4'],'PASS_FINITE_RETENTION')

    def test_15_closure_ablation_control_not_removed(self):
        self.assertTrue(all(r['candidate_vs_no_closure_field_rel']>.01 for r in self.report['experiments']))
        self.assertEqual(self.report['gates']['I5'],'PASS_ABLATION_EFFECT_ONLY')

    def test_16_spectrum_source_target_fail_not_relabelled(self):
        self.assertEqual(self.report['gates']['I8'],'FAIL_SOURCE_SPECTRAL_TARGET')
        self.assertEqual(self.report['gates']['I6'],'FAIL_SPECTRAL_RELIABILITY')

    def test_17_phi_search_constrained_not_claimed_discovery(self):
        self.assertEqual(self.report['gates']['I7'],'FAIL_OR_UNINFORMATIVE_PHI_WINDOW')
        for r in self.report['experiments']:
            self.assertTrue(r['runs']['candidate']['final']['scale']['phi_in_window_by_design'])

    def test_18_entropy_stability_not_structure_proof(self):
        self.assertEqual(self.report['gates']['I9'],'PASS_NUMERIC_TAIL_NOT_UNIQUE')
        self.assertTrue(all(r['runs']['diffusion_only']['tail_entropy_relative_change']<.001
                            for r in self.report['experiments']))

    def test_19_no_born_claim(self):
        self.assertEqual(self.report['born_rule'],'NOT_DERIVED')
        self.assertEqual(self.report['scientific_verdict'],'INVARIANT_FIDELITY_NOT_CERTIFIED')

    def test_20_source_html_unmodified(self):
        expected=json.loads((ROOT/'config/XVI_INVARIANTS_LOCK_v001.json').read_text())['inputs']['html']['sha256']
        self.assertEqual(audit.sha(ROOT/'docs/sources/XVI_ENGINE_v084.html'),expected)

if __name__=='__main__': unittest.main()
