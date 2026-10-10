// SCR-III-B PREFLIGHT_v007 -- exact full-space verifier (energy + grammar) for finite square-ice patches.
// Not the original simulator. Inputs (K_ij from the FROZEN v005 python evaluator, incidence masks from the v006 grammar) are
// passed in a text file; this program only enumerates and evaluates. No physical constants live here: energies are normalised, H/A = sum_{i<j} K_ij s_i s_j.
// State id: bit i = 1  <=>  s_i = +1  (same as v005/v006).
// Input file:  n  npairs ; npairs lines "i j K" (%.17g) ; nv ; nv lines "islandmask negmask" (uint32) ; nv lines "vertex-order" is implicit (0..nv-1)
// Usage:  verify3 <input> full [W ...]   | verify3 <input> ids <idsfile> | verify3 <input> construct
#include <bits/stdc++.h>
#include <sys/resource.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned int u32;
static int n, npairs, nv;
static vector<int> PI, PJ; static vector<double> PK; static vector<u32> IM, NM;
static double Kf[40][40];
static inline double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
static long maxrss_kb() { struct rusage r; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }
static inline double energy_direct(u64 s) {
    double e = 0.0;
    for (int p = 0; p < npairs; ++p) e += ((((s >> PI[p]) ^ (s >> PJ[p])) & 1ULL) ? -PK[p] : PK[p]);
    return e;
}
static inline bool grammar(u64 s) {
    for (int v = 0; v < nv; ++v) if (__builtin_popcount(((u32)s ^ NM[v]) & IM[v]) != 2) return false;
    return true;
}
static void read_input(const char* path) {
    FILE* f = fopen(path, "r"); if (!f) { fprintf(stderr, "cannot open input\n"); exit(2); }
    if (fscanf(f, "%d %d", &n, &npairs) != 2) exit(2);
    PI.resize(npairs); PJ.resize(npairs); PK.resize(npairs);
    memset(Kf, 0, sizeof Kf);
    for (int p = 0; p < npairs; ++p) {
        if (fscanf(f, "%d %d %lf", &PI[p], &PJ[p], &PK[p]) != 3) exit(2);
        Kf[PI[p]][PJ[p]] = PK[p]; Kf[PJ[p]][PI[p]] = PK[p];
    }
    if (fscanf(f, "%d", &nv) != 1) exit(2);
    IM.resize(nv); NM.resize(nv);
    for (int v = 0; v < nv; ++v) { unsigned a, b; if (fscanf(f, "%u %u", &a, &b) != 2) exit(2); IM[v] = a; NM[v] = b; }
    fclose(f);
}
int main(int argc, char** argv) {
    if (argc < 3) return 2;
    read_input(argv[1]);
    string mode = argv[2];
    if (mode == "ids") {
        FILE* f = fopen(argv[3], "r"); unsigned long long id;
        while (fscanf(f, "%llu", &id) == 1) printf("%llu %.17g\n", id, energy_direct(id));
        return 0;
    }
    if (mode == "construct") {
        // assignment order: islands in the order vertices complete; each completed vertex checked immediately (mirrors v006 python)
        vector<int> order; vector<char> seen(n, 0); vector<vector<int>> check(n + 1);
        for (int v = 0; v < nv; ++v) {
            for (int i = 0; i < n; ++i) if ((IM[v] >> i & 1) && !seen[i]) { seen[i] = 1; order.push_back(i); }
            check[(int)order.size() - 1].push_back(v);
        }
        for (int i = 0; i < n; ++i) if (!seen[i]) { seen[i] = 1; order.push_back(i); }
        u64 nodes = 0, found = 0, sum = 0, xr = 0; double emin = 1e300; u64 state_at_min = 0;
        vector<u64> stack_state(n + 2);
        double t0 = now();
        // iterative DFS
        function<void(int, u64)> rec = [&](int pos, u64 st) {
            if (pos == (int)order.size()) { found++; sum += st; xr ^= st; return; }
            int isl = order[pos];
            for (int bit = 0; bit < 2; ++bit) {
                u64 s2 = st | ((u64)bit << isl); nodes++;
                bool ok = true;
                for (int v : check[pos]) if (__builtin_popcount(((u32)s2 ^ NM[v]) & IM[v]) != 2) { ok = false; break; }
                if (ok) rec(pos + 1, s2);
            }
        };
        rec(0, 0);
        double t1 = now();
        // energies of generated states (second sweep, regenerate ids cheaply)
        vector<u64> ids;
        function<void(int, u64)> rec2 = [&](int pos, u64 st) {
            if (pos == (int)order.size()) { ids.push_back(st); return; }
            int isl = order[pos];
            for (int bit = 0; bit < 2; ++bit) {
                u64 s2 = st | ((u64)bit << isl); bool ok = true;
                for (int v : check[pos]) if (__builtin_popcount(((u32)s2 ^ NM[v]) & IM[v]) != 2) { ok = false; break; }
                if (ok) rec2(pos + 1, s2);
            }
        };
        rec2(0, 0);
        double t2 = now(); vector<double> en(ids.size());
        for (size_t k = 0; k < ids.size(); ++k) en[k] = energy_direct(ids[k]);
        double t3 = now();
        for (size_t k = 0; k < ids.size(); ++k) if (en[k] < emin) { emin = en[k]; state_at_min = ids[k]; }
        printf("n=%d\nnodes=%llu\nfound=%llu\nid_sum=%llu\nid_xor=%llu\ngen_seconds=%.9g\nenergy_seconds_on_survivors=%.9g\nemin_over_grammar=%.17g\nstate_at_emin=%llu\n",
               n, nodes, found, sum, xr, t1 - t0, t3 - t2, emin, state_at_min);
        return 0;
    }
    // ---- full mode
    vector<double> W; for (int a = 3; a < argc; ++a) W.push_back(atof(argv[a]));
    u64 N0 = 1ULL << n;
    vector<double> E; E.resize(N0);
    double t0 = now();
    double emin = 1e300, emax = -1e300;
    for (u64 s = 0; s < N0; ++s) { double e = energy_direct(s); E[s] = e; if (e < emin) emin = e; if (e > emax) emax = e; }
    double t_direct = now() - t0;
    // grammar-only scan (cost of the filter over the nominal space)
    t0 = now(); u64 ngram = 0;
    for (u64 s = 0; s < N0; ++s) ngram += grammar(s);
    double t_gram = now() - t0;
    // gray-code incremental pass compared against direct energies
    t0 = now();
    double h[40], sp[40]; for (int i = 0; i < n; ++i) { sp[i] = -1.0; }
    for (int i = 0; i < n; ++i) { double a = 0; for (int j = 0; j < n; ++j) a += Kf[i][j] * sp[j]; h[i] = a; }
    double eg = E[0], maxdiff = 0.0; u64 g = 0, evaluated = 1;
    for (u64 t = 1; t < N0; ++t) {
        int k = __builtin_ctzll(t);
        eg += -2.0 * sp[k] * h[k];
        double d = -2.0 * sp[k];
        for (int j = 0; j < n; ++j) h[j] += Kf[j][k] * d;
        sp[k] = -sp[k]; g ^= (1ULL << k); evaluated++;
        double df = fabs(eg - E[g]); if (df > maxdiff) maxdiff = df;
    }
    double t_gray = now() - t0;
    double scale = max(fabs(emin), fabs(emax)); double tol = 1e-9 * scale;
    // windows
    t0 = now();
    vector<u64> T(W.size(), 0), FN(W.size(), 0);
    double wmax = 0; for (double w : W) wmax = max(wmax, w);
    for (u64 s = 0; s < N0; ++s) {
        double e = E[s]; if (e > emin + wmax + tol) continue;
        bool gr = grammar(s);
        for (size_t k = 0; k < W.size(); ++k) if (e <= emin + W[k] + tol) { T[k]++; if (!gr) FN[k]++; }
    }
    double t_win = now() - t0;
    // ground-state record (W=0 anchor)
    u64 gs = 0, gs_fn = 0; 
    for (u64 s = 0; s < N0; ++s) if (E[s] <= emin + tol) { gs++; if (!grammar(s)) gs_fn++; }
    // order-independent digest of all energies (for run-to-run identity)
    unsigned long long dig = 1469598103934665603ULL;
    for (u64 s = 0; s < N0; ++s) { double e = E[s]; u64 b; memcpy(&b, &e, 8); dig ^= b; dig *= 1099511628211ULL; }
    printf("n=%d\nnominal=%llu\nevaluated_direct=%llu\nevaluated_gray=%llu\nemin=%.17g\nemax=%.17g\nscale=%.17g\ntol=%.17g\n", n, N0, N0, evaluated, emin, emax, scale, tol);
    printf("grammar_states=%llu\nground_states=%llu\nground_false_exclusions=%llu\ngray_vs_direct_max_abs_diff=%.17g\nenergy_digest=%llu\n", ngram, gs, gs_fn, maxdiff, dig);
    printf("t_direct_energy_pass=%.9g\nt_grammar_scan=%.9g\nt_gray_pass=%.9g\nt_window_scan=%.9g\nmaxrss_kb=%ld\npairs=%d\n", t_direct, t_gram, t_gray, t_win, maxrss_kb(), npairs);
    for (size_t k = 0; k < W.size(); ++k) printf("window %zu %.17g %llu %llu\n", k, W[k], T[k], FN[k]);
    return 0;
}
