%--------------------------------------------------------------------------
% File     : GRND022-corr-nonunique-1.p
% Domain   : Foundational Ontology (UFO-L) / Deontic ODRL Grounding
% Problem  : Correlativity violated: two NoRight positions in same relator
% Status   : Unsatisfiable
% Refs     : [Mus+26] D. M. Mustafa, C. Lange, G. Guizzardi, D. Collarana, C. Quix, S. Decker. What Does ODRL Mean? A Cross-Level Ontological Grounding of Permissions, Prohibitions, and Duties in UFO-L. FOIS 2026; Frontiers in Artificial Intelligence and Applications, IOS Press. arXiv:2606.24344.
% Source   : https://github.com/Daham-Mustaf/odrl-ufol-grounding
% Authors  : Daham Mustafa
% Policy   : Policies/GRND022-corr-nonunique-policy.ttl
% Generated: 2026-06-25 by gen_foundation_problems.py v1.6
%
% % odrl_rel(rho1) + Permission(l) partOf rho1.
% % Two distinct no_right positions n1 != n2 both partOf rho1 with same content.
% % ax_correlativity_permission requires unique NoRight => contradiction.
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
fof(pos_l,         axiom, position(l)).
fof(pos_n1,        axiom, position(n1)).
fof(pos_n2,        axiom, position(n2)).
fof(rel_rho1,      axiom, legal_relator(rho1)).
fof(odrl_rho1,     axiom, odrl_rel(rho1)).
fof(permission_l,  axiom, permission(l)).
fof(no_right_n1,   axiom, no_right(n1)).
fof(no_right_n2,   axiom, no_right(n2)).
fof(partof_l,      axiom, part_of(l,  rho1)).
fof(partof_n1,     axiom, part_of(n1, rho1)).
fof(partof_n2,     axiom, part_of(n2, rho1)).
fof(cnt_l,         axiom, cnt(l,  some_action, some_target)).
fof(cnt_n1,        axiom, cnt(n1, some_action, some_target)).
fof(cnt_n2,        axiom, cnt(n2, some_action, some_target)).
fof(action_typed,  axiom, action(some_action)).
fof(target_typed,  axiom, target(some_target)).
fof(n1_neq_n2,     axiom, n1 != n2).
fof(perm_l_unique, axiom,
    ! [L2] : ( ( permission(L2) & part_of(L2, rho1) & cnt(L2, some_action, some_target) )
              => L2 = l )).
