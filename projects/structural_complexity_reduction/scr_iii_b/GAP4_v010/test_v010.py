#!/usr/bin/env python3
"""Public small-size conformance; no real 4x4 energies."""
import subprocess,sys,pathlib,json
here=pathlib.Path(__file__).resolve().parent
for L in (1,2):
    f=here/f'public_{L}.txt'
    subprocess.run([sys.executable,str(here/'make_instance_v010.py'),'--size',str(L),'--output',str(f)],check=True)
    out=subprocess.check_output([str(here/'solver_v010'),str(f),'10'],text=True)
    records=[json.loads(t) for t in out.splitlines()]
    assert all(r['completed'] for r in records)
    assert records[0]['upper'] <= records[1]['upper']
    print('SMALL_PASS',L,[(r['objective'],r['upper'],r['nodes']) for r in records])
# guard
r=subprocess.run([sys.executable,str(here/'make_instance_v010.py'),'--size','4','--output',str(here/'DO_NOT_CREATE_REAL.txt')],capture_output=True,text=True)
assert r.returncode != 0 and 'BLOCKED' in r.stderr
print('GUARD_PASS')
