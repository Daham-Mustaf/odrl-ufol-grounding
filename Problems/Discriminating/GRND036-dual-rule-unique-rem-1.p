%--------------------------------------------------------------------------
% File     : GRND036-dual-rule-unique-rem-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Dual-rule unique rem: same event+rule founds at most one remedy relator
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND036-dual-rule-unique-rem-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % Real DRK scenario: pol1 = BerlinerEnsemble prohibition with remedy.
% % founds_rem(e1,rhoR1,pol1) and founds_rem(e1,rhoR2,pol1) => rhoR1=rhoR2.
% % ax_unique_founding_rem fires: same event e1 + same rule pol1.
% % Mirrors GRND025 but grounded in actual DRK culture-dataspace entities.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% # Uniqueness test: same rule pol1 at same event e1 => same remedy relator.
% ... (12 more lines — see Policies/ file)
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
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
fof(rule_pol1,     axiom, rule(pol1)).
fof(event_e1,      axiom, event(e1)).
fof(relator_rhoR1, axiom, legal_relator(rhoR1)).
fof(relator_rhoR2, axiom, legal_relator(rhoR2)).
fof(founds_rem1,   axiom, founds_rem(e1, rhoR1, pol1)).
fof(founds_rem2,   axiom, founds_rem(e1, rhoR2, pol1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( rhoR1 = rhoR2 )).