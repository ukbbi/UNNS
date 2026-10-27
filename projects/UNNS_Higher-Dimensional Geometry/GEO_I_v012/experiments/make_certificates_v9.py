"""v009: RANK certificates for the 12 minimal reduced nullity-5 boxes (certificates/C5_rank5.json)."""
import sys,json,os; HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,'..','theory')); sys.path.insert(0,os.path.join(HERE,'..','certificates'))
import binary_min as BM, checker8 as K
rows=json.load(open(os.path.join(HERE,'..','output','data','v9_binary5.json'))); out=[]
for n,sig,mr in rows:
    cols=BM.code_to_parity_columns(sig,len(sig))
    c={'kind':'RANK','claim':'minimal non-embedded box of nullity 5 (reduced support of PG(4,2)), minimum witness rank = min_rank; B-SERIES data','columns':cols,'min_rank':mr,'nullity':5,'series_classes':len(cols),'reduced_support':sig,'multiplicities':[1]*len(cols)}
    ok,why=K.check_RANK(c); assert ok,(sig,why); out.append(c)
json.dump(out,open(os.path.join(HERE,'..','certificates','C5_rank5.json'),'w')); print(len(out),'certificates accepted')
