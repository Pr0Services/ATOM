/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 🏛️ GREEK ENGINE — LE LOGOS ET LES SOLIDES
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Les Grecs sont les pères de l'Arithmos. Ils apportent:
 * 
 * 1. La Musique des Sphères (Pythagore) — Base des fréquences Hz
 * 2. Les 5 Solides de Platon — Les briques de l'univers
 * 3. La Tétraktys — Le triangle sacré (1+2+3+4=10)
 * 4. Les Intervalles Harmoniques — Ratios musicaux sacrés
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @symbol Ω (Omega)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LA TÉTRAKTYS — LE TRIANGLE SACRÉ
// ═══════════════════════════════════════════════════════════════════════════════

/**
 *           ●           (1) La Monade — L'Unité
 *          ● ●          (2) La Dyade — La Dualité
 *         ● ● ●         (3) La Triade — L'Harmonie
 *        ● ● ● ●        (4) La Tétrade — Les Éléments
 *        ─────────
 *           10          Le nombre parfait
 * 
 * "Par celui qui a transmis à notre âme la Tétraktys,
 *  Source de la nature éternelle."
 *  — Serment pythagoricien
 */

export const TETRAKTYS = {
  name: "Tétraktys",
  levels: [
    { level: 1, points: 1, meaning: "Monade", concept: "Unité, Source, Dieu" },
    { level: 2, points: 2, meaning: "Dyade", concept: "Dualité, Polarité, Ligne" },
    { level: 3, points: 3, meaning: "Triade", concept: "Harmonie, Triangle, Plan" },
    { level: 4, points: 4, meaning: "Tétrade", concept: "Éléments, Carré, Volume" }
  ],
  total: 10,
  formula: "1 + 2 + 3 + 4 = 10",
  
  // Correspondances musicales
  ratios: {
    octave: { ratio: "2:1", interval: 2/1 },
    quinte: { ratio: "3:2", interval: 3/2 },
    quarte: { ratio: "4:3", interval: 4/3 }
  }
};

/**
 * Décompose un nombre selon la Tétraktys
 */
export function decomposeByTetraktys(num) {
  const tens = Math.floor(num / 10);
  const units = num % 10;
  
  // Trouver le niveau de la Tétraktys pour les unités
  let level = 0;
  let sum = 0;
  for (let i = 1; i <= 4; i++) {
    sum += i;
    if (units <= sum) {
      level = i;
      break;
    }
  }
  
  return {
    original: num,
    tens,
    units,
    tetraktysLevel: level,
    tetraktysName: TETRAKTYS.levels[level - 1]?.meaning || "Au-delà",
    significance: TETRAKTYS.levels[level - 1]?.concept || "Transcendance",
    isPerfect: num % 10 === 0 // Multiples de 10
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LA MUSIQUE DES SPHÈRES — PYTHAGORE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Pythagore découvrit que les intervalles musicaux sont des rapports mathématiques.
 * Les planètes, en mouvement, produisent une musique cosmique.
 */

export const PYTHAGOREAN_RATIOS = {
  // Intervalles fondamentaux
  unisson: { ratio: [1, 1], decimal: 1.000, consonance: "Parfait" },
  octave: { ratio: [2, 1], decimal: 2.000, consonance: "Parfait" },
  quinte: { ratio: [3, 2], decimal: 1.500, consonance: "Parfait" },
  quarte: { ratio: [4, 3], decimal: 1.333, consonance: "Parfait" },
  tierce_majeure: { ratio: [5, 4], decimal: 1.250, consonance: "Imparfait" },
  tierce_mineure: { ratio: [6, 5], decimal: 1.200, consonance: "Imparfait" },
  sixte_majeure: { ratio: [5, 3], decimal: 1.667, consonance: "Imparfait" },
  seconde_majeure: { ratio: [9, 8], decimal: 1.125, consonance: "Dissonant" },
  septieme: { ratio: [15, 8], decimal: 1.875, consonance: "Dissonant" }
};

/**
 * Calcule l'harmonique pythagoricienne entre deux fréquences
 */
export function calculatePythagoreanHarmony(freq1, freq2) {
  const ratio = Math.max(freq1, freq2) / Math.min(freq1, freq2);
  
  // Trouver l'intervalle le plus proche
  let closestInterval = null;
  let closestDiff = Infinity;
  
  for (const [name, data] of Object.entries(PYTHAGOREAN_RATIOS)) {
    const diff = Math.abs(ratio - data.decimal);
    if (diff < closestDiff) {
      closestDiff = diff;
      closestInterval = { name, ...data };
    }
  }
  
  return {
    frequency1: freq1,
    frequency2: freq2,
    ratio: ratio,
    closestInterval: closestInterval,
    deviation: closestDiff,
    isHarmonic: closestDiff < 0.05, // 5% de tolérance
    consonance: closestInterval?.consonance || "Indéterminé"
  };
}

/**
 * Génère les harmoniques d'une fréquence fondamentale
 */
export function generateHarmonics(fundamental, count = 8) {
  const harmonics = [];
  
  for (let n = 1; n <= count; n++) {
    harmonics.push({
      number: n,
      frequency: fundamental * n,
      interval: n === 1 ? "Fondamentale"
              : n === 2 ? "Octave"
              : n === 3 ? "Quinte + Octave"
              : n === 4 ? "Double Octave"
              : n === 5 ? "Tierce majeure + 2 Octaves"
              : `Harmonique ${n}`
    });
  }
  
  return harmonics;
}

// ═══════════════════════════════════════════════════════════════════════════════
// LES 5 SOLIDES DE PLATON
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les 5 solides réguliers convexes — les seuls possibles en 3D.
 * Platon les associa aux éléments dans le Timée.
 */

export const PLATONIC_SOLIDS = {
  TETRAHEDRON: {
    name: "Tétraèdre",
    greek: "Τετράεδρον",
    faces: 4,
    vertices: 4,
    edges: 6,
    faceShape: "Triangle",
    element: "Feu",
    symbol: "🔺",
    color: "#FF4500",
    frequency: 555, // AT·OM
    chakra: 3, // Manipura
    quality: "Transformation, Aspiration, Élévation",
    dihedral_angle: 70.53, // degrés
    platonic_dual: "TETRAHEDRON", // Auto-dual
    category: ["spiritualité", "transformation", "énergie"]
  },
  
  HEXAHEDRON: {
    name: "Hexaèdre (Cube)",
    greek: "Ἑξάεδρον",
    faces: 6,
    vertices: 8,
    edges: 12,
    faceShape: "Carré",
    element: "Terre",
    symbol: "⬛",
    color: "#8B4513",
    frequency: 111, // AT·OM
    chakra: 1, // Muladhara
    quality: "Stabilité, Fondation, Manifestation",
    dihedral_angle: 90,
    platonic_dual: "OCTAHEDRON",
    category: ["science", "structure", "matière"]
  },
  
  OCTAHEDRON: {
    name: "Octaèdre",
    greek: "Ὀκτάεδρον",
    faces: 8,
    vertices: 6,
    edges: 12,
    faceShape: "Triangle",
    element: "Air",
    symbol: "◇",
    color: "#87CEEB",
    frequency: 444, // AT·OM - ANCRAGE
    chakra: 4, // Anahata
    quality: "Intégration, Équilibre, Amour",
    dihedral_angle: 109.47,
    platonic_dual: "HEXAHEDRON",
    category: ["pensée", "communication", "logique"]
  },
  
  ICOSAHEDRON: {
    name: "Icosaèdre",
    greek: "Εἰκοσάεδρον",
    faces: 20,
    vertices: 12,
    edges: 30,
    faceShape: "Triangle",
    element: "Eau",
    symbol: "💧",
    color: "#0000FF",
    frequency: 222, // AT·OM
    chakra: 2, // Svadhisthana
    quality: "Flux, Transformation, Émotion",
    dihedral_angle: 138.19,
    platonic_dual: "DODECAHEDRON",
    category: ["émotion", "créativité", "flux"]
  },
  
  DODECAHEDRON: {
    name: "Dodécaèdre",
    greek: "Δωδεκάεδρον",
    faces: 12,
    vertices: 20,
    edges: 30,
    faceShape: "Pentagone",
    element: "Éther/Cosmos",
    symbol: "⬡",
    color: "#EE82EE",
    frequency: 999, // AT·OM - UNITÉ
    chakra: 7, // Sahasrara
    quality: "Conscience Cosmique, Ascension, Univers",
    dihedral_angle: 116.57,
    platonic_dual: "ICOSAHEDRON",
    category: ["spiritualité", "cosmos", "conscience"]
  }
};

/**
 * Trouve le solide de Platon pour une catégorie de concept
 */
export function getSolidForCategory(category) {
  const solids = Object.values(PLATONIC_SOLIDS);
  
  const categoryMap = {
    // Feu - Tétraèdre
    "spiritualité": "TETRAHEDRON",
    "transformation": "TETRAHEDRON",
    "énergie": "TETRAHEDRON",
    
    // Terre - Cube
    "science": "HEXAHEDRON",
    "structure": "HEXAHEDRON",
    "matière": "HEXAHEDRON",
    "technologie": "HEXAHEDRON",
    
    // Air - Octaèdre
    "pensée": "OCTAHEDRON",
    "communication": "OCTAHEDRON",
    "logique": "OCTAHEDRON",
    "ia": "OCTAHEDRON",
    
    // Eau - Icosaèdre
    "émotion": "ICOSAHEDRON",
    "créativité": "ICOSAHEDRON",
    "art": "ICOSAHEDRON",
    "adn": "ICOSAHEDRON",
    
    // Éther - Dodécaèdre
    "cosmos": "DODECAHEDRON",
    "conscience": "DODECAHEDRON",
    "univers": "DODECAHEDRON"
  };
  
  const solidKey = categoryMap[category.toLowerCase()];
  return solidKey ? PLATONIC_SOLIDS[solidKey] : PLATONIC_SOLIDS.OCTAHEDRON;
}

/**
 * Trouve le solide pour un Arithmos
 */
export function getSolidForArithmos(arithmos) {
  const mapping = {
    1: "HEXAHEDRON",    // Terre/Stabilité
    2: "ICOSAHEDRON",   // Eau/Dualité
    3: "TETRAHEDRON",   // Feu/Trinité
    4: "HEXAHEDRON",    // Terre/Structure
    5: "TETRAHEDRON",   // Feu/Mouvement
    6: "ICOSAHEDRON",   // Eau/Harmonie
    7: "OCTAHEDRON",    // Air/Introspection
    8: "OCTAHEDRON",    // Air/Infini
    9: "DODECAHEDRON"   // Éther/Unité
  };
  
  return PLATONIC_SOLIDS[mapping[arithmos]] || PLATONIC_SOLIDS.OCTAHEDRON;
}

// ═══════════════════════════════════════════════════════════════════════════════
// FORMULE D'EULER POUR LES POLYÈDRES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * V - E + F = 2 (Caractéristique d'Euler)
 * Vertices - Edges + Faces = 2
 */
export function verifyEulerFormula(solid) {
  const V = solid.vertices;
  const E = solid.edges;
  const F = solid.faces;
  
  const euler = V - E + F;
  
  return {
    vertices: V,
    edges: E,
    faces: F,
    euler: euler,
    valid: euler === 2,
    formula: `${V} - ${E} + ${F} = ${euler}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LES MOYENNES PYTHAGORICIENNES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les trois moyennes de Pythagore:
 * 1. Arithmétique: (a + b) / 2
 * 2. Géométrique: √(a × b)
 * 3. Harmonique: 2ab / (a + b)
 */

export function pythagoreanMeans(a, b) {
  return {
    arithmetic: (a + b) / 2,
    geometric: Math.sqrt(a * b),
    harmonic: (2 * a * b) / (a + b),
    
    // Relation: Harmonique ≤ Géométrique ≤ Arithmétique
    ordered: [
      { name: "Harmonique", value: (2 * a * b) / (a + b) },
      { name: "Géométrique", value: Math.sqrt(a * b) },
      { name: "Arithmétique", value: (a + b) / 2 }
    ].sort((x, y) => x.value - y.value)
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la résonance grecque pour AT·OM
 */
export function getGreekResonance(arithmos, frequency, category = null) {
  // Décomposition Tétraktys
  const tetraktys = decomposeByTetraktys(arithmos);
  
  // Solide de Platon correspondant
  const solid = category 
    ? getSolidForCategory(category)
    : getSolidForArithmos(arithmos);
  
  // Vérifier Euler
  const euler = verifyEulerFormula(solid);
  
  // Harmoniques
  const harmonics = generateHarmonics(frequency, 5);
  
  // Vérifier si la fréquence est harmonique avec 444 Hz (ancrage)
  const harmonyWith444 = calculatePythagoreanHarmony(frequency, 444);
  
  // Moyennes
  const means = pythagoreanMeans(arithmos, 9);
  
  return {
    // Tétraktys
    tetraktys: {
      level: tetraktys.tetraktysLevel,
      name: tetraktys.tetraktysName,
      significance: tetraktys.significance
    },
    
    // Solide de Platon
    solid: {
      name: solid.name,
      element: solid.element,
      symbol: solid.symbol,
      faces: solid.faces,
      color: solid.color,
      quality: solid.quality
    },
    
    // Euler
    euler: euler,
    
    // Harmoniques
    harmonics: harmonics.slice(0, 3),
    
    // Harmonie avec l'ancrage
    harmony: {
      with444: harmonyWith444,
      isConsonant: harmonyWith444.consonance === "Parfait"
    },
    
    // Moyennes
    means: means,
    
    // Message
    message: `${solid.symbol} ${solid.name} (${solid.element}) — ${tetraktys.tetraktysName}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Tétraktys
  TETRAKTYS,
  decomposeByTetraktys,
  
  // Pythagore
  PYTHAGOREAN_RATIOS,
  calculatePythagoreanHarmony,
  generateHarmonics,
  pythagoreanMeans,
  
  // Platon
  PLATONIC_SOLIDS,
  getSolidForCategory,
  getSolidForArithmos,
  verifyEulerFormula,
  
  // Intégration
  getGreekResonance
};
