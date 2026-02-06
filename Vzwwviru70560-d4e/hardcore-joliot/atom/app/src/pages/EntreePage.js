/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ███████╗███╗   ██╗████████╗██████╗ ███████╗███████╗
 *      ██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██╔════╝██╔════╝
 *      █████╗  ██╔██╗ ██║   ██║   ██████╔╝█████╗  █████╗
 *      ██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗██╔══╝  ██╔══╝
 *      ███████╗██║ ╚████║   ██║   ██║  ██║███████╗███████╗
 *      ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
 *
 *                    🔱 PORTE D'ENTRÉE CANONIQUE 🔱
 *                      Affichage MINIMAL requis
 *
 *   VÉRITÉS CANONIQUES RESPECTÉES:
 *   - Aucune animation gratuite
 *   - Aucun badge, compteur ou indicateur envahissant
 *   - Calme cognitif (silence est une fonctionnalité)
 *   - Un seul thème
 *   - Clarté > fonctionnalités
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import OnboardingWizard from '../components/OnboardingWizard';
import { useAuth } from '../contexts/AuthContext';

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PUBLIQUE: LANDING MINIMAL
// Accessible SANS authentification
// ═══════════════════════════════════════════════════════════════════════════════

const LandingMinimal = ({ onEnter, onLogin }) => {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-4">
      {/* Logo - Simple, pas d'animation */}
      <div className="text-center mb-12">
        <div className="text-5xl mb-4">🔱</div>
        <h1 className="text-2xl font-bold tracking-widest text-yellow-500 mb-2">
          AT·OM
        </h1>
        <p className="text-sm text-gray-600">
          L'Arche des Résonances
        </p>
      </div>

      {/* Message court - Calme cognitif */}
      <p className="text-gray-500 text-center max-w-xs mb-12">
        Un système à 8 sphères pour organiser votre vie numérique.
      </p>

      {/* Actions - Minimal */}
      <div className="flex flex-col gap-3 w-full max-w-xs">
        <button
          onClick={onEnter}
          className="w-full px-6 py-3 bg-yellow-600 text-black font-medium rounded-lg hover:bg-yellow-500 transition-colors"
        >
          Commencer
        </button>
        <button
          onClick={onLogin}
          className="w-full px-6 py-3 text-gray-500 hover:text-white transition-colors"
        >
          J'ai déjà un compte
        </button>
      </div>

      {/* Footer minimal */}
      <div className="fixed bottom-4 text-gray-800 text-xs">
        CHE·NU V76
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PUBLIQUE: CONNEXION MINIMAL
// ═══════════════════════════════════════════════════════════════════════════════

const LoginMinimal = ({ onBack, onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Remplissez tous les champs.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const result = await login(email, password);
      if (result.success) {
        localStorage.setItem('atom_charte_accepted', 'true');
        localStorage.setItem('atom_onboarding_complete', 'true');
        onLogin();
      } else {
        setError(result.error || 'Email ou mot de passe incorrect');
      }
    } catch (err) {
      setError('Erreur de connexion. Veuillez réessayer.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-xs">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="text-3xl mb-2">🔱</div>
          <h2 className="text-lg font-bold text-white">Connexion</h2>
        </div>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Courriel"
            className="w-full px-4 py-3 bg-gray-900 border border-gray-800 rounded-lg text-white
              placeholder-gray-600 focus:outline-none focus:border-yellow-500/50"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Mot de passe"
            className="w-full px-4 py-3 bg-gray-900 border border-gray-800 rounded-lg text-white
              placeholder-gray-600 focus:outline-none focus:border-yellow-500/50"
          />

          {error && (
            <p className="text-red-500 text-sm">{error}</p>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full px-6 py-3 font-medium rounded-lg transition-colors ${
              isLoading
                ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                : 'bg-yellow-600 text-black hover:bg-yellow-500'
            }`}
          >
            {isLoading ? 'Connexion...' : 'Se connecter'}
          </button>
        </form>

        {/* Retour */}
        <button
          onClick={onBack}
          className="w-full mt-4 px-6 py-3 text-gray-500 hover:text-white transition-colors"
        >
          Retour
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: ENTRÉE
// Gère le flux: Landing → Login OU Onboarding → Dashboard
// ═══════════════════════════════════════════════════════════════════════════════

const EntreePage = () => {
  const navigate = useNavigate();
  const [view, setView] = useState('landing'); // landing, login, onboarding

  // Vérifier si déjà onboardé
  useEffect(() => {
    const onboardingComplete = localStorage.getItem('atom_onboarding_complete');
    const charteAccepted = localStorage.getItem('atom_charte_accepted');

    if (onboardingComplete && charteAccepted) {
      navigate('/tableau-de-bord');
    }
  }, [navigate]);

  // Handlers
  const handleEnter = () => setView('onboarding');
  const handleLogin = () => setView('login');
  const handleBack = () => setView('landing');
  const handleLoginSuccess = () => navigate('/tableau-de-bord');
  const handleOnboardingComplete = () => navigate('/tableau-de-bord');

  // Rendu conditionnel
  if (view === 'login') {
    return <LoginMinimal onBack={handleBack} onLogin={handleLoginSuccess} />;
  }

  if (view === 'onboarding') {
    return <OnboardingWizard onComplete={handleOnboardingComplete} />;
  }

  return <LandingMinimal onEnter={handleEnter} onLogin={handleLogin} />;
};

export default EntreePage;
