/**
 * AT·OM — Module d'Export Principal
 * Système de Résonance Vibrationnelle
 * 
 * @version 2.0.0 — FINAL
 * @architect Jonathan Rodrigue (999 Hz)
 */

// Hook principal
export { default as useAtomResonance } from './useAtomResonance';
export { DebugConsole } from './useAtomResonance';

// Composants
export { default as ArcheDesResonances } from './ArcheDesResonances';
export { default as CivilisationSwitch } from './CivilisationSwitch';
export { default as AtomMultiMode } from './AtomMultiMode';
export { default as GratitudeMemorial } from './GratitudeMemorial';
export { default as OracleVoiceModal } from './OracleVoiceModal';
export { default as AtomApp } from './AtomApp';

// Constants (re-exported)
export {
  SYSTEM_HEARTBEAT,
  DEBOUNCE_DELAY,
  TRANSITION_DURATION,
  ARITHMOS_MAP,
  RESONANCE_MATRIX,
  FOUNDATION_STONES,
  TRANSITION_NODES,
  sanitize,
  calculateArithmos,
  getResonance,
} from './useAtomResonance';
