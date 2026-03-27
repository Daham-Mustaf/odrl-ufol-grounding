(* ============================================================
   ODRLDeonticOntology.thy  --  Stage 1
   FOIS 2026 -- "What Does ODRL Mean?"
   run isabelle build -D /Users/dahammhamad/Desktop/tptp-odrl/Isabelle/ -v
   ============================================================ *)
(* ============================================================
   ODRLDeonticOntology.thy
   FOIS 2026 -- "What Does ODRL Mean?"
   All axioms Ax5.1–5.11, A1–A3, B1–B3, lemmas F1–F3,
   and named theorems/lemmas.
   run: isabelle build -D /Users/dahammhamad/Desktop/tptp-odrl/Isabelle/ -v
   ============================================================ *)
theory ODRLDeonticOntology
  imports Main
begin

(* ── Sorts ──────────────────────────────────────────────────
   Seven base types.  All abstract -- no structure beyond
   what axioms impose.
   ─────────────────────────────────────────────────────────── *)
typedecl Agent
typedecl Action
typedecl Target
typedecl Rule
typedecl Position
typedecl LegalRelator
typedecl Event

(* ── Hohfeldian position classifiers ────────────────────────
   Conduct:    Permission  Duty  Right  NoRight
   Competence: Power  Subj  Immunity  Disability
   ─────────────────────────────────────────────────────────── *)
consts
  Permission    :: "Position => bool"
  Duty          :: "Position => bool"
  Right         :: "Position => bool"
  NoRight       :: "Position => bool"
  Power         :: "Position => bool"
  Subj          :: "Position => bool"
  Immunity      :: "Position => bool"
  Disability    :: "Position => bool"

consts
  remAct :: "Rule => Action => bool"

(* ── Rule classifiers ───────────────────────────────────────
   Perm / Proh / obl: ODRL rule types
   obl:      ODRL Duty rule (distinct from Hohfeldian Duty above)
   has_rem:  prohibition carries odrl:remedy  (paper: \hasrem)
   strong:   strongly-permitted (profile extension point)
   ─────────────────────────────────────────────────────────── *)
consts
  Perm    :: "Rule => bool"
  Proh    :: "Rule => bool"
  obl     :: "Rule => bool"
  has_rem :: "Rule => bool"
  strong  :: "Rule => bool"

(* ── Relator classifiers ────────────────────────────────────
   Rel:      rho is a legal relator
   ODRLRel:  rho is a relator founded by an ODRL rule activation.
             Gates correlativity (Ax5.8).
   ─────────────────────────────────────────────────────────── *)
consts
  Rel     :: "LegalRelator => bool"
  ODRLRel :: "LegalRelator => bool"

(* ── Structural relations ───────────────────────────────────
   aee / aer / act / tgt: rule parameters
   activates:   event e activates rule r
   founds:      Event => LegalRelator => Rule => bool
                founds(e, rho, r): e founds the CONDUCT relator rho for rule r.
                Used by: Ax5.1 (Permission), Ax5.3 (Prohibition), Ax5.5 (Obligation).
   founds_rem:  Event => LegalRelator => Rule => bool
                founds_rem(e, rho_R, f): e founds the COMPETENCE (remedy) relator
                rho_R for prohibition f carrying odrl:remedy.
                DISTINCT from founds so rho_F =/= rho_R (paper Table 1 footnote).
   founds_imm:  Event => LegalRelator => Rule => bool
                founds_imm(e, rho_I, p): e founds the COMPETENCE (immunity) relator
                rho_I for strongly-permitted rule p.
                DISTINCT from founds so rho_P =/= rho_I (paper Ax5.2 note).
   bearer:      position p is borne by agent x
   cnt:         position p has content (action a, target t)
   partOf:      position p is a mereological part of relator rho
   ─────────────────────────────────────────────────────────── *)
consts
  aee        :: "Rule => Agent => bool"
  aer        :: "Rule => Agent => bool"
  act        :: "Rule => Action => bool"
  tgt        :: "Rule => Target => bool"
  activates  :: "Event => Rule => bool"
  founds     :: "Event => LegalRelator => Rule => bool"
  founds_rem :: "Event => LegalRelator => Rule => bool"   (* FIX 1 -- added *)
  founds_imm :: "Event => LegalRelator => Rule => bool"   (* FIX 1 -- added *)
  bearer     :: "Position => Agent => bool"
  cnt        :: "Position => Action => Target => bool"
  partOf     :: "Position => LegalRelator => bool"

(* ── rfr : Action -> Action  (injective, irreflexive) ───────
   Maps a regulated action to its forbearance (omission).
   rfr(a) =/= a enforces Act/Forbearance sort disjointness.
   Prohibitions impose Duty over rfr(a), not a directly.
   ─────────────────────────────────────────────────────────── *)
consts rfr :: "Action => Action"

axiomatization where
  rfr_irreflexive : "ALL a.   rfr a ~= a"       and
  rfr_injective   : "ALL a b. rfr a = rfr b --> a = b"

(* ── decl : Action -> Action  (injective, disjoint from rfr) ─
   Maps a regulated action to the institutional act of
   declaring its violation.
   decl(a) =/= rfr(a) prevents collapse between
   proh_relator_conduct (Duty/Right over rfr(a)) and
   proh_relator_remedy  (Power/Subj over decl(a)).
   ─────────────────────────────────────────────────────────── *)
consts decl :: "Action => Action"

axiomatization where
  decl_injective    : "ALL a b. decl a = decl b --> a = b" and
  decl_rfr_disjoint : "ALL a.   decl a ~= rfr a"

(* ── Ax 5.1  Permission Relator -- Weak ─────────────────────
   Paper: ax:perm-relator-weak
   Perm(p) activated at e founds conduct relator rho_P containing:
     - Permission l  borne by assignee x over <a,t>
     - NoRight n     borne by assigner y over <a,t>  (correlative)
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_perm_relator_weak :
    "ALL p x y a t e.
       Perm p & aee p x & aer p y & act p a & tgt p t & activates e p
       -->
       (EX rho l n.
          Rel rho & founds e rho p
          & Permission l & bearer l x & cnt l a t & partOf l rho
          & NoRight n   & bearer n y & cnt n a t & partOf n rho)"

(* ── Ax 5.2  Permission Relator -- Strong ───────────────────
   Paper: ax:perm-relator-strong
   FIX 2: Strong permission founds a SECOND distinct simple relator rho_I
   via founds_imm (not founds), bundling Immunity--Disability.
   rho_P =/= rho_I because founds and founds_imm are distinct predicates
   (paper: "Two simple relators, one founding event").
   Conduct relator rho_P is founded by Ax5.1 (founds).
   Competence relator rho_I is founded here (founds_imm).
   strong(p) is a profile extension point (not in ODRL 2.2 core).
   Immunity is not exclusive to strong permission -- open-world (paper note).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_perm_relator_strong :
    "ALL p x y a t e.
       Perm p & strong p & aee p x & aer p y & act p a & tgt p t & activates e p
       -->
       (EX rho_I im db.
          Rel rho_I & founds_imm e rho_I p
          & Immunity   im & bearer im x & cnt im a t & partOf im rho_I
          & Disability db & bearer db y & cnt db a t & partOf db rho_I)"

(* ── Ax 5.3  Prohibition Relator -- Conduct ─────────────────
   Paper: ax:proh-relator-conduct
   Proh(f) activated at e founds conduct relator rho_F containing:
     - Duty d  borne by assignee x over <rfr(a),t>  (duty to OMIT)
     - Right c borne by assigner y over <rfr(a),t>  (correlative)
   Content is rfr(a), not a: prohibitions regulate the omission.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_proh_relator_conduct :
    "ALL f x y a t e.
       Proh f & aee f x & aer f y & act f a & tgt f t & activates e f
       -->
       (EX rho d c.
          Rel rho & founds e rho f
          & Duty d  & bearer d x & cnt d (rfr a) t & partOf d rho
          & Right c & bearer c y & cnt c (rfr a) t & partOf c rho)"

(* ── Ax 5.4  Prohibition Relator -- Remedy ──────────────────
   Paper: ax:proh-relator-remedy
   FIX 3: A prohibition carrying has_rem founds a SECOND distinct simple
   relator rho_R via founds_rem (not founds), bundling Power--Subj.
   rho_F =/= rho_R because founds and founds_rem are distinct predicates
   (paper: "Two simple relators, one activation event").
   Conduct relator rho_F is founded by Ax5.3 (founds).
   Competence relator rho_R is founded here (founds_rem).
   Power is constituted at ACTIVATION, not at violation:
   it is a standing position licensing a future institutional act.
   Content is decl(a), not rfr(a) or a.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_proh_relator_remedy :
    "ALL f x y a t e.
       Proh f & has_rem f & aee f x & aer f y & act f a & tgt f t & activates e f
       -->
       (EX rho_R pw s.
          Rel rho_R & founds_rem e rho_R f
          & Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho_R
          & Subj  s  & bearer s  x & cnt s  (decl a) t & partOf s  rho_R)"

(* ── Ax 5.5  Obligation Relator ─────────────────────────────
   Paper: ax:obl-relator  (paper Ax5.5; was mislabelled Ax5.7 before)
   obl(d) activated at e founds conduct relator rho containing:
     - Duty du  borne by assignee x over <a,t>  (duty to PERFORM)
     - Right c  borne by assigner y over <a,t>  (correlative)
   Content is a directly -- duty to act, not to refrain.
   Contrast with Ax5.3 where content is rfr(a).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_obl_relator :
    "ALL d x y a t e.
       obl d & aee d x & aer d y & act d a & tgt d t & activates e d
       -->
       (EX rho du c.
          Rel rho & founds e rho d
          & Duty du & bearer du x & cnt du a t & partOf du rho
          & Right c  & bearer c  y & cnt c  a t & partOf c  rho)"

(* ── Ax 5.6  Unique Founding ────────────────────────────────
   Paper: ax:unique-founding  (paper Ax5.6; was mislabelled Ax5.5 before)
   FIX 4: Applies independently to EACH of the three founding predicates:
   founds, founds_rem, founds_imm.
   Two directions per predicate:
   (1) same (e, r) pair founds at most one relator
   (2) same (rho, r) pair is founded by at most one event
   Together: a relator is individuated by its (e,r) pair.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_unique_founding_relator :
    "ALL r rho1 rho2 e.
       founds e rho1 r & founds e rho2 r --> rho1 = rho2"
  and
  ax_unique_founding_event :
    "ALL r e1 e2 rho.
       founds e1 rho r & founds e2 rho r --> e1 = e2"
  and
  ax_unique_founding_relator_rem :
    "ALL r rho1 rho2 e.
       founds_rem e rho1 r & founds_rem e rho2 r --> rho1 = rho2"
  and
  ax_unique_founding_event_rem :
    "ALL r e1 e2 rho.
       founds_rem e1 rho r & founds_rem e2 rho r --> e1 = e2"
  and
  ax_unique_founding_relator_imm :
    "ALL r rho1 rho2 e.
       founds_imm e rho1 r & founds_imm e rho2 r --> rho1 = rho2"
  and
  ax_unique_founding_event_imm :
    "ALL r e1 e2 rho.
       founds_imm e1 rho r & founds_imm e2 rho r --> e1 = e2"

(* ── Ax 5.7  ODRL Relator Typing ───────────────────────────
   Paper: ax:odrl-rel-typing  (paper Ax5.7; was mislabelled Ax5.6 before)
   FIX 5: Three instances -- one per founding predicate:
     founds     & (Perm | Proh | obl) --> ODRLRel
     founds_rem & Proh                --> ODRLRel
     founds_imm & Perm                --> ODRLRel
   Gates ax_correlativity (Ax5.8) to ODRL relators only.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_odrl_rel_typing :
    "ALL e rho r.
       founds e rho r & (Perm r | Proh r | obl r)
       --> ODRLRel rho"
  and
  ax_odrl_rel_typing_rem :
    "ALL e rho r.
       founds_rem e rho r & Proh r
       --> ODRLRel rho"
  and
  ax_odrl_rel_typing_imm :
    "ALL e rho r.
       founds_imm e rho r & Perm r
       --> ODRLRel rho"

(* ── Ax 5.8  Correlativity ──────────────────────────────────
   Paper: ax:correlativity  (paper Ax5.8)
   Each ODRL legal relator rho contains exactly one position
   from each correlative pair over the same <a,t> content.
   Four biconditionals with EX! (unique existence):
     Permission <-> NoRight      (conduct)
     Duty       <-> Right        (conduct)
     Power      <-> Subj         (competence)
     Immunity   <-> Disability   (competence)
   Gated on ODRLRel(rho) -- set by Ax5.7.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_correlativity_permission_noright :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! l. Permission l & partOf l rho & cnt l a t)
        =
        (EX! n. NoRight n & partOf n rho & cnt n a t))"
  and
  ax_correlativity_duty_right :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! d. Duty d  & partOf d rho & cnt d a t)
        =
        (EX! c. Right c & partOf c rho & cnt c a t))"
  and
  ax_correlativity_power_subj :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! pw. Power pw & partOf pw rho & cnt pw a t)
        =
        (EX! s.  Subj  s  & partOf s  rho & cnt s  a t))"
  and
  ax_correlativity_immunity_disability :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! im. Immunity   im & partOf im rho & cnt im a t)
        =
        (EX! db. Disability db & partOf db rho & cnt db a t))"

(* ── Ax 5.9  Normative Position Incompatibility ────────────
   Paper: ax:cross-relator  (paper Ax5.9)
   FIX 7 (comment): This is a NORMATIVE fact, independent of UFO type
   disjointness.  UFO type disjointness governs whether a single moment
   individual can have two types.  This axiom governs whether a BEARER
   can hold two distinct moments of incompatible types -- which requires
   a separate normative axiom (paper §5, Ax5.9 note).
   No agent can simultaneously bear a Permission to Act and a
   Duty to Omit over the same <a,t>.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_cross_relator :
    "ALL l d x a t.
       Permission l & bearer l x & cnt l a t
       & Duty d  & bearer d x & cnt d (rfr a) t
       --> False"

(* ── Corollary 5.9a  Permission-Duty Conflict Within a Relator ─
   Paper: ax:conflict
   Immediate from ax_cross_relator.
   ─────────────────────────────────────────────────────────── *)
lemma conflict_within_relator :
  "ALL rho l d x a t.
     ODRLRel rho
     & Permission l & bearer l x & cnt l a t & partOf l rho
     & Duty d    & bearer d x & cnt d (rfr a) t & partOf d rho
     --> False"
  using ax_cross_relator by blast

(* ── Ax 5.10  Disability Precludes Prohibition Creation ────
   Paper: ax:disability-block  (paper Ax5.10)
   No prohibition by assigner y over <a,t> can exist while y holds
   a Disability over that same pair.  Required for adequacy of the
   strong-permission grounding (thm:strong-crosslevel).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_disability_block :
    "ALL f x y a t.
       Proh f & aee f x & aer f y & act f a & tgt f t
       --> ~ (EX db. Disability db & bearer db y & cnt db a t)"

(* ── Ax 5.11  ODRL Relator Is a Relator ────────────────────
   Paper: ax:odrl-rel-is-rel  (Table 2, SZS column "Thm")
   Every relator founded by any of the three founding predicates
   is a legal relator (Rel).  Covers rho_R and rho_I which are
   not reachable by Ax5.1/5.3/5.5 alone after FIX 2 and FIX 3.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_odrl_rel_is_rel :
    "ALL e rho r. founds     e rho r --> Rel rho"
  and
  ax_odrl_rel_is_rel_rem :
    "ALL e rho r. founds_rem e rho r --> Rel rho"
  and
  ax_odrl_rel_is_rel_imm :
    "ALL e rho r. founds_imm e rho r --> Rel rho"

(* ── Predicate shorthand note ───────────────────────────────
   In the paper, Permission(x,a,t) abbreviates
   EX l. Permission(l) & bearer(l,x) & cnt(l,a,t).
   In this theory we use the long form throughout for clarity.
   Abbreviations: see paper Appendix app:abbrev.
   ─────────────────────────────────────────────────────────── *)

(* ── Faithfulness Lemmas F1–F3 ──────────────────────────────
   Paper: prop:faithfulness (Proposition 5.12)
   Soundness: each evaluator verdict traces to one axiom.
   Incompleteness: grounding entails four additional positions
   (NoRight, Right-to-Omission, Immunity, Disability) absent
   from the W3C Evaluation Report.
   ─────────────────────────────────────────────────────────── *)
lemma faithfulness_F1 :
  "ALL p x y a t e.
     Perm p & aee p x & aer p y & act p a & tgt p t & activates e p
     --> (EX l. Permission l & bearer l x & cnt l a t)"
  using ax_perm_relator_weak by blast

lemma faithfulness_F2 :
  "ALL f x y a t e.
     Proh f & aee f x & aer f y & act f a & tgt f t & activates e f
     --> (EX d. Duty d & bearer d x & cnt d (rfr a) t)"
  using ax_proh_relator_conduct by blast

(* FIX 9: faithfulness_F3 uses founds_rem (not founds) in the conclusion,
   because the remedy relator rho_R is founded by ax_proh_relator_remedy
   via founds_rem, not founds.                                            *)
lemma faithfulness_F3 :
  "ALL f x y a t e.
     Proh f & has_rem f & aee f x & aer f y & act f a & tgt f t
     & activates e f
     --> (EX rho_R pw. founds_rem e rho_R f
          & Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho_R)"
  using ax_proh_relator_remedy by blast

(* ── Appendix A.2 -- Abstract normative position witness ────
   NormPos: abstract type for A1--A3 and B1--B3.
   Distinct from Position (concrete Hohfeldian moment).
   ─────────────────────────────────────────────────────────── *)
typedecl NormPos

consts
  NormStateChange :: "Agent => Action => Target => NormPos => bool"
  InstEvent       :: "Event => bool"
  triggers        :: "Event => Agent => Action => Target => NormPos => bool"
  competentFor    :: "Agent => Event => bool"
  aboutEvent      :: "Position => Event => bool"
  does            :: "Agent => Action => Target => bool"
  Duty_rem        :: NormPos

(* ── Appendix A.2 -- Axiom A1 ───────────────────────────────
   Paper: ax:A1
   Any normative state change requires a triggering institutional event.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_A1 :
    "ALL x a t q.
       NormStateChange x a t q
       --> (EX e. InstEvent e & triggers e x a t q)"

(* ── Appendix A.2 -- Axiom A2 ───────────────────────────────
   Paper: ax:A2
   No institutional event occurs without a competent agent.
   Agent(y) absorbed by type system (y :: Agent).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_A2 :
    "ALL e.
       InstEvent e
       --> (EX y. competentFor y e)"

(* ── Appendix A.2 -- Axiom A3 ───────────────────────────────
   Paper: ax:A3
   Competence to perform institutional event e is grounded in
   a Power--Subjection pair.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_A3 :
    "ALL y e.
       competentFor y e
       --> (EX pw s x.
              Power pw & bearer pw y & aboutEvent pw e
              & Subj s  & bearer s  x & aboutEvent s  e)"

(* ── Appendix A.2 -- Bridge Axiom B1 ────────────────────────
   Paper: B1
   Performing action a in violation of prohibition f (with remedy)
   constitutes a normative state change activating the remedy duty.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_B1 :
    "ALL f x a t.
       Proh f & has_rem f & act f a & tgt f t & aee f x
       & does x a t
       --> (EX b. remAct f b & NormStateChange x b t Duty_rem)"

(* ── Appendix A.2 -- Bridge Axiom B2 ────────────────────────
   Paper: B2
   FIX 8: Uses founds_rem (not founds): the remedy Power is in rho_R,
   which is founded by founds_rem.  B2 links that relator to aboutEvent.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_B2 :
    "ALL pw a t rho e f.
       Power pw & cnt pw (decl a) t
       & partOf pw rho & founds_rem e rho f
       --> aboutEvent pw e"

(* ── Appendix A.2 -- Bridge Axiom B3 ────────────────────────
   Paper: B3
   FIX 8: Uses founds_rem (not founds): the remedy Subj is in rho_R.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_B3 :
    "ALL s a t rho e f.
       Subj s & cnt s (decl a) t
       & partOf s rho & founds_rem e rho f
       --> aboutEvent s e"

(* ── Proposition prop:sanctioned ───────────────────────────
   Paper: prop:sanctioned (§3)
   ODRL prohibition is SANCTIONED: violation triggers
   NormStateChange via the B1 --> A1 chain.
   ─────────────────────────────────────────────────────────── *)
lemma prop_sanctioned :
  assumes "Proh f" "has_rem f"
          "act f a" "tgt f t" "aee f x"
          "does x a t"
  shows "EX e b. InstEvent e & remAct f b
                 & NormStateChange x b t Duty_rem
                 & triggers e x b t Duty_rem"
proof -
  from assms ax_B1
    obtain b where B: "remAct f b & NormStateChange x b t Duty_rem"
      by blast
  from B ax_A1
    obtain e where E: "InstEvent e & triggers e x b t Duty_rem"
      by blast
  show ?thesis
    using B E by blast
qed

(* ── Proposition prop:weak-complete ────────────────────────
   Paper: prop:weak-complete (§4)
   Weak permission is adequately characterised at conduct level.
   Direction (a): Permission + NoRight are entailed.
   Direction (b): no competence axiom needed -- proof closes
   using only ax_perm_relator_weak.
   ─────────────────────────────────────────────────────────── *)
lemma prop_weak_complete_conduct :
  assumes "Perm p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p"
  shows "EX rho l n.
           Permission l & bearer l x & cnt l a t & partOf l rho
           & NoRight n & bearer n y & cnt n a t & partOf n rho"
  using assms ax_perm_relator_weak by blast

lemma prop_weak_complete_no_competence_needed :
  assumes "Perm p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p"
  shows "EX l n.
           Permission l & bearer l x & cnt l a t
           & NoRight n & bearer n y & cnt n a t"
  using assms ax_perm_relator_weak by blast

(* ── Theorem thm:strong-crosslevel ─────────────────────────
   Paper: thm:strong-crosslevel (§4)
   Strong permission is cross-level.
   Part 1 (H1 inadequate): Permission + NoRight alone is destroyed
     by a prohibition from y, via ax_proh_relator_conduct +
     ax_cross_relator (NORMATIVE incompatibility, not type disjointness).
   Part 2 (H2 adequate): Disability blocks the prohibition
     via ax_disability_block.
   ─────────────────────────────────────────────────────────── *)
lemma thm_strong_crosslevel_H1_inadequate :
  assumes
    "Permission l" "bearer l x" "cnt l a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f"
  shows "False"
proof -
  from assms ax_proh_relator_conduct
    obtain rho d c where
      D: "Duty d" "bearer d x" "cnt d (rfr a) t"
      by blast
  from assms(1,2,3) D ax_cross_relator
  show ?thesis by blast
qed

lemma thm_strong_crosslevel_H2_adequate :
  assumes
    "Permission l"  "bearer l x"  "cnt l a t"
    "Disability db" "bearer db y" "cnt db a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
  shows "False"
proof -
  from assms ax_disability_block
  have "~ (EX db. Disability db & bearer db y & cnt db a t)"
    by blast
  with assms show ?thesis by blast
qed

(* ── Theorem thm:sanctioned-crosslevel ─────────────────────
   Paper: thm:sanctioned-crosslevel (§4)
   Sanctioned prohibition is cross-level.
   Part 1 (H3 inadequate): {Duty, Right} provides no Power.
   Part 2 (H4 adequate):   adding Power + Subj grounds the full chain.
   FIX 11: H4 premise uses founds_rem (not founds) for the remedy relator.
   ─────────────────────────────────────────────────────────── *)
lemma thm_sanctioned_crosslevel_H3_inadequate :
  assumes
    "Proh f" "has_rem f"
    "act f a" "tgt f t" "aee f x"
    "does x a t"
    "ALL pw. ~ (Power pw & bearer pw y & aboutEvent pw e')"
    "InstEvent e'"
    "competentFor y e'"
  shows "False"
proof -
  from assms(9) ax_A3
    obtain pw s z where
      PW: "Power pw" "bearer pw y" "aboutEvent pw e'"
      by blast
  from assms(7) PW show ?thesis by blast
qed

lemma thm_sanctioned_crosslevel_H4_adequate :
  assumes
    "Proh f" "has_rem f"
    "act f a" "tgt f t" "aee f x" "aer f y"
    "activates e f"
    "founds_rem e rho f"          (* FIX 11: founds_rem, not founds *)
    "does x a t"
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho"
    "Subj s"   "bearer s x"  "cnt s  (decl a) t" "partOf s  rho"
  shows
    "EX e' b. InstEvent e'
              & remAct f b
              & NormStateChange x b t Duty_rem
              & triggers e' x b t Duty_rem"
proof -
  from assms ax_B1
    obtain b where B1: "remAct f b" "NormStateChange x b t Duty_rem"
      by blast
  from B1(2) ax_A1
    obtain e' where A1: "InstEvent e'" "triggers e' x b t Duty_rem"
      by blast
  show ?thesis
    using B1 A1 by blast
qed

(* ── Theorem thm:crosslevel ─────────────────────────────────
   Paper: thm:crosslevel (§4)
   Any norm that is (i) violable and (ii) consequential requires
   competence-level positions.  Proof: NormStateChange chains
   A1 --> A2 --> A3 to force a Power-Subjection pair.
   ─────────────────────────────────────────────────────────── *)
lemma thm_crosslevel :
  assumes
    "NormStateChange x a t q"
    "ALL pw. ~ (Power pw & bearer pw y & aboutEvent pw e)"
    "InstEvent e"
    "competentFor y e"
  shows "False"
proof -
  from assms(4) ax_A3
    obtain pw s z where
      PW: "Power pw" "bearer pw y" "aboutEvent pw e"
      by blast
  from assms(2) PW show ?thesis by blast
qed

lemma thm_crosslevel_odrl_instance :
  assumes
    "Proh f" "has_rem f"
    "act f a" "tgt f t" "aee f x"
    "does x a t"
    "InstEvent e" "competentFor y e"
    "ALL pw. ~ (Power pw & bearer pw y & aboutEvent pw e)"
  shows "False"
proof -
  from assms ax_B1
    obtain b where NSC: "NormStateChange x b t Duty_rem"
      by blast
  from NSC assms(7,8,9) thm_crosslevel
  show ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Named lemmas (paper §6 / GRND benchmark)
   ══════════════════════════════════════════════════════════════ *)

(* Lemma 1: Permission creates Permission  (F1) *)
lemma perm_creates_Permission:
  assumes "Perm p" "aee p x" "aer p y" "act p a" "tgt p t" "activates e p"
  shows "EX rho l. Rel rho & founds e rho p &
                   Permission l & bearer l x & cnt l a t & partOf l rho"
proof -
  from assms ax_perm_relator_weak
  obtain rho l n where
    "Rel rho" "founds e rho p"
    "Permission l" "bearer l x" "cnt l a t" "partOf l rho"
    "NoRight n" "bearer n y" "cnt n a t" "partOf n rho"
    by blast
  thus ?thesis by blast
qed

(* Lemma 2: Prohibition creates Duty + Right  (F2) *)
lemma proh_creates_duty:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t" "activates e f"
  shows "EX rho d c. Rel rho & founds e rho f &
                     Duty d & bearer d x & cnt d (rfr a) t & partOf d rho &
                     Right c & bearer c y & cnt c (rfr a) t & partOf c rho"
proof -
  from assms ax_proh_relator_conduct
  obtain rho d c where
    "Rel rho" "founds e rho f"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho"
    "Right c" "bearer c y" "cnt c (rfr a) t" "partOf c rho"
    by blast
  thus ?thesis by blast
qed

(* Lemma 3: Prohibition with remedy creates Power + Subj in rho_R  (F3)
   FIX 10: rho_R is founded by founds_rem; no longer takes rho as input premise.  *)
lemma proh_remedy_creates_power:
  assumes "Proh f" "has_rem f"
          "aee f x" "aer f y" "act f a" "tgt f t"
          "activates e f"
  shows "EX rho_R pw s. Rel rho_R & founds_rem e rho_R f &
                         Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho_R &
                         Subj s  & bearer s  x & cnt s  (decl a) t & partOf s  rho_R"
proof -
  from assms ax_proh_relator_remedy
  obtain rho_R pw s where
    "Rel rho_R" "founds_rem e rho_R f"
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho_R"
    "Subj s"   "bearer s  x" "cnt s  (decl a) t" "partOf s  rho_R"
    by blast
  thus ?thesis by blast
qed

(* Lemma 4: Disability precludes prohibition creation *)
lemma disability_blocks_proh:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
          "Disability db" "bearer db y" "cnt db a t"
  shows "False"
proof -
  from assms ax_disability_block
  have "~ (EX db. Disability db & bearer db y & cnt db a t)"
    by blast
  with assms show ?thesis by blast
qed

(* Lemma 5: Permission-Duty conflict within one relator *)
lemma conflict_is_unsat:
  assumes "partOf l rho" "partOf d rho"
          "Permission l" "Duty d"
          "bearer l x" "bearer d x"
          "cnt l a t" "cnt d (rfr a) t"
  shows "False"
  using assms ax_cross_relator by blast

(* Lemma 5b: Permission-Duty conflict across any relators *)
lemma conflict_cross_relator:
  assumes "Permission l" "bearer l x" "cnt l a t"
          "Duty d"    "bearer d x" "cnt d (rfr a) t"
  shows "False"
  using assms ax_cross_relator by blast

(* Lemma 6a: Immunity + Disability blocks new Duty *)
lemma immunity_blocks_duty:
  assumes "Immunity im" "bearer im x" "cnt im a t"
          "Disability db" "bearer db y" "cnt db a t"
          "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
  shows "False"
  using assms disability_blocks_proh by blast

(* Lemma 6b: Strong permission persists under model extension *)
lemma strong_perm_persists:
  assumes
    "Permission l"  "bearer l x"  "cnt l a t"
    "Immunity im"   "bearer im x" "cnt im a t"
    "Disability db" "bearer db y" "cnt db a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f"
  shows "False"
  using assms disability_blocks_proh by blast

(* Lemma 7: Violation triggers NormStateChange  (B1) *)
lemma violation_triggers_normstate:
  assumes "Proh f" "has_rem f"
          "act f a" "tgt f t" "aee f x"
          "does x a t"
  shows "EX b. remAct f b & NormStateChange x b t Duty_rem"
  using assms ax_B1 by blast

(* Lemma 7b: NormStateChange requires institutional event  (A1) *)
lemma normstate_requires_event:
  assumes "NormStateChange x b t Duty_rem"
  shows "EX e. InstEvent e & triggers e x b t Duty_rem"
  using assms ax_A1 by blast

(* Lemma 7c: Institutional event requires competent agent  (A2) *)
lemma event_requires_competence:
  assumes "InstEvent e"
  shows "EX y. competentFor y e"
  using assms ax_A2 by blast

(* Lemma 7d: Competence grounded in Power-Subjection  (A3) *)
lemma competence_grounds_power:
  assumes "competentFor y e"
  shows "EX pw s x. Power pw & bearer pw y &
                    Subj s   & bearer s  x &
                    aboutEvent pw e & aboutEvent s e"
  using assms ax_A3 by blast

(* ── Lemma 8: Full sanctioned-prohibition lifecycle ─────────
   Paper: §6 Validation
   FIX 12: rho_F (conduct) and rho_R (remedy) are now DISTINCT relators.
   rho_F is founded by founds; rho_R by founds_rem.
   The conclusion separates the two relators explicitly.
   ─────────────────────────────────────────────────────────── *)
lemma full_lifecycle:
  assumes
    "Proh f" "has_rem f"
    "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f"
    "does x a t"
  shows
    "(EX rho_F d c.
       Rel rho_F & founds e rho_F f &
       Duty d  & bearer d x & cnt d (rfr a) t & partOf d rho_F &
       Right c & bearer c y & cnt c (rfr a) t & partOf c rho_F) &
    (EX rho_R pw s.
       Rel rho_R & founds_rem e rho_R f &
       Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho_R &
       Subj s   & bearer s  x & cnt s  (decl a) t & partOf s  rho_R) &
    (EX b. remAct f b & NormStateChange x b t Duty_rem) &
    (EX e' b. InstEvent e' & remAct f b & triggers e' x b t Duty_rem &
              (EX y'. competentFor y' e' &
                      (EX pw' s' x''.
                         Power pw' & bearer pw' y' &
                         Subj s'   & bearer s'  x'' &
                         aboutEvent pw' e' & aboutEvent s' e')))"
proof -
  from assms ax_proh_relator_conduct
  obtain rho_F d c where
    rF: "Rel rho_F" "founds e rho_F f"
        "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho_F"
        "Right c" "bearer c y" "cnt c (rfr a) t" "partOf c rho_F"
    by blast
  from assms ax_proh_relator_remedy
  obtain rho_R pw s where
    rR: "Rel rho_R" "founds_rem e rho_R f"
        "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho_R"
        "Subj s"   "bearer s  x" "cnt s  (decl a) t" "partOf s  rho_R"
    by blast
  from assms ax_B1
  obtain b where
    bB: "remAct f b" "NormStateChange x b t Duty_rem"
    by blast
  from bB(2) ax_A1
  obtain e' where
    eE: "InstEvent e'" "triggers e' x b t Duty_rem"
    by blast
  from eE(1) ax_A2
  obtain y' where comp: "competentFor y' e'"
    by blast
  from comp ax_A3
  obtain pw' s' x'' where
    psa: "Power pw'" "bearer pw' y'"
         "Subj s'"   "bearer s'  x''"
         "aboutEvent pw' e'" "aboutEvent s' e'"
    by blast
  show ?thesis
    apply (intro conjI)
    subgoal using rF by blast
    subgoal using rR by blast
    subgoal using bB by blast
    subgoal using eE bB comp psa by blast
    done
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 9: Correlativity uniqueness  (Ax5.8 / GRND006)
   ══════════════════════════════════════════════════════════════ *)
lemma permission_unique_noright:
  assumes "ODRLRel rho"
          "EX! l. Permission l & partOf l rho & cnt l a t"
  shows "EX! n. NoRight n & partOf n rho & cnt n a t"
proof -
  from ax_correlativity_permission_noright
  have inst: "ODRLRel rho -->
    ((EX! l. Permission l & partOf l rho & cnt l a t) =
     (EX! n. NoRight n & partOf n rho & cnt n a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed

lemma duty_unique_right:
  assumes "ODRLRel rho"
          "EX! d. Duty d & partOf d rho & cnt d a t"
  shows "EX! c. Right c & partOf c rho & cnt c a t"
proof -
  from ax_correlativity_duty_right
  have inst: "ODRLRel rho -->
    ((EX! d. Duty d & partOf d rho & cnt d a t) =
     (EX! c. Right c & partOf c rho & cnt c a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed

lemma power_unique_subj:
  assumes "ODRLRel rho"
          "EX! pw. Power pw & partOf pw rho & cnt pw a t"
  shows "EX! s. Subj s & partOf s rho & cnt s a t"
proof -
  from ax_correlativity_power_subj
  have inst: "ODRLRel rho -->
    ((EX! pw. Power pw & partOf pw rho & cnt pw a t) =
     (EX! s. Subj s & partOf s rho & cnt s a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed

lemma immunity_unique_disability:
  assumes "ODRLRel rho"
          "EX! im. Immunity im & partOf im rho & cnt im a t"
  shows "EX! db. Disability db & partOf db rho & cnt db a t"
proof -
  from ax_correlativity_immunity_disability
  have inst: "ODRLRel rho -->
    ((EX! im. Immunity im & partOf im rho & cnt im a t) =
     (EX! db. Disability db & partOf db rho & cnt db a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 10: Unique founding consequences  (Ax5.6 / GRND)
   ══════════════════════════════════════════════════════════════ *)
lemma unique_founding_determines_relator:
  assumes "founds e rho1 r" "founds e rho2 r"
  shows "rho1 = rho2"
  using assms ax_unique_founding_relator by blast

lemma two_activations_two_relators:
  assumes "founds e1 rho1 r" "founds e2 rho2 r" "e1 ~= e2"
  shows "rho1 ~= rho2"
proof -
  from assms ax_unique_founding_relator
  have "rho1 = rho2 --> founds e1 rho2 r" by blast
  with assms ax_unique_founding_event
  have "rho1 = rho2 --> e1 = e2" by blast
  with assms show ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 11: Grounding strictly richer than ODRL evaluator
   Paper: prop:faithfulness converse / Table 1 rows 2,4,7,8
   ══════════════════════════════════════════════════════════════ *)
lemma grounding_surfaces_noright:
  assumes "Perm p" "aee p x" "aer p y" "act p a" "tgt p t" "activates e p"
  shows "EX rho n. Rel rho & founds e rho p &
                   NoRight n & bearer n y & cnt n a t & partOf n rho"
proof -
  from assms ax_perm_relator_weak
  obtain rho l n where
    "Rel rho" "founds e rho p"
    "Permission l" "bearer l x" "cnt l a t" "partOf l rho"
    "NoRight n" "bearer n y" "cnt n a t" "partOf n rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_right:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t" "activates e f"
  shows "EX rho c. Rel rho & founds e rho f &
                   Right c & bearer c y & cnt c (rfr a) t & partOf c rho"
proof -
  from assms ax_proh_relator_conduct
  obtain rho d c where
    "Rel rho" "founds e rho f"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho"
    "Right c" "bearer c y" "cnt c (rfr a) t" "partOf c rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_immunity:
  assumes "Perm p" "strong p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p"
  shows "EX rho_I im. Rel rho_I & founds_imm e rho_I p &
                       Immunity im & bearer im x & cnt im a t & partOf im rho_I"
proof -
  from assms ax_perm_relator_strong
  obtain rho_I im db where
    "Rel rho_I" "founds_imm e rho_I p"
    "Immunity im"   "bearer im x"  "cnt im a t"  "partOf im rho_I"
    "Disability db" "bearer db y"  "cnt db a t"  "partOf db rho_I"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_disability:
  assumes "Perm p" "strong p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p"
  shows "EX rho_I db. Rel rho_I & founds_imm e rho_I p &
                       Disability db & bearer db y & cnt db a t & partOf db rho_I"
proof -
  from assms ax_perm_relator_strong
  obtain rho_I im db where
    "Rel rho_I" "founds_imm e rho_I p"
    "Immunity im"   "bearer im x"  "cnt im a t"  "partOf im rho_I"
    "Disability db" "bearer db y"  "cnt db a t"  "partOf db rho_I"
    by blast
  thus ?thesis by blast
qed

end
