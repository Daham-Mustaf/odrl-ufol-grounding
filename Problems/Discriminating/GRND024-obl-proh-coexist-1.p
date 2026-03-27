%--------------------------------------------------------------------------
% File     : GRND024-obl-proh-coexist-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Obligation + Prohibition coexist: Duty(a) vs Duty(rfr(a)) distinct
% Status   : Satisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND024-obl-proh-coexist-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % obl(obl1) activated at e1: creates Duty(bibliothek, read, theater_ds).
% % proh(f1)  activated at e2: creates Duty(bibliothek, rfr(read), theater_ds).
% % ax_cross_relator fires on Permission+Duty(rfr), NOT Duty(a)+Duty(rfr(a)).
% % Status: Satisfiable — the two duties coexist (different content).
% % Discriminating: shows obl and proh do NOT directly conflict in the grounding.
% % Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
% %   ensemble=drk:BerlinerEnsemble, museen=drk:StaatlicheMuseenBerlin,
% %   read=odrl:read, theater_ds=drk:TheaterShowtimeDataset
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% # Obligation to read AND prohibition on reading coexist
% ... (19 more lines — see Policies/ file)
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
% NOTE: FOF inlines per-problem subsets only (fof_axioms key) to avoid
% Vampire timeouts. SMT-LIB embeds the full axiom set (Z3 does not
% timeout on the full set). This asymmetry is intentional.
fof(ax_obl_relator, axiom,
    ! [D, X, Y, A, T, E] :
      ( ( obl(D) & aee(D,X) & aer(D,Y) & act(D,A) & tgt(D,T) & activates(E,D) )
     => ? [Rho, Du, C] :
          ( founds(E,Rho,D)
          & duty(Du) & bearer(Du,X) & cnt(Du,A,T) & part_of(Du,Rho)
          & right(C) & bearer(C,Y)  & cnt(C,A,T)  & part_of(C,Rho) ) )).
fof(ax_proh_relator_conduct, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & right(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).
fof(ax_cross_relator, axiom,
    ! [L, D, X, A, T] :
      ( ( permission(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)       & bearer(D,X) & cnt(D,rfr(A),T) )
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
fof(agent_ensemble,   axiom, agent(ensemble)).
fof(agent_museen,     axiom, agent(museen)).
fof(action_read,      axiom, action(read)).
fof(target_theater,   axiom, target(theater_ds)).
% Obligation: bibliothek must read theater_ds
fof(rule_obl1,        axiom, rule(obl1)).
fof(event_e1,         axiom, event(e1)).
fof(obl_obl1,         axiom, obl(obl1)).
fof(aee_obl1,         axiom, aee(obl1, bibliothek)).
fof(aer_obl1,         axiom, aer(obl1, ensemble)).
fof(act_obl1,         axiom, act(obl1, read)).
fof(tgt_obl1,         axiom, tgt(obl1, theater_ds)).
fof(act_e1_obl1,      axiom, activates(e1, obl1)).
% Prohibition: bibliothek must not read theater_ds
fof(rule_f1,          axiom, rule(f1)).
fof(event_e2,         axiom, event(e2)).
fof(proh_f1,          axiom, proh(f1)).
fof(aee_f1,           axiom, aee(f1, bibliothek)).
fof(aer_f1,           axiom, aer(f1, museen)).
fof(act_f1,           axiom, act(f1, read)).
fof(tgt_f1,           axiom, tgt(f1, theater_ds)).
fof(act_e2_f1,        axiom, activates(e2, f1)).
