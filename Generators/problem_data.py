"""
problem_data.py
===============
Problem definitions for the FOIS 2026 deontic grounding benchmark.
Each problem dict contains:
  id, subdir, name, status_fof, status_smt
  fof_axioms        — axiom keys from axiom_data.FOF_AXIOM_DICT
  description       — comment lines for .p / .smt2 header
  ttl               — real Turtle policy (written to Policies/ directory)
  fof_extra_decls   — FOF ground instance
  fof_conjecture    — FOF conjecture string or None
  smt2_extra_decls  — SMT-LIB ground instance
  smt2_conjecture   — SMT-LIB negated conjecture or None

DRK ontology entities used:
  Prefix  drk:    <http://w3id.org/drk/ontology/>
  Classes dcat:Dataset, dcat:DataService, schema:Organization
  Only classes/properties defined in the DRK ontology or imported vocabs.

Abstract constant naming convention (TPTP requires lowercase identifiers):
  Constants use short snake_case abbreviations of DRK entities.
  Each problem documents its own mapping in a comment block.
  The same abstract name (e.g. 'bibliothek') may represent the same real
  entity across problems; reuse is intentional and documented per-problem.

NormContent — gen_layer0_signature.py replaces separate Action/Forbearance
  sorts with a unified NormContent sort. All SMT2 (declare-const X Action)
  updated to (declare-const X NormContent).

Imported by: writers.py, gen_foundation_problems.py
"""
from pathlib import Path
from datetime import date

# ============================================================================
# TTL WRITER — saves real Turtle policy files
# ============================================================================

def write_ttl_policy(p: dict, out_dir: Path) -> Path | None:
    """Write a real .ttl policy file for problem p into out_dir/Policies/."""
    ttl = p.get("ttl")
    if not ttl:
        return None
    subdir = out_dir / "Policies"
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-policy.ttl"
    header = (
        f"# ------------------------------------------------------------------------------\n"
        f"# File     : {p['id']}-policy.ttl\n"
        f"# Domain   : Deontic Ontology / ODRL Grounding\n"
        f"# Problem  : {p['name']}\n"
        f"# Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026\n"
        f"# Generated: {date.today().isoformat()} by gen_foundation_problems.py\n"
        f"# Links    : {p['subdir']}/{p['id']}-1.p\n"
        f"#            {p['subdir']}/{p['id']}-1.smt2\n"
        f"# ------------------------------------------------------------------------------\n\n"
    )
    path.write_text(header + ttl.strip() + "\n", encoding="utf-8")
    return path


# ============================================================================
# PROBLEM DEFINITIONS
# ============================================================================

PROBLEMS = [
    # -------------------------------------------------------------------------
    # GRND001 — Satisfiability witness for the full axiom set
    # Abstract constants:
    #   bibliothek = drk:UniversitaetsbibliothekMuenchen (assignee)
    #   ensemble   = drk:BerlinerEnsemble (assigner)
    #   read       = odrl:read
    #   theater_ds = drk:TheaterShowtimeDataset
    # Bug 5 fix: fof_axioms includes ALL Layer1 axioms (paper §6.2 claim).
    # Note: may require extended timeout (--time 120) for Vampire.
    # -------------------------------------------------------------------------
    {
        "id": "GRND001", "subdir": "Consistency",
        "name": "Full axiom set consistency",
        "status_fof": "Satisfiable",
        "status_smt": "sat",
        "fof_axioms": [
            "ax_perm_relator_weak", "ax_perm_relator_strong",
            "ax_proh_relator_conduct", "ax_proh_relator_remedy",
            "ax_obl_relator",
            "ax_unique_founding", "ax_unique_event",
            "ax_unique_founding_rem", "ax_unique_event_rem",
            "ax_unique_founding_imm", "ax_unique_event_imm",
            "ax_odrl_rel_typing", "ax_odrl_rel_typing_rem", "ax_odrl_rel_typing_imm",
            "ax_correlativity_permission", "ax_correlativity_duty",
            "ax_correlativity_power", "ax_correlativity_immunity",
            "ax_cross_relator", "ax_conflict",
            "ax_disability_block", "ax_odrl_rel_is_rel",
            "ax_A1", "ax_A2", "ax_A3", "ax_B1", "ax_B2", "ax_B3",
        ],
        "description": """\
% The full axiom set (Ax5.1-5.11, A1-A3, B1-B3) is satisfiable.
% Minimal model: one perm rule, one agent pair, one action, one target.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   ensemble=drk:BerlinerEnsemble, read=odrl:read,
%   theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-theater-read> a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:BerlinerEnsemble ;
        odrl:action   odrl:read ;
        odrl:target   drk:TheaterShowtimeDataset] .
drk:TheaterShowtimeDataset>          a dcat:Dataset ;
    schema:name "Berliner Ensemble Showtime Dataset" .
drk:BerlinerEnsemble                    a schema:Organization .
drk:UniversitaetsbibliothekMuenchen     a schema:Organization .
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   ensemble=drk:BerlinerEnsemble, read=odrl:read,
#   theater_ds=drk:TheaterShowtimeDataset""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_ensemble,   axiom, agent(ensemble)).
fof(action_read,      axiom, action(read)).
fof(target_theater,   axiom, target(theater_ds)).
fof(rule_p1,          axiom, rule(p1)).
fof(event_e1,         axiom, event(e1)).
fof(perm_p1,          axiom, perm(p1)).
fof(aee_p1,           axiom, aee(p1, bibliothek)).
fof(aer_p1,           axiom, aer(p1, ensemble)).
fof(act_p1,           axiom, act(p1, read)).
fof(tgt_p1,           axiom, tgt(p1, theater_ds)).
fof(act_e1_p1,        axiom, activates(e1, p1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const bibliothek Agent) (declare-const ensemble  Agent)
(declare-const read       NormContent) (declare-const theater-ds Target)
(declare-const p1         Rule)  (declare-const e1        Event)
(assert (perm p1))
(assert (aee p1 bibliothek)) (assert (aer p1 ensemble))
(assert (act p1 read))       (assert (tgt p1 theater-ds))
(assert (activates e1 p1))
""",
        "smt2_conjecture": None,
    },

    # -------------------------------------------------------------------------
    # GRND002 — Permission entailment
    # Abstract constants:
    #   bibliothek = drk:UniversitaetsbibliothekMuenchen (assignee)
    #   ensemble   = drk:BerlinerEnsemble (assigner)
    #   read       = odrl:read
    #   theater_ds = drk:TheaterShowtimeDataset
    # -------------------------------------------------------------------------
    {
        "id": "GRND002", "subdir": "Entailment",
        "name": "Permission creates Permission and NoRight",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_perm_relator_weak"],
        "description": """\
% perm(p1) activated by e1 entails Permission(bibliothek,read,theater_ds)
% and NoRight(ensemble,read,theater_ds).
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   ensemble=drk:BerlinerEnsemble, read=odrl:read,
%   theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-theater-read a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchens ;
        odrl:assigner drk:BerlinerEnsemble ;
        odrl:action   odrl:read ;
        odrl:target   drk:TheaterShowtimeDataset ] .
drk:TheaterShowtimeDataset               a dcat:Dataset ;
    schema:name "Berliner Ensemble Showtime Dataset" .
drk:BerlinerEnsemble                    a schema:Organization .
drk:UniversitaetsbibliothekMuenchen     a schema:Organization .
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   ensemble=drk:BerlinerEnsemble, read=odrl:read,
#   theater_ds=drk:TheaterShowtimeDataset""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_ensemble,   axiom, agent(ensemble)).
fof(action_read,      axiom, action(read)).
fof(target_theater,   axiom, target(theater_ds)).
fof(rule_p1,          axiom, rule(p1)).
fof(event_e1,         axiom, event(e1)).
fof(perm_p1,          axiom, perm(p1)).
fof(aee_p1,           axiom, aee(p1, bibliothek)).
fof(aer_p1,           axiom, aer(p1, ensemble)).
fof(act_p1,           axiom, act(p1, read)).
fof(tgt_p1,           axiom, tgt(p1, theater_ds)).
fof(act_e1_p1,        axiom, activates(e1, p1)).
""",
        "fof_conjecture": """\
? [Rho, L, N] :
  ( founds(e1, Rho, p1)
  & permission(L) & bearer(L, bibliothek) & cnt(L, read, theater_ds) & part_of(L, Rho)
  & no_right(N)   & bearer(N, ensemble)   & cnt(N, read, theater_ds) & part_of(N, Rho) )""",
        "smt2_extra_decls": """\
(declare-const bibliothek Agent) (declare-const ensemble  Agent)
(declare-const read       NormContent) (declare-const theater-ds Target)
(declare-const p1         Rule)  (declare-const e1        Event)
(assert (perm p1))
(assert (aee p1 bibliothek)) (assert (aer p1 ensemble))
(assert (act p1 read))       (assert (tgt p1 theater-ds))
(assert (activates e1 p1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho Relator) (l Position) (n Position))
    (and (founds e1 rho p1)
         (permission l) (bearer l bibliothek) (cnt l read theater-ds) (part-of l rho)
         (no-right n)   (bearer n ensemble)   (cnt n read theater-ds) (part-of n rho)))))""",
    },

    # -------------------------------------------------------------------------
    # GRND003 — Prohibition conduct entailment
    # Abstract constants:
    #   portal  = drk:StreamingPortalGmbH (assignee)
    #   museen  = drk:StaatlicheMuseenBerlin (assigner)
    #   distrib = odrl:distribute
    #   museum_api = drk:MuseumCollectionAPI
    # Bug 9 fix: ax_proh_relator_basic -> ax_proh_relator_conduct
    # -------------------------------------------------------------------------
    {
        "id": "GRND003", "subdir": "Entailment",
        "name": "Prohibition creates Duty and Right over rfr(a)",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_conduct"],
        "description": """\
% proh(f1) activated by e1 entails Duty(portal,rfr(distrib),museum_api)
% and Right(museen,rfr(distrib),museum_api).
% Abstract constants: portal=drk:StreamingPortalGmbH,
%   museen=drk:StaatlicheMuseenBerlin, distrib=odrl:distribute,
%   museum_api=drk:MuseumCollectionAPI""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-no-distribute> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:StreamingPortalGmbH ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:distribute ;
        odrl:target   drk:MuseumCollectionAPI ] .
drk:MuseumCollectionAPI    a dcat:DataService ;
    schema:name "Staatliche Museen Berlin Collection API" .
drk:StaatlicheMuseenBerlin a schema:Organization .
drk:StreamingPortalGmbH    a schema:Organization .
# Abstract constants: portal=drk:StreamingPortalGmbH,
#   museen=drk:StaatlicheMuseenBerlin, distrib=odrl:distribute,
#   museum_api=drk:MuseumCollectionAPI""",
        "fof_extra_decls": """\
fof(agent_portal,     axiom, agent(portal)).
fof(agent_museen,     axiom, agent(museen)).
fof(action_distrib,   axiom, action(distrib)).
fof(target_museum,    axiom, target(museum_api)).
fof(rule_f1,          axiom, rule(f1)).
fof(event_e1,         axiom, event(e1)).
fof(proh_f1,          axiom, proh(f1)).
fof(aee_f1,           axiom, aee(f1, portal)).
fof(aer_f1,           axiom, aer(f1, museen)).
fof(act_f1,           axiom, act(f1, distrib)).
fof(tgt_f1,           axiom, tgt(f1, museum_api)).
fof(act_e1_f1,        axiom, activates(e1, f1)).
""",
        "fof_conjecture": """\
? [Rho, D, C] :
  ( founds(e1, Rho, f1)
  & duty(D)  & bearer(D, portal) & cnt(D, rfr(distrib), museum_api) & part_of(D, Rho)
  & right(C) & bearer(C, museen) & cnt(C, rfr(distrib), museum_api) & part_of(C, Rho) )""",
        "smt2_extra_decls": """\
(declare-const portal    Agent) (declare-const museen    Agent)
(declare-const distrib   NormContent) (declare-const museum-api Target)
(declare-const f1        Rule)  (declare-const e1        Event)
(assert (proh f1))
(assert (aee f1 portal)) (assert (aer f1 museen))
(assert (act f1 distrib)) (assert (tgt f1 museum-api))
(assert (activates e1 f1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho Relator) (d Position) (c Position))
    (and (founds e1 rho f1)
         (duty d)  (bearer d portal) (cnt d (rfr distrib) museum-api) (part-of d rho)
         (right c) (bearer c museen) (cnt c (rfr distrib) museum-api) (part-of c rho)))))""",
    },

    # -------------------------------------------------------------------------
    # GRND004 — Prohibition remedy entailment
    # Abstract constants:
    #   marketplace  = drk:MusicMarketplaceAG (assignee)
    #   philharmonie = drk:PhilharmonieBerlin (assigner)
    #   distrib      = odrl:distribute
    #   concert_ds   = drk:ConcertRecordingDataset
    # Bug 9 fix: ax_proh_relator_basic -> ax_proh_relator_conduct
    # -------------------------------------------------------------------------
    {
        "id": "GRND004", "subdir": "Entailment",
        "name": "Prohibition with remedy creates Power and Subjection",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_conduct", "ax_proh_relator_remedy"],
        "description": """\
% proh(f1) + has_rem(f1) + activates(e1,f1).
% Ax5.4 existentially founds rho_R via founds_rem.
% Entails Power(philharmonie,decl(distrib),concert_ds)
% and Subjection(marketplace,decl(distrib),concert_ds) in rho_R.
% Abstract constants: marketplace=drk:MusicMarketplaceAG,
%   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
%   concert_ds=drk:ConcertRecordingDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-concert-remedy a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:MusicMarketplaceAG ;
        odrl:assigner drk:PhilharmonieBerlin ;
        odrl:action   odrl:distribute ;
        odrl:target   drk:ConcertRecordingDataset ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action odrl:compensate ] ] .
drk:ConcertRecordingDataset               a dcat:Dataset ;
    schema:name "Philharmonie Berlin Concert Recordings" .
drk:PhilharmonieBerlin  a schema:Organization .
drk:MusicMarketplaceAG  a schema:Organization .
# Power(drk:PhilharmonieBerlin, decl(distribute)) constituted at activation
# in fresh competence relator rho_R (Ax5.4 via founds_rem).
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
  & power(Pw)     & bearer(Pw, philharmonie) & cnt(Pw, decl(distrib), concert_ds) & part_of(Pw, RhoR)
  & subjection(S) & bearer(S,  marketplace)  & cnt(S,  decl(distrib), concert_ds) & part_of(S,  RhoR) )""",
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
         (power pw)     (bearer pw philharmonie) (cnt pw (decl distrib) concert-ds) (part-of pw rho-r)
         (subjection s) (bearer s  marketplace)  (cnt s  (decl distrib) concert-ds) (part-of s  rho-r)))))""",
    },

    # -------------------------------------------------------------------------
    # GRND005 — Within-relator conflict detection
    # Abstract constants:
    #   bibliothek = drk:UniversitaetsbibliothekMuenchen
    #   read       = odrl:read
    #   theater_ds = drk:TheaterShowtimeDataset
    # Bug 1 fix: fof_axioms uses ax_conflict (within-relator corollary),
    #   not ax_cross_relator (which is the cross-bearer axiom Ax5.9).
    #   GRND005 places Permission and Duty in the SAME relator — that is
    #   exactly what ax_conflict governs. ax_cross_relator would also fire
    #   but misrepresents the paper's derivation structure.
    # -------------------------------------------------------------------------
    {
        "id": "GRND005", "subdir": "Entailment",
        "name": "Permission-Duty conflict detection (single relator)",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_conflict"],
        "description": """\
% Permission(l,bibliothek,read,theater_ds) and Duty(d,bibliothek,rfr(read),theater_ds)
% in same relator rho1. Corollary ax:conflict derives False.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   read=odrl:read, theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# Conflict witness — not a valid standalone policy.
# Ground instance asserts:
#   Permission(drk:UniversitaetsbibliothekMuenchen, read, drk:TheaterShowtimeDataset)
# AND
#   Duty(drk:UniversitaetsbibliothekMuenchen, rfr(read), drk:TheaterShowtimeDataset)
# in the same relator. ax:conflict (Corollary of Ax5.9) derives False.
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

    # -------------------------------------------------------------------------
    # GRND006 — Correlativity: Permission implies unique NoRight
    # Abstract constants:
    #   bibliothek  = drk:UniversitaetsbibliothekMuenchen
    #   ensemble    = drk:BerlinerEnsemble
    #   use_act     = odrl:use
    #   play_ds     = drk:PlayProductionMetadataDataset
    # -------------------------------------------------------------------------
    {
        "id": "GRND006", "subdir": "Entailment",
        "name": "Correlativity: Permission implies unique NoRight in relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_correlativity_permission"],
        "description": """\
% odrl_rel(rho1), Permission(l) partOf rho1 => exists unique n. NoRight(n) partOf rho1.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   ensemble=drk:BerlinerEnsemble, use_act=odrl:use,
%   play_ds=drk:PlayProductionMetadataDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
<drk:policy-corr> a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:BerlinerEnsemble> ;
        odrl:action   odrl:use ;
        odrl:target   <drk:PlayProductionMetadataDataset> ] .
drk:PlayProductionMetadataDataset   a dcat:Dataset ;
    schema:name "Berliner Ensemble Play Production Metadata" .
drk:BerlinerEnsemble               a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .
# Permission(Bibliothek) entails unique NoRight(Ensemble) in relator.
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   ensemble=drk:BerlinerEnsemble, use_act=odrl:use,
#   play_ds=drk:PlayProductionMetadataDataset""",
        "fof_extra_decls": """\
fof(pos_l,            axiom, position(l)).
fof(rel_rho1,         axiom, legal_relator(rho1)).
fof(odrl_rho1,        axiom, odrl_rel(rho1)).
fof(permission_l,     axiom, permission(l)).
fof(partof_l,         axiom, part_of(l, rho1)).
fof(cnt_l,            axiom, cnt(l, use_act, play_ds)).
fof(use_act_typed,    axiom, action(use_act)).
fof(play_ds_typed,    axiom, target(play_ds)).
fof(perm_l_unique,    axiom,
    ! [L2] : ( ( permission(L2) & part_of(L2, rho1) & cnt(L2, use_act, play_ds) )
              => L2 = l )).
""",
        "fof_conjecture": """\
? [N] : ( no_right(N) & part_of(N, rho1) & cnt(N, use_act, play_ds)
        & ! [M] : ( ( no_right(M) & part_of(M, rho1)
                    & cnt(M, use_act, play_ds) )
                  => M = N ) )""",
        "smt2_extra_decls": """\
(declare-const l        Position)
(declare-const rho1     Relator)
(declare-const use-act  NormContent)
(declare-const play-ds  Target)
(assert (permission l)) (assert (part-of l rho1))
(assert (cnt l use-act play-ds))
(assert (odrl-rel rho1))
; l is the unique permission in rho1 — triggers exists-unique antecedent
(assert (forall ((l2 Position))
  (=> (and (permission l2) (part-of l2 rho1) (cnt l2 use-act play-ds))
      (= l2 l))))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((n Position))
    (and (no-right n) (part-of n rho1) (cnt n use-act play-ds)
         (forall ((m Position))
           (=> (and (no-right m) (part-of m rho1)
                    (cnt m use-act play-ds))
               (= m n)))))))""",
    },

    # -------------------------------------------------------------------------
    # GRND007-open — Open-world discriminating
    # fof_axioms: [] — open-world closure is a custom axiom in fof_extra_decls,
    #   not a Layer1 axiom. This is intentional: the open-world assumption is
    #   a policy-evaluation convention, not a grounding axiom.
    # Abstract constants:
    #   portal     = drk:StreamingPortalGmbH
    #   ensemble   = drk:BerlinerEnsemble
    #   modify_act = odrl:modify
    #   theater_ds = drk:TheaterShowtimeDataset
    # -------------------------------------------------------------------------
    {
        "id": "GRND007-open", "subdir": "Discriminating",
        "name": "Open-world: uncovered action entails Permission by default",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [],  # open-world closure is a custom axiom in fof_extra_decls
        "skip_smt2_axioms": True,  # problem is self-contained; Layer 1 axioms cause Z3 timeout
        "description": """\
% Open-world closure added. No proh for modify_act.
% Permission(portal,modify_act,theater_ds) is derivable.
% Abstract constants: portal=drk:StreamingPortalGmbH,
%   ensemble=drk:BerlinerEnsemble, modify_act=odrl:modify,
%   theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# behaviour=open policy over drk:TheaterShowtimeDataset.
# No prohibition on odrl:modify declared.
# => Permission(drk:StreamingPortalGmbH, modify, drk:TheaterShowtimeDataset)
#    derivable by open-world default.
# Abstract constants: portal=drk:StreamingPortalGmbH,
#   ensemble=drk:BerlinerEnsemble, modify_act=odrl:modify,
#   theater_ds=drk:TheaterShowtimeDataset""",
        "fof_extra_decls": """\
fof(agent_portal,       axiom, agent(portal)).
fof(agent_ensemble,     axiom, agent(ensemble)).
fof(action_modify,      axiom, action(modify_act)).
fof(target_theater,     axiom, target(theater_ds)).
fof(no_proh_modify,     axiom,
    ~ ? [F, E] : ( proh(F) & aee(F,portal) & act(F,modify_act) & activates(E,F) )).
fof(open_world_closure, axiom,
    ! [X, A, T] :
      ( ( agent(X) & action(A) & target(T)
        & ~ ? [F, E] : ( proh(F) & aee(F,X) & act(F,A) & activates(E,F) ) )
     => ? [L] : ( permission(L) & bearer(L,X) & cnt(L,A,T) ) )).
""",
        "fof_conjecture": """\
? [L] : ( permission(L) & bearer(L, portal) & cnt(L, modify_act, theater_ds) )""",
        "smt2_extra_decls": """\
(declare-const portal     Agent) (declare-const ensemble   Agent)
(declare-const modify-act NormContent) (declare-const theater-ds Target)
(assert (not (exists ((f Rule) (e Event))
               (and (proh f) (aee f portal) (act f modify-act) (activates e f)))))
(assert (forall ((x Agent) (a NormContent) (t Target))
  (=> (not (exists ((f Rule) (e Event))
              (and (proh f) (aee f x) (act f a) (activates e f))))
      (exists ((l Position))
        (and (permission l) (bearer l x) (cnt l a t))))))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((l Position))
    (and (permission l) (bearer l portal) (cnt l modify-act theater-ds)))))""",
    },

    # -------------------------------------------------------------------------
    # GRND007-closed — Closed-world discriminating
    # Abstract constants: same as GRND007-open
    # -------------------------------------------------------------------------
    {
        "id": "GRND007-closed", "subdir": "Discriminating",
        "name": "Closed-world: no Permission for uncovered action",
        "status_fof": "Satisfiable",
        "status_smt": "sat",
        "fof_axioms": [],
        "description": """\
% No perm rule for modify_act. No open-world closure.
% Permission(portal,modify_act,theater_ds) is NOT derivable.
% Abstract constants: portal=drk:StreamingPortalGmbH,
%   modify_act=odrl:modify, theater_ds=drk:TheaterShowtimeDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# behaviour=closed policy over drk:TheaterShowtimeDataset.
# No permission for odrl:modify declared.
# => Permission(drk:StreamingPortalGmbH, modify, drk:TheaterShowtimeDataset)
#    NOT derivable.
# Abstract constants: portal=drk:StreamingPortalGmbH,
#   modify_act=odrl:modify, theater_ds=drk:TheaterShowtimeDataset""",
        "fof_extra_decls": """\
fof(agent_portal,           axiom, agent(portal)).
fof(action_modify,          axiom, action(modify_act)).
fof(target_theater,         axiom, target(theater_ds)).
fof(no_permission_modify,   axiom,
    ~ ? [L] : ( permission(L) & bearer(L, portal) & cnt(L, modify_act, theater_ds) )).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const portal     Agent)
(declare-const modify-act NormContent) (declare-const theater-ds Target)
(assert (not (exists ((l Position))
               (and (permission l) (bearer l portal) (cnt l modify-act theater-ds)))))
""",
        "smt2_conjecture": None,
    },

    # -------------------------------------------------------------------------
    # GRND008-sanctioned — Sanctioned prohibition
    # Abstract constants:
    #   marketplace  = drk:MusicMarketplaceAG (assignee)
    #   philharmonie = drk:PhilharmonieBerlin (assigner)
    #   distrib      = odrl:distribute
    #   concert_ds   = drk:ConcertRecordingDataset
    # Bug 2 fix: cnt(Pw, decl(distrib), concert_ds) and
    #   cnt(S, decl(distrib), concert_ds) added to both FOF and SMT2 conjecture.
    # -------------------------------------------------------------------------
    {
        "id": "GRND008-sanctioned", "subdir": "Discriminating",
        "name": "Sanctioned prohibition: violation reachable, remedy norm fires",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_remedy"],
        "description": """\
% proh(f1) + has_rem(f1) + activates(e1,f1) + does(marketplace,distrib,concert_ds).
% Conjecture: Power+Subjection pair with cnt exists in fresh rho_R via founds_rem.
% Abstract constants: marketplace=drk:MusicMarketplaceAG,
%   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
%   concert_ds=drk:ConcertRecordingDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
<drk:policy-sanctioned> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:MusicMarketplaceAG> ;
        odrl:assigner <drk:PhilharmonieBerlin> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:ConcertRecordingDataset> ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action odrl:compensate ] ] .
drk:ConcertRecordingDataset a dcat:Dataset ;
    schema:name "Philharmonie Berlin Concert Recordings" .
drk:PhilharmonieBerlin a schema:Organization .
drk:MusicMarketplaceAG a schema:Organization .
# drk:MusicMarketplaceAG performs distribute => violation reachable.
# Power(drk:PhilharmonieBerlin, decl(distribute)) constituted at activation.
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
  & power(Pw)     & bearer(Pw, philharmonie) & cnt(Pw, decl(distrib), concert_ds) & part_of(Pw, RhoR)
  & subjection(S) & bearer(S,  marketplace)  & cnt(S,  decl(distrib), concert_ds) & part_of(S,  RhoR) )""",
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
         (power pw)     (bearer pw philharmonie) (cnt pw (decl distrib) concert-ds) (part-of pw rho-r)
         (subjection s) (bearer s  marketplace)  (cnt s  (decl distrib) concert-ds) (part-of s  rho-r)))))""",
    },

    # -------------------------------------------------------------------------
    # GRND008-regimented — Regimented prohibition: contradiction
    # Abstract constants:
    #   marketplace = drk:MusicMarketplaceAG
    #   distrib     = odrl:distribute
    #   concert_ds  = drk:ConcertRecordingDataset
    # Bug 3 fix: has_rem removed — regimented reading has no remedy.
    # -------------------------------------------------------------------------
    {
        "id": "GRND008-regimented", "subdir": "Discriminating",
        "name": "Regimented prohibition: contradiction",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": [],
        "description": """\
% Regimented axiom: ~does when prohibited.
% Ground witness: does(marketplace,distrib,concert_ds). Contradiction.
% has_rem NOT asserted — regimented reading presupposes no remedy.
% Abstract constants: marketplace=drk:MusicMarketplaceAG,
%   distrib=odrl:distribute, concert_ds=drk:ConcertRecordingDataset""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
<drk:policy-regimented> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:MusicMarketplaceAG> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:ConcertRecordingDataset> ] .
drk:ConcertRecordingDataset               a dcat:Dataset .
drk:MusicMarketplaceAG      a schema:Organization .
# Regimented reading: does(MusicMarketplaceAG, distribute) impossible.
# No remedy — regimentation makes violation structurally impossible.
# Ground witness asserts does => contradiction.
# Abstract constants: marketplace=drk:MusicMarketplaceAG,
#   distrib=odrl:distribute, concert_ds=drk:ConcertRecordingDataset""",
        "fof_extra_decls": """\
fof(agent_marketplace,  axiom, agent(marketplace)).
fof(action_distrib,     axiom, action(distrib)).
fof(target_concert,     axiom, target(concert_ds)).
fof(rule_f1,            axiom, rule(f1)).
fof(event_e1,           axiom, event(e1)).
fof(proh_f1,            axiom, proh(f1)).
fof(act_f1,             axiom, act(f1, distrib)).
fof(aee_f1,             axiom, aee(f1, marketplace)).
fof(act_e1_f1,          axiom, activates(e1, f1)).
fof(regimented,         axiom,
    ! [X, A, T, F, E] :
      ( ( proh(F) & aee(F,X) & act(F,A) & activates(E,F) )
     => ~ does(X,A,T) )).
fof(marketplace_does,   axiom, does(marketplace, distrib, concert_ds)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const marketplace Agent)
(declare-const distrib     NormContent) (declare-const concert-ds Target)
(declare-const f1          Rule)  (declare-const e1         Event)
(assert (proh f1))
(assert (act f1 distrib)) (assert (aee f1 marketplace))
(assert (activates e1 f1))
(assert (forall ((x Agent) (a NormContent) (t Target) (f2 Rule) (e2 Event))
  (=> (and (proh f2) (aee f2 x) (act f2 a) (activates e2 f2))
      (not (does x a t)))))
(assert (does marketplace distrib concert-ds))
""",
        "smt2_conjecture": None,
    },

    # -------------------------------------------------------------------------
    # GRND009-immunity — Strong permission: Disability blocks prohibition
    # Abstract constants:
    #   bibliothek = drk:UniversitaetsbibliothekMuenchen (assignee)
    #   museen     = drk:StaatlicheMuseenBerlin (assigner)
    #   read       = odrl:read
    #   museum_api = drk:MuseumCollectionAPI
    # Bug 6 fix: odrl_rel(rho1) added.
    # Ax numbering fix: ax_disability_block = Ax5.10 (not Ax5.11).
    # -------------------------------------------------------------------------
    {
        "id": "GRND009-immunity", "subdir": "Discriminating",
        "name": "Strong permission: Permission persists (Disability blocks prohibition)",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_disability_block"],
        "description": """\
% H2 = {Permission, NoRight, Immunity, Disability}.
% museen attempts proh(f2). Ax5.10: Disability + proh => False.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   museen=drk:StaatlicheMuseenBerlin, read=odrl:read,
%   museum_api=drk:MuseumCollectionAPI""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-strong a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:MuseumCollectionAPI ] .
drk:MuseumCollectionAPI             a dcat:DataService ;
    schema:name "Staatliche Museen Berlin Collection API" .
drk:StaatlicheMuseenBerlin          a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .
# strong(p) asserted (profile extension, not ODRL 2.2).
# Immunity(bibliothek) + Disability(museen).
# museen attempts prohibition => blocked by Disability (Ax5.10).
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   museen=drk:StaatlicheMuseenBerlin, read=odrl:read,
#   museum_api=drk:MuseumCollectionAPI""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_museen,     axiom, agent(museen)).
fof(action_read,      axiom, action(read)).
fof(target_museum,    axiom, target(museum_api)).
fof(pos_l,            axiom, position(l)).
fof(pos_n,            axiom, position(n)).
fof(pos_im,           axiom, position(im)).
fof(pos_db,           axiom, position(db)).
fof(rel_rho1,         axiom, legal_relator(rho1)).
fof(odrl_rho1,        axiom, odrl_rel(rho1)).
fof(permission_l,     axiom, permission(l)).
fof(no_right_n,       axiom, no_right(n)).
fof(immunity_im,      axiom, immunity(im)).
fof(disability_db,    axiom, disability(db)).
fof(bearer_l,         axiom, bearer(l,  bibliothek)).
fof(bearer_n,         axiom, bearer(n,  museen)).
fof(bearer_im,        axiom, bearer(im, bibliothek)).
fof(bearer_db,        axiom, bearer(db, museen)).
fof(cnt_l,            axiom, cnt(l,  read, museum_api)).
fof(cnt_n,            axiom, cnt(n,  read, museum_api)).
fof(cnt_im,           axiom, cnt(im, read, museum_api)).
fof(cnt_db,           axiom, cnt(db, read, museum_api)).
fof(rule_f2,          axiom, rule(f2)).
fof(proh_f2,          axiom, proh(f2)).
fof(aee_f2,           axiom, aee(f2, bibliothek)).
fof(aer_f2,           axiom, aer(f2, museen)).
fof(act_f2,           axiom, act(f2, read)).
fof(tgt_f2,           axiom, tgt(f2, museum_api)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const bibliothek Agent) (declare-const museen     Agent)
(declare-const read       NormContent) (declare-const museum-api Target)
(declare-const l          Position) (declare-const n          Position)
(declare-const im         Position) (declare-const db         Position)
(declare-const rho1       Relator)  (declare-const f2         Rule)
(assert (permission l)) (assert (no-right n))
(assert (immunity im))  (assert (disability db))
(assert (bearer l bibliothek))  (assert (bearer n museen))
(assert (bearer im bibliothek)) (assert (bearer db museen))
(assert (cnt l read museum-api))   (assert (cnt n read museum-api))
(assert (cnt im read museum-api))  (assert (cnt db read museum-api))
(assert (odrl-rel rho1))
(assert (proh f2))
(assert (aee f2 bibliothek)) (assert (aer f2 museen))
(assert (act f2 read))       (assert (tgt f2 museum-api))
""",
        "smt2_conjecture": None,
    },

    # -------------------------------------------------------------------------
    # GRND009-no-immunity — Weak permission: Permission+Duty conflict
    # Abstract constants: same as GRND009-immunity
    # Bug 7 fix: ax_proh_relator_basic -> ax_proh_relator_conduct
    # Ax numbering fix: ax_cross_relator = Ax5.9 (not Ax5.10).
    # -------------------------------------------------------------------------
    {
        "id": "GRND009-no-immunity", "subdir": "Discriminating",
        "name": "Weak permission: Permission+Duty conflict when prohibition added",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_conduct", "ax_cross_relator"],
        "description": """\
% H1 = {Permission, NoRight} — no Immunity/Disability.
% museen adds proh(f2): Ax5.3 creates Duty(bibliothek,rfr(read),museum_api).
% Ax5.9: Permission + Duty-to-refrain => False.
% Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%   museen=drk:StaatlicheMuseenBerlin, read=odrl:read,
%   museum_api=drk:MuseumCollectionAPI""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
drk:policy-conflict a odrl:Agreement ;
    odrl:permission  [ a odrl:Permission ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:MuseumCollectionAPI ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee drk:UniversitaetsbibliothekMuenchen ;
        odrl:assigner drk:StaatlicheMuseenBerlin ;
        odrl:action   odrl:read ;
        odrl:target   drk:MuseumCollectionAPI ] .
drk:MuseumCollectionAPI             a dcat:DataService .
drk:StaatlicheMuseenBerlin          a schema:Organization .
drk:UniversitaetsbibliothekMuenchen a schema:Organization .
# Weak permission (no Immunity/Disability).
# Prohibition creates Duty(rfr(read)) => Permission + Duty conflict => False.
# Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
#   museen=drk:StaatlicheMuseenBerlin, read=odrl:read,
#   museum_api=drk:MuseumCollectionAPI""",
        "fof_extra_decls": """\
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_museen,     axiom, agent(museen)).
fof(action_read,      axiom, action(read)).
fof(target_museum,    axiom, target(museum_api)).
fof(pos_l,            axiom, position(l)).
fof(pos_n,            axiom, position(n)).
fof(rel_rho1,         axiom, legal_relator(rho1)).
fof(rule_f2,          axiom, rule(f2)).
fof(event_e2,         axiom, event(e2)).
fof(permission_l,     axiom, permission(l)).
fof(no_right_n,       axiom, no_right(n)).
fof(bearer_l,         axiom, bearer(l, bibliothek)).
fof(bearer_n,         axiom, bearer(n, museen)).
fof(cnt_l,            axiom, cnt(l, read, museum_api)).
fof(cnt_n,            axiom, cnt(n, read, museum_api)).
fof(proh_f2,          axiom, proh(f2)).
fof(aee_f2,           axiom, aee(f2, bibliothek)).
fof(aer_f2,           axiom, aer(f2, museen)).
fof(act_f2,           axiom, act(f2, read)).
fof(tgt_f2,           axiom, tgt(f2, museum_api)).
fof(act_e2_f2,        axiom, activates(e2, f2)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const bibliothek Agent) (declare-const museen    Agent)
(declare-const read       NormContent) (declare-const museum-api Target)
(declare-const l          Position) (declare-const n         Position)
(declare-const rho1       Relator)
(declare-const f2         Rule) (declare-const e2 Event)
(assert (permission l)) (assert (no-right n))
(assert (bearer l bibliothek)) (assert (bearer n museen))
(assert (cnt l read museum-api))  (assert (cnt n read museum-api))
(assert (proh f2))
(assert (aee f2 bibliothek)) (assert (aer f2 museen))
(assert (act f2 read))       (assert (tgt f2 museum-api))
(assert (activates e2 f2))
""",
        "smt2_conjecture": None,
    },
]