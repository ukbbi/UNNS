import subprocess, sys, json
rows=[]; F=[0,1]
while len(F)<=60: F.append(F[-1]+F[-2])
for k in range(2,36):
    try:
        out=subprocess.run(["python3","fib_one.py",str(k)],capture_output=True,text=True,timeout=int(sys.argv[1]))
        d=int(out.stdout.strip())
    except subprocess.TimeoutExpired: d=None
    rows.append((k,F[k],F[k+1],d)); print(k,F[k],F[k+1],d,flush=True)
    if d is None and sum(1 for r in rows[-3:] if r[3] is None)==3: break
open(sys.argv[2],"w").write("k,F_k,F_k1,d\n"+"".join(f"{k},{a},{b},{'' if d is None else d}\n" for k,a,b,d in rows))
