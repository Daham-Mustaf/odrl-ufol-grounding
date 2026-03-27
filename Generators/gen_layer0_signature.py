"""
gen_layer0_signature.py
================
Generates TWO signature files for the FOIS 2026 deontic grounding:
  Problems/DeonticOntology/Axioms/Layer0-Signature/GRND000-0.ax     — FOF/TPTP  (Vampire)
  Problems/DeonticOntology/Axioms/Layer0-Signature/GRND000-0.smt2   — SMT-LIB   (Z3)
FOF file:
  Used via include() at the top of every .p problem file.
SMT-LIB file:
  SMT-LIB has NO include directive.
  This file is a PREAMBLE TEMPLATE embedded verbatim by every
  problem generator into each .smt2 problem file.
  Import via:
      from gen_layer0_signature import generate_smt2 as _gen_smt2
      SMT2_PREAMBLE = _gen_smt2()
Usage:
    uv run Generators/DeonticOntology/gen_layer0_signature.py \
      --out-dir Problems/DeonticOntology/Axioms/Layer0-Signature
"""
import argparse
import textwrap
from pathlib import Path
from datetime import date

META = {
    "domain":  "Deontic Ontology / ODRL Grounding",
    "source":  "Mohammed et al., What Does ODRL Mean? FOIS 2026",
    "version": "1.5",
}

# ============================================================================
# FOF
# ============================================================================

def fof_header() -> str:
    return textwrap.dedent(f"""\
        %--------------------------------------------------------------------------
        % File     : GRND000-0.ax
        % Domain   : {META['domain']}
        % Problem  : Signature — sorts, predicates, rfr/decl functions
        % Version  : {META['version']}
        % English  : FOF signature. Include in ALL DeonticOntology .p files via:
        %              include('Axioms/Layer0-Signature/GRND000-0.ax').
        %
        % Source   : {META['source']}
        % Generated: {date.today().isoformat()} by gen_layer0_signature.py
        %
        % Sorts (unary guard predicates — FOF has no native sorts):
        %   agent, action, target, rule, position, legal_relator, event,
        %   forbearance
        %
        % Functions:
        %   rfr/1   : Act -> Forbearance   (refrain from action)
        %   pos/1   : Forbearance -> Act   (left-inverse of rfr)
        %   decl/1  : Act -> Act           (declare-violation institutional act)
        %   issue/1 : Rule -> Act          (issue-policy institutional act)
        %                                  [FIX Bug6: was Policy -> Act]
        %
        % CHANGELOG v1.5:
        %   - Issue 2: liberty -> permission, claim -> right throughout
        %     (UFO-L terms; consistent with paper and axiom_data.py)
        %   - Issue 3: founds_rem and founds_imm added to relator predicates
        % CHANGELOG v1.4:
        %   - version aligned with gen_foundation_problems.py v1.4
        % CHANGELOG v1.1:
        %   - founds/2 -> founds/3 (event, relator, rule)
        %   - Added odrl_rel/1, strong/1, issue/1
        %--------------------------------------------------------------------------
    """)

FOF_SORT_GUARDS = """\
%--------------------------------------------------------------------------
% SORT GUARDS
% FOF has no native sorts. We use unary predicates as type guards.
% Guards are NOT asserted here — problem files assert them for constants.
%
%   agent(X)         — X is an agent (assigner or assignee)
%   action(X)        — X is an action in Act
%   target(X)        — X is a target asset
%   rule(X)          — X is an ODRL rule (perm / proh / duty)
%   position(X)      — X is a UFO-L legal position (moment)
%   legal_relator(X) — X is a UFO legal relator
%   odrl_rel(X)      — X is a relator founded by an ODRL rule activation
%   event(X)         — X is an activation event
%   forbearance(X)   — X is a forbearance in rfr(Act)
%--------------------------------------------------------------------------
"""

FOF_RULE_PREDICATES = """\
%--------------------------------------------------------------------------
% ODRL RULE TYPE PREDICATES
%   perm(R)    — R is an odrl:Permission
%   proh(R)    — R is an odrl:Prohibition
%   obl(R)     — R is an odrl:Duty  [CANONICAL NAME]
%   has_rem(R) — R is a prohibition carrying odrl:remedy  [CANONICAL NAME]
%   strong(R)  — R is a strongly-permitted permission (profile extension)
%
% ODRL STRUCTURAL ROLE PREDICATES
%   aee(R, X)  — assignee of R is X
%   aer(R, Y)  — assigner of R is Y
%   act(R, A)  — action  of R is A
%   tgt(R, T)  — target  of R is T
%
% ACTIVATION PREDICATE
%   activates(E, R) — event E activates rule R
%--------------------------------------------------------------------------
"""

FOF_RELATOR_PREDICATES = """\
%--------------------------------------------------------------------------
% UFO RELATOR AND POSITION PREDICATES
%
%   founds(E, Rho, R)     — event E founds relator Rho for rule R  (3-ary)
%                           Used for conduct relators (Ax5.1, Ax5.3, Ax5.6).
%   founds_rem(E, Rho, R) — event E founds competence relator rho_R for
%                           prohibition R with remedy; distinct from founds
%                           so rho_F != rho_R (paper Ax5.4).
%   founds_imm(E, Rho, R) — event E founds competence relator rho_I for
%                           strongly-permitted rule R; distinct from founds
%                           so rho_P != rho_I (paper Ax5.2).
%
%   part_of(Pos, Rho) — Pos is part of Rho
%   bearer(Pos, X)    — Pos inheres in agent X
%   cnt(Pos, A, T)    — Pos has normative content A on target T [CANONICAL]
%                       A in Act union Forbearance; distinguished by
%                       action(A) / forbearance(A) guards.
%
%--------------------------------------------------------------------------
"""

FOF_RFR = """\
%--------------------------------------------------------------------------
% RFR FUNCTION  rfr : Act -> Forbearance
% rfr(A) = forbearance of performing A (duty to refrain).
% pos : Forbearance -> Act  (left-inverse of rfr)
%--------------------------------------------------------------------------
fof(rfr_distinct, axiom,
    ! [A] : ( action(A) => rfr(A) != A )).
fof(rfr_injective, axiom,
    ! [A, B] : ( ( action(A) & action(B) & rfr(A) = rfr(B) ) => A = B )).
fof(rfr_left_inverse, axiom,
    ! [A] : ( action(A) => pos(rfr(A)) = A )).
fof(rfr_range_forbearance, axiom,
    ! [A] : ( action(A) => forbearance(rfr(A)) )).
fof(forbearance_not_action, axiom,
    ! [F] : ( forbearance(F) => ~ action(F) )).
"""

FOF_DECL = """\
%--------------------------------------------------------------------------
% DECL FUNCTION  decl : Act -> Act
% decl(A) = institutional act of declaring a violation on action A.
%--------------------------------------------------------------------------
fof(decl_range_action, axiom,
    ! [A] : ( action(A) => action(decl(A)) )).
fof(decl_injective, axiom,
    ! [A, B] : ( ( action(A) & action(B) & decl(A) = decl(B) ) => A = B )).
fof(decl_distinct, axiom,
    ! [A] : ( action(A) => decl(A) != A )).
"""

FOF_ISSUE = """\
%--------------------------------------------------------------------------
% ISSUE FUNCTION  issue : Rule -> Act
% issue(Pi) = institutional act of issuing policy Pi.
%
% NOTE: issue/1 is NOT used in GRND001-024 (FOIS paper problems).
% Present for PAAR 2026 benchmark only.
%--------------------------------------------------------------------------
fof(issue_range_action, axiom,
    ! [R] : ( rule(R) => action(issue(R)) )).
fof(issue_injective, axiom,
    ! [A, B] : ( ( rule(A) & rule(B) & issue(A) = issue(B) ) => A = B )).
"""

FOF_NORMCONTENT = """\
%--------------------------------------------------------------------------
% NORMCONTENT TYPE DISTINCTION
% A position cannot bear both action and forbearance content over the same
% target. This encodes Ax5.9 (Normative Position Incompatibility) at the
% cnt level: a position bears content of exactly one type over a given
% target, following UFO moment typing and paper Ax5.9.
%--------------------------------------------------------------------------
fof(cnt_content_unique_type, axiom,
    ! [Pos, A, T] : ( action(A) =>
      ~ ( cnt(Pos, A, T) & cnt(Pos, rfr(A), T) ))).
"""

FOF_POSITION_DISJOINTNESS = """\
%--------------------------------------------------------------------------
% POSITION SORT DISJOINTNESS — all 8 UFO-L types mutually disjoint
% UFO-L terms: permission (not liberty), right (not claim).
%--------------------------------------------------------------------------
% Within conduct level
fof(permission_not_duty,     axiom, ! [P] : ~ ( permission(P) & duty(P)     )).
fof(permission_not_right,    axiom, ! [P] : ~ ( permission(P) & right(P)    )).
fof(permission_not_no_right, axiom, ! [P] : ~ ( permission(P) & no_right(P) )).
fof(duty_not_right,          axiom, ! [P] : ~ ( duty(P)       & right(P)    )).
fof(duty_not_no_right,       axiom, ! [P] : ~ ( duty(P)       & no_right(P) )).
fof(right_not_no_right,      axiom, ! [P] : ~ ( right(P)      & no_right(P) )).
% Within competence level
fof(power_not_subjection,      axiom, ! [P] : ~ ( power(P)      & subjection(P) )).
fof(power_not_immunity,        axiom, ! [P] : ~ ( power(P)      & immunity(P)   )).
fof(power_not_disability,      axiom, ! [P] : ~ ( power(P)      & disability(P) )).
fof(subjection_not_immunity,   axiom, ! [P] : ~ ( subjection(P) & immunity(P)   )).
fof(subjection_not_disability, axiom, ! [P] : ~ ( subjection(P) & disability(P) )).
fof(immunity_not_disability,   axiom, ! [P] : ~ ( immunity(P)   & disability(P) )).
% Conduct vs competence (16 pairs)
fof(cn_1,  axiom, ! [P] : ~ ( permission(P) & power(P)      )).
fof(cn_2,  axiom, ! [P] : ~ ( permission(P) & subjection(P) )).
fof(cn_3,  axiom, ! [P] : ~ ( permission(P) & immunity(P)   )).
fof(cn_4,  axiom, ! [P] : ~ ( permission(P) & disability(P) )).
fof(cn_5,  axiom, ! [P] : ~ ( duty(P)       & power(P)      )).
fof(cn_6,  axiom, ! [P] : ~ ( duty(P)       & subjection(P) )).
fof(cn_7,  axiom, ! [P] : ~ ( duty(P)       & immunity(P)   )).
fof(cn_8,  axiom, ! [P] : ~ ( duty(P)       & disability(P) )).
fof(cn_9,  axiom, ! [P] : ~ ( right(P)      & power(P)      )).
fof(cn_10, axiom, ! [P] : ~ ( right(P)      & subjection(P) )).
fof(cn_11, axiom, ! [P] : ~ ( right(P)      & immunity(P)   )).
fof(cn_12, axiom, ! [P] : ~ ( right(P)      & disability(P) )).
fof(cn_13, axiom, ! [P] : ~ ( no_right(P)   & power(P)      )).
fof(cn_14, axiom, ! [P] : ~ ( no_right(P)   & subjection(P) )).
fof(cn_15, axiom, ! [P] : ~ ( no_right(P)   & immunity(P)   )).
fof(cn_16, axiom, ! [P] : ~ ( no_right(P)   & disability(P) )).
% End of GRND000-0.ax
"""

def generate_fof() -> str:
    return "\n".join([
        fof_header(),
        FOF_SORT_GUARDS,
        FOF_RULE_PREDICATES,
        FOF_RELATOR_PREDICATES,
        FOF_RFR,
        FOF_DECL,
        FOF_ISSUE,
        FOF_NORMCONTENT,
        FOF_POSITION_DISJOINTNESS,
    ])

# ============================================================================
# SMT-LIB
# ============================================================================

def smt2_header() -> str:
    return textwrap.dedent(f"""\
        ; --------------------------------------------------------------------------
        ; File     : GRND000-0.smt2
        ; Domain   : {META['domain']}
        ; Problem  : Signature preamble — sorts, functions, rfr/decl axioms
        ; Version  : {META['version']}
        ; English  : SMT-LIB preamble embedded verbatim into every .smt2 file.
        ;            Do NOT add (check-sat) here.
        ;            Import via:
        ;              from gen_layer0_signature import generate_smt2 as _gen_smt2
        ;              SMT2_PREAMBLE = _gen_smt2()
        ;
        ; Source   : {META['source']}
        ; Generated: {date.today().isoformat()} by gen_layer0_signature.py
        ;
        ; Key design decisions:
        ;   NormContent (Issue 1): replaces separate Action + Forbearance sorts.
        ;     rfr : NormContent -> NormContent. cnt : (Position NormContent Target).
        ;     cnt-f removed. rfr_distinctness (rfr(a)!=a) carries the
        ;     act/forbearance distinction instead of separate sort disjointness.
        ;   permission/right (Issue 2): UFO-L terms replace liberty/claim.
        ;   founds-rem, founds-imm (Issue 3): declared here alongside founds.
        ;
        ; CHANGELOG v1.5:
        ;   - Issue 1: NormContent sort; cnt unified; cnt-f removed.
        ;   - Issue 2: liberty->permission, claim->right.
        ;   - Issue 3: founds-rem and founds-imm in SMT2_RELATOR_PREDICATES.
        ; --------------------------------------------------------------------------
        (set-logic UF)
        (set-info :source |{META['source']}|)
        (set-info :status unknown)
    """)

SMT2_SORTS = """\
; --------------------------------------------------------------------------
; SORTS
; NormContent is a unified sort for Act and Forbearance content.
; rfr maps within NormContent; rfr_distinctness (rfr(a)!=a) replaces
; the former sort-level disjointness that held when Action and
; Forbearance were separate sorts.
; --------------------------------------------------------------------------
(declare-sort Agent       0)
(declare-sort NormContent 0)
(declare-sort Target      0)
(declare-sort Rule        0)
(declare-sort Position    0)
(declare-sort Relator     0)
(declare-sort Event       0)
"""

SMT2_RULE_PREDICATES = """\
; --------------------------------------------------------------------------
; ODRL RULE TYPE PREDICATES
; --------------------------------------------------------------------------
(declare-fun perm    (Rule) Bool)
(declare-fun proh    (Rule) Bool)
(declare-fun obl     (Rule) Bool)
(declare-fun has-rem (Rule) Bool)
(declare-fun strong  (Rule) Bool)
(declare-fun aee (Rule Agent)       Bool)
(declare-fun aer (Rule Agent)       Bool)
(declare-fun act (Rule NormContent) Bool)
(declare-fun tgt (Rule Target)      Bool)
(declare-fun activates (Event Rule) Bool)
"""

SMT2_RELATOR_PREDICATES = """\
; --------------------------------------------------------------------------
; UFO RELATOR AND POSITION PREDICATES
;
; Three founding predicates for three kinds of simple legal relator:
;   founds     — conduct relator (Duty-Right or Permission-NoRight)
;   founds-rem — competence relator rho_R for prohibition+remedy (Ax5.4)
;   founds-imm — competence relator rho_I for strong permission (Ax5.2)
; Unique Founding applies independently within each predicate.
;
; cnt: single predicate (Position NormContent Target).
;   rfr(a) and a are distinct NormContent values (rfr_distinctness).
;   cnt-f is removed entirely.
;
; UFO-L position terms (Issue 2): permission/right replace liberty/claim.
; --------------------------------------------------------------------------
(declare-fun founds     (Event Relator Rule) Bool)
(declare-fun founds-rem (Event Relator Rule) Bool)
(declare-fun founds-imm (Event Relator Rule) Bool)
(declare-fun part-of    (Position Relator)   Bool)
(declare-fun bearer     (Position Agent)     Bool)
(declare-fun cnt        (Position NormContent Target) Bool)
(declare-fun odrl-rel   (Relator) Bool)
; UFO-L position type predicates
(declare-fun permission (Position) Bool)
(declare-fun no-right   (Position) Bool)
(declare-fun duty       (Position) Bool)
(declare-fun right      (Position) Bool)
(declare-fun power      (Position) Bool)
(declare-fun subjection (Position) Bool)
(declare-fun immunity   (Position) Bool)
(declare-fun disability (Position) Bool)
"""

SMT2_RFR = """\
; --------------------------------------------------------------------------
; RFR FUNCTION  rfr : NormContent -> NormContent
; pos = left-inverse of rfr.
; rfr_distinctness replaces the sort-level guarantee that formerly held
; when Action and Forbearance were distinct sorts.
; NOTE: pos(rfr(x))=x is asserted universally over all NormContent —
; this is conservative (stronger than the FOF action-guarded version)
; but never unsound: it cannot produce false unsat.
; --------------------------------------------------------------------------
(declare-fun rfr (NormContent) NormContent)
(declare-fun pos (NormContent) NormContent)
; Injectivity
(assert (forall ((a NormContent) (b NormContent))
  (=> (= (rfr a) (rfr b)) (= a b))))
; Left-inverse (universal; conservative over FOF action-guarded version)
(assert (forall ((a NormContent))
  (= (pos (rfr a)) a)))
; Distinctness: rfr(a) != a
(assert (forall ((a NormContent))
  (not (= (rfr a) a))))
"""

SMT2_DECL = """\
; --------------------------------------------------------------------------
; DECL FUNCTION  decl : NormContent -> NormContent
; decl(a) = institutional act of declaring a violation on action a.
; --------------------------------------------------------------------------
(declare-fun decl (NormContent) NormContent)
; Injectivity
(assert (forall ((a NormContent) (b NormContent))
  (=> (= (decl a) (decl b)) (= a b))))
; Distinctness from base content
(assert (forall ((a NormContent))
  (not (= (decl a) a))))
; decl(a) != rfr(a): no sort separation in unified NormContent;
; in FOF this is guaranteed by decl_range_action + rfr_range_forbearance
; + forbearance_not_action; here it must be explicit.
(assert (forall ((a NormContent))
  (not (= (decl a) (rfr a)))))
"""

SMT2_ISSUE = """\
; --------------------------------------------------------------------------
; ISSUE FUNCTION  issue : Rule -> NormContent
;
; NOTE: issue/1 is NOT used in GRND001-024 (FOIS paper problems).
; Present for PAAR 2026 benchmark only.
; --------------------------------------------------------------------------
(declare-fun issue (Rule) NormContent)
; Injectivity
(assert (forall ((a Rule) (b Rule))
  (=> (= (issue a) (issue b)) (= a b))))
"""

SMT2_NORMCONTENT = """\
; --------------------------------------------------------------------------
; NORMCONTENT TYPE DISTINCTION
; A position cannot bear both action-content and forbearance-content
; (i.e., a and rfr(a)) over the same target.
; Mirrors FOF cnt_content_unique_type; encodes Ax5.9 at the cnt level.
; A position bears content of exactly one type over a given target,
; following UFO moment typing and paper Ax5.9.
; --------------------------------------------------------------------------
(assert (forall ((p Position) (a NormContent) (t Target))
  (not (and (cnt p a t) (cnt p (rfr a) t)))))
"""

SMT2_POSITION_DISJOINTNESS = """\
; --------------------------------------------------------------------------
; POSITION SORT DISJOINTNESS (UFO-L terms)
; --------------------------------------------------------------------------
; Within conduct level
(assert (forall ((p Position)) (not (and (permission p) (duty p)))))
(assert (forall ((p Position)) (not (and (permission p) (right p)))))
(assert (forall ((p Position)) (not (and (permission p) (no-right p)))))
(assert (forall ((p Position)) (not (and (duty p)       (right p)))))
(assert (forall ((p Position)) (not (and (duty p)       (no-right p)))))
(assert (forall ((p Position)) (not (and (right p)      (no-right p)))))
; Within competence level
(assert (forall ((p Position)) (not (and (power p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (power p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (power p)      (disability p)))))
(assert (forall ((p Position)) (not (and (subjection p) (immunity p)))))
(assert (forall ((p Position)) (not (and (subjection p) (disability p)))))
(assert (forall ((p Position)) (not (and (immunity p)   (disability p)))))
; Conduct vs competence (16 pairs)
(assert (forall ((p Position)) (not (and (permission p) (power p)))))
(assert (forall ((p Position)) (not (and (permission p) (subjection p)))))
(assert (forall ((p Position)) (not (and (permission p) (immunity p)))))
(assert (forall ((p Position)) (not (and (permission p) (disability p)))))
(assert (forall ((p Position)) (not (and (duty p)       (power p)))))
(assert (forall ((p Position)) (not (and (duty p)       (subjection p)))))
(assert (forall ((p Position)) (not (and (duty p)       (immunity p)))))
(assert (forall ((p Position)) (not (and (duty p)       (disability p)))))
(assert (forall ((p Position)) (not (and (right p)      (power p)))))
(assert (forall ((p Position)) (not (and (right p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (right p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (right p)      (disability p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (power p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (subjection p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (immunity p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (disability p)))))
; --------------------------------------------------------------------------
; END OF PREAMBLE — problem files append axioms + conjecture after this
; --------------------------------------------------------------------------
"""

def generate_smt2() -> str:
    return "\n".join([
        smt2_header(),
        SMT2_SORTS,
        SMT2_RULE_PREDICATES,
        SMT2_RELATOR_PREDICATES,
        SMT2_RFR,
        SMT2_DECL,
        SMT2_ISSUE,
        SMT2_NORMCONTENT,
        SMT2_POSITION_DISJOINTNESS,
    ])

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate GRND000-0.ax (FOF) and GRND000-0.smt2 (SMT-LIB) signatures."
    )
    parser.add_argument(
        "--out-dir",
        default="Problems/DeonticOntology/Axioms/Layer0-Signature",
    )
    parser.add_argument("--stdout-fof",  action="store_true")
    parser.add_argument("--stdout-smt2", action="store_true")
    args = parser.parse_args()

    fof_content  = generate_fof()
    smt2_content = generate_smt2()

    if args.stdout_fof:
        print(fof_content)
        return
    if args.stdout_smt2:
        print(smt2_content)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    fof_path  = out_dir / "GRND000-0.ax"
    smt2_path = out_dir / "GRND000-0.smt2"

    fof_path.write_text(fof_content,  encoding="utf-8")
    smt2_path.write_text(smt2_content, encoding="utf-8")

    fof_axioms  = fof_content.count("fof(")
    smt2_assert = smt2_content.count("(assert")
    smt2_decl   = smt2_content.count("(declare-")

    print(f"Written: {fof_path}")
    print(f"  Lines: {fof_content.count(chr(10))}  FOF axioms: {fof_axioms}")
    print(f"Written: {smt2_path}")
    print(f"  Lines: {smt2_content.count(chr(10))}  (assert): {smt2_assert}  (declare-): {smt2_decl}")

if __name__ == "__main__":
    main()