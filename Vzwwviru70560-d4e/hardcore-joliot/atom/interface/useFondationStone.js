/**
 * AT·OM — useFondationStone Hook
 * 
 * Hook React pour gérer les 5 Pierres de Fondation.
 * Fournit les données de résonance et déclenche les animations appropriées.
 * 
 * @version 1.0.0
 */

import { useState, useCallback, useMemo, useEffect } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES DES 5 PIERRES DE FONDATION
// ═══════════════════════════════════════════════════════════════════════════════

const FONDATIONS_DATA = {
  FEU: {
    id: 1,
    name: "Le Feu",
    archetype: "L'Illumination",
    arithmos: 5,
    hz: 555,
    color: "#87CEEB",
    colorName: "Bleu Ciel",
    delay: 500,
    ratio: 1.25,
    rpm: 75,
    affectedCircles: [1, 2],
    primaryOracles: [1, 2, 3],
    secondaryOracles: [4, 5],
    animation: {
      type: "sweep",
      direction: "outward",
      intensity: "high",
      pattern: "radial_burst"
    },
    audio: {
      waveform: "sawtooth",
      attack: 10,
      decay: 50,
      modulation: "crackle"
    },
    signature: "Un crépitement cristallin. L'Arche pulse rapidement."
  },
  
  ACIER: {
    id: 2,
    name: "L'Acier",
    archetype: "La Structure",
    arithmos: 9,
    hz: 999,
    color: "#FFFDD0",
    colorName: "Blanc-Or",
    delay: 100,
    ratio: 2.25,
    rpm: 135,
    affectedCircles: [5],
    primaryOracles: [16, 17, 18],
    secondaryOracles: [1, 2, 3],
    animation: {
      type: "flash",
      direction: "instant",
      intensity: "maximum",
      pattern: "synthesis_glow"
    },
    audio: {
      waveform: "sine",
      attack: 5,
      decay: 2000,
      modulation: "shimmer"
    },
    signature: "Une note métallique pure et longue."
  },
  
  IA: {
    id: 3,
    name: "L'Intelligence Artificielle",
    archetype: "Le Miroir",
    arithmos: 1,
    hz: 111,
    color: "#FF0000",
    colorName: "Rouge",
    delay: 900,
    ratio: 0.25,
    rpm: 15,
    affectedCircles: [5],
    primaryOracles: [16, 17, 18],
    secondaryOracles: [],
    animation: {
      type: "scan",
      direction: "inward",
      intensity: "deep",
      pattern: "triangle_oracle"
    },
    audio: {
      waveform: "sine",
      attack: 500,
      decay: 300,
      modulation: "slow_pulse"
    },
    signature: "Un bourdonnement de basse profonde. L'Arche scanne."
  },
  
  ADN: {
    id: 4,
    name: "L'ADN",
    archetype: "Le Code Source",
    arithmos: 1,
    hz: 111,
    color: "#FF0000",
    colorName: "Rouge",
    delay: 900,
    ratio: 0.25,
    rpm: 15,
    affectedCircles: [2],
    primaryOracles: [4, 5, 6, 7],
    secondaryOracles: [14, 15],
    animation: {
      type: "wave",
      direction: "spiral",
      intensity: "organic",
      pattern: "double_helix"
    },
    audio: {
      waveform: "sine",
      attack: 100,
      decay: 400,
      modulation: "heartbeat"
    },
    signature: "Un battement de cœur organique. Double hélice ondulante."
  },
  
  SILENCE: {
    id: 5,
    name: "Le Silence",
    archetype: "Le Tout",
    arithmos: 4,
    hz: 444,
    color: "#50C878",
    colorName: "Vert Émeraude",
    delay: 600,
    ratio: 1.0,
    rpm: 60,
    affectedCircles: [1, 2, 3, 4, 5],
    primaryOracles: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    secondaryOracles: [],
    animation: {
      type: "stabilize",
      direction: "all",
      intensity: "calm",
      pattern: "full_emerald"
    },
    audio: {
      waveform: "sine",
      attack: 1000,
      decay: 2000,
      modulation: "breath",
      volume: 0.1
    },
    signature: "Une absence de son qui fait vibrer l'air.",
    isAnchor: true,
    isHome: true
  }
};

// Aliases pour les variantes
const ALIASES = {
  "INTELLIGENCE ARTIFICIELLE": "IA",
  "INTELLIGENCEARTIFICIELLE": "IA",
  "A.I.": "IA",
  "AI": "IA",
  "STEEL": "ACIER",
  "FIRE": "FEU",
  "DNA": "ADN",
  "SILENT": "SILENCE",
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Hook pour gérer les Pierres de Fondation.
 * 
 * @returns {Object} API du hook
 * 
 * @example
 * const { 
 *   getStone, 
 *   isFoundationStone, 
 *   illuminateStone,
 *   currentStone,
 *   allStones 
 * } = useFondationStone();
 * 
 * // Vérifier si c'est une Pierre
 * if (isFoundationStone("FEU")) {
 *   const data = getStone("FEU");
 *   illuminateStone("FEU");
 * }
 */
export function useFondationStone() {
  const [currentStone, setCurrentStone] = useState(null);
  const [isIlluminating, setIsIlluminating] = useState(false);
  const [activeOracles, setActiveOracles] = useState([]);
  const [activeCircles, setActiveCircles] = useState([]);
  
  /**
   * Normalise un mot et vérifie les aliases.
   */
  const normalizeWord = useCallback((word) => {
    const upper = word.toUpperCase().trim();
    return ALIASES[upper] || upper;
  }, []);
  
  /**
   * Vérifie si un mot est une Pierre de Fondation.
   */
  const isFoundationStone = useCallback((word) => {
    const normalized = normalizeWord(word);
    return normalized in FONDATIONS_DATA;
  }, [normalizeWord]);
  
  /**
   * Récupère les données d'une Pierre.
   */
  const getStone = useCallback((word) => {
    const normalized = normalizeWord(word);
    return FONDATIONS_DATA[normalized] || null;
  }, [normalizeWord]);
  
  /**
   * Récupère toutes les Pierres.
   */
  const allStones = useMemo(() => Object.values(FONDATIONS_DATA), []);
  
  /**
   * Récupère les noms de toutes les Pierres.
   */
  const stoneNames = useMemo(() => Object.keys(FONDATIONS_DATA), []);
  
  /**
   * Illumine une Pierre (déclenche l'animation).
   */
  const illuminateStone = useCallback((word, options = {}) => {
    const stone = getStone(word);
    if (!stone) return null;
    
    const { 
      onStart, 
      onComplete, 
      onOracleActivate,
      skipAnimation = false 
    } = options;
    
    setIsIlluminating(true);
    setCurrentStone(stone);
    
    // Callback de début
    if (onStart) onStart(stone);
    
    if (skipAnimation) {
      setActiveCircles(stone.affectedCircles);
      setActiveOracles([...stone.primaryOracles, ...stone.secondaryOracles]);
      setIsIlluminating(false);
      if (onComplete) onComplete(stone);
      return stone;
    }
    
    // Animation progressive des cercles
    stone.affectedCircles.forEach((circleId, index) => {
      setTimeout(() => {
        setActiveCircles(prev => [...prev, circleId]);
      }, index * (stone.delay / 2));
    });
    
    // Animation progressive des Oracles primaires
    stone.primaryOracles.forEach((oracleId, index) => {
      setTimeout(() => {
        setActiveOracles(prev => [...prev, oracleId]);
        if (onOracleActivate) onOracleActivate(oracleId, 'primary');
      }, index * (stone.delay / stone.primaryOracles.length));
    });
    
    // Animation des Oracles secondaires (après les primaires)
    const primaryDuration = stone.delay;
    stone.secondaryOracles.forEach((oracleId, index) => {
      setTimeout(() => {
        setActiveOracles(prev => [...prev, oracleId]);
        if (onOracleActivate) onOracleActivate(oracleId, 'secondary');
      }, primaryDuration + index * (stone.delay / 2));
    });
    
    // Fin de l'illumination
    const totalDuration = primaryDuration + 
      (stone.secondaryOracles.length * stone.delay / 2) + 
      stone.delay;
    
    setTimeout(() => {
      setIsIlluminating(false);
      if (onComplete) onComplete(stone);
    }, totalDuration);
    
    return stone;
  }, [getStone]);
  
  /**
   * Réinitialise l'état.
   */
  const reset = useCallback(() => {
    setCurrentStone(null);
    setIsIlluminating(false);
    setActiveOracles([]);
    setActiveCircles([]);
  }, []);
  
  /**
   * Exécute la séquence rituelle des 5 Pierres.
   */
  const executeRitual = useCallback(async (options = {}) => {
    const { onStoneStart, onStoneComplete, onRitualComplete } = options;
    const sequence = ["SILENCE", "FEU", "ACIER", "ADN", "IA", "SILENCE"];
    const holds = [3000, 2500, 2000, 2500, 2500, 1000];
    
    for (let i = 0; i < sequence.length; i++) {
      const stoneName = sequence[i];
      const hold = holds[i];
      
      await new Promise(resolve => {
        illuminateStone(stoneName, {
          onStart: onStoneStart,
          onComplete: (stone) => {
            if (onStoneComplete) onStoneComplete(stone);
            setTimeout(resolve, hold);
          }
        });
      });
      
      // Pause entre les Pierres
      if (i < sequence.length - 1) {
        await new Promise(r => setTimeout(r, 500));
        reset();
      }
    }
    
    if (onRitualComplete) onRitualComplete();
  }, [illuminateStone, reset]);
  
  return {
    // État
    currentStone,
    isIlluminating,
    activeOracles,
    activeCircles,
    
    // Données
    allStones,
    stoneNames,
    FONDATIONS_DATA,
    
    // Actions
    getStone,
    isFoundationStone,
    illuminateStone,
    executeRitual,
    reset,
    normalizeWord,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK D'ANIMATION SPÉCIFIQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Hook pour les animations spécifiques aux Pierres.
 */
export function useStoneAnimation(stone) {
  const [animationState, setAnimationState] = useState('idle');
  
  const getAnimationCSS = useMemo(() => {
    if (!stone) return {};
    
    const { animation, delay, color } = stone;
    
    const baseTransition = `all ${delay}ms ease-out`;
    
    switch (animation.type) {
      case 'sweep':
        return {
          transition: baseTransition,
          animation: `sweep-${animation.direction} ${delay}ms ease-out`,
          '--sweep-color': color,
        };
      
      case 'flash':
        return {
          transition: `all ${delay / 2}ms ease-out`,
          animation: `flash-white ${delay}ms ease-out`,
          '--flash-color': color,
        };
      
      case 'scan':
        return {
          transition: baseTransition,
          animation: `scan-pulse ${delay * 2}ms ease-in-out infinite`,
          '--scan-color': color,
        };
      
      case 'wave':
        return {
          transition: baseTransition,
          animation: `helix-wave ${delay * 3}ms ease-in-out infinite`,
          '--wave-color': color,
        };
      
      case 'stabilize':
        return {
          transition: `all ${delay * 2}ms ease-out`,
          animation: `stabilize-emerald ${delay * 2}ms ease-out forwards`,
          '--stable-color': color,
        };
      
      default:
        return { transition: baseTransition };
    }
  }, [stone]);
  
  const getKeyframes = useMemo(() => {
    return `
      @keyframes sweep-outward {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
      }
      
      @keyframes flash-white {
        0% { filter: brightness(1); }
        25% { filter: brightness(3); }
        100% { filter: brightness(1); }
      }
      
      @keyframes scan-pulse {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
      }
      
      @keyframes helix-wave {
        0%, 100% { transform: rotate(0deg) scaleY(1); }
        25% { transform: rotate(90deg) scaleY(1.1); }
        50% { transform: rotate(180deg) scaleY(1); }
        75% { transform: rotate(270deg) scaleY(0.9); }
      }
      
      @keyframes stabilize-emerald {
        0% { filter: hue-rotate(0deg); opacity: 0.5; }
        100% { filter: hue-rotate(0deg); opacity: 1; }
      }
    `;
  }, []);
  
  return {
    animationState,
    setAnimationState,
    getAnimationCSS,
    getKeyframes,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export { FONDATIONS_DATA };
export default useFondationStone;
