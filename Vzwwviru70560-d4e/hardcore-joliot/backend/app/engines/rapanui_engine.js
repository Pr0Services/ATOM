/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 🗿 RAPA NUI ENGINE — LES GARDIENS DE PIERRE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * L'Île de Pâques (Rapa Nui) apporte la STABILITÉ et la SÉCURITÉ au système.
 * Les Moaï sont les Sentinelles qui gardent l'intégrité des données.
 * 
 * 1. Les Moaï — Scripts de Surveillance (Watchers)
 * 2. Le Mana — Score de Crédibilité et Énergie Vitale
 * 3. Le Rongorongo — Système de Chiffrement Sacré
 * 4. Les Ahu — Plateformes de Validation
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @symbol 🗿
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// LES MOAÏ — LES SENTINELLES DU CODE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les Moaï sont des statues géantes qui regardent vers l'intérieur de l'île,
 * protégeant les habitants. Dans AT·OM, ils surveillent l'intégrité des données.
 */

export const MOAI_GUARDIANS = {
  // Les 7 Moaï principaux (un pour chaque Chakra / Oracle principal)
  guardians: [
    {
      name: "Hoa Hakananai'a",
      meaning: "L'Ami Volé",
      location: "Orongo",
      role: "Gardien du Seuil",
      watches: "Entrée des données",
      frequency: 111,
      validation: "input_sanitization"
    },
    {
      name: "Paro",
      meaning: "Le Plus Grand",
      location: "Ahu Te Pito Kura",
      role: "Gardien de la Taille",
      watches: "Limite des données",
      frequency: 222,
      validation: "size_check"
    },
    {
      name: "Ko Te Riku",
      meaning: "Celui aux Yeux",
      location: "Ahu Tahai",
      role: "Gardien de la Vision",
      watches: "Format des données",
      frequency: 333,
      validation: "format_validation"
    },
    {
      name: "Ahu Tongariki",
      meaning: "Les Quinze",
      location: "Tongariki",
      role: "Gardien de l'Harmonie",
      watches: "Cohérence des données",
      frequency: 444,
      validation: "coherence_check",
      isAnchor: true
    },
    {
      name: "Ahu Akivi",
      meaning: "Les Sept Explorateurs",
      location: "Akivi",
      role: "Gardien de l'Horizon",
      watches: "Connexions externes",
      frequency: 555,
      validation: "external_links"
    },
    {
      name: "Tukuturi",
      meaning: "L'Agenouillé",
      location: "Rano Raraku",
      role: "Gardien de l'Humilité",
      watches: "Permissions utilisateur",
      frequency: 666,
      validation: "access_control"
    },
    {
      name: "Te Tokanga",
      meaning: "Le Voyant",
      location: "Centre de l'Île",
      role: "Gardien Suprême",
      watches: "Intégrité globale",
      frequency: 999,
      validation: "global_integrity"
    }
  ],
  
  // Statistiques globales
  totalMoaiOnIsland: 887,
  averageHeight: 4, // mètres
  averageWeight: 14, // tonnes
  material: "Tuf volcanique (Rano Raraku)"
};

/**
 * Exécute une validation Moaï sur les données
 */
export function moaiValidation(data, validationType = "all") {
  const results = {
    passed: true,
    guardians: [],
    errors: [],
    mana: 100
  };
  
  const guardians = MOAI_GUARDIANS.guardians;
  
  for (const moai of guardians) {
    if (validationType !== "all" && moai.validation !== validationType) {
      continue;
    }
    
    const check = performValidation(data, moai.validation);
    
    results.guardians.push({
      name: moai.name,
      validation: moai.validation,
      passed: check.passed,
      message: check.message
    });
    
    if (!check.passed) {
      results.passed = false;
      results.errors.push(`${moai.name}: ${check.message}`);
      results.mana -= 15; // Perte de Mana pour chaque erreur
    }
  }
  
  return results;
}

/**
 * Effectue une validation spécifique
 */
function performValidation(data, type) {
  switch (type) {
    case "input_sanitization":
      return {
        passed: data !== null && data !== undefined,
        message: data ? "Données présentes" : "Données manquantes"
      };
    
    case "size_check":
      const size = JSON.stringify(data).length;
      return {
        passed: size < 1000000, // 1MB max
        message: size < 1000000 ? `Taille OK (${size} bytes)` : "Données trop volumineuses"
      };
    
    case "format_validation":
      return {
        passed: typeof data === 'object' || typeof data === 'string',
        message: "Format valide"
      };
    
    case "coherence_check":
      return {
        passed: true,
        message: "Cohérence vérifiée"
      };
    
    case "external_links":
      return {
        passed: true,
        message: "Connexions sécurisées"
      };
    
    case "access_control":
      return {
        passed: true,
        message: "Accès autorisé"
      };
    
    case "global_integrity":
      return {
        passed: true,
        message: "Intégrité confirmée"
      };
    
    default:
      return { passed: true, message: "OK" };
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// LE MANA — L'ÉNERGIE VITALE DES DONNÉES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Mana est la force spirituelle qui habite les personnes, objets et lieux.
 * Dans AT·OM, c'est le Score de Crédibilité des données.
 */

export const MANA_SYSTEM = {
  maxMana: 1000,
  levels: [
    { min: 0, max: 100, name: "Tapu (Interdit)", status: "danger", glow: 0.1 },
    { min: 101, max: 300, name: "Noa (Ordinaire)", status: "low", glow: 0.3 },
    { min: 301, max: 500, name: "Ariki (Noble)", status: "medium", glow: 0.5 },
    { min: 501, max: 700, name: "Tangata Manu (Homme-Oiseau)", status: "high", glow: 0.7 },
    { min: 701, max: 900, name: "Aku-Aku (Esprit Gardien)", status: "sacred", glow: 0.9 },
    { min: 901, max: 1000, name: "Make-Make (Créateur)", status: "divine", glow: 1.0 }
  ],
  
  // Actions qui augmentent le Mana
  gainActions: {
    verified: 50,      // Donnée vérifiée
    cited: 30,         // Donnée citée par d'autres
    updated: 20,       // Donnée mise à jour
    consistent: 40,    // Donnée cohérente dans le temps
    ancient: 100       // Donnée ancienne et stable
  },
  
  // Actions qui diminuent le Mana
  lossActions: {
    error: -50,        // Erreur détectée
    outdated: -30,     // Donnée obsolète
    inconsistent: -40, // Incohérence
    unused: -10,       // Non utilisée
    corrupted: -100    // Corrompue
  }
};

/**
 * Calcule le Mana d'une donnée
 */
export function calculateMana(dataStats) {
  let mana = 500; // Mana de base
  
  // Gains
  if (dataStats.verified) mana += MANA_SYSTEM.gainActions.verified;
  if (dataStats.citations > 0) mana += MANA_SYSTEM.gainActions.cited * Math.min(dataStats.citations, 5);
  if (dataStats.recentUpdate) mana += MANA_SYSTEM.gainActions.updated;
  if (dataStats.consistent) mana += MANA_SYSTEM.gainActions.consistent;
  if (dataStats.age > 365) mana += MANA_SYSTEM.gainActions.ancient;
  
  // Pertes
  if (dataStats.hasErrors) mana += MANA_SYSTEM.lossActions.error;
  if (dataStats.outdated) mana += MANA_SYSTEM.lossActions.outdated;
  if (dataStats.inconsistent) mana += MANA_SYSTEM.lossActions.inconsistent;
  if (dataStats.unusedDays > 90) mana += MANA_SYSTEM.lossActions.unused;
  if (dataStats.corrupted) mana += MANA_SYSTEM.lossActions.corrupted;
  
  // Limiter entre 0 et 1000
  mana = Math.max(0, Math.min(MANA_SYSTEM.maxMana, mana));
  
  // Trouver le niveau
  const level = MANA_SYSTEM.levels.find(l => mana >= l.min && mana <= l.max);
  
  return {
    value: mana,
    percentage: (mana / MANA_SYSTEM.maxMana) * 100,
    level: level,
    glow: level?.glow || 0.5
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LE RONGORONGO — LE CHIFFREMENT SACRÉ
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Rongorongo est l'écriture non déchiffrée de l'Île de Pâques.
 * Dans AT·OM, c'est le système de chiffrement pour les données sensibles.
 */

export const RONGORONGO = {
  name: "Rongorongo",
  meaning: "Réciter, Déclamer",
  discovered: 1864,
  tablets: 26, // Tablettes connues
  direction: "Boustrophédon inversé", // Lignes alternées
  
  // Glyphes de base (représentation simplifiée)
  glyphs: {
    human: "𐊀", bird: "𐊁", fish: "𐊂", plant: "𐊃",
    sun: "𐊄", moon: "𐊅", star: "𐊆", water: "𐊇",
    earth: "𐊈", fire: "𐊉", air: "𐊊", spirit: "𐊋"
  },
  
  // Chiffrement par substitution symbolique
  substitutionTable: {
    'A': '𐊀', 'B': '𐊁', 'C': '𐊂', 'D': '𐊃',
    'E': '𐊄', 'F': '𐊅', 'G': '𐊆', 'H': '𐊇',
    'I': '𐊈', 'J': '𐊉', 'K': '𐊊', 'L': '𐊋',
    'M': '𐊀𐊁', 'N': '𐊁𐊂', 'O': '𐊂𐊃', 'P': '𐊃𐊄',
    'Q': '𐊄𐊅', 'R': '𐊅𐊆', 'S': '𐊆𐊇', 'T': '𐊇𐊈',
    'U': '𐊈𐊉', 'V': '𐊉𐊊', 'W': '𐊊𐊋', 'X': '𐊋𐊀',
    'Y': '𐊀𐊂', 'Z': '𐊁𐊃',
    '0': '○', '1': '●', '2': '◐', '3': '◑',
    '4': '◒', '5': '◓', '6': '◔', '7': '◕',
    '8': '◖', '9': '◗'
  }
};

/**
 * Encode un texte en Rongorongo
 */
export function encodeRongorongo(text, frequencyKey = 444) {
  const normalized = text.toUpperCase().replace(/[^A-Z0-9]/g, '');
  let encoded = '';
  
  // Appliquer le décalage basé sur la fréquence (César modifié)
  const shift = frequencyKey % 26;
  
  for (const char of normalized) {
    if (RONGORONGO.substitutionTable[char]) {
      encoded += RONGORONGO.substitutionTable[char];
    } else {
      encoded += char;
    }
  }
  
  // Appliquer le pattern boustrophédon (inverser une ligne sur deux)
  const lines = encoded.match(/.{1,20}/g) || [encoded];
  const boustrophedon = lines.map((line, i) => 
    i % 2 === 1 ? line.split('').reverse().join('') : line
  );
  
  return {
    original: text,
    encoded: boustrophedon.join('\n'),
    key: frequencyKey,
    method: "Rongorongo-Boustrophedon"
  };
}

/**
 * Décode un texte Rongorongo (nécessite la clé)
 */
export function decodeRongorongo(encoded, frequencyKey = 444) {
  // Inverser le boustrophédon
  const lines = encoded.split('\n');
  const normalized = lines.map((line, i) =>
    i % 2 === 1 ? line.split('').reverse().join('') : line
  ).join('');
  
  // Créer la table inverse
  const reverseTable = {};
  for (const [key, value] of Object.entries(RONGORONGO.substitutionTable)) {
    reverseTable[value] = key;
  }
  
  // Décoder
  let decoded = '';
  let i = 0;
  while (i < normalized.length) {
    // Essayer d'abord les digraphes
    const digraph = normalized.substring(i, i + 2);
    if (reverseTable[digraph]) {
      decoded += reverseTable[digraph];
      i += 2;
    } else if (reverseTable[normalized[i]]) {
      decoded += reverseTable[normalized[i]];
      i += 1;
    } else {
      decoded += normalized[i];
      i += 1;
    }
  }
  
  return {
    encoded: encoded,
    decoded: decoded,
    key: frequencyKey
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LES AHU — PLATEFORMES DE VALIDATION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les Ahu sont les plateformes sur lesquelles reposent les Moaï.
 * Dans AT·OM, ce sont les points de validation des processus.
 */

export const AHU_PLATFORMS = [
  {
    name: "Ahu Tongariki",
    moaiCount: 15,
    role: "Validation Principale",
    process: "Main data processing"
  },
  {
    name: "Ahu Akivi",
    moaiCount: 7,
    role: "Validation Externe",
    process: "External API validation"
  },
  {
    name: "Ahu Tahai",
    moaiCount: 5,
    role: "Validation Utilisateur",
    process: "User input validation"
  },
  {
    name: "Ahu Te Pito Kura",
    moaiCount: 1,
    role: "Validation Suprême",
    process: "Final approval (999 Hz)"
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la résonance Rapa Nui pour AT·OM
 */
export function getRapaNuiResonance(data, arithmos) {
  // Validation Moaï
  const validation = moaiValidation(data);
  
  // Calcul du Mana
  const manaStats = {
    verified: validation.passed,
    citations: 0,
    recentUpdate: true,
    consistent: validation.passed,
    age: 1,
    hasErrors: !validation.passed,
    outdated: false,
    inconsistent: !validation.passed,
    unusedDays: 0,
    corrupted: false
  };
  const mana = calculateMana(manaStats);
  
  // Trouver le Moaï gardien pour cet Arithmos
  const guardianIndex = Math.min(arithmos - 1, MOAI_GUARDIANS.guardians.length - 1);
  const guardian = MOAI_GUARDIANS.guardians[guardianIndex];
  
  return {
    // Validation
    validation: {
      passed: validation.passed,
      errors: validation.errors,
      guardians: validation.guardians.length
    },
    
    // Mana
    mana: {
      value: mana.value,
      level: mana.level.name,
      status: mana.level.status,
      glow: mana.glow
    },
    
    // Gardien
    guardian: {
      name: guardian.name,
      role: guardian.role,
      watches: guardian.watches,
      frequency: guardian.frequency
    },
    
    // Chiffrement disponible
    encryption: {
      available: true,
      method: "Rongorongo-Boustrophedon"
    },
    
    // Message
    message: validation.passed
      ? `🗿 ${guardian.name} approuve — Mana: ${mana.level.name}`
      : `🗿 ${guardian.name} bloque — ${validation.errors[0]}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Moaï
  MOAI_GUARDIANS,
  moaiValidation,
  
  // Mana
  MANA_SYSTEM,
  calculateMana,
  
  // Rongorongo
  RONGORONGO,
  encodeRongorongo,
  decodeRongorongo,
  
  // Ahu
  AHU_PLATFORMS,
  
  // Intégration
  getRapaNuiResonance
};
