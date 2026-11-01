#!/usr/bin/env python3
"""GEO-HD-1 / HD-0 / E0 — build BASELINE/SOURCE_LOCK.json and BASELINE/SOURCE_OVERLAP_MATRIX.tsv.

Inputs
  --repo        a git clone of https://github.com/ukbbi/UNNS (read only; blobs are read with `git show`)
  --local-hashes JSON {relative local path: sha256|null} measured on the local source tree
Outputs
  SOURCE_LOCK.json, SOURCE_OVERLAP_MATRIX.tsv (UTF-8, LF)
Nothing is written to the repository.
"""
import argparse
import csv
import hashlib
import json
import subprocess
import sys

GEO_I = "343f9aef2b6697466058165c5fc2ddf0f00e882b"
FOUND = "bb8b12d753c600c597feb00df17fe139c7cc65fa"
VOLS = "fefa7910c807a5fdac90980749a5d7993e3ec0ca"       # commit that first adds the Vol. I / II manuscripts
UNNS = "projects/UNNS_MATH_FOUNDATIONS"
GEO = "projects/UNNS_Higher-Dimensional Geometry"

# key -> (local path relative to UNNS_ENTANGLE_I, github path or None, commit that introduces the github blob)
FILES = {
    "VOL1_TEX": ("Manuscript/UNNS_Math_Foundations_Vol_I/UNNS_Math_Foundations_Vol_I.tex", f"{UNNS}/Manuscript/UNNS_Math_Foundations_Vol_I/UNNS_Math_Foundations_Vol_I.tex", VOLS),
    "VOL1_PDF": ("Manuscript/UNNS_Math_Foundations_Vol_I/UNNS_Math_Foundations_Vol_I.pdf", f"{UNNS}/Manuscript/UNNS_Math_Foundations_Vol_I/UNNS_Math_Foundations_Vol_I.pdf", VOLS),
    "VOL1_XW": ("Manuscript/UNNS_Math_Foundations_Vol_I/THEOREM_CROSSWALK.tsv", f"{UNNS}/Manuscript/UNNS_Math_Foundations_Vol_I/THEOREM_CROSSWALK.tsv", VOLS),
    "VOL2_CH1": ("Manuscript/UNNS_Math_Foundations_Vol_II/tex/ch1.tex", f"{UNNS}/Manuscript/UNNS_Math_Foundations_Vol_II/tex/ch1.tex", VOLS),
    "VOL2_CH2": ("Manuscript/UNNS_Math_Foundations_Vol_II/tex/ch2.tex", f"{UNNS}/Manuscript/UNNS_Math_Foundations_Vol_II/tex/ch2.tex", VOLS),
    "VOL2_REG": ("Manuscript/UNNS_Math_Foundations_Vol_II/registry.json", f"{UNNS}/Manuscript/UNNS_Math_Foundations_Vol_II/registry.json", VOLS),
    "REG_CSV": ("MATH_FOUNDATIONS_REGISTRY/registry.csv", None, None),
    "SEL2_RES": ("SELECT-II/RESULTS.md", f"{UNNS}/sources/SELECT-II/RESULTS.md", FOUND),
    "SEL2_V002": ("SELECT-II/v002/SELECT2_note.md", f"{UNNS}/sources/SELECT-II/v002/SELECT2_note.md", FOUND),
    "SEL2_V002B": ("SELECT-II/v002b/SELECT2B_note.md", f"{UNNS}/sources/SELECT-II/v002b/SELECT2B_note.md", FOUND),
    "FLD_V001": ("FIELD-I/FIELD-I v001/FIELD1_note.md", f"{UNNS}/sources/FIELD-I/v001/FIELD1_note.md", FOUND),
    "FLD_V004": ("FIELD-I/FIELD-I_v004/THEOREMS.md", f"{UNNS}/sources/FIELD-I/v004/THEOREMS.md", FOUND),
    "FLD_V005": ("FIELD-I/FIELD-I v005/THEOREMS.md", f"{UNNS}/sources/FIELD-I/v005/THEOREMS.md", FOUND),
    "FLD_V006": ("FIELD-I/FIELD-I_v006/THEOREMS.md", f"{UNNS}/sources/FIELD-I/v006/THEOREMS.md", FOUND),
    "FLD_V012": ("FIELD-I/FIELD-I_v012/THEOREMS.md", f"{UNNS}/sources/FIELD-I/v012/THEOREMS.md", FOUND),
    "GEO2": ("UNNS_Higher-Dimensional Geometry/GEO_I_v002/MATHEMATICS.md", f"{GEO}/GEO_I_v002/MATHEMATICS.md", GEO_I),
    "GEO3": ("UNNS_Higher-Dimensional Geometry/GEO_I_v003/MATHEMATICS.md", f"{GEO}/GEO_I_v003/MATHEMATICS.md", GEO_I),
    "GEO4": ("UNNS_Higher-Dimensional Geometry/GEO_I_v004/MATHEMATICS.md", f"{GEO}/GEO_I_v004/MATHEMATICS.md", GEO_I),
    "GEO11": ("UNNS_Higher-Dimensional Geometry/GEO_I_v011/THEOREM_REGISTRY.tsv", f"{GEO}/GEO_I_v011/THEOREM_REGISTRY.tsv", GEO_I),
    "GEO12": ("UNNS_Higher-Dimensional Geometry/GEO_I_v012/MATHEMATICS.md", f"{GEO}/GEO_I_v012/MATHEMATICS.md", GEO_I),
    "GEO12R": ("UNNS_Higher-Dimensional Geometry/GEO_I_v012/THEOREM_REGISTRY.tsv", f"{GEO}/GEO_I_v012/THEOREM_REGISTRY.tsv", GEO_I),
    "PAPA": ("UNNS_Higher-Dimensional Geometry/Manuscripts/PAPER_A_manuscript_v1_2.zip", None, None),
    "PAPB": ("UNNS_Higher-Dimensional Geometry/Manuscripts/PAPER_B_manuscript_v001.zip", None, None),
}
EXTRA_LOCAL = {"PAPA_P1": ("ZIPMEMBER:PAPER_A_manuscript_v1_2/tex/part1.tex", None, None)}

COLS = ["row_id", "hd_claim_id", "hd_claim", "overlap_status", "relation", "source_record", "source_release",
        "source_statement", "hypotheses_scope", "source_status", "local_path", "local_sha256", "github_path",
        "github_commit", "github_match", "overlap_note"]


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True)


def blob(repo, commit, path):
    r = git(repo, "show", f"{commit}:{path}")
    return r.stdout if r.returncode == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def lf(b):
    return b.replace(b"\r\n", b"\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--local-hashes", required=True)
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    local = json.load(open(a.local_hashes))

    lock = {"spec": "GEO_HD_1_SPEC_v003", "repository": "https://github.com/ukbbi/UNNS (read only; no write performed)",
            "commits": {
                "geo_i_pinned": {"sha": GEO_I, "role": "GEO-I v001-v012 pinned tree; HEAD of the cloned default branch when locked"},
                "foundations_sources": {"sha": FOUND, "role": "UNNS_MATH_FOUNDATIONS reference collection (sources/: SELECT-I/II incl. v002b, FIELD-I v001-v012)"},
                "foundations_manuscripts": {"sha": VOLS, "role": "first commit containing Volume I and Volume II manuscripts"}},
            "files": {}}
    rows = []
    gh = {}
    for key, (lp, gp, c0) in {**FILES, **EXTRA_LOCAL}.items():
        entry = {"local_path": lp.replace("ZIPMEMBER:", "(zip member) "), "local_sha256": local.get(lp), "github_path": gp,
                 "github_introduced_in": c0, "github_blob_git_id": None, "github_sha256_at_pinned": None, "github_match": "local_only"}
        if gp:
            b = blob(a.repo, GEO_I, gp)
            b0 = blob(a.repo, c0, gp)
            if b is None:
                entry["github_match"] = "missing_at_pinned_commit"
            else:
                entry["github_blob_git_id"] = git(a.repo, "rev-parse", f"{GEO_I}:{gp}").stdout.decode().strip()
                entry["github_sha256_at_pinned"] = sha(b)
                entry["same_blob_at_introducing_commit"] = (b0 == b)
                if local.get(lp) is None:
                    entry["github_match"] = "github_only"
                elif local[lp] == sha(b):
                    entry["github_match"] = "identical"
                else:
                    entry["github_match"] = "differs"
        lock["files"][key] = entry
        gh[key] = entry

    # R: rows -------------------------------------------------------------
    def S(key):  # (local_path, local_sha, github_path, commit, match)
        e = gh[key]
        return (e["local_path"], e["local_sha256"] or "", e["github_path"] or "none", e["github_introduced_in"] or "none", e["github_match"])

    ROWS = []

    def add(claim, status, relation, src, release, stmt, hyp, sstat, key, note, claim_id, claim_txt):
        lp, ls, gp, gc, gm = S(key) if key else ("", "", "", "", "")
        ROWS.append([f"R{len(ROWS) + 1:02d}", claim_id, claim_txt, status, relation, src, release, stmt, hyp, sstat, lp, ls, gp, gc, gm, note])

    # --- HD-BRIDGE-01
    c, t = "HD-BRIDGE-01", "Occurrence section O_x is in bijection with the exponent-coordinate fibre via d=N+1 (inverse N=d-1, M=a(d-1)/(b d^2))"
    add(c, "INHERITED", "duplicates", "F.T1 = Vol. I Thm 1.2", "FIELD-I v001", "For reduced x=a/b, occurrences correspond to {d>=2: d^2|a, d=1 mod b}; N=d-1, M=(a/d^2)(d-1)/b.", "Positive rationals; rule S_N(M)=M(N+1)^2/N", "PROVED+CHECKED", "VOL1_TEX", "Exactly the stated bijection; no extension claimed.", c, t)
    add(c, "INHERITED", "duplicates", "F.T22 = Vol. I Thm 1.7", "FIELD-I v004", "With a=s^2 t (t squarefree): D(a/b)={d|s: d>=2, d=1 mod b}; the fibre depends only on (s,b).", "", "PROVED+CHECKED", "VOL1_TEX", "Source of the square-root part s used throughout GEO-HD.", c, t)
    add(c, "INHERITED", "related", "Vol. I Cor. 1.3", "Foundations Vol. I", "R(m)=prod_p(floor(v_p(m)/2)+1)-1; R(m)=0 iff m squarefree.", "integers m", "PROVED (Scope A0)", "VOL1_TEX", "Integer fibre multiplicity; used for the source test in the atlas.", c, t)
    add(c, "INHERITED", "related", "GEO-I v002 §1 definitions", "GEO-I v002", "Exponent coordinates alpha, box B, character chi_b(alpha)=prod p_i^{alpha_i} mod b, fibre F_x.", "reduced x=a/b; active primes q_i=floor(e_i/2)>=1", "definition", "GEO2", "Coordinate model used by the atlas fibre geometry (b=1 here).", c, t)
    # --- transport
    cc, tt = "HD-TR-01", "s(m)=g*c(m,N) and s(t)=g*(N+1) on every SELECT-II edge m --N--> t (g=gcd(s(m),s(t)); c(m,N)=prod_{p|N}p^{l_p})"
    add(cc, "NEW_CANDIDATE", "none found", "searched: S2.1-S2.16, F.T5, F.T22, GEO-I v002 Prop D1", "SELECT-II / FIELD-I / GEO-I v002", "No record states how s(m) or D(m) changes along a SELECT-II edge.", "", "-", "SEL2_RES", "Elementary valuation arithmetic; no priority claim (spec §28 prior-art audit still owed).", cc, tt)
    add(cc, "NEW_CANDIDATE", "partial overlap", "GEO-I v002 Prop D1 (A2)", "GEO-I v002", "With v(m')=v(m)-v(N)+2v(N+1): k(m')-k(m) in [-omega(N), omega(N+1)]; geometry change along SELECT-II edges is not monotone (36->162, 72->384); Delta d_amb statistics over 3,124 edges.", "SELECT-II integer edges, endpoints <=5000", "PROVED + CHECKED", "GEO2", "D1 bounds the change in the number of active primes; the factorization gives the exact index sets (lost primes divide N, gained primes divide N+1). Consistent with D1, strictly more precise.", cc, tt)
    cc, tt = "HD-TR-02", "D(m) subset D(t) iff c(m,N)=1 iff every p|N has v_p(N)=1 and v_p(m) odd"
    add(cc, "NEW_CANDIDATE", "none found", "searched: S2.*, F.T5 (T_q:(k,d)->(k/q^2,dq), a different map inside one rational fibre)", "SELECT-II / FIELD-I", "No record gives a preservation criterion for D along SELECT-II edges.", "", "-", "FLD_V001", "Corollary of HD-TR-01. F.T5 concerns a different map and is not a duplicate.", cc, tt)
    cc, tt = "HD-TR-03", "N+1 = s(t)/gcd(s(m),s(t)): the edge label is recoverable from the square-root parts of the two endpoint fibres"
    add(cc, "REFORMULATION", "extends", "S2.3 = Vol. I Thm 5.5", "SELECT-II v001", "For an edge m=kN -> t=k(N+1)^2: gcd(m,t)=k, N=m/gcd(m,t); the edge test is exact from the two values.", "self-iteration convention", "PROVED", "VOL1_TEX", "Label recovery from the VALUES is inherited. The new form uses only s(m), s(t) (fibre data) - a variant, not a new theorem.", cc, tt)
    cc, tt = "HD-TR-04", "Every SELECT-II edge m -> t gains an index: D(t) \\ D(m) is nonempty (s(t) itself is new)"
    add(cc, "NEW_CANDIDATE", "none found", "searched: S2.2 (sources = squarefree integers; every integer has a squarefree ancestor)", "SELECT-II v001", "Related but distinct: ancestry/source structure, not index gain along edges.", "", "PROVED", "SEL2_RES", "Corollary of HD-TR-01 (s(t)=g(N+1)>g). Elementary.", cc, tt)
    cc, tt = "HD-TR-05", "Retained/lost/gained index counts tau(g)-1, tau(s(m))-tau(g), tau(s(t))-tau(g)"
    add(cc, "NEW_CANDIDATE", "none found", "searched: S2.*, F.*", "-", "No record counts index transport along edges.", "", "-", "SEL2_RES", "Divisor counting on top of HD-TR-01; elementary.", cc, tt)
    # --- counterexample / trivial lattice
    cc, tt = "HD-CNT-01", "b=1, k>=2, coordinate-cell grammar: U_Q = {u in [0,Q]: max u_i >= 1} is a proper subset of conv(F_Q) = {u: sum u_i >= 1} for every integer box Q_i>=1"
    add(cc, "REPLICATION", "duplicates (k=2)", "GEO-I v004 §1.5 (d=1) [P]", "GEO-I v004", "Gamma=Z^2, Graver moves +-e_i; U is the union of unit squares of the box except the corner square [0,1]^2 (plus two edges); contractible; 'Not conv(F): the triangle (1,0),(0,1),(1,1) of the hull near the origin is not covered, which is why S1 requires d>=2'.", "k=2, d=1", "PROVED [P]", "GEO4", "The planar origin-deletion non-coverage is already proved in v004. HD-CNT-01 adds only the trivial k-dimensional form.", cc, tt)
    add(cc, "REPLICATION", "duplicates (cell union)", "GEO-I v002 Prop 2", "GEO-I v002", "For b=1, K_axis(x) is homotopy-equivalent to a point; its realization is Y={x in [0,q]: some x_i>=1}.", "b=1, all k", "PROVED + CHECKED", "GEO2", "Y is exactly U_Q; hull comparison is the only addition.", cc, tt)
    cc, tt = "HD-ERR-01", "Paper A v1.2 Remark 'The case d=1' wrongly asserts that coordinate parallelograms span all of H_Q when both box sides are >=2"
    add(cc, "COUNTEREXAMPLE", "contradicts statement (not a theorem)", "Paper A v1.2 tex/part1.tex, Remark rem:d1", "Paper A v1.2", "'The cell construction is trivial in this case (all of H_Q is spanned by coordinate parallelograms, if the box has both sides at least 2) ...'", "d=1; outside the stabilization theorem (d>=2)", "remark, no proof", "PAPA", "x=1296, box (2,2): (1/2,1/2) lies in conv(F) but in no admissible parallelogram. The theorem (d>=2) is unaffected. GEO-I v004 §1.5 already states the correct fact; the erratum should cite it.", cc, tt)
    # --- parity
    cc, tt = "HD-PAR-01", "Lambda_k={z in Z^k: sum z_i even} arises as the relation lattice of x_k=(p_1..p_k)^4/3 with p_i = 2 mod 3, box q=(2,..,2)"
    add(cc, "INHERITED", "duplicates", "GEO-I v004 parity-lattice family (b=3, residues (2,..,2))", "GEO-I v004", "Parity lattice Lambda_4 = {sum alpha_i even} (b=3, residues (2,2,2,2)); Lambda_3: first obstruction at (2,1,1); Lambda_4: new non-embedded box (1,1,1,1).", "k=3,4; exhaustive audits", "CHECKED [C] (template atlas for k=4 UNAVAILABLE)", "GEO4", "Archived. The 13-point (k=3) and 40-point (k=4) fibres are regression benchmarks (spec §2.2).", cc, tt)
    cc, tt = "HD-PAR-02", "Graver basis of the parity lattice is {+-2e_i} u {+-e_i +-e_j}"
    add(cc, "REFORMULATION", "classical", "GEO-I v003 Thm T2(a/c) pattern; Graver 1975; D_k root lattice", "GEO-I v003/v004", "Graver bases of such lattices computed by Lemma 0 (box bound); classical.", "", "PROVED (classical)", "GEO3", "Standard fact on the D_k lattice; no novelty claim.", cc, tt)
    cc, tt = "HD-CELL-01", "Coverage U=conv(F), face-to-face embedding and topology of the Graver-cell union for k=3,4 under the declared grammar"
    add(cc, "OPEN", "partial overlap", "GEO-I v004 Thm T-FIN / templates; v003 Thm T2", "GEO-I v003-v004", "Embedding obstructions classified by finite templates; Klein-four and parity classes; coverage for k>=3 is not addressed.", "k>=3", "CHECKED/PROVED (embedding); coverage not stated", "GEO4", "Embedding is archived; hull coverage for k>=3 and cross-fibre behaviour are not found in the sources. Paper A explicitly excludes k>=3. Primary open target.", cc, tt)
    add(cc, "OPEN", "scope boundary", "Paper A v1.2 Question 'Three or more active primes'; G12-O1", "Paper A v1.2 / GEO-I v012", "Planar stabilization theorem G12-T8 is for d>=2, unit s, Q>=(d,d), Q!=(d,d); global organisation (G12-O1) OPEN.", "k=2", "PROVED+CHECKED (k=2); OPEN (global)", "GEO12R", "No k>=3 theorem is inherited.", cc, tt)
    # --- histories
    cc, tt = "HD-HIST-01", "Distinct histories can share initial state, endpoint and length (1-4-16-72 vs 1-4-18-72); the complete histories of 72 are exactly four"
    add(cc, "REPLICATION", "duplicates", "S2.12 = Vol. I Thm 6.6 (B2)", "SELECT-II v002b", "H(72)=4 with histories 1-4-18-72, 1-4-16-72, 3-16-72, 10-72 versus R(72)=3; H(t)>=max(1,R(t)); route does not determine history (C4).", "self-iteration graph; t<=3000 enumeration, <=20000 data", "PROVED+CHECKED", "SEL2_V002B", "Reproduced exactly in E1 (FR-3). Not a new result.", cc, tt)
    cc, tt = "HD-ATLAS-02", "The last-edge map from complete histories of t onto O_t is surjective and not injective (72: 4 histories, 3 occurrences)"
    add(cc, "REPLICATION", "duplicates", "S2.12 / v002b C4 (tower value -> route -> history strict)", "SELECT-II v002b", "Route (8,3) in F(72) has predecessor 16 with two histories; 346 routes with t<=3000 have a predecessor with >=2 histories.", "", "PROVED+CHECKED", "SEL2_V002B", "Same content stated as a map between typed sets.", cc, tt)
    cc, tt = "HD-ATLAS-03", "Endpoint, (endpoint,length) and last-edge projections each identify distinct histories of 72; only source+label sequence (or the full state sequence) separates all four"
    add(cc, "REPLICATION", "duplicates", "S2.13 = Vol. I Thm 6.8 (Markov no-go) with S2.12", "SELECT-II v002b", "Continuations of a history depend only on its endpoint; history information is retrospective only.", "t<400, depth 3", "PROVED+CHECKED", "SEL2_V002B", "Atlas tabulates the collision classes; no new theorem.", cc, tt)
    cc, tt = "HD-CONF-01", "Minimal common successors of the predecessors 96, 27 of the routes (16,7),(1,28) of 784 are {432,784} up to 784 and additionally 3750 up to 5000"
    add(cc, "NEW_CANDIDATE", "extends data", "S2.15 = Vol. I Prop 6.12; v002b C7 (data)", "SELECT-II v002b", "t is a minimal common successor of the predecessors; second incomparable merge for 9/1277 pairs (t=784: {432,784}).", "t<=3000", "PROVED+CHECKED / DATA", "SEL2_V002B", "The part <=784 reproduces C7. The element 3750 lies beyond t and is a finite bounded observation, not a theorem; relates to open item O.S2b.", cc, tt)
    cc, tt = "HD-HIST-02", "A new arithmetic-specific retrospective invariant of histories/merges (beyond path unfolding)"
    add(cc, "OPEN", "partial overlap", "S2.16 (verdict); O.S2b; O.S2c; S2.14", "SELECT-II v002b", "Only retrospective information exists; J_pred separation is leakage; double-confluence pattern and relation to D open.", "", "INTERPRETATION / OPEN", "SEL2_V002B", "Primary open target. Falsification F6 applies (no forward-predictive claim).", cc, tt)
    # --- FIELD
    cc, tt = "HD-FIELD-01", "C-orbits satisfy D(x) subset D(C(x)); regime I (G=1) eventually satisfies x_{n+3}=4x_n"
    add(cc, "INHERITED", "duplicates", "F.T31 = Vol. II Thm 1.3", "FIELD-I v005", "D(x_n) subset D(x_{n+1}) and G_{n+1}|G_n.", "scope C (collective map C(x)=x+L^2/G)", "PROVED", "VOL2_CH1", "Scope C only; not a SELECT-II statement.", cc, tt)
    add(cc, "INHERITED", "duplicates", "F.L3 = Vol. II Thm 2.4 (with F.T32 = Thm 2.3)", "FIELD-I v006 / v005", "For G=1: x_{n+3}=4x_n, gamma(x_n)=t_n in {1,2,3}, s_{n+3}=2s_n.", "regime I; entry time N; 'no three-step law before N'", "PROVED", "VOL2_CH2", "Reproduced numerically for 72 (72,108,144,288,432,576,1152,...).", cc, tt)
    cc, tt = "HD-T2-FIELD", "Cell/edge/embedding transport along the inclusion F_x -> F_{C(x)} (spec HD-T2a-d)"
    add(cc, "OPEN", "partial overlap", "GEO-I v002 Cor A1 / D2 (C-scope)", "GEO-I v002", "Along an eventual regime x_{n+P}=p^{2s}x_n, b, S, T are constant; component counts quasi-linear (p in T) or eventually periodic (p in S); verified only on the g=11 orbit.", "eventual regime", "COROLLARY (C-scope), verified on one orbit", "GEO2", "Component counts of K_axis are archived for one orbit; vertex-to-cell transport is not.", cc, tt)
    cc, tt = "HD-T4-PERSIST", "Geometric organisation of collective persistence, carries and G-reduction (spec HD-T4)"
    add(cc, "OPEN", "partial overlap", "F.T31, F.T34-F.T36, carry theorems (Vol. II Ch. 2-5)", "FIELD-I v005-v012", "Plateau, carry, scheduler and eventual-scaling theorems for the explicit map C.", "scope C", "PROVED / PROVED+CHECKED", "VOL2_CH2", "Numerical/dynamical facts are inherited; their geometric image is not.", cc, tt)
    # --- atlas
    cc, tt = "HD-ATLAS-01", "The typed atlas (values, occurrences, edges, incoming labels, complete histories, fibre coordinates) is well defined: every connecting map has a declared domain, codomain and a verified bijection/surjection property"
    add(cc, "REFORMULATION", "composition", "Vol. I Thm 1.2, Thm 5.3 (S2.5), Def. 6.1; GEO-I v002 §1", "Foundations Vol. I / GEO-I v002", "Occurrence <-> D(x) <-> F_x; occurrence <-> incoming edge; complete histories of t.", "integer states (b=1) for the SELECT-II part", "PROVED / PROVED+CHECKED", "VOL1_TEX", "Organisational bookkeeping of inherited maps (see BASELINE/HD0_CONNECTING_MAPS.md). No new theorem.", cc, tt)

    with open(a.out_dir + "/SOURCE_OVERLAP_MATRIX.tsv", "w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(COLS)
        for r in ROWS:
            w.writerow([str(x).replace("\t", " ").replace("\n", " ") for x in r])
    with open(a.out_dir + "/SOURCE_LOCK.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(lock, fh, indent=1, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    # summary
    import collections
    st = collections.Counter(r[3] for r in ROWS)
    ids = collections.OrderedDict()
    for r in ROWS:
        ids.setdefault(r[1], r[3])
    print("rows", len(ROWS), "claims", len(ids))
    print("row statuses", dict(st))
    print("claim statuses", collections.Counter(ids.values()))
    mm = collections.Counter(e["github_match"] for e in lock["files"].values())
    print("github_match", dict(mm))


if __name__ == "__main__":
    main()
