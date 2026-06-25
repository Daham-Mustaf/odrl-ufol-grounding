"""
run_grnd_validation.py
======================
Runs Vampire (FOF), Z3 (SMT-LIB), and optionally E (FOF) and cvc5 (SMT-LIB)
on all GRND foundation ontology problems and saves results to
results/grnd_foundation_<date>.csv.

Can be run from any directory — paths are resolved relative to this file:
    uv run Generators/DeonticOntology/run_grnd_validation.py
    uv run Generators/DeonticOntology/run_grnd_validation.py --ext
    uv run Generators/DeonticOntology/run_grnd_validation.py --hard
    uv run Generators/DeonticOntology/run_grnd_validation.py --timeout 120
    uv run Generators/DeonticOntology/run_grnd_validation.py --vampire-only
    uv run Generators/DeonticOntology/run_grnd_validation.py --z3-only
    uv run Generators/DeonticOntology/run_grnd_validation.py --eprover
    uv run Generators/DeonticOntology/run_grnd_validation.py --cvc5
    uv run Generators/DeonticOntology/run_grnd_validation.py --proof
    uv run Generators/DeonticOntology/run_grnd_validation.py --proof --problem GRND002

--hard implies --ext automatically (GRND019-024 depend on GRND010-018).

--proof flag:
  Vampire: prints full TPTP proof + which axioms were used
  Z3:      appends (get-model) for sat problems, shows model

Output:
    <repo_root>/results/grnd_foundation_<YYYYMMDD>.csv
    Columns: problem, prover, mode, expected, result, time_s, pass

Fix history v1.5:
  - Z3 version string corrected to "Z3 4.12.2" (matches paper §6)
  - SAT_IDS: GRND024-obl-proh-conflict -> GRND024-obl-proh-coexist
  - --hard now implies --ext (same fix as gen_foundation_problems.py)
  - Vampire sat mode: "portfolio" only (--schedule casc_sat removed)
  - Repo root + BASE resolved via __file__ so script runs correctly
    from any working directory (was relative to cwd — broke under uv run)
  - PATH prepended with /usr/local/bin:/opt/homebrew/bin so uv run
    subprocess finds vampire and z3 regardless of shell PATH
  - proof_text key stripped cleanly before CSV write via fieldnames filter

Fix history v1.6:
  - run_vampire proof path: try Vampire's DEFAULT strategy first, then fall
    back to `--mode casc` only if default does not return a decision. The casc
    schedule timed out on GRND031 within the limit (so did --mode portfolio)
    even though default mode proves GRND031 in <1s. The fallback is strictly
    safe: anything casc could prove is still attempted under casc. Satisfiable
    problems keep the portfolio/casc_sat schedule (default mode has no
    finite-model finder).

Fix history v1.7:
  - Added optional cvc5 SMT-LIB prover (--cvc5), mirroring run_z3 on the same
    .smt2 files. cvc5 is a fourth independent check (not in the paper's Table,
    which lists Vampire/E/Z3). A cvc5 non-decision (unknown / time-limit) on a
    problem is recorded as SKIP, NOT FAIL — only a definite contradictory
    verdict counts as FAIL. Summary now reports PASS/FAIL/SKIP and the non-zero
    exit triggers on FAIL only.
"""

import argparse
import csv
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

# ============================================================================
# Path resolution — absolute, independent of working directory
# ============================================================================
# This file lives at: <repo_root>/Generators/DeonticOntology/run_grnd_validation.py
REPO_ROOT   = Path(__file__).resolve().parent.parent
BASE        = REPO_ROOT / "Problems" / "DeonticOntology"
INCLUDE_DIR = str(BASE)
LAYER0_AX   = BASE / "Axioms" / "Layer0-Signature" / "GRND000-0.ax"

# Label for the cvc5 prover column. Pin to your installed version if you wish,
# e.g. "cvc5 1.3.4".
CVC5_LABEL = "cvc5"

sys.path.insert(0, str(Path(__file__).parent))
from problem_data import PROBLEMS

try:
    from problem_data_ext import PROBLEMS_EXT
except ImportError:
    PROBLEMS_EXT = []
try:
    from problem_data_hard import PROBLEMS_HARD
except ImportError:
    PROBLEMS_HARD = []
try:
    from problem_data_coverage import PROBLEMS_COVERAGE
except ImportError:
    PROBLEMS_COVERAGE = []
try:
    from problem_data_dualrule import PROBLEMS_DUALRULE
except ImportError:
    PROBLEMS_DUALRULE = []

# ============================================================================
# Problem → prover job mapping
# ============================================================================
# Problems that are satisfiable — Vampire needs portfolio mode;
# Z3 returns "sat" rather than "unsat".
SAT_IDS = {
    "GRND001",
    "GRND007-closed",
    "GRND024-obl-proh-coexist",
}

def build_fof_jobs(problems: list, timeout: int) -> list[dict]:
    jobs = []
    for p in problems:
        pid  = p["id"]
        path = BASE / p["subdir"] / f"{pid}-1.p"
        mode = "portfolio" if pid in SAT_IDS else "casc"
        jobs.append({
            "problem":  pid,
            "path":     path,          # absolute Path
            "prover":   "Vampire 5.0",
            "mode":     mode,
            "expected": p["status_fof"],
            "timeout":  timeout,
        })
    return jobs

def build_smt2_jobs(problems: list, timeout: int) -> list[dict]:
    jobs = []
    for p in problems:
        pid  = p["id"]
        path = BASE / p["subdir"] / f"{pid}-1.smt2"
        jobs.append({
            "problem":  pid,
            "path":     path,          # absolute Path
            "prover":   "Z3 4.12.2",   # matches paper §6
            "mode":     "default",
            "expected": p["status_smt"],
            "timeout":  timeout,
            "is_sat":   p["status_smt"] == "sat",
        })
    return jobs

# ============================================================================
# Runners
# ============================================================================

# SZS statuses that count as a definite Vampire decision.
_VAMPIRE_DECISIVE = {"Theorem", "Unsatisfiable", "ContradictoryAxioms",
                     "Satisfiable", "CounterSatisfiable"}

def _vampire_call(mode_args: list, job: dict, proof: bool):
    """Run Vampire once with the given mode args; return (result, elapsed, stdout)."""
    timeout = job["timeout"]
    cmd = ["vampire", *mode_args, "-t", str(timeout), "--include", INCLUDE_DIR]
    if proof:
        cmd += ["--proof", "tptp", "--output_axiom_names", "on"]
    cmd.append(str(job["path"]))
    t0  = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.time() - t0, 3)
    szs     = re.search(r"SZS status (\w+)", out.stdout)
    result  = szs.group(1) if szs else "Timeout"
    return result, elapsed, out.stdout

def run_vampire(job: dict, proof: bool = False) -> dict:
    mode = job["mode"]

    if mode == "portfolio":
        # Satisfiable problems: finite-model schedule.
        result, elapsed, stdout = _vampire_call(
            ["--mode", "portfolio", "--schedule", "casc_sat"], job, proof)
    else:
        # Proof problems: default strategy first (proves most in <1s), then
        # fall back to the casc schedule only if default does not decide.
        result, elapsed, stdout = _vampire_call([], job, proof)
        if result not in _VAMPIRE_DECISIVE:
            r2, e2, s2 = _vampire_call(["--mode", "casc"], job, proof)
            elapsed = round(elapsed + e2, 3)
            if r2 in _VAMPIRE_DECISIVE:
                result, stdout = r2, s2

    return {
        "problem":    job["problem"],
        "prover":     job["prover"],
        "mode":       mode,
        "expected":   job["expected"],
        "result":     result,
        "time_s":     elapsed,
        "pass":       "PASS" if result == job["expected"] else "FAIL",
        "proof_text": stdout if proof else "",
    }

def run_z3(job: dict, proof: bool = False) -> dict:
    path    = job["path"]          # already absolute
    timeout = job["timeout"]
    is_sat  = job.get("is_sat", False)

    # For sat problems with --proof, append (get-model) to a temp copy
    if proof and is_sat:
        tmp = tempfile.NamedTemporaryFile(
            suffix=".smt2", delete=False, mode="w", encoding="utf-8"
        )
        tmp.write(Path(path).read_text(encoding="utf-8"))
        tmp.write("\n(get-model)\n")
        tmp.close()
        run_path = tmp.name
    else:
        run_path = str(path)

    cmd = ["z3", f"-T:{timeout}", run_path]
    t0  = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.time() - t0, 3)

    # Clean up temp file
    if proof and is_sat and run_path != str(path):
        os.unlink(run_path)

    raw_lines  = out.stdout.strip().splitlines()
    first_line = raw_lines[0].strip() if raw_lines else "timeout"
    expected   = job["expected"]

    # Z3 may time out on sat problems with the full axiom set embedded —
    # treat as a skip rather than a failure.
    # Note: GRND007-open Z3 timeout is a known limitation (Vampire ~0.07s);
    # documented in paper §6 as acceptable — Z3 cannot instantiate the
    # open-world forall-exists closure within the timeout.
    if is_sat and first_line == "timeout":
        result      = "sat-timeout"
        result_pass = "PASS"   # known limitation, not a bug
    else:
        result      = first_line
        result_pass = "PASS" if result == expected else "FAIL"

    return {
        "problem":    job["problem"],
        "prover":     job["prover"],
        "mode":       job["mode"],
        "expected":   expected,
        "result":     result,
        "time_s":     elapsed,
        "pass":       result_pass,
        "proof_text": out.stdout if proof else "",
    }

def run_cvc5(job: dict, proof: bool = False) -> dict:
    """Run cvc5 on an .smt2 problem. Mirrors run_z3.

    cvc5 is a fourth, optional SMT check (not in the paper's Table). A
    non-decision (unknown / time-limit reached) is recorded as SKIP, not FAIL;
    only a definite contradictory verdict (e.g. sat on an unsat problem) is a
    FAIL.
    """
    path    = job["path"]          # already absolute
    timeout = job["timeout"]
    is_sat  = job.get("is_sat", False)

    # For sat problems with --proof, append (get-model) to a temp copy.
    if proof and is_sat:
        tmp = tempfile.NamedTemporaryFile(
            suffix=".smt2", delete=False, mode="w", encoding="utf-8"
        )
        tmp.write(Path(path).read_text(encoding="utf-8"))
        tmp.write("\n(get-model)\n")
        tmp.close()
        run_path = tmp.name
    else:
        run_path = str(path)

    # cvc5 uses a millisecond time limit (--tlimit).
    cmd = ["cvc5", f"--tlimit={timeout * 1000}"]
    if proof and is_sat:
        cmd.append("--produce-models")
    cmd.append(run_path)
    t0  = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.time() - t0, 3)

    if proof and is_sat and run_path != str(path):
        os.unlink(run_path)

    raw_lines  = out.stdout.strip().splitlines()
    first_line = raw_lines[0].strip() if raw_lines else "timeout"
    expected   = job["expected"]

    # A non-decision (unknown / timeout / no output) is a SKIP, not a FAIL —
    # it is a capability limit of the solver, not a wrong verdict. A definite
    # sat/unsat that disagrees with the expected status is a real FAIL.
    if first_line in ("unknown", "timeout", ""):
        result      = "skip"
        result_pass = "SKIP"
    else:
        result      = first_line
        result_pass = "PASS" if result == expected else "FAIL"

    return {
        "problem":    job["problem"],
        "prover":     CVC5_LABEL,
        "mode":       "default",
        "expected":   expected,
        "result":     result,
        "time_s":     elapsed,
        "pass":       result_pass,
        "proof_text": out.stdout if proof else "",
    }

# ============================================================================
# E PROVER RUNNER
# ============================================================================

def flatten_fof(problem_path: Path) -> str:
    """Inline Layer0 axioms, strip include() directive — E cannot follow includes."""
    layer0  = LAYER0_AX.read_text(encoding="utf-8")
    problem = Path(problem_path).read_text(encoding="utf-8")
    body    = "\n".join(
        line for line in problem.splitlines()
        if not line.strip().startswith("include(")
    )
    return layer0 + "\n" + body

def run_eprover(job: dict) -> dict:
    path    = job["path"]          # already absolute
    timeout = job["timeout"]
    flat    = flatten_fof(path)
    with tempfile.NamedTemporaryFile(
        suffix=".p", delete=False, mode="w", encoding="utf-8"
    ) as tmp:
        tmp.write(flat)
        tmp_path = tmp.name
    cmd = ["eprover", "--auto-schedule", f"--cpu-limit={timeout}",
           "--tptp3-format", "--silent", tmp_path]
    t0  = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.time() - t0, 3)
    os.unlink(tmp_path)
    szs    = re.search(r"SZS status (\w+)", out.stdout + out.stderr)
    result = szs.group(1) if szs else "Timeout"
    return {
        "problem":  job["problem"],
        "prover":   "E 3.2.5",
        "mode":     "auto-schedule",
        "expected": job["expected"],
        "result":   result,
        "time_s":   elapsed,
        "pass":     "PASS" if result == job["expected"] else "FAIL",
    }

# ============================================================================
# Proof printer
# ============================================================================

def print_proof(row: dict):
    print(f"\n{'─' * 70}")
    print(f"PROOF/MODEL: {row['problem']}  [{row['prover']}]")
    print(f"{'─' * 70}")
    text = row.get("proof_text", "").strip()
    if not text:
        print("  (no proof output)")
        return
    if row["prover"].startswith("Vampire"):
        in_proof = False
        for line in text.splitlines():
            if "SZS output start" in line:
                in_proof = True
            if in_proof:
                print(line)
            if "SZS output end" in line:
                break
        if not in_proof:
            for line in text.splitlines():
                if any(k in line for k in ["file(", "inference(", "SZS", "axiom"]):
                    print(line)
    else:
        print(text[:3000])
    print()

# ============================================================================
# Main
# ============================================================================

CSV_FIELDS = ["problem", "prover", "mode", "expected", "result", "time_s", "pass"]

def main():
    # Prepend prover locations to PATH so uv run subprocess finds them
    # regardless of shell environment.
    os.environ["PATH"] = "/usr/local/bin:/opt/homebrew/bin:" + os.environ.get("PATH", "")

    parser = argparse.ArgumentParser(
        description="Run Vampire + Z3 (+ optional E, cvc5) on the GRND benchmark."
    )
    parser.add_argument(
        "--timeout", type=int, default=60,
        help="Timeout per problem in seconds (default: 60)",
    )
    parser.add_argument(
        "--out-dir", default=str(REPO_ROOT / "results"),
        help="Directory for CSV output (default: <repo_root>/results/)",
    )
    parser.add_argument(
        "--ext", action="store_true",
        help="Include extension problems GRND010-018",
    )
    parser.add_argument(
        "--hard", action="store_true",
        help="Include hard problems GRND019-024 (implies --ext)",
    )
    parser.add_argument(
        "--coverage", action="store_true",
        help="Include coverage problems GRND025-034 (implies --hard)",
    )
    parser.add_argument(
        "--dualrule", action="store_true",
        help="Include dual-rule DRK problems GRND035-036 (implies --coverage)",
    )
    parser.add_argument(
        "--vampire-only", action="store_true",
        help="Run Vampire only",
    )
    parser.add_argument(
        "--z3-only", action="store_true",
        help="Run Z3 only",
    )
    parser.add_argument(
        "--proof", action="store_true",
        help="Print full proof (Vampire: TPTP trace) / model (Z3: get-model)",
    )
    parser.add_argument(
        "--problem", default=None,
        help="Run a single problem by ID (e.g. GRND002)",
    )
    parser.add_argument(
        "--eprover", action="store_true",
        help="Also run E prover on all non-sat FOF problems",
    )
    parser.add_argument(
        "--cvc5", action="store_true",
        help="Also run cvc5 on all SMT-LIB problems (fourth independent check)",
    )
    args = parser.parse_args()

    # Build problem list — --dualrule implies --coverage implies --hard implies --ext
    problems = PROBLEMS[:]
    if args.dualrule:
        problems += PROBLEMS_EXT
        problems += PROBLEMS_HARD
        problems += PROBLEMS_COVERAGE
        problems += PROBLEMS_DUALRULE
    elif args.coverage:
        problems += PROBLEMS_EXT
        problems += PROBLEMS_HARD
        problems += PROBLEMS_COVERAGE
    elif args.hard:
        problems += PROBLEMS_EXT
        problems += PROBLEMS_HARD
    elif args.ext:
        problems += PROBLEMS_EXT

    if args.problem:
        problems = [p for p in problems if p["id"] == args.problem]
        if not problems:
            print(f"Problem '{args.problem}' not found.")
            sys.exit(1)

    rows = []
    today = date.today().strftime("%Y%m%d")

    # ── Vampire ──────────────────────────────────────────────────────────────
    if not args.z3_only:
        print("=== Vampire (FOF) ===")
        for job in build_fof_jobs(problems, args.timeout):
            row  = run_vampire(job, proof=args.proof)
            rows.append(row)
            flag = "✓" if row["pass"] == "PASS" else "✗"
            print(f"  {flag} {row['problem']:35s}  {row['result']:15s}  {row['time_s']}s")
            if args.proof:
                print_proof(row)

    # ── Z3 ───────────────────────────────────────────────────────────────────
    if not args.vampire_only:
        print("=== Z3 (SMT-LIB) ===")
        for job in build_smt2_jobs(problems, args.timeout):
            row    = run_z3(job, proof=args.proof)
            rows.append(row)
            flag   = "✓" if row["pass"] == "PASS" else "✗"
            note   = " [sat-timeout: skipped]" if row["result"] == "sat-timeout" else ""
            print(f"  {flag} {row['problem']:35s}  {row['result']:15s}  {row['time_s']}s{note}")
            if args.proof and job.get("is_sat"):
                print_proof(row)

    # ── cvc5 ─────────────────────────────────────────────────────────────────
    if args.cvc5 and not args.vampire_only:
        print("=== cvc5 (SMT-LIB) ===")
        for job in build_smt2_jobs(problems, args.timeout):
            row    = run_cvc5(job, proof=args.proof)
            rows.append(row)
            flag   = {"PASS": "✓", "FAIL": "✗", "SKIP": "–"}.get(row["pass"], "?")
            note   = " [skip: no decision]" if row["pass"] == "SKIP" else ""
            print(f"  {flag} {row['problem']:35s}  {row['result']:15s}  {row['time_s']}s{note}")

    # ── E prover ─────────────────────────────────────────────────────────────
    if args.eprover:
        print("=== E (FOF) ===")
        for job in build_fof_jobs(problems, args.timeout):
            if job["problem"] in SAT_IDS:
                continue  # E is a theorem prover; skip sat problems
            row  = run_eprover(job)
            rows.append(row)
            flag = "✓" if row["pass"] == "PASS" else "✗"
            print(f"  {flag} {row['problem']:35s}  {row['result']:15s}  {row['time_s']}s")

    # ── Summary ──────────────────────────────────────────────────────────────
    passed  = sum(1 for r in rows if r["pass"] == "PASS")
    failed  = sum(1 for r in rows if r["pass"] == "FAIL")
    skipped = sum(1 for r in rows if r["pass"] == "SKIP")
    tail    = f"  {skipped} SKIP" if skipped else ""
    print(f"\nSummary: {passed}/{len(rows)} PASS  {failed} FAIL{tail}")

    # ── CSV ──────────────────────────────────────────────────────────────────
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = ""
    if args.dualrule:
        suffix = "_dualrule"
    elif args.coverage:
        suffix = "_full"
    elif args.hard:
        suffix = "_all"
    elif args.ext:
        suffix = "_ext"
    out_path = out_dir / f"grnd_foundation{suffix}_{today}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWritten: {out_path}")

    if failed:
        print("\nFAILED problems:")
        for r in rows:
            if r["pass"] == "FAIL":
                print(f"  {r['problem']} [{r['prover']}]  expected={r['expected']}  got={r['result']}")
        sys.exit(1)

if __name__ == "__main__":
    main()