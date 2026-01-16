/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM ENGINES — INDEX PRINCIPAL
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   █████╗ ████████╗    ██████╗ ███╗   ███╗
 *  ██╔══██╗╚══██╔══╝   ██╔═══██╗████╗ ████║
 *  ███████║   ██║      ██║   ██║██╔████╔██║
 *  ██╔══██║   ██║      ██║   ██║██║╚██╔╝██║
 *  ██║  ██║   ██║   ██╗╚██████╔╝██║ ╚═╝ ██║
 *  ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝
 * 
 *                    ENGINES INDEX
 * 
 * Point d'entrée pour tous les moteurs de résonance:
 * 
 * ┌─────────────────────────────────────────────────────────────────┐
 * │  🌀 Tzolkin Engine    - Calendrier Maya (13 Tons × 20 Nawals)  │
 * │  ☯️ Yi-King Engine     - 64 Hexagrammes chinois                │
 * │  🌳 Kabbalah Engine   - Arbre de Vie (10 Sephiroth)            │
 * │  🧘 Chakra Engine     - 7 Centres énergétiques                 │
 * │  🔮 Cymatics Engine   - Géométrie sacrée & Fibonacci           │
 * │  ✨ Universal Engine  - FUSION DE TOUS LES SYSTÈMES            │
 * └─────────────────────────────────────────────────────────────────┘
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// MOTEURS INDIVIDUELS
// ═══════════════════════════════════════════════════════════════════════════════

// 🌀 Maya - Tzolkin (13 × 20 = 260 jours)
export { 
  default as TzolkinEngine,
  NAWALS,
  TONS,
  calculateKin,
  getMayaResonance,
  findNawalForArithmos,
  calculateKinCompatibility
} from './tzolkin_engine.js';

// ☯️ Chine - Yi-King (64 Hexagrammes)
export {
  default as YiKingEngine,
  TRIGRAMS,
  ALL_HEXAGRAMS,
  getHexagramForArithmos,
  getMutatingHexagram,
  getYiKingReading,
  getYiKingResonance,
  castCoins
} from './yiking_engine.js';

// 🌳 Kabbale - Arbre de Vie (10 Sephiroth + 22 Sentiers)
export {
  default as KabbalahEngine,
  SEPHIROTH,
  PATHS,
  PILLARS,
  WORLDS,
  getSephirahForArithmos,
  getPathBetween,
  calculatePath,
  getKabbalahResonance,
  generateTreeOfLifeData,
  mapSephirahToOracle
} from './kabbalah_engine.js';

// 🧘 Inde - Chakras (7 Centres)
export {
  default as ChakraEngine,
  CHAKRAS,
  NADIS,
  SOLFEGGIO,
  getChakraForAtomFrequency,
  getChakraForArithmos,
  calculateEnergyState,
  getChakraResonance,
  generateChakraSystemData,
  solfeggioToAtom,
  atomToSolfeggio
} from './chakra_engine.js';

// 🔮 Géométrie Sacrée & Cymatique
export {
  default as CymaticsEngine,
  PHI,
  PHI_INVERSE,
  FIBONACCI,
  SACRED_CONSTANTS,
  SACRED_GEOMETRY,
  PLATONIC_SOLIDS,
  CYMATICS_PATTERNS,
  generateFibonacci,
  isFibonacci,
  calculateGoldenRatio,
  isGoldenRatio,
  calculateVitalityRate,
  generateFibonacciSpiral,
  generateFlowerOfLife,
  generateMetatronsCube,
  getCymaticsForFrequency,
  getGeometryForArithmos,
  calculateGeometricSignature,
  generateCymaticAnimation
} from './cymatics_engine.js';

// ═══════════════════════════════════════════════════════════════════════════════
// MOTEUR UNIVERSEL (FUSION)
// ═══════════════════════════════════════════════════════════════════════════════

export {
  default as UniversalEngine,
  SYSTEM_CONFIG,
  RESONANCE_MATRIX,
  calculateUniversalResonance,
  useUniversalResonance,
  getDailyGreeting
} from './universal_resonance_engine.js';

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT - MOTEUR UNIVERSEL
// ═══════════════════════════════════════════════════════════════════════════════

import UniversalEngine from './universal_resonance_engine.js';
export default UniversalEngine;

// ═══════════════════════════════════════════════════════════════════════════════
// DOCUMENTATION RAPIDE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * USAGE RAPIDE:
 * 
 * ```javascript
 * import { calculateUniversalResonance, getDailyGreeting } from './engines';
 * 
 * // Analyser un mot
 * const result = calculateUniversalResonance("AMOUR");
 * console.log(result.arithmos.frequency);  // 666 Hz
 * console.log(result.maya.signature);      // "7 Kan" (par exemple)
 * console.log(result.chakra.name);         // "Anahata"
 * 
 * // Salutation du jour
 * const greeting = getDailyGreeting();
 * console.log(greeting.text);
 * ```
 * 
 * SYSTÈMES DISPONIBLES:
 * 
 * 1. ARITHMOS (Pythagoricien)
 *    - Réduction numérique 1-9
 *    - Fréquences 111-999 Hz
 * 
 * 2. TZOLKIN (Maya)
 *    - 13 Tons de la Création
 *    - 20 Nawals (Glyphes)
 *    - Cycle de 260 jours
 * 
 * 3. YI-KING (Chinois)
 *    - 8 Trigrammes
 *    - 64 Hexagrammes
 *    - Prédiction des transformations
 * 
 * 4. KABBALE (Hébraïque)
 *    - 10 Sephiroth
 *    - 22 Sentiers
 *    - 3 Piliers
 *    - 4 Mondes
 * 
 * 5. CHAKRAS (Indien)
 *    - 7 Centres principaux
 *    - 3 Nadis
 *    - Fréquences Solfège
 * 
 * 6. CYMATIQUE (Universel)
 *    - Nombre d'Or (φ)
 *    - Suite de Fibonacci
 *    - Géométrie Sacrée
 *    - Solides de Platon
 */
