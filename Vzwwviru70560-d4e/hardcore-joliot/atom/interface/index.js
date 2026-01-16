/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM INTERFACE — INDEX
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Point d'entrée pour tous les composants d'interface AT·OM.
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// Composant principal
export { default as UniversalResonanceInterface } from './UniversalResonanceInterface';

// Hook universel
export { 
  default as useUniversalResonance,
  SYSTEM_CONFIG,
  ARITHMOS_MAP,
  RESONANCE_MATRIX,
  NAWALS,
  TONS,
  CHAKRAS,
  SEPHIROTH,
  PHI,
  FIBONACCI,
  sanitize,
  calculateArithmos,
  calculateMayaKin,
  getChakraForArithmos,
  getSephirahForArithmos
} from './useUniversalResonance';

// Export par défaut
export { default } from './UniversalResonanceInterface';
