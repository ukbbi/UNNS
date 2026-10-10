from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

HERE=Path(__file__).resolve(); PR=HERE.parents[1]; S3=PR.parent; PROJECT=S3.parent

def sha(p):
    h=hashlib.sha256();
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def main():
    required=[PR/'SCR_III_PREREG_v001.md',PR/'SEEDS_v001.json',PR/'config'/'prereg_v001.json',PR/'schema'/'route_csp_c_v001.schema.json',PR/'schema'/'result_v001.schema.json',PR/'SOURCE_LOCK.md',PR/'METRICS.md',PR/'NULLS.md',PR/'DECISION_RULES.md',PR/'SHA256SUMS.txt']
    missing=[str(x.relative_to(PR)) for x in required if not x.exists()]
    if missing:
        print('FAIL missing:', ', '.join(missing)); return 1
    cfg=json.loads((PR/'config'/'prereg_v001.json').read_text(encoding='utf-8'))
    if cfg.get('status')!='FROZEN_BEFORE_AUDIT': print('FAIL config status'); return 1
    seeds=json.loads((PR/'SEEDS_v001.json').read_text(encoding='utf-8'))
    vals=[]
    for xs in seeds['audit'].values(): vals.extend(xs)
    for xs in seeds['primary'].values(): vals.extend(xs)
    vals.extend(seeds['null_seed_bases'].values()); vals += [seeds['estimator_sample_seed'],seeds['trend_permutation_seed']]
    if len(vals)!=len(set(vals)): print('FAIL duplicate frozen seed'); return 1
    burned=set(seeds['burned_exclusions']['smoke_test'])
    if burned & set(vals): print('FAIL burned seed reused'); return 1
    # verify bundle hashes (SHA256SUMS excludes itself)
    for line in (PR/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        expected, rel=line.split(None,1); p=PR/rel.strip()
        if not p.exists() or sha(p)!=expected:
            print('FAIL hash:', rel.strip()); return 1
    print('SCR_III_PREREG_v001 validation: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
