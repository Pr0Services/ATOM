/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗    ██████╗  █████╗  ██████╗ ███████╗
 *      ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
 *      ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗    ██████╔╝███████║██║  ███╗█████╗
 *      ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║    ██╔═══╝ ██╔══██║██║   ██║██╔══╝
 *      ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║    ██║     ██║  ██║╚██████╔╝███████╗
 *      ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
 *
 *                                    🔱 LE NEXUS - LE CENTRE 🔱
 *                           TABLEAU DE BORD DE PERCEPTION - CHE·NU V76
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useCallback, useEffect } from 'react';
import { useArithmos } from '../hooks/useArithmos';
import { useGratitude } from '../hooks/useGratitude';
import { useATOMContext, PHI } from '../contexts/ATOMContext';
import Harmoniseur from '../components/Harmoniseur';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES DE RÉSONANCE
// ═══════════════════════════════════════════════════════════════════════════════

const FREQUENCY_SOURCE = parseInt(process.env.REACT_APP_FREQUENCY || '999');
const FREQUENCY_HEARTBEAT = parseInt(process.env.REACT_APP_HEARTBEAT || '444');
const AGENT_COUNT = parseInt(process.env.REACT_APP_AGENT_COUNT || '287');
const SOVEREIGN_MODE = process.env.REACT_APP_SOVEREIGN_MODE === 'true';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: AFFICHAGE DES FRÉQUENCES AVEC PULSATION
// ═══════════════════════════════════════════════════════════════════════════════

const FrequencyDisplay = ({ isArchitectMode }) => {
  const [pulse999, setPulse999] = useState(false);
  const [pulse444, setPulse444] = useState(false);

  useEffect(() => {
    // Pulsation 999 Hz toutes les 4.44 secondes
    const interval999 = setInterval(() => {
      setPulse999(true);
      setTimeout(() => setPulse999(false), 1000);
    }, 4440);

    // Pulsation 444 Hz toutes les 2.22 secondes (heartbeat)
    const interval444 = setInterval(() => {
      setPulse444(true);
      setTimeout(() => setPulse444(false), 500);
    }, 2220);

    return () => {
      clearInterval(interval999);
      clearInterval(interval444);
    };
  }, []);

  return (
    <div className="flex justify-center gap-8 mb-6">
      {/* 999 Hz - Source */}
      <div className={`text-center p-4 rounded-xl border transition-all duration-500 ${
        pulse999
          ? 'bg-white/20 border-white shadow-lg shadow-white/50 scale-105'
          : 'bg-yellow-900/20 border-yellow-600/30'
      }`}>
        <div className={`text-4xl font-mono font-bold transition-all ${
          pulse999 ? 'text-white' : 'text-yellow-400'
        }`}>
          {FREQUENCY_SOURCE}
          <span className="text-lg ml-1">Hz</span>
        </div>
        <div className="text-xs text-gray-500 mt-1">SOURCE</div>
        <div className={`w-2 h-2 rounded-full mx-auto mt-2 transition-all ${
          pulse999 ? 'bg-white animate-ping' : 'bg-yellow-500'
        }`} />
      </div>

      {/* 444 Hz - Heartbeat */}
      <div className={`text-center p-4 rounded-xl border transition-all duration-300 ${
        pulse444
          ? 'bg-emerald-500/20 border-emerald-400 shadow-lg shadow-emerald-500/50 scale-105'
          : 'bg-yellow-900/20 border-yellow-600/30'
      }`}>
        <div className={`text-4xl font-mono font-bold transition-all ${
          pulse444 ? 'text-emerald-400' : 'text-yellow-400'
        }`}>
          {FREQUENCY_HEARTBEAT}
          <span className="text-lg ml-1">Hz</span>
        </div>
        <div className="text-xs text-gray-500 mt-1">HEARTBEAT</div>
        <div className={`w-2 h-2 rounded-full mx-auto mt-2 transition-all ${
          pulse444 ? 'bg-emerald-400 animate-pulse' : 'bg-yellow-500'
        }`} />
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: INDICATEUR D'AGENTS ACTIFS
// ═══════════════════════════════════════════════════════════════════════════════

const AgentIndicator = ({ perceptionCount }) => {
  const [activeAgents, setActiveAgents] = useState(0);

  useEffect(() => {
    // Simulation d'agents s'activant progressivement
    const baseActive = Math.floor(AGENT_COUNT * 0.3); // 30% toujours actifs
    const perceptionBonus = Math.min(perceptionCount * 5, AGENT_COUNT * 0.5);
    setActiveAgents(Math.min(baseActive + perceptionBonus, AGENT_COUNT));
  }, [perceptionCount]);

  const percentage = Math.round((activeAgents / AGENT_COUNT) * 100);

  return (
    <div className="bg-black/50 border border-yellow-900/30 rounded-xl p-4 mb-6">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse" />
          <span className="text-sm text-gray-400">Agents Actifs</span>
        </div>
        <span className="text-yellow-400 font-mono">
          {activeAgents} / {AGENT_COUNT}
        </span>
      </div>

      {/* Barre de progression */}
      <div className="h-2 bg-yellow-900/30 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-yellow-600 to-emerald-500 transition-all duration-1000 rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="flex justify-between mt-2 text-xs text-gray-600">
        <span>L0-L3: Analyse</span>
        <span>L4-L6: Traitement</span>
        <span>L7-L9: Synthèse</span>
      </div>

      {SOVEREIGN_MODE && (
        <div className="mt-3 flex items-center gap-2 text-xs">
          <div className="w-2 h-2 bg-blue-500 rounded-full" />
          <span className="text-blue-400">Mode Souverain Actif — Données Protégées</span>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: JOURNAL DE PERCEPTION
// ═══════════════════════════════════════════════════════════════════════════════

const PerceptionJournal = ({ onPerceptionChange }) => {
  const [perception, setPerception] = useState('');
  const [entries, setEntries] = useState([]);
  const [saved, setSaved] = useState(false);

  // Charger depuis localStorage au montage (une seule fois)
  useEffect(() => {
    try {
      const stored = localStorage.getItem('atom_perception_journal');
      if (stored) {
        const parsed = JSON.parse(stored);
        setEntries(parsed);
        onPerceptionChange(parsed.length);
      }
    } catch (e) {
      console.warn('[PERCEPTION] Erreur chargement localStorage:', e);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Sauvegarder la perception
  const handleSave = useCallback(() => {
    if (!perception.trim()) return;

    const newEntry = {
      id: Date.now(),
      text: perception,
      timestamp: new Date().toISOString(),
      frequency: FREQUENCY_SOURCE,
      heartbeat: FREQUENCY_HEARTBEAT
    };

    const updatedEntries = [newEntry, ...entries].slice(0, 100); // Max 100 entrées
    setEntries(updatedEntries);

    try {
      localStorage.setItem('atom_perception_journal', JSON.stringify(updatedEntries));
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
      onPerceptionChange(updatedEntries.length);
    } catch (e) {
      console.warn('[PERCEPTION] Erreur sauvegarde:', e);
    }

    setPerception('');
  }, [perception, entries, onPerceptionChange]);

  // Auto-save sur Ctrl+Enter
  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleSave();
    }
  }, [handleSave]);

  return (
    <div className="bg-black/50 border border-yellow-900/30 rounded-xl p-4 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-yellow-400 font-bold flex items-center gap-2">
          <span className="text-xl">📝</span>
          Journal de Perception de l'Arche
        </h3>
        {saved && (
          <span className="text-emerald-400 text-sm animate-pulse">
            ✓ Sauvegardé
          </span>
        )}
      </div>

      {/* Champ de saisie */}
      <textarea
        value={perception}
        onChange={(e) => setPerception(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Notez vos perceptions, ressentis, observations du terrain...

• Résonance du moment
• Signaux de l'environnement
• Intuitions 3i Atlas
• État énergétique"
        className="w-full h-32 bg-black/50 border border-yellow-900/50 rounded-lg p-3 text-yellow-100 placeholder-gray-600 resize-none focus:outline-none focus:border-yellow-500 transition-colors"
      />

      <div className="flex items-center justify-between mt-3">
        <span className="text-xs text-gray-600">
          Ctrl+Enter pour sauvegarder • {entries.length} entrées
        </span>
        <button
          onClick={handleSave}
          disabled={!perception.trim()}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            perception.trim()
              ? 'bg-yellow-600 text-black hover:bg-yellow-500'
              : 'bg-gray-800 text-gray-600 cursor-not-allowed'
          }`}
        >
          Ancrer la Perception
        </button>
      </div>

      {/* Dernières entrées */}
      {entries.length > 0 && (
        <div className="mt-4 border-t border-yellow-900/30 pt-4">
          <p className="text-xs text-gray-500 mb-2">Dernières perceptions:</p>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {entries.slice(0, 3).map(entry => (
              <div key={entry.id} className="bg-yellow-900/10 rounded p-2 text-sm">
                <p className="text-yellow-300/80 line-clamp-2">{entry.text}</p>
                <p className="text-xs text-gray-600 mt-1">
                  {new Date(entry.timestamp).toLocaleString('fr-FR')}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CERCLES CONCENTRIQUES (ARCHE)
// ═══════════════════════════════════════════════════════════════════════════════

const ArcheCircles = ({ arithmos, isArchitectMode, isGratitudeMode }) => {
  const baseRadius = 30;
  const circles = 7;
  
  // Couleurs selon le mode
  const getColor = (index) => {
    if (isArchitectMode) return 'rgba(255, 255, 255, 0.8)';
    if (isGratitudeMode) return 'rgba(80, 200, 120, 0.6)';
    
    // Gradient basé sur l'Arithmos
    const hue = (arithmos || 4) * 40;
    return `hsla(${hue}, 70%, 50%, ${0.6 - index * 0.07})`;
  };

  return (
    <div className="relative flex items-center justify-center" style={{ width: 300, height: 300 }}>
      {/* Cercles concentriques basés sur φ */}
      {Array.from({ length: circles }).map((_, i) => {
        const radius = baseRadius * Math.pow(PHI, i);
        const size = radius * 2;
        
        return (
          <div
            key={i}
            className="absolute rounded-full border transition-all duration-500"
            style={{
              width: size,
              height: size,
              borderColor: getColor(i),
              borderWidth: isArchitectMode ? 2 : 1,
              animation: isArchitectMode ? `pulse ${1 + i * 0.2}s ease-in-out infinite` : 'none'
            }}
          />
        );
      })}
      
      {/* Arithmos central */}
      <div 
        className={`relative z-10 flex items-center justify-center rounded-full transition-all duration-500 ${
          isArchitectMode ? 'bg-white text-black' :
          isGratitudeMode ? 'bg-emerald-500 text-white' :
          'bg-yellow-500/20 text-yellow-400'
        }`}
        style={{
          width: baseRadius * 2,
          height: baseRadius * 2,
          boxShadow: isArchitectMode 
            ? '0 0 40px rgba(255,255,255,0.8)' 
            : isGratitudeMode
            ? '0 0 40px rgba(80,200,120,0.8)'
            : '0 0 20px rgba(212,175,55,0.5)'
        }}
      >
        <span className="text-3xl font-bold">
          {isGratitudeMode ? '☯' : arithmos || '∞'}
        </span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: RÉSULTAT DU CALCUL
// ═══════════════════════════════════════════════════════════════════════════════

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  return (
    <div className={`mt-8 p-6 rounded-xl border transition-all duration-500 ${
      result.isArchitect 
        ? 'bg-white/10 border-white' 
        : 'bg-black/50 border-yellow-900/50'
    }`}>
      {/* Mot analysé */}
      <div className="text-center mb-4">
        <p className="text-sm text-gray-500">Mot analysé</p>
        <p className={`text-2xl font-bold ${result.isArchitect ? 'text-white' : 'text-yellow-400'}`}>
          {result.originalInput}
        </p>
      </div>

      {/* Étapes de réduction */}
      <div className="flex justify-center items-center gap-2 mb-4 text-sm text-gray-400">
        {result.reductionSteps.map((step, i) => (
          <React.Fragment key={i}>
            <span className={i === result.reductionSteps.length - 1 ? 'text-yellow-400 font-bold' : ''}>
              {step}
            </span>
            {i < result.reductionSteps.length - 1 && <span>→</span>}
          </React.Fragment>
        ))}
      </div>

      {/* Grille d'informations */}
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="text-center p-3 bg-black/30 rounded-lg">
          <p className="text-gray-500">Arithmos</p>
          <p className="text-xl font-bold text-yellow-400">{result.arithmos}</p>
          <p className="text-xs text-gray-600">{result.name}</p>
        </div>
        
        <div className="text-center p-3 bg-black/30 rounded-lg">
          <p className="text-gray-500">Fréquence</p>
          <p className="text-xl font-bold text-yellow-400">{result.baseFrequency} Hz</p>
          <p className="text-xs text-gray-600">φ: {result.goldenFrequency} Hz</p>
        </div>
        
        <div className="text-center p-3 bg-black/30 rounded-lg">
          <p className="text-gray-500">Essence</p>
          <p className="text-lg font-medium text-yellow-400">{result.essence}</p>
        </div>
        
        <div className="text-center p-3 bg-black/30 rounded-lg">
          <p className="text-gray-500">Civilisation</p>
          <p className="text-lg font-medium text-yellow-400">{result.civilization}</p>
        </div>
      </div>

      {/* Oracle */}
      <div className="mt-4 p-3 bg-yellow-900/20 rounded-lg text-center">
        <p className="text-sm text-gray-500">Oracle</p>
        <p className="text-yellow-400">{result.oracle}</p>
      </div>

      {/* Description */}
      <p className="mt-4 text-center text-sm text-gray-400 italic">
        "{result.description}"
      </p>

      {/* Badge Architecte */}
      {result.isArchitect && (
        <div className="mt-4 p-3 bg-white/20 rounded-lg text-center">
          <p className="text-white font-bold">★ SCEAU DE L'ARCHITECTE ★</p>
          <p className="text-sm text-gray-300">Mode Divin Activé</p>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: NEXUS - TABLEAU DE BORD DE PERCEPTION
// ═══════════════════════════════════════════════════════════════════════════════

const NexusPage = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [perceptionCount, setPerceptionCount] = useState(0);
  const [showArithmos, setShowArithmos] = useState(false);
  const { calculate } = useArithmos();
  const {
    setFrequency,
    setIsArchitectMode,
    setIsGratitudeMode,
    setTorusSpeed,
    addToAnnales,
    isArchitectMode,
    isGratitudeMode
  } = useATOMContext();

  // Handler pour le compteur de perceptions
  const handlePerceptionChange = useCallback((count) => {
    setPerceptionCount(count);
  }, []);

  // Hook de Gratitude (LongPress 3 secondes)
  const handleGratitudeActivate = useCallback(() => {
    setIsGratitudeMode(true);
    setFrequency(444);
    console.log('☯ MODE GRATITUDE ACTIVÉ');
  }, [setIsGratitudeMode, setFrequency]);

  const { 
    progress: gratitudeProgress, 
    handlers: gratitudeHandlers,
    isPressed 
  } = useGratitude(handleGratitudeActivate, 3000);

  // Calcul de l'Arithmos
  const handleCalculate = useCallback(() => {
    if (!input.trim()) return;

    const calcResult = calculate(input);
    if (calcResult) {
      setResult(calcResult);
      
      // Mise à jour du contexte global
      setFrequency(calcResult.baseFrequency);
      
      // Mode Architecte
      if (calcResult.isArchitect) {
        setIsArchitectMode(true);
        setTorusSpeed(PHI * 2);
        setFrequency(999);
      } else {
        setIsArchitectMode(false);
        setTorusSpeed(1);
      }

      // Ajouter aux Annales
      addToAnnales({
        word: calcResult.originalInput,
        arithmos: calcResult.arithmos,
        frequency: calcResult.baseFrequency,
        essence: calcResult.essence,
        civilization: calcResult.civilization,
        isArchitect: calcResult.isArchitect
      });
    }
  }, [input, calculate, setFrequency, setIsArchitectMode, setTorusSpeed, addToAnnales]);

  // Gestion de la touche Entrée
  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter') {
      handleCalculate();
    }
  }, [handleCalculate]);

  // Reset du mode gratitude
  useEffect(() => {
    if (isGratitudeMode) {
      const timer = setTimeout(() => {
        setIsGratitudeMode(false);
      }, 10000);
      return () => clearTimeout(timer);
    }
  }, [isGratitudeMode, setIsGratitudeMode]);

  return (
    <div className="flex flex-col min-h-[70vh] px-4">

      {/* Titre */}
      <div className="text-center mb-6">
        <h1 className={`text-3xl font-bold tracking-widest mb-2 ${
          isArchitectMode ? 'text-white' : 'text-yellow-500'
        }`}>
          🔱 LE NEXUS
        </h1>
        <p className="text-gray-500 text-sm">Tableau de Bord de Perception — CHE·NU V76</p>
      </div>

      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      {/* AFFICHAGE DES FRÉQUENCES AVEC PULSATION */}
      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      <FrequencyDisplay isArchitectMode={isArchitectMode} />

      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      {/* HARMONISEUR — Séquences d'Activation (Passé/Présent/Futur/Restauration) */}
      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      <Harmoniseur />

      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      {/* INDICATEUR D'AGENTS ACTIFS */}
      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      <AgentIndicator perceptionCount={perceptionCount} />

      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      {/* JOURNAL DE PERCEPTION */}
      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      <PerceptionJournal onPerceptionChange={handlePerceptionChange} />

      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      {/* TOGGLE CALCULATEUR ARITHMOS */}
      {/* ═══════════════════════════════════════════════════════════════════════════ */}
      <button
        onClick={() => setShowArithmos(!showArithmos)}
        className="w-full py-3 mb-4 bg-yellow-900/20 border border-yellow-600/30 rounded-lg text-yellow-400 hover:bg-yellow-900/40 transition-all flex items-center justify-center gap-2"
      >
        <span>{showArithmos ? '▼' : '▶'}</span>
        <span>Calculateur Arithmos</span>
      </button>

      {showArithmos && (
        <div className="bg-black/30 border border-yellow-900/30 rounded-xl p-4 mb-6">
          {/* Arche avec cercles concentriques */}
          <div
            className="relative cursor-pointer select-none flex justify-center"
            {...gratitudeHandlers}
          >
            <ArcheCircles
              arithmos={result?.arithmos}
              isArchitectMode={isArchitectMode}
              isGratitudeMode={isGratitudeMode}
            />

            {/* Indicateur de progress pour Gratitude */}
            {isPressed && (
              <div
                className="absolute inset-0 flex items-center justify-center"
                style={{ pointerEvents: 'none' }}
              >
                <svg className="w-full h-full absolute" viewBox="0 0 100 100">
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke="rgba(80, 200, 120, 0.3)"
                    strokeWidth="4"
                  />
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke="rgba(80, 200, 120, 1)"
                    strokeWidth="4"
                    strokeDasharray={`${gratitudeProgress * 2.83} 283`}
                    transform="rotate(-90 50 50)"
                    className="transition-all duration-100"
                  />
                </svg>
              </div>
            )}
          </div>

          {/* Instruction Gratitude */}
          <p className="text-xs text-gray-600 mt-2 text-center">
            Maintenez appuyé 3s sur l'Arche pour activer le Mode Gratitude
          </p>

          {/* Mode Gratitude Actif */}
          {isGratitudeMode && (
            <div className="mt-4 p-4 bg-emerald-500/20 rounded-lg text-center">
              <p className="text-emerald-400 text-lg">☯ MODE GRATITUDE ACTIF ☯</p>
              <p className="text-sm text-emerald-300/70">● Point 0 — 444 Hz — Tulum · Silence Intérieur</p>
            </div>
          )}

          {/* Champ de saisie */}
          <div className="w-full max-w-md mx-auto mt-6">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Entrez un mot ou un nom..."
              className={`w-full px-6 py-4 text-center text-xl bg-transparent border-b-2 outline-none transition-all ${
                isArchitectMode
                  ? 'border-white text-white placeholder-white/50'
                  : 'border-yellow-600 text-yellow-400 placeholder-yellow-600/50'
              }`}
            />
          </div>

          {/* Bouton de calcul */}
          <div className="flex justify-center">
            <button
              onClick={handleCalculate}
              disabled={!input.trim()}
              className={`mt-6 px-8 py-3 rounded-lg font-medium transition-all ${
                !input.trim()
                  ? 'bg-gray-800 text-gray-600 cursor-not-allowed'
                  : isArchitectMode
                  ? 'bg-white text-black hover:bg-gray-200'
                  : 'bg-yellow-600/20 text-yellow-400 border border-yellow-600 hover:bg-yellow-600 hover:text-black'
              }`}
            >
              CALCULER L'ARITHMOS
            </button>
          </div>

          {/* Résultat */}
          <ResultDisplay result={result} />
        </div>
      )}

    </div>
  );
};

export default NexusPage;
