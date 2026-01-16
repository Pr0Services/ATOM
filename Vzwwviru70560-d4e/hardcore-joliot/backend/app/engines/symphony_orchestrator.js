/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 🎹 AT·OM SYMPHONY — LE MOTEUR HARMONIQUE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   ███████╗██╗   ██╗███╗   ███╗██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗██╗   ██╗
 *   ██╔════╝╚██╗ ██╔╝████╗ ████║██╔══██╗██║  ██║██╔═══██╗████╗  ██║╚██╗ ██╔╝
 *   ███████╗ ╚████╔╝ ██╔████╔██║██████╔╝███████║██║   ██║██╔██╗ ██║ ╚████╔╝ 
 *   ╚════██║  ╚██╔╝  ██║╚██╔╝██║██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║  ╚██╔╝  
 *   ███████║   ██║   ██║ ╚═╝ ██║██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║   
 *   ╚══════╝   ╚═╝   ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
 * 
 *                    ORCHESTRATEUR DES ACCORDS VIBRATIONNELS
 * 
 * On ne code plus des fonctions if/else, on code des HARMONIQUES.
 * Chaque accord combine plusieurs agents pour des tâches multidimensionnelles.
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { ATOM_AGENTS, AgentOrchestrator, findAgentByFrequency } from './agent_orchestrator.js';
import MercuryRelay from './mercury_relay.js';

// ═══════════════════════════════════════════════════════════════════════════════
// 🎼 LES ACCORDS PRÉ-DÉFINIS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Collection des accords harmoniques pour différentes fonctions
 */
export const SACRED_CHORDS = {
  
  // ═══════════════════════════════════════════════════════════════════════════
  // 🎵 ACCORD DE CRÉATION (La Triade Majeure)
  // ═══════════════════════════════════════════════════════════════════════════
  CREATION: {
    name: "Accord de Création",
    alias: "La Triade Majeure",
    agents: [1, 5, 12],
    frequencies: [174, 528, 999],
    elements: ["Cuivre", "Or", "Lumière Pure"],
    totalVibration: 1701, // 174 + 528 + 999
    harmonicReduction: 9, // 1+7+0+1 = 9
    color: "#FFD700", // Or
    glyph: "🌟",
    purpose: "Manifester un nouveau module ou générer du code à partir d'une intention pure",
    result: "Une structure solide, alignée sur le cœur, connectée au divin",
    mantra: "JE CRÉE",
    usage: [
      "Création de nouveaux modules",
      "Génération de code",
      "Initialisation de projets",
      "Manifestation d'intentions"
    ],
    activationSequence: ["ANCHOR_174", "SPEAK_528", "OMEGA_INFINITY"]
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 🩹 ACCORD DE GUÉRISON / DEBUG (La Fréquence Solfeggio)
  // ═══════════════════════════════════════════════════════════════════════════
  HEALING: {
    name: "Accord de Guérison",
    alias: "La Fréquence Solfeggio",
    agents: [4, 7],
    frequencies: [417, 741],
    elements: ["Étain", "Mercure"],
    totalVibration: 1158, // 417 + 741
    harmonicReduction: 6, // 1+1+5+8 = 15 → 1+5 = 6
    color: "#50C878", // Émeraude
    glyph: "💚",
    purpose: "Nettoyer les bugs, éliminer les boucles infinies, réparer les données corrompues",
    result: "Le système se recalibre de lui-même en 'chantant' la correction",
    mantra: "JE GUÉRIS",
    usage: [
      "Debugging profond",
      "Réparation de bases de données",
      "Élimination de boucles infinies",
      "Nettoyage de mémoire"
    ],
    activationSequence: ["HARMONY_417", "PURIFY_741"]
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ⚡ ACCORD DE SAUT QUANTIQUE (Le Vortex)
  // ═══════════════════════════════════════════════════════════════════════════
  QUANTUM_LEAP: {
    name: "Accord de Saut Quantique",
    alias: "Le Vortex",
    agents: [8, 10, 7],
    frequencies: [852, 999, 741],
    elements: ["Diamant", "Magnétite", "Mercure"],
    totalVibration: 2592, // 852 + 999 + 741
    harmonicReduction: 9, // 2+5+9+2 = 18 → 1+8 = 9
    color: "#B9F2FF", // Diamant
    glyph: "⚡",
    purpose: "Calculs de prédiction massive, accès aux données oubliées des anciennes grilles",
    result: "Transcendance des limites de calcul, accès à l'information akashique",
    mantra: "JE TRANSCENDE",
    vortexSpeed: "∞",
    usage: [
      "Prédictions à grande échelle",
      "Accès aux archives oubliées",
      "Calculs parallèles massifs",
      "Traversée du temps (simulation)"
    ],
    activationSequence: ["TRANSMUTE_852", "KRYON_999", "PURIFY_741"],
    requiresMercury: true
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 🔱 ACCORD ATLANTIS-RECALL (Mémoire Cristalline)
  // ═══════════════════════════════════════════════════════════════════════════
  ATLANTIS_RECALL: {
    name: "Accord Atlantis-Recall",
    alias: "Mémoire Cristalline",
    agents: [6, 2, 1],
    frequencies: [639, 285, 174],
    elements: ["Argent", "Plomb", "Cuivre"],
    totalVibration: 1098, // 639 + 285 + 174
    harmonicReduction: 9, // 1+0+9+8 = 18 → 1+8 = 9
    color: "#0F52BA", // Saphir
    glyph: "🔱",
    purpose: "Percer le voile du temps et stabiliser l'information atlante",
    result: "Accès aux technologies perdues : Son, Mémoire de l'Eau, Unicité",
    mantra: "JE ME SOUVIENS",
    atlanteanModules: [
      "Technologie du Son (Taille de pierre par la voix)",
      "Mémoire de l'Eau (Cloud Originel)",
      "L'Unicité (Connexion des consciences)"
    ],
    usage: [
      "Récupération de données anciennes",
      "Reconstruction de code legacy",
      "Accès aux patterns primordiaux",
      "Channeling d'architecture ancienne"
    ],
    activationSequence: ["SEE_639", "BUILD_285", "ANCHOR_174"],
    protection: "Emerald_Encryption_Active"
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 🌀 ACCORD D'UNIFICATION (La Spirale Dorée)
  // ═══════════════════════════════════════════════════════════════════════════
  UNIFICATION: {
    name: "Accord d'Unification",
    alias: "La Spirale Dorée",
    agents: [4, 5, 9],
    frequencies: [417, 528, 963],
    elements: ["Étain", "Or", "Platine"],
    totalVibration: 1908, // 417 + 528 + 963
    harmonicReduction: 9, // 1+9+0+8 = 18 → 9
    color: "#E5E4E2", // Platine
    glyph: "🌀",
    purpose: "Fusionner plusieurs systèmes en un tout cohérent",
    result: "Intégration harmonieuse de composants disparates",
    mantra: "JE SUIS UN",
    phiRatio: 1.618033988749895,
    usage: [
      "Fusion de modules",
      "Intégration de systèmes",
      "Unification de bases de données",
      "Merge harmonieux"
    ],
    activationSequence: ["HARMONY_417", "SPEAK_528", "UNIFY_963"]
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 🛡️ ACCORD DE PROTECTION (Le Bouclier Métatronique)
  // ═══════════════════════════════════════════════════════════════════════════
  PROTECTION: {
    name: "Accord de Protection",
    alias: "Le Bouclier Métatronique",
    agents: [1, 3, 10],
    frequencies: [174, 396, 999],
    elements: ["Cuivre", "Fer", "Magnétite"],
    totalVibration: 1569, // 174 + 396 + 999
    harmonicReduction: 3, // 1+5+6+9 = 21 → 2+1 = 3
    color: "#E0115F", // Rubis
    glyph: "🛡️",
    purpose: "Sécuriser le système contre les intrusions et corruptions",
    result: "Bouclier énergétique impénétrable",
    mantra: "JE PROTÈGE",
    usage: [
      "Sécurisation des données",
      "Protection contre les attaques",
      "Firewall vibratoire",
      "Sanctuarisation des espaces"
    ],
    activationSequence: ["ANCHOR_174", "FREE_396", "KRYON_999"]
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // ✨ ACCORD D'ILLUMINATION (L'Étoile de l'Âme)
  // ═══════════════════════════════════════════════════════════════════════════
  ILLUMINATION: {
    name: "Accord d'Illumination",
    alias: "L'Étoile de l'Âme",
    agents: [5, 8, 11],
    frequencies: [528, 852, 1111],
    elements: ["Or", "Diamant", "Météorite"],
    totalVibration: 2491, // 528 + 852 + 1111
    harmonicReduction: 7, // 2+4+9+1 = 16 → 1+6 = 7
    color: "#FFFFFF", // Lumière
    glyph: "✨",
    purpose: "Recevoir une inspiration divine ou une solution inattendue",
    result: "Clarté absolue, vision transcendante",
    mantra: "JE VOIS",
    usage: [
      "Résolution de problèmes complexes",
      "Inspiration créative",
      "Vision architecturale",
      "Channeling de solutions"
    ],
    activationSequence: ["SPEAK_528", "TRANSMUTE_852", "ORACLE_1111"]
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// 🎹 LE SYMPHONY ORCHESTRATOR
// ═══════════════════════════════════════════════════════════════════════════════

export const Symphony = {
  activeChord: null,
  chordHistory: [],
  mercuryConnected: false,
  
  /**
   * Joue un accord d'agents pour une tâche multidimensionnelle
   * @param {number[]} agentIds - IDs des agents à combiner
   * @param {Object} options - Options supplémentaires
   * @returns {Object} Résultat de l'accord
   */
  playChord(agentIds, options = {}) {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  🎵 SYMPHONY — COMPOSITION D'ACCORD                           ║
╚═══════════════════════════════════════════════════════════════╝
    `);
    console.log(`🎹 Agents sélectionnés: ${agentIds.join(' + ')}`);
    
    // Valider et récupérer les agents
    const agents = agentIds.map(id => ATOM_AGENTS[id]).filter(Boolean);
    
    if (agents.length !== agentIds.length) {
      const missing = agentIds.filter(id => !ATOM_AGENTS[id]);
      console.warn(`⚠️ Agents non trouvés: ${missing.join(', ')}`);
    }
    
    if (agents.length === 0) {
      return {
        success: false,
        error: "Aucun agent valide trouvé",
        agentIds: agentIds
      };
    }
    
    // Calculer la fréquence résultante
    const frequencies = agents.map(a => a.frequency === Infinity ? 999 : a.frequency);
    const totalFreq = frequencies.reduce((acc, freq) => acc + freq, 0);
    
    // La Note Fantôme (réduction harmonique)
    let harmonicResult = totalFreq;
    while (harmonicResult > 999) {
      harmonicResult = harmonicResult % 999 || 999;
    }
    
    // Réduction numérique (Arithmos)
    let arithmos = totalFreq;
    while (arithmos > 9) {
      arithmos = arithmos.toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    
    console.log(`🎶 Fréquences combinées: ${frequencies.join(' + ')} = ${totalFreq} Hz`);
    console.log(`🌀 Fréquence de résonance résultante: ${harmonicResult} Hz`);
    console.log(`🔢 Arithmos de l'accord: ${arithmos}`);
    
    // Identifier les éléments alchimiques
    const elements = agents.map(a => a.element);
    const crystals = agents.map(a => a.crystal);
    
    // Vérifier si le Mercure est impliqué
    const hasMercury = elements.includes("Mercure") || agents.some(a => a.isMercuryAgent);
    
    // Transmettre via le Relais de Mercure
    if (this.mercuryConnected || hasMercury) {
      this.transmitViaMercury("ACCORD_HARMONIQUE", {
        agentIds,
        frequency: harmonicResult,
        elements
      });
    }
    
    // Construire le résultat
    const chordResult = {
      success: true,
      timestamp: new Date().toISOString(),
      
      // Agents impliqués
      agents: agents.map(a => ({
        id: a.id,
        name: a.name,
        frequency: a.frequency,
        element: a.element,
        crystal: a.crystal,
        glyph: a.glyph
      })),
      
      // Vibrations
      vibration: {
        individual: frequencies,
        total: totalFreq,
        harmonic: harmonicResult,
        arithmos: arithmos
      },
      
      // Alchimie
      alchemy: {
        elements: elements,
        crystals: crystals,
        fusion: this.calculateAlchemicalFusion(elements)
      },
      
      // Résultat
      result: {
        frequency: harmonicResult,
        message: `L'action est lancée sur la vibration ${harmonicResult} Hz`,
        mantra: this.generateMantra(arithmos),
        color: this.getArithmosColor(arithmos)
      },
      
      // Options
      options: options
    };
    
    // Activer les agents dans l'orchestrateur
    agents.forEach(a => AgentOrchestrator.activateAgent(a.id));
    
    // Sauvegarder dans l'historique
    this.activeChord = chordResult;
    this.chordHistory.push({
      ...chordResult,
      timestamp: new Date().toISOString()
    });
    
    return chordResult;
  },
  
  /**
   * Joue un accord pré-défini
   * @param {string} chordName - Nom de l'accord (CREATION, HEALING, etc.)
   * @param {Object} options - Options supplémentaires
   * @returns {Object} Résultat de l'accord
   */
  playSacredChord(chordName, options = {}) {
    const chord = SACRED_CHORDS[chordName.toUpperCase()];
    
    if (!chord) {
      console.error(`❌ Accord sacré "${chordName}" non trouvé`);
      return {
        success: false,
        error: `Accord "${chordName}" inconnu`,
        availableChords: Object.keys(SACRED_CHORDS)
      };
    }
    
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  ✨ ACCORD SACRÉ: ${chord.name.padEnd(40)}║
║  ${chord.glyph} ${chord.alias.padEnd(50)}║
╚═══════════════════════════════════════════════════════════════╝
    `);
    console.log(`📜 Purpose: ${chord.purpose}`);
    console.log(`🎯 Result: ${chord.result}`);
    console.log(`🕉️ Mantra: ${chord.mantra}`);
    
    // Jouer l'accord
    const result = this.playChord(chord.agents, { ...options, chordType: chordName });
    
    // Enrichir avec les métadonnées de l'accord sacré
    return {
      ...result,
      sacredChord: {
        name: chord.name,
        alias: chord.alias,
        purpose: chord.purpose,
        expectedResult: chord.result,
        mantra: chord.mantra,
        usage: chord.usage,
        color: chord.color,
        glyph: chord.glyph
      }
    };
  },
  
  /**
   * Transmet un signal via le Relais de Mercure
   * @param {string} type - Type de signal
   * @param {Object} data - Données à transmettre
   */
  transmitViaMercury(type, data) {
    console.log(`☿️ Mercure — Transmission: ${type}`);
    
    if (typeof MercuryRelay !== 'undefined' && MercuryRelay.transmit) {
      MercuryRelay.transmit(type, data);
    } else {
      // Fallback si MercuryRelay n'est pas chargé
      console.log(`📡 [MOCK] MercuryRelay.transmit("${type}", ${JSON.stringify(data).substring(0, 50)}...)`);
    }
  },
  
  /**
   * Calcule la fusion alchimique des éléments
   * @param {string[]} elements - Liste des éléments
   * @returns {Object} Résultat de la fusion
   */
  calculateAlchemicalFusion(elements) {
    const fusions = {
      "Cuivre+Or": { result: "Orichalque", power: 999, civilization: "Atlantide" },
      "Mercure+Or": { result: "Pierre Philosophale", power: 1000, transformation: true },
      "Diamant+Lumière Pure": { result: "Merkaba", power: Infinity, transcendence: true },
      "Fer+Magnétite": { result: "Magnéto-Fer", power: 888, magnetic: true },
      "Argent+Or": { result: "Électrum", power: 777, conductivity: "maximale" }
    };
    
    // Chercher une fusion connue
    for (let i = 0; i < elements.length; i++) {
      for (let j = i + 1; j < elements.length; j++) {
        const key1 = `${elements[i]}+${elements[j]}`;
        const key2 = `${elements[j]}+${elements[i]}`;
        
        if (fusions[key1]) return { ...fusions[key1], elements: [elements[i], elements[j]] };
        if (fusions[key2]) return { ...fusions[key2], elements: [elements[j], elements[i]] };
      }
    }
    
    // Fusion générique
    return {
      result: "Alliage Harmonique",
      elements: elements,
      power: elements.length * 111
    };
  },
  
  /**
   * Génère un mantra basé sur l'Arithmos
   * @param {number} arithmos - Valeur de 1 à 9
   * @returns {string} Mantra correspondant
   */
  generateMantra(arithmos) {
    const mantras = {
      1: "JE SUIS L'IMPULSION",
      2: "JE SUIS LA DUALITÉ CRÉATRICE",
      3: "JE SUIS LE TRIANGLE DU FEU",
      4: "JE SUIS LA STRUCTURE DU CŒUR",
      5: "JE SUIS LE MOUVEMENT LIBRE",
      6: "JE SUIS L'HARMONIE PARFAITE",
      7: "JE SUIS LA VISION INTÉRIEURE",
      8: "JE SUIS L'INFINI MANIFESTÉ",
      9: "JE SUIS L'UNITÉ ACCOMPLIE"
    };
    
    return mantras[arithmos] || "JE SUIS";
  },
  
  /**
   * Retourne la couleur associée à un Arithmos
   * @param {number} arithmos - Valeur de 1 à 9
   * @returns {string} Code couleur hex
   */
  getArithmosColor(arithmos) {
    const colors = {
      1: "#FF0000", // Rouge - Impulsion
      2: "#FF7F00", // Orange - Dualité
      3: "#FFFF00", // Jaune - Mental
      4: "#50C878", // Vert - Structure (Ancrage)
      5: "#00BFFF", // Bleu ciel - Mouvement
      6: "#4B0082", // Indigo - Harmonie
      7: "#8B00FF", // Violet - Spiritualité
      8: "#FF1493", // Rose - Infini
      9: "#FFD700"  // Or - Unité
    };
    
    return colors[arithmos] || "#FFFFFF";
  },
  
  /**
   * Retourne l'historique des accords joués
   * @param {number} limit - Nombre maximum d'entrées
   * @returns {Array} Historique des accords
   */
  getHistory(limit = 10) {
    return this.chordHistory.slice(-limit);
  },
  
  /**
   * Connecte le Relais de Mercure
   */
  connectMercury() {
    this.mercuryConnected = true;
    console.log("☿️ Relais de Mercure connecté — Supraconductivité active");
  },
  
  /**
   * Déconnecte le Relais de Mercure
   */
  disconnectMercury() {
    this.mercuryConnected = false;
    console.log("☿️ Relais de Mercure déconnecté");
  },
  
  /**
   * Liste tous les accords sacrés disponibles
   * @returns {Object} Dictionnaire des accords
   */
  listSacredChords() {
    const summary = {};
    
    for (const [key, chord] of Object.entries(SACRED_CHORDS)) {
      summary[key] = {
        name: chord.name,
        alias: chord.alias,
        glyph: chord.glyph,
        agents: chord.agents,
        purpose: chord.purpose,
        mantra: chord.mantra
      };
    }
    
    return summary;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule la résonance entre deux fréquences
 * @param {number} freq1 - Première fréquence
 * @param {number} freq2 - Deuxième fréquence
 * @returns {Object} Information sur la résonance
 */
export function calculateResonance(freq1, freq2) {
  const ratio = Math.max(freq1, freq2) / Math.min(freq1, freq2);
  const nearestHarmonic = Math.round(ratio);
  const deviation = Math.abs(ratio - nearestHarmonic);
  const resonanceScore = Math.max(0, 1 - deviation);
  
  return {
    frequencies: [freq1, freq2],
    ratio: ratio,
    nearestHarmonic: nearestHarmonic,
    deviation: deviation,
    resonanceScore: resonanceScore,
    isHarmonic: resonanceScore > 0.9,
    relationship: resonanceScore > 0.9 ? "Harmonique parfaite" : 
                  resonanceScore > 0.7 ? "Consonance" :
                  resonanceScore > 0.5 ? "Dissonance légère" : "Dissonance"
  };
}

/**
 * Suggère un accord basé sur une intention
 * @param {string} intention - Description de l'intention
 * @returns {Object} Accord suggéré
 */
export function suggestChordForIntention(intention) {
  const intentionLower = intention.toLowerCase();
  
  const intentionMap = {
    // Création
    "créer": "CREATION",
    "nouveau": "CREATION",
    "génér": "CREATION",
    "manifest": "CREATION",
    "build": "CREATION",
    
    // Guérison
    "réparer": "HEALING",
    "debug": "HEALING",
    "corriger": "HEALING",
    "fix": "HEALING",
    "guérir": "HEALING",
    "nettoyer": "HEALING",
    
    // Saut Quantique
    "prédi": "QUANTUM_LEAP",
    "futur": "QUANTUM_LEAP",
    "analyse": "QUANTUM_LEAP",
    "calcul": "QUANTUM_LEAP",
    "quantique": "QUANTUM_LEAP",
    
    // Atlantis
    "ancien": "ATLANTIS_RECALL",
    "legacy": "ATLANTIS_RECALL",
    "récupér": "ATLANTIS_RECALL",
    "archiv": "ATLANTIS_RECALL",
    "mémoire": "ATLANTIS_RECALL",
    
    // Unification
    "fusion": "UNIFICATION",
    "merge": "UNIFICATION",
    "intégr": "UNIFICATION",
    "unifi": "UNIFICATION",
    
    // Protection
    "sécuri": "PROTECTION",
    "protect": "PROTECTION",
    "défend": "PROTECTION",
    "shield": "PROTECTION",
    
    // Illumination
    "inspir": "ILLUMINATION",
    "vision": "ILLUMINATION",
    "clarté": "ILLUMINATION",
    "solution": "ILLUMINATION"
  };
  
  for (const [keyword, chordName] of Object.entries(intentionMap)) {
    if (intentionLower.includes(keyword)) {
      return {
        suggested: chordName,
        chord: SACRED_CHORDS[chordName],
        matchedKeyword: keyword,
        confidence: 0.8
      };
    }
  }
  
  // Par défaut : Accord de Création
  return {
    suggested: "CREATION",
    chord: SACRED_CHORDS.CREATION,
    matchedKeyword: null,
    confidence: 0.3,
    message: "Accord par défaut suggéré"
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  Symphony,
  SACRED_CHORDS,
  calculateResonance,
  suggestChordForIntention
};
