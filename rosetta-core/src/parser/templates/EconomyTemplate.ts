/**
 * AT·OM — EconomyTemplate
 * TranslatorTemplate pour l'Économie de Résonance (Sphère 4: 444Hz)
 *
 * "La richesse circule comme le sang. Donner = Recevoir."
 *
 * L'Économie de Résonance mesure la VRAIE valeur :
 * la contribution réelle, pas la spéculation.
 * Pas de création monétaire arbitraire, pas de dette.
 */

import {
  type SphereId,
  type ResonanceLevel,
  type EconomicCategory,
  type FlowKeeperConfig,
  SPHERES,
  RESONANCE_MATRIX,
  SACRED_FREQUENCIES,
  DEFAULT_FLOW_KEEPER,
} from '../../types/atom-types';
import { type TranslatorTemplate, type ParserContext, RosettaParser } from '../RosettaParser';

// ═══════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════

export type TransactionType =
  | 'CONTRIBUTION'    // Apport de valeur (travail, code, contenu)
  | 'FLOW_KEEPER'     // Don volontaire (remplace les taxes)
  | 'EXCHANGE'        // Échange pair-à-pair
  | 'REBATE'          // Ristourne résonance
  | 'STIMULUS'        // Injection communautaire
  | 'BURN'            // Régulation (destruction)
  | 'MINT_JT'         // Création de Jetons de Transition
  | 'MINT_SOUVENIR';  // Token Souvenir gravé

export interface EconomyInput {
  transaction_id: string;
  type: TransactionType;
  from_id: string | 'SYSTEM';
  to_id: string | 'SYSTEM';
  amount_ur: number;
  sphere_id: SphereId;
  description: string;
  from_resonance?: number;          // resonance_score de l'émetteur
  to_resonance?: number;
  is_flow_keeper?: boolean;         // Don volontaire
  metadata?: Record<string, unknown>;
}

// ═══════════════════════════════════════════════════════════
// TEMPLATE
// ═══════════════════════════════════════════════════════════

export const EconomyTemplate: TranslatorTemplate<EconomyInput> = {
  domain: 'economy',

  toTech(input, ctx) {
    return {
      schema_version: '1.0',
      data_type: 'economic_transaction',
      values: {
        transaction_id: input.transaction_id,
        type: input.type,
        from_id: input.from_id,
        to_id: input.to_id,
        amount_ur: input.amount_ur,
        sphere_id: input.sphere_id,
        from_resonance: input.from_resonance ?? 0,
        to_resonance: input.to_resonance ?? 0,
        is_flow_keeper: input.is_flow_keeper ?? false,
        flow_direction: input.from_id === 'SYSTEM' ? 'INJECTION' : input.to_id === 'SYSTEM' ? 'EXTRACTION' : 'CIRCULATION',
        system_frequency: ctx.system_frequency,
        metadata: input.metadata ?? {},
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, _ctx) {
    const sphere = SPHERES[input.sphere_id];
    const typeDesc = TRANSACTION_LABELS[input.type];

    let narrative: string;
    if (input.type === 'FLOW_KEEPER') {
      narrative = `Don volontaire de ${input.amount_ur} UR vers la sphère ${sphere.label}. `;
      narrative += `Ce flux nourrit directement la communauté — 100% va à la stimulation, 0% à la bureaucratie.`;
    } else if (input.type === 'CONTRIBUTION') {
      narrative = `Contribution de ${input.amount_ur} UR dans la sphère ${sphere.label}. `;
      narrative += `La valeur créée circule et renforce l'ensemble de l'Arche.`;
    } else if (input.type === 'REBATE') {
      narrative = `Ristourne de résonance : ${input.amount_ur} UR. `;
      narrative += `Votre alignement vibratoire génère un retour naturel.`;
    } else if (input.type === 'BURN') {
      narrative = `Régulation : ${input.amount_ur} UR retirés de la circulation. `;
      narrative += `L'équilibre du système est maintenu par ce mécanisme naturel.`;
    } else if (input.type === 'MINT_SOUVENIR') {
      narrative = `Token Souvenir gravé : ${input.amount_ur} UR de valeur symbolique. `;
      narrative += `Cette participation est inscrite dans l'éternité via Hedera.`;
    } else {
      narrative = `${typeDesc} : ${input.amount_ur} UR dans la sphère ${sphere.label}. `;
      narrative += input.description;
    }

    const tone = input.type === 'FLOW_KEEPER' || input.type === 'CONTRIBUTION'
      ? 'encourageant' as const
      : input.type === 'BURN' ? 'neutre' as const
      : input.type === 'MINT_SOUVENIR' ? 'celebratoire' as const
      : 'neutre' as const;

    return {
      narrative,
      explanation: input.description,
      guide_steps: [
        `Type : ${typeDesc}`,
        `Sphère : ${sphere.label} (${sphere.frequency}Hz)`,
        `Montant : ${input.amount_ur} UR`,
        input.is_flow_keeper
          ? `Flow Keeper : 100% stimulation communautaire`
          : `Circuit : ${input.from_id === 'SYSTEM' ? 'Système' : 'Pair'} → ${input.to_id === 'SYSTEM' ? 'Système' : 'Pair'}`,
      ],
      emotional_tone: tone,
      language: 'fr',
    };
  },

  toSpirit(input, _ctx) {
    const sphere = SPHERES[input.sphere_id];
    // La fréquence économique est ancrée sur 444Hz (Sphère 4 = Cœur)
    // mais modulée par le type de transaction
    const freqMod = TRANSACTION_FREQ_MOD[input.type] ?? 0;
    const baseLevel = 4; // 444Hz = ancre
    const modLevel = Math.max(1, Math.min(9, baseLevel + freqMod)) as ResonanceLevel;
    const resonance = RESONANCE_MATRIX[modLevel];

    return {
      frequency_hz: resonance.hz,
      resonance_level: modLevel,
      color: sphere.color,
      sacred_geometry: RosettaParser.geometryFor(modLevel),
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
// LABELS & CONSTANTES
// ═══════════════════════════════════════════════════════════

const TRANSACTION_LABELS: Record<TransactionType, string> = {
  CONTRIBUTION: 'Contribution',
  FLOW_KEEPER: 'Flow Keeper (don volontaire)',
  EXCHANGE: 'Échange pair-à-pair',
  REBATE: 'Ristourne résonance',
  STIMULUS: 'Stimulation communautaire',
  BURN: 'Régulation / Burn',
  MINT_JT: 'Jeton de Transition',
  MINT_SOUVENIR: 'Token Souvenir',
};

/** Modificateur de fréquence par type de transaction */
const TRANSACTION_FREQ_MOD: Record<TransactionType, number> = {
  CONTRIBUTION: +1,      // 555Hz — Contribution élève
  FLOW_KEEPER: +2,       // 666Hz — Don volontaire harmonise
  EXCHANGE: 0,           // 444Hz — Échange neutre (ancre)
  REBATE: +1,            // 555Hz — Récompense élève
  STIMULUS: +2,          // 666Hz — Injection harmonise
  BURN: -1,              // 333Hz — Destruction descend
  MINT_JT: +1,           // 555Hz — Création élève
  MINT_SOUVENIR: +3,     // 777Hz — Mémoire transcende
};

// ═══════════════════════════════════════════════════════════
// FLOW KEEPER ENGINE — Stabilisation automatique
// ═══════════════════════════════════════════════════════════

/**
 * Moteur de stabilisation économique.
 * Surveille les métriques et ajuste automatiquement les paramètres.
 */
export class FlowKeeperEngine {
  private config: FlowKeeperConfig;

  constructor(config: FlowKeeperConfig = DEFAULT_FLOW_KEEPER) {
    this.config = { ...config };
  }

  /**
   * Analyse l'état économique et recommande des ajustements.
   */
  analyze(metrics: {
    velocity_30d: number;
    reserve_ratio: number;
    total_supply: number;
    total_burned: number;
  }): FlowKeeperAction {
    const { velocity_30d, reserve_ratio } = metrics;
    const { velocity_target_30d, reserve_ratio_min } = this.config;

    // Détection CRISE
    if (reserve_ratio < 0.30) {
      return {
        action: 'CRISE',
        description: 'Bouclier de liquidité activé — gel des conversions UR→fiat',
        adjustments: {
          freeze_conversions: true,
          emergency_notification: true,
          burn_rate: 0,
        },
        severity: 'critical',
      };
    }

    // Détection INFLATION (vélocité trop haute)
    if (velocity_30d > velocity_target_30d * 2) {
      return {
        action: 'ANTI_INFLATION',
        description: 'Vélocité excessive — augmentation du burn rate et réduction des ristournes',
        adjustments: {
          burn_rate: this.config.burn_rate_base * 2,
          resonance_rebate_pct: this.config.resonance_rebate_pct * 0.5,
          savings_incentive: true,
        },
        severity: 'warning',
      };
    }

    // Détection DEFLATION (vélocité trop basse)
    if (velocity_30d < velocity_target_30d * 0.5) {
      return {
        action: 'ANTI_DEFLATION',
        description: 'Vélocité insuffisante — réduction du burn et facilitation des échanges',
        adjustments: {
          burn_rate: this.config.burn_rate_base * 0.5,
          usage_bonus: true,
          lending_facilitated: true,
        },
        severity: 'warning',
      };
    }

    // ÉQUILIBRE
    return {
      action: 'EQUILIBRE',
      description: 'Système en équilibre — paramètres nominaux',
      adjustments: {
        burn_rate: this.config.burn_rate_base,
        resonance_rebate_pct: this.config.resonance_rebate_pct,
      },
      severity: 'info',
    };
  }

  /** Calcule la ristourne résonance pour un utilisateur */
  calculateRebate(amount_ur: number, resonance_score: number): number {
    // Plus le resonance_score est élevé, plus la ristourne est grande
    const factor = resonance_score / 100;
    return amount_ur * this.config.resonance_rebate_pct * factor;
  }

  /** Calcule le burn sur une transaction */
  calculateBurn(amount_ur: number): number {
    return amount_ur * this.config.burn_rate_base;
  }

  getConfig(): Readonly<FlowKeeperConfig> {
    return { ...this.config };
  }

  updateConfig(patch: Partial<FlowKeeperConfig>): void {
    Object.assign(this.config, patch);
  }
}

export interface FlowKeeperAction {
  action: 'EQUILIBRE' | 'ANTI_INFLATION' | 'ANTI_DEFLATION' | 'CRISE';
  description: string;
  adjustments: Record<string, unknown>;
  severity: 'info' | 'warning' | 'critical';
}
