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

// Configuration Supabase (à remplacer par tes vraies clés)
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'https://your-project.supabase.co';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'your-anon-key';

// Client Supabase
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
});

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES DE RÔLES - HIÉRARCHIE DE CIVILISATION
// ═══════════════════════════════════════════════════════════════════════════════

export const ROLES = {
  SOUVERAIN: 'souverain',        // Toi - Accès total L0-L9
  COLLABORATEUR: 'collaborateur', // Scientifiques - Accès recherche
  CITOYEN: 'citoyen'              // Utilisateurs locaux - Accès forum/besoins
};

export const ROLE_PERMISSIONS = {
  [ROLES.SOUVERAIN]: {
    levels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], // L0-L9 complet
    canManageFrequencies: true,
    canManageAgents: true,
    canManageUsers: true,
    canAccessAnalytics: true,
    canModerateForums: true,
    canEditLibrary: true
  },
  [ROLES.COLLABORATEUR]: {
    levels: [0, 1, 2, 3, 4, 5, 6], // L0-L6 (Analyse + Traitement)
    canManageFrequencies: false,
    canManageAgents: false,
    canManageUsers: false,
    canAccessAnalytics: true,
    canModerateForums: true,
    canEditLibrary: true
  },
  [ROLES.CITOYEN]: {
    levels: [0, 1, 2, 3], // L0-L3 (Analyse basique)
    canManageFrequencies: false,
    canManageAgents: false,
    canManageUsers: false,
    canAccessAnalytics: false,
    canModerateForums: false,
    canEditLibrary: false
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
