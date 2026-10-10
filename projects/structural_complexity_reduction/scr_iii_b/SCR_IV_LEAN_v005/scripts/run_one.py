#!/usr/bin/env python3
"""usage: run_one.py ROOT FILE LOGDIR -> kernel-check one prefix theorem file; writes <name>.json {rc, wall_s, cpu_s, peak_rss_kb, out}. (peak RSS of the child lean process)"""
import sys, os, json, time, subprocess, resource, pathlib
ROOT, F, LD = sys.argv[1:4]; os.makedirs(LD, exist_ok=True); name = pathlib.Path(F).stem
t0 = time.time(); r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
p = subprocess.run(["lake", "env", "lean", F], cwd=ROOT, capture_output=True, text=True)
# RUSAGE_CHILDREN maxrss is a running max over this process's children: this python process has exactly one child, so it is that child's peak
r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
json.dump(dict(name=name, rc=p.returncode, wall_s=round(time.time()-t0, 2), cpu_s=round(r1.ru_utime+r1.ru_stime-r0.ru_utime-r0.ru_stime, 2), peak_rss_kb=r1.ru_maxrss, out=(p.stdout+p.stderr)[:400]), open(f"{LD}/{name}.json", "w"))
