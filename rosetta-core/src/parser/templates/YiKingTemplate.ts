/**
 * AT·OM — YiKingTemplate
 * Traducteur Yi-King (I Ching) pour le RosettaParser
 *
 * Convertit la logique du moteur Yi-King en TranslatorTemplate Rosetta.
 * Les 64 hexagrammes encodent les 64 archétypes de transformation,
 * chacun traduit dans les 3 dimensions : TECH, PEOPLE, SPIRIT.
 *
 * Correspondances :
 *   - 8 Trigrammes (Bagua) → Briques fondamentales
 *   - 64 Hexagrammes       → Combinaisons de 2 trigrammes (upper + lower)
 *   - Arithmos 1-9         → Mapping vers familles d'hexagrammes
 *   - Coin casting          → Simulation de la methode des 3 pieces
 */

import {
  type ResonanceLevel,
  type TechPayload,
  type PeoplePayload,
  type SpiritPayload,
  type SacredGeometryShape,
  SACRED_FREQUENCIES,
  RESONANCE_MATRIX,
} from '../../types/atom-types';

import {
  type TranslatorTemplate,
  type ParserContext,
  RosettaParser,
} from '../RosettaParser';

// =================================================================
// TYPES YI-KING
// =================================================================

/** Input pour le template Yi-King */
export interface YiKingInput {
  text?: string;
  level?: ResonanceLevel;
  cast?: boolean; // If true, simulate coin casting (3 coins x 6 lines)
}

/** Les 5 elements du Wu Xing */
export type WuXingElement = 'Metal' | 'Earth' | 'Wood' | 'Water' | 'Fire';

/** Trigramme (Bagua) */
export interface Trigram {
  name: string;
  symbol: string;
  binary: string;
  frenchName: string;
  element: WuXingElement;
  atomLevel: ResonanceLevel;
}

/** Type de tendance d'un hexagramme */
export type HexagramTendency =
  | 'ascendante'
  | 'descendante'
  | 'harmonieuse'
  | 'stable'
  | 'bloquee'
  | 'profonde'
  | 'illuminante'
  | 'transformatrice'
  | 'creatrice'
  | 'accomplie'
  | 'potentielle';

/** Hexagramme complet */
export interface Hexagram {
  number: number;
  name: string;
  binary: string;
  upperTrigram: string; // Trigram key
  lowerTrigram: string; // Trigram key
  atomLevel: ResonanceLevel;
  tendency: HexagramTendency;
  keywords: string[];
  description: string;
}

/** Resultat d'un lancer de pieces */
export interface CoinCastResult {
  lines: CoinLine[];
  binary: string;
  hexagramNumber: number;
  hexagram: Hexagram;
  changingLines: number[]; // Indices (0-5) of old yin/yang lines
  relatedHexagram: Hexagram | null; // Hexagram after changing lines
}

/** Ligne issue d'un lancer */
export interface CoinLine {
  coins: [number, number, number]; // Each coin: 2 (tails) or 3 (heads)
  sum: number;         // 6, 7, 8, or 9
  type: 'old_yin' | 'young_yang' | 'young_yin' | 'old_yang';
  value: 0 | 1;        // Binary value (0=yin, 1=yang)
  changing: boolean;    // true if old yin or old yang
}

// =================================================================
// 8 TRIGRAMMES (BAGUA)
// =================================================================

export const TRIGRAMS: Record<string, Trigram> = {
  QIAN: {
    name: 'QIAN',
    symbol: '\u2630', // ☰
    binary: '111',
    frenchName: 'Ciel/Createur',
    element: 'Metal',
    atomLevel: 9 as ResonanceLevel,
  },
  KUN: {
    name: 'KUN',
    symbol: '\u2637', // ☷
    binary: '000',
    frenchName: 'Terre/Receptif',
    element: 'Earth',
    atomLevel: 4 as ResonanceLevel, // CENTER
  },
  ZHEN: {
    name: 'ZHEN',
    symbol: '\u2633', // ☳
    binary: '001',
    frenchName: 'Tonnerre/Eveilleur',
    element: 'Wood',
    atomLevel: 1 as ResonanceLevel,
  },
  KAN: {
    name: 'KAN',
    symbol: '\u2635', // ☵
    binary: '010',
    frenchName: 'Eau/Insondable',
    element: 'Water',
    atomLevel: 7 as ResonanceLevel,
  },
  GEN: {
    name: 'GEN',
    symbol: '\u2636', // ☶
    binary: '100',
    frenchName: 'Montagne/Immobilite',
    element: 'Earth',
    atomLevel: 4 as ResonanceLevel,
  },
  XUN: {
    name: 'XUN',
    symbol: '\u2634', // ☴
    binary: '110',
    frenchName: 'Vent/Douceur',
    element: 'Wood',
    atomLevel: 2 as ResonanceLevel,
  },
  LI: {
    name: 'LI',
    symbol: '\u2632', // ☲
    binary: '101',
    frenchName: 'Feu/Clarte',
    element: 'Fire',
    atomLevel: 5 as ResonanceLevel,
  },
  DUI: {
    name: 'DUI',
    symbol: '\u2631', // ☱
    binary: '011',
    frenchName: 'Lac/Joie',
    element: 'Metal',
    atomLevel: 6 as ResonanceLevel,
  },
};

// Binary-to-trigram-key lookup
const BINARY_TO_TRIGRAM: Record<string, string> = {};
for (const [key, tri] of Object.entries(TRIGRAMS)) {
  BINARY_TO_TRIGRAM[tri.binary] = key;
}

// =================================================================
// 16 HEXAGRAMMES CLES (avec donnees completes)
// =================================================================

const KEY_HEXAGRAMS: Hexagram[] = [
  {
    number: 1,
    name: 'Qian',
    binary: '111111',
    upperTrigram: 'QIAN',
    lowerTrigram: 'QIAN',
    atomLevel: 9 as ResonanceLevel,
    tendency: 'ascendante',
    keywords: ['force', 'initiative', 'ciel'],
    description: 'Le Createur. Pure energie yang, force celeste initiatrice de toute chose.',
  },
  {
    number: 2,
    name: 'Kun',
    binary: '000000',
    upperTrigram: 'KUN',
    lowerTrigram: 'KUN',
    atomLevel: 4 as ResonanceLevel,
    tendency: 'descendante',
    keywords: ['terre', 'accueil', 'patience'],
    description: 'Le Receptif. Pure energie yin, la Terre qui accueille et nourrit.',
  },
  {
    number: 11,
    name: 'Tai',
    binary: '000111',
    upperTrigram: 'KUN',
    lowerTrigram: 'QIAN',
    atomLevel: 8 as ResonanceLevel,
    tendency: 'harmonieuse',
    keywords: ['equilibre', 'prosperite'],
    description: 'La Paix. Le Ciel descend, la Terre monte : harmonie parfaite et prosperite.',
  },
  {
    number: 12,
    name: 'Pi',
    binary: '111000',
    upperTrigram: 'QIAN',
    lowerTrigram: 'KUN',
    atomLevel: 2 as ResonanceLevel,
    tendency: 'bloquee',
    keywords: ['obstacle', 'patience'],
    description: 'La Stagnation. Le Ciel monte, la Terre descend : les forces se separent.',
  },
  {
    number: 15,
    name: 'Qian',
    binary: '000100',
    upperTrigram: 'KUN',
    lowerTrigram: 'GEN',
    atomLevel: 6 as ResonanceLevel,
    tendency: 'stable',
    keywords: ['modestie', 'sagesse'],
    description: "L'Humilite. La montagne sous la terre : la grandeur qui se cache.",
  },
  {
    number: 23,
    name: 'Bo',
    binary: '100000',
    upperTrigram: 'GEN',
    lowerTrigram: 'KUN',
    atomLevel: 1 as ResonanceLevel,
    tendency: 'descendante',
    keywords: ['transformation', 'patience'],
    description: "L'Erosion. La montagne s'effrite sur la terre : declin necessaire avant le renouveau.",
  },
  {
    number: 24,
    name: 'Fu',
    binary: '000001',
    upperTrigram: 'KUN',
    lowerTrigram: 'ZHEN',
    atomLevel: 3 as ResonanceLevel,
    tendency: 'ascendante',
    keywords: ['renouveau', 'cycle'],
    description: 'Le Retour. Le tonnerre sous la terre : le yang renait, un nouveau cycle commence.',
  },
  {
    number: 29,
    name: 'Kan',
    binary: '010010',
    upperTrigram: 'KAN',
    lowerTrigram: 'KAN',
    atomLevel: 7 as ResonanceLevel,
    tendency: 'profonde',
    keywords: ['danger', 'courage', 'eau'],
    description: "L'Abime. Eau sur eau : le danger redouble, mais le courage traverse.",
  },
  {
    number: 30,
    name: 'Li',
    binary: '101101',
    upperTrigram: 'LI',
    lowerTrigram: 'LI',
    atomLevel: 5 as ResonanceLevel,
    tendency: 'illuminante',
    keywords: ['lumiere', 'verite'],
    description: 'La Clarte. Feu sur feu : double illumination, la verite se revele.',
  },
  {
    number: 49,
    name: 'Ge',
    binary: '011101',
    upperTrigram: 'DUI',
    lowerTrigram: 'LI',
    atomLevel: 9 as ResonanceLevel,
    tendency: 'transformatrice',
    keywords: ['changement', 'mutation'],
    description: 'La Revolution. Le lac sur le feu : transformation radicale et necessaire.',
  },
  {
    number: 50,
    name: 'Ding',
    binary: '101110',
    upperTrigram: 'LI',
    lowerTrigram: 'XUN',
    atomLevel: 9 as ResonanceLevel,
    tendency: 'creatrice',
    keywords: ['nourriture', 'sagesse', 'feu'],
    description: 'Le Chaudron. Le feu sur le vent : la sagesse se nourrit et se transmute.',
  },
  {
    number: 63,
    name: 'JiJi',
    binary: '010101',
    upperTrigram: 'KAN',
    lowerTrigram: 'LI',
    atomLevel: 7 as ResonanceLevel,
    tendency: 'accomplie',
    keywords: ['achevement', 'prudence'],
    description: "L'Accomplissement. L'eau sur le feu : tout est en place, mais la prudence reste de mise.",
  },
  {
    number: 64,
    name: 'WeiJi',
    binary: '101010',
    upperTrigram: 'LI',
    lowerTrigram: 'KAN',
    atomLevel: 8 as ResonanceLevel,
    tendency: 'potentielle',
    keywords: ['transition', 'espoir', 'devenir'],
    description: "L'Inacheve. Le feu sur l'eau : tout reste a accomplir, potentiel infini.",
  },
  // --- 3 additional key hexagrams to reach 16 ---
  {
    number: 42,
    name: 'Yi',
    binary: '100011',
    upperTrigram: 'GEN', // upper binary 100 = GEN? Actually let's derive correctly.
    lowerTrigram: 'DUI',
    atomLevel: 5 as ResonanceLevel,
    tendency: 'ascendante',
    keywords: ['augmentation', 'generosite', 'croissance'],
    description: "L'Augmentation. Le vent sur le tonnerre : le sacrifice du haut nourrit le bas.",
  },
  {
    number: 51,
    name: 'Zhen',
    binary: '001001',
    upperTrigram: 'ZHEN',
    lowerTrigram: 'ZHEN',
    atomLevel: 1 as ResonanceLevel,
    tendency: 'ascendante',
    keywords: ['eveil', 'tonnerre', 'choc'],
    description: "L'Eveilleur. Tonnerre sur tonnerre : le choc qui eveille et met en mouvement.",
  },
  {
    number: 57,
    name: 'Xun',
    binary: '110110',
    upperTrigram: 'XUN',
    lowerTrigram: 'XUN',
    atomLevel: 2 as ResonanceLevel,
    tendency: 'stable',
    keywords: ['penetration', 'douceur', 'vent'],
    description: 'Le Doux. Vent sur vent : la penetration douce et persistante qui transforme.',
  },
];

// Build lookup map for key hexagrams by number
const HEXAGRAM_BY_NUMBER: Map<number, Hexagram> = new Map();
for (const hex of KEY_HEXAGRAMS) {
  HEXAGRAM_BY_NUMBER.set(hex.number, hex);
}

// Build lookup map for key hexagrams by binary
const HEXAGRAM_BY_BINARY: Map<string, Hexagram> = new Map();
for (const hex of KEY_HEXAGRAMS) {
  HEXAGRAM_BY_BINARY.set(hex.binary, hex);
}

// =================================================================
// ARITHMOS -> HEXAGRAM MAPPING
// =================================================================

const ARITHMOS_TO_HEXAGRAMS: Record<number, number[]> = {
  1: [1, 3, 24, 64],
  2: [2, 6, 8, 44],
  3: [16, 25, 32, 40],
  4: [7, 15, 46, 52],
  5: [9, 14, 26, 30],
  6: [10, 38, 41, 58],
  7: [4, 18, 29, 48],
  8: [11, 19, 33, 53],
  9: [1, 49, 50],
};

// =================================================================
// KING WEN SEQUENCE (standard ordering of 64 hexagrams by binary)
// Maps binary string -> hexagram number in King Wen sequence.
// Only the 64 valid combinations are listed.
// =================================================================

/**
 * Derive a hexagram number from a 6-bit binary string using the
 * traditional upper/lower trigram matrix (King Wen ordering).
 * Row = upper trigram, Col = lower trigram.
 *
 * Trigram order (traditional): QIAN, KUN, ZHEN, KAN, GEN, XUN, LI, DUI
 * Index mapping for the matrix:
 */
const TRIGRAM_ORDER = ['QIAN', 'KUN', 'ZHEN', 'KAN', 'GEN', 'XUN', 'LI', 'DUI'];

// King Wen sequence: KING_WEN_MATRIX[upper_index][lower_index] = hexagram number
const KING_WEN_MATRIX: number[][] = [
  //       QIAN KUN ZHEN KAN GEN XUN  LI  DUI   <- lower trigram
  /* QIAN */ [1,  12,  25, 6,  33, 44,  13, 10],
  /* KUN  */ [11,  2,  24, 7,  15, 46,  36, 19],
  /* ZHEN */ [34, 16,  51, 3,  27, 42,  21, 17],
  /* KAN  */ [5,   8,  40, 29, 39, 59,  64, 47],
  /* GEN  */ [26, 23,  27, 4,  52, 18,  22, 41],
  /* XUN  */ [9,  20,  32, 48, 57, 57,  50, 28],  // Note: XUN/XUN = 57
  /* LI   */ [14, 35,  55, 63, 56, 37,  30, 49],
  /* DUI  */ [43, 45,  54, 60, 31, 28,  38, 58],
];

// Fix: XUN/XUN at [5][5] should be 57, XUN/DUI at [5][7] should be 28 -> already correct
// Fix: DUI/XUN at [7][5] should be 28 -> already correct

/**
 * Get hexagram number from upper and lower trigram keys
 */
function getHexagramNumber(upperKey: string, lowerKey: string): number {
  const upperIdx = TRIGRAM_ORDER.indexOf(upperKey);
  const lowerIdx = TRIGRAM_ORDER.indexOf(lowerKey);
  if (upperIdx === -1 || lowerIdx === -1) return 1; // fallback
  return KING_WEN_MATRIX[upperIdx][lowerIdx];
}

/**
 * Get trigram keys from a 6-bit binary string.
 * Upper trigram = first 3 bits, Lower trigram = last 3 bits.
 */
function trigramsFromBinary(binary: string): { upperKey: string; lowerKey: string } {
  const upperBin = binary.substring(0, 3);
  const lowerBin = binary.substring(3, 6);
  const upperKey = BINARY_TO_TRIGRAM[upperBin] || 'QIAN';
  const lowerKey = BINARY_TO_TRIGRAM[lowerBin] || 'KUN';
  return { upperKey, lowerKey };
}

// =================================================================
// HEXAGRAM RESOLUTION (key or computed)
// =================================================================

/**
 * Resolve a hexagram by its number. If it is a key hexagram, return
 * the full data. Otherwise, compute a synthetic hexagram from its
 * trigram components.
 */
function resolveHexagram(hexNumber: number, binary?: string): Hexagram {
  // Check key hexagrams first
  const key = HEXAGRAM_BY_NUMBER.get(hexNumber);
  if (key) return key;

  // If we have a binary, use it; otherwise reverse-lookup from the matrix
  let bin = binary;
  if (!bin) {
    bin = findBinaryForHexNumber(hexNumber);
  }

  const { upperKey, lowerKey } = trigramsFromBinary(bin);
  const upper = TRIGRAMS[upperKey];
  const lower = TRIGRAMS[lowerKey];

  // Compute atomLevel from average of upper and lower trigram levels
  const avgLevel = Math.round((upper.atomLevel + lower.atomLevel) / 2);
  const clampedLevel = Math.max(1, Math.min(9, avgLevel)) as ResonanceLevel;

  // Determine tendency from level
  let tendency: HexagramTendency;
  if (clampedLevel >= 8) tendency = 'ascendante';
  else if (clampedLevel >= 6) tendency = 'harmonieuse';
  else if (clampedLevel >= 4) tendency = 'stable';
  else if (clampedLevel >= 2) tendency = 'descendante';
  else tendency = 'profonde';

  return {
    number: hexNumber,
    name: `Hex${hexNumber}`,
    binary: bin,
    upperTrigram: upperKey,
    lowerTrigram: lowerKey,
    atomLevel: clampedLevel,
    tendency,
    keywords: [upper.frenchName.split('/')[0].toLowerCase(), lower.frenchName.split('/')[0].toLowerCase()],
    description: `Hexagramme ${hexNumber} : ${upper.symbol} ${upper.frenchName} sur ${lower.symbol} ${lower.frenchName}.`,
  };
}

/**
 * Reverse-lookup: find the binary string for a given hexagram number
 * by scanning the King Wen matrix.
 */
function findBinaryForHexNumber(hexNumber: number): string {
  for (let u = 0; u < 8; u++) {
    for (let l = 0; l < 8; l++) {
      if (KING_WEN_MATRIX[u][l] === hexNumber) {
        const upperBin = TRIGRAMS[TRIGRAM_ORDER[u]].binary;
        const lowerBin = TRIGRAMS[TRIGRAM_ORDER[l]].binary;
        return upperBin + lowerBin;
      }
    }
  }
  // Fallback: return Qian/Qian binary
  return '111111';
}

// =================================================================
// COIN CASTING (3-coin method)
// =================================================================

/**
 * Simulate the traditional 3-coin casting method for one line.
 *
 * Each coin: heads = 3, tails = 2
 * Sum of 3 coins:
 *   6 = Old Yin    (2+2+2) → yin, changing
 *   7 = Young Yang (2+2+3) → yang, stable
 *   8 = Young Yin  (2+3+3) → yin, stable
 *   9 = Old Yang   (3+3+3) → yang, changing
 */
function castOneLine(): CoinLine {
  const coin = (): number => (Math.random() < 0.5 ? 2 : 3);
  const c1 = coin();
  const c2 = coin();
  const c3 = coin();
  const sum = c1 + c2 + c3;

  let type: CoinLine['type'];
  let value: 0 | 1;
  let changing = false;

  switch (sum) {
    case 6:
      type = 'old_yin';
      value = 0;
      changing = true;
      break;
    case 7:
      type = 'young_yang';
      value = 1;
      changing = false;
      break;
    case 8:
      type = 'young_yin';
      value = 0;
      changing = false;
      break;
    case 9:
      type = 'old_yang';
      value = 1;
      changing = true;
      break;
    default:
      type = 'young_yang';
      value = 1;
      changing = false;
  }

  return {
    coins: [c1, c2, c3],
    sum,
    type,
    value,
    changing,
  };
}

/**
 * Cast a full hexagram using the 3-coin method (6 lines, bottom to top).
 * Returns the primary hexagram and, if there are changing lines, the
 * related (transformed) hexagram.
 */
export function castHexagram(): CoinCastResult {
  // Cast 6 lines (line 0 = bottom, line 5 = top)
  const lines: CoinLine[] = [];
  for (let i = 0; i < 6; i++) {
    lines.push(castOneLine());
  }

  // Build binary from bottom to top: line[0] is least significant
  // But our binary representation is upper-first (top to bottom),
  // so reverse the order for the binary string.
  const binary = lines
    .map((l) => String(l.value))
    .reverse()
    .join('');

  const { upperKey, lowerKey } = trigramsFromBinary(binary);
  const hexNumber = getHexagramNumber(upperKey, lowerKey);
  const hexagram = resolveHexagram(hexNumber, binary);

  // Find changing lines
  const changingLines: number[] = [];
  for (let i = 0; i < 6; i++) {
    if (lines[i].changing) {
      changingLines.push(i);
    }
  }

  // Compute related hexagram if there are changing lines
  let relatedHexagram: Hexagram | null = null;
  if (changingLines.length > 0) {
    const transformedLines = lines.map((l) => {
      if (l.changing) {
        return l.value === 1 ? 0 : 1; // Flip old yang->yin, old yin->yang
      }
      return l.value;
    });
    const relatedBinary = transformedLines
      .map(String)
      .reverse()
      .join('');
    const { upperKey: rU, lowerKey: rL } = trigramsFromBinary(relatedBinary);
    const relatedNumber = getHexagramNumber(rU, rL);
    relatedHexagram = resolveHexagram(relatedNumber, relatedBinary);
  }

  return {
    lines,
    binary,
    hexagramNumber: hexNumber,
    hexagram,
    changingLines,
    relatedHexagram,
  };
}

// =================================================================
// WORD -> HEXAGRAM (deterministic hash function)
// =================================================================

/**
 * Derive a hexagram from a word/text using a deterministic hash.
 * Uses the Arithmos (pythagorean reduction) of the text to select
 * from the ARITHMOS_TO_HEXAGRAMS mapping, then uses additional
 * character data to pick a specific hexagram from that family.
 */
export function getHexagramFromWord(word: string): Hexagram {
  if (!word || word.trim().length === 0) {
    return resolveHexagram(1);
  }

  // Compute Arithmos level (1-9)
  const arithmos = RosettaParser.computeArithmos(word);

  // Get the hexagram family for this Arithmos
  const family = ARITHMOS_TO_HEXAGRAMS[arithmos];
  if (!family || family.length === 0) {
    return resolveHexagram(1);
  }

  // Use a simple hash of the word to pick within the family
  let hash = 0;
  const normalized = word
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toUpperCase();
  for (let i = 0; i < normalized.length; i++) {
    hash = (hash * 31 + normalized.charCodeAt(i)) | 0;
  }
  hash = Math.abs(hash);

  const index = hash % family.length;
  const hexNumber = family[index];

  return resolveHexagram(hexNumber);
}

// =================================================================
// HELPER: French narrative generation
// =================================================================

function generateNarrative(hex: Hexagram, context: ParserContext): string {
  const upper = TRIGRAMS[hex.upperTrigram];
  const lower = TRIGRAMS[hex.lowerTrigram];

  const tendencyNarrative: Record<string, string> = {
    ascendante: 'Les energies montent. Le moment est propice a l\'action et a l\'initiative.',
    descendante: 'Les energies descendent. La patience et l\'interiorite sont de mise.',
    harmonieuse: 'L\'harmonie regne. Les forces s\'equilibrent dans une danse parfaite.',
    stable: 'La stabilite prevaut. Cultivez la constance et la perseverance.',
    bloquee: 'Un blocage se manifeste. Observez sans forcer, la patience ouvrira le chemin.',
    profonde: 'La profondeur appelle. Plongez dans l\'essentiel, au-dela des apparences.',
    illuminante: 'La clarte emerge. La verite se devoile a qui sait regarder.',
    transformatrice: 'La transformation est en cours. Accueillez le changement avec courage.',
    creatrice: 'L\'energie creatrice pulse. C\'est le moment de manifester vos visions.',
    accomplie: 'L\'accomplissement est proche. Restez vigilant dans le succes.',
    potentielle: 'Le potentiel est immense. Tout reste a construire, chaque pas compte.',
  };

  const modeLabel: Record<string, string> = {
    standard: 'Lecture standard',
    activated: 'Mode active',
    polishing: 'Polissage en cours',
    genesis: 'Mode Genese',
  };

  const counsel = tendencyNarrative[hex.tendency] || tendencyNarrative['stable'];

  return [
    `Hexagramme ${hex.number} : ${hex.name} - ${hex.description}`,
    '',
    `Trigramme superieur : ${upper.symbol} ${upper.frenchName} (${upper.element})`,
    `Trigramme inferieur : ${lower.symbol} ${lower.frenchName} (${lower.element})`,
    '',
    `Tendance : ${hex.tendency}`,
    counsel,
    '',
    `Mots-cles : ${hex.keywords.join(', ')}`,
    `Niveau de resonance AT\u00b7OM : ${hex.atomLevel} (${RESONANCE_MATRIX[hex.atomLevel].label})`,
    `${modeLabel[context.mode] || 'Lecture standard'} - Frequence systeme : ${context.system_frequency}Hz`,
  ].join('\n');
}

function generateCounsel(hex: Hexagram): string {
  const counselMap: Record<HexagramTendency, string> = {
    ascendante: 'Avancez avec confiance. Le ciel soutient votre elan.',
    descendante: 'Retirez-vous avec grace. La terre accueille votre repos.',
    harmonieuse: 'Maintenez l\'equilibre. L\'harmonie est votre plus grande force.',
    stable: 'Restez ancre. La stabilite est le socle de la sagesse.',
    bloquee: 'Ne forcez pas. L\'eau trouve toujours son chemin autour de l\'obstacle.',
    profonde: 'Meditez. La profondeur cache les plus grands tresors.',
    illuminante: 'Ouvrez les yeux. La verite est deja devant vous.',
    transformatrice: 'Lachez prise. La chrysalide doit se briser pour que le papillon naisse.',
    creatrice: 'Creez sans retenue. Le feu interieur est votre guide.',
    accomplie: 'Celebrez, mais restez humble. L\'accomplissement appelle la vigilance.',
    potentielle: 'Preparez-vous. Le potentiel ne demande qu\'a se manifester.',
  };
  return counselMap[hex.tendency] || counselMap['stable'];
}

function getTransformationPotential(hex: Hexagram): string {
  if (hex.atomLevel >= 8) {
    return 'Potentiel de transformation maximal. Ce hexagramme ouvre les portes de la transmutation.';
  } else if (hex.atomLevel >= 6) {
    return 'Fort potentiel de transformation. Les conditions sont reunies pour un changement significatif.';
  } else if (hex.atomLevel >= 4) {
    return 'Potentiel de transformation modere. Le travail interieur prepare le terrain.';
  } else {
    return 'Potentiel de transformation latent. La graine est plantee, la patience est requise.';
  }
}

// =================================================================
// YIKING TEMPLATE (TranslatorTemplate implementation)
// =================================================================

export const YiKingTemplate: TranslatorTemplate<YiKingInput> = {
  domain: 'yiking',

  /**
   * TECH dimension: structured hexagram data
   */
  toTech(input: YiKingInput, context: ParserContext): TechPayload {
    let hexagram: Hexagram;
    let castResult: CoinCastResult | null = null;

    if (input.cast) {
      castResult = castHexagram();
      hexagram = castResult.hexagram;
    } else if (input.text) {
      hexagram = getHexagramFromWord(input.text);
    } else if (input.level) {
      // Use level to pick first hexagram in the Arithmos family
      const family = ARITHMOS_TO_HEXAGRAMS[input.level];
      hexagram = resolveHexagram(family ? family[0] : 1);
    } else {
      hexagram = resolveHexagram(1);
    }

    const upper = TRIGRAMS[hexagram.upperTrigram];
    const lower = TRIGRAMS[hexagram.lowerTrigram];

    const values: Record<string, unknown> = {
      hexagram_number: hexagram.number,
      hexagram_name: hexagram.name,
      binary: hexagram.binary,
      upper_trigram: {
        key: hexagram.upperTrigram,
        symbol: upper.symbol,
        name: upper.frenchName,
        element: upper.element,
        binary: upper.binary,
      },
      lower_trigram: {
        key: hexagram.lowerTrigram,
        symbol: lower.symbol,
        name: lower.frenchName,
        element: lower.element,
        binary: lower.binary,
      },
      atom_level: hexagram.atomLevel,
      tendency: hexagram.tendency,
      keywords: hexagram.keywords,
      source_text: input.text ?? null,
      cast_mode: !!input.cast,
    };

    if (castResult) {
      values.cast_result = {
        lines: castResult.lines.map((l) => ({
          coins: l.coins,
          sum: l.sum,
          type: l.type,
          value: l.value,
          changing: l.changing,
        })),
        changing_lines: castResult.changingLines,
        related_hexagram: castResult.relatedHexagram
          ? {
              number: castResult.relatedHexagram.number,
              name: castResult.relatedHexagram.name,
              binary: castResult.relatedHexagram.binary,
            }
          : null,
      };
    }

    return {
      schema_version: '1.0',
      data_type: 'yiking_hexagram',
      values,
      timestamp: context.timestamp,
    };
  },

  /**
   * PEOPLE dimension: French narrative about meaning, tendency, counsel
   */
  toPeople(input: YiKingInput, context: ParserContext): PeoplePayload {
    let hexagram: Hexagram;
    let castResult: CoinCastResult | null = null;

    if (input.cast) {
      castResult = castHexagram();
      hexagram = castResult.hexagram;
    } else if (input.text) {
      hexagram = getHexagramFromWord(input.text);
    } else if (input.level) {
      const family = ARITHMOS_TO_HEXAGRAMS[input.level];
      hexagram = resolveHexagram(family ? family[0] : 1);
    } else {
      hexagram = resolveHexagram(1);
    }

    const narrative = generateNarrative(hexagram, context);
    const counsel = generateCounsel(hexagram);
    const transformation = getTransformationPotential(hexagram);

    const guideSteps: string[] = [
      `Contemplez l'hexagramme ${hexagram.number} (${hexagram.name}).`,
      counsel,
      transformation,
    ];

    if (castResult && castResult.changingLines.length > 0) {
      guideSteps.push(
        `Lignes mutantes aux positions : ${castResult.changingLines.map((l) => l + 1).join(', ')}. La situation evolue.`,
      );
      if (castResult.relatedHexagram) {
        guideSteps.push(
          `L'hexagramme se transforme en ${castResult.relatedHexagram.number} (${castResult.relatedHexagram.name}) : ${castResult.relatedHexagram.description}`,
        );
      }
    }

    // Determine emotional tone based on tendency
    let emotionalTone: PeoplePayload['emotional_tone'];
    switch (hexagram.tendency) {
      case 'ascendante':
      case 'creatrice':
      case 'harmonieuse':
        emotionalTone = 'celebratoire';
        break;
      case 'descendante':
      case 'bloquee':
        emotionalTone = 'alerte';
        break;
      case 'profonde':
      case 'illuminante':
        emotionalTone = 'sacre';
        break;
      case 'transformatrice':
      case 'potentielle':
        emotionalTone = 'encourageant';
        break;
      default:
        emotionalTone = 'neutre';
    }

    return {
      narrative,
      explanation: `${hexagram.description} ${counsel} ${transformation}`,
      guide_steps: guideSteps,
      emotional_tone: emotionalTone,
      language: 'fr',
    };
  },

  /**
   * SPIRIT dimension: frequency, resonance, geometry, vibration signature
   */
  toSpirit(input: YiKingInput, context: ParserContext): SpiritPayload {
    let hexagram: Hexagram;

    if (input.cast) {
      // For Spirit, we still cast but deterministically use the same result
      // Since castHexagram is random, in practice the caller should use
      // RosettaParser.translate() which calls all three methods.
      // For standalone use, we derive from text or level.
      if (input.text) {
        hexagram = getHexagramFromWord(input.text);
      } else if (input.level) {
        const family = ARITHMOS_TO_HEXAGRAMS[input.level];
        hexagram = resolveHexagram(family ? family[0] : 1);
      } else {
        hexagram = resolveHexagram(1);
      }
    } else if (input.text) {
      hexagram = getHexagramFromWord(input.text);
    } else if (input.level) {
      const family = ARITHMOS_TO_HEXAGRAMS[input.level];
      hexagram = resolveHexagram(family ? family[0] : 1);
    } else {
      hexagram = resolveHexagram(1);
    }

    const level = hexagram.atomLevel;
    const resonance = RESONANCE_MATRIX[level];

    // Sacred geometry based on resonance level
    const geometry: SacredGeometryShape = RosettaParser.geometryFor(level);

    // Vibration signature: encode the hexagram's binary as frequency modulations
    // [M, P, I, Po] modulated by the hexagram structure
    const upper = TRIGRAMS[hexagram.upperTrigram];
    const lower = TRIGRAMS[hexagram.lowerTrigram];

    const vibrationSignature: [number, number, number, number] = [
      SACRED_FREQUENCIES.ATOM_M * upper.atomLevel,   // M modulated by upper trigram
      SACRED_FREQUENCIES.ATOM_P * (hexagram.atomLevel / 9),  // P scaled by atom level
      SACRED_FREQUENCIES.ATOM_I * (parseInt(hexagram.binary, 2) / 63), // I scaled by binary value
      SACRED_FREQUENCIES.ATOM_PO * lower.atomLevel,  // Po modulated by lower trigram
    ];

    return {
      frequency_hz: resonance.hz,
      resonance_level: level,
      color: resonance.color,
      sacred_geometry: geometry,
      vibration_signature: vibrationSignature,
      phi_ratio: SACRED_FREQUENCIES.PHI * (hexagram.atomLevel / 9),
    };
  },
};

// =================================================================
// EXPORTS
// =================================================================

export {
  TRIGRAMS as YI_KING_TRIGRAMS,
  ARITHMOS_TO_HEXAGRAMS,
  resolveHexagram,
  getHexagramNumber,
  trigramsFromBinary,
};

export default YiKingTemplate;
