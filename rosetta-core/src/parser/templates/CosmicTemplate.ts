/**
 * AT·OM — CosmicTemplate
 * Template unifié qui chaîne les 4 moteurs cosmologiques
 * (Chakra + Kabbale + Maya + Yi-King) en une seule traduction Rosetta.
 *
 * "Nous n'inventons rien. Nous nous souvenons de tout."
 */

import {
  type ResonanceLevel,
  type TechPayload,
  type PeoplePayload,
  type SpiritPayload,
  SACRED_FREQUENCIES,
  RESONANCE_MATRIX,
} from '../../types/atom-types';

import {
  type TranslatorTemplate,
  type ParserContext,
  RosettaParser,
} from '../RosettaParser';

import { ChakraTemplate, CHAKRA_DATA, harmonizeFrequency } from './ChakraTemplate';
import { KabbaleTemplate, SEPHIROTH_DATA } from './KabbaleTemplate';
import { MayaTemplate, getMayaKin } from './MayaTemplate';
import { YiKingTemplate, getHexagramFromWord } from './YiKingTemplate';

// ═══════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════

export interface CosmicInput {
  text: string;
  date?: Date;
  include_all?: boolean;
}

// ═══════════════════════════════════════════════════════════
// CALCULS COSMIQUES
// ═══════════════════════════════════════════════════════════

/**
 * Calcule la fréquence cosmique unifiée.
 * Moyenne pondérée des 4 modificateurs + base, clampée 111-999.
 */
export function calculateCosmicFrequency(
  baseHz: number,
  mayaMod: number,
  yikingMod: number,
  kabbaleMod: number,
  chakraMod: number,
): number {
  const cosmicHz = baseHz + (mayaMod + yikingMod + kabbaleMod + chakraMod) / 4;
  // Clamp aux bornes AT·OM
  const clamped = Math.max(111, Math.min(999, cosmicHz));
  // Snap au palier 111×n le plus proche
  const level = Math.round(clamped / 111);
  return Math.max(1, Math.min(9, level)) * 111;
}

/**
 * Raccourci : Oracle quotidien pour un mot/intention.
 */
export function getDailyOracle(text: string): {
  tech: TechPayload;
  people: PeoplePayload;
  spirit: SpiritPayload;
} {
  const ctx: ParserContext = {
    system_frequency: SACRED_FREQUENCIES.HEARTBEAT,
    user_id: null,
    sphere: null,
    timestamp: Date.now(),
    mode: 'standard',
  };
  const input: CosmicInput = { text, include_all: true };
  return {
    tech: CosmicTemplate.toTech(input, ctx),
    people: CosmicTemplate.toPeople(input, ctx),
    spirit: CosmicTemplate.toSpirit(input, ctx),
  };
}

/**
 * Enregistre les 5 templates cosmologiques sur un parser.
 */
export function registerAllCosmicTemplates(parser: RosettaParser): void {
  parser.registerTemplate(ChakraTemplate);
  parser.registerTemplate(KabbaleTemplate);
  parser.registerTemplate(MayaTemplate);
  parser.registerTemplate(YiKingTemplate);
  parser.registerTemplate(CosmicTemplate);
}

// ═══════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════

function resolveLevel(text: string): ResonanceLevel {
  return RosettaParser.computeArithmos(text);
}

function getSubsystemData(text: string, date: Date, level: ResonanceLevel) {
  // Chakra
  const chakraIdx = Math.min(level - 1, CHAKRA_DATA.length - 1);
  const chakra = CHAKRA_DATA[chakraIdx];

  // Kabbale
  const sephIdx = Math.min(level - 1, SEPHIROTH_DATA.length - 1);
  const sephirah = SEPHIROTH_DATA[sephIdx];

  // Maya
  const maya = getMayaKin(date);

  // Yi-King
  const hexagram = getHexagramFromWord(text);

  return { chakra, sephirah, maya, hexagram };
}

// ═══════════════════════════════════════════════════════════
// COSMIC TEMPLATE
// ═══════════════════════════════════════════════════════════

export const CosmicTemplate: TranslatorTemplate<CosmicInput> = {
  domain: 'cosmic',

  toTech(input, ctx) {
    const level = resolveLevel(input.text);
    const baseHz = level * 111;
    const date = input.date ?? new Date();
    const { chakra, sephirah, maya, hexagram } = getSubsystemData(input.text, date, level);

    const mayaMod = maya.ton.number * 11.1;
    const yikingMod = (hexagram.atomLevel ?? level) * 11;
    const kabbaleMod = sephirah.index * 10;
    const chakraMod = (chakra.atomFrequency - baseHz) * 0.1;

    const cosmicHz = calculateCosmicFrequency(baseHz, mayaMod, yikingMod, kabbaleMod, chakraMod);
    const harmonicHz = Math.round(baseHz * SACRED_FREQUENCIES.PHI);

    return {
      schema_version: '1.0',
      data_type: 'cosmic_oracle',
      values: {
        text: input.text,
        arithmos_level: level,
        base_frequency: baseHz,
        cosmic_frequency: cosmicHz,
        harmonic_frequency: harmonicHz,
        subsystems: {
          chakra: {
            name: chakra.name,
            sanskrit: chakra.sanskrit,
            element: chakra.element,
            solfeggio: chakra.solfeggioHz,
            harmonic_mean: harmonizeFrequency(baseHz, chakra.solfeggioHz),
          },
          kabbale: {
            name: sephirah.name,
            meaning: sephirah.meaning,
            world: sephirah.world,
            pillar: sephirah.pillar,
            archangel: sephirah.archangel,
          },
          maya: {
            kin_number: maya.kinNumber,
            ton: maya.ton.name,
            nawal: maya.nawal.name,
            is_portal: maya.isPortalDay,
            frequency_mod: mayaMod,
          },
          yiking: {
            hexagram_number: hexagram.number,
            name: hexagram.name,
            tendency: hexagram.tendency,
            atom_level: hexagram.atomLevel,
          },
        },
        modifiers: { maya: mayaMod, yiking: yikingMod, kabbale: kabbaleMod, chakra: chakraMod },
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, ctx) {
    const level = resolveLevel(input.text);
    const date = input.date ?? new Date();
    const { chakra, sephirah, maya, hexagram } = getSubsystemData(input.text, date, level);

    const narrative = [
      `Oracle Cosmique pour "${input.text}" (Niveau ${level}, ${level * 111}Hz).`,
      `Aujourd'hui, l'énergie du Nawal ${maya.nawal.name} (${maya.nawal.meaning}) rencontre la sagesse de ${sephirah.name} (${sephirah.meaning}).`,
      `Ton chakra ${chakra.name} (${chakra.sanskrit}) résonne au mantra ${chakra.mantra}.`,
      `L'hexagramme ${hexagram.name} (#${hexagram.number}) indique une tendance ${hexagram.tendency}.`,
    ].join(' ');

    const explanation = [
      `Le Ton ${maya.ton.number} (${maya.ton.name}) apporte l'action de ${maya.ton.meaning}.`,
      `${sephirah.name} te guide depuis le monde de ${sephirah.world}, pilier de ${sephirah.pillar}.`,
      maya.isPortalDay ? 'Jour de Portail Galactique — les énergies sont amplifiées.' : '',
    ].filter(Boolean).join(' ');

    const steps = [
      `Médite avec le mantra ${chakra.mantra} pour ancrer la fréquence ${chakra.atomFrequency}Hz.`,
      `Contemple la qualité de ${sephirah.quality} dans ta journée.`,
      `L'hexagramme suggère : ${hexagram.keywords?.join(', ') ?? 'transformation en cours'}.`,
      `Couleur du jour : harmonise-toi avec la vibration de ${chakra.element}.`,
    ];

    return {
      narrative,
      explanation,
      guide_steps: steps,
      emotional_tone: maya.isPortalDay ? 'sacre' : level >= 7 ? 'celebratoire' : 'encourageant',
      language: 'fr',
    };
  },

  toSpirit(input, ctx) {
    const level = resolveLevel(input.text);
    const date = input.date ?? new Date();
    const { chakra, sephirah, maya, hexagram } = getSubsystemData(input.text, date, level);

    const baseHz = level * 111;
    const mayaMod = maya.ton.number * 11.1;
    const yikingMod = (hexagram.atomLevel ?? level) * 11;
    const kabbaleMod = sephirah.index * 10;
    const chakraMod = (chakra.atomFrequency - baseHz) * 0.1;
    const cosmicHz = calculateCosmicFrequency(baseHz, mayaMod, yikingMod, kabbaleMod, chakraMod);

    const cosmicLevel = Math.max(1, Math.min(9, Math.round(cosmicHz / 111))) as ResonanceLevel;

    return {
      frequency_hz: RESONANCE_MATRIX[cosmicLevel].hz,
      resonance_level: cosmicLevel,
      color: chakra.color,
      sacred_geometry: RosettaParser.geometryFor(cosmicLevel),
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
