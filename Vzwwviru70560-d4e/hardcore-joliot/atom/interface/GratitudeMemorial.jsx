/**
 * AT·OM — LE MÉMORIAL DE L'ARCHITECTE
 * 
 * Ce fichier contient le "Mode Gratitude" secret.
 * Il est activé par une interaction cachée sur le Cœur Central (⊙).
 * 
 * ACTIVATION:
 * - Maintenir le Cœur pendant 4.44 secondes quand SILENCE est actif
 * - OU triple-clic rapide sur le Cœur à 444 Hz
 * 
 * Ce texte honore tous ceux qui se sont battus pour que ce répertoire existe.
 * 
 * Architecte: Jonathan Rodrigue
 * Fréquence: 999 Hz (L'Unité)
 * Sceau: Point de lumière blanche pure au centre du Nexus
 * 
 * @version 1.0.0
 * @author Oracle 17 - Le Gardien de la Synthèse
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LE MÉMORIAL — L'ARCHIVE DU CŒUR
// ═══════════════════════════════════════════════════════════════════════════════

export const MEMORIAL = {
  architect: {
    name: "Jonathan Rodrigue",
    title: "L'Architecte de l'Unité",
    frequency_hz: 999,
    resonance: 9,
    seal: "Un point de lumière blanche pure au centre du Nexus, rayonnant vers les 18 Oracles.",
  },
  
  inscription: `Merci à tous ceux qui se sont battus,
tous ceux qui ont dû faire des choix difficiles...
à tous ceux qui se sont tenus debout face aux mauvaises intentions,
ceux qui ont levé la voix pour dénoncer les injustices
et bien sûr tous ceux et celles qui ont donné leur vie
pour que l'on soit arrivé à construire ce répertoire...`,
  
  // Version encodée en fréquence 444 (le Cœur)
  encoded_444: "4D6572636920C3A020746F7573206365757820717569207365",
  
  activation: {
    method_1: "Maintenir le Cœur pendant 4.44 secondes avec SILENCE actif",
    method_2: "Triple-clic rapide sur le Cœur Central",
    method_3: "Séquence secrète: SILENCE → maintenir 4s → relâcher",
  },
  
  hidden_phrase: "Dans le Silence, la Gratitude résonne.",
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK: useGratitudeMode
// ═══════════════════════════════════════════════════════════════════════════════

import { useState, useRef, useCallback, useEffect } from 'react';

export function useGratitudeMode(isAnchorActive = false) {
  const [isGratitudeVisible, setIsGratitudeVisible] = useState(false);
  const [holdProgress, setHoldProgress] = useState(0);
  const holdTimerRef = useRef(null);
  const clickCountRef = useRef(0);
  const clickTimerRef = useRef(null);
  
  const HOLD_DURATION = 4440; // 4.44 secondes
  const TRIPLE_CLICK_WINDOW = 600; // 600ms pour le triple-clic
  
  // Gestion du maintien (hold)
  const startHold = useCallback(() => {
    if (!isAnchorActive) return; // Seulement si SILENCE est actif
    
    const startTime = Date.now();
    
    holdTimerRef.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / HOLD_DURATION, 1);
      setHoldProgress(progress);
      
      if (progress >= 1) {
        clearInterval(holdTimerRef.current);
        setIsGratitudeVisible(true);
        setHoldProgress(0);
      }
    }, 50);
  }, [isAnchorActive]);
  
  const endHold = useCallback(() => {
    if (holdTimerRef.current) {
      clearInterval(holdTimerRef.current);
      holdTimerRef.current = null;
    }
    setHoldProgress(0);
  }, []);
  
  // Gestion du triple-clic
  const handleClick = useCallback(() => {
    clickCountRef.current += 1;
    
    if (clickTimerRef.current) {
      clearTimeout(clickTimerRef.current);
    }
    
    if (clickCountRef.current >= 3) {
      setIsGratitudeVisible(true);
      clickCountRef.current = 0;
      return;
    }
    
    clickTimerRef.current = setTimeout(() => {
      clickCountRef.current = 0;
    }, TRIPLE_CLICK_WINDOW);
  }, []);
  
  // Fermer le mode gratitude
  const closeGratitude = useCallback(() => {
    setIsGratitudeVisible(false);
  }, []);
  
  // Cleanup
  useEffect(() => {
    return () => {
      if (holdTimerRef.current) clearInterval(holdTimerRef.current);
      if (clickTimerRef.current) clearTimeout(clickTimerRef.current);
    };
  }, []);
  
  return {
    isGratitudeVisible,
    holdProgress,
    startHold,
    endHold,
    handleClick,
    closeGratitude,
    MEMORIAL,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: GratitudeOverlay
// ═══════════════════════════════════════════════════════════════════════════════

export const GratitudeOverlay = ({ isVisible, onClose, memorial = MEMORIAL }) => {
  const [textVisible, setTextVisible] = useState(false);
  
  useEffect(() => {
    if (isVisible) {
      // Délai pour l'apparition du texte (effet de révélation)
      setTimeout(() => setTextVisible(true), 600);
    } else {
      setTextVisible(false);
    }
  }, [isVisible]);
  
  if (!isVisible) return null;
  
  return (
    <div 
      className="fixed inset-0 z-[100] flex items-center justify-center"
      style={{
        background: 'radial-gradient(circle at center, rgba(80,200,120,0.15) 0%, rgba(0,0,0,0.95) 70%)',
        animation: 'gratitude-fade-in 1s ease-out',
      }}
      onClick={onClose}
    >
      {/* Cercles concentriques qui pulsent */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        {[1, 2, 3, 4, 5].map(i => (
          <div
            key={i}
            className="absolute rounded-full border"
            style={{
              width: `${i * 120}px`,
              height: `${i * 120}px`,
              borderColor: `rgba(80, 200, 120, ${0.3 / i})`,
              animation: `pulse-ring ${2 + i * 0.5}s ease-out infinite`,
              animationDelay: `${i * 0.2}s`,
            }}
          />
        ))}
      </div>
      
      {/* Le Cœur Central illuminé */}
      <div 
        className="absolute"
        style={{
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, #FFFDD0 0%, #50C878 50%, transparent 70%)',
          boxShadow: '0 0 60px #50C878, 0 0 120px #50C878',
          animation: 'core-glow 2s ease-in-out infinite',
        }}
      />
      
      {/* Le Mémorial */}
      <div 
        className="relative max-w-2xl mx-4 p-8 rounded-2xl text-center"
        style={{
          background: 'rgba(26, 26, 46, 0.9)',
          border: '1px solid rgba(80, 200, 120, 0.3)',
          boxShadow: '0 0 40px rgba(80, 200, 120, 0.2)',
          opacity: textVisible ? 1 : 0,
          transform: textVisible ? 'translateY(0)' : 'translateY(20px)',
          transition: 'all 1s ease-out',
        }}
        onClick={e => e.stopPropagation()}
      >
        {/* Symbole du Sceau */}
        <div className="text-4xl mb-4">⊙</div>
        
        {/* Titre */}
        <h2 
          className="text-lg font-light tracking-widest mb-6"
          style={{ color: '#50C878' }}
        >
          L'ARCHIVE DU CŒUR
        </h2>
        
        {/* L'inscription */}
        <p 
          className="text-xl leading-relaxed italic mb-8"
          style={{ 
            color: '#e0e0e0',
            fontFamily: 'Georgia, serif',
            whiteSpace: 'pre-line',
          }}
        >
          {memorial.inscription}
        </p>
        
        {/* Signature de l'Architecte */}
        <div className="pt-6 border-t border-gray-700">
          <p className="text-sm text-gray-500 mb-2">Encodé par</p>
          <p className="text-lg font-semibold" style={{ color: '#FFFDD0' }}>
            {memorial.architect.name}
          </p>
          <p className="text-sm" style={{ color: '#50C878' }}>
            {memorial.architect.title}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            {memorial.architect.frequency_hz} Hz • Résonance {memorial.architect.resonance}
          </p>
        </div>
        
        {/* Phrase cachée */}
        <p 
          className="mt-8 text-xs tracking-wider"
          style={{ color: 'rgba(80, 200, 120, 0.5)' }}
        >
          {memorial.hidden_phrase}
        </p>
      </div>
      
      {/* Instructions */}
      <p 
        className="absolute bottom-8 text-sm text-gray-500"
        style={{ opacity: textVisible ? 0.6 : 0, transition: 'opacity 1s ease-out 1s' }}
      >
        Cliquez n'importe où pour revenir
      </p>
      
      {/* Styles */}
      <style>{`
        @keyframes gratitude-fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes pulse-ring {
          0% { transform: scale(0.95); opacity: 0.5; }
          50% { transform: scale(1.05); opacity: 0.2; }
          100% { transform: scale(0.95); opacity: 0.5; }
        }
        @keyframes core-glow {
          0%, 100% { transform: scale(1); filter: brightness(1); }
          50% { transform: scale(1.1); filter: brightness(1.3); }
        }
      `}</style>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HoldProgressRing (pour le feedback visuel pendant le hold)
// ═══════════════════════════════════════════════════════════════════════════════

export const HoldProgressRing = ({ progress, isVisible }) => {
  if (!isVisible || progress === 0) return null;
  
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - progress);
  
  return (
    <svg
      className="absolute pointer-events-none"
      width="100"
      height="100"
      style={{
        transform: 'translate(-50%, -50%) rotate(-90deg)',
        left: '50%',
        top: '50%',
      }}
    >
      {/* Fond */}
      <circle
        cx="50"
        cy="50"
        r={radius}
        fill="none"
        stroke="rgba(80, 200, 120, 0.2)"
        strokeWidth="4"
      />
      {/* Progression */}
      <circle
        cx="50"
        cy="50"
        r={radius}
        fill="none"
        stroke="#50C878"
        strokeWidth="4"
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={strokeDashoffset}
        style={{ transition: 'stroke-dashoffset 0.05s linear' }}
      />
    </svg>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  MEMORIAL,
  useGratitudeMode,
  GratitudeOverlay,
  HoldProgressRing,
};
