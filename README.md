# ODRL Grounding in UFO-L

[![E 3.3.2](https://img.shields.io/badge/E-3.3.2-1f6feb)](https://github.com/eprover/eprover)
[![Vampire 5.0.1](https://img.shields.io/badge/Vampire-5.0.1-1f6feb)](https://github.com/vprover/vampire)
[![Z3 4.8.12](https://img.shields.io/badge/Z3-4.8.12-1f6feb)](https://github.com/Z3Prover/z3)
[![cvc5 1.3.4](https://img.shields.io/badge/cvc5-1.3.4-1f6feb)](https://github.com/cvc5/cvc5)


Mechanized verification benchmark and OWL profile for the paper:
**"What Does ODRL Mean? A Cross-Level Ontological Grounding of
Permissions, Prohibitions, and Duties in UFO-L"**

39 problems (TPTP/FOF + SMT-LIB 2 + Turtle) verifying the UFO-L
grounding of ODRL across three independent provers, plus the
ODRL-Legal (`odrl-l:`) OWL profile.

## TPTP Library

A subset of the first-order (TPTP/FOF) encodings in this benchmark has
been accepted into the Thousands of Problems for Theorem Provers (TPTP)
library, maintained by Geoff Sutcliffe (University of Miami). The
contribution is acknowledged in the [TPTP Technical Report](https://tptp.org/UserDocs/ProblemLibraryManual/TPTPTR.shtml#Conclusion). See
https://tptp.org/ for the library and its usage conditions.

The full problem set is mirrored here for reproducibility, alongside the
SMT-LIB 2 counterparts and the source policies.

## Repository structure
```
Generators/           Python scripts that generate all problem files
Problems/             Generated TPTP/FOF, SMT-LIB 2, and Turtle files
Isabelle/             Isabelle/HOL mechanization
ODRL-Legal-Profile/   OWL profile (odrl-l:): the ODRL-Legal profile
```

## Requirements
- [Vampire 5.0.0](https://vprover.github.io/)
- [Z3 4.12.2](https://github.com/Z3Prover/z3)
- [E 3.2.5](https://wwwlehre.dhbw-stuttgart.de/~sschulz/E/E.html)
- Python 3.10+, [uv](https://docs.astral.sh/uv/)
- Isabelle 2025 (for Isabelle/HOL verification only)

## Reproduce all results
```bash
cd ~/odrl-ufol-grounding

# Step 1: Generate axiom files
uv run Generators/gen_layer0_signature.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer0-Signature
uv run Generators/gen_layer1_deontic.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer1-Deontic

# Step 2: Generate all 39 problems (117 files)
uv run Generators/gen_foundation_problems.py \
  --out-dir Problems/DeonticOntology --dualrule

# Step 3: Validate with Vampire + Z3 (78 checks)
cd Generators
uv run run_grnd_validation.py --dualrule --timeout 30

# Step 4: Validate with Vampire + E (75 checks)
uv run run_grnd_validation.py --dualrule --timeout 30 \
  --eprover --vampire-only
```

## Isabelle/HOL
```bash
isabelle build -D odrl_isabelle_formalization/
# Expected: Finished ODRLDeonticOntology in ~8s
```

## Results summary
| Prover | Problems | Checks | Result |
|---|---|---|---|
| Vampire 5.0.0 | 39 | 39 | 39/39 pass |
| Z3 4.12.2 | 39 | 39 | 39/39 pass |
| E 3.2.5 | 36* | 36 | 36/36 pass |
| Isabelle/HOL | n/a | 11 axioms + 23 lemmas | all pass |

\* E skips the 3 satisfiability problems (E is refutation-complete only).