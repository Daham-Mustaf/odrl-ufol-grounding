"""
problem_data_coverage.py
========================
Coverage completion problems for the FOIS/PAAR 2026 benchmark.
Fills axiom gaps identified after the base+ext+hard audit:
  GRND025  ax_unique_founding_rem  — founds_rem uniqueness (relator)
  GRND026  ax_unique_founding_imm  — founds_imm uniqueness (relator)
  GRND027  ax_unique_event_rem     — founds_rem uniqueness (event)
  GRND028  ax_unique_event_imm     — founds_imm uniqueness (event)
  GRND029  ax_B2 alone             — Power about-event link in isolation
  GRND030  ax_B3 alone             — Subjection about-event link in isolation
  GRND031  ax_odrl_rel_is_rel      — Ax5.11 standalone entailment
  GRND032  ax_odrl_rel_typing_rem  — Ax5.7 rem variant standalone
  GRND033  ax_odrl_rel_typing_imm  — Ax5.7 imm variant standalone
  GRND034  ax_disability_block (positive) — strong perm creates Disability

Usage:
    from problem_data_coverage import PROBLEMS_COVERAGE
    # merge with other problem lists in gen_foundation_problems.py or standalone

All required keys are present in axiom_data.FOF_AXIOM_DICT v1.5.
"""

PROBLEMS_COVERAGE = [
    # =========================================================================
    # GRND025 — ax_unique_founding_rem: founds_rem uniqueness (relator side)
    # =========================================================================
    {
        "id": "GRND025-unique-founding-rem", "subdir": "Entailment",
        "name": "Unique founding rem: same event+rule founds at most one remedy relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_unique_founding_rem"],
        "description": """\
% founds_rem(e1,rho1,f1) and founds_rem(e1,rho2,f1) => rho1 = rho2.
% UFO uniqueness for remedy relator — mirrors GRND015 for founds_rem.""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Uniqueness: activating the same prohibition-with-remedy at the same event
# cannot produce two distinct remedy relators.""",
        "fof_extra_decls": """\
fof(rule_f1,      axiom, rule(f1)).
fof(event_e1,     axiom, event(e1)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(relator_rho2, axiom, legal_relator(rho2)).
fof(founds1,      axiom, founds_rem(e1, rho1, f1)).
fof(founds2,      axiom, founds_rem(e1, rho2, f1)).
""",
        "fof_conjecture": "rho1 = rho2",
        "smt2_extra_decls": """\
(declare-const f1   Rule)
(declare-const e1   Event)
(declare-const rho1 Relator)
(declare-const rho2 Relator)
(assert (founds-rem e1 rho1 f1))
(assert (founds-rem e1 rho2 f1))
""",
        "smt2_conjecture": "(assert (not (= rho1 rho2)))",
    },

    # =========================================================================
    # GRND026 — ax_unique_founding_imm: founds_imm uniqueness (relator side)
    # =========================================================================
    {
        "id": "GRND026-unique-founding-imm", "subdir": "Entailment",
        "name": "Unique founding imm: same event+rule founds at most one immunity relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_unique_founding_imm"],
        "description": """\
% founds_imm(e1,rho1,p1) and founds_imm(e1,rho2,p1) => rho1 = rho2.
% UFO uniqueness for immunity relator — mirrors GRND015 for founds_imm.""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Uniqueness: activating the same strong permission at the same event
# cannot produce two distinct immunity relators.""",
        "fof_extra_decls": """\
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(relator_rho2, axiom, legal_relator(rho2)).
fof(founds1,      axiom, founds_imm(e1, rho1, p1)).
fof(founds2,      axiom, founds_imm(e1, rho2, p1)).
""",
        "fof_conjecture": "rho1 = rho2",
        "smt2_extra_decls": """\
(declare-const p1   Rule)
(declare-const e1   Event)
(declare-const rho1 Relator)
(declare-const rho2 Relator)
(assert (founds-imm e1 rho1 p1))
(assert (founds-imm e1 rho2 p1))
""",
        "smt2_conjecture": "(assert (not (= rho1 rho2)))",
    },

    # =========================================================================
    # GRND027 — ax_unique_event_rem: founds_rem uniqueness (event side)
    # =========================================================================
    {
        "id": "GRND027-unique-event-rem", "subdir": "Entailment",
        "name": "Unique event rem: same relator+rule founded by at most one event",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_unique_event_rem"],
        "description": """\
% founds_rem(e1,rho1,f1) and founds_rem(e2,rho1,f1) => e1 = e2.
% UFO uniqueness (event side) for remedy relator.""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# A remedy relator is individuated by a unique founding event.""",
        "fof_extra_decls": """\
fof(rule_f1,      axiom, rule(f1)).
fof(event_e1,     axiom, event(e1)).
fof(event_e2,     axiom, event(e2)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(founds1,      axiom, founds_rem(e1, rho1, f1)).
fof(founds2,      axiom, founds_rem(e2, rho1, f1)).
""",
        "fof_conjecture": "e1 = e2",
        "smt2_extra_decls": """\
(declare-const f1   Rule)
(declare-const e1   Event)
(declare-const e2   Event)
(declare-const rho1 Relator)
(assert (founds-rem e1 rho1 f1))
(assert (founds-rem e2 rho1 f1))
""",
        "smt2_conjecture": "(assert (not (= e1 e2)))",
    },

    # =========================================================================
    # GRND028 — ax_unique_event_imm: founds_imm uniqueness (event side)
    # =========================================================================
    {
        "id": "GRND028-unique-event-imm", "subdir": "Entailment",
        "name": "Unique event imm: same relator+rule founded by at most one event",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_unique_event_imm"],
        "description": """\
% founds_imm(e1,rho1,p1) and founds_imm(e2,rho1,p1) => e1 = e2.
% UFO uniqueness (event side) for immunity relator.""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# An immunity relator is individuated by a unique founding event.""",
        "fof_extra_decls": """\
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(event_e2,     axiom, event(e2)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(founds1,      axiom, founds_imm(e1, rho1, p1)).
fof(founds2,      axiom, founds_imm(e2, rho1, p1)).
""",
        "fof_conjecture": "e1 = e2",
        "smt2_extra_decls": """\
(declare-const p1   Rule)
(declare-const e1   Event)
(declare-const e2   Event)
(declare-const rho1 Relator)
(assert (founds-imm e1 rho1 p1))
(assert (founds-imm e2 rho1 p1))
""",
        "smt2_conjecture": "(assert (not (= e1 e2)))",
    },

    # =========================================================================
    # GRND029 — ax_B2 alone: Power about-event link in isolation
    # =========================================================================
    {
        "id": "GRND029-b2-power-about-event", "subdir": "Entailment",
        "name": "B2 alone: Power in remedy relator concerns founding event",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_B2"],
        "description": """\
% Power(pw) with cnt(pw,decl(distrib),concert_ds) partOf rho_R,
% and founds_rem(e1,rho_R,f1) => about_event(pw, e1).
% B2 tested in isolation (not combined with B3 or A-axioms).""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# B2 standalone: Power in a remedy relator concerns the founding event.""",
        "fof_extra_decls": """\
fof(pos_pw,      axiom, position(pw)).
fof(rel_rho_r,   axiom, legal_relator(rho_r)).
fof(rule_f1,     axiom, rule(f1)).
fof(event_e1,    axiom, event(e1)).
fof(action_a,    axiom, action(some_action)).
fof(target_t,    axiom, target(some_target)).
fof(power_pw,    axiom, power(pw)).
fof(cnt_pw,      axiom, cnt(pw, decl(some_action), some_target)).
fof(partof_pw,   axiom, part_of(pw, rho_r)).
fof(founds_rem1, axiom, founds_rem(e1, rho_r, f1)).
""",
        "fof_conjecture": "about_event(pw, e1)",
        "smt2_extra_decls": """\
(declare-const pw          Position)
(declare-const rho-r       Relator)
(declare-const f1          Rule)
(declare-const e1          Event)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (power pw))
(assert (cnt pw (decl some-action) some-target))
(assert (part-of pw rho-r))
(assert (founds-rem e1 rho-r f1))
""",
        "smt2_conjecture": "(assert (not (about-event pw e1)))",
    },

    # =========================================================================
    # GRND030 — ax_B3 alone: Subjection about-event link in isolation
    # =========================================================================
    {
        "id": "GRND030-b3-subjection-about-event", "subdir": "Entailment",
        "name": "B3 alone: Subjection in remedy relator concerns founding event",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_B3"],
        "description": """\
% Subjection(s) with cnt(s,decl(some_action),some_target) partOf rho_R,
% and founds_rem(e1,rho_R,f1) => about_event(s, e1).
% B3 tested in isolation (not combined with B2 or A-axioms).""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# B3 standalone: Subjection in a remedy relator concerns the founding event.""",
        "fof_extra_decls": """\
fof(pos_s,       axiom, position(s)).
fof(rel_rho_r,   axiom, legal_relator(rho_r)).
fof(rule_f1,     axiom, rule(f1)).
fof(event_e1,    axiom, event(e1)).
fof(action_a,    axiom, action(some_action)).
fof(target_t,    axiom, target(some_target)).
fof(subj_s,      axiom, subjection(s)).
fof(cnt_s,       axiom, cnt(s, decl(some_action), some_target)).
fof(partof_s,    axiom, part_of(s, rho_r)).
fof(founds_rem1, axiom, founds_rem(e1, rho_r, f1)).
""",
        "fof_conjecture": "about_event(s, e1)",
        "smt2_extra_decls": """\
(declare-const s           Position)
(declare-const rho-r       Relator)
(declare-const f1          Rule)
(declare-const e1          Event)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (subjection s))
(assert (cnt s (decl some-action) some-target))
(assert (part-of s rho-r))
(assert (founds-rem e1 rho-r f1))
""",
        "smt2_conjecture": "(assert (not (about-event s e1)))",
    },

    # =========================================================================
    # GRND031 — ax_odrl_rel_is_rel: Ax5.11 standalone entailment
    # =========================================================================
    {
        "id": "GRND031-odrl-rel-is-legal-rel", "subdir": "Entailment",
        "name": "Ax5.11: ODRL relator is a UFO legal relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_odrl_rel_is_rel"],
        "description": """\
% odrl_rel(rho1) => legal_relator(rho1).
% Ax5.11 standalone: the subsumption bridge to UFO-L.""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Ax5.11: every ODRL relator is a UFO legal relator.""",
        "fof_extra_decls": """\
fof(odrl_rho1,    axiom, odrl_rel(rho1)).
""",
        "fof_conjecture": "legal_relator(rho1)",
        "smt2_extra_decls": """\
(declare-const rho1 Relator)
(assert (odrl-rel rho1))
""",
        "smt2_conjecture": "(assert (not (legal-relator rho1)))",
    },

    # =========================================================================
    # GRND032 — ax_odrl_rel_typing_rem: Ax5.7 rem variant standalone
    # =========================================================================
    {
        "id": "GRND032-odrl-rel-typing-rem", "subdir": "Entailment",
        "name": "Ax5.7 rem: founds_rem + proh => odrl_rel",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_odrl_rel_typing_rem"],
        "description": """\
% founds_rem(e1,rho1,f1) & proh(f1) => odrl_rel(rho1).
% Ax5.7 remedy variant tested in isolation.""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Ax5.7 rem: a remedy relator founded by a prohibition is an ODRL relator.""",
        "fof_extra_decls": """\
fof(rule_f1,      axiom, rule(f1)).
fof(event_e1,     axiom, event(e1)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(proh_f1,      axiom, proh(f1)).
fof(founds1,      axiom, founds_rem(e1, rho1, f1)).
""",
        "fof_conjecture": "odrl_rel(rho1)",
        "smt2_extra_decls": """\
(declare-const f1   Rule)
(declare-const e1   Event)
(declare-const rho1 Relator)
(assert (proh f1))
(assert (founds-rem e1 rho1 f1))
""",
        "smt2_conjecture": "(assert (not (odrl-rel rho1)))",
    },

    # =========================================================================
    # GRND033 — ax_odrl_rel_typing_imm: Ax5.7 imm variant standalone
    # =========================================================================
    {
        "id": "GRND033-odrl-rel-typing-imm", "subdir": "Entailment",
        "name": "Ax5.7 imm: founds_imm + perm => odrl_rel",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_odrl_rel_typing_imm"],
        "description": """\
% founds_imm(e1,rho1,p1) & perm(p1) => odrl_rel(rho1).
% Ax5.7 immunity variant tested in isolation.""",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
# Ax5.7 imm: an immunity relator founded by a permission is an ODRL relator.""",
        "fof_extra_decls": """\
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(perm_p1,      axiom, perm(p1)).
fof(founds1,      axiom, founds_imm(e1, rho1, p1)).
""",
        "fof_conjecture": "odrl_rel(rho1)",
        "smt2_extra_decls": """\
(declare-const p1   Rule)
(declare-const e1   Event)
(declare-const rho1 Relator)
(assert (perm p1))
(assert (founds-imm e1 rho1 p1))
""",
        "smt2_conjecture": "(assert (not (odrl-rel rho1)))",
    },

    # =========================================================================
    # GRND034 — Disability existence as positive conjecture
    # Strong permission creates Disability in assigner — conjecture form
    # =========================================================================
    {
        "id": "GRND034-disability-exists", "subdir": "Entailment",
        "name": "Strong perm creates Disability in assigner (positive conjecture)",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_perm_relator_strong"],
        "description": """\
% perm(p1) + strong(p1) + activates(e1,p1).
% Conjecture: exists Disability(museen, read, museum_api) in some rho_I.
% Tests Ax5.2 positive entailment directly (GRND020 only tested blocking).
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   museen=drk:StaatlicheMuseenBerlin""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-disability-exists a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:MuseumCollectionAPI ] .
drk:MuseumCollectionAPI             a dcat:DataService .
drk:StaatlicheMuseenBerlin          a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .""",
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
? [RhoI, Db] :
  ( founds_imm(e1, RhoI, p1)
  & disability(Db) & bearer(Db, museen) & cnt(Db, read, museum_api) & part_of(Db, RhoI) )""",
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
  (exists ((rho-i Relator) (db Position))
    (and (founds-imm e1 rho-i p1)
         (disability db) (bearer db museen) (cnt db read museum-api) (part-of db rho-i)))))""",
    },
]