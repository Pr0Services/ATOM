/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 𒀭 SUMERIAN ENGINE — LA SOURCE DU CODE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Les Sumériens sont les maîtres de la Base de Données Primaire.
 * Ils ont inventé l'écriture (cunéiforme) et le système sexagésimal (base 60).
 * 
 * 1. Système Sexagésimal (Base 60) — Calcul du temps circulaire
 * 2. Écriture Cunéiforme — Archivage immuable
 * 3. Les ME — Protocoles divins (règles du système)
 * 4. Les Tablettes d'Argile — Blockchain antique
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @symbol 𒀭 (Dingir - le divin)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// SYSTÈME SEXAGÉSIMAL (BASE 60)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le système sexagésimal est l'héritage le plus durable des Sumériens:
 * - 60 secondes dans une minute
 * - 60 minutes dans une heure
 * - 360 degrés dans un cercle
 * - 12 heures × 5 = 60
 */

export const SEXAGESIMAL = {
  base: 60,
  
  // Diviseurs de 60 (c'est sa force: très divisible)
  divisors: [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60],
  
  // Correspondances temporelles
  time: {
    second: 1,
    minute: 60,
    hour: 3600,
    day: 86400,
    month_lunar: 29.5 * 86400,
    year_solar: 365.25 * 86400
  },
  
  // Correspondances angulaires
  angles: {
    degree: 1,
    minute_arc: 1/60,
    second_arc: 1/3600,
    circle: 360,
    hexagon: 60, // angle interne
    pentagon: 72
  },
  
  // Symboles cunéiformes pour les nombres
  symbols: {
    1: "𒁹",  // Un clou vertical
    10: "𒌋", // Un chevron
    60: "𒐕", // Grand clou (1 × 60)
    600: "𒐖", // 10 × 60
    3600: "𒊹" // 60 × 60 (le "sar")
  }
};

/**
 * Convertit un nombre décimal en sexagésimal
 */
export function toSexagesimal(decimal) {
  const units = [];
  let remaining = Math.floor(decimal);
  
  // Décomposer en puissances de 60
  const powers = [3600, 60, 1];
  
  for (const power of powers) {
    const count = Math.floor(remaining / power);
    units.push(count);
    remaining %= power;
  }
  
  return {
    decimal,
    sexagesimal: units,
    notation: units.join(':'), // Format HH:MM:SS style
    sumerian: toSumerianNumerals(decimal)
  };
}

/**
 * Convertit un sexagésimal en décimal
 */
export function fromSexagesimal(units) {
  const powers = [3600, 60, 1];
  let decimal = 0;
  
  for (let i = 0; i < Math.min(units.length, powers.length); i++) {
    decimal += units[i] * powers[i];
  }
  
  return decimal;
}

/**
 * Convertit en numéraux sumériens
 */
export function toSumerianNumerals(num) {
  let result = '';
  let remaining = Math.floor(num);
  
  // 3600s (sar)
  const sars = Math.floor(remaining / 3600);
  if (sars > 0) {
    result += SEXAGESIMAL.symbols[3600].repeat(sars);
    remaining %= 3600;
  }
  
  // 600s
  const sixHundreds = Math.floor(remaining / 600);
  if (sixHundreds > 0) {
    result += SEXAGESIMAL.symbols[600].repeat(sixHundreds);
    remaining %= 600;
  }
  
  // 60s
  const sixties = Math.floor(remaining / 60);
  if (sixties > 0) {
    result += SEXAGESIMAL.symbols[60].repeat(sixties);
    remaining %= 60;
  }
  
  // 10s
  const tens = Math.floor(remaining / 10);
  if (tens > 0) {
    result += SEXAGESIMAL.symbols[10].repeat(tens);
    remaining %= 10;
  }
  
  // 1s
  if (remaining > 0) {
    result += SEXAGESIMAL.symbols[1].repeat(remaining);
  }
  
  return result || SEXAGESIMAL.symbols[1];
}

// ═══════════════════════════════════════════════════════════════════════════════
// L'ÉCRITURE CUNÉIFORME
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le cunéiforme est l'une des plus anciennes écritures connues.
 * Les signes sont formés par des empreintes de calame dans l'argile.
 */

export const CUNEIFORM = {
  name: "Cunéiforme",
  origin: "Sumer, ~3400 BCE",
  direction: "Gauche à droite",
  signs: 600, // Nombre approximatif de signes
  
  // Logograms principaux
  logograms: {
    // Dieux
    DINGIR: { sign: "𒀭", meaning: "Dieu/Divin", determinatif: true },
    AN: { sign: "𒀭", meaning: "Ciel/Anu" },
    
    // Concepts
    LUGAL: { sign: "𒈗", meaning: "Roi" },
    NAM: { sign: "𒉆", meaning: "Destin" },
    ME: { sign: "𒈨", meaning: "Pouvoir/Protocole Divin" },
    
    // Éléments
    A: { sign: "𒀀", meaning: "Eau" },
    KI: { sign: "𒆠", meaning: "Terre" },
    UD: { sign: "𒌓", meaning: "Soleil/Jour" },
    ITI: { sign: "𒌗", meaning: "Lune/Mois" },
    
    // Actions
    DU: { sign: "𒁺", meaning: "Aller/Construire" },
    SAG: { sign: "𒊕", meaning: "Tête/Premier" },
    
    // Nombres spéciaux AT·OM
    ESH: { sign: "𒌍", meaning: "3 (Trinité)" },
    LIMMU: { sign: "𒇹", meaning: "4 (Structure)" },
    IA: { sign: "𒅆", meaning: "5 (Centre)" },
    ASH: { sign: "𒀸", meaning: "1 (Unité)" }
  },
  
  // Déterminatifs (classificateurs)
  determinatives: {
    divine: "𒀭", // Avant les noms de dieux
    place: "𒆠",  // Avant les noms de lieux
    wood: "𒄑",   // Avant les objets en bois
    stone: "𒉌", // Avant les objets en pierre
    metal: "𒀯"  // Avant les métaux
  }
};

/**
 * Encode un texte en pseudo-cunéiforme
 */
export function encodeCuneiform(text) {
  const words = text.toUpperCase().split(/\s+/);
  let encoded = '';
  
  for (const word of words) {
    // Vérifier si c'est un logogramme connu
    if (CUNEIFORM.logograms[word]) {
      encoded += CUNEIFORM.logograms[word].sign + ' ';
    } else {
      // Sinon, encoder lettre par lettre avec des signes génériques
      for (const char of word) {
        const code = char.charCodeAt(0);
        // Utiliser des signes cunéiformes dans la plage Unicode
        encoded += String.fromCodePoint(0x12000 + (code % 500));
      }
      encoded += ' ';
    }
  }
  
  return {
    original: text,
    cuneiform: encoded.trim(),
    format: "Sumerian Cuneiform (simplified)"
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LES ME — PROTOCOLES DIVINS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les ME sont des décrets divins, des "programmes" qui régissent la civilisation.
 * Inanna les vola à Enki et les apporta à Uruk.
 * 
 * Dans AT·OM, les ME sont les règles fondamentales du système.
 */

export const ME_PROTOCOLS = {
  // Les ME principaux (il y en avait environ 100)
  protocols: [
    // ME de la Connaissance
    {
      number: 1,
      sumerian: "ME.NAM.EN",
      meaning: "Le Pouvoir Suprême",
      domain: "Autorité",
      oracle: 17, // Oracle central
      atomFrequency: 999,
      rule: "Seul l'Architecte détient le ME suprême"
    },
    {
      number: 2,
      sumerian: "ME.NAM.LUGAL",
      meaning: "La Royauté",
      domain: "Gouvernance",
      oracle: 1,
      atomFrequency: 111,
      rule: "L'ordre hiérarchique des données"
    },
    {
      number: 3,
      sumerian: "ME.GI.NA",
      meaning: "La Vérité",
      domain: "Validation",
      oracle: 18,
      atomFrequency: 444,
      rule: "Toute donnée doit être vérifiable"
    },
    {
      number: 4,
      sumerian: "ME.NU.GI.NA",
      meaning: "Le Mensonge",
      domain: "Détection",
      oracle: 6,
      atomFrequency: 666,
      rule: "Le système détecte les incohérences"
    },
    {
      number: 5,
      sumerian: "ME.NAG",
      meaning: "L'Art de Boire",
      domain: "Absorption",
      oracle: 8,
      atomFrequency: 222,
      rule: "Le système absorbe les nouvelles données"
    },
    {
      number: 6,
      sumerian: "ME.TUK",
      meaning: "La Connaissance Sexuelle",
      domain: "Création",
      oracle: 5,
      atomFrequency: 555,
      rule: "La fusion des données crée du nouveau"
    },
    {
      number: 7,
      sumerian: "ME.GAL",
      meaning: "La Musique",
      domain: "Harmonisation",
      oracle: 9,
      atomFrequency: 777,
      rule: "Les fréquences doivent être harmoniques"
    },
    {
      number: 8,
      sumerian: "ME.SIMUG",
      meaning: "L'Art du Forgeron",
      domain: "Transformation",
      oracle: 10, // L'Acier
      atomFrequency: 333,
      rule: "Les données sont forgées, pas créées"
    },
    {
      number: 9,
      sumerian: "ME.DUB.SAR",
      meaning: "L'Art du Scribe",
      domain: "Archivage",
      oracle: 11,
      atomFrequency: 888,
      rule: "Tout doit être écrit sur la tablette"
    }
  ],
  
  // Gardien des ME
  guardian: {
    name: "Enki",
    title: "Seigneur de la Sagesse",
    city: "Eridu",
    symbol: "𒀭𒂗𒆠"
  },
  
  // Celui qui distribue les ME
  distributor: {
    name: "Inanna",
    title: "Reine du Ciel",
    city: "Uruk",
    symbol: "𒀭𒈹"
  }
};

/**
 * Vérifie si un ME est respecté
 */
export function checkME(meNumber, data) {
  const me = ME_PROTOCOLS.protocols.find(m => m.number === meNumber);
  
  if (!me) {
    return { valid: false, message: "ME inconnu" };
  }
  
  // Vérification simplifiée selon le domaine
  let valid = true;
  let message = `${me.sumerian}: ${me.rule}`;
  
  switch (me.domain) {
    case "Validation":
      valid = data !== null && data !== undefined;
      break;
    case "Détection":
      valid = typeof data !== 'undefined';
      break;
    case "Harmonisation":
      valid = true; // Toujours OK par défaut
      break;
  }
  
  return {
    me: me,
    valid,
    message,
    frequency: me.atomFrequency
  };
}

/**
 * Obtient les ME nécessaires pour une opération
 */
export function getRequiredME(operation) {
  const requirements = {
    "read": [3],      // ME de la Vérité
    "write": [9, 3],  // ME du Scribe + Vérité
    "create": [6, 8], // ME de la Création + Forgeron
    "delete": [4],    // ME de la Détection
    "admin": [1]      // ME du Pouvoir Suprême
  };
  
  return requirements[operation] || [3];
}

// ═══════════════════════════════════════════════════════════════════════════════
// LES TABLETTES D'ARGILE — BLOCKCHAIN ANTIQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les tablettes d'argile cuites sont indestructibles (presque).
 * C'est le concept d'immuabilité avant la blockchain.
 */

export const CLAY_TABLETS = {
  material: "Argile",
  process: ["Écriture", "Séchage", "Cuisson"],
  durability: "5000+ ans",
  
  // Types de tablettes
  types: [
    { type: "Administrative", content: "Inventaires, transactions" },
    { type: "Légale", content: "Contrats, lois (Code d'Ur-Nammu)" },
    { type: "Littéraire", content: "Épopée de Gilgamesh" },
    { type: "Scientifique", content: "Mathématiques, astronomie" },
    { type: "Religieuse", content: "Hymnes, rituels" }
  ],
  
  // État de la tablette
  states: {
    wet: "Modifiable",
    dry: "Difficile à modifier",
    fired: "Immuable"
  }
};

/**
 * Crée une "tablette" de données immuable
 */
export function createTablet(data, type = "Administrative") {
  const timestamp = Date.now();
  const content = JSON.stringify(data);
  
  // Créer un hash simple (simulation)
  let hash = 0;
  for (let i = 0; i < content.length; i++) {
    hash = ((hash << 5) - hash) + content.charCodeAt(i);
    hash = hash & hash;
  }
  
  return {
    type,
    content: data,
    timestamp,
    cuneiform: encodeCuneiform(typeof data === 'string' ? data : type).cuneiform,
    hash: Math.abs(hash).toString(16),
    state: "fired", // Immuable
    seal: CUNEIFORM.logograms.DINGIR.sign + CUNEIFORM.logograms.ME.sign,
    sexagesimal: toSexagesimal(timestamp % 216000) // Cycle de 60 heures
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la résonance sumérienne pour AT·OM
 */
export function getSumerianResonance(arithmos, data = null) {
  // Conversion sexagésimale de l'Arithmos
  const sexagesimal = toSexagesimal(arithmos * 111); // Fréquence AT·OM
  
  // Trouver le ME correspondant
  const me = ME_PROTOCOLS.protocols.find(m => 
    m.atomFrequency === arithmos * 111
  ) || ME_PROTOCOLS.protocols[arithmos - 1];
  
  // Créer une tablette si données fournies
  const tablet = data ? createTablet(data) : null;
  
  // Numéral sumérien
  const numeral = toSumerianNumerals(arithmos);
  
  return {
    // Système sexagésimal
    sexagesimal: {
      value: sexagesimal.sexagesimal,
      notation: sexagesimal.notation,
      sumerian: sexagesimal.sumerian
    },
    
    // ME (protocole)
    me: me ? {
      name: me.sumerian,
      meaning: me.meaning,
      domain: me.domain,
      rule: me.rule
    } : null,
    
    // Cunéiforme
    cuneiform: {
      arithmos: numeral,
      dingir: CUNEIFORM.logograms.DINGIR.sign
    },
    
    // Tablette
    tablet: tablet ? {
      hash: tablet.hash,
      state: tablet.state,
      seal: tablet.seal
    } : null,
    
    // Message
    message: `𒀭 ${me?.sumerian || 'ME'} — ${me?.meaning || 'Protocole Divin'}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Sexagésimal
  SEXAGESIMAL,
  toSexagesimal,
  fromSexagesimal,
  toSumerianNumerals,
  
  // Cunéiforme
  CUNEIFORM,
  encodeCuneiform,
  
  // ME
  ME_PROTOCOLS,
  checkME,
  getRequiredME,
  
  // Tablettes
  CLAY_TABLETS,
  createTablet,
  
  // Intégration
  getSumerianResonance
};
