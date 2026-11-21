#!/usr/bin/env python3
"""Independent mesh/timestep resolution check for principal Maxwell amplitudes."""
from __future__ import annotations
import json
from pathlib import Path
from maxwell_solver import simulate
ROOT=Path(__file__).resolve().parents[1]

def main():
    pred=json.loads((ROOT/'protocol'/'PREDICTIONS_LOCK.json').read_text())
    specs=pred['numerics']; baseline=json.loads((ROOT/'results'/'heldout_raw.json').read_text())['cases']
    out={}
    for case_id in ('A_forward','reverse_nonUNNS','matched_nonUNNS_target'):
        c=next(x for x in pred['locked_cases'] if x['id']==case_id)
        kw={x:c[x] for x in ('q_first','q_second','start','first_on','second_on')}
        refined=simulate(**kw,eta=specs['eta'],cells=512,dt=.001,t_stage=specs['stage_duration'])
        mode=36 if c['start']==2 else 38
        a=baseline[case_id]['outgoing']['after_stage_2'][str(mode)]['amplitude']
        b=refined['outgoing']['after_stage_2'][str(mode)]['amplitude']
        err=abs(b-a)/abs(b)
        assert err<.005,(case_id,err)
        out[case_id]={'mode':mode,'baseline_amplitude':a,'refined_amplitude':b,'relative_change':err}
        print(case_id,'mode',mode,'mesh/time relative change',format(err,'.5g'),'PASS')
    (ROOT/'results'/'convergence.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('MUG-I v009 GRID/TIME CONVERGENCE PASS')
if __name__=='__main__':main()
