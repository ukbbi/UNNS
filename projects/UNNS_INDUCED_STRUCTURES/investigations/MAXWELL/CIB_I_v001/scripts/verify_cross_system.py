"""Cross-equation Fourier-matrix identity: scalar Maxwell, Schr and acoustic analogues.

This checks first-order material/potential matrix elements only, not dynamics.
Requires NumPy, standard in user's existing Ubuntu setup.
"""
from fractions import Fraction
import math
import numpy as np
cases=[(2,8),(8,36),(2,9),(9,36),(4,38),(11,12)]
for st in ['1/2','1/3','1/5','1/7']:
    D=Fraction(st)
    K=8192*D.denominator
    z=2*math.pi*(np.arange(K)+.5)/K
    u=(z<2*math.pi*float(D)).astype(float)-float(D)
    for m,mp in cases:
        q=mp-m
        # Independent plane-wave matrix integration on grid.
        left=np.exp(-1j*mp*z)
        right=np.exp(1j*m*z)
        maxwell_mass=np.dot(left,u*right)/K
        schrodinger_potential=np.dot(left*right,u)/K
        acoustic_density_mass=np.mean(u*np.exp(-1j*q*z))
        expected=np.exp(-1j*math.pi*q*float(D))*math.sin(math.pi*q*float(D))/(math.pi*q)
        assert abs(maxwell_mass-expected)<3e-6
        assert abs(schrodinger_potential-maxwell_mass)<3e-15
        assert abs(acoustic_density_mass-maxwell_mass)<3e-15
    print('PASS normalized first-order cross-system Fourier kernel',st,'modes',len(cases))
print('CIB-I v001 CROSS-SYSTEM VERIFY PASS')
