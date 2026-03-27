; --------------------------------------------------------------------------
; File     : GRND000-0.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Problem  : Signature preamble — sorts, functions, rfr/decl axioms
; Version  : 1.5
; English  : SMT-LIB preamble embedded verbatim into every .smt2 file.
;            Do NOT add (check-sat) here.
;            Import via:
;              from gen_layer0_signature import generate_smt2 as _gen_smt2
;              SMT2_PREAMBLE = _gen_smt2()
;
; Source   : Mohammed et al., What Does ODRL Mean? FOIS 2026
; Generated: 2026-03-25 by gen_layer0_signature.py
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
(set-info :source |Mohammed et al., What Does ODRL Mean? FOIS 2026|)
(set-info :status unknown)

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
