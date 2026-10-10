// SCR-III-B PREFLIGHT_v009 -- shared infrastructure for prereg_gate_v009 and e2_v009.
//   * instance reader (v007 format) + FNV-1a fingerprint of the file bytes
//   * tolerance hierarchy (all relative to Q = sum|K|):  eps_input < eps_direct < eps_gray < tau
//   * COMMON physical reference E0 (--e0): the target threshold is Ecut = E0 + W + tau for EVERY solver
//   * membership cascade: certain from the scan energy -> direct (double) energy -> __float128 energy -> UNRESOLVED_BOUNDARY
//   * outcome-blind guard + append-only invocation audit log
#pragma once
#include <bits/stdc++.h>
#include <sys/resource.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned int u32; typedef __float128 f128;

static int n, npairs, nv;
static vector<int> PI, PJ; static vector<double> PK; static vector<u32> IM, NM;
static double Kf[40][40];
static double Q = 0, EPS_INPUT = 0, EPS_DIR = 0, EPS_GRAY = 0;
static u64 FP = 0;
static inline double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
// peak resident set of THIS process image: VmHWM (reset at exec); ru_maxrss would inherit the parent's high-water mark across fork+exec
static long maxrss_kb() {
    long v = -1; FILE* f = fopen("/proc/self/status", "r");
    if (f) { char l[256]; while (fgets(l, sizeof l, f)) if (!strncmp(l, "VmHWM:", 6)) { sscanf(l + 6, "%ld", &v); break; } fclose(f); }
    if (v < 0) { struct rusage r; getrusage(RUSAGE_SELF, &r); v = r.ru_maxrss; }
    return v;
}

struct Cnt { u64 nodes = 0, leaves = 0, grammar_checks = 0, vertex_checks = 0, pair_ops = 0, full_energy_evals = 0, field_updates = 0, bound_evals = 0, pruned = 0,
             states_visited = 0, materialized = 0, candidates_kept = 0, comparisons = 0, resyncs = 0, scan_in = 0, scan_out = 0, direct_fallbacks = 0, hp_evals = 0,
             unresolved = 0, cert_rejects = 0, cert_accepts = 0, e2_fallbacks = 0, z2_expansions = 0, ref_checks = 0; } C;
static double T_pre = 0, T_trav = 0, T_gram = 0, T_energy = 0, T_final = 0, T_ser = 0, T_read = 0;

struct Opt { string e0s, dump, audit, protectedf, tag, mode, fpstr; bool z2 = false, synthetic = false, unblind = false, have_e0 = false; double e0 = 0, frac = 0.25, W = 0, tau = 0; u64 cap = 200000000ULL; };
static Opt O;
static double Eref = 0, Ecut_d = 0; static f128 Ecut_h = 0;

static void read_input(const char* path) {
    double tr0 = now();
    FILE* f = fopen(path, "rb"); if (!f) { fprintf(stderr, "cannot open input\n"); exit(2); }
    string buf; char tmp[65536]; size_t k; while ((k = fread(tmp, 1, sizeof tmp, f)) > 0) buf.append(tmp, k); fclose(f);
    FP = 1469598103934665603ULL; for (unsigned char c : buf) { FP ^= c; FP *= 1099511628211ULL; }
    char hx[32]; snprintf(hx, sizeof hx, "%016llx", FP); O.fpstr = hx;
    istringstream in(buf); if (!(in >> n >> npairs)) exit(2);
    PI.resize(npairs); PJ.resize(npairs); PK.resize(npairs); memset(Kf, 0, sizeof Kf); Q = 0;
    for (int p = 0; p < npairs; ++p) { string s; if (!(in >> PI[p] >> PJ[p] >> s)) exit(2); PK[p] = strtod(s.c_str(), nullptr); Kf[PI[p]][PJ[p]] = PK[p]; Kf[PJ[p]][PI[p]] = PK[p]; Q += fabs(PK[p]); }
    if (!(in >> nv)) exit(2);
    IM.resize(nv); NM.resize(nv);
    for (int v = 0; v < nv; ++v) { unsigned a, b; if (!(in >> a >> b)) exit(2); IM[v] = a; NM[v] = b; }
    T_read = now() - tr0;
    EPS_INPUT = ldexp(Q, -52); EPS_DIR = (npairs + 4) * ldexp(1.0, -53) * Q; EPS_GRAY = 1e-10 * Q;
}
static inline double energy_direct(u64 s) {
    double e = 0.0;
    for (int p = 0; p < npairs; ++p) e += ((((s >> PI[p]) ^ (s >> PJ[p])) & 1ULL) ? -PK[p] : PK[p]);
    C.full_energy_evals++; C.pair_ops += npairs; return e;
}
static inline f128 energy_hp(u64 s) {
    f128 e = 0;
    for (int p = 0; p < npairs; ++p) e += ((((s >> PI[p]) ^ (s >> PJ[p])) & 1ULL) ? -(f128)PK[p] : (f128)PK[p]);
    C.hp_evals++; C.pair_ops += npairs; return e;
}
static inline bool grammar_counted(u64 s) {
    C.grammar_checks++;
    for (int v = 0; v < nv; ++v) { C.vertex_checks++; if (__builtin_popcount(((u32)s ^ NM[v]) & IM[v]) != 2) return false; }
    return true;
}
static inline bool grammar_quiet(u64 s) { for (int v = 0; v < nv; ++v) if (__builtin_popcount(((u32)s ^ NM[v]) & IM[v]) != 2) return false; return true; }
static void set_threshold() {
    Ecut_h = (f128)Eref + (f128)O.W + (f128)O.tau; Ecut_d = (double)Ecut_h;
}
// direct (double) energy with the higher-precision boundary cascade.  returns membership of E <= Ecut.  UNRESOLVED -> member (target only ever enlarged)
static inline int decide_direct(u64 s, double* Eout = nullptr) {
    double E = energy_direct(s); if (Eout) *Eout = E; C.direct_fallbacks++;
    if (fabs(E - Ecut_d) > EPS_DIR) return E <= Ecut_d;
    f128 d = energy_hp(s) - Ecut_h; f128 ad = d < 0 ? -d : d;
    if (ad <= (f128)EPS_INPUT) { C.unresolved++; return 1; }
    return d <= 0;
}
static inline int decide_scan(u64 s, double Es, double err) {
    if (Es <= Ecut_d - err) { C.scan_in++; return 1; }
    if (Es > Ecut_d + err) { C.scan_out++; return 0; }
    return decide_direct(s);
}
// ---- audit + guard
static void audit(const char* status, const char* reason) {
    const char* path = !O.audit.empty() ? O.audit.c_str() : getenv("SCR_AUDIT_LOG"); if (!path) return;
    FILE* f = fopen(path, "a"); if (!f) return;
    fprintf(f, "{\"tool\":\"%s\",\"mode\":\"%s\",\"tag\":\"%s\",\"n\":%d,\"W\":%.17g,\"tau\":%.17g,\"instance_fp\":\"%s\",\"synthetic_flag\":%s,\"unblind_flag\":%s,\"z2\":%s,\"status\":\"%s\",\"reason\":\"%s\"}\n",
            "gate_v009", O.mode.c_str(), O.tag.c_str(), n, O.W, O.tau, O.fpstr.c_str(), O.synthetic ? "true" : "false", O.unblind ? "true" : "false", O.z2 ? "true" : "false", status, reason);
    fclose(f);
}
static bool in_protected_list() {
    if (O.protectedf.empty()) return false;
    ifstream f(O.protectedf); string l; while (getline(f, l)) { while (!l.empty() && isspace((unsigned char)l.back())) l.pop_back(); if (l == O.fpstr) return true; }
    return false;
}
// guarded = a request that could reveal 3x3-type excited information (n>16 with W>0, or any excitation-gap mode)
static void guard(bool excitation_mode) {
    bool guarded = (n > 16) && (O.W > 0 || excitation_mode);
    if (!guarded) { audit("ALLOWED", "not a guarded request (n<=16, or W=0 anchor)"); return; }
    if (O.unblind) { audit("ALLOWED", "post-freeze unblinding flag"); return; }
    if (O.synthetic && !O.protectedf.empty() && !in_protected_list()) { audit("ALLOWED", "synthetic instance, fingerprint not in protected list"); return; }
    audit("BLOCKED", O.synthetic ? "synthetic flag rejected: no protected-fingerprint list or instance is protected" : "outcome-blind guard");
    fprintf(stderr, "REFUSED: outcome-blind guard (n>16 with W>0 or excitation-gap mode) -- allowed only after preregistration freeze (--unblind-after-freeze) or on a non-protected synthetic instance\n");
    exit(3);
}
static void parse_opts(int argc, char** argv, int from) {
    for (int a = from; a < argc; ++a) {
        string s = argv[a];
        if (s == "--dump" && a + 1 < argc) O.dump = argv[++a]; else if (s == "--audit" && a + 1 < argc) O.audit = argv[++a];
        else if (s == "--protected" && a + 1 < argc) O.protectedf = argv[++a]; else if (s == "--tag" && a + 1 < argc) O.tag = argv[++a];
        else if (s == "--e0" && a + 1 < argc) { O.e0 = strtod(argv[++a], nullptr); O.have_e0 = true; }
        else if (s == "--frac" && a + 1 < argc) O.frac = atof(argv[++a]); else if (s == "--cap" && a + 1 < argc) O.cap = strtoull(argv[++a], nullptr, 10);
        else if (s == "--z2") O.z2 = true; else if (s == "--synthetic") O.synthetic = true; else if (s == "--unblind-after-freeze") O.unblind = true;
    }
}
static void ref_reject(const char* why, double own) {
    audit("E0_REJECTED", why); fprintf(stderr, "E0_REJECTED: %s (reference=%.17g, own=%.17g, tau=%.3g)\n", why, Eref, own, O.tau); exit(4);
}
// reference consistency for solvers that see the full nominal space (B0, B1)
[[maybe_unused]] static void ref_check_full_space(double own_min_direct, bool any) {
    C.ref_checks++;
    if (!any) ref_reject("no state within the reference window (reference below the true minimum)", NAN);
    if (fabs(own_min_direct - Eref) > O.tau) ref_reject("reference differs from the solver's own exact minimum by more than tau", own_min_direct);
}
static void expand_z2(vector<u64>& out) {
    if (!O.z2) return;
    u64 mask = (n >= 64) ? ~0ULL : ((1ULL << n) - 1); size_t k = out.size();
    for (size_t i = 0; i < k; ++i) { out.push_back((~out[i]) & mask); C.z2_expansions++; }
    sort(out.begin(), out.end()); out.erase(unique(out.begin(), out.end()), out.end());
}
static void print_trailer(double wall) {
    { struct rusage ru; getrusage(RUSAGE_SELF, &ru); printf("cpu_s=%.9g\n", ru.ru_utime.tv_sec + ru.ru_utime.tv_usec * 1e-6 + ru.ru_stime.tv_sec + ru.ru_stime.tv_usec * 1e-6); }
    printf("t_serialize_s=%.9g\nt_read_input_s=%.9g\n", T_ser, T_read);
    printf("wall_s=%.9g\nt_preprocess_s=%.9g\nt_traverse_s=%.9g\nt_grammar_s=%.9g\nt_energy_s=%.9g\nt_finalize_s=%.9g\nmaxrss_kb=%ld\n", wall, T_pre, T_trav, T_gram, T_energy, T_final, maxrss_kb());
    printf("states_visited=%llu\nnodes=%llu\nleaves=%llu\ngrammar_checks=%llu\nvertex_checks=%llu\nfull_energy_evals=%llu\nfield_updates=%llu\npair_ops=%llu\nbound_evals=%llu\npruned=%llu\nmaterialized=%llu\ncandidates_kept=%llu\ncomparisons=%llu\n",
           C.states_visited, C.nodes, C.leaves, C.grammar_checks, C.vertex_checks, C.full_energy_evals, C.field_updates, C.pair_ops, C.bound_evals, C.pruned, C.materialized, C.candidates_kept, C.comparisons);
    printf("resyncs=%llu\nscan_certain_in=%llu\nscan_certain_out=%llu\ndirect_fallbacks=%llu\nhp_evals=%llu\nunresolved_boundary=%llu\ncert_rejects=%llu\ncert_accepts=%llu\ne2_fallbacks=%llu\nz2_expansions=%llu\nref_checks=%llu\n",
           C.resyncs, C.scan_in, C.scan_out, C.direct_fallbacks, C.hp_evals, C.unresolved, C.cert_rejects, C.cert_accepts, C.e2_fallbacks, C.z2_expansions, C.ref_checks);
}
static void print_common(const char* solver, const vector<u64>& out, double wall, double own_min, const char* extra_ref_status) {
    u64 dig = 1469598103934665603ULL; for (u64 s : out) { dig ^= s; dig *= 1099511628211ULL; }
    printf("solver=%s\nn=%d\nW=%.17g\ntau=%.17g\nE0_used=%.17g\nE0_used_hex=%a\nE0_source=%s\nEcut=%.17g\nown_min=%.17g\nref_status=%s\n", solver, n, O.W, O.tau, Eref, Eref, O.have_e0 ? "reference" : "none", Ecut_d, own_min, extra_ref_status);
    printf("Q=%.17g\neps_input=%.17g\neps_direct=%.17g\neps_gray=%.17g\ninstance_fp=%s\nz2=%d\ntarget_count=%zu\nid_digest=%llu\n", Q, EPS_INPUT, EPS_DIR, EPS_GRAY, O.fpstr.c_str(), (int)O.z2, out.size(), dig);
    if (out.size() <= 16) { printf("ids="); for (size_t i = 0; i < out.size(); ++i) printf("%s%llu", i ? "," : "", out[i]); printf("\n"); }
    double tser = now();
    if (!O.dump.empty()) { FILE* f = fopen(O.dump.c_str(), "w"); for (u64 s : out) fprintf(f, "%llu\n", s); fclose(f); }
    T_ser = now() - tser;
    print_trailer(wall);
}
static const int GRAY_RESYNC = 256;       // exact recomputation interval of the incremental Gray-code energy/fields (bounds accumulated rounding)
