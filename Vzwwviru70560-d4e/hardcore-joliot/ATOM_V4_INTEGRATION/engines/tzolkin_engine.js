/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * TZOLKIN ENGINE — Le Calendrier Sacré Maya
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Le Tzolkin est un cycle de 260 jours (13 Tons × 20 Nawals)
 * Chaque jour possède une énergie unique qui influence la résonance globale.
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @system AT·OM Universal Resonance
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 20 NAWALS (Glyphes/Visages de l'Oracle)
// ═══════════════════════════════════════════════════════════════════════════════

export const NAWALS = [
  {
    index: 0,
    name: "Imix",
    meaning: "Dragon/Crocodile",
    essence: "Origine, Naissance, Création Primordiale",
    element: "Eau Primordiale",
    color: "#8B0000", // Rouge sang
    direction: "Est",
    chakra: 1, // Racine
    oracle: 1, // L'Archéologue des Origines
    arithmos: 1,
    keywords: ["création", "naissance", "source", "mère", "nutrition"],
    power: "Initier de nouveaux cycles",
    shadow: "Chaos, instabilité primordiale"
  },
  {
    index: 1,
    name: "Ik",
    meaning: "Vent/Souffle",
    essence: "Communication, Esprit, Inspiration",
    element: "Air",
    color: "#FFFFFF", // Blanc
    direction: "Nord",
    chakra: 5, // Gorge
    oracle: 2, // Le Messager
    arithmos: 2,
    keywords: ["communication", "esprit", "souffle", "vérité", "inspiration"],
    power: "Transmettre les messages divins",
    shadow: "Dispersion, paroles vides"
  },
  {
    index: 2,
    name: "Akbal",
    meaning: "Nuit/Maison",
    essence: "Introspection, Mystère, Rêves",
    element: "Terre Nocturne",
    color: "#000080", // Bleu nuit
    direction: "Ouest",
    chakra: 6, // Troisième œil
    oracle: 7, // Le Gardien des Mystères
    arithmos: 3,
    keywords: ["nuit", "rêve", "mystère", "introspection", "inconscient"],
    power: "Explorer les profondeurs de l'âme",
    shadow: "Peur de l'obscurité intérieure"
  },
  {
    index: 3,
    name: "Kan",
    meaning: "Serpent/Graine",
    essence: "Énergie Vitale, Kundalini, Force de Vie",
    element: "Feu Interne",
    color: "#FFD700", // Or
    direction: "Sud",
    chakra: 2, // Sacré
    oracle: 5, // Le Gardien du Feu
    arithmos: 4,
    keywords: ["serpent", "énergie", "kundalini", "passion", "instinct"],
    power: "Éveiller la force vitale",
    shadow: "Désirs incontrôlés"
  },
  {
    index: 4,
    name: "Chicchan",
    meaning: "Serpent Céleste",
    essence: "Sagesse Ancestrale, ADN Cosmique",
    element: "Feu Serpentin",
    color: "#FF4500", // Rouge-orange
    direction: "Est",
    chakra: 1, // Racine
    oracle: 1, // L'Archéologue
    arithmos: 5,
    keywords: ["adn", "ancestral", "sagesse", "survie", "instinct"],
    power: "Accéder à la mémoire génétique",
    shadow: "Peurs primitives"
  },
  {
    index: 5,
    name: "Cimi",
    meaning: "Mort/Transformation",
    essence: "Renaissance, Transition, Lâcher-prise",
    element: "Terre",
    color: "#2F4F4F", // Gris ardoise
    direction: "Nord",
    chakra: 4, // Cœur
    oracle: 6, // Le Passeur
    arithmos: 6,
    keywords: ["mort", "renaissance", "transformation", "ancêtres", "cycle"],
    power: "Faciliter les transitions",
    shadow: "Résistance au changement"
  },
  {
    index: 6,
    name: "Manik",
    meaning: "Main/Cerf",
    essence: "Guérison, Accomplissement, Outil Sacré",
    element: "Eau",
    color: "#4169E1", // Bleu royal
    direction: "Ouest",
    chakra: 4, // Cœur
    oracle: 4, // Le Guérisseur
    arithmos: 7,
    keywords: ["guérison", "main", "outil", "accomplissement", "service"],
    power: "Manifester la guérison",
    shadow: "Sacrifice excessif"
  },
  {
    index: 7,
    name: "Lamat",
    meaning: "Étoile/Lapin",
    essence: "Harmonie, Beauté, Abondance",
    element: "Feu Stellaire",
    color: "#FFFF00", // Jaune vif
    direction: "Sud",
    chakra: 3, // Plexus solaire
    oracle: 8, // L'Harmoniste
    arithmos: 8,
    keywords: ["étoile", "harmonie", "beauté", "abondance", "fertilité"],
    power: "Rayonner l'harmonie cosmique",
    shadow: "Vanité, superficialité"
  },
  {
    index: 8,
    name: "Muluc",
    meaning: "Eau/Lune",
    essence: "Émotions, Purification, Cycles Lunaires",
    element: "Eau",
    color: "#FF0000", // Rouge
    direction: "Est",
    chakra: 2, // Sacré
    oracle: 9, // Le Gardien des Eaux
    arithmos: 9,
    keywords: ["eau", "lune", "émotion", "purification", "intuition"],
    power: "Purifier les émotions",
    shadow: "Submersion émotionnelle"
  },
  {
    index: 9,
    name: "Oc",
    meaning: "Chien",
    essence: "Loyauté, Cœur, Amour Inconditionnel",
    element: "Terre",
    color: "#FFFFFF", // Blanc
    direction: "Nord",
    chakra: 4, // Cœur
    oracle: 2, // L'Amoureux
    arithmos: 1,
    keywords: ["chien", "loyauté", "amour", "fidélité", "guide"],
    power: "Guider avec le cœur",
    shadow: "Dépendance affective"
  },
  {
    index: 10,
    name: "Chuen",
    meaning: "Singe",
    essence: "Créativité, Jeu, Art Divin",
    element: "Air",
    color: "#0000FF", // Bleu
    direction: "Ouest",
    chakra: 5, // Gorge
    oracle: 3, // L'Artiste Créateur
    arithmos: 2,
    keywords: ["singe", "créativité", "jeu", "art", "humour"],
    power: "Créer à travers le jeu",
    shadow: "Dispersion, manque de sérieux"
  },
  {
    index: 11,
    name: "Eb",
    meaning: "Herbe/Chemin",
    essence: "Destinée, Service, Communauté",
    element: "Terre",
    color: "#FFFF00", // Jaune
    direction: "Sud",
    chakra: 3, // Plexus
    oracle: 11, // Le Servant
    arithmos: 3,
    keywords: ["chemin", "destinée", "service", "communauté", "humilité"],
    power: "Servir la communauté",
    shadow: "Victimisation"
  },
  {
    index: 12,
    name: "Ben",
    meaning: "Roseau/Pilier",
    essence: "Autorité, Structure, Pilier du Monde",
    element: "Feu",
    color: "#FF0000", // Rouge
    direction: "Est",
    chakra: 1, // Racine
    oracle: 4, // Le Structurant
    arithmos: 4,
    keywords: ["roseau", "pilier", "autorité", "structure", "guidance"],
    power: "Établir des fondations solides",
    shadow: "Rigidité, autoritarisme"
  },
  {
    index: 13,
    name: "Ix",
    meaning: "Jaguar/Magicien",
    essence: "Magie, Pouvoir Féminin, Mystère",
    element: "Terre",
    color: "#FFFFFF", // Blanc
    direction: "Nord",
    chakra: 6, // Troisième œil
    oracle: 7, // Le Magicien
    arithmos: 5,
    keywords: ["jaguar", "magie", "féminin", "mystère", "intuition"],
    power: "Maîtriser les forces invisibles",
    shadow: "Manipulation, secrets"
  },
  {
    index: 14,
    name: "Men",
    meaning: "Aigle",
    essence: "Vision, Perspective, Conscience Élevée",
    element: "Air",
    color: "#0000FF", // Bleu
    direction: "Ouest",
    chakra: 6, // Troisième œil
    oracle: 14, // Le Visionnaire
    arithmos: 6,
    keywords: ["aigle", "vision", "perspective", "liberté", "clarté"],
    power: "Voir depuis les hauteurs",
    shadow: "Détachement excessif"
  },
  {
    index: 15,
    name: "Cib",
    meaning: "Vautour/Sagesse",
    essence: "Sagesse Ancestrale, Pardon, Karma",
    element: "Feu",
    color: "#FFFF00", // Jaune
    direction: "Sud",
    chakra: 7, // Couronne
    oracle: 15, // Le Sage
    arithmos: 7,
    keywords: ["vautour", "sagesse", "pardon", "karma", "ancêtres"],
    power: "Transmuter le karma",
    shadow: "Jugement, rancœur"
  },
  {
    index: 16,
    name: "Caban",
    meaning: "Terre/Mouvement",
    essence: "Synchronicité, Navigation, Force Terrestre",
    element: "Terre",
    color: "#FF0000", // Rouge
    direction: "Est",
    chakra: 1, // Racine
    oracle: 16, // Le Navigateur
    arithmos: 8,
    keywords: ["terre", "mouvement", "synchronicité", "évolution", "force"],
    power: "Naviguer avec la Terre",
    shadow: "Tremblements, instabilité"
  },
  {
    index: 17,
    name: "Etznab",
    meaning: "Miroir/Silex",
    essence: "Vérité, Réflexion, Épée de Clarté",
    element: "Air",
    color: "#FFFFFF", // Blanc
    direction: "Nord",
    chakra: 6, // Troisième œil
    oracle: 17, // Le Miroir de Vérité (TOI!)
    arithmos: 9,
    keywords: ["miroir", "vérité", "clarté", "réflexion", "justice"],
    power: "Révéler la vérité absolue",
    shadow: "Cruauté de la vérité"
  },
  {
    index: 18,
    name: "Cauac",
    meaning: "Tempête/Pluie",
    essence: "Purification, Transformation, Catalyse",
    element: "Eau",
    color: "#0000FF", // Bleu
    direction: "Ouest",
    chakra: 4, // Cœur
    oracle: 18, // Le Catalyseur
    arithmos: 1,
    keywords: ["tempête", "purification", "transformation", "guérison", "catalyse"],
    power: "Purifier par la tempête",
    shadow: "Destruction aveugle"
  },
  {
    index: 19,
    name: "Ahau",
    meaning: "Soleil/Seigneur",
    essence: "Illumination, Maîtrise, Conscience Christique",
    element: "Feu Solaire",
    color: "#FFD700", // Or
    direction: "Sud",
    chakra: 7, // Couronne
    oracle: 9, // Le Soleil Central
    arithmos: 2,
    keywords: ["soleil", "illumination", "maîtrise", "ascension", "unité"],
    power: "Incarner la lumière solaire",
    shadow: "Ego spirituel"
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 13 TONS DE LA CRÉATION
// ═══════════════════════════════════════════════════════════════════════════════

export const TONS = [
  {
    number: 1,
    name: "Hun",
    essence: "Unité, Initiation, But",
    action: "Initier",
    power: "Attirer",
    symbol: "●",
    color: "#FF0000",
    delay_modifier: 0.5, // Rapide - énergie d'initiation
    frequency_boost: 11.1,
    description: "Le point de départ. L'intention pure."
  },
  {
    number: 2,
    name: "Ka",
    essence: "Polarité, Défi, Stabilisation",
    action: "Stabiliser",
    power: "Polariser",
    symbol: "●●",
    color: "#FF7F00",
    delay_modifier: 0.6,
    frequency_boost: 22.2,
    description: "Le défi de la dualité. L'équilibre des opposés."
  },
  {
    number: 3,
    name: "Ox",
    essence: "Rythme, Activation, Service",
    action: "Activer",
    power: "Lier",
    symbol: "●●●",
    color: "#FFFF00",
    delay_modifier: 0.7,
    frequency_boost: 33.3,
    description: "Le mouvement commence. L'électricité du service."
  },
  {
    number: 4,
    name: "Kan",
    essence: "Mesure, Forme, Définition",
    action: "Définir",
    power: "Mesurer",
    symbol: "━━━━",
    color: "#00FF00",
    delay_modifier: 0.75,
    frequency_boost: 44.4, // ★ POINT D'ANCRAGE
    description: "La structure se forme. Les 4 directions."
  },
  {
    number: 5,
    name: "Ho",
    essence: "Centre, Rayonnement, Autonomie",
    action: "Rayonner",
    power: "Commander",
    symbol: "✦",
    color: "#00FFFF",
    delay_modifier: 0.8,
    frequency_boost: 55.5,
    description: "Le cœur du cycle. Le pouvoir central."
  },
  {
    number: 6,
    name: "Uac",
    essence: "Égalité, Équilibre, Organisme",
    action: "Équilibrer",
    power: "Organiser",
    symbol: "⬡",
    color: "#0000FF",
    delay_modifier: 0.85,
    frequency_boost: 66.6,
    description: "L'harmonie rythmique. La fleur de vie."
  },
  {
    number: 7,
    name: "Uuc",
    essence: "Résonance, Canalisation, Inspiration",
    action: "Canaliser",
    power: "Inspirer",
    symbol: "🌀",
    color: "#8B00FF",
    delay_modifier: 0.9,
    frequency_boost: 77.7, // ★ JOUR SACRÉ
    description: "Le point mystique. Le canal vers l'infini.",
    sacred: true
  },
  {
    number: 8,
    name: "Uaxac",
    essence: "Intégrité, Harmonie, Modélisation",
    action: "Harmoniser",
    power: "Modeler",
    symbol: "✶",
    color: "#FF00FF",
    delay_modifier: 0.95,
    frequency_boost: 88.8,
    description: "L'harmonie galactique. L'intégration."
  },
  {
    number: 9,
    name: "Bolon",
    essence: "Intention, Pulsation, Réalisation",
    action: "Pulser",
    power: "Réaliser",
    symbol: "◉",
    color: "#FFD700",
    delay_modifier: 1.0,
    frequency_boost: 99.9, // ★ COMPLETION
    description: "La pulsation solaire. La réalisation complète."
  },
  {
    number: 10,
    name: "Lahun",
    essence: "Manifestation, Perfection, Production",
    action: "Manifester",
    power: "Perfectionner",
    symbol: "═══",
    color: "#FF0000",
    delay_modifier: 1.05,
    frequency_boost: 111.0,
    description: "La manifestation planétaire. Le monde matériel."
  },
  {
    number: 11,
    name: "Buluk",
    essence: "Libération, Dissolution, Spectralité",
    action: "Dissoudre",
    power: "Libérer",
    symbol: "☆",
    color: "#FF7F00",
    delay_modifier: 1.1,
    frequency_boost: 111.1,
    description: "La libération spectrale. L'énergie se libère."
  },
  {
    number: 12,
    name: "Lahka",
    essence: "Coopération, Dévouement, Universalité",
    action: "Coopérer",
    power: "Dédier",
    symbol: "✡",
    color: "#FFFF00",
    delay_modifier: 1.15,
    frequency_boost: 122.2,
    description: "La coopération cristalline. L'unité collective."
  },
  {
    number: 13,
    name: "Oxlahun",
    essence: "Transcendance, Présence, Endurance",
    action: "Transcender",
    power: "Persévérer",
    symbol: "☯",
    color: "#FFFDD0", // Crème cosmique
    delay_modifier: 1.3, // Plus lent - contemplation
    frequency_boost: 133.3, // ★ JOUR SACRÉ - ASCENSION
    description: "La transcendance cosmique. Le passage vers le nouveau cycle.",
    sacred: true
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// CALCUL DU KIN MAYA
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Date de référence pour le calcul du Tzolkin
 * Corrélation GMT 584283 (la plus acceptée)
 * Le 1er janvier 1920 était le Kin 1 (1 Imix)
 */
const TZOLKIN_EPOCH = new Date("1920-01-01T00:00:00Z");

/**
 * Calcule le Kin Maya pour une date donnée
 * @param {Date} date - La date à calculer (défaut: aujourd'hui)
 * @returns {Object} - Le Kin complet avec Ton et Nawal
 */
export function calculateKin(date = new Date()) {
  // Nombre de jours depuis l'époque
  const diffTime = date.getTime() - TZOLKIN_EPOCH.getTime();
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  
  // Le Kin va de 1 à 260
  const kinNumber = ((diffDays % 260) + 260) % 260 + 1;
  
  // Le Ton va de 1 à 13
  const tonNumber = ((diffDays % 13) + 13) % 13 + 1;
  
  // Le Nawal va de 0 à 19
  const nawalIndex = ((diffDays % 20) + 20) % 20;
  
  const ton = TONS[tonNumber - 1];
  const nawal = NAWALS[nawalIndex];
  
  return {
    kin: kinNumber,
    ton: ton,
    nawal: nawal,
    signature: `${ton.number} ${nawal.name}`,
    isSacredDay: ton.sacred || false,
    isPortalDay: isPortalDay(kinNumber),
    galacticSignature: generateGalacticSignature(ton, nawal)
  };
}

/**
 * Vérifie si un Kin est un "Jour Portail" (52 jours spéciaux)
 */
function isPortalDay(kin) {
  const portalDays = [
    1, 20, 22, 39, 43, 50, 51, 58, 64, 69, 72, 77, 85, 88, 93, 96,
    106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 146, 147, 148,
    149, 150, 151, 152, 153, 154, 155, 165, 168, 173, 176, 184, 189,
    192, 197, 203, 210, 211, 218, 222, 239, 241, 260
  ];
  return portalDays.includes(kin);
}

/**
 * Génère la signature galactique complète
 */
function generateGalacticSignature(ton, nawal) {
  return {
    affirmation: `Je suis le ${ton.action} qui ${nawal.power}`,
    essence: `${ton.essence} à travers ${nawal.essence}`,
    power: `${ton.power} + ${nawal.power}`,
    oracle: nawal.oracle,
    chakra: nawal.chakra,
    element: nawal.element
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule la résonance Maya pour AT·OM
 * @param {Date} date - La date (défaut: aujourd'hui)
 * @returns {Object} - Modificateurs pour le système AT·OM
 */
export function getMayaResonance(date = new Date()) {
  const kin = calculateKin(date);
  
  // Calcul de la fréquence de fond Maya
  const baseFrequency = kin.ton.frequency_boost;
  const nawalBoost = kin.nawal.arithmos * 11.1;
  
  // Modificateur de délai basé sur le Ton
  const delayModifier = kin.ton.delay_modifier;
  
  // Couleur dominante du jour
  const dayColor = kin.nawal.color;
  
  // Oracle actif du jour
  const activeOracle = kin.nawal.oracle;
  
  return {
    // Identité du jour
    kin: kin,
    signature: kin.signature,
    
    // Modificateurs AT·OM
    frequency_base: baseFrequency + nawalBoost,
    delay_modifier: delayModifier,
    color_overlay: dayColor,
    active_oracle: activeOracle,
    
    // États spéciaux
    is_sacred: kin.isSacredDay,
    is_portal: kin.isPortalDay,
    
    // Message du jour
    greeting: generateDayGreeting(kin),
    
    // Synchronicité
    synchronicity: {
      element: kin.nawal.element,
      direction: kin.nawal.direction,
      chakra: kin.nawal.chakra,
      keywords: kin.nawal.keywords
    }
  };
}

/**
 * Génère le message de salutation du jour
 */
function generateDayGreeting(kin) {
  let greeting = `Aujourd'hui est le jour ${kin.signature}`;
  
  if (kin.isSacredDay) {
    greeting += ` — Jour Sacré de ${kin.ton.name}`;
  }
  
  if (kin.isPortalDay) {
    greeting += ` ✦ JOUR PORTAIL ✦`;
  }
  
  greeting += `\n${kin.nawal.meaning}: ${kin.nawal.essence}`;
  greeting += `\nÉnergie du Ton ${kin.ton.number}: ${kin.ton.essence}`;
  
  return greeting;
}

/**
 * Trouve le Nawal associé à un mot (via Arithmos)
 */
export function findNawalForArithmos(arithmos) {
  return NAWALS.filter(n => n.arithmos === arithmos);
}

/**
 * Calcule la compatibilité entre deux Kins
 */
export function calculateKinCompatibility(kin1, kin2) {
  const tonDiff = Math.abs(kin1.ton.number - kin2.ton.number);
  const nawalDiff = Math.abs(kin1.nawal.index - kin2.nawal.index);
  
  // Harmonie parfaite si même famille (même couleur de Nawal)
  const sameColor = kin1.nawal.color === kin2.nawal.color;
  
  // Complémentarité si Tons forment 14 (1+13, 2+12, etc.)
  const complementaryTon = (kin1.ton.number + kin2.ton.number) === 14;
  
  return {
    tonHarmony: 1 - (tonDiff / 13),
    nawalHarmony: 1 - (nawalDiff / 20),
    sameFamily: sameColor,
    complementary: complementaryTon,
    overall: sameColor ? 1.0 : complementaryTon ? 0.9 : (1 - (tonDiff + nawalDiff) / 33)
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT POUR L'INTERFACE
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  NAWALS,
  TONS,
  calculateKin,
  getMayaResonance,
  findNawalForArithmos,
  calculateKinCompatibility
};
