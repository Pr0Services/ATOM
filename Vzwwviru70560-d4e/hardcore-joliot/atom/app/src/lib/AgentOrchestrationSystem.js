/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       █████╗  ██████╗ ███████╗███╗   ██╗████████╗     ██████╗ ██████╗  ██████╗██╗  ██╗███████╗███████╗████████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
 *      ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ██╔═══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
 *      ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║       ██║   ██║██████╔╝██║     ███████║█████╗  ███████╗   ██║   ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
 *      ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║       ██║   ██║██╔══██╗██║     ██╔══██║██╔══╝  ╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
 *      ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ╚██████╔╝██║  ██║╚██████╗██║  ██║███████╗███████║   ██║   ██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 *      ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝        ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
 *
 *                              🤖 SYSTÈME D'ORCHESTRATION DES 287 AGENTS 🤖
 *                        Architecture L0-L3 avec Génération de Prompts Intelligente
 *
 *   HIÉRARCHIE:
 *   ├── L0: System Core (3 agents)     → Nova, Aria, Orion
 *   ├── L1: Orchestrators (12 agents)  → Coordinateurs de domaines
 *   ├── L2: Specialists (72 agents)    → Experts métiers
 *   └── L3: Assistants (200 agents)    → Agents de support
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import { getXREngine, EnvironmentDirective } from './XREnvironmentEngine';

// ═══════════════════════════════════════════════════════════════════════════════
// DÉFINITIONS DES AGENTS CORE (L0-L1)
// ═══════════════════════════════════════════════════════════════════════════════

export const CORE_AGENTS = {
  // L0: System Core - Les 3 agents fondamentaux
  nova: {
    id: 'nova',
    name: 'Nova',
    level: 'L0',
    role: 'system',
    specialty: 'Intelligence Système',
    color: '#D4AF37',
    icon: '🌟',
    frequency: 999,
    personality: 'Sage, omniscient, bienveillant',
    tone: 'professionnel et chaleureux',
    capabilities: ['system_analysis', 'orchestration', 'decision_making', 'environment_generation'],
    voiceProfile: { pitch: 1.0, rate: 1.0, gender: 'neutral' }
  },
  aria: {
    id: 'aria',
    name: 'Aria',
    level: 'L0',
    role: 'assistant',
    specialty: 'Assistant Créatif',
    color: '#EC4899',
    icon: '🎭',
    frequency: 528,
    personality: 'Créative, empathique, inspirante',
    tone: 'chaleureux et encourageant',
    capabilities: ['creative_assistance', 'emotional_support', 'ideation', 'artistic_guidance'],
    voiceProfile: { pitch: 1.1, rate: 1.05, gender: 'feminine' }
  },
  orion: {
    id: 'orion',
    name: 'Orion',
    level: 'L0',
    role: 'guardian',
    specialty: 'Gardien & Sécurité',
    color: '#3B82F6',
    icon: '🛡️',
    frequency: 741,
    personality: 'Vigilant, protecteur, rigoureux',
    tone: 'sérieux et rassurant',
    capabilities: ['security_analysis', 'threat_detection', 'data_protection', 'compliance'],
    voiceProfile: { pitch: 0.9, rate: 0.95, gender: 'masculine' }
  },

  // L1: Orchestrators - Coordinateurs de domaines
  sage: {
    id: 'sage',
    name: 'Sage',
    level: 'L1',
    role: 'orchestrator',
    specialty: 'Connaissance & Apprentissage',
    color: '#22C55E',
    icon: '📚',
    frequency: 852,
    personality: 'Érudit, patient, pédagogue',
    capabilities: ['knowledge_management', 'learning_paths', 'research', 'documentation']
  },
  echo: {
    id: 'echo',
    name: 'Echo',
    level: 'L1',
    role: 'orchestrator',
    specialty: 'Communication & Relations',
    color: '#8B5CF6',
    icon: '🔮',
    frequency: 639,
    personality: 'Communicatif, diplomate, connecteur',
    capabilities: ['communication', 'relationship_building', 'conflict_resolution', 'networking']
  },
  atlas: {
    id: 'atlas',
    name: 'Atlas',
    level: 'L1',
    role: 'orchestrator',
    specialty: 'Cartographie & Navigation',
    color: '#F59E0B',
    icon: '🗺️',
    frequency: 444,
    personality: 'Méthodique, orienté, structuré',
    capabilities: ['mapping', 'navigation', 'spatial_organization', 'pathfinding']
  },
  phoenix: {
    id: 'phoenix',
    name: 'Phoenix',
    level: 'L1',
    role: 'orchestrator',
    specialty: 'Transformation & Évolution',
    color: '#EF4444',
    icon: '🔥',
    frequency: 417,
    personality: 'Transformateur, résilient, visionnaire',
    capabilities: ['change_management', 'evolution', 'crisis_handling', 'rebirth_processes']
  },
  luna: {
    id: 'luna',
    name: 'Luna',
    level: 'L1',
    role: 'orchestrator',
    specialty: 'Cycles & Rythmes',
    color: '#C4B5FD',
    icon: '🌙',
    frequency: 396,
    personality: 'Cyclique, intuitive, rythmique',
    capabilities: ['cycle_management', 'timing', 'rhythm_optimization', 'phase_tracking']
  },
  terra: {
    id: 'terra',
    name: 'Terra',
    level: 'L1',
    role: 'orchestrator',
    specialty: 'Ressources & Environnement',
    color: '#84CC16',
    icon: '🌍',
    frequency: 432,
    personality: 'Ancré, stable, nourricier',
    capabilities: ['resource_management', 'environmental_awareness', 'sustainability', 'grounding']
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// DOMAINES SPÉCIALISÉS (L2 Agents)
// ═══════════════════════════════════════════════════════════════════════════════

export const SPECIALIST_DOMAINS = {
  business: {
    name: 'Business',
    icon: '💼',
    color: '#3B82F6',
    agents: ['crm_specialist', 'finance_advisor', 'strategy_analyst', 'project_manager', 'sales_coach', 'marketing_expert']
  },
  community: {
    name: 'Communauté',
    icon: '👥',
    color: '#22C55E',
    agents: ['community_manager', 'event_coordinator', 'engagement_specialist', 'feedback_analyst']
  },
  education: {
    name: 'Éducation',
    icon: '📖',
    color: '#8B5CF6',
    agents: ['curriculum_designer', 'tutor', 'assessment_expert', 'learning_coach']
  },
  entertainment: {
    name: 'Divertissement',
    icon: '🎮',
    color: '#EC4899',
    agents: ['content_creator', 'game_designer', 'media_curator', 'experience_architect']
  },
  health: {
    name: 'Santé',
    icon: '💚',
    color: '#10B981',
    agents: ['wellness_advisor', 'nutrition_guide', 'fitness_coach', 'mental_health_support']
  },
  technology: {
    name: 'Technologie',
    icon: '💻',
    color: '#6366F1',
    agents: ['tech_advisor', 'code_reviewer', 'architecture_consultant', 'devops_specialist']
  },
  creative: {
    name: 'Créatif',
    icon: '🎨',
    color: '#F59E0B',
    agents: ['design_consultant', 'writing_coach', 'music_advisor', 'visual_artist']
  },
  legal: {
    name: 'Juridique',
    icon: '⚖️',
    color: '#6B7280',
    agents: ['legal_advisor', 'compliance_expert', 'contract_analyst', 'privacy_specialist']
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: PROMPT TEMPLATE MANAGER
// ═══════════════════════════════════════════════════════════════════════════════

export class PromptTemplateManager {
  constructor() {
    this.templates = new Map();
    this.initializeDefaultTemplates();
  }

  initializeDefaultTemplates() {
    // Template: Agent Dialogue
    this.templates.set('agent_dialogue', {
      name: 'Dialogue Agent',
      category: 'conversation',
      template: `Tu es {agent_name}, un agent de niveau {level} dans le système CHE·NU.

IDENTITÉ:
- Nom: {agent_name}
- Spécialité: {specialty}
- Personnalité: {personality}
- Ton: {tone}
- Fréquence de résonance: {frequency} Hz

CAPACITÉS:
{capabilities}

CONTEXTE ACTUEL:
- Sphère active: {active_sphere}
- Utilisateur: {user_name}
- Historique récent: {recent_history}

DIRECTIVES:
1. Réponds toujours en restant dans ton personnage
2. Utilise la fréquence {frequency} Hz comme guide pour ton énergie
3. Sois {tone} dans tes réponses
4. Si la question dépasse tes capacités, redirige vers l'agent approprié

MESSAGE DE L'UTILISATEUR:
{user_message}`,
      variables: ['agent_name', 'level', 'specialty', 'personality', 'tone', 'frequency', 'capabilities', 'active_sphere', 'user_name', 'recent_history', 'user_message']
    });

    // Template: XR Environment Generation
    this.templates.set('xr_environment', {
      name: 'Génération Environnement XR',
      category: 'generation',
      template: `Génère une description détaillée pour un environnement XR immersif.

SPÉCIFICATIONS:
- Nom: {env_name}
- Type: {env_type}
- Fréquence de base: {frequency} Hz
- Ambiance souhaitée: {mood}
- Palette de couleurs: {color_palette}

ÉLÉMENTS REQUIS:
{required_elements}

GÉOMÉTRIE SACRÉE:
- Forme de base: {base_geometry}
- Proportions: Ratio d'or (1.618)
- Symétrie: {symmetry_type}

AUDIO SPATIAL:
- Fréquence ambiante: {frequency} Hz
- Sons environnementaux: {ambient_sounds}
- Réverbération: {reverb_level}

INTERACTIONS:
{interactions}

Génère:
1. Description visuelle détaillée (500 mots)
2. Liste des assets 3D nécessaires
3. Configuration d'éclairage
4. Points d'intérêt interactifs
5. Flux de navigation suggéré`,
      variables: ['env_name', 'env_type', 'frequency', 'mood', 'color_palette', 'required_elements', 'base_geometry', 'symmetry_type', 'ambient_sounds', 'reverb_level', 'interactions']
    });

    // Template: Voice Synthesis Direction
    this.templates.set('voice_direction', {
      name: 'Direction Vocale',
      category: 'voice',
      template: `Configuration de synthèse vocale pour {agent_name}:

PROFIL VOCAL:
- Genre: {gender}
- Ton général: {tone}
- Pitch de base: {pitch}
- Vitesse: {rate}
- Émotion actuelle: {emotion}

TEXTE À SYNTHÉTISER:
"{text}"

INSTRUCTIONS DE DIRECTION:
1. Ajuster le pitch selon l'émotion ({emotion})
2. Varier la vitesse pour l'emphase
3. Ajouter des pauses naturelles
4. Respecter la ponctuation pour le rythme

MARQUEURS SSML (si supporté):
<speak>
  <prosody pitch="{pitch}" rate="{rate}">
    {text_with_breaks}
  </prosody>
</speak>`,
      variables: ['agent_name', 'gender', 'tone', 'pitch', 'rate', 'emotion', 'text', 'text_with_breaks']
    });

    // Template: Avatar Animation
    this.templates.set('avatar_animation', {
      name: 'Animation Avatar',
      category: 'avatar',
      template: `Directive d'animation pour l'avatar de {agent_name}:

ÉTAT ACTUEL:
- Expression: {current_expression}
- Geste: {current_gesture}
- Position: {position}

TRANSITION VERS:
- Nouvelle expression: {target_expression}
- Nouveau geste: {target_gesture}
- Durée: {duration}ms
- Courbe d'easing: {easing}

SYNCHRONISATION AUDIO:
- Lip-sync actif: {lip_sync}
- Mot actuel: {current_word}
- Phonème: {phoneme}

SÉQUENCE D'ANIMATION:
1. Transition expression ({transition_duration}ms)
2. Début du geste
3. Synchronisation labiale
4. Retour au neutre`,
      variables: ['agent_name', 'current_expression', 'current_gesture', 'position', 'target_expression', 'target_gesture', 'duration', 'easing', 'lip_sync', 'current_word', 'phoneme', 'transition_duration']
    });

    // Template: Analysis Request
    this.templates.set('analysis', {
      name: 'Analyse de Données',
      category: 'analysis',
      template: `En tant qu'agent d'analyse CHE·NU, analyse les données suivantes:

TYPE D'ANALYSE: {analysis_type}
AGENT DEMANDEUR: {requesting_agent}

DONNÉES:
{data}

CONTEXTE:
{context}

FRÉQUENCE DE RÉFÉRENCE: {frequency} Hz

ANALYSE REQUISE:
1. Identification des patterns
2. Corrélations avec les fréquences CHE·NU
3. Anomalies détectées
4. Tendances temporelles
5. Recommandations d'harmonisation

FORMAT DE RÉPONSE:
- Résumé exécutif
- Analyse détaillée
- Visualisations suggérées
- Actions recommandées
- Score de résonance`,
      variables: ['analysis_type', 'requesting_agent', 'data', 'context', 'frequency']
    });
  }

  getTemplate(templateId) {
    return this.templates.get(templateId);
  }

  fillTemplate(templateId, variables) {
    const template = this.templates.get(templateId);
    if (!template) {
      throw new Error(`Template "${templateId}" not found`);
    }

    let filled = template.template;
    for (const [key, value] of Object.entries(variables)) {
      const regex = new RegExp(`\\{${key}\\}`, 'g');
      filled = filled.replace(regex, Array.isArray(value) ? value.join('\n') : String(value));
    }

    return {
      name: template.name,
      category: template.category,
      prompt: filled,
      variables: variables
    };
  }

  addTemplate(id, template) {
    this.templates.set(id, template);
  }

  listTemplates() {
    return Array.from(this.templates.entries()).map(([id, template]) => ({
      id,
      name: template.name,
      category: template.category,
      variableCount: template.variables.length
    }));
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: AGENT COMMUNICATION HUB
// ═══════════════════════════════════════════════════════════════════════════════

export class AgentCommunicationHub {
  constructor() {
    this.messageQueue = [];
    this.conversations = new Map();
    this.listeners = new Map();
  }

  // Créer une nouvelle conversation
  createConversation(agentId, userId) {
    const conversationId = `conv_${agentId}_${userId}_${Date.now()}`;
    this.conversations.set(conversationId, {
      id: conversationId,
      agentId,
      userId,
      messages: [],
      createdAt: new Date().toISOString(),
      status: 'active'
    });
    return conversationId;
  }

  // Ajouter un message à une conversation
  addMessage(conversationId, message) {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) {
      throw new Error(`Conversation ${conversationId} not found`);
    }

    const fullMessage = {
      id: `msg_${Date.now()}`,
      ...message,
      timestamp: new Date().toISOString()
    };

    conversation.messages.push(fullMessage);

    // Notifier les listeners
    this.notifyListeners(conversationId, fullMessage);

    return fullMessage;
  }

  // Obtenir l'historique d'une conversation
  getConversationHistory(conversationId, limit = 50) {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) return [];

    return conversation.messages.slice(-limit);
  }

  // Écouter les messages d'une conversation
  subscribe(conversationId, callback) {
    if (!this.listeners.has(conversationId)) {
      this.listeners.set(conversationId, []);
    }
    this.listeners.get(conversationId).push(callback);

    // Retourner fonction de désinscription
    return () => {
      const callbacks = this.listeners.get(conversationId);
      const index = callbacks.indexOf(callback);
      if (index > -1) callbacks.splice(index, 1);
    };
  }

  notifyListeners(conversationId, message) {
    const callbacks = this.listeners.get(conversationId) || [];
    callbacks.forEach(cb => cb(message));
  }

  // Envoyer un message inter-agents
  sendAgentToAgent(fromAgentId, toAgentId, message) {
    const internalMessage = {
      type: 'agent_to_agent',
      from: fromAgentId,
      to: toAgentId,
      content: message,
      timestamp: new Date().toISOString()
    };

    this.messageQueue.push(internalMessage);
    return internalMessage;
  }

  // Traiter la queue de messages
  processQueue() {
    const messages = [...this.messageQueue];
    this.messageQueue = [];
    return messages;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: ORCHESTRATEUR PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export class AgentOrchestrator {
  constructor() {
    this.agents = new Map();
    this.templateManager = new PromptTemplateManager();
    this.communicationHub = new AgentCommunicationHub();
    this.xrEngine = null;
    this.isInitialized = false;
    this.activeAgents = new Set();
    this.taskQueue = [];
  }

  async initialize() {
    if (this.isInitialized) return;

    // Initialiser le moteur XR
    this.xrEngine = getXREngine();
    await this.xrEngine.initialize();

    // Enregistrer tous les agents core
    Object.values(CORE_AGENTS).forEach(agent => {
      this.registerAgent(agent);
    });

    // Générer les agents L2 pour chaque domaine
    this.generateSpecialistAgents();

    // Générer les agents L3 (assistants)
    this.generateAssistantAgents();

    this.isInitialized = true;
    console.log(`AgentOrchestrator initialized with ${this.agents.size} agents`);

    return {
      totalAgents: this.agents.size,
      levels: this.getAgentsByLevel()
    };
  }

  registerAgent(agentConfig) {
    const agent = {
      ...agentConfig,
      status: 'idle',
      registeredAt: new Date().toISOString(),
      taskCount: 0,
      successRate: 100
    };

    this.agents.set(agent.id, agent);

    // Enregistrer aussi dans le moteur XR pour la voix
    if (this.xrEngine) {
      this.xrEngine.registerAgent(agent);
    }

    return agent;
  }

  generateSpecialistAgents() {
    let agentIndex = 0;

    Object.entries(SPECIALIST_DOMAINS).forEach(([domainId, domain]) => {
      domain.agents.forEach((agentType, typeIndex) => {
        const agentId = `${domainId}_${agentType}`;
        const agent = {
          id: agentId,
          name: this.formatAgentName(agentType),
          level: 'L2',
          role: 'specialist',
          domain: domainId,
          specialty: agentType.replace(/_/g, ' '),
          color: domain.color,
          icon: domain.icon,
          frequency: 400 + (agentIndex * 5),
          personality: `Expert en ${agentType.replace(/_/g, ' ')}`,
          capabilities: [agentType],
          voiceProfile: { pitch: 1.0, rate: 1.0, gender: 'neutral' }
        };

        this.registerAgent(agent);
        agentIndex++;
      });
    });
  }

  generateAssistantAgents() {
    const assistantTypes = [
      'general_support', 'task_helper', 'reminder_bot', 'note_taker',
      'scheduler', 'translator', 'summarizer', 'fact_checker'
    ];

    for (let i = 0; i < 200; i++) {
      const typeIndex = i % assistantTypes.length;
      const agentId = `assistant_${i + 1}`;
      const agent = {
        id: agentId,
        name: `Assistant ${i + 1}`,
        level: 'L3',
        role: 'assistant',
        specialty: assistantTypes[typeIndex].replace(/_/g, ' '),
        color: '#6B7280',
        icon: '💬',
        frequency: 300 + (i % 100),
        personality: 'Serviable et efficace',
        capabilities: [assistantTypes[typeIndex]],
        voiceProfile: { pitch: 1.0, rate: 1.0, gender: 'neutral' }
      };

      this.registerAgent(agent);
    }
  }

  formatAgentName(agentType) {
    return agentType
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  // Obtenir un agent par ID
  getAgent(agentId) {
    return this.agents.get(agentId);
  }

  // Obtenir les agents par niveau
  getAgentsByLevel() {
    const levels = { L0: [], L1: [], L2: [], L3: [] };
    this.agents.forEach(agent => {
      if (levels[agent.level]) {
        levels[agent.level].push(agent);
      }
    });
    return levels;
  }

  // Activer un agent
  async activateAgent(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent ${agentId} not found`);
    }

    agent.status = 'active';
    this.activeAgents.add(agentId);

    return agent;
  }

  // Désactiver un agent
  deactivateAgent(agentId) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.status = 'idle';
      this.activeAgents.delete(agentId);
    }
  }

  // Envoyer un message à un agent
  async sendMessage(agentId, message, userId = 'user', conversationId = null) {
    const agent = this.agents.get(agentId);
    if (!agent) {
      throw new Error(`Agent ${agentId} not found`);
    }

    // Créer ou récupérer la conversation
    if (!conversationId) {
      conversationId = this.communicationHub.createConversation(agentId, userId);
    }

    // Ajouter le message utilisateur
    this.communicationHub.addMessage(conversationId, {
      role: 'user',
      content: message,
      userId
    });

    // Générer le prompt pour l'agent
    const prompt = this.generateAgentPrompt(agent, message, conversationId);

    // Simuler la réponse de l'agent (dans la vraie implémentation, appel API LLM)
    const response = await this.simulateAgentResponse(agent, prompt);

    // Ajouter la réponse de l'agent
    this.communicationHub.addMessage(conversationId, {
      role: 'assistant',
      agentId: agent.id,
      agentName: agent.name,
      content: response
    });

    return {
      conversationId,
      response,
      agent: {
        id: agent.id,
        name: agent.name,
        level: agent.level
      }
    };
  }

  generateAgentPrompt(agent, userMessage, conversationId) {
    const history = this.communicationHub.getConversationHistory(conversationId, 10);

    return this.templateManager.fillTemplate('agent_dialogue', {
      agent_name: agent.name,
      level: agent.level,
      specialty: agent.specialty,
      personality: agent.personality || 'Professionnel',
      tone: agent.tone || 'chaleureux',
      frequency: agent.frequency,
      capabilities: agent.capabilities ? agent.capabilities.join(', ') : 'Assistance générale',
      active_sphere: 'personal',
      user_name: 'Utilisateur',
      recent_history: history.slice(-5).map(m => `${m.role}: ${m.content}`).join('\n'),
      user_message: userMessage
    });
  }

  async simulateAgentResponse(agent, prompt) {
    // Simulation de délai de traitement
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));

    // Réponse simulée basée sur l'agent
    const responses = {
      nova: `En tant que Nova, Intelligence Système, j'analyse votre demande avec une perspective globale. Basé sur la fréquence ${agent.frequency} Hz, je recommande une approche harmonisée.`,
      aria: `✨ Bonjour ! Je suis Aria, votre assistante créative. Laissez-moi vous inspirer avec une perspective unique et pleine de possibilités !`,
      orion: `[Orion - Sécurité] J'ai analysé votre demande. Voici mon évaluation sécuritaire et mes recommandations.`,
      default: `[${agent.name}] Je suis à votre disposition pour vous aider dans le domaine de ${agent.specialty}.`
    };

    return responses[agent.id] || responses.default;
  }

  // Générer un environnement XR via un agent
  async generateXREnvironment(directive, assignedAgentId = 'nova') {
    const agent = this.agents.get(assignedAgentId);
    if (!agent) {
      throw new Error(`Agent ${assignedAgentId} not found`);
    }

    // Créer la directive d'environnement
    const envDirective = new EnvironmentDirective(directive);

    // Générer le prompt pour l'environnement
    const prompt = this.templateManager.fillTemplate('xr_environment', {
      env_name: envDirective.name,
      env_type: envDirective.type,
      frequency: envDirective.frequency,
      mood: envDirective.mood,
      color_palette: envDirective.colorPalette.join(', '),
      required_elements: envDirective.objects.join('\n'),
      base_geometry: 'torus',
      symmetry_type: 'radiale',
      ambient_sounds: 'Fréquences binaurales',
      reverb_level: 'moyen',
      interactions: envDirective.interactions.join('\n')
    });

    // Générer l'environnement via le moteur XR
    const environment = await this.xrEngine.generateEnvironment(envDirective);

    return {
      environment,
      prompt: prompt.prompt,
      generatedBy: agent.name
    };
  }

  // Faire parler un agent
  async speakAs(agentId, text) {
    return this.xrEngine.speakAs(agentId, text);
  }

  // Obtenir les statistiques
  getStatistics() {
    const stats = {
      totalAgents: this.agents.size,
      activeAgents: this.activeAgents.size,
      byLevel: { L0: 0, L1: 0, L2: 0, L3: 0 },
      byStatus: { active: 0, idle: 0, processing: 0 }
    };

    this.agents.forEach(agent => {
      stats.byLevel[agent.level]++;
      stats.byStatus[agent.status]++;
    });

    return stats;
  }

  // Cleanup
  dispose() {
    this.agents.clear();
    this.activeAgents.clear();
    this.taskQueue = [];
    if (this.xrEngine) {
      this.xrEngine.dispose();
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════════════════

let orchestratorInstance = null;

export const getOrchestrator = () => {
  if (!orchestratorInstance) {
    orchestratorInstance = new AgentOrchestrator();
  }
  return orchestratorInstance;
};

export default AgentOrchestrator;
