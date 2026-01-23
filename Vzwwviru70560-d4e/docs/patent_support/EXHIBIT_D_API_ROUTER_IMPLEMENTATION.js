/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       █████╗ ██████╗ ██╗    ██████╗  ██████╗ ██╗   ██╗████████╗███████╗██████╗
 *      ██╔══██╗██╔══██╗██║    ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
 *      ███████║██████╔╝██║    ██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██████╔╝
 *      ██╔══██║██╔═══╝ ██║    ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
 *      ██║  ██║██║     ██║    ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║
 *      ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
 *
 *                           PROXY SOUVERAIN - ROUTEUR API UNIFIE
 *                    L'Arche comme centrale d'energie pour toutes les APIs
 *                              AT.OM / CHE.NU V76 - Grid System
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *   ARCHITECTURE:
 *   L'utilisateur -> Arche (Proxy) -> OpenRouter/API Unifiee -> Claude/GPT-4/Llama/etc.
 *
 *   AVANTAGES:
 *   - Une seule cle API maitre pour l'Arche
 *   - Utilisateurs n'ont jamais besoin de leurs propres cles
 *   - Tracking de consommation integre
 *   - Choix automatique du modele optimal
 *   - Confidentialite totale (SOVEREIGN_MODE)
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import { supabase } from '../lib/supabase';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION DES PROVIDERS
// ═══════════════════════════════════════════════════════════════════════════════

const API_PROVIDERS = {
  openrouter: {
    name: 'OpenRouter',
    baseUrl: 'https://openrouter.ai/api/v1',
    models: {
      'claude-3-opus': 'anthropic/claude-3-opus',
      'claude-3-sonnet': 'anthropic/claude-3-sonnet',
      'gpt-4': 'openai/gpt-4-turbo',
      'gpt-4o': 'openai/gpt-4o',
      'llama-3': 'meta-llama/llama-3-70b-instruct',
      'mistral-large': 'mistralai/mistral-large'
    },
    // Cout approximatif par 1000 tokens (en centimes)
    costs: {
      'claude-3-opus': { input: 1.5, output: 7.5 },
      'claude-3-sonnet': { input: 0.3, output: 1.5 },
      'gpt-4': { input: 1.0, output: 3.0 },
      'gpt-4o': { input: 0.5, output: 1.5 },
      'llama-3': { input: 0.07, output: 0.07 },
      'mistral-large': { input: 0.4, output: 1.2 }
    }
  },
  anthropic: {
    name: 'Anthropic Direct',
    baseUrl: 'https://api.anthropic.com/v1',
    models: {
      'claude-3-opus': 'claude-3-opus-20240229',
      'claude-3-sonnet': 'claude-3-sonnet-20240229',
      'claude-3-haiku': 'claude-3-haiku-20240307'
    }
  },
  openai: {
    name: 'OpenAI Direct',
    baseUrl: 'https://api.openai.com/v1',
    models: {
      'gpt-4': 'gpt-4-turbo-preview',
      'gpt-4o': 'gpt-4o',
      'gpt-3.5': 'gpt-3.5-turbo'
    }
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// SYSTEME DE CREDITS DE RESONANCE
// ═══════════════════════════════════════════════════════════════════════════════

// Credits mensuels selon le plan (en milliers de tokens)
const PLAN_CREDITS = {
  citoyen: 50000,      // Plan gratuit - 50K tokens/mois
  fondateur: 500000,   // Membres fondateurs - 500K tokens/mois
  souverain: Infinity  // Souverain - Illimite
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE: API ROUTER
// ═══════════════════════════════════════════════════════════════════════════════

class APIRouter {
  constructor() {
    this.defaultProvider = 'openrouter';
    this.defaultModel = 'claude-3-sonnet';
    this.usageCache = new Map();
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // VERIFICATION DES CREDITS
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * Verifie si l'utilisateur a assez de credits
   * @param {string} userId - ID de l'utilisateur
   * @param {number} estimatedTokens - Tokens estimes pour la requete
   * @returns {Promise<{allowed: boolean, remaining: number, message?: string}>}
   */
  async checkCredits(userId, estimatedTokens = 1000) {
    try {
      // Recuperer le profil utilisateur
      const { data: profile, error } = await supabase
        .from('profiles')
        .select('role')
        .eq('id', userId)
        .single();

      if (error) throw error;

      // Souverain = illimite
      if (profile?.role === 'souverain') {
        return { allowed: true, remaining: Infinity };
      }

      // Recuperer l'usage actuel du mois
      const currentMonth = new Date().toISOString().slice(0, 7); // YYYY-MM
      const { data: usage } = await supabase
        .from('api_usage')
        .select('tokens_used')
        .eq('user_id', userId)
        .eq('month', currentMonth)
        .single();

      const tokensUsed = usage?.tokens_used || 0;
      const maxCredits = PLAN_CREDITS[profile?.role] || PLAN_CREDITS.citoyen;
      const remaining = maxCredits - tokensUsed;

      if (remaining < estimatedTokens) {
        return {
          allowed: false,
          remaining,
          message: `Credits insuffisants. ${remaining} tokens restants ce mois.`
        };
      }

      return { allowed: true, remaining };
    } catch (err) {
      console.error('Erreur verification credits:', err);
      // En cas d'erreur, autoriser par defaut (fail-open)
      return { allowed: true, remaining: PLAN_CREDITS.citoyen };
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // ENREGISTREMENT DE L'USAGE
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * Enregistre l'utilisation de tokens
   * @param {string} userId - ID de l'utilisateur
   * @param {Object} usage - Details de l'utilisation
   */
  async recordUsage(userId, { model, inputTokens, outputTokens, provider, cost }) {
    try {
      const currentMonth = new Date().toISOString().slice(0, 7);
      const totalTokens = inputTokens + outputTokens;

      // Upsert l'usage mensuel
      const { error: monthError } = await supabase.rpc('record_api_usage', {
        p_user_id: userId,
        p_month: currentMonth,
        p_tokens: totalTokens,
        p_cost: cost || 0
      });

      if (monthError) console.warn('Erreur enregistrement usage mensuel:', monthError);

      // Enregistrer le detail de la requete
      const { error: detailError } = await supabase
        .from('api_requests')
        .insert({
          user_id: userId,
          provider,
          model,
          input_tokens: inputTokens,
          output_tokens: outputTokens,
          total_tokens: totalTokens,
          cost_cents: cost || 0
        });

      if (detailError) console.warn('Erreur enregistrement detail:', detailError);

    } catch (err) {
      console.error('Erreur recording usage:', err);
    }
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // SELECTION DU MODELE OPTIMAL
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * Selectionne le meilleur modele selon le contexte
   * @param {Object} options - Options de selection
   * @returns {Object} - Modele et provider selectionnes
   */
  selectOptimalModel({ task = 'general', maxCost = null, preferredModel = null }) {
    // Si un modele prefere est specifie et disponible
    if (preferredModel && this.isModelAvailable(preferredModel)) {
      return {
        provider: this.defaultProvider,
        model: preferredModel,
        modelId: API_PROVIDERS[this.defaultProvider].models[preferredModel]
      };
    }

    // Selection basee sur la tache
    const taskModels = {
      creative: 'claude-3-opus',      // Taches creatives complexes
      analysis: 'gpt-4o',             // Analyse de donnees
      coding: 'claude-3-sonnet',      // Code et technique
      general: 'claude-3-sonnet',     // Usage general
      fast: 'llama-3',                // Reponses rapides
      cheap: 'llama-3'                // Budget limite
    };

    const selectedModel = taskModels[task] || this.defaultModel;

    return {
      provider: this.defaultProvider,
      model: selectedModel,
      modelId: API_PROVIDERS[this.defaultProvider].models[selectedModel]
    };
  }

  /**
   * Verifie si un modele est disponible
   */
  isModelAvailable(model) {
    return Object.values(API_PROVIDERS).some(
      provider => Object.keys(provider.models).includes(model)
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // APPEL API UNIFIE
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * Effectue un appel API via le routeur
   * @param {Object} options - Options de l'appel
   * @returns {Promise<Object>} - Reponse de l'API
   */
  async call({
    userId,
    messages,
    model = null,
    task = 'general',
    maxTokens = 2048,
    temperature = 0.7,
    stream = false
  }) {
    // Verification des credits
    const creditCheck = await this.checkCredits(userId, maxTokens);
    if (!creditCheck.allowed) {
      return {
        success: false,
        error: creditCheck.message,
        remaining: creditCheck.remaining
      };
    }

    // Selection du modele
    const { provider, model: selectedModel, modelId } = this.selectOptimalModel({
      task,
      preferredModel: model
    });

    try {
      // Obtenir la cle API depuis les variables d'environnement
      const apiKey = this.getAPIKey(provider);
      if (!apiKey) {
        throw new Error(`Cle API non configuree pour ${provider}`);
      }

      // Construire la requete selon le provider
      const response = await this.makeRequest({
        provider,
        modelId,
        messages,
        maxTokens,
        temperature,
        apiKey,
        stream
      });

      // Calculer le cout
      const costs = API_PROVIDERS[provider]?.costs?.[selectedModel] || { input: 0.1, output: 0.3 };
      const inputTokens = response.usage?.prompt_tokens || 0;
      const outputTokens = response.usage?.completion_tokens || 0;
      const cost = ((inputTokens * costs.input) + (outputTokens * costs.output)) / 1000;

      // Enregistrer l'usage
      await this.recordUsage(userId, {
        model: selectedModel,
        provider,
        inputTokens,
        outputTokens,
        cost: Math.round(cost * 100) // En centimes
      });

      return {
        success: true,
        content: response.choices?.[0]?.message?.content || '',
        model: selectedModel,
        provider,
        usage: {
          inputTokens,
          outputTokens,
          totalTokens: inputTokens + outputTokens,
          cost: cost.toFixed(4)
        },
        remaining: creditCheck.remaining - (inputTokens + outputTokens)
      };

    } catch (err) {
      console.error('Erreur appel API:', err);
      return {
        success: false,
        error: err.message || 'Erreur lors de l\'appel API',
        remaining: creditCheck.remaining
      };
    }
  }

  /**
   * Obtient la cle API pour un provider
   */
  getAPIKey(provider) {
    const keyMap = {
      openrouter: process.env.REACT_APP_OPENROUTER_API_KEY,
      anthropic: process.env.REACT_APP_ANTHROPIC_API_KEY,
      openai: process.env.REACT_APP_OPENAI_API_KEY
    };
    return keyMap[provider];
  }

  /**
   * Effectue la requete HTTP selon le provider
   */
  async makeRequest({ provider, modelId, messages, maxTokens, temperature, apiKey, stream }) {
    const providerConfig = API_PROVIDERS[provider];

    // Format OpenRouter / OpenAI compatible
    if (provider === 'openrouter' || provider === 'openai') {
      const response = await fetch(`${providerConfig.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
          ...(provider === 'openrouter' && {
            'HTTP-Referer': window.location.origin,
            'X-Title': 'AT.OM Arche'
          })
        },
        body: JSON.stringify({
          model: modelId,
          messages,
          max_tokens: maxTokens,
          temperature,
          stream
        })
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error?.message || `Erreur API: ${response.status}`);
      }

      return response.json();
    }

    // Format Anthropic
    if (provider === 'anthropic') {
      const response = await fetch(`${providerConfig.baseUrl}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: modelId,
          messages: messages.map(m => ({
            role: m.role === 'assistant' ? 'assistant' : 'user',
            content: m.content
          })),
          max_tokens: maxTokens,
          temperature
        })
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error?.message || `Erreur API: ${response.status}`);
      }

      const data = await response.json();

      // Convertir au format OpenAI pour uniformite
      return {
        choices: [{
          message: {
            content: data.content?.[0]?.text || ''
          }
        }],
        usage: {
          prompt_tokens: data.usage?.input_tokens || 0,
          completion_tokens: data.usage?.output_tokens || 0
        }
      };
    }

    throw new Error(`Provider non supporte: ${provider}`);
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // HELPERS
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * Obtient les statistiques d'utilisation de l'utilisateur
   */
  async getUserStats(userId) {
    try {
      const currentMonth = new Date().toISOString().slice(0, 7);

      const { data: usage } = await supabase
        .from('api_usage')
        .select('tokens_used, cost_cents')
        .eq('user_id', userId)
        .eq('month', currentMonth)
        .single();

      const { data: profile } = await supabase
        .from('profiles')
        .select('role')
        .eq('id', userId)
        .single();

      const maxCredits = PLAN_CREDITS[profile?.role] || PLAN_CREDITS.citoyen;

      return {
        tokensUsed: usage?.tokens_used || 0,
        costCents: usage?.cost_cents || 0,
        tokensRemaining: maxCredits === Infinity ? 'Illimite' : maxCredits - (usage?.tokens_used || 0),
        maxTokens: maxCredits === Infinity ? 'Illimite' : maxCredits,
        percentUsed: maxCredits === Infinity ? 0 : Math.round(((usage?.tokens_used || 0) / maxCredits) * 100)
      };
    } catch (err) {
      console.error('Erreur stats utilisateur:', err);
      return null;
    }
  }

  /**
   * Liste les modeles disponibles
   */
  getAvailableModels() {
    const models = [];
    Object.entries(API_PROVIDERS).forEach(([providerId, provider]) => {
      Object.entries(provider.models).forEach(([modelKey, modelId]) => {
        models.push({
          key: modelKey,
          id: modelId,
          provider: providerId,
          providerName: provider.name,
          cost: provider.costs?.[modelKey]
        });
      });
    });
    return models;
  }
}

// Export singleton
export const apiRouter = new APIRouter();
export default apiRouter;
