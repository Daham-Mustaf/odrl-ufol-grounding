"""
problem_data_ext.py
===================
Extension problems for the FOIS 2026 deontic grounding benchmark.
Covers axioms not yet tested in problem_data.py:
  GRND010  Ax5.2  — strong perm creates Immunity + Disability
  GRND011  Ax5.6  — obl creates Duty + Right
  GRND012  Ax5.8  — correlativity duty <-> right
  GRND013  Ax5.8  — correlativity power <-> subjection
  GRND014  Ax5.8  — correlativity immunity <-> disability
  GRND015  Ax5.5a — unique founding
  GRND016  Ax5.9  — conflict detection within relator
  GRND017  A1+A2+A3+B1 — violation triggers institutional event chain
  GRND018  B2+B3  — Power/Subjection about-event link
Usage — merge with main PROBLEMS list in gen_foundation_problems.py:
    from problem_data import PROBLEMS
    from problem_data_ext import PROBLEMS_EXT
    ALL_PROBLEMS = PROBLEMS + PROBLEMS_EXT
Or run standalone:
    uv run Generators/DeonticOntology/gen_foundation_problems.py \\
      --out-dir Problems/DeonticOntology --ext
All required keys are present in axiom_data.FOF_AXIOM_DICT v1.5.
Fix history:
  Bug 1 — GRND010: old Ax5.2 added Immunity/Disability into rho1 (rho_P).
           Fixed Ax5.2 uses founds_imm existentially for fresh rho_I.
           rho1 assertions removed; conjecture uses ? [RhoI] founds_imm.
  Bug 2 — GRND011: claim -> right in fof_conjecture and smt2_conjecture.
  Bug 3 — GRND012: claim -> right in fof_conjecture and smt2_conjecture.
  Bug 4 — GRND016: liberty -> permission in fof_extra_decls and
           smt2_extra_decls; cnt-f -> cnt in smt2_extra_decls.
  Bug 5 — GRND018: Power/Subjection must be in fresh rho_R via founds_rem
           (not rho1 which founds rho_F). rho1 assertions removed;
           conjecture and B2/B3 use founds_rem + existential rho_R.
  v1.5  — GRND010: ax_perm_relator_basic -> ax_perm_relator_weak (KeyError fix)
         — GRND016: ax_conflict_detection -> ax_conflict (KeyError fix)
         — GRND017: ax_proh_relator_basic -> ax_proh_relator_conduct (KeyError fix)
         — GRND017: conjecture strengthened to verify specific Power from
                    violation chain via founds_rem (was too weak)
         — TTL: angle brackets removed from drk:-prefixed terms throughout
                (were being parsed as relative IRIs, not prefix expansions)
  NormContent — gen_layer0_signature.py replaced Action/Forbearance with a
           unified NormContent sort. All SMT2 (declare-const X Action) updated
           to (declare-const X NormContent). some-action :: NormContent.
"""

PROBLEMS_EXT = [
    # =========================================================================
    # GRND010 — Ax5.2: Strong permission creates Immunity + Disability
    # Bug 1: Immunity/Disability must be in fresh rho_I via founds_imm.
    #        rho1 (rho_P) assertions removed; conjecture uses ? [RhoI].
    # v1.5:  ax_perm_relator_basic -> ax_perm_relator_weak
    # =========================================================================
    {
        "id": "GRND010-strong-perm", "subdir": "Entailment",
        "name": "Strong permission creates Immunity and Disability",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_perm_relator_weak", "ax_perm_relator_strong"],
        "description": """\
% perm(p1) + strong(p1) + activates(e1,p1).
% Ax5.2 existentially founds rho_I via founds_imm.
% Entails Immunity(bibliothek,read,museum_api) and Disability(museen,read,museum_api)
% in the fresh immunity relator rho_I.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   museen=drk:StaatlicheMuseenBerlin, read=odrl:read,
%   museum_api=drk:MuseumCollectionAPI""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# strong(p1) asserted by profile extension (not ODRL 2.2 alone).
drk:policy-strong-read a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:MuseumCollectionAPI ] .
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
fof(perm_p1,          axiom, perm(p1)).
fof(strong_p1,        axiom, strong(p1)).
fof(aee_p1,           axiom, aee(p1, bibliothek)).
fof(aer_p1,           axiom, aer(p1, museen)).
fof(act_p1,           axiom, act(p1, read)).
fof(tgt_p1,           axiom, tgt(p1, museum_api)).
fof(act_e1_p1,        axiom, activates(e1, p1)).
""",
        "fof_conjecture": """\
? [RhoI, Im, Db] :
  ( founds_imm(e1, RhoI, p1)
  & immunity(Im)   & bearer(Im, bibliothek) & cnt(Im, read, museum_api) & part_of(Im, RhoI)
  & disability(Db) & bearer(Db, museen)     & cnt(Db, read, museum_api) & part_of(Db, RhoI) )""",
        "smt2_extra_decls": """\
(declare-const bibliothek Agent) (declare-const museen    Agent)
(declare-const read       NormContent) (declare-const museum-api Target)
(declare-const p1         Rule)  (declare-const e1        Event)
(assert (perm p1)) (assert (strong p1))
(assert (aee p1 bibliothek)) (assert (aer p1 museen))
(assert (act p1 read))       (assert (tgt p1 museum-api))
(assert (activates e1 p1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho-i Relator) (im Position) (db Position))
    (and (founds-imm e1 rho-i p1)
         (immunity im)   (bearer im bibliothek) (cnt im read museum-api) (part-of im rho-i)
         (disability db) (bearer db museen)     (cnt db read museum-api) (part-of db rho-i)))))""",
    },

    # =========================================================================
    # GRND011 — Ax5.5: Obligation creates Duty + Right
    # =========================================================================
    {
        "id": "GRND011-obl-relator", "subdir": "Entailment",
        "name": "Obligation creates Duty and Right",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_obl_relator"],
        "description": """\
% obl(obl1) activated by e1 entails Duty(bibliothek,read,play_ds)
% and Right(ensemble,read,play_ds).
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   ensemble=drk:BerlinerEnsemble, read=odrl:read,
%   play_ds=drk:PlayProductionMetadataDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-obl-read a odrl:Agreement ;
    odrl:obligation [ a odrl:Duty ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:BerlinerEnsemble ;
        odrl:action   odrl:read ;
        odrl:target   drk:PlayProductionMetadataDataset ] .
drk:PlayProductionMetadataDataset   a dcat:Dataset .
drk:BerlinerEnsemble                a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   ensemble=drk:BerlinerEnsemble, read=odrl:read,
#   play_ds=drk:PlayProductionMetadataDataset""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_ensemble,   axiom, agent(ensemble)).
fof(action_read,      axiom, action(read)).
fof(target_play,      axiom, target(play_ds)).
fof(rule_obl1,        axiom, rule(obl1)).
fof(event_e1,         axiom, event(e1)).
fof(obl_obl1,         axiom, obl(obl1)).
fof(aee_obl1,         axiom, aee(obl1, bibliothek)).
fof(aer_obl1,         axiom, aer(obl1, ensemble)).
fof(act_obl1,         axiom, act(obl1, read)).
fof(tgt_obl1,         axiom, tgt(obl1, play_ds)).
fof(act_e1_obl1,      axiom, activates(e1, obl1)).
""",
        "fof_conjecture": """\
? [Rho, Du, C] :
  ( founds(e1, Rho, obl1)
  & duty(Du)  & bearer(Du, bibliothek) & cnt(Du, read, play_ds) & part_of(Du, Rho)
  & right(C)  & bearer(C,  ensemble)   & cnt(C,  read, play_ds) & part_of(C,  Rho) )""",
        "smt2_extra_decls": """\
(declare-const bibliothek Agent) (declare-const ensemble  Agent)
(declare-const read       NormContent) (declare-const play-ds Target)
(declare-const obl1       Rule)  (declare-const e1       Event)
(assert (obl obl1))
(assert (aee obl1 bibliothek)) (assert (aer obl1 ensemble))
(assert (act obl1 read))       (assert (tgt obl1 play-ds))
(assert (activates e1 obl1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho Relator) (du Position) (c Position))
    (and (founds e1 rho obl1)
         (duty du) (bearer du bibliothek) (cnt du read play-ds) (part-of du rho)
         (right c) (bearer c  ensemble)   (cnt c  read play-ds) (part-of c  rho)))))""",
    },

    # =========================================================================
    # GRND012 — Ax5.8: Correlativity duty <-> right
    # =========================================================================
    {
        "id": "GRND012-corr-duty", "subdir": "Entailment",
        "name": "Correlativity: Duty implies unique Right in relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_correlativity_duty"],
        "description": """\
% odrl_rel(rho1), Duty(d) partOf rho1 => exists unique c. Right(c) partOf rho1.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# Correlativity: every Duty in an ODRL relator has a unique correlative Right.
# Tested on drk:TheaterShowtimeDataset prohibition relator.""",
        "fof_extra_decls": """\
fof(pos_d,             axiom, position(d)).
fof(rel_rho1,          axiom, legal_relator(rho1)).
fof(odrl_rho1,         axiom, odrl_rel(rho1)).
fof(duty_d,            axiom, duty(d)).
fof(partof_d,          axiom, part_of(d, rho1)).
fof(cnt_d,             axiom, cnt(d, some_action, some_target)).
fof(some_action_typed, axiom, action(some_action)).
fof(some_target_typed, axiom, target(some_target)).
fof(duty_d_unique,     axiom,
    ! [D2] : ( ( duty(D2) & part_of(D2, rho1) & cnt(D2, some_action, some_target) )
              => D2 = d )).
""",
        "fof_conjecture": """\
? [C] : ( right(C) & part_of(C, rho1) & cnt(C, some_action, some_target)
        & ! [K] : ( ( right(K) & part_of(K, rho1)
                    & cnt(K, some_action, some_target) )
                  => K = C ) )""",
        "smt2_extra_decls": """\
(declare-const d           Position)
(declare-const rho1        Relator)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (duty d)) (assert (part-of d rho1))
(assert (cnt d some-action some-target))
(assert (odrl-rel rho1))
; d is the unique duty in rho1 — triggers exists-unique antecedent
(assert (forall ((d2 Position))
  (=> (and (duty d2) (part-of d2 rho1) (cnt d2 some-action some-target))
      (= d2 d))))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((c Position))
    (and (right c) (part-of c rho1) (cnt c some-action some-target)
         (forall ((k Position))
           (=> (and (right k) (part-of k rho1)
                    (cnt k some-action some-target))
               (= k c)))))))""",
    },

    # =========================================================================
    # GRND013 — Ax5.8: Correlativity power <-> subjection
    # =========================================================================
    {
        "id": "GRND013-corr-power", "subdir": "Entailment",
        "name": "Correlativity: Power implies unique Subjection in relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_correlativity_power"],
        "description": """\
% odrl_rel(rho1), Power(pw) partOf rho1 => exists unique s. Subjection(s) partOf rho1.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# Correlativity: every Power in an ODRL relator has a unique correlative Subjection.
# Grounded in a prohibition-with-remedy relator over drk:ConcertRecordingDataset.""",
        "fof_extra_decls": """\
fof(pos_pw,            axiom, position(pw)).
fof(rel_rho1,          axiom, legal_relator(rho1)).
fof(odrl_rho1,         axiom, odrl_rel(rho1)).
fof(power_pw,          axiom, power(pw)).
fof(partof_pw,         axiom, part_of(pw, rho1)).
fof(cnt_pw,            axiom, cnt(pw, some_action, some_target)).
fof(some_action_typed, axiom, action(some_action)).
fof(some_target_typed, axiom, target(some_target)).
fof(power_pw_unique,   axiom,
    ! [Pw2] : ( ( power(Pw2) & part_of(Pw2, rho1) & cnt(Pw2, some_action, some_target) )
               => Pw2 = pw )).
""",
        "fof_conjecture": """\
? [S] : ( subjection(S) & part_of(S, rho1) & cnt(S, some_action, some_target)
        & ! [S2] : ( ( subjection(S2) & part_of(S2, rho1)
                     & cnt(S2, some_action, some_target) )
                   => S2 = S ) )""",
        "smt2_extra_decls": """\
(declare-const pw          Position)
(declare-const rho1        Relator)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (power pw)) (assert (part-of pw rho1))
(assert (cnt pw some-action some-target))
(assert (odrl-rel rho1))
; pw is the unique power in rho1 — triggers exists-unique antecedent
(assert (forall ((pw2 Position))
  (=> (and (power pw2) (part-of pw2 rho1) (cnt pw2 some-action some-target))
      (= pw2 pw))))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((s Position))
    (and (subjection s) (part-of s rho1) (cnt s some-action some-target)
         (forall ((s2 Position))
           (=> (and (subjection s2) (part-of s2 rho1)
                    (cnt s2 some-action some-target))
               (= s2 s)))))))""",
    },

    # =========================================================================
    # GRND014 — Ax5.8: Correlativity immunity <-> disability
    # =========================================================================
    {
        "id": "GRND014-corr-immunity", "subdir": "Entailment",
        "name": "Correlativity: Immunity implies unique Disability in relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_correlativity_immunity"],
        "description": """\
% odrl_rel(rho1), Immunity(im) partOf rho1 => exists unique db. Disability(db) partOf rho1.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# Correlativity: every Immunity in an ODRL relator has a unique correlative Disability.
# Grounded in a strong-permission relator over drk:MuseumCollectionAPI.""",
        "fof_extra_decls": """\
fof(pos_im,            axiom, position(im)).
fof(rel_rho1,          axiom, legal_relator(rho1)).
fof(odrl_rho1,         axiom, odrl_rel(rho1)).
fof(immun_im,          axiom, immunity(im)).
fof(partof_im,         axiom, part_of(im, rho1)).
fof(cnt_im,            axiom, cnt(im, some_action, some_target)).
fof(some_action_typed, axiom, action(some_action)).
fof(some_target_typed, axiom, target(some_target)).
fof(immun_im_unique,   axiom,
    ! [Im2] : ( ( immunity(Im2) & part_of(Im2, rho1) & cnt(Im2, some_action, some_target) )
               => Im2 = im )).
""",
        "fof_conjecture": """\
? [Db] : ( disability(Db) & part_of(Db, rho1) & cnt(Db, some_action, some_target)
         & ! [Db2] : ( ( disability(Db2) & part_of(Db2, rho1)
                       & cnt(Db2, some_action, some_target) )
                     => Db2 = Db ) )""",
        "smt2_extra_decls": """\
(declare-const im          Position)
(declare-const rho1        Relator)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (immunity im)) (assert (part-of im rho1))
(assert (cnt im some-action some-target))
(assert (odrl-rel rho1))
; im is the unique immunity in rho1 — triggers exists-unique antecedent
(assert (forall ((im2 Position))
  (=> (and (immunity im2) (part-of im2 rho1) (cnt im2 some-action some-target))
      (= im2 im))))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((db Position))
    (and (disability db) (part-of db rho1) (cnt db some-action some-target)
         (forall ((db2 Position))
           (=> (and (disability db2) (part-of db2 rho1)
                    (cnt db2 some-action some-target))
               (= db2 db)))))))""",
    },

    # =========================================================================
    # GRND015 — Ax5.6a: Unique founding
    # =========================================================================
    {
        "id": "GRND015-unique-founding", "subdir": "Entailment",
        "name": "Unique founding: same event+rule founds at most one relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_unique_founding"],
        "description": """\
% founds(e1,rho1,p1) and founds(e1,rho2,p1) => rho1 = rho2.
% UFO axiom a77 — relator individuated by rule-event pair.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
# Uniqueness: activating the same permission twice at the same event
# cannot produce two distinct relators.""",
        "fof_extra_decls": """\
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(relator_rho2, axiom, legal_relator(rho2)).
fof(founds1,      axiom, founds(e1, rho1, p1)).
fof(founds2,      axiom, founds(e1, rho2, p1)).
""",
        "fof_conjecture": "rho1 = rho2",
        "smt2_extra_decls": """\
(declare-const p1   Rule)
(declare-const e1   Event)
(declare-const rho1 Relator)
(declare-const rho2 Relator)
(assert (founds e1 rho1 p1))
(assert (founds e1 rho2 p1))
""",
        "smt2_conjecture": """\
(assert (not (= rho1 rho2)))""",
    },

    # =========================================================================
    # GRND016 — Corollary ax:conflict: Conflict detection within a single relator
    # Bug 4: liberty -> permission throughout
    # v1.5:  ax_conflict_detection -> ax_conflict
    # =========================================================================
    {
        "id": "GRND016-conflict-relator", "subdir": "Entailment",
        "name": "Conflict detection: Permission and Duty in same relator",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_conflict"],
        "description": """\
% Permission(l) and Duty(d) both partOf rho1, same bearer, same content.
% Corollary ax:conflict derives False (within-relator check).
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   read=odrl:read, theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# Within-relator conflict: Permission and Duty-to-refrain
# co-borne by drk:UniversitaetsbibliothekMuenchen in the same relator.
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   read=odrl:read, theater_ds=drk:TheaterShowtimeDataset""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(action_read,      axiom, action(read)).
fof(target_theater,   axiom, target(theater_ds)).
fof(pos_l,            axiom, position(l)).
fof(pos_d,            axiom, position(d)).
fof(rel_rho1,         axiom, legal_relator(rho1)).
fof(permission_l,     axiom, permission(l)).
fof(duty_d,           axiom, duty(d)).
fof(bearer_l,         axiom, bearer(l, bibliothek)).
fof(bearer_d,         axiom, bearer(d, bibliothek)).
fof(cnt_l,            axiom, cnt(l, read, theater_ds)).
fof(cnt_d,            axiom, cnt(d, rfr(read), theater_ds)).
fof(partof_l,         axiom, part_of(l, rho1)).
fof(partof_d,         axiom, part_of(d, rho1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const bibliothek Agent)
(declare-const read       NormContent) (declare-const theater-ds Target)
(declare-const l          Position) (declare-const d          Position)
(declare-const rho1       Relator)
(assert (permission l)) (assert (duty d))
(assert (bearer l bibliothek)) (assert (bearer d bibliothek))
(assert (cnt l read theater-ds))  (assert (cnt d (rfr read) theater-ds))
(assert (part-of l rho1)) (assert (part-of d rho1))
""",
        "smt2_conjecture": None,
    },

    # =========================================================================
    # GRND017 — A1+A2+A3+B1: Violation triggers institutional event chain
    # v1.5:  ax_proh_relator_basic -> ax_proh_relator_conduct
    #        conjecture strengthened to verify specific Power from violation
    #        chain via founds_rem (was too weak — matched any Power in model)
    # NormContent fix: distribute :: NormContent
    # Abstract constants:
    #   marketplace  = drk:MusicMarketplaceAG (assignee)
    #   philharmonie = drk:PhilharmonieBerlin (assigner)
    # =========================================================================
    {
        "id": "GRND017-violation-chain", "subdir": "Entailment",
        "name": "A1-A3+B1: violation triggers norm state change requiring Power",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_proh_relator_conduct",
            "ax_proh_relator_remedy",
            "ax_A1", "ax_A2", "ax_A3", "ax_B1",
            "ax_B2", "ax_B3",
        ],
        "description": """\
% proh(f1) + has_rem(f1) + does(marketplace,distrib,concert_ds).
% B1: violation => NormStateChange.
% A1: NormStateChange => InstEvent.
% A2: InstEvent => competent agent.
% A3: competence => Power+Subjection pair.
% Conjecture: Power+Subjection in fresh rho_R founded via founds_rem at e1.
% Abstract constants: marketplace=drk:MusicMarketplaceAG,
%   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
%   concert_ds=drk:ConcertRecordingDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-violation-chain a odrl:Agreement ;
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
# drk:MusicMarketplaceAG violates the prohibition.
# The violation triggers a normative state change (B1),
# which requires an institutional event (A1),
# which requires a competent agent (A2),
# whose competence is a Power-Subjection pair (A3).
# Abstract constants: marketplace=drk:MusicMarketplaceAG,
#   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
#   concert_ds=drk:ConcertRecordingDataset""",
        "fof_extra_decls": """\
fof(agent_marketplace,  axiom, agent(marketplace)).
fof(agent_philharmonie, axiom, agent(philharmonie)).
fof(action_distrib,     axiom, action(distrib)).
fof(target_concert,     axiom, target(concert_ds)).
fof(rule_f1,            axiom, rule(f1)).
fof(event_e1,           axiom, event(e1)).
fof(proh_f1,            axiom, proh(f1)).
fof(rem_f1,             axiom, has_rem(f1)).
fof(aee_f1,             axiom, aee(f1, marketplace)).
fof(aer_f1,             axiom, aer(f1, philharmonie)).
fof(act_f1,             axiom, act(f1, distrib)).
fof(tgt_f1,             axiom, tgt(f1, concert_ds)).
fof(act_e1_f1,          axiom, activates(e1, f1)).
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
(assert (proh f1)) (assert (has-rem f1))
(assert (aee f1 marketplace)) (assert (aer f1 philharmonie))
(assert (act f1 distrib))     (assert (tgt f1 concert-ds))
(assert (activates e1 f1))
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
    # GRND018 — B2+B3: Power/Subjection about-event link
    # Bug 5: Power/Subjection in rho_R (founds_rem), not rho1 (founds).
    #        rho1 assertions removed; conjecture uses founds_rem + ? [RhoR].
    # Abstract constants:
    #   marketplace  = drk:MusicMarketplaceAG (assignee)
    #   philharmonie = drk:PhilharmonieBerlin (assigner)
    # =========================================================================
    {
        "id": "GRND018-about-event", "subdir": "Entailment",
        "name": "B2+B3: Power and Subjection in relator concern founding event",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_proh_relator_remedy",
            "ax_B2", "ax_B3",
        ],
        "description": """\
% proh(f1) + has_rem(f1) + activates(e1,f1).
% Ax5.4 existentially founds rho_R via founds_rem.
% B2: Power in rho_R => about_event(pw, e1).
% B3: Subjection in rho_R => about_event(s, e1).
% Abstract constants: marketplace=drk:MusicMarketplaceAG,
%   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
%   concert_ds=drk:ConcertRecordingDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-about-event a odrl:Agreement ;
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
# The Power and Subjection are in rho_R (founded via founds_rem at activation).
# B2/B3 link them to the founding event e1.
# Abstract constants: marketplace=drk:MusicMarketplaceAG,
#   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
#   concert_ds=drk:ConcertRecordingDataset""",
        "fof_extra_decls": """\
fof(agent_marketplace,  axiom, agent(marketplace)).
fof(agent_philharmonie, axiom, agent(philharmonie)).
fof(action_distrib,     axiom, action(distrib)).
fof(target_concert,     axiom, target(concert_ds)).
fof(rule_f1,            axiom, rule(f1)).
fof(event_e1,           axiom, event(e1)).
fof(proh_f1,            axiom, proh(f1)).
fof(rem_f1,             axiom, has_rem(f1)).
fof(aee_f1,             axiom, aee(f1, marketplace)).
fof(aer_f1,             axiom, aer(f1, philharmonie)).
fof(act_f1,             axiom, act(f1, distrib)).
fof(tgt_f1,             axiom, tgt(f1, concert_ds)).
fof(act_e1_f1,          axiom, activates(e1, f1)).
""",
        "fof_conjecture": """\
? [RhoR, Pw, S] :
  ( founds_rem(e1, RhoR, f1)
  & power(Pw)     & bearer(Pw, philharmonie) & part_of(Pw, RhoR) & about_event(Pw, e1)
  & subjection(S) & bearer(S,  marketplace)  & part_of(S,  RhoR) & about_event(S,  e1) )""",
        "smt2_extra_decls": """\
(declare-const marketplace  Agent) (declare-const philharmonie Agent)
(declare-const distrib      NormContent) (declare-const concert-ds Target)
(declare-const f1           Rule)  (declare-const e1           Event)
(assert (proh f1)) (assert (has-rem f1))
(assert (aee f1 marketplace)) (assert (aer f1 philharmonie))
(assert (act f1 distrib))     (assert (tgt f1 concert-ds))
(assert (activates e1 f1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho-r Relator) (pw Position) (s Position))
    (and (founds-rem e1 rho-r f1)
         (power pw)     (bearer pw philharmonie) (part-of pw rho-r) (about-event pw e1)
         (subjection s) (bearer s  marketplace)  (part-of s  rho-r) (about-event s  e1)))))""",
    },
]