"""Writes STATUS.json from the root PDF actually delivered."""
import json, hashlib, os, re, subprocess
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf = H + '/PAPER_IV_SYNTHESIS_v0.5.pdf'
sha = hashlib.sha256(open(pdf, 'rb').read()).hexdigest()
try: pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
except Exception: pages = None
d = {'package': 'PAPER_IV_SYNTHESIS', 'version': '0.5', 'author': 'UNNS Research Collective',
     'title': 'The Geometry of Generation in the UNNS Substrate: A Mathematical Synthesis', 'date': '2026-11-03',
     'pdf': 'PAPER_IV_SYNTHESIS_v0.5.pdf', 'pdf_sha256': sha, 'pages': pages, 'figures': 22, 'synthesis_propositions': 9,
     'cites': {'PAPER_I_TRANSPORT': 'v0.4', 'PAPER_II_HISTORIES': 'v0.4', 'PAPER_III_EVOLUTION': 'v0.4'},
     'inherited_verification': 'NOT_RERUN', 'c3': 'unclaimed', 'github': 'read-only'}
json.dump(d, open(H + '/STATUS.json', 'w'), indent=1)
print('STATUS.json written; sha256', sha)
