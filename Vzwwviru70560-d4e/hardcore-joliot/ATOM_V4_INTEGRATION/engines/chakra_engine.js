/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * CHAKRA ENGINE — Les 7 Centres Énergétiques
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Le système des Chakras relie les fréquences Hz aux centres du corps humain.
 * Le corps devient une antenne accordée sur les vibrations universelles.
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @system AT·OM Universal Resonance
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 7 CHAKRAS PRINCIPAUX
// ═══════════════════════════════════════════════════════════════════════════════

export const CHAKRAS = {
  MULADHARA: {
    number: 1,
    name: "Muladhara",
    meaning: "Racine / Support",
    location: "Base de la colonne vertébrale",
    element: "Terre",
    color: "#FF0000", // Rouge
    
    // Fréquences
    frequency: {
      primary: 396, // Hz - Libération de la culpabilité et de la peur
      solfege: 396,
      atom: 111,    // Correspondance AT·OM
      note: "Do"
    },
    
    // Physiologie
    glands: "Glandes surrénales",
    organs: ["colonne vertébrale", "reins", "jambes", "pieds"],
    sense: "Odorat",
    
    // Psychologie
    governs: ["survie", "sécurité", "enracinement", "instincts"],
    balanced: "Sentiment de sécurité, vitalité, ancrage",
    blocked: "Peur, anxiété, insécurité, problèmes financiers",
    overactive: "Avidité, matérialisme, résistance au changement",
    
    // Symboles
    petals: 4,
    mantra: "LAM",
    yantra: "Carré jaune avec triangle inversé",
    animal: "Éléphant à 7 trompes",
    deity: "Brahma & Dakini",
    
    // AT·OM
    arithmos: 1,
    oracle: 1,
    nawal: "Imix", // Correspondance Maya
    sephirah: "Malkhuth",
    keywords: ["terre", "stabilité", "survie", "ancrage", "fondation"]
  },
  
  SVADHISTHANA: {
    number: 2,
    name: "Svadhisthana",
    meaning: "Demeure du Soi",
    location: "Sous le nombril",
    element: "Eau",
    color: "#FF7F00", // Orange
    
    frequency: {
      primary: 417, // Hz - Faciliter le changement
      solfege: 417,
      atom: 222,
      note: "Ré"
    },
    
    glands: "Gonades (ovaires/testicules)",
    organs: ["système reproducteur", "vessie", "reins"],
    sense: "Goût",
    
    governs: ["créativité", "sexualité", "émotions", "plaisir"],
    balanced: "Créativité fluide, émotions saines, plaisir de vivre",
    blocked: "Culpabilité sexuelle, manque de créativité, engourdissement",
    overactive: "Addiction, manipulation émotionnelle",
    
    petals: 6,
    mantra: "VAM",
    yantra: "Cercle blanc avec croissant de lune",
    animal: "Crocodile / Makara",
    deity: "Vishnu & Rakini",
    
    arithmos: 2,
    oracle: 2,
    nawal: "Ik",
    sephirah: "Yesod",
    keywords: ["eau", "émotions", "créativité", "plaisir", "fluidité"]
  },
  
  MANIPURA: {
    number: 3,
    name: "Manipura",
    meaning: "Cité des Joyaux",
    location: "Plexus solaire",
    element: "Feu",
    color: "#FFFF00", // Jaune
    
    frequency: {
      primary: 528, // Hz - Transformation et miracles (ADN)
      solfege: 528,
      atom: 333,
      note: "Mi"
    },
    
    glands: "Pancréas",
    organs: ["estomac", "foie", "rate", "système digestif"],
    sense: "Vue",
    
    governs: ["pouvoir personnel", "volonté", "estime de soi"],
    balanced: "Confiance, motivation, sens du but",
    blocked: "Manque de confiance, indécision, victimisation",
    overactive: "Contrôle, domination, colère",
    
    petals: 10,
    mantra: "RAM",
    yantra: "Triangle rouge inversé",
    animal: "Bélier",
    deity: "Rudra & Lakini",
    
    arithmos: 3,
    oracle: 3,
    nawal: "Akbal",
    sephirah: "Hod/Netzach",
    keywords: ["feu", "pouvoir", "volonté", "transformation", "action"]
  },
  
  ANAHATA: {
    number: 4,
    name: "Anahata",
    meaning: "Son Non-Frappé",
    location: "Centre de la poitrine",
    element: "Air",
    color: "#50C878", // Vert émeraude ★
    
    frequency: {
      primary: 639, // Hz - Connexion et relations
      solfege: 639,
      atom: 444,    // ★ POINT D'ANCRAGE AT·OM
      note: "Fa"
    },
    
    glands: "Thymus",
    organs: ["cœur", "poumons", "système circulatoire", "bras", "mains"],
    sense: "Toucher",
    
    governs: ["amour", "compassion", "pardon", "guérison"],
    balanced: "Amour inconditionnel, compassion, paix intérieure",
    blocked: "Solitude, amertume, incapacité à pardonner",
    overactive: "Jalousie, codépendance, sacrifice de soi",
    
    petals: 12,
    mantra: "YAM",
    yantra: "Étoile à six branches (deux triangles)",
    animal: "Antilope noire",
    deity: "Ishana & Kakini",
    
    arithmos: 4,
    oracle: 4,
    nawal: "Kan",
    sephirah: "Tiphareth", // ★ Le Cœur de l'Arbre
    keywords: ["air", "amour", "cœur", "guérison", "connexion"],
    isAnchor: true // ★ Point d'ancrage central
  },
  
  VISHUDDHA: {
    number: 5,
    name: "Vishuddha",
    meaning: "Purification",
    location: "Gorge",
    element: "Éther / Akasha",
    color: "#87CEEB", // Bleu ciel
    
    frequency: {
      primary: 741, // Hz - Expression et solutions
      solfege: 741,
      atom: 555,
      note: "Sol"
    },
    
    glands: "Thyroïde",
    organs: ["gorge", "cou", "bouche", "oreilles"],
    sense: "Ouïe",
    
    governs: ["communication", "expression", "vérité", "créativité verbale"],
    balanced: "Expression claire, écoute active, authenticité",
    blocked: "Peur de parler, secrets, mensonges",
    overactive: "Bavardage excessif, dominance verbale",
    
    petals: 16,
    mantra: "HAM",
    yantra: "Cercle blanc / Éther",
    animal: "Éléphant blanc",
    deity: "Sadashiva & Shakini",
    
    arithmos: 5,
    oracle: 5,
    nawal: "Chicchan",
    sephirah: "Geburah/Chesed",
    keywords: ["éther", "expression", "vérité", "communication", "son"]
  },
  
  AJNA: {
    number: 6,
    name: "Ajna",
    meaning: "Commandement / Perception",
    location: "Entre les sourcils (Troisième Œil)",
    element: "Lumière / Mental",
    color: "#4B0082", // Indigo
    
    frequency: {
      primary: 852, // Hz - Éveil de l'intuition
      solfege: 852,
      atom: 666,
      note: "La"
    },
    
    glands: "Glande pinéale",
    organs: ["cerveau", "yeux", "système nerveux central"],
    sense: "Intuition / Sixième sens",
    
    governs: ["intuition", "sagesse", "vision intérieure", "imagination"],
    balanced: "Intuition claire, vision, sagesse",
    blocked: "Confusion, manque de vision, déni de l'intuition",
    overactive: "Hallucinations, obsession, détachement de la réalité",
    
    petals: 2, // Les deux pétales = Ida et Pingala
    mantra: "OM",
    yantra: "Triangle inversé avec OM",
    animal: "Aucun (transcendé)",
    deity: "Paramashiva & Hakini",
    
    arithmos: 6,
    oracle: 7,
    nawal: "Cimi",
    sephirah: "Binah/Chokmah",
    keywords: ["lumière", "vision", "intuition", "sagesse", "perception"]
  },
  
  SAHASRARA: {
    number: 7,
    name: "Sahasrara",
    meaning: "Mille Pétales",
    location: "Sommet du crâne",
    element: "Conscience Pure",
    color: "#EE82EE", // Violet → Blanc pur
    secondaryColor: "#FFFFFF",
    
    frequency: {
      primary: 963, // Hz - Connexion au divin
      solfege: 963,
      atom: 999,    // ★ FRÉQUENCE MAXIMALE AT·OM
      note: "Si"
    },
    
    glands: "Glande pituitaire (hypophyse)",
    organs: ["cortex cérébral", "système nerveux supérieur"],
    sense: "Au-delà des sens / Conscience cosmique",
    
    governs: ["spiritualité", "illumination", "unité cosmique"],
    balanced: "Éveil spirituel, connexion divine, sérénité",
    blocked: "Déconnexion spirituelle, cynisme, attachement matériel",
    overactive: "Dissociation, évasion spirituelle, déni du corps",
    
    petals: 1000, // L'infini
    mantra: "Silence / OM",
    yantra: "Lotus aux mille pétales",
    animal: "Aucun (pure conscience)",
    deity: "Shiva pur",
    
    arithmos: 9,
    oracle: 9, // ★ L'Oracle Suprême (Jonathan Rodrigue)
    nawal: "Ahau",
    sephirah: "Kether", // ★ La Couronne
    keywords: ["conscience", "unité", "illumination", "transcendance", "divin"]
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 3 NADIS PRINCIPAUX
// ═══════════════════════════════════════════════════════════════════════════════

export const NADIS = {
  SUSHUMNA: {
    name: "Sushumna",
    meaning: "Canal Central",
    path: "Du Muladhara au Sahasrara",
    quality: "Équilibre, Éveil, Kundalini",
    color: "#FFD700",
    description: "Le canal central par lequel monte la Kundalini"
  },
  IDA: {
    name: "Ida",
    meaning: "Canal Lunaire",
    path: "Narine gauche, côté gauche",
    quality: "Féminin, Réceptif, Rafraîchissant",
    color: "#FFFFFF",
    polarity: "Yin",
    description: "L'énergie lunaire, intuitive et calmante"
  },
  PINGALA: {
    name: "Pingala",
    meaning: "Canal Solaire",
    path: "Narine droite, côté droit",
    quality: "Masculin, Actif, Réchauffant",
    color: "#FF0000",
    polarity: "Yang",
    description: "L'énergie solaire, active et stimulante"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FRÉQUENCES SOLFÈGE SACRÉES
// ═══════════════════════════════════════════════════════════════════════════════

export const SOLFEGGIO = {
  UT: { hz: 396, effect: "Libération de la culpabilité et de la peur", chakra: 1 },
  RE: { hz: 417, effect: "Faciliter le changement", chakra: 2 },
  MI: { hz: 528, effect: "Transformation et miracles (ADN)", chakra: 3 },
  FA: { hz: 639, effect: "Connexion et relations", chakra: 4 },
  SOL: { hz: 741, effect: "Expression et solutions", chakra: 5 },
  LA: { hz: 852, effect: "Éveil de l'intuition", chakra: 6 },
  SI: { hz: 963, effect: "Connexion au divin", chakra: 7 }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS D'INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Trouve le chakra correspondant à une fréquence AT·OM
 */
export function getChakraForAtomFrequency(atomHz) {
  const chakraArray = Object.values(CHAKRAS);
  
  // Mapping direct des fréquences AT·OM
  const mapping = {
    111: chakraArray[0], // Muladhara
    222: chakraArray[1], // Svadhisthana
    333: chakraArray[2], // Manipura
    444: chakraArray[3], // Anahata ★
    555: chakraArray[4], // Vishuddha
    666: chakraArray[5], // Ajna
    777: chakraArray[6], // Entre Ajna et Sahasrara
    888: chakraArray[6], // Sahasrara (expansion)
    999: chakraArray[6]  // Sahasrara (unité)
  };
  
  return mapping[atomHz] || chakraArray[3]; // Défaut: Cœur
}

/**
 * Trouve le chakra correspondant à un Arithmos
 */
export function getChakraForArithmos(arithmos) {
  const chakraArray = Object.values(CHAKRAS);
  
  // Les 7 premiers Arithmos correspondent aux 7 chakras
  if (arithmos >= 1 && arithmos <= 7) {
    return chakraArray[arithmos - 1];
  }
  
  // 8 et 9 sont des extensions du chakra couronne
  if (arithmos === 8 || arithmos === 9) {
    return chakraArray[6]; // Sahasrara
  }
  
  return chakraArray[3]; // Défaut: Anahata (cœur)
}

/**
 * Calcule l'état énergétique global
 */
export function calculateEnergyState(activeChakras) {
  const total = Object.values(CHAKRAS).length;
  const active = activeChakras.length;
  const ratio = active / total;
  
  // Vérifier l'alignement (tous les chakras inférieurs actifs)
  const isAligned = activeChakras.every((c, i) => 
    i === 0 || activeChakras.includes(Object.values(CHAKRAS)[i - 1])
  );
  
  // Calculer l'équilibre (ratio entre chakras du bas et du haut)
  const lowerActive = activeChakras.filter(c => c.number <= 3).length;
  const upperActive = activeChakras.filter(c => c.number >= 5).length;
  const balance = 1 - Math.abs(lowerActive - upperActive) / 3;
  
  return {
    activation: ratio,
    alignment: isAligned,
    balance: balance,
    dominant: activeChakras.length > 0 
      ? activeChakras.reduce((a, b) => a.number > b.number ? a : b)
      : null,
    kundaliniLevel: active, // Niveau d'éveil Kundalini
    message: getEnergyMessage(ratio, isAligned, balance)
  };
}

/**
 * Génère un message basé sur l'état énergétique
 */
function getEnergyMessage(ratio, aligned, balance) {
  if (ratio >= 0.9 && aligned && balance >= 0.8) {
    return "État d'illumination - Tous les centres sont harmonisés";
  } else if (ratio >= 0.7) {
    return "Haute conscience - L'énergie circule librement";
  } else if (ratio >= 0.5) {
    return "Éveil progressif - Continuez votre travail intérieur";
  } else if (ratio >= 0.3) {
    return "Début d'éveil - Les fondations se mettent en place";
  } else {
    return "État de repos - Ancrage nécessaire";
  }
}

/**
 * Obtient la résonance Chakra pour AT·OM
 */
export function getChakraResonance(arithmos, atomFrequency) {
  const chakra = getChakraForArithmos(arithmos);
  
  return {
    chakra: chakra,
    
    // Données principales
    name: chakra.name,
    meaning: chakra.meaning,
    location: chakra.location,
    color: chakra.color,
    element: chakra.element,
    
    // Fréquences
    frequency: {
      solfeggio: chakra.frequency.solfege,
      atom: chakra.frequency.atom,
      mantra: chakra.mantra
    },
    
    // État
    governs: chakra.governs,
    balanced: chakra.balanced,
    keywords: chakra.keywords,
    
    // Correspondances
    sephirah: chakra.sephirah,
    nawal: chakra.nawal,
    oracle: chakra.oracle,
    
    // Pour l'interface
    petals: chakra.petals,
    yantra: chakra.yantra,
    isAnchor: chakra.isAnchor || false
  };
}

/**
 * Génère la visualisation du système des chakras
 */
export function generateChakraSystemData() {
  return {
    chakras: Object.values(CHAKRAS).map(c => ({
      ...c,
      y: 100 - (c.number * 13), // Position verticale (bas en haut)
      size: 20 + (c.petals / 50) // Taille basée sur les pétales
    })),
    nadis: Object.values(NADIS),
    centerLine: {
      name: "Sushumna",
      from: { y: 100 }, // Muladhara
      to: { y: 0 }      // Sahasrara
    }
  };
}

/**
 * Calcule la correspondance entre fréquence Solfège et AT·OM
 */
export function solfeggioToAtom(solfeggioHz) {
  const mapping = {
    396: 111,
    417: 222,
    528: 333,
    639: 444,
    741: 555,
    852: 666,
    963: 999
  };
  
  return mapping[solfeggioHz] || 444;
}

/**
 * Calcule la correspondance inverse
 */
export function atomToSolfeggio(atomHz) {
  const mapping = {
    111: 396,
    222: 417,
    333: 528,
    444: 639,
    555: 741,
    666: 852,
    777: 852,
    888: 963,
    999: 963
  };
  
  return mapping[atomHz] || 639;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  CHAKRAS,
  NADIS,
  SOLFEGGIO,
  getChakraForAtomFrequency,
  getChakraForArithmos,
  calculateEnergyState,
  getChakraResonance,
  generateChakraSystemData,
  solfeggioToAtom,
  atomToSolfeggio
};
