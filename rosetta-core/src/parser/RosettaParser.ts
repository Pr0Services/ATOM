/**
 * AT·OM — RosettaParser
 * Le Cœur du système de traduction tri-dimensionnel
 *
 * Comme la Pierre de Rosette traduit un même message en 3 langues,
 * ce parser garantit que toute donnée existe simultanément dans :
 *   - TECH (Grec)         → JSON structuré, prêt pour Hedera
 *   - PEOPLE (Démotique)  → Langage naturel, clair et narratif
 *   - SPIRIT (Hiéroglyphe)→ Fréquence Hz + géométrie sacrée
 *
 * Design Pattern : Template Engine réutilisable
 * Chaque "translator" est un template injectable pour différents domaines.
 */

import {
  type RosettaTranslation,
  type QuantumRosettaTranslation,
  type DimensionHashes,
  type RosettaDimension,
  type TechPayload,
  type PeoplePayload,
  type SpiritPayload,
  type SacredGeometryShape,
  type ResonanceLevel,
  type SphereId,
  type GearEvent,
  SACRED_FREQUENCIES,
  RESONANCE_MATRIX,
  ARITHMOS_MAP,
  SPHERES,
} from '../types/atom-types';

// ═══════════════════════════════════════════════════════════
// INTERFACES DU TEMPLATE ENGINE
// ═══════════════════════════════════════════════════════════

/** Template de traduction — injectable pour chaque domaine */
export interface TranslatorTemplate<TInput = unknown> {
  domain: string;
  toTech(input: TInput, context: ParserContext): TechPayload;
  toPeople(input: TInput, context: ParserContext): PeoplePayload;
  toSpirit(input: TInput, context: ParserContext): SpiritPayload;
}

/** Contexte partagé entre les 3 dimensions pendant une traduction */
export interface ParserContext {
  system_frequency: number;
  user_id: string | null;
  sphere: SphereId | null;
  timestamp: number;
  mode: 'standard' | 'activated' | 'polishing' | 'genesis';
}

/** Événement émis après chaque traduction */
export interface RosettaEvent {
  type: 'translation_complete' | 'validation_error' | 'gear_triggered';
  translation?: RosettaTranslation;
  error?: string;
  gear_event?: GearEvent;
}

type RosettaListener = (event: RosettaEvent) => void;

// ═══════════════════════════════════════════════════════════
// ROSETTA PARSER — Classe Principale
// ═══════════════════════════════════════════════════════════

export class RosettaParser {
  private templates: Map<string, TranslatorTemplate> = new Map();
  private listeners: RosettaListener[] = [];
  private context: ParserContext;

  constructor(initialContext?: Partial<ParserContext>) {
    this.context = {
      system_frequency: SACRED_FREQUENCIES.HEARTBEAT,
      user_id: null,
      sphere: null,
      timestamp: Date.now(),
      mode: 'standard',
      ...initialContext,
    };
  }

  // ─── Template Registry ─────────────────────────────────

  /** Enregistre un template de traduction pour un domaine */
  registerTemplate<T>(template: TranslatorTemplate<T>): void {
    this.templates.set(template.domain, template as TranslatorTemplate);
  }

  /** Récupère un template enregistré */
  getTemplate(domain: string): TranslatorTemplate | undefined {
    return this.templates.get(domain);
  }

  /** Liste tous les domaines enregistrés */
  listDomains(): string[] {
    return Array.from(this.templates.keys());
  }

  // ─── Core Translation ──────────────────────────────────

  /**
   * Traduit une donnée dans les 3 dimensions Rosetta
   * C'est l'opération fondamentale — aucune donnée ne rentre
   * dans AT·OM sans passer par cette traduction.
   */
  translate<T>(
    domain: string,
    input: T,
    sourceDimension: RosettaDimension = 'TECH',
    nodeId?: string,
  ): RosettaTranslation {
    const template = this.templates.get(domain);
    if (!template) {
      throw new RosettaError(`Aucun template enregistré pour le domaine: ${domain}`);
    }

    this.context.timestamp = Date.now();
    const id = this.generateId();
    const node_id = nodeId ?? id;

    const tech = template.toTech(input, this.context);
    const people = template.toPeople(input, this.context);
    const spirit = template.toSpirit(input, this.context);

    // Validation : les 3 dimensions doivent être cohérentes
    this.validateCoherence(tech, people, spirit);

    const translation: RosettaTranslation = {
      id,
      node_id,
      tech,
      people,
      spirit,
      created_at: this.context.timestamp,
      source_dimension: sourceDimension,
      integrity_hash: this.computeHash(tech, people, spirit),
    };

    // Émettre l'événement
    this.emit({
      type: 'translation_complete',
      translation,
    });

    return translation;
  }

  // ─── Anticythère : Propagation par Engrenages ──────────

  /**
   * Quand une sphère change, propage le changement via les engrenages
   * Comme la Machine d'Anticythère : un engrenage en fait tourner d'autres
   */
  propagateGearChange(
    sourceSphere: SphereId,
    payload: TechPayload,
    maxDepth: number = 2,
  ): GearEvent[] {
    const events: GearEvent[] = [];
    const visited = new Set<SphereId>();

    const propagate = (sphere: SphereId, depth: number) => {
      if (depth > maxDepth || visited.has(sphere)) return;
      visited.add(sphere);

      const connections = SPHERES[sphere].gear_connections;
      const event: GearEvent = {
        id: this.generateId(),
        source_sphere: sphere,
        target_spheres: connections,
        event_type: depth === 0 ? 'mutation' : 'cascade',
        payload,
        propagation_depth: depth,
        timestamp: Date.now(),
      };

      events.push(event);
      this.emit({ type: 'gear_triggered', gear_event: event });

      for (const target of connections) {
        propagate(target, depth + 1);
      }
    };

    propagate(sourceSphere, 0);
    return events;
  }

  // ─── Context Management ────────────────────────────────

  updateContext(patch: Partial<ParserContext>): void {
    Object.assign(this.context, patch);
  }

  getContext(): Readonly<ParserContext> {
    return { ...this.context };
  }

  // ─── Event System ──────────────────────────────────────

  on(listener: RosettaListener): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  private emit(event: RosettaEvent): void {
    for (const listener of this.listeners) {
      listener(event);
    }
  }

  // ─── Utilitaires Sacrés ────────────────────────────────

  /** Calcul Pythagoricien (Arithmos) — réduit un texte à son niveau 1-9 */
  static computeArithmos(text: string): ResonanceLevel {
    const clean = text
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toUpperCase()
      .replace(/[^A-Z]/g, '');

    let sum = 0;
    for (const char of clean) {
      sum += ARITHMOS_MAP[char] ?? 0;
    }

    // Réduction théosophique → 1-9
    while (sum > 9) {
      sum = String(sum).split('').reduce((a, b) => a + parseInt(b), 0);
    }

    return (sum || 9) as ResonanceLevel;
  }

  /** Retourne la fréquence Hz pour un texte */
  static frequencyOf(text: string): number {
    const level = RosettaParser.computeArithmos(text);
    return RESONANCE_MATRIX[level].hz;
  }

  /** Retourne la géométrie sacrée pour un niveau de résonance */
  static geometryFor(level: ResonanceLevel): SacredGeometryShape {
    const map: Record<ResonanceLevel, SacredGeometryShape> = {
      1: 'point',
      2: 'vesica_piscis',
      3: 'triangle',
      4: 'tetrahedron',
      5: 'pentagram',
      6: 'hexagram',
      7: 'heptagram',
      8: 'octahedron',
      9: 'enneagram',
    };
    return map[level];
  }

  // ─── Validation de Cohérence ───────────────────────────

  private validateCoherence(
    tech: TechPayload,
    people: PeoplePayload,
    spirit: SpiritPayload,
  ): void {
    if (!tech.data_type) {
      throw new RosettaError('Tech payload manque data_type');
    }
    if (!people.narrative || people.narrative.length < 1) {
      throw new RosettaError('People payload manque narrative');
    }
    if (!spirit.frequency_hz || spirit.frequency_hz <= 0) {
      throw new RosettaError('Spirit payload manque frequency_hz valide');
    }
    // La fréquence doit correspondre au niveau de résonance
    const expected = RESONANCE_MATRIX[spirit.resonance_level].hz;
    if (spirit.frequency_hz !== expected) {
      throw new RosettaError(
        `Incohérence fréquentielle: niveau ${spirit.resonance_level} = ${expected}Hz, reçu ${spirit.frequency_hz}Hz`
      );
    }
  }

  // ─── Traduction Quantique (avec hashes par dimension) ──

  /**
   * Traduit une donnée dans les 3 dimensions Rosetta
   * ET ajoute les hashes individuels par dimension pour la correction quantique.
   * Backward-compatible : retourne un QuantumRosettaTranslation (extends RosettaTranslation).
   */
  translateQuantum<T>(
    domain: string,
    input: T,
    sourceDimension: RosettaDimension = 'TECH',
    nodeId?: string,
  ): QuantumRosettaTranslation {
    const base = this.translate(domain, input, sourceDimension, nodeId);
    return {
      ...base,
      dimension_hashes: RosettaParser.computeDimensionHashes(
        base.tech,
        base.people,
        base.spirit,
      ),
    };
  }

  // ─── Hash d'Intégrité ──────────────────────────────────

  /** Hash combiné des 3 dimensions (backward-compatible, utilisé par translate()) */
  private computeHash(
    tech: TechPayload,
    people: PeoplePayload,
    spirit: SpiritPayload,
  ): string {
    return RosettaParser.computeCombinedHash(tech, people, spirit);
  }

  /** Hash combiné statique — accessible depuis QuantumCorrector */
  static computeCombinedHash(
    tech: TechPayload,
    people: PeoplePayload,
    spirit: SpiritPayload,
  ): string {
    const content = JSON.stringify({ tech, people, spirit });
    return RosettaParser.hashString(content, 'rosetta');
  }

  /** Hash d'une seule dimension — localise la corruption */
  static computeDimensionHash(payload: TechPayload | PeoplePayload | SpiritPayload): string {
    const content = JSON.stringify(payload);
    return RosettaParser.hashString(content, 'dim');
  }

  /** Calcule les 3 hashes individuels + le hash combiné */
  static computeDimensionHashes(
    tech: TechPayload,
    people: PeoplePayload,
    spirit: SpiritPayload,
  ): DimensionHashes {
    return {
      tech_hash: RosettaParser.computeDimensionHash(tech),
      people_hash: RosettaParser.computeDimensionHash(people),
      spirit_hash: RosettaParser.computeDimensionHash(spirit),
      combined_hash: RosettaParser.computeCombinedHash(tech, people, spirit),
    };
  }

  /** Algorithme de hashing interne (DJB2 variant) */
  private static hashString(content: string, prefix: string): string {
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0;
    }
    return `${prefix}_${Math.abs(hash).toString(36)}`;
  }

  private generateId(): string {
    const ts = Date.now().toString(36);
    const rand = Math.random().toString(36).substring(2, 8);
    return `atom_${ts}_${rand}`;
  }
}

// ═══════════════════════════════════════════════════════════
// ERREURS ROSETTA
// ═══════════════════════════════════════════════════════════

export class RosettaError extends Error {
  constructor(message: string) {
    super(`[RosettaParser] ${message}`);
    this.name = 'RosettaError';
  }
}

// ═══════════════════════════════════════════════════════════
// TEMPLATES PRÉ-CONSTRUITS (Exemples réutilisables)
// ═══════════════════════════════════════════════════════════

/** Template générique pour les données de type "Talent" */
export const TalentTemplate: TranslatorTemplate<{
  name: string;
  sphere: SphereId;
  description: string;
  level: number;
}> = {
  domain: 'talent',

  toTech(input, ctx) {
    return {
      schema_version: '1.0',
      data_type: 'talent',
      values: {
        name: input.name,
        sphere: input.sphere,
        level: input.level,
        registered_by: ctx.user_id,
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, ctx) {
    const sphere = SPHERES[input.sphere];
    return {
      narrative: `${input.name} — Un talent de niveau ${input.level} dans la sphère ${sphere.label}.`,
      explanation: input.description,
      guide_steps: [
        `Ce talent est ancré dans la sphère ${sphere.label} (${sphere.frequency}Hz).`,
        `Il contribue à l'harmonie du système à travers ${sphere.gear_connections.length} connexions.`,
      ],
      emotional_tone: input.level >= 7 ? 'celebratoire' : 'encourageant',
      language: 'fr',
    };
  },

  toSpirit(input, _ctx) {
    const level = (input.level > 9 ? 9 : input.level < 1 ? 1 : input.level) as ResonanceLevel;
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

/** Template pour les événements de sphère (Anticythère) */
export const SphereEventTemplate: TranslatorTemplate<{
  sphere: SphereId;
  event_name: string;
  data: Record<string, unknown>;
}> = {
  domain: 'sphere_event',

  toTech(input, ctx) {
    return {
      schema_version: '1.0',
      data_type: 'sphere_event',
      values: {
        sphere: input.sphere,
        event: input.event_name,
        ...input.data,
        system_frequency: ctx.system_frequency,
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, _ctx) {
    const sphere = SPHERES[input.sphere];
    return {
      narrative: `La sphère ${sphere.label} vient de recevoir l'événement "${input.event_name}".`,
      explanation: `Cet événement active les engrenages vers ${sphere.gear_connections.map(c => SPHERES[c].label).join(', ')}.`,
      emotional_tone: 'neutre',
      language: 'fr',
    };
  },

  toSpirit(input, _ctx) {
    const sphere = SPHERES[input.sphere];
    const level = sphere.index as ResonanceLevel;
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

/** Template pour la validation alchimique (Table d'Émeraude) */
export const AlchemyTemplate: TranslatorTemplate<{
  node_id: string;
  stage: string;
  stage_index: number;
  passed: boolean;
  reason?: string;
}> = {
  domain: 'alchemy_validation',

  toTech(input, ctx) {
    return {
      schema_version: '1.0',
      data_type: 'alchemy_validation',
      values: {
        node_id: input.node_id,
        stage: input.stage,
        stage_index: input.stage_index,
        passed: input.passed,
        reason: input.reason ?? null,
      },
      timestamp: ctx.timestamp,
    };
  },

  toPeople(input, _ctx) {
    const stageNames: Record<number, string> = {
      1: 'Calcination — Destruction des illusions',
      2: 'Dissolution — Libération des structures rigides',
      3: 'Séparation — Tri du vrai et du faux',
      4: 'Conjonction — Union des forces',
      5: 'Fermentation — Germination de la vérité',
      6: 'Distillation — Purification finale',
      7: 'Coagulation — Cristallisation en Or',
    };

    const stageName = stageNames[input.stage_index] ?? input.stage;

    return {
      narrative: input.passed
        ? `Étape ${input.stage_index}/7 réussie : ${stageName}. Le processus de transformation avance.`
        : `Étape ${input.stage_index}/7 bloquée : ${stageName}. ${input.reason ?? 'Données non alignées.'}`,
      explanation: input.passed
        ? 'Cette donnée est en harmonie avec les Lois Universelles.'
        : 'Cette donnée nécessite un polissage avant de continuer.',
      emotional_tone: input.passed ? 'encourageant' : 'alerte',
      language: 'fr',
    };
  },

  toSpirit(input, _ctx) {
    // Chaque étape alchimique monte en fréquence
    const level = Math.min(input.stage_index + 2, 9) as ResonanceLevel;
    const resonance = RESONANCE_MATRIX[level];
    return {
      frequency_hz: resonance.hz,
      resonance_level: level,
      color: input.passed ? resonance.color : '#8B0000', // Rouge sombre si bloqué
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
