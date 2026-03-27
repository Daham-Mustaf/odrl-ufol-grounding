%--------------------------------------------------------------------------
% File     : GRND007-open-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Open-world: uncovered action entails Permission by default
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND007-open-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % Open-world closure added. No proh for modify_act.
% % Permission(portal,modify_act,theater_ds) is derivable.
% % Abstract constants: portal=drk:StreamingPortalGmbH,
% %   ensemble=drk:BerlinerEnsemble, modify_act=odrl:modify,
% %   theater_ds=drk:TheaterShowtimeDataset
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% # behaviour=open policy over drk:TheaterShowtimeDataset.
% # No prohibition on odrl:modify declared.
% ... (5 more lines — see Policies/ file)
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.

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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [L] : ( permission(L) & bearer(L, portal) & cnt(L, modify_act, theater_ds) ) )).