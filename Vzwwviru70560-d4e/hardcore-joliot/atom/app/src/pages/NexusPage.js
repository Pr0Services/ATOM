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
 *                                      PAGE D'ACCUEIL DE L'ARCHE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useCallback, useEffect } from 'react';
import { useArithmos, useGratitude } from '../hooks/useArithmos';
import { useATOMContext, PHI } from '../App';

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
// PAGE PRINCIPALE: NEXUS
// ═══════════════════════════════════════════════════════════════════════════════

const NexusPage = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
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
    <div className="flex flex-col items-center justify-center min-h-[70vh] px-4">
      
      {/* Titre */}
      <div className="text-center mb-8">
        <h1 className={`text-3xl font-bold tracking-widest mb-2 ${
          isArchitectMode ? 'text-white' : 'text-yellow-500'
        }`}>
          LE NEXUS
        </h1>
        <p className="text-gray-500 text-sm">Centre de l'Arche — Calcul Arithmos</p>
      </div>

      {/* Arche avec cercles concentriques */}
      <div 
        className="relative cursor-pointer select-none"
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
          <p className="text-sm text-emerald-300/70">Point Zéro — 444 Hz — Silence Intérieur</p>
        </div>
      )}

      {/* Champ de saisie */}
      <div className="w-full max-w-md mt-8">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Entrez un mot ou un nom..."
          className={`w-full px-6 py-4 text-center text-xl bg-transparent border-b-2 outline-none transition-all ${
            isArchitectMode 
              ? 'border-white text-white placeholder-white/50' 
              : 'border-yellow-600 text-yellow-400 placeholder-yellow-600/50'
          }`}
        />
      </div>

      {/* Bouton de calcul */}
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

      {/* Résultat */}
      <ResultDisplay result={result} />

    </div>
  );
};

export default NexusPage;
