"""
problem_data_hard.py
====================
Hard/medium problems for the PAAR 2026 automated reasoning track.
These test deeper inference chains, multi-relator reasoning,
and untested functions (issue/1).
  GRND019  Two policies conflict via assigner Right          Hard
  GRND020  Strong perm + prohibition attempt = Unsat (H2)   Medium
  GRND021  Full A1-B1-B2-B3 violation-to-remedy chain       Hard
  GRND022  Correlativity blocks non-unique NoRight           Medium
  GRND023  Policy issuance Power (P3-P4, issue/1)           Hard
  GRND024  obl + proh on same target = coexist              Medium
Fix history:
  Bug 1  — GRND019: liberty -> permission (UFO-L terms)
  Bug 2  — GRND022: ax_correlativity_liberty -> ax_correlativity_permission;
            liberty -> permission
  Bug 3  — GRND023: SMT2 conjecture was (not (= (issue pi) (issue pi))) —
            trivially (assert false). Replaced with injectivity negation
            using two distinct rule constants.
  v1.5   — GRND019: ax_proh_relator_basic -> ax_proh_relator_conduct;
                     ax_cross_relator_consistency -> ax_cross_relator (KeyError fix)
          — GRND020: ax_perm_relator_basic -> ax_perm_relator_weak (KeyError fix)
          — GRND021: ax_proh_relator_basic -> ax_proh_relator_conduct (KeyError fix)
          — GRND023: fof_axioms: [] — issue/1 is in Layer0; ax_obl_relator unrelated
          — GRND024: ax_proh_relator_basic -> ax_proh_relator_conduct;
                     ax_cross_relator_consistency -> ax_cross_relator (KeyError fix)
          — SMT2: Action -> NormContent throughout (unified sort fix)
          — TTL: angle brackets removed from drk:-prefixed terms throughout
  Note   — GRND020/GRND021: founds(e1,rho1,...) assertions are redundant
            (Ax5.2 and Ax5.4 fire from activates alone) but harmless —
            retained for explicitness.
"""

PROBLEMS_HARD = [
    # =========================================================================
    # GRND019 — Two policies conflict via assigner Right
    # Difficulty: Hard
    # v1.5: ax_proh_relator_basic -> ax_proh_relator_conduct
    #        ax_cross_relator_consistency -> ax_cross_relator
    #        SMT2: Action -> NormContent; TTL: angle brackets removed
    # Abstract constants:
    #   bibliothek = drk:UniversitaetsbibliothekMuenchen (assignee)
    #   ensemble   = drk:BerlinerEnsemble (assigner perm)
    #   museen     = drk:StaatlicheMuseenBerlin (assigner proh1)
    #   philharmonie = drk:PhilharmonieBerlin (assigner proh2)
    # =========================================================================
    {
        "id": "GRND019-two-policy-conflict", "subdir": "Discriminating",
        "name": "Two policies conflict: competing Rights from distinct assigners",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_proh_relator_conduct",
            "ax_cross_relator",
        ],
        "description": """\
% Two prohibitions over the same (bibliothek, read, theater_ds):
%   f1: assigner museen, activates at e1 => Duty(bibliothek,rfr(read),theater_ds)
%   f2: assigner philharmonie, activates at e2 => Duty(bibliothek,rfr(read),theater_ds)
% bibliothek also holds Permission(bibliothek,read,theater_ds).
% ax_cross_relator: Permission + Duty(rfr) => False.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   ensemble=drk:BerlinerEnsemble, museen=drk:StaatlicheMuseenBerlin,
%   philharmonie=drk:PhilharmonieBerlin, read=odrl:read,
%   theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Two competing prohibitions from different assigners over the same asset.
# Combined with an existing Permission => conflict.
drk:policy-conflict-two a odrl:Agreement ;
    odrl:permission  [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:BerlinerEnsemble ;
        odrl:action   odrl:read ;
        odrl:target   drk:TheaterShowtimeDataset ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:TheaterShowtimeDataset ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:PhilharmonieBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:TheaterShowtimeDataset ] .
drk:TheaterShowtimeDataset          a dcat:Dataset .
drk:BerlinerEnsemble                a schema:Organization .
drk:StaatlicheMuseenBerlin          a schema:Organization .
drk:PhilharmonieBerlin              a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   museen=drk:StaatlicheMuseenBerlin, philharmonie=drk:PhilharmonieBerlin""",
        "fof_extra_decls": """\
fof(agent_bibliothek,   axiom, agent(bibliothek)).
fof(agent_museen,       axiom, agent(museen)).
fof(agent_philharmonie, axiom, agent(philharmonie)).
fof(action_read,        axiom, action(read)).
fof(target_theater,     axiom, target(theater_ds)).
% Existing permission
fof(pos_l,              axiom, position(l)).
fof(permission_l,       axiom, permission(l)).
fof(bearer_l,           axiom, bearer(l, bibliothek)).
fof(cnt_l,              axiom, cnt(l, read, theater_ds)).
% Prohibition 1: museen prohibits bibliothek from reading theater_ds
fof(rule_f1,            axiom, rule(f1)).
fof(event_e1,           axiom, event(e1)).
fof(proh_f1,            axiom, proh(f1)).
fof(aee_f1,             axiom, aee(f1, bibliothek)).
fof(aer_f1,             axiom, aer(f1, museen)).
fof(act_f1,             axiom, act(f1, read)).
fof(tgt_f1,             axiom, tgt(f1, theater_ds)).
fof(act_e1_f1,          axiom, activates(e1, f1)).
% Prohibition 2: philharmonie also prohibits bibliothek
fof(rule_f2,            axiom, rule(f2)).
fof(event_e2,           axiom, event(e2)).
fof(proh_f2,            axiom, proh(f2)).
fof(aee_f2,             axiom, aee(f2, bibliothek)).
fof(aer_f2,             axiom, aer(f2, philharmonie)).
fof(act_f2,             axiom, act(f2, read)).
fof(tgt_f2,             axiom, tgt(f2, theater_ds)).
fof(act_e2_f2,          axiom, activates(e2, f2)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const bibliothek   Agent)
(declare-const museen       Agent) (declare-const philharmonie Agent)
(declare-const read         NormContent) (declare-const theater-ds Target)
(declare-const l            Position)
(declare-const f1           Rule) (declare-const e1 Event)
(declare-const f2           Rule) (declare-const e2 Event)
(assert (permission l)) (assert (bearer l bibliothek)) (assert (cnt l read theater-ds))
; Prohibition 1
(assert (proh f1))
(assert (aee f1 bibliothek)) (assert (aer f1 museen))
(assert (act f1 read))       (assert (tgt f1 theater-ds))
(assert (activates e1 f1))
; Prohibition 2
(assert (proh f2))
(assert (aee f2 bibliothek)) (assert (aer f2 philharmonie))
(assert (act f2 read))       (assert (tgt f2 theater-ds))
(assert (activates e2 f2))
""",
        "smt2_conjecture": None,
    },

    # =========================================================================
    # GRND020 — Strong perm + prohibition attempt = Unsatisfiable (full H2)
    # Difficulty: Medium
    # v1.5: ax_perm_relator_basic -> ax_perm_relator_weak
    #        SMT2: Action -> NormContent; TTL: angle brackets removed
    # Abstract constants:
    #   bibliothek = drk:UniversitaetsbibliothekMuenchen (assignee)
    #   museen     = drk:StaatlicheMuseenBerlin (assigner)
    # =========================================================================
    {
        "id": "GRND020-strong-perm-full-h2", "subdir": "Discriminating",
        "name": "Strong permission full H2: Disability blocks same assigner prohibition",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_perm_relator_weak",
            "ax_perm_relator_strong",
            "ax_disability_block",
        ],
        "description": """\
% perm(p1) + strong(p1) + activates(e1,p1).
% Ax5.2 (founds_imm): creates rho_I with Immunity(bibliothek,read,museum_api)
%                     and Disability(museen,read,museum_api).
% proh(f2) with aer(f2,museen) also asserted.
% ax_disability_block: Disability(museen,read,museum_api) + proh(f2,aer=museen) => False.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   museen=drk:StaatlicheMuseenBerlin, read=odrl:read,
%   museum_api=drk:MuseumCollectionAPI""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Strong permission: assigner holds Disability over the asset.
# Assigner then attempts to issue a prohibition => blocked.
drk:policy-strong-h2 a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:MuseumCollectionAPI ] .
# strong(p) asserted by profile extension.
# drk:StaatlicheMuseenBerlin then attempts prohibition => contradiction.
drk:MuseumCollectionAPI             a dcat:DataService .
drk:StaatlicheMuseenBerlin          a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   museen=drk:StaatlicheMuseenBerlin""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_museen,     axiom, agent(museen)).
fof(action_read,      axiom, action(read)).
fof(target_museum,    axiom, target(museum_api)).
fof(rule_p1,          axiom, rule(p1)).
fof(event_e1,         axiom, event(e1)).
fof(relator_rho1,     axiom, legal_relator(rho1)).
fof(perm_p1,          axiom, perm(p1)).
fof(strong_p1,        axiom, strong(p1)).
fof(aee_p1,           axiom, aee(p1, bibliothek)).
fof(aer_p1,           axiom, aer(p1, museen)).
fof(act_p1,           axiom, act(p1, read)).
fof(tgt_p1,           axiom, tgt(p1, museum_api)).
fof(act_e1_p1,        axiom, activates(e1, p1)).
fof(founds_e1,        axiom, founds(e1, rho1, p1)).
% museen attempts a prohibition — blocked by Disability from Ax5.2
fof(rule_f2,          axiom, rule(f2)).
fof(proh_f2,          axiom, proh(f2)).
fof(aee_f2,           axiom, aee(f2, bibliothek)).
fof(aer_f2,           axiom, aer(f2, museen)).
fof(act_f2,           axiom, act(f2, read)).
fof(tgt_f2,           axiom, tgt(f2, museum_api)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const bibliothek Agent) (declare-const museen    Agent)
(declare-const read       NormContent) (declare-const museum-api Target)
(declare-const p1         Rule)  (declare-const e1        Event)
(declare-const rho1       Relator)
(declare-const f2         Rule)
(assert (perm p1)) (assert (strong p1))
(assert (aee p1 bibliothek)) (assert (aer p1 museen))
(assert (act p1 read))       (assert (tgt p1 museum-api))
(assert (activates e1 p1)) (assert (founds e1 rho1 p1))
; museen attempts prohibition — Disability created by Ax5.2 blocks it
(assert (proh f2))
(assert (aee f2 bibliothek)) (assert (aer f2 museen))
(assert (act f2 read))       (assert (tgt f2 museum-api))
""",
        "smt2_conjecture": None,
    },

    # =========================================================================
    # GRND021 — Full A1-B1-B2-B3 violation-to-remedy chain
    # Difficulty: Hard
    # v1.5: ax_proh_relator_basic -> ax_proh_relator_conduct
    #        SMT2: Action -> NormContent; TTL: angle brackets removed
    # Abstract constants:
    #   marketplace  = drk:MusicMarketplaceAG (assignee)
    #   philharmonie = drk:PhilharmonieBerlin (assigner)
    # =========================================================================
    {
        "id": "GRND021-remedy-chain", "subdir": "Discriminating",
        "name": "Full remedy chain: violation triggers Power-licensed institutional act",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_proh_relator_conduct",
            "ax_proh_relator_remedy",
            "ax_B1", "ax_B2", "ax_B3",
            "ax_A1", "ax_A2", "ax_A3",
        ],
        "description": """\
% proh(f1) + has_rem(f1) + activates(e1,f1) + does(marketplace,distrib,concert_ds).
% Ax5.4 (founds_rem): creates rho_R with Power(philharmonie,decl(distrib),concert_ds)
%                     and Subjection(marketplace,decl(distrib),concert_ds).
% B1: does(marketplace,...) => NormStateChange.
% A1: NormStateChange => exists InstEvent(ev) triggers it.
% B2: Power(pw) partOf rho_R & founds_rem(e1,rho_R,f1) => about_event(pw,e1).
% B3: Subjection(s,...) => about_event(s,e1).
% A2: InstEvent => competent agent.
% A3: competence => Power+Subjection pair about ev.
% Conjecture: exists pw, s, ev such that about_event(pw,ev) and about_event(s,ev).
% Abstract constants: marketplace=drk:MusicMarketplaceAG,
%   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
%   concert_ds=drk:ConcertRecordingDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Full violation-to-remedy chain.
# drk:MusicMarketplaceAG violates the prohibition.
# drk:PhilharmonieBerlin holds Power to declare violation.
# The chain A1->A2->A3 grounds the institutional authority.
drk:policy-remedy-chain a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:MusicMarketplaceAG ;
        odrl:assigner drk:PhilharmonieBerlin ;
        odrl:action   odrl:distribute ;
        odrl:target   drk:ConcertRecordingDataset ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action odrl:compensate ] ] .
drk:ConcertRecordingDataset a dcat:Dataset .
drk:PhilharmonieBerlin      a schema:Organization .
drk:MusicMarketplaceAG      a schema:Organization .
# Abstract constants: marketplace=drk:MusicMarketplaceAG,
#   philharmonie=drk:PhilharmonieBerlin""",
        "fof_extra_decls": """\
fof(agent_marketplace,  axiom, agent(marketplace)).
fof(agent_philharmonie, axiom, agent(philharmonie)).
fof(action_distrib,     axiom, action(distrib)).
fof(target_concert,     axiom, target(concert_ds)).
fof(rule_f1,            axiom, rule(f1)).
fof(event_e1,           axiom, event(e1)).
fof(relator_rho1,       axiom, legal_relator(rho1)).
fof(proh_f1,            axiom, proh(f1)).
fof(rem_f1,             axiom, has_rem(f1)).
fof(aee_f1,             axiom, aee(f1, marketplace)).
fof(aer_f1,             axiom, aer(f1, philharmonie)).
fof(act_f1,             axiom, act(f1, distrib)).
fof(tgt_f1,             axiom, tgt(f1, concert_ds)).
fof(act_e1_f1,          axiom, activates(e1, f1)).
fof(founds_e1_rho1,     axiom, founds(e1, rho1, f1)).
fof(marketplace_does,   axiom, does(marketplace, distrib, concert_ds)).
""",
        "fof_conjecture": """\
? [RhoR, Pw, S] :
  ( founds_rem(e1, RhoR, f1)
  & power(Pw)     & bearer(Pw, philharmonie) & cnt(Pw, decl(distrib), concert_ds) & part_of(Pw, RhoR) & about_event(Pw, e1)
  & subjection(S) & bearer(S,  marketplace)  & cnt(S,  decl(distrib), concert_ds) & part_of(S,  RhoR) & about_event(S,  e1) )""",
        "smt2_extra_decls": """\
(declare-const marketplace  Agent) (declare-const philharmonie Agent)
(declare-const distrib      NormContent) (declare-const concert-ds Target)
(declare-const f1           Rule)  (declare-const e1           Event)
(declare-const rho1         Relator)
(assert (proh f1)) (assert (has-rem f1))
(assert (aee f1 marketplace)) (assert (aer f1 philharmonie))
(assert (act f1 distrib))     (assert (tgt f1 concert-ds))
(assert (activates e1 f1)) (assert (founds e1 rho1 f1))
(assert (does marketplace distrib concert-ds))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho-r Relator) (pw Position) (s Position))
    (and (founds-rem e1 rho-r f1)
         (power pw)     (bearer pw philharmonie) (cnt pw (decl distrib) concert-ds) (part-of pw rho-r) (about-event pw e1)
         (subjection s) (bearer s  marketplace)  (cnt s  (decl distrib) concert-ds) (part-of s  rho-r) (about-event s  e1)))))""",
    },

    # =========================================================================
    # GRND022 — Correlativity blocks non-unique NoRight
    # Difficulty: Medium
    # fof_axioms already correct; TTL angle brackets removed
    # =========================================================================
    {
        "id": "GRND022-corr-nonunique", "subdir": "Discriminating",
        "name": "Correlativity violated: two NoRight positions in same relator",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_correlativity_permission"],
        "description": """\
% odrl_rel(rho1) + Permission(l) partOf rho1.
% Two distinct no_right positions n1 != n2 both partOf rho1 with same content.
% ax_correlativity_permission requires unique NoRight => contradiction.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# Correlativity uniqueness test:
# A relator cannot contain two distinct NoRight positions
# with the same content — correlativity requires exactly one.""",
        "fof_extra_decls": """\
fof(pos_l,         axiom, position(l)).
fof(pos_n1,        axiom, position(n1)).
fof(pos_n2,        axiom, position(n2)).
fof(rel_rho1,      axiom, legal_relator(rho1)).
fof(odrl_rho1,     axiom, odrl_rel(rho1)).
fof(permission_l,  axiom, permission(l)).
fof(no_right_n1,   axiom, no_right(n1)).
fof(no_right_n2,   axiom, no_right(n2)).
fof(partof_l,      axiom, part_of(l,  rho1)).
fof(partof_n1,     axiom, part_of(n1, rho1)).
fof(partof_n2,     axiom, part_of(n2, rho1)).
fof(cnt_l,         axiom, cnt(l,  some_action, some_target)).
fof(cnt_n1,        axiom, cnt(n1, some_action, some_target)).
fof(cnt_n2,        axiom, cnt(n2, some_action, some_target)).
fof(action_typed,  axiom, action(some_action)).
fof(target_typed,  axiom, target(some_target)).
fof(n1_neq_n2,     axiom, n1 != n2).
fof(perm_l_unique, axiom,
    ! [L2] : ( ( permission(L2) & part_of(L2, rho1) & cnt(L2, some_action, some_target) )
              => L2 = l )).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const l           Position)
(declare-const n1          Position)
(declare-const n2          Position)
(declare-const rho1        Relator)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (permission l))
(assert (no-right n1)) (assert (no-right n2))
(assert (part-of l  rho1)) (assert (part-of n1 rho1)) (assert (part-of n2 rho1))
(assert (cnt l  some-action some-target))
(assert (cnt n1 some-action some-target))
(assert (cnt n2 some-action some-target))
(assert (odrl-rel rho1))
(assert (not (= n1 n2)))
; l is the unique permission in rho1 — triggers exists-unique antecedent
(assert (forall ((l2 Position))
  (=> (and (permission l2) (part-of l2 rho1) (cnt l2 some-action some-target))
      (= l2 l))))
""",
        "smt2_conjecture": None,
    },

    # =========================================================================
    # GRND023 — Policy issuance: issue/1 injectivity
    # Difficulty: Hard
    # v1.5: fof_axioms: [] — issue/1 is in Layer0 (included automatically);
    #        ax_obl_relator was unrelated and caused confusion
    #        TTL: angle brackets removed
    # =========================================================================
    {
        "id": "GRND023-policy-issuance", "subdir": "Discriminating",
        "name": "Policy issuance: issue/1 injectivity (distinct rules => distinct acts)",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [],  # issue/1 injectivity is in Layer0 (GRND000-0.ax)
        "description": """\
% Two distinct rules pi1 != pi2.
% Layer0 issue_injective: issue(A)=issue(B) => A=B.
% Conjecture (FOF): issue(pi1) != issue(pi2).
% SMT2 negated: (assert (= (issue pi1) (issue pi2))) with pi1 != pi2.
% Injectivity forces pi1=pi2 => contradiction with distinctness.
% NOTE: issue/1 is a PAAR benchmark function; not used in GRND001-024 paper problems.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Policy issuance authority test.
# Two distinct policies — their issue() acts must be distinct.
drk:policy-issuance-1 a odrl:Agreement ;
    odrl:obligation [ a odrl:Duty ;
        odrl:assignee drk:PhilharmonieBerlin ;
        odrl:assigner drk:FraunhoferFIT ;
        odrl:action   odrl:distribute ;
        odrl:target   drk:ConcertRecordingDataset ] .
drk:policy-issuance-2 a odrl:Agreement ;
    odrl:obligation [ a odrl:Duty ;
        odrl:assignee drk:StaatlicheMuseenBerlin ;
        odrl:assigner drk:FraunhoferFIT ;
        odrl:action   odrl:read ;
        odrl:target   drk:MuseumCollectionAPI ] .
drk:ConcertRecordingDataset a dcat:Dataset .
drk:MuseumCollectionAPI     a dcat:DataService .
drk:PhilharmonieBerlin      a schema:Organization .
drk:StaatlicheMuseenBerlin  a schema:Organization .
drk:FraunhoferFIT           a schema:Organization .""",
        "fof_extra_decls": """\
fof(rule_pi1,     axiom, rule(pi1)).
fof(rule_pi2,     axiom, rule(pi2)).
fof(pi1_neq_pi2,  axiom, pi1 != pi2).
""",
        "fof_conjecture": "issue(pi1) != issue(pi2)",
        "smt2_extra_decls": """\
(declare-const pi1  Rule)
(declare-const pi2  Rule)
; Distinctness of the two rules
(assert (not (= pi1 pi2)))
; Negated conjecture: assume issue(pi1) = issue(pi2) — should be unsat
; via Layer0 injectivity: issue(A)=issue(B) => A=B, contradicting pi1!=pi2
""",
        "smt2_conjecture": """\
(assert (= (issue pi1) (issue pi2)))""",
    },

    # =========================================================================
    # GRND024 — obl + proh on same target = Satisfiable (no direct conflict)
    # Difficulty: Medium
    # v1.5: ax_proh_relator_basic -> ax_proh_relator_conduct
    #        ax_cross_relator_consistency -> ax_cross_relator
    #        SMT2: Action -> NormContent; TTL: angle brackets removed
    # Abstract constants:
    #   bibliothek = drk:UniversitaetsbibliothekMuenchen (assignee)
    #   ensemble   = drk:BerlinerEnsemble (assigner obl)
    #   museen     = drk:StaatlicheMuseenBerlin (assigner proh)
    # =========================================================================
    {
        "id": "GRND024-obl-proh-coexist", "subdir": "Discriminating",
        "name": "Obligation + Prohibition coexist: Duty(a) vs Duty(rfr(a)) distinct",
        "status_fof": "Satisfiable",
        "status_smt": "sat",
        "fof_axioms": [
            "ax_obl_relator",
            "ax_proh_relator_conduct",
            "ax_cross_relator",
        ],
        "description": """\
% obl(obl1) activated at e1: creates Duty(bibliothek, read, theater_ds).
% proh(f1)  activated at e2: creates Duty(bibliothek, rfr(read), theater_ds).
% ax_cross_relator fires on Permission+Duty(rfr), NOT Duty(a)+Duty(rfr(a)).
% Status: Satisfiable — the two duties coexist (different content).
% Discriminating: shows obl and proh do NOT directly conflict in the grounding.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   ensemble=drk:BerlinerEnsemble, museen=drk:StaatlicheMuseenBerlin,
%   read=odrl:read, theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Obligation to read AND prohibition on reading coexist
# because their duties have different content: read vs rfr(read).
# This demonstrates obl+proh do NOT directly conflict in the grounding.
drk:policy-obl-proh a odrl:Agreement ;
    odrl:obligation  [ a odrl:Duty ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:BerlinerEnsemble ;
        odrl:action   odrl:read ;
        odrl:target   drk:TheaterShowtimeDataset ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:TheaterShowtimeDataset ] .
drk:TheaterShowtimeDataset          a dcat:Dataset .
drk:BerlinerEnsemble                a schema:Organization .
drk:StaatlicheMuseenBerlin          a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   ensemble=drk:BerlinerEnsemble, museen=drk:StaatlicheMuseenBerlin""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_ensemble,   axiom, agent(ensemble)).
fof(agent_museen,     axiom, agent(museen)).
fof(action_read,      axiom, action(read)).
fof(target_theater,   axiom, target(theater_ds)).
% Obligation: bibliothek must read theater_ds
fof(rule_obl1,        axiom, rule(obl1)).
fof(event_e1,         axiom, event(e1)).
fof(obl_obl1,         axiom, obl(obl1)).
fof(aee_obl1,         axiom, aee(obl1, bibliothek)).
fof(aer_obl1,         axiom, aer(obl1, ensemble)).
fof(act_obl1,         axiom, act(obl1, read)).
fof(tgt_obl1,         axiom, tgt(obl1, theater_ds)).
fof(act_e1_obl1,      axiom, activates(e1, obl1)).
% Prohibition: bibliothek must not read theater_ds
fof(rule_f1,          axiom, rule(f1)).
fof(event_e2,         axiom, event(e2)).
fof(proh_f1,          axiom, proh(f1)).
fof(aee_f1,           axiom, aee(f1, bibliothek)).
fof(aer_f1,           axiom, aer(f1, museen)).
fof(act_f1,           axiom, act(f1, read)).
fof(tgt_f1,           axiom, tgt(f1, theater_ds)).
fof(act_e2_f1,        axiom, activates(e2, f1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const bibliothek Agent)
(declare-const ensemble   Agent) (declare-const museen    Agent)
(declare-const read       NormContent) (declare-const theater-ds Target)
(declare-const obl1       Rule)  (declare-const e1        Event)
(declare-const f1         Rule)  (declare-const e2        Event)
; Obligation
(assert (obl obl1))
(assert (aee obl1 bibliothek)) (assert (aer obl1 ensemble))
(assert (act obl1 read))       (assert (tgt obl1 theater-ds))
(assert (activates e1 obl1))
; Prohibition
(assert (proh f1))
(assert (aee f1 bibliothek)) (assert (aer f1 museen))
(assert (act f1 read))       (assert (tgt f1 theater-ds))
(assert (activates e2 f1))
""",
        "smt2_conjecture": None,
    },
]