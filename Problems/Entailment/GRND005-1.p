%--------------------------------------------------------------------------
% File     : GRND005-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Permission-Duty conflict detection (single relator)
% Status   : Unsatisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND005-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % Permission(l,bibliothek,read,theater_ds) and Duty(d,bibliothek,rfr(read),theater_ds)
% % in same relator rho1. Corollary ax:conflict derives False.
% % Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
% %   read=odrl:read, theater_ds=drk:TheaterShowtimeDataset
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% # Conflict witness — not a valid standalone policy.
% # Ground instance asserts:
% ... (6 more lines — see Policies/ file)
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_conflict, lemma,
    ! [Rho, L, D, X, A, T] :
      ( ( part_of(L,Rho) & part_of(D,Rho)
        & permission(L) & duty(D)
        & bearer(L,X) & bearer(D,X)
        & cnt(L,A,T)  & cnt(D,rfr(A),T) )
     => $false )).

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
fof(action_read,      axiom, action(read)).
fof(target_theater,   axiom, target(theater_ds)).
fof(pos_l,            axiom, position(l)).
fof(pos_d,            axiom, position(d)).
fof(rel_rho1,         axiom, legal_relator(rho1)).
fof(permission_l,     axiom, permission(l)).
fof(duty_d,           axiom, duty(d)).
fof(bearer_l,         axiom, bearer(l, bibliothek)).
fof(bearer_d,         axiom, bearer(d, bibliothek)).
fof(cnt_l,            axiom, cnt(l, read, theater_ds)).
fof(cnt_d,            axiom, cnt(d, rfr(read), theater_ds)).
fof(partof_l,         axiom, part_of(l, rho1)).
fof(partof_d,         axiom, part_of(d, rho1)).
