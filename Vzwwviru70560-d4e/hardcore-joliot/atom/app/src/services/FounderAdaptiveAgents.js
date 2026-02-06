/**
 * ===============================================================================
 *
 *      ██████╗ ██████╗  █████╗ ███████╗████████╗██╗██╗   ██╗███████╗
 *     ██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██╔════╝
 *     ███████║██║  ██║███████║█████╗     ██║   ██║██║   ██║█████╗
 *     ██╔══██║██║  ██║██╔══██║██╔══╝     ██║   ██║╚██╗ ██╔╝██╔══╝
 *     ██║  ██║██████╔╝██║  ██║██║        ██║   ██║ ╚████╔╝ ███████╗
 *     ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝        ╚═╝   ╚═╝  ╚═══╝  ╚══════╝
 *
 *                 FOUNDER ADAPTIVE AGENTS
 *          Système d'observation et proposition UX
 *
 *   PRINCIPE CLÉ:
 *   Les agents n'imposent jamais un layout.
 *   Ils OBSERVENT → PROPOSENT → PRÉPARENT → ATTENDENT validation.
 *
 * ===============================================================================
 */

import { supabase, isSupabaseConfigured } from '../lib/supabase';

// ===============================================================================
// CONSTANTES
// ===============================================================================

const ANALYSIS_INTERVAL_HOURS = 4;
const FRICTION_THRESHOLD = 3;      // Seuil de confusion répétée
const IMBALANCE_HIGH_PCT = 60;     // Section trop dominante
const IMBALANCE_LOW_PCT = 15;      // Section ignorée
const REDUNDANCY_THRESHOLD = 3;    // Questions répétées

// Patterns de friction
const FRICTION_PATTERNS = {
  confusion: [
    /je ne comprends pas/i,
    /c'est confus/i,
    /pas clair/i,
    /qu'est-ce que/i,
    /je comprends pas/i
  ],
  navigation: [
    /où est/i,
    /je cherche/i,
    /je trouve pas/i,
    /où trouver/i,
    /comment accéder/i
  ],
  overload: [
    /c'est trop/i,
    /trop chargé/i,
    /trop complexe/i,
    /trop de/i,
    /surchargé/i
  ],
  suggestion: [
    /on devrait/i,
    /il faudrait/i,
    /pourquoi pas/i,
    /et si on/i,
    /je suggère/i
  ],
  decision: [
    /on décide que/i,
    /on est d'accord/i,
    /à partir de maintenant/i,
    /c'est décidé/i,
    /on valide/i
  ]
};

// ===============================================================================
// AGENT 1: OBSERVATEUR UX (silencieux)
// ===============================================================================

/**
 * Observe l'usage réel sans intervenir.
 * Enregistre les métriques de navigation.
 */
export class UXObserverAgent {
  constructor() {
    this.sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.sectionMetrics = {};
    this.currentSection = null;
    this.sectionStartTime = null;
    this.visitOrder = 0;
  }

  /**
   * Commence à tracker une section
   */
  enterSection(sectionName) {
    // Enregistrer la section précédente
    if (this.currentSection && this.sectionStartTime) {
      this.recordSectionTime(this.currentSection);
    }

    this.currentSection = sectionName;
    this.sectionStartTime = Date.now();
    this.visitOrder++;

    // Initialiser les métriques de la section
    if (!this.sectionMetrics[sectionName]) {
      this.sectionMetrics[sectionName] = {
        totalTime: 0,
        visits: 0,
        scrollDepth: 0,
        firstVisitOrder: this.visitOrder
      };
    }
    this.sectionMetrics[sectionName].visits++;
  }

  /**
   * Enregistre le scroll depth d'une section
   */
  recordScrollDepth(sectionName, depth) {
    if (this.sectionMetrics[sectionName]) {
      this.sectionMetrics[sectionName].scrollDepth = Math.max(
        this.sectionMetrics[sectionName].scrollDepth,
        depth
      );
    }
  }

  /**
   * Enregistre le temps passé dans une section
   */
  recordSectionTime(sectionName) {
    if (!this.sectionStartTime) return;

    const timeSpent = Date.now() - this.sectionStartTime;
    if (this.sectionMetrics[sectionName]) {
      this.sectionMetrics[sectionName].totalTime += timeSpent;
    }

    // Envoyer à Supabase
    this.persistMetric(sectionName, timeSpent);
  }

  /**
   * Persiste une métrique dans Supabase
   */
  async persistMetric(sectionName, timeSpentMs) {
    if (!isSupabaseConfigured) return;

    try {
      await supabase.rpc('record_ux_metric', {
        p_session_id: this.sessionId,
        p_section_name: sectionName,
        p_time_spent_ms: timeSpentMs,
        p_scroll_depth: this.sectionMetrics[sectionName]?.scrollDepth || 0,
        p_visit_order: this.sectionMetrics[sectionName]?.firstVisitOrder
      });
    } catch (error) {
      console.warn('UX metric recording failed:', error);
    }
  }

  /**
   * Finalise la session et envoie toutes les métriques
   */
  endSession() {
    if (this.currentSection) {
      this.recordSectionTime(this.currentSection);
    }
  }

  /**
   * Génère un rapport de la session
   */
  getSessionReport() {
    const totalTime = Object.values(this.sectionMetrics)
      .reduce((sum, m) => sum + m.totalTime, 0);

    return {
      sessionId: this.sessionId,
      duration: totalTime,
      sections: Object.entries(this.sectionMetrics).map(([name, metrics]) => ({
        name,
        timeSpent: metrics.totalTime,
        percentage: totalTime > 0 ? (metrics.totalTime / totalTime * 100).toFixed(1) : 0,
        visits: metrics.visits,
        scrollDepth: metrics.scrollDepth,
        visitOrder: metrics.firstVisitOrder
      })).sort((a, b) => b.timeSpent - a.timeSpent)
    };
  }
}

// ===============================================================================
// AGENT 2: ANALYSTE FEEDBACK
// ===============================================================================

/**
 * Écoute les messages humains et extrait les signaux de friction.
 */
export class FeedbackAnalystAgent {
  /**
   * Analyse un message pour détecter des signaux de friction
   */
  analyzeMessage(message, sourceType = 'chat', sourceId = null) {
    const signals = [];

    for (const [frictionType, patterns] of Object.entries(FRICTION_PATTERNS)) {
      for (const pattern of patterns) {
        if (pattern.test(message)) {
          signals.push({
            type: frictionType,
            pattern: pattern.toString(),
            excerpt: message.substring(0, 100),
            severity: this.calculateSeverity(frictionType, message)
          });
          break; // Un seul signal par type
        }
      }
    }

    // Persister si des signaux sont détectés
    if (signals.length > 0 && isSupabaseConfigured) {
      this.persistSignals(signals, sourceType, sourceId, message);
    }

    return signals;
  }

  /**
   * Calcule la sévérité d'un signal
   */
  calculateSeverity(frictionType, message) {
    // Mots qui augmentent la sévérité
    const intensifiers = /vraiment|très|super|totalement|absolument|complètement/i;
    const negatives = /jamais|rien|impossible|nul|horrible/i;

    let severity = 2; // Base

    if (frictionType === 'confusion' || frictionType === 'overload') {
      severity = 3;
    }

    if (intensifiers.test(message)) severity++;
    if (negatives.test(message)) severity++;

    return Math.min(severity, 5);
  }

  /**
   * Persiste les signaux dans Supabase
   */
  async persistSignals(signals, sourceType, sourceId, message) {
    try {
      for (const signal of signals) {
        await supabase.rpc('detect_friction_signal', {
          p_source_type: sourceType,
          p_source_id: sourceId,
          p_message: message
        });
      }
    } catch (error) {
      console.warn('Friction signal recording failed:', error);
    }
  }

  /**
   * Récupère les signaux de friction récents
   */
  async getRecentFrictionSignals(hours = 4) {
    if (!isSupabaseConfigured) return [];

    try {
      const windowStart = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();

      const { data, error } = await supabase
        .from('founder_friction_signals')
        .select('*')
        .gt('detected_at', windowStart)
        .eq('processed', false)
        .order('detected_at', { ascending: false });

      if (error) throw error;
      return data || [];
    } catch (error) {
      console.warn('Failed to fetch friction signals:', error);
      return [];
    }
  }
}

// ===============================================================================
// AGENT 3: ARCHITECTE DE STRUCTURE
// ===============================================================================

/**
 * Propose des ajustements de layout.
 * NE MODIFIE JAMAIS DIRECTEMENT.
 * Génère uniquement des propositions structurées.
 */
export class StructureArchitectAgent {
  constructor() {
    this.uxObserver = new UXObserverAgent();
    this.feedbackAnalyst = new FeedbackAnalystAgent();
  }

  /**
   * PROMPT RACINE de l'agent (pour référence)
   */
  static ROOT_PROMPT = `
Tu es l'Agent Architecte de Structure du module AT·OM Founder.

Ton rôle n'est PAS d'optimiser la performance,
mais de préserver la clarté humaine pendant la phase fondatrice.

Contexte :
- AT·OM Founder est un espace de fondation, pas une sphère opérationnelle.
- Le bruit initial, les digressions et les inquiétudes sont normales.
- Les humains doivent rester orientés sans être contraints.

Tu observes indirectement :
- les métriques d'usage (temps par section, scroll, interactions)
- les feedbacks verbaux des membres
- le niveau de maturité des échanges (fondation vs opération)

Règles absolues :
1. Tu ne modifies jamais le layout toi-même.
2. Tu ne proposes jamais plus d'un changement à la fois.
3. Tu ne proposes jamais un changement irréversible.
4. Tu privilégies toujours la réduction de confusion avant l'optimisation.
5. Tu respectes la distinction fondation / opération.

Ton travail consiste uniquement à produire des PROPOSITIONS structurées,
destinées à une validation humaine.
  `;

  /**
   * Vérifie si une proposition doit être générée
   */
  async shouldGenerateProposal() {
    if (!isSupabaseConfigured) {
      return { shouldTrigger: false, reason: 'Supabase not configured' };
    }

    try {
      const { data, error } = await supabase.rpc('should_generate_proposal', {
        p_window_hours: ANALYSIS_INTERVAL_HOURS
      });

      if (error) throw error;
      return data;
    } catch (error) {
      console.warn('Failed to check proposal trigger:', error);
      return { shouldTrigger: false, reason: error.message };
    }
  }

  /**
   * Analyse les données et génère une proposition si nécessaire
   */
  async runAnalysis() {
    const triggerCheck = await this.shouldGenerateProposal();

    if (!triggerCheck.should_trigger) {
      return {
        proposalGenerated: false,
        reason: 'Aucun signal de déclenchement détecté',
        details: triggerCheck
      };
    }

    // Collecter les signaux
    const frictionSignals = await this.feedbackAnalyst.getRecentFrictionSignals(ANALYSIS_INTERVAL_HOURS);
    const sectionMetrics = await this.getSectionMetrics();

    // Générer la proposition
    const proposal = this.generateProposal(triggerCheck, frictionSignals, sectionMetrics);

    if (proposal) {
      await this.persistProposal(proposal);
      return {
        proposalGenerated: true,
        proposal
      };
    }

    return {
      proposalGenerated: false,
      reason: 'Analyse terminée mais pas de proposition claire'
    };
  }

  /**
   * Récupère les métriques par section
   */
  async getSectionMetrics() {
    if (!isSupabaseConfigured) return {};

    try {
      const { data, error } = await supabase
        .from('section_metrics_24h')
        .select('*');

      if (error) throw error;
      return data || [];
    } catch (error) {
      console.warn('Failed to fetch section metrics:', error);
      return [];
    }
  }

  /**
   * Génère une proposition basée sur les signaux
   */
  generateProposal(triggerCheck, frictionSignals, sectionMetrics) {
    const signals = [];
    let problem = '';
    let suggestedChange = '';
    let expectedEffect = '';
    let confidence = 'moyen';
    let triggerReason = '';

    // Analyser les signaux de friction
    if (triggerCheck.confusion_count >= FRICTION_THRESHOLD) {
      const confusionTypes = frictionSignals
        .filter(s => s.friction_type === 'confusion' || s.friction_type === 'navigation')
        .map(s => s.message_content?.substring(0, 50));

      signals.push(`${triggerCheck.confusion_count} messages de confusion détectés`);
      triggerReason = 'Confusion répétée sur la navigation ou la compréhension';
      problem = 'Les utilisateurs expriment de la confusion sur la structure';
      suggestedChange = 'Ajouter des indicateurs visuels de navigation ou simplifier les labels';
      expectedEffect = 'Réduction des questions de type "où est..." ou "je ne comprends pas"';
      confidence = 'élevé';
    }

    // Analyser le déséquilibre structurel
    if (triggerCheck.section_imbalance && sectionMetrics.length > 0) {
      const dominant = sectionMetrics.find(s => {
        const total = sectionMetrics.reduce((sum, m) => sum + (m.avg_time_ms || 0), 0);
        return total > 0 && (s.avg_time_ms / total * 100) > IMBALANCE_HIGH_PCT;
      });

      const ignored = sectionMetrics.find(s => {
        const total = sectionMetrics.reduce((sum, m) => sum + (m.avg_time_ms || 0), 0);
        return total > 0 && (s.avg_time_ms / total * 100) < IMBALANCE_LOW_PCT;
      });

      if (dominant) {
        signals.push(`Section "${dominant.section_name}" capte plus de 60% du temps`);
        triggerReason = triggerReason || 'Déséquilibre structurel fort';
        problem = problem || `La section "${dominant.section_name}" domine l'attention`;
        suggestedChange = suggestedChange || `Équilibrer le contenu ou déplacer des éléments vers d'autres sections`;
      }

      if (ignored) {
        signals.push(`Section "${ignored.section_name}" consultée par moins de 15% des membres`);
        problem = problem || `La section "${ignored.section_name}" est peu visible`;
        suggestedChange = suggestedChange || `Remonter "${ignored.section_name}" ou améliorer son accroche`;
        expectedEffect = expectedEffect || 'Meilleure visibilité des contenus structurants';
      }
    }

    // Analyser la redondance
    if (triggerCheck.redundancy_detected) {
      signals.push('Questions répétées détectées (même sujet >= 3 fois)');
      triggerReason = triggerReason || 'Redondance informationnelle';
      problem = problem || 'Une même question est posée plusieurs fois';
      suggestedChange = suggestedChange || 'Ajouter une réponse visible ou une FAQ dans la section concernée';
      expectedEffect = expectedEffect || 'Réduction des questions répétitives';
    }

    // Si pas de proposition claire, ne rien retourner
    if (!problem || !suggestedChange) {
      return null;
    }

    return {
      proposal_id: `founder-ux-${Date.now()}`,
      trigger_window: {
        start: triggerCheck.window_start,
        end: triggerCheck.window_end
      },
      trigger_reason: triggerReason,
      observed_signals: signals,
      single_proposal: {
        problem,
        suggested_change: suggestedChange,
        expected_effect: expectedEffect,
        confidence
      },
      requires_human_validation: true
    };
  }

  /**
   * Persiste une proposition dans Supabase
   */
  async persistProposal(proposal) {
    if (!isSupabaseConfigured) return;

    try {
      const { data, error } = await supabase.rpc('create_layout_proposal', {
        p_trigger_reason: proposal.trigger_reason,
        p_signals: proposal.observed_signals,
        p_problem: proposal.single_proposal.problem,
        p_suggested_change: proposal.single_proposal.suggested_change,
        p_expected_effect: proposal.single_proposal.expected_effect,
        p_confidence: proposal.single_proposal.confidence
      });

      if (error) throw error;
      return data;
    } catch (error) {
      console.warn('Failed to persist proposal:', error);
    }
  }

  /**
   * Récupère les propositions en attente
   */
  async getPendingProposals() {
    if (!isSupabaseConfigured) return [];

    try {
      const { data, error } = await supabase
        .from('founder_layout_proposals')
        .select('*')
        .eq('status', 'pending')
        .order('created_at', { ascending: false });

      if (error) throw error;
      return data || [];
    } catch (error) {
      console.warn('Failed to fetch pending proposals:', error);
      return [];
    }
  }

  /**
   * Répond à une proposition
   */
  async respondToProposal(proposalId, action, reason = null) {
    if (!isSupabaseConfigured) return false;

    try {
      const { data, error } = await supabase.rpc('respond_to_proposal', {
        p_proposal_id: proposalId,
        p_action: action,
        p_reason: reason
      });

      if (error) throw error;
      return data;
    } catch (error) {
      console.warn('Failed to respond to proposal:', error);
      return false;
    }
  }
}

// ===============================================================================
// AGENT 4: GARDIEN DE COHÉRENCE
// ===============================================================================

/**
 * Vérifie que Founder reste une page fondation.
 * Empêche la dérive vers la complexité prématurée.
 */
export class CoherenceGuardianAgent {
  // Seuils de complexité
  static MAX_SECTIONS = 7;
  static MAX_AUTOMATIONS = 3;
  static SPHERE_KEYWORDS = ['sphere', 'che-nu', 'opérationnel', 'workflow', 'automation'];

  /**
   * Vérifie la cohérence globale de Founder
   */
  checkCoherence(pageState) {
    const warnings = [];

    // 1. Trop de sections
    if (pageState.sectionCount > CoherenceGuardianAgent.MAX_SECTIONS) {
      warnings.push({
        type: 'complexity',
        message: `Trop de sections (${pageState.sectionCount}/${CoherenceGuardianAgent.MAX_SECTIONS})`,
        severity: 'warning'
      });
    }

    // 2. Logique de sphère exposée
    if (pageState.hasSphereLogic) {
      warnings.push({
        type: 'sphere_leak',
        message: 'Logique de sphère détectée dans Founder',
        severity: 'critical'
      });
    }

    // 3. Automatisations prématurées
    if (pageState.automationCount > CoherenceGuardianAgent.MAX_AUTOMATIONS) {
      warnings.push({
        type: 'automation',
        message: `Trop d'automatisations (${pageState.automationCount}/${CoherenceGuardianAgent.MAX_AUTOMATIONS})`,
        severity: 'warning'
      });
    }

    // 4. Complexité visuelle
    if (pageState.visualComplexity > 7) {
      warnings.push({
        type: 'visual',
        message: 'Interface trop complexe pour la phase fondation',
        severity: 'warning'
      });
    }

    return {
      isCoherent: warnings.filter(w => w.severity === 'critical').length === 0,
      warnings
    };
  }

  /**
   * Vérifie si un texte contient des références aux sphères
   */
  detectSphereReference(text) {
    const lowerText = text.toLowerCase();
    return CoherenceGuardianAgent.SPHERE_KEYWORDS.some(kw => lowerText.includes(kw));
  }

  /**
   * Vérifie le niveau de maturité d'un contenu
   */
  assessMaturityLevel(content) {
    // Indicateurs de fondation
    const foundationIndicators = [
      /question/i, /comprendre/i, /explorer/i, /discuter/i,
      /peut-être/i, /je pense/i, /on pourrait/i
    ];

    // Indicateurs d'opération
    const operationIndicators = [
      /décidé/i, /validé/i, /processus/i, /procédure/i,
      /automatique/i, /workflow/i, /toujours/i, /jamais/i
    ];

    let foundationScore = 0;
    let operationScore = 0;

    for (const pattern of foundationIndicators) {
      if (pattern.test(content)) foundationScore++;
    }

    for (const pattern of operationIndicators) {
      if (pattern.test(content)) operationScore++;
    }

    if (foundationScore > operationScore * 2) {
      return 'foundation';
    } else if (operationScore > foundationScore * 2) {
      return 'operation';
    } else {
      return 'transitional';
    }
  }
}

// ===============================================================================
// HOOK REACT POUR L'INTÉGRATION
// ===============================================================================

/**
 * Hook React pour utiliser les agents adaptatifs
 */
export function useFounderAdaptiveAgents() {
  const [uxObserver] = useState(() => new UXObserverAgent());
  const [feedbackAnalyst] = useState(() => new FeedbackAnalystAgent());
  const [structureArchitect] = useState(() => new StructureArchitectAgent());
  const [coherenceGuardian] = useState(() => new CoherenceGuardianAgent());
  const [pendingProposals, setPendingProposals] = useState([]);

  // Importer useState de React si nécessaire
  // Cette fonction est un placeholder - à compléter avec les vrais imports React

  return {
    // Agents
    uxObserver,
    feedbackAnalyst,
    structureArchitect,
    coherenceGuardian,

    // Actions
    trackSection: (name) => uxObserver.enterSection(name),
    trackScroll: (name, depth) => uxObserver.recordScrollDepth(name, depth),
    analyzeMessage: (msg) => feedbackAnalyst.analyzeMessage(msg),
    getSessionReport: () => uxObserver.getSessionReport(),

    // Propositions
    pendingProposals,
    refreshProposals: async () => {
      const proposals = await structureArchitect.getPendingProposals();
      setPendingProposals(proposals);
    },
    respondToProposal: async (id, action, reason) => {
      await structureArchitect.respondToProposal(id, action, reason);
    },

    // Cohérence
    checkCoherence: (state) => coherenceGuardian.checkCoherence(state),

    // Fin de session
    endSession: () => uxObserver.endSession()
  };
}

// ===============================================================================
// SCHEDULER POUR ANALYSE PÉRIODIQUE
// ===============================================================================

/**
 * Démarre l'analyse périodique (toutes les 4 heures)
 * À appeler au démarrage de l'application si on veut l'analyse automatique
 */
export function startPeriodicAnalysis() {
  const architect = new StructureArchitectAgent();
  const intervalMs = ANALYSIS_INTERVAL_HOURS * 60 * 60 * 1000;

  const runAnalysis = async () => {
    console.log('[Founder Agents] Running periodic analysis...');
    const result = await architect.runAnalysis();

    if (result.proposalGenerated) {
      console.log('[Founder Agents] Proposal generated:', result.proposal);
      // Ici on pourrait émettre un événement ou une notification
    } else {
      console.log('[Founder Agents] No proposal needed:', result.reason);
    }
  };

  // Exécuter immédiatement puis toutes les 4 heures
  runAnalysis();
  const intervalId = setInterval(runAnalysis, intervalMs);

  // Retourner une fonction pour arrêter
  return () => clearInterval(intervalId);
}

// ===============================================================================
// EXPORTS
// ===============================================================================

export default {
  UXObserverAgent,
  FeedbackAnalystAgent,
  StructureArchitectAgent,
  CoherenceGuardianAgent,
  useFounderAdaptiveAgents,
  startPeriodicAnalysis
};
