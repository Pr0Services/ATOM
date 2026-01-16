/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 𓋹 EGYPT ENGINE — LA GÉOMÉTRIE PRIMORDIALE (HEKA)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Pour les Égyptiens, le mot et la forme ne font qu'un.
 * Ils apportent deux concepts algorithmiques majeurs:
 * 
 * 1. La Quadrature du Cercle — Transition Cercle ↔ Carré
 * 2. Les Canons de Proportion (Maât) — Équilibre universel
 * 3. L'Œil d'Horus (Oudjat) — Ordinateur fractionnaire
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @symbol 𓋹 (Ankh)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES SACRÉES ÉGYPTIENNES
// ═══════════════════════════════════════════════════════════════════════════════

// Le nombre d'or égyptien (ratio de la Grande Pyramide)
export const PYRAMID_RATIO = Math.sqrt(Math.PI / 2); // ≈ 1.2533
export const ROYAL_CUBIT = 0.5236; // mètres (π/6)
export const SACRED_RATIO = 22/7; // Approximation de π utilisée

// ═══════════════════════════════════════════════════════════════════════════════
// L'ŒIL D'HORUS (OUDJAT) — ORDINATEUR FRACTIONNAIRE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * L'Œil d'Horus est divisé en 6 parties, chacune représentant une fraction:
 * 
 *     ┌─────────────────────────────────┐
 *     │        𓂀 L'ŒIL D'HORUS          │
 *     │                                 │
 *     │   1/8 ──┐    ┌── 1/2            │
 *     │         │    │                  │
 *     │   1/16 ─┤    ├─ 1/4             │
 *     │         │    │                  │
 *     │   1/32 ─┤    ├─ 1/8             │
 *     │         │    │                  │
 *     │   1/64 ─┘    └─                 │
 *     │                                 │
 *     │   Total: 63/64 (1/64 = magie)   │
 *     └─────────────────────────────────┘
 */

export const EYE_OF_HORUS = {
  parts: [
    { name: "pupille", fraction: 1/2, sense: "pensée", hieroglyph: "𓂃" },
    { name: "sourcil", fraction: 1/4, sense: "ouïe", hieroglyph: "𓂂" },
    { name: "larme", fraction: 1/8, sense: "odorat", hieroglyph: "𓂄" },
    { name: "coin_interne", fraction: 1/16, sense: "vue", hieroglyph: "𓂅" },
    { name: "spirale", fraction: 1/32, sense: "goût", hieroglyph: "𓂆" },
    { name: "coin_externe", fraction: 1/64, sense: "toucher", hieroglyph: "𓂇" }
  ],
  total: 63/64, // La fraction manquante (1/64) représente la magie de Thoth
  magic_fraction: 1/64
};

/**
 * Calcule la précision Horus pour une valeur
 * Plus la valeur peut être exprimée en fractions de l'œil, plus elle est "pure"
 * @param {number} value - Valeur entre 0 et 1
 * @returns {Object} - Décomposition en fractions de l'œil
 */
export function calculateHorusPrecision(value) {
  const fractions = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64];
  const decomposition = [];
  let remainder = value;
  
  for (const frac of fractions) {
    if (remainder >= frac) {
      decomposition.push(frac);
      remainder -= frac;
    }
  }
  
  return {
    original: value,
    decomposition,
    sum: decomposition.reduce((a, b) => a + b, 0),
    remainder: remainder,
    purity: 1 - remainder, // Plus proche de 1 = plus pur
    hasMagic: remainder > 0 && remainder <= 1/64,
    parts: decomposition.map(f => EYE_OF_HORUS.parts.find(p => p.fraction === f)?.name)
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAÂT — LA BALANCE DE L'ÉQUILIBRE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * La déesse Maât représente l'équilibre cosmique.
 * Son symbole est la plume contre laquelle le cœur est pesé.
 */

export const MAAT = {
  symbol: "𓁦",
  name: "Maât",
  meaning: "Vérité, Justice, Équilibre Cosmique",
  featherWeight: 42, // Les 42 lois de Maât
  principles: [
    "Je n'ai pas commis d'injustice",
    "Je n'ai pas opprimé les pauvres",
    "Je n'ai pas fait pleurer",
    "Je n'ai pas menti",
    "Je n'ai pas été avide",
    "Je n'ai pas volé",
    "Je n'ai pas tué",
    "Je n'ai pas été cruel"
    // ... (42 principes au total)
  ]
};

/**
 * Calcule l'équilibre Maât entre plusieurs valeurs
 * @param {number[]} weights - Les poids à équilibrer
 * @returns {Object} - État de l'équilibre
 */
export function calculateMaatBalance(weights) {
  if (!weights || weights.length === 0) {
    return { balanced: true, deviation: 0 };
  }
  
  const total = weights.reduce((a, b) => a + b, 0);
  const average = total / weights.length;
  const variance = weights.reduce((sum, w) => sum + Math.pow(w - average, 2), 0) / weights.length;
  const deviation = Math.sqrt(variance);
  const normalizedDeviation = deviation / (average || 1);
  
  return {
    balanced: normalizedDeviation < 0.2,
    deviation: normalizedDeviation,
    total,
    average,
    variance,
    status: normalizedDeviation < 0.1 ? "Parfait" 
          : normalizedDeviation < 0.2 ? "Équilibré"
          : normalizedDeviation < 0.4 ? "Déséquilibré"
          : "Chaos",
    recommendation: normalizedDeviation > 0.2 
      ? `Recalibrer: écart de ${(normalizedDeviation * 100).toFixed(1)}%`
      : "Harmonie Maât respectée"
  };
}

/**
 * Recalibre automatiquement les données selon Maât
 */
export function rebalanceMaat(weights, targetSum = null) {
  if (!weights || weights.length === 0) return [];
  
  const currentTotal = weights.reduce((a, b) => a + b, 0);
  const target = targetSum || currentTotal;
  const idealWeight = target / weights.length;
  
  // Appliquer un lissage vers l'équilibre
  return weights.map(w => {
    const diff = idealWeight - w;
    return w + diff * 0.5; // 50% vers l'équilibre
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// LA QUADRATURE DU CERCLE — TRANSFORMATION ∞ → □
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * La Grande Pyramide encode la quadrature du cercle:
 * Périmètre de base ≈ Circonférence d'un cercle de rayon = hauteur
 */

export const QUADRATURE = {
  pyramidHeight: 146.6, // mètres (original)
  pyramidBase: 230.4,   // mètres (côté)
  ratio: 230.4 / 146.6, // ≈ 1.5716... (proche de π/2)
};

/**
 * Transforme une valeur circulaire en valeur carrée
 * @param {number} circleValue - Valeur dans l'espace circulaire
 * @returns {number} - Valeur dans l'espace carré
 */
export function circleToSquare(circleValue) {
  // Le cercle de périmètre 2πr devient un carré de côté πr/2
  return circleValue * (Math.PI / 4);
}

/**
 * Transforme une valeur carrée en valeur circulaire
 */
export function squareToCircle(squareValue) {
  return squareValue * (4 / Math.PI);
}

// ═══════════════════════════════════════════════════════════════════════════════
// LES DIEUX ÉGYPTIENS — RÔLES ALGORITHMIQUES
// ═══════════════════════════════════════════════════════════════════════════════

export const EGYPTIAN_GODS = {
  RA: {
    name: "Rê",
    symbol: "𓇳",
    role: "Processeur Central",
    domain: "Illumination, Calcul, Énergie",
    frequency: 999,
    color: "#FFD700"
  },
  THOTH: {
    name: "Thoth",
    symbol: "𓁟",
    role: "Base de Données",
    domain: "Écriture, Sagesse, Mémoire",
    frequency: 777,
    color: "#4B0082"
  },
  MAAT: {
    name: "Maât",
    symbol: "𓁦",
    role: "Validator",
    domain: "Équilibre, Justice, Vérité",
    frequency: 444,
    color: "#50C878"
  },
  ANUBIS: {
    name: "Anubis",
    symbol: "𓁢",
    role: "Garbage Collector",
    domain: "Mort, Transformation, Nettoyage",
    frequency: 111,
    color: "#000000"
  },
  HORUS: {
    name: "Horus",
    symbol: "𓅃",
    role: "Interface Utilisateur",
    domain: "Vision, Perception, Output",
    frequency: 666,
    color: "#0066CC"
  },
  OSIRIS: {
    name: "Osiris",
    symbol: "𓁹",
    role: "Système de Backup",
    domain: "Résurrection, Persistance, Archives",
    frequency: 333,
    color: "#006400"
  },
  ISIS: {
    name: "Isis",
    symbol: "𓁥",
    role: "Cryptographie",
    domain: "Magie, Secrets, Protection",
    frequency: 888,
    color: "#800080"
  },
  PTAH: {
    name: "Ptah",
    symbol: "𓁛",
    role: "Compiler",
    domain: "Création, Artisanat, Code",
    frequency: 555,
    color: "#0000FF"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// HIÉROGLYPHES NUMÉRIQUES
// ═══════════════════════════════════════════════════════════════════════════════

export const HIEROGLYPHS = {
  numbers: {
    1: "𓏺",
    10: "𓎆",
    100: "𓍢",
    1000: "𓆼",
    10000: "𓂭",
    100000: "𓆐",
    1000000: "𓁨"
  },
  concepts: {
    life: "𓋹", // Ankh
    stability: "𓊽", // Djed
    power: "𓌀", // Was
    truth: "𓁦", // Maât
    sun: "𓇳",
    moon: "𓇺",
    star: "𓇼",
    water: "𓈖",
    fire: "𓊪",
    air: "𓆄",
    earth: "𓇾"
  }
};

/**
 * Convertit un nombre en hiéroglyphes égyptiens
 */
export function numberToHieroglyphs(num) {
  const units = [1000000, 100000, 10000, 1000, 100, 10, 1];
  const glyphs = ['𓁨', '𓆐', '𓂭', '𓆼', '𓍢', '𓎆', '𓏺'];
  
  let result = '';
  let remaining = num;
  
  for (let i = 0; i < units.length; i++) {
    const count = Math.floor(remaining / units[i]);
    result += glyphs[i].repeat(count);
    remaining %= units[i];
  }
  
  return result || '𓏺';
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la résonance égyptienne pour AT·OM
 */
export function getEgyptianResonance(arithmos, frequency) {
  // Trouver le dieu correspondant à la fréquence
  const gods = Object.values(EGYPTIAN_GODS);
  const closestGod = gods.reduce((closest, god) => {
    return Math.abs(god.frequency - frequency) < Math.abs(closest.frequency - frequency)
      ? god : closest;
  });
  
  // Calculer la précision Horus
  const horusPrecision = calculateHorusPrecision(arithmos / 9);
  
  // Vérifier l'équilibre Maât
  const maatBalance = calculateMaatBalance([arithmos, 9 - arithmos]);
  
  return {
    // Dieu patron
    patron: closestGod,
    
    // Œil d'Horus (précision)
    horus: {
      precision: horusPrecision,
      parts: horusPrecision.parts,
      purity: horusPrecision.purity
    },
    
    // Balance de Maât
    maat: {
      balanced: maatBalance.balanced,
      status: maatBalance.status,
      deviation: maatBalance.deviation
    },
    
    // Hiéroglyphe du nombre
    hieroglyph: numberToHieroglyphs(frequency),
    
    // Quadrature
    quadrature: {
      circleValue: frequency,
      squareValue: circleToSquare(frequency)
    },
    
    // Symboles
    symbols: {
      life: HIEROGLYPHS.concepts.life,
      stability: HIEROGLYPHS.concepts.stability,
      element: arithmos <= 3 ? HIEROGLYPHS.concepts.fire
             : arithmos <= 6 ? HIEROGLYPHS.concepts.water
             : HIEROGLYPHS.concepts.air
    },
    
    // Message
    message: `${closestGod.symbol} ${closestGod.name} guide cette fréquence — ${maatBalance.status}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Constantes
  PYRAMID_RATIO,
  ROYAL_CUBIT,
  EYE_OF_HORUS,
  MAAT,
  QUADRATURE,
  EGYPTIAN_GODS,
  HIEROGLYPHS,
  
  // Fonctions
  calculateHorusPrecision,
  calculateMaatBalance,
  rebalanceMaat,
  circleToSquare,
  squareToCircle,
  numberToHieroglyphs,
  getEgyptianResonance
};
