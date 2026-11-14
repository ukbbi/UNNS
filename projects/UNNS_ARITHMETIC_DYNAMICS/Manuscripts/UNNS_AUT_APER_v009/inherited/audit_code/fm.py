"""Second, independent emptiness solver: exact Fourier-Motzkin elimination (k first, then t) on integer constraints."""
def nonempty_fm(cons):
    lo=[];up=[];rest=[]
    for ct,ck,c0 in cons:
        if ck>0: lo.append((ct,ck,c0))       # k >= -(ct t + c0)/ck
        elif ck<0: up.append((ct,ck,c0))     # k <= (ct t + c0)/(-ck)
        else: rest.append((ct,c0))
    for (a1,b1,c1) in lo:
        for (a2,b2,c2) in up:
            # b1>0, b2<0: combine  (-b2)*(a1 t+b1 k+c1) + b1*(a2 t+b2 k+c2) >= 0  (k cancels)
            rest.append((-b2*a1+b1*a2, -b2*c1+b1*c2))
    # now 1-D in t: ct t + c0 >= 0
    tlo=None; tup=None
    for ct,c0 in rest:
        if ct==0:
            if c0<0: return False
        elif ct>0:
            v=(-c0,ct)               # t >= -c0/ct
            if tlo is None or v[0]*tlo[1]>tlo[0]*v[1]: tlo=v
        else:
            v=(c0,-ct)               # t <= c0/(-ct)
            if tup is None or v[0]*tup[1]<tup[0]*v[1]: tup=v
    if tlo is None or tup is None: return True
    return tlo[0]*tup[1]<=tup[0]*tlo[1]
