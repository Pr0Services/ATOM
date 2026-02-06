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

import React, { useState, useCallback, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import SocialAuthButtons from './SocialAuthButtons';

// ═══════════════════════════════════════════════════════════════════════════════
// VALIDATION SÉCURISÉE DES ENTRÉES
// ═══════════════════════════════════════════════════════════════════════════════

const VALIDATION_RULES = {
  email: {
    pattern: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
    maxLength: 254,
    message: 'Format d\'email invalide'
  },
  password: {
    minLength: 8,
    maxLength: 128,
    requireUppercase: true,
    requireLowercase: true,
    requireNumber: true,
    message: 'Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule et un chiffre'
  },
  displayName: {
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-ZÀ-ÿ0-9\s\-_'.]+$/,
    message: 'Le nom doit contenir entre 2 et 50 caractères alphanumériques'
  }
};

// Rate limiting côté client (protection basique)
const RATE_LIMIT = {
  maxAttempts: 5,
  windowMs: 60000, // 1 minute
  blockDuration: 300000 // 5 minutes
};

/**
 * Valide un email
 */
const validateEmail = (email) => {
  if (!email) return { valid: false, message: 'Email requis' };
  if (email.length > VALIDATION_RULES.email.maxLength) {
    return { valid: false, message: 'Email trop long' };
  }
  if (!VALIDATION_RULES.email.pattern.test(email)) {
    return { valid: false, message: VALIDATION_RULES.email.message };
  }
  return { valid: true };
};

/**
 * Valide un mot de passe
 */
const validatePassword = (password, isRegistration = false) => {
  if (!password) return { valid: false, message: 'Mot de passe requis' };
  if (password.length < VALIDATION_RULES.password.minLength) {
    return { valid: false, message: `Le mot de passe doit contenir au moins ${VALIDATION_RULES.password.minLength} caractères` };
  }
  if (password.length > VALIDATION_RULES.password.maxLength) {
    return { valid: false, message: 'Mot de passe trop long' };
  }

  // Règles strictes pour l'inscription
  if (isRegistration) {
    if (VALIDATION_RULES.password.requireUppercase && !/[A-Z]/.test(password)) {
      return { valid: false, message: 'Le mot de passe doit contenir au moins une majuscule' };
    }
    if (VALIDATION_RULES.password.requireLowercase && !/[a-z]/.test(password)) {
      return { valid: false, message: 'Le mot de passe doit contenir au moins une minuscule' };
    }
    if (VALIDATION_RULES.password.requireNumber && !/[0-9]/.test(password)) {
      return { valid: false, message: 'Le mot de passe doit contenir au moins un chiffre' };
    }
  }

  return { valid: true };
};

/**
 * Valide un nom d'affichage
 */
const validateDisplayName = (name) => {
  if (!name) return { valid: false, message: 'Nom requis' };
  const trimmed = name.trim();
  if (trimmed.length < VALIDATION_RULES.displayName.minLength) {
    return { valid: false, message: `Le nom doit contenir au moins ${VALIDATION_RULES.displayName.minLength} caractères` };
  }
  if (trimmed.length > VALIDATION_RULES.displayName.maxLength) {
    return { valid: false, message: `Le nom ne peut pas dépasser ${VALIDATION_RULES.displayName.maxLength} caractères` };
  }
  if (!VALIDATION_RULES.displayName.pattern.test(trimmed)) {
    return { valid: false, message: VALIDATION_RULES.displayName.message };
  }
  return { valid: true };
};

/**
 * Sanitize une chaîne pour éviter XSS
 */
const sanitizeInput = (input) => {
  if (!input) return '';
  return input
    .replace(/[<>]/g, '') // Supprime < et >
    .trim();
};

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
  const [fieldErrors, setFieldErrors] = useState({});

  // Rate limiting state
  const attemptCount = useRef(0);
  const firstAttemptTime = useRef(null);
  const blockedUntil = useRef(null);

  const { login, register, loading, error } = useAuth();

  // Vérifie si l'utilisateur est bloqué (rate limit)
  const checkRateLimit = useCallback(() => {
    const now = Date.now();

    // Si bloqué, vérifie si le blocage est terminé
    if (blockedUntil.current && now < blockedUntil.current) {
      const remainingSeconds = Math.ceil((blockedUntil.current - now) / 1000);
      return { blocked: true, message: `Trop de tentatives. Réessayez dans ${remainingSeconds}s` };
    }

    // Reset si le blocage est terminé
    if (blockedUntil.current && now >= blockedUntil.current) {
      blockedUntil.current = null;
      attemptCount.current = 0;
      firstAttemptTime.current = null;
    }

    // Reset si la fenêtre de temps est passée
    if (firstAttemptTime.current && (now - firstAttemptTime.current) > RATE_LIMIT.windowMs) {
      attemptCount.current = 0;
      firstAttemptTime.current = null;
    }

    return { blocked: false };
  }, []);

  // Enregistre une tentative
  const recordAttempt = useCallback(() => {
    const now = Date.now();

    if (!firstAttemptTime.current) {
      firstAttemptTime.current = now;
    }

    attemptCount.current++;

    if (attemptCount.current >= RATE_LIMIT.maxAttempts) {
      blockedUntil.current = now + RATE_LIMIT.blockDuration;
    }
  }, []);

  // Gestion de la connexion - SÉCURISÉE
  const handleLogin = useCallback(async (e) => {
    e.preventDefault();
    setLocalError('');
    setFieldErrors({});

    // Vérifier le rate limit
    const rateLimitCheck = checkRateLimit();
    if (rateLimitCheck.blocked) {
      setLocalError(rateLimitCheck.message);
      return;
    }

    // Sanitize les entrées
    const sanitizedEmail = sanitizeInput(email).toLowerCase();
    const sanitizedPassword = password; // Ne pas modifier le mot de passe

    // Valider l'email
    const emailValidation = validateEmail(sanitizedEmail);
    if (!emailValidation.valid) {
      setFieldErrors(prev => ({ ...prev, email: emailValidation.message }));
      return;
    }

    // Valider le mot de passe (règles basiques pour login)
    const passwordValidation = validatePassword(sanitizedPassword, false);
    if (!passwordValidation.valid) {
      setFieldErrors(prev => ({ ...prev, password: passwordValidation.message }));
      return;
    }

    // Enregistrer la tentative
    recordAttempt();

    const result = await login(sanitizedEmail, sanitizedPassword);
    if (result.success) {
      // Reset rate limit on success
      attemptCount.current = 0;
      setSuccess('Connexion réussie ! Bienvenue dans l\'Arche.');
      setTimeout(() => onClose?.(), 1500);
    } else {
      // Message générique pour ne pas révéler si l'email existe
      setLocalError('Email ou mot de passe incorrect');
    }
  }, [email, password, login, onClose, checkRateLimit, recordAttempt]);

  // Gestion de l'inscription - SÉCURISÉE
  const handleRegister = useCallback(async (e) => {
    e.preventDefault();
    setLocalError('');
    setFieldErrors({});

    // Vérifier le rate limit
    const rateLimitCheck = checkRateLimit();
    if (rateLimitCheck.blocked) {
      setLocalError(rateLimitCheck.message);
      return;
    }

    // Sanitize les entrées
    const sanitizedEmail = sanitizeInput(email).toLowerCase();
    const sanitizedDisplayName = sanitizeInput(displayName);
    const sanitizedPassword = password; // Ne pas modifier le mot de passe

    // Valider tous les champs
    const errors = {};

    const emailValidation = validateEmail(sanitizedEmail);
    if (!emailValidation.valid) errors.email = emailValidation.message;

    const passwordValidation = validatePassword(sanitizedPassword, true);
    if (!passwordValidation.valid) errors.password = passwordValidation.message;

    const nameValidation = validateDisplayName(sanitizedDisplayName);
    if (!nameValidation.valid) errors.displayName = nameValidation.message;

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    // Enregistrer la tentative
    recordAttempt();

    const result = await register(sanitizedEmail, sanitizedPassword, sanitizedDisplayName);
    if (result.success) {
      attemptCount.current = 0;
      setSuccess('Inscription réussie ! Vérifiez votre email pour confirmer.');
      setTimeout(() => setMode('login'), 3000);
    } else {
      // Message générique
      setLocalError('Impossible de créer le compte. Veuillez réessayer.');
    }
  }, [email, password, displayName, register, checkRateLimit, recordAttempt]);

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
                onChange={(e) => {
                  setDisplayName(e.target.value);
                  setFieldErrors(prev => ({ ...prev, displayName: null }));
                }}
                placeholder="Votre nom dans l'Arche"
                maxLength={50}
                autoComplete="name"
                className={`w-full px-4 py-3 bg-black/50 border rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none transition-colors ${
                  fieldErrors.displayName ? 'border-red-500' : 'border-yellow-900/50 focus:border-yellow-500'
                }`}
                disabled={loading}
              />
              {fieldErrors.displayName && (
                <p className="text-red-400 text-xs mt-1">{fieldErrors.displayName}</p>
              )}
            </div>
          )}

          {/* Email */}
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setFieldErrors(prev => ({ ...prev, email: null }));
              }}
              placeholder="votre@email.com"
              maxLength={254}
              autoComplete={mode === 'login' ? 'email' : 'off'}
              className={`w-full px-4 py-3 bg-black/50 border rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none transition-colors ${
                fieldErrors.email ? 'border-red-500' : 'border-yellow-900/50 focus:border-yellow-500'
              }`}
              disabled={loading}
            />
            {fieldErrors.email && (
              <p className="text-red-400 text-xs mt-1">{fieldErrors.email}</p>
            )}
          </div>

          {/* Mot de passe */}
          <div className="mb-6">
            <label className="block text-gray-400 text-sm mb-2">Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setFieldErrors(prev => ({ ...prev, password: null }));
              }}
              placeholder="••••••••"
              maxLength={128}
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
              className={`w-full px-4 py-3 bg-black/50 border rounded-lg text-yellow-100 placeholder-gray-600 focus:outline-none transition-colors ${
                fieldErrors.password ? 'border-red-500' : 'border-yellow-900/50 focus:border-yellow-500'
              }`}
              disabled={loading}
            />
            {fieldErrors.password && (
              <p className="text-red-400 text-xs mt-1">{fieldErrors.password}</p>
            )}
            {mode === 'register' && !fieldErrors.password && (
              <p className="text-gray-500 text-xs mt-1">Min. 8 caractères, 1 majuscule, 1 minuscule, 1 chiffre</p>
            )}
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

        {/* Social Auth Buttons */}
        <SocialAuthButtons
          mode={mode === 'login' ? 'login' : 'signup'}
          onSuccess={() => {
            setSuccess('Connexion sociale réussie !');
            setTimeout(() => onClose?.(), 1500);
          }}
          onError={(provider, err) => setLocalError(`Erreur ${provider}: ${err}`)}
        />

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
