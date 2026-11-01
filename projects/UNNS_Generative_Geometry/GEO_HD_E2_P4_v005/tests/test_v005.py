import os, sys, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'RUN_VERIFY.py'), '--shard', shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]

def test_hash_pins():            run('S0')
def test_tiling_lemma():         run('S1')
def test_conformal_and_hard():   run('S2')
def test_counterexamples():      run('S3')
def test_dilation():             run('S4')
def test_split_identity():       run('S5')
def test_split_criterion():      run('S6')
def test_stored_scans():         run('S8')

def test_status_gates():
    st = json.load(open(os.path.join(ROOT, 'STATUS.json')))
    assert st['gates']['C3'] == 'NOT_CLAIMED'
    assert 'same author' in st['independence_caveat']
