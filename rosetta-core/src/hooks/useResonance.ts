/**
 * AT·OM — useResonance
 * Hook de résonance — score, rang, phase, forge, diamant
 *
 * "Chaque fréquence est un message. Chaque transition un choix."
 *
 * Expose les métriques du VibrationalMotor :
 *   - Score de résonance (0-100, 5 axes)
 *   - Rang (INITIÉ → ARCHITECTE)
 *   - Phase du système (ACTUEL → TRANSITION → OPTIMAL)
 *   - Étape de forge (CONSERVATION → HARMONISATION)
 *   - Résonance du diamant (moyenne pondérée des 6 facettes)
 *   - Delay vibratoire (temps de réponse selon la fréquence)
 */

import { useCallback, useMemo } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import { VibrationalMotor } from '../engines/VibrationalMotor';
import type {
  ResonanceRank,
  ForgeStep,
  SystemPhase,
  DiamondFacet,
} from '../types/atom-types';

export function useResonance() {
  const { state, motor } = useATOM();

  // ─── Score et rang ──────────────────────────────────────
  const resonanceScore = useMemo(() =>
    state.identity.sovereign_identity?.resonance_score ?? 0,
  [state.identity]);

  const rank = useMemo((): ResonanceRank =>
    state.identity.sovereign_identity?.rank ?? 'INITIE',
  [state.identity]);

  const rankInfo = useMemo(() =>
    VibrationalMotor.getRankInfo(rank),
  [rank]);

  // ─── Calculer un score ──────────────────────────────────
  const computeScore = useCallback((components: {
    activity: number;
    contribution: number;
    tenure: number;
    investment: number;
    referral: number;
  }) => {
    return VibrationalMotor.computeResonanceScore(components);
  }, []);

  // ─── Phase du système ───────────────────────────────────
  const systemPhase = useMemo((): SystemPhase =>
    motor.getSystemPhase(),
  [motor, state.vibrational.system_resonance]);

  const phaseInfo = useMemo(() =>
    motor.getPhaseInfo(),
  [motor, state.vibrational.system_resonance]);

  // ─── Forge ──────────────────────────────────────────────
  const forgeStep = useMemo((): ForgeStep =>
    motor.getForgeStep(),
  [motor, state.vibrational.system_resonance]);

  // ─── Diamant ────────────────────────────────────────────
  const diamondResonance = useMemo(() =>
    VibrationalMotor.getDiamondResonance(),
  []);

  // ─── Delay vibratoire ───────────────────────────────────
  const vibrationalDelay = useMemo(() =>
    motor.getVibrationalDelay(),
  [motor, state.vibrational.system_resonance]);

  // ─── Fréquence et position ──────────────────────────────
  const frequency = useMemo(() =>
    state.vibrational.system_resonance,
  [state.vibrational]);

  const resonanceLevel = useMemo(() =>
    motor.getResonanceLevel(),
  [motor, state.vibrational.system_resonance]);

  const resonanceInfo = useMemo(() =>
    motor.getResonanceInfo(),
  [motor, state.vibrational.system_resonance]);

  const isInCrater = useMemo(() =>
    state.vibrational.is_in_crater,
  [state.vibrational]);

  const distanceToZero = useMemo(() =>
    state.vibrational.distance_to_zero,
  [state.vibrational]);

  return {
    // Score et rang
    resonanceScore,
    rank,
    rankInfo,
    computeScore,

    // Phase du système
    systemPhase,
    phaseInfo,

    // Forge
    forgeStep,

    // Diamant
    diamondResonance,

    // Vibration
    frequency,
    resonanceLevel,
    resonanceInfo,
    vibrationalDelay,
    isInCrater,
    distanceToZero,
  };
}
