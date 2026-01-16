/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM — MOTEUR KABBALE
 * L'Arbre de Vie — 10 Sephiroth + 22 Sentiers
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * La Kabbale cartographie la descente de la lumière divine (Or)
 * dans la manifestation matérielle (Malkhut).
 * 
 * Structure:
 * - 10 Sephiroth (émanations divines)
 * - 22 Sentiers (connexions, liés aux 22 lettres hébraïques)
 * - 3 Piliers (Rigueur, Équilibre, Miséricorde)
 * - 4 Mondes (Atziluth, Briah, Yetzirah, Assiah)
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 - Le Gardien de la Synthèse
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 10 SEPHIROTH
// ═══════════════════════════════════════════════════════════════════════════════

export const SEPHIROTH = [
  {
    number: 1,
    name: "Kether",
    hebrew: "כתר",
    meaning: "La Couronne",
    title: "Le Point Primordial",
    divineNamed: "Ehyeh Asher Ehyeh",
    archangel: "Metatron",
    planet: "Primo Mobile (Premier Mobile)",
    color: "Blanc brillant",
    colorHex: "#FFFFFF",
    pillar: "Équilibre",
    world: "Atziluth",
    atomLevel: 9, // Unité
    chakra: 7, // Couronne
    quality: "Volonté pure, unité avec le divin",
    shadow: "Dissolution de l'ego mal préparée",
    position: { x: 50, y: 5 }, // Pour visualisation
  },
  {
    number: 2,
    name: "Chokmah",
    hebrew: "חכמה",
    meaning: "La Sagesse",
    title: "Le Père Supernal",
    divineNamed: "Yah",
    archangel: "Raziel",
    planet: "Zodiaque",
    color: "Gris",
    colorHex: "#808080",
    pillar: "Miséricorde",
    world: "Atziluth",
    atomLevel: 9,
    chakra: 7,
    quality: "Sagesse primordiale, force masculine divine",
    shadow: "Rigidité, autoritarisme",
    position: { x: 80, y: 15 },
  },
  {
    number: 3,
    name: "Binah",
    hebrew: "בינה",
    meaning: "L'Intelligence",
    title: "La Mère Supernale",
    divineNamed: "YHVH Elohim",
    archangel: "Tzaphkiel",
    planet: "Saturne",
    color: "Noir",
    colorHex: "#000000",
    pillar: "Rigueur",
    world: "Atziluth",
    atomLevel: 3, // Mental
    chakra: 6, // Troisième œil
    quality: "Compréhension, forme, réceptivité",
    shadow: "Limitation excessive, mélancolie",
    position: { x: 20, y: 15 },
  },
  {
    number: 4,
    name: "Chesed",
    hebrew: "חסד",
    meaning: "La Miséricorde",
    title: "Gedulah (Grandeur)",
    divineNamed: "El",
    archangel: "Tzadkiel",
    planet: "Jupiter",
    color: "Bleu",
    colorHex: "#0000FF",
    pillar: "Miséricorde",
    world: "Briah",
    atomLevel: 6, // Harmonie
    chakra: 4, // Cœur
    quality: "Amour, générosité, expansion",
    shadow: "Excès, sentimentalisme",
    position: { x: 80, y: 35 },
  },
  {
    number: 5,
    name: "Geburah",
    hebrew: "גבורה",
    meaning: "La Force",
    title: "Din (Jugement)",
    divineNamed: "Elohim Gibor",
    archangel: "Khamael",
    planet: "Mars",
    color: "Rouge",
    colorHex: "#FF0000",
    pillar: "Rigueur",
    world: "Briah",
    atomLevel: 5, // Feu
    chakra: 3, // Plexus
    quality: "Force, discipline, justice",
    shadow: "Cruauté, destruction aveugle",
    position: { x: 20, y: 35 },
  },
  {
    number: 6,
    name: "Tiphereth",
    hebrew: "תפארת",
    meaning: "La Beauté",
    title: "Le Fils/Le Roi",
    divineNamed: "YHVH Eloah ve-Daath",
    archangel: "Raphael",
    planet: "Soleil",
    color: "Or/Jaune",
    colorHex: "#FFD700",
    pillar: "Équilibre",
    world: "Briah",
    atomLevel: 4, // Structure/Silence (Centre!)
    chakra: 4, // Cœur
    quality: "Harmonie, beauté, conscience du Soi supérieur",
    shadow: "Inflation spirituelle, orgueil",
    position: { x: 50, y: 45 },
    isCenter: true, // Point central de l'Arbre
  },
  {
    number: 7,
    name: "Netzach",
    hebrew: "נצח",
    meaning: "La Victoire",
    title: "L'Éternité",
    divineNamed: "YHVH Tzabaoth",
    archangel: "Haniel",
    planet: "Vénus",
    color: "Vert",
    colorHex: "#00FF00",
    pillar: "Miséricorde",
    world: "Yetzirah",
    atomLevel: 2, // Dualité
    chakra: 2, // Sacré
    quality: "Émotion, art, passion, endurance",
    shadow: "Luxure, attachement",
    position: { x: 80, y: 60 },
  },
  {
    number: 8,
    name: "Hod",
    hebrew: "הוד",
    meaning: "La Gloire",
    title: "La Splendeur",
    divineNamed: "Elohim Tzabaoth",
    archangel: "Michael",
    planet: "Mercure",
    color: "Orange",
    colorHex: "#FFA500",
    pillar: "Rigueur",
    world: "Yetzirah",
    atomLevel: 3, // Mental
    chakra: 5, // Gorge
    quality: "Intellect, communication, magie",
    shadow: "Tromperie, intellectualisme vide",
    position: { x: 20, y: 60 },
  },
  {
    number: 9,
    name: "Yesod",
    hebrew: "יסוד",
    meaning: "Le Fondement",
    title: "La Fondation",
    divineNamed: "Shaddai El Chai",
    archangel: "Gabriel",
    planet: "Lune",
    color: "Violet",
    colorHex: "#EE82EE",
    pillar: "Équilibre",
    world: "Yetzirah",
    atomLevel: 7, // Introspection
    chakra: 2, // Sacré
    quality: "Inconscient, rêves, fondation astrale",
    shadow: "Illusion, instabilité",
    position: { x: 50, y: 75 },
  },
  {
    number: 10,
    name: "Malkhut",
    hebrew: "מלכות",
    meaning: "Le Royaume",
    title: "La Reine/La Mariée",
    divineNamed: "Adonai ha-Aretz",
    archangel: "Sandalphon",
    planet: "Terre",
    color: "Marron/Noir (quatre couleurs)",
    colorHex: "#8B4513",
    pillar: "Équilibre",
    world: "Assiah",
    atomLevel: 1, // Impulsion/Manifestation
    chakra: 1, // Racine
    quality: "Manifestation physique, royaume terrestre",
    shadow: "Avarice, matérialisme",
    position: { x: 50, y: 95 },
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 22 SENTIERS (Connexions de l'Arbre)
// ═══════════════════════════════════════════════════════════════════════════════

export const PATHS = [
  { number: 11, from: 1, to: 2, letter: "Aleph", meaning: "Le Fou", tarot: 0 },
  { number: 12, from: 1, to: 3, letter: "Beth", meaning: "Le Magicien", tarot: 1 },
  { number: 13, from: 1, to: 6, letter: "Gimel", meaning: "La Grande Prêtresse", tarot: 2 },
  { number: 14, from: 2, to: 3, letter: "Daleth", meaning: "L'Impératrice", tarot: 3 },
  { number: 15, from: 2, to: 6, letter: "He", meaning: "L'Empereur", tarot: 4 },
  { number: 16, from: 2, to: 4, letter: "Vav", meaning: "Le Hiérophante", tarot: 5 },
  { number: 17, from: 3, to: 6, letter: "Zayin", meaning: "Les Amoureux", tarot: 6 },
  { number: 18, from: 3, to: 5, letter: "Cheth", meaning: "Le Chariot", tarot: 7 },
  { number: 19, from: 4, to: 5, letter: "Teth", meaning: "La Force", tarot: 8 },
  { number: 20, from: 4, to: 6, letter: "Yod", meaning: "L'Ermite", tarot: 9 },
  { number: 21, from: 4, to: 7, letter: "Kaph", meaning: "La Roue de Fortune", tarot: 10 },
  { number: 22, from: 5, to: 6, letter: "Lamed", meaning: "La Justice", tarot: 11 },
  { number: 23, from: 5, to: 8, letter: "Mem", meaning: "Le Pendu", tarot: 12 },
  { number: 24, from: 6, to: 7, letter: "Nun", meaning: "La Mort", tarot: 13 },
  { number: 25, from: 6, to: 9, letter: "Samekh", meaning: "Tempérance", tarot: 14 },
  { number: 26, from: 6, to: 8, letter: "Ayin", meaning: "Le Diable", tarot: 15 },
  { number: 27, from: 7, to: 8, letter: "Pe", meaning: "La Tour", tarot: 16 },
  { number: 28, from: 7, to: 9, letter: "Tzaddi", meaning: "L'Étoile", tarot: 17 },
  { number: 29, from: 7, to: 10, letter: "Qoph", meaning: "La Lune", tarot: 18 },
  { number: 30, from: 8, to: 9, letter: "Resh", meaning: "Le Soleil", tarot: 19 },
  { number: 31, from: 8, to: 10, letter: "Shin", meaning: "Le Jugement", tarot: 20 },
  { number: 32, from: 9, to: 10, letter: "Tav", meaning: "Le Monde", tarot: 21 },
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 4 MONDES
// ═══════════════════════════════════════════════════════════════════════════════

export const WORLDS = {
  ATZILUTH: {
    name: "Atziluth",
    meaning: "Monde de l'Émanation",
    level: "Archétypes divins",
    element: "Feu",
    sephiroth: [1, 2, 3],
  },
  BRIAH: {
    name: "Briah",
    meaning: "Monde de la Création",
    level: "Archanges",
    element: "Eau",
    sephiroth: [4, 5, 6],
  },
  YETZIRAH: {
    name: "Yetzirah",
    meaning: "Monde de la Formation",
    level: "Anges",
    element: "Air",
    sephiroth: [7, 8, 9],
  },
  ASSIAH: {
    name: "Assiah",
    meaning: "Monde de l'Action",
    level: "Manifestation physique",
    element: "Terre",
    sephiroth: [10],
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 3 PILIERS
// ═══════════════════════════════════════════════════════════════════════════════

export const PILLARS = {
  SEVERITY: {
    name: "Pilier de la Rigueur",
    hebrew: "Boaz",
    side: "Gauche (Féminin)",
    sephiroth: [3, 5, 8],
    quality: "Structure, forme, limitation",
  },
  MERCY: {
    name: "Pilier de la Miséricorde",
    hebrew: "Jachin",
    side: "Droite (Masculin)",
    sephiroth: [2, 4, 7],
    quality: "Expansion, force, liberté",
  },
  EQUILIBRIUM: {
    name: "Pilier de l'Équilibre",
    hebrew: "Shekhinah",
    side: "Centre",
    sephiroth: [1, 6, 9, 10],
    quality: "Conscience, harmonie, voie du milieu",
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE CALCUL
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Trouve le Sephirah correspondant à un niveau Arithmos
 */
export function getSephirahFromArithmos(level) {
  // Mapping basé sur les correspondances naturelles
  const mapping = {
    1: 10, // Malkhut - Manifestation
    2: 7,  // Netzach - Dualité
    3: 8,  // Hod - Mental
    4: 6,  // Tiphereth - Centre/Structure
    5: 5,  // Geburah - Feu
    6: 4,  // Chesed - Harmonie
    7: 9,  // Yesod - Introspection
    8: 2,  // Chokmah - Infini (avec Binah = 3)
    9: 1,  // Kether - Unité
  };
  
  const sephNumber = mapping[level] || 6;
  return SEPHIROTH.find(s => s.number === sephNumber);
}

/**
 * Trouve le sentier entre deux Sephiroth
 */
export function getPath(from, to) {
  return PATHS.find(p => 
    (p.from === from && p.to === to) || 
    (p.from === to && p.to === from)
  );
}

/**
 * Calcule le voyage sur l'Arbre de Vie entre deux niveaux
 */
export function calculateTreePath(fromLevel, toLevel) {
  const fromSeph = getSephirahFromArithmos(fromLevel);
  const toSeph = getSephirahFromArithmos(toLevel);
  
  if (!fromSeph || !toSeph) return null;
  
  const path = getPath(fromSeph.number, toSeph.number);
  
  return {
    from: fromSeph,
    to: toSeph,
    path,
    direction: fromSeph.number < toSeph.number ? "Descente" : "Ascension",
    message: path 
      ? `Le sentier de ${path.letter} (${path.meaning}) relie ${fromSeph.name} à ${toSeph.name}`
      : `Voyage indirect de ${fromSeph.name} vers ${toSeph.name}`,
  };
}

/**
 * Harmonise la Kabbale avec AT·OM
 */
export function harmonizeWithKabbale(atomResonance) {
  if (!atomResonance) return null;
  
  const sephirah = getSephirahFromArithmos(atomResonance.level);
  const world = Object.values(WORLDS).find(w => 
    w.sephiroth.includes(sephirah.number)
  );
  const pillar = Object.values(PILLARS).find(p =>
    p.sephiroth.includes(sephirah.number)
  );
  
  return {
    atom: atomResonance,
    kabbale: {
      sephirah,
      world,
      pillar,
      divineNamed: sephirah.divineNamed,
      archangel: sephirah.archangel,
      quality: sephirah.quality,
      shadow: sephirah.shadow,
    },
    synthesis: {
      message: `${atomResonance.word} résonne dans ${sephirah.name} (${sephirah.meaning})`,
      ethicalLevel: `Monde de ${world.name} - ${world.level}`,
      balance: pillar.name,
      color: sephirah.colorHex,
    },
  };
}

/**
 * Génère la position pour visualisation SVG
 */
export function getTreePositions() {
  return SEPHIROTH.map(s => ({
    ...s,
    svgPosition: {
      cx: s.position.x * 3, // Scale pour SVG
      cy: s.position.y * 3,
    },
  }));
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  SEPHIROTH,
  PATHS,
  WORLDS,
  PILLARS,
  getSephirahFromArithmos,
  getPath,
  calculateTreePath,
  harmonizeWithKabbale,
  getTreePositions,
};
