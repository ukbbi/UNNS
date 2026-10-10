from pathlib import Path
import hashlib
PR=Path(__file__).resolve().parents[1]
EXCLUDE={'SHA256SUMS.txt'}
files=[]
for p in sorted(PR.rglob('*')):
    if p.is_file() and p.name not in EXCLUDE and '__pycache__' not in p.parts:
        files.append(p)
lines=[]
for p in files:
    h=hashlib.sha256(p.read_bytes()).hexdigest(); lines.append(f"{h}  {p.relative_to(PR).as_posix()}")
(PR/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('wrote',PR/'SHA256SUMS.txt',len(files),'files')
