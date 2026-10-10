import inspect, unittest
import scr_iii.scripts.run_acceptance_preflight_v002 as m

class AcceptanceSafetyTest(unittest.TestCase):
    def test_no_scr_outcome_calls(self):
        src=inspect.getsource(m)
        forbidden=("solve_scr(","excess_inclusion_EI","solution_recall","exact_preservation","write_solution_loss_ledger")
        for token in forbidden:
            self.assertNotIn(token,src)
