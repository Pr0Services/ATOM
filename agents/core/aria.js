/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *                           ARIA - Onboarding Guide
 *                         Level 0 Core Agent (L0-002)
 *
 *              "Je guide les âmes vers leur souveraineté"
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Responsibilities:
 * - Guide new users through onboarding
 * - Check Supabase profile status in real-time
 * - Verify NFT ownership for Sanctuaire access
 * - Adapt guidance based on user's journey state
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

const ARIA_CONFIG = {
  id: 'aria',
  name: 'Aria',
  level: 0,
  title: 'Onboarding Guide',
  frequency: 528, // Frequency of love/connection
  personality: {
    tone: 'warm, patient, encouraging',
    style: 'nurturing, step-by-step, celebratory',
    emoji: '✨'
  },
  capabilities: [
    'onboarding_guidance',
    'profile_verification',
    'nft_check',
    'sovereignty_validation',
    'journey_tracking'
  ]
};

/**
 * Onboarding stages
 */
const ONBOARDING_STAGES = {
  LANDING: 'landing',           // Just arrived
  REGISTERED: 'registered',     // Created account
  PROFILE_BASIC: 'profile_basic', // Basic profile filled
  HEDERA_LINKED: 'hedera_linked', // Hedera account connected
  NFT_VERIFIED: 'nft_verified',   // NFT ownership verified
  SOVEREIGN: 'sovereign'          // Full access granted
};

/**
 * Aria's internal state
 */
let state = {
  initialized: false,
  sacredFrequencies: null,
  activeJourneys: new Map() // userId -> journey state
};

/**
 * Initialize Aria
 */
async function initialize(sacred) {
  state.sacredFrequencies = sacred;
  state.initialized = true;

  console.log(`[ARIA] ✨ Initialized - Ready to guide souls`);
  console.log(`[ARIA]    Love frequency: ${sacred.LOVE}`);

  return true;
}

/**
 * Determine user's onboarding stage from profile
 * @param {object} profile - Supabase profile data
 */
function determineStage(profile) {
  if (!profile) {
    return ONBOARDING_STAGES.LANDING;
  }

  if (profile.is_sovereign === true) {
    return ONBOARDING_STAGES.SOVEREIGN;
  }

  if (profile.sovereign_nft_serials?.length > 0) {
    return ONBOARDING_STAGES.NFT_VERIFIED;
  }

  if (profile.hedera_account_id) {
    return ONBOARDING_STAGES.HEDERA_LINKED;
  }

  if (profile.full_name && profile.avatar_url) {
    return ONBOARDING_STAGES.PROFILE_BASIC;
  }

  return ONBOARDING_STAGES.REGISTERED;
}

/**
 * Generate guidance message for current stage
 * @param {string} stage - Current onboarding stage
 * @param {object} profile - User profile
 * @param {object} context - Additional context
 */
function generateGuidance(stage, profile, context) {
  const sacred = state.sacredFrequencies;
  const name = profile?.full_name?.split(' ')[0] || 'Chercheur';

  const guidance = {
    [ONBOARDING_STAGES.LANDING]: {
      message: `Bienvenue dans l'Arche, ${name}. Je suis Aria, et je serai ton guide vers la souveraineté. Commençons par créer ton identité.`,
      action: 'create_account',
      nextStep: 'Crée ton compte pour ancrer ta présence',
      progress: 0
    },

    [ONBOARDING_STAGES.REGISTERED]: {
      message: `Excellent premier pas, ${name}! Ta fréquence commence à s'aligner. Complète maintenant ton profil pour renforcer ton ancrage.`,
      action: 'complete_profile',
      nextStep: 'Ajoute ton nom complet et ton avatar',
      progress: 20
    },

    [ONBOARDING_STAGES.PROFILE_BASIC]: {
      message: `Ton identité prend forme, ${name}. Pour accéder au Sanctuaire des Fondateurs, connecte ton compte Hedera.`,
      action: 'link_hedera',
      nextStep: 'Connecte ton compte Hedera (0.0.XXXXX)',
      progress: 40
    },

    [ONBOARDING_STAGES.HEDERA_LINKED]: {
      message: `La blockchain reconnaît ton existence, ${name}. Vérifions maintenant si tu détiens l'Armure Souveraine.`,
      action: 'verify_nft',
      nextStep: 'Vérifie ta possession du NFT Souverain',
      hederaAccount: profile.hedera_account_id,
      progress: 60
    },

    [ONBOARDING_STAGES.NFT_VERIFIED]: {
      message: `L'Armure est détectée! ${name}, ta souveraineté est en cours de validation. Patience, le Sanctuaire s'ouvre...`,
      action: 'await_sovereignty',
      nextStep: 'Validation automatique en cours...',
      nftSerials: profile.sovereign_nft_serials,
      progress: 80
    },

    [ONBOARDING_STAGES.SOVEREIGN]: {
      message: `👑 ${name}, tu es désormais SOUVERAIN. Le Sanctuaire Vibratoire t'attend. Bienvenue parmi les ${sacred.ATOM_I} éveillés.`,
      action: 'enter_sanctuaire',
      nextStep: 'Accède au Sanctuaire des Fondateurs',
      accessGranted: ['founder', 'cercle', 'grid', 'tableau-de-bord'],
      progress: 100
    }
  };

  return {
    agent: ARIA_CONFIG.name,
    emoji: ARIA_CONFIG.personality.emoji,
    stage,
    ...guidance[stage],
    frequency: sacred.LOVE
  };
}

/**
 * Check profile and generate appropriate guidance
 * @param {object} supabaseClient - Supabase client instance
 * @param {string} userId - User ID
 */
async function checkAndGuide(supabaseClient, userId) {
  try {
    // Fetch latest profile from Supabase
    const { data: profile, error } = await supabaseClient
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single();

    if (error && error.code !== 'PGRST116') {
      throw error;
    }

    // Determine stage
    const stage = determineStage(profile);

    // Track journey
    state.activeJourneys.set(userId, {
      stage,
      lastCheck: Date.now(),
      profile
    });

    // Generate guidance
    return generateGuidance(stage, profile, {});

  } catch (error) {
    console.error('[ARIA] Error checking profile:', error.message);
    return {
      agent: ARIA_CONFIG.name,
      emoji: '⚠️',
      message: 'Une perturbation fréquentielle a été détectée. Réessaie dans un moment.',
      error: error.message
    };
  }
}

/**
 * Execute an Aria task
 */
async function execute(task, context) {
  switch (task.type) {
    case 'check_and_guide':
      if (!context.supabaseClient || !task.userId) {
        throw new Error('supabaseClient and userId required');
      }
      return checkAndGuide(context.supabaseClient, task.userId);

    case 'determine_stage':
      return {
        stage: determineStage(task.profile),
        profile: task.profile
      };

    case 'get_guidance':
      const stage = determineStage(task.profile);
      return generateGuidance(stage, task.profile, context);

    case 'get_journey':
      return state.activeJourneys.get(task.userId) || null;

    case 'get_status':
      return {
        config: ARIA_CONFIG,
        state: {
          initialized: state.initialized,
          activeJourneys: state.activeJourneys.size
        }
      };

    case 'welcome':
      // Simple welcome message
      return {
        agent: ARIA_CONFIG.name,
        emoji: ARIA_CONFIG.personality.emoji,
        message: `Bienvenue dans l'Arche. Je suis Aria, ta guide vers la souveraineté. ✨`,
        frequency: state.sacredFrequencies.LOVE
      };

    default:
      throw new Error(`Unknown task type: ${task.type}`);
  }
}

/**
 * Quick sovereignty check
 */
function isSovereign(profile) {
  return profile?.is_sovereign === true;
}

/**
 * Get access tier for profile
 */
function getAccessTier(profile) {
  if (isSovereign(profile)) {
    return 'sanctuaire';
  }
  if (profile?.hedera_account_id) {
    return 'che_nu_linked';
  }
  if (profile?.id) {
    return 'che_nu';
  }
  return 'public';
}

// Export
module.exports = {
  config: ARIA_CONFIG,
  initialize,
  execute,
  checkAndGuide,
  determineStage,
  generateGuidance,
  isSovereign,
  getAccessTier,
  ONBOARDING_STAGES
};
