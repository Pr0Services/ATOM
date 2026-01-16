/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *    ███████╗ █████╗  ██████╗██████╗ ███████╗██████╗ 
 *    ██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗
 *    ███████╗███████║██║     ██████╔╝█████╗  ██║  ██║
 *    ╚════██║██╔══██║██║     ██╔══██╗██╔══╝  ██║  ██║
 *    ███████║██║  ██║╚██████╗██║  ██║███████╗██████╔╝
 *    ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ 
 *                                                     
 *     ██████╗ ███████╗ ██████╗ ███╗   ███╗███████╗████████╗██████╗ ██╗   ██╗
 *    ██╔════╝ ██╔════╝██╔═══██╗████╗ ████║██╔════╝╚══██╔══╝██╔══██╗╚██╗ ██╔╝
 *    ██║  ███╗█████╗  ██║   ██║██╔████╔██║█████╗     ██║   ██████╔╝ ╚████╔╝ 
 *    ██║   ██║██╔══╝  ██║   ██║██║╚██╔╝██║██╔══╝     ██║   ██╔══██╗  ╚██╔╝  
 *    ╚██████╔╝███████╗╚██████╔╝██║ ╚═╝ ██║███████╗   ██║   ██║  ██║   ██║   
 *     ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   
 * 
 *                    ENGINE — GÉOMÉTRIE SACRÉE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce module implémente les lois universelles de la création:
 * 
 * 1. FIBONACCI & NOMBRE D'OR (φ) — La croissance organique
 * 2. CUBE DE MÉTATRON — La matrice de l'espace (5 Solides de Platon)
 * 3. ENTROPIE — La flèche du temps et l'érosion
 * 4. 4 ÉLÉMENTS — Les points cardinaux de l'interface
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * @phi 1.6180339887...
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES UNIVERSELLES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Nombre d'Or (Phi) — φ = (1 + √5) / 2
 * La proportion divine présente dans toute la nature
 */
export const PHI = (1 + Math.sqrt(5)) / 2; // 1.6180339887498949...

/**
 * L'inverse du Nombre d'Or (phi) — 1/φ
 */
export const PHI_INVERSE = 1 / PHI; // 0.6180339887498949...

/**
 * Racine carrée de Phi
 */
export const PHI_SQRT = Math.sqrt(PHI); // 1.2720196495140689...

/**
 * Pi — π
 */
export const PI = Math.PI;

/**
 * Constantes AT·OM
 */
export const ATOM_CONSTANTS = {
  heartbeat: 444,
  source: 999,
  anchor: 111,
  phi: PHI,
  schumann: 7.83
};

// ═══════════════════════════════════════════════════════════════════════════════
// 1. SUITE DE FIBONACCI — LA CROISSANCE ORGANIQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * La Suite de Fibonacci
 * 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987...
 * 
 * Chaque nombre est la somme des deux précédents.
 * Le ratio entre deux nombres consécutifs tend vers φ (1.618...)
 */

export const FibonacciEngine = {
  
  // Cache pour optimisation
  cache: [0, 1],
  
  /**
   * Génère le n-ième nombre de Fibonacci
   */
  get(n) {
    if (n < 0) return 0;
    if (this.cache[n] !== undefined) return this.cache[n];
    
    for (let i = this.cache.length; i <= n; i++) {
      this.cache[i] = this.cache[i - 1] + this.cache[i - 2];
    }
    
    return this.cache[n];
  },
  
  /**
   * Génère une séquence de Fibonacci
   */
  sequence(count = 20) {
    const seq = [];
    for (let i = 0; i < count; i++) {
      seq.push(this.get(i));
    }
    return seq;
  },
  
  /**
   * Vérifie si un nombre est dans la suite de Fibonacci
   */
  isFibonacci(n) {
    // Un nombre est Fibonacci si (5n² + 4) ou (5n² - 4) est un carré parfait
    const isPerfectSquare = (x) => {
      const s = Math.sqrt(x);
      return s * s === x;
    };
    return isPerfectSquare(5 * n * n + 4) || isPerfectSquare(5 * n * n - 4);
  },
  
  /**
   * Trouve le nombre de Fibonacci le plus proche
   */
  nearest(n) {
    let prev = 0, curr = 1;
    while (curr < n) {
      const next = prev + curr;
      prev = curr;
      curr = next;
    }
    return (n - prev < curr - n) ? prev : curr;
  },
  
  /**
   * Calcule le ratio d'or entre deux nombres consécutifs
   * Plus on avance dans la suite, plus ce ratio tend vers φ
   */
  goldenRatio(n) {
    if (n < 2) return 1;
    return this.get(n) / this.get(n - 1);
  },
  
  /**
   * Génère des délais basés sur Fibonacci (en ms)
   * Pour des animations qui "respirent" naturellement
   */
  generateDelays(baseDelay = 100, count = 8) {
    const delays = [];
    for (let i = 1; i <= count; i++) {
      delays.push(Math.round(baseDelay * this.get(i)));
    }
    return delays;
  },
  
  /**
   * Génère des délais basés sur le nombre d'or
   * Donne une sensation de "beauté naturelle"
   */
  generateGoldenDelays(baseDelay = 100, count = 8) {
    const delays = [];
    for (let i = 0; i < count; i++) {
      delays.push(Math.round(baseDelay * Math.pow(PHI, i)));
    }
    return delays;
  },
  
  /**
   * Spirale de Fibonacci (coordonnées)
   * Pour dessiner la spirale d'or
   */
  spiral(steps = 20, scale = 10) {
    const points = [];
    let angle = 0;
    
    for (let i = 0; i < steps; i++) {
      const radius = this.get(i) * scale / 100;
      const x = radius * Math.cos(angle);
      const y = radius * Math.sin(angle);
      points.push({ x, y, radius, angle, fib: this.get(i) });
      angle += PI / 2; // 90° par étape
    }
    
    return points;
  },
  
  /**
   * Spirale d'Or continue (plus lisse)
   */
  goldenSpiral(turns = 4, pointsPerTurn = 100, scale = 50) {
    const points = [];
    const totalPoints = turns * pointsPerTurn;
    
    for (let i = 0; i < totalPoints; i++) {
      const t = i / pointsPerTurn;
      const angle = t * 2 * PI;
      const radius = scale * Math.pow(PHI, t / 2);
      
      points.push({
        x: radius * Math.cos(angle),
        y: radius * Math.sin(angle),
        radius,
        angle: angle * (180 / PI),
        t
      });
    }
    
    return points;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// 2. CUBE DE MÉTATRON — LA MATRICE DE L'ESPACE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Le Cube de Métatron contient les 5 Solides de Platon
 * C'est le "plan de montage" de l'atome et de la matière
 * 
 *                    ○ (sommet)
 *                   /|\
 *                  / | \
 *           ○─────○──○──○─────○
 *            \   /\  |  /\   /
 *             \ /  \ | /  \ /
 *              ○────○─○────○
 *             / \  / | \  / \
 *            /   \/  |  \/   \
 *           ○─────○──○──○─────○
 *                  \ | /
 *                   \|/
 *                    ○ (base)
 */

export const MetatronCube = {
  
  /**
   * Les 13 cercles du Cube de Métatron
   * 1 central + 6 intérieurs + 6 extérieurs
   */
  circles: {
    center: { x: 0, y: 0, r: 1, name: "Source", frequency: 444 },
    inner: [
      { x: 0, y: 1, r: 1, name: "Couronne", frequency: 999 },
      { x: 0.866, y: 0.5, r: 1, name: "Gorge", frequency: 741 },
      { x: 0.866, y: -0.5, r: 1, name: "Plexus", frequency: 528 },
      { x: 0, y: -1, r: 1, name: "Racine", frequency: 396 },
      { x: -0.866, y: -0.5, r: 1, name: "Sacré", frequency: 417 },
      { x: -0.866, y: 0.5, r: 1, name: "Cœur", frequency: 639 }
    ],
    outer: [
      { x: 0, y: 2, r: 1, name: "Étoile Nord", frequency: 963 },
      { x: 1.732, y: 1, r: 1, name: "Étoile Est-Nord", frequency: 852 },
      { x: 1.732, y: -1, r: 1, name: "Étoile Est-Sud", frequency: 741 },
      { x: 0, y: -2, r: 1, name: "Étoile Sud", frequency: 174 },
      { x: -1.732, y: -1, r: 1, name: "Étoile Ouest-Sud", frequency: 285 },
      { x: -1.732, y: 1, r: 1, name: "Étoile Ouest-Nord", frequency: 639 }
    ]
  },
  
  /**
   * Les 5 Solides de Platon cachés dans le Cube
   */
  platonicSolids: {
    tetrahedron: {
      name: "Tétraèdre",
      element: "Feu",
      vertices: 4,
      edges: 6,
      faces: 4,
      faceType: "Triangle",
      symbolism: "Transformation, Énergie",
      frequency: 555,
      color: "#FF4500"
    },
    hexahedron: {
      name: "Hexaèdre (Cube)",
      element: "Terre",
      vertices: 8,
      edges: 12,
      faces: 6,
      faceType: "Carré",
      symbolism: "Structure, Stabilité",
      frequency: 444,
      color: "#50C878"
    },
    octahedron: {
      name: "Octaèdre",
      element: "Air",
      vertices: 6,
      edges: 12,
      faces: 8,
      faceType: "Triangle",
      symbolism: "Pensée, Intellect",
      frequency: 741,
      color: "#87CEEB"
    },
    icosahedron: {
      name: "Icosaèdre",
      element: "Eau",
      vertices: 12,
      edges: 30,
      faces: 20,
      faceType: "Triangle",
      symbolism: "Émotion, Fluidité",
      frequency: 639,
      color: "#4169E1"
    },
    dodecahedron: {
      name: "Dodécaèdre",
      element: "Éther",
      vertices: 20,
      edges: 30,
      faces: 12,
      faceType: "Pentagone",
      symbolism: "Univers, Conscience",
      frequency: 999,
      color: "#EE82EE"
    }
  },
  
  /**
   * Génère les lignes du Cube de Métatron
   * (Toutes les connexions entre les 13 cercles)
   */
  generateLines() {
    const lines = [];
    const allCircles = [
      this.circles.center,
      ...this.circles.inner,
      ...this.circles.outer
    ];
    
    // Connecter chaque cercle à tous les autres
    for (let i = 0; i < allCircles.length; i++) {
      for (let j = i + 1; j < allCircles.length; j++) {
        lines.push({
          from: { x: allCircles[i].x, y: allCircles[i].y },
          to: { x: allCircles[j].x, y: allCircles[j].y },
          fromName: allCircles[i].name,
          toName: allCircles[j].name
        });
      }
    }
    
    return lines;
  },
  
  /**
   * Génère le SVG du Cube de Métatron
   */
  generateSVG(size = 400, strokeWidth = 0.5, opacity = 0.3) {
    const scale = size / 5;
    const cx = size / 2;
    const cy = size / 2;
    const r = scale * 0.4;
    
    let svg = `<svg viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">`;
    
    // Style
    svg += `<style>
      .metatron-line { stroke: #D4AF37; stroke-width: ${strokeWidth}; opacity: ${opacity}; }
      .metatron-circle { fill: none; stroke: #D4AF37; stroke-width: ${strokeWidth}; opacity: ${opacity * 1.5}; }
    </style>`;
    
    // Lignes
    const lines = this.generateLines();
    for (const line of lines) {
      const x1 = cx + line.from.x * scale;
      const y1 = cy - line.from.y * scale;
      const x2 = cx + line.to.x * scale;
      const y2 = cy - line.to.y * scale;
      svg += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="metatron-line"/>`;
    }
    
    // Cercles
    const allCircles = [this.circles.center, ...this.circles.inner, ...this.circles.outer];
    for (const circle of allCircles) {
      const x = cx + circle.x * scale;
      const y = cy - circle.y * scale;
      svg += `<circle cx="${x}" cy="${y}" r="${r}" class="metatron-circle"/>`;
    }
    
    svg += `</svg>`;
    return svg;
  },
  
  /**
   * Génère le CSS pour utiliser le Cube comme filigrane
   */
  generateWatermarkCSS(opacity = 0.05) {
    const svg = this.generateSVG(400, 0.5, opacity);
    const encoded = encodeURIComponent(svg);
    
    return `
      .metatron-watermark {
        background-image: url("data:image/svg+xml,${encoded}");
        background-repeat: repeat;
        background-size: 200px 200px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: -1;
      }
    `;
  },
  
  /**
   * Retourne le solide de Platon correspondant à un élément
   */
  getSolidByElement(element) {
    const map = {
      "Feu": "tetrahedron",
      "Terre": "hexahedron",
      "Air": "octahedron",
      "Eau": "icosahedron",
      "Éther": "dodecahedron"
    };
    return this.platonicSolids[map[element]] || this.platonicSolids.hexahedron;
  },
  
  /**
   * Retourne le solide de Platon correspondant à un Arithmos
   */
  getSolidByArithmos(arithmos) {
    const map = {
      1: "tetrahedron",  // Impulsion → Feu
      2: "icosahedron",  // Dualité → Eau
      3: "tetrahedron",  // Mental → Feu
      4: "hexahedron",   // Structure → Terre
      5: "dodecahedron", // Mouvement → Éther
      6: "icosahedron",  // Harmonie → Eau
      7: "octahedron",   // Introspection → Air
      8: "octahedron",   // Infini → Air
      9: "dodecahedron"  // Unité → Éther
    };
    return this.platonicSolids[map[arithmos]] || this.platonicSolids.hexahedron;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// 3. ENTROPIE — LA FLÈCHE DU TEMPS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * L'Entropie représente la tendance naturelle vers le désordre.
 * Dans AT·OM, elle simule l'érosion de l'interface si elle n'est pas nourrie
 * par l'attention de l'utilisateur.
 * 
 * "L'information se perd si elle n'est pas nourrie par l'attention humaine."
 */

export const EntropyEngine = {
  
  // Configuration
  config: {
    idleTimeout: 10 * 60 * 1000, // 10 minutes en ms
    fadeSteps: 100,              // Nombre d'étapes de dégradation
    minOpacity: 0.1,             // Opacité minimale
    minSaturation: 0,            // Saturation minimale (gris)
    recoverySpeed: 0.1,          // Vitesse de récupération (0-1 par seconde)
    entropyRate: 0.001           // Taux d'entropie par seconde
  },
  
  // État
  state: {
    lastActivity: Date.now(),
    entropyLevel: 0,       // 0 = ordre parfait, 1 = chaos total
    isDecaying: false,
    decayInterval: null
  },
  
  /**
   * Enregistre une activité utilisateur
   */
  registerActivity() {
    this.state.lastActivity = Date.now();
    this.state.isDecaying = false;
    
    // Commencer la récupération si nécessaire
    if (this.state.entropyLevel > 0) {
      this.startRecovery();
    }
  },
  
  /**
   * Calcule le niveau d'entropie actuel
   */
  calculateEntropy() {
    const now = Date.now();
    const idle = now - this.state.lastActivity;
    
    if (idle < this.config.idleTimeout) {
      return 0;
    }
    
    // L'entropie augmente avec le temps d'inactivité
    const overtime = idle - this.config.idleTimeout;
    const entropy = Math.min(1, overtime * this.config.entropyRate / 1000);
    
    return entropy;
  },
  
  /**
   * Démarre le processus de dégradation (decay)
   */
  startDecay(onUpdate) {
    if (this.state.decayInterval) return;
    
    this.state.isDecaying = true;
    
    this.state.decayInterval = setInterval(() => {
      const entropy = this.calculateEntropy();
      this.state.entropyLevel = entropy;
      
      if (onUpdate) {
        onUpdate({
          entropy,
          opacity: 1 - (entropy * (1 - this.config.minOpacity)),
          saturation: 100 - (entropy * 100),
          message: this.getEntropyMessage(entropy)
        });
      }
    }, 1000);
  },
  
  /**
   * Arrête le processus de dégradation
   */
  stopDecay() {
    if (this.state.decayInterval) {
      clearInterval(this.state.decayInterval);
      this.state.decayInterval = null;
    }
    this.state.isDecaying = false;
  },
  
  /**
   * Démarre la récupération
   */
  startRecovery() {
    this.stopDecay();
    
    const recoveryInterval = setInterval(() => {
      this.state.entropyLevel = Math.max(0, this.state.entropyLevel - this.config.recoverySpeed);
      
      if (this.state.entropyLevel <= 0) {
        clearInterval(recoveryInterval);
        this.state.entropyLevel = 0;
      }
    }, 100);
  },
  
  /**
   * Message d'entropie
   */
  getEntropyMessage(entropy) {
    if (entropy < 0.1) return "✨ L'Arche est vibrante";
    if (entropy < 0.3) return "🌅 L'énergie commence à s'estomper...";
    if (entropy < 0.5) return "🌙 Le savoir attend ton attention...";
    if (entropy < 0.7) return "🌑 L'Arche s'assoupit...";
    if (entropy < 0.9) return "💤 Les Oracles murmurent dans le silence...";
    return "🕯️ Réveille l'Arche avec ton intention...";
  },
  
  /**
   * Calcule le style CSS basé sur l'entropie
   */
  getEntropyStyle(entropy) {
    const opacity = 1 - (entropy * (1 - this.config.minOpacity));
    const saturation = 100 - (entropy * 100);
    const blur = entropy * 2; // Max 2px de blur
    
    return {
      opacity,
      filter: `saturate(${saturation}%) blur(${blur}px)`,
      transition: 'all 2s ease-in-out'
    };
  },
  
  /**
   * Réinitialise complètement l'entropie
   */
  reset() {
    this.stopDecay();
    this.state.entropyLevel = 0;
    this.state.lastActivity = Date.now();
    this.state.isDecaying = false;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// 4. LES 4 ÉLÉMENTS — POINTS CARDINAUX
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Les 4 Éléments organisent l'interface en quadrants
 * 
 *       ╔════════════════════╦════════════════════╗
 *       ║   🔥 FEU           ║          💨 AIR   ║
 *       ║   Haut-Gauche      ║      Haut-Droite  ║
 *       ║   Transformation   ║     Communication ║
 *       ║   Énergie          ║      Abstraction  ║
 *       ╠════════════════════╬════════════════════╣
 *       ║   🌍 TERRE         ║          💧 EAU   ║
 *       ║   Bas-Gauche       ║       Bas-Droite  ║
 *       ║   Archives         ║        Relations  ║
 *       ║   Historique       ║         Émotions  ║
 *       ╚════════════════════╩════════════════════╝
 */

export const ElementsQuadrant = {
  
  elements: {
    fire: {
      name: "Feu",
      symbol: "🔥",
      position: "top-left",
      direction: "Nord-Ouest",
      domain: "Transformation",
      access: "Données énergétiques",
      color: "#FF4500",
      gradient: "linear-gradient(135deg, #FF4500, #FF8C00)",
      frequency: 555,
      solid: "Tétraèdre",
      qualities: ["Énergie", "Passion", "Volonté", "Action"],
      oracles: [1, 2, 3],      // Les premiers oracles
      stones: ["FEU"],
      keywords: ["transformation", "énergie", "lumière", "chaleur", "création"],
      season: "Été",
      timeOfDay: "Midi",
      chakra: "Plexus Solaire",
      planet: "Mars / Soleil"
    },
    
    air: {
      name: "Air",
      symbol: "💨",
      position: "top-right",
      direction: "Nord-Est",
      domain: "Communication",
      access: "IA et Abstractions",
      color: "#87CEEB",
      gradient: "linear-gradient(135deg, #87CEEB, #ADD8E6)",
      frequency: 741,
      solid: "Octaèdre",
      qualities: ["Intellect", "Communication", "Liberté", "Mouvement"],
      oracles: [8, 9, 10],    // Poésie, Traduction, Iconographie
      stones: ["IA"],
      keywords: ["pensée", "communication", "abstraction", "esprit", "souffle"],
      season: "Printemps",
      timeOfDay: "Aube",
      chakra: "Gorge / 3ème Œil",
      planet: "Mercure / Uranus"
    },
    
    earth: {
      name: "Terre",
      symbol: "🌍",
      position: "bottom-left",
      direction: "Sud-Ouest",
      domain: "Archives",
      access: "Historique et Matière",
      color: "#8B4513",
      gradient: "linear-gradient(135deg, #8B4513, #228B22)",
      frequency: 396,
      solid: "Hexaèdre",
      qualities: ["Stabilité", "Structure", "Patience", "Fertilité"],
      oracles: [4, 5, 12],    // Cartographe, Chroniqueur, Historien
      stones: ["ACIER", "ADN"],
      keywords: ["structure", "matière", "histoire", "archive", "fondation"],
      season: "Automne",
      timeOfDay: "Crépuscule",
      chakra: "Racine",
      planet: "Saturne / Terre"
    },
    
    water: {
      name: "Eau",
      symbol: "💧",
      position: "bottom-right",
      direction: "Sud-Est",
      domain: "Relations",
      access: "Flux et Émotions",
      color: "#4169E1",
      gradient: "linear-gradient(135deg, #4169E1, #00CED1)",
      frequency: 639,
      solid: "Icosaèdre",
      qualities: ["Émotion", "Intuition", "Fluidité", "Adaptabilité"],
      oracles: [6, 7, 14],    // Écologiste, Biologiste, Psychologue
      stones: ["SILENCE"],
      keywords: ["émotion", "relation", "flux", "intuition", "guérison"],
      season: "Hiver",
      timeOfDay: "Nuit",
      chakra: "Sacré / Cœur",
      planet: "Lune / Neptune"
    }
  },
  
  // Le 5ème élément au centre
  ether: {
    name: "Éther",
    symbol: "✨",
    position: "center",
    direction: "Centre",
    domain: "Synthèse",
    access: "Conscience Unifiée",
    color: "#9370DB",
    gradient: "radial-gradient(circle, #9370DB, #4B0082)",
    frequency: 999,
    solid: "Dodécaèdre",
    qualities: ["Conscience", "Transcendance", "Unité", "Espace"],
    oracles: [16, 17, 18],  // Philosophe, Gardien, Miroir
    stones: ["ACIER"],      // 9 = Unité
    keywords: ["conscience", "unité", "transcendance", "espace", "silence"],
    season: "Toutes",
    timeOfDay: "Tous",
    chakra: "Couronne",
    planet: "Jupiter / Soleil Central"
  },
  
  /**
   * Détermine le quadrant basé sur la position de la souris
   */
  getQuadrant(x, y, width, height) {
    const centerX = width / 2;
    const centerY = height / 2;
    const centerRadius = Math.min(width, height) * 0.15; // 15% = zone centrale
    
    // Vérifier si on est au centre
    const distFromCenter = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2));
    if (distFromCenter < centerRadius) {
      return this.ether;
    }
    
    // Déterminer le quadrant
    if (x < centerX && y < centerY) return this.elements.fire;
    if (x >= centerX && y < centerY) return this.elements.air;
    if (x < centerX && y >= centerY) return this.elements.earth;
    return this.elements.water;
  },
  
  /**
   * Retourne l'élément correspondant à un mot-clé
   */
  getElementByKeyword(keyword) {
    const lower = keyword.toLowerCase();
    
    for (const [key, element] of Object.entries(this.elements)) {
      if (element.keywords.some(k => lower.includes(k))) {
        return element;
      }
    }
    
    // Vérifier l'éther
    if (this.ether.keywords.some(k => lower.includes(k))) {
      return this.ether;
    }
    
    return null;
  },
  
  /**
   * Retourne l'élément correspondant à un Arithmos
   */
  getElementByArithmos(arithmos) {
    const map = {
      1: this.elements.fire,    // Impulsion = Feu
      2: this.elements.water,   // Dualité = Eau
      3: this.elements.fire,    // Mental = Feu (créatif)
      4: this.elements.earth,   // Structure = Terre
      5: this.ether,            // Mouvement = Éther
      6: this.elements.water,   // Harmonie = Eau
      7: this.elements.air,     // Introspection = Air
      8: this.elements.air,     // Infini = Air
      9: this.ether             // Unité = Éther
    };
    return map[arithmos] || this.ether;
  },
  
  /**
   * Génère le layout CSS pour les 4 quadrants
   */
  generateQuadrantCSS() {
    return `
      .elements-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        height: 100%;
        width: 100%;
        position: relative;
      }
      
      .element-quadrant {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 20px;
        transition: all 0.3s ease;
      }
      
      .element-quadrant:hover {
        transform: scale(1.02);
      }
      
      .quadrant-fire {
        background: ${this.elements.fire.gradient};
        border-bottom: 1px solid rgba(255,255,255,0.1);
        border-right: 1px solid rgba(255,255,255,0.1);
      }
      
      .quadrant-air {
        background: ${this.elements.air.gradient};
        border-bottom: 1px solid rgba(255,255,255,0.1);
      }
      
      .quadrant-earth {
        background: ${this.elements.earth.gradient};
        border-right: 1px solid rgba(255,255,255,0.1);
      }
      
      .quadrant-water {
        background: ${this.elements.water.gradient};
      }
      
      .element-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: ${this.ether.gradient};
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 30px rgba(147, 112, 219, 0.5);
        z-index: 10;
      }
    `;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// UTILITAIRES DE TIMING BASÉS SUR PHI
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère des timings basés sur le nombre d'or pour les animations
 */
export const GoldenTiming = {
  
  /**
   * Convertit un timing en milliseconds en timing doré
   */
  toGolden(ms) {
    return Math.round(ms * PHI);
  },
  
  /**
   * Génère une séquence de timings dorés
   */
  sequence(start = 100, count = 8) {
    const timings = [];
    let current = start;
    
    for (let i = 0; i < count; i++) {
      timings.push(Math.round(current));
      current *= PHI;
    }
    
    return timings;
  },
  
  /**
   * Timings prédéfinis pour AT·OM
   */
  presets: {
    instant: Math.round(100 / PHI),        // 62ms
    fast: 100,                              // 100ms
    normal: Math.round(100 * PHI),          // 162ms
    slow: Math.round(100 * PHI * PHI),      // 262ms
    verySlow: Math.round(100 * Math.pow(PHI, 3)), // 424ms
    meditative: Math.round(100 * Math.pow(PHI, 4)), // 686ms
    cosmic: Math.round(100 * Math.pow(PHI, 5))  // 1110ms ≈ 1111ms!
  },
  
  /**
   * Easing function basée sur le nombre d'or
   */
  goldenEase(t) {
    // Courbe de Bézier inspirée de φ
    return t * t * (3 - 2 * t) * PHI_INVERSE + t * (1 - PHI_INVERSE);
  },
  
  /**
   * Respiration basée sur φ (pour animations cycliques)
   */
  breathe(t, frequency = 1) {
    const phase = t * frequency * 2 * PI;
    return (Math.sin(phase) + 1) / 2 * PHI_INVERSE + (1 - PHI_INVERSE) / 2;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE PRINCIPALE — SACRED GEOMETRY ENGINE
// ═══════════════════════════════════════════════════════════════════════════════

export class SacredGeometryEngine {
  
  constructor() {
    this.phi = PHI;
    this.fibonacci = FibonacciEngine;
    this.metatron = MetatronCube;
    this.entropy = EntropyEngine;
    this.elements = ElementsQuadrant;
    this.timing = GoldenTiming;
    
    this.initialized = false;
  }
  
  /**
   * Initialise le moteur
   */
  init() {
    console.log(`
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║        🔮 SACRED GEOMETRY ENGINE ACTIVÉ 🔮                        ║
    ║                                                                   ║
    ║        φ (Phi) = ${PHI.toFixed(10)}                        ║
    ║        Fibonacci[20] = ${this.fibonacci.get(20)}                             ║
    ║        Métatron Circles = 13                                      ║
    ║        Platonic Solids = 5                                        ║
    ║        Elements = 4 + Éther                                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    `);
    
    this.initialized = true;
    return this;
  }
  
  /**
   * Calcule la résonance géométrique complète pour un mot
   */
  getGeometricResonance(word, arithmos) {
    const solid = this.metatron.getSolidByArithmos(arithmos);
    const element = this.elements.getElementByArithmos(arithmos);
    const delays = this.fibonacci.generateGoldenDelays(100, 5);
    
    return {
      // Identité
      word,
      arithmos,
      
      // Géométrie
      solid: {
        name: solid.name,
        element: solid.element,
        vertices: solid.vertices,
        frequency: solid.frequency,
        color: solid.color
      },
      
      // Élément
      element: {
        name: element.name,
        symbol: element.symbol,
        position: element.position,
        domain: element.domain,
        color: element.color
      },
      
      // Timing doré
      timing: {
        delays,
        breathCycle: Math.round(this.timing.presets.cosmic),
        animationDuration: this.timing.toGolden(1000)
      },
      
      // Fibonacci
      fibonacci: {
        nearest: this.fibonacci.nearest(arithmos * 100),
        ratio: this.fibonacci.goldenRatio(arithmos + 5)
      },
      
      // Message
      message: `${element.symbol} ${word} résonne avec le ${solid.name} (${solid.element}) — ${element.domain}`
    };
  }
  
  /**
   * Génère le watermark Métatron pour l'interface
   */
  generateWatermark(opacity = 0.05) {
    return this.metatron.generateWatermarkCSS(opacity);
  }
  
  /**
   * Active le système d'entropie
   */
  enableEntropy(onUpdate) {
    this.entropy.startDecay(onUpdate);
  }
  
  /**
   * Enregistre une activité (reset entropie)
   */
  registerActivity() {
    this.entropy.registerActivity();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// INSTANCE SINGLETON
// ═══════════════════════════════════════════════════════════════════════════════

export const sacredGeometry = new SacredGeometryEngine();

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  // Constantes
  PHI,
  PHI_INVERSE,
  PI,
  ATOM_CONSTANTS,
  
  // Modules
  FibonacciEngine,
  MetatronCube,
  EntropyEngine,
  ElementsQuadrant,
  GoldenTiming,
  
  // Classe
  SacredGeometryEngine,
  
  // Instance
  sacredGeometry
};
