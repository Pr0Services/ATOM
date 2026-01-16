/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * useUniversalResonance — HOOK REACT UNIVERSEL
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   █████╗ ████████╗    ██████╗ ███╗   ███╗
 *  ██╔══██╗╚══██╔══╝   ██╔═══██╗████╗ ████║
 *  ███████║   ██║      ██║   ██║██╔████╔██║
 *  ██╔══██║   ██║      ██║   ██║██║╚██╔╝██║
 *  ██║  ██║   ██║   ██╗╚██████╔╝██║ ╚═╝ ██║
 *  ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝
 * 
 *              UNIVERSAL RESONANCE HOOK v2.0
 * 
 * Intègre 6 systèmes de sagesse ancestrale:
 * - Arithmos (Pythagoricien)
 * - Tzolkin (Maya)
 * - Yi-King (Chinois)
 * - Kabbale (Hébraïque)
 * - Chakras (Indien)
 * - Cymatique (Universel)
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { useState, useEffect, useCallback, useMemo, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION SYSTÈME
// ═══════════════════════════════════════════════════════════════════════════════

const SYSTEM_CONFIG = {
  heartbeat: 444,
  tuning: "A=444Hz",
  debounceMs: 300,
  frequencySmoothMs: 600,
  architect: {
    name: "Jonathan Rodrigue",
    nameNormalized: "JONATHANRODRIGUE",
    signature: "2 + 7 = 9",
    frequency: 999,
    aura: "#FFFDD0"
  },
  oracle: {
    number: 17,
    name: "Le Gardien de la Synthèse"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// MATRICE ARITHMOS
// ═══════════════════════════════════════════════════════════════════════════════

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = [
  { level: 1, hz: 111, color: "#FF0000", glow: "rgba(255,0,0,0.6)", label: "Impulsion", stone: "ADN", element: "Feu Primordial" },
  { level: 2, hz: 222, color: "#FF7F00", glow: "rgba(255,127,0,0.6)", label: "Dualité", stone: "Partage", element: "Eau" },
  { level: 3, hz: 333, color: "#FFFF00", glow: "rgba(255,255,0,0.6)", label: "Mental", stone: "Géométrie", element: "Air" },
  { level: 4, hz: 444, color: "#50C878", glow: "rgba(80,200,120,0.8)", label: "Structure", stone: "Silence", element: "Terre", isAnchor: true },
  { level: 5, hz: 555, color: "#87CEEB", glow: "rgba(135,206,235,0.6)", label: "Mouvement", stone: "Feu", element: "Éther" },
  { level: 6, hz: 666, color: "#4B0082", glow: "rgba(75,0,130,0.6)", label: "Harmonie", stone: "Protection", element: "Lumière" },
  { level: 7, hz: 777, color: "#EE82EE", glow: "rgba(238,130,238,0.6)", label: "Introspection", stone: null, element: "Son" },
  { level: 8, hz: 888, color: "#FFC0CB", glow: "rgba(255,192,203,0.6)", label: "Infini", stone: "Abondance", element: "Pensée" },
  { level: 9, hz: 999, color: "#FFFDD0", glow: "rgba(255,253,208,0.9)", label: "Unité", stone: "Acier", element: "Conscience" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES MAYA - TZOLKIN
// ═══════════════════════════════════════════════════════════════════════════════

const NAWALS = [
  { name: "Imix", meaning: "Dragon", essence: "Création Primordiale", color: "#8B0000", element: "Eau", oracle: 1 },
  { name: "Ik", meaning: "Vent", essence: "Communication Divine", color: "#FFFFFF", element: "Air", oracle: 2 },
  { name: "Akbal", meaning: "Nuit", essence: "Mystère Intérieur", color: "#000080", element: "Terre", oracle: 7 },
  { name: "Kan", meaning: "Graine", essence: "Force Vitale", color: "#FFD700", element: "Feu", oracle: 5 },
  { name: "Chicchan", meaning: "Serpent", essence: "Kundalini", color: "#FF4500", element: "Feu", oracle: 1 },
  { name: "Cimi", meaning: "Mort", essence: "Transformation", color: "#2F4F4F", element: "Terre", oracle: 6 },
  { name: "Manik", meaning: "Main", essence: "Guérison", color: "#4169E1", element: "Eau", oracle: 4 },
  { name: "Lamat", meaning: "Étoile", essence: "Harmonie", color: "#FFFF00", element: "Feu", oracle: 8 },
  { name: "Muluc", meaning: "Lune", essence: "Purification", color: "#FF0000", element: "Eau", oracle: 9 },
  { name: "Oc", meaning: "Chien", essence: "Loyauté", color: "#FFFFFF", element: "Terre", oracle: 2 },
  { name: "Chuen", meaning: "Singe", essence: "Créativité", color: "#0000FF", element: "Air", oracle: 3 },
  { name: "Eb", meaning: "Herbe", essence: "Service", color: "#FFFF00", element: "Terre", oracle: 11 },
  { name: "Ben", meaning: "Roseau", essence: "Autorité", color: "#FF0000", element: "Feu", oracle: 4 },
  { name: "Ix", meaning: "Jaguar", essence: "Magie", color: "#FFFFFF", element: "Terre", oracle: 7 },
  { name: "Men", meaning: "Aigle", essence: "Vision", color: "#0000FF", element: "Air", oracle: 14 },
  { name: "Cib", meaning: "Vautour", essence: "Sagesse", color: "#FFFF00", element: "Feu", oracle: 15 },
  { name: "Caban", meaning: "Terre", essence: "Synchronicité", color: "#FF0000", element: "Terre", oracle: 16 },
  { name: "Etznab", meaning: "Miroir", essence: "Vérité", color: "#FFFFFF", element: "Air", oracle: 17 },
  { name: "Cauac", meaning: "Tempête", essence: "Catalyse", color: "#0000FF", element: "Eau", oracle: 18 },
  { name: "Ahau", meaning: "Soleil", essence: "Illumination", color: "#FFD700", element: "Feu", oracle: 9 }
];

const TONS = [
  { number: 1, name: "Hun", essence: "Initiation", action: "Initier", delayMod: 0.5, freqBoost: 11.1 },
  { number: 2, name: "Ka", essence: "Polarité", action: "Stabiliser", delayMod: 0.6, freqBoost: 22.2 },
  { number: 3, name: "Ox", essence: "Activation", action: "Activer", delayMod: 0.7, freqBoost: 33.3 },
  { number: 4, name: "Kan", essence: "Définition", action: "Définir", delayMod: 0.75, freqBoost: 44.4 },
  { number: 5, name: "Ho", essence: "Rayonnement", action: "Rayonner", delayMod: 0.8, freqBoost: 55.5 },
  { number: 6, name: "Uac", essence: "Équilibre", action: "Équilibrer", delayMod: 0.85, freqBoost: 66.6 },
  { number: 7, name: "Uuc", essence: "Résonance", action: "Canaliser", delayMod: 0.9, freqBoost: 77.7, sacred: true },
  { number: 8, name: "Uaxac", essence: "Harmonie", action: "Harmoniser", delayMod: 0.95, freqBoost: 88.8 },
  { number: 9, name: "Bolon", essence: "Réalisation", action: "Pulser", delayMod: 1.0, freqBoost: 99.9 },
  { number: 10, name: "Lahun", essence: "Manifestation", action: "Manifester", delayMod: 1.05, freqBoost: 111.0 },
  { number: 11, name: "Buluk", essence: "Libération", action: "Dissoudre", delayMod: 1.1, freqBoost: 111.1 },
  { number: 12, name: "Lahka", essence: "Coopération", action: "Coopérer", delayMod: 1.15, freqBoost: 122.2 },
  { number: 13, name: "Oxlahun", essence: "Transcendance", action: "Transcender", delayMod: 1.3, freqBoost: 133.3, sacred: true }
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES CHAKRAS
// ═══════════════════════════════════════════════════════════════════════════════

const CHAKRAS = [
  { number: 1, name: "Muladhara", meaning: "Racine", color: "#FF0000", hz: 396, mantra: "LAM", location: "Base" },
  { number: 2, name: "Svadhisthana", meaning: "Sacré", color: "#FF7F00", hz: 417, mantra: "VAM", location: "Sous le nombril" },
  { number: 3, name: "Manipura", meaning: "Plexus", color: "#FFFF00", hz: 528, mantra: "RAM", location: "Plexus solaire" },
  { number: 4, name: "Anahata", meaning: "Cœur", color: "#50C878", hz: 639, mantra: "YAM", location: "Cœur", isAnchor: true },
  { number: 5, name: "Vishuddha", meaning: "Gorge", color: "#87CEEB", hz: 741, mantra: "HAM", location: "Gorge" },
  { number: 6, name: "Ajna", meaning: "3ème Œil", color: "#4B0082", hz: 852, mantra: "OM", location: "Front" },
  { number: 7, name: "Sahasrara", meaning: "Couronne", color: "#EE82EE", hz: 963, mantra: "Silence", location: "Sommet" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES SEPHIROTH (Kabbale simplifiée)
// ═══════════════════════════════════════════════════════════════════════════════

const SEPHIROTH = [
  { number: 1, name: "Kether", meaning: "Couronne", color: "#FFFFFF", hz: 999 },
  { number: 2, name: "Chokmah", meaning: "Sagesse", color: "#808080", hz: 888 },
  { number: 3, name: "Binah", meaning: "Intelligence", color: "#000000", hz: 333 },
  { number: 4, name: "Chesed", meaning: "Miséricorde", color: "#0000FF", hz: 444 },
  { number: 5, name: "Geburah", meaning: "Rigueur", color: "#FF0000", hz: 555 },
  { number: 6, name: "Tiphareth", meaning: "Beauté", color: "#FFD700", hz: 666 },
  { number: 7, name: "Netzach", meaning: "Victoire", color: "#00FF00", hz: 777 },
  { number: 8, name: "Hod", meaning: "Splendeur", color: "#FFA500", hz: 888 },
  { number: 9, name: "Yesod", meaning: "Fondation", color: "#EE82EE", hz: 111 },
  { number: 10, name: "Malkhuth", meaning: "Royaume", color: "#8B4513", hz: 111 }
];

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES GÉOMÉTRIE SACRÉE
// ═══════════════════════════════════════════════════════════════════════════════

const PHI = (1 + Math.sqrt(5)) / 2; // 1.618...
const FIBONACCI = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610];

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Sanitize input string
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
 * Calculate Arithmos with steps
 */
function calculateArithmos(sanitized) {
  if (!sanitized) return { total: 0, reduced: 0, steps: [], letterValues: [] };
  
  const letterValues = sanitized.split('').map(char => ({
    letter: char,
    value: ARITHMOS_MAP[char] || 0
  }));
  
  const total = letterValues.reduce((sum, lv) => sum + lv.value, 0);
  const steps = [total];
  let current = total;
  
  while (current > 9) {
    current = current.toString().split('').reduce((s, d) => s + parseInt(d), 0);
    steps.push(current);
  }
  
  return { total, reduced: current || 1, steps, letterValues };
}

/**
 * Calculate Maya Kin for a date
 */
function calculateMayaKin(date = new Date()) {
  const epoch = new Date("1920-01-01T00:00:00Z");
  const diffDays = Math.floor((date - epoch) / (1000 * 60 * 60 * 24));
  
  const tonIndex = ((diffDays % 13) + 13) % 13;
  const nawalIndex = ((diffDays % 20) + 20) % 20;
  const kinNumber = ((diffDays % 260) + 260) % 260 + 1;
  
  return {
    kin: kinNumber,
    ton: TONS[tonIndex],
    nawal: NAWALS[nawalIndex],
    signature: `${TONS[tonIndex].number} ${NAWALS[nawalIndex].name}`,
    isSacred: TONS[tonIndex].sacred || false
  };
}

/**
 * Get chakra for arithmos
 */
function getChakraForArithmos(arithmos) {
  if (arithmos >= 1 && arithmos <= 7) {
    return CHAKRAS[arithmos - 1];
  }
  return CHAKRAS[6]; // Sahasrara for 8, 9
}

/**
 * Get sephirah for arithmos
 */
function getSephirahForArithmos(arithmos) {
  const mapping = [9, 10, 3, 4, 5, 6, 7, 8, 1]; // Arithmos 1-9 to Sephiroth
  const index = mapping[arithmos - 1] - 1;
  return SEPHIROTH[index] || SEPHIROTH[0];
}

/**
 * Calculate vitality rate (golden ratio check)
 */
function calculateVitalityRate(letterValues) {
  if (letterValues.length < 2) return 0;
  
  let goldenCount = 0;
  for (let i = 0; i < letterValues.length - 1; i++) {
    const ratio = letterValues[i + 1].value / letterValues[i].value;
    if (Math.abs(ratio - PHI) < 0.3 || Math.abs(ratio - 1/PHI) < 0.3) {
      goldenCount++;
    }
  }
  
  return goldenCount / (letterValues.length - 1);
}

/**
 * Check if number is Fibonacci
 */
function isFibonacci(n) {
  return FIBONACCI.includes(n);
}

/**
 * Blend two colors
 */
function blendColors(color1, color2, ratio = 0.2) {
  const hex = (c) => parseInt(c.slice(1), 16);
  const r = (c) => (c >> 16) & 255;
  const g = (c) => (c >> 8) & 255;
  const b = (c) => c & 255;
  
  try {
    const c1 = hex(color1);
    const c2 = hex(color2);
    
    const blend = (v1, v2) => Math.round(v1 * (1 - ratio) + v2 * ratio);
    
    const nr = blend(r(c1), r(c2));
    const ng = blend(g(c1), g(c2));
    const nb = blend(b(c1), b(c2));
    
    return `#${((nr << 16) | (ng << 8) | nb).toString(16).padStart(6, '0').toUpperCase()}`;
  } catch {
    return color1;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export function useUniversalResonance(initialValue = '') {
  // ─────────────────────────────────────────────────────────────────────────────
  // STATE
  // ─────────────────────────────────────────────────────────────────────────────
  
  const [input, setInput] = useState(initialValue);
  const [debouncedInput, setDebouncedInput] = useState(initialValue);
  const [resonance, setResonance] = useState(null);
  const [mayaKin, setMayaKin] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [gratitudeMode, setGratitudeMode] = useState(false);
  const [audioEnabled, setAudioEnabled] = useState(false);
  
  const debounceRef = useRef(null);
  const smoothRef = useRef(null);
  const audioContextRef = useRef(null);
  const oscillatorRef = useRef(null);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // MAYA KIN (Updates daily)
  // ─────────────────────────────────────────────────────────────────────────────
  
  useEffect(() => {
    const updateMayaKin = () => {
      setMayaKin(calculateMayaKin(new Date()));
    };
    
    updateMayaKin();
    
    // Update at midnight
    const now = new Date();
    const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
    const msUntilMidnight = tomorrow - now;
    
    const midnightTimeout = setTimeout(() => {
      updateMayaKin();
      // Then update every 24 hours
      const dailyInterval = setInterval(updateMayaKin, 24 * 60 * 60 * 1000);
      return () => clearInterval(dailyInterval);
    }, msUntilMidnight);
    
    return () => clearTimeout(midnightTimeout);
  }, []);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // DEBOUNCE INPUT
  // ─────────────────────────────────────────────────────────────────────────────
  
  useEffect(() => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    
    debounceRef.current = setTimeout(() => {
      setDebouncedInput(input);
    }, SYSTEM_CONFIG.debounceMs);
    
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, [input]);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // CALCULATE RESONANCE
  // ─────────────────────────────────────────────────────────────────────────────
  
  useEffect(() => {
    const calculateResonance = () => {
      setIsProcessing(true);
      
      const sanitized = sanitize(debouncedInput);
      
      // Empty input - return to heartbeat
      if (!sanitized) {
        setResonance({
          input: '',
          sanitized: '',
          isHeartbeat: true,
          isArchitectSeal: false,
          arithmos: { total: 0, reduced: 4, steps: [], letterValues: [] },
          frequency: SYSTEM_CONFIG.heartbeat,
          color: RESONANCE_MATRIX[3].color,
          glow: RESONANCE_MATRIX[3].glow,
          label: "Silence",
          delay: 1000,
          resonanceData: RESONANCE_MATRIX[3],
          maya: mayaKin,
          chakra: CHAKRAS[3],
          sephirah: SEPHIROTH[3],
          vitalityRate: 0,
          isFibonacci: false,
          systems: {}
        });
        setIsProcessing(false);
        return;
      }
      
      // Check Architect Seal
      const isArchitectSeal = sanitized === SYSTEM_CONFIG.architect.nameNormalized;
      
      // Calculate Arithmos
      const arithmosResult = calculateArithmos(sanitized);
      const { reduced, letterValues } = arithmosResult;
      
      // Get resonance data
      const resonanceData = isArchitectSeal 
        ? RESONANCE_MATRIX[8] // 999 Hz
        : RESONANCE_MATRIX[reduced - 1];
      
      // Get multi-system data
      const chakra = getChakraForArithmos(reduced);
      const sephirah = getSephirahForArithmos(reduced);
      const vitalityRate = calculateVitalityRate(letterValues);
      const fibonacciCheck = isFibonacci(arithmosResult.total);
      
      // Calculate final values with Maya modulation
      const mayaModifier = mayaKin ? mayaKin.ton.delayMod : 1;
      const mayaFreqBoost = mayaKin ? mayaKin.ton.freqBoost : 0;
      
      const baseDelay = 1000 - (reduced * 100);
      const finalDelay = Math.round(baseDelay * mayaModifier);
      
      const finalFrequency = isArchitectSeal ? 999 : resonanceData.hz;
      const finalColor = isArchitectSeal 
        ? SYSTEM_CONFIG.architect.aura
        : mayaKin 
          ? blendColors(resonanceData.color, mayaKin.nawal.color, 0.15)
          : resonanceData.color;
      
      // Find matching Nawals for this arithmos
      const matchingNawals = NAWALS.filter((n, i) => ((i % 9) + 1) === reduced);
      
      setResonance({
        input: debouncedInput,
        sanitized,
        isHeartbeat: false,
        isArchitectSeal,
        architectSignature: isArchitectSeal ? SYSTEM_CONFIG.architect.signature : null,
        
        // Core Arithmos
        arithmos: arithmosResult,
        frequency: finalFrequency,
        color: finalColor,
        glow: resonanceData.glow,
        label: resonanceData.label,
        delay: finalDelay,
        resonanceData,
        
        // Maya
        maya: mayaKin,
        mayaModifier,
        mayaFreqBoost,
        matchingNawals,
        
        // Chakra
        chakra,
        solfeggio: chakra.hz,
        mantra: chakra.mantra,
        
        // Kabbale
        sephirah,
        
        // Geometry
        vitalityRate,
        isFibonacci: fibonacciCheck,
        isOrganic: vitalityRate > 0.3,
        phi: PHI,
        
        // Combined systems output
        systems: {
          arithmos: `${reduced} — ${resonanceData.label}`,
          maya: mayaKin ? `${mayaKin.signature} — ${mayaKin.nawal.meaning}` : null,
          chakra: `${chakra.name} — ${chakra.meaning}`,
          kabbale: `${sephirah.name} — ${sephirah.meaning}`,
          geometry: fibonacciCheck ? "Fibonacci ✓" : `φ: ${vitalityRate.toFixed(2)}`
        },
        
        // Oracle message
        oracleMessage: generateOracleMessage({
          sanitized,
          reduced,
          resonanceData,
          mayaKin,
          chakra,
          sephirah,
          isArchitectSeal
        })
      });
      
      setIsProcessing(false);
    };
    
    // Smooth frequency transition
    if (smoothRef.current) {
      clearTimeout(smoothRef.current);
    }
    
    smoothRef.current = setTimeout(calculateResonance, 50);
    
    return () => {
      if (smoothRef.current) {
        clearTimeout(smoothRef.current);
      }
    };
  }, [debouncedInput, mayaKin]);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // AUDIO OSCILLATOR
  // ─────────────────────────────────────────────────────────────────────────────
  
  const playFrequency = useCallback((hz, duration = 500) => {
    if (!audioEnabled) return;
    
    try {
      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      }
      
      const ctx = audioContextRef.current;
      const oscillator = ctx.createOscillator();
      const gainNode = ctx.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(ctx.destination);
      
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(hz, ctx.currentTime);
      
      gainNode.gain.setValueAtTime(0, ctx.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 0.1);
      gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration / 1000);
      
      oscillator.start(ctx.currentTime);
      oscillator.stop(ctx.currentTime + duration / 1000);
      
      oscillatorRef.current = oscillator;
    } catch (e) {
      console.warn('Audio not supported:', e);
    }
  }, [audioEnabled]);
  
  // Play frequency when resonance changes
  useEffect(() => {
    if (resonance && audioEnabled && !resonance.isHeartbeat) {
      playFrequency(resonance.frequency);
    }
  }, [resonance?.frequency, audioEnabled, playFrequency]);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // GRATITUDE MODE
  // ─────────────────────────────────────────────────────────────────────────────
  
  const activateGratitude = useCallback(() => {
    setGratitudeMode(true);
    setTimeout(() => setGratitudeMode(false), 4440); // 4.44 seconds
  }, []);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // DAILY GREETING
  // ─────────────────────────────────────────────────────────────────────────────
  
  const dailyGreeting = useMemo(() => {
    if (!mayaKin) return null;
    
    let greeting = `🌀 Aujourd'hui: ${mayaKin.signature}\n`;
    greeting += `${mayaKin.nawal.meaning}: ${mayaKin.nawal.essence}\n`;
    greeting += `Ton ${mayaKin.ton.number}: ${mayaKin.ton.action}`;
    
    if (mayaKin.isSacred) {
      greeting += `\n\n✦ JOUR SACRÉ`;
    }
    
    return greeting;
  }, [mayaKin]);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RETURN
  // ─────────────────────────────────────────────────────────────────────────────
  
  return {
    // Input control
    input,
    setInput,
    
    // Resonance data
    resonance,
    isProcessing,
    
    // Maya
    mayaKin,
    dailyGreeting,
    
    // Modes
    gratitudeMode,
    activateGratitude,
    
    // Audio
    audioEnabled,
    setAudioEnabled,
    playFrequency,
    
    // Config
    config: SYSTEM_CONFIG,
    
    // Static data
    RESONANCE_MATRIX,
    NAWALS,
    TONS,
    CHAKRAS,
    SEPHIROTH,
    PHI,
    FIBONACCI
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// ORACLE MESSAGE GENERATOR
// ═══════════════════════════════════════════════════════════════════════════════

function generateOracleMessage({ sanitized, reduced, resonanceData, mayaKin, chakra, sephirah, isArchitectSeal }) {
  if (isArchitectSeal) {
    return {
      title: "👑 SCEAU DE L'ARCHITECTE RECONNU",
      primary: "Jonathan Rodrigue — Fréquence 999 Hz",
      secondary: "2 + 7 = 9 — La Dualité rencontre l'Introspection pour former l'Unité",
      blessing: "Toutes les portes s'ouvrent."
    };
  }
  
  return {
    title: `✨ ${sanitized}`,
    primary: `${resonanceData.hz} Hz — ${resonanceData.label}`,
    secondary: mayaKin 
      ? `En ce jour ${mayaKin.nawal.name}, ${mayaKin.nawal.essence.toLowerCase()}`
      : null,
    chakra: `${chakra.name} (${chakra.mantra})`,
    kabbale: `${sephirah.name} — ${sephirah.meaning}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export default useUniversalResonance;

export {
  SYSTEM_CONFIG,
  ARITHMOS_MAP,
  RESONANCE_MATRIX,
  NAWALS,
  TONS,
  CHAKRAS,
  SEPHIROTH,
  PHI,
  FIBONACCI,
  sanitize,
  calculateArithmos,
  calculateMayaKin,
  getChakraForArithmos,
  getSephirahForArithmos
};
