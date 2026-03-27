"""
writers.py
==========
File writers for the FOIS 2026 deontic grounding benchmark.
Imports axiom content from axiom_data.py and problem definitions
from problem_data.py.
Exported functions:
  write_fof_problem(p, out_dir)   -> Path
  write_smt2_problem(p, out_dir)  -> Path
Imported by: gen_foundation_problems.py
Fix history:
  v1.5 — import corrected from gen_layer0_signature (Bug 1 — was gen_signature);
          _get_axiom helper added for diagnostic KeyError on missing axiom keys
            (Bug 2 — was silent KeyError with no problem/key context);
          SMT2 axiom count computed dynamically from len(SMT2_AXIOMS)
            (Bug 3 — was hardcoded 28, actual count is len(SMT2_AXIOMS));
          TTL header truncated to 5 lines in FOF/SMT2 for Vampire readability
            (Observation 1);
          SMT2 description strip uses removeprefix logic not lstrip('% ')
            (Observation 2 — lstrip is character-set not prefix-strip).
          SMT2 writer asymmetry documented — full axiom set always embedded
          because Z3 does not timeout on full set; FOF uses per-problem subsets
          to avoid Vampire timeouts (was undocumented).
"""
import sys
import textwrap
from pathlib import Path
from datetime import date

# Import preamble from gen_layer0_signature so it never diverges from the
# generated GRND000-0.smt2 file.
sys.path.insert(0, str(Path(__file__).parent))
from gen_layer0_signature import generate_smt2 as _gen_smt2
from axiom_data import (
    FOF_AXIOM_DICT,
    SMT2_AXIOMS,
    SMT2_APPENDIX_SORTS,
    FOF_APPENDIX_DECLS,
)

VERSION = "1.5"
GENERATOR = f"gen_foundation_problems.py v{VERSION}"
SMT2_PREAMBLE = _gen_smt2()

# Maximum TTL lines inlined into problem file headers.
# Full policy is always in Policies/<id>-policy.ttl.
_TTL_HEADER_MAX_LINES = 5


# ============================================================================
# HELPERS
# ============================================================================

def _get_axiom(key: str, problem_id: str) -> str:
    """Look up a FOF axiom by key with a diagnostic error if missing."""
    if key not in FOF_AXIOM_DICT:
        raise KeyError(
            f"Problem {problem_id}: axiom key '{key}' not found in FOF_AXIOM_DICT. "
            f"Available keys: {sorted(FOF_AXIOM_DICT)}"
        )
    return FOF_AXIOM_DICT[key]


def _ttl_header_lines(ttl: str, prefix: str) -> list[str]:
    """Return TTL lines for embedding in a .p or .smt2 header, truncated."""
    all_lines = ttl.strip().splitlines()
    shown = all_lines[:_TTL_HEADER_MAX_LINES]
    result = [f"{prefix}{line}" for line in shown]
    if len(all_lines) > _TTL_HEADER_MAX_LINES:
        remaining = len(all_lines) - _TTL_HEADER_MAX_LINES
        result.append(f"{prefix}... ({remaining} more lines — see Policies/ file)")
    return result


def _strip_fof_comment_prefix(line: str) -> str:
    """Strip a single leading '% ' prefix (not character-set lstrip)."""
    if line.startswith("% "):
        return line[2:]
    if line.startswith("%"):
        return line[1:]
    return line


# ============================================================================
# FOF WRITER
# ============================================================================

def write_fof_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-1.p"
    conj = p.get("fof_conjecture")

    lines = [
        "%--------------------------------------------------------------------------",
        f"% File     : {p['id']}-1.p",
        "% Domain   : Deontic Ontology / ODRL Grounding",
        f"% Problem  : {p['name']}",
        f"% Status   : {p['status_fof']}",
        "% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026",
        f"% Policy   : Policies/{p['id']}-policy.ttl",
        f"% Generated: {date.today().isoformat()} by {GENERATOR}",
        "%",
    ]
    for line in textwrap.dedent(p["description"]).strip().splitlines():
        lines.append(f"% {line}")

    # TTL summary in header — truncated for Vampire --proof readability
    if p.get("ttl"):
        lines.append("%")
        lines.append("% ODRL Policy (Turtle) — see Policies/ for full file:")
        lines.extend(_ttl_header_lines(p["ttl"], "% "))

    lines += [
        "%--------------------------------------------------------------------------",
        "",
        "% Layer 0: Signature (sorts, rfr/decl, position disjointness)",
        "include('Axioms/Layer0-Signature/GRND000-0.ax').",
        "",
        "% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)",
        "% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid",
        "% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not",
        "% timeout on the full set). This asymmetry is intentional.",
        *[_get_axiom(ax, p["id"]) for ax in p.get("fof_axioms", [])],
        "",
        FOF_APPENDIX_DECLS,
        "%--------------------------------------------------------------------------",
        "% Ground instance (gamma)",
        "%--------------------------------------------------------------------------",
        p["fof_extra_decls"],
    ]

    if conj is not None:
        lines += [
            "%--------------------------------------------------------------------------",
            "% Conjecture",
            "%--------------------------------------------------------------------------",
            "fof(conjecture, conjecture,",
            f"    ( {conj} )).",
        ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ============================================================================
# SMT-LIB WRITER
# ============================================================================

def write_smt2_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-1.smt2"
    conj = p.get("smt2_conjecture")

    lines = [
        "; --------------------------------------------------------------------------",
        f"; File     : {p['id']}-1.smt2",
        "; Domain   : Deontic Ontology / ODRL Grounding",
        f"; Problem  : {p['name']}",
        f"; Status   : {p['status_smt']}",
        "; Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026",
        f"; Policy   : Policies/{p['id']}-policy.ttl",
        f"; Generated: {date.today().isoformat()} by {GENERATOR}",
        ";",
    ]
    for line in textwrap.dedent(p["description"]).strip().splitlines():
        lines.append(f"; {_strip_fof_comment_prefix(line)}")

    # TTL summary in header — truncated for readability
    if p.get("ttl"):
        lines.append(";")
        lines.append("; ODRL Policy (Turtle) — see Policies/ for full file:")
        lines.extend(_ttl_header_lines(p["ttl"], "; "))

    skip_axioms = p.get("skip_smt2_axioms", False)
    lines += [
        "; --------------------------------------------------------------------------",
        "",
        "; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===",
        "; === Source: Axioms/Layer0-Signature/GRND000-0.smt2 ===",
        SMT2_PREAMBLE,
        "; === Appendix A.0 additional sorts/predicates ===",
        SMT2_APPENDIX_SORTS,
        "",
    ]

    if skip_axioms:
        lines += [
            "; === Layer 1: axioms omitted (skip_smt2_axioms=True) ===",
            "; === Problem is self-contained in smt2_extra_decls. ===",
            "",
        ]
    else:
        lines += [
            f"; === Layer 1: ALL paper axioms embedded ({len(SMT2_AXIOMS)} formulae) ===",
            "; === Z3 does not timeout on the full set; FOF inlines per-problem subsets ===",
            "; === only (fof_axioms key) to avoid Vampire timeouts. Asymmetry intentional. ===",
            "; === Authoritative source: Axioms/Layer1-Deontic/GRND-AX-1.smt2 ===",
            "; === (SMT-LIB has no include directive — axioms embedded directly) ===",
            "",
        ]
        for name, formula in SMT2_AXIOMS:
            lines.append(f"; {name}")
            lines.append(formula)
            lines.append("")

    lines += [
        "; === Ground instance (gamma) ===",
        p["smt2_extra_decls"],
    ]

    if conj is not None:
        lines += [
            "; === Negated conjecture ===",
            conj,
            "",
        ]

    lines.append("(check-sat)")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path