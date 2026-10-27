"""G9-Z check: a parity-check matrix with a zero column is never a minimal non-embedded box.  Exhaustive over all column multisets (incl. zero columns) m<=3, n<=8
(path: binary_01).  usage: zero_column.py OUT.json"""
import sys,json,itertools; sys.path.insert(0,'theory')
import binary_01 as B
res={'tested':0,'nonembedded_with_zero':0,'minimal_with_zero':0}
for m in (2,3):
    for n in range(2,9):
        for cols in itertools.combinations_with_replacement(range(0,1<<m),n):
            if 0 not in cols: continue
            res['tested']+=1
            if not B.is_embedded(list(cols)):
                res['nonembedded_with_zero']+=1
                if B.minimal_nonembedded(list(cols)): res['minimal_with_zero']+=1; print('MINIMAL WITH ZERO',cols)
json.dump(res,open(sys.argv[1],'w')); print(res)
