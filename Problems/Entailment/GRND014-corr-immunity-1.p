%--------------------------------------------------------------------------
% File     : GRND014-corr-immunity-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Correlativity: Immunity implies unique Disability in relator
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND014-corr-immunity-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % odrl_rel(rho1), Immunity(im) partOf rho1 => exists unique db. Disability(db) partOf rho1.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% # Correlativity: every Immunity in an ODRL relator has a unique correlative Disability.
% # Grounded in a strong-permission relator over drk:MuseumCollectionAPI.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_correlativity_immunity, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Im] : ( immunity(Im) & part_of(Im,Rho) & cnt(Im,A,T)
                      & ! [Im2] : ( ( immunity(Im2) & part_of(Im2,Rho) & cnt(Im2,A,T) )
                                   => Im2 = Im ) ) )
        <=> ( ? [Db] : ( disability(Db) & part_of(Db,Rho) & cnt(Db,A,T)
                       & ! [Db2] : ( ( disability(Db2) & part_of(Db2,Rho) & cnt(Db2,A,T) )
                                    => Db2 = Db ) ) ) ) )).

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
fof(pos_im,            axiom, position(im)).
fof(rel_rho1,          axiom, legal_relator(rho1)).
fof(odrl_rho1,         axiom, odrl_rel(rho1)).
fof(immun_im,          axiom, immunity(im)).
fof(partof_im,         axiom, part_of(im, rho1)).
fof(cnt_im,            axiom, cnt(im, some_action, some_target)).
fof(some_action_typed, axiom, action(some_action)).
fof(some_target_typed, axiom, target(some_target)).
fof(immun_im_unique,   axiom,
    ! [Im2] : ( ( immunity(Im2) & part_of(Im2, rho1) & cnt(Im2, some_action, some_target) )
               => Im2 = im )).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Db] : ( disability(Db) & part_of(Db, rho1) & cnt(Db, some_action, some_target)
         & ! [Db2] : ( ( disability(Db2) & part_of(Db2, rho1)
                       & cnt(Db2, some_action, some_target) )
                     => Db2 = Db ) ) )).