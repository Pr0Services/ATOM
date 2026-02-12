/**
 * AT·OM — useThreatMonitor
 * Hook React pour consommer l'etat de la ThreatAmygdala
 *
 * "L'amygdale alerte tout l'organisme — le hook alerte tout le UI."
 *
 * Expose :
 *   - alertLevel        → CALM / VIGILANT / ALERT / LOCKDOWN
 *   - alertScore        → 0-100 (score numerique precis)
 *   - alertColor        → Couleur associee au niveau d'alerte
 *   - activeThreats     → Menaces actives non-expirees
 *   - isQuarantined     → true si LOCKDOWN
 *   - isCalm            → true si CALM
 *   - scanContent(text) → Scanner manuellement du contenu
 *   - scanTransaction() → Scanner manuellement une transaction
 *   - memory            → Memoire des menaces
 *   - timeline          → Timeline forensique
 *   - sensitivity       → Sensibilite courante (0-1)
 *   - resetAlert()      → Force retour a CALM
 */

import { useMemo, useCallback } from 'react';
import { useATOM } from '../context/GlobalStateContext';
import type { ThreatSignal, ThreatMemory, AlertLevel } from '../types/atom-types';

// ═══════════════════════════════════════════════════════════
// HOOK
// ═══════════════════════════════════════════════════════════

export function useThreatMonitor() {
  const { amygdala, state } = useATOM();

  // ── Niveaux d'alerte ──────────────────────────────────

  /** Niveau d'alerte courant (CALM / VIGILANT / ALERT / LOCKDOWN) */
  const alertLevel = useMemo(
    (): AlertLevel => state.threats.alert_level,
    [state.threats.alert_level],
  );

  /** Score numerique 0-100 */
  const alertScore = useMemo(
    () => state.threats.alert_score,
    [state.threats.alert_score],
  );

  /** Menaces actives (non-expirees) */
  const activeThreats = useMemo(
    (): ThreatSignal[] => state.threats.active_threats,
    [state.threats.active_threats],
  );

  // ── Couleur d'alerte (pour l'UI) ─────────────────────

  const alertColor = useMemo((): string => {
    switch (alertLevel) {
      case 'CALM':     return '#2ECC40'; // Vert — tout va bien
      case 'VIGILANT': return '#D4AF37'; // Or — attention
      case 'ALERT':    return '#FF851B'; // Orange — menace confirmee
      case 'LOCKDOWN': return '#E74C3C'; // Rouge — quarantaine
    }
  }, [alertLevel]);

  /** Icone d'alerte */
  const alertIcon = useMemo((): string => {
    switch (alertLevel) {
      case 'CALM':     return '🟢';
      case 'VIGILANT': return '🟡';
      case 'ALERT':    return '🟠';
      case 'LOCKDOWN': return '🔴';
    }
  }, [alertLevel]);

  // ── Scan manuel ───────────────────────────────────────

  /** Scanner du contenu texte (ex: avant publication) */
  const scanContent = useCallback(
    (text: string, source?: string): ThreatSignal | null =>
      amygdala.scan({ type: 'intention', data: { text }, source }),
    [amygdala],
  );

  /** Scanner une transaction (ex: transfert UR) */
  const scanTransaction = useCallback(
    (tx: unknown, source?: string): ThreatSignal | null =>
      amygdala.scan({ type: 'transaction', data: tx, source }),
    [amygdala],
  );

  /** Scanner une frequence */
  const scanFrequency = useCallback(
    (frequency: number, source?: string): ThreatSignal | null =>
      amygdala.scan({ type: 'frequency', data: { frequency }, source }),
    [amygdala],
  );

  // ── Memoire & Timeline ────────────────────────────────

  /** Memoire des menaces (buffer circulaire) */
  const memory = useMemo(
    (): ThreatMemory => amygdala.getMemory(),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [amygdala, state.threats.active_threats],
  );

  /** Timeline forensique — tous les signaux recents */
  const timeline = useMemo(
    (): ThreatSignal[] => amygdala.getThreatTimeline(),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [amygdala, state.threats.active_threats],
  );

  // ── Controle ──────────────────────────────────────────

  /** Force retour a CALM (action administrative) */
  const resetAlert = useCallback(
    () => amygdala.resetAlert(),
    [amygdala],
  );

  // ── Return ────────────────────────────────────────────

  return {
    // Etat
    alertLevel,
    alertScore,
    alertColor,
    alertIcon,
    activeThreats,
    isQuarantined: alertLevel === 'LOCKDOWN',
    isCalm: alertLevel === 'CALM',

    // Scan manuel
    scanContent,
    scanTransaction,
    scanFrequency,

    // Memoire & forensique
    memory,
    timeline,
    sensitivity: memory.sensitivity,
    threatCount: memory.recent_signals.length,

    // Controle
    resetAlert,
  };
}
