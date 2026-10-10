// SCR-III-B PREFLIGHT_v009 -- gate binary: B0, G1, G2, B1 with a COMMON physical reference E0, plus E0 certification, null-gap and grammar-count tools.
// Usage:  prereg_gate <input> <mode> <W> <tau> [--e0 E0] [--z2] [--dump f] [--audit f] [--protected f] [--synthetic] [--tag t] [--unblind-after-freeze] [--cap N]
//   modes: b0 g1 g2 b1            complete target-set task with threshold Ecut = E0 + W + tau (E0 REQUIRED, identical for every solver)
//          cert_b0 cert_b1        certify the global minimum E0 (one-time cost, reported separately)
//          nullgap                Delta = min_{s not in S_G}(H(s)-E0)  (excitation-gap mode: guarded exactly like W>0 on n>16)
//          gcount gscan           grammar-only survivor counting (no Hamiltonian): constructive DFS / full nominal scan
//          boundtest <file>       B1 lower-bound values for listed partial assignments
// Candidate order (all deterministic, outcome-independent): B0 Gray code over spins 0..n-1 (bit ctz(t) flips); G1 ascending state id;
//   G2 islands in vertex-completion order (first appearance in the vertex list), value 0 before 1; B1 spin index order 0..n-1, lower-energy value first.
#include "gate_common_v009.hpp"

static double SUFFIX_ABS[42];
static void init_suffix() { for (int d = 0; d <= n + 1; ++d) SUFFIX_ABS[d] = 0; for (int d = n - 1; d >= 0; --d) { double s = 0; for (int k = d + 1; k < n; ++k) s += fabs(Kf[d][k]); SUFFIX_ABS[d] = SUFFIX_ABS[d + 1] + s; } }

typedef vector<pair<u64, double>> Cands;
static void finalize(const Cands& c, vector<u64>& out) {
    double t0 = now(); out.clear();
    for (auto& p : c) if (decide_scan(p.first, p.second, EPS_GRAY)) out.push_back(p.first);
    expand_z2(out); sort(out.begin(), out.end()); T_final += now() - t0;
}
// ------------------------------------------------------------------ Gray-code scan engine (B0, cert_b0): retains states with scan energy <= thr
static void gray_scan(Cands* cand, double thr, bool running, double& minE, u64& argmin) {
    int nb = n - (O.z2 ? 1 : 0); u64 N0 = 1ULL << nb; vector<double> h(n), sp(n, -1.0); double E = 0; u64 g = 0;
    auto resync = [&](u64 gg) {
        for (int i = 0; i < n; ++i) sp[i] = ((gg >> i) & 1) ? 1.0 : -1.0;
        for (int i = 0; i < n; ++i) { double a = 0; for (int j = 0; j < n; ++j) a += Kf[i][j] * sp[j]; h[i] = a; }
        double e = 0; for (int p = 0; p < npairs; ++p) e += PK[p] * (sp[PI[p]] * sp[PJ[p]]); E = e; C.resyncs++; C.pair_ops += (u64)n * n + npairs; };
    resync(0); minE = E; argmin = 0; C.states_visited = 1;
    if (cand && (running || E <= thr)) { cand->push_back({0, E}); C.candidates_kept++; }
    for (u64 t = 1; t < N0; ++t) {
        int k = __builtin_ctzll(t); g ^= (1ULL << k);
        if ((t & (GRAY_RESYNC - 1)) == 0) { sp[k] = -sp[k]; resync(g); }
        else { double d = -2.0 * sp[k]; E += d * h[k]; for (int j = 0; j < n; ++j) h[j] += Kf[j][k] * d; sp[k] = -sp[k]; C.field_updates++; C.pair_ops += n + 1; }
        C.states_visited++; C.comparisons++;
        if (E < minE) {
            minE = E; argmin = g;
            if (running && cand) { size_t k = 0; for (size_t i = 0; i < cand->size(); ++i) if ((*cand)[i].second <= minE + EPS_GRAY) (*cand)[k++] = (*cand)[i]; cand->resize(k); }
        }
        if (cand && (running ? E <= minE + EPS_GRAY : E <= thr)) { cand->push_back({g, E}); C.candidates_kept++; }
    }
}
static void run_b0(vector<u64>& out, double& own_min) {
    double t0 = now(); Cands cand; double minE; u64 am;
    gray_scan(&cand, Ecut_d + EPS_GRAY, false, minE, am); T_trav += now() - t0;
    double own = energy_direct(am); own_min = own; ref_check_full_space(own, !cand.empty());
    finalize(cand, out);
}
static int run_cert_b0(vector<u64>& out, double& E0) {
    double t0 = now(); Cands cand; double minE; u64 am;
    gray_scan(&cand, 0, true, minE, am); T_trav += now() - t0; t0 = now();
    double best = 1e300; vector<pair<u64, double>> dir;
    for (auto& p : cand) { double e = energy_direct(p.first); dir.push_back({p.first, e}); best = min(best, e); }
    out.clear(); for (auto& p : dir) if (p.second <= best + O.tau) out.push_back(p.first);
    expand_z2(out); sort(out.begin(), out.end()); E0 = best; T_final += now() - t0; return 0;
}
// ------------------------------------------------------------------ G1
static void run_g1(vector<u64>& out, double& own_min) {
    int nb = n - (O.z2 ? 1 : 0); u64 N0 = 1ULL << nb; double t0 = now(); vector<u64> surv;
    for (u64 s = 0; s < N0; ++s) { C.states_visited++; if (grammar_counted(s)) surv.push_back(s); }
    T_gram += now() - t0; C.materialized = surv.size(); t0 = now(); out.clear(); own_min = 1e300;
    for (u64 s : surv) { double E; int m = decide_direct(s, &E); if (E < own_min) own_min = E; if (m) out.push_back(s); }
    T_energy += now() - t0; expand_z2(out); sort(out.begin(), out.end());
}
// ------------------------------------------------------------------ G2
static vector<int> g2_order; static vector<vector<int>> g2_check; static vector<vector<double>> g2_f; static Cands g2_cand; static double g2_min = 1e300; static u64 g2_arg = 0;
static void g2_rec(int pos, u64 st, double E) {
    if (pos == (int)g2_order.size()) { C.leaves++; C.materialized++; if (E < g2_min) { g2_min = E; g2_arg = st; } if (E <= Ecut_d + EPS_GRAY) { g2_cand.push_back({st, E}); C.candidates_kept++; } return; }
    int isl = g2_order[pos];
    for (int bit = 0; bit < 2; ++bit) {
        if (pos == 0 && O.z2 && bit == 1) continue;
        double sg = bit ? 1.0 : -1.0; u64 s2 = st | ((u64)bit << isl); C.nodes++;
        double E2 = E + sg * g2_f[pos][isl];
        vector<double>& fn = g2_f[pos + 1]; const vector<double>& fo = g2_f[pos];
        for (int p2 = pos + 1; p2 < (int)g2_order.size(); ++p2) { int j = g2_order[p2]; fn[j] = fo[j] + Kf[j][isl] * sg; }
        C.field_updates++; C.pair_ops += (g2_order.size() - pos - 1) + 1;
        bool ok = true;
        for (int v : g2_check[pos]) { C.vertex_checks++; if (__builtin_popcount(((u32)s2 ^ NM[v]) & IM[v]) != 2) { ok = false; C.pruned++; break; } }
        if (ok) g2_rec(pos + 1, s2, E2);
    }
}
static void g2_setup() {
    vector<char> seen(n, 0); g2_check.assign(n + 1, {}); g2_order.clear();
    for (int v = 0; v < nv; ++v) { for (int i = 0; i < n; ++i) if ((IM[v] >> i & 1) && !seen[i]) { seen[i] = 1; g2_order.push_back(i); } g2_check[(int)g2_order.size() - 1].push_back(v); }
    for (int i = 0; i < n; ++i) if (!seen[i]) { seen[i] = 1; g2_order.push_back(i); }
    g2_f.assign(n + 1, vector<double>(n, 0.0));
}
static void run_g2(vector<u64>& out, double& own_min) {
    double t0 = now(); g2_setup(); T_pre += now() - t0; t0 = now();
    g2_rec(0, 0, 0.0); T_trav += now() - t0;
    own_min = g2_cand.empty() && g2_min > 1e299 ? 1e300 : energy_direct(g2_arg);
    finalize(g2_cand, out);
}
// ------------------------------------------------------------------ B1 (decision branch-and-bound at the common threshold; incumbent mode for cert_b1)
static vector<vector<double>> b1_f; static Cands b1_cand; static double b1_inc = 1e300, b1_min = 1e300; static u64 b1_arg = 0; static bool b1_incumbent_mode = false;
static void b1_prune_list() { size_t k = 0; for (size_t i = 0; i < b1_cand.size(); ++i) if (b1_cand[i].second <= b1_inc + EPS_GRAY) b1_cand[k++] = b1_cand[i]; b1_cand.resize(k); }
static void b1_rec(int d, u64 st, double E) {
    if (d == n) {
        C.leaves++; C.materialized++; if (E < b1_min) { b1_min = E; b1_arg = st; }
        if (b1_incumbent_mode) { if (E < b1_inc) { b1_inc = E; b1_prune_list(); } if (E <= b1_inc + EPS_GRAY) { b1_cand.push_back({st, E}); C.candidates_kept++; } }
        else { b1_cand.push_back({st, E}); C.candidates_kept++; }
        return;
    }
    double fd = b1_f[d][d]; int first = (fd > 0) ? 0 : 1;
    for (int t = 0; t < 2; ++t) {
        int bit = t == 0 ? first : 1 - first; if (d == 0 && O.z2 && bit == 1) continue;
        double sg = bit ? 1.0 : -1.0; C.nodes++; double E2 = E + sg * fd;
        vector<double>& fn = b1_f[d + 1]; const vector<double>& fo = b1_f[d]; double sa = 0;
        for (int j = d + 1; j < n; ++j) { fn[j] = fo[j] + Kf[j][d] * sg; sa += fabs(fn[j]); }
        C.field_updates++; C.pair_ops += (n - d - 1) + 1; C.bound_evals++;
        double LB = E2 - sa - SUFFIX_ABS[d + 1];                    // admissible lower bound of any completion
        double thr = b1_incumbent_mode ? b1_inc + EPS_GRAY : Ecut_d + EPS_GRAY;
        if (LB > thr) { C.pruned++; continue; }
        b1_rec(d + 1, st | ((u64)bit << d), E2);
    }
}
static void run_b1(vector<u64>& out, double& own_min) {
    double t0 = now(); init_suffix(); b1_f.assign(n + 1, vector<double>(n, 0.0)); T_pre += now() - t0; t0 = now();
    b1_rec(0, 0, 0.0); T_trav += now() - t0;
    own_min = b1_cand.empty() ? 1e300 : energy_direct(b1_arg); ref_check_full_space(own_min, !b1_cand.empty());
    finalize(b1_cand, out);
}
static int run_cert_b1(vector<u64>& out, double& E0) {
    double t0 = now(); init_suffix(); b1_incumbent_mode = true; b1_f.assign(n + 1, vector<double>(n, 0.0)); T_pre += now() - t0; t0 = now();
    b1_rec(0, 0, 0.0); T_trav += now() - t0; t0 = now();
    double best = 1e300; vector<pair<u64, double>> dir; for (auto& p : b1_cand) { double e = energy_direct(p.first); dir.push_back({p.first, e}); best = min(best, e); }
    out.clear(); for (auto& p : dir) if (p.second <= best + O.tau) out.push_back(p.first);
    expand_z2(out); sort(out.begin(), out.end()); E0 = best; T_final += now() - t0; return 0;
}
// ------------------------------------------------------------------ nullgap: Delta = min over states NOT in S_G of (H - E0); also |S_G|
static int run_nullgap(double& delta, u64& nG, u64& nExcl) {
    u64 N0 = 1ULL << n; vector<double> h(n), sp(n, -1.0); double E = 0; u64 g = 0; double t0 = now();
    auto resync = [&](u64 gg) { for (int i = 0; i < n; ++i) sp[i] = ((gg >> i) & 1) ? 1.0 : -1.0;
        for (int i = 0; i < n; ++i) { double a = 0; for (int j = 0; j < n; ++j) a += Kf[i][j] * sp[j]; h[i] = a; }
        double e = 0; for (int p = 0; p < npairs; ++p) e += PK[p] * (sp[PI[p]] * sp[PJ[p]]); E = e; C.resyncs++; C.pair_ops += (u64)n * n + npairs; };
    resync(0); double m = 1e300; Cands cand; nG = 0;
    auto visit = [&](u64 s, double e) { C.states_visited++; if (grammar_counted(s)) { nG++; return; }
        if (e <= m + EPS_GRAY) { if (e < m) { m = e; size_t k = 0; for (size_t i = 0; i < cand.size(); ++i) if (cand[i].second <= m + EPS_GRAY) cand[k++] = cand[i]; cand.resize(k); } cand.push_back({s, e}); } };
    visit(0, E);
    for (u64 t = 1; t < N0; ++t) {
        int k = __builtin_ctzll(t); g ^= (1ULL << k);
        if ((t & (GRAY_RESYNC - 1)) == 0) { sp[k] = -sp[k]; resync(g); }
        else { double d = -2.0 * sp[k]; E += d * h[k]; for (int j = 0; j < n; ++j) h[j] += Kf[j][k] * d; sp[k] = -sp[k]; C.field_updates++; C.pair_ops += n + 1; }
        visit(g, E);
    }
    T_trav += now() - t0; nExcl = N0 - nG;
    if (nExcl == 0) { delta = INFINITY; return 0; }
    double best = 1e300; for (auto& p : cand) best = min(best, energy_direct(p.first));
    delta = best - Eref; return 0;
}
// ------------------------------------------------------------------ grammar-only counters
static u64 mix64(u64 x) { x += 0x9e3779b97f4a7c15ULL; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL; x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL; return x ^ (x >> 31); }
static u64 gc_digest = 0, gc_cap_hit = 0; static vector<u64> gc_ids;
static void gc_rec(int pos, u64 st) {
    if (gc_cap_hit) return;
    if (pos == (int)g2_order.size()) { C.leaves++; gc_digest += mix64(st); if (!O.dump.empty()) gc_ids.push_back(st); if (C.leaves > O.cap) gc_cap_hit = 1; return; }
    int isl = g2_order[pos];
    for (int bit = 0; bit < 2; ++bit) {
        u64 s2 = st | ((u64)bit << isl); C.nodes++; bool ok = true;
        for (int v : g2_check[pos]) { C.vertex_checks++; if (__builtin_popcount(((u32)s2 ^ NM[v]) & IM[v]) != 2) { ok = false; C.pruned++; break; } }
        if (ok) gc_rec(pos + 1, s2);
    }
}
static int run_boundtest(const char* path) {
    init_suffix(); FILE* f = fopen(path, "r"); int m; unsigned long long bits;
    while (fscanf(f, "%d %llu", &m, &bits) == 2) {
        double E = 0; vector<double> fld(n, 0.0);
        for (int i = 0; i < m; ++i) { double si = ((bits >> i) & 1ULL) ? 1.0 : -1.0; E += si * fld[i]; for (int j = i + 1; j < n; ++j) fld[j] += Kf[j][i] * si; }
        double sa = 0; for (int j = m; j < n; ++j) sa += fabs(fld[j]);
        printf("%d %llu %.17g\n", m, bits, E - sa - SUFFIX_ABS[m]);
    }
    return 0;
}
int main(int argc, char** argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 2; }
    read_input(argv[1]); O.mode = argv[2];
    if (O.mode == "boundtest") return run_boundtest(argv[3]);
    if (argc < 5) return 2;
    O.W = atof(argv[3]); O.tau = atof(argv[4]); parse_opts(argc, argv, 5);
    if (O.W < 0) { fprintf(stderr, "W must be >= 0\n"); return 2; }
    const string& m = O.mode;
    bool solver = (m == "b0" || m == "g1" || m == "g2" || m == "b1"), cert = (m == "cert_b0" || m == "cert_b1"), ng = (m == "nullgap"), gram = (m == "gcount" || m == "gscan");
    if (!(solver || cert || ng || gram)) { fprintf(stderr, "unknown mode\n"); return 2; }
    if (gram) audit("ALLOWED", "grammar-only mode (no Hamiltonian evaluated)"); else guard(ng);
    if ((solver || ng) && !O.have_e0) { fprintf(stderr, "this mode requires the common reference --e0\n"); return 2; }
    if (cert) { O.W = 0; }
    Eref = O.have_e0 ? O.e0 : 0.0; set_threshold();
    vector<u64> out; double own = 0; double t0 = now();
    if (solver) {
        if (m == "b0") run_b0(out, own); else if (m == "g1") run_g1(out, own); else if (m == "g2") run_g2(out, own); else run_b1(out, own);
        const char* rs = "EXACT_SPACE_CONSISTENT";
        if (m == "g1" || m == "g2") {
            C.ref_checks++;
            if (own < Eref - O.tau) ref_reject("a grammar state lies below the reference: reference E0 is not the global minimum", own);
            rs = (own <= Eref + O.tau) ? "GROUND_STATE_IN_GRAMMAR" : "GROUND_EXCLUDED_BY_GRAMMAR_REFERENCE_NOT_SELF_CERTIFIABLE";
        }
        print_common(m.c_str(), out, now() - t0, own, rs);
        if (m == "g2") { printf("g2_island_order="); for (size_t i = 0; i < g2_order.size(); ++i) printf("%s%d", i ? "," : "", g2_order[i]); printf("\n"); }
        return 0;
    }
    if (cert) {
        double E0 = 0; if (m == "cert_b0") run_cert_b0(out, E0); else run_cert_b1(out, E0);
        Eref = E0; set_threshold(); print_common(m.c_str(), out, now() - t0, E0, "CERTIFIED_MINIMUM"); printf("E0_certified=%.17g\nground_count_within_tau=%zu\n", E0, out.size()); return 0;
    }
    if (ng) {
        double delta; u64 nG, nE; run_nullgap(delta, nG, nE);
        printf("mode=nullgap\nn=%d\nE0_used=%.17g\ndelta_nonG=%.17g\nn_grammar=%llu\nn_excluded=%llu\nempty_excluded_set=%d\ninstance_fp=%s\ntau=%.17g\nQ=%.17g\n", n, Eref, delta, nG, nE, (int)(nE == 0), O.fpstr.c_str(), O.tau, Q);
        print_trailer(now() - t0); return 0;
    }
    // grammar-only
    if (m == "gcount") {
        g2_setup(); double t1 = now(); gc_rec(0, 0); T_trav += now() - t1;
        if (!O.dump.empty()) { sort(gc_ids.begin(), gc_ids.end()); FILE* f = fopen(O.dump.c_str(), "w"); for (u64 s : gc_ids) fprintf(f, "%llu\n", s); fclose(f); }
        printf("mode=gcount\nn=%d\nsurvivors=%llu\ndigest=%llu\ncap_hit=%llu\ninstance_fp=%s\n", n, C.leaves, gc_digest, gc_cap_hit, O.fpstr.c_str());
    } else {
        u64 cnt = 0, dg = 0; double t1 = now(); for (u64 s = 0; s < (1ULL << n); ++s) { C.states_visited++; if (grammar_counted(s)) { cnt++; dg += mix64(s); } } T_gram += now() - t1;
        printf("mode=gscan\nn=%d\nsurvivors=%llu\ndigest=%llu\ninstance_fp=%s\n", n, cnt, dg, O.fpstr.c_str());
    }
    print_trailer(now() - t0); return 0;
}
