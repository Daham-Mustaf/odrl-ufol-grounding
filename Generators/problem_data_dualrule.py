"""
problem_data_dualrule.py
========================
Two-provider dual-rule problems for the FOIS 2026 / PAAR 2026 benchmark.
Grounded in the DRK culture-dataspace scenario:
  - Consumer:  drk:UniversitaetsbibliothekMuenchen  (bibliothek)
  - ProviderA: drk:BerlinerEnsemble                 (ensemble)
  - ProviderB: drk:StaatlicheMuseenBerlin            (museen)
  - DatasetA:  drk:TheaterShowtimeDataset            (theater_ds)
  - DatasetB:  drk:MuseumCollectionAPI               (museum_api)
  - RemedyA:   odrl:compensate                       (compensate)
  - RemedyB:   odrl:delete                           (delete_act)
Both providers prohibit the consumer from distributing their dataset,
but with different remedies:
  pol1 (ensemble):  remedy = compensate  → Power(ensemble, decl(distrib), theater_ds)
  pol2 (museen):    remedy = delete      → Power(museen,   decl(distrib), museum_api)
Problems:
  GRND035  B2 entailment in dual-rule scenario     Entailment / Theorem
  GRND036  Two remedy relators are distinct         Discriminating / Theorem
All required keys are present in axiom_data.FOF_AXIOM_DICT v1.5.
"""

PROBLEMS_DUALRULE = [
    # =========================================================================
    # GRND035 — Dual-rule: both remedy relators created; Power in rho_R1
    #           concerns founding event e1 (B2 entailment in real scenario)
    # =========================================================================
    {
        "id": "GRND035-dual-rule-remedy-chain", "subdir": "Entailment",
        "name": "Dual-rule: Power in remedy relator concerns founding event (B2)",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_proh_relator_remedy",
            "ax_B2",
        ],
        "description": """\
% Two prohibitions with distinct remedies from two DRK providers:
%   pol1: ensemble prohibits bibliothek from distributing theater_ds
%         remedy = compensate (pay ensemble)
%   pol2: museen  prohibits bibliothek from distributing museum_api
%         remedy = delete     (destroy copy)
% Conjecture: activating pol1 at e1 creates a remedy relator rho_R1
% containing Power(ensemble, decl(distrib), theater_ds) linked to e1 (B2).
% Abstract constants:
%   bibliothek = drk:UniversitaetsbibliothekMuenchen (consumer)
%   ensemble   = drk:BerlinerEnsemble  (ProviderA, remedy=compensate)
%   museen     = drk:StaatlicheMuseenBerlin (ProviderB, remedy=delete)
%   theater_ds = drk:TheaterShowtimeDataset
%   museum_api = drk:MuseumCollectionAPI
%   distrib    = odrl:distribute
%   compensate = odrl:compensate
%   delete_act = odrl:delete""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# ProviderA: BerlinerEnsemble prohibits distribution, remedy = compensate
drk:pol1 a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:BerlinerEnsemble ;
        odrl:action   odrl:distribute ;
        odrl:target   drk:TheaterShowtimeDataset ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action   odrl:compensate ;
            odrl:assignee drk:BerlinerEnsemble ] ] .
# ProviderB: StaatlicheMuseenBerlin prohibits distribution, remedy = delete
drk:pol2 a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:distribute ;
        odrl:target   drk:MuseumCollectionAPI ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action odrl:delete ] ] .
drk:TheaterShowtimeDataset          a dcat:Dataset .
drk:MuseumCollectionAPI             a dcat:DataService .
drk:BerlinerEnsemble                a schema:Organization .
drk:StaatlicheMuseenBerlin          a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .""",
        "fof_extra_decls": """\
fof(agent_bibliothek,  axiom, agent(bibliothek)).
fof(agent_ensemble,    axiom, agent(ensemble)).
fof(agent_museen,      axiom, agent(museen)).
fof(action_distrib,    axiom, action(distrib)).
fof(action_compensate, axiom, action(compensate)).
fof(action_delete,     axiom, action(delete_act)).
fof(target_theater,    axiom, target(theater_ds)).
fof(target_museum,     axiom, target(museum_api)).
fof(rule_pol1,         axiom, rule(pol1)).
fof(rule_pol2,         axiom, rule(pol2)).
fof(event_e1,          axiom, event(e1)).
fof(event_e2,          axiom, event(e2)).
% pol1: ensemble prohibits bibliothek from distributing theater_ds
%       remedy = compensate
fof(proh_pol1,         axiom, proh(pol1)).
fof(rem_pol1,          axiom, has_rem(pol1)).
fof(aee_pol1,          axiom, aee(pol1, bibliothek)).
fof(aer_pol1,          axiom, aer(pol1, ensemble)).
fof(act_pol1,          axiom, act(pol1, distrib)).
fof(tgt_pol1,          axiom, tgt(pol1, theater_ds)).
fof(act_e1_pol1,       axiom, activates(e1, pol1)).
% pol2: museen prohibits bibliothek from distributing museum_api
%       remedy = delete
fof(proh_pol2,         axiom, proh(pol2)).
fof(rem_pol2,          axiom, has_rem(pol2)).
fof(aee_pol2,          axiom, aee(pol2, bibliothek)).
fof(aer_pol2,          axiom, aer(pol2, museen)).
fof(act_pol2,          axiom, act(pol2, distrib)).
fof(tgt_pol2,          axiom, tgt(pol2, museum_api)).
fof(act_e2_pol2,       axiom, activates(e2, pol2)).
""",
        "fof_conjecture": """\
? [RhoR1, Pw1] :
  ( founds_rem(e1, RhoR1, pol1)
  & power(Pw1) & bearer(Pw1, ensemble)
  & cnt(Pw1, decl(distrib), theater_ds)
  & part_of(Pw1, RhoR1)
  & about_event(Pw1, e1) )""",
        "smt2_extra_decls": """\
(declare-const bibliothek  Agent) (declare-const ensemble   Agent)
(declare-const museen      Agent)
(declare-const distrib     NormContent) (declare-const compensate NormContent)
(declare-const delete-act  NormContent)
(declare-const theater-ds  Target) (declare-const museum-api Target)
(declare-const pol1        Rule)   (declare-const pol2       Rule)
(declare-const e1          Event)  (declare-const e2         Event)
; pol1: ensemble prohibits bibliothek, remedy = compensate
(assert (proh pol1)) (assert (has-rem pol1))
(assert (aee pol1 bibliothek)) (assert (aer pol1 ensemble))
(assert (act pol1 distrib))    (assert (tgt pol1 theater-ds))
(assert (activates e1 pol1))
; pol2: museen prohibits bibliothek, remedy = delete
(assert (proh pol2)) (assert (has-rem pol2))
(assert (aee pol2 bibliothek)) (assert (aer pol2 museen))
(assert (act pol2 distrib))    (assert (tgt pol2 museum-api))
(assert (activates e2 pol2))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho-r1 Relator) (pw1 Position))
    (and (founds-rem e1 rho-r1 pol1)
         (power pw1) (bearer pw1 ensemble)
         (cnt pw1 (decl distrib) theater-ds)
         (part-of pw1 rho-r1)
         (about-event pw1 e1)))))""",
    },

    # =========================================================================
    # =========================================================================
    # GRND036 — ax_unique_founding_rem in real DRK scenario
    # Same rule + same event founds at most one remedy relator.
    # Mirrors GRND025 (abstract) grounded in actual DRK entities.
    # Bug 1 fix: original rhoR1!=rhoR2 was trivially true without the axiom.
    #            Replaced with rhoR1=rhoR2 which actually fires ax_unique_founding_rem.
    # Bug 2 fix: SMT2 uses explicit (= rho-r1 rho-r2) not (not (distinct ...)).
    # =========================================================================
    {
        "id": "GRND036-dual-rule-unique-rem", "subdir": "Discriminating",
        "name": "Dual-rule unique rem: same event+rule founds at most one remedy relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_unique_founding_rem"],
        "description": """% Real DRK scenario: pol1 = BerlinerEnsemble prohibition with remedy.
% founds_rem(e1,rhoR1,pol1) and founds_rem(e1,rhoR2,pol1) => rhoR1=rhoR2.
% ax_unique_founding_rem fires: same event e1 + same rule pol1.
% Mirrors GRND025 but grounded in actual DRK culture-dataspace entities.""",
        "ttl": """@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Uniqueness test: same rule pol1 at same event e1 => same remedy relator.
drk:pol1 a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:BerlinerEnsemble ;
        odrl:action   odrl:distribute ;
        odrl:target   drk:TheaterShowtimeDataset ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action   odrl:compensate ;
            odrl:assignee drk:BerlinerEnsemble ] ] .
drk:TheaterShowtimeDataset          a dcat:Dataset .
drk:BerlinerEnsemble                a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .""",
        "fof_extra_decls": """fof(rule_pol1,     axiom, rule(pol1)).
fof(event_e1,      axiom, event(e1)).
fof(relator_rhoR1, axiom, legal_relator(rhoR1)).
fof(relator_rhoR2, axiom, legal_relator(rhoR2)).
fof(founds_rem1,   axiom, founds_rem(e1, rhoR1, pol1)).
fof(founds_rem2,   axiom, founds_rem(e1, rhoR2, pol1)).
""",
        "fof_conjecture": "rhoR1 = rhoR2",
        "smt2_extra_decls": """(declare-const pol1   Rule)
(declare-const e1     Event)
(declare-const rho-r1 Relator)
(declare-const rho-r2 Relator)
(assert (founds-rem e1 rho-r1 pol1))
(assert (founds-rem e1 rho-r2 pol1))
""",
        "smt2_conjecture": "(assert (not (= rho-r1 rho-r2)))",
    },

]