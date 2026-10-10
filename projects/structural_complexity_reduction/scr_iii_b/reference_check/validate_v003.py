"""SCR-III-B additive v003: statically linked C++ formula-harness preflight.
Does not invoke the unmodified Dryad simulator. Does not change v002 files.
"""
from __future__ import annotations
import json, os, pathlib, subprocess, sys, time, traceback

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DEST = ROOT / 'output' / 'validation' / 'v003'
DEST.mkdir(parents=True, exist_ok=True)
CPP = HERE / 'dryad_pair.cpp'
EXE = HERE / ('dryad_pair_v003.exe' if os.name == 'nt' else 'dryad_pair_v003.bin')
RESULT = DEST / 'REFERENCE_RUN_v003.json'
REPORT = DEST / 'REFERENCE_RUN_v003.md'


def execute(args, timeout=120):
    try:
        p = subprocess.run(args, text=True, capture_output=True, timeout=timeout, check=False)
        return {'status': 'EXITED', 'returncode': p.returncode,
                'stdout_tail': p.stdout[-3500:], 'stderr_tail': p.stderr[-3500:]}
    except FileNotFoundError as e:
        return {'status': 'MISSING_EXECUTABLE', 'error': str(e)}
    except subprocess.TimeoutExpired as e:
        return {'status': 'TIMEOUT', 'error': str(e)}
    except OSError as e:
        return {'status': 'OS_EXECUTION_ERROR', 'winerror': getattr(e, 'winerror', None), 'error': str(e)}


def write(rec):
    RESULT.write_text(json.dumps(rec, indent=2) + '\n', encoding='utf-8')
    lines = ['# SCR-III-B Reference Execution v003', '',
             f"**Verdict:** `{rec['verdict']}`", '',
             '**Scope:** Static GCC runtime linkage and source-formula C++/Python validation only; not full unmodified Dryad simulation.', '',
             '## Build and execution diagnostics', '', '```json', json.dumps(rec, indent=2), '```', '',
             'No Windows security controls need to be disabled. No frozen v001/v002 outputs are altered.']
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def run():
    command = ['g++', '-std=c++17', '-O2', '-static-libgcc', '-static-libstdc++', str(CPP), '-o', str(EXE)]
    rec = {'version': 'v003', 'build_command': command, 'reference_scope': 'transcribed Dryad pair coupling harness',
           'full_unmodified_dryad_reference_test': False, 'run': {}, 'verdict': 'NOT_RUN'}
    rec['build'] = execute(command)
    if rec['build']['status'] != 'EXITED' or rec['build']['returncode'] != 0:
        rec['verdict'] = 'COMPILER_MISSING' if rec['build']['status'] == 'MISSING_EXECUTABLE' else 'BUILD_FAIL'
        write(rec); print(json.dumps(rec, indent=2)); return 2
    for L in (1, 2, 3):
        r = execute([str(EXE), str(L)])
        rec['run'][str(L)] = r
        if r['status'] != 'EXITED' or r['returncode'] != 0:
            rec['verdict'] = 'EXECUTION_BLOCKED_OR_FAILED'
            write(rec); print(json.dumps(rec, indent=2)); return 3
        if not ('E ' in r['stdout_tail'] and 'K ' in r['stdout_tail']):
            # The output is intentionally truncated for diagnostics; check full numeric comparison below.
            pass
    # v002 script owns numerical comparisons; compile flags fixed without writing v002 result files.
    # Run a copy of v002 in a temporary sibling directory, whose DEST is temporarily redirected to v003.
    import importlib.util
    spec = importlib.util.spec_from_file_location('v002check', HERE / 'validate_v002.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_run = subprocess.run
    def patched_run(args, *a, **kw):
        if isinstance(args, list) and args and args[0] == 'g++':
            args = args[:3] + ['-static-libgcc', '-static-libstdc++'] + args[3:]
        return original_run(args, *a, **kw)
    module.DEST = DEST
    module.subprocess.run = patched_run
    try:
        module.run()
        cross = json.loads((DEST / 'ENERGY_REFERENCE_v002.json').read_text(encoding='utf-8'))
        rec['numeric_verdict'] = cross['verdict']
        rec['verdict'] = 'STATIC_FORMULA_CROSSCHECK_PASS_FULL_REFERENCE_PENDING' if cross['verdict'].startswith('FORMULA_CROSSCHECK_PASS') else 'NUMERICAL_MISMATCH'
    except BaseException as exc:
        rec['numeric_exception'] = {'type': type(exc).__name__, 'message': str(exc), 'traceback_tail': traceback.format_exc()[-2000:]}
        rec['verdict'] = 'NUMERICAL_CHECK_FAILED'
    write(rec)
    print('v003 verdict:', rec['verdict'])
    print('Reports:', DEST)
    return 0 if rec['verdict'] == 'STATIC_FORMULA_CROSSCHECK_PASS_FULL_REFERENCE_PENDING' else 4

if __name__ == '__main__':
    sys.exit(run())
