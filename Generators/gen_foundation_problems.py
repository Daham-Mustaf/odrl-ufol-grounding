"""
gen_foundation_problems.py
==========================
Generates FOF/TPTP (.p), SMT-LIB (.smt2), and Turtle (.ttl) files for the
FOIS 2026 deontic grounding validation (Paper §6).
Module structure:
  axiom_data.py        — FOF_AXIOM_DICT, SMT2_AXIOMS, shared constants
  problem_data.py      — PROBLEMS list (GRND001-009), write_ttl_policy()
  problem_data_ext.py  — PROBLEMS_EXT (GRND010-018, easy/medium)
  problem_data_hard.py — PROBLEMS_HARD (GRND019-024, hard)
  writers.py           — write_fof_problem(), write_smt2_problem()
  gen_foundation_problems.py  — this file: main() only
CHANGELOG v1.5:
  - --ext flag: include extension problems GRND010-018
  - --hard flag: include hard problems GRND019-024; implies --ext automatically
  - Bug 1: --hard now implies --ext (hard problems depend on ext axioms)
  - Bug 2: verify counts computed dynamically from actual problem lists
  - Bug 3: dead ax_list assignment removed (was computed but never printed)
  - Bug 4: file count corrects for None ttl_path
  - Usage comment corrected: --hard alone is sufficient for all problems
  - verify_all.sh print aligned: --hard alone shown (not --ext --hard)
CHANGELOG v1.4:
  - Split into modules: axiom_data, problem_data, writers
  - Real .ttl policy files written to Problems/DeonticOntology/Policies/
  - Policy link added to every .p and .smt2 header
  - SMT2_PREAMBLE imported from gen_layer0_signature.generate_smt2()
  - TTL uses real Turtle syntax
CHANGELOG v1.3:
  - Per-problem axiom inlining (fof_axioms key)
CHANGELOG v1.2:
  - FOF files use include() for Layer0 + inline Layer1 subset
Output layout:
  Problems/DeonticOntology/
    Axioms/
      Layer0-Signature/
        GRND000-0.ax        -- signature    (gen_layer0_signature.py)
        GRND000-0.smt2
      Layer1-Deontic/
        GRND-AX-1.ax        -- theory axioms (gen_layer1_deontic.py)
        GRND-AX-1.smt2      -- SMT-LIB reference copy
    Policies/
        GRND001-policy.ttl  -- real Turtle policy per problem
        ...
    Consistency/
        GRND001-1.p / .smt2
    Entailment/
        GRND002-1.p / .smt2  ...
    Discriminating/
        GRND007-open-1.p / .smt2  ...
Usage:
    # base problems only (GRND001-009)
    uv run Generators/DeonticOntology/gen_foundation_problems.py \
      --out-dir Problems/DeonticOntology

    # base + extension (GRND001-018)
    uv run Generators/DeonticOntology/gen_foundation_problems.py \
      --out-dir Problems/DeonticOntology --ext

    # all problems (GRND001-024); --hard implies --ext automatically
    uv run Generators/DeonticOntology/gen_foundation_problems.py \
      --out-dir Problems/DeonticOntology --hard
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from problem_data import PROBLEMS, write_ttl_policy
from writers import write_fof_problem, write_smt2_problem

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


def main():
    parser = argparse.ArgumentParser(
        description="Generate FOF/SMT-LIB/TTL files for GRND DeonticOntology v1.5."
    )
    parser.add_argument(
        "--out-dir",
        default="Problems/DeonticOntology",
        help="Root output directory (default: Problems/DeonticOntology)",
    )
    parser.add_argument(
        "--ext",
        action="store_true",
        help="Also generate extension problems GRND010-018 (easy/medium)",
    )
    parser.add_argument(
        "--hard",
        action="store_true",
        help="Also generate hard problems GRND019-024 (implies --ext)",
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Also generate coverage problems GRND025-034 (implies --hard)",
    )
    parser.add_argument(
        "--dualrule",
        action="store_true",
        help="Also generate dual-rule DRK problems GRND035-036 (implies --coverage)",
    )
    # kept for backward compat with run_all.sh — values ignored
    parser.add_argument("--sig-ax",  default=None, help=argparse.SUPPRESS)
    parser.add_argument("--sig-smt", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    # --hard implies --ext; GRND019-024 depend on GRND010-018.
    # Build problem list in correct order with no gaps.
    problems = PROBLEMS[:]
    if args.dualrule:
        problems += PROBLEMS_EXT
        problems += PROBLEMS_HARD
        problems += PROBLEMS_COVERAGE
        problems += PROBLEMS_DUALRULE
        tier = "base+ext+hard+coverage+dualrule"
    elif args.coverage:
        problems += PROBLEMS_EXT
        problems += PROBLEMS_HARD
        problems += PROBLEMS_COVERAGE
        tier = "base+ext+hard+coverage"
    elif args.hard:
        problems += PROBLEMS_EXT   # always include ext when hard is requested
        problems += PROBLEMS_HARD
        tier = "base+ext+hard"
    elif args.ext:
        problems += PROBLEMS_EXT
        tier = "base+ext"
    else:
        tier = "base"

    out_dir = Path(args.out_dir)
    written = []

    for p in problems:
        ttl_path  = write_ttl_policy(p, out_dir)
        fof_path  = write_fof_problem(p, out_dir)
        smt2_path = write_smt2_problem(p, out_dir)
        written.append((fof_path, smt2_path, ttl_path))

        print(f"  {p['id']:30s}  FOF:{p['status_fof']:16s}  {fof_path.name}")
        print(f"  {'':30s}  SMT:{p['status_smt']:16s}  {smt2_path.name}")
        if ttl_path:
            print(f"  {'':30s}  TTL:             {ttl_path.name}")

    # Count actual files written; ttl_path may be None for some problems.
    n_problems = len(written)
    n_files = sum(2 + (1 if ttl else 0) for _, _, ttl in written)

    # Derive prover-check counts dynamically from actual problem lists.
    # Each problem generates one FOF + one SMT-LIB check.
    base_checks = len(PROBLEMS) * 2
    ext_checks  = (len(PROBLEMS) + len(PROBLEMS_EXT)) * 2
    hard_checks = (len(PROBLEMS) + len(PROBLEMS_EXT) + len(PROBLEMS_HARD)) * 2

    print(f"\nTotal [{tier}]: {n_problems} problems ({n_files} files written)")
    coverage_checks = (len(PROBLEMS) + len(PROBLEMS_EXT) + len(PROBLEMS_HARD) + len(PROBLEMS_COVERAGE)) * 2
    dualrule_checks = coverage_checks + len(PROBLEMS_DUALRULE) * 2
    print(f"\nProver check counts (FOF + SMT-LIB per problem):")
    print(f"  base              : {base_checks:3d} checks   bash verify_all.sh")
    print(f"  base + ext        : {ext_checks:3d} checks   bash verify_all.sh --ext")
    print(f"  base+ext+hard     : {hard_checks:3d} checks   bash verify_all.sh --hard")
    print(f"  base+ext+hard+cov : {coverage_checks:3d} checks   bash verify_all.sh --coverage")
    print(f"  +dualrule         : {dualrule_checks:3d} checks   bash verify_all.sh --dualrule")


if __name__ == "__main__":
    main()