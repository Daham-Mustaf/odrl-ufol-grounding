%--------------------------------------------------------------------------
% File     : GRND011-obl-relator-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Obligation creates Duty and Right
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND011-obl-relator-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % obl(obl1) activated by e1 entails Duty(bibliothek,read,play_ds)
% % and Right(ensemble,read,play_ds).
% % Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
% %   ensemble=drk:BerlinerEnsemble, read=odrl:read,
% %   play_ds=drk:PlayProductionMetadataDataset
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% drk:policy-obl-read a odrl:Agreement ;
% ... (11 more lines — see Policies/ file)
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_obl_relator, axiom,
    ! [D, X, Y, A, T, E] :
      ( ( obl(D) & aee(D,X) & aer(D,Y) & act(D,A) & tgt(D,T) & activates(E,D) )
     => ? [Rho, Du, C] :
          ( founds(E,Rho,D)
          & duty(Du) & bearer(Du,X) & cnt(Du,A,T) & part_of(Du,Rho)
          & right(C) & bearer(C,Y)  & cnt(C,A,T)  & part_of(C,Rho) ) )).

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

%--------------------------------------------------------------------------
% Ground instance (gamma)
%--------------------------------------------------------------------------
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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Rho, Du, C] :
  ( founds(e1, Rho, obl1)
  & duty(Du)  & bearer(Du, bibliothek) & cnt(Du, read, play_ds) & part_of(Du, Rho)
  & right(C)  & bearer(C,  ensemble)   & cnt(C,  read, play_ds) & part_of(C,  Rho) ) )).