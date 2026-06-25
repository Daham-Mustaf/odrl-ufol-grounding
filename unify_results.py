#!/usr/bin/env python3
"""
unify_results.py - normalise benchmark results CSVs into one shared schema.

Reads one or more results CSVs (each in either the WIDE per-problem format
emitted by check_benchmark.py / check_grounding.py -- one row per problem with
a column per solver -- or the LONG per-row format from run_grnd_validation.py),
and writes a single combined CSV in the unified long schema:

    benchmark, problem, group, prover, mode, expected, result, time_s, pass

One row per (problem, prover). 'pass' is PASS / FAIL / SKIP, where SKIP means
the solver did not return a definite decision (timeout / gaveup / unknown).

Usage:
    python3 unify_results.py temporal=results.csv grounding=grounding-results.csv -o all_results.csv
    python3 unify_results.py grnd_foundation_dualrule_20260612.csv      # auto-label from filename
"""
import argparse, csv, os, re, sys

UNIFIED = ["benchmark", "problem", "group", "prover", "mode", "expected", "result", "time_s", "pass"]
SOLVERS = ["vampire", "eprover", "z3", "cvc5"]
PROVED  = {"theorem", "unsatisfiable", "contradictoryaxioms"}
COUNTER = {"satisfiable", "countersatisfiable"}

def col(row, *names):
    for n in names:
        if n in row and row[n] not in (None, ""):
            return row[n]
    return ""

def verdict_pass(prover, expected, result):
    e, r = (expected or "").lower(), (result or "").lower()
    if not r or r in ("timeout", "gaveup", "resourceout", "unknown", "sat-timeout", "n/a", "absent", "-"):
        return "SKIP"
    if prover in ("z3", "cvc5") or prover.startswith(("z3", "cvc5")):
        if r in ("sat", "unsat"):
            return "PASS" if r == e else "FAIL"
        return "SKIP"
    # TPTP prover
    want = COUNTER if e in ("satisfiable", "countersatisfiable") else PROVED
    bad  = PROVED if e in ("satisfiable", "countersatisfiable") else COUNTER
    if r in want: return "PASS"
    if r in bad:  return "FAIL"
    return "SKIP"

def melt_wide(rows, benchmark):
    out = []
    for row in rows:
        problem = col(row, "problem", "odrl_id", "grnd_id", "id")
        group   = col(row, "group", "category", "tier_row")
        exp_t   = col(row, "expected_tptp_status", "declared_szs", "tptp_status")
        exp_s   = col(row, "expected_smt_status", "smt_status")
        for s in SOLVERS:
            if s in row:
                expected = exp_t if s in ("vampire", "eprover") else exp_s
                result   = row[s]
                out.append(dict(benchmark=benchmark, problem=problem, group=group,
                                prover=s, mode="", expected=expected, result=result,
                                time_s="", **{"pass": verdict_pass(s, expected, result)}))
    return out

def pass_long(rows, benchmark):
    out = []
    for row in rows:
        prover = col(row, "prover")
        out.append(dict(benchmark=benchmark,
                        problem=col(row, "problem"),
                        group=col(row, "group", "category"),
                        prover=prover, mode=col(row, "mode"),
                        expected=col(row, "expected"), result=col(row, "result"),
                        time_s=col(row, "time_s", "time"),
                        **{"pass": col(row, "pass") or verdict_pass(prover, col(row,"expected"), col(row,"result"))}))
    return out

def load(path, benchmark):
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return []
    cols = set(rows[0].keys())
    if "prover" in cols and "result" in cols:        # long (run_grnd_validation)
        return pass_long(rows, benchmark)
    if cols & set(SOLVERS):                           # wide (check_benchmark / check_grounding)
        return melt_wide(rows, benchmark)
    sys.exit(f"{path}: unrecognised schema (columns: {sorted(cols)})")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="CSV paths, optionally label=path to tag the benchmark")
    ap.add_argument("-o", "--out", default="unified_results.csv")
    a = ap.parse_args()
    allrows = []
    for item in a.inputs:
        if "=" in item and not os.path.exists(item):
            label, path = item.split("=", 1)
        else:
            label, path = re.sub(r"[-_].*$", "", os.path.basename(item).replace("results", "").strip("-_.") or "bench"), item
        allrows.extend(load(path, label))
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=UNIFIED)
        w.writeheader(); w.writerows(allrows)
    # summary
    from collections import Counter
    bybench = Counter(r["benchmark"] for r in allrows)
    bypass  = Counter(r["pass"] for r in allrows)
    print(f"wrote {a.out}: {len(allrows)} rows  ({dict(bybench)})")
    print(f"pass/fail/skip: {dict(bypass)}")
    fails = [r for r in allrows if r["pass"] == "FAIL"]
    if fails:
        print(f"FAILS: {len(fails)}")
        for r in fails[:20]:
            print(f"  {r['benchmark']} {r['problem']} {r['prover']}: expected {r['expected']}, got {r['result']}")

if __name__ == "__main__":
    main()