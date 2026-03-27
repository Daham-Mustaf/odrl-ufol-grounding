%--------------------------------------------------------------------------
% File     : GRND021-remedy-chain-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Full remedy chain: violation triggers Power-licensed institutional act
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND021-remedy-chain-policy.ttl
% Generated: 2026-03-26 by gen_foundation_problems.py v1.5
%
% % proh(f1) + has_rem(f1) + activates(e1,f1) + does(marketplace,distrib,concert_ds).
% % Ax5.4 (founds_rem): creates rho_R with Power(philharmonie,decl(distrib),concert_ds)
% %                     and Subjection(marketplace,decl(distrib),concert_ds).
% % B1: does(marketplace,...) => NormStateChange.
% % A1: NormStateChange => exists InstEvent(ev) triggers it.
% % B2: Power(pw) partOf rho_R & founds_rem(e1,rho_R,f1) => about_event(pw,e1).
% % B3: Subjection(s,...) => about_event(s,e1).
% % A2: InstEvent => competent agent.
% % A3: competence => Power+Subjection pair about ev.
% % Conjecture: exists pw, s, ev such that about_event(pw,ev) and about_event(s,ev).
% % Abstract constants: marketplace=drk:MusicMarketplaceAG,
% %   philharmonie=drk:PhilharmonieBerlin, distrib=odrl:distribute,
% %   concert_ds=drk:ConcertRecordingDataset
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% # Full violation-to-remedy chain.
% ... (16 more lines — see Policies/ file)
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
fof(ax_B1, axiom,
    ! [F, X, A, T] :
      ( ( proh(F) & has_rem(F) & act(F,A) & tgt(F,T) & aee(F,X) & does(X,A,T) )
     => ? [B] : ( rem_act(F,B) & norm_state_change(X,B,T,duty_rem) ) )).
fof(ax_B2, axiom,
    ! [Pw, A, T, Rho, E, R] :
      ( ( power(Pw) & cnt(Pw,decl(A),T) & part_of(Pw,Rho) & founds_rem(E,Rho,R) )
     => about_event(Pw,E) )).
fof(ax_B3, axiom,
    ! [S, A, T, Rho, E, R] :
      ( ( subjection(S) & cnt(S,decl(A),T) & part_of(S,Rho) & founds_rem(E,Rho,R) )
     => about_event(S,E) )).
fof(ax_A1, axiom,
    ! [X, A, T, Q] :
      ( norm_state_change(X,A,T,Q)
     => ? [E] : ( inst_event(E) & triggers(E,X,A,T,Q) ) )).
fof(ax_A2, axiom,
    ! [E] :
      ( inst_event(E)
     => ? [Y] : competent_for(Y,E) )).
fof(ax_A3, axiom,
    ! [Y, E] :
      ( competent_for(Y,E)
     => ? [Pw, S, X] :
          ( power(Pw)     & bearer(Pw,Y) & about_event(Pw,E)
          & subjection(S) & bearer(S,X)  & about_event(S,E) ) )).

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
fof(agent_marketplace,  axiom, agent(marketplace)).
fof(agent_philharmonie, axiom, agent(philharmonie)).
fof(action_distrib,     axiom, action(distrib)).
fof(target_concert,     axiom, target(concert_ds)).
fof(rule_f1,            axiom, rule(f1)).
fof(event_e1,           axiom, event(e1)).
fof(relator_rho1,       axiom, legal_relator(rho1)).
fof(proh_f1,            axiom, proh(f1)).
fof(rem_f1,             axiom, has_rem(f1)).
fof(aee_f1,             axiom, aee(f1, marketplace)).
fof(aer_f1,             axiom, aer(f1, philharmonie)).
fof(act_f1,             axiom, act(f1, distrib)).
fof(tgt_f1,             axiom, tgt(f1, concert_ds)).
fof(act_e1_f1,          axiom, activates(e1, f1)).
fof(founds_e1_rho1,     axiom, founds(e1, rho1, f1)).
fof(marketplace_does,   axiom, does(marketplace, distrib, concert_ds)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [RhoR, Pw, S] :
  ( founds_rem(e1, RhoR, f1)
  & power(Pw)     & bearer(Pw, philharmonie) & cnt(Pw, decl(distrib), concert_ds) & part_of(Pw, RhoR) & about_event(Pw, e1)
  & subjection(S) & bearer(S,  marketplace)  & cnt(S,  decl(distrib), concert_ds) & part_of(S,  RhoR) & about_event(S,  e1) ) )).