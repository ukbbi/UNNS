#!/usr/bin/env python3
"""Portable launcher for the frozen inherited v005 regression suite (regression_v005.py, byte-identical, NOT modified).
regression_v005.py calls the external program `sha256sum -c MANIFEST.sha256` for optional sibling releases GEO_I_v001..v004 found next to this folder;
that program does not exist on Windows (FileNotFoundError aborted the whole suite).  This launcher provides a pure-Python equivalent with the same
semantics (`<path>: OK` / `<path>: FAILED`) and then runs the unmodified suite.  Nothing is suppressed: a sibling that does not verify is still reported."""
import os, sys, hashlib, subprocess, runpy
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); TARGET = os.path.join(ROOT, 'regression_v005.py')
_real = subprocess.run
class _Res:
    def __init__(self, out, rc): self.stdout, self.stderr, self.returncode = out, '', rc
def _sha256sum_check(cwd):
    out = []; bad = 0
    for l in open(os.path.join(cwd, 'MANIFEST.sha256'), encoding='utf-8'):
        l = l.rstrip('\r\n')
        if not l.strip(): continue
        h, p = l.split(None, 1); p = p.lstrip('*'); q = os.path.join(cwd, p)
        ok = os.path.isfile(q) and hashlib.sha256(open(q, 'rb').read()).hexdigest() == h
        out.append('%s: %s' % (p, 'OK' if ok else 'FAILED')); bad += (not ok)
    return _Res('\n'.join(out) + '\n', 1 if bad else 0)
def _run(args, *a, **k):
    if isinstance(args, (list, tuple)) and len(args) >= 3 and args[0] == 'sha256sum' and args[1] == '-c':
        return _sha256sum_check(k.get('cwd') or os.getcwd())
    return _real(args, *a, **k)
subprocess.run = _run
sys.argv = [TARGET] + sys.argv[1:]
runpy.run_path(TARGET, run_name='__main__')
