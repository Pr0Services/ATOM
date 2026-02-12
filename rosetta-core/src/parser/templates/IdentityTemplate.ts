/**
 * AT·OM — IdentityTemplate
 * TranslatorTemplate pour l'Identité Souveraine (Sphère 1: 111Hz)
 *
 * "Si tu ne possèdes pas tes données, tu ne te possèdes pas toi-même."
 *
 * Chaque utilisateur est PROPRIÉTAIRE ABSOLU de ses données.
 * Ce n'est pas une fonctionnalité. C'est un DROIT INALIÉNABLE.
 *
 * Transition: Ministère de l'Identité → Sphère 1
 *   - Registre naissances → Blockchain d'identité (Hedera)
 *   - Cartes d'identité → DID (Decentralized Identity)
 *   - Passeports → Credentials vérifiables
 *   - Nationalité → Citoyenneté de l'Arche (opt-in)
 */

import {
  type SphereId,
  type ResonanceLevel,
  type ResonanceRank,
  type NFTTier,
  type VerifiableCredential,
  SPHERES,
  RESONANCE_MATRIX,
  SACRED_FREQUENCIES,
  RESONANCE_RANKS,
  NFT_TIERS,
} from '../../types/atom-types';
import { type TranslatorTemplate, type ParserContext, RosettaParser } from '../RosettaParser';

// ═══════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════

export type IdentityAction =
  | 'CREATE_DID'          // Création de l'identité décentralisée
  | 'VERIFY_CREDENTIAL'   // Vérification d'un credential
  | 'ISSUE_CREDENTIAL'    // Émission d'un credential
  | 'REVOKE_CREDENTIAL'   // Révocation
  | 'UPDATE_PROFILE'      // Mise à jour du profil
  | 'MINT_NFT'            // Mint d'un NFT de contribution
  | 'SOVEREIGNTY_CLAIM'   // Réclamation de souveraineté
  | 'EXPORT_DATA'         // Export de toutes ses données
  | 'DELETE_DATA';         // Droit à l'oubli

export interface IdentityInput {
  action: IdentityAction;
  did: string;
  display_name: string;
  resonance_score: number;
  rank: ResonanceRank;
  nft_tier: NFTTier | null;
  spheres_active: SphereId[];
  credentials_count: number;
  is_sovereign: boolean;             // A réclamé sa souveraineté
  is_verified: boolean;              // Identité vérifiée par pairs
  privacy_level: 'PUBLIC' | 'SELECTIVE' | 'ANONYMOUS';
  credential?: VerifiableCredential; // Si action implique un credential
  metadata?: Record<string, unknown>;
}

// ═══════════════════════════════════════════════════════════
// TEMPLATE
// ═══════════════════════════════════════════════════════════

export const IdentityTemplate: TranslatorTemplate<IdentityInput> = {
  domain: 'identity',

  toTech(input, ctx) {
    const rankInfo = RESONANCE_RANKS[input.rank];
    const nftInfo = input.nft_tier ? NFT_TIERS[input.nft_tier] : null;

    return {
      schema_version: '1.0',
      data_type: 'identity_action',
      values: {
        action: input.action,
        did: input.did,
        resonance_score: input.resonance_score,
        rank: input.rank,
        rank_rights: rankInfo.rights,
        ai_token_quota: rankInfo.ai_token_quota,
        nft_tier: input.nft_tier,
        nft_edition_max: nftInfo?.max_edition ?? null,
        nft_ur_bonus_pct: nftInfo?.ur_bonus_pct ?? 0,
        spheres_active: input.spheres_active,
        credentials_count: input.credentials_count,
        is_sovereign: input.is_sovereign,
        is_verified: input.is_verified,
        privacy_level: input.privacy_level,
        credential: input.credential ?? null,
        system_frequency: ctx.system_frequency,
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, _ctx) {
    const rankInfo = RESONANCE_RANKS[input.rank];
    const actionLabel = ACTION_LABELS[input.action];

    let narrative: string;

    if (input.action === 'CREATE_DID') {
      narrative = `Naissance d'une identité souveraine : ${input.display_name}. `;
      narrative += `Tu es maintenant propriétaire de tes données. Tes clés, ta responsabilité, ta liberté.`;
    } else if (input.action === 'SOVEREIGNTY_CLAIM') {
      narrative = `${input.display_name} réclame sa souveraineté dans l'Arche. `;
      narrative += `"Si tu ne possèdes pas tes données, tu ne te possèdes pas toi-même."`;
    } else if (input.action === 'MINT_NFT' && input.nft_tier) {
      const nft = NFT_TIERS[input.nft_tier];
      narrative = `NFT "${nft.label}" attribué à ${input.display_name}. `;
      narrative += `Édition limitée à ${nft.max_edition === 'unlimited' ? '∞' : nft.max_edition}. `;
      narrative += `Bonus UR: ${nft.ur_bonus_pct}%. Cette graine grandira avec l'Arche.`;
    } else if (input.action === 'VERIFY_CREDENTIAL' && input.credential) {
      narrative = `Credential vérifié : ${input.credential.type} pour ${input.display_name}. `;
      narrative += `Preuve enregistrée de manière immuable. Pas besoin de diplôme — la compétence parle.`;
    } else if (input.action === 'EXPORT_DATA') {
      narrative = `${input.display_name} exporte l'intégralité de ses données. `;
      narrative += `C'est ton DROIT. Tu peux partir avec tout. Aucune donnée retenue.`;
    } else if (input.action === 'DELETE_DATA') {
      narrative = `${input.display_name} exerce son droit à l'oubli. `;
      narrative += `Les données personnelles sont supprimées. Les preuves blockchain restent anonymisées.`;
    } else {
      narrative = `${actionLabel} pour ${input.display_name} (${rankInfo.label}). `;
      narrative += `Résonance: ${input.resonance_score}/100. `;
      narrative += `${input.spheres_active.length} sphère(s) active(s).`;
    }

    const tone = input.action === 'CREATE_DID' || input.action === 'SOVEREIGNTY_CLAIM'
      ? 'celebratoire' as const
      : input.action === 'DELETE_DATA' ? 'sacre' as const
      : 'neutre' as const;

    return {
      narrative,
      explanation: `Action: ${actionLabel}`,
      guide_steps: [
        `Rang: ${rankInfo.label} (score ${input.resonance_score}/100)`,
        `Droits: ${rankInfo.rights.join(', ')}`,
        `Quota IA: ${rankInfo.ai_token_quota === 'unlimited' ? 'Illimité' : rankInfo.ai_token_quota.toLocaleString()} tokens`,
        `Souveraineté: ${input.is_sovereign ? 'Réclamée ✓' : 'Non réclamée'}`,
        `Confidentialité: ${PRIVACY_LABELS[input.privacy_level]}`,
      ],
      emotional_tone: tone,
      language: 'fr',
    };
  },

  toSpirit(input, _ctx) {
    // Sphère 1 (111Hz) comme base, modulée par le rank
    const rankLevel: Record<ResonanceRank, ResonanceLevel> = {
      INITIE: 1,      // 111Hz
      CITOYEN: 2,     // 222Hz
      FONDATEUR: 4,   // 444Hz
      GARDIEN: 7,     // 777Hz
      ARCHITECTE: 9,  // 999Hz
    };

    const level = rankLevel[input.rank];
    const resonance = RESONANCE_MATRIX[level];

    return {
      frequency_hz: resonance.hz,
      resonance_level: level,
      color: resonance.color,
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
// CONSTANTES & UTILITAIRES
// ═══════════════════════════════════════════════════════════

const ACTION_LABELS: Record<IdentityAction, string> = {
  CREATE_DID: 'Création DID',
  VERIFY_CREDENTIAL: 'Vérification de credential',
  ISSUE_CREDENTIAL: 'Émission de credential',
  REVOKE_CREDENTIAL: 'Révocation de credential',
  UPDATE_PROFILE: 'Mise à jour du profil',
  MINT_NFT: 'Mint NFT de contribution',
  SOVEREIGNTY_CLAIM: 'Réclamation de souveraineté',
  EXPORT_DATA: 'Export de données',
  DELETE_DATA: 'Droit à l\'oubli',
};

const PRIVACY_LABELS: Record<string, string> = {
  PUBLIC: 'Public — profil visible par tous',
  SELECTIVE: 'Sélectif — tu choisis ce qui est visible',
  ANONYMOUS: 'Anonyme — seul ton DID est visible',
};

/**
 * Vérifie si un credential est encore valide
 */
export function isCredentialValid(credential: VerifiableCredential): boolean {
  if (credential.expires_at && Date.now() > credential.expires_at) return false;
  return true;
}

/**
 * Calcule le NFT Tier basé sur la contribution totale
 */
export function getNFTTierFromContribution(amount: number): NFTTier | null {
  if (amount >= 10000) return 'ARBRE';
  if (amount >= 2000) return 'RACINE';
  if (amount >= 500) return 'BRANCHE';
  if (amount >= 100) return 'POUSSE';
  if (amount >= 10) return 'GRAINE';
  return null;
}

/**
 * Vérifie les droits d'accès basés sur la version de lecture
 */
export function canAccessVersion(resonance_score: number, version: string): boolean {
  switch (version) {
    case 'EXECUTIVE': return true;
    case 'PHILOSOPHIQUE': return resonance_score >= 20;
    case 'INITIATIQUE': return resonance_score >= 40;
    case 'MYTHIQUE': return resonance_score >= 80;
    default: return false;
  }
}

/**
 * Génère un rapport de souveraineté pour un utilisateur
 */
export function generateSovereigntyReport(input: IdentityInput): {
  score: number;
  status: 'NON_SOUVERAIN' | 'EN_TRANSITION' | 'SOUVERAIN' | 'ARCHITECTE';
  checklist: { item: string; done: boolean }[];
} {
  const checklist = [
    { item: 'DID créé', done: !!input.did },
    { item: 'Identité vérifiée par pairs', done: input.is_verified },
    { item: 'Souveraineté réclamée', done: input.is_sovereign },
    { item: 'Au moins 1 credential vérifié', done: input.credentials_count > 0 },
    { item: 'Au moins 1 sphère active', done: input.spheres_active.length > 0 },
    { item: 'Résonance ≥ 20 (Citoyen)', done: input.resonance_score >= 20 },
    { item: 'Résonance ≥ 40 (Fondateur)', done: input.resonance_score >= 40 },
    { item: 'NFT de contribution', done: input.nft_tier !== null },
  ];

  const done = checklist.filter(c => c.done).length;
  const score = Math.round((done / checklist.length) * 100);

  const status = score >= 90 ? 'ARCHITECTE'
    : score >= 60 ? 'SOUVERAIN'
    : score >= 30 ? 'EN_TRANSITION'
    : 'NON_SOUVERAIN';

  return { score, status, checklist };
}
