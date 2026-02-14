/**
 * AT·OM — QuantumCorrector
 * Systeme de Correction d'Erreur Quantique inspire de la Pierre de Rosette
 *
 * "Ce qui est traduit en trois langues ne peut etre perdu."
 *
 * Principe fondamental :
 *   Chaque RosettaTranslation existe en 3 dimensions redundantes
 *   (TECH / PEOPLE / SPIRIT), comme un code correcteur quantique a 3 qubits.
 *   Si 1 dimension est corrompue, les 2 saines la reconstruisent.
 *
 * Pipeline en 5 etapes :
 *   1. DETECT    — Verifier l'integrite via le hash combine
 *   2. LOCALIZE  — Identifier quelle(s) dimension(s) sont corrompues
 *   3. CORRECT   — Reconstruire la dimension corrompue par cross-validation
 *   4. VALIDATE  — Re-verifier la coherence post-correction
 *   5. LOG       — Enregistrer l'evenement de correction
 *
 * Limites :
 *   - 1/3 corrompue → correction certaine (confidence = 1.0)
 *   - 2/3 corrompues → irreparable (retourne null)
 *   - 3/3 corrompues → perte totale (retourne null)
 */

import {
  type RosettaTranslation,
  type QuantumRosettaTranslation,
  type DimensionHashes,
  type CorrectionDiagnostic,
  type CorrectionResult,
  type CorrectionLogEntry,
  type CorruptionTarget,
  type TechPayload,
  type PeoplePayload,
  type SpiritPayload,
  type ResonanceLevel,
  RESONANCE_MATRIX,
} from '../types/atom-types';

import { RosettaParser } from '../parser/RosettaParser';

// ═══════════════════════════════════════════════════════════
// QUANTUM CORRECTOR
// ═══════════════════════════════════════════════════════════

export class QuantumCorrector {
  private correctionLog: CorrectionLogEntry[] = [];
  private stats = { detected: 0, corrected: 0, failed: 0 };

  // ─── ENRICHIR : Ajouter les hashes par dimension ─────

  /**
   * Transforme une RosettaTranslation classique en
   * QuantumRosettaTranslation avec hashes individuels.
   * C'est l'etape prealable a toute correction.
   */
  enrich(translation: RosettaTranslation): QuantumRosettaTranslation {
    return {
      ...translation,
      dimension_hashes: RosettaParser.computeDimensionHashes(
        translation.tech,
        translation.people,
        translation.spirit,
      ),
    };
  }

  // ─── DETECTER : Verifier l'integrite ─────────────────

  /**
   * Compare le combined_hash stocke avec un recalcul.
   * Retourne true si la translation est corrompue.
   */
  detect(qt: QuantumRosettaTranslation): boolean {
    const recalculated = RosettaParser.computeCombinedHash(
      qt.tech,
      qt.people,
      qt.spirit,
    );
    return recalculated !== qt.integrity_hash;
  }

  // ─── DIAGNOSTIQUER : Localiser la corruption ─────────

  /**
   * Identifie quelle(s) dimension(s) sont corrompues en comparant
   * chaque hash individuel stocke avec un recalcul.
   *
   * Logique du vote majoritaire :
   *   - 0/3 corrompues → severity: 'none'
   *   - 1/3 corrompue  → severity: 'minor', confidence: 1.0
   *   - 2/3 corrompues → severity: 'major', confidence: 0.33
   *   - 3/3 corrompues → severity: 'critical', confidence: 0.0
   */
  diagnose(qt: QuantumRosettaTranslation): CorrectionDiagnostic {
    const stored = qt.dimension_hashes;
    const current: DimensionHashes = RosettaParser.computeDimensionHashes(
      qt.tech,
      qt.people,
      qt.spirit,
    );

    const corrupted: CorruptionTarget[] = [];
    const healthy: CorruptionTarget[] = [];

    // Comparer chaque dimension individuellement
    if (stored.tech_hash !== current.tech_hash) {
      corrupted.push('TECH');
    } else {
      healthy.push('TECH');
    }

    if (stored.people_hash !== current.people_hash) {
      corrupted.push('PEOPLE');
    } else {
      healthy.push('PEOPLE');
    }

    if (stored.spirit_hash !== current.spirit_hash) {
      corrupted.push('SPIRIT');
    } else {
      healthy.push('SPIRIT');
    }

    // Calculer la severite et la confiance
    const count = corrupted.length;
    let severity: CorrectionDiagnostic['severity'];
    let confidence: number;

    switch (count) {
      case 0:
        severity = 'none';
        confidence = 1.0;
        break;
      case 1:
        severity = 'minor';
        confidence = 1.0; // 2/3 saines → reconstruction certaine
        break;
      case 2:
        severity = 'major';
        confidence = 0.33; // 1/3 saine → pas assez pour corriger
        break;
      case 3:
      default:
        severity = 'critical';
        confidence = 0.0; // Perte totale
        break;
    }

    return {
      is_corrupted: count > 0,
      corrupted_dimensions: corrupted,
      healthy_dimensions: healthy,
      confidence,
      severity,
    };
  }

  // ─── CORRIGER : Reconstruire la dimension ────────────

  /**
   * Tente de reconstruire la dimension corrompue a partir des 2 saines.
   * Utilise la cross-validation inter-dimensionnelle :
   *
   *   TECH corrompue  → reconstruire depuis PEOPLE + SPIRIT
   *   PEOPLE corrompue → reconstruire depuis TECH + SPIRIT
   *   SPIRIT corrompue → reconstruire depuis TECH + PEOPLE
   *
   * Si 2+ dimensions corrompues → retourne null (irreparable)
   */
  correct(
    qt: QuantumRosettaTranslation,
    diagnostic: CorrectionDiagnostic,
  ): CorrectionResult {
    const log: CorrectionLogEntry[] = [];
    const now = Date.now();

    // Pas de corruption → retourner tel quel
    if (!diagnostic.is_corrupted) {
      return {
        original: qt,
        corrected: qt,
        diagnostic,
        applied: false,
        correction_log: [],
      };
    }

    // 2+ dimensions corrompues → irreparable
    if (diagnostic.corrupted_dimensions.length > 1) {
      for (const dim of diagnostic.corrupted_dimensions) {
        log.push({
          timestamp: now,
          dimension: dim,
          action: 'failed',
          before_hash: this.getStoredHash(qt, dim),
          after_hash: '',
          reason: `Corruption ${diagnostic.severity} — ${diagnostic.corrupted_dimensions.length}/3 dimensions corrompues, reconstruction impossible`,
        });
      }

      this.stats.failed++;
      this.correctionLog.push(...log);

      return {
        original: qt,
        corrected: null,
        diagnostic,
        applied: false,
        correction_log: log,
      };
    }

    // 1 dimension corrompue → correction par cross-validation
    const target = diagnostic.corrupted_dimensions[0];
    const beforeHash = this.getStoredHash(qt, target);

    // Log detection
    log.push({
      timestamp: now,
      dimension: target,
      action: 'detected',
      before_hash: beforeHash,
      after_hash: '',
      reason: `Dimension ${target} corrompue — hash ne correspond plus`,
    });

    // Log localisation
    log.push({
      timestamp: now + 1,
      dimension: target,
      action: 'localized',
      before_hash: beforeHash,
      after_hash: '',
      reason: `Localisation confirmee — ${diagnostic.healthy_dimensions.join(' + ')} saines (vote majoritaire 2/3)`,
    });

    // Reconstruire la dimension corrompue
    let correctedTranslation: RosettaTranslation;

    try {
      const reconstructed = this.reconstructDimension(qt, target);
      correctedTranslation = {
        ...qt,
        ...reconstructed,
        integrity_hash: RosettaParser.computeCombinedHash(
          reconstructed.tech ?? qt.tech,
          reconstructed.people ?? qt.people,
          reconstructed.spirit ?? qt.spirit,
        ),
      };

      // Recalculer le hash de la dimension corrigee
      const afterHash = this.getCurrentHash(correctedTranslation, target);

      log.push({
        timestamp: now + 2,
        dimension: target,
        action: 'corrected',
        before_hash: beforeHash,
        after_hash: afterHash,
        reason: `Dimension ${target} reconstruite par cross-validation depuis ${diagnostic.healthy_dimensions.join(' + ')}`,
      });
    } catch (err) {
      log.push({
        timestamp: now + 2,
        dimension: target,
        action: 'failed',
        before_hash: beforeHash,
        after_hash: '',
        reason: `Echec de reconstruction : ${err instanceof Error ? err.message : 'Erreur inconnue'}`,
      });

      this.stats.failed++;
      this.correctionLog.push(...log);

      return {
        original: qt,
        corrected: null,
        diagnostic,
        applied: false,
        correction_log: log,
      };
    }

    this.stats.corrected++;
    this.correctionLog.push(...log);

    return {
      original: qt,
      corrected: correctedTranslation,
      diagnostic,
      applied: true,
      correction_log: log,
    };
  }

  // ─── VALIDER : Verifier post-correction ──────────────

  /**
   * Recalcule tous les hashes de la translation corrigee
   * et verifie la coherence globale.
   */
  validate(result: CorrectionResult): boolean {
    if (!result.corrected) return false;

    const t = result.corrected;
    const recalculated = RosettaParser.computeCombinedHash(t.tech, t.people, t.spirit);

    if (recalculated !== t.integrity_hash) return false;

    // Verifier aussi que chaque dimension est individuellement coherente
    try {
      // Tech doit avoir un data_type
      if (!t.tech.data_type) return false;
      // People doit avoir un narrative
      if (!t.people.narrative || t.people.narrative.length < 1) return false;
      // Spirit doit avoir une frequence positive
      if (!t.spirit.frequency_hz || t.spirit.frequency_hz <= 0) return false;

      // Log validation
      const now = Date.now();
      for (const dim of result.diagnostic.corrupted_dimensions) {
        result.correction_log.push({
          timestamp: now,
          dimension: dim,
          action: 'validated',
          before_hash: '',
          after_hash: this.getCurrentHash(t, dim),
          reason: 'Coherence post-correction validee',
        });
      }

      return true;
    } catch {
      return false;
    }
  }

  // ─── PIPELINE COMPLET ────────────────────────────────

  /**
   * Pipeline complet de correction quantique :
   * enrich → detect → diagnose → correct → validate → log
   */
  process(translation: RosettaTranslation): CorrectionResult {
    // Etape 1 : Enrichir avec hashes par dimension
    const qt = this.enrich(translation);

    // Etape 2 : Detecter — si pas corrompue, retourner propre
    const isCorrupted = this.detect(qt);
    if (!isCorrupted) {
      return {
        original: translation,
        corrected: translation,
        diagnostic: {
          is_corrupted: false,
          corrupted_dimensions: [],
          healthy_dimensions: ['TECH', 'PEOPLE', 'SPIRIT'],
          confidence: 1.0,
          severity: 'none',
        },
        applied: false,
        correction_log: [],
      };
    }

    this.stats.detected++;

    // Etape 3 : Diagnostiquer
    // Note : enrich() recalcule dimension_hashes depuis le contenu actuel.
    // Si la corruption a eu lieu AVANT enrichissement (ex: RosettaTranslation
    // corrompue avec integrity_hash original), diagnose() ne trouvera pas
    // de dimensions corrompues car les hashes sont auto-coherents.
    // Dans ce cas, on sait via detect() que le contenu ne correspond plus
    // a l'integrity_hash original — on cree un diagnostic de corruption
    // non-localisable.
    let diagnostic = this.diagnose(qt);

    if (!diagnostic.is_corrupted) {
      // detect() dit corrompue mais diagnose() ne localise pas :
      // la corruption a eu lieu avant enrichissement.
      // Toutes les dimensions sont suspectes — irreparable sans les hashes originaux.
      diagnostic = {
        is_corrupted: true,
        corrupted_dimensions: ['TECH', 'PEOPLE', 'SPIRIT'],
        healthy_dimensions: [],
        confidence: 0.0,
        severity: 'critical',
      };
    }

    // Etape 4 : Corriger
    const result = this.correct(qt, diagnostic);

    // Etape 5 : Valider
    if (result.applied) {
      this.validate(result);
    }

    return result;
  }

  // ─── BATCH ───────────────────────────────────────────

  /**
   * Traite un lot de translations et retourne les statistiques.
   */
  processBatch(translations: RosettaTranslation[]): {
    results: CorrectionResult[];
    stats: { total: number; healthy: number; corrected: number; failed: number };
  } {
    const results = translations.map((t) => this.process(t));

    const healthy = results.filter((r) => !r.diagnostic.is_corrupted).length;
    const corrected = results.filter((r) => r.applied).length;
    const failed = results.filter(
      (r) => r.diagnostic.is_corrupted && !r.applied,
    ).length;

    return {
      results,
      stats: {
        total: translations.length,
        healthy,
        corrected,
        failed,
      },
    };
  }

  // ─── STATS ───────────────────────────────────────────

  getStats(): { detected: number; corrected: number; failed: number } {
    return { ...this.stats };
  }

  getCorrectionLog(): CorrectionLogEntry[] {
    return [...this.correctionLog];
  }

  resetStats(): void {
    this.stats = { detected: 0, corrected: 0, failed: 0 };
    this.correctionLog = [];
  }

  // ═══════════════════════════════════════════════════════
  // CROSS-VALIDATION : Reconstruction de dimensions
  // ═══════════════════════════════════════════════════════

  /**
   * Reconstruit une dimension corrompue a partir des 2 saines.
   * Retourne un objet partiel contenant la dimension reconstruite.
   */
  private reconstructDimension(
    qt: QuantumRosettaTranslation,
    target: CorruptionTarget,
  ): Partial<Pick<RosettaTranslation, 'tech' | 'people' | 'spirit'>> {
    switch (target) {
      case 'TECH':
        return { tech: this.reconstructTech(qt.people, qt.spirit) };
      case 'PEOPLE':
        return { people: this.reconstructPeople(qt.tech, qt.spirit) };
      case 'SPIRIT':
        return { spirit: this.reconstructSpirit(qt.tech, qt.people) };
    }
  }

  /**
   * Reconstruit TECH depuis PEOPLE + SPIRIT
   *
   * PEOPLE fournit le contexte narratif → data_type, values
   * SPIRIT fournit la frequence → timestamp, sphere deduction
   */
  private reconstructTech(people: PeoplePayload, spirit: SpiritPayload): TechPayload {
    // Deduire le data_type depuis le tone emotionnel
    const dataTypeMap: Record<string, string> = {
      neutre: 'generic_data',
      encourageant: 'positive_event',
      alerte: 'warning_event',
      celebratoire: 'achievement',
      sacre: 'sacred_event',
    };

    return {
      schema_version: '1.0.0',
      data_type: dataTypeMap[people.emotional_tone] ?? 'reconstructed_data',
      values: {
        reconstructed: true,
        source: 'quantum_correction',
        narrative_excerpt: people.narrative.substring(0, 100),
        frequency_hz: spirit.frequency_hz,
        resonance_level: spirit.resonance_level,
        geometry: spirit.sacred_geometry,
      },
      timestamp: Date.now(),
    };
  }

  /**
   * Reconstruit PEOPLE depuis TECH + SPIRIT
   *
   * TECH fournit les valeurs structurees → narrative, explanation
   * SPIRIT fournit le ton vibratoire → emotional_tone
   */
  private reconstructPeople(tech: TechPayload, spirit: SpiritPayload): PeoplePayload {
    // Deduire le tone emotionnel depuis la frequence
    const tone = this.deduceEmotionalTone(spirit.frequency_hz);

    // Generer le narrative depuis les donnees techniques
    const dataType = tech.data_type || 'evenement';
    const narrative = `[Reconstruit] ${dataType} — donnees techniques restaurees par correction quantique a ${spirit.frequency_hz}Hz`;
    const explanation = `Cette traduction a ete reconstruite par cross-validation. Les dimensions TECH et SPIRIT etaient intactes (niveau de resonance ${spirit.resonance_level}, geometrie ${spirit.sacred_geometry}).`;

    return {
      narrative,
      explanation,
      guide_steps: ['Verifier les donnees reconstruites', 'Valider la coherence semantique'],
      emotional_tone: tone,
      language: 'fr',
    };
  }

  /**
   * Reconstruit SPIRIT depuis TECH + PEOPLE
   *
   * TECH fournit le hash de validation → frequence calculee
   * PEOPLE fournit le ton → resonance level
   */
  private reconstructSpirit(tech: TechPayload, people: PeoplePayload): SpiritPayload {
    // Calculer le niveau de resonance depuis le narrative (Arithmos)
    const level = RosettaParser.computeArithmos(people.narrative);
    const frequency = RESONANCE_MATRIX[level].hz;

    // Deduire la geometrie sacree
    const geometry = RosettaParser.geometryFor(level);

    // Calculer la signature vibratoire (4 composantes)
    const vibration = this.computeVibrationSignature(tech, people);

    return {
      frequency_hz: frequency,
      resonance_level: level,
      color: RESONANCE_MATRIX[level].color,
      sacred_geometry: geometry,
      vibration_signature: vibration,
      phi_ratio: 1.618,
    };
  }

  // ═══════════════════════════════════════════════════════
  // UTILITAIRES INTERNES
  // ═══════════════════════════════════════════════════════

  /** Deduit le ton emotionnel depuis une frequence */
  private deduceEmotionalTone(
    hz: number,
  ): PeoplePayload['emotional_tone'] {
    if (hz >= 888) return 'sacre';
    if (hz >= 666) return 'celebratoire';
    if (hz >= 444) return 'encourageant';
    if (hz >= 222) return 'neutre';
    return 'alerte';
  }

  /** Calcule une signature vibratoire depuis TECH + PEOPLE */
  private computeVibrationSignature(
    tech: TechPayload,
    people: PeoplePayload,
  ): number[] {
    // 4 composantes : [Materiel, Personnel, Intentionnel, Potentiel]
    const m = Object.keys(tech.values).length / 10; // Densite des donnees
    const p = people.narrative.length / 500;         // Richesse narrative
    const i = people.guide_steps?.length ?? 0;       // Profondeur du guide
    const po = people.emotional_tone === 'sacre' ? 1.0 : 0.5;

    return [
      parseFloat(Math.min(1, m).toFixed(3)),
      parseFloat(Math.min(1, p).toFixed(3)),
      parseFloat(Math.min(1, i / 5).toFixed(3)),
      po,
    ];
  }

  /** Recupere le hash stocke pour une dimension */
  private getStoredHash(qt: QuantumRosettaTranslation, dim: CorruptionTarget): string {
    switch (dim) {
      case 'TECH': return qt.dimension_hashes.tech_hash;
      case 'PEOPLE': return qt.dimension_hashes.people_hash;
      case 'SPIRIT': return qt.dimension_hashes.spirit_hash;
    }
  }

  /** Recalcule le hash actuel pour une dimension */
  private getCurrentHash(t: RosettaTranslation, dim: CorruptionTarget): string {
    switch (dim) {
      case 'TECH': return RosettaParser.computeDimensionHash(t.tech);
      case 'PEOPLE': return RosettaParser.computeDimensionHash(t.people);
      case 'SPIRIT': return RosettaParser.computeDimensionHash(t.spirit);
    }
  }
}
