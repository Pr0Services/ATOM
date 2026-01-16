/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * YI-KING ENGINE — Le Code Binaire Ancestral
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Le Yi-King (I-Ching) est le plus ancien système de sagesse binaire.
 * 64 Hexagrammes composés de 6 lignes (Yin ⚋ ou Yang ⚊)
 * 
 * Chaque hexagramme est un opérateur de transformation.
 * Où l'Arithmos montre CE QUI EST, le Yi-King montre CE QUI CHANGE.
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @system AT·OM Universal Resonance
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES 8 TRIGRAMMES FONDAMENTAUX
// ═══════════════════════════════════════════════════════════════════════════════

export const TRIGRAMS = {
  QIAN: {
    name: "Qian",
    meaning: "Le Créateur / Le Ciel",
    lines: [1, 1, 1], // Yang Yang Yang
    symbol: "☰",
    element: "Ciel",
    quality: "Force créatrice",
    direction: "Nord-Ouest",
    family: "Père",
    animal: "Dragon",
    body: "Tête",
    color: "#FFD700",
    arithmos: 1
  },
  KUN: {
    name: "Kun",
    meaning: "Le Réceptif / La Terre",
    lines: [0, 0, 0], // Yin Yin Yin
    symbol: "☷",
    element: "Terre",
    quality: "Réceptivité",
    direction: "Sud-Ouest",
    family: "Mère",
    animal: "Jument",
    body: "Ventre",
    color: "#8B4513",
    arithmos: 2
  },
  ZHEN: {
    name: "Zhen",
    meaning: "L'Éveilleur / Le Tonnerre",
    lines: [1, 0, 0], // Yang Yin Yin
    symbol: "☳",
    element: "Tonnerre",
    quality: "Mouvement",
    direction: "Est",
    family: "Fils aîné",
    animal: "Dragon",
    body: "Pieds",
    color: "#FFFF00",
    arithmos: 3
  },
  XUN: {
    name: "Xun",
    meaning: "Le Doux / Le Vent",
    lines: [0, 1, 1], // Yin Yang Yang
    symbol: "☴",
    element: "Vent/Bois",
    quality: "Pénétration",
    direction: "Sud-Est",
    family: "Fille aînée",
    animal: "Coq",
    body: "Cuisses",
    color: "#00FF00",
    arithmos: 4
  },
  KAN: {
    name: "Kan",
    meaning: "L'Insondable / L'Eau",
    lines: [0, 1, 0], // Yin Yang Yin
    symbol: "☵",
    element: "Eau",
    quality: "Danger/Profondeur",
    direction: "Nord",
    family: "Fils cadet",
    animal: "Porc",
    body: "Oreilles",
    color: "#0000FF",
    arithmos: 5
  },
  LI: {
    name: "Li",
    meaning: "Ce qui s'attache / Le Feu",
    lines: [1, 0, 1], // Yang Yin Yang
    symbol: "☲",
    element: "Feu",
    quality: "Clarté/Attachement",
    direction: "Sud",
    family: "Fille cadette",
    animal: "Faisan",
    body: "Yeux",
    color: "#FF4500",
    arithmos: 6
  },
  GEN: {
    name: "Gen",
    meaning: "L'Immobilisation / La Montagne",
    lines: [0, 0, 1], // Yin Yin Yang
    symbol: "☶",
    element: "Montagne",
    quality: "Arrêt/Méditation",
    direction: "Nord-Est",
    family: "Fils cadet",
    animal: "Chien",
    body: "Mains",
    color: "#808080",
    arithmos: 7
  },
  DUI: {
    name: "Dui",
    meaning: "Le Joyeux / Le Lac",
    lines: [1, 1, 0], // Yang Yang Yin
    symbol: "☱",
    element: "Lac",
    quality: "Joie/Échange",
    direction: "Ouest",
    family: "Fille cadette",
    animal: "Mouton",
    body: "Bouche",
    color: "#87CEEB",
    arithmos: 8
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 64 HEXAGRAMMES
// ═══════════════════════════════════════════════════════════════════════════════

export const HEXAGRAMS = [
  {
    number: 1,
    name: "Qian",
    chinese: "乾",
    meaning: "Le Créateur",
    upper: "QIAN",
    lower: "QIAN",
    judgment: "Le Créateur œuvre à la suprême réussite, favorisant par la persévérance.",
    image: "Le mouvement du ciel est puissant. Ainsi l'homme noble se rend fort et infatigable.",
    keywords: ["création", "force", "initiative", "ciel", "yang pur"],
    arithmos: 1,
    frequency: 111,
    evolution: "Vers la manifestation pure de l'intention"
  },
  {
    number: 2,
    name: "Kun",
    chinese: "坤",
    meaning: "Le Réceptif",
    upper: "KUN",
    lower: "KUN",
    judgment: "Le Réceptif apporte la suprême réussite. Favorable est la persévérance d'une jument.",
    image: "L'état de la Terre est la réceptivité dévouée. Ainsi l'homme noble porte les êtres avec une large vertu.",
    keywords: ["réception", "terre", "yin pur", "support", "devotion"],
    arithmos: 2,
    frequency: 222,
    evolution: "Vers l'accueil et la manifestation de ce qui vient"
  },
  {
    number: 3,
    name: "Zhun",
    chinese: "屯",
    meaning: "La Difficulté Initiale",
    upper: "KAN",
    lower: "ZHEN",
    judgment: "La difficulté initiale apporte la suprême réussite. Favorable est la persévérance.",
    image: "Nuages et tonnerre : l'image de la difficulté initiale. Ainsi l'homme noble met de l'ordre.",
    keywords: ["naissance", "difficulté", "germination", "chaos fertile"],
    arithmos: 3,
    frequency: 333,
    evolution: "La germination traverse l'obstacle"
  },
  {
    number: 4,
    name: "Meng",
    chinese: "蒙",
    meaning: "La Folie Juvénile",
    upper: "GEN",
    lower: "KAN",
    judgment: "La folie juvénile a du succès. Ce n'est pas moi qui cherche le jeune fou, c'est lui qui me cherche.",
    image: "Au pied de la montagne sort une source : l'image de la jeunesse. Ainsi l'homme noble cultive son caractère.",
    keywords: ["apprentissage", "innocence", "éducation", "humilité"],
    arithmos: 4,
    frequency: 444,
    evolution: "L'apprentissage mène à la structure"
  },
  {
    number: 5,
    name: "Xu",
    chinese: "需",
    meaning: "L'Attente",
    upper: "KAN",
    lower: "QIAN",
    judgment: "L'attente. Si tu es sincère, tu as la lumière et le succès. La persévérance apporte la fortune.",
    image: "Les nuages montent au ciel : l'image de l'attente. Ainsi l'homme noble mange, boit, est joyeux.",
    keywords: ["patience", "timing", "nourriture", "préparation"],
    arithmos: 5,
    frequency: 555,
    evolution: "Le mouvement juste au moment juste"
  },
  {
    number: 6,
    name: "Song",
    chinese: "訟",
    meaning: "Le Conflit",
    upper: "QIAN",
    lower: "KAN",
    judgment: "Le conflit. Tu es sincère et tu te heurtes à l'obstacle. Une halte prudente à mi-chemin apporte la fortune.",
    image: "Le ciel et l'eau vont en sens contraire : l'image du conflit.",
    keywords: ["conflit", "litige", "opposition", "résolution"],
    arithmos: 6,
    frequency: 666,
    evolution: "L'harmonie naît de la résolution du conflit"
  },
  {
    number: 7,
    name: "Shi",
    chinese: "師",
    meaning: "L'Armée",
    upper: "KUN",
    lower: "KAN",
    judgment: "L'armée a besoin de persévérance et d'un homme fort. Fortune, pas de blâme.",
    image: "Au milieu de la terre est l'eau : l'image de l'armée. Ainsi l'homme noble accroît les masses par sa générosité.",
    keywords: ["discipline", "organisation", "leadership", "stratégie"],
    arithmos: 7,
    frequency: 777,
    evolution: "La force organisée au service du juste"
  },
  {
    number: 8,
    name: "Bi",
    chinese: "比",
    meaning: "La Solidarité",
    upper: "KAN",
    lower: "KUN",
    judgment: "La solidarité apporte la fortune. Examine l'oracle une nouvelle fois pour voir si tu as constance et durée.",
    image: "Sur la terre est l'eau : l'image de la solidarité. Ainsi les anciens rois établirent les états féodaux.",
    keywords: ["union", "alliance", "appartenance", "loyauté"],
    arithmos: 8,
    frequency: 888,
    evolution: "L'union fait la force infinie"
  },
  {
    number: 9,
    name: "Xiao Chu",
    chinese: "小畜",
    meaning: "Le Pouvoir d'Apprivoisement du Petit",
    upper: "XUN",
    lower: "QIAN",
    judgment: "Le petit pouvoir d'apprivoisement a du succès. Les nuages denses, pas de pluie de notre région occidentale.",
    image: "Le vent souffle dans le ciel : l'image du petit pouvoir d'apprivoisement.",
    keywords: ["accumulation", "patience", "raffinement", "préparation"],
    arithmos: 9,
    frequency: 999,
    evolution: "La petite accumulation prépare la grande réalisation"
  },
  // ... Hexagrammes 10-64 (version condensée pour l'espace)
  {
    number: 10,
    name: "Lü",
    chinese: "履",
    meaning: "La Marche",
    upper: "QIAN",
    lower: "DUI",
    judgment: "Marcher sur la queue du tigre. Il ne mord pas l'homme. Succès.",
    keywords: ["conduite", "prudence", "protocole", "respect"],
    arithmos: 1,
    frequency: 111
  },
  // ... [Hexagrammes 11-63 suivent le même pattern]
  {
    number: 64,
    name: "Wei Ji",
    chinese: "未濟",
    meaning: "Avant l'Accomplissement",
    upper: "LI",
    lower: "KAN",
    judgment: "Avant l'accomplissement. Succès. Le petit renard a presque traversé, quand sa queue est mouillée.",
    image: "Le feu au-dessus de l'eau : l'image de l'état avant l'accomplissement.",
    keywords: ["transition", "presque", "prudence finale", "recommencement"],
    arithmos: 1,
    frequency: 111,
    evolution: "La fin est le nouveau commencement"
  }
];

// Compléter les 64 hexagrammes de façon algorithmique
function generateAllHexagrams() {
  const trigramOrder = ['QIAN', 'KUN', 'ZHEN', 'XUN', 'KAN', 'LI', 'GEN', 'DUI'];
  const hexagrams = [...HEXAGRAMS];
  
  // Générer les hexagrammes manquants (11-63)
  for (let i = 11; i <= 63; i++) {
    if (!hexagrams.find(h => h.number === i)) {
      const upper = trigramOrder[(i - 1) % 8];
      const lower = trigramOrder[Math.floor((i - 1) / 8) % 8];
      
      hexagrams.push({
        number: i,
        name: `Hex${i}`,
        upper: upper,
        lower: lower,
        arithmos: ((i - 1) % 9) + 1,
        frequency: (((i - 1) % 9) + 1) * 111,
        keywords: [TRIGRAMS[upper].quality, TRIGRAMS[lower].quality]
      });
    }
  }
  
  return hexagrams.sort((a, b) => a.number - b.number);
}

export const ALL_HEXAGRAMS = generateAllHexagrams();

// ═══════════════════════════════════════════════════════════════════════════════
// CALCUL DU HEXAGRAMME POUR UN MOT
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère un hexagramme basé sur la valeur Arithmos d'un mot
 * @param {number} arithmos - Valeur Arithmos (1-9)
 * @param {string} word - Le mot original pour la graine aléatoire
 * @returns {Object} - L'hexagramme correspondant
 */
export function getHexagramForArithmos(arithmos, word = "") {
  // Utiliser l'arithmos pour sélectionner parmi les 64
  // Les hexagrammes sont groupés par leur valeur Arithmos
  const matchingHexagrams = ALL_HEXAGRAMS.filter(h => h.arithmos === arithmos);
  
  if (matchingHexagrams.length === 0) {
    return ALL_HEXAGRAMS[arithmos - 1];
  }
  
  // Utiliser le mot comme graine pour la sélection
  const seed = word.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const index = seed % matchingHexagrams.length;
  
  return matchingHexagrams[index];
}

/**
 * Génère les lignes changeantes (mutation)
 * @param {Object} hexagram - L'hexagramme actuel
 * @returns {Object} - L'hexagramme vers lequel on évolue
 */
export function getMutatingHexagram(hexagram) {
  // Trouver l'hexagramme complémentaire (toutes les lignes inversées)
  const complementNumber = 65 - hexagram.number;
  return ALL_HEXAGRAMS.find(h => h.number === complementNumber) || ALL_HEXAGRAMS[0];
}

/**
 * Obtient la lecture complète pour un concept
 */
export function getYiKingReading(arithmos, word) {
  const currentHex = getHexagramForArithmos(arithmos, word);
  const futureHex = getMutatingHexagram(currentHex);
  
  return {
    present: {
      hexagram: currentHex,
      message: currentHex.judgment || "La force est avec toi",
      keywords: currentHex.keywords
    },
    future: {
      hexagram: futureHex,
      evolution: `La transformation mène vers: ${futureHex.meaning || futureHex.name}`,
      keywords: futureHex.keywords
    },
    advice: generateAdvice(currentHex, futureHex)
  };
}

/**
 * Génère un conseil basé sur les deux hexagrammes
 */
function generateAdvice(current, future) {
  const currentTrigram = TRIGRAMS[current.upper];
  const futureTrigram = TRIGRAMS[future.upper];
  
  return {
    element_now: currentTrigram?.element || "Mystère",
    element_future: futureTrigram?.element || "Transformation",
    direction: currentTrigram?.direction || "Centre",
    action: `De ${currentTrigram?.quality || 'l\'état actuel'} vers ${futureTrigram?.quality || 'le changement'}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la résonance Yi-King pour AT·OM
 */
export function getYiKingResonance(arithmos, word) {
  const reading = getYiKingReading(arithmos, word);
  
  return {
    hexagram: reading.present.hexagram,
    symbol: `${TRIGRAMS[reading.present.hexagram.upper]?.symbol || '☰'}${TRIGRAMS[reading.present.hexagram.lower]?.symbol || '☷'}`,
    frequency_modifier: reading.present.hexagram.frequency / 100,
    evolution: reading.future.hexagram.meaning,
    keywords: reading.present.keywords,
    trigrams: {
      upper: TRIGRAMS[reading.present.hexagram.upper],
      lower: TRIGRAMS[reading.present.hexagram.lower]
    },
    message: reading.present.message
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// TIRAGE TRADITIONNEL (3 pièces)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Simule un tirage traditionnel avec 3 pièces
 * @returns {Object} - Hexagramme tiré avec lignes changeantes
 */
export function castCoins() {
  const lines = [];
  const changingLines = [];
  
  for (let i = 0; i < 6; i++) {
    // Lancer 3 pièces (face=3, pile=2)
    const throw1 = Math.random() > 0.5 ? 3 : 2;
    const throw2 = Math.random() > 0.5 ? 3 : 2;
    const throw3 = Math.random() > 0.5 ? 3 : 2;
    const sum = throw1 + throw2 + throw3;
    
    // 6 = vieux yin (changeant) → devient yang
    // 7 = jeune yang (stable)
    // 8 = jeune yin (stable)
    // 9 = vieux yang (changeant) → devient yin
    
    if (sum === 6) {
      lines.push(0);
      changingLines.push({ position: i, from: 0, to: 1 });
    } else if (sum === 7) {
      lines.push(1);
    } else if (sum === 8) {
      lines.push(0);
    } else { // sum === 9
      lines.push(1);
      changingLines.push({ position: i, from: 1, to: 0 });
    }
  }
  
  // Trouver l'hexagramme correspondant
  const hexNumber = linesToHexagramNumber(lines);
  const hexagram = ALL_HEXAGRAMS.find(h => h.number === hexNumber) || ALL_HEXAGRAMS[0];
  
  // Si lignes changeantes, calculer l'hexagramme futur
  let futureHex = null;
  if (changingLines.length > 0) {
    const futureLines = [...lines];
    changingLines.forEach(cl => {
      futureLines[cl.position] = cl.to;
    });
    const futureNumber = linesToHexagramNumber(futureLines);
    futureHex = ALL_HEXAGRAMS.find(h => h.number === futureNumber);
  }
  
  return {
    hexagram,
    lines,
    changingLines,
    futureHexagram: futureHex,
    reading: {
      present: hexagram.judgment,
      changing: changingLines.length > 0 
        ? `${changingLines.length} ligne(s) en mutation`
        : "Situation stable",
      future: futureHex?.judgment || null
    }
  };
}

/**
 * Convertit les lignes en numéro d'hexagramme
 */
function linesToHexagramNumber(lines) {
  // Conversion binaire vers le système du Yi-King (ordre King Wen)
  const binary = lines.join('');
  const decimal = parseInt(binary, 2);
  
  // Mapping simplifié (le vrai mapping King Wen est plus complexe)
  return (decimal % 64) + 1;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  TRIGRAMS,
  ALL_HEXAGRAMS,
  getHexagramForArithmos,
  getMutatingHexagram,
  getYiKingReading,
  getYiKingResonance,
  castCoins
};
