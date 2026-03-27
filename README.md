# ODRL Grounding Benchmark

Mechanized verification benchmark for the paper:
**"What Does ODRL Mean? Grounding Permissions, Prohibitions,
and Duties in Deontic Logic and Foundational Ontology"**

39 problems (TPTP/FOF + SMT-LIB 2 + Turtle) verifying the
UFO-L grounding of ODRL across three independent provers.

## Repository structure

```
Generators/   Python scripts that generate all problem files
Problems/     Generated TPTP/FOF, SMT-LIB 2, and Turtle files
Isabelle/     Isabelle/HOL mechanization
```

## Requirements

- [Vampire 5.0.0](https://vprover.github.io/)
- [Z3 4.12.2](https://github.com/Z3Prover/z3)
- [E 3.2.5](https://wwwlehre.dhbw-stuttgart.de/~sschulz/E/E.html)
- Python 3.10+, [uv](https://docs.astral.sh/uv/)
- Isabelle 2025 (for Isabelle/HOL verification only)

## Reproduce all results

```bash
cd ~/odrl-grounding-benchmark

# Step 1 — Generate axiom files
uv run Generators/gen_layer0_signature.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer0-Signature
uv run Generators/gen_layer1_deontic.py \
  --out-dir Problems/DeonticOntology/Axioms/Layer1-Deontic

# Step 2 — Generate all 39 problems (117 files)
uv run Generators/gen_foundation_problems.py \
  --out-dir Problems/DeonticOntology --dualrule

# Step 3 — Validate: Vampire + Z3 (78 checks, all pass)
cd Generators
uv run run_grnd_validation.py --dualrule --timeout 30

# Step 4 — Validate: Vampire + E (75 checks, all pass)
uv run run_grnd_validation.py --dualrule --timeout 30 \
  --eprover --vampire-only
```

## Isabelle/HOL

```bash
isabelle build -D Isabelle/
# Expected: Finished ODRLDeonticOntology in ~8s
```

## Results summary

| Prover | Problems | Checks | Result |
|---|---|---|---|
| Vampire 5.0.0 | 39 | 39 | 39/39 ✓ |
| Z3 4.12.2 | 39 | 39 | 39/39 ✓ |
| E 3.2.5 | 36* | 36 | 36/36 ✓ |
| Isabelle/HOL | — | 11 axioms + 23 lemmas | all ✓ |

\* E skips the 3 satisfiability problems (E is refutation-complete only).
