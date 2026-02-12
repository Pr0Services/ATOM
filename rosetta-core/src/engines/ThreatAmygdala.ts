/**
 * AT·OM — ThreatAmygdala
 * Sentinelle Pre-Corticale — Systeme d'alerte rapide inspire de l'amygdale cerebrale
 *
 * "L'amygdale ne reflechit pas — elle reconnait."
 *
 * L'amygdale cerebrale traite les menaces AVANT l'analyse consciente.
 * De meme, la ThreatAmygdala scanne chaque operation AVANT le pipeline
 * Rosetta (PolishingEngine, QuantumCorrector).
 *
 * Double voie (comme le cerveau humain) :
 *
 *   FAST PATH (thalamus → amygdale) — 5 checks legers, ~1ms
 *     1. frequencyCheck     → Frequence hors range [44.4 – 1728] ?
 *     2. hashQuickCheck     → integrity_hash mismatch ?
 *     3. dimensionBalance   → Dimension vide/nulle ?
 *     4. spikeDetection     → Delta > 300Hz soudain ?
 *     5. repetitionCheck    → Meme input repete > 3x en 10s ?
 *
 *   DEEP PATH (thalamus → cortex → amygdale) — quand Fast detecte
 *     1. InformationFilter  → Intention MANIPULATIF / DIVISIF ?
 *     2. IntentionGuard     → Verdict EXTRAIRE ?
 *     3. Sovereignty check  → 7 principes immuables violes ?
 *     4. Memory cross-ref   → Pattern recurrent ?
 *     5. Cascade detection  → 3+ signaux en 5s ?
 *
 * Reponse graduee :
 *   CALM (0-25) → VIGILANT (26-50) → ALERT (51-75) → LOCKDOWN (76-100)
 *
 * Memoire adaptative :
 *   Buffer circulaire de 50 signaux, sensibilite auto-ajustee, decay naturel
 */

import type {
  RosettaTranslation,
  ThreatType,
  AlertLevel,
  ThreatSignal,
  ThreatMemory,
  AmygdalaState,
  AmygdalaEvent,
  TechPayload,
  PeoplePayload,
  SpiritPayload,
} from '../types/atom-types';
import { SACRED_FREQUENCIES } from '../types/atom-types';
import { RosettaParser } from '../parser/RosettaParser';
import { InformationFilter, IntentionGuard } from './PolishingEngine';

// ═══════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════

/** Taille maximale du buffer memoire (signaux recents) */
const MAX_MEMORY_SIZE = 50;

/** Seuils de frequence valides */
const FREQ_MIN = SACRED_FREQUENCIES.ATOM_M;   // 44.4
const FREQ_MAX = SACRED_FREQUENCIES.ATOM_PO;  // 1728

/** Delta max de frequence avant detection de spike (Hz) */
const SPIKE_THRESHOLD = 300;

/** Nombre max de repetitions avant detection */
const REPETITION_MAX = 3;

/** Fenetre de repetition en ms (10 secondes) */
const REPETITION_WINDOW = 10_000;

/** Fenetre de cascade en ms (5 secondes) */
const CASCADE_WINDOW = 5_000;

/** Nombre de signaux pour declencher une cascade */
const CASCADE_THRESHOLD = 3;

/** Decay de l'alert_score par minute (en points) */
const DECAY_PER_MINUTE = 5;

/** Sensibilite initiale (0-1) */
const DEFAULT_SENSITIVITY = 0.5;

// ═══════════════════════════════════════════════════════════
// SCAN CONTEXT — Re-export depuis atom-types pour backward compat
// ═══════════════════════════════════════════════════════════

export type { ScanContext } from '../types/atom-types';

// ═══════════════════════════════════════════════════════════
// THREAT AMYGDALA
// ═══════════════════════════════════════════════════════════

export class ThreatAmygdala {
  private parser: RosettaParser;
  private memory: ThreatMemory;
  private alertScore: number = 0;
  private activeThreats: ThreatSignal[] = [];
  private listeners: ((event: AmygdalaEvent) => void)[] = [];
  private lastFrequency: number = SACRED_FREQUENCIES.HEARTBEAT;
  private lastScan: number = Date.now();
  private isScanning: boolean = false;

  /** Buffer pour la detection de repetitions (hash → timestamps[]) */
  private repetitionBuffer: Map<string, number[]> = new Map();

  constructor(parser: RosettaParser) {
    this.parser = parser;
    this.memory = this.createEmptyMemory();
  }

  // ─── SCAN PRINCIPAL ─────────────────────────────────────

  /**
   * Point d'entree principal — scanne un contexte pour detecter les menaces.
   * Toujours Fast Path d'abord, puis Deep Path si Fast detecte.
   */
  scan(context: ScanContext): ThreatSignal | null {
    this.isScanning = true;
    this.lastScan = Date.now();

    // Decay naturel : reduire l'alert_score selon le temps ecoule
    this.applyDecay();

    // ── FAST PATH : 5 checks legers ──
    const fastSignal = this.fastPath(context);

    if (fastSignal) {
      // ── DEEP PATH : analyse detaillee (si fast a detecte) ──
      const deepSignal = this.deepPath(context, fastSignal);

      // Le signal le plus severe gagne
      const finalSignal = deepSignal && deepSignal.severity > fastSignal.severity
        ? deepSignal
        : fastSignal;

      this.registerThreat(finalSignal);
      this.isScanning = false;
      return finalSignal;
    }

    // Si on est deja en VIGILANT+, faire le deep path meme sans fast detection
    if (this.getAlertLevel() !== 'CALM') {
      const deepSignal = this.deepPath(context, null);
      if (deepSignal) {
        this.registerThreat(deepSignal);
        this.isScanning = false;
        return deepSignal;
      }
    }

    this.isScanning = false;
    return null;
  }

  // ═══════════════════════════════════════════════════════════
  // FAST PATH — 5 checks legers (~1ms)
  // ═══════════════════════════════════════════════════════════

  private fastPath(context: ScanContext): ThreatSignal | null {
    const data = context.data as Record<string, unknown>;

    // 1. Frequency check
    if (context.type === 'frequency' || context.type === 'translation') {
      const freq = this.extractFrequency(data);
      if (freq !== null) {
        const freqSignal = this.frequencyCheck(freq);
        if (freqSignal) return freqSignal;

        const spikeSignal = this.spikeDetection(freq);
        if (spikeSignal) return spikeSignal;

        // Mettre a jour la derniere frequence connue
        this.lastFrequency = freq;
      }
    }

    // 2. Hash integrity check (translations only)
    if (context.type === 'translation' && this.isRosettaTranslation(data)) {
      const hashSignal = this.hashQuickCheck(data as RosettaTranslation);
      if (hashSignal) return hashSignal;

      // 3. Dimension balance check
      const translation = data as RosettaTranslation;
      const balanceSignal = this.dimensionBalanceCheck(
        translation.tech,
        translation.people,
        translation.spirit,
      );
      if (balanceSignal) return balanceSignal;
    }

    // 5. Repetition check (all types)
    const repSignal = this.repetitionCheck(context);
    if (repSignal) return repSignal;

    return null;
  }

  /** Check 1 : Frequence hors range sacre */
  private frequencyCheck(freq: number): ThreatSignal | null {
    if (freq < FREQ_MIN || freq > FREQ_MAX) {
      return this.createSignal(
        'frequency_anomaly',
        40 + Math.min(30, Math.abs(freq - SACRED_FREQUENCIES.HEARTBEAT) / 10),
        'fast',
        `Frequence ${freq}Hz hors range [${FREQ_MIN}-${FREQ_MAX}]`,
        'VibrationalMotor',
      );
    }
    return null;
  }

  /** Check 2 : Hash d'integrite corrompu */
  private hashQuickCheck(translation: RosettaTranslation): ThreatSignal | null {
    const recalculated = RosettaParser.computeCombinedHash(
      translation.tech,
      translation.people,
      translation.spirit,
    );
    if (recalculated !== translation.integrity_hash) {
      return this.createSignal(
        'integrity_breach',
        65,
        'fast',
        `Hash mismatch: attendu ${translation.integrity_hash}, recalcule ${recalculated}`,
        'RosettaParser',
      );
    }
    return null;
  }

  /** Check 3 : Une dimension vide ou nulle */
  private dimensionBalanceCheck(
    tech: TechPayload,
    people: PeoplePayload,
    spirit: SpiritPayload,
  ): ThreatSignal | null {
    const missing: string[] = [];

    if (!tech || !tech.data_type) missing.push('TECH');
    if (!people || !people.narrative) missing.push('PEOPLE');
    if (!spirit || !spirit.frequency_hz) missing.push('SPIRIT');

    if (missing.length > 0) {
      return this.createSignal(
        'integrity_breach',
        30 + missing.length * 20,
        'fast',
        `Dimension(s) manquante(s): ${missing.join(', ')}`,
        'RosettaParser',
      );
    }
    return null;
  }

  /** Check 4 : Spike de frequence soudain */
  private spikeDetection(freq: number): ThreatSignal | null {
    const delta = Math.abs(freq - this.lastFrequency);
    if (delta > SPIKE_THRESHOLD) {
      return this.createSignal(
        'frequency_anomaly',
        35 + Math.min(40, delta / 10),
        'fast',
        `Spike detecte: delta ${delta}Hz (${this.lastFrequency}→${freq})`,
        'VibrationalMotor',
      );
    }
    return null;
  }

  /** Check 5 : Repetition suspecte (meme input > 3x en 10s) */
  private repetitionCheck(context: ScanContext): ThreatSignal | null {
    const key = this.hashInput(context);
    const now = Date.now();

    // Recuperer les timestamps existants pour cette cle
    const timestamps = this.repetitionBuffer.get(key) ?? [];
    // Filtrer ceux dans la fenetre
    const recent = timestamps.filter(t => now - t < REPETITION_WINDOW);
    recent.push(now);

    // Mettre a jour le buffer
    this.repetitionBuffer.set(key, recent);

    // Nettoyer les vieilles entrees (max 100 cles)
    if (this.repetitionBuffer.size > 100) {
      const firstKey = this.repetitionBuffer.keys().next().value;
      if (firstKey !== undefined) {
        this.repetitionBuffer.delete(firstKey);
      }
    }

    if (recent.length > REPETITION_MAX) {
      return this.createSignal(
        'cascade_risk',
        25 + recent.length * 5,
        'fast',
        `Input repete ${recent.length}x en ${REPETITION_WINDOW / 1000}s`,
        context.source ?? 'Unknown',
      );
    }
    return null;
  }

  // ═══════════════════════════════════════════════════════════
  // DEEP PATH — Analyse detaillee (quand Fast detecte)
  // ═══════════════════════════════════════════════════════════

  private deepPath(context: ScanContext, _fastSignal: ThreatSignal | null): ThreatSignal | null {
    const data = context.data as Record<string, unknown>;

    // 1. Analyse de manipulation (texte)
    const text = this.extractText(data);
    if (text) {
      const manipSignal = this.analyzeManipulation(text);
      if (manipSignal) return manipSignal;
    }

    // 2. Analyse d'extraction (intention)
    if (context.type === 'intention' || context.type === 'governance') {
      const description = text ?? String(data?.description ?? '');
      if (description) {
        const extractSignal = this.analyzeExtraction(description);
        if (extractSignal) return extractSignal;

        // 3. Verification de souverainete
        const sovSignal = this.analyzeSovereignty(description);
        if (sovSignal) return sovSignal;
      }
    }

    // 4. Detection de cascade (signaux correles)
    const cascadeSignal = this.detectCascade();
    if (cascadeSignal) return cascadeSignal;

    return null;
  }

  /** Deep 1 : Contenu MANIPULATIF / DIVISIF */
  private analyzeManipulation(text: string): ThreatSignal | null {
    const intention = InformationFilter.detectIntention(text);

    if (intention === 'MANIPULATIF') {
      return this.createSignal(
        'manipulation_detected',
        60,
        'deep',
        `Contenu detecte comme MANIPULATIF`,
        'InformationFilter',
      );
    }

    if (intention === 'DIVISIF') {
      return this.createSignal(
        'manipulation_detected',
        70,
        'deep',
        `Contenu detecte comme DIVISIF`,
        'InformationFilter',
      );
    }

    return null;
  }

  /** Deep 2 : Verdict EXTRAIRE */
  private analyzeExtraction(description: string): ThreatSignal | null {
    const check = IntentionGuard.evaluate({ description });

    if (check.verdict === 'EXTRAIRE') {
      // Compter les criteres echoues pour la severite
      const failedCriteria = [
        !check.sert_epanouissement && 'epanouissement',
        !check.respecte_souverainete && 'souverainete',
        !check.est_transparent && 'transparence',
        !check.cree_plus_de_valeur && 'valeur',
        !check.aligne_9_spheres && 'spheres',
        !check.visible_par_tous && 'visibilite',
      ].filter(Boolean) as string[];

      return this.createSignal(
        'extraction_attempt',
        50 + failedCriteria.length * 5,
        'deep',
        `Intention EXTRAIRE detectee — criteres echoues: ${failedCriteria.join(', ')}`,
        'IntentionGuard',
      );
    }
    return null;
  }

  /** Deep 3 : Violation des 7 principes immuables */
  private analyzeSovereignty(description: string): ThreatSignal | null {
    const { respects, violations } = IntentionGuard.checkPrinciples(description);

    if (!respects) {
      return this.createSignal(
        'sovereignty_violation',
        55 + violations.length * 10,
        'deep',
        violations.join(' | '),
        'IntentionGuard',
      );
    }
    return null;
  }

  /** Deep 4+5 : Detection de cascade (3+ signaux en 5s) */
  private detectCascade(): ThreatSignal | null {
    const now = Date.now();
    const recentThreats = this.memory.recent_signals.filter(
      s => now - s.timestamp < CASCADE_WINDOW,
    );

    if (recentThreats.length >= CASCADE_THRESHOLD) {
      // Verifier la diversite des types (pas juste des repetitions)
      const uniqueTypes = new Set(recentThreats.map(s => s.type));
      if (uniqueTypes.size >= 2) {
        return this.createSignal(
          'cascade_risk',
          70 + recentThreats.length * 3,
          'deep',
          `Cascade: ${recentThreats.length} signaux de ${uniqueTypes.size} types en ${CASCADE_WINDOW / 1000}s`,
          'ThreatAmygdala',
        );
      }
    }
    return null;
  }

  // ═══════════════════════════════════════════════════════════
  // ETAT & MEMOIRE
  // ═══════════════════════════════════════════════════════════

  /** Retourne l'etat complet de l'amygdale */
  getState(): AmygdalaState {
    return {
      alert_level: this.getAlertLevel(),
      alert_score: this.alertScore,
      active_threats: [...this.activeThreats],
      memory: this.getMemory(),
      is_scanning: this.isScanning,
      last_scan: this.lastScan,
    };
  }

  /** Niveau d'alerte courant */
  getAlertLevel(): AlertLevel {
    if (this.alertScore >= 76) return 'LOCKDOWN';
    if (this.alertScore >= 51) return 'ALERT';
    if (this.alertScore >= 26) return 'VIGILANT';
    return 'CALM';
  }

  /** Score d'alerte brut (0-100) */
  getAlertScore(): number {
    return this.alertScore;
  }

  /** Copie de la memoire */
  getMemory(): ThreatMemory {
    return {
      recent_signals: [...this.memory.recent_signals],
      threat_frequency: { ...this.memory.threat_frequency },
      sensitivity: this.memory.sensitivity,
      last_lockdown: this.memory.last_lockdown,
    };
  }

  /** Timeline forensique des signaux */
  getThreatTimeline(): ThreatSignal[] {
    return [...this.memory.recent_signals];
  }

  // ═══════════════════════════════════════════════════════════
  // EVENEMENTS (meme pattern que VibrationalMotor)
  // ═══════════════════════════════════════════════════════════

  /** S'abonner aux evenements de menace */
  onThreat(listener: (event: AmygdalaEvent) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  /** Notifier tous les abonnes */
  private notifyListeners(event: AmygdalaEvent): void {
    for (const listener of this.listeners) {
      listener(event);
    }
  }

  // ═══════════════════════════════════════════════════════════
  // CONTROLE
  // ═══════════════════════════════════════════════════════════

  /** Force retour a CALM (action administrative) */
  resetAlert(): void {
    const previousLevel = this.getAlertLevel();
    this.alertScore = 0;
    this.activeThreats = [];

    if (previousLevel !== 'CALM') {
      this.notifyListeners({
        type: 'all_clear',
        previous_level: previousLevel,
        new_level: 'CALM',
      });
    }
  }

  /** Ajuste la sensibilite (±delta, clamp 0.1-1.0) */
  adjustSensitivity(delta: number): void {
    this.memory.sensitivity = Math.max(0.1, Math.min(1.0,
      this.memory.sensitivity + delta,
    ));
  }

  // ═══════════════════════════════════════════════════════════
  // INTERNALS
  // ═══════════════════════════════════════════════════════════

  /** Enregistre un signal dans la memoire et met a jour l'etat */
  private registerThreat(signal: ThreatSignal): void {
    const previousLevel = this.getAlertLevel();

    // Ajouter aux menaces actives
    this.activeThreats.push(signal);

    // Nettoyer les menaces > 60s
    const now = Date.now();
    this.activeThreats = this.activeThreats.filter(t => now - t.timestamp < 60_000);

    // Ajouter a la memoire (buffer circulaire)
    this.memory.recent_signals.push(signal);
    if (this.memory.recent_signals.length > MAX_MEMORY_SIZE) {
      this.memory.recent_signals.shift();
    }

    // Mettre a jour les compteurs par type
    this.memory.threat_frequency[signal.type] =
      (this.memory.threat_frequency[signal.type] ?? 0) + 1;

    // Calculer le nouveau score (sensibilite-ponderee)
    const severityWeighted = signal.severity * this.memory.sensitivity;
    this.alertScore = Math.min(100, this.alertScore + severityWeighted * 0.4);

    // Adapter la sensibilite (plus de menaces → plus sensible)
    const recentCount = this.memory.recent_signals.filter(
      s => now - s.timestamp < 30_000,
    ).length;
    if (recentCount >= 3) {
      this.memory.sensitivity = Math.min(1.0, this.memory.sensitivity + 0.05);
    }

    const newLevel = this.getAlertLevel();

    // Emettre evenements
    this.notifyListeners({
      type: 'threat_detected',
      signal,
    });

    // Transition de niveau ?
    if (newLevel !== previousLevel) {
      this.notifyListeners({
        type: newLevel === 'LOCKDOWN' ? 'lockdown_engaged' : 'alert_changed',
        previous_level: previousLevel,
        new_level: newLevel,
      });

      if (newLevel === 'LOCKDOWN') {
        this.memory.last_lockdown = now;
      }
    }
  }

  /** Applique le decay naturel de l'alert_score */
  private applyDecay(): void {
    const now = Date.now();
    const elapsed = now - this.lastScan;
    const minutesElapsed = elapsed / 60_000;

    if (minutesElapsed > 0 && this.alertScore > 0) {
      const previousLevel = this.getAlertLevel();
      this.alertScore = Math.max(0, this.alertScore - DECAY_PER_MINUTE * minutesElapsed);

      const newLevel = this.getAlertLevel();
      if (newLevel !== previousLevel) {
        this.notifyListeners({
          type: newLevel === 'CALM' ? 'all_clear' : 'alert_changed',
          previous_level: previousLevel,
          new_level: newLevel,
        });
      }

      // Reduire la sensibilite graduellement en periode calme
      if (this.alertScore === 0 && this.memory.sensitivity > DEFAULT_SENSITIVITY) {
        this.memory.sensitivity = Math.max(
          DEFAULT_SENSITIVITY,
          this.memory.sensitivity - 0.01 * minutesElapsed,
        );
      }
    }
  }

  /** Cree un signal de menace */
  private createSignal(
    type: ThreatType,
    rawSeverity: number,
    pathway: 'fast' | 'deep',
    evidence: string,
    source: string,
  ): ThreatSignal {
    // Clamp severity 0-100
    const severity = Math.max(0, Math.min(100, Math.round(rawSeverity)));

    return {
      id: `threat_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 6)}`,
      type,
      severity,
      alert_level: this.severityToLevel(severity),
      source,
      timestamp: Date.now(),
      evidence: [evidence],
      pathway,
    };
  }

  /** Mappe une severite numerique a un AlertLevel */
  private severityToLevel(severity: number): AlertLevel {
    if (severity >= 76) return 'LOCKDOWN';
    if (severity >= 51) return 'ALERT';
    if (severity >= 26) return 'VIGILANT';
    return 'CALM';
  }

  /** Cree une memoire vide */
  private createEmptyMemory(): ThreatMemory {
    return {
      recent_signals: [],
      threat_frequency: {
        frequency_anomaly: 0,
        manipulation_detected: 0,
        extraction_attempt: 0,
        integrity_breach: 0,
        cascade_risk: 0,
        sovereignty_violation: 0,
      },
      sensitivity: DEFAULT_SENSITIVITY,
      last_lockdown: null,
    };
  }

  /** Extrait la frequence d'un contexte de donnees */
  private extractFrequency(data: Record<string, unknown>): number | null {
    // Translation
    if (data && typeof data === 'object') {
      const spirit = data.spirit as Record<string, unknown> | undefined;
      if (spirit?.frequency_hz && typeof spirit.frequency_hz === 'number') {
        return spirit.frequency_hz;
      }
      // Direct frequency value
      if (typeof data.frequency === 'number') return data.frequency;
      if (typeof data.frequency_hz === 'number') return data.frequency_hz;
    }
    return null;
  }

  /** Extrait le texte d'un contexte de donnees */
  private extractText(data: Record<string, unknown>): string | null {
    if (!data || typeof data !== 'object') return null;

    // Texte direct
    if (typeof data.text === 'string') return data.text;
    if (typeof data.description === 'string') return data.description;

    // Narrative depuis people
    const people = data.people as Record<string, unknown> | undefined;
    if (people?.narrative && typeof people.narrative === 'string') {
      return people.narrative;
    }

    return null;
  }

  /** Verifie si un objet est une RosettaTranslation */
  private isRosettaTranslation(data: unknown): boolean {
    if (!data || typeof data !== 'object') return false;
    const d = data as Record<string, unknown>;
    return !!d.tech && !!d.people && !!d.spirit && typeof d.integrity_hash === 'string';
  }

  /** Hash rapide d'un input pour la detection de repetitions */
  private hashInput(context: ScanContext): string {
    const content = JSON.stringify({ type: context.type, data: context.data });
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0;
    }
    return `rep_${Math.abs(hash).toString(36)}`;
  }
}
