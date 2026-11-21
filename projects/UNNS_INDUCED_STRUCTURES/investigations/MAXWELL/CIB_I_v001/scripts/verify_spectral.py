"""Independent numerical Fourier oracle using spatial grid and FFT (optional NumPy)."""
from pathlib import Path
import json, hashlib, math
from fractions import Fraction
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'protocol'/'PROTOCOL.json'
data=json.loads(P.read_text())
assert hashlib.sha256(P.read_bytes()).hexdigest()==(ROOT/'protocol'/'PROTOCOL.sha256').read_text().strip()
for profile in data['medium_profiles']+data['additional_checks']:
    duty=Fraction(profile)
    K=duty.denominator*4096  # duty boundary falls exactly on a cell boundary
    z=(np.arange(K)+0.5)/K
    eps_perturb=(z<float(duty)).astype(float)-float(duty)
    spectrum=np.abs(np.fft.rfft(eps_perturb))/K
    q=np.arange(1,256)
    oracle=np.abs(np.sin(math.pi*q*float(duty))/(math.pi*q))
    abs_err=float(np.max(np.abs(spectrum[1:256]-oracle)))
    zero_idxs=np.arange(duty.denominator,256,duty.denominator)
    assert float(np.max(spectrum[zero_idxs]))<1e-12
    assert abs_err<3e-6,(profile,abs_err)
    print('PASS independent FFT',profile,'N',K,'max_amp_abs_err',f'{abs_err:.3g}','zero_harmonics',len(zero_idxs))
print('CIB-I v001 SPECTRAL VERIFY PASS')
