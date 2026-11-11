import json,sys
from fibcert3 import certify_class
paths=json.load(open('../data/class_paths.json'))
out={}
for r,p in paths.items():
    o=certify_class(p['P'],p['r'],[tuple(s) for s in p['steps']],p['nf'])
    out[r]=o
    print(r,{k:v for k,v in o.items() if k in('length','symbolic_final_equals_y','integrality_all_states_and_labels','positivity_all','monotone_states','numeric_legal_replay')},flush=True)
json.dump(out,open('../reports/class_certificates.json','w'),indent=1)
