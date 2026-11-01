"""GEO_HD_BRIDGE v003 verification runner.   python RUN_VERIFY.py [--fast|--full] [--shard Z3] [--list] [--write]"""
import os, sys, time, json
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(ROOT, "src"))
sys.dont_write_bytecode = True
import verify_v003 as V
if __name__ == "__main__":
    full = "--full" in sys.argv
    if "--list" in sys.argv:
        for k, f in V.SHARDS.items(): print(k, (f.__doc__ or "").strip().split("\n")[0])
        sys.exit(0)
    todo = [sys.argv[sys.argv.index("--shard") + 1]] if "--shard" in sys.argv else list(V.SHARDS)
    t0 = time.time()
    for k in todo:
        t = time.time(); print("== shard %s ==" % k, flush=True); V.SHARDS[k](full); print("   (%s: %.1fs)" % (k, time.time() - t), flush=True)
    print("\nSUMMARY: %d checks, %d PASS, %d FAIL, %.0fs" % (len(V.RESULTS), sum(1 for r in V.RESULTS if r[1]), len(V.FAILS), time.time() - t0))
    if "--write" in sys.argv:
        json.dump([{"name": n, "ok": ok, "detail": str(d)} for n, ok, d in V.RESULTS], open(os.path.join(ROOT, "results", "VERIFY_LAST.json"), "w"), indent=1)
    sys.exit(1 if V.FAILS else 0)
