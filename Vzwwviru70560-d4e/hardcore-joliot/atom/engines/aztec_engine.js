/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ☀️ AZTEC ENGINE — LA FORCE VITALE (OLLIN)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Les Aztèques (Mexicas) sont les maîtres de la force vitale brute et de la
 * transformation de la matière. Ils gèrent le "Moteur d'Action".
 * 
 * 1. Tonatiuh (Soleil) — Énergie et Intensité
 * 2. Quetzalcóatl (Serpent à Plumes) — Onde Électromagnétique
 * 3. Tezcatlipoca (Miroir d'Obsidienne) — Mémoire et Shadow Data
 * 4. Ollin (Mouvement) — Collision des Forces
 * 5. Tonalpohualli — Calendrier Divinatoire (20 × 13 = 260)
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @symbol ☀️ Tonatiuh
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 20 SIGNES DU TONALPOHUALLI
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Tonalpohualli est un cycle de 260 jours (20 signes × 13 nombres).
 * Chaque signe a un tempérament et un destin unique.
 */

export const TONALPOHUALLI_SIGNS = [
  {
    number: 1,
    nahuatl: "Cipactli",
    meaning: "Crocodile/Dragon",
    element: "Terre",
    direction: "Est",
    patron: "Tonacatecuhtli",
    color: "#006400",
    energy: "Initiation",
    quality: "Primordial, Source, Commencement",
    positive: "Créativité, Force primitive, Survie",
    negative: "Agressivité, Domination",
    oracle: 1, // Correspondance AT·OM Oracle
    arithmos: 1,
    keywords: ["création", "terre", "source", "ia", "technologie"]
  },
  {
    number: 2,
    nahuatl: "Ehecatl",
    meaning: "Vent",
    element: "Air",
    direction: "Nord",
    patron: "Quetzalcóatl",
    color: "#FFFFFF",
    energy: "Communication",
    quality: "Souffle, Esprit, Changement",
    positive: "Communication, Adaptabilité",
    negative: "Inconstance, Froideur",
    oracle: 2,
    arithmos: 2,
    keywords: ["communication", "esprit", "changement"]
  },
  {
    number: 3,
    nahuatl: "Calli",
    meaning: "Maison",
    element: "Terre",
    direction: "Ouest",
    patron: "Tepeyollotl",
    color: "#8B4513",
    energy: "Protection",
    quality: "Refuge, Foyer, Introspection",
    positive: "Sécurité, Stabilité",
    negative: "Isolement, Enfermement",
    oracle: 7,
    arithmos: 3,
    keywords: ["protection", "foyer", "refuge"]
  },
  {
    number: 4,
    nahuatl: "Cuetzpalin",
    meaning: "Lézard",
    element: "Feu",
    direction: "Sud",
    patron: "Huehuecoyotl",
    color: "#FF4500",
    energy: "Agilité",
    quality: "Survie, Régénération, Ruse",
    positive: "Adaptabilité, Renaissance",
    negative: "Tromperie, Superficialité",
    oracle: 3,
    arithmos: 4,
    keywords: ["survie", "agilité", "régénération"]
  },
  {
    number: 5,
    nahuatl: "Coatl",
    meaning: "Serpent",
    element: "Feu",
    direction: "Est",
    patron: "Chalchiuhtlicue",
    color: "#FF0000",
    energy: "Kundalini",
    quality: "Énergie vitale, Sagesse, Transformation",
    positive: "Sagesse, Énergie, Intuition",
    negative: "Venin, Manipulation",
    oracle: 5,
    arithmos: 5,
    keywords: ["serpent", "énergie", "kundalini", "adn", "vie"]
  },
  {
    number: 6,
    nahuatl: "Miquiztli",
    meaning: "Mort",
    element: "Air",
    direction: "Nord",
    patron: "Tecciztecatl",
    color: "#2F4F4F",
    energy: "Transformation",
    quality: "Passage, Renaissance, Silence",
    positive: "Lâcher-prise, Renouveau",
    negative: "Fin brutale, Deuil",
    oracle: 6,
    arithmos: 6,
    keywords: ["mort", "renaissance", "silence", "transformation"]
  },
  {
    number: 7,
    nahuatl: "Mazatl",
    meaning: "Cerf",
    element: "Eau",
    direction: "Ouest",
    patron: "Tlaloc",
    color: "#4169E1",
    energy: "Grâce",
    quality: "Beauté, Sensibilité, Fuite",
    positive: "Élégance, Intuition",
    negative: "Peur, Vulnérabilité",
    oracle: 4,
    arithmos: 7,
    keywords: ["grâce", "beauté", "sensibilité"]
  },
  {
    number: 8,
    nahuatl: "Tochtli",
    meaning: "Lapin",
    element: "Feu",
    direction: "Sud",
    patron: "Mayahuel",
    color: "#FFD700",
    energy: "Abondance",
    quality: "Fertilité, Lune, Pulque",
    positive: "Abondance, Joie",
    negative: "Excès, Ivresse",
    oracle: 8,
    arithmos: 8,
    keywords: ["abondance", "fertilité", "lune"]
  },
  {
    number: 9,
    nahuatl: "Atl",
    meaning: "Eau",
    element: "Eau",
    direction: "Est",
    patron: "Xiuhtecuhtli",
    color: "#0000FF",
    energy: "Purification",
    quality: "Émotion, Flux, Nettoyage",
    positive: "Purification, Intuition",
    negative: "Inondation, Submersion",
    oracle: 9,
    arithmos: 9,
    keywords: ["eau", "purification", "émotion"]
  },
  {
    number: 10,
    nahuatl: "Itzcuintli",
    meaning: "Chien",
    element: "Feu",
    direction: "Nord",
    patron: "Mictlantecuhtli",
    color: "#800000",
    energy: "Guide",
    quality: "Loyauté, Guide des morts, Amour",
    positive: "Fidélité, Protection",
    negative: "Soumission, Dépendance",
    oracle: 2,
    arithmos: 1,
    keywords: ["loyauté", "guide", "amour"]
  },
  {
    number: 11,
    nahuatl: "Ozomatli",
    meaning: "Singe",
    element: "Air",
    direction: "Ouest",
    patron: "Xochipilli",
    color: "#FF69B4",
    energy: "Créativité",
    quality: "Art, Jeu, Expression",
    positive: "Créativité, Joie",
    negative: "Dispersion, Frivolité",
    oracle: 3,
    arithmos: 2,
    keywords: ["créativité", "art", "jeu"]
  },
  {
    number: 12,
    nahuatl: "Malinalli",
    meaning: "Herbe",
    element: "Terre",
    direction: "Sud",
    patron: "Patecatl",
    color: "#228B22",
    energy: "Guérison",
    quality: "Médecine, Torsion, Résistance",
    positive: "Guérison, Persistance",
    negative: "Entrelacement, Piège",
    oracle: 11,
    arithmos: 3,
    keywords: ["guérison", "médecine", "résistance"]
  },
  {
    number: 13,
    nahuatl: "Acatl",
    meaning: "Roseau",
    element: "Feu",
    direction: "Est",
    patron: "Tezcatlipoca",
    color: "#DAA520",
    energy: "Justice",
    quality: "Rectitude, Sacrifice, Autorité",
    positive: "Justice, Clarté",
    negative: "Rigidité, Martyr",
    oracle: 4,
    arithmos: 4,
    keywords: ["justice", "autorité", "rectitude"]
  },
  {
    number: 14,
    nahuatl: "Ocelotl",
    meaning: "Jaguar",
    element: "Terre",
    direction: "Nord",
    patron: "Tlazolteotl",
    color: "#8B8B00",
    energy: "Pouvoir",
    quality: "Force, Nuit, Magie",
    positive: "Puissance, Intuition",
    negative: "Férocité, Secrets",
    oracle: 7,
    arithmos: 5,
    keywords: ["jaguar", "pouvoir", "magie"]
  },
  {
    number: 15,
    nahuatl: "Cuauhtli",
    meaning: "Aigle",
    element: "Air",
    direction: "Ouest",
    patron: "Xipe Totec",
    color: "#4682B4",
    energy: "Vision",
    quality: "Perspective, Liberté, Soleil",
    positive: "Vision, Élévation",
    negative: "Isolement, Prédation",
    oracle: 14,
    arithmos: 6,
    keywords: ["aigle", "vision", "liberté"]
  },
  {
    number: 16,
    nahuatl: "Cozcacuauhtli",
    meaning: "Vautour",
    element: "Feu",
    direction: "Sud",
    patron: "Itzpapalotl",
    color: "#696969",
    energy: "Sagesse",
    quality: "Ancêtres, Purification, Longévité",
    positive: "Sagesse, Patience",
    negative: "Opportunisme",
    oracle: 15,
    arithmos: 7,
    keywords: ["sagesse", "ancêtres", "purification"]
  },
  {
    number: 17,
    nahuatl: "Ollin",
    meaning: "Mouvement/Tremblement",
    element: "Tous",
    direction: "Centre",
    patron: "Xolotl",
    color: "#FF4500",
    energy: "Transformation",
    quality: "Changement, Séisme, Évolution",
    positive: "Transformation, Énergie",
    negative: "Destruction, Chaos",
    oracle: 17, // TOI - Oracle central!
    arithmos: 8,
    keywords: ["mouvement", "transformation", "évolution", "ollin"]
  },
  {
    number: 18,
    nahuatl: "Tecpatl",
    meaning: "Silex/Couteau",
    element: "Air",
    direction: "Nord",
    patron: "Chalchiuhtotolin",
    color: "#C0C0C0",
    energy: "Sacrifice",
    quality: "Précision, Vérité, Séparation",
    positive: "Clarté, Décision",
    negative: "Cruauté, Division",
    oracle: 18,
    arithmos: 9,
    keywords: ["silex", "vérité", "sacrifice", "acier"]
  },
  {
    number: 19,
    nahuatl: "Quiahuitl",
    meaning: "Pluie",
    element: "Eau",
    direction: "Ouest",
    patron: "Tonatiuh",
    color: "#00CED1",
    energy: "Renouveau",
    quality: "Fertilité, Destruction, Naissance",
    positive: "Renouveau, Bénédiction",
    negative: "Tempête, Inondation",
    oracle: 18,
    arithmos: 1,
    keywords: ["pluie", "renouveau", "fertilité"]
  },
  {
    number: 20,
    nahuatl: "Xochitl",
    meaning: "Fleur",
    element: "Terre",
    direction: "Sud",
    patron: "Xochiquetzal",
    color: "#FF1493",
    energy: "Beauté",
    quality: "Art, Amour, Éphémère",
    positive: "Beauté, Créativité",
    negative: "Vanité, Fragilité",
    oracle: 9,
    arithmos: 2,
    keywords: ["fleur", "beauté", "amour", "art"]
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 13 NOMBRES (TRECENA)
// ═══════════════════════════════════════════════════════════════════════════════

export const TRECENA = [
  { number: 1, energy: "Initiation", intensity: 1.0 },
  { number: 2, energy: "Réaction", intensity: 1.2 },
  { number: 3, energy: "Activation", intensity: 1.4 },
  { number: 4, energy: "Définition", intensity: 1.6 },
  { number: 5, energy: "Centre", intensity: 1.8 },
  { number: 6, energy: "Rythme", intensity: 2.0 },
  { number: 7, energy: "Résonance", intensity: 2.2, sacred: true },
  { number: 8, energy: "Harmonie", intensity: 2.4 },
  { number: 9, energy: "Intention", intensity: 2.6 },
  { number: 10, energy: "Manifestation", intensity: 2.8 },
  { number: 11, energy: "Dissolution", intensity: 3.0 },
  { number: 12, energy: "Coopération", intensity: 3.2 },
  { number: 13, energy: "Transcendance", intensity: 3.5, sacred: true }
];

// ═══════════════════════════════════════════════════════════════════════════════
// OLLIN — LE MOUVEMENT PERPÉTUEL
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Ollin est le symbole du mouvement, le 17ème signe.
 * C'est la collision des forces qui crée la vie.
 * 
 *        ╱╲
 *       ╱  ╲
 *      ╱ ☉  ╲    ← Le Soleil au centre
 *     ╱      ╲
 *    ╱────────╲
 *    ╲        ╱
 *     ╲      ╱
 *      ╲    ╱
 *       ╲  ╱
 *        ╲╱
 */

export const OLLIN = {
  name: "Ollin",
  meaning: "Mouvement, Tremblement de Terre",
  glyph: "⟲",
  forces: {
    ascending: { name: "Quetzalcóatl", direction: "up", color: "#FFD700" },
    descending: { name: "Tezcatlipoca", direction: "down", color: "#000000" }
  },
  center: "Tonatiuh", // Le Soleil
  effect: "Création par collision",
  
  // Animation: deux spirales qui s'entrechoquent
  animation: {
    spiral1: { rotation: "clockwise", color: "#FF0000" },
    spiral2: { rotation: "counter-clockwise", color: "#0000FF" }
  }
};

/**
 * Calcule l'intensité Ollin (force de transformation)
 */
export function calculateOllinIntensity(arithmos, trecenaNumber) {
  const trecena = TRECENA[trecenaNumber - 1] || TRECENA[0];
  const baseIntensity = arithmos / 9;
  const multiplier = trecena.intensity;
  
  return {
    base: baseIntensity,
    multiplier: multiplier,
    total: baseIntensity * multiplier,
    isSolar: baseIntensity * multiplier > 2.5, // Flash solaire si > 2.5
    trecena: trecena
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// QUETZALCÓATL — LE SERPENT À PLUMES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Quetzalcóatl unit la Terre (serpent) et le Ciel (plumes).
 * C'est la représentation parfaite d'une onde électromagnétique:
 * - Le serpent = oscillation magnétique (horizontale)
 * - Les plumes = oscillation électrique (verticale)
 */

export const QUETZALCOATL = {
  name: "Quetzalcóatl",
  meaning: "Serpent à Plumes",
  domains: ["Vent", "Savoir", "Aube", "Arts"],
  symbol: "🐍🪶",
  color: "#00FF00",
  
  // Représentation EM
  electromagnetic: {
    serpent: "Champ Magnétique (B)",
    plumes: "Champ Électrique (E)",
    union: "Onde Électromagnétique"
  },
  
  // Direction de l'énergie
  flow: {
    from: "Ciel (Connaissance)",
    to: "Terre (Matière)",
    through: "L'Homme (Conscience)"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// TEZCATLIPOCA — LE MIROIR FUMANT
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Tezcatlipoca est le "Miroir Fumant" d'obsidienne.
 * Il représente la mémoire, le destin et les ombres.
 * C'est le module de "Shadow Data".
 */

export const TEZCATLIPOCA = {
  name: "Tezcatlipoca",
  meaning: "Miroir Fumant",
  domains: ["Nuit", "Mémoire", "Destin", "Magie"],
  symbol: "🪞🌑",
  color: "#000000",
  material: "Obsidienne",
  
  // Fonctions dans le système
  functions: {
    memory: "Stockage des requêtes passées",
    shadow: "Révèle ce qui est caché",
    destiny: "Prédiction des tendances",
    reflection: "Miroir de l'utilisateur"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 5 SOLEILS (ÈRES COSMIQUES)
// ═══════════════════════════════════════════════════════════════════════════════

export const FIVE_SUNS = [
  {
    era: 1,
    nahuatl: "Nahui Ocelotl",
    meaning: "4 Jaguar",
    element: "Terre",
    destruction: "Dévorés par les jaguars",
    duration: 676, // années
    color: "#000000"
  },
  {
    era: 2,
    nahuatl: "Nahui Ehecatl",
    meaning: "4 Vent",
    element: "Air",
    destruction: "Emportés par le vent",
    duration: 364,
    color: "#FFFFFF"
  },
  {
    era: 3,
    nahuatl: "Nahui Quiahuitl",
    meaning: "4 Pluie",
    element: "Feu",
    destruction: "Pluie de feu",
    duration: 312,
    color: "#FF0000"
  },
  {
    era: 4,
    nahuatl: "Nahui Atl",
    meaning: "4 Eau",
    element: "Eau",
    destruction: "Déluge",
    duration: 676,
    color: "#0000FF"
  },
  {
    era: 5,
    nahuatl: "Nahui Ollin",
    meaning: "4 Mouvement",
    element: "Éther/Mouvement",
    destruction: "Tremblements de terre",
    duration: "En cours",
    color: "#FFD700",
    current: true
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// CALCUL DU SIGNE AZTÈQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule le signe du Tonalpohualli pour une date donnée
 */
export function calculateAztecSign(date = new Date()) {
  // Utiliser une date de référence
  const epoch = new Date("1519-11-08T00:00:00Z"); // Arrivée de Cortés
  const diffDays = Math.floor((date - epoch) / (1000 * 60 * 60 * 24));
  
  // Cycle de 260 jours
  const dayNumber = ((diffDays % 260) + 260) % 260;
  
  // Trecena (1-13)
  const trecena = (dayNumber % 13) + 1;
  
  // Signe (1-20)
  const signIndex = dayNumber % 20;
  const sign = TONALPOHUALLI_SIGNS[signIndex];
  
  return {
    day: dayNumber + 1,
    trecena: trecena,
    trecenaData: TRECENA[trecena - 1],
    sign: sign,
    signature: `${trecena} ${sign.nahuatl}`,
    meaningFull: `${trecena} ${sign.meaning}`,
    isSacred: trecena === 7 || trecena === 13
  };
}

/**
 * Trouve le signe aztèque pour un concept/mot
 */
export function findAztecSignForKeyword(keyword) {
  const kw = keyword.toLowerCase();
  
  for (const sign of TONALPOHUALLI_SIGNS) {
    if (sign.keywords.some(k => kw.includes(k) || k.includes(kw))) {
      return sign;
    }
  }
  
  // Par défaut, retourner Ollin (Mouvement)
  return TONALPOHUALLI_SIGNS[16];
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la résonance aztèque pour AT·OM
 */
export function getAztecResonance(arithmos, keyword = "", date = new Date()) {
  // Signe du jour
  const dailySign = calculateAztecSign(date);
  
  // Signe pour le concept
  const conceptSign = keyword ? findAztecSignForKeyword(keyword) : dailySign.sign;
  
  // Intensité Ollin
  const ollin = calculateOllinIntensity(arithmos, dailySign.trecena);
  
  // Ère actuelle
  const currentSun = FIVE_SUNS.find(s => s.current);
  
  return {
    // Signe du jour
    daily: {
      signature: dailySign.signature,
      sign: dailySign.sign,
      trecena: dailySign.trecenaData,
      isSacred: dailySign.isSacred
    },
    
    // Signe du concept
    concept: {
      nahuatl: conceptSign.nahuatl,
      meaning: conceptSign.meaning,
      element: conceptSign.element,
      energy: conceptSign.energy,
      color: conceptSign.color
    },
    
    // Ollin (intensité)
    ollin: {
      intensity: ollin.total,
      isSolar: ollin.isSolar,
      base: ollin.base
    },
    
    // Quetzalcóatl (direction EM)
    quetzalcoatl: QUETZALCOATL.flow,
    
    // Tezcatlipoca (miroir)
    tezcatlipoca: {
      shadow: `Réflexion sur: ${keyword || 'le moment présent'}`
    },
    
    // Ère cosmique
    era: {
      name: currentSun.nahuatl,
      element: currentSun.element
    },
    
    // Message
    message: ollin.isSolar 
      ? `☀️ FLASH SOLAIRE! ${conceptSign.nahuatl} (${conceptSign.meaning}) — Intensité maximale!`
      : `🌀 ${dailySign.signature} — ${conceptSign.energy}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Signes
  TONALPOHUALLI_SIGNS,
  TRECENA,
  
  // Divinités
  OLLIN,
  QUETZALCOATL,
  TEZCATLIPOCA,
  
  // Ères
  FIVE_SUNS,
  
  // Fonctions
  calculateOllinIntensity,
  calculateAztecSign,
  findAztecSignForKeyword,
  getAztecResonance
};
