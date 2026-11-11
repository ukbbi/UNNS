"""Registered orbit analysis (do not edit after registration)."""
import rn_core as C
def tail_sig(labels,window=6):
    if len(labels)<window+2: return None
    t=labels[-window:]
    for p in (1,2,3):
        if all(t[i]==t[i%p] for i in range(window)): return tuple(t[:p])
    return "irregular"
def analyse(o,ESC):
    seq=o["seq"];st=o["status"]
    body=seq[:-1] if st=="escape" else seq              # last escape term is not examined (may exceed certified range)
    primes=[]; 
    for v in body:
        pr,c=C.is_prime(v)
        if pr: primes.append(v)
    a=dict(status=st,length=len(seq),certified=o["certified"],n_prime_visits=len(primes),distinct_primes=len(set(primes)),primes=sorted(set(primes))[:10],
           sig=tail_sig(o["labels"]) if st in("escape","horizon") else None)
    if st=="cyclic":
        cyc=seq[o["pre"]:o["pre"]+o["period"]]
        a.update(pre=o["pre"],period=o["period"],cycle=cyc[:8],cycle_has_prime=any(C.is_prime(v)[0] for v in cyc))
    if st=="stuck":
        v=seq[-1];f=C.factor(v)[0]
        a.update(terminal=v,terminal_squarefree=all(e==1 for e in f.values()),terminal_prime=C.is_prime(v)[0],terminal_deg=C.degree_from_fact(f))
    return a
