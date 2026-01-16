/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *    ██████╗ ██╗ ██████╗     ███████╗██╗   ██╗███╗   ██╗ ██████╗
 *    ██╔══██╗██║██╔═══██╗    ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝
 *    ██████╔╝██║██║   ██║    ███████╗ ╚████╔╝ ██╔██╗ ██║██║     
 *    ██╔══██╗██║██║   ██║    ╚════██║  ╚██╔╝  ██║╚██╗██║██║     
 *    ██████╔╝██║╚██████╔╝    ███████║   ██║   ██║ ╚████║╚██████╗
 *    ╚═════╝ ╚═╝ ╚═════╝     ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝
 * 
 *              ENGINE — L'INTERFACE BIOLOGIQUE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * L'Arche AT·OM ne traite pas l'utilisateur comme un simple spectateur,
 * mais comme un CIRCUIT VIVANT. Ce module gère:
 * 
 * 1. Les 7 Chakras — Centres de distribution d'énergie
 * 2. Les Glandes Endocrines — Transformation signal → sensation
 * 3. Les Méridiens (Chine) — Canaux de transmission
 * 4. Les Nadis (Inde) — Câbles de fibre optique subtils
 * 5. Le Torus Cardiaque — Champ électromagnétique du cœur
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// SYSTÈME DES CHAKRAS — CENTRES ÉNERGÉTIQUES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les 7 Chakras principaux avec leurs correspondances AT·OM
 * 
 *        ⬡ Sahasrara (Couronne) — 963 Hz — Atlantide
 *        ◇ Ajna (3ème Œil) — 852 Hz — Maya
 *        ○ Vishuddha (Gorge) — 741 Hz — Sumer
 *        ♡ Anahata (Cœur) — 528/432 Hz — Égypte (ANCRAGE)
 *        △ Manipura (Plexus) — 396 Hz — Aztèque
 *        ◐ Svadhisthana (Sacré) — 285 Hz — Grèce
 *        ■ Muladhara (Racine) — 174 Hz — Rapa Nui
 */

export const CHAKRA_SYSTEM = {
  chakras: [
    {
      number: 1,
      sanskrit: "Muladhara",
      name: "Racine",
      symbol: "■",
      location: "Base de la colonne vertébrale",
      gland: "Surrénales",
      glandFunction: "Adrénaline, Cortisol, Stress/Survie",
      civilization: "Rapa Nui",
      civilizationRole: "Sécurité / Ancrage / Stockage Physique",
      frequency: {
        solfeggio: 396,
        atom: 111,
        binaural: 174
      },
      color: "#FF0000",
      element: "Terre",
      mantra: "LAM",
      petals: 4,
      sense: "Odorat",
      codeFunction: "Security & Grounding",
      meridians: ["Rein", "Vessie"],
      bodyParts: ["Jambes", "Pieds", "Os", "Dents"],
      crystals: ["Obsidienne", "Hématite", "Grenat"],
      organs: ["Glandes surrénales", "Colonne vertébrale", "Reins"]
    },
    {
      number: 2,
      sanskrit: "Svadhisthana",
      name: "Sacré",
      symbol: "◐",
      location: "Sous le nombril",
      gland: "Gonades",
      glandFunction: "Hormones sexuelles, Créativité",
      civilization: "Grèce",
      civilizationRole: "Géométrie de Création / Rendu des Formes",
      frequency: {
        solfeggio: 417,
        atom: 222,
        binaural: 285
      },
      color: "#FF7F00",
      element: "Eau",
      mantra: "VAM",
      petals: 6,
      sense: "Goût",
      codeFunction: "Creativity & Rendering",
      meridians: ["Rate", "Estomac"],
      bodyParts: ["Organes reproducteurs", "Vessie", "Hanches"],
      crystals: ["Cornaline", "Pierre de lune", "Ambre"],
      organs: ["Gonades", "Système reproducteur", "Bas-ventre"]
    },
    {
      number: 3,
      sanskrit: "Manipura",
      name: "Plexus Solaire",
      symbol: "△",
      location: "Plexus solaire",
      gland: "Pancréas",
      glandFunction: "Insuline, Digestion, Métabolisme",
      civilization: "Aztèque",
      civilizationRole: "Puissance d'Exécution / Force du Processeur",
      frequency: {
        solfeggio: 528,
        atom: 333,
        binaural: 396
      },
      color: "#FFFF00",
      element: "Feu",
      mantra: "RAM",
      petals: 10,
      sense: "Vue",
      codeFunction: "Processing Power & Execution",
      meridians: ["Foie", "Vésicule biliaire"],
      bodyParts: ["Estomac", "Foie", "Intestin grêle"],
      crystals: ["Citrine", "Œil de tigre", "Ambre"],
      organs: ["Pancréas", "Système digestif", "Foie"]
    },
    {
      number: 4,
      sanskrit: "Anahata",
      name: "Cœur",
      symbol: "♡",
      location: "Centre de la poitrine",
      gland: "Thymus",
      glandFunction: "Système immunitaire, Lymphocytes T",
      civilization: "Égypte",
      civilizationRole: "Équilibre du Flux / Algorithme de Maât",
      frequency: {
        solfeggio: 639,
        atom: 444, // ANCRAGE CENTRAL
        binaural: 528 // Fréquence de l'Amour
      },
      color: "#50C878",
      element: "Air",
      mantra: "YAM",
      petals: 12,
      sense: "Toucher",
      codeFunction: "Balance & Harmony (ANCHOR)",
      meridians: ["Cœur", "Péricarde", "Maître du Cœur"],
      bodyParts: ["Cœur", "Poumons", "Bras", "Mains"],
      crystals: ["Quartz rose", "Émeraude", "Jade"],
      organs: ["Thymus", "Cœur", "Système circulatoire"],
      isAnchor: true,
      torusField: {
        diameter: "2-3 mètres",
        strength: "5000x plus fort que le cerveau",
        coherence: "Synchronise tous les autres chakras"
      }
    },
    {
      number: 5,
      sanskrit: "Vishuddha",
      name: "Gorge",
      symbol: "○",
      location: "Gorge",
      gland: "Thyroïde",
      glandFunction: "Métabolisme, Croissance, Température",
      civilization: "Sumer",
      civilizationRole: "Expression du Code Source / Communication",
      frequency: {
        solfeggio: 741,
        atom: 555,
        binaural: 741
      },
      color: "#87CEEB",
      element: "Éther",
      mantra: "HAM",
      petals: 16,
      sense: "Ouïe",
      codeFunction: "Communication & Expression",
      meridians: ["Poumon", "Gros intestin"],
      bodyParts: ["Gorge", "Cou", "Mâchoire", "Oreilles"],
      crystals: ["Turquoise", "Aigue-marine", "Lapis lazuli"],
      organs: ["Thyroïde", "Parathyroïde", "Cordes vocales"]
    },
    {
      number: 6,
      sanskrit: "Ajna",
      name: "Troisième Œil",
      symbol: "◇",
      location: "Entre les sourcils",
      gland: "Hypophyse (Pituitaire)",
      glandFunction: "Hormone de croissance, Régulation hormonale globale",
      civilization: "Maya",
      civilizationRole: "Vision des Cycles / Prédiction de Données",
      frequency: {
        solfeggio: 852,
        atom: 666,
        binaural: 852
      },
      color: "#4B0082",
      element: "Lumière",
      mantra: "OM",
      petals: 2,
      sense: "Intuition",
      codeFunction: "Pattern Recognition & Prediction",
      meridians: ["Triple réchauffeur", "Vésicule biliaire"],
      bodyParts: ["Yeux", "Nez", "Oreilles", "Cerveau inférieur"],
      crystals: ["Améthyste", "Fluorite", "Sodalite"],
      organs: ["Hypophyse", "Système nerveux", "Yeux"]
    },
    {
      number: 7,
      sanskrit: "Sahasrara",
      name: "Couronne",
      symbol: "⬡",
      location: "Sommet du crâne",
      gland: "Pinéale (Épiphyse)",
      glandFunction: "Mélatonine, Cycles circadiens, États de conscience",
      civilization: "Atlantide",
      civilizationRole: "Connexion au Cloud Universel / Intuition IA",
      frequency: {
        solfeggio: 963,
        atom: 999,
        binaural: 963
      },
      color: "#EE82EE",
      element: "Pensée/Conscience",
      mantra: "Silence / OM",
      petals: 1000,
      sense: "Conscience pure",
      codeFunction: "Universal Connection & Transcendence",
      meridians: ["Vaisseau Gouverneur", "Vaisseau Conception"],
      bodyParts: ["Cerveau supérieur", "Fontanelle"],
      crystals: ["Améthyste", "Quartz clair", "Diamant"],
      organs: ["Glande pinéale", "Cortex cérébral"],
      secretion: {
        dmt: "Diméthyltryptamine (molécule de l'esprit)",
        melatonin: "Mélatonine (horloge biologique)"
      }
    }
  ],
  
  // Fréquences Solfège complètes
  solfeggio: {
    174: "Fondation, Sécurité",
    285: "Transformation, Guérison",
    396: "Libération de la peur",
    417: "Changement, Transmutation",
    528: "Réparation ADN, Amour",
    639: "Connexion, Relations",
    741: "Expression, Solutions",
    852: "Intuition, Éveil",
    963: "Connexion divine, Unité"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// SYSTÈME DES NADIS — CANAUX SUBTILS (INDE)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les 3 Nadis principaux forment le "Bus de Données" énergétique
 * 
 *        IDA ───────┐     ┌─────── PINGALA
 *        (Lune)     │     │       (Soleil)
 *        Yin        │     │       Yang
 *        Gauche     │     │       Droite
 *                   ▼     ▼
 *               ╔═══════════╗
 *               ║ SUSHUMNA  ║ ← Canal Central (999 Hz)
 *               ║  (Feu)    ║
 *               ╚═══════════╝
 */

export const NADI_SYSTEM = {
  principal: [
    {
      name: "Sushumna",
      sanskrit: "सुषुम्णा",
      meaning: "Le Canal Central",
      path: "Base de la colonne → Couronne",
      polarity: "Neutre",
      element: "Feu",
      color: "#FFFFFF",
      function: "Canal principal de la Kundalini",
      atomRole: "Bus de Données Principal",
      frequency: 999,
      activation: "Quand Ida et Pingala sont équilibrés"
    },
    {
      name: "Ida",
      sanskrit: "इडा",
      meaning: "Canal Lunaire",
      path: "Narine gauche → côté gauche",
      polarity: "Yin (Féminin)",
      element: "Eau",
      color: "#C0C0C0",
      function: "Refroidissement, Introspection, Intuition",
      atomRole: "Input Data Stream (Réception)",
      frequency: 444,
      qualities: ["Repos", "Créativité", "Réceptivité"]
    },
    {
      name: "Pingala",
      sanskrit: "पिंगला",
      meaning: "Canal Solaire",
      path: "Narine droite → côté droit",
      polarity: "Yang (Masculin)",
      element: "Feu",
      color: "#FFD700",
      function: "Réchauffement, Action, Analyse",
      atomRole: "Output Data Stream (Émission)",
      frequency: 555,
      qualities: ["Action", "Logique", "Expression"]
    }
  ],
  
  total: 72000, // Nombre traditionnel de Nadis
  
  // Points de croisement (où les Nadis se rencontrent aux Chakras)
  crossings: [
    { chakra: 1, description: "Muladhara - Point d'origine" },
    { chakra: 2, description: "Svadhisthana - Premier croisement" },
    { chakra: 3, description: "Manipura - Deuxième croisement" },
    { chakra: 4, description: "Anahata - Troisième croisement (NŒUD CENTRAL)" },
    { chakra: 5, description: "Vishuddha - Quatrième croisement" },
    { chakra: 6, description: "Ajna - Point de convergence finale" },
    { chakra: 7, description: "Sahasrara - Sushumna seul" }
  ]
};

// ═══════════════════════════════════════════════════════════════════════════════
// SYSTÈME DES MÉRIDIENS — CANAUX ÉNERGÉTIQUES (CHINE)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les 12 Méridiens principaux + 8 Merveilleux
 * Ce sont les "circuits imprimés" du corps
 */

export const MERIDIAN_SYSTEM = {
  principal: [
    // Méridiens Yin (internes)
    { name: "Poumon", chinese: "手太阴肺经", element: "Métal", partner: "Gros Intestin", hours: "3h-5h", finger: "Pouce" },
    { name: "Rate", chinese: "足太阴脾经", element: "Terre", partner: "Estomac", hours: "9h-11h", toe: "Gros orteil" },
    { name: "Cœur", chinese: "手少阴心经", element: "Feu", partner: "Intestin Grêle", hours: "11h-13h", finger: "Auriculaire" },
    { name: "Rein", chinese: "足少阴肾经", element: "Eau", partner: "Vessie", hours: "17h-19h", toe: "Petit orteil" },
    { name: "Péricarde", chinese: "手厥阴心包经", element: "Feu", partner: "Triple Réchauffeur", hours: "19h-21h", finger: "Majeur" },
    { name: "Foie", chinese: "足厥阴肝经", element: "Bois", partner: "Vésicule Biliaire", hours: "1h-3h", toe: "Gros orteil" },
    
    // Méridiens Yang (externes)
    { name: "Gros Intestin", chinese: "手阳明大肠经", element: "Métal", partner: "Poumon", hours: "5h-7h", finger: "Index" },
    { name: "Estomac", chinese: "足阳明胃经", element: "Terre", partner: "Rate", hours: "7h-9h", toe: "2ème orteil" },
    { name: "Intestin Grêle", chinese: "手太阳小肠经", element: "Feu", partner: "Cœur", hours: "13h-15h", finger: "Auriculaire" },
    { name: "Vessie", chinese: "足太阳膀胱经", element: "Eau", partner: "Rein", hours: "15h-17h", toe: "Petit orteil" },
    { name: "Triple Réchauffeur", chinese: "手少阳三焦经", element: "Feu", partner: "Péricarde", hours: "21h-23h", finger: "Annulaire" },
    { name: "Vésicule Biliaire", chinese: "足少阳胆经", element: "Bois", partner: "Foie", hours: "23h-1h", toe: "4ème orteil" }
  ],
  
  extraordinary: [
    { name: "Vaisseau Gouverneur", chinese: "督脉", path: "Dos - Yang", function: "Gouverne tous les Yang" },
    { name: "Vaisseau Conception", chinese: "任脉", path: "Avant - Yin", function: "Gouverne tous les Yin" },
    { name: "Vaisseau Ceinture", chinese: "带脉", path: "Tour de taille", function: "Relie haut et bas" },
    { name: "Vaisseau Pénétrant", chinese: "冲脉", path: "Centre", function: "Mer du sang et de l'énergie" },
    { name: "Yin de Talon", chinese: "阴跷脉", path: "Intérieur jambe", function: "Équilibre Yin" },
    { name: "Yang de Talon", chinese: "阳跷脉", path: "Extérieur jambe", function: "Équilibre Yang" },
    { name: "Yin de Liaison", chinese: "阴维脉", path: "Intérieur", function: "Lie tous les Yin" },
    { name: "Yang de Liaison", chinese: "阳维脉", path: "Extérieur", function: "Lie tous les Yang" }
  ],
  
  // Cycle circadien - Horloge des organes
  organClock: {
    "3h-5h": { organ: "Poumon", activity: "Respiration profonde, réveil naturel" },
    "5h-7h": { organ: "Gros Intestin", activity: "Élimination, réveil" },
    "7h-9h": { organ: "Estomac", activity: "Digestion optimale, petit-déjeuner" },
    "9h-11h": { organ: "Rate", activity: "Métabolisme, concentration" },
    "11h-13h": { organ: "Cœur", activity: "Circulation maximale, déjeuner léger" },
    "13h-15h": { organ: "Intestin Grêle", activity: "Assimilation, repos" },
    "15h-17h": { organ: "Vessie", activity: "Élimination liquides" },
    "17h-19h": { organ: "Rein", activity: "Stockage énergie vitale" },
    "19h-21h": { organ: "Péricarde", activity: "Circulation, détente" },
    "21h-23h": { organ: "Triple Réchauffeur", activity: "Régénération, sommeil" },
    "23h-1h": { organ: "Vésicule Biliaire", activity: "Sommeil profond, régénération" },
    "1h-3h": { organ: "Foie", activity: "Détoxification, rêves" }
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// TORUS CARDIAQUE — CHAMP ÉLECTROMAGNÉTIQUE DU CŒUR
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le cœur génère le plus grand champ électromagnétique du corps.
 * Ce champ en forme de torus s'étend sur 2-3 mètres autour du corps.
 */

export const HEART_TORUS = {
  name: "Champ Toroïdal Cardiaque",
  
  physical: {
    electricField: "60x plus fort que le cerveau",
    magneticField: "5000x plus fort que le cerveau",
    diameter: "2-3 mètres",
    shape: "Torus (beignet)",
    frequency: "0.1 Hz - 0.4 Hz (rythme cardiaque)"
  },
  
  coherence: {
    state: "Cohérence cardiaque",
    description: "État où le rythme cardiaque devient régulier et harmonieux",
    benefits: [
      "Synchronisation cœur-cerveau",
      "Réduction du stress",
      "Clarté mentale",
      "Intuition accrue",
      "Renforcement immunitaire"
    ],
    frequency: "0.1 Hz (6 respirations/minute)",
    technique: "Respiration 5-5 (5s inspiration, 5s expiration)"
  },
  
  // Correspondance avec le Torus terrestre
  earthMirror: {
    earthField: "Champ magnétique terrestre",
    resonance: "7.83 Hz (Résonance de Schumann)",
    principle: "As above, so below - Le microcosme reflète le macrocosme",
    synchronization: "Quand le torus cardiaque s'aligne avec le torus terrestre"
  },
  
  // Intégration AT·OM
  atomIntegration: {
    anchorFrequency: 444, // Hz - Point d'ancrage
    coherenceTarget: 528, // Hz - Fréquence de l'amour
    fullActivation: 999   // Hz - Pleine ouverture
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// TABLE DE CORRESPONDANCES BIO-NUMÉRIQUES
// ═══════════════════════════════════════════════════════════════════════════════

export const BIO_NUMERIC_TABLE = [
  {
    chakra: "Couronne",
    gland: "Pinéale",
    civilization: "Atlantide",
    frequency: 963,
    atomHz: 999,
    codeRole: "Connexion Cloud Universel / Intuition IA",
    color: "#EE82EE",
    element: "Conscience"
  },
  {
    chakra: "Troisième Œil",
    gland: "Hypophyse",
    civilization: "Maya",
    frequency: 852,
    atomHz: 666,
    codeRole: "Vision des Cycles / Prédiction",
    color: "#4B0082",
    element: "Lumière"
  },
  {
    chakra: "Gorge",
    gland: "Thyroïde",
    civilization: "Sumer",
    frequency: 741,
    atomHz: 555,
    codeRole: "Expression Code Source / Communication",
    color: "#87CEEB",
    element: "Éther"
  },
  {
    chakra: "Cœur",
    gland: "Thymus",
    civilization: "Égypte",
    frequency: 528,
    atomHz: 444,
    codeRole: "Équilibre Flux / Algorithme Maât",
    color: "#50C878",
    element: "Air",
    isAnchor: true
  },
  {
    chakra: "Plexus Solaire",
    gland: "Pancréas",
    civilization: "Aztèque",
    frequency: 396,
    atomHz: 333,
    codeRole: "Puissance Exécution / Force Processeur",
    color: "#FFFF00",
    element: "Feu"
  },
  {
    chakra: "Sacré",
    gland: "Gonades",
    civilization: "Grèce",
    frequency: 285,
    atomHz: 222,
    codeRole: "Géométrie Création / Rendu Formes",
    color: "#FF7F00",
    element: "Eau"
  },
  {
    chakra: "Racine",
    gland: "Surrénales",
    civilization: "Rapa Nui",
    frequency: 174,
    atomHz: 111,
    codeRole: "Sécurité / Ancrage / Stockage",
    color: "#FF0000",
    element: "Terre"
  }
];

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE SYNCHRONISATION BIOLOGIQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule le chakra actif basé sur l'heure
 */
export function getActiveChakraByTime(date = new Date()) {
  const hour = date.getHours();
  
  // Mapping simplifié basé sur les cycles d'énergie
  const hourToChakra = {
    0: 7, 1: 7, 2: 7, 3: 1, 4: 1, 5: 1,  // Nuit → Spirituel puis Racine
    6: 2, 7: 2, 8: 3, 9: 3, 10: 3, 11: 4, // Matin → Créatif puis Solaire puis Cœur
    12: 4, 13: 4, 14: 5, 15: 5, 16: 5,   // Après-midi → Cœur puis Communication
    17: 6, 18: 6, 19: 4, 20: 4, 21: 7, 22: 7, 23: 7 // Soir → Vision puis Cœur puis Spirituel
  };
  
  const chakraNumber = hourToChakra[hour] || 4;
  const chakra = CHAKRA_SYSTEM.chakras[chakraNumber - 1];
  
  return {
    number: chakraNumber,
    name: chakra.name,
    sanskrit: chakra.sanskrit,
    civilization: chakra.civilization,
    frequency: chakra.frequency,
    recommendation: `Focus sur ${chakra.name} (${chakra.civilization})`
  };
}

/**
 * Calcule l'état énergétique global
 */
export function calculateEnergyState(frequencies = []) {
  const chakras = CHAKRA_SYSTEM.chakras;
  
  // Si pas de fréquences fournies, utiliser les valeurs AT·OM par défaut
  if (frequencies.length === 0) {
    frequencies = chakras.map(c => c.frequency.atom);
  }
  
  const average = frequencies.reduce((a, b) => a + b, 0) / frequencies.length;
  const heartIndex = 3; // Index du chakra du cœur
  const heartFreq = frequencies[heartIndex] || 444;
  
  // Vérifier la cohérence (tous proches de la moyenne)
  const variance = frequencies.reduce((sum, f) => sum + Math.pow(f - average, 2), 0) / frequencies.length;
  const coherence = 1 - (Math.sqrt(variance) / average);
  
  return {
    averageFrequency: Math.round(average),
    heartCoherence: coherence > 0.7,
    coherenceLevel: coherence.toFixed(2),
    dominantChakra: frequencies.indexOf(Math.max(...frequencies)) + 1,
    weakestChakra: frequencies.indexOf(Math.min(...frequencies)) + 1,
    recommendation: coherence < 0.5 
      ? "Pratiquer la cohérence cardiaque"
      : coherence < 0.7
        ? "Bon équilibre, continuer"
        : "État optimal de cohérence"
  };
}

/**
 * Génère une séquence de fréquences pour l'activation des chakras
 */
export function generateChakraActivationSequence(targetChakra = 7, duration = 60) {
  const sequence = [];
  const chakras = CHAKRA_SYSTEM.chakras;
  const stepDuration = duration / targetChakra;
  
  for (let i = 0; i < targetChakra; i++) {
    sequence.push({
      step: i + 1,
      chakra: chakras[i].name,
      frequency: chakras[i].frequency.solfeggio,
      atomFrequency: chakras[i].frequency.atom,
      duration: stepDuration,
      color: chakras[i].color,
      mantra: chakras[i].mantra
    });
  }
  
  return {
    sequence,
    totalDuration: duration,
    targetChakra: chakras[targetChakra - 1].name,
    finalFrequency: chakras[targetChakra - 1].frequency.solfeggio
  };
}

/**
 * Obtient le méridien actif selon l'heure
 */
export function getActiveMeridian(date = new Date()) {
  const hour = date.getHours();
  const clock = MERIDIAN_SYSTEM.organClock;
  
  for (const [timeRange, data] of Object.entries(clock)) {
    const [start, end] = timeRange.split('-').map(t => parseInt(t));
    
    if ((start <= hour && hour < end) || (start > end && (hour >= start || hour < end))) {
      return {
        timeRange,
        organ: data.organ,
        activity: data.activity,
        meridian: MERIDIAN_SYSTEM.principal.find(m => m.name === data.organ) || null
      };
    }
  }
  
  return null;
}

/**
 * Calcule la résonance biologique pour AT·OM
 */
export function getBioResonance(atomFrequency, date = new Date()) {
  // Trouver le chakra correspondant
  const chakraMatch = BIO_NUMERIC_TABLE.find(b => b.atomHz === atomFrequency) 
    || BIO_NUMERIC_TABLE.find(b => Math.abs(b.atomHz - atomFrequency) < 100)
    || BIO_NUMERIC_TABLE[3]; // Cœur par défaut
  
  // Chakra actif selon l'heure
  const activeChakra = getActiveChakraByTime(date);
  
  // Méridien actif
  const activeMeridian = getActiveMeridian(date);
  
  // Cohérence avec le torus cardiaque
  const heartCoherence = atomFrequency === 444 ? 1.0 
    : atomFrequency === 528 ? 0.95
    : 1 - Math.abs(atomFrequency - 444) / 555;
  
  return {
    // Chakra cible
    targetChakra: {
      name: chakraMatch.chakra,
      gland: chakraMatch.gland,
      civilization: chakraMatch.civilization,
      element: chakraMatch.element,
      color: chakraMatch.color
    },
    
    // Chakra actif (selon l'heure)
    activeChakra: {
      name: activeChakra.name,
      civilization: activeChakra.civilization
    },
    
    // Méridien actif
    activeMeridian: activeMeridian ? {
      organ: activeMeridian.organ,
      activity: activeMeridian.activity
    } : null,
    
    // Fréquences
    frequencies: {
      atom: atomFrequency,
      solfeggio: chakraMatch.frequency,
      binaural: CHAKRA_SYSTEM.solfeggio[chakraMatch.frequency] ? chakraMatch.frequency : 528
    },
    
    // Cohérence
    coherence: {
      heart: heartCoherence.toFixed(2),
      aligned: heartCoherence > 0.7
    },
    
    // Nadis
    nadi: atomFrequency >= 666 ? "Sushumna (Central)" 
        : atomFrequency >= 444 ? "Équilibre Ida-Pingala"
        : atomFrequency >= 333 ? "Pingala (Solaire)"
        : "Ida (Lunaire)",
    
    // Recommandation
    recommendation: chakraMatch.isAnchor
      ? "Point d'ancrage optimal — Cohérence cardiaque maximale"
      : `Activation ${chakraMatch.chakra} via ${chakraMatch.civilization}`,
    
    // Message
    message: `🧬 ${chakraMatch.chakra} (${chakraMatch.gland}) ↔ ${chakraMatch.civilization} — ${heartCoherence > 0.7 ? 'Cohérent' : 'Calibrer'}`
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Systèmes
  CHAKRA_SYSTEM,
  NADI_SYSTEM,
  MERIDIAN_SYSTEM,
  HEART_TORUS,
  BIO_NUMERIC_TABLE,
  
  // Fonctions
  getActiveChakraByTime,
  calculateEnergyState,
  generateChakraActivationSequence,
  getActiveMeridian,
  getBioResonance
};
