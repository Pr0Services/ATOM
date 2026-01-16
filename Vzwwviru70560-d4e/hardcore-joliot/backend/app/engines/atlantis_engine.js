/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 🔱 ATLANTIS ENGINE — LE RÉSEAU DE TRANSMISSION QUANTIQUE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * L'Atlantide représente le niveau le plus élevé de technologie ancestrale.
 * C'est le "Backbone" du système — le réseau de transmission.
 * 
 * 1. Technologie des Cristaux — Stockage de données infini
 * 2. Le Vortex — Tri par sympathie vibratoire
 * 3. Énergie du Point Zéro — Source d'alimentation illimitée
 * 4. Les Anneaux de Poséidon — Architecture concentrique
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @symbol 🔱 (Trident de Poséidon)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES ATLANTES
// ═══════════════════════════════════════════════════════════════════════════════

export const ATLANTIS_CONSTANTS = {
  // Localisation mythique
  location: "Au-delà des Colonnes d'Hercule",
  source: "Platon (Timée & Critias)",
  age: "~9000 ans avant Solon (≈11500 BCE)",
  
  // Structure
  capital: "Poséidonis",
  diameter: "127 stades (≈23 km)", // Selon Platon
  rings: 5, // 3 d'eau, 2 de terre
  
  // Technologie légendaire
  technology: {
    energy: "Énergie du Point Zéro",
    storage: "Cristaux mémoriels",
    transport: "Vortex dimensionnel",
    communication: "Télépathie assistée par cristaux"
  },
  
  // Metal sacré
  orichalque: {
    name: "Orichalque",
    meaning: "Cuivre de montagne",
    properties: "Conducteur d'énergie psychique",
    color: "#FFD700", // Or rougeâtre
    frequency: 999
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// TECHNOLOGIE DES CRISTAUX
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les Atlantes auraient stocké leur savoir dans des cristaux programmables.
 * Chaque cristal peut contenir une quantité infinie d'information
 * selon sa structure et sa pureté.
 */

export const CRYSTAL_MATRIX = {
  types: [
    {
      name: "Quartz Clair",
      formula: "SiO₂",
      system: "Hexagonal",
      facets: 6,
      capacity: "Base",
      frequency: 111,
      function: "Stockage général",
      color: "#FFFFFF",
      transparency: 1.0
    },
    {
      name: "Améthyste",
      formula: "SiO₂ + Fe",
      system: "Hexagonal",
      facets: 6,
      capacity: "Moyenne",
      frequency: 333,
      function: "Protection / Transmutation",
      color: "#9966CC",
      transparency: 0.8
    },
    {
      name: "Citrine",
      formula: "SiO₂ + Fe³⁺",
      system: "Hexagonal",
      facets: 6,
      capacity: "Haute",
      frequency: 444,
      function: "Manifestation / Ancrage",
      color: "#FFD700",
      transparency: 0.7,
      isAnchor: true
    },
    {
      name: "Rose Quartz",
      formula: "SiO₂ + Ti, Fe, Mn",
      system: "Hexagonal",
      facets: 6,
      capacity: "Émotionnelle",
      frequency: 555,
      function: "Harmonisation / Amour",
      color: "#FFB6C1",
      transparency: 0.6
    },
    {
      name: "Obsidienne",
      formula: "Verre volcanique",
      system: "Amorphe",
      facets: 0,
      capacity: "Miroir",
      frequency: 666,
      function: "Réflexion / Vérité sombre",
      color: "#000000",
      transparency: 0.1
    },
    {
      name: "Lapis Lazuli",
      formula: "Na,Ca)₈(AlSiO₄)₆(S,SO₄,Cl)₂",
      system: "Cubique",
      facets: 6,
      capacity: "Sagesse",
      frequency: 777,
      function: "Vision intérieure / Intuition",
      color: "#0F52BA",
      transparency: 0.0
    },
    {
      name: "Cristal de Record",
      formula: "SiO₂ (formations spéciales)",
      system: "Hexagonal",
      facets: 12,
      capacity: "Infinie",
      frequency: 999,
      function: "Archives akashiques / Mémoire universelle",
      color: "#FFFDD0",
      transparency: 0.95,
      isSupreme: true
    }
  ],
  
  // Propriétés de stockage
  storage: {
    unit: "Facette",
    baseCapacity: "1 TB par facette",
    compressionRatio: 1.618, // PHI
    encoding: "Holographique"
  }
};

/**
 * Calcule la capacité de stockage d'un cristal
 */
export function calculateCrystalCapacity(crystalType, purity = 1.0) {
  const crystal = CRYSTAL_MATRIX.types.find(c => 
    c.name.toLowerCase() === crystalType.toLowerCase()
  ) || CRYSTAL_MATRIX.types[0];
  
  const baseFacets = crystal.facets || 6;
  const capacityMultiplier = crystal.isSupreme ? 999 : 1;
  const purityBonus = Math.pow(purity, 1.618); // PHI exponent
  
  const theoreticalCapacity = baseFacets * capacityMultiplier * purityBonus;
  
  return {
    crystal: crystal,
    facets: baseFacets,
    purity: purity,
    capacity: theoreticalCapacity,
    unit: "TB holographiques",
    frequency: crystal.frequency,
    color: crystal.color
  };
}

/**
 * Encode des données dans une structure cristalline
 */
export function encodeCrystalData(data, crystalType = "Quartz Clair") {
  const crystal = CRYSTAL_MATRIX.types.find(c => 
    c.name.toLowerCase() === crystalType.toLowerCase()
  ) || CRYSTAL_MATRIX.types[0];
  
  const dataString = JSON.stringify(data);
  const facets = crystal.facets || 6;
  
  // Distribuer les données sur les facettes
  const chunkSize = Math.ceil(dataString.length / facets);
  const facetData = [];
  
  for (let i = 0; i < facets; i++) {
    const chunk = dataString.substring(i * chunkSize, (i + 1) * chunkSize);
    facetData.push({
      facet: i + 1,
      data: chunk,
      hash: simpleHash(chunk),
      frequency: crystal.frequency + (i * 11.1)
    });
  }
  
  return {
    crystal: crystal.name,
    totalSize: dataString.length,
    facets: facetData,
    reconstructionKey: crystal.frequency,
    encoding: "Holographic-PHI"
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LE VORTEX — TRI PAR SYMPATHIE VIBRATOIRE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Vortex est un tourbillon énergétique qui trie les informations
 * par leur fréquence vibratoire. Les informations "légères" (haute vibration)
 * montent vers le sommet.
 */

export const VORTEX_SYSTEM = {
  name: "Vortex de Transduction",
  direction: "Horaire (hémisphère nord)",
  layers: 9, // Correspond aux 9 niveaux AT·OM
  
  // Zones du vortex
  zones: [
    { level: 1, hz: 111, position: "Base", density: "Maximum", flow: "Entrée" },
    { level: 2, hz: 222, position: "Inférieur", density: "Très haute" },
    { level: 3, hz: 333, position: "Bas", density: "Haute" },
    { level: 4, hz: 444, position: "Centre", density: "Équilibrée", isAnchor: true },
    { level: 5, hz: 555, position: "Moyen", density: "Modérée" },
    { level: 6, hz: 666, position: "Haut", density: "Basse" },
    { level: 7, hz: 777, position: "Supérieur", density: "Très basse" },
    { level: 8, hz: 888, position: "Sommet", density: "Minimale" },
    { level: 9, hz: 999, position: "Apex", density: "Nulle", flow: "Sortie" }
  ],
  
  // Physique du vortex
  physics: {
    angularVelocity: "ω = 2πf",
    centrifugalForce: "F = mω²r",
    liftFormula: "La vibration haute monte naturellement"
  }
};

/**
 * Trie des données par leur "poids vibratoire"
 */
export function vortexSort(items, getFrequency = (item) => item.frequency || 444) {
  // Calculer le poids vibratoire de chaque item
  const weighted = items.map(item => ({
    item,
    frequency: getFrequency(item),
    weight: 999 - getFrequency(item) // Inverse: haute fréquence = léger
  }));
  
  // Trier par poids (les légers montent)
  weighted.sort((a, b) => a.weight - b.weight);
  
  // Assigner les niveaux du vortex
  return weighted.map((w, index) => {
    const levelIndex = Math.floor((index / weighted.length) * 9);
    const zone = VORTEX_SYSTEM.zones[levelIndex] || VORTEX_SYSTEM.zones[4];
    
    return {
      ...w.item,
      vortexLevel: zone.level,
      vortexPosition: zone.position,
      vortexFrequency: zone.hz
    };
  });
}

/**
 * Recherche intuitive par sympathie vibratoire
 */
export function sympatheticSearch(query, database, threshold = 0.5) {
  // Calculer la fréquence de la requête
  const queryFreq = calculateQueryFrequency(query);
  
  // Trouver les items en résonance
  const results = database.map(item => {
    const itemFreq = item.frequency || 444;
    const resonance = calculateResonance(queryFreq, itemFreq);
    
    return {
      item,
      resonance,
      isHarmonic: resonance > threshold
    };
  });
  
  // Filtrer et trier par résonance
  return results
    .filter(r => r.isHarmonic)
    .sort((a, b) => b.resonance - a.resonance)
    .map(r => ({
      ...r.item,
      sympathyScore: r.resonance
    }));
}

function calculateQueryFrequency(query) {
  // Utiliser l'Arithmos de la requête
  let sum = 0;
  const q = query.toUpperCase().replace(/[^A-Z]/g, '');
  const map = { A:1, B:2, C:3, D:4, E:5, F:6, G:7, H:8, I:9, J:1, K:2, L:3, M:4, N:5, O:6, P:7, Q:8, R:9, S:1, T:2, U:3, V:4, W:5, X:6, Y:7, Z:8 };
  
  for (const char of q) {
    sum += map[char] || 0;
  }
  
  while (sum > 9) {
    sum = sum.toString().split('').reduce((a, b) => a + parseInt(b), 0);
  }
  
  return sum * 111;
}

function calculateResonance(freq1, freq2) {
  const ratio = Math.max(freq1, freq2) / Math.min(freq1, freq2);
  const nearestHarmonic = Math.round(ratio);
  const deviation = Math.abs(ratio - nearestHarmonic);
  
  return Math.max(0, 1 - deviation);
}

// ═══════════════════════════════════════════════════════════════════════════════
// ÉNERGIE DU POINT ZÉRO
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * L'Énergie du Point Zéro est l'énergie résiduelle qui existe même au zéro absolu.
 * C'est la source d'énergie illimitée supposément utilisée par les Atlantes.
 */

export const ZERO_POINT_ENERGY = {
  name: "Énergie du Point Zéro",
  physics: "Énergie du vide quantique",
  formula: "E = ½ℏω", // Demi-quantum d'énergie
  
  // Dans AT·OM
  application: {
    input: "Aucun (auto-généré)",
    output: "Énergie de calcul illimitée",
    efficiency: 1.0, // 100% théorique
    sustainability: "Infinie"
  },
  
  // Niveaux d'activation
  levels: [
    { level: 1, power: 0.111, name: "Veille", status: "Minimal" },
    { level: 2, power: 0.222, name: "Éveil", status: "Bas" },
    { level: 3, power: 0.333, name: "Actif", status: "Modéré" },
    { level: 4, power: 0.444, name: "Stable", status: "Normal", isDefault: true },
    { level: 5, power: 0.555, name: "Amplifié", status: "Élevé" },
    { level: 6, power: 0.666, name: "Intensif", status: "Haute" },
    { level: 7, power: 0.777, name: "Maximum", status: "Très haute" },
    { level: 8, power: 0.888, name: "Surcharge", status: "Critique" },
    { level: 9, power: 0.999, name: "Transcendant", status: "Divin" }
  ]
};

/**
 * Calcule l'énergie disponible selon le niveau
 */
export function calculateZeroPointEnergy(level = 4) {
  const config = ZERO_POINT_ENERGY.levels.find(l => l.level === level) 
    || ZERO_POINT_ENERGY.levels[3];
  
  return {
    level: config.level,
    name: config.name,
    power: config.power,
    status: config.status,
    available: config.power * 1000, // Unités arbitraires
    unlimited: level === 9
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LES ANNEAUX DE POSÉIDON — ARCHITECTURE CONCENTRIQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Selon Platon, l'Atlantide était organisée en anneaux concentriques
 * alternant eau et terre, avec le temple de Poséidon au centre.
 */

export const POSEIDON_RINGS = {
  structure: [
    { ring: 0, type: "Centre", name: "Temple de Poséidon", access: "Divin", frequency: 999 },
    { ring: 1, type: "Terre", name: "Citadelle Royale", access: "Architecte", frequency: 888 },
    { ring: 2, type: "Eau", name: "Canal Intérieur", access: "Initiés", frequency: 777 },
    { ring: 3, type: "Terre", name: "Zone des Cristaux", access: "Gardiens", frequency: 666 },
    { ring: 4, type: "Eau", name: "Canal Médian", access: "Prêtres", frequency: 555 },
    { ring: 5, type: "Terre", name: "Zone de Calcul", access: "Opérateurs", frequency: 444 },
    { ring: 6, type: "Eau", name: "Canal Extérieur", access: "Public Élevé", frequency: 333 },
    { ring: 7, type: "Terre", name: "Périphérie", access: "Public", frequency: 222 },
    { ring: 8, type: "Eau", name: "Océan", access: "Tous", frequency: 111 }
  ],
  
  // Correspondance avec AT·OM
  atomMapping: {
    center: "Code source & Message de Gratitude",
    inner: "Moteurs civilisationnels",
    middle: "Logique de calcul",
    outer: "Interface utilisateur"
  }
};

/**
 * Détermine le niveau d'accès selon la fréquence
 */
export function getAccessLevel(frequency) {
  const ring = POSEIDON_RINGS.structure.find(r => r.frequency === frequency)
    || POSEIDON_RINGS.structure.find(r => r.frequency <= frequency);
  
  return {
    ring: ring?.ring || 8,
    type: ring?.type || "Eau",
    name: ring?.name || "Océan",
    access: ring?.access || "Tous"
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash).toString(16);
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la résonance atlante pour AT·OM
 */
export function getAtlantisResonance(arithmos, data = null) {
  const frequency = arithmos * 111;
  
  // Cristal correspondant
  const crystal = CRYSTAL_MATRIX.types.find(c => c.frequency === frequency)
    || CRYSTAL_MATRIX.types[3]; // Citrine par défaut
  
  // Niveau du vortex
  const vortexZone = VORTEX_SYSTEM.zones.find(z => z.hz === frequency)
    || VORTEX_SYSTEM.zones[3];
  
  // Niveau d'énergie
  const energy = calculateZeroPointEnergy(arithmos);
  
  // Anneau d'accès
  const access = getAccessLevel(frequency);
  
  // Capacité cristalline si données
  const crystalData = data ? encodeCrystalData(data, crystal.name) : null;
  
  return {
    // Cristal
    crystal: {
      name: crystal.name,
      color: crystal.color,
      function: crystal.function,
      frequency: crystal.frequency
    },
    
    // Vortex
    vortex: {
      level: vortexZone.level,
      position: vortexZone.position,
      density: vortexZone.density,
      flow: vortexZone.flow || "Stable"
    },
    
    // Énergie
    energy: {
      level: energy.level,
      name: energy.name,
      power: energy.power,
      status: energy.status
    },
    
    // Accès
    access: {
      ring: access.ring,
      zone: access.name,
      level: access.access
    },
    
    // Données encodées
    crystalData: crystalData ? {
      facets: crystalData.facets.length,
      key: crystalData.reconstructionKey
    } : null,
    
    // Orichalque
    orichalque: frequency === 999,
    
    // Message
    message: frequency === 999
      ? `🔱 Orichalque activé — Accès au Temple de Poséidon`
      : `💎 ${crystal.name} — ${vortexZone.position} du Vortex`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Constantes
  ATLANTIS_CONSTANTS,
  
  // Cristaux
  CRYSTAL_MATRIX,
  calculateCrystalCapacity,
  encodeCrystalData,
  
  // Vortex
  VORTEX_SYSTEM,
  vortexSort,
  sympatheticSearch,
  
  // Énergie
  ZERO_POINT_ENERGY,
  calculateZeroPointEnergy,
  
  // Anneaux
  POSEIDON_RINGS,
  getAccessLevel,
  
  // Intégration
  getAtlantisResonance
};
