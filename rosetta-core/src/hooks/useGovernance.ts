/**
 * AT·OM — useGovernance
 * Hook de gouvernance directe — propositions, votes, consensus
 *
 * "Nous décidons ensemble. Personne n'est au-dessus."
 *
 * Le même flux Rosetta circule ici :
 *   TECH   → Payload JSON structuré (quorum, votes, poids)
 *   PEOPLE → Narration humaine (résultat du vote, consensus)
 *   SPIRIT → Fréquence de consensus (333Hz→777Hz)
 */

import { useCallback, useMemo } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import {
  getStakeRequired,
  calculateVoteWeight,
  canPropose,
  checkQuorum,
  checkConsensus,
} from '../parser/templates/GovernanceTemplate';
import type {
  ProposalType,
  VoteValue,
  SphereId,
  GovernanceProposal,
} from '../types/atom-types';
import { GOVERNANCE_DEFAULTS } from '../types/atom-types';

export function useGovernance() {
  const { state, dispatch, parser } = useATOM();
  const { governance } = state;

  // ─── Créer une proposition ──────────────────────────────
  const createProposal = useCallback((params: {
    type: ProposalType;
    title: string;
    description: string;
    sphere_id: SphereId | null;
    discussion_days: number;
  }) => {
    const resonanceScore = state.identity.sovereign_identity?.resonance_score ?? 0;

    // Vérifier que l'utilisateur peut proposer
    if (!canPropose(resonanceScore, params.type)) {
      return { success: false, reason: 'Score de résonance insuffisant pour ce type de proposition' };
    }

    const proposal: GovernanceProposal = {
      id: `proposal_${Date.now().toString(36)}`,
      type: params.type,
      title: params.title,
      description: params.description,
      sphere_id: params.sphere_id,
      proposer_id: state.user_id ?? 'anonymous',
      status: 'DRAFT',
      stake_required: getStakeRequired(params.type),
      quorum_pct: GOVERNANCE_DEFAULTS.quorum_pct,
      approval_pct: GOVERNANCE_DEFAULTS.approval_pct,
      discussion_days: params.discussion_days,
      votes_pour: 0,
      votes_contre: 0,
      votes_abstention: 0,
      created_at: Date.now(),
      voting_ends_at: Date.now() + params.discussion_days * 86400000,
    };

    // Traduire par Rosetta (3 dimensions)
    parser.translate('governance', {
      proposal_type: params.type,
      sphere_id: params.sphere_id ?? 'POLITIQUE',
      proposer_score: resonanceScore,
      title: params.title,
      description: params.description,
      council_size: governance.council_count,
    }, 'TECH', proposal.id);

    dispatch({
      type: 'GOVERNANCE_UPDATE',
      payload: {
        proposals: [...governance.proposals, proposal],
        active_proposal: proposal,
      },
    });

    return { success: true, proposal };
  }, [state, dispatch, parser, governance]);

  // ─── Voter sur une proposition ──────────────────────────
  const vote = useCallback((proposalId: string, value: VoteValue) => {
    const resonanceScore = state.identity.sovereign_identity?.resonance_score ?? 0;
    const weight = calculateVoteWeight(resonanceScore);

    const updatedProposals = governance.proposals.map(p => {
      if (p.id !== proposalId) return p;
      return {
        ...p,
        votes_pour: value === 'POUR' ? p.votes_pour + 1 : p.votes_pour,
        votes_contre: value === 'CONTRE' ? p.votes_contre + 1 : p.votes_contre,
        votes_abstention: value === 'ABSTENTION' ? p.votes_abstention + 1 : p.votes_abstention,
      };
    });

    dispatch({
      type: 'GOVERNANCE_UPDATE',
      payload: { proposals: updatedProposals },
    });

    return { success: true, weight };
  }, [state, dispatch, governance]);

  // ─── Vérificateurs ──────────────────────────────────────
  const isConsensusReached = useCallback((proposal: GovernanceProposal) => {
    return checkConsensus(proposal.votes_pour, proposal.votes_contre);
  }, []);

  const isQuorumMet = useCallback((totalVotes: number) => {
    return checkQuorum(totalVotes, governance.council_count);
  }, [governance.council_count]);

  // ─── Métriques dérivées ─────────────────────────────────
  const activeProposals = useMemo(() =>
    governance.proposals.filter(p => p.status === 'VOTING'),
  [governance.proposals]);

  const approvedProposals = useMemo(() =>
    governance.proposals.filter(p => p.status === 'APPROVED'),
  [governance.proposals]);

  return {
    // État
    proposals: governance.proposals,
    activeProposal: governance.active_proposal,
    councilCount: governance.council_count,
    activeProposals,
    approvedProposals,

    // Actions
    createProposal,
    vote,

    // Vérificateurs
    isConsensusReached,
    isQuorumMet,
    canPropose: (score: number, type: ProposalType) => canPropose(score, type),
    getStakeRequired,
    calculateVoteWeight,
  };
}
