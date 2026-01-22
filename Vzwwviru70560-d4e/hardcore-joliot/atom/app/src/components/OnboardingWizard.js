/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       ██████╗ ███╗   ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗
 *      ██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝
 *      ██║   ██║██╔██╗ ██║██████╔╝██║   ██║███████║██████╔╝██║  ██║██║██╔██╗ ██║██║  ███╗
 *      ██║   ██║██║╚██╗██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║██║██║╚██╗██║██║   ██║
 *      ╚██████╔╝██║ ╚████║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝
 *       ╚═════╝ ╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝
 *
 *                          🏛️ ONBOARDING WIZARD CANONIQUE 🏛️
 *                              7 Étapes Non-Linéaires
 *
 *   VÉRITÉS CANONIQUES RESPECTÉES:
 *   - 7 étapes (5 et 7 optionnelles)
 *   - Affichage MINIMAL (calme cognitif)
 *   - Nova guide silencieusement (pas de chat)
 *   - Aucune animation gratuite
 *   - Aucune gamification
 *
 *   FLUX:
 *   1 → 2 → 3 → 4 → 5(opt) → 6 → 7(opt)
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES CANONIQUES
// ═══════════════════════════════════════════════════════════════════════════════

// Les 4 Univers disponibles
const UNIVERS = [
  { id: 'minimal', name: 'Minimal', desc: 'Épuré, essentiel', preview: '⬜' },
  { id: 'nature', name: 'Nature', desc: 'Organique, calme', preview: '🌿' },
  { id: 'cosmos', name: 'Cosmos', desc: 'Profond, infini', preview: '🌌' },
  { id: 'arche', name: 'Arche', desc: 'Doré, souverain', preview: '🔱' }
];

// Les 8 Sphères (FROZEN)
const SPHERES = [
  { id: 'personal', name: 'Personnel', icon: '🏠', defaultRoom: 'Chambre' },
  { id: 'business', name: 'Affaires', icon: '💼', defaultRoom: 'Bureau' },
  { id: 'government', name: 'Gouvernement', icon: '🏛️', defaultRoom: 'Hall' },
  { id: 'studio', name: 'Studio', icon: '🎨', defaultRoom: 'Atelier' },
  { id: 'community', name: 'Communauté', icon: '👥', defaultRoom: 'Agora' },
  { id: 'social', name: 'Social', icon: '📱', defaultRoom: 'Salon' },
  { id: 'entertainment', name: 'Divertissement', icon: '🎬', defaultRoom: 'Cinéma' },
  { id: 'team', name: 'Mon Équipe', icon: '🤝', defaultRoom: 'Salle' }
];

// Les 4 Concepts du Tutorial
const CONCEPTS = [
  { id: 'spheres', title: 'Les Sphères', desc: '8 contextes de vie séparés. Chaque sphère isole vos données et votre attention.' },
  { id: 'bureau', title: 'Le Bureau Unifié', desc: '6 sections maximum par sphère. Quick Capture, Threads, Fichiers, Agents, Réunions.' },
  { id: 'navigation', title: 'Navigation & Pièces', desc: 'Chaque sphère a sa pièce. Vous décidez où placer chaque contexte.' },
  { id: 'governance', title: 'Gouvernance & Tokens', desc: 'Vous contrôlez. Les agents proposent, vous décidez. Tokens = énergie d\'intelligence.' }
];

// Plateformes de connexion (optionnel)
const PLATFORMS = [
  { id: 'google', name: 'Google', icon: '📧', desc: 'Gmail, Calendar, Drive' },
  { id: 'outlook', name: 'Outlook', icon: '📬', desc: 'Email, Calendar' },
  { id: 'notion', name: 'Notion', icon: '📝', desc: 'Notes, Bases de données' },
  { id: 'slack', name: 'Slack', icon: '💬', desc: 'Messages, Canaux' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: INDICATEUR DE PROGRESSION (Minimal)
// ═══════════════════════════════════════════════════════════════════════════════

const ProgressIndicator = ({ currentStep, totalSteps }) => {
  return (
    <div className="flex items-center justify-center gap-2 mb-8">
      {Array.from({ length: totalSteps }, (_, i) => (
        <div
          key={i}
          className={`w-2 h-2 rounded-full transition-colors ${
            i + 1 === currentStep
              ? 'bg-yellow-500'
              : i + 1 < currentStep
              ? 'bg-gray-600'
              : 'bg-gray-800'
          }`}
        />
      ))}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: NOVA GUIDE (Silencieux, factuel)
// ═══════════════════════════════════════════════════════════════════════════════

const NovaGuide = ({ message }) => {
  if (!message) return null;

  return (
    <div className="flex items-start gap-3 p-4 bg-gray-900/50 rounded-lg border border-gray-800 mb-6">
      <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center flex-shrink-0">
        <span className="text-sm">🌟</span>
      </div>
      <p className="text-sm text-gray-400">{message}</p>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAPE 1: BIENVENUE & INTRODUCTION
// ═══════════════════════════════════════════════════════════════════════════════

const Step1Welcome = ({ onNext }) => {
  return (
    <div className="text-center max-w-md mx-auto">
      <div className="text-6xl mb-6">🔱</div>
      <h1 className="text-2xl font-bold text-white mb-4">CHE·NU</h1>
      <p className="text-gray-400 mb-8">
        Un système à 8 sphères pour organiser votre vie numérique.
      </p>

      <NovaGuide message="Bienvenue. Ce parcours prend environ 3 minutes. Les étapes 5 et 7 sont optionnelles." />

      <button
        onClick={onNext}
        className="px-8 py-3 bg-yellow-600 text-black font-medium rounded-lg hover:bg-yellow-500 transition-colors"
      >
        Commencer
      </button>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAPE 2: CHOIX DE L'UNIVERS
// ═══════════════════════════════════════════════════════════════════════════════

const Step2Universe = ({ selected, onSelect, onNext, onBack }) => {
  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-xl font-bold text-white mb-2 text-center">Choisissez votre univers</h2>
      <p className="text-gray-500 text-sm mb-6 text-center">Le thème visuel de votre espace.</p>

      <NovaGuide message="L'univers définit l'ambiance visuelle. Vous pourrez le changer plus tard." />

      <div className="grid grid-cols-2 gap-3 mb-8">
        {UNIVERS.map(u => (
          <button
            key={u.id}
            onClick={() => onSelect(u.id)}
            className={`p-4 rounded-xl border text-left transition-colors ${
              selected === u.id
                ? 'border-yellow-500 bg-yellow-500/10'
                : 'border-gray-800 hover:border-gray-600'
            }`}
          >
            <div className="text-3xl mb-2">{u.preview}</div>
            <div className="text-white font-medium">{u.name}</div>
            <div className="text-xs text-gray-500">{u.desc}</div>
          </button>
        ))}
      </div>

      <div className="flex gap-3">
        <button onClick={onBack} className="px-6 py-3 text-gray-400 hover:text-white transition-colors">
          Retour
        </button>
        <button
          onClick={onNext}
          disabled={!selected}
          className={`flex-1 px-6 py-3 rounded-lg font-medium transition-colors ${
            selected
              ? 'bg-yellow-600 text-black hover:bg-yellow-500'
              : 'bg-gray-800 text-gray-600 cursor-not-allowed'
          }`}
        >
          Continuer
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAPE 3: ATTRIBUTION DES 8 PIÈCES
// ═══════════════════════════════════════════════════════════════════════════════

const Step3Rooms = ({ rooms, onUpdateRoom, onNext, onBack }) => {
  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-xl font-bold text-white mb-2 text-center">Nommez vos pièces</h2>
      <p className="text-gray-500 text-sm mb-6 text-center">Chaque sphère a sa pièce dans votre espace.</p>

      <NovaGuide message="Les noms par défaut fonctionnent bien. Personnalisez si vous le souhaitez." />

      <div className="space-y-2 mb-8">
        {SPHERES.map(sphere => (
          <div key={sphere.id} className="flex items-center gap-3 p-3 bg-gray-900/50 rounded-lg">
            <span className="text-xl w-8">{sphere.icon}</span>
            <span className="text-sm text-gray-400 w-24">{sphere.name}</span>
            <input
              type="text"
              value={rooms[sphere.id] || sphere.defaultRoom}
              onChange={(e) => onUpdateRoom(sphere.id, e.target.value)}
              placeholder={sphere.defaultRoom}
              className="flex-1 px-3 py-2 bg-black border border-gray-700 rounded text-sm text-white
                placeholder-gray-600 focus:outline-none focus:border-yellow-500/50"
            />
          </div>
        ))}
      </div>

      <div className="flex gap-3">
        <button onClick={onBack} className="px-6 py-3 text-gray-400 hover:text-white transition-colors">
          Retour
        </button>
        <button
          onClick={onNext}
          className="flex-1 px-6 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 transition-colors"
        >
          Continuer
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAPE 4: TUTORIAL INTERACTIF (4 Concepts)
// ═══════════════════════════════════════════════════════════════════════════════

const Step4Tutorial = ({ currentConcept, onNextConcept, onComplete, onBack }) => {
  const concept = CONCEPTS[currentConcept];
  const isLast = currentConcept === CONCEPTS.length - 1;

  return (
    <div className="max-w-md mx-auto text-center">
      <div className="text-xs text-gray-600 mb-4">
        Concept {currentConcept + 1} / {CONCEPTS.length}
      </div>

      <h2 className="text-xl font-bold text-white mb-4">{concept.title}</h2>
      <p className="text-gray-400 mb-8">{concept.desc}</p>

      <div className="flex gap-3">
        <button onClick={onBack} className="px-6 py-3 text-gray-400 hover:text-white transition-colors">
          Retour
        </button>
        <button
          onClick={isLast ? onComplete : onNextConcept}
          className="flex-1 px-6 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 transition-colors"
        >
          {isLast ? 'Compris' : 'Suivant'}
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAPE 5: CONNEXIONS PLATEFORMES (Optionnel)
// ═══════════════════════════════════════════════════════════════════════════════

const Step5Connections = ({ connected, onToggle, onNext, onSkip, onBack }) => {
  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-xl font-bold text-white mb-2 text-center">Connexions</h2>
      <p className="text-gray-500 text-sm mb-6 text-center">Optionnel. Vous pouvez le faire plus tard.</p>

      <NovaGuide message="Les connexions permettent de synchroniser vos données existantes." />

      <div className="grid grid-cols-2 gap-3 mb-8">
        {PLATFORMS.map(p => (
          <button
            key={p.id}
            onClick={() => onToggle(p.id)}
            className={`p-4 rounded-xl border text-left transition-colors ${
              connected.includes(p.id)
                ? 'border-green-500 bg-green-500/10'
                : 'border-gray-800 hover:border-gray-600'
            }`}
          >
            <div className="text-2xl mb-2">{p.icon}</div>
            <div className="text-white font-medium text-sm">{p.name}</div>
            <div className="text-xs text-gray-500">{p.desc}</div>
          </button>
        ))}
      </div>

      <div className="flex gap-3">
        <button onClick={onBack} className="px-6 py-3 text-gray-400 hover:text-white transition-colors">
          Retour
        </button>
        <button
          onClick={onSkip}
          className="px-6 py-3 text-gray-400 hover:text-white transition-colors"
        >
          Passer
        </button>
        <button
          onClick={onNext}
          className="flex-1 px-6 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 transition-colors"
        >
          Continuer
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAPE 6: RÉSUMÉ DES CHOIX
// ═══════════════════════════════════════════════════════════════════════════════

const Step6Summary = ({ data, onNext, onBack }) => {
  const universe = UNIVERS.find(u => u.id === data.universe);

  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-xl font-bold text-white mb-6 text-center">Résumé</h2>

      <div className="space-y-4 mb-8">
        {/* Univers */}
        <div className="p-4 bg-gray-900/50 rounded-lg border border-gray-800">
          <div className="text-xs text-gray-600 mb-1">Univers</div>
          <div className="flex items-center gap-2">
            <span>{universe?.preview}</span>
            <span className="text-white">{universe?.name}</span>
          </div>
        </div>

        {/* Pièces */}
        <div className="p-4 bg-gray-900/50 rounded-lg border border-gray-800">
          <div className="text-xs text-gray-600 mb-2">Vos 8 Pièces</div>
          <div className="grid grid-cols-2 gap-2">
            {SPHERES.map(s => (
              <div key={s.id} className="flex items-center gap-2 text-sm">
                <span>{s.icon}</span>
                <span className="text-gray-400">{data.rooms[s.id] || s.defaultRoom}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Connexions */}
        {data.connections.length > 0 && (
          <div className="p-4 bg-gray-900/50 rounded-lg border border-gray-800">
            <div className="text-xs text-gray-600 mb-1">Connexions</div>
            <div className="flex gap-2">
              {data.connections.map(c => {
                const platform = PLATFORMS.find(p => p.id === c);
                return <span key={c} className="text-xl">{platform?.icon}</span>;
              })}
            </div>
          </div>
        )}
      </div>

      <div className="flex gap-3">
        <button onClick={onBack} className="px-6 py-3 text-gray-400 hover:text-white transition-colors">
          Modifier
        </button>
        <button
          onClick={onNext}
          className="flex-1 px-6 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 transition-colors"
        >
          Valider et Terminer
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ÉTAPE 7: PROFILS SPHÈRES (Optionnel, peut être fait plus tard)
// ═══════════════════════════════════════════════════════════════════════════════

const Step7Profiles = ({ onComplete, onSkip }) => {
  return (
    <div className="max-w-md mx-auto text-center">
      <h2 className="text-xl font-bold text-white mb-4">Configuration avancée</h2>
      <p className="text-gray-400 mb-8">
        Vous pouvez configurer chaque sphère en détail maintenant ou plus tard depuis les paramètres.
      </p>

      <NovaGuide message="La plupart des utilisateurs préfèrent explorer d'abord, puis configurer." />

      <div className="flex flex-col gap-3">
        <button
          onClick={onSkip}
          className="px-6 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 transition-colors"
        >
          Commencer à explorer
        </button>
        <button
          onClick={onComplete}
          className="px-6 py-3 text-gray-400 hover:text-white transition-colors"
        >
          Configurer maintenant
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// WIZARD PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const OnboardingWizard = ({ onComplete }) => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [tutorialConcept, setTutorialConcept] = useState(0);

  // Données collectées
  const [data, setData] = useState({
    universe: null,
    rooms: {},
    connections: []
  });

  // Handlers
  const handleComplete = useCallback(() => {
    // Sauvegarder les données d'onboarding
    localStorage.setItem('atom_onboarding_complete', 'true');
    localStorage.setItem('atom_onboarding_data', JSON.stringify(data));
    localStorage.setItem('atom_charte_accepted', 'true');

    if (onComplete) {
      onComplete(data);
    } else {
      navigate('/tableau-de-bord');
    }
  }, [data, navigate, onComplete]);

  const updateRooms = useCallback((sphereId, roomName) => {
    setData(prev => ({
      ...prev,
      rooms: { ...prev.rooms, [sphereId]: roomName }
    }));
  }, []);

  const toggleConnection = useCallback((platformId) => {
    setData(prev => ({
      ...prev,
      connections: prev.connections.includes(platformId)
        ? prev.connections.filter(c => c !== platformId)
        : [...prev.connections, platformId]
    }));
  }, []);

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-4">
      <ProgressIndicator currentStep={step} totalSteps={7} />

      {step === 1 && (
        <Step1Welcome onNext={() => setStep(2)} />
      )}

      {step === 2 && (
        <Step2Universe
          selected={data.universe}
          onSelect={(u) => setData(prev => ({ ...prev, universe: u }))}
          onNext={() => setStep(3)}
          onBack={() => setStep(1)}
        />
      )}

      {step === 3 && (
        <Step3Rooms
          rooms={data.rooms}
          onUpdateRoom={updateRooms}
          onNext={() => setStep(4)}
          onBack={() => setStep(2)}
        />
      )}

      {step === 4 && (
        <Step4Tutorial
          currentConcept={tutorialConcept}
          onNextConcept={() => setTutorialConcept(c => c + 1)}
          onComplete={() => setStep(5)}
          onBack={() => {
            if (tutorialConcept > 0) {
              setTutorialConcept(c => c - 1);
            } else {
              setStep(3);
            }
          }}
        />
      )}

      {step === 5 && (
        <Step5Connections
          connected={data.connections}
          onToggle={toggleConnection}
          onNext={() => setStep(6)}
          onSkip={() => setStep(6)}
          onBack={() => {
            setTutorialConcept(CONCEPTS.length - 1);
            setStep(4);
          }}
        />
      )}

      {step === 6 && (
        <Step6Summary
          data={data}
          onNext={() => setStep(7)}
          onBack={() => setStep(5)}
        />
      )}

      {step === 7 && (
        <Step7Profiles
          onComplete={() => {
            // Aller vers configuration avancée
            handleComplete();
          }}
          onSkip={handleComplete}
        />
      )}

      {/* Footer minimal */}
      <div className="fixed bottom-4 text-center text-gray-800 text-xs">
        CHE·NU • Mode Souverain
      </div>
    </div>
  );
};

export default OnboardingWizard;
