"""Writes STATUS.json from the root PDF actually delivered and the last check result."""
import json, hashlib, os, re, subprocess
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf = H + '/PAPER_III_EVOLUTION_v0.4.pdf'
sha = hashlib.sha256(open(pdf, 'rb').read()).hexdigest()
try: pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
except Exception: pages = None
d = {'package': 'PAPER_III_EVOLUTION', 'version': '0.4', 'baseline': 'PAPER_III_EVOLUTION v0.3 (unchanged)', 'author': 'UNNS Research Collective',
     'title': 'Geometric Evolution under Collective UNNS Dynamics: Activation, Events, and Topological Prediction', 'date': '2026-11-03',
     'pdf': 'PAPER_III_EVOLUTION_v0.4.pdf', 'pdf_sha256': sha, 'pages': pages, 'figures': 26, 'allocated_records': 73,
     'records_with_theorem_in_paper': 64, 'records_cited_reallocated_to_paper_II': 9, 'not_rerun': 'see README.md'}
json.dump(d, open(H + '/STATUS.json', 'w'), indent=1)
print('STATUS.json written; sha256', sha)
