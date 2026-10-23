#!/usr/bin/env python3
"""FIELD-I v001 deterministic, standard-library-only verification and example exports."""
import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys
import unittest

from src.nest import value
from src.fibres import occurrences
from src.intersections import common_step, first_common_occurrences
from src.relations import successor_separation, scalar_successor_well_defined
from src.selection import nonselection_witness

BASE = Path(__file__).resolve().parent
OUT = BASE / 'output'


def write_json(path: Path, item) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(item, indent=2, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')


def test_cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from test_cases(item)
        else:
            yield item


def run_tests() -> bool:
    suite = unittest.defaultTestLoader.discover(str(BASE / 'tests'), pattern='test_*.py', top_level_dir=str(BASE))
    names = [test.id() for test in test_cases(suite)]
    result = unittest.TextTestRunner(verbosity=1, stream=sys.stdout).run(suite)
    report = {
        'program': 'FIELD-I v001',
        'asserted_test_cases': result.testsRun,
        'successful': result.wasSuccessful(),
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skips': len(result.skipped),
        'case_identifiers': names,
        'scope': 'Arithmetic tests and conditional nonselection witness; no physical interpretation'
    }
    write_json(OUT / 'reports' / 'test_report.json', report)
    print('TEST VERDICT:', 'ALL PASS' if result.wasSuccessful() else 'FAIL')
    return result.wasSuccessful()


def run_report() -> None:
    # Independent finite sample, not a proof or general novelty claim.
    bounded = defaultdict(list)
    for N in range(1, 12):
        for M in range(1, 200):
            bounded[value(M, N)].append((M, N))
    collisions = {x: v for x, v in bounded.items() if x.denominator > 1 and len(v) >= 2}
    keys = sorted(collisions)
    sample = [{'value': str(x), 'bounded_occurrences': [list(o) for o in collisions[x]],
               'full_fibre': [list(o) for o in occurrences(x)]} for x in keys[:15]]
    write_json(OUT/'witnesses'/'rational_collisions.json', {
        'bound': {'N_min':1,'N_max':11,'M_min':1,'M_max':199},
        'distinct_noninteger_collision_values_in_bound': len(keys),
        'first_15_in_ascending_value': sample,
        'interpretation': 'Bounded enumeration of equal outputs; not an independent relational operation.'
    })
    witness = nonselection_witness()
    write_json(OUT/'witnesses'/'nonselection.json', witness)

    values = [Fraction(72), Fraction(225, 2), Fraction(36), Fraction(81), Fraction(100),
              Fraction(9, 2), Fraction(361), Fraction(225, 4)]
    with (OUT/'tables'/'rational_fibres.csv').open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['reduced_value','numerator','denominator','multiplicity','occurrences_M_N', 'unique_next_values'])
        for x in values:
            os = occurrences(x)
            w.writerow([str(x),x.numerator,x.denominator,len(os),';'.join(f'{M}:{N}' for M,N in os),
                        int(scalar_successor_well_defined(x))])

    with (OUT/'tables'/'cross_nest.csv').open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['nest_1','nest_2','first_common_rational','first_modulus_1','first_modulus_2'])
        for n1,n2 in [(1,2),(2,4),(2,6),(3,5),(7,8),(9,11),(18,1)]:
            x,m1,m2=first_common_occurrences(n1,n2)
            w.writerow([n1,n2,str(x),m1,m2])

    summary = {
        'program':'FIELD-I v001',
        'phase_F1_F3':'Exact rational fibre and intersection formulae, with proofs in THEOREMS.md',
        'phase_F4':'Next-value injectivity is coordinate/label leakage, not independent interaction selection',
        'phase_F5':'Two distinct CAI binary operations commute with simultaneous unary successor',
        'bounded_rational_collision_values': len(keys),
        'bounded_collision_domain': '1<=N<=11; 1<=M<=199; only noninteger values and at least two in-bound occurrences',
        'sample_72': successor_separation(72),
        'sample_225_over_2': successor_separation(Fraction(225,2)),
        'cross_nest_2_4_first': str(common_step(2,4)),
        'conditional_nonselection_witness': witness,
        'open':'A binary interaction selected by the original unary fixed-nest dynamics is not established',
        'scope':'No physical/quantum entanglement claim; no arbitrary binary law promoted as intrinsic'
    }
    write_json(OUT/'reports'/'field1_report.json', summary)
    print('REPORT GENERATED:')
    print('  bounded noninteger collision values:', len(keys))
    print('  sample rational collision 225/2:', occurrences(Fraction(225,2)))
    print('  nonselection operations disagree:', witness['low'], witness['high'])
    print('  files under output/reports, output/tables and output/witnesses')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tests-only', action='store_true')
    parser.add_argument('--report-only', action='store_true')
    args = parser.parse_args()
    (OUT / 'reports').mkdir(parents=True, exist_ok=True)
    (OUT / 'tables').mkdir(parents=True, exist_ok=True)
    (OUT / 'witnesses').mkdir(parents=True, exist_ok=True)
    if args.tests_only and args.report_only:
        parser.error('choose at most one mode')
    if args.tests_only:
        return 0 if run_tests() else 1
    if args.report_only:
        run_report()
        return 0
    if not run_tests():
        print('Aborting report generation after tests failed.')
        return 1
    run_report()
    return 0


if __name__ == '__main__':
    sys.exit(main())
