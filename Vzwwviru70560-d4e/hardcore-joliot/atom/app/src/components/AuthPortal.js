/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *      ██████╗  ██████╗ ██████╗ ████████╗ █████╗ ██╗██╗
 *      ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗██║██║
 *      ██████╔╝██║   ██║██████╔╝   ██║   ███████║██║██║
 *      ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══██║██║██║
 *      ██║     ╚██████╔╝██║  ██║   ██║   ██║  ██║██║███████╗
 *      ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝
 *
 *                    PORTAIL D'AUTHENTIFICATION
 *                  Rejoindre l'Arche des Résonances
 *                         CHE·NU V76 - AT·OM
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: PORTAIL D'AUTHENTIFICATION
// ═══════════════════════════════════════════════════════════════════════════════

const AuthPortal = ({ onClose, initialMode = 'login' }) => {
  const [mode, setMode] = useState(initialMode); // 'login' | 'register'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [localError, setLocalError] = useState('');
  const [success, setSuccess] = useState('');

  const { login, register, loading, error } = useAuth();

  // Gestion de la connexion
  const handleLogin = useCallback(async (e) => {
    e.preventDefault();
    setLocalError('');

    if (!email || !password) {
      setLocalError('Veuillez remplir tous les champs');
      return;
    }

    const result = await login(email, password);
    if (result.success) {
      setSuccess('Connexion réussie ! Bienvenue dans l\'Arche.');
      setTimeout(() => onClose?.(), 1500);
    } else {
      setLocalError(result.error || 'Erreur de connexion');
    }
  }, [email, password, login, onClose]);

  // Gestion de l'inscription
  const handleRegister = useCallback(async (e) => {
    e.preventDefault();
    setLocalError('');

    if (!email || !password || !displayName) {
      setLocalError('Veuillez remplir tous les champs');
      return;
    }

    if (password.length < 6) {
      setLocalError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }

    const result = await register(email, password, displayName);
    if (result.success) {
      setSuccess('Inscription réussie ! Vérifiez votre email pour confirmer.');
      setTimeout(() => setMode('login'), 3000);
    } else {
      setLocalError(result.error || 'Erreur d\'inscription');
    }
  }, [email, password, displayName, register]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <div className="relative w-full max-w-md mx-4 bg-gradient-to-b from-gray-900 to-black border border-yellow-600/30 rounded-2xl p-8 shadow-2xl">

        {/* Bouton fermer */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-yellow-400 transition-colors"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* En-tête */}
        <div className="text-center mb-8">
          <div className="text-5xl mb-4">🔱</div>
          <h2 className="text-2xl font-bold text-yellow-400 tracking-wider">
            {mode === 'login' ? 'CONNEXION' : 'REJOINDRE L\'ARCHE'}
          </h2>
          <p className="text-gray-500 text-sm mt-2">
            {mode === 'login'
              ? 'Entrez dans l\'espace des résonances'
              : 'Créez votre compte citoyen'
            }
          </p>
        </div>

        {/* Messages */}
        {(localError || error) && (
          <div className="mb-4 p-3 bg-red-900/30 border border-red-500/50 rounded-lg text-red-400 text-sm text-center">
            {localError || error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-emerald-900/30 border border-emerald-500/50 rounded-lg text-emerald-400 text-sm text-center">
            {success}
          </div>
        )}

        {/* Formulaire */}
        <form onSubmit={mode === 'login' ? handleLogin : handleRegister}>

          {/* Nom d'affichage (inscription seulement) */}
          {mode === 'register' && (
            <div className="mb-4">
              <label className="block text-gray-400 text-sm mb-2">Nom d'Arche</label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Votre nom dans l'Arche"
                className="w-full px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none focus:border-yellow-500 transition-colors"
                disabled={loading}
              />
            </div>
          )}

          {/* Email */}
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="votre@email.com"
              className="w-full px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none focus:border-yellow-500 transition-colors"
              disabled={loading}
            />
          </div>

          {/* Mot de passe */}
          <div className="mb-6">
            <label className="block text-gray-400 text-sm mb-2">Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 bg-black/50 border border-yellow-900/50 rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none focus:border-yellow-500 transition-colors"
              disabled={loading}
            />
          </div>

          {/* Bouton principal */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-4 rounded-lg font-bold text-lg transition-all ${
              loading
                ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400 shadow-lg shadow-yellow-600/30'
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Chargement...
              </span>
            ) : mode === 'login' ? (
              'ENTRER DANS L\'ARCHE'
            ) : (
              'CRÉER MON COMPTE'
            )}
          </button>
        </form>

        {/* Toggle login/register */}
        <div className="mt-6 text-center">
          <p className="text-gray-500 text-sm">
            {mode === 'login' ? (
              <>
                Pas encore de compte ?{' '}
                <button
                  onClick={() => { setMode('register'); setLocalError(''); setSuccess(''); }}
                  className="text-yellow-400 hover:text-yellow-300 underline"
                >
                  Rejoindre l'Arche
                </button>
              </>
            ) : (
              <>
                Déjà un compte ?{' '}
                <button
                  onClick={() => { setMode('login'); setLocalError(''); setSuccess(''); }}
                  className="text-yellow-400 hover:text-yellow-300 underline"
                >
                  Se connecter
                </button>
              </>
            )}
          </p>
        </div>

        {/* Info rôles */}
        {mode === 'register' && (
          <div className="mt-6 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
            <p className="text-blue-400 text-xs text-center">
              Les nouveaux comptes reçoivent le rôle <strong>Citoyen</strong> (accès L0-L3).
              <br />
              Les rôles Collaborateur et Souverain sont attribués sur demande.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BOUTON DE PROFIL UTILISATEUR
// ═══════════════════════════════════════════════════════════════════════════════

export const UserProfileButton = ({ onClick }) => {
  const { user, isAuthenticated, logout, getRole } = useAuth();

  if (!isAuthenticated) {
    return (
      <button
        onClick={onClick}
        className="flex items-center gap-2 px-4 py-2 bg-yellow-600/20 border border-yellow-600/50 rounded-lg text-yellow-400 hover:bg-yellow-600/40 transition-all"
      >
        <span>🔱</span>
        <span className="text-sm">Rejoindre</span>
      </button>
    );
  }

  const role = getRole();
  const roleColors = {
    souverain: 'text-white bg-white/20 border-white',
    collaborateur: 'text-emerald-400 bg-emerald-900/30 border-emerald-500/50',
    citoyen: 'text-yellow-400 bg-yellow-900/30 border-yellow-500/50'
  };

  return (
    <div className="flex items-center gap-3">
      <div className={`px-3 py-1 rounded-lg border text-xs ${roleColors[role]}`}>
        {role.toUpperCase()}
      </div>
      <div className="text-right">
        <p className="text-yellow-400 text-sm font-medium">
          {user?.user_metadata?.display_name || user?.email?.split('@')[0]}
        </p>
        <button
          onClick={logout}
          className="text-gray-500 hover:text-red-400 text-xs transition-colors"
        >
          Déconnexion
        </button>
      </div>
    </div>
  );
};

export default AuthPortal;
