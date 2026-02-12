/**
 * AT·OM — VibrationalMotor
 * Moteur de Résonance Géolocalisé
 *
 * Calcule la distance entre l'utilisateur et le Point Zéro (Cratère de Chicxulub).
 * Ajuste dynamiquement la fréquence du système :
 *   - Dans le cratère (< 100km) → 999Hz (Source)
 *   - Hors cratère              → 444Hz (Heartbeat)
 *
 * Template Engine : Ce moteur est réutilisable pour tout calcul
 * basé sur la proximité géographique d'un point d'ancrage.
 */

import {
  type GeoPosition,
  type VibrationalState,
  type ResonanceLevel,
  type SystemPhase,
  type ResonanceScoreWeights,
  type ResonanceRank,
  type ForgeStep,
  type DiamondFacet,
  SACRED_FREQUENCIES,
  RESONANCE_MATRIX,
  POINT_ZERO,
  VIBRATIONAL_DELAY,
  SYSTEM_PHASES,
  DEFAULT_RESONANCE_WEIGHTS,
  RESONANCE_RANKS,
  FORGE_STEPS,
  DIAMOND_FACETS,
} from '../types/atom-types';

// ═══════════════════════════════════════════════════════════
// INTERFACE TEMPLATE (réutilisable)
// ═══════════════════════════════════════════════════════════

export interface AnchorPoint {
  latitude: number;
  longitude: number;
  name: string;
  activation_radius_km: number;
  activated_frequency: number;
  default_frequency: number;
}

// ═══════════════════════════════════════════════════════════
// VIBRATIONAL MOTOR
// ═══════════════════════════════════════════════════════════

export class VibrationalMotor {
  private state: VibrationalState;
  private anchor: AnchorPoint;
  private listeners: ((state: VibrationalState) => void)[] = [];

  constructor(anchor?: AnchorPoint) {
    this.anchor = anchor ?? {
      latitude: POINT_ZERO.latitude,
      longitude: POINT_ZERO.longitude,
      name: POINT_ZERO.name,
      activation_radius_km: POINT_ZERO.activationRadius_km,
      activated_frequency: SACRED_FREQUENCIES.SOURCE,    // 999Hz
      default_frequency: SACRED_FREQUENCIES.HEARTBEAT,   // 444Hz
    };

    this.state = {
      system_resonance: this.anchor.default_frequency,
      user_position: null,
      distance_to_zero: Infinity,
      is_in_crater: false,
      mode: 'standard',
      last_sync: Date.now(),
    };
  }

  // ─── Position Update ───────────────────────────────────

  /**
   * Met à jour la position de l'utilisateur et recalcule la résonance.
   * C'est l'opération principale — appelée à chaque changement GPS.
   */
  updatePosition(position: GeoPosition): VibrationalState {
    this.state.user_position = position;
    this.state.distance_to_zero = VibrationalMotor.haversine(
      position.latitude,
      position.longitude,
      this.anchor.latitude,
      this.anchor.longitude,
    );

    const wasInCrater = this.state.is_in_crater;
    this.state.is_in_crater = this.state.distance_to_zero <= this.anchor.activation_radius_km;

    // Ajustement dynamique de la fréquence
    if (this.state.is_in_crater) {
      this.state.system_resonance = this.anchor.activated_frequency;
      this.state.mode = 'activated';
    } else {
      // Dégradé progressif basé sur la distance
      this.state.system_resonance = this.computeGradientFrequency(
        this.state.distance_to_zero,
      );
      this.state.mode = 'standard';
    }

    this.state.last_sync = Date.now();

    // Notification si changement de zone
    if (wasInCrater !== this.state.is_in_crater) {
      this.notifyListeners();
    }

    return this.getState();
  }

  // ─── Frequency Computation ─────────────────────────────

  /**
   * Calcule la fréquence par dégradé en fonction de la distance.
   * Plus on s'éloigne du Point Zéro, plus la fréquence descend
   * jusqu'au HEARTBEAT (444Hz).
   *
   * Utilise le nombre d'or (Phi) pour la courbe de dégradé.
   */
  private computeGradientFrequency(distance_km: number): number {
    const { activation_radius_km, activated_frequency, default_frequency } = this.anchor;

    if (distance_km <= activation_radius_km) {
      return activated_frequency;
    }

    // Dégradé logarithmique basé sur Phi
    const ratio = Math.log(activation_radius_km / distance_km) / Math.log(1 / SACRED_FREQUENCIES.PHI);
    const normalized = Math.max(0, Math.min(1, 1 + ratio));
    const freq = default_frequency + (activated_frequency - default_frequency) * normalized;

    // Arrondir au niveau de résonance le plus proche (111, 222, ..., 999)
    return this.snapToResonance(freq);
  }

  /** Arrondit une fréquence au palier de résonance 111×n le plus proche */
  private snapToResonance(freq: number): number {
    const level = Math.round(freq / 111);
    const clamped = Math.max(1, Math.min(9, level));
    return clamped * 111;
  }

  // ─── Transaction Header ────────────────────────────────

  /**
   * Génère l'en-tête vibratoire pour une transaction réseau.
   * Chaque transaction envoyée au réseau porte la signature fréquentielle.
   */
  createTransactionHeader(): Record<string, string | number> {
    return {
      'X-ATOM-Frequency': this.state.system_resonance,
      'X-ATOM-Resonance-Level': this.getResonanceLevel(),
      'X-ATOM-Distance-Zero': Math.round(this.state.distance_to_zero),
      'X-ATOM-Crater-Active': this.state.is_in_crater ? '1' : '0',
      'X-ATOM-Mode': this.state.mode,
      'X-ATOM-Timestamp': this.state.last_sync,
      'X-ATOM-Anchor': this.anchor.name,
    };
  }

  // ─── State Getters ─────────────────────────────────────

  getState(): VibrationalState {
    return { ...this.state };
  }

  getFrequency(): number {
    return this.state.system_resonance;
  }

  getResonanceLevel(): ResonanceLevel {
    const level = Math.round(this.state.system_resonance / 111);
    return Math.max(1, Math.min(9, level)) as ResonanceLevel;
  }

  getResonanceInfo() {
    const level = this.getResonanceLevel();
    return RESONANCE_MATRIX[level];
  }

  isInCrater(): boolean {
    return this.state.is_in_crater;
  }

  getDistanceToZero(): number {
    return this.state.distance_to_zero;
  }

  // ─── Mode Control ──────────────────────────────────────

  setMode(mode: VibrationalState['mode']): void {
    this.state.mode = mode;
    if (mode === 'genesis') {
      this.state.system_resonance = SACRED_FREQUENCIES.SOURCE;
    }
    this.notifyListeners();
  }

  // ─── Event System ──────────────────────────────────────

  onStateChange(listener: (state: VibrationalState) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  private notifyListeners(): void {
    const state = this.getState();
    for (const listener of this.listeners) {
      listener(state);
    }
  }

  // ─── Haversine (Distance Géographique) ─────────────────

  /**
   * Formule de Haversine — calcule la distance en km entre deux points GPS.
   * Utilisée pour mesurer la distance au Point Zéro (Chicxulub).
   */
  static haversine(
    lat1: number,
    lon1: number,
    lat2: number,
    lon2: number,
  ): number {
    const R = 6371; // Rayon de la Terre en km
    const dLat = VibrationalMotor.toRad(lat2 - lat1);
    const dLon = VibrationalMotor.toRad(lon2 - lon1);

    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(VibrationalMotor.toRad(lat1)) *
      Math.cos(VibrationalMotor.toRad(lat2)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  private static toRad(deg: number): number {
    return deg * (Math.PI / 180);
  }

  // ─── Delay Vibratoire ─────────────────────────────────

  /** Delay vibratoire : temps de réponse en ms selon la fréquence actuelle */
  getVibrationalDelay(): number {
    const level = this.getResonanceLevel();
    return VIBRATIONAL_DELAY[level];
  }

  // ─── System Phase Detection ───────────────────────────

  /** Détecte la phase du système (ACTUEL/TRANSITION/OPTIMAL) basée sur la fréquence */
  getSystemPhase(): SystemPhase {
    const freq = this.state.system_resonance;
    if (freq >= 777) return 'OPTIMAL';
    if (freq >= 444) return 'TRANSITION';
    return 'ACTUEL';
  }

  /** Retourne les métadonnées de la phase actuelle */
  getPhaseInfo() {
    const phase = this.getSystemPhase();
    return { phase, ...SYSTEM_PHASES[phase] };
  }

  // ─── Resonance Score ──────────────────────────────────

  /** Calcule le resonance_score d'un utilisateur (0-100) */
  static computeResonanceScore(
    components: {
      activity: number;       // 0-100
      contribution: number;   // 0-100
      tenure: number;         // 0-100
      investment: number;     // 0-100
      referral: number;       // 0-100
    },
    weights: ResonanceScoreWeights = DEFAULT_RESONANCE_WEIGHTS,
  ): number {
    return Math.min(100, Math.max(0,
      (components.activity * weights.activity) +
      (components.contribution * weights.contribution) +
      (components.tenure * weights.tenure) +
      (components.investment * weights.investment) +
      (components.referral * weights.referral)
    ));
  }

  /** Détermine le rang d'un utilisateur selon son resonance_score */
  static getRank(score: number): ResonanceRank {
    if (score >= 80) return 'ARCHITECTE';
    if (score >= 60) return 'GARDIEN';
    if (score >= 40) return 'FONDATEUR';
    if (score >= 20) return 'CITOYEN';
    return 'INITIE';
  }

  /** Retourne les droits et infos pour un rang donné */
  static getRankInfo(rank: ResonanceRank) {
    return RESONANCE_RANKS[rank];
  }

  // ─── Forge Transition ─────────────────────────────────

  /** Forge : détermine l'étape de transition active selon la fréquence */
  getForgeStep(): ForgeStep {
    const freq = this.state.system_resonance;
    if (freq >= 999) return 'HARMONISATION';
    if (freq >= 666) return 'ELEVATION';
    if (freq >= 555) return 'TRANSMUTATION';
    if (freq >= 444) return 'EXTRACTION';
    return 'CONSERVATION';
  }

  // ─── Diamond Facet Progress ───────────────────────────

  /** Retourne le score de résonance global du diamant (moyenne pondérée des facettes) */
  static getDiamondResonance(): { score: number; facets: Record<DiamondFacet, number> } {
    const facets = {} as Record<DiamondFacet, number>;
    let total = 0;
    let count = 0;
    for (const [key, val] of Object.entries(DIAMOND_FACETS)) {
      const pct = val.current_pct;
      facets[key as DiamondFacet] = pct;
      total += pct;
      count++;
    }
    return { score: count > 0 ? total / count : 0, facets };
  }
}
