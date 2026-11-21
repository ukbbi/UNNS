#!/usr/bin/env python3
"""Post-lock illustrations of infinitely many Maxwell-accessible/UNNS-forbidden pairs.
Not part of the 13 pre-locked predictions.
"""
import csv
from pathlib import Path
from maxwell_solver import simulate
ROOT=Path(__file__).resolve().parents[1]

def main():
    rows=[]
    for m in (12,13,20):
        out=simulate(start=m,eta=.009,t_stage=1.7)
        tar=m+34
        amp=out['outgoing']['after_stage_2'][str(tar)]['amplitude']
        assert (tar/m)<4 and amp>0.005
        rows.append({'source':m,'target':tar,'first_intermediate':m+6,
                     'ratio':tar/m,'UNNS_path':'absent: target < 4*source',
                     'Maxwell_outgoing_amplitude':amp})
        print(f'UNNS-FORBIDDEN, Maxwell excited: {m} -> {tar}, outgoing amplitude {amp:.9g}')
    with (ROOT/'results'/'nonUNNS_family_samples.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('MUG-I v009 COUNTERFAMILY NUMERICAL EXAMPLES PASS')

if __name__=='__main__':main()
