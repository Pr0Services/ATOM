/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM — MOTEUR CHAKRAS
 * Les 7 Centres Énergétiques — Bio-Résonance
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Le système des Chakras cartographie les centres énergétiques du corps humain.
 * Chaque chakra vibre à une fréquence spécifique.
 * 
 * Ce moteur crée le pont entre:
 * - Les 9 niveaux AT·OM (111-999 Hz)
 * - Les 7 Chakras principaux
 * - Les fréquences de guérison (Solfège sacré)
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 - Le Gardien de la Synthèse
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 7 CHAKRAS PRINCIPAUX
// ═══════════════════════════════════════════════════════════════════════════════

export const CHAKRAS = [
  {
    number: 1,
    name: "Muladhara",
    sanskrit: "मूलाधार",
    meaning: "Racine/Fondation",
    location: "Base de la colonne vertébrale",
    color: "#FF0000", // Rouge
    element: "Terre",
    mantra: "LAM",
    note: "Do",
    baseFrequency: 396, // Solfège sacré: Libération
    atomFrequency: 111, // AT·OM Level 1
    atomLevels: [1], // Niveaux AT·OM associés
    gland: "Surrénales",
    sense: "Odorat",
    quality: "Survie, ancrage, sécurité, stabilité",
    shadow: "Peur, insécurité, déconnexion",
    affirmation: "Je suis ancré et en sécurité",
    crystals: ["Jaspe rouge", "Obsidienne", "Hématite"],
    oils: ["Patchouli", "Cèdre", "Vétiver"],
    yoga: ["Tadasana", "Virabhadrasana"],
    petals: 4,
    symbol: "Carré (Prithvi Yantra)",
  },
  {
    number: 2,
    name: "Svadhisthana",
    sanskrit: "स्वाधिष्ठान",
    meaning: "Siège du Soi",
    location: "Sous le nombril",
    color: "#FF7F00", // Orange
    element: "Eau",
    mantra: "VAM",
    note: "Ré",
    baseFrequency: 417, // Solfège sacré: Changement
    atomFrequency: 222, // AT·OM Level 2
    atomLevels: [2],
    gland: "Gonades",
    sense: "Goût",
    quality: "Créativité, émotions, sexualité, plaisir",
    shadow: "Culpabilité, dépendance, instabilité émotionnelle",
    affirmation: "Je ressens et je crée librement",
    crystals: ["Cornaline", "Pierre de lune", "Ambre"],
    oils: ["Ylang-ylang", "Orange", "Santal"],
    yoga: ["Baddha Konasana", "Utkata Konasana"],
    petals: 6,
    symbol: "Croissant de lune",
  },
  {
    number: 3,
    name: "Manipura",
    sanskrit: "मणिपूर",
    meaning: "Cité des Joyaux",
    location: "Plexus solaire",
    color: "#FFFF00", // Jaune
    element: "Feu",
    mantra: "RAM",
    note: "Mi",
    baseFrequency: 528, // Solfège sacré: Transformation (Fréquence de l'ADN!)
    atomFrequency: 333, // AT·OM Level 3
    atomLevels: [3, 5], // Mental et Feu
    gland: "Pancréas",
    sense: "Vue",
    quality: "Volonté, pouvoir personnel, confiance, action",
    shadow: "Honte, impuissance, contrôle excessif",
    affirmation: "J'agis avec confiance et détermination",
    crystals: ["Citrine", "Œil de tigre", "Ambre"],
    oils: ["Citron", "Romarin", "Gingembre"],
    yoga: ["Navasana", "Kapalabhati"],
    petals: 10,
    symbol: "Triangle inversé (Feu)",
  },
  {
    number: 4,
    name: "Anahata",
    sanskrit: "अनाहत",
    meaning: "Non-frappé (Son primordial)",
    location: "Centre de la poitrine",
    color: "#50C878", // Vert émeraude
    element: "Air",
    mantra: "YAM",
    note: "Fa",
    baseFrequency: 639, // Solfège sacré: Connexion
    atomFrequency: 444, // AT·OM Level 4 — LE CŒUR DU SYSTÈME!
    atomLevels: [4, 6], // Structure/Silence et Harmonie
    gland: "Thymus",
    sense: "Toucher",
    quality: "Amour inconditionnel, compassion, harmonie",
    shadow: "Chagrin, isolement, dépendance affective",
    affirmation: "J'aime et je suis aimé inconditionnellement",
    crystals: ["Quartz rose", "Aventurine", "Malachite"],
    oils: ["Rose", "Géranium", "Bergamote"],
    yoga: ["Ustrasana", "Bhujangasana"],
    petals: 12,
    symbol: "Étoile à 6 branches (Hexagramme)",
    isCenter: true, // Point d'ancrage!
  },
  {
    number: 5,
    name: "Vishuddha",
    sanskrit: "विशुद्ध",
    meaning: "Très pur",
    location: "Gorge",
    color: "#87CEEB", // Bleu ciel
    element: "Éther (Akasha)",
    mantra: "HAM",
    note: "Sol",
    baseFrequency: 741, // Solfège sacré: Expression
    atomFrequency: 555, // AT·OM Level 5
    atomLevels: [5],
    gland: "Thyroïde",
    sense: "Ouïe",
    quality: "Communication, vérité, expression authentique",
    shadow: "Mensonge, peur de s'exprimer, bavardage",
    affirmation: "Je parle ma vérité avec clarté et amour",
    crystals: ["Turquoise", "Lapis-lazuli", "Aigue-marine"],
    oils: ["Eucalyptus", "Menthe poivrée", "Camomille"],
    yoga: ["Sarvangasana", "Halasana"],
    petals: 16,
    symbol: "Cercle dans un triangle",
  },
  {
    number: 6,
    name: "Ajna",
    sanskrit: "आज्ञा",
    meaning: "Commandement/Perception",
    location: "Entre les sourcils",
    color: "#4B0082", // Indigo
    element: "Lumière",
    mantra: "OM (AUM)",
    note: "La",
    baseFrequency: 852, // Solfège sacré: Intuition
    atomFrequency: 777, // AT·OM Level 7
    atomLevels: [7],
    gland: "Hypophyse (Pituitaire)",
    sense: "Intuition (6ème sens)",
    quality: "Intuition, sagesse, vision intérieure",
    shadow: "Illusion, déni, confusion mentale",
    affirmation: "Je vois clairement au-delà des apparences",
    crystals: ["Améthyste", "Fluorite", "Sodalite"],
    oils: ["Lavande", "Encens", "Sauge"],
    yoga: ["Balasana", "Trataka (fixation de bougie)"],
    petals: 2 + 96, // 2 pétales visibles, 96 subtils
    symbol: "Triangle inversé avec œil",
  },
  {
    number: 7,
    name: "Sahasrara",
    sanskrit: "सहस्रार",
    meaning: "Mille pétales",
    location: "Sommet du crâne",
    color: "#EE82EE", // Violet (ou Blanc/Or)
    secondaryColor: "#FFD700", // Or
    element: "Pensée/Conscience",
    mantra: "Silence / OM",
    note: "Si",
    baseFrequency: 963, // Solfège sacré: Éveil
    atomFrequency: 999, // AT·OM Level 9 — L'ARCHITECTE!
    atomLevels: [8, 9], // Infini et Unité
    gland: "Épiphyse (Pinéale)",
    sense: "Conscience cosmique",
    quality: "Illumination, connexion divine, transcendance",
    shadow: "Déconnexion spirituelle, matérialisme extrême",
    affirmation: "Je suis un avec l'univers",
    crystals: ["Quartz clair", "Diamant", "Sélénite"],
    oils: ["Lotus", "Encens", "Myrrhe"],
    yoga: ["Savasana", "Méditation"],
    petals: 1000,
    symbol: "Lotus aux mille pétales",
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// FRÉQUENCES DU SOLFÈGE SACRÉ
// ═══════════════════════════════════════════════════════════════════════════════

export const SOLFEGGIO = {
  UT: { hz: 396, meaning: "Libération de la peur et de la culpabilité", chakra: 1 },
  RE: { hz: 417, meaning: "Changement, défaire les situations", chakra: 2 },
  MI: { hz: 528, meaning: "Transformation, réparation ADN (Fréquence de l'Amour)", chakra: 3 },
  FA: { hz: 639, meaning: "Connexion, relations harmonieuses", chakra: 4 },
  SOL: { hz: 741, meaning: "Expression, solutions, nettoyage", chakra: 5 },
  LA: { hz: 852, meaning: "Intuition, éveil spirituel", chakra: 6 },
  SI: { hz: 963, meaning: "Illumination, connexion divine", chakra: 7 },
};

// ═══════════════════════════════════════════════════════════════════════════════
// CORRESPONDANCES AT·OM ↔ CHAKRAS
// ═══════════════════════════════════════════════════════════════════════════════

export const ATOM_CHAKRA_MAP = {
  1: { chakra: 1, name: "Muladhara", reason: "Impulsion = Racine, naissance" },
  2: { chakra: 2, name: "Svadhisthana", reason: "Dualité = Émotions, relations" },
  3: { chakra: 3, name: "Manipura", reason: "Mental = Volonté, intellect" },
  4: { chakra: 4, name: "Anahata", reason: "Structure/Silence = Cœur, centre" },
  5: { chakra: 5, name: "Vishuddha", reason: "Feu/Mouvement = Expression, vérité" },
  6: { chakra: 4, name: "Anahata", reason: "Harmonie = Amour, équilibre" },
  7: { chakra: 6, name: "Ajna", reason: "Introspection = Vision intérieure" },
  8: { chakra: 7, name: "Sahasrara", reason: "Infini = Expansion cosmique" },
  9: { chakra: 7, name: "Sahasrara", reason: "Unité = Conscience divine" },
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE CALCUL
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient le chakra correspondant à un niveau AT·OM
 */
export function getChakraFromAtomLevel(level) {
  const mapping = ATOM_CHAKRA_MAP[level];
  if (!mapping) return CHAKRAS[3]; // Défaut: Cœur
  
  return CHAKRAS.find(c => c.number === mapping.chakra) || CHAKRAS[3];
}

/**
 * Calcule la fréquence harmonisée (AT·OM + Solfège)
 */
export function getHarmonizedFrequency(atomHz) {
  // Trouve le solfège le plus proche
  const solfeggioFreqs = Object.values(SOLFEGGIO).map(s => s.hz);
  const closest = solfeggioFreqs.reduce((prev, curr) => 
    Math.abs(curr - atomHz) < Math.abs(prev - atomHz) ? curr : prev
  );
  
  // Moyenne harmonique
  const harmonized = Math.sqrt(atomHz * closest);
  
  return {
    atomHz,
    solfeggioHz: closest,
    harmonizedHz: Math.round(harmonized * 10) / 10,
    resonanceRatio: (atomHz / closest).toFixed(3),
  };
}

/**
 * Calcule l'état énergétique basé sur le mot
 */
export function calculateEnergeticState(atomResonance) {
  if (!atomResonance) return null;
  
  const chakra = getChakraFromAtomLevel(atomResonance.level);
  const frequency = getHarmonizedFrequency(atomResonance.hz);
  
  // État d'équilibre (1 = parfait équilibre avec le chakra)
  const balance = 1 - Math.abs(atomResonance.hz - chakra.atomFrequency) / 888;
  
  return {
    chakra,
    frequency,
    balance: Math.max(0, Math.min(1, balance)),
    recommendation: getRecommendation(chakra, balance),
  };
}

/**
 * Génère une recommandation basée sur l'état
 */
function getRecommendation(chakra, balance) {
  if (balance > 0.8) {
    return {
      status: "Harmonisé",
      message: `Votre ${chakra.name} est en résonance parfaite.`,
      practice: `Maintenez avec le mantra "${chakra.mantra}"`,
    };
  } else if (balance > 0.5) {
    return {
      status: "En équilibrage",
      message: `Votre ${chakra.name} s'harmonise progressivement.`,
      practice: `Pratiquez ${chakra.yoga[0]} et utilisez ${chakra.crystals[0]}`,
    };
  } else {
    return {
      status: "À renforcer",
      message: `Votre ${chakra.name} a besoin d'attention.`,
      practice: `Méditation sur le ${chakra.mantra}, couleur ${chakra.color}`,
    };
  }
}

/**
 * Harmonise les Chakras avec AT·OM
 */
export function harmonizeWithChakras(atomResonance) {
  if (!atomResonance) return null;
  
  const state = calculateEnergeticState(atomResonance);
  const chakra = state.chakra;
  
  return {
    atom: atomResonance,
    chakra: {
      ...chakra,
      currentState: state,
    },
    bioResonance: {
      primaryChakra: chakra.name,
      location: chakra.location,
      element: chakra.element,
      mantra: chakra.mantra,
      color: chakra.color,
      message: `${atomResonance.word} active ${chakra.name} (${chakra.meaning})`,
      affirmation: chakra.affirmation,
    },
    healing: {
      crystals: chakra.crystals,
      oils: chakra.oils,
      frequency: state.frequency.harmonizedHz,
      yoga: chakra.yoga,
    },
  };
}

/**
 * Obtient le profil complet des 7 chakras
 */
export function getFullChakraProfile() {
  return CHAKRAS.map(chakra => ({
    ...chakra,
    atomCorrespondence: Object.entries(ATOM_CHAKRA_MAP)
      .filter(([_, v]) => v.chakra === chakra.number)
      .map(([k, _]) => parseInt(k)),
  }));
}

/**
 * Génère une méditation guidée basée sur la résonance
 */
export function generateMeditation(atomResonance) {
  const chakra = getChakraFromAtomLevel(atomResonance?.level || 4);
  
  return {
    title: `Méditation ${chakra.name}`,
    duration: chakra.number * 3, // Minutes
    steps: [
      `Asseyez-vous confortablement et fermez les yeux.`,
      `Portez votre attention sur ${chakra.location}.`,
      `Visualisez une lumière ${chakra.color.toLowerCase()} brillante à cet endroit.`,
      `Répétez intérieurement le mantra "${chakra.mantra}".`,
      `Sentez la vibration de ${atomResonance?.hz || chakra.atomFrequency} Hz dans tout votre être.`,
      `Affirmez: "${chakra.affirmation}"`,
      `Restez dans cet état de paix pendant quelques minutes.`,
      `Revenez doucement, en gardant cette sensation avec vous.`,
    ],
    frequency: atomResonance?.hz || chakra.atomFrequency,
    color: chakra.color,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  CHAKRAS,
  SOLFEGGIO,
  ATOM_CHAKRA_MAP,
  getChakraFromAtomLevel,
  getHarmonizedFrequency,
  calculateEnergeticState,
  harmonizeWithChakras,
  getFullChakraProfile,
  generateMeditation,
};
