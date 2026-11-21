#!/usr/bin/env python3
"""Independent post-test check: compare predictions lock to reported Maxwell amplitudes."""
from pathlib import Path
import csv,hashlib,json
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=ROOT/'protocol'/'PREDICTIONS_LOCK.json';spec=json.loads(p.read_text())
    lockhash=hashlib.sha256(p.read_bytes()).hexdigest()
    assert lockhash==(ROOT/'protocol'/'PREDICTIONS_LOCK.sha256').read_text().split()[0]
    raw=json.loads((ROOT/'results'/'heldout_raw.json').read_text());assert raw['protocol_sha256']==lockhash
    summary=json.loads((ROOT/'results'/'heldout_summary.json').read_text())
    assert summary['lock_sha256']==lockhash
    num=0
    for case in spec['locked_cases']:
        data=raw['cases'][case['id']]
        assert data['initial']['carrier']==case['start']
        assert data['pump']['first_q']==case['q_first']
        assert data['pump']['second_q']==case['q_second']
        assert data['scheme']['cells']==spec['numerics']['cells']
        for rule in case['predictions']:
            actual=data['outgoing'][rule['stage']][str(rule['mode'])]['amplitude']
            if rule['relation']=='>':assert actual>rule['threshold'],(case['id'],rule,actual)
            elif rule['relation']=='<':assert actual<rule['threshold'],(case['id'],rule,actual)
            else:raise AssertionError('unsupported comparator')
            num+=1
    rows=list(csv.DictReader((ROOT/'results'/'heldout_predictions.csv').open()))
    assert len(rows)==num
    assert num==summary['passed']==summary['n_predictions'] and not summary['failed']
    # No effect of window timing on exact even-mode parity: all cases with q even show vanishing odd modes
    for name in ('A_forward','reverse_nonUNNS','single_6','single_28','matched_nonUNNS_target'):
        data=raw['cases'][name]
        assert data['final_total_absmax_odd']<5e-11
        assert data['final_total_absmax_odd_B']<5e-11
    print(f'PASS held-out lock binding, {len(spec["locked_cases"])} cases, {num} predictions')
    print('PASS exact parity-protected odd-mode nulls in all even-harmonic pumps')
    print('MUG-I v009 HELDOUT VERIFY PASS')

if __name__=='__main__':main()
