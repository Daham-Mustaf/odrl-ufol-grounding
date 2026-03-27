%--------------------------------------------------------------------------
% File     : GRND006-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Correlativity: Permission implies unique NoRight in relator
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND006-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % odrl_rel(rho1), Permission(l) partOf rho1 => exists unique n. NoRight(n) partOf rho1.
% % Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
% %   ensemble=drk:BerlinerEnsemble, use_act=odrl:use,
% %   play_ds=drk:PlayProductionMetadataDataset
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% <drk:policy-corr> a odrl:Agreement ;
% ... (13 more lines — see Policies/ file)
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_correlativity_permission, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [L] : ( permission(L) & part_of(L,Rho) & cnt(L,A,T)
                    & ! [L2] : ( ( permission(L2) & part_of(L2,Rho) & cnt(L2,A,T) )
                                => L2 = L ) ) )
        <=> ( ? [N] : ( no_right(N) & part_of(N,Rho) & cnt(N,A,T)
                      & ! [M] : ( ( no_right(M) & part_of(M,Rho) & cnt(M,A,T) )
                                 => M = N ) ) ) ) )).

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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [N] : ( no_right(N) & part_of(N, rho1) & cnt(N, use_act, play_ds)
        & ! [M] : ( ( no_right(M) & part_of(M, rho1)
                    & cnt(M, use_act, play_ds) )
                  => M = N ) ) )).