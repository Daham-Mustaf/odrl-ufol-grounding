%--------------------------------------------------------------------------
% File     : GRND012-corr-duty-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Correlativity: Duty implies unique Right in relator
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND012-corr-duty-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % odrl_rel(rho1), Duty(d) partOf rho1 => exists unique c. Right(c) partOf rho1.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% # Correlativity: every Duty in an ODRL relator has a unique correlative Right.
% # Tested on drk:TheaterShowtimeDataset prohibition relator.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_correlativity_duty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [D] : ( duty(D) & part_of(D,Rho) & cnt(D,A,T)
                    & ! [D2] : ( ( duty(D2) & part_of(D2,Rho) & cnt(D2,A,T) )
                                => D2 = D ) ) )
        <=> ( ? [C] : ( right(C) & part_of(C,Rho) & cnt(C,A,T)
                      & ! [K] : ( ( right(K) & part_of(K,Rho) & cnt(K,A,T) )
                                 => K = C ) ) ) ) )).

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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [C] : ( right(C) & part_of(C, rho1) & cnt(C, some_action, some_target)
        & ! [K] : ( ( right(K) & part_of(K, rho1)
                    & cnt(K, some_action, some_target) )
                  => K = C ) ) )).