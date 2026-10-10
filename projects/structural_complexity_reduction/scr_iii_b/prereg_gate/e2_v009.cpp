// SCR-III-B PREFLIGHT_v009 -- E2: exact Hamiltonian-aware comparator with a certified omitted-interaction bound.
//   H = H_R + H_O,  R = strongest ceil(frac*npairs) pairs by |K| (ties: smaller pair index first), B_O = sum_{O}|K|  =>  H_R - B_O <= H <= H_R + B_O.
//   Ecut = E0 + W + tau (the SAME common reference E0 as every solver).
//   reject  a state only if  H_R - B_O - eps_gray >  Ecut     (certified: H > Ecut)
//   accept  a state only if  H_R + B_O + eps_gray <= Ecut     (certified: H <= Ecut)
//   otherwise fall back to the full exact evaluation (same boundary cascade as every other solver).  E2 never queries grammar membership.
// Usage: e2 <input> e2 <W> <tau> --e0 E0 [--frac 0.25] [--z2] [--dump f] [--audit f] [--protected f] [--synthetic] [--tag t] [--unblind-after-freeze]
#include "gate_common_v009.hpp"

int main(int argc, char** argv) {
    if (argc < 5) { fprintf(stderr, "usage\n"); return 2; }
    read_input(argv[1]); O.mode = argv[2]; if (O.mode != "e2") { fprintf(stderr, "mode must be e2\n"); return 2; }
    O.W = atof(argv[3]); O.tau = atof(argv[4]); parse_opts(argc, argv, 5);
    guard(false);
    if (!O.have_e0) { fprintf(stderr, "this mode requires the common reference --e0\n"); return 2; }
    Eref = O.e0; set_threshold(); double t0 = now(), tp = now();
    // ---- preprocessing: deterministic retained-interaction ordering (|K| descending, pair index ascending) -- uses no target information
    vector<int> ord(npairs); iota(ord.begin(), ord.end(), 0);
    stable_sort(ord.begin(), ord.end(), [&](int a, int b) { double fa = fabs(PK[a]), fb = fabs(PK[b]); if (fa != fb) return fa > fb; return a < b; });
    int r = (int)ceil(O.frac * npairs - 1e-12); r = max(0, min(npairs, r));
    vector<char> ret(npairs, 0); u64 dg = 1469598103934665603ULL; double wret = 0;
    for (int i = 0; i < r; ++i) { ret[ord[i]] = 1; dg ^= (u64)ord[i]; dg *= 1099511628211ULL; wret += fabs(PK[ord[i]]); }
    double BO = 0; for (int p = 0; p < npairs; ++p) if (!ret[p]) BO += fabs(PK[p]);
    double BO_cert = BO * (1.0 + 2.0 * npairs * ldexp(1.0, -53)); BO_cert = nextafter(BO_cert, INFINITY);       // outward-rounded certified bound
    vector<vector<pair<int, double>>> adj(n); vector<int> RI, RJ; vector<double> RK;
    for (int p = 0; p < npairs; ++p) if (ret[p]) { adj[PI[p]].push_back({PJ[p], PK[p]}); adj[PJ[p]].push_back({PI[p], PK[p]}); RI.push_back(PI[p]); RJ.push_back(PJ[p]); RK.push_back(PK[p]); }
    T_pre += now() - tp;
    // ---- Gray-code scan over H_R with periodic exact resynchronisation
    int nb = n - (O.z2 ? 1 : 0); u64 N0 = 1ULL << nb; vector<double> sp(n, -1.0), hR(n, 0.0); double HR = 0; u64 g = 0;
    auto resync = [&](u64 gg) {
        for (int i = 0; i < n; ++i) sp[i] = ((gg >> i) & 1) ? 1.0 : -1.0;
        for (int i = 0; i < n; ++i) { double a = 0; for (auto& e : adj[i]) a += e.second * sp[e.first]; hR[i] = a; }
        double e = 0; for (size_t q = 0; q < RK.size(); ++q) e += RK[q] * (sp[RI[q]] * sp[RJ[q]]); HR = e; C.resyncs++; C.pair_ops += 3 * RK.size(); };
    vector<u64> mem; double ownmin = 1e300; double ts = now();
    auto process = [&](u64 s) {
        C.states_visited++; C.bound_evals++;
        double lo = HR - BO_cert - EPS_GRAY, up = HR + BO_cert + EPS_GRAY;
        if (up < Eref - O.tau) ref_reject("certified upper bound of a state lies below the reference E0", up);
        if (lo > Ecut_d) { C.cert_rejects++; return; }
        if (up <= Ecut_d) { C.cert_accepts++; mem.push_back(s); return; }
        C.e2_fallbacks++; double E; if (decide_direct(s, &E)) mem.push_back(s);
        if (E < ownmin) ownmin = E;
        if (E < Eref - O.tau) ref_reject("a fully evaluated state lies below the reference E0", E);
    };
    resync(0); process(0);
    for (u64 t = 1; t < N0; ++t) {
        int k = __builtin_ctzll(t); g ^= (1ULL << k);
        if ((t & (GRAY_RESYNC - 1)) == 0) { sp[k] = -sp[k]; resync(g); }
        else { double d = -2.0 * sp[k]; HR += d * hR[k]; for (auto& e : adj[k]) hR[e.first] += e.second * d; sp[k] = -sp[k]; C.field_updates++; C.pair_ops += adj[k].size() + 1; }
        process(g);
    }
    T_trav += now() - ts;
    if (mem.empty()) ref_reject("empty target: reference E0 lies below the true minimum", NAN);
    C.ref_checks++; double tf = now(); expand_z2(mem); sort(mem.begin(), mem.end()); T_final += now() - tf;
    print_common("e2", mem, now() - t0, ownmin, "E2_CERTIFICATE_CONSISTENT_NOT_SELF_CERTIFYING");
    printf("e2_frac=%.17g\ne2_retained_pairs=%d\ne2_omitted_pairs=%d\ne2_B_O=%.17g\ne2_B_O_certified=%.17g\ne2_retained_weight_fraction=%.17g\ne2_order_digest=%llu\n", O.frac, r, npairs - r, BO, BO_cert, Q > 0 ? wret / Q : 0.0, dg);
    return 0;
}
