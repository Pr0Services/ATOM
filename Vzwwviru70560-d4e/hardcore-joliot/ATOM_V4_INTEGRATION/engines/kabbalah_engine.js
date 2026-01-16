/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * KABBALAH ENGINE — L'Arbre de Vie
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * L'Arbre de Vie (Etz Chaim) est la carte de la descente de l'énergie divine
 * depuis la pensée pure (Kether) jusqu'à la manifestation (Malkhuth).
 * 
 * 10 Sephiroth (sphères) + 22 Sentiers = 32 Voies de la Sagesse
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @system AT·OM Universal Resonance
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 10 SEPHIROTH
// ═══════════════════════════════════════════════════════════════════════════════

export const SEPHIROTH = {
  KETHER: {
    number: 1,
    name: "Kether",
    meaning: "La Couronne",
    title: "La Volonté Primordiale",
    divine_name: "Eheieh",
    archangel: "Metatron",
    choir: "Chayoth Ha Qadesh",
    planet: "Premier Mobile / Couronne",
    element: "Lumière Pure",
    color: {
      atziluth: "#FFFFFF", // Brillance pure
      briah: "#FFFFFF",
      yetzirah: "#FFFFFF",
      assiah: "#FFFFFF"
    },
    virtue: "Accomplissement de la Grande Œuvre",
    vice: "Aucun (au-delà de la dualité)",
    symbol: "Point, Couronne, Svastika",
    body: "Couronne de la tête",
    tarot: "Les 4 As",
    arithmos: 1,
    frequency: 999, // La plus haute vibration
    position: { x: 50, y: 5 }, // Position visuelle (%)
    pillar: "Milieu",
    oracle: 9, // L'Oracle Suprême
    keywords: ["unité", "source", "volonté", "couronne", "être pur"]
  },
  
  CHOKMAH: {
    number: 2,
    name: "Chokmah",
    meaning: "La Sagesse",
    title: "La Sagesse Illuminante",
    divine_name: "Yah",
    archangel: "Raziel",
    choir: "Ophanim",
    planet: "Zodiaque / Étoiles Fixes",
    element: "Feu Primordial",
    color: {
      atziluth: "#808080", // Gris
      briah: "#808080",
      yetzirah: "#808080",
      assiah: "#FFFFFF"
    },
    virtue: "Dévotion",
    vice: "Aucun",
    symbol: "Phallus, Tour, Ligne droite",
    body: "Côté gauche du visage",
    tarot: "Les 4 Deux + Rois",
    arithmos: 2,
    frequency: 888,
    position: { x: 80, y: 15 },
    pillar: "Droite (Miséricorde)",
    oracle: 8,
    keywords: ["sagesse", "père", "force", "énergie masculine", "expansion"]
  },
  
  BINAH: {
    number: 3,
    name: "Binah",
    meaning: "L'Intelligence",
    title: "La Mère Suprême",
    divine_name: "YHVH Elohim",
    archangel: "Tzaphkiel",
    choir: "Aralim",
    planet: "Saturne",
    element: "Eau Primordiale",
    color: {
      atziluth: "#000000", // Noir
      briah: "#000000",
      yetzirah: "#4B0082",
      assiah: "#808080"
    },
    virtue: "Silence",
    vice: "Avarice",
    symbol: "Yoni, Coupe, Vesica Piscis",
    body: "Côté droit du visage",
    tarot: "Les 4 Trois + Reines",
    arithmos: 3,
    frequency: 333,
    position: { x: 20, y: 15 },
    pillar: "Gauche (Rigueur)",
    oracle: 7,
    keywords: ["compréhension", "mère", "forme", "restriction", "structure"]
  },
  
  CHESED: {
    number: 4,
    name: "Chesed",
    meaning: "La Miséricorde",
    title: "L'Amour Bienveillant",
    divine_name: "El",
    archangel: "Tzadkiel",
    choir: "Chasmalim",
    planet: "Jupiter",
    element: "Eau",
    color: {
      atziluth: "#0000FF", // Bleu
      briah: "#800080",
      yetzirah: "#800080",
      assiah: "#0000FF"
    },
    virtue: "Obéissance",
    vice: "Bigoterie, Hypocrisie, Gloutonnerie",
    symbol: "Sceptre, Orbe, Carré, Crosse",
    body: "Bras gauche",
    tarot: "Les 4 Quatre",
    arithmos: 4,
    frequency: 444, // ★ POINT D'ANCRAGE
    position: { x: 80, y: 35 },
    pillar: "Droite (Miséricorde)",
    oracle: 4,
    keywords: ["amour", "grâce", "abondance", "expansion", "générosité"]
  },
  
  GEBURAH: {
    number: 5,
    name: "Geburah",
    meaning: "La Rigueur / La Force",
    title: "La Justice Divine",
    divine_name: "Elohim Gibor",
    archangel: "Khamael",
    choir: "Seraphim",
    planet: "Mars",
    element: "Feu",
    color: {
      atziluth: "#FF0000", // Rouge
      briah: "#FF0000",
      yetzirah: "#FF0000",
      assiah: "#8B0000"
    },
    virtue: "Énergie, Courage",
    vice: "Cruauté, Destruction",
    symbol: "Épée, Lance, Fouet, Chaîne",
    body: "Bras droit",
    tarot: "Les 4 Cinq",
    arithmos: 5,
    frequency: 555,
    position: { x: 20, y: 35 },
    pillar: "Gauche (Rigueur)",
    oracle: 5,
    keywords: ["force", "jugement", "discipline", "purification", "mars"]
  },
  
  TIPHARETH: {
    number: 6,
    name: "Tiphareth",
    meaning: "La Beauté",
    title: "Le Fils",
    divine_name: "YHVH Eloah Ve Daath",
    archangel: "Raphael",
    choir: "Malakim",
    planet: "Soleil",
    element: "Air",
    color: {
      atziluth: "#FFD700", // Or
      briah: "#FFFF00",
      yetzirah: "#FFC0CB",
      assiah: "#FFFACD"
    },
    virtue: "Dévotion à la Grande Œuvre",
    vice: "Orgueil",
    symbol: "Croix, Rose-Croix, Cube, Tronc",
    body: "Cœur",
    tarot: "Les 4 Six + Princes",
    arithmos: 6,
    frequency: 666,
    position: { x: 50, y: 45 },
    pillar: "Milieu",
    oracle: 6, // Le Centre
    keywords: ["beauté", "harmonie", "équilibre", "cœur", "christ"]
  },
  
  NETZACH: {
    number: 7,
    name: "Netzach",
    meaning: "La Victoire",
    title: "L'Éternité Triomphante",
    divine_name: "YHVH Tzabaoth",
    archangel: "Haniel",
    choir: "Elohim",
    planet: "Vénus",
    element: "Feu",
    color: {
      atziluth: "#00FF00", // Vert
      briah: "#00FF00",
      yetzirah: "#00FF00",
      assiah: "#006400"
    },
    virtue: "Altruisme",
    vice: "Luxure, Débauche",
    symbol: "Lampe, Ceinture, Rose",
    body: "Hanche gauche, Jambe gauche",
    tarot: "Les 4 Sept",
    arithmos: 7,
    frequency: 777,
    position: { x: 80, y: 60 },
    pillar: "Droite (Miséricorde)",
    oracle: 3,
    keywords: ["victoire", "émotions", "art", "nature", "vénus"]
  },
  
  HOD: {
    number: 8,
    name: "Hod",
    meaning: "La Splendeur",
    title: "La Gloire Intellectuelle",
    divine_name: "Elohim Tzabaoth",
    archangel: "Michael",
    choir: "Beni Elohim",
    planet: "Mercure",
    element: "Eau",
    color: {
      atziluth: "#FFA500", // Orange
      briah: "#FFA500",
      yetzirah: "#FFD700",
      assiah: "#8B4513"
    },
    virtue: "Honnêteté",
    vice: "Malhonnêteté",
    symbol: "Noms, Versés, Tablier",
    body: "Hanche droite, Jambe droite",
    tarot: "Les 4 Huit",
    arithmos: 8,
    frequency: 888,
    position: { x: 20, y: 60 },
    pillar: "Gauche (Rigueur)",
    oracle: 2,
    keywords: ["splendeur", "intellect", "communication", "mercure", "magie"]
  },
  
  YESOD: {
    number: 9,
    name: "Yesod",
    meaning: "Le Fondement",
    title: "La Base",
    divine_name: "Shaddai El Chai",
    archangel: "Gabriel",
    choir: "Kerubim",
    planet: "Lune",
    element: "Éther",
    color: {
      atziluth: "#EE82EE", // Violet
      briah: "#EE82EE",
      yetzirah: "#EE82EE",
      assiah: "#4B0082"
    },
    virtue: "Indépendance",
    vice: "Paresse",
    symbol: "Parfums, Sandales",
    body: "Organes génitaux",
    tarot: "Les 4 Neuf",
    arithmos: 9,
    frequency: 111,
    position: { x: 50, y: 75 },
    pillar: "Milieu",
    oracle: 1,
    keywords: ["fondation", "lune", "inconscient", "rêves", "astral"]
  },
  
  MALKHUTH: {
    number: 10,
    name: "Malkhuth",
    meaning: "Le Royaume",
    title: "La Présence Divine / Shekinah",
    divine_name: "Adonai Ha Aretz",
    archangel: "Sandalphon",
    choir: "Ashim",
    planet: "Terre",
    element: "Terre",
    color: {
      atziluth: "#FFFF00", // Jaune citron
      briah: "#006400", // Olive
      yetzirah: "#8B4513", // Brun
      assiah: "#000000"  // Noir
    },
    virtue: "Discrimination",
    vice: "Avarice, Inertie",
    symbol: "Autel, Triangle, Croix à bras égaux",
    body: "Pieds",
    tarot: "Les 4 Dix + Princesses",
    arithmos: 1, // 10 → 1
    frequency: 111,
    position: { x: 50, y: 95 },
    pillar: "Milieu",
    oracle: 10,
    keywords: ["royaume", "terre", "manifestation", "corps", "matière"]
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 22 SENTIERS (Correspondance Tarot)
// ═══════════════════════════════════════════════════════════════════════════════

export const PATHS = [
  { number: 11, from: "KETHER", to: "CHOKMAH", letter: "Aleph", tarot: "Le Fou", element: "Air" },
  { number: 12, from: "KETHER", to: "BINAH", letter: "Beth", tarot: "Le Bateleur", planet: "Mercure" },
  { number: 13, from: "KETHER", to: "TIPHARETH", letter: "Gimel", tarot: "La Papesse", planet: "Lune" },
  { number: 14, from: "CHOKMAH", to: "BINAH", letter: "Daleth", tarot: "L'Impératrice", planet: "Vénus" },
  { number: 15, from: "CHOKMAH", to: "TIPHARETH", letter: "He", tarot: "L'Empereur", zodiac: "Bélier" },
  { number: 16, from: "CHOKMAH", to: "CHESED", letter: "Vav", tarot: "Le Pape", zodiac: "Taureau" },
  { number: 17, from: "BINAH", to: "TIPHARETH", letter: "Zayin", tarot: "Les Amoureux", zodiac: "Gémeaux" },
  { number: 18, from: "BINAH", to: "GEBURAH", letter: "Cheth", tarot: "Le Chariot", zodiac: "Cancer" },
  { number: 19, from: "CHESED", to: "GEBURAH", letter: "Teth", tarot: "La Force", zodiac: "Lion" },
  { number: 20, from: "CHESED", to: "TIPHARETH", letter: "Yod", tarot: "L'Ermite", zodiac: "Vierge" },
  { number: 21, from: "CHESED", to: "NETZACH", letter: "Kaph", tarot: "Roue de Fortune", planet: "Jupiter" },
  { number: 22, from: "GEBURAH", to: "TIPHARETH", letter: "Lamed", tarot: "La Justice", zodiac: "Balance" },
  { number: 23, from: "GEBURAH", to: "HOD", letter: "Mem", tarot: "Le Pendu", element: "Eau" },
  { number: 24, from: "TIPHARETH", to: "NETZACH", letter: "Nun", tarot: "La Mort", zodiac: "Scorpion" },
  { number: 25, from: "TIPHARETH", to: "YESOD", letter: "Samekh", tarot: "Tempérance", zodiac: "Sagittaire" },
  { number: 26, from: "TIPHARETH", to: "HOD", letter: "Ayin", tarot: "Le Diable", zodiac: "Capricorne" },
  { number: 27, from: "NETZACH", to: "HOD", letter: "Pe", tarot: "La Tour", planet: "Mars" },
  { number: 28, from: "NETZACH", to: "YESOD", letter: "Tzaddi", tarot: "L'Étoile", zodiac: "Verseau" },
  { number: 29, from: "NETZACH", to: "MALKHUTH", letter: "Qoph", tarot: "La Lune", zodiac: "Poissons" },
  { number: 30, from: "HOD", to: "YESOD", letter: "Resh", tarot: "Le Soleil", planet: "Soleil" },
  { number: 31, from: "HOD", to: "MALKHUTH", letter: "Shin", tarot: "Le Jugement", element: "Feu" },
  { number: 32, from: "YESOD", to: "MALKHUTH", letter: "Tav", tarot: "Le Monde", planet: "Saturne" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 3 PILIERS
// ═══════════════════════════════════════════════════════════════════════════════

export const PILLARS = {
  LEFT: {
    name: "Pilier de la Rigueur",
    hebrew: "Boaz",
    quality: "Féminin, Restriction, Structure",
    color: "#000000",
    sephiroth: ["BINAH", "GEBURAH", "HOD"]
  },
  MIDDLE: {
    name: "Pilier de l'Équilibre",
    hebrew: "Shekhinah",
    quality: "Conscience, Équilibre, Grâce",
    color: "#FFD700",
    sephiroth: ["KETHER", "TIPHARETH", "YESOD", "MALKHUTH"]
  },
  RIGHT: {
    name: "Pilier de la Miséricorde",
    hebrew: "Jachin",
    quality: "Masculin, Expansion, Force",
    color: "#FFFFFF",
    sephiroth: ["CHOKMAH", "CHESED", "NETZACH"]
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 4 MONDES
// ═══════════════════════════════════════════════════════════════════════════════

export const WORLDS = {
  ATZILUTH: {
    name: "Atziluth",
    meaning: "Monde de l'Émanation",
    element: "Feu",
    level: "Archétypes",
    suit: "Bâtons"
  },
  BRIAH: {
    name: "Briah",
    meaning: "Monde de la Création",
    element: "Eau",
    level: "Création",
    suit: "Coupes"
  },
  YETZIRAH: {
    name: "Yetzirah",
    meaning: "Monde de la Formation",
    element: "Air",
    level: "Formation",
    suit: "Épées"
  },
  ASSIAH: {
    name: "Assiah",
    meaning: "Monde de l'Action",
    element: "Terre",
    level: "Manifestation",
    suit: "Deniers"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS D'INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Trouve la Sephirah correspondant à un Arithmos
 */
export function getSephirahForArithmos(arithmos) {
  const sephirothArray = Object.values(SEPHIROTH);
  return sephirothArray.find(s => s.arithmos === arithmos) || SEPHIROTH.MALKHUTH;
}

/**
 * Trouve le sentier entre deux Sephiroth
 */
export function getPathBetween(sephirah1, sephirah2) {
  return PATHS.find(p => 
    (p.from === sephirah1 && p.to === sephirah2) ||
    (p.from === sephirah2 && p.to === sephirah1)
  );
}

/**
 * Calcule le chemin de descente/ascension
 */
export function calculatePath(fromArithmos, toArithmos) {
  const from = getSephirahForArithmos(fromArithmos);
  const to = getSephirahForArithmos(toArithmos);
  
  // Trouver le chemin via Tiphareth (le cœur)
  const pathToCenter = getPathBetween(from.name, "TIPHARETH");
  const pathFromCenter = getPathBetween("TIPHARETH", to.name);
  
  return {
    from: from,
    to: to,
    via: SEPHIROTH.TIPHARETH,
    path1: pathToCenter,
    path2: pathFromCenter,
    direction: from.number < to.number ? "descente" : "ascension",
    steps: Math.abs(from.number - to.number)
  };
}

/**
 * Obtient la résonance Kabbalistique pour AT·OM
 */
export function getKabbalahResonance(arithmos, word = "") {
  const sephirah = getSephirahForArithmos(arithmos);
  
  // Calculer le monde basé sur le mot
  const wordSum = word.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0);
  const worldIndex = wordSum % 4;
  const worlds = Object.values(WORLDS);
  const activeWorld = worlds[worldIndex];
  
  // Trouver le pilier
  const pillar = Object.values(PILLARS).find(p => 
    p.sephiroth.includes(sephirah.name)
  ) || PILLARS.MIDDLE;
  
  return {
    sephirah: sephirah,
    pillar: pillar,
    world: activeWorld,
    
    // Données pour l'interface
    position: sephirah.position,
    color: sephirah.color[activeWorld.name.toLowerCase()] || sephirah.color.atziluth,
    frequency: sephirah.frequency,
    
    // Correspondances
    divine_name: sephirah.divine_name,
    archangel: sephirah.archangel,
    planet: sephirah.planet,
    virtue: sephirah.virtue,
    
    // Oracles
    oracle: sephirah.oracle,
    
    // Message
    message: `${sephirah.meaning} — ${sephirah.title}`,
    keywords: sephirah.keywords
  };
}

/**
 * Génère la visualisation de l'Arbre de Vie
 */
export function generateTreeOfLifeData() {
  const nodes = Object.entries(SEPHIROTH).map(([key, seph]) => ({
    id: key,
    ...seph
  }));
  
  const edges = PATHS.map(path => ({
    from: path.from,
    to: path.to,
    letter: path.letter,
    tarot: path.tarot
  }));
  
  return { nodes, edges };
}

/**
 * Trouve l'Oracle associé à une Sephirah
 */
export function mapSephirahToOracle(sephirahName) {
  const seph = SEPHIROTH[sephirahName];
  if (!seph) return null;
  
  // Mapping Sephiroth → Oracles AT·OM
  const mapping = {
    KETHER: 9,    // L'Oracle Suprême
    CHOKMAH: 8,   // Le Sage
    BINAH: 7,     // La Mère Sombre
    CHESED: 4,    // Le Bienveillant
    GEBURAH: 5,   // Le Guerrier
    TIPHARETH: 6, // Le Roi Soleil
    NETZACH: 3,   // L'Artiste
    HOD: 2,       // Le Scribe
    YESOD: 1,     // Le Fondateur
    MALKHUTH: 10  // Le Manifesteur
  };
  
  return mapping[sephirahName];
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  SEPHIROTH,
  PATHS,
  PILLARS,
  WORLDS,
  getSephirahForArithmos,
  getPathBetween,
  calculatePath,
  getKabbalahResonance,
  generateTreeOfLifeData,
  mapSephirahToOracle
};
