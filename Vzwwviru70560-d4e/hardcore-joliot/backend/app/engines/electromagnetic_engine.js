/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ⚡ ELECTROMAGNETIC ENGINE — LA PHYSIQUE DU SIGNAL
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * L'électromagnétisme est le SIGNAL qui sort de l'écran pour toucher l'utilisateur.
 * Ce moteur transforme les fréquences AT·OM en propriétés physiques réelles.
 * 
 * 1. Spectre Électromagnétique — Traduction de la lumière
 * 2. Équations de Maxwell — Champ E + Champ B = Onde
 * 3. Vecteur de Poynting — Puissance du signal
 * 4. Le Tore (Torus) — La forme universelle de l'énergie
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @symbol ⚡
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES PHYSIQUES
// ═══════════════════════════════════════════════════════════════════════════════

export const PHYSICS_CONSTANTS = {
  c: 299792458,           // Vitesse de la lumière (m/s)
  h: 6.62607015e-34,      // Constante de Planck (J·s)
  hbar: 1.054571817e-34,  // Constante de Planck réduite
  e: 1.602176634e-19,     // Charge élémentaire (C)
  epsilon0: 8.854187817e-12, // Permittivité du vide
  mu0: 1.25663706212e-6,  // Perméabilité du vide
  k: 1.380649e-23,        // Constante de Boltzmann
  
  // Constante dérivée
  Z0: 376.730313668       // Impédance du vide (Ω)
};

// ═══════════════════════════════════════════════════════════════════════════════
// SPECTRE ÉLECTROMAGNÉTIQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le spectre EM complet, des ondes radio aux rayons gamma.
 * Chaque bande est associée à une fréquence AT·OM.
 */

export const EM_SPECTRUM = {
  RADIO: {
    name: "Ondes Radio",
    wavelength: { min: 1e-1, max: 1e5, unit: "m" },
    frequency: { min: 3e3, max: 3e9, unit: "Hz" },
    atomFrequency: 111, // AT·OM: Ancrage profond
    color: "#8B0000",
    quality: "Traverse les obstacles, voyage loin",
    applications: ["Communication", "Radar", "MRI"],
    element: "Terre",
    chakra: 1
  },
  
  MICROWAVE: {
    name: "Micro-ondes",
    wavelength: { min: 1e-3, max: 1e-1, unit: "m" },
    frequency: { min: 3e9, max: 3e11, unit: "Hz" },
    atomFrequency: 222,
    color: "#FF4500",
    quality: "Réchauffe la matière, transmet les données",
    applications: ["Four", "WiFi", "Satellites"],
    element: "Eau (chauffe)",
    chakra: 2
  },
  
  INFRARED: {
    name: "Infrarouge",
    wavelength: { min: 7e-7, max: 1e-3, unit: "m" },
    frequency: { min: 3e11, max: 4e14, unit: "Hz" },
    atomFrequency: 333,
    color: "#FF6347",
    quality: "Chaleur, vision nocturne",
    applications: ["Thermographie", "Télécommandes", "Astronomie"],
    element: "Feu (chaleur)",
    chakra: 3
  },
  
  VISIBLE: {
    name: "Lumière Visible",
    wavelength: { min: 380e-9, max: 700e-9, unit: "m" },
    frequency: { min: 4e14, max: 8e14, unit: "Hz" },
    atomFrequency: 444, // ANCRAGE CENTRAL
    color: "rainbow",
    quality: "L'interface entre l'homme et l'univers",
    applications: ["Vision", "Photosynthèse", "Communication"],
    element: "Air (perception)",
    chakra: 4,
    isAnchor: true,
    
    // Sous-bandes de la lumière visible
    bands: {
      red: { wavelength: 700e-9, frequency: 4.3e14, hex: "#FF0000", atomHz: 111 },
      orange: { wavelength: 620e-9, frequency: 4.8e14, hex: "#FF7F00", atomHz: 222 },
      yellow: { wavelength: 580e-9, frequency: 5.2e14, hex: "#FFFF00", atomHz: 333 },
      green: { wavelength: 530e-9, frequency: 5.7e14, hex: "#00FF00", atomHz: 444 },
      cyan: { wavelength: 490e-9, frequency: 6.1e14, hex: "#00FFFF", atomHz: 555 },
      blue: { wavelength: 450e-9, frequency: 6.7e14, hex: "#0000FF", atomHz: 666 },
      violet: { wavelength: 400e-9, frequency: 7.5e14, hex: "#8B00FF", atomHz: 777 }
    }
  },
  
  ULTRAVIOLET: {
    name: "Ultraviolet",
    wavelength: { min: 1e-8, max: 380e-9, unit: "m" },
    frequency: { min: 8e14, max: 3e16, unit: "Hz" },
    atomFrequency: 666,
    color: "#4B0082",
    quality: "Révèle l'invisible, stérilise",
    applications: ["Stérilisation", "Détection", "Bronzage"],
    element: "Éther (au-delà)",
    chakra: 6
  },
  
  XRAY: {
    name: "Rayons X",
    wavelength: { min: 1e-11, max: 1e-8, unit: "m" },
    frequency: { min: 3e16, max: 3e19, unit: "Hz" },
    atomFrequency: 888,
    color: "#00CED1",
    quality: "Pénètre la matière, révèle la structure",
    applications: ["Médecine", "Sécurité", "Cristallographie"],
    element: "Lumière pure",
    chakra: 7
  },
  
  GAMMA: {
    name: "Rayons Gamma",
    wavelength: { min: 0, max: 1e-11, unit: "m" },
    frequency: { min: 3e19, max: Infinity, unit: "Hz" },
    atomFrequency: 999, // Information pure
    color: "#FFFFFF",
    quality: "Énergie maximale, origine cosmique",
    applications: ["Médecine nucléaire", "Astronomie gamma"],
    element: "Conscience pure",
    chakra: 7
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// CALCULS ÉLECTROMAGNÉTIQUES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule la longueur d'onde à partir de la fréquence
 * λ = c / f
 */
export function wavelengthFromFrequency(frequency) {
  return PHYSICS_CONSTANTS.c / frequency;
}

/**
 * Calcule la fréquence à partir de la longueur d'onde
 * f = c / λ
 */
export function frequencyFromWavelength(wavelength) {
  return PHYSICS_CONSTANTS.c / wavelength;
}

/**
 * Calcule l'énergie d'un photon
 * E = h × f
 */
export function photonEnergy(frequency) {
  const joules = PHYSICS_CONSTANTS.h * frequency;
  const electronVolts = joules / PHYSICS_CONSTANTS.e;
  
  return {
    joules,
    electronVolts,
    scientific: joules.toExponential(3) + " J"
  };
}

/**
 * Calcule la couleur hexadécimale pour une longueur d'onde visible
 */
export function wavelengthToColor(wavelength) {
  // Convertir en nanomètres si nécessaire
  const nm = wavelength > 1 ? wavelength : wavelength * 1e9;
  
  let r, g, b;
  
  if (nm >= 380 && nm < 440) {
    r = -(nm - 440) / (440 - 380);
    g = 0;
    b = 1;
  } else if (nm >= 440 && nm < 490) {
    r = 0;
    g = (nm - 440) / (490 - 440);
    b = 1;
  } else if (nm >= 490 && nm < 510) {
    r = 0;
    g = 1;
    b = -(nm - 510) / (510 - 490);
  } else if (nm >= 510 && nm < 580) {
    r = (nm - 510) / (580 - 510);
    g = 1;
    b = 0;
  } else if (nm >= 580 && nm < 645) {
    r = 1;
    g = -(nm - 645) / (645 - 580);
    b = 0;
  } else if (nm >= 645 && nm <= 780) {
    r = 1;
    g = 0;
    b = 0;
  } else {
    r = 0;
    g = 0;
    b = 0;
  }
  
  // Convertir en hex
  const toHex = (v) => Math.round(v * 255).toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
}

// ═══════════════════════════════════════════════════════════════════════════════
// VECTEUR DE POYNTING — PUISSANCE DU SIGNAL
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Vecteur de Poynting S = E × H représente le flux d'énergie.
 * Dans notre système, il mesure l'IMPACT de l'information.
 */

export function calculatePoyntingVector(electricField, magneticField) {
  // S = E × H (produit vectoriel)
  // Simplifié pour des champs scalaires
  const magnitude = electricField * magneticField;
  
  return {
    magnitude,
    power: magnitude, // W/m²
    intensity: magnitude > 100 ? "Haute" : magnitude > 10 ? "Moyenne" : "Basse",
    impact: Math.log10(magnitude + 1) // Échelle logarithmique pour l'UI
  };
}

/**
 * Calcule l'impact "émotionnel" d'une recherche basé sur la fréquence
 */
export function calculateSignalImpact(atomFrequency, userResonance = 444) {
  // L'intention de l'utilisateur (champ électrique)
  const E = atomFrequency / 111; // Normalisé
  
  // La mémoire du système (champ magnétique)
  const H = userResonance / 111;
  
  // Vecteur de Poynting
  const S = calculatePoyntingVector(E, H);
  
  // Résonance si les fréquences sont harmoniques
  const ratio = Math.max(atomFrequency, userResonance) / Math.min(atomFrequency, userResonance);
  const isHarmonic = Math.abs(ratio - Math.round(ratio)) < 0.1;
  
  return {
    electricField: E,
    magneticField: H,
    poynting: S,
    isHarmonic,
    resonanceBoost: isHarmonic ? 1.5 : 1.0,
    totalImpact: S.impact * (isHarmonic ? 1.5 : 1.0)
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LE TORE (TORUS) — LA FORME UNIVERSELLE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Tore est la forme fondamentale de l'énergie dans l'univers.
 * On le retrouve dans: atomes, galaxies, champ magnétique terrestre, cœur humain.
 */

export const TORUS = {
  name: "Tore",
  description: "Le flux universel d'énergie",
  
  // Géométrie
  geometry: {
    majorRadius: "R", // Distance du centre du tube au centre du tore
    minorRadius: "r", // Rayon du tube
    surfaceArea: "4π²Rr",
    volume: "2π²Rr²"
  },
  
  // Flux énergétique
  flow: {
    entry: "Pôle Nord (réception)",
    exit: "Pôle Sud (émission)",
    cycle: "L'énergie circule en boucle continue"
  },
  
  // Exemples naturels
  examples: [
    { name: "Champ magnétique terrestre", scale: "planétaire" },
    { name: "Champ magnétique du cœur", scale: "humain" },
    { name: "Structure des galaxies", scale: "cosmique" },
    { name: "Structure atomique", scale: "quantique" },
    { name: "Pomme (coupe transversale)", scale: "naturel" }
  ],
  
  // AT·OM
  atomConnection: {
    north: "Input utilisateur (Questions)",
    south: "Output Oracle (Réponses)",
    center: "444 Hz (Ancrage)"
  }
};

/**
 * Génère les coordonnées d'un tore pour visualisation 3D
 */
export function generateTorusPoints(R = 3, r = 1, segments = 32, rings = 16) {
  const points = [];
  
  for (let i = 0; i <= rings; i++) {
    const theta = (i / rings) * 2 * Math.PI;
    for (let j = 0; j <= segments; j++) {
      const phi = (j / segments) * 2 * Math.PI;
      
      const x = (R + r * Math.cos(phi)) * Math.cos(theta);
      const y = (R + r * Math.cos(phi)) * Math.sin(theta);
      const z = r * Math.sin(phi);
      
      points.push({ x, y, z, theta, phi });
    }
  }
  
  return points;
}

// ═══════════════════════════════════════════════════════════════════════════════
// CORRESPONDANCE AT·OM ↔ SPECTRE EM
// ═══════════════════════════════════════════════════════════════════════════════

export const ATOM_TO_SPECTRUM = {
  111: { band: "RADIO", element: "Terre", solid: "Cube", stability: "Ancrage profond" },
  222: { band: "MICROWAVE", element: "Eau", solid: "Icosaèdre", stability: "Flux de données" },
  333: { band: "INFRARED", element: "Feu", solid: "Tétraèdre", stability: "Chaleur transformatrice" },
  444: { band: "VISIBLE", element: "Air", solid: "Octaèdre", stability: "ANCRAGE CENTRAL" },
  555: { band: "VISIBLE", element: "Éther", solid: "Tétraèdre", stability: "Mouvement vital" },
  666: { band: "ULTRAVIOLET", element: "Lumière", solid: "Octaèdre", stability: "Révélation" },
  777: { band: "ULTRAVIOLET", element: "Son", solid: "Dodécaèdre", stability: "Introspection" },
  888: { band: "XRAY", element: "Pensée", solid: "Octaèdre", stability: "Pénétration" },
  999: { band: "GAMMA", element: "Conscience", solid: "Dodécaèdre", stability: "Unité absolue" }
};

// ═══════════════════════════════════════════════════════════════════════════════
// INTÉGRATION AVEC AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule la signature électromagnétique complète
 */
export function calculateEMSignature(arithmos, atomFrequency) {
  const mapping = ATOM_TO_SPECTRUM[atomFrequency] || ATOM_TO_SPECTRUM[444];
  const spectrum = EM_SPECTRUM[mapping.band];
  
  // Calculer une longueur d'onde fictive basée sur la fréquence AT·OM
  // (mapping symbolique, pas physique réel)
  const symbolicWavelength = 700 - (atomFrequency / 999) * 320; // 700nm (rouge) à 380nm (violet)
  const color = wavelengthToColor(symbolicWavelength);
  
  // Énergie du photon (symbolique)
  const energy = photonEnergy(atomFrequency * 1e12); // THz range symbolique
  
  // Impact du signal
  const impact = calculateSignalImpact(atomFrequency);
  
  return {
    // Bande du spectre
    spectrum: {
      band: spectrum.name,
      quality: spectrum.quality,
      element: spectrum.element,
      chakra: spectrum.chakra
    },
    
    // Propriétés physiques (symboliques)
    physics: {
      wavelength: symbolicWavelength + " nm (symbolique)",
      energy: energy,
      color: color
    },
    
    // Solide de Platon associé
    solid: mapping.solid,
    
    // Impact
    impact: {
      intensity: impact.totalImpact,
      isHarmonic: impact.isHarmonic,
      poynting: impact.poynting.intensity
    },
    
    // Tore
    torus: {
      input: "Votre question",
      output: "La réponse de l'Oracle",
      center: `${atomFrequency} Hz`
    },
    
    // Couleur UI
    uiGlow: color,
    
    // Message
    message: `⚡ Signal ${spectrum.name} — ${mapping.stability}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Constantes
  PHYSICS_CONSTANTS,
  EM_SPECTRUM,
  ATOM_TO_SPECTRUM,
  TORUS,
  
  // Fonctions
  wavelengthFromFrequency,
  frequencyFromWavelength,
  photonEnergy,
  wavelengthToColor,
  calculatePoyntingVector,
  calculateSignalImpact,
  generateTorusPoints,
  calculateEMSignature
};
