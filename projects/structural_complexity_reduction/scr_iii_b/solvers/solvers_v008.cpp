// SCR-III-B PREFLIGHT_v008 -- fair solver implementations for the complete-target-set task
//   task: given window W (normalised units H/A) return all states s with H(s) <= E0 + W + tau, E0 = ground energy of the solver's own search space.
//   B0 : optimized single-thread Gray-code exhaustive scan (incremental fields), single pass with running-minimum candidate list
//   G1 : scan every nominal state with the grammar check, then DIRECT energy on survivors
//   G2 : constructive grammar generation (DFS) with INCREMENTAL pair-energy/field updates along the search tree
//   B1 : exact branch-and-bound with an admissible lower bound  LB = E_fixed - sum_free |f_j| - sum_{free j<k} |K_jk|
// G1/G2 return S_T ∩ S_G with E0-hat = min over S_G (equals the true E0 iff a ground state is grammar-admissible).
// Input file = v007 format (n npairs, "i j K"..., nv, "islandmask negmask"...). State id: bit i = 1 <=> s_i = +1.
// Outcome-blind guard: for n > 16, W > 0 is refused unless --unblind-after-freeze is given.
// Usage: solvers <input> <b0|g1|g2|b1> <W> <tau> [--dump file] [--unblind-after-freeze]
//        solvers <input> boundtest <partials-file>      (lines: "m bits" ; first m spins fixed, bit i of bits = spin i)
#include <bits/stdc++.h>
#include <sys/resource.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned int u32;
static int n, npairs, nv;
static vector<int> PI, PJ; static vector<double> PK; static vector<u32> IM, NM;
static double Kf[40][40]; static double SUFFIX_ABS[42];     // SUFFIX_ABS[d] = sum_{d<=j<k} |K_jk|
static inline double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
static long maxrss_kb() { struct rusage r; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }
struct Cnt { u64 nodes = 0, leaves = 0, grammar_checks = 0, vertex_checks = 0, pair_ops = 0, full_energy_evals = 0, field_updates = 0,
             bound_evals = 0, pruned = 0, states_visited = 0, materialized = 0, candidates_kept = 0, comparisons = 0; } C;
static double T_pre = 0, T_trav = 0, T_gram = 0, T_energy = 0, T_final = 0;

static inline double energy_direct(u64 s) {
    double e = 0.0;
    for (int p = 0; p < npairs; ++p) e += ((((s >> PI[p]) ^ (s >> PJ[p])) & 1ULL) ? -PK[p] : PK[p]);
    C.full_energy_evals++; C.pair_ops += npairs; return e;
}
static inline bool grammar_counted(u64 s) {
    C.grammar_checks++;
    for (int v = 0; v < nv; ++v) { C.vertex_checks++; if (__builtin_popcount(((u32)s ^ NM[v]) & IM[v]) != 2) return false; }
    return true;
}
static void read_input(const char* path) {
    FILE* f = fopen(path, "r"); if (!f) { fprintf(stderr, "cannot open input\n"); exit(2); }
    if (fscanf(f, "%d %d", &n, &npairs) != 2) exit(2);
    PI.resize(npairs); PJ.resize(npairs); PK.resize(npairs); memset(Kf, 0, sizeof Kf);
    for (int p = 0; p < npairs; ++p) { if (fscanf(f, "%d %d %lf", &PI[p], &PJ[p], &PK[p]) != 3) exit(2); Kf[PI[p]][PJ[p]] = PK[p]; Kf[PJ[p]][PI[p]] = PK[p]; }
    if (fscanf(f, "%d", &nv) != 1) exit(2);
    IM.resize(nv); NM.resize(nv);
    for (int v = 0; v < nv; ++v) { unsigned a, b; if (fscanf(f, "%u %u", &a, &b) != 2) exit(2); IM[v] = a; NM[v] = b; }
    fclose(f);
    for (int d = 0; d <= n + 1; ++d) SUFFIX_ABS[d] = 0;
    for (int d = n - 1; d >= 0; --d) { double s = 0; for (int k = d + 1; k < n; ++k) s += fabs(Kf[d][k]); SUFFIX_ABS[d] = SUFFIX_ABS[d + 1] + s; }
}
// ---- result collector
struct Res { vector<pair<u64, double>> c; double m = 1e300; };
static void finalize(Res& r, double W, double tau, vector<u64>& out, double& E0hat) {
    double t0 = now(); E0hat = r.m; out.clear();
    for (auto& p : r.c) if (p.second <= r.m + W + tau) out.push_back(p.first);
    sort(out.begin(), out.end()); T_final += now() - t0;
}
static inline void prune(Res& r, double W, double tau) {
    size_t k = 0; for (size_t i = 0; i < r.c.size(); ++i) if (r.c[i].second <= r.m + W + tau) r.c[k++] = r.c[i];
    r.c.resize(k);
}
// ---- B0
static void run_b0(double W, double tau, vector<u64>& out, double& E0hat) {
    double t0 = now(); u64 N0 = 1ULL << n; Res r;
    vector<double> h(n), sp(n, -1.0);
    for (int i = 0; i < n; ++i) { double a = 0; for (int j = 0; j < n; ++j) a += Kf[i][j] * sp[j]; h[i] = a; }
    double E = energy_direct(0); r.m = E; r.c.push_back({0, E});
    T_pre += now() - t0; t0 = now();
    u64 g = 0; C.states_visited = 1;
    for (u64 t = 1; t < N0; ++t) {
        int k = __builtin_ctzll(t); double d = -2.0 * sp[k];
        E += -2.0 * sp[k] * h[k];
        for (int j = 0; j < n; ++j) h[j] += Kf[j][k] * d;
        sp[k] = -sp[k]; g ^= (1ULL << k);
        C.states_visited++; C.field_updates++; C.pair_ops += n;
        C.comparisons++;
        if (E < r.m) { r.m = E; prune(r, W, tau); }
        if (E <= r.m + W + tau) { r.c.push_back({g, E}); C.candidates_kept++; }
    }
    T_trav += now() - t0; finalize(r, W, tau, out, E0hat);
}
// ---- G1
static void run_g1(double W, double tau, vector<u64>& out, double& E0hat) {
    u64 N0 = 1ULL << n; double t0 = now(); vector<u64> surv; 
    for (u64 s = 0; s < N0; ++s) { C.states_visited++; if (grammar_counted(s)) surv.push_back(s); }
    T_gram += now() - t0; C.materialized = surv.size();
    t0 = now(); Res r;
    for (u64 s : surv) { double e = energy_direct(s); r.c.push_back({s, e}); if (e < r.m) r.m = e; }
    T_energy += now() - t0; finalize(r, W, tau, out, E0hat);
}
// ---- G2
static vector<int> g2_order; static vector<vector<int>> g2_check; static Res g2_res;
static vector<vector<double>> g2_f;
static void g2_rec(int pos, u64 st, double E) {
    if (pos == (int)g2_order.size()) { C.leaves++; C.materialized++; g2_res.c.push_back({st, E}); if (E < g2_res.m) g2_res.m = E; return; }
    int isl = g2_order[pos];
    for (int bit = 0; bit < 2; ++bit) {
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
static void run_g2(double W, double tau, vector<u64>& out, double& E0hat) {
    double t0 = now();
    vector<char> seen(n, 0); g2_check.assign(n + 1, {});
    for (int v = 0; v < nv; ++v) { for (int i = 0; i < n; ++i) if ((IM[v] >> i & 1) && !seen[i]) { seen[i] = 1; g2_order.push_back(i); } g2_check[(int)g2_order.size() - 1].push_back(v); }
    for (int i = 0; i < n; ++i) if (!seen[i]) { seen[i] = 1; g2_order.push_back(i); }
    g2_f.assign(n + 1, vector<double>(n, 0.0));
    T_pre += now() - t0; t0 = now();
    g2_rec(0, 0, 0.0);
    T_trav += now() - t0; finalize(g2_res, W, tau, out, E0hat);
}
// ---- B1
static Res b1_res; static double b1_W, b1_tau, b1_inc = 1e300; static vector<vector<double>> b1_f;
static void b1_rec(int d, u64 st, double E, double sumabs_f) {
    if (d == n) { C.leaves++; C.materialized++; b1_res.c.push_back({st, E}); if (E < b1_inc) { b1_inc = E; b1_res.m = E; prune(b1_res, b1_W, b1_tau); } return; }
    double fd = b1_f[d][d];
    int first = (fd > 0) ? 0 : 1;                       // try the lower-energy value first (deterministic value ordering)
    for (int t = 0; t < 2; ++t) {
        int bit = t == 0 ? first : 1 - first; double sg = bit ? 1.0 : -1.0; C.nodes++;
        double E2 = E + sg * fd;
        vector<double>& fn = b1_f[d + 1]; const vector<double>& fo = b1_f[d];
        double sa = 0;
        for (int j = d + 1; j < n; ++j) { fn[j] = fo[j] + Kf[j][d] * sg; sa += fabs(fn[j]); }
        C.field_updates++; C.pair_ops += (n - d - 1) + 1; C.bound_evals++;
        double LB = E2 - sa - SUFFIX_ABS[d + 1];
        if (LB > b1_inc + b1_W + b1_tau) { C.pruned++; continue; }
        b1_rec(d + 1, st | ((u64)bit << d), E2, sa);
    }
}
static void run_b1(double W, double tau, vector<u64>& out, double& E0hat) {
    double t0 = now(); b1_W = W; b1_tau = tau; b1_f.assign(n + 1, vector<double>(n, 0.0)); T_pre += now() - t0; t0 = now();
    b1_rec(0, 0, 0.0, 0.0); T_trav += now() - t0; finalize(b1_res, W, tau, out, E0hat);
}
static int run_boundtest(const char* path) {
    FILE* f = fopen(path, "r"); int m; unsigned long long bits;
    while (fscanf(f, "%d %llu", &m, &bits) == 2) {
        double E = 0; vector<double> fld(n, 0.0);
        for (int i = 0; i < m; ++i) { double si = ((bits >> i) & 1ULL) ? 1.0 : -1.0; E += si * fld[i]; for (int j = i + 1; j < n; ++j) fld[j] += Kf[j][i] * si; }
        double sa = 0; for (int j = m; j < n; ++j) sa += fabs(fld[j]);
        printf("%d %llu %.17g\n", m, bits, E - sa - SUFFIX_ABS[m]);
    }
    return 0;
}
int main(int argc, char** argv) {
    if (argc < 4) return 2;
    read_input(argv[1]); string sol = argv[2];
    if (sol == "boundtest") return run_boundtest(argv[3]);
    double W = atof(argv[3]), tau = atof(argv[4]); string dump; bool unblind = false;
    for (int a = 5; a < argc; ++a) { string s = argv[a]; if (s == "--dump" && a + 1 < argc) dump = argv[++a]; else if (s == "--unblind-after-freeze") unblind = true; }
    if (n > 16 && W > 0 && !unblind) { fprintf(stderr, "REFUSED: outcome-blind guard (n>16, W>0) -- run only after preregistration freeze with --unblind-after-freeze\n"); return 3; }
    vector<u64> out; double E0hat = 0; double t0 = now();
    if (sol == "b0") run_b0(W, tau, out, E0hat); else if (sol == "g1") run_g1(W, tau, out, E0hat);
    else if (sol == "g2") run_g2(W, tau, out, E0hat); else if (sol == "b1") run_b1(W, tau, out, E0hat); else return 2;
    double wall = now() - t0;
    u64 dig = 1469598103934665603ULL; for (u64 s : out) { dig ^= s; dig *= 1099511628211ULL; }
    printf("solver=%s\nn=%d\nW=%.17g\ntau=%.17g\nE0hat=%.17g\ntarget_count=%zu\nid_digest=%llu\n", sol.c_str(), n, W, tau, E0hat, out.size(), dig);
    if (out.size() <= 16) { printf("ids="); for (size_t i = 0; i < out.size(); ++i) printf("%s%llu", i ? "," : "", out[i]); printf("\n"); }
    if (!dump.empty()) { FILE* f = fopen(dump.c_str(), "w"); for (u64 s : out) fprintf(f, "%llu\n", s); fclose(f); }
    printf("wall_s=%.9g\nt_preprocess_s=%.9g\nt_traverse_s=%.9g\nt_grammar_s=%.9g\nt_energy_s=%.9g\nt_finalize_s=%.9g\nmaxrss_kb=%ld\n", wall, T_pre, T_trav, T_gram, T_energy, T_final, maxrss_kb());
    printf("states_visited=%llu\nnodes=%llu\nleaves=%llu\ngrammar_checks=%llu\nvertex_checks=%llu\nfull_energy_evals=%llu\nfield_updates=%llu\npair_ops=%llu\nbound_evals=%llu\npruned=%llu\nmaterialized=%llu\ncandidates_kept=%llu\ncomparisons=%llu\n",
           C.states_visited, C.nodes, C.leaves, C.grammar_checks, C.vertex_checks, C.full_energy_evals, C.field_updates, C.pair_ops, C.bound_evals, C.pruned, C.materialized, C.candidates_kept, C.comparisons);
    return 0;
}
