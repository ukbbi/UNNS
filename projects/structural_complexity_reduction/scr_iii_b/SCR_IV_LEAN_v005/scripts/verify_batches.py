#!/usr/bin/env python3
"""IV-4B stage runner: kernel-check every batch module (Bat/B<g|n>_NNN.lean) with a bounded number of concurrent Lean processes (default 2:
unbounded `lake build` parallelism OOM-killed 2 of the first 21 modules on an 8 GB machine). Resumable: a module with a passing record is skipped.
usage: verify_batches.py ROOT g|n [P]   -> writes logs/<module>.json {rc, wall_s, cpu_s, peak_rss_kb, src_sha256}; exit 0 only if ALL batches pass and Fin_<g|n> compiles."""
import sys, os, json, time, subprocess, pathlib, hashlib
from concurrent.futures import ThreadPoolExecutor
ROOT = pathlib.Path(sys.argv[1]); tag = sys.argv[2]; P = int(sys.argv[3]) if len(sys.argv) > 3 else 2
LG = ROOT/"logs"; LG.mkdir(exist_ok=True); OL = ROOT/".lake/build/lib/lean/Bat"; OL.mkdir(parents=True, exist_ok=True)
mods = json.load(open(ROOT/f"bat_{tag}.json"))["mods"]
WRAP = ("import resource,subprocess,sys,json,time;t=time.time();"
        "p=subprocess.run(sys.argv[1:],capture_output=True,text=True);r=resource.getrusage(resource.RUSAGE_CHILDREN);"
        "print(json.dumps(dict(rc=p.returncode,wall_s=round(time.time()-t,1),cpu_s=round(r.ru_utime+r.ru_stime,1),peak_rss_kb=r.ru_maxrss,out=(p.stdout+p.stderr)[:300])))")
def run(m):
    rec = LG/f"{m}.json"; src = ROOT/"Bat"/f"{m}.lean"; sha = hashlib.sha256(src.read_bytes()).hexdigest()
    if rec.exists():
        r = json.load(open(rec))
        if r["rc"] == 0 and r["src_sha256"] == sha: return r
    p = subprocess.run([sys.executable, "-I", "-c", WRAP, "lake", "env", "lean", f"Bat/{m}.lean", "-o", str(OL/f"{m}.olean"), "-i", str(OL/f"{m}.ilean")], cwd=ROOT, capture_output=True, text=True)
    r = json.loads(p.stdout.strip().splitlines()[-1]); r.update(name=m, src_sha256=sha); json.dump(r, open(rec, "w")); return r
t0 = time.time()
with ThreadPoolExecutor(P) as ex: res = list(ex.map(run, mods))
bad = [r["name"] for r in res if r["rc"] != 0]
print(f"[{tag}] batches {len(res)} failed {len(bad)} {bad[:5]} wall {round(time.time()-t0)} s; cpu {round(sum(r['cpu_s'] for r in res))} s; max RSS {max(r['peak_rss_kb'] for r in res)//1024} MB", flush=True)
if bad: sys.exit(1)
OF = ROOT/".lake/build/lib/lean"
f = subprocess.run(["lake", "env", "lean", f"Fin_{tag}.lean", "-o", str(OF/f"Fin_{tag}.olean"), "-i", str(OF/f"Fin_{tag}.ilean")], cwd=ROOT, capture_output=True, text=True); (LG/f"Fin_{tag}.out").write_text(f.stdout+f.stderr)
print(f"[{tag}] assembly Fin_{tag}.lean rc={f.returncode}"); print((f.stdout+f.stderr)[:1500]); sys.exit(f.returncode)
