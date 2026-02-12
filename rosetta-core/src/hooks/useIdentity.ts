/**
 * AT·OM — useIdentity
 * Hook d'identité souveraine — DID, credentials, souveraineté des données
 *
 * "Si tu ne possèdes pas tes données, tu ne te possèdes pas toi-même."
 *
 * Le même flux Rosetta circule ici :
 *   TECH   → Payload JSON (DID, credentials, actions)
 *   PEOPLE → Narration humaine ("Marie a revendiqué sa souveraineté")
 *   SPIRIT → Fréquence liée au rang (INITIÉ=111Hz → ARCHITECTE=999Hz)
 */

import { useCallback, useMemo } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import {
  isCredentialValid,
  getNFTTierFromContribution,
  canAccessVersion,
  generateSovereigntyReport,
} from '../parser/templates/IdentityTemplate';
import type {
  SovereignIdentity,
  VerifiableCredential,
  ReadingVersion,
  ResonanceRank,
  NFTTier,
} from '../types/atom-types';
import { VibrationalMotor } from '../engines/VibrationalMotor';

export function useIdentity() {
  const { state, dispatch, parser } = useATOM();
  const { identity } = state;

  // ─── Créer un DID ──────────────────────────────────────
  const createDID = useCallback((params: {
    display_name: string;
    avatar_hash?: string;
  }) => {
    const did = `did:atom:${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;

    const sovereignIdentity: SovereignIdentity = {
      did,
      display_name: params.display_name,
      avatar_hash: params.avatar_hash ?? '',
      resonance_score: 0,
      rank: 'INITIE',
      nft_tier: null,
      spheres_active: [],
      credentials: [],
      created_at: Date.now(),
      is_sovereign: false,
    };

    // Traduire par Rosetta (3 dimensions)
    parser.translate('identity', {
      action: 'CREATE_DID',
      did,
      display_name: params.display_name,
      resonance_score: 0,
    }, 'TECH', did);

    dispatch({
      type: 'IDENTITY_UPDATE',
      payload: {
        sovereign_identity: sovereignIdentity,
        sovereignty_status: 'EN_TRANSITION',
      },
    });

    return { success: true, did, identity: sovereignIdentity };
  }, [dispatch, parser]);

  // ─── Revendiquer la souveraineté ───────────────────────
  const claimSovereignty = useCallback(() => {
    if (!identity.sovereign_identity) {
      return { success: false, reason: 'Aucune identité créée' };
    }

    const report = generateSovereigntyReport(identity.sovereign_identity);

    if (report.score < 50) {
      return { success: false, reason: 'Score de souveraineté insuffisant', report };
    }

    const updated: SovereignIdentity = {
      ...identity.sovereign_identity,
      is_sovereign: true,
    };

    dispatch({
      type: 'IDENTITY_UPDATE',
      payload: {
        sovereign_identity: updated,
        sovereignty_status: 'SOUVERAIN',
      },
    });

    return { success: true, report };
  }, [identity, dispatch]);

  // ─── Mettre à jour le score de résonance ───────────────
  const updateResonanceScore = useCallback((components: {
    activity: number;
    contribution: number;
    tenure: number;
    investment: number;
    referral: number;
  }) => {
    if (!identity.sovereign_identity) return;

    const score = VibrationalMotor.computeResonanceScore(components);
    const rank = VibrationalMotor.getRank(score);

    const updated: SovereignIdentity = {
      ...identity.sovereign_identity,
      resonance_score: score,
      rank,
    };

    const sovereigntyStatus =
      rank === 'ARCHITECTE' ? 'ARCHITECTE' as const :
      updated.is_sovereign ? 'SOUVERAIN' as const :
      score >= 20 ? 'EN_TRANSITION' as const :
      'NON_SOUVERAIN' as const;

    dispatch({
      type: 'IDENTITY_UPDATE',
      payload: {
        sovereign_identity: updated,
        sovereignty_status: sovereigntyStatus,
      },
    });
  }, [identity, dispatch]);

  // ─── Vérificateurs ──────────────────────────────────────
  const checkVersionAccess = useCallback((version: ReadingVersion) => {
    const score = identity.sovereign_identity?.resonance_score ?? 0;
    return canAccessVersion(score, version);
  }, [identity]);

  const checkNFTTier = useCallback((contribution: number): NFTTier | null => {
    return getNFTTierFromContribution(contribution);
  }, []);

  const getSovereigntyReport = useCallback(() => {
    if (!identity.sovereign_identity) return null;
    return generateSovereigntyReport(identity.sovereign_identity);
  }, [identity]);

  // ─── Métriques dérivées ─────────────────────────────────
  const resonanceScore = useMemo(() =>
    identity.sovereign_identity?.resonance_score ?? 0,
  [identity]);

  const rank = useMemo(() =>
    identity.sovereign_identity?.rank ?? 'INITIE' as ResonanceRank,
  [identity]);

  const isSovereign = useMemo(() =>
    identity.sovereign_identity?.is_sovereign ?? false,
  [identity]);

  return {
    // État
    identity: identity.sovereign_identity,
    credentialsCount: identity.credentials_count,
    sovereigntyStatus: identity.sovereignty_status,
    resonanceScore,
    rank,
    isSovereign,

    // Actions
    createDID,
    claimSovereignty,
    updateResonanceScore,

    // Vérificateurs
    checkVersionAccess,
    checkNFTTier,
    isCredentialValid,
    getSovereigntyReport,
    getNFTTierFromContribution,
    canAccessVersion,
  };
}
