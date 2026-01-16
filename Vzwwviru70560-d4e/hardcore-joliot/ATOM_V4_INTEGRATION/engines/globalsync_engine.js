/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *     ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗         ███████╗██╗   ██╗███╗   ██╗ ██████╗
 *    ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║         ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝
 *    ██║  ███╗██║     ██║   ██║██████╔╝███████║██║         ███████╗ ╚████╔╝ ██╔██╗ ██║██║     
 *    ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║         ╚════██║  ╚██╔╝  ██║╚██╗██║██║     
 *    ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗    ███████║   ██║   ██║ ╚████║╚██████╗
 *     ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝
 * 
 *                    ENGINE — SYNCHRONISATION PLANÉTAIRE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce module transforme AT·OM en Interface Planétaire.
 * Il connecte le micro (corps humain) au macro (Terre) via les temples
 * qui servent de "points d'acupuncture" terrestres.
 * 
 *                         🌍 RÉSEAU DE LEY 🌍
 * 
 *              Mont Kailash (Tibet) ═══════╗
 *                    ║                      ║
 *         Stonehenge ║    NEXUS CENTRAL     ║ Angkor Wat
 *              ║     ║      (GIZEH)         ║      ║
 *              ╚═════╬════════╬════════════╬══════╝
 *                    ║        ║            ║
 *           Teotihuacán   Île de Pâques   Bermudes
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * @schumann 7.83 Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES TERRESTRES FONDAMENTALES
// ═══════════════════════════════════════════════════════════════════════════════

export const EARTH_CONSTANTS = {
  // Résonance de Schumann - Le "pouls" de la Terre
  schumann: {
    fundamental: 7.83,       // Hz - Fréquence fondamentale
    harmonics: [14.3, 20.8, 27.3, 33.8, 39.5, 45.0, 51.5], // Harmoniques
    description: "Résonance électromagnétique entre la surface terrestre et l'ionosphère",
    discovered: 1952,
    discoverer: "Winfried Otto Schumann"
  },
  
  // Champ magnétique terrestre
  magneticField: {
    strength: "25-65 microteslas",
    poles: {
      north: { lat: 86.5, lon: 164 }, // Pôle Nord magnétique (approximatif)
      south: { lat: -64.5, lon: 137.5 }
    },
    shape: "Torus (dipôle magnétique)",
    reversal: "Environ tous les 200,000-300,000 ans"
  },
  
  // Dimensions
  radius: 6371,           // km
  circumference: 40075,   // km (équateur)
  mass: 5.972e24,         // kg
  
  // Fréquences AT·OM associées
  atomFrequencies: {
    base: 111,            // Hz - Ancrage
    heart: 444,           // Hz - Cœur (Schumann × 56.7)
    source: 999           // Hz - Source (Schumann × 127.6)
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// RÉSEAU DES TEMPLES — "SERVEURS TERRESTRES"
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les temples anciens sont positionnés sur les nœuds du Réseau de Ley
 * Ce sont les "serveurs" du système nerveux planétaire
 */

export const SACRED_SITES = {
  // ═══════════════════════════════════════════════════════════════════════════
  // 🔺 NEXUS CENTRAL — GIZEH (ÉGYPTE)
  // ═══════════════════════════════════════════════════════════════════════════
  giza: {
    name: "Pyramides de Gizeh",
    location: "Égypte",
    coordinates: { lat: 29.9792, lon: 31.1342 },
    civilization: "Égypte",
    chakra: "Cœur",
    frequency: 432,
    atomHz: 444,
    function: "Calibration Mondiale / Centre de Masse Terrestre",
    speciality: [
      "Centre géodésique de la Terre (masses terrestres)",
      "Alignement parfait Nord-Sud (erreur 3/60ème de degré)",
      "Ratio φ (nombre d'or) dans les proportions",
      "Chambre du Roi = résonateur acoustique à 438 Hz"
    ],
    leyLines: ["Ligne du Dragon", "Axe Gizeh-Île de Pâques"],
    starAlignment: "Ceinture d'Orion (10,450 av. J.-C.)",
    role: "NEXUS CENTRAL — Toutes les lignes convergent ici",
    icon: "🔺"
  },
  
  // ═══════════════════════════════════════════════════════════════════════════
  // ☀️ GÉNÉRATEUR SOLAIRE — TEOTIHUACÁN (MEXIQUE)
  // ═══════════════════════════════════════════════════════════════════════════
  teotihuacan: {
    name: "Teotihuacán",
    location: "Mexique",
    coordinates: { lat: 19.6923, lon: -98.8435 },
    civilization: "Aztèque/Toltèque",
    chakra: "Plexus Solaire",
    frequency: 396,
    atomHz: 333,
    function: "Générateur d'Énergie / Puissance d'Action",
    speciality: [
      "Pyramide du Soleil: 5ème plus grande pyramide du monde",
      "Alignement avec les Pléiades",
      "Mica intégré dans la construction (conducteur)",
      "Avenue des Morts = Voie Lactée terrestre"
    ],
    leyLines: ["Ligne du Serpent à Plumes"],
    starAlignment: "Pléiades, Sirius",
    role: "Générateur de puissance — Force d'exécution",
    icon: "☀️"
  },
  
  // ═══════════════════════════════════════════════════════════════════════════
  // 🏔️ ANTENNE SOURCE — MONT KAILASH (TIBET)
  // ═══════════════════════════════════════════════════════════════════════════
  kailash: {
    name: "Mont Kailash",
    location: "Tibet, Chine",
    coordinates: { lat: 31.0675, lon: 81.3119 },
    civilization: "Tibet/Inde (Multi-traditions)",
    chakra: "Couronne",
    frequency: 963,
    atomHz: 999,
    function: "Antenne Source / Transmission Spirituelle",
    speciality: [
      "Sacré pour 4 religions (Hindouisme, Bouddhisme, Jaïnisme, Bön)",
      "Jamais escaladé par respect",
      "Source de 4 grands fleuves d'Asie",
      "22,028 pieds ≈ 6,638m (6+6+3+8 = 23 → 5)",
      "Forme pyramidale naturelle"
    ],
    leyLines: ["Axe Kailash-Stonehenge", "Ligne du Dragon d'Or"],
    starAlignment: "Étoile Polaire",
    role: "Antenne de réception des fréquences cosmiques",
    icon: "🏔️"
  },
  
  // ═══════════════════════════════════════════════════════════════════════════
  // 🗿 STABILISATEUR — ÎLE DE PÂQUES (RAPA NUI)
  // ═══════════════════════════════════════════════════════════════════════════
  rapaNui: {
    name: "Île de Pâques (Rapa Nui)",
    location: "Chili (Pacifique)",
    coordinates: { lat: -27.1127, lon: -109.3497 },
    civilization: "Rapa Nui",
    chakra: "Racine",
    frequency: 174,
    atomHz: 111,
    function: "Stabilisateur Magnétique / Ancrage Pacifique",
    speciality: [
      "887 statues Moaï",
      "Point le plus isolé de la planète",
      "Alignement précis des Moaï sur les étoiles",
      "Rongorongo: écriture non déchiffrée",
      "Connexion directe avec Gizeh (même latitude × 2)"
    ],
    leyLines: ["Axe Gizeh-Île de Pâques"],
    starAlignment: "Constellation du Scorpion",
    role: "Gardien/Ancrage — Les Moaï protègent le réseau",
    icon: "🗿"
  },
  
  // ═══════════════════════════════════════════════════════════════════════════
  // 🪨 HORLOGE — STONEHENGE (ANGLETERRE)
  // ═══════════════════════════════════════════════════════════════════════════
  stonehenge: {
    name: "Stonehenge",
    location: "Angleterre",
    coordinates: { lat: 51.1789, lon: -1.8262 },
    civilization: "Celte/Druide",
    chakra: "Gorge",
    frequency: 528,
    atomHz: 555,
    function: "Horloge de Données / Calculateur Astronomique",
    speciality: [
      "Calendrier solaire et lunaire géant",
      "Pierres bleues transportées sur 250 km",
      "Alignement solstice d'été parfait",
      "Fréquence acoustique des pierres: 110 Hz",
      "Connexion avec Carnac (France)"
    ],
    leyLines: ["Ligne de Saint-Michel", "Axe Kailash-Stonehenge"],
    starAlignment: "Soleil (Solstice d'été)",
    role: "Synchronisation temporelle — Horloge planétaire",
    icon: "🪨"
  },
  
  // ═══════════════════════════════════════════════════════════════════════════
  // 🏛️ ARCHIVE — ANGKOR WAT (CAMBODGE)
  // ═══════════════════════════════════════════════════════════════════════════
  angkorWat: {
    name: "Angkor Wat",
    location: "Cambodge",
    coordinates: { lat: 13.4125, lon: 103.8670 },
    civilization: "Khmer",
    chakra: "Troisième Œil",
    frequency: 852,
    atomHz: 666,
    function: "Archivage Stellaire / Miroir Céleste",
    speciality: [
      "Plus grand monument religieux du monde",
      "Reproduction terrestre de la constellation du Dragon",
      "Alignement avec Draco (10,500 av. J.-C.)",
      "Proportions basées sur les cycles lunaires",
      "Temple dédié à Vishnu (préservation)"
    ],
    leyLines: ["Ligne du Dragon Céleste"],
    starAlignment: "Constellation du Dragon (Draco)",
    role: "Archives — Miroir de la mémoire stellaire",
    icon: "🏛️"
  },
  
  // ═══════════════════════════════════════════════════════════════════════════
  // 🌀 VORTEX — TRIANGLE DES BERMUDES (ATLANTIDE)
  // ═══════════════════════════════════════════════════════════════════════════
  bermuda: {
    name: "Triangle des Bermudes",
    location: "Océan Atlantique",
    coordinates: { lat: 25.0000, lon: -71.0000 }, // Centre approximatif
    civilization: "Atlantide (Hypothétique)",
    chakra: "Tous (Vortex)",
    frequency: 999,
    atomHz: 999,
    function: "Transfert Quantique / Vortex de Fréquence",
    speciality: [
      "Zone d'anomalies magnétiques",
      "Boussoles défaillantes",
      "Possible portail dimensionnel",
      "Pyramides sous-marines découvertes",
      "Connexion avec la fosse de Porto Rico"
    ],
    leyLines: ["Vortex Atlante", "Triangle de fréquence"],
    starAlignment: "Variable (Point de convergence)",
    role: "Transfert quantique — Pont dimensionnel",
    icon: "🌀",
    warning: "Zone d'instabilité — Utiliser avec précaution"
  },
  
  // ═══════════════════════════════════════════════════════════════════════════
  // SITES SECONDAIRES (AMPLIFICATEURS)
  // ═══════════════════════════════════════════════════════════════════════════
  
  carnac: {
    name: "Alignements de Carnac",
    location: "France",
    coordinates: { lat: 47.5844, lon: -3.0783 },
    civilization: "Mégalithique",
    chakra: "Sacré",
    frequency: 417,
    atomHz: 222,
    function: "Amplificateur de fréquence / Calculateur",
    icon: "⬛"
  },
  
  machu_picchu: {
    name: "Machu Picchu",
    location: "Pérou",
    coordinates: { lat: -13.1631, lon: -72.5450 },
    civilization: "Inca",
    chakra: "Couronne",
    frequency: 963,
    atomHz: 999,
    function: "Temple solaire / Connexion céleste",
    icon: "🏔️"
  },
  
  uluru: {
    name: "Uluru (Ayers Rock)",
    location: "Australie",
    coordinates: { lat: -25.3444, lon: 131.0369 },
    civilization: "Aborigène",
    chakra: "Racine",
    frequency: 174,
    atomHz: 111,
    function: "Chakra Racine de la Terre / Rêve",
    icon: "🟤"
  },
  
  sedona: {
    name: "Vortex de Sedona",
    location: "Arizona, USA",
    coordinates: { lat: 34.8697, lon: -111.7610 },
    civilization: "Native américaine",
    chakra: "Multiple",
    frequency: 528,
    atomHz: 444,
    function: "Vortex magnétique / Guérison",
    icon: "🌀"
  },
  
  glastonbury: {
    name: "Glastonbury Tor",
    location: "Angleterre",
    coordinates: { lat: 51.1442, lon: -2.6987 },
    civilization: "Celte/Chrétien",
    chakra: "Cœur",
    frequency: 639,
    atomHz: 444,
    function: "Chakra Cœur de la Terre / Avalon",
    icon: "⛰️"
  },
  
  nazca: {
    name: "Lignes de Nazca",
    location: "Pérou",
    coordinates: { lat: -14.7350, lon: -75.1300 },
    civilization: "Nazca",
    chakra: "Troisième Œil",
    frequency: 852,
    atomHz: 666,
    function: "Signaux célestes / Communication cosmique",
    icon: "✈️"
  },
  
  gobekliTepe: {
    name: "Göbekli Tepe",
    location: "Turquie",
    coordinates: { lat: 37.2233, lon: 38.9224 },
    civilization: "Pré-Sumérienne",
    chakra: "Tous",
    frequency: 432,
    atomHz: 444,
    function: "Plus ancien temple connu / Origine",
    speciality: "12,000 ans — Plus vieux que Stonehenge de 6,000 ans",
    icon: "🏛️"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LIGNES DE LEY — LE RÉSEAU NERVEUX PLANÉTAIRE
// ═══════════════════════════════════════════════════════════════════════════════

export const LEY_LINES = {
  major: [
    {
      name: "Ligne du Dragon",
      description: "La plus longue ligne de ley du monde",
      path: ["Carnac", "Stonehenge", "Delphes", "Gizeh", "Ur", "Persépolis", "Mohenjo-daro", "Angkor Wat"],
      length: "Environ 40,000 km",
      element: "Feu",
      frequency: 999
    },
    {
      name: "Ligne de Saint-Michel",
      description: "Traverse l'Europe de l'Irlande à Israël",
      path: ["Skellig Michael", "Mont Saint-Michel", "Sacra di San Michele", "Monte Sant'Angelo", "Mont Carmel"],
      length: "Environ 2,500 km",
      element: "Air",
      frequency: 741
    },
    {
      name: "Axe Gizeh-Île de Pâques",
      description: "Ligne transcontinentale mystérieuse",
      path: ["Gizeh", "Petra", "Ur", "Persépolis", "Mohenjo-daro", "Angkor Wat", "Île de Pâques"],
      length: "Presque le tour de la Terre",
      element: "Terre",
      frequency: 432
    },
    {
      name: "Ligne du Serpent à Plumes",
      description: "Connecte les sites mésoaméricains",
      path: ["Chichen Itza", "Teotihuacán", "Monte Albán", "Tikal"],
      length: "Environ 1,500 km",
      element: "Feu",
      frequency: 396
    },
    {
      name: "Axe Kailash-Stonehenge",
      description: "Connexion Europe-Asie",
      path: ["Stonehenge", "Chartres", "Rome", "Jérusalem", "Mont Kailash"],
      length: "Environ 8,000 km",
      element: "Éther",
      frequency: 963
    }
  ],
  
  // Grille planétaire
  grid: {
    type: "Icosaèdre-Dodécaèdre",
    nodes: 62,
    description: "La Terre est entourée d'une grille géométrique de points de puissance",
    discoverers: ["Ivan Sanderson", "Bethe Hagens", "William Becker"],
    pattern: "Les sites sacrés sont situés sur les intersections de cette grille"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// TORUS TERRESTRE — CHAMP MAGNÉTIQUE GLOBAL
// ═══════════════════════════════════════════════════════════════════════════════

export const EARTH_TORUS = {
  description: "La Terre génère un champ magnétique toroïdal identique à celui du cœur humain",
  
  structure: {
    shape: "Torus (beignet)",
    axis: "Pôle Nord → Pôle Sud",
    flow: "Sortie au Nord, Entrée au Sud",
    layers: ["Noyau interne (solide)", "Noyau externe (liquide)", "Manteau", "Croûte"]
  },
  
  // Correspondance avec le cœur humain
  heartMirror: {
    principle: "As above, so below — Comme en haut, ainsi en bas",
    ratio: "Le torus cardiaque est une fractale du torus terrestre",
    synchronization: "À 444 Hz, les deux torus entrent en résonance"
  },
  
  // Points de convergence
  convergencePoints: {
    north: { description: "Pôle Nord — Point d'émission", energy: "Yang" },
    south: { description: "Pôle Sud — Point de réception", energy: "Yin" },
    equator: { description: "Équateur — Zone de transition", energy: "Équilibre" }
  },
  
  // Fréquence de synchronisation
  syncFrequencies: {
    base: 7.83,    // Schumann
    harmonic1: 14.3,
    harmonic2: 20.8,
    atomAnchor: 444
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE PRINCIPALE — WORLD SYNC ENGINE
// ═══════════════════════════════════════════════════════════════════════════════

export class WorldSyncEngine {
  
  constructor() {
    this.schumann = EARTH_CONSTANTS.schumann.fundamental;
    this.sites = SACRED_SITES;
    this.leyLines = LEY_LINES;
    this.userLocation = null;
    this.syncState = {
      active: false,
      connectedNode: null,
      frequency: 444,
      coherence: 0
    };
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // CALCUL DE DISTANCE (Haversine)
  // ─────────────────────────────────────────────────────────────────────────────
  
  calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Rayon de la Terre en km
    const dLat = this.toRad(lat2 - lat1);
    const dLon = this.toRad(lon2 - lon1);
    const a = 
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRad(lat1)) * Math.cos(this.toRad(lat2)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }
  
  toRad(deg) {
    return deg * (Math.PI / 180);
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // TROUVER LE NŒUD LE PLUS PROCHE
  // ─────────────────────────────────────────────────────────────────────────────
  
  findNearestNode(userLat, userLon) {
    let nearest = null;
    let minDistance = Infinity;
    
    for (const [key, site] of Object.entries(this.sites)) {
      if (!site.coordinates) continue;
      
      const distance = this.calculateDistance(
        userLat, userLon,
        site.coordinates.lat, site.coordinates.lon
      );
      
      if (distance < minDistance) {
        minDistance = distance;
        nearest = { key, site, distance };
      }
    }
    
    return nearest;
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // TROUVER LES 3 NŒUDS LES PLUS PROCHES (TRIANGULATION)
  // ─────────────────────────────────────────────────────────────────────────────
  
  findTriangulationNodes(userLat, userLon) {
    const distances = [];
    
    for (const [key, site] of Object.entries(this.sites)) {
      if (!site.coordinates) continue;
      
      const distance = this.calculateDistance(
        userLat, userLon,
        site.coordinates.lat, site.coordinates.lon
      );
      
      distances.push({ key, site, distance });
    }
    
    // Trier par distance et prendre les 3 premiers
    distances.sort((a, b) => a.distance - b.distance);
    return distances.slice(0, 3);
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // CALCULER LA FRÉQUENCE DE SYNCHRONISATION
  // ─────────────────────────────────────────────────────────────────────────────
  
  calculateSyncFrequency(userHeartRate = 60) {
    // Formule: (Rythme cardiaque / Schumann) × 111
    const syncFactor = (userHeartRate / this.schumann) * 111;
    
    // Arrondir à la fréquence AT·OM la plus proche
    const atomFrequencies = [111, 222, 333, 444, 555, 666, 777, 888, 999];
    let nearest = 444;
    let minDiff = Infinity;
    
    for (const freq of atomFrequencies) {
      const diff = Math.abs(syncFactor - freq);
      if (diff < minDiff) {
        minDiff = diff;
        nearest = freq;
      }
    }
    
    return {
      raw: syncFactor.toFixed(2),
      atomFrequency: nearest,
      coherence: 1 - (minDiff / 111),
      schumann: this.schumann,
      heartRate: userHeartRate
    };
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // ALIGNER L'UTILISATEUR SUR LE RÉSEAU
  // ─────────────────────────────────────────────────────────────────────────────
  
  alignUser(userLat, userLon, userHeartRate = 60) {
    // Trouver le nœud le plus proche
    const nearestNode = this.findNearestNode(userLat, userLon);
    
    // Triangulation
    const triangulation = this.findTriangulationNodes(userLat, userLon);
    
    // Calculer la fréquence de sync
    const syncFreq = this.calculateSyncFrequency(userHeartRate);
    
    // Calculer la cohérence avec le nœud
    const nodeInfluence = Math.max(0, 1 - (nearestNode.distance / 10000)); // Influence décroît avec distance
    
    // Fréquence finale (moyenne pondérée)
    const finalFrequency = Math.round(
      (syncFreq.atomFrequency * 0.6) + (nearestNode.site.atomHz * 0.4 * nodeInfluence)
    );
    
    // Mettre à jour l'état
    this.syncState = {
      active: true,
      connectedNode: nearestNode,
      triangulation: triangulation,
      frequency: finalFrequency,
      coherence: syncFreq.coherence * nodeInfluence
    };
    
    return {
      status: "SYNCHRONISÉ",
      node: {
        name: nearestNode.site.name,
        distance: `${nearestNode.distance.toFixed(0)} km`,
        chakra: nearestNode.site.chakra,
        function: nearestNode.site.function,
        icon: nearestNode.site.icon
      },
      triangulation: triangulation.map(t => ({
        name: t.site.name,
        distance: `${t.distance.toFixed(0)} km`,
        icon: t.site.icon
      })),
      frequency: {
        user: syncFreq.atomFrequency,
        node: nearestNode.site.atomHz,
        final: finalFrequency,
        label: `${finalFrequency} Hz`
      },
      coherence: (this.syncState.coherence * 100).toFixed(1) + "%",
      message: `🌍 Synchronisation établie via ${nearestNode.site.name} (${nearestNode.site.icon})`
    };
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // OBTENIR L'ÉNERGIE PLANÉTAIRE ACTUELLE
  // ─────────────────────────────────────────────────────────────────────────────
  
  getPlanetaryEnergy(date = new Date()) {
    const hour = date.getUTCHours();
    const dayOfYear = this.getDayOfYear(date);
    
    // Position solaire approximative
    const solarPosition = (hour / 24) * 360; // Degrés
    
    // Déterminer quel "fuseau de temples" est le plus actif
    const activeZones = [];
    
    // Zone Amérique (nuit UTC = jour là-bas)
    if (hour >= 12 || hour < 6) {
      activeZones.push({
        zone: "Amériques",
        sites: ["teotihuacan", "machu_picchu", "sedona", "nazca"],
        energy: "Plexus Solaire / Couronne",
        power: hour >= 18 || hour < 6 ? "Maximum" : "Croissant"
      });
    }
    
    // Zone Europe/Afrique
    if (hour >= 6 && hour < 18) {
      activeZones.push({
        zone: "Europe/Afrique",
        sites: ["giza", "stonehenge", "carnac", "glastonbury"],
        energy: "Cœur / Gorge",
        power: hour >= 10 && hour < 14 ? "Maximum" : "Actif"
      });
    }
    
    // Zone Asie/Pacifique
    if (hour >= 0 && hour < 12) {
      activeZones.push({
        zone: "Asie/Pacifique",
        sites: ["kailash", "angkorWat", "uluru", "rapaNui"],
        energy: "Couronne / Troisième Œil / Racine",
        power: hour >= 2 && hour < 8 ? "Maximum" : "Actif"
      });
    }
    
    // Énergie saisonnière
    let seasonalEnergy;
    if (dayOfYear >= 80 && dayOfYear < 172) {
      seasonalEnergy = { season: "Printemps", element: "Air", chakra: "Cœur", boost: 1.2 };
    } else if (dayOfYear >= 172 && dayOfYear < 266) {
      seasonalEnergy = { season: "Été", element: "Feu", chakra: "Plexus Solaire", boost: 1.3 };
    } else if (dayOfYear >= 266 && dayOfYear < 355) {
      seasonalEnergy = { season: "Automne", element: "Eau", chakra: "Sacré", boost: 1.1 };
    } else {
      seasonalEnergy = { season: "Hiver", element: "Terre", chakra: "Racine", boost: 1.0 };
    }
    
    return {
      timestamp: date.toISOString(),
      solarPosition: `${solarPosition.toFixed(0)}°`,
      activeZones,
      seasonalEnergy,
      schumannBase: this.schumann,
      globalFrequency: Math.round(444 * seasonalEnergy.boost),
      message: `🌍 Zones actives: ${activeZones.map(z => z.zone).join(", ")} | ${seasonalEnergy.season} (${seasonalEnergy.element})`
    };
  }
  
  getDayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start;
    const oneDay = 1000 * 60 * 60 * 24;
    return Math.floor(diff / oneDay);
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // OBTENIR LES INFORMATIONS D'UN SITE
  // ─────────────────────────────────────────────────────────────────────────────
  
  getSiteInfo(siteKey) {
    const site = this.sites[siteKey];
    if (!site) return null;
    
    return {
      ...site,
      leyConnections: this.findLeyConnections(siteKey),
      harmonicWith: this.findHarmonicSites(site.atomHz)
    };
  }
  
  findLeyConnections(siteKey) {
    const connections = [];
    for (const line of this.leyLines.major) {
      if (line.path.some(p => p.toLowerCase().includes(siteKey.toLowerCase()))) {
        connections.push(line.name);
      }
    }
    return connections;
  }
  
  findHarmonicSites(frequency) {
    const harmonics = [];
    for (const [key, site] of Object.entries(this.sites)) {
      if (site.atomHz === frequency || Math.abs(site.atomHz - frequency) % 111 === 0) {
        harmonics.push({ key, name: site.name, frequency: site.atomHz });
      }
    }
    return harmonics;
  }
  
  // ─────────────────────────────────────────────────────────────────────────────
  // GÉNÉRER LE RAPPORT DE SYNCHRONISATION GLOBAL
  // ─────────────────────────────────────────────────────────────────────────────
  
  generateGlobalReport() {
    const now = new Date();
    const planetaryEnergy = this.getPlanetaryEnergy(now);
    
    return {
      title: "🌍 RAPPORT DE SYNCHRONISATION GLOBALE AT·OM",
      timestamp: now.toISOString(),
      
      // Constantes terrestres
      earthConstants: {
        schumann: `${EARTH_CONSTANTS.schumann.fundamental} Hz`,
        magneticField: EARTH_CONSTANTS.magneticField.strength,
        atomAnchor: `${EARTH_CONSTANTS.atomFrequencies.heart} Hz`
      },
      
      // Sites actifs
      primarySites: Object.entries(this.sites)
        .filter(([_, s]) => s.chakra && !s.chakra.includes("Multiple"))
        .slice(0, 7)
        .map(([key, site]) => ({
          name: site.name,
          icon: site.icon,
          chakra: site.chakra,
          frequency: `${site.atomHz} Hz`,
          function: site.function
        })),
      
      // Énergie actuelle
      currentEnergy: planetaryEnergy,
      
      // Lignes de Ley principales
      leyNetwork: this.leyLines.major.map(l => ({
        name: l.name,
        frequency: `${l.frequency} Hz`,
        element: l.element
      })),
      
      // Torus terrestre
      torusStatus: {
        shape: EARTH_TORUS.structure.shape,
        syncFrequency: `${EARTH_TORUS.syncFrequencies.atomAnchor} Hz`,
        principle: EARTH_TORUS.heartMirror.principle
      },
      
      // Message final
      message: `L'Arche AT·OM est synchronisée avec le réseau planétaire. ${planetaryEnergy.message}`
    };
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// INSTANCE PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export const globalSync = new WorldSyncEngine();

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Aligne un utilisateur sur le réseau planétaire
 */
export function alignWithEarth(latitude, longitude, heartRate = 60) {
  return globalSync.alignUser(latitude, longitude, heartRate);
}

/**
 * Obtient l'énergie planétaire actuelle
 */
export function getCurrentPlanetaryEnergy() {
  return globalSync.getPlanetaryEnergy();
}

/**
 * Génère un rapport de synchronisation global
 */
export function getGlobalSyncReport() {
  return globalSync.generateGlobalReport();
}

/**
 * Trouve le site le plus proche
 */
export function findNearestSacredSite(latitude, longitude) {
  return globalSync.findNearestNode(latitude, longitude);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Constantes
  EARTH_CONSTANTS,
  SACRED_SITES,
  LEY_LINES,
  EARTH_TORUS,
  
  // Classe
  WorldSyncEngine,
  
  // Instance
  globalSync,
  
  // Fonctions
  alignWithEarth,
  getCurrentPlanetaryEnergy,
  getGlobalSyncReport,
  findNearestSacredSite
};
