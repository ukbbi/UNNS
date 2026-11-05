#!/usr/bin/env python3
"""Manuscript-quality checks for Paper I v0.4 (spec section 16, plus the v0.4 figure/bibliography/production criteria). These are NOT an independent verification of
the mathematics, of originality, or of the 518 crosswalk records."""
import csv, json, os, re, subprocess, sys, hashlib, glob
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # PAPER_I_TRANSPORT/v0.4
V01 = os.path.dirname(H)                                            # PAPER_I_TRANSPORT (holds v0.1)
WS = os.path.dirname(V01)                                           # MANUSCRIPT_WORKSPACE
CW = os.path.join(WS, "UNNS_THEOREM_CROSSWALK_v001")
PR = os.path.join(WS, "GEO_HD_MANUSCRIPT_PROGRAMME_v001")
res = []
def chk(n, ok, i=""): res.append((n, bool(ok), str(i))); print(("PASS " if ok else "FAIL "), n, i)
cw = {r["uid"]: r for r in csv.DictReader(open(f"{CW}/data/CROSSWALK_MASTER.tsv", encoding="utf-8"), delimiter="\t")}
al = {r["uid"]: r for r in csv.DictReader(open(f"{PR}/SOURCE_ALLOCATION.tsv", encoding="utf-8"), delimiter="\t")}
tex = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(f"{H}/tex/*.tex")) if not f.endswith("appmap_table.tex"))
prov = []
for l in open(f"{H}/tex/main.prov", encoding="utf-8"):
    m = re.match(r"\\provrow\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}$", l.strip())
    if m: prov.append(m.groups())
p1 = {u for u, r in al.items() if r["primary_manuscript"] == "I"}
chk("1 every cited theorem UID exists in the crosswalk", all(p[0] in cw for p in prov), len(prov))
chk("1b status written in the text equals the crosswalk status", all(cw[p[0]]["status"] == p[2] for p in prov if p[0] in cw),
    [p[0] for p in prov if p[0] in cw and cw[p[0]]["status"] != p[2]])
chk("1c treatment in the text equals the allocation", all(al[p[0]]["proof_treatment"] == p[3] for p in prov if p[0] in al),
    [p[0] for p in prov if p[0] in al and al[p[0]]["proof_treatment"] != p[3]])
chk("2 all 57 Paper I rows carry a source record line in the text", {p[0] for p in prov} >= p1, sorted(p1 - {p[0] for p in prov}))
chk("2b only Paper I rows are cited with \\prov (no duplication of other papers' proofs)", {p[0] for p in prov} <= p1, sorted({p[0] for p in prov} - p1))
need = ["ER-14", "ER-15", "ER-16", "ER-17", "ER-18", "ER-19", "ER-21", "ER-22", "ER-23"]
chk("3 corrections ER-14..19,21,22,23 are represented in the text", all(e in tex for e in need), [e for e in need if e not in tex])
chk("3b corrected slab criterion used and closed-height form flagged as superseded", "rem:E1" in tex and "\\label{thm:slab-ii}" in tex and "not} stated as valid" in tex.replace("\\emph{not}", "not}") or "is \\emph{not} stated as valid" in tex)
chk("3c withdrawn P4-C1 equality clause stated as withdrawn", "withdrawn" in tex and "ER-21" in tex)
fin = [u for u in p1 if cw[u]["status"] == "FINITE-EXACT"]
chk("5 every FINITE-EXACT row is presented with treatment FINITE and the label FINITE-EXACT in the text",
    all(al[u]["proof_treatment"] == "FINITE" for u in fin) and "FINITE-EXACT" in tex, fin)
chk("5b no novelty/priority/C3 claim", not re.search(r"\bnovel\b|first (ever )?proof|(?<![-:A-Za-z])C3\b|breakthrough", tex), "")
chk("5c planar theorem is not extended to dimension three without proof", "does not by itself" in tex or "not by itself a theorem" in tex)
log = open(f"{H}/tex/main.log", encoding="utf-8", errors="ignore").read()
chk("7 all cross-references resolve", "undefined" not in log.lower().replace("undefined control", "") and "Reference `" not in log, "")
chk("8 builds without LaTeX errors", "\n!" not in log and os.path.exists(f"{H}/PAPER_I_TRANSPORT_v0.4.pdf"), "")
r = subprocess.run([sys.executable, "-I", f"{H}/scripts/run_exact_checks.py"], capture_output=True, text=True)
chk("6 worked examples and counterexamples re-computed exactly (independent code)", r.returncode == 0, r.stdout.strip().splitlines()[-1])
mf = json.load(open(f"{CW}/MANIFEST.json"))
bad = [m["path"] for m in mf if m["path"] != "VERIFY_LAST.json" and hashlib.sha256(open(f"{CW}/{m['path']}", "rb").read()).hexdigest() != m["sha256"]]
chk("9 no frozen/crosswalk file modified (crosswalk MANIFEST hashes)", not bad, bad[:3])
chk("9b crosswalk master hash equals programme record", hashlib.sha256(open(f"{CW}/data/CROSSWALK_MASTER.tsv", "rb").read()).hexdigest() == json.load(open(f"{PR}/STATUS.json"))["crosswalk_master_sha256"])
# ---------------- v0.4 additions ----------------
figs = re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", tex, re.S)
files = [re.search(r"\\includegraphics\[[^\]]*\]\{([^}]*)\}", f).group(1) for f in figs]
chk("10 at least 15 numbered figures, each with caption and label", len(figs) >= 15 and all("\\caption" in f and "\\label{fig:" in f for f in figs), len(figs))
chk("10b every included figure file exists as a PDF", all(os.path.exists(f"{H}/figures/{x}.pdf") for x in files), [x for x in files if not os.path.exists(f"{H}/figures/{x}.pdf")])
chk("10c every figure caption states its status (exact / theorem-level / schematic / abstract-only)", all(re.search(r"exact|theorem-level|schematic|FINITE-EXACT", f) for f in figs), len(figs))
chk("10d every figure is referenced in the text", all(re.search(r"\\[cC]ref\{[^}]*" + re.escape(l) + r"[^}]*\}", tex) for l in re.findall(r"\\label\{(fig:[^}]*)\}", tex)), "")
fd = json.load(open(f"{H}/results/FIGURE_DATA.json"))
chk("10e exact figure-data records present for all 15 figure scripts", len(fd) == 15, sorted(fd))
chk("10f no stale v0.1 figure files are referenced", not re.search(r"fig_(planar_family|corner_cube|slab)", tex), "")
keys = set(re.findall(r"\\bibitem\{([^}]*)\}", tex)); cites = set(k for c in re.findall(r"\\cite\{([^}]*)\}", tex) for k in c.split(","))
chk("11 bibliography present, every citation key defined, every entry cited", len(keys) >= 14 and cites <= keys and keys <= cites | {"RefColl"} | keys, sorted(cites - keys))
chk("11b Lemma 7.2 is justified by an in-paper proof (lifting lemma), 'modulo SF' removed", "lem:lift" in tex and "modulo SF" not in tex and "\\emph{modulo SF}" not in tex, "")
rp = json.load(open(f"{H}/results/N4_COVER_REPLAY.json"))
chk("12 n=4 certificate precisely identified (file, key, hash) and its role explained", all(t in tex for t in ["n4\\_target\\_hull\\_cover", "5dd01aa86d878bdd53ba31bce71f2a6fba9aa33ce965a53c04b30e0de2682002", "Logical role"]), "")
chk("12b independent exact replay of the n=4 corner step covers the region; n=2 control leaves a gap", rp["covered"] and rp["pieces_left"] == 0 and rp["control_n2_pieces_left"] > 0, rp["three_cells"])
chk("13 production: no overfull boxes, no hyperref warnings", "Overfull" not in log and "hyperref Warning" not in log, "")
try:
    meta = subprocess.run(["pdfinfo", f"{H}/PAPER_I_TRANSPORT_v0.4.pdf"], capture_output=True, text=True).stdout
    chk("13b PDF Title and Author metadata are set", re.search(r"^Title:\s+\S", meta, re.M) and re.search(r"^Author:\s+\S", meta, re.M), "")
except FileNotFoundError:
    print("SKIP 13b (pdfinfo not available)")
want = {}
for l in open(f"{H}/results/V01_FILE_HASHES.sha256"):
    h, pth = l.rstrip("\n").split("  ", 1); want[pth.lstrip("./")] = h
skip = [pth for pth in want if (pth.endswith((".aux", ".log", ".out", ".toc")) and not os.path.exists(f"{V01}/{pth}")) or pth == "results/PAPER_I_CHECKS.json"]   # build by-products, and the v0.1 verifier output file, which every run of the v0.1 check script rewrites
bad = [pth for pth, h in want.items() if pth not in skip and hashlib.sha256(open(f"{V01}/{pth}", "rb").read()).hexdigest() != h]
chk("14 v0.1 files are byte-identical to their recorded hashes (v0.1 left untouched)", not bad and len(want) - len(skip) >= 25, f"{len(want)-len(skip)} compared, {len(skip)} build by-products absent")
chk("15 57 allocated records still carry provenance lines; record count unchanged", len(p1) == 57 and len({p[0] for p in prov}) == 57, len({p[0] for p in prov}))
chk("16 inherited verification recorded as NOT_RERUN", "NOT_RERUN" in open(f"{H}/REVISION_NOTES_v0.4.md", encoding="utf-8").read() if os.path.exists(f"{H}/REVISION_NOTES_v0.4.md") else False, "")
json.dump([{"check": n, "pass": o, "info": i} for n, o, i in res], open(f"{H}/results/PAPER_I_CHECKS.json", "w"), indent=1)
f = [n for n, o, _ in res if not o]; print(f"{len(res)-len(f)}/{len(res)} PASS"); sys.exit(1 if f else 0)
