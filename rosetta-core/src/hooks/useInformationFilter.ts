/**
 * AT·OM — useInformationFilter
 * Hook de tri de l'information — Chapitre 11 de la Vision Complète
 *
 * "Nous ne disons pas aux gens quoi penser.
 *  Nous leur donnons les outils pour VOIR CLAIREMENT."
 *
 * 5 niveaux de tri :
 *   1. Cohérence interne
 *   2. Cohérence externe (sources)
 *   3. Diversité des sources
 *   4. Transparence méthodologique
 *   5. Fiabilité de l'auteur
 *
 * + Détection d'intention : INFORMATIF | PERSUASIF | MANIPULATIF | COMMERCIAL | DIVISIF
 * + Filtre SERVIR vs EXTRAIRE
 */

import { useCallback } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import type { ContentIntention, InformationResonanceScore } from '../types/atom-types';

export function useInformationFilter() {
  const { informationFilter, intentionGuard, universalLawValidator } = useATOM();

  // ─── Analyser un contenu ────────────────────────────────
  const analyzeContent = useCallback((content: {
    text: string;
    author_id?: string;
    sources?: { reference: string; verified: boolean }[];
    methodology_disclosed?: boolean;
    author_history_score?: number;
  }): InformationResonanceScore => {
    return informationFilter.analyzeResonance(content);
  }, [informationFilter]);

  // ─── Détecter l'intention ───────────────────────────────
  const detectIntention = useCallback((text: string): ContentIntention => {
    return informationFilter.detectIntention(text);
  }, [informationFilter]);

  // ─── Vérifier le seuil ─────────────────────────────────
  const meetsThreshold = useCallback((
    score: InformationResonanceScore,
    threshold: number = 50,
  ): boolean => {
    return informationFilter.meetsResonanceThreshold(score, threshold);
  }, [informationFilter]);

  // ─── Évaluer une action (SERVIR vs EXTRAIRE) ───────────
  const evaluateIntention = useCallback((action: {
    description: string;
    sert_epanouissement?: boolean;
    respecte_souverainete?: boolean;
    est_transparent?: boolean;
    cree_plus_de_valeur?: boolean;
    aligne_spheres?: boolean;
    visible_par_tous?: boolean;
  }) => {
    return intentionGuard.evaluate(action);
  }, [intentionGuard]);

  // ─── Vérifier les 7 principes immuables ─────────────────
  const checkPrinciples = useCallback((action: string) => {
    return intentionGuard.checkPrinciples(action);
  }, [intentionGuard]);

  return {
    // Tri de l'information
    analyzeContent,
    detectIntention,
    meetsThreshold,

    // Filtre d'intention
    evaluateIntention,
    checkPrinciples,
    immutablePrinciples: intentionGuard.IMMUTABLE_PRINCIPLES,

    // Lois universelles (validation)
    universalLawValidator,
  };
}
