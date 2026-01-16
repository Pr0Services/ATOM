/**
 * AT·OM — VIBRATIONAL TIMING ENGINE
 * 
 * Synchronisateur Visuel basé sur les Fréquences Sacrées
 * 
 * Loi fondamentale:
 *   - Plus la fréquence est haute (999Hz) → animation fluide et rapide
 *   - Plus la fréquence est basse (111Hz) → animation dense et lente
 *   - 444Hz = référence (ancre)
 * 
 * @version 2.0.0
 * @anchor 444 Hz
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const ANCHOR_FREQUENCY = 444;
const MIN_FREQUENCY = 111;
const MAX_FREQUENCY = 999;

// Mapping fréquence → delay (en ms)
const FREQUENCY_DELAY_MAP = {
  111: 900,   // Très lent - Dense
  222: 800,   // Lent
  333: 700,   // Modéré
  444: 600,   // Référence - Ancre
  555: 500,   // Rapide
  666: 400,   // Très rapide
  777: 300,   // Ultra rapide
  888: 200,   // Instantané
  999: 100,   // Flash
};

// Mapping fréquence → easing function
const FREQUENCY_EASING_MAP = {
  111: 'cubic-bezier(0.4, 0, 0.2, 1)',     // ease-out dense
  222: 'cubic-bezier(0.4, 0, 0.2, 1)',
  333: 'cubic-bezier(0.25, 0.1, 0.25, 1)', // ease standard
  444: 'cubic-bezier(0.25, 0.1, 0.25, 1)', // référence
  555: 'cubic-bezier(0.0, 0, 0.2, 1)',     // ease-out
  666: 'cubic-bezier(0.0, 0, 0.2, 1)',
  777: 'linear',                            // ultra fluide
  888: 'linear',
  999: 'steps(1)',                          // instantané
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTION PRINCIPALE: getVibrationalDelay
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Calcule le délai d'animation basé sur la fréquence.
 * 
 * @param {number} frequency - Fréquence en Hz (111-999)
 * @returns {number} Délai en millisecondes
 * 
 * @example
 * getVibrationalDelay(444) // → 600
 * getVibrationalDelay(999) // → 100
 * getVibrationalDelay(111) // → 900
 */
function getVibrationalDelay(frequency) {
  // Validation
  if (typeof frequency !== 'number' || isNaN(frequency)) {
    console.warn('getVibrationalDelay: fréquence invalide, utilisation de 444Hz');
    return FREQUENCY_DELAY_MAP[444];
  }

  // Clamp entre 111 et 999
  const clampedFreq = Math.max(MIN_FREQUENCY, Math.min(MAX_FREQUENCY, frequency));
  
  // Lookup direct si c'est une fréquence exacte
  if (FREQUENCY_DELAY_MAP[clampedFreq]) {
    return FREQUENCY_DELAY_MAP[clampedFreq];
  }
  
  // Interpolation linéaire pour les fréquences intermédiaires
  // Formule: delay = 900 - ((freq - 111) / (999 - 111)) * (900 - 100)
  const normalizedFreq = (clampedFreq - MIN_FREQUENCY) / (MAX_FREQUENCY - MIN_FREQUENCY);
  const delay = 900 - (normalizedFreq * 800);
  
  return Math.round(delay);
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE TIMING AVANCÉES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Obtient la configuration de timing complète pour une fréquence.
 * 
 * @param {number} frequency - Fréquence en Hz
 * @returns {Object} Configuration de timing
 */
function getVibrationalTiming(frequency) {
  const delay = getVibrationalDelay(frequency);
  const clampedFreq = Math.max(MIN_FREQUENCY, Math.min(MAX_FREQUENCY, frequency));
  
  // Trouver la fréquence de référence la plus proche
  const frequencies = Object.keys(FREQUENCY_DELAY_MAP).map(Number);
  const closestFreq = frequencies.reduce((prev, curr) => 
    Math.abs(curr - clampedFreq) < Math.abs(prev - clampedFreq) ? curr : prev
  );
  
  return {
    frequency: clampedFreq,
    delay_ms: delay,
    duration_ms: delay * 1.5,
    easing: FREQUENCY_EASING_MAP[closestFreq] || 'ease',
    stagger_ms: Math.round(delay / 10),
    pulse_interval_ms: Math.round(1000 / (frequency / 100)),
    is_anchor: frequency === ANCHOR_FREQUENCY,
    density: getDensityLevel(frequency),
    speed_class: getSpeedClass(frequency),
  };
}

/**
 * Détermine le niveau de densité basé sur la fréquence.
 */
function getDensityLevel(frequency) {
  if (frequency <= 222) return 'maximum';
  if (frequency <= 333) return 'high';
  if (frequency <= 444) return 'balanced';
  if (frequency <= 555) return 'medium';
  if (frequency <= 666) return 'low';
  if (frequency <= 777) return 'minimal';
  return 'ethereal';
}

/**
 * Détermine la classe de vitesse.
 */
function getSpeedClass(frequency) {
  if (frequency <= 111) return 'very-slow';
  if (frequency <= 222) return 'slow';
  if (frequency <= 333) return 'moderate';
  if (frequency <= 444) return 'reference';
  if (frequency <= 555) return 'fast';
  if (frequency <= 666) return 'very-fast';
  if (frequency <= 777) return 'ultra-fast';
  if (frequency <= 888) return 'instant';
  return 'flash';
}

// ═══════════════════════════════════════════════════════════════════════════════
// REMPLACEMENT DE setTimeout / setInterval
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * setTimeout basé sur la fréquence vibratoire.
 * Remplace setTimeout avec un timing harmonisé.
 * 
 * @param {Function} callback - Fonction à exécuter
 * @param {number} frequency - Fréquence en Hz
 * @param {number} multiplier - Multiplicateur optionnel (défaut: 1)
 * @returns {number} ID du timeout
 */
function vibrationalTimeout(callback, frequency, multiplier = 1) {
  const delay = getVibrationalDelay(frequency) * multiplier;
  return setTimeout(callback, delay);
}

/**
 * setInterval basé sur la fréquence vibratoire.
 * 
 * @param {Function} callback - Fonction à exécuter
 * @param {number} frequency - Fréquence en Hz
 * @returns {number} ID de l'interval
 */
function vibrationalInterval(callback, frequency) {
  const delay = getVibrationalDelay(frequency);
  return setInterval(callback, delay);
}

/**
 * Crée une animation pulsante basée sur la fréquence.
 * 
 * @param {HTMLElement} element - Élément DOM
 * @param {number} frequency - Fréquence en Hz
 * @param {Object} options - Options d'animation
 */
function vibrationalPulse(element, frequency, options = {}) {
  const timing = getVibrationalTiming(frequency);
  
  const keyframes = [
    { transform: 'scale(1)', opacity: 1 },
    { transform: 'scale(1.05)', opacity: 0.8 },
    { transform: 'scale(1)', opacity: 1 },
  ];
  
  const animationOptions = {
    duration: timing.duration_ms,
    easing: timing.easing,
    iterations: options.infinite ? Infinity : 1,
  };
  
  return element.animate(keyframes, animationOptions);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CSS GENERATION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère les CSS custom properties pour une fréquence.
 * 
 * @param {number} frequency - Fréquence en Hz
 * @returns {Object} CSS custom properties
 */
function generateCSSProperties(frequency) {
  const timing = getVibrationalTiming(frequency);
  
  return {
    '--vibration-delay': `${timing.delay_ms}ms`,
    '--vibration-duration': `${timing.duration_ms}ms`,
    '--vibration-easing': timing.easing,
    '--vibration-stagger': `${timing.stagger_ms}ms`,
    '--vibration-pulse': `${timing.pulse_interval_ms}ms`,
  };
}

/**
 * Applique les CSS properties à un élément.
 * 
 * @param {HTMLElement} element - Élément DOM
 * @param {number} frequency - Fréquence en Hz
 */
function applyVibrationalStyles(element, frequency) {
  const props = generateCSSProperties(frequency);
  
  Object.entries(props).forEach(([key, value]) => {
    element.style.setProperty(key, value);
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// ANIMATION SEQUENCES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Crée une séquence d'animations avec stagger basé sur la fréquence.
 * 
 * @param {NodeList|Array} elements - Éléments à animer
 * @param {number} frequency - Fréquence en Hz
 * @param {Object} animationConfig - Configuration Anime.js / Web Animations
 */
function vibrationalStagger(elements, frequency, animationConfig = {}) {
  const timing = getVibrationalTiming(frequency);
  const elementsArray = Array.from(elements);
  
  elementsArray.forEach((el, index) => {
    const staggerDelay = timing.stagger_ms * index;
    
    setTimeout(() => {
      el.animate(
        animationConfig.keyframes || [
          { opacity: 0, transform: 'translateY(20px)' },
          { opacity: 1, transform: 'translateY(0)' },
        ],
        {
          duration: timing.duration_ms,
          easing: timing.easing,
          fill: 'forwards',
        }
      );
    }, staggerDelay);
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

// Pour ES Modules
export {
  ANCHOR_FREQUENCY,
  getVibrationalDelay,
  getVibrationalTiming,
  getDensityLevel,
  getSpeedClass,
  vibrationalTimeout,
  vibrationalInterval,
  vibrationalPulse,
  generateCSSProperties,
  applyVibrationalStyles,
  vibrationalStagger,
};

// Pour CommonJS
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    ANCHOR_FREQUENCY,
    getVibrationalDelay,
    getVibrationalTiming,
    getDensityLevel,
    getSpeedClass,
    vibrationalTimeout,
    vibrationalInterval,
    vibrationalPulse,
    generateCSSProperties,
    applyVibrationalStyles,
    vibrationalStagger,
  };
}

// Pour usage global dans le navigateur
if (typeof window !== 'undefined') {
  window.VibrationalTiming = {
    ANCHOR_FREQUENCY,
    getVibrationalDelay,
    getVibrationalTiming,
    getDensityLevel,
    getSpeedClass,
    vibrationalTimeout,
    vibrationalInterval,
    vibrationalPulse,
    generateCSSProperties,
    applyVibrationalStyles,
    vibrationalStagger,
  };
}
