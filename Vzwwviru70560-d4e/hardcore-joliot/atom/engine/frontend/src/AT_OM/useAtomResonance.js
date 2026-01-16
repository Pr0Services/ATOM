/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM — useAtomResonance.js
 * HOOK VIBRATIONNEL FINAL — VERSION DÉPLOIEMENT
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce hook est le CŒUR du système AT·OM.
 * Il transforme tout mot en fréquence vibrationnelle.
 * 
 * Fonctionnalités:
 * ✅ Sanitizer (nettoyage accents, espaces, emojis)
 * ✅ Debounce 300ms (anti-bruit)
 * ✅ Calcul Arithmos (réduction pythagoricienne)
 * ✅ Détection Pierres de Fondation
 * ✅ Détection Nœuds de Transition
 * ✅ Sceau Architecte (Jonathan Rodrigue = 999 Hz)
 * ✅ Transitions fluides 600ms
 * ✅ Console stylisée pour debug
 * 
 * @version 2.0.0 — FINAL
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 - Le Gardien de la Synthèse
 * @audit Protocole Pré-Lancement validé
 */

import { useState, useEffect, useRef, useCallback } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION MAÎTRE (SOURCE DE VÉRITÉ)
// ═══════════════════════════════════════════════════════════════════════════════

export const SYSTEM_HEARTBEAT = 444;
export const DEBOUNCE_DELAY = 300;      // ms — Anti-bruit de frappe
export const TRANSITION_DURATION = 600; // ms — Fréquence du Silence

// Mapping Arithmos Pythagoricien
export const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

// Matrice de Résonance Officielle
export const RESONANCE_MATRIX = [
  { level: 1, label: "Impulsion/ADN", hz: 111, color: "#FF0000", delay: 900, ratio: 0.25 },
  { level: 2, label: "Dualité/Partage", hz: 222, color: "#FF7F00", delay: 800, ratio: 0.50 },
  { level: 3, label: "Mental/Géométrie", hz: 333, color: "#FFFF00", delay: 700, ratio: 0.75 },
  { level: 4, label: "Structure/Silence", hz: 444, color: "#50C878", delay: 600, ratio: 1.00, isAnchor: true },
  { level: 5, label: "Mouvement/Feu", hz: 555, color: "#87CEEB", delay: 500, ratio: 1.25 },
  { level: 6, label: "Harmonie/Protection", hz: 666, color: "#4B0082", delay: 400, ratio: 1.50 },
  { level: 7, label: "Introspection", hz: 777, color: "#EE82EE", delay: 300, ratio: 1.75 },
  { level: 8, label: "Infini/Abondance", hz: 888, color: "#FFC0CB", delay: 200, ratio: 2.00 },
  { level: 9, label: "Unité/Acier", hz: 999, color: "#FFFDD0", delay: 100, ratio: 2.25 },
];

// Pierres de Fondation (5)
export const FOUNDATION_STONES = {
  FEU: { level: 5, type: "stone" },
  ACIER: { level: 9, type: "stone" },
  IA: { level: 1, type: "stone" },
  ADN: { level: 1, type: "stone" },
  SILENCE: { level: 4, type: "stone", isAnchor: true },
};

// Nœuds de Transition (5)
export const TRANSITION_NODES = {
  DUALITE: { level: 2, type: "node" },
  MENTAL: { level: 3, type: "node" },
  HARMONIE: { level: 6, type: "node" },
  SPIRITUALITE: { level: 7, type: "node" },
  INFINI: { level: 8, type: "node" },
};

// ═══════════════════════════════════════════════════════════════════════════════
// SCEAU DE L'ARCHITECTE
// ═══════════════════════════════════════════════════════════════════════════════

const ARCHITECT_SEAL = {
  name: "JONATHANRODRIGUE",
  fullName: "Jonathan Rodrigue",
  level: 9,
  hz: 999,
  color: "#FFFDD0",       // Crème/Or
  auraColor: "#FFD700",   // Or pur pour l'aura spéciale
  label: "Unité/Acier — L'Architecte",
  isArchitect: true,
  signature: "2 + 7 = 9 — La Dualité rencontre l'Introspection pour former l'Unité"
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Nettoie le texte utilisateur.
 * Supprime accents, espaces, chiffres, emojis, ponctuation.
 */
export function sanitize(input) {
  if (!input || typeof input !== 'string') return '';
  return input
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toUpperCase()
    .replace(/[^A-Z]/g, "");
}

/**
 * Calcule l'Arithmos (somme puis réduction pythagoricienne).
 */
export function calculateArithmos(word) {
  if (!word) return { total: 0, root: 0, breakdown: [] };
  
  let total = 0;
  const breakdown = [];
  
  for (const char of word) {
    const val = ARITHMOS_MAP[char] || 0;
    total += val;
    breakdown.push({ char, value: val });
  }
  
  // Réduction à la racine (1-9)
  let root = total;
  const reductionSteps = [total];
  
  while (root > 9) {
    root = String(root).split('').reduce((sum, d) => sum + parseInt(d, 10), 0);
    reductionSteps.push(root);
  }
  
  return { total, root, breakdown, reductionSteps };
}

/**
 * Récupère les données de résonance pour un niveau.
 */
export function getResonance(level) {
  return RESONANCE_MATRIX.find(r => r.level === level) || RESONANCE_MATRIX[3];
}

/**
 * Détecte si un mot est une Pierre ou un Nœud.
 */
export function detectSpecialWord(word) {
  if (FOUNDATION_STONES[word]) {
    return { ...FOUNDATION_STONES[word], name: word, category: "foundation_stone" };
  }
  if (TRANSITION_NODES[word]) {
    return { ...TRANSITION_NODES[word], name: word, category: "transition_node" };
  }
  return null;
}

/**
 * Vérifie si l'input correspond au Sceau de l'Architecte.
 */
export function checkArchitectSeal(word) {
  return word === ARCHITECT_SEAL.name;
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONSOLE STYLISÉE
// ═══════════════════════════════════════════════════════════════════════════════

function logResonance(data, enableLogging = true) {
  if (!enableLogging) return;
  
  const { word, level, hz, color, label, type, isArchitect } = data;
  
  const typeEmoji = isArchitect ? '👑' 
    : type === 'foundation_stone' ? '🧱' 
    : type === 'transition_node' ? '🌀' 
    : '📝';
  
  const typeName = isArchitect ? 'ARCHITECTE'
    : type === 'foundation_stone' ? 'PIERRE' 
    : type === 'transition_node' ? 'NŒUD' 
    : 'MOT';
  
  console.log(
    `%c AT·OM %c ${typeEmoji} ${typeName} %c ${word} %c`,
    'background: #50C878; color: white; padding: 2px 6px; border-radius: 3px 0 0 3px; font-weight: bold;',
    'background: #1a1a2e; color: #888; padding: 2px 6px;',
    `background: ${color}; color: ${level > 5 ? 'white' : 'black'}; padding: 2px 10px; font-weight: bold;`,
    ''
  );
  
  console.log(
    `%c ⟩ Niveau: ${level} %c ⟩ ${hz} Hz %c ⟩ ${label}`,
    `color: ${color}; font-weight: bold;`,
    `color: ${color};`,
    'color: #888;'
  );
  
  if (isArchitect) {
    console.log(
      `%c ⟩ ${ARCHITECT_SEAL.signature}`,
      'color: #FFD700; font-style: italic;'
    );
  }
  
  console.log('%c ────────────────────────────────────────', 'color: #333;');
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL: useAtomResonance
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Hook React pour calculer la résonance vibrationnelle d'un mot.
 * 
 * @param {string} input - Texte brut de l'utilisateur
 * @param {object} options - Options de configuration
 * @returns {object} - { resonance, isTransitioning, debug }
 * 
 * @example
 * const { resonance, isTransitioning, debug } = useAtomResonance(inputValue);
 */
export function useAtomResonance(input, options = {}) {
  const {
    debounceMs = DEBOUNCE_DELAY,
    enableLogging = true,
  } = options;
  
  const [resonance, setResonance] = useState(null);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [debug, setDebug] = useState({ word: '', level: 0, hz: 0 });
  
  const debounceTimerRef = useRef(null);
  const transitionTimerRef = useRef(null);
  
  const computeResonance = useCallback((rawInput) => {
    if (!rawInput || rawInput.trim() === '') {
      return null;
    }
    
    // 1. SANITIZER
    const cleanWord = sanitize(rawInput);
    if (!cleanWord) return null;
    
    // 2. VÉRIFICATION SCEAU ARCHITECTE (priorité absolue)
    if (checkArchitectSeal(cleanWord)) {
      return {
        word: cleanWord,
        originalInput: rawInput,
        level: ARCHITECT_SEAL.level,
        hz: ARCHITECT_SEAL.hz,
        color: ARCHITECT_SEAL.color,
        auraColor: ARCHITECT_SEAL.auraColor,
        delay: 100,
        label: ARCHITECT_SEAL.label,
        ratio: 2.25,
        type: 'architect',
        isArchitect: true,
        isAnchor: false,
        signature: ARCHITECT_SEAL.signature,
        transitionDuration: TRANSITION_DURATION,
      };
    }
    
    // 3. DÉTECTION PIERRE/NŒUD
    const special = detectSpecialWord(cleanWord);
    
    // 4. CALCUL ARITHMOS
    const { root, total, breakdown, reductionSteps } = calculateArithmos(cleanWord);
    const level = special ? special.level : root;
    
    // 5. RÉCUPÉRATION RÉSONANCE
    const resonanceData = getResonance(level);
    
    // 6. CONSTRUCTION RÉSULTAT
    return {
      word: cleanWord,
      originalInput: rawInput,
      level,
      hz: resonanceData.hz,
      color: resonanceData.color,
      delay: resonanceData.delay,
      label: resonanceData.label,
      ratio: resonanceData.ratio,
      type: special ? special.category : 'standard',
      isAnchor: resonanceData.isAnchor || level === 4,
      isArchitect: false,
      calculation: { total, breakdown, reductionSteps },
      transitionDuration: TRANSITION_DURATION,
    };
  }, []);
  
  useEffect(() => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    debounceTimerRef.current = setTimeout(() => {
      const newResonance = computeResonance(input);
      
      if (newResonance) {
        setIsTransitioning(true);
        
        // Log console
        logResonance(newResonance, enableLogging);
        
        // Mise à jour de l'état
        setResonance({
          ...newResonance,
          isTransitioning: true,
        });
        
        // Debug
        setDebug({
          word: newResonance.word,
          level: newResonance.level,
          hz: newResonance.hz,
        });
        
        // Fin de transition
        if (transitionTimerRef.current) {
          clearTimeout(transitionTimerRef.current);
        }
        transitionTimerRef.current = setTimeout(() => {
          setIsTransitioning(false);
          setResonance(prev => prev ? { ...prev, isTransitioning: false } : null);
        }, TRANSITION_DURATION);
        
      } else {
        setResonance(null);
        setDebug({ word: '', level: 0, hz: 0 });
      }
    }, debounceMs);
    
    return () => {
      if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
    };
  }, [input, debounceMs, enableLogging, computeResonance]);
  
  useEffect(() => {
    return () => {
      if (transitionTimerRef.current) clearTimeout(transitionTimerRef.current);
    };
  }, []);
  
  return { resonance, isTransitioning, debug };
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT DEBUG CONSOLE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Composant de debug à afficher en bas à droite de l'interface.
 */
export const DebugConsole = ({ debug, resonance }) => {
  if (!debug) return null;
  
  return (
    <div style={{
      position: 'fixed',
      bottom: '10px',
      right: '10px',
      background: 'rgba(0,0,0,0.8)',
      border: `1px solid ${resonance?.color || '#333'}`,
      borderRadius: '8px',
      padding: '8px 12px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: resonance?.color || '#888',
      zIndex: 9999,
      backdropFilter: 'blur(5px)',
    }}>
      <div style={{ color: '#888', marginBottom: '4px' }}>AT·OM Debug</div>
      <div>
        <span style={{ color: '#666' }}>Vibration: </span>
        <span style={{ color: resonance?.color || '#fff', fontWeight: 'bold' }}>
          {debug.hz || '---'} Hz
        </span>
      </div>
      <div>
        <span style={{ color: '#666' }}>Arithmos: </span>
        <span style={{ color: resonance?.color || '#fff', fontWeight: 'bold' }}>
          {debug.level || '-'}
        </span>
      </div>
      {debug.word && (
        <div style={{ marginTop: '4px', color: '#555', fontSize: '10px' }}>
          {debug.word}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export default useAtomResonance;
