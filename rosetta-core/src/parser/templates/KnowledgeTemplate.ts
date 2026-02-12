/**
 * AT·OM — KnowledgeTemplate
 * TranslatorTemplate pour le Système Digestif (DigestiveSystem)
 *
 * "Toute connaissance ingérée doit être digérée en 3 dimensions
 *  pour nourrir l'Arche de manière complète."
 *
 * Ce template traduit la ChewedFood — le contenu web structuré
 * après mastication par le DigestiveSystem — en les 3 dimensions
 * de la Pierre de Rosette :
 *   - TECH  → Article structuré, métadonnées vérifiables
 *   - PEOPLE → Narratif humain, guide de recherche
 *   - SPIRIT → Fréquence vibratoire dérivée du titre (Arithmos)
 */

import {
  type ResonanceLevel,
  RESONANCE_MATRIX,
  SACRED_FREQUENCIES,
} from '../../types/atom-types';
import type { ChewedFood } from '../../types/atom-types';
import { type TranslatorTemplate, type ParserContext, RosettaParser } from '../RosettaParser';

// ═══════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════

/** Mots-clés déclencheurs pour le ton 'alerte' (santé / sécurité) */
const ALERTE_KEYWORDS = [
  'santé', 'health', 'sécurité', 'security', 'danger',
  'urgence', 'emergency', 'risque', 'risk', 'maladie',
  'disease', 'virus', 'pandémie', 'pandemic', 'alerte',
];

/** Mots-clés déclencheurs pour le ton 'encourageant' (éducation / culture) */
const ENCOURAGEANT_KEYWORDS = [
  'éducation', 'education', 'culture', 'apprentissage', 'learning',
  'formation', 'training', 'savoir', 'knowledge', 'science',
  'recherche', 'research', 'découverte', 'discovery', 'innovation',
];

// ═══════════════════════════════════════════════════════════
// TEMPLATE
// ═══════════════════════════════════════════════════════════

export const KnowledgeTemplate: TranslatorTemplate<ChewedFood> = {
  domain: 'knowledge',

  toTech(input, ctx) {
    const verified_source_count = input.sources.filter(s => s.verified).length;

    return {
      schema_version: '1.0',
      data_type: 'knowledge_article',
      values: {
        title: input.title,
        word_count: input.word_count,
        source_count: input.sources.length,
        verified_source_count,
        keywords: input.keywords,
        language: input.language,
        ...(input.author != null ? { author: input.author } : {}),
        ...(input.published_at != null ? { published_at: input.published_at } : {}),
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, _ctx) {
    // Narrative : extrait des 200 premiers caractères du corps
    const truncated = input.body.length > 200;
    const narrative = truncated
      ? input.body.slice(0, 200) + '...'
      : input.body;

    // Explication avec ou sans auteur
    const explanation = input.author
      ? `Article de ${input.author} sur \u00ab ${input.title} \u00bb`
      : `Contenu sur \u00ab ${input.title} \u00bb`;

    // Pistes de recherche basées sur les 5 premiers mots-clés
    const guide_steps = input.keywords
      .slice(0, 5)
      .map(kw => `Explorer le concept : ${kw}`);

    // Tonalité émotionnelle basée sur les mots-clés
    const emotional_tone = detectEmotionalTone(input.keywords);

    return {
      narrative,
      explanation,
      guide_steps,
      emotional_tone,
      language: input.language,
    };
  },

  toSpirit(input, _ctx) {
    // Réduction pythagoricienne du titre → niveau de résonance (1-9)
    const level: ResonanceLevel = RosettaParser.computeArithmos(input.title);
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
// UTILITAIRES
// ═══════════════════════════════════════════════════════════

/**
 * Détermine la tonalité émotionnelle à partir des mots-clés.
 *   - Si un mot-clé touche la santé / sécurité → 'alerte'
 *   - Si un mot-clé touche l'éducation / culture → 'encourageant'
 *   - Sinon → 'neutre'
 */
function detectEmotionalTone(
  keywords: string[],
): 'neutre' | 'encourageant' | 'alerte' {
  const lower = keywords.map(kw => kw.toLowerCase());

  if (lower.some(kw => ALERTE_KEYWORDS.includes(kw))) {
    return 'alerte';
  }

  if (lower.some(kw => ENCOURAGEANT_KEYWORDS.includes(kw))) {
    return 'encourageant';
  }

  return 'neutre';
}
