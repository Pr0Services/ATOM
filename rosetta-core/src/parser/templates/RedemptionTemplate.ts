/**
 * AT·OM — RedemptionTemplate (PRI)
 * Passerelle de Rédemption Institutionnelle
 * Traduction tri-dimensionnelle des contributions institutionnelles
 * via le protocole du "Lavage par la Lumière"
 *
 * "Ce qui est en bas est comme ce qui est en haut" — Table d'Émeraude
 */

import {
  type ResonanceLevel,
  type TechPayload,
  type PeoplePayload,
  type SpiritPayload,
  type SphereId,
  type AlchemyStage,
  SACRED_FREQUENCIES,
  RESONANCE_MATRIX,
  SPHERES,
} from '../../types/atom-types';

import {
  type TranslatorTemplate,
  type ParserContext,
  RosettaParser,
} from '../RosettaParser';

// ═══════════════════════════════════════════════════════════
// TYPES — Passerelle de Rédemption Institutionnelle
// ═══════════════════════════════════════════════════════════

/** Type de contribution institutionnelle */
export type ContributionType = 'GRANT' | 'REDEMPTION' | 'PARTNERSHIP' | 'RESTITUTION';

/** Statut du processus de rédemption */
export type RedemptionStatus =
  | 'SUBMITTED'
  | 'UNDER_AUDIT'
  | 'ACCEPTED'
  | 'REJECTED'
  | 'ESCROW'
  | 'COMPLETED'
  | 'REVOKED';

/** Entrée de données pour une rédemption institutionnelle */
export interface RedemptionInput {
  entity_name: string;
  entity_type: string;
  contribution_type: ContributionType;
  amount_fiat: number;
  currency: string;
  impact_sector: string;
  target_sphere: SphereId;
  description: string;
  trust_score: number;         // 0-100
  alchemy_stage_index: number; // 1-7
  is_public_disclosure: boolean;
}

// ═══════════════════════════════════════════════════════════
// CONSTANTES — Table d'Émeraude Institutionnelle
// ═══════════════════════════════════════════════════════════

/**
 * Les 7 étapes alchimiques appliquées à la rédemption institutionnelle.
 * Chaque étape augmente le modificateur de résonance, reflétant
 * la purification progressive de l'intention vers l'Or.
 */
export const ALCHEMY_STAGES: {
  name: AlchemyStage;
  index: number;
  description_fr: string;
  resonance_modifier: number;
}[] = [
  {
    name: 'CALCINATION',
    index: 1,
    description_fr: 'Destruction des anciennes structures — l\'institution reconnaît ses torts',
    resonance_modifier: 0.1,
  },
  {
    name: 'DISSOLUTION',
    index: 2,
    description_fr: 'Dissolution des mécanismes opaques — transparence naissante',
    resonance_modifier: 0.25,
  },
  {
    name: 'SEPARATION',
    index: 3,
    description_fr: 'Séparation du vrai et du faux — audit des intentions réelles',
    resonance_modifier: 0.4,
  },
  {
    name: 'CONJUNCTION',
    index: 4,
    description_fr: 'Union des forces — alignement entre promesse et action',
    resonance_modifier: 0.55,
  },
  {
    name: 'FERMENTATION',
    index: 5,
    description_fr: 'Germination du changement — les fruits de la rédemption apparaissent',
    resonance_modifier: 0.7,
  },
  {
    name: 'DISTILLATION',
    index: 6,
    description_fr: 'Purification finale — extraction de la quintessence de l\'engagement',
    resonance_modifier: 0.85,
  },
  {
    name: 'COAGULATION',
    index: 7,
    description_fr: 'Cristallisation en Or — rédemption complète, confiance restaurée',
    resonance_modifier: 1.0,
  },
];

/**
 * Pondération des contributions.
 * La RESTITUTION pèse le plus car elle guérit davantage :
 * rendre ce qui a été pris amplifie la résonance.
 */
export const CONTRIBUTION_WEIGHTS: Record<ContributionType, number> = {
  GRANT: 1.0,
  REDEMPTION: 1.2,
  PARTNERSHIP: 0.8,
  RESTITUTION: 1.5,
};

// ═══════════════════════════════════════════════════════════
// FONCTIONS — Calculs de Résonance
// ═══════════════════════════════════════════════════════════

/**
 * Calcule les Unités de Résonance (UR) d'une contribution institutionnelle.
 *
 * La formule alchimique :
 *   base = amountFiat * 0.001 (1000 fiat = 1 UR de base)
 *   × trustFactor (confiance amplifie la résonance)
 *   × alchemyFactor (progression alchimique)
 *   × phiBonus (Nombre d'Or pour les stades avancés >= 5)
 *   × transparencyBonus (le protocole "Lavage par la Lumière")
 *   × contributionWeight (la nature de la contribution)
 *
 * Plafond : 999 (fréquence SOURCE — on ne dépasse pas l'Unité)
 */
export function calculateResonanceUnits(
  amountFiat: number,
  trustScore: number,
  alchemyIndex: number,
  contributionType: ContributionType,
  isPublicDisclosure: boolean,
): number {
  const base = amountFiat * 0.001;
  const trustFactor = 1 + (trustScore / 100) * 0.5;
  const alchemyFactor = alchemyIndex / 7;
  const phiBonus = alchemyIndex >= 5 ? SACRED_FREQUENCIES.PHI : 1.0;
  const transparencyBonus = isPublicDisclosure ? 1.111 : 1.0;
  const contributionWeight = CONTRIBUTION_WEIGHTS[contributionType];

  const result =
    base * trustFactor * alchemyFactor * phiBonus * transparencyBonus * contributionWeight;

  // Plafond SOURCE : 999 — la fréquence d'unité maximale
  return Math.min(result, 999);
}

/**
 * Détermine l'étape alchimique d'une institution en fonction de
 * son score de confiance et du nombre de rédemptions complétées.
 *
 * La COAGULATION (Or) ne s'atteint que par la confiance ET l'expérience :
 * trust >= 90 ET au moins 7 rédemptions accomplies.
 */
export function getRedemptionAlchemyStage(
  trustScore: number,
  completedRedemptions: number,
): { stage: AlchemyStage; index: number } {
  if (trustScore < 15) return { stage: 'CALCINATION', index: 1 };
  if (trustScore < 30) return { stage: 'DISSOLUTION', index: 2 };
  if (trustScore < 45) return { stage: 'SEPARATION', index: 3 };
  if (trustScore < 60) return { stage: 'CONJUNCTION', index: 4 };
  if (trustScore < 75) return { stage: 'FERMENTATION', index: 5 };
  if (trustScore < 90) return { stage: 'DISTILLATION', index: 6 };
  if (trustScore >= 90 && completedRedemptions >= 7) return { stage: 'COAGULATION', index: 7 };
  // trust >= 90 mais pas assez de rédemptions → reste en DISTILLATION
  return { stage: 'DISTILLATION', index: 6 };
}

// ═══════════════════════════════════════════════════════════
// HELPERS INTERNES
// ═══════════════════════════════════════════════════════════

/**
 * Résout l'étape alchimique à partir de l'index fourni dans l'input.
 * Clampe entre 1 et 7.
 */
function resolveAlchemyStage(index: number): typeof ALCHEMY_STAGES[number] {
  const clamped = Math.max(1, Math.min(7, Math.round(index)));
  return ALCHEMY_STAGES[clamped - 1];
}

/**
 * Traduit le type de contribution en libellé français.
 */
function contributionLabel(type: ContributionType): string {
  const labels: Record<ContributionType, string> = {
    GRANT: 'subvention',
    REDEMPTION: 'rédemption',
    PARTNERSHIP: 'partenariat',
    RESTITUTION: 'restitution',
  };
  return labels[type];
}

/**
 * Détermine le ton émotionnel en fonction du stade alchimique.
 */
function resolveEmotionalTone(
  alchemyIndex: number,
): PeoplePayload['emotional_tone'] {
  if (alchemyIndex <= 2) return 'alerte';
  if (alchemyIndex <= 4) return 'neutre';
  if (alchemyIndex <= 6) return 'encourageant';
  return 'celebratoire';
}

// ═══════════════════════════════════════════════════════════
// REDEMPTION TEMPLATE — TranslatorTemplate<RedemptionInput>
// Passerelle de Rédemption Institutionnelle (PRI)
// ═══════════════════════════════════════════════════════════

export const RedemptionTemplate: TranslatorTemplate<RedemptionInput> = {
  domain: 'redemption',

  // ---------------------------------------------------------------
  // TECH (Grec) — JSON structuré pour smart contracts / APIs
  // Données complètes de la rédemption avec calculs de résonance
  // ---------------------------------------------------------------
  toTech(input: RedemptionInput, ctx: ParserContext): TechPayload {
    const stage = resolveAlchemyStage(input.alchemy_stage_index);
    const sphere = SPHERES[input.target_sphere];
    const resonanceUnits = calculateResonanceUnits(
      input.amount_fiat,
      input.trust_score,
      input.alchemy_stage_index,
      input.contribution_type,
      input.is_public_disclosure,
    );

    const values: Record<string, unknown> = {
      // Identité institutionnelle
      entity_name: input.entity_name,
      entity_type: input.entity_type,

      // Contribution
      contribution_type: input.contribution_type,
      contribution_weight: CONTRIBUTION_WEIGHTS[input.contribution_type],
      amount_fiat: input.amount_fiat,
      currency: input.currency,
      impact_sector: input.impact_sector,
      description: input.description,

      // Sphère cible
      target_sphere: input.target_sphere,
      sphere_label: sphere.label,
      sphere_frequency_hz: sphere.frequency,

      // Confiance et Alchimie
      trust_score: input.trust_score,
      alchemy_stage: stage.name,
      alchemy_stage_index: stage.index,
      alchemy_resonance_modifier: stage.resonance_modifier,

      // Calculs de résonance
      resonance_units: Math.round(resonanceUnits * 1000) / 1000,
      resonance_units_cap: 999,

      // Protocole de transparence
      is_public_disclosure: input.is_public_disclosure,
      transparency_protocol: input.is_public_disclosure
        ? 'LAVAGE_PAR_LA_LUMIERE'
        : 'STANDARD',

      // Conversion fiat → résonance
      conversion_rate: 0.001,
      phi_bonus_active: input.alchemy_stage_index >= 5,
      phi_value: SACRED_FREQUENCIES.PHI,

      // Métadonnées système
      system_frequency: ctx.system_frequency,
      registered_by: ctx.user_id,
    };

    return {
      schema_version: '1.0',
      data_type: 'redemption',
      values,
      timestamp: ctx.timestamp,
    };
  },

  // ---------------------------------------------------------------
  // PEOPLE (Démotique) — Narratif français accessible
  // Raconte l'histoire de la rédemption en langage humain
  // ---------------------------------------------------------------
  toPeople(input: RedemptionInput, _ctx: ParserContext): PeoplePayload {
    const stage = resolveAlchemyStage(input.alchemy_stage_index);
    const sphere = SPHERES[input.target_sphere];
    const resonanceUnits = calculateResonanceUnits(
      input.amount_fiat,
      input.trust_score,
      input.alchemy_stage_index,
      input.contribution_type,
      input.is_public_disclosure,
    );

    // Narratif principal
    const narrative =
      `L'institution ${input.entity_name} (${input.entity_type}) soumet une ` +
      `${contributionLabel(input.contribution_type)} de ${input.amount_fiat.toLocaleString('fr-FR')} ${input.currency} ` +
      `pour la sphère ${sphere.label}. ` +
      `Cette contribution génère ${Math.round(resonanceUnits * 100) / 100} Unités de Résonance ` +
      `dans le secteur ${input.impact_sector}.`;

    // Explication alchimique et confiance
    const trustDescription =
      input.trust_score < 30
        ? 'un indice de confiance faible — le chemin de purification est long'
        : input.trust_score < 60
          ? 'un indice de confiance modéré — la transformation est en cours'
          : input.trust_score < 90
            ? 'un indice de confiance élevé — la rédemption approche de sa cristallisation'
            : 'un indice de confiance exemplaire — la lumière est presque totale';

    const transparencyNote = input.is_public_disclosure
      ? ' Protocole de Lavage par la Lumière activé — la transparence amplifie la résonance.'
      : '';

    const explanation =
      `L'entité se trouve au stade alchimique de ${stage.name} (étape ${stage.index}/7) : ` +
      `${stage.description_fr}. ` +
      `Avec un score de confiance de ${input.trust_score}/100, cela représente ${trustDescription}.` +
      transparencyNote;

    // Guide en 4 étapes — chemin de rédemption
    const guide_steps: string[] = [
      `Soumission : La contribution de ${input.amount_fiat.toLocaleString('fr-FR')} ${input.currency} est enregistrée dans la sphère ${sphere.label} (${sphere.frequency} Hz).`,
      `Audit alchimique : Vérification au stade ${stage.name} — le modificateur de résonance est de ${stage.resonance_modifier}.`,
      `Transmutation : Conversion en ${Math.round(resonanceUnits * 100) / 100} Unités de Résonance via la formule sacrée (base × confiance × alchimie × phi × transparence × poids).`,
      `Intégration : Les Unités de Résonance sont absorbées par la sphère ${sphere.label}, activant les engrenages vers ${sphere.gear_connections.map(c => SPHERES[c].label).join(', ')}.`,
    ];

    // Ton émotionnel basé sur le stade alchimique
    const emotional_tone = resolveEmotionalTone(stage.index);

    return {
      narrative,
      explanation,
      guide_steps,
      emotional_tone,
      language: 'fr',
    };
  },

  // ---------------------------------------------------------------
  // SPIRIT (Hiéroglyphe) — Fréquence, géométrie sacrée, vibration
  // La dimension invisible de la rédemption
  // ---------------------------------------------------------------
  toSpirit(input: RedemptionInput, _ctx: ParserContext): SpiritPayload {
    const sphere = SPHERES[input.target_sphere];

    // Le niveau de résonance est dérivé de l'index de la sphère,
    // plafonné par la progression alchimique
    const sphereLevel = sphere.index as ResonanceLevel;
    const alchemyCap = Math.max(1, Math.min(9, input.alchemy_stage_index + 2));
    const effectiveLevel = Math.min(sphereLevel, alchemyCap) as ResonanceLevel;

    const resonance = RESONANCE_MATRIX[effectiveLevel];

    return {
      frequency_hz: resonance.hz,
      resonance_level: effectiveLevel,
      color: resonance.color,
      sacred_geometry: RosettaParser.geometryFor(effectiveLevel),
      vibration_signature: [
        SACRED_FREQUENCIES.ATOM_M,   // 44.4   — Masse / Matière
        SACRED_FREQUENCIES.ATOM_P,   // 161.8  — Puissance / Phi
        SACRED_FREQUENCIES.ATOM_I,   // 369    — Intensité / Tesla
        SACRED_FREQUENCIES.ATOM_PO,  // 1728   — Position / Polarité
      ],
      phi_ratio: SACRED_FREQUENCIES.PHI,
    };
  },
};
