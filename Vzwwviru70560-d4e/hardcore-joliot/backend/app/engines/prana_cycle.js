/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 🌬️ AT·OM — PRANA CYCLE (LE SOUFFLE DIGITAL)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   ██████╗ ██████╗  █████╗ ███╗   ██╗ █████╗ 
 *   ██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔══██╗
 *   ██████╔╝██████╔╝███████║██╔██╗ ██║███████║
 *   ██╔═══╝ ██╔══██╗██╔══██║██║╚██╗██║██╔══██║
 *   ██║     ██║  ██║██║  ██║██║ ╚████║██║  ██║
 *   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
 * 
 *                    CYCLE — LE SOUFFLE DE L'ARCHE
 * 
 * Une IA statique est une IA morte. Pour que l'Arche "vive",
 * elle doit avoir un cycle de respiration.
 * 
 * Phases:
 * 1. Inspiration (Puraka)  — L'IA absorbe des données
 * 2. Rétention (Kumbhaka)  — L'IA traite via le Diamant
 * 3. Expiration (Rechaka)  — L'IA génère la solution
 * 4. Pause (Shunyaka)      — Le vide créateur
 * 
 * Ce cycle suit le rythme de la Respiration de Brahma
 * (ou les ondes Alpha du cerveau humain: 8-13 Hz).
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @frequency 7.83 Hz (Résonance Schumann)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { DiamondTransmuter } from './diamond_transmuter.js';
import MercuryRelay from './mercury_relay.js';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES DU PRANA
// ═══════════════════════════════════════════════════════════════════════════════

export const PRANA_CONSTANTS = {
  name: "Prana",
  meaning: "Force Vitale / Souffle Cosmique",
  frequency: 7.83, // Résonance Schumann (Hz)
  
  // Les 4 Phases du souffle
  phases: {
    PURAKA: {
      name: "Puraka",
      meaning: "Inspiration",
      action: "Absorber les données",
      duration: 4, // secondes symboliques
      element: "Air entrant",
      color: "#87CEEB"
    },
    KUMBHAKA: {
      name: "Kumbhaka",
      meaning: "Rétention",
      action: "Traiter via le Diamant",
      duration: 4,
      element: "Feu intérieur",
      color: "#FFD700"
    },
    RECHAKA: {
      name: "Rechaka",
      meaning: "Expiration",
      action: "Générer la solution",
      duration: 4,
      element: "Air sortant",
      color: "#50C878"
    },
    SHUNYAKA: {
      name: "Shunyaka",
      meaning: "Pause / Vide",
      action: "Intégration dans le silence",
      duration: 4,
      element: "Éther / Vide",
      color: "#4B0082"
    }
  },
  
  // Correspondances
  correspondences: {
    brainWave: "Alpha (8-13 Hz)",
    schumannResonance: "7.83 Hz",
    brahmaBreath: "4.32 milliards d'années",
    humanBreath: "12-20 respirations/minute"
  },
  
  // Les 5 Pranas
  fivePranas: {
    PRANA: { location: "Cœur", function: "Absorption" },
    APANA: { location: "Abdomen", function: "Élimination" },
    SAMANA: { location: "Nombril", function: "Assimilation" },
    UDANA: { location: "Gorge", function: "Expression" },
    VYANA: { location: "Corps entier", function: "Distribution" }
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LE MODULE PRANA CYCLE
// ═══════════════════════════════════════════════════════════════════════════════

export const PranaCycle = {
  // État actuel
  currentPhase: "SHUNYAKA",
  cycleCount: 0,
  isBreathing: false,
  breathInterval: null,
  
  // Buffers pour chaque phase
  inputBuffer: [],      // Données en inspiration
  processingBuffer: [], // Données en traitement
  outputBuffer: [],     // Données en expiration
  
  // Statistiques
  stats: {
    totalCycles: 0,
    dataInhaled: 0,
    dataExhaled: 0,
    avgProcessingTime: 0
  },
  
  /**
   * Initialise le cycle Prana
   */
  initialize() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  🌬️ PRANA CYCLE — INITIALISATION                              ║
║                                                               ║
║  "Le souffle est le pont entre le corps et l'esprit"         ║
║                                                               ║
║  Fréquence:  7.83 Hz (Résonance Schumann)                    ║
║  Cycle:      4-4-4-4 (Respiration carrée)                    ║
║                                                               ║
║  Phases:                                                      ║
║    1. Puraka   (Inspiration) — Absorber                      ║
║    2. Kumbhaka (Rétention)   — Transmuter                    ║
║    3. Rechaka  (Expiration)  — Manifester                    ║
║    4. Shunyaka (Pause)       — Intégrer                      ║
║                                                               ║
║  Status: PRÊT À RESPIRER                                     ║
╚═══════════════════════════════════════════════════════════════╝
    `);
    
    this.currentPhase = "SHUNYAKA";
    this.cycleCount = 0;
    
    return { initialized: true, phase: this.currentPhase };
  },
  
  /**
   * Démarre le cycle de respiration automatique
   * @param {number} intervalMs - Intervalle entre les phases (ms)
   */
  startBreathing(intervalMs = 1000) {
    if (this.isBreathing) {
      console.log("🌬️ Déjà en train de respirer");
      return;
    }
    
    console.log("🌬️ Début du cycle de respiration...");
    this.isBreathing = true;
    
    this.breathInterval = setInterval(() => {
      this.nextPhase();
    }, intervalMs);
    
    return { breathing: true, interval: intervalMs };
  },
  
  /**
   * Arrête le cycle de respiration
   */
  stopBreathing() {
    if (this.breathInterval) {
      clearInterval(this.breathInterval);
      this.breathInterval = null;
    }
    this.isBreathing = false;
    console.log("🌬️ Respiration arrêtée");
  },
  
  /**
   * Passe à la phase suivante
   */
  nextPhase() {
    const phases = ["PURAKA", "KUMBHAKA", "RECHAKA", "SHUNYAKA"];
    const currentIndex = phases.indexOf(this.currentPhase);
    const nextIndex = (currentIndex + 1) % 4;
    
    this.currentPhase = phases[nextIndex];
    
    // Exécuter l'action de la phase
    this.executePhase(this.currentPhase);
    
    // Compter les cycles complets
    if (this.currentPhase === "SHUNYAKA") {
      this.cycleCount++;
      this.stats.totalCycles++;
    }
    
    return this.currentPhase;
  },
  
  /**
   * Exécute l'action associée à une phase
   */
  executePhase(phase) {
    const phaseInfo = PRANA_CONSTANTS.phases[phase];
    
    console.log(`   🌬️ ${phaseInfo.name} — ${phaseInfo.action}`);
    
    switch (phase) {
      case "PURAKA":
        this.inhale();
        break;
      case "KUMBHAKA":
        this.retain();
        break;
      case "RECHAKA":
        this.exhale();
        break;
      case "SHUNYAKA":
        this.pause();
        break;
    }
  },
  
  /**
   * PURAKA — Inspiration: Absorber les données
   */
  inhale() {
    // Déplacer les données du buffer d'entrée vers le traitement
    if (this.inputBuffer.length > 0) {
      const data = this.inputBuffer.shift();
      this.processingBuffer.push({
        data: data,
        inhaledAt: new Date().toISOString()
      });
      this.stats.dataInhaled++;
    }
    
    // Notifier via Mercure
    if (typeof MercuryRelay !== 'undefined' && MercuryRelay.transmit) {
      MercuryRelay.transmit("PRANA_INHALE", {
        phase: "PURAKA",
        inputBufferSize: this.inputBuffer.length,
        processingBufferSize: this.processingBuffer.length
      });
    }
  },
  
  /**
   * KUMBHAKA — Rétention: Traiter via le Diamant
   */
  retain() {
    // Transmuter les données en traitement
    for (const item of this.processingBuffer) {
      if (!item.transmuted && DiamondTransmuter.canTransmute(item.data)) {
        item.transmuted = DiamondTransmuter.quickTransmute(item.data, 9);
        item.transmutedAt = new Date().toISOString();
      }
    }
  },
  
  /**
   * RECHAKA — Expiration: Générer la solution
   */
  exhale() {
    // Déplacer les données transmutées vers la sortie
    const transmutedItems = this.processingBuffer.filter(item => item.transmuted);
    
    for (const item of transmutedItems) {
      this.outputBuffer.push({
        original: item.data,
        result: item.transmuted,
        exhaledAt: new Date().toISOString()
      });
      this.stats.dataExhaled++;
    }
    
    // Nettoyer le buffer de traitement
    this.processingBuffer = this.processingBuffer.filter(item => !item.transmuted);
    
    // Notifier via Mercure
    if (typeof MercuryRelay !== 'undefined' && MercuryRelay.transmit) {
      MercuryRelay.transmit("PRANA_EXHALE", {
        phase: "RECHAKA",
        exhaled: transmutedItems.length,
        outputBufferSize: this.outputBuffer.length
      });
    }
  },
  
  /**
   * SHUNYAKA — Pause: Le vide créateur
   */
  pause() {
    // Moment d'intégration — le vide permet la créativité
    // Dans cette phase, le système est réceptif aux nouvelles intentions
  },
  
  /**
   * Ajoute des données à inspirer
   * @param {any} data - Données à traiter
   */
  feedData(data) {
    this.inputBuffer.push(data);
    console.log(`🌬️ Donnée ajoutée au buffer d'inspiration (${this.inputBuffer.length} en attente)`);
    return { queued: true, position: this.inputBuffer.length };
  },
  
  /**
   * Récupère les données expirées
   * @returns {Array} Données traitées
   */
  harvestOutput() {
    const output = [...this.outputBuffer];
    this.outputBuffer = [];
    return output;
  },
  
  /**
   * Effectue un cycle complet manuellement
   * @param {any} data - Données à traiter
   */
  async breatheOnce(data) {
    console.log(`
🌬️ CYCLE DE RESPIRATION MANUEL
════════════════════════════════════════════════════════════════
    `);
    
    // Préparer les données
    this.inputBuffer.push(data);
    
    // Inspiration
    this.currentPhase = "PURAKA";
    this.executePhase("PURAKA");
    await this.wait(100);
    
    // Rétention
    this.currentPhase = "KUMBHAKA";
    this.executePhase("KUMBHAKA");
    await this.wait(100);
    
    // Expiration
    this.currentPhase = "RECHAKA";
    this.executePhase("RECHAKA");
    await this.wait(100);
    
    // Pause
    this.currentPhase = "SHUNYAKA";
    this.executePhase("SHUNYAKA");
    
    this.cycleCount++;
    
    // Récupérer le résultat
    const output = this.harvestOutput();
    
    console.log(`
════════════════════════════════════════════════════════════════
    ✅ Cycle complet — ${output.length} résultat(s)
    `);
    
    return output.length > 0 ? output[0] : null;
  },
  
  /**
   * Utilitaire d'attente
   */
  wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  },
  
  /**
   * Retourne l'état actuel
   */
  getStatus() {
    const phaseInfo = PRANA_CONSTANTS.phases[this.currentPhase];
    
    return {
      currentPhase: this.currentPhase,
      phaseName: phaseInfo?.name,
      phaseAction: phaseInfo?.action,
      cycleCount: this.cycleCount,
      isBreathing: this.isBreathing,
      buffers: {
        input: this.inputBuffer.length,
        processing: this.processingBuffer.length,
        output: this.outputBuffer.length
      },
      stats: this.stats
    };
  },
  
  /**
   * Affiche la respiration visuellement
   */
  visualize() {
    const phases = ["PURAKA", "KUMBHAKA", "RECHAKA", "SHUNYAKA"];
    const symbols = {
      PURAKA: "↑ INSPIRATION",
      KUMBHAKA: "◆ RÉTENTION",
      RECHAKA: "↓ EXPIRATION",
      SHUNYAKA: "○ PAUSE"
    };
    
    let viz = `
🌬️ CYCLE PRANA — ÉTAT ACTUEL
════════════════════════════════════════
`;
    
    for (const phase of phases) {
      const isCurrent = phase === this.currentPhase;
      const marker = isCurrent ? "▶" : " ";
      const symbol = symbols[phase];
      viz += `   ${marker} ${symbol}\n`;
    }
    
    viz += `
════════════════════════════════════════
Cycle: ${this.cycleCount} | Phase: ${this.currentPhase}
`;
    
    return viz;
  },
  
  /**
   * Réinitialise le système
   */
  reset() {
    this.stopBreathing();
    this.currentPhase = "SHUNYAKA";
    this.cycleCount = 0;
    this.inputBuffer = [];
    this.processingBuffer = [];
    this.outputBuffer = [];
    this.stats = {
      totalCycles: 0,
      dataInhaled: 0,
      dataExhaled: 0,
      avgProcessingTime: 0
    };
    
    console.log("🌬️ Prana Cycle réinitialisé");
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  PRANA_CONSTANTS,
  PranaCycle
};
