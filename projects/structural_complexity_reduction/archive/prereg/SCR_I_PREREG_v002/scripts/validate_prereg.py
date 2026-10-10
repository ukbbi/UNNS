from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/'config'/'scr_i_prereg_v002.json'
REQ=['README.md','PREREG.md','TARGET_ORACLE.md','DESIGN_AUDIT.md','BENCH_A.md','GATES.md','METRICS.md','NULLS.md','DECISION_RULES.md','SOURCE_LOCK.md','UPI_BLIND.md','RUN_PLAN.md','MANIFEST.md']

def main():
    errors=[]
    for n in REQ:
        p=ROOT/n
        if not p.is_file() or p.stat().st_size<180: errors.append(f'missing/too-small: {n}')
    c=json.loads(CFG.read_text(encoding='utf-8'))
    if c.get('preregistration')!='SCR_I_PREREG_v002': errors.append('wrong prereg id')
    if c.get('gate_order')!=['G1','G2','G3','G4']: errors.append('gate order changed')
    if c['candidate_pool']['sizes']!=[2500,10000,40000]: errors.append('pool sizes changed')
    if c['candidate_pool']['primary_seeds']!=[2026100801,2026100802,2026100803,2026100804,2026100805]: errors.append('primary seeds changed')
    if set(c['candidate_pool']['primary_seeds']) & set(c['design_audit']['seeds']): errors.append('audit/primary seed overlap')
    if c['target_oracle']['replicates']!=20 or c['target_oracle']['pass_rate_gte']!=0.85: errors.append('target oracle changed')
    if c['target_oracle']['checks']['locality_score_lt']!=0.20: errors.append('viability locality changed')
    if c['primary_requirements']['target_recall']!=1.0: errors.append('recall must be 1.0')
    if c['upi']['prunes'] is not False: errors.append('UPI must be non-pruning')
    # Verify frozen file hashes if SHA256SUMS exists.
    sums=ROOT/'SHA256SUMS.txt'
    if sums.is_file():
        for line in sums.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            dig, rel=line.split('  ',1); p=ROOT/rel
            if not p.is_file(): errors.append(f'hash file missing: {rel}'); continue
            actual=hashlib.sha256(p.read_bytes()).hexdigest()
            if actual!=dig: errors.append(f'hash mismatch: {rel}')
    if errors:
        print('SCR-I preregistration v002 validation: FAIL')
        for e in errors: print(' -',e)
        return 1
    print('SCR-I preregistration v002 validation: PASS')
    print('Target: Chamber LIII source-equivalent viability')
    print('Primary seeds: 2026100801..2026100805 (disjoint from design audit)')
    print('Gate order: G1 -> G2 -> G3 -> G4')
    return 0
if __name__=='__main__': raise SystemExit(main())
