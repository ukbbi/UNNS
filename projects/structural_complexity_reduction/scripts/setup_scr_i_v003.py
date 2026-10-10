from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.scr_i_v003.source_lock_v003 import install
print('[SCR-I v003] verifying pinned source lock...')
s=install(ROOT,allow_download=True);print('V003 SOURCE LOCK:', 'PASS' if s.get('ok') else 'FAIL')
p=subprocess.run([sys.executable,str(ROOT/'SCR_I_PREREG_v003'/'scripts'/'validate_prereg.py')],cwd=str(ROOT/'SCR_I_PREREG_v003'));print('V003 PREREG:', 'PASS' if p.returncode==0 else 'FAIL')
if not s.get('ok') or p.returncode!=0: raise SystemExit(1)
r=subprocess.run([sys.executable,str(ROOT/'scripts'/'run_v003_regression.py')],cwd=str(ROOT))
if r.returncode: raise SystemExit(r.returncode)
print('\nSCR-I v003 setup completed. Refresh the dashboard. Do not run the primary until all readiness gates are green.')
