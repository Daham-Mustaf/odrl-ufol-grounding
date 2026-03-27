%--------------------------------------------------------------------------
% File     : GRND013-corr-power-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Correlativity: Power implies unique Subjection in relator
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND013-corr-power-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % odrl_rel(rho1), Power(pw) partOf rho1 => exists unique s. Subjection(s) partOf rho1.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% # Correlativity: every Power in an ODRL relator has a unique correlative Subjection.
% # Grounded in a prohibition-with-remedy relator over drk:ConcertRecordingDataset.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_correlativity_power, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Pw] : ( power(Pw) & part_of(Pw,Rho) & cnt(Pw,A,T)
                      & ! [Pw2] : ( ( power(Pw2) & part_of(Pw2,Rho) & cnt(Pw2,A,T) )
                                   => Pw2 = Pw ) ) )
        <=> ( ? [S] : ( subjection(S) & part_of(S,Rho) & cnt(S,A,T)
                      & ! [S2] : ( ( subjection(S2) & part_of(S2,Rho) & cnt(S2,A,T) )
                                  => S2 = S ) ) ) ) )).

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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [S] : ( subjection(S) & part_of(S, rho1) & cnt(S, some_action, some_target)
        & ! [S2] : ( ( subjection(S2) & part_of(S2, rho1)
                     & cnt(S2, some_action, some_target) )
                   => S2 = S ) ) )).