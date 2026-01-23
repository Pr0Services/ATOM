/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *                    CONTEXTE D'AUTHENTIFICATION
 *                    Gestion des Sessions & Rôles
 *                         CHE·NU V76 - AT·OM
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { supabase, ROLES, ROLE_PERMISSIONS, signIn, signUp, signOut, getCurrentUser } from '../lib/supabase';

// Contexte d'authentification
const AuthContext = createContext(null);

// Hook pour utiliser le contexte
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Provider d'authentification
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialisation - Vérifier la session existante
  useEffect(() => {
    const initAuth = async () => {
      try {
        // Récupérer la session existante
        const { data: { session: currentSession } } = await supabase.auth.getSession();

        if (currentSession) {
          setSession(currentSession);
          setUser(currentSession.user);
        }
      } catch (err) {
        console.error('[AUTH] Erreur initialisation:', err);
      } finally {
        setLoading(false);
      }
    };

    initAuth();

    // Écouter les changements d'authentification
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, currentSession) => {
        console.log('[AUTH] Événement:', event);
        setSession(currentSession);
        setUser(currentSession?.user || null);
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  // Connexion
  const login = useCallback(async (email, password) => {
    setLoading(true);
    setError(null);

    const result = await signIn(email, password);

    if (result.success) {
      setUser(result.user);
      setSession(result.session);
    } else {
      setError(result.error);
    }

    setLoading(false);
    return result;
  }, []);

  // Inscription
  const register = useCallback(async (email, password, displayName) => {
    setLoading(true);
    setError(null);

    const result = await signUp(email, password, displayName);

    if (result.success) {
      setUser(result.user);
    } else {
      setError(result.error);
    }

    setLoading(false);
    return result;
  }, []);

  // Déconnexion
  const logout = useCallback(async () => {
    setLoading(true);
    const result = await signOut();

    if (result.success) {
      setUser(null);
      setSession(null);
    }

    setLoading(false);
    return result;
  }, []);

  // Récupérer le rôle de l'utilisateur
  const getRole = useCallback(() => {
    return user?.user_metadata?.role || ROLES.CITOYEN;
  }, [user]);

  // Vérifier une permission
  const checkPermission = useCallback((permission) => {
    const role = getRole();
    return ROLE_PERMISSIONS[role]?.[permission] || false;
  }, [getRole]);

  // Vérifier l'accès à un niveau Oracle
  const checkLevelAccess = useCallback((level) => {
    const role = getRole();
    return ROLE_PERMISSIONS[role]?.levels?.includes(level) || false;
  }, [getRole]);

  // Est-ce le Souverain ?
  const isSovereign = useCallback(() => {
    return getRole() === ROLES.SOUVERAIN;
  }, [getRole]);

  // Est-ce un collaborateur ?
  const isCollaborator = useCallback(() => {
    return getRole() === ROLES.COLLABORATEUR;
  }, [getRole]);

  // Valeur du contexte
  const value = {
    // État
    user,
    session,
    loading,
    error,
    isAuthenticated: !!user,

    // Actions
    login,
    register,
    logout,

    // Permissions
    getRole,
    checkPermission,
    checkLevelAccess,
    isSovereign,
    isCollaborator,

    // Constantes
    ROLES,
    ROLE_PERMISSIONS
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
