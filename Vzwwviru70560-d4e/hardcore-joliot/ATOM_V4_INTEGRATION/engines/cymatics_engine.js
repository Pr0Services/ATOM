/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * CYMATICS & SACRED GEOMETRY ENGINE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * La Cymatique est la science de la visualisation du son.
 * Chaque fréquence crée un motif géométrique unique.
 * 
 * Ce moteur intègre:
 * - Cymatique (formes sonores)
 * - Suite de Fibonacci
 * - Nombre d'Or (φ = 1.618...)
 * - Géométrie Sacrée
 * - Topologie des Nœuds
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @system AT·OM Universal Resonance
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES SACRÉES
// ═══════════════════════════════════════════════════════════════════════════════

// Le Nombre d'Or
export const PHI = (1 + Math.sqrt(5)) / 2; // ≈ 1.6180339887...
export const PHI_INVERSE = 1 / PHI;        // ≈ 0.6180339887...
export const PHI_SQUARED = PHI * PHI;      // ≈ 2.6180339887...

// Constantes mathématiques sacrées
export const SACRED_CONSTANTS = {
  PHI: PHI,
  PI: Math.PI,
  E: Math.E,
  SQRT2: Math.SQRT2,
  SQRT3: Math.sqrt(3),
  SQRT5: Math.sqrt(5)
};

// Suite de Fibonacci (premiers 21 nombres)
export const FIBONACCI = [
  0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765
];

// ═══════════════════════════════════════════════════════════════════════════════
// GÉOMÉTRIE SACRÉE - LES FORMES FONDAMENTALES
// ═══════════════════════════════════════════════════════════════════════════════

export const SACRED_GEOMETRY = {
  VESICA_PISCIS: {
    name: "Vesica Piscis",
    meaning: "Vessie du Poisson",
    description: "L'intersection de deux cercles de même rayon - matrice de la création",
    frequency: 222, // Dualité
    ratio: Math.sqrt(3),
    vertices: 2,
    symbolism: ["naissance", "vulve cosmique", "passage", "dualité"],
    construction: "Deux cercles dont le centre de chacun est sur la circonférence de l'autre"
  },
  
  SEED_OF_LIFE: {
    name: "Graine de Vie",
    meaning: "Les 7 Jours de la Création",
    description: "7 cercles interconnectés formant un motif hexagonal",
    frequency: 777,
    circles: 7,
    symbolism: ["création", "genèse", "7 jours", "début"],
    construction: "6 cercles autour d'un cercle central, tous de même rayon"
  },
  
  FLOWER_OF_LIFE: {
    name: "Fleur de Vie",
    meaning: "Le Modèle de l'Univers",
    description: "19 cercles interconnectés - contient tous les modèles de création",
    frequency: 666, // Harmonie parfaite
    circles: 19,
    symbolism: ["univers", "ADN", "création", "interconnexion"],
    contains: ["Vesica Piscis", "Seed of Life", "Egg of Life", "Fruit of Life"],
    arithmos: 6,
    construction: "Extension de la Graine de Vie avec 12 cercles supplémentaires"
  },
  
  FRUIT_OF_LIFE: {
    name: "Fruit de Vie",
    meaning: "Le Plan de l'Univers",
    description: "13 cercles formant le modèle de tout ce qui existe",
    frequency: 444,
    circles: 13,
    symbolism: ["structure atomique", "réalité", "forme"],
    leads_to: "Metatron's Cube"
  },
  
  METATRONS_CUBE: {
    name: "Cube de Métatron",
    meaning: "Le Conteneur de Toute Chose",
    description: "Tous les solides de Platon sont contenus dans ce motif",
    frequency: 999,
    vertices: 13,
    lines: 78, // Toutes les connexions possibles entre 13 points
    symbolism: ["création", "solides platoniciens", "géométrie universelle"],
    contains: ["Tetrahedron", "Cube", "Octahedron", "Icosahedron", "Dodecahedron"],
    arithmos: 9
  },
  
  SRI_YANTRA: {
    name: "Sri Yantra",
    meaning: "Instrument de la Richesse",
    description: "9 triangles entrelacés - la représentation du cosmos",
    frequency: 999,
    triangles: 9,
    points: 43,
    symbolism: ["shakti", "shiva", "création", "cosmos"],
    arithmos: 9
  },
  
  MERKABA: {
    name: "Merkaba",
    meaning: "Chariot de Lumière",
    description: "Deux tétraèdres entrelacés - le véhicule de l'ascension",
    frequency: 888,
    vertices: 8,
    faces: 8,
    symbolism: ["ascension", "véhicule spirituel", "protection"],
    rotation: "Contre-rotation des deux tétraèdres"
  },
  
  TORUS: {
    name: "Tore",
    meaning: "Le Flux Universel",
    description: "La forme fondamentale de l'énergie dans l'univers",
    frequency: 444,
    symbolism: ["flux", "énergie", "auto-organisation", "cœur"],
    appears_in: ["atomes", "galaxies", "champ magnétique terrestre", "cœur humain"]
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 5 SOLIDES DE PLATON
// ═══════════════════════════════════════════════════════════════════════════════

export const PLATONIC_SOLIDS = {
  TETRAHEDRON: {
    name: "Tétraèdre",
    faces: 4,
    vertices: 4,
    edges: 6,
    element: "Feu",
    color: "#FF0000",
    frequency: 555,
    chakra: 3, // Manipura
    symbolism: "Transformation, aspiration, élévation"
  },
  
  CUBE: {
    name: "Hexaèdre (Cube)",
    faces: 6,
    vertices: 8,
    edges: 12,
    element: "Terre",
    color: "#8B4513",
    frequency: 111,
    chakra: 1, // Muladhara
    symbolism: "Stabilité, fondation, manifestation"
  },
  
  OCTAHEDRON: {
    name: "Octaèdre",
    faces: 8,
    vertices: 6,
    edges: 12,
    element: "Air",
    color: "#87CEEB",
    frequency: 444,
    chakra: 4, // Anahata
    symbolism: "Intégration, équilibre, amour"
  },
  
  DODECAHEDRON: {
    name: "Dodécaèdre",
    faces: 12,
    vertices: 20,
    edges: 30,
    element: "Éther/Univers",
    color: "#EE82EE",
    frequency: 999,
    chakra: 7, // Sahasrara
    symbolism: "Conscience cosmique, ascension"
  },
  
  ICOSAHEDRON: {
    name: "Icosaèdre",
    faces: 20,
    vertices: 12,
    edges: 30,
    element: "Eau",
    color: "#0000FF",
    frequency: 222,
    chakra: 2, // Svadhisthana
    symbolism: "Flux, transformation, émotion"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// MOTIFS CYMATIQUES PAR FRÉQUENCE
// ═══════════════════════════════════════════════════════════════════════════════

export const CYMATICS_PATTERNS = {
  111: {
    hz: 111,
    pattern: "Point central avec 1 anneau",
    nodes: 1,
    geometry: "Cercle simple",
    complexity: 1,
    description: "L'unité primordiale - le point de départ"
  },
  
  222: {
    hz: 222,
    pattern: "Vesica Piscis dynamique",
    nodes: 2,
    geometry: "Deux lobes en oscillation",
    complexity: 2,
    description: "La dualité en mouvement - yin/yang vibratoire"
  },
  
  333: {
    hz: 333,
    pattern: "Triangle vibrant",
    nodes: 3,
    geometry: "Forme triangulaire avec spirales",
    complexity: 3,
    description: "La trinité manifestée - stabilité dynamique"
  },
  
  444: {
    hz: 444,
    pattern: "Carré stabilisé",
    nodes: 4,
    geometry: "Croix avec cercles aux intersections",
    complexity: 4,
    description: "Les 4 directions - ancrage parfait"
  },
  
  555: {
    hz: 555,
    pattern: "Étoile pentagonale",
    nodes: 5,
    geometry: "Pentagramme avec spirales dorées",
    complexity: 5,
    description: "Le nombre de l'homme - le mouvement vital"
  },
  
  666: {
    hz: 666,
    pattern: "Fleur hexagonale",
    nodes: 6,
    geometry: "Hexagone avec 6 pétales - Fleur de Vie partielle",
    complexity: 6,
    description: "L'harmonie parfaite - structure cristalline"
  },
  
  777: {
    hz: 777,
    pattern: "Heptagone mystique",
    nodes: 7,
    geometry: "7 branches en rotation",
    complexity: 7,
    description: "Le nombre sacré - connexion spirituelle"
  },
  
  888: {
    hz: 888,
    pattern: "Double carré (Octogone)",
    nodes: 8,
    geometry: "Deux carrés superposés à 45°",
    complexity: 8,
    description: "L'infini manifesté - expansion sans limite"
  },
  
  999: {
    hz: 999,
    pattern: "Ennéagramme complet",
    nodes: 9,
    geometry: "9 points en cercle avec interconnexions internes",
    complexity: 9,
    description: "La complétude - retour à l'unité supérieure"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE CALCUL
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère les N premiers nombres de Fibonacci
 */
export function generateFibonacci(n) {
  const fib = [0, 1];
  for (let i = 2; i < n; i++) {
    fib.push(fib[i - 1] + fib[i - 2]);
  }
  return fib.slice(0, n);
}

/**
 * Vérifie si un nombre est dans la suite de Fibonacci
 */
export function isFibonacci(n) {
  // Un nombre est Fibonacci si 5n² + 4 ou 5n² - 4 est un carré parfait
  const isPerfectSquare = (x) => Math.sqrt(x) % 1 === 0;
  return isPerfectSquare(5 * n * n + 4) || isPerfectSquare(5 * n * n - 4);
}

/**
 * Calcule le ratio d'or entre deux nombres consécutifs
 */
export function calculateGoldenRatio(a, b) {
  if (a === 0) return 0;
  return b / a;
}

/**
 * Vérifie si un ratio est proche du nombre d'or
 */
export function isGoldenRatio(ratio, tolerance = 0.01) {
  return Math.abs(ratio - PHI) < tolerance;
}

/**
 * Calcule le "Taux de Vitalité" d'un concept
 * Plus le concept respecte le nombre d'or, plus il est "vivant"
 */
export function calculateVitalityRate(values) {
  if (values.length < 2) return 0;
  
  let goldenCount = 0;
  for (let i = 0; i < values.length - 1; i++) {
    const ratio = calculateGoldenRatio(values[i], values[i + 1]);
    if (isGoldenRatio(ratio, 0.1)) {
      goldenCount++;
    }
  }
  
  return goldenCount / (values.length - 1);
}

/**
 * Génère une spirale de Fibonacci (coordonnées)
 */
export function generateFibonacciSpiral(steps, scale = 1) {
  const points = [];
  const fib = generateFibonacci(steps + 2);
  
  for (let i = 0; i < steps; i++) {
    const angle = i * PHI * 2 * Math.PI; // Angle d'or
    const radius = fib[i + 2] * scale;
    
    points.push({
      x: Math.cos(angle) * radius,
      y: Math.sin(angle) * radius,
      radius: radius,
      angle: angle
    });
  }
  
  return points;
}

/**
 * Génère les points d'une Fleur de Vie
 */
export function generateFlowerOfLife(centerX, centerY, radius, layers = 2) {
  const circles = [];
  const angles = [0, 60, 120, 180, 240, 300];
  
  // Cercle central
  circles.push({ x: centerX, y: centerY, r: radius });
  
  // Première couche (6 cercles)
  for (const angle of angles) {
    const rad = (angle * Math.PI) / 180;
    circles.push({
      x: centerX + radius * Math.cos(rad),
      y: centerY + radius * Math.sin(rad),
      r: radius
    });
  }
  
  // Couches supplémentaires
  if (layers > 1) {
    for (let layer = 2; layer <= layers; layer++) {
      for (let i = 0; i < 6; i++) {
        const baseAngle = (i * 60 * Math.PI) / 180;
        for (let j = 0; j < layer; j++) {
          const distance = radius * layer;
          const subAngle = baseAngle + (j * Math.PI / 3 / layer);
          circles.push({
            x: centerX + distance * Math.cos(subAngle),
            y: centerY + distance * Math.sin(subAngle),
            r: radius
          });
        }
      }
    }
  }
  
  return circles;
}

/**
 * Génère les points du Cube de Métatron
 */
export function generateMetatronsCube(centerX, centerY, radius) {
  const points = [];
  
  // 13 points: 1 centre + 6 intérieur + 6 extérieur
  points.push({ x: centerX, y: centerY, type: 'center' });
  
  // Hexagone intérieur
  for (let i = 0; i < 6; i++) {
    const angle = (i * 60 - 90) * Math.PI / 180;
    points.push({
      x: centerX + radius * 0.5 * Math.cos(angle),
      y: centerY + radius * 0.5 * Math.sin(angle),
      type: 'inner'
    });
  }
  
  // Hexagone extérieur
  for (let i = 0; i < 6; i++) {
    const angle = (i * 60 - 60) * Math.PI / 180;
    points.push({
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
      type: 'outer'
    });
  }
  
  // Générer toutes les lignes (78 connexions)
  const lines = [];
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      lines.push({
        from: points[i],
        to: points[j]
      });
    }
  }
  
  return { points, lines };
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient le motif cymatique pour une fréquence AT·OM
 */
export function getCymaticsForFrequency(atomHz) {
  return CYMATICS_PATTERNS[atomHz] || CYMATICS_PATTERNS[444];
}

/**
 * Trouve la géométrie sacrée correspondant à un Arithmos
 */
export function getGeometryForArithmos(arithmos) {
  const mapping = {
    1: SACRED_GEOMETRY.SEED_OF_LIFE,
    2: SACRED_GEOMETRY.VESICA_PISCIS,
    3: PLATONIC_SOLIDS.TETRAHEDRON,
    4: PLATONIC_SOLIDS.CUBE,
    5: PLATONIC_SOLIDS.OCTAHEDRON,
    6: SACRED_GEOMETRY.FLOWER_OF_LIFE,
    7: SACRED_GEOMETRY.MERKABA,
    8: PLATONIC_SOLIDS.DODECAHEDRON,
    9: SACRED_GEOMETRY.METATRONS_CUBE
  };
  
  return mapping[arithmos] || SACRED_GEOMETRY.TORUS;
}

/**
 * Calcule la "signature géométrique" d'un mot
 */
export function calculateGeometricSignature(word, arithmos) {
  const cymatic = getCymaticsForFrequency(arithmos * 111);
  const geometry = getGeometryForArithmos(arithmos);
  
  // Calculer le taux de vitalité basé sur les valeurs des lettres
  const letterValues = word.toUpperCase().split('').map(c => {
    const val = c.charCodeAt(0) - 64;
    return val > 0 && val <= 26 ? val : 0;
  }).filter(v => v > 0);
  
  const vitalityRate = calculateVitalityRate(letterValues);
  const isOrganic = vitalityRate > 0.3;
  
  // Générer la spirale si organique
  const spiral = isOrganic ? generateFibonacciSpiral(arithmos * 2) : null;
  
  return {
    cymatic: cymatic,
    geometry: geometry,
    vitalityRate: vitalityRate,
    isOrganic: isOrganic,
    spiral: spiral,
    nodes: cymatic.nodes,
    complexity: cymatic.complexity,
    
    // Pour la visualisation
    primaryShape: geometry.name || geometry.geometry,
    symbolism: geometry.symbolism,
    element: PLATONIC_SOLIDS[Object.keys(PLATONIC_SOLIDS).find(k => 
      PLATONIC_SOLIDS[k].frequency === arithmos * 111
    )]?.element || "Éther"
  };
}

/**
 * Génère les données de visualisation cymatique animée
 */
export function generateCymaticAnimation(frequency, frames = 60) {
  const pattern = getCymaticsForFrequency(frequency);
  const nodes = pattern.nodes;
  
  const animation = [];
  for (let f = 0; f < frames; f++) {
    const phase = (f / frames) * 2 * Math.PI;
    const points = [];
    
    for (let i = 0; i < nodes; i++) {
      const angle = (i / nodes) * 2 * Math.PI;
      const radius = 50 + 20 * Math.sin(phase + angle * nodes);
      
      points.push({
        x: 100 + radius * Math.cos(angle),
        y: 100 + radius * Math.sin(angle),
        intensity: 0.5 + 0.5 * Math.sin(phase + angle)
      });
    }
    
    animation.push({
      frame: f,
      points: points,
      phase: phase
    });
  }
  
  return {
    pattern: pattern,
    animation: animation,
    duration: 2000, // 2 secondes par cycle
    loop: true
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Constantes
  PHI,
  PHI_INVERSE,
  FIBONACCI,
  SACRED_CONSTANTS,
  
  // Géométrie
  SACRED_GEOMETRY,
  PLATONIC_SOLIDS,
  CYMATICS_PATTERNS,
  
  // Fonctions
  generateFibonacci,
  isFibonacci,
  calculateGoldenRatio,
  isGoldenRatio,
  calculateVitalityRate,
  generateFibonacciSpiral,
  generateFlowerOfLife,
  generateMetatronsCube,
  
  // Intégration AT·OM
  getCymaticsForFrequency,
  getGeometryForArithmos,
  calculateGeometricSignature,
  generateCymaticAnimation
};
