%--------------------------------------------------------------------------
% File     : GRND036-dual-rule-distinct-relators-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Dual-rule: two remedy relators from distinct providers are distinct
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND036-dual-rule-distinct-relators-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % pol1 (ensemble) and pol2 (museen) are distinct rules (pol1 ≠ pol2).
% % Each activates at a different event and founds its own remedy relator.
% % ax_unique_founding_rem: same event+rule founds at most one relator.
% % Since pol1 ≠ pol2, rho_R1 and rho_R2 are individuated by distinct rules.
% % Conjecture: rho_R1 ≠ rho_R2.
% % This discriminates the two providers' enforcement authority structures.
% % Abstract constants:
% %   bibliothek = drk:UniversitaetsbibliothekMuenchen (consumer)
% %   ensemble   = drk:BerlinerEnsemble  (ProviderA)
% %   museen     = drk:StaatlicheMuseenBerlin (ProviderB)
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% # Same as GRND035 — two provider policies, distinct remedy relators.
% ... (24 more lines — see Policies/ file)
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
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) )
     => ? [RhoR, Pw, S] :
          ( founds_rem(E,RhoR,F)
          & power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,RhoR)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,RhoR) ) )).
fof(ax_unique_founding_rem, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds_rem(E,Rho1,R) & founds_rem(E,Rho2,R) ) => Rho1 = Rho2 )).

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
fof(agent_bibliothek,  axiom, agent(bibliothek)).
fof(agent_ensemble,    axiom, agent(ensemble)).
fof(agent_museen,      axiom, agent(museen)).
fof(action_distrib,    axiom, action(distrib)).
fof(target_theater,    axiom, target(theater_ds)).
fof(target_museum,     axiom, target(museum_api)).
fof(rule_pol1,         axiom, rule(pol1)).
fof(rule_pol2,         axiom, rule(pol2)).
fof(event_e1,          axiom, event(e1)).
fof(event_e2,          axiom, event(e2)).
fof(relator_rhoR1,     axiom, legal_relator(rhoR1)).
fof(relator_rhoR2,     axiom, legal_relator(rhoR2)).
% pol1 and pol2 are distinct rules
fof(pol1_neq_pol2,     axiom, pol1 != pol2).
% Each activation founds its own remedy relator
fof(proh_pol1,         axiom, proh(pol1)).
fof(rem_pol1,          axiom, has_rem(pol1)).
fof(aee_pol1,          axiom, aee(pol1, bibliothek)).
fof(aer_pol1,          axiom, aer(pol1, ensemble)).
fof(act_pol1,          axiom, act(pol1, distrib)).
fof(tgt_pol1,          axiom, tgt(pol1, theater_ds)).
fof(act_e1_pol1,       axiom, activates(e1, pol1)).
fof(founds_rem1,       axiom, founds_rem(e1, rhoR1, pol1)).
fof(proh_pol2,         axiom, proh(pol2)).
fof(rem_pol2,          axiom, has_rem(pol2)).
fof(aee_pol2,          axiom, aee(pol2, bibliothek)).
fof(aer_pol2,          axiom, aer(pol2, museen)).
fof(act_pol2,          axiom, act(pol2, distrib)).
fof(tgt_pol2,          axiom, tgt(pol2, museum_api)).
fof(act_e2_pol2,       axiom, activates(e2, pol2)).
fof(founds_rem2,       axiom, founds_rem(e2, rhoR2, pol2)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( rhoR1 != rhoR2 )).