/**
 * AT·OM — OSCILLATOR ENGINE
 * 
 * Audio Engine basé sur le tempérament juste (Just Intonation)
 * Référence: LA = 444 Hz (au lieu du standard 440 Hz)
 * 
 * Ce moteur génère des tonalités pures alignées sur la Matrice Sacrée.
 * Chaque résonance (1-9) correspond à une fréquence harmonique.
 * 
 * @version 2.0.0
 * @tuning Just Intonation
 * @reference LA = 444 Hz
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES FONDAMENTALES
// ═══════════════════════════════════════════════════════════════════════════════

const REFERENCE_FREQUENCY = 444; // LA en Just Intonation AT-OM
const STANDARD_A4 = 440;         // LA standard (non utilisé)

// Matrice des fréquences sacrées
const SACRED_FREQUENCIES = {
  1: 111,  // Impulsion - Rouge
  2: 222,  // Dualité - Orange
  3: 333,  // Mental - Jaune
  4: 444,  // Structure/Cœur - Vert Émeraude (ANCRE)
  5: 555,  // Mouvement - Bleu Ciel
  6: 666,  // Harmonie - Indigo
  7: 777,  // Silence - Violet
  8: 888,  // Infini - Rose
  9: 999,  // Unité - Blanc-Or
};

// Nombres maîtres
const MASTER_FREQUENCIES = {
  11: 1111,
  22: 2222,
  33: 3333,
};

// Configuration ADSR par défaut
const DEFAULT_ADSR = {
  attack: 0.05,   // 50ms
  decay: 0.1,     // 100ms
  sustain: 0.7,   // 70% du volume
  release: 0.2,   // 200ms
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE PRINCIPALE: ATOMAudioEngine
// ═══════════════════════════════════════════════════════════════════════════════

class ATOMAudioEngine {
  constructor(options = {}) {
    this.context = null;
    this.masterGain = null;
    this.isInitialized = false;
    this.activeOscillators = new Map();
    
    // Options
    this.options = {
      referenceFrequency: REFERENCE_FREQUENCY,
      defaultWaveform: options.waveform || 'sine',
      defaultVolume: options.volume || 0.5,
      adsr: { ...DEFAULT_ADSR, ...options.adsr },
    };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // INITIALISATION
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Initialise le contexte audio.
   * Doit être appelé après une interaction utilisateur (click, etc.)
   */
  async init() {
    if (this.isInitialized) return this;

    try {
      // Créer le contexte audio
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.context = new AudioContext();

      // Créer le gain master
      this.masterGain = this.context.createGain();
      this.masterGain.gain.value = this.options.defaultVolume;
      this.masterGain.connect(this.context.destination);

      // Résumer le contexte si suspendu
      if (this.context.state === 'suspended') {
        await this.context.resume();
      }

      this.isInitialized = true;
      console.log(`AT·OM Audio Engine initialisé @ ${this.options.referenceFrequency}Hz`);
      
      return this;
    } catch (error) {
      console.error('Erreur initialisation audio:', error);
      throw error;
    }
  }

  /**
   * Vérifie que le moteur est initialisé.
   */
  ensureInitialized() {
    if (!this.isInitialized) {
      throw new Error('ATOMAudioEngine non initialisé. Appelez init() après une interaction utilisateur.');
    }
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // GÉNÉRATION DE TONS
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Joue une tonalité basée sur la valeur arithmos (1-9).
   * 
   * @param {number} arithmosValue - Valeur de résonance (1-9 ou 11/22/33)
   * @param {Object} options - Options de lecture
   * @returns {string} ID de l'oscillateur
   */
  playResonance(arithmosValue, options = {}) {
    this.ensureInitialized();

    // Récupérer la fréquence
    let frequency;
    if (MASTER_FREQUENCIES[arithmosValue]) {
      frequency = MASTER_FREQUENCIES[arithmosValue];
    } else if (SACRED_FREQUENCIES[arithmosValue]) {
      frequency = SACRED_FREQUENCIES[arithmosValue];
    } else {
      console.warn(`Valeur arithmos ${arithmosValue} invalide, utilisation de 444Hz`);
      frequency = SACRED_FREQUENCIES[4];
    }

    return this.playFrequency(frequency, options);
  }

  /**
   * Joue une fréquence spécifique.
   * 
   * @param {number} frequency - Fréquence en Hz
   * @param {Object} options - Options de lecture
   * @returns {string} ID de l'oscillateur
   */
  playFrequency(frequency, options = {}) {
    this.ensureInitialized();

    const {
      duration = 1000,        // Durée en ms
      waveform = this.options.defaultWaveform,
      volume = 1,
      pan = 0,                // -1 (gauche) à 1 (droite)
      adsr = this.options.adsr,
    } = options;

    const id = `osc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const now = this.context.currentTime;

    // Créer l'oscillateur
    const oscillator = this.context.createOscillator();
    oscillator.type = waveform;
    oscillator.frequency.value = frequency;

    // Créer le gain pour l'enveloppe ADSR
    const gainNode = this.context.createGain();
    gainNode.gain.value = 0;

    // Créer le panner (optionnel)
    let panNode = null;
    if (pan !== 0) {
      panNode = this.context.createStereoPanner();
      panNode.pan.value = pan;
    }

    // Connecter la chaîne audio
    oscillator.connect(gainNode);
    if (panNode) {
      gainNode.connect(panNode);
      panNode.connect(this.masterGain);
    } else {
      gainNode.connect(this.masterGain);
    }

    // Appliquer l'enveloppe ADSR
    const peakTime = now + adsr.attack;
    const sustainTime = peakTime + adsr.decay;
    const releaseTime = now + (duration / 1000) - adsr.release;
    const endTime = now + (duration / 1000);

    // Attack
    gainNode.gain.setValueAtTime(0, now);
    gainNode.gain.linearRampToValueAtTime(volume, peakTime);

    // Decay → Sustain
    gainNode.gain.linearRampToValueAtTime(volume * adsr.sustain, sustainTime);

    // Release
    gainNode.gain.setValueAtTime(volume * adsr.sustain, releaseTime);
    gainNode.gain.linearRampToValueAtTime(0, endTime);

    // Démarrer et arrêter
    oscillator.start(now);
    oscillator.stop(endTime);

    // Stocker pour référence
    this.activeOscillators.set(id, {
      oscillator,
      gainNode,
      panNode,
      frequency,
      startTime: now,
      endTime,
    });

    // Nettoyer après la fin
    oscillator.onended = () => {
      this.activeOscillators.delete(id);
    };

    return id;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // SÉQUENCES ET ACCORDS
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Joue une séquence de résonances.
   * 
   * @param {Array<number>} sequence - Tableau de valeurs arithmos
   * @param {Object} options - Options
   * @returns {Promise} Résolu quand la séquence est terminée
   */
  async playSequence(sequence, options = {}) {
    this.ensureInitialized();

    const {
      noteDuration = 500,
      gap = 100,
    } = options;

    for (const value of sequence) {
      this.playResonance(value, { duration: noteDuration });
      await this.sleep(noteDuration + gap);
    }
  }

  /**
   * Joue un accord (plusieurs fréquences simultanées).
   * 
   * @param {Array<number>} values - Valeurs arithmos à jouer ensemble
   * @param {Object} options - Options
   */
  playChord(values, options = {}) {
    this.ensureInitialized();

    const volumePerNote = (options.volume || 1) / Math.sqrt(values.length);

    values.forEach((value, index) => {
      this.playResonance(value, {
        ...options,
        volume: volumePerNote,
        pan: this.calculatePan(index, values.length),
      });
    });
  }

  /**
   * Joue l'accord de la Matrice complète (1-9).
   */
  playFullMatrix(options = {}) {
    this.playChord([1, 2, 3, 4, 5, 6, 7, 8, 9], {
      duration: 3000,
      ...options,
    });
  }

  /**
   * Joue la tonalité d'ancrage (444 Hz).
   */
  playAnchor(options = {}) {
    return this.playResonance(4, { duration: 2000, ...options });
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // UTILITAIRES
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Calcule la position pan pour un accord.
   */
  calculatePan(index, total) {
    if (total === 1) return 0;
    return -1 + (2 * index / (total - 1));
  }

  /**
   * Utilitaire sleep.
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Arrête tous les oscillateurs actifs.
   */
  stopAll() {
    this.activeOscillators.forEach(({ oscillator }) => {
      try {
        oscillator.stop();
      } catch (e) {
        // Déjà arrêté
      }
    });
    this.activeOscillators.clear();
  }

  /**
   * Définit le volume master.
   */
  setMasterVolume(volume) {
    if (this.masterGain) {
      this.masterGain.gain.value = Math.max(0, Math.min(1, volume));
    }
  }

  /**
   * Obtient la fréquence pour une valeur arithmos.
   */
  getFrequencyForValue(arithmosValue) {
    return MASTER_FREQUENCIES[arithmosValue] || 
           SACRED_FREQUENCIES[arithmosValue] || 
           SACRED_FREQUENCIES[4];
  }

  /**
   * Ferme le contexte audio.
   */
  async close() {
    this.stopAll();
    if (this.context) {
      await this.context.close();
      this.isInitialized = false;
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS HELPER STATIQUES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Convertit une note musicale en fréquence (tempérament 444Hz).
 * 
 * @param {string} note - Note (ex: "A4", "C5", "F#3")
 * @returns {number} Fréquence en Hz
 */
function noteToFrequency444(note) {
  const noteRegex = /^([A-G]#?)(\d+)$/;
  const match = note.toUpperCase().match(noteRegex);
  
  if (!match) {
    throw new Error(`Note invalide: ${note}`);
  }

  const noteName = match[1];
  const octave = parseInt(match[2]);

  // Demi-tons depuis A4
  const noteOffsets = {
    'C': -9, 'C#': -8, 'D': -7, 'D#': -6,
    'E': -5, 'F': -4, 'F#': -3, 'G': -2,
    'G#': -1, 'A': 0, 'A#': 1, 'B': 2,
  };

  const semitonesFromA4 = noteOffsets[noteName] + (octave - 4) * 12;
  
  // Formule: f = 444 * 2^(n/12)
  return REFERENCE_FREQUENCY * Math.pow(2, semitonesFromA4 / 12);
}

/**
 * Génère un tableau d'harmoniques pour une fréquence fondamentale.
 * 
 * @param {number} fundamental - Fréquence fondamentale
 * @param {number} count - Nombre d'harmoniques
 * @returns {Array<number>} Tableau de fréquences
 */
function generateHarmonics(fundamental, count = 8) {
  return Array.from({ length: count }, (_, i) => fundamental * (i + 1));
}

// ═══════════════════════════════════════════════════════════════════════════════
// INSTANCE SINGLETON
// ═══════════════════════════════════════════════════════════════════════════════

let atomAudioInstance = null;

/**
 * Obtient l'instance singleton du moteur audio.
 */
function getATOMAudio() {
  if (!atomAudioInstance) {
    atomAudioInstance = new ATOMAudioEngine();
  }
  return atomAudioInstance;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export {
  REFERENCE_FREQUENCY,
  SACRED_FREQUENCIES,
  MASTER_FREQUENCIES,
  ATOMAudioEngine,
  noteToFrequency444,
  generateHarmonics,
  getATOMAudio,
};

export default ATOMAudioEngine;

// Pour CommonJS
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    REFERENCE_FREQUENCY,
    SACRED_FREQUENCIES,
    MASTER_FREQUENCIES,
    ATOMAudioEngine,
    noteToFrequency444,
    generateHarmonics,
    getATOMAudio,
  };
}

// Pour usage global
if (typeof window !== 'undefined') {
  window.ATOMAudio = {
    REFERENCE_FREQUENCY,
    SACRED_FREQUENCIES,
    MASTER_FREQUENCIES,
    ATOMAudioEngine,
    noteToFrequency444,
    generateHarmonics,
    getATOMAudio,
  };
}
