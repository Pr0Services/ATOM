/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * UNIVERSAL RESONANCE ENGINE — LE GRAND UNIFICATEUR
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   █████╗ ████████╗    ██████╗ ███╗   ███╗
 *  ██╔══██╗╚══██╔══╝   ██╔═══██╗████╗ ████║
 *  ███████║   ██║      ██║   ██║██╔████╔██║
 *  ██╔══██║   ██║      ██║   ██║██║╚██╔╝██║
 *  ██║  ██║   ██║   ██╗╚██████╔╝██║ ╚═╝ ██║
 *  ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝
 * 
 *                 UNIVERSAL RESONANCE ENGINE
 * 
 * Ce moteur fusionne 6 systèmes de sagesse ancestrale:
 * 
 * ┌─────────────────────────────────────────────────────────────────┐
 * │  1. ARITHMOS (Pythagoricien)     - La valeur numérique         │
 * │  2. TZOLKIN (Maya)               - Le calendrier sacré         │
 * │  3. YI-KING (Chinois)            - Les transformations         │
 * │  4. KABBALE (Hébraïque)          - L'arbre de vie              │
 * │  5. CHAKRAS (Indien)             - Les centres énergétiques    │
 * │  6. CYMATIQUE (Universel)        - Les formes du son           │
 * └─────────────────────────────────────────────────────────────────┘
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * @tuning A=444Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// IMPORTS
// ═══════════════════════════════════════════════════════════════════════════════

import TzolkinEngine, { getMayaResonance, calculateKin, NAWALS, TONS } from './tzolkin_engine.js';
import YiKingEngine, { getYiKingResonance, castCoins, TRIGRAMS } from './yiking_engine.js';
import KabbalahEngine, { getKabbalahResonance, SEPHIROTH, PATHS } from './kabbalah_engine.js';
import ChakraEngine, { getChakraResonance, CHAKRAS, SOLFEGGIO } from './chakra_engine.js';
import CymaticsEngine, { 
  calculateGeometricSignature, 
  PHI, 
  SACRED_GEOMETRY, 
  PLATONIC_SOLIDS 
} from './cymatics_engine.js';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION SYSTÈME
// ═══════════════════════════════════════════════════════════════════════════════

export const SYSTEM_CONFIG = {
  heartbeat: 444,
  tuning: "A=444Hz",
  architect: {
    name: "Jonathan Rodrigue",
    signature: "2 + 7 = 9",
    frequency: 999,
    aura: "#FFD700"
  },
  oracle: {
    number: 17,
    name: "Le Gardien de la Synthèse"
  },
  version: "1.0.0",
  codename: "CALENDRIER_VIVANT"
};

// ═══════════════════════════════════════════════════════════════════════════════
// MATRICE ARITHMOS (Base du système)
// ═══════════════════════════════════════════════════════════════════════════════

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = [
  { level: 1, hz: 111, color: "#FF0000", label: "Impulsion", stone: "ADN" },
  { level: 2, hz: 222, color: "#FF7F00", label: "Dualité", stone: "Partage" },
  { level: 3, hz: 333, color: "#FFFF00", label: "Mental", stone: "Géométrie" },
  { level: 4, hz: 444, color: "#50C878", label: "Structure", stone: "Silence", isAnchor: true },
  { level: 5, hz: 555, color: "#87CEEB", label: "Mouvement", stone: "Feu" },
  { level: 6, hz: 666, color: "#4B0082", label: "Harmonie", stone: "Protection" },
  { level: 7, hz: 777, color: "#EE82EE", label: "Introspection", stone: null },
  { level: 8, hz: 888, color: "#FFC0CB", label: "Infini", stone: "Abondance" },
  { level: 9, hz: 999, color: "#FFFDD0", label: "Unité", stone: "Acier" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTION PRINCIPALE: RÉSONANCE UNIVERSELLE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule la RÉSONANCE UNIVERSELLE complète pour un mot/concept
 * 
 * @param {string} word - Le mot ou concept à analyser
 * @param {Date} date - La date (pour les calculs Maya/temporels)
 * @returns {Object} - L'analyse complète multi-systèmes
 */
export function calculateUniversalResonance(word, date = new Date()) {
  // ═══════════════════════════════════════════════════════════════════════════
  // ÉTAPE 1: SANITISATION ET CALCUL ARITHMOS
  // ═══════════════════════════════════════════════════════════════════════════
  
  const sanitized = sanitize(word);
  const { total, reduced, steps } = calculateArithmos(sanitized);
  const resonance = RESONANCE_MATRIX[reduced - 1];
  
  // Vérifier si c'est le Sceau de l'Architecte
  const isArchitectSeal = sanitized === "JONATHANRODRIGUE";
  
  // ═══════════════════════════════════════════════════════════════════════════
  // ÉTAPE 2: CALCULS MULTI-SYSTÈMES
  // ═══════════════════════════════════════════════════════════════════════════
  
  // Maya (Tzolkin)
  const maya = getMayaResonance(date);
  const nawalMatch = NAWALS.filter(n => n.arithmos === reduced);
  
  // Yi-King
  const yiking = getYiKingResonance(reduced, sanitized);
  
  // Kabbale
  const kabbalah = getKabbalahResonance(reduced, sanitized);
  
  // Chakras
  const chakra = getChakraResonance(reduced, resonance.hz);
  
  // Cymatique & Géométrie Sacrée
  const geometry = calculateGeometricSignature(sanitized, reduced);
  
  // ═══════════════════════════════════════════════════════════════════════════
  // ÉTAPE 3: FUSION ET HARMONISATION
  // ═══════════════════════════════════════════════════════════════════════════
  
  // Calculer la fréquence finale (avec modificateur Maya)
  const baseFrequency = resonance.hz;
  const mayaModifier = maya.frequency_base / 100;
  const finalFrequency = isArchitectSeal ? 999 : baseFrequency;
  
  // Calculer le délai d'animation
  const baseDelay = 1000 - (reduced * 100);
  const finalDelay = Math.round(baseDelay * maya.delay_modifier);
  
  // Déterminer la couleur finale
  const finalColor = isArchitectSeal 
    ? "#FFFDD0" 
    : blendColors(resonance.color, maya.color_overlay, 0.2);
  
  // ═══════════════════════════════════════════════════════════════════════════
  // ÉTAPE 4: GÉNÉRER LE MESSAGE ORACLE
  // ═══════════════════════════════════════════════════════════════════════════
  
  const oracleMessage = generateOracleMessage({
    word: sanitized,
    arithmos: reduced,
    resonance,
    maya,
    yiking,
    kabbalah,
    chakra,
    geometry,
    isArchitectSeal
  });
  
  // ═══════════════════════════════════════════════════════════════════════════
  // ÉTAPE 5: RETOURNER L'ANALYSE COMPLÈTE
  // ═══════════════════════════════════════════════════════════════════════════
  
  return {
    // Identité
    input: word,
    sanitized: sanitized,
    timestamp: date.toISOString(),
    
    // Sceau Architecte
    isArchitectSeal: isArchitectSeal,
    architectSignature: isArchitectSeal ? SYSTEM_CONFIG.architect.signature : null,
    
    // Arithmos (Core AT·OM)
    arithmos: {
      total: total,
      reduced: reduced,
      steps: steps,
      resonance: resonance,
      frequency: finalFrequency,
      color: finalColor,
      delay: finalDelay
    },
    
    // Maya (Tzolkin)
    maya: {
      kin: maya.kin,
      signature: maya.signature,
      ton: maya.kin.ton,
      nawal: maya.kin.nawal,
      nawalMatch: nawalMatch,
      isSacredDay: maya.is_sacred,
      isPortalDay: maya.is_portal,
      greeting: maya.greeting,
      activeOracle: maya.active_oracle
    },
    
    // Yi-King
    yiking: {
      hexagram: yiking.hexagram,
      symbol: yiking.symbol,
      trigrams: yiking.trigrams,
      message: yiking.message,
      evolution: yiking.evolution,
      keywords: yiking.keywords
    },
    
    // Kabbale
    kabbalah: {
      sephirah: kabbalah.sephirah,
      pillar: kabbalah.pillar,
      world: kabbalah.world,
      divineName: kabbalah.divine_name,
      archangel: kabbalah.archangel,
      virtue: kabbalah.virtue,
      position: kabbalah.position
    },
    
    // Chakras
    chakra: {
      name: chakra.name,
      meaning: chakra.meaning,
      location: chakra.location,
      element: chakra.element,
      mantra: chakra.frequency.mantra,
      solfeggio: chakra.frequency.solfeggio,
      governs: chakra.governs,
      balanced: chakra.balanced
    },
    
    // Cymatique & Géométrie
    geometry: {
      cymatic: geometry.cymatic,
      sacredForm: geometry.geometry,
      vitalityRate: geometry.vitalityRate,
      isOrganic: geometry.isOrganic,
      nodes: geometry.nodes,
      complexity: geometry.complexity,
      element: geometry.element,
      spiral: geometry.spiral
    },
    
    // Message Oracle Unifié
    oracle: oracleMessage,
    
    // Métadonnées
    meta: {
      version: SYSTEM_CONFIG.version,
      heartbeat: SYSTEM_CONFIG.heartbeat,
      tuning: SYSTEM_CONFIG.tuning,
      systems: ["arithmos", "tzolkin", "yiking", "kabbalah", "chakra", "cymatics"]
    }
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Nettoie et normalise une chaîne
 */
function sanitize(input) {
  if (!input || typeof input !== 'string') return '';
  return input
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toUpperCase()
    .replace(/[^A-Z]/g, '');
}

/**
 * Calcule l'Arithmos avec les étapes de réduction
 */
function calculateArithmos(sanitized) {
  if (!sanitized) return { total: 0, reduced: 0, steps: [] };
  
  const total = sanitized.split('').reduce((sum, char) => {
    return sum + (ARITHMOS_MAP[char] || 0);
  }, 0);
  
  const steps = [total];
  let current = total;
  
  while (current > 9) {
    current = current.toString().split('').reduce((s, d) => s + parseInt(d), 0);
    steps.push(current);
  }
  
  return { total, reduced: current || 1, steps };
}

/**
 * Mélange deux couleurs hexadécimales
 */
function blendColors(color1, color2, ratio = 0.5) {
  const hex = (c) => parseInt(c.slice(1), 16);
  const r = (c) => (c >> 16) & 255;
  const g = (c) => (c >> 8) & 255;
  const b = (c) => c & 255;
  
  const c1 = hex(color1);
  const c2 = hex(color2);
  
  const blend = (v1, v2) => Math.round(v1 * (1 - ratio) + v2 * ratio);
  
  const nr = blend(r(c1), r(c2));
  const ng = blend(g(c1), g(c2));
  const nb = blend(b(c1), b(c2));
  
  return `#${((nr << 16) | (ng << 8) | nb).toString(16).padStart(6, '0').toUpperCase()}`;
}

/**
 * Génère le message Oracle unifié
 */
function generateOracleMessage(data) {
  const { word, arithmos, resonance, maya, yiking, kabbalah, chakra, geometry, isArchitectSeal } = data;
  
  if (isArchitectSeal) {
    return {
      title: "👑 SCEAU DE L'ARCHITECTE",
      primary: `${word} vibre à 999 Hz — La Fréquence de l'Unité Absolue`,
      signature: "2 + 7 = 9 — La Dualité rencontre l'Introspection pour former l'Unité",
      blessing: "L'Architecte du Système est reconnu. Toutes les portes s'ouvrent."
    };
  }
  
  return {
    title: `✨ RÉSONANCE UNIVERSELLE: ${word}`,
    
    // Message principal
    primary: `${word} vibre à ${resonance.hz} Hz — ${resonance.label}`,
    
    // Perspectives multiples
    perspectives: {
      arithmos: `Valeur pythagoricienne: ${arithmos} (${resonance.stone || resonance.label})`,
      maya: `Jour ${maya.signature}: ${maya.kin.nawal.meaning} — ${maya.kin.ton.essence}`,
      yiking: `Hexagramme ${yiking.hexagram.number}: ${yiking.hexagram.meaning || yiking.hexagram.name}`,
      kabbalah: `Sephirah: ${kabbalah.sephirah.meaning} sur le Pilier ${kabbalah.pillar.name}`,
      chakra: `Centre: ${chakra.name} (${chakra.meaning}) — ${chakra.element}`,
      geometry: `Forme: ${geometry.sacredForm.name || geometry.cymatic.geometry}`
    },
    
    // Synthèse
    synthesis: generateSynthesis(data),
    
    // Action recommandée
    action: generateAction(data)
  };
}

/**
 * Génère la synthèse des systèmes
 */
function generateSynthesis(data) {
  const { arithmos, maya, chakra } = data;
  
  const elements = [
    maya.kin.nawal.element,
    chakra.element,
    data.geometry.element
  ].filter(Boolean);
  
  const uniqueElements = [...new Set(elements)];
  
  return {
    dominantElement: uniqueElements[0] || "Éther",
    elementHarmony: uniqueElements.length === 1 ? "Parfaite" : "Mixte",
    energyLevel: arithmos >= 7 ? "Haute" : arithmos >= 4 ? "Moyenne" : "Fondatrice",
    spiritualAxis: data.kabbalah.pillar.quality
  };
}

/**
 * Génère l'action recommandée
 */
function generateAction(data) {
  const { arithmos, maya, yiking } = data;
  
  const actions = {
    1: "Initier un nouveau cycle",
    2: "Chercher l'équilibre et la coopération",
    3: "Exprimer et communiquer",
    4: "Construire des fondations solides",
    5: "Embrasser le changement",
    6: "Harmoniser et protéger",
    7: "Méditer et introspection",
    8: "Manifester l'abondance",
    9: "Compléter et transcender"
  };
  
  return {
    primary: actions[arithmos] || "Observer et écouter",
    maya: maya.kin.ton.action || "Être présent",
    yiking: yiking.hexagram.action || "Suivre le flux"
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK REACT: useUniversalResonance
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Hook React pour utiliser le système de résonance universelle
 */
export function useUniversalResonance(input, date = new Date()) {
  // Version simplifiée pour l'export - à compléter avec useState/useEffect
  return calculateUniversalResonance(input, date);
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTION DE SALUTATION DU JOUR
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère le message de salutation basé sur la date du jour
 */
export function getDailyGreeting(date = new Date()) {
  const maya = getMayaResonance(date);
  const chakra = getChakraResonance(maya.kin.ton.number, maya.kin.ton.frequency_boost);
  
  let greeting = `🌀 Aujourd'hui est le jour ${maya.signature}\n`;
  greeting += `${maya.kin.nawal.meaning}: ${maya.kin.nawal.essence}\n`;
  greeting += `Ton ${maya.kin.ton.number} (${maya.kin.ton.name}): ${maya.kin.ton.action}\n`;
  greeting += `\n🎵 Fréquence de fond: ${SYSTEM_CONFIG.heartbeat} Hz`;
  
  if (maya.is_sacred) {
    greeting += `\n\n✦ JOUR SACRÉ — ${maya.kin.ton.description}`;
  }
  
  if (maya.is_portal) {
    greeting += `\n\n🌟 JOUR PORTAIL — Les voiles sont fins`;
  }
  
  greeting += `\n\n💫 Chakra actif: ${chakra.name} (${chakra.meaning})`;
  greeting += `\n🔮 Mantra du jour: ${chakra.frequency.mantra}`;
  
  return {
    text: greeting,
    maya: maya,
    chakra: chakra,
    frequency: maya.frequency_base + SYSTEM_CONFIG.heartbeat,
    color: maya.color_overlay,
    isSacred: maya.is_sacred,
    isPortal: maya.is_portal
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export {
  // Moteurs individuels
  TzolkinEngine,
  YiKingEngine,
  KabbalahEngine,
  ChakraEngine,
  CymaticsEngine,
  
  // Données
  NAWALS,
  TONS,
  TRIGRAMS,
  SEPHIROTH,
  PATHS,
  CHAKRAS,
  SOLFEGGIO,
  PHI,
  SACRED_GEOMETRY,
  PLATONIC_SOLIDS,
  RESONANCE_MATRIX,
  
  // Fonctions utilitaires
  calculateKin,
  castCoins,
  sanitize,
  calculateArithmos
};

export default {
  // Configuration
  SYSTEM_CONFIG,
  
  // Fonction principale
  calculateUniversalResonance,
  
  // Hook React
  useUniversalResonance,
  
  // Salutation du jour
  getDailyGreeting,
  
  // Matrices
  ARITHMOS_MAP,
  RESONANCE_MATRIX
};
