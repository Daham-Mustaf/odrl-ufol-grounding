# ODRL Grounding Benchmark

39 TPTP/FOF + SMT-LIB 2 problems verifying the UFO-L grounding of ODRL.

## Requirements
- Vampire 5.0.0
- Z3 4.12.2
- E 3.2.5
- Python 3.10+, uv

## Reproduce all results
```bash
cd Generators

# Generate all 39 problems
uv run gen_foundation_problems.py \
  --out-dir ../Problems/DeonticOntology --dualrule

# Validate: Vampire + Z3 (78 checks)
uv run run_grnd_validation.py --dualrule --timeout 30

# Validate: Vampire + E (75 checks)
uv run run_grnd_validation.py --dualrule --timeout 30 \
  --eprover --vampire-only
```

## Isabelle/HOL
```bash
isabelle build -D Isabelle/
```
