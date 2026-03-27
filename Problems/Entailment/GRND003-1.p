%--------------------------------------------------------------------------
% File     : GRND003-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Prohibition creates Duty and Right over rfr(a)
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND003-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % proh(f1) activated by e1 entails Duty(portal,rfr(distrib),museum_api)
% % and Right(museen,rfr(distrib),museum_api).
% % Abstract constants: portal=drk:StreamingPortalGmbH,
% %   museen=drk:StaatlicheMuseenBerlin, distrib=odrl:distribute,
% %   museum_api=drk:MuseumCollectionAPI
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% <drk:policy-no-distribute> a odrl:Agreement ;
% ... (12 more lines — see Policies/ file)
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_proh_relator_conduct, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & right(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).

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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Rho, D, C] :
  ( founds(e1, Rho, f1)
  & duty(D)  & bearer(D, portal) & cnt(D, rfr(distrib), museum_api) & part_of(D, Rho)
  & right(C) & bearer(C, museen) & cnt(C, rfr(distrib), museum_api) & part_of(C, Rho) ) )).