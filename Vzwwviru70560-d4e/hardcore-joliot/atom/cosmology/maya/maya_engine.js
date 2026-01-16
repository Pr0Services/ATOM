/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM — MOTEUR TZOLKIN MAYA
 * Le Calendrier Sacré des 260 Jours
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Le Tzolkin est la respiration de l'univers Maya.
 * 13 Tons × 20 Nawals = 260 Kins (jours sacrés)
 * 
 * Corrélation utilisée: GMT 584283 (Goodman-Martinez-Thompson)
 * Date de référence: 4 Ahau 8 Cumku = 11 août 3114 av. J.-C.
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 - Le Gardien de la Synthèse
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 20 NAWALS (Glyphes/Visages du Temps)
// ═══════════════════════════════════════════════════════════════════════════════

export const NAWALS = [
  {
    index: 0,
    name: "Imix",
    yucatec: "Imix",
    meaning: "Crocodile/Dragon",
    element: "Eau primordiale",
    direction: "Est",
    color: "#DC143C", // Rouge cramoisi
    energy: "Naissance, origine, matrice cosmique",
    oracle: 1, // Lien avec Oracle AT·OM
    chakra: 1, // Racine
    cssEffect: "pulse-deep",
    sound: "grave",
  },
  {
    index: 1,
    name: "Ik",
    yucatec: "Ik'",
    meaning: "Vent/Souffle",
    element: "Air",
    direction: "Nord",
    color: "#FFFFFF", // Blanc
    energy: "Communication, esprit, respiration divine",
    oracle: 2,
    chakra: 5, // Gorge
    cssEffect: "float-gentle",
    sound: "aigu",
  },
  {
    index: 2,
    name: "Akbal",
    yucatec: "Ak'b'al",
    meaning: "Nuit/Maison",
    element: "Terre nocturne",
    direction: "Ouest",
    color: "#191970", // Bleu nuit
    energy: "Introspection, rêves, mystère",
    oracle: 7,
    chakra: 6, // Troisième œil
    cssEffect: "shadow-deep",
    sound: "sourd",
  },
  {
    index: 3,
    name: "Kan",
    yucatec: "K'an",
    meaning: "Serpent/Graine",
    element: "Feu vital",
    direction: "Sud",
    color: "#FFD700", // Or
    energy: "Force vitale, kundalini, semence",
    oracle: 5,
    chakra: 2, // Sacré
    cssEffect: "serpentine",
    sound: "sifflant",
  },
  {
    index: 4,
    name: "Chicchan",
    yucatec: "Chikchan",
    meaning: "Serpent Céleste",
    element: "Feu cosmique",
    direction: "Est",
    color: "#FF4500", // Rouge-orange
    energy: "Kundalini éveillée, transformation",
    oracle: 5,
    chakra: 3, // Plexus
    cssEffect: "wave-energy",
    sound: "vibrant",
  },
  {
    index: 5,
    name: "Cimi",
    yucatec: "Kimi",
    meaning: "Mort/Transformation",
    element: "Terre",
    direction: "Nord",
    color: "#2F4F4F", // Gris ardoise
    energy: "Renaissance, ancêtres, lâcher-prise",
    oracle: 9,
    chakra: 1, // Racine
    cssEffect: "fade-transform",
    sound: "silence",
  },
  {
    index: 6,
    name: "Manik",
    yucatec: "Manik'",
    meaning: "Cerf/Main",
    element: "Air",
    direction: "Ouest",
    color: "#4169E1", // Bleu royal
    energy: "Guérison, outils, accomplissement",
    oracle: 6,
    chakra: 4, // Cœur
    cssEffect: "healing-glow",
    sound: "harmonique",
  },
  {
    index: 7,
    name: "Lamat",
    yucatec: "Lamat",
    meaning: "Étoile/Lapin",
    element: "Feu stellaire",
    direction: "Sud",
    color: "#FFFF00", // Jaune vif
    energy: "Harmonie, beauté, Vénus",
    oracle: 3,
    chakra: 3, // Plexus
    cssEffect: "star-twinkle",
    sound: "cristallin",
  },
  {
    index: 8,
    name: "Muluc",
    yucatec: "Muluk",
    meaning: "Eau/Lune",
    element: "Eau",
    direction: "Est",
    color: "#FF0000", // Rouge
    energy: "Émotions, purification, offrande",
    oracle: 2,
    chakra: 2, // Sacré
    cssEffect: "ripple-water",
    sound: "liquide",
  },
  {
    index: 9,
    name: "Oc",
    yucatec: "Ok",
    meaning: "Chien",
    element: "Feu du cœur",
    direction: "Nord",
    color: "#FFFAF0", // Blanc floral
    energy: "Loyauté, guide, amour inconditionnel",
    oracle: 4,
    chakra: 4, // Cœur
    cssEffect: "warm-glow",
    sound: "doux",
  },
  {
    index: 10,
    name: "Chuen",
    yucatec: "Chuwen",
    meaning: "Singe",
    element: "Air créatif",
    direction: "Ouest",
    color: "#0000CD", // Bleu medium
    energy: "Créativité, jeu, arts, tissage du temps",
    oracle: 3,
    chakra: 5, // Gorge
    cssEffect: "playful-bounce",
    sound: "joyeux",
  },
  {
    index: 11,
    name: "Eb",
    yucatec: "E'b'",
    meaning: "Herbe/Chemin",
    element: "Terre fertile",
    direction: "Sud",
    color: "#FFFF00", // Jaune
    energy: "Destinée, service, humanité",
    oracle: 8,
    chakra: 1, // Racine
    cssEffect: "grow-organic",
    sound: "terrestre",
  },
  {
    index: 12,
    name: "Ben",
    yucatec: "B'en",
    meaning: "Roseau/Pilier",
    element: "Feu céleste",
    direction: "Est",
    color: "#DC143C", // Cramoisi
    energy: "Autorité, pilier du ciel, connexion",
    oracle: 4,
    chakra: 7, // Couronne
    cssEffect: "pillar-rise",
    sound: "puissant",
  },
  {
    index: 13,
    name: "Ix",
    yucatec: "Ix",
    meaning: "Jaguar",
    element: "Terre magique",
    direction: "Nord",
    color: "#FFFFFF", // Blanc
    energy: "Magie, chaman, monde souterrain",
    oracle: 7,
    chakra: 6, // Troisième œil
    cssEffect: "stealth-fade",
    sound: "mystique",
  },
  {
    index: 14,
    name: "Men",
    yucatec: "Men",
    meaning: "Aigle",
    element: "Air élevé",
    direction: "Ouest",
    color: "#4169E1", // Bleu royal
    energy: "Vision, liberté, conscience supérieure",
    oracle: 7,
    chakra: 6, // Troisième œil
    cssEffect: "soar-high",
    sound: "perçant",
  },
  {
    index: 15,
    name: "Cib",
    yucatec: "Kib'",
    meaning: "Vautour/Chouette",
    element: "Feu ancien",
    direction: "Sud",
    color: "#FFD700", // Or
    energy: "Sagesse ancestrale, karma, pardon",
    oracle: 9,
    chakra: 7, // Couronne
    cssEffect: "ancient-glow",
    sound: "ancestral",
  },
  {
    index: 16,
    name: "Caban",
    yucatec: "Kab'an",
    meaning: "Terre/Tremblement",
    element: "Terre vivante",
    direction: "Est",
    color: "#FF0000", // Rouge
    energy: "Force terrestre, synchronicité, navigation",
    oracle: 6,
    chakra: 1, // Racine
    cssEffect: "earth-pulse",
    sound: "profond",
  },
  {
    index: 17,
    name: "Etznab",
    yucatec: "Etz'nab'",
    meaning: "Miroir/Silex",
    element: "Air tranchant",
    direction: "Nord",
    color: "#FFFFFF", // Blanc
    energy: "Vérité, réflexion, sacrifice",
    oracle: 9,
    chakra: 6, // Troisième œil
    cssEffect: "mirror-flash",
    sound: "tranchant",
  },
  {
    index: 18,
    name: "Cauac",
    yucatec: "Kawak",
    meaning: "Tempête/Orage",
    element: "Eau-Feu (vapeur)",
    direction: "Ouest",
    color: "#0000CD", // Bleu
    energy: "Purification, catalyseur, guérison collective",
    oracle: 8,
    chakra: 4, // Cœur
    cssEffect: "storm-surge",
    sound: "tonnerre",
  },
  {
    index: 19,
    name: "Ahau",
    yucatec: "Ajaw",
    meaning: "Soleil/Seigneur",
    element: "Feu solaire",
    direction: "Sud",
    color: "#FFD700", // Or solaire
    energy: "Illumination, maîtrise, conscience solaire",
    oracle: 9, // L'Unité
    chakra: 7, // Couronne
    cssEffect: "sun-radiate",
    sound: "cosmique",
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 13 TONS DE LA CRÉATION
// ═══════════════════════════════════════════════════════════════════════════════

export const TONS = [
  {
    number: 1,
    name: "Hun",
    meaning: "Unité/Initiation",
    energy: "Début, impulsion, graine",
    action: "Initier",
    power: "Attraction magnétique",
    delayMod: 0.5, // Rapide
    intensityMod: 1.0,
    cssClass: "ton-initiation",
  },
  {
    number: 2,
    name: "Ka",
    meaning: "Dualité/Défi",
    energy: "Polarité, choix, relation",
    action: "Stabiliser",
    power: "Polarisation lunaire",
    delayMod: 0.6,
    intensityMod: 0.9,
    cssClass: "ton-challenge",
  },
  {
    number: 3,
    name: "Ox",
    meaning: "Rythme/Activation",
    energy: "Mouvement, dynamisme",
    action: "Activer",
    power: "Lien électrique",
    delayMod: 0.5,
    intensityMod: 1.1,
    cssClass: "ton-activation",
  },
  {
    number: 4,
    name: "Kan",
    meaning: "Mesure/Définition",
    energy: "Structure, forme, fondation",
    action: "Définir",
    power: "Auto-existence",
    delayMod: 0.7,
    intensityMod: 0.8,
    cssClass: "ton-definition",
  },
  {
    number: 5,
    name: "Ho",
    meaning: "Centre/Rayonnement",
    energy: "Cœur, centre, pouvoir",
    action: "Commander",
    power: "Rayonnement harmonique",
    delayMod: 0.6,
    intensityMod: 1.2,
    cssClass: "ton-radiance",
  },
  {
    number: 6,
    name: "Uac",
    meaning: "Équilibre/Organisation",
    energy: "Flux, équilibre organique",
    action: "Équilibrer",
    power: "Égalité rythmique",
    delayMod: 0.7,
    intensityMod: 0.9,
    cssClass: "ton-balance",
  },
  {
    number: 7,
    name: "Uuc",
    meaning: "Résonance/Canalisation",
    energy: "Accord, mystique, alignement",
    action: "Canaliser",
    power: "Accord résonant",
    delayMod: 0.8,
    intensityMod: 1.3, // Point sacré!
    cssClass: "ton-resonance",
    isSacred: true,
  },
  {
    number: 8,
    name: "Uaxac",
    meaning: "Intégrité/Harmonisation",
    energy: "Intégration, modélisation",
    action: "Harmoniser",
    power: "Intégrité galactique",
    delayMod: 0.7,
    intensityMod: 1.0,
    cssClass: "ton-integrity",
  },
  {
    number: 9,
    name: "Bolon",
    meaning: "Intention/Pulsion",
    energy: "Accomplissement, complétion",
    action: "Pulser",
    power: "Intention solaire",
    delayMod: 0.6,
    intensityMod: 1.1,
    cssClass: "ton-intention",
  },
  {
    number: 10,
    name: "Lahun",
    meaning: "Manifestation/Perfection",
    energy: "Manifestation, réalisation",
    action: "Parfaire",
    power: "Manifestation planétaire",
    delayMod: 0.7,
    intensityMod: 1.0,
    cssClass: "ton-manifestation",
  },
  {
    number: 11,
    name: "Buluc",
    meaning: "Libération/Dissolution",
    energy: "Changement, libération",
    action: "Dissoudre",
    power: "Libération spectrale",
    delayMod: 0.5,
    intensityMod: 1.2,
    cssClass: "ton-liberation",
  },
  {
    number: 12,
    name: "Lahca",
    meaning: "Coopération/Dévouement",
    energy: "Universalisation, partage",
    action: "Dédier",
    power: "Coopération cristalline",
    delayMod: 0.8,
    intensityMod: 0.9,
    cssClass: "ton-cooperation",
  },
  {
    number: 13,
    name: "Oxlahun",
    meaning: "Présence/Transcendance",
    energy: "Transcendance, ascension",
    action: "Transcender",
    power: "Présence cosmique",
    delayMod: 1.2, // Lent, contemplatif
    intensityMod: 1.5, // Maximum!
    cssClass: "ton-transcendence",
    isSacred: true,
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// CALCUL DU KIN MAYA
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Date de référence pour la corrélation GMT 584283
 * 4 Ahau 8 Cumku = 11 août 3114 av. J.-C. (Julien)
 * En calendrier grégorien proleptique: -3113-08-11
 */
const TZOLKIN_EPOCH = new Date("1507-04-21"); // Date de référence simplifiée (1 Imix)
const HAAB_EPOCH = new Date("1507-04-21");

/**
 * Calcule le Kin Maya pour une date donnée
 * @param {Date} date - Date à calculer (défaut: aujourd'hui)
 * @returns {Object} - Données complètes du Kin
 */
export function getMayaKin(date = new Date()) {
  // Nombre de jours depuis l'époque de référence
  const diffTime = date.getTime() - TZOLKIN_EPOCH.getTime();
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  
  // Calcul du Ton (cycle de 13)
  let tonIndex = diffDays % 13;
  if (tonIndex < 0) tonIndex += 13;
  const ton = TONS[tonIndex];
  
  // Calcul du Nawal (cycle de 20)
  let nawalIndex = diffDays % 20;
  if (nawalIndex < 0) nawalIndex += 20;
  const nawal = NAWALS[nawalIndex];
  
  // Numéro du Kin (1-260)
  let kinNumber = ((tonIndex * 20 + nawalIndex) % 260) + 1;
  if (kinNumber <= 0) kinNumber += 260;
  
  // Calcul de l'onde enchantée (Wavespell)
  const wavespell = Math.floor((kinNumber - 1) / 13);
  const wavespellNawal = NAWALS[wavespell % 20];
  
  // Jour portail galactique?
  const isGalacticPortal = isPortalDay(kinNumber);
  
  // Fréquence modificatrice AT·OM
  const frequencyMod = ton.number * 11.1; // Base 11.1 Hz par ton
  
  return {
    date: date,
    kinNumber,
    kinName: `${ton.number} ${nawal.name}`,
    ton: {
      ...ton,
      index: tonIndex,
    },
    nawal: {
      ...nawal,
    },
    wavespell: {
      number: wavespell + 1,
      nawal: wavespellNawal,
    },
    frequencyMod,
    isGalacticPortal,
    isSacredDay: ton.isSacred || false,
    // Modificateurs pour AT·OM
    atomMod: {
      delayMultiplier: ton.delayMod,
      intensityMultiplier: ton.intensityMod,
      dominantColor: nawal.color,
      cssEffect: nawal.cssEffect,
      linkedOracle: nawal.oracle,
      linkedChakra: nawal.chakra,
    },
  };
}

/**
 * Vérifie si un Kin est un jour portail galactique
 * Les 52 jours portails forment un motif fractal dans le Tzolkin
 */
function isPortalDay(kinNumber) {
  const portalDays = [
    1, 20, 22, 39, 43, 50, 51, 58, 64, 69,
    72, 77, 85, 88, 93, 96, 106, 107, 108, 109,
    110, 111, 112, 113, 114, 115, 146, 147, 148, 149,
    150, 151, 152, 153, 154, 155, 165, 168, 173, 176,
    184, 189, 192, 197, 203, 210, 211, 218, 222, 239,
    241, 260
  ];
  return portalDays.includes(kinNumber);
}

/**
 * Obtient le Kin Maya d'aujourd'hui
 */
export function getTodayKin() {
  return getMayaKin(new Date());
}

/**
 * Calcule le Kin de naissance (Signature Galactique)
 * @param {Date} birthDate - Date de naissance
 */
export function getBirthKin(birthDate) {
  const kin = getMayaKin(birthDate);
  return {
    ...kin,
    type: "Signature Galactique",
    description: `Tu es ${kin.kinName} - ${kin.nawal.meaning} avec le pouvoir de ${kin.ton.action}`,
  };
}

/**
 * Message de bienvenue Maya pour l'interface AT·OM
 */
export function getMayaGreeting() {
  const kin = getTodayKin();
  const sacred = kin.isSacredDay ? "🌟 JOUR SACRÉ! " : "";
  const portal = kin.isGalacticPortal ? "🌀 PORTAIL GALACTIQUE! " : "";
  
  return {
    greeting: `${sacred}${portal}Aujourd'hui est ${kin.kinName}`,
    subtitle: `${kin.nawal.meaning} — ${kin.ton.meaning}`,
    energy: kin.nawal.energy,
    action: `Action du jour: ${kin.ton.action}`,
    frequencyBoost: `+${kin.frequencyMod.toFixed(1)} Hz de résonance Maya`,
    color: kin.nawal.color,
    effect: kin.nawal.cssEffect,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// HARMONISATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Fusionne la résonance AT·OM avec l'énergie Maya
 * @param {Object} atomResonance - Résultat de useAtomResonance
 * @returns {Object} - Résonance enrichie
 */
export function harmonizeWithMaya(atomResonance) {
  const maya = getTodayKin();
  
  if (!atomResonance) {
    return { maya, combined: null };
  }
  
  // Fréquence combinée
  const combinedHz = atomResonance.hz + maya.frequencyMod;
  
  // Délai ajusté par le Ton
  const adjustedDelay = Math.round(atomResonance.delay * maya.atomMod.delayMultiplier);
  
  // Intensité ajustée
  const intensity = atomResonance.ratio * maya.atomMod.intensityMultiplier;
  
  return {
    atom: atomResonance,
    maya,
    combined: {
      hz: combinedHz,
      delay: adjustedDelay,
      intensity,
      primaryColor: atomResonance.color,
      mayaColor: maya.nawal.color,
      effect: maya.atomMod.cssEffect,
      message: `${atomResonance.word} résonne à ${combinedHz.toFixed(1)} Hz en ce jour ${maya.kinName}`,
      oracleSync: maya.atomMod.linkedOracle === atomResonance.level,
      chakraLink: maya.atomMod.linkedChakra,
    },
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  NAWALS,
  TONS,
  getMayaKin,
  getTodayKin,
  getBirthKin,
  getMayaGreeting,
  harmonizeWithMaya,
};
