/**
 * AT·OM — GovernanceTemplate
 * TranslatorTemplate pour la Gouvernance Directe (Sphère 5: 555Hz)
 *
 * "Nous décidons ensemble. Personne n'est au-dessus."
 *
 * Traduit les propositions, votes et décisions de gouvernance
 * dans les 3 dimensions Rosetta :
 *   - TECH : Smart contract specs, vote tallies, quorum data
 *   - PEOPLE : Description accessible de la proposition et son impact
 *   - SPIRIT : Fréquence de consensus, géométrie de la décision collective
 */

import {
  type SphereId,
  type ResonanceLevel,
  type ProposalType,
  type ProposalStatus,
  type VoteValue,
  SPHERES,
  RESONANCE_MATRIX,
  SACRED_FREQUENCIES,
  GOVERNANCE_DEFAULTS,
  RESONANCE_RANKS,
} from '../../types/atom-types';
import { type TranslatorTemplate, type ParserContext, RosettaParser } from '../RosettaParser';

// ═══════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════

export interface GovernanceInput {
  proposal_id: string;
  type: ProposalType;
  title: string;
  description: string;
  sphere_id: SphereId | null;
  proposer_id: string;
  proposer_resonance: number;         // 0-100
  status: ProposalStatus;
  votes_pour: number;
  votes_contre: number;
  votes_abstention: number;
  total_weight_pour: number;          // Pondéré par resonance_score
  total_weight_contre: number;
  discussion_days: number;
  stake_amount: number;               // UR stakés
}

// ═══════════════════════════════════════════════════════════
// TEMPLATE
// ═══════════════════════════════════════════════════════════

export const GovernanceTemplate: TranslatorTemplate<GovernanceInput> = {
  domain: 'governance',

  toTech(input, ctx) {
    const totalVotes = input.votes_pour + input.votes_contre + input.votes_abstention;
    const totalWeight = input.total_weight_pour + input.total_weight_contre;
    const approvalRate = totalWeight > 0 ? input.total_weight_pour / totalWeight : 0;
    const quorumMet = totalVotes >= GOVERNANCE_DEFAULTS.council_size * GOVERNANCE_DEFAULTS.quorum_pct;

    return {
      schema_version: '1.0',
      data_type: 'governance_proposal',
      values: {
        proposal_id: input.proposal_id,
        type: input.type,
        status: input.status,
        sphere_id: input.sphere_id,
        votes: {
          pour: input.votes_pour,
          contre: input.votes_contre,
          abstention: input.votes_abstention,
          total: totalVotes,
        },
        weighted_approval: Math.round(approvalRate * 10000) / 100, // %
        quorum_met: quorumMet,
        quorum_required: GOVERNANCE_DEFAULTS.quorum_pct,
        approval_required: GOVERNANCE_DEFAULTS.approval_pct,
        stake_amount: input.stake_amount,
        stake_required: getStakeRequired(input.type),
        discussion_days: input.discussion_days,
        proposer_id: input.proposer_id,
        proposer_resonance: input.proposer_resonance,
        system_frequency: ctx.system_frequency,
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, _ctx) {
    const sphere = input.sphere_id ? SPHERES[input.sphere_id] : null;
    const typeLabel = PROPOSAL_TYPE_LABELS[input.type];
    const statusLabel = PROPOSAL_STATUS_LABELS[input.status];
    const totalVotes = input.votes_pour + input.votes_contre + input.votes_abstention;
    const totalWeight = input.total_weight_pour + input.total_weight_contre;
    const approvalPct = totalWeight > 0 ? Math.round((input.total_weight_pour / totalWeight) * 100) : 0;

    const sphereInfo = sphere
      ? ` dans la sphère ${sphere.label} (${sphere.frequency}Hz)`
      : '';

    let narrative = `Proposition ${typeLabel}${sphereInfo} : "${input.title}". `;
    narrative += `Statut : ${statusLabel}. `;

    if (totalVotes > 0) {
      narrative += `${totalVotes} votes exprimés — ${approvalPct}% d'approbation pondérée. `;
      if (approvalPct >= 67) {
        narrative += `Le consensus est atteint ! La communauté a parlé d'une seule voix.`;
      } else if (approvalPct >= 50) {
        narrative += `La majorité est favorable mais le consensus (67%) n'est pas encore atteint.`;
      } else {
        narrative += `La proposition nécessite plus de soutien communautaire.`;
      }
    } else {
      narrative += `En attente des premières voix du Conseil.`;
    }

    const tone = input.status === 'APPROVED' ? 'celebratoire' as const
      : input.status === 'REJECTED' ? 'alerte' as const
      : input.status === 'VOTING' ? 'encourageant' as const
      : 'neutre' as const;

    return {
      narrative,
      explanation: input.description,
      guide_steps: [
        `Type de proposition : ${typeLabel} (stake requis : ${getStakeRequired(input.type)} UR)`,
        `Quorum requis : ${Math.round(GOVERNANCE_DEFAULTS.quorum_pct * 100)}% du Conseil des ${GOVERNANCE_DEFAULTS.council_size}`,
        `Seuil d'approbation : ${Math.round(GOVERNANCE_DEFAULTS.approval_pct * 100)}% (pondéré par résonance)`,
        `Période de discussion : ${input.discussion_days} jours`,
      ],
      emotional_tone: tone,
      language: 'fr',
    };
  },

  toSpirit(input, _ctx) {
    // La fréquence de gouvernance est basée sur Sphère 5 (555Hz)
    // mais s'élève avec le consensus
    const totalWeight = input.total_weight_pour + input.total_weight_contre;
    const approvalRate = totalWeight > 0 ? input.total_weight_pour / totalWeight : 0;

    // Plus le consensus est fort, plus la fréquence monte
    // 0% consensus → 333Hz (Mental), 100% consensus → 777Hz (Silence/Sagesse)
    const consensusFreq = 333 + Math.round(approvalRate * 4) * 111; // 333, 444, 555, 666, 777
    const level = Math.max(1, Math.min(9, Math.round(consensusFreq / 111))) as ResonanceLevel;
    const resonance = RESONANCE_MATRIX[level];

    return {
      frequency_hz: resonance.hz,
      resonance_level: level,
      color: input.status === 'APPROVED' ? '#50C878' // Émeraude du consensus
        : input.status === 'REJECTED' ? '#8B0000'
        : resonance.color,
      sacred_geometry: RosettaParser.geometryFor(level),
      vibration_signature: [
        SACRED_FREQUENCIES.ATOM_M,
        SACRED_FREQUENCIES.ATOM_P,
        SACRED_FREQUENCIES.ATOM_I,
        SACRED_FREQUENCIES.ATOM_PO,
      ],
      phi_ratio: SACRED_FREQUENCIES.PHI,
    };
  },
};

// ═══════════════════════════════════════════════════════════
// UTILITAIRES
// ═══════════════════════════════════════════════════════════

const PROPOSAL_TYPE_LABELS: Record<ProposalType, string> = {
  OPERATIONNELLE: 'Opérationnelle',
  STRUCTURELLE: 'Structurelle',
  CONSTITUTIONNELLE: 'Constitutionnelle',
};

const PROPOSAL_STATUS_LABELS: Record<ProposalStatus, string> = {
  DRAFT: 'Brouillon',
  DISCUSSION: 'En discussion',
  VOTING: 'En vote',
  APPROVED: 'Approuvée ✓',
  REJECTED: 'Rejetée ✗',
  EXECUTED: 'Exécutée',
};

/** Retourne le stake minimum requis pour chaque type de proposition */
export function getStakeRequired(type: ProposalType): number {
  switch (type) {
    case 'OPERATIONNELLE': return GOVERNANCE_DEFAULTS.proposal_stake_operationnelle;
    case 'STRUCTURELLE': return GOVERNANCE_DEFAULTS.proposal_stake_structurelle;
    case 'CONSTITUTIONNELLE': return GOVERNANCE_DEFAULTS.proposal_stake_constitutionnelle;
  }
}

/** Calcule le poids de vote d'un utilisateur basé sur son resonance_score */
export function calculateVoteWeight(resonance_score: number): number {
  // Le poids est proportionnel au score, avec un minimum de 1
  return Math.max(1, Math.round(resonance_score / 10));
}

/** Vérifie si un utilisateur peut proposer un certain type de proposition */
export function canPropose(resonance_score: number, type: ProposalType): boolean {
  switch (type) {
    case 'OPERATIONNELLE': return resonance_score >= 20;   // CITOYEN+
    case 'STRUCTURELLE': return resonance_score >= 40;     // FONDATEUR+
    case 'CONSTITUTIONNELLE': return resonance_score >= 80; // ARCHITECTE
  }
}

/** Vérifie le quorum sur un vote */
export function checkQuorum(totalVotes: number): boolean {
  return totalVotes >= Math.ceil(GOVERNANCE_DEFAULTS.council_size * GOVERNANCE_DEFAULTS.quorum_pct);
}

/** Vérifie si le consensus est atteint */
export function checkConsensus(weightPour: number, weightContre: number): boolean {
  const total = weightPour + weightContre;
  if (total === 0) return false;
  return (weightPour / total) >= GOVERNANCE_DEFAULTS.approval_pct;
}
