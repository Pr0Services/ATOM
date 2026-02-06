/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *                    SUPABASE - CONNEXION SOUVERAINE
 *                  Authentification & Base de Données
 *                         CHE·NU V76 - AT·OM
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { createClient } from '@supabase/supabase-js';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION SÉCURISÉE - AUCUN FALLBACK POUR LES CLÉS SENSIBLES
// ═══════════════════════════════════════════════════════════════════════════════

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

// Validation stricte des variables d'environnement
const validateConfig = () => {
  const missing = [];
  if (!supabaseUrl) missing.push('REACT_APP_SUPABASE_URL');
  if (!supabaseAnonKey) missing.push('REACT_APP_SUPABASE_ANON_KEY');

  if (missing.length > 0) {
    console.error(`[SECURITY] Variables d'environnement manquantes: ${missing.join(', ')}`);
    console.error('[SECURITY] Configurez ces variables dans le Setup Wizard (/admin) ou dans votre fichier .env');
    // En développement, on avertit mais on ne bloque pas complètement
    if (process.env.NODE_ENV === 'production') {
      throw new Error(`Configuration Supabase incomplète. Variables manquantes: ${missing.join(', ')}`);
    }
  }
  return missing.length === 0;
};

const isConfigured = validateConfig();

// Client Supabase - créé seulement si configuré, sinon client mock pour dev
export const supabase = isConfigured
  ? createClient(supabaseUrl, supabaseAnonKey, {
      auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true
      }
    })
  : createMockClient();

// Client mock pour développement sans Supabase configuré
function createMockClient() {
  console.warn('[DEV] Supabase non configuré - utilisation du client mock');
  const mockResponse = { data: null, error: { message: 'Supabase non configuré' } };
  const mockAuth = {
    signUp: async () => mockResponse,
    signInWithPassword: async () => mockResponse,
    signOut: async () => ({ error: null }),
    getUser: async () => ({ data: { user: null }, error: null }),
    getSession: async () => ({ data: { session: null }, error: null }),
    onAuthStateChange: () => ({ data: { subscription: { unsubscribe: () => {} } } })
  };
  return {
    auth: mockAuth,
    from: () => ({
      select: () => ({ eq: () => ({ order: () => ({ limit: () => mockResponse }) }) }),
      insert: () => ({ select: () => mockResponse }),
      update: () => ({ eq: () => mockResponse }),
      delete: () => ({ eq: () => mockResponse })
    }),
    rpc: async () => mockResponse
  };
}

// Export du status de configuration
export const isSupabaseConfigured = isConfigured;

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES DE RÔLES - HIÉRARCHIE DE CIVILISATION
// ═══════════════════════════════════════════════════════════════════════════════

export const ROLES = {
  SOUVERAIN: 'souverain',        // Toi - Accès total L0-L9
  COLLABORATEUR: 'collaborateur', // Scientifiques - Accès recherche
  CITOYEN: 'citoyen'              // Utilisateurs locaux - Accès forum/besoins
};

// ═══════════════════════════════════════════════════════════════════════════════
// SYSTÈME DES 3 STRATES D'ACCÈS
// ═══════════════════════════════════════════════════════════════════════════════

export const ACCESS_TIERS = {
  PUBLIC: 'public',           // Landing page, info générale
  CHE_NU: 'che_nu',          // Société actuelle, forum, besoins
  SANCTUAIRE: 'sanctuaire'   // Espace vibratoire (is_sovereign = true)
};

export const TIER_ROUTES = {
  [ACCESS_TIERS.PUBLIC]: [
    '/entree',
    '/accreditation',
    '/'  // Nexus accessible mais limité
  ],
  [ACCESS_TIERS.CHE_NU]: [
    '/besoins',
    '/gratitude',
    '/annales',
    '/lexique',
    '/flux',
    '/forge',
    '/agent'
  ],
  [ACCESS_TIERS.SANCTUAIRE]: [
    '/founder',
    '/cercle',
    '/grid',
    '/tableau-de-bord',
    '/invitation',
    '/admin'
  ]
};

// ═══════════════════════════════════════════════════════════════════════════════
// FRÉQUENCES SACRÉES - CONSTANTES AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

export const SACRED_FREQUENCIES = {
  ATOM_M: 44.4,           // Manifestation
  ATOM_P: 161.8,          // Phi - Ratio d'or
  ATOM_I: 369,            // Intégration Tesla
  ATOM_PO: 1728,          // Année de Platon
  HEARTBEAT: 444,         // Fréquence cardiaque
  SOURCE: 999,            // Fréquence source
  LOVE: 528,              // Fréquence de l'amour
  PHI: 1.6180339887498949 // Nombre d'or
};

export const ROLE_PERMISSIONS = {
  [ROLES.SOUVERAIN]: {
    levels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], // L0-L9 complet
    tier: ACCESS_TIERS.SANCTUAIRE,
    canManageFrequencies: true,
    canManageAgents: true,
    canManageUsers: true,
    canAccessAnalytics: true,
    canModerateForums: true,
    canEditLibrary: true,
    canAccessSanctuaire: true
  },
  [ROLES.COLLABORATEUR]: {
    levels: [0, 1, 2, 3, 4, 5, 6], // L0-L6 (Analyse + Traitement)
    tier: ACCESS_TIERS.CHE_NU,
    canManageFrequencies: false,
    canManageAgents: false,
    canManageUsers: false,
    canAccessAnalytics: true,
    canModerateForums: true,
    canEditLibrary: true,
    canAccessSanctuaire: false
  },
  [ROLES.CITOYEN]: {
    levels: [0, 1, 2, 3], // L0-L3 (Analyse basique)
    tier: ACCESS_TIERS.CHE_NU,
    canManageFrequencies: false,
    canManageAgents: false,
    canManageUsers: false,
    canAccessAnalytics: false,
    canModerateForums: false,
    canEditLibrary: false,
    canAccessSanctuaire: false
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS D'AUTHENTIFICATION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Inscription d'un nouvel utilisateur
 */
export async function signUp(email, password, displayName) {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          display_name: displayName,
          role: ROLES.CITOYEN, // Par défaut = citoyen
          frequency: 444,
          joined_at: new Date().toISOString()
        }
      }
    });

    if (error) throw error;

    console.log('[AUTH] Inscription réussie:', data.user?.email);
    return { success: true, user: data.user };
  } catch (error) {
    console.error('[AUTH] Erreur inscription:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Connexion utilisateur
 */
export async function signIn(email, password) {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (error) throw error;

    console.log('[AUTH] Connexion réussie:', data.user?.email);
    return { success: true, user: data.user, session: data.session };
  } catch (error) {
    console.error('[AUTH] Erreur connexion:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Déconnexion
 */
/**
 * Connexion via OAuth (Facebook, Google, Apple)
 * @param {'facebook'|'google'|'apple'} provider
 */
export async function signInWithSocial(provider) {
  try {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${window.location.origin}/profil`,
        scopes: provider === 'facebook'
          ? 'public_profile,email'
          : provider === 'google'
            ? 'profile email'
            : 'name email',
      }
    });

    if (error) throw error;

    console.log(`[AUTH] Redirection OAuth ${provider}`);
    return { success: true, data };
  } catch (error) {
    console.error(`[AUTH] Erreur OAuth ${provider}:`, error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Lier un compte social additionnel (sans remplacer le login existant)
 * @param {'facebook'|'google'|'apple'} provider
 */
export async function linkSocialAccount(provider) {
  try {
    const { data, error } = await supabase.auth.linkIdentity({
      provider,
      options: {
        redirectTo: `${window.location.origin}/profil`,
      }
    });

    if (error) throw error;

    console.log(`[AUTH] Liaison compte ${provider}`);
    return { success: true, data };
  } catch (error) {
    console.error(`[AUTH] Erreur liaison ${provider}:`, error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Mettre à jour le profil utilisateur dans Supabase
 */
export async function updateProfile(userId, profileData) {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .upsert({
        id: userId,
        ...profileData,
        updated_at: new Date().toISOString()
      })
      .select();

    if (error) throw error;

    console.log('[PROFILE] Profil mis à jour');
    return { success: true, data: data[0] };
  } catch (error) {
    console.error('[PROFILE] Erreur mise à jour:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Upload d'avatar dans Supabase Storage
 */
export async function uploadAvatar(userId, file) {
  try {
    const fileExt = file.name.split('.').pop();
    const filePath = `avatars/${userId}.${fileExt}`;

    const { error: uploadError } = await supabase.storage
      .from('avatars')
      .upload(filePath, file, { upsert: true });

    if (uploadError) throw uploadError;

    const { data: { publicUrl } } = supabase.storage
      .from('avatars')
      .getPublicUrl(filePath);

    // Mettre à jour le profil avec l'URL
    await updateProfile(userId, { avatar_url: publicUrl });

    return { success: true, url: publicUrl };
  } catch (error) {
    console.error('[AVATAR] Erreur upload:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Déconnexion
 */
export async function signOut() {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;

    console.log('[AUTH] Déconnexion réussie');
    return { success: true };
  } catch (error) {
    console.error('[AUTH] Erreur déconnexion:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Récupérer l'utilisateur courant
 */
export async function getCurrentUser() {
  try {
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) throw error;
    return user;
  } catch (error) {
    console.error('[AUTH] Erreur récupération utilisateur:', error.message);
    return null;
  }
}

/**
 * Récupérer la session courante
 */
export async function getSession() {
  try {
    const { data: { session }, error } = await supabase.auth.getSession();
    if (error) throw error;
    return session;
  } catch (error) {
    console.error('[AUTH] Erreur récupération session:', error.message);
    return null;
  }
}

/**
 * Vérifier les permissions d'un utilisateur
 */
export function hasPermission(user, permission) {
  if (!user) return false;
  const role = user.user_metadata?.role || ROLES.CITOYEN;
  const permissions = ROLE_PERMISSIONS[role];
  return permissions?.[permission] || false;
}

/**
 * Vérifier si l'utilisateur a accès à un niveau Oracle
 */
export function hasLevelAccess(user, level) {
  if (!user) return false;
  const role = user.user_metadata?.role || ROLES.CITOYEN;
  const permissions = ROLE_PERMISSIONS[role];
  return permissions?.levels?.includes(level) || false;
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE SOUVERAINETÉ - VÉRIFICATION NFT & ACCÈS SANCTUAIRE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Vérifier si l'utilisateur est Souverain (possède le NFT)
 * @param {string} userId - ID de l'utilisateur
 * @returns {Promise<{isSovereign: boolean, profile: object}>}
 */
export async function checkSovereignty(userId) {
  try {
    const { data: profile, error } = await supabase
      .from('profiles')
      .select('id, full_name, is_sovereign, hedera_account_id, sovereign_nft_serials, role, frequency')
      .eq('id', userId)
      .single();

    if (error) throw error;

    return {
      isSovereign: profile?.is_sovereign === true,
      profile: profile,
      accessTier: profile?.is_sovereign ? ACCESS_TIERS.SANCTUAIRE : ACCESS_TIERS.CHE_NU
    };
  } catch (error) {
    console.error('[SOVEREIGNTY] Erreur vérification:', error.message);
    return { isSovereign: false, profile: null, accessTier: ACCESS_TIERS.PUBLIC };
  }
}

/**
 * Vérifier l'accès à une route selon le tier
 * @param {object} user - Utilisateur courant
 * @param {string} route - Route demandée
 * @returns {Promise<{allowed: boolean, reason: string}>}
 */
export async function checkRouteAccess(user, route) {
  // Routes publiques toujours accessibles
  if (TIER_ROUTES[ACCESS_TIERS.PUBLIC].some(r => route.startsWith(r))) {
    return { allowed: true, reason: 'Route publique' };
  }

  // Utilisateur non connecté
  if (!user) {
    return { allowed: false, reason: 'Connexion requise', redirect: '/entree' };
  }

  // Vérifier le statut de souveraineté
  const { isSovereign, accessTier } = await checkSovereignty(user.id);

  // Routes du Sanctuaire
  if (TIER_ROUTES[ACCESS_TIERS.SANCTUAIRE].some(r => route.startsWith(r))) {
    if (isSovereign) {
      return { allowed: true, reason: 'Accès Sanctuaire confirmé' };
    }
    return {
      allowed: false,
      reason: 'Accès réservé aux Souverains (détenteurs du NFT)',
      redirect: '/accreditation'
    };
  }

  // Routes CHE-NU (société actuelle)
  if (TIER_ROUTES[ACCESS_TIERS.CHE_NU].some(r => route.startsWith(r))) {
    return { allowed: true, reason: 'Accès CHE-NU confirmé' };
  }

  // Par défaut, autoriser
  return { allowed: true, reason: 'Route non restreinte' };
}

/**
 * Récupérer le profil complet avec statut de souveraineté
 * @param {string} userId - ID de l'utilisateur
 */
export async function getFullProfile(userId) {
  try {
    const { data: profile, error } = await supabase
      .from('profiles')
      .select(`
        id,
        full_name,
        avatar_url,
        role,
        frequency,
        is_sovereign,
        hedera_account_id,
        sovereign_nft_serials,
        sovereign_verified_at,
        youtube_channel_url,
        facebook_url,
        is_active_creator,
        origin_context,
        migration_status,
        created_at,
        updated_at
      `)
      .eq('id', userId)
      .single();

    if (error) throw error;

    // Déterminer le tier d'accès
    const accessTier = profile?.is_sovereign
      ? ACCESS_TIERS.SANCTUAIRE
      : ACCESS_TIERS.CHE_NU;

    return {
      success: true,
      profile: {
        ...profile,
        accessTier,
        permissions: ROLE_PERMISSIONS[profile?.role || ROLES.CITOYEN]
      }
    };
  } catch (error) {
    console.error('[PROFILE] Erreur récupération:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Mettre à jour le compte Hedera d'un utilisateur
 * @param {string} userId - ID de l'utilisateur
 * @param {string} hederaAccountId - ID du compte Hedera (0.0.XXXXX)
 */
export async function linkHederaAccount(userId, hederaAccountId) {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .update({
        hedera_account_id: hederaAccountId,
        updated_at: new Date().toISOString()
      })
      .eq('id', userId)
      .select();

    if (error) throw error;

    console.log('[HEDERA] Compte lié:', hederaAccountId);
    return { success: true, data };
  } catch (error) {
    console.error('[HEDERA] Erreur liaison:', error.message);
    return { success: false, error: error.message };
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS BASE DE DONNÉES - PERCEPTIONS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Sauvegarder une perception dans la base cloud
 */
export async function savePerception(perception) {
  try {
    const user = await getCurrentUser();

    const { data, error } = await supabase
      .from('perceptions')
      .insert({
        user_id: user?.id || null,
        text: perception.text,
        frequency: perception.frequency || 999,
        heartbeat: perception.heartbeat || 444,
        created_at: new Date().toISOString()
      })
      .select();

    if (error) throw error;
    return { success: true, data };
  } catch (error) {
    console.error('[DB] Erreur sauvegarde perception:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Récupérer les perceptions d'un utilisateur
 */
export async function getPerceptions(userId, limit = 100) {
  try {
    const { data, error } = await supabase
      .from('perceptions')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) throw error;
    return { success: true, data };
  } catch (error) {
    console.error('[DB] Erreur récupération perceptions:', error.message);
    return { success: false, error: error.message };
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS BASE DE DONNÉES - BESOINS LOCAUX (Moteur de Civilisation)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Soumettre un besoin local
 */
export async function submitNeed(need) {
  try {
    const user = await getCurrentUser();

    const { data, error } = await supabase
      .from('local_needs')
      .insert({
        user_id: user?.id,
        title: need.title,
        description: need.description,
        category: need.category, // santé, éducation, environnement, économie...
        location: need.location || 'Québec',
        priority: need.priority || 'medium',
        votes: 0,
        status: 'pending',
        created_at: new Date().toISOString()
      })
      .select();

    if (error) throw error;
    return { success: true, data };
  } catch (error) {
    console.error('[DB] Erreur soumission besoin:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Voter pour un besoin
 */
export async function voteForNeed(needId) {
  try {
    const { data, error } = await supabase.rpc('increment_votes', {
      need_id: needId
    });

    if (error) throw error;
    return { success: true, data };
  } catch (error) {
    console.error('[DB] Erreur vote:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Récupérer les besoins locaux
 */
export async function getLocalNeeds(filters = {}) {
  try {
    let query = supabase
      .from('local_needs')
      .select('*')
      .order('votes', { ascending: false });

    if (filters.category) {
      query = query.eq('category', filters.category);
    }
    if (filters.location) {
      query = query.eq('location', filters.location);
    }

    const { data, error } = await query.limit(50);

    if (error) throw error;
    return { success: true, data };
  } catch (error) {
    console.error('[DB] Erreur récupération besoins:', error.message);
    return { success: false, error: error.message };
  }
}

export default supabase;
