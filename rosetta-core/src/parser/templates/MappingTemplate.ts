/**
 * AT·OM — MappingTemplate
 * TranslatorTemplate pour le AT-OM Mapping (Cartographie Universelle)
 *
 * "Nous ne réécrivons pas l'histoire. Nous la DÉCHIFFRONS."
 *
 * 6 couches de lecture pour chaque événement :
 *   1. ÉVÉNEMENTS  — Faits vérifiables (gravés sur blockchain)
 *   2. NARRATIFS   — Interprétations multiples (pas de version unique)
 *   3. PATTERNS    — Récurrences identifiées par l'IA
 *   4. CAUSALITÉS  — Chaînes cause→effet
 *   5. VIBRATIONS  — Fréquence vibratoire des époques
 *   6. PROJECTIONS — Scénarios futurs possibles
 */

import {
  type SphereId,
  type ResonanceLevel,
  type MappingLayer,
  type MappingSource,
  type UniversalLaw,
  SPHERES,
  RESONANCE_MATRIX,
  SACRED_FREQUENCIES,
  MAPPING_LAYERS_META,
  UNIVERSAL_LAWS,
} from '../../types/atom-types';
import { type TranslatorTemplate, type ParserContext, RosettaParser } from '../RosettaParser';

// ═══════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════

export type HistoricalEra = 'CYCLES_NATURELS' | 'EMPIRES' | 'REVOLUTIONS' | 'TRANSITION' | 'HARMONIE';

export interface MappingInput {
  entry_id: string;
  title: string;
  description: string;
  layer: MappingLayer;
  era: HistoricalEra;
  epoch_start: number;              // Year or timestamp
  epoch_end: number | null;          // null = ongoing
  sphere_connections: SphereId[];
  sources: MappingSource[];
  narratives: string[];              // Multiple perspectives
  patterns_linked: string[];         // IDs of connected pattern entries
  causal_chain?: { cause: string; effect: string }[];
  laws_manifested: UniversalLaw[];   // Which universal laws are visible
  frequency_estimate: number;        // Hz estimate for the era/event
}

// ═══════════════════════════════════════════════════════════
// TEMPLATE
// ═══════════════════════════════════════════════════════════

export const MappingTemplate: TranslatorTemplate<MappingInput> = {
  domain: 'mapping',

  toTech(input, ctx) {
    const verifiedSources = input.sources.filter(s => s.verified_on_chain);
    const avgCredibility = input.sources.length > 0
      ? input.sources.reduce((sum, s) => sum + s.credibility_score, 0) / input.sources.length
      : 0;

    return {
      schema_version: '1.0',
      data_type: 'mapping_entry',
      values: {
        entry_id: input.entry_id,
        layer: input.layer,
        layer_index: MAPPING_LAYERS_META[input.layer].index,
        era: input.era,
        era_pattern: ERA_PATTERNS[input.era],
        epoch_start: input.epoch_start,
        epoch_end: input.epoch_end,
        sphere_connections: input.sphere_connections,
        sources_total: input.sources.length,
        sources_verified: verifiedSources.length,
        avg_credibility: Math.round(avgCredibility),
        narratives_count: input.narratives.length,
        patterns_linked: input.patterns_linked,
        causal_chain: input.causal_chain ?? [],
        laws_manifested: input.laws_manifested,
        frequency_estimate: input.frequency_estimate,
        system_frequency: ctx.system_frequency,
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, _ctx) {
    const layerMeta = MAPPING_LAYERS_META[input.layer];
    const eraLabel = ERA_LABELS[input.era];
    const sphereNames = input.sphere_connections.map(s => SPHERES[s].label).join(', ');

    let narrative = `[Couche ${layerMeta.index}: ${layerMeta.label}] `;
    narrative += `"${input.title}" — Ère: ${eraLabel}. `;
    narrative += `Sphères connectées: ${sphereNames}. `;

    if (input.narratives.length > 1) {
      narrative += `${input.narratives.length} perspectives documentées — `;
      narrative += `nous ne choisissons pas UNE vérité, nous les préservons toutes. `;
    }

    if (input.patterns_linked.length > 0) {
      narrative += `${input.patterns_linked.length} patterns historiques connectés. `;
    }

    if (input.laws_manifested.length > 0) {
      const lawLabels = input.laws_manifested.map(l => UNIVERSAL_LAWS[l].maxim).join(' | ');
      narrative += `Lois universelles manifestées: ${lawLabels}. `;
    }

    if (input.causal_chain && input.causal_chain.length > 0) {
      narrative += `Chaîne causale: `;
      narrative += input.causal_chain.map(c => `${c.cause} → ${c.effect}`).join(' → ') + '. ';
    }

    const tone = input.layer === 'PROJECTIONS' ? 'encourageant' as const
      : input.layer === 'VIBRATIONS' ? 'sacre' as const
      : input.layer === 'PATTERNS' ? 'alerte' as const
      : 'neutre' as const;

    return {
      narrative,
      explanation: input.description,
      guide_steps: [
        `Couche: ${layerMeta.label} — ${layerMeta.description}`,
        `Ère: ${eraLabel} (${input.epoch_start}${input.epoch_end ? ' → ' + input.epoch_end : ' → présent'})`,
        `Sources: ${input.sources.length} (${input.sources.filter(s => s.verified_on_chain).length} vérifiées on-chain)`,
        `Fréquence vibratoire estimée: ${input.frequency_estimate}Hz`,
      ],
      emotional_tone: tone,
      language: 'fr',
    };
  },

  toSpirit(input, _ctx) {
    // La fréquence est basée sur l'estimation vibratoire de l'ère/événement
    const level = Math.max(1, Math.min(9, Math.round(input.frequency_estimate / 111))) as ResonanceLevel;
    const resonance = RESONANCE_MATRIX[level];

    return {
      frequency_hz: resonance.hz,
      resonance_level: level,
      color: ERA_COLORS[input.era],
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

const ERA_LABELS: Record<HistoricalEra, string> = {
  CYCLES_NATURELS: 'Cycles Naturels (Tribus, harmonie avec la Terre)',
  EMPIRES: 'Empires & Contrôle (Rome, Féodalisme, Colonialisme)',
  REVOLUTIONS: 'Révolutions & Rupture (1789, 1917, 1968)',
  TRANSITION: 'Transition — Nous sommes ici (2020-2050)',
  HARMONIE: 'Harmonie Possible (Souveraineté Collective)',
};

const ERA_PATTERNS: Record<HistoricalEra, string> = {
  CYCLES_NATURELS: 'Décentralisé, Organique',
  EMPIRES: 'Centralisation, Hiérarchie',
  REVOLUTIONS: 'Réaction, Chaos',
  TRANSITION: 'Transition, Choix',
  HARMONIE: 'Synthèse, Harmonie',
};

const ERA_COLORS: Record<HistoricalEra, string> = {
  CYCLES_NATURELS: '#228B22', // Vert forêt
  EMPIRES: '#8B0000',         // Rouge sombre
  REVOLUTIONS: '#FF4500',     // Orange feu
  TRANSITION: '#4169E1',      // Bleu royal
  HARMONIE: '#FFD700',        // Or
};

/**
 * Calcule le score de crédibilité d'un ensemble de sources.
 * Sources multiples, diversifiées et vérifiées = score élevé.
 */
export function calculateSourceCredibility(sources: MappingSource[]): number {
  if (sources.length === 0) return 0;

  const avgScore = sources.reduce((sum, s) => sum + s.credibility_score, 0) / sources.length;
  const verifiedBonus = sources.filter(s => s.verified_on_chain).length / sources.length * 20;
  const diversityBonus = new Set(sources.map(s => s.type)).size / 4 * 20; // 4 types possibles

  return Math.min(100, Math.round(avgScore + verifiedBonus + diversityBonus));
}

/**
 * Identifie les patterns récurrents dans un ensemble d'entrées de mapping.
 * Retourne les connexions (causal chains) les plus fréquentes.
 */
export function detectPatterns(entries: MappingInput[]): {
  recurring_causes: string[];
  cycle_indicators: string[];
  law_frequencies: Record<string, number>;
} {
  const causeCount: Record<string, number> = {};
  const lawCount: Record<string, number> = {};

  for (const entry of entries) {
    if (entry.causal_chain) {
      for (const chain of entry.causal_chain) {
        causeCount[chain.cause] = (causeCount[chain.cause] ?? 0) + 1;
      }
    }
    for (const law of entry.laws_manifested) {
      lawCount[law] = (lawCount[law] ?? 0) + 1;
    }
  }

  const recurring = Object.entries(causeCount)
    .filter(([_, count]) => count >= 2)
    .sort((a, b) => b[1] - a[1])
    .map(([cause]) => cause);

  const cycles = recurring.length > 0
    ? ['Pattern cyclique détecté: certaines causes se répètent à travers les ères']
    : [];

  return {
    recurring_causes: recurring,
    cycle_indicators: cycles,
    law_frequencies: lawCount,
  };
}

/**
 * Détermine l'ère historique d'un événement basé sur sa date.
 */
export function getEraFromDate(year: number): HistoricalEra {
  if (year < -3000) return 'CYCLES_NATURELS';
  if (year < 1750) return 'EMPIRES';
  if (year < 2020) return 'REVOLUTIONS';
  if (year < 2050) return 'TRANSITION';
  return 'HARMONIE';
}
