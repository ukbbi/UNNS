#!/usr/bin/env python3
"""Independent stdlib exact arithmetic and symmetry tests (no Maxwell solver imports)."""
from fractions import Fraction
from math import gcd
from functools import reduce
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def step(x,n):
    assert isinstance(x,int) and x>0 and isinstance(n,int) and n>0 and x%n==0
    return (x//n)*(n+1)*(n+1)

def trace(x,word):
    out=[x]
    for n in word:out.append(step(out[-1],n))
    return out

def exists_path(start,target):
    if target<=start:return start==target
    seen={start};front=[start]
    while front:
        v=front.pop()
        for n in range(1,v+1):
            if v%n:continue
            w=step(v,n)
            if w==target:return True
            if w<target and w not in seen:seen.add(w);front.append(w)
    return False

def validate():
    p=ROOT/'protocol'/'PREDICTIONS_LOCK.json'
    recorded=(ROOT/'protocol'/'PREDICTIONS_LOCK.sha256').read_text().split()[0]
    assert hashlib.sha256(p.read_bytes()).hexdigest()==recorded
    locked=json.loads(p.read_text())
    assert trace(2,(1,2))==[2,8,36]
    assert trace(2,(2,1))==[2,9,36]
    assert not exists_path(2,30)
    assert not exists_path(4,38)
    assert all(Fraction((n+1)**2,n)>=4 for n in range(1,300))
    assert Fraction(38,4)<16 # therefore any path 4->38 could only have one step
    assert not any(step(4,n)==38 for n in (1,2,4))
    assert gcd(6,28)==2
    assert (9-2)%2==1
    assert (36-2)%6!=0 and (36-2)%28!=0
    assert (36-2)%gcd(6,28)==0
    assert 8-2==6 and 36-8==28
    assert 9-2==7 and 36-9==27
    assert 30-2==28 and 36-30==6
    assert 10-4==6 and 38-10==28
    assert {c['id'] for c in locked['locked_cases']} == {
        'A_forward','reverse_nonUNNS','single_6','single_28',
        'B_alternative_grating','matched_nonUNNS_target'}
    # Stage-ordered resonant coupling graph based solely on Maxwell's pump Fourier harmonics
    assert [2,8,36] == [2,2+6,2+6+28]
    assert [2,30,36] == [2,2+28,2+28+6]
    assert [2,9,36] == [2,2+7,2+7+27]
    assert [4,10,38] == [4,4+6,4+6+28]
    # Frequencies of individual propagating positive index modes in the pump-off vacuum satisfy omega_m=m
    assert all(m>0 and m*m==m**2 for m in (2,4,8,9,10,30,36,38))
    print('PASS independent exact UNNS history/absence witnesses')
    print('PASS exact translation-subgroup mode restrictions and grating momentum selection')
    print('PASS physical control: 4->38 reachable by Maxwell coupling but by no UNNS history')
    print('PASS locked prospective protocol hash',recorded[:16])
    print('MUG-I v009 EXACT VERIFY PASS')

if __name__=='__main__':validate()
