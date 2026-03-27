"""
gen_layer1_deontic.py
=====================
Generates the Layer 1 deontic grounding axiom files:
  Problems/DeonticOntology/Axioms/Layer1-Deontic/GRND-AX-1.ax    — FOF/TPTP
  Problems/DeonticOntology/Axioms/Layer1-Deontic/GRND-AX-1.smt2  — SMT-LIB reference
Contains: Ax5.1-5.10, A1-A3, B1-B3
Requires: Layer0-Signature/GRND000-0.ax (included by problem files, not here)
SMT-LIB note:
  GRND-AX-1.smt2 is a reference/documentation file only.
  SMT-LIB has no include directive — axioms are embedded directly in
  each .smt2 problem file by gen_foundation_problems.py.
  SMT2_AXIOMS is imported from axiom_data.py to guarantee the reference
  copy is always identical to what is embedded.
Usage:
    uv run Generators/DeonticOntology/gen_layer1_deontic.py \
      --out-dir Problems/DeonticOntology/Axioms/Layer1-Deontic
"""
import argparse
import textwrap
from pathlib import Path
from datetime import date
import sys
sys.path.insert(0, str(Path(__file__).parent))
from axiom_data import SMT2_AXIOMS

META = {
    "domain":  "Deontic Ontology / ODRL Grounding",
    "source":  "Mohammed et al., What Does ODRL Mean? FOIS 2026",
    "version": "1.5",
}

def header() -> str:
    return textwrap.dedent(f"""\
        %--------------------------------------------------------------------------
        % File     : GRND-AX-1.ax
        % Domain   : {META['domain']}
        % Axioms   : Deontic grounding axioms (Ax5.1-5.10, A1-A3, B1-B3)
        % Version  : {META['version']}
        % English  : Layer 1 axioms for ODRL deontic grounding.
        %            Requires Layer0-Signature/GRND000-0.ax (included by
        %            problem files via include() — not repeated here).
        %
        %            Ax5.1   Permission Relator — Weak    (ax:perm-relator-weak)
        %            Ax5.2   Permission Relator — Strong  (ax:perm-relator-strong;
        %                      founds_imm; rho_P != rho_I)
        %            Ax5.3   Prohibition Relator — Conduct (ax:proh-relator-conduct)
        %            Ax5.4   Prohibition Relator — Remedy  (ax:proh-relator-remedy;
        %                      founds_rem; rho_F != rho_R)
        %            Ax5.5   Obligation Relator            (ax:obl-relator)
        %            Ax5.6a  Unique Founding  — founds     (clause 1: same e,r -> same rho)
        %            Ax5.6b  Unique Event     — founds     (clause 2: same rho,r -> same e)
        %            Ax5.6c  Unique Founding  — founds_rem
        %            Ax5.6d  Unique Event     — founds_rem
        %            Ax5.6e  Unique Founding  — founds_imm
        %            Ax5.6f  Unique Event     — founds_imm
        %            Ax5.7   ODRL Relator Typing (3 rules: founds / founds_rem / founds_imm)
        %                      NOTE: base case consolidated as disjunction for brevity;
        %                      logically equivalent to three separate axioms.
        %            Ax5.8   Correlativity (4 biconditionals, ∃! on both sides)
        %            Ax5.9   Normative Position Incompatibility — cross-relator
        %                      (ax:cross-relator; normative axiom independent of
        %                       UFO type disjointness; paper Ax5.9)
        %            Corollary  Permission-Duty Conflict Within a Relator
        %                      (ax:conflict; derived from Ax5.9; role=corollary)
        %            Ax5.10  Disability Precludes Prohibition Creation
        %                      (ax:disability-block)
        %            Ax5.11  ODRL Relators Subsume Legal Relators
        %                      (ax:odrl-rel-is-rel; odrl_rel => legal_relator)
        %            A1      Normative State Changes Require Institutional Event
        %            A2      Institutional Events Require Competent Agent
        %            A3      Competence Is a Power-Subjection Pair
        %            B1      Performing Prohibited Action = NormStateChange
        %            B2      Power Content Links to Founding Event (founds_rem)
        %            B3      Subjection Content Links to Founding Event (founds_rem)
        %
        % Source   : {META['source']}
        % Generated: {date.today().isoformat()} by gen_layer1_deontic.py
        %
        % Status   : Layer 1 — Theory-Specific Deontic Axioms
        %
        % Syntax   : Number of formulae : 28 (27 axioms, 1 corollary)
        %
        % SPC      : FOF_THM_RFN
        %
        % Predicates (from Layer0 — UFO-L terms):
        %   perm/1, proh/1, obl/1, has_rem/1, strong/1
        %   aee/2, aer/2, act/2, tgt/2, activates/2
        %   founds/3, founds_rem/3, founds_imm/3
        %   part_of/2, bearer/2, cnt/3
        %   permission/1, no_right/1, duty/1, right/1
        %   power/1, subjection/1, immunity/1, disability/1
        %   odrl_rel/1, legal_relator/1, action/1, forbearance/1
        %
        % Functions (from Layer0):
        %   rfr/1  : Act -> Forbearance
        %   decl/1 : Act -> Act
        %
        % Appendix A.0 predicates (declared in problem files):
        %   norm_state_change/4, inst_event/1, triggers/5
        %   competent_for/2, about_event/2, does/3, rem_act/2
        %   duty_rem — distinguished ground constant; declared in problem files
        %
        % CHANGELOG v1.5:
        %   - Bug 1 : liberty -> permission, claim -> right (UFO-L terms)
        %   - Bug 2 : B1 existential B with rem_act guard (was unsound)
        %   - Bug 3 : Correlativity: ∃! on both sides of all 4 biconditionals
        %   - Bug 4 : ax5.5/ax5.6 numbering fixed (obl=5.5, unique-founding=5.6)
        %   - Bug 5 : Unique-event clauses added for founds_rem and founds_imm
        %   - Bug 6 : ax:conflict demoted to corollary role (was axiom Ax5.9)
        %             ax:cross-relator promoted to Ax5.9 (was Ax5.10)
        %   - Bug 7 : Axiom names aligned to paper labels
        %             (_basic -> _weak/_conduct; _consistency -> _cross_relator)
        %   - Bug 8 : ax_odrl_rel_is_rel subsumption axiom added
        %   - Count : 20 -> 28 formulae (27 axioms + 1 corollary)
        % CHANGELOG v1.4:
        %   - version aligned with gen_foundation_problems.py v1.4
        %   - GRND-AX-1.smt2 imported from axiom_data.SMT2_AXIOMS
        %--------------------------------------------------------------------------
    """)

AXIOMS = """\
%--------------------------------------------------------------------------
% Ax5.1  Permission Relator — Weak                    [ax:perm-relator-weak]
% A permission activation founds a relator with Permission + NoRight.
%--------------------------------------------------------------------------
fof(ax_perm_relator_weak, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & permission(L) & bearer(L,X) & cnt(L,A,T) & part_of(L,Rho)
          & no_right(N)   & bearer(N,Y) & cnt(N,A,T) & part_of(N,Rho) ) )).

%--------------------------------------------------------------------------
% Ax5.2  Permission Relator — Strong               [ax:perm-relator-strong]
% Requires strong(P) asserted by profile extension (not ODRL 2.2).
% rho_I is a DISTINCT simple relator founded by founds_imm, not founds,
% so ax_unique_founding cannot collapse rho_P = rho_I.
%--------------------------------------------------------------------------
fof(ax_perm_relator_strong, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & strong(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T)
        & activates(E,P) )
     => ? [RhoI, Im, Db] :
          ( founds_imm(E,RhoI,P)
          & immunity(Im)   & bearer(Im,X) & cnt(Im,A,T) & part_of(Im,RhoI)
          & disability(Db) & bearer(Db,Y) & cnt(Db,A,T) & part_of(Db,RhoI) ) )).

%--------------------------------------------------------------------------
% Ax5.3  Prohibition Relator — Conduct           [ax:proh-relator-conduct]
% A prohibition activation founds a relator with Duty + Right.
% Content is rfr(A) — the forbearance (omission) of performing A.
%--------------------------------------------------------------------------
fof(ax_proh_relator_conduct, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & right(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).

%--------------------------------------------------------------------------
% Ax5.4  Prohibition Relator — Remedy             [ax:proh-relator-remedy]
% rho_R is a DISTINCT simple relator founded by founds_rem, not founds,
% so ax_unique_founding cannot collapse rho_F = rho_R.
% Power is constituted at activation time, not at violation time.
%--------------------------------------------------------------------------
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) )
     => ? [RhoR, Pw, S] :
          ( founds_rem(E,RhoR,F)
          & power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,RhoR)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,RhoR) ) )).

%--------------------------------------------------------------------------
% Ax5.5  Obligation Relator                              [ax:obl-relator]
% An obligation activation founds a relator with Duty + Right.
%--------------------------------------------------------------------------
fof(ax_obl_relator, axiom,
    ! [D, X, Y, A, T, E] :
      ( ( obl(D) & aee(D,X) & aer(D,Y) & act(D,A) & tgt(D,T) & activates(E,D) )
     => ? [Rho, Du, C] :
          ( founds(E,Rho,D)
          & duty(Du) & bearer(Du,X) & cnt(Du,A,T) & part_of(Du,Rho)
          & right(C) & bearer(C,Y)  & cnt(C,A,T)  & part_of(C,Rho) ) )).

%--------------------------------------------------------------------------
% Ax5.6  Unique Founding — all three founding predicates      [ax:unique-founding]
% Both clauses applied to founds, founds_rem, founds_imm (UFO axiom a77).
% Clause 1: same (e,r) founds at most one relator.
% Clause 2: same (rho,r) is founded by at most one event.
%--------------------------------------------------------------------------
fof(ax_unique_founding, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds(E,Rho1,R) & founds(E,Rho2,R) ) => Rho1 = Rho2 )).
fof(ax_unique_event, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds(E1,Rho,R) & founds(E2,Rho,R) ) => E1 = E2 )).
fof(ax_unique_founding_rem, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds_rem(E,Rho1,R) & founds_rem(E,Rho2,R) ) => Rho1 = Rho2 )).
fof(ax_unique_event_rem, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds_rem(E1,Rho,R) & founds_rem(E2,Rho,R) ) => E1 = E2 )).
fof(ax_unique_founding_imm, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds_imm(E,Rho1,R) & founds_imm(E,Rho2,R) ) => Rho1 = Rho2 )).
fof(ax_unique_event_imm, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds_imm(E1,Rho,R) & founds_imm(E2,Rho,R) ) => E1 = E2 )).

%--------------------------------------------------------------------------
% Ax5.7  ODRL Relator Typing                        [ax:odrl-rel-typing]
% All three founding predicates produce odrl_rel-typed relators.
% NOTE: base case consolidated as disjunction for brevity;
% logically equivalent to three separate per-predicate axioms.
%--------------------------------------------------------------------------
fof(ax_odrl_rel_typing, axiom,
    ! [E, Rho, R] :
      ( ( founds(E,Rho,R) & ( perm(R) | proh(R) | obl(R) ) )
     => odrl_rel(Rho) )).
fof(ax_odrl_rel_typing_rem, axiom,
    ! [E, Rho, R] :
      ( ( founds_rem(E,Rho,R) & proh(R) )
     => odrl_rel(Rho) )).
fof(ax_odrl_rel_typing_imm, axiom,
    ! [E, Rho, R] :
      ( ( founds_imm(E,Rho,R) & perm(R) )
     => odrl_rel(Rho) )).

%--------------------------------------------------------------------------
% Ax5.8  Correlativity — 4 biconditionals, ∃! on BOTH sides  [ax:correlativity]
% Each ODRL relator pairs each position with exactly one correlative
% over the same action-target content. odrl_rel(Rho) guards each.
%--------------------------------------------------------------------------
fof(ax_correlativity_permission, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [L] : ( permission(L) & part_of(L,Rho) & cnt(L,A,T)
                    & ! [L2] : ( ( permission(L2) & part_of(L2,Rho) & cnt(L2,A,T) )
                                => L2 = L ) ) )
        <=> ( ? [N] : ( no_right(N) & part_of(N,Rho) & cnt(N,A,T)
                      & ! [M] : ( ( no_right(M) & part_of(M,Rho) & cnt(M,A,T) )
                                 => M = N ) ) ) ) )).

fof(ax_correlativity_duty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [D] : ( duty(D) & part_of(D,Rho) & cnt(D,A,T)
                    & ! [D2] : ( ( duty(D2) & part_of(D2,Rho) & cnt(D2,A,T) )
                                => D2 = D ) ) )
        <=> ( ? [C] : ( right(C) & part_of(C,Rho) & cnt(C,A,T)
                      & ! [K] : ( ( right(K) & part_of(K,Rho) & cnt(K,A,T) )
                                 => K = C ) ) ) ) )).

fof(ax_correlativity_power, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Pw] : ( power(Pw) & part_of(Pw,Rho) & cnt(Pw,A,T)
                      & ! [Pw2] : ( ( power(Pw2) & part_of(Pw2,Rho) & cnt(Pw2,A,T) )
                                   => Pw2 = Pw ) ) )
        <=> ( ? [S] : ( subjection(S) & part_of(S,Rho) & cnt(S,A,T)
                      & ! [S2] : ( ( subjection(S2) & part_of(S2,Rho) & cnt(S2,A,T) )
                                  => S2 = S ) ) ) ) )).

fof(ax_correlativity_immunity, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Im] : ( immunity(Im) & part_of(Im,Rho) & cnt(Im,A,T)
                      & ! [Im2] : ( ( immunity(Im2) & part_of(Im2,Rho) & cnt(Im2,A,T) )
                                   => Im2 = Im ) ) )
        <=> ( ? [Db] : ( disability(Db) & part_of(Db,Rho) & cnt(Db,A,T)
                       & ! [Db2] : ( ( disability(Db2) & part_of(Db2,Rho) & cnt(Db2,A,T) )
                                    => Db2 = Db ) ) ) ) )).

%--------------------------------------------------------------------------
% Ax5.9  Normative Position Incompatibility — cross-relator  [ax:cross-relator]
% No agent can simultaneously bear a Permission to Act and a Duty to Omit
% over the same <a,t>, regardless of which relator they belong to.
% This is a NORMATIVE axiom — independent of UFO type disjointness, which
% governs whether a single moment can have two types, not whether a bearer
% can hold two distinct moments of incompatible types (Giancarlo Comment 13).
%--------------------------------------------------------------------------
fof(ax_cross_relator, axiom,
    ! [L, D, X, A, T] :
      ( ( permission(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)       & bearer(D,X) & cnt(D,rfr(A),T) )
     => $false )).

%--------------------------------------------------------------------------
% Corollary  Permission-Duty Conflict Within a Relator        [ax:conflict]
% No ODRL relator contains Permission and Duty-to-refrain for same bearer
% over the same <a,t>. Follows immediately from Ax5.9 (ax_cross_relator):
% co-instantiation in any bearer is impossible within a relator in
% particular. Retained as a corollary for prover convenience.
%--------------------------------------------------------------------------
fof(ax_conflict, corollary,
    ! [Rho, L, D, X, A, T] :
      ( ( part_of(L,Rho) & part_of(D,Rho)
        & permission(L) & duty(D)
        & bearer(L,X) & bearer(D,X)
        & cnt(L,A,T)  & cnt(D,rfr(A),T) )
     => $false )).

%--------------------------------------------------------------------------
% Ax5.10  Disability Precludes Prohibition Creation         [ax:disability-block]
% No prohibition by Y over (A,T) can exist while Y holds Disability
% over (A,T). Disability renders the institutional act void.
%--------------------------------------------------------------------------
fof(ax_disability_block, axiom,
    ! [F, X, Y, A, T] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) )
     => ~ ? [Db] : ( disability(Db) & bearer(Db,Y) & cnt(Db,A,T) ) )).

%--------------------------------------------------------------------------
% Ax5.11  ODRL Relators Subsume Legal Relators           [ax:odrl-rel-is-rel]
% Every ODRL-typed relator is also a UFO legal relator.
% Needed when background KBs reason directly over legal_relator/1.
%--------------------------------------------------------------------------
fof(ax_odrl_rel_is_rel, axiom,
    ! [Rho] : ( odrl_rel(Rho) => legal_relator(Rho) )).

%--------------------------------------------------------------------------
% A1  Normative State Changes Require an Institutional Event
%--------------------------------------------------------------------------
fof(ax_A1, axiom,
    ! [X, A, T, Q] :
      ( norm_state_change(X,A,T,Q)
     => ? [E] : ( inst_event(E) & triggers(E,X,A,T,Q) ) )).

%--------------------------------------------------------------------------
% A2  Institutional Events Require a Competent Agent
%--------------------------------------------------------------------------
fof(ax_A2, axiom,
    ! [E] :
      ( inst_event(E)
     => ? [Y] : competent_for(Y,E) )).

%--------------------------------------------------------------------------
% A3  Competence Is a Power-Subjection Pair
%--------------------------------------------------------------------------
fof(ax_A3, axiom,
    ! [Y, E] :
      ( competent_for(Y,E)
     => ? [Pw, S, X] :
          ( power(Pw)     & bearer(Pw,Y) & about_event(Pw,E)
          & subjection(S) & bearer(S,X)  & about_event(S,E) ) )).

%--------------------------------------------------------------------------
% B1  Performing a Prohibited Action Constitutes a NormStateChange
% B is existentially quantified and guarded by rem_act so the state
% change is scoped to the remedy action of F (not every action).
% duty_rem is a distinguished ground constant declared in problem files.
%--------------------------------------------------------------------------
fof(ax_B1, axiom,
    ! [F, X, A, T] :
      ( ( proh(F) & has_rem(F) & act(F,A) & tgt(F,T) & aee(F,X) & does(X,A,T) )
     => ? [B] : ( rem_act(F,B) & norm_state_change(X,B,T,duty_rem) ) )).

%--------------------------------------------------------------------------
% B2  Power Content Links to Founding Event (via founds_rem)
% Power lives in rho_R, not rho_F, so founds_rem is the correct predicate.
%--------------------------------------------------------------------------
fof(ax_B2, axiom,
    ! [Pw, A, T, Rho, E, R] :
      ( ( power(Pw) & cnt(Pw,decl(A),T) & part_of(Pw,Rho) & founds_rem(E,Rho,R) )
     => about_event(Pw,E) )).

%--------------------------------------------------------------------------
% B3  Subjection Content Links to Founding Event (via founds_rem)
% Subjection lives in rho_R, not rho_F, so founds_rem is correct.
%--------------------------------------------------------------------------
fof(ax_B3, axiom,
    ! [S, A, T, Rho, E, R] :
      ( ( subjection(S) & cnt(S,decl(A),T) & part_of(S,Rho) & founds_rem(E,Rho,R) )
     => about_event(S,E) )).
"""

def generate() -> str:
    return header() + "\n" + AXIOMS

def main():
    parser = argparse.ArgumentParser(
        description="Generate GRND-AX-1.ax and GRND-AX-1.smt2 — Layer 1 deontic axioms."
    )
    parser.add_argument(
        "--out-dir",
        default="Problems/DeonticOntology/Axioms/Layer1-Deontic",
    )
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    content = generate()

    if args.stdout:
        print(content)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write FOF axiom file
    ax_path = out_dir / "GRND-AX-1.ax"
    ax_path.write_text(content, encoding="utf-8")

    axiom_count = content.count("fof(")
    print(f"Written: {ax_path}")
    print(f"  Lines : {content.count(chr(10))}")
    print(f"  Formulae: {axiom_count} ({axiom_count - 1} axioms, 1 corollary)")
    print(f"\nInclude in problem files with:")
    print(f"  include('Axioms/Layer1-Deontic/GRND-AX-1.ax').")

    # Write SMT-LIB reference copy
    # SMT2_AXIOMS imported from axiom_data.py — guaranteed identical to
    # what is embedded in every .smt2 problem file by gen_foundation_problems.py.
    smt2_lines = [
        "; --------------------------------------------------------------------------",
        "; File     : GRND-AX-1.smt2",
        "; Domain   : Deontic Ontology / ODRL Grounding",
        f"; Version  : {META['version']}",
        "; Axioms   : Layer 1 deontic grounding axioms (Ax5.1-5.10, A1-A3, B1-B3)",
        f"; Refs     : {META['source']}",
        f"; Generated: {date.today().isoformat()} by gen_layer1_deontic.py",
        ";",
        "; NOTE: SMT-LIB 2 has no include directive.",
        "; These axioms are embedded directly in each .smt2 problem file.",
        "; This file is the authoritative reference — generated from",
        "; axiom_data.SMT2_AXIOMS to guarantee identity with embedded content.",
        "; --------------------------------------------------------------------------",
        "",
    ]
    for name, formula in SMT2_AXIOMS:
        smt2_lines.append(f"; {name}")
        smt2_lines.append(formula)
        smt2_lines.append("")

    smt2_path = out_dir / "GRND-AX-1.smt2"
    smt2_path.write_text("\n".join(smt2_lines), encoding="utf-8")
    smt2_count = len(SMT2_AXIOMS)
    print(f"Written: {smt2_path}")
    print(f"  SMT-LIB axiom blocks: {smt2_count}")

if __name__ == "__main__":
    main()