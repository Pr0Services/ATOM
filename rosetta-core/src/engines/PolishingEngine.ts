/**
 * AT·OM — PolishingEngine (Le Grand Nettoyage)
 * Moteur de validation alchimique basé sur la Table d'Émeraude
 *
 * "Ce qui est en haut est comme ce qui est en bas."
 *
 * Ce moteur compare les données du "Diamant Actuel" (Chaos)
 * à la structure du "Diamant Optimal" (Vérité).
 *
 * 7 étapes de transformation alchimique :
 *   1. CALCINATION    — Destruction des illusions (données invalides)
 *   2. DISSOLUTION    — Dissolution des structures rigides
 *   3. SEPARATION     — Tri du vrai et du faux
 *   4. CONJUNCTION    — Union des opposés
 *   5. FERMENTATION   — Germination du nouveau
 *   6. DISTILLATION   — Purification finale
 *   7. COAGULATION    — Cristallisation de la vérité (Or)
 *
 * Template Engine : Les règles de validation sont injectables
 * pour chaque domaine/sphère.
 */

import {
  type AlchemyStage,
  type EmeraldValidation,
  type ATOMNode,
  type RosettaTranslation,
  type SphereId,
  type ResonanceLevel,
  type ContentIntention,
  type InformationResonanceScore,
  type IntentionFilter,
  type IntentionCheck,
  type UniversalLaw,
  SACRED_FREQUENCIES,
  RESONANCE_MATRIX,
  UNIVERSAL_LAWS,
} from '../types/atom-types';

// ═══════════════════════════════════════════════════════════
// INTERFACES TEMPLATE (Règles de validation injectables)
// ═══════════════════════════════════════════════════════════

/** Règle de validation pour une étape alchimique */
export interface AlchemyRule {
  stage: AlchemyStage;
  stage_index: number;
  name: string;
  description: string;
  validate(data: PolishingInput): PolishingResult;
}

/** Données en entrée du polissage */
export interface PolishingInput {
  node: ATOMNode;
  rosetta: RosettaTranslation;
  optimal_schema?: Record<string, unknown>;
}

/** Résultat d'une étape de polissage */
export interface PolishingResult {
  passed: boolean;
  reason?: string;
  suggestions?: string[];
  severity: 'info' | 'warning' | 'critical';
}

/** Profil de validation pour un domaine spécifique */
export interface PolishingProfile {
  domain: string;
  sphere?: SphereId;
  custom_rules: AlchemyRule[];
}

// ═══════════════════════════════════════════════════════════
// POLISHING ENGINE
// ═══════════════════════════════════════════════════════════

export class PolishingEngine {
  private defaultRules: AlchemyRule[];
  private profiles: Map<string, PolishingProfile> = new Map();

  constructor() {
    this.defaultRules = PolishingEngine.createDefaultRules();
  }

  // ─── Core: Polissage Complet ───────────────────────────

  /**
   * Opération principale : fait passer une donnée à travers les 7 étapes.
   * Retourne un rapport complet de transformation alchimique.
   */
  polishData(input: PolishingInput, profileDomain?: string): EmeraldValidation {
    const rules = this.getRulesFor(profileDomain);
    const log: EmeraldValidation['transformation_log'] = [];
    let currentStage: AlchemyStage = 'CALCINATION';
    let stageIndex = 1;
    let allPassed = true;
    const notes: string[] = [];

    for (const rule of rules) {
      const result = rule.validate(input);

      log.push({
        stage: rule.stage,
        passed: result.passed,
        timestamp: Date.now(),
        reason: result.reason,
      });

      if (!result.passed) {
        allPassed = false;
        currentStage = rule.stage;
        stageIndex = rule.stage_index;
        notes.push(`[${rule.stage}] ${result.reason ?? 'Non aligné'}`);
        if (result.suggestions) {
          notes.push(...result.suggestions.map(s => `  → ${s}`));
        }
        // Arrêt au premier échec — on ne peut pas sauter une étape
        break;
      }

      currentStage = rule.stage;
      stageIndex = rule.stage_index;
    }

    return {
      node_id: input.node.id,
      current_stage: allPassed ? 'COAGULATION' : currentStage,
      stage_index: allPassed ? 7 : stageIndex,
      is_aligned: allPassed,
      polishing_notes: notes,
      transformation_log: log,
    };
  }

  /**
   * Polissage rapide — vérifie uniquement si la donnée est alignée
   * sans générer le rapport complet.
   */
  isAligned(input: PolishingInput, profileDomain?: string): boolean {
    const rules = this.getRulesFor(profileDomain);
    return rules.every(rule => rule.validate(input).passed);
  }

  /**
   * Diagnostic — retourne la première étape qui échoue
   */
  diagnose(input: PolishingInput, profileDomain?: string): {
    stage: AlchemyStage;
    reason: string;
  } | null {
    const rules = this.getRulesFor(profileDomain);
    for (const rule of rules) {
      const result = rule.validate(input);
      if (!result.passed) {
        return { stage: rule.stage, reason: result.reason ?? 'Non aligné' };
      }
    }
    return null;
  }

  // ─── Profile Management ────────────────────────────────

  /** Enregistre un profil de validation pour un domaine */
  registerProfile(profile: PolishingProfile): void {
    this.profiles.set(profile.domain, profile);
  }

  private getRulesFor(domain?: string): AlchemyRule[] {
    if (!domain) return this.defaultRules;
    const profile = this.profiles.get(domain);
    if (!profile) return this.defaultRules;
    // Merge : default rules + custom rules (custom overrides par stage)
    const customStages = new Set(profile.custom_rules.map(r => r.stage));
    const merged = this.defaultRules.filter(r => !customStages.has(r.stage));
    return [...merged, ...profile.custom_rules].sort((a, b) => a.stage_index - b.stage_index);
  }

  // ─── Batch Operations ──────────────────────────────────

  /** Polissage en lot — retourne les résultats pour un ensemble de nodes */
  polishBatch(
    inputs: PolishingInput[],
    profileDomain?: string,
  ): { aligned: EmeraldValidation[]; toPolish: EmeraldValidation[] } {
    const aligned: EmeraldValidation[] = [];
    const toPolish: EmeraldValidation[] = [];

    for (const input of inputs) {
      const result = this.polishData(input, profileDomain);
      if (result.is_aligned) {
        aligned.push(result);
      } else {
        toPolish.push(result);
      }
    }

    return { aligned, toPolish };
  }

  /** Statistiques de polissage */
  getStats(results: EmeraldValidation[]): {
    total: number;
    aligned: number;
    toPolish: number;
    alignment_ratio: number;
    stage_distribution: Record<AlchemyStage, number>;
  } {
    const stages: Record<string, number> = {};
    let alignedCount = 0;

    for (const r of results) {
      if (r.is_aligned) alignedCount++;
      stages[r.current_stage] = (stages[r.current_stage] ?? 0) + 1;
    }

    return {
      total: results.length,
      aligned: alignedCount,
      toPolish: results.length - alignedCount,
      alignment_ratio: results.length > 0 ? alignedCount / results.length : 0,
      stage_distribution: stages as Record<AlchemyStage, number>,
    };
  }

  // ─── Default Rules (Les 7 Lois Universelles) ───────────

  static createDefaultRules(): AlchemyRule[] {
    return [
      // 1. CALCINATION — Les données existent-elles ?
      {
        stage: 'CALCINATION',
        stage_index: 1,
        name: 'Existence',
        description: 'Destruction des illusions — la donnée doit exister et être non-vide',
        validate(input: PolishingInput): PolishingResult {
          if (!input.node.id || !input.node.title) {
            return {
              passed: false,
              reason: 'Le node n\'a pas d\'identifiant ou de titre',
              severity: 'critical',
            };
          }
          if (!input.rosetta) {
            return {
              passed: false,
              reason: 'Aucune traduction Rosetta associée',
              suggestions: ['Faire passer la donnée par le RosettaParser'],
              severity: 'critical',
            };
          }
          return { passed: true, severity: 'info' };
        },
      },

      // 2. DISSOLUTION — Les structures sont-elles flexibles ?
      {
        stage: 'DISSOLUTION',
        stage_index: 2,
        name: 'Flexibilité',
        description: 'Dissolution des rigidités — les 3 dimensions Rosetta doivent être complètes',
        validate(input: PolishingInput): PolishingResult {
          const { tech, people, spirit } = input.rosetta;
          if (!tech?.data_type) {
            return {
              passed: false,
              reason: 'Dimension TECH incomplète (manque data_type)',
              severity: 'warning',
            };
          }
          if (!people?.narrative) {
            return {
              passed: false,
              reason: 'Dimension PEOPLE incomplète (manque narrative)',
              suggestions: ['Ajouter une description humaine de cette donnée'],
              severity: 'warning',
            };
          }
          if (!spirit?.frequency_hz) {
            return {
              passed: false,
              reason: 'Dimension SPIRIT incomplète (manque frequency_hz)',
              severity: 'warning',
            };
          }
          return { passed: true, severity: 'info' };
        },
      },

      // 3. SEPARATION — Le vrai est-il séparé du faux ?
      {
        stage: 'SEPARATION',
        stage_index: 3,
        name: 'Vérité',
        description: 'Séparation du vrai et du faux — cohérence interne',
        validate(input: PolishingInput): PolishingResult {
          const { spirit } = input.rosetta;
          // La fréquence doit correspondre au niveau de résonance
          const expectedHz = spirit.resonance_level * 111;
          if (spirit.frequency_hz !== expectedHz) {
            return {
              passed: false,
              reason: `Incohérence fréquentielle: niveau ${spirit.resonance_level} devrait être ${expectedHz}Hz, reçu ${spirit.frequency_hz}Hz`,
              severity: 'warning',
            };
          }
          // Le node doit appartenir à une sphère valide
          if (!input.node.sphere_id) {
            return {
              passed: false,
              reason: 'Le node n\'est assigné à aucune sphère',
              severity: 'warning',
            };
          }
          return { passed: true, severity: 'info' };
        },
      },

      // 4. CONJUNCTION — Les opposés sont-ils unis ?
      {
        stage: 'CONJUNCTION',
        stage_index: 4,
        name: 'Union',
        description: 'Union des contraires — la donnée technique et la narration humaine convergent',
        validate(input: PolishingInput): PolishingResult {
          const { tech, people } = input.rosetta;
          // Le data_type technique doit être reflété dans la narration
          if (people.narrative.length < 10) {
            return {
              passed: false,
              reason: 'La narration est trop courte pour porter le sens de la donnée technique',
              suggestions: ['Enrichir la description humaine (min 10 caractères)'],
              severity: 'warning',
            };
          }
          // Le schema_version doit être défini
          if (!tech.schema_version) {
            return {
              passed: false,
              reason: 'Pas de version de schéma — impossible de versionner la vérité',
              severity: 'warning',
            };
          }
          return { passed: true, severity: 'info' };
        },
      },

      // 5. FERMENTATION — Le nouveau germe-t-il ?
      {
        stage: 'FERMENTATION',
        stage_index: 5,
        name: 'Germination',
        description: 'La donnée est-elle vivante ? A-t-elle un potentiel de croissance ?',
        validate(input: PolishingInput): PolishingResult {
          // Le node doit avoir un statut actif (pas archivé)
          if (input.node.status === 'archived') {
            return {
              passed: false,
              reason: 'Node archivé — les données mortes ne fermentent pas',
              suggestions: ['Réactiver le node pour permettre la croissance'],
              severity: 'info',
            };
          }
          // La signature vibratoire doit contenir les 4 constantes
          const sig = input.rosetta.spirit.vibration_signature;
          if (!sig || sig.length < 4) {
            return {
              passed: false,
              reason: 'Signature vibratoire incomplète (besoin de M, P, I, Po)',
              severity: 'warning',
            };
          }
          return { passed: true, severity: 'info' };
        },
      },

      // 6. DISTILLATION — La pureté est-elle atteinte ?
      {
        stage: 'DISTILLATION',
        stage_index: 6,
        name: 'Purification',
        description: 'Purification finale — élimination de toute pollution',
        validate(input: PolishingInput): PolishingResult {
          // L'intégrité du hash doit être présente
          if (!input.rosetta.integrity_hash) {
            return {
              passed: false,
              reason: 'Pas de hash d\'intégrité — la donnée pourrait être corrompue',
              severity: 'critical',
            };
          }
          // Le phi_ratio doit être cohérent
          const phi = input.rosetta.spirit.phi_ratio;
          if (phi && Math.abs(phi - SACRED_FREQUENCIES.PHI) > 0.001) {
            return {
              passed: false,
              reason: `Ratio Phi incorrect: ${phi} ≠ ${SACRED_FREQUENCIES.PHI}`,
              severity: 'warning',
            };
          }
          return { passed: true, severity: 'info' };
        },
      },

      // 7. COAGULATION — L'Or est-il cristallisé ?
      {
        stage: 'COAGULATION',
        stage_index: 7,
        name: 'Cristallisation',
        description: 'Cristallisation de la vérité — la donnée est prête pour l\'immuabilité (Hedera)',
        validate(input: PolishingInput): PolishingResult {
          // Si on arrive ici, toutes les étapes précédentes ont été validées
          // Dernière vérification : le node est-il prêt pour le consensus ?
          if (input.node.status === 'polishing') {
            return {
              passed: false,
              reason: 'Le node est encore en phase de polissage',
              suggestions: ['Changer le statut à "aligned" une fois les corrections appliquées'],
              severity: 'info',
            };
          }
          return { passed: true, severity: 'info' };
        },
      },
    ];
  }
}

// ═══════════════════════════════════════════════════════════
// TRI DE L'INFORMATION — Analyse de résonance informationnelle
// ═══════════════════════════════════════════════════════════

/**
 * Analyseur de résonance informationnelle.
 * Évalue le contenu sur 5 axes (Ch.11 Vision) et détecte l'intention.
 * "Nous ne disons pas aux gens quoi penser.
 *  Nous leur donnons les outils pour VOIR CLAIREMENT."
 */
export class InformationFilter {

  /**
   * Calcule le score de résonance informationnelle d'un contenu.
   * 5 niveaux de tri : source, cohérence, diversité, transparence, intention
   */
  static analyzeResonance(content: {
    text: string;
    author_id?: string;
    sources?: { reference: string; verified: boolean }[];
    methodology_disclosed?: boolean;
    author_history_score?: number;
  }): InformationResonanceScore {
    // Niveau 1 : Vérification de source
    const sourceCount = content.sources?.length ?? 0;
    const verifiedCount = content.sources?.filter(s => s.verified).length ?? 0;
    const coherence_externe = sourceCount > 0 ? (verifiedCount / sourceCount) * 100 : 0;

    // Niveau 2 : Cohérence interne (longueur, structure, non-contradiction)
    const textLen = content.text.length;
    const coherence_interne = Math.min(100,
      (textLen > 50 ? 30 : 0) +
      (textLen > 200 ? 20 : 0) +
      (content.text.includes('.') ? 15 : 0) + // Phrases structurées
      (sourceCount > 0 ? 20 : 0) +
      (content.author_id ? 15 : 0)
    );

    // Niveau 3 : Diversité des sources
    const diversite_sources = Math.min(100, sourceCount * 20);

    // Niveau 4 : Transparence méthodologique
    const transparence_methodo = content.methodology_disclosed ? 80 : 20;

    // Niveau 5 : Fiabilité historique de l'auteur
    const fiabilite_auteur = content.author_history_score ?? 50;

    // Détection d'intention
    const intention_detectee = InformationFilter.detectIntention(content.text);

    // Score global composite
    const score_global = Math.round(
      coherence_interne * 0.20 +
      coherence_externe * 0.25 +
      diversite_sources * 0.20 +
      transparence_methodo * 0.15 +
      fiabilite_auteur * 0.20
    );

    return {
      content_id: `info_${Date.now().toString(36)}`,
      coherence_interne: Math.round(coherence_interne),
      coherence_externe: Math.round(coherence_externe),
      diversite_sources: Math.round(diversite_sources),
      transparence_methodo: Math.round(transparence_methodo),
      fiabilite_auteur: Math.round(fiabilite_auteur),
      intention_detectee,
      score_global,
    };
  }

  /**
   * Détecte l'intention dominante d'un contenu.
   * Catégories : INFORMATIF, PERSUASIF, MANIPULATIF, COMMERCIAL, DIVISIF
   */
  static detectIntention(text: string): ContentIntention {
    const lower = text.toLowerCase();

    // Marqueurs DIVISIF (polarisation, nous vs eux)
    const divisifMarkers = ['ennemi', 'contre nous', 'ils veulent', 'complot', 'menace',
      'détruire', 'envahir', 'danger immédiat', 'urgence absolue'];
    const divisifScore = divisifMarkers.filter(m => lower.includes(m)).length;
    if (divisifScore >= 2) return 'DIVISIF';

    // Marqueurs MANIPULATIF (émotions exploitées, urgence artificielle)
    const manipMarkers = ['dernière chance', 'agissez maintenant', 'ne ratez pas',
      'secret révélé', 'ils ne veulent pas que vous', 'choquant', 'incroyable'];
    const manipScore = manipMarkers.filter(m => lower.includes(m)).length;
    if (manipScore >= 2) return 'MANIPULATIF';

    // Marqueurs COMMERCIAL
    const commercialMarkers = ['achetez', 'promotion', 'réduction', 'offre limitée',
      'gratuit', 'essai', 'abonnez', 'prix'];
    const commercialScore = commercialMarkers.filter(m => lower.includes(m)).length;
    if (commercialScore >= 2) return 'COMMERCIAL';

    // Marqueurs PERSUASIF (opinion structurée)
    const persuasifMarkers = ['je pense que', 'il faut', 'nous devons', 'il est clair',
      'évidemment', 'sans aucun doute', 'la solution est'];
    const persuasifScore = persuasifMarkers.filter(m => lower.includes(m)).length;
    if (persuasifScore >= 2) return 'PERSUASIF';

    // Par défaut : INFORMATIF
    return 'INFORMATIF';
  }

  /**
   * Vérifie si un contenu passe le seuil de résonance minimal
   */
  static meetsResonanceThreshold(score: InformationResonanceScore, threshold: number = 50): boolean {
    return score.score_global >= threshold && score.intention_detectee !== 'MANIPULATIF';
  }
}

// ═══════════════════════════════════════════════════════════
// FILTRE D'INTENTION — SERVIR vs EXTRAIRE
// ═══════════════════════════════════════════════════════════

/**
 * Filtre d'intention AT-OM.
 * Chaque fonctionnalité, chaque action, chaque décision est filtrée :
 * "Cette action SERT-elle l'épanouissement humain,
 *  ou EXTRAIT-elle de la valeur des humains ?"
 */
export class IntentionGuard {

  /**
   * Exécute le filtre d'intention sur une action.
   * Retourne SERVIR ou EXTRAIRE avec le détail du diagnostic.
   */
  static evaluate(action: {
    description: string;
    sert_epanouissement?: boolean;
    respecte_souverainete?: boolean;
    est_transparent?: boolean;
    cree_plus_de_valeur?: boolean;
    aligne_spheres?: boolean;
    visible_par_tous?: boolean;
  }): IntentionCheck {
    const checks = {
      sert_epanouissement: action.sert_epanouissement ?? true,
      respecte_souverainete: action.respecte_souverainete ?? true,
      est_transparent: action.est_transparent ?? true,
      cree_plus_de_valeur: action.cree_plus_de_valeur ?? true,
      aligne_9_spheres: action.aligne_spheres ?? true,
      visible_par_tous: action.visible_par_tous ?? true,
    };

    // Si l'un des critères échoue → EXTRAIRE
    const allPass = Object.values(checks).every(v => v === true);

    return {
      action: action.description,
      ...checks,
      verdict: allPass ? 'SERVIR' : 'EXTRAIRE',
    };
  }

  /**
   * Les 7 principes non-négociables de l'Arche.
   * Si une action viole l'un d'entre eux, elle est rejetée.
   */
  static readonly IMMUTABLE_PRINCIPLES = [
    'Souveraineté individuelle — Chaque être possède ses données, son identité, son temps',
    'Transparence totale — Toutes les transactions et décisions sont publiques',
    'Non-extraction — Le système ne peut jamais extraire de valeur des utilisateurs',
    'Consentement éclairé — Rien sans compréhension et acceptation',
    'Droit de sortie — Quiconque peut quitter avec toutes ses données',
    'Équité d\'accès — Fonctionnalités de base accessibles à tous',
    'Vérité préservée — L\'histoire n\'est pas réécrite, les données pas falsifiées',
  ] as const;

  /**
   * Vérifie si une action respecte les 7 principes immuables
   */
  static checkPrinciples(action: string): { respects: boolean; violations: string[] } {
    // En mode production, ceci utiliserait l'IA pour analyser l'action
    // Pour l'instant : vérification de base sur les mots-clés
    const violations: string[] = [];
    const lower = action.toLowerCase();

    if (lower.includes('supprimer') && lower.includes('données utilisateur'))
      violations.push('Violation: Souveraineté individuelle');
    if (lower.includes('cacher') || lower.includes('secret'))
      violations.push('Violation possible: Transparence totale');
    if (lower.includes('forcer') || lower.includes('obliger'))
      violations.push('Violation: Consentement éclairé');
    if (lower.includes('bloquer sortie') || lower.includes('empêcher départ'))
      violations.push('Violation: Droit de sortie');
    if (lower.includes('paywall') && lower.includes('fondamental'))
      violations.push('Violation: Équité d\'accès');

    return { respects: violations.length === 0, violations };
  }
}

// ═══════════════════════════════════════════════════════════
// VALIDATEUR DES 7 LOIS UNIVERSELLES
// ═══════════════════════════════════════════════════════════

/**
 * Vérifie l'alignement d'une donnée ou action avec les 7 Lois Universelles.
 * Utilisé par le PolishingEngine comme couche de validation supplémentaire.
 */
export class UniversalLawValidator {

  /**
   * Vérifie la Loi de Correspondance :
   * La donnée doit être cohérente entre les niveaux micro (node) et macro (sphère)
   */
  static checkCorrespondance(node: ATOMNode, rosetta: RosettaTranslation): boolean {
    // Le niveau de résonance du node doit correspondre à la fréquence spirit
    const expected = node.resonance_level * 111;
    return rosetta.spirit.frequency_hz === expected;
  }

  /**
   * Vérifie la Loi de Vibration :
   * La donnée doit avoir une fréquence positive et dans la matrice 111-999
   */
  static checkVibration(rosetta: RosettaTranslation): boolean {
    const hz = rosetta.spirit.frequency_hz;
    return hz >= 111 && hz <= 999 && hz % 111 === 0;
  }

  /**
   * Vérifie la Loi de Polarité :
   * Les 3 dimensions Rosetta doivent être présentes (TECH + PEOPLE + SPIRIT = union des pôles)
   */
  static checkPolarite(rosetta: RosettaTranslation): boolean {
    return !!rosetta.tech?.data_type && !!rosetta.people?.narrative && !!rosetta.spirit?.frequency_hz;
  }

  /**
   * Vérifie la Loi de Cause à Effet :
   * La donnée doit avoir un hash d'intégrité (traçabilité)
   */
  static checkCauseEffet(rosetta: RosettaTranslation): boolean {
    return !!rosetta.integrity_hash && rosetta.integrity_hash.length > 0;
  }

  /**
   * Évaluation complète — retourne les lois respectées et violées
   */
  static fullAudit(node: ATOMNode, rosetta: RosettaTranslation): {
    score: number;
    passed: UniversalLaw[];
    failed: UniversalLaw[];
  } {
    const results: [UniversalLaw, boolean][] = [
      ['CORRESPONDANCE', this.checkCorrespondance(node, rosetta)],
      ['VIBRATION', this.checkVibration(rosetta)],
      ['POLARITE', this.checkPolarite(rosetta)],
      ['CAUSE_EFFET', this.checkCauseEffet(rosetta)],
      // RYTHME, GENRE, MENTALISME — vérifié au niveau macro (système), pas micro (node)
      ['RYTHME', true],
      ['GENRE', true],
      ['MENTALISME', true],
    ];

    const passed = results.filter(([_, ok]) => ok).map(([law]) => law);
    const failed = results.filter(([_, ok]) => !ok).map(([law]) => law);

    return {
      score: Math.round((passed.length / results.length) * 100),
      passed,
      failed,
    };
  }
}
