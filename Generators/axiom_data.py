"""
axiom_data.py
=============
Shared axiom content for the FOIS 2026 deontic grounding benchmark.
Imported by:
  - gen_foundation_problems.py  (problem generation)
  - gen_layer1_deontic.py       (GRND-AX-1.smt2 reference copy)
Contents:
  FOF_AXIOM_DICT      — named FOF axioms for per-problem selective inclusion
  SMT2_AXIOMS         — SMT-LIB axiom blocks (embedded in every .smt2 file)
  SMT2_APPENDIX_SORTS — Appendix A.0 sort/predicate declarations
  FOF_APPENDIX_DECLS  — Appendix A.0 comment block for .p files

CHANGELOG v1.5:
  - Renamed ax_perm_relator_basic  -> ax_perm_relator_weak
  - Renamed ax_proh_relator_basic  -> ax_proh_relator_conduct
  - Renamed ax_cross_relator_consistency -> ax_cross_relator
  - Renamed ax_conflict_detection  -> ax_conflict (role=lemma; derived from Ax5.9)
  - Added ax_unique_event, ax_unique_event_rem, ax_unique_event_imm
  - Added ax_odrl_rel_is_rel
  - SMT2: Action -> NormContent throughout (unified sort)
  - SMT2: correlativity fixed to exists-unique on both sides
  - SMT2: ax_unique_event_rem, ax_unique_event_imm added
  - SMT2_APPENDIX_SORTS: founds-rem/founds-imm removed (declared in Layer 0)
  - Bug fix: ax_conflict role corollary -> lemma (corollary invalid TPTP FOF role)
  - Bug fix: Z3 portability comment added to ax_cross_relator and ax_conflict SMT2
  - Bug fix: legal-relator declaration ordering note added to SMT2_APPENDIX_SORTS
"""

# ============================================================================
# FOF: individual axioms by name — subset included per problem
# ============================================================================

FOF_AXIOM_DICT = {
    # ------------------------------------------------------------------
    # Ax5.1  Permission Relator — Weak
    # ------------------------------------------------------------------
    "ax_perm_relator_weak": """\
fof(ax_perm_relator_weak, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & permission(L) & bearer(L,X) & cnt(L,A,T) & part_of(L,Rho)
          & no_right(N)   & bearer(N,Y) & cnt(N,A,T) & part_of(N,Rho) ) )).""",

    # ------------------------------------------------------------------
    # Ax5.2  Permission Relator — Strong
    # ------------------------------------------------------------------
    "ax_perm_relator_strong": """\
fof(ax_perm_relator_strong, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & strong(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T)
        & activates(E,P) )
     => ? [RhoI, Im, Db] :
          ( founds_imm(E,RhoI,P)
          & immunity(Im)   & bearer(Im,X) & cnt(Im,A,T) & part_of(Im,RhoI)
          & disability(Db) & bearer(Db,Y) & cnt(Db,A,T) & part_of(Db,RhoI) ) )).""",

    # ------------------------------------------------------------------
    # Ax5.3  Prohibition Relator — Conduct
    # ------------------------------------------------------------------
    "ax_proh_relator_conduct": """\
fof(ax_proh_relator_conduct, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & right(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).""",

    # ------------------------------------------------------------------
    # Ax5.4  Prohibition Relator — Remedy
    # ------------------------------------------------------------------
    "ax_proh_relator_remedy": """\
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) )
     => ? [RhoR, Pw, S] :
          ( founds_rem(E,RhoR,F)
          & power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,RhoR)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,RhoR) ) )).""",

    # ------------------------------------------------------------------
    # Ax5.5  Obligation Relator
    # ------------------------------------------------------------------
    "ax_obl_relator": """\
fof(ax_obl_relator, axiom,
    ! [D, X, Y, A, T, E] :
      ( ( obl(D) & aee(D,X) & aer(D,Y) & act(D,A) & tgt(D,T) & activates(E,D) )
     => ? [Rho, Du, C] :
          ( founds(E,Rho,D)
          & duty(Du) & bearer(Du,X) & cnt(Du,A,T) & part_of(Du,Rho)
          & right(C) & bearer(C,Y)  & cnt(C,A,T)  & part_of(C,Rho) ) )).""",

    # ------------------------------------------------------------------
    # Ax5.6  Unique Founding — all three predicates, both clauses
    # ------------------------------------------------------------------
    "ax_unique_founding": """\
fof(ax_unique_founding, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds(E,Rho1,R) & founds(E,Rho2,R) ) => Rho1 = Rho2 )).""",

    "ax_unique_event": """\
fof(ax_unique_event, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds(E1,Rho,R) & founds(E2,Rho,R) ) => E1 = E2 )).""",

    "ax_unique_founding_rem": """\
fof(ax_unique_founding_rem, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds_rem(E,Rho1,R) & founds_rem(E,Rho2,R) ) => Rho1 = Rho2 )).""",

    "ax_unique_event_rem": """\
fof(ax_unique_event_rem, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds_rem(E1,Rho,R) & founds_rem(E2,Rho,R) ) => E1 = E2 )).""",

    "ax_unique_founding_imm": """\
fof(ax_unique_founding_imm, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds_imm(E,Rho1,R) & founds_imm(E,Rho2,R) ) => Rho1 = Rho2 )).""",

    "ax_unique_event_imm": """\
fof(ax_unique_event_imm, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds_imm(E1,Rho,R) & founds_imm(E2,Rho,R) ) => E1 = E2 )).""",

    # ------------------------------------------------------------------
    # Ax5.7  ODRL Relator Typing
    # NOTE: base case consolidated as disjunction for brevity;
    # logically equivalent to three separate per-predicate axioms.
    # ------------------------------------------------------------------
    "ax_odrl_rel_typing": """\
fof(ax_odrl_rel_typing, axiom,
    ! [E, Rho, R] :
      ( ( founds(E,Rho,R) & ( perm(R) | proh(R) | obl(R) ) )
     => odrl_rel(Rho) )).""",

    "ax_odrl_rel_typing_rem": """\
fof(ax_odrl_rel_typing_rem, axiom,
    ! [E, Rho, R] :
      ( ( founds_rem(E,Rho,R) & proh(R) )
     => odrl_rel(Rho) )).""",

    "ax_odrl_rel_typing_imm": """\
fof(ax_odrl_rel_typing_imm, axiom,
    ! [E, Rho, R] :
      ( ( founds_imm(E,Rho,R) & perm(R) )
     => odrl_rel(Rho) )).""",

    # ------------------------------------------------------------------
    # Ax5.8  Correlativity — exists-unique on BOTH sides
    # ------------------------------------------------------------------
    "ax_correlativity_permission": """\
fof(ax_correlativity_permission, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [L] : ( permission(L) & part_of(L,Rho) & cnt(L,A,T)
                    & ! [L2] : ( ( permission(L2) & part_of(L2,Rho) & cnt(L2,A,T) )
                                => L2 = L ) ) )
        <=> ( ? [N] : ( no_right(N) & part_of(N,Rho) & cnt(N,A,T)
                      & ! [M] : ( ( no_right(M) & part_of(M,Rho) & cnt(M,A,T) )
                                 => M = N ) ) ) ) )).""",

    "ax_correlativity_duty": """\
fof(ax_correlativity_duty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [D] : ( duty(D) & part_of(D,Rho) & cnt(D,A,T)
                    & ! [D2] : ( ( duty(D2) & part_of(D2,Rho) & cnt(D2,A,T) )
                                => D2 = D ) ) )
        <=> ( ? [C] : ( right(C) & part_of(C,Rho) & cnt(C,A,T)
                      & ! [K] : ( ( right(K) & part_of(K,Rho) & cnt(K,A,T) )
                                 => K = C ) ) ) ) )).""",

    "ax_correlativity_power": """\
fof(ax_correlativity_power, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Pw] : ( power(Pw) & part_of(Pw,Rho) & cnt(Pw,A,T)
                      & ! [Pw2] : ( ( power(Pw2) & part_of(Pw2,Rho) & cnt(Pw2,A,T) )
                                   => Pw2 = Pw ) ) )
        <=> ( ? [S] : ( subjection(S) & part_of(S,Rho) & cnt(S,A,T)
                      & ! [S2] : ( ( subjection(S2) & part_of(S2,Rho) & cnt(S2,A,T) )
                                  => S2 = S ) ) ) ) )).""",

    "ax_correlativity_immunity": """\
fof(ax_correlativity_immunity, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Im] : ( immunity(Im) & part_of(Im,Rho) & cnt(Im,A,T)
                      & ! [Im2] : ( ( immunity(Im2) & part_of(Im2,Rho) & cnt(Im2,A,T) )
                                   => Im2 = Im ) ) )
        <=> ( ? [Db] : ( disability(Db) & part_of(Db,Rho) & cnt(Db,A,T)
                       & ! [Db2] : ( ( disability(Db2) & part_of(Db2,Rho) & cnt(Db2,A,T) )
                                    => Db2 = Db ) ) ) ) )).""",

    # ------------------------------------------------------------------
    # Ax5.9  Normative Position Incompatibility — cross-relator
    # Normative axiom independent of UFO type disjointness.
    # ------------------------------------------------------------------
    "ax_cross_relator": """\
fof(ax_cross_relator, axiom,
    ! [L, D, X, A, T] :
      ( ( permission(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)       & bearer(D,X) & cnt(D,rfr(A),T) )
     => $false )).""",

    # ------------------------------------------------------------------
    # Corollary  Permission-Duty Conflict Within a Relator
    # Derived from Ax5.9 (ax_cross_relator). Retained as a lemma for
    # prover convenience.
    # Role = lemma (TPTP valid; 'corollary' is not a valid FOF role).
    # ------------------------------------------------------------------
    "ax_conflict": """\
fof(ax_conflict, lemma,
    ! [Rho, L, D, X, A, T] :
      ( ( part_of(L,Rho) & part_of(D,Rho)
        & permission(L) & duty(D)
        & bearer(L,X) & bearer(D,X)
        & cnt(L,A,T)  & cnt(D,rfr(A),T) )
     => $false )).""",

    # ------------------------------------------------------------------
    # Ax5.10  Disability Precludes Prohibition Creation
    # ------------------------------------------------------------------
    "ax_disability_block": """\
fof(ax_disability_block, axiom,
    ! [F, X, Y, A, T] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) )
     => ~ ? [Db] : ( disability(Db) & bearer(Db,Y) & cnt(Db,A,T) ) )).""",

    # ------------------------------------------------------------------
    # Ax5.11  ODRL Relators Subsume Legal Relators
    # ------------------------------------------------------------------
    "ax_odrl_rel_is_rel": """\
fof(ax_odrl_rel_is_rel, axiom,
    ! [Rho] : ( odrl_rel(Rho) => legal_relator(Rho) )).""",

    # ------------------------------------------------------------------
    # A1-A3  Cross-level axioms
    # ------------------------------------------------------------------
    "ax_A1": """\
fof(ax_A1, axiom,
    ! [X, A, T, Q] :
      ( norm_state_change(X,A,T,Q)
     => ? [E] : ( inst_event(E) & triggers(E,X,A,T,Q) ) )).""",

    "ax_A2": """\
fof(ax_A2, axiom,
    ! [E] :
      ( inst_event(E)
     => ? [Y] : competent_for(Y,E) )).""",

    "ax_A3": """\
fof(ax_A3, axiom,
    ! [Y, E] :
      ( competent_for(Y,E)
     => ? [Pw, S, X] :
          ( power(Pw)     & bearer(Pw,Y) & about_event(Pw,E)
          & subjection(S) & bearer(S,X)  & about_event(S,E) ) )).""",

    # ------------------------------------------------------------------
    # B1-B3  Bridge axioms
    # ------------------------------------------------------------------
    "ax_B1": """\
fof(ax_B1, axiom,
    ! [F, X, A, T] :
      ( ( proh(F) & has_rem(F) & act(F,A) & tgt(F,T) & aee(F,X) & does(X,A,T) )
     => ? [B] : ( rem_act(F,B) & norm_state_change(X,B,T,duty_rem) ) )).""",

    "ax_B2": """\
fof(ax_B2, axiom,
    ! [Pw, A, T, Rho, E, R] :
      ( ( power(Pw) & cnt(Pw,decl(A),T) & part_of(Pw,Rho) & founds_rem(E,Rho,R) )
     => about_event(Pw,E) )).""",

    "ax_B3": """\
fof(ax_B3, axiom,
    ! [S, A, T, Rho, E, R] :
      ( ( subjection(S) & cnt(S,decl(A),T) & part_of(S,Rho) & founds_rem(E,Rho,R) )
     => about_event(S,E) )).""",
}


# ============================================================================
# SMT-LIB: axiom blocks — embedded in every .smt2 problem file
# founds is 3-ary: (founds Event Relator Rule) throughout.
# NormContent sort used throughout (unified; replaces separate Action sort).
# Embedding order in writers.py: preamble -> SMT2_APPENDIX_SORTS -> SMT2_AXIOMS.
# This ordering guarantees legal-relator (declared in APPENDIX_SORTS) is
# available before ax_odrl_rel_is_rel uses it, and NormPos is available
# before A1/B1 use it.
# Authoritative source: Axioms/Layer1-Deontic/GRND-AX-1.smt2
# ============================================================================

SMT2_AXIOMS = [
    # Ax5.1
    ("ax_perm_relator_weak",
     """\
(assert (forall ((p Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (perm p) (aee p x) (aer p y) (act p a) (tgt p t) (activates e p))
      (exists ((rho Relator) (l Position) (n Position))
        (and (founds e rho p)
             (permission l) (bearer l x) (cnt l a t) (part-of l rho)
             (no-right n)   (bearer n y) (cnt n a t) (part-of n rho))))))"""),

    # Ax5.2
    ("ax_perm_relator_strong",
     """\
(assert (forall ((p Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (perm p) (strong p) (aee p x) (aer p y) (act p a) (tgt p t)
           (activates e p))
      (exists ((rho-i Relator) (im Position) (db Position))
        (and (founds-imm e rho-i p)
             (immunity im)   (bearer im x) (cnt im a t) (part-of im rho-i)
             (disability db) (bearer db y) (cnt db a t) (part-of db rho-i))))))"""),

    # Ax5.3
    ("ax_proh_relator_conduct",
     """\
(assert (forall ((f Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t) (activates e f))
      (exists ((rho Relator) (d Position) (c Position))
        (and (founds e rho f)
             (duty d)  (bearer d x) (cnt d (rfr a) t) (part-of d rho)
             (right c) (bearer c y) (cnt c (rfr a) t) (part-of c rho))))))"""),

    # Ax5.4
    ("ax_proh_relator_remedy",
     """\
(assert (forall ((f Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (proh f) (has-rem f) (aee f x) (aer f y) (act f a) (tgt f t)
           (activates e f))
      (exists ((rho-r Relator) (pw Position) (s Position))
        (and (founds-rem e rho-r f)
             (power pw)     (bearer pw y) (cnt pw (decl a) t) (part-of pw rho-r)
             (subjection s) (bearer s x)  (cnt s  (decl a) t) (part-of s rho-r))))))"""),

    # Ax5.5
    ("ax_obl_relator",
     """\
(assert (forall ((d Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (obl d) (aee d x) (aer d y) (act d a) (tgt d t) (activates e d))
      (exists ((rho Relator) (du Position) (c Position))
        (and (founds e rho d)
             (duty du) (bearer du x) (cnt du a t) (part-of du rho)
             (right c) (bearer c y)  (cnt c  a t) (part-of c rho))))))"""),

    # Ax5.6a
    ("ax_unique_founding",
     """\
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds e rho1 r) (founds e rho2 r)) (= rho1 rho2))))"""),

    # Ax5.6b
    ("ax_unique_event",
     """\
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds e1 rho r) (founds e2 rho r)) (= e1 e2))))"""),

    # Ax5.6c
    ("ax_unique_founding_rem",
     """\
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds-rem e rho1 r) (founds-rem e rho2 r))
      (= rho1 rho2))))"""),

    # Ax5.6d
    ("ax_unique_event_rem",
     """\
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds-rem e1 rho r) (founds-rem e2 rho r)) (= e1 e2))))"""),

    # Ax5.6e
    ("ax_unique_founding_imm",
     """\
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds-imm e rho1 r) (founds-imm e rho2 r))
      (= rho1 rho2))))"""),

    # Ax5.6f
    ("ax_unique_event_imm",
     """\
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds-imm e1 rho r) (founds-imm e2 rho r)) (= e1 e2))))"""),

    # Ax5.7
    ("ax_odrl_rel_typing",
     """\
(assert (forall ((e Event) (rho Relator) (r Rule))
  (=> (and (founds e rho r) (or (perm r) (proh r) (obl r)))
      (odrl-rel rho))))"""),

    ("ax_odrl_rel_typing_rem",
     """\
(assert (forall ((e Event) (rho Relator) (r Rule))
  (=> (and (founds-rem e rho r) (proh r))
      (odrl-rel rho))))"""),

    ("ax_odrl_rel_typing_imm",
     """\
(assert (forall ((e Event) (rho Relator) (r Rule))
  (=> (and (founds-imm e rho r) (perm r))
      (odrl-rel rho))))"""),

    # Ax5.8  Correlativity — exists-unique on BOTH sides
    ("ax_correlativity_permission",
     """\
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((l Position))
           (and (permission l) (part-of l rho) (cnt l a t)
                (forall ((l2 Position))
                  (=> (and (permission l2) (part-of l2 rho) (cnt l2 a t))
                      (= l2 l)))))
         (exists ((n Position))
           (and (no-right n) (part-of n rho) (cnt n a t)
                (forall ((m Position))
                  (=> (and (no-right m) (part-of m rho) (cnt m a t))
                      (= m n)))))))))"""),

    ("ax_correlativity_duty",
     """\
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((d Position))
           (and (duty d) (part-of d rho) (cnt d a t)
                (forall ((d2 Position))
                  (=> (and (duty d2) (part-of d2 rho) (cnt d2 a t))
                      (= d2 d)))))
         (exists ((c Position))
           (and (right c) (part-of c rho) (cnt c a t)
                (forall ((k Position))
                  (=> (and (right k) (part-of k rho) (cnt k a t))
                      (= k c)))))))))"""),

    ("ax_correlativity_power",
     """\
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((pw Position))
           (and (power pw) (part-of pw rho) (cnt pw a t)
                (forall ((pw2 Position))
                  (=> (and (power pw2) (part-of pw2 rho) (cnt pw2 a t))
                      (= pw2 pw)))))
         (exists ((s Position))
           (and (subjection s) (part-of s rho) (cnt s a t)
                (forall ((s2 Position))
                  (=> (and (subjection s2) (part-of s2 rho) (cnt s2 a t))
                      (= s2 s)))))))))"""),

    ("ax_correlativity_immunity",
     """\
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((im Position))
           (and (immunity im) (part-of im rho) (cnt im a t)
                (forall ((im2 Position))
                  (=> (and (immunity im2) (part-of im2 rho) (cnt im2 a t))
                      (= im2 im)))))
         (exists ((db Position))
           (and (disability db) (part-of db rho) (cnt db a t)
                (forall ((db2 Position))
                  (=> (and (disability db2) (part-of db2 rho) (cnt db2 a t))
                      (= db2 db)))))))))"""),

    # Ax5.9  Cross-relator (normative, independent of UFO type disjointness)
    # Z3 accepts `false` as Bool term in (=> P false); equivalent to (not P).
    # Standard SMT-LIB 2 alternative: (not (and ...)) — both are valid in Z3.
    ("ax_cross_relator",
     """\
; Z3 accepts `false` as Bool term in (=> P false); equivalent to (not P)
(assert (forall ((l Position) (d Position) (x Agent) (a NormContent) (t Target))
  (=> (and (permission l) (bearer l x) (cnt l a t)
           (duty d)       (bearer d x) (cnt d (rfr a) t))
      false)))"""),

    # Corollary: Within-relator conflict (derived from ax_cross_relator).
    # Role = lemma in FOF ('corollary' is not a valid TPTP FOF formula role).
    # Z3 accepts `false` as Bool term in (=> P false); equivalent to (not P).
    ("ax_conflict",
     """\
; Z3 accepts `false` as Bool term in (=> P false); equivalent to (not P)
(assert (forall ((rho Relator) (l Position) (d Position)
                 (x Agent) (a NormContent) (t Target))
  (=> (and (part-of l rho) (part-of d rho)
           (permission l) (duty d)
           (bearer l x) (bearer d x)
           (cnt l a t) (cnt d (rfr a) t))
      false)))"""),

    # Ax5.10
    ("ax_disability_block",
     """\
(assert (forall ((f Rule) (x Agent) (y Agent) (a NormContent) (t Target))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t))
      (not (exists ((db Position))
             (and (disability db) (bearer db y) (cnt db a t)))))))"""),

    # Ax5.11
    # Requires legal-relator declared in SMT2_APPENDIX_SORTS.
    # writers.py embeds: preamble -> SMT2_APPENDIX_SORTS -> SMT2_AXIOMS,
    # so legal-relator is always in scope here.
    ("ax_odrl_rel_is_rel",
     """\
(assert (forall ((rho Relator))
  (=> (odrl-rel rho) (legal-relator rho))))"""),

    # A1
    ("ax_A1",
     """\
(assert (forall ((x Agent) (a NormContent) (t Target) (q NormPos))
  (=> (norm-state-change x a t q)
      (exists ((e Event))
        (and (inst-event e) (triggers e x a t q))))))"""),

    # A2
    ("ax_A2",
     """\
(assert (forall ((e Event))
  (=> (inst-event e)
      (exists ((y Agent)) (competent-for y e)))))"""),

    # A3
    ("ax_A3",
     """\
(assert (forall ((y Agent) (e Event))
  (=> (competent-for y e)
      (exists ((pw Position) (s Position) (x Agent))
        (and (power pw)     (bearer pw y) (about-event pw e)
             (subjection s) (bearer s x)  (about-event s e))))))"""),

    # B1
    ("ax_B1",
     """\
(assert (forall ((f Rule) (x Agent) (a NormContent) (t Target))
  (=> (and (proh f) (has-rem f) (act f a) (tgt f t) (aee f x) (does x a t))
      (exists ((b NormContent))
        (and (rem-act f b) (norm-state-change x b t duty-rem))))))"""),

    # B2
    ("ax_B2",
     """\
(assert (forall ((pw Position) (a NormContent) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (power pw) (cnt pw (decl a) t) (part-of pw rho) (founds-rem e rho r))
      (about-event pw e))))"""),

    # B3
    ("ax_B3",
     """\
(assert (forall ((s Position) (a NormContent) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (subjection s) (cnt s (decl a) t) (part-of s rho) (founds-rem e rho r))
      (about-event s e))))"""),
]


# ============================================================================
# SMT-LIB: Appendix A.0 sort/predicate declarations
# Embedded BEFORE SMT2_AXIOMS by writers.py, guaranteeing:
#   - legal-relator is declared before ax_odrl_rel_is_rel uses it
#   - NormPos is declared before A1/B1 use it
# NOTE: founds-rem and founds-imm are declared in the Layer 0 preamble
# (gen_layer0_signature.py) — NOT repeated here to avoid duplicate declarations.
# ============================================================================

SMT2_APPENDIX_SORTS = """\
; Appendix A.0 additional sorts and predicates
; Embedded before SMT2_AXIOMS — legal-relator and NormPos must be declared
; before ax_odrl_rel_is_rel and A1/B1 respectively.
; Note: odrl-rel, strong, founds-rem, founds-imm are declared in the
; Layer 0 preamble — not repeated here.
(declare-sort NormPos 0)
(declare-fun legal-relator      (Relator) Bool)
(declare-fun norm-state-change  (Agent NormContent Target NormPos) Bool)
(declare-fun inst-event         (Event) Bool)
(declare-fun triggers           (Event Agent NormContent Target NormPos) Bool)
(declare-fun competent-for      (Agent Event) Bool)
(declare-fun about-event        (Position Event) Bool)
(declare-fun does               (Agent NormContent Target) Bool)
(declare-fun rem-act            (Rule NormContent) Bool)
(declare-const duty-rem         NormPos)
"""


# ============================================================================
# FOF: Appendix A.0 comment block for .p files
# ============================================================================

FOF_APPENDIX_DECLS = """\
%--------------------------------------------------------------------------
% Appendix A.0 extra predicates (declared via axiom context in Layer1)
%   norm_state_change(X,A,T,Q)  -- position Q changes for X over (A,T)
%   inst_event(E)               -- E is an institutional event
%   triggers(E,X,A,T,Q)         -- E triggers the change of Q
%   competent_for(Y,E)          -- Y is competent to perform E
%   about_event(Pos,E)          -- position Pos concerns event E
%   does(X,A,T)                 -- X performs A on T
%   rem_act(F,B)                -- B is the action of the remedy attached to F
%   founds_rem(E,Rho,F)         -- E founds the competence relator rho_R for
%                                  prohibition F with remedy; distinct from
%                                  founds/3 so rho_F != rho_R.
%                                  B2/B3 use founds_rem because Power and
%                                  Subjection live in rho_R, not rho_F.
%   founds_imm(E,Rho,P)         -- E founds the competence relator rho_I for
%                                  strongly-permitted rule P; distinct from
%                                  founds/3 so rho_P != rho_I
%   duty_rem                    -- constant: token for remedy-duty position
%   odrl_rel(Rho)               -- Rho is a relator founded by an ODRL rule
%   legal_relator(Rho)          -- Rho is a UFO legal relator (subsumes odrl_rel)
%--------------------------------------------------------------------------
"""