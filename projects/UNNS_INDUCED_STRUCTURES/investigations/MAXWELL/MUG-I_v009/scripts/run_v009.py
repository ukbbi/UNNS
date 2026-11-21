#!/usr/bin/env python3
"""Execute pre-locked Maxwell experiment; no UNNS logic in numerical solver."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
from maxwell_solver import simulate
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'protocol'/'PREDICTIONS_LOCK.json'
R=ROOT/'results'

def main():
    recorded=(ROOT/'protocol'/'PREDICTIONS_LOCK.sha256').read_text().split()[0]
    actual=hashlib.sha256(P.read_bytes()).hexdigest()
    if recorded!=actual: raise RuntimeError('PREDICTIONS_LOCK hash mismatch!')
    spec=json.loads(P.read_text())
    conf=spec['numerics']
    cases={}; rows=[]
    for c in spec['locked_cases']:
        kw={name:c[name] for name in ('start','q_first','q_second','first_on','second_on')}
        vals=simulate(**kw,eta=conf['eta'],cells=conf['cells'],dt=conf['dt'],t_stage=conf['stage_duration'])
        cases[c['id']]=vals
        for pred in c['predictions']:
            amp=vals['outgoing'][pred['stage']][str(pred['mode'])]['amplitude']
            passed=amp>pred['threshold'] if pred['relation']=='>' else amp<pred['threshold']
            rows.append({'case':c['id'],'stage':pred['stage'],'mode':pred['mode'],'relation':pred['relation'],
                         'threshold':pred['threshold'],'amplitude':amp,'passed':passed})
        print(c['id'], ' | '.join(f"m{r['mode']}={r['amplitude']:.8g} {'PASS' if r['passed'] else 'FAIL'}" for r in rows if r['case']==c['id']))
    R.mkdir(parents=True,exist_ok=True)
    (R/'heldout_raw.json').write_text(json.dumps({'protocol_sha256':actual,'cases':cases},indent=2,sort_keys=True)+'\n')
    with (R/'heldout_predictions.csv').open('w',newline='') as f:
        out=csv.DictWriter(f,fieldnames=['case','stage','mode','relation','threshold','amplitude','passed']);out.writeheader();out.writerows(rows)
    (R/'heldout_summary.json').write_text(json.dumps({'lock_sha256':actual,'n_cases':len(cases),'n_predictions':len(rows),
        'passed':sum(bool(x['passed']) for x in rows),'failed':[x for x in rows if not x['passed']],
        'claim':'prospective computational test, not blinded physical measurement'},indent=2)+'\n')
    print('MUG-I v009 HELDOUT', 'PASS' if all(x['passed'] for x in rows) else 'FAIL',f"{sum(x['passed'] for x in rows)}/{len(rows)}",'lock',actual[:16])
    if not all(x['passed'] for x in rows): raise SystemExit(2)

if __name__=='__main__':main()
