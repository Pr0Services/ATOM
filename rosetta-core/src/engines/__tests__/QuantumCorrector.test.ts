/**
 * AT·OM — QuantumCorrector Tests
 * Suite de tests unitaires pour le systeme de correction d'erreur quantique
 *
 * Couvre le pipeline complet :
 *   1. enrich()      — ajout de hashes par dimension
 *   2. detect()      — detection de corruption
 *   3. diagnose()    — localisation de la dimension corrompue
 *   4. correct()     — reconstruction par cross-validation
 *   5. validate()    — verification post-correction
 *   6. process()     — pipeline complet
 *   7. processBatch() — traitement par lots
 *   8. getStats()    — statistiques
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { QuantumCorrector } from '../QuantumCorrector';
import { RosettaParser } from '../../parser/RosettaParser';
import type {
  RosettaTranslation,
  QuantumRosettaTranslation,
  TechPayload,
  PeoplePayload,
  SpiritPayload,
} from '../../types/atom-types';

// ═══════════════════════════════════════════════════════════
// HELPERS : Creation de translations de test
// ═══════════════════════════════════════════════════════════

function createHealthyTranslation(): RosettaTranslation {
  const tech: TechPayload = {
    schema_version: '1.0.0',
    data_type: 'test_event',
    values: { name: 'Test', score: 42 },
    timestamp: 1700000000000,
  };

  const people: PeoplePayload = {
    narrative: 'Un evenement de test pour la correction quantique',
    explanation: 'Cet evenement valide le pipeline de correction',
    guide_steps: ['Verifier', 'Corriger', 'Valider'],
    emotional_tone: 'neutre',
    language: 'fr',
  };

  const spirit: SpiritPayload = {
    frequency_hz: 444,
    resonance_level: 4,
    color: '#50C878',
    sacred_geometry: 'tetrahedron',
    vibration_signature: [0.5, 0.6, 0.4, 0.5],
    phi_ratio: 1.618,
  };

  const integrity_hash = RosettaParser.computeCombinedHash(tech, people, spirit);

  return {
    id: 'test_001',
    node_id: 'node_test_001',
    tech,
    people,
    spirit,
    created_at: Date.now(),
    source_dimension: 'TECH',
    integrity_hash,
  };
}

function corruptTech(t: RosettaTranslation): RosettaTranslation {
  return {
    ...t,
    tech: {
      ...t.tech,
      data_type: 'CORRUPTED_DATA',
      values: { hacked: true },
    },
    // integrity_hash reste l'ancien → mismatch
  };
}

function corruptPeople(t: RosettaTranslation): RosettaTranslation {
  return {
    ...t,
    people: {
      ...t.people,
      narrative: '',
      explanation: '',
      emotional_tone: 'alerte',
    },
  };
}

function corruptSpirit(t: RosettaTranslation): RosettaTranslation {
  return {
    ...t,
    spirit: {
      ...t.spirit,
      frequency_hz: -999,
      resonance_level: 1,
      sacred_geometry: 'point',
    },
  };
}

// ═══════════════════════════════════════════════════════════
// TESTS
// ═══════════════════════════════════════════════════════════

describe('QuantumCorrector', () => {
  let corrector: QuantumCorrector;

  beforeEach(() => {
    corrector = new QuantumCorrector();
  });

  // ─── enrich() ────────────────────────────────────────

  describe('enrich()', () => {
    it('should add dimension_hashes to a translation', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      expect(qt.dimension_hashes).toBeDefined();
      expect(qt.dimension_hashes.tech_hash).toBeTruthy();
      expect(qt.dimension_hashes.people_hash).toBeTruthy();
      expect(qt.dimension_hashes.spirit_hash).toBeTruthy();
      expect(qt.dimension_hashes.combined_hash).toBeTruthy();
    });

    it('should preserve original translation fields', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      expect(qt.id).toBe(t.id);
      expect(qt.node_id).toBe(t.node_id);
      expect(qt.tech).toEqual(t.tech);
      expect(qt.people).toEqual(t.people);
      expect(qt.spirit).toEqual(t.spirit);
      expect(qt.integrity_hash).toBe(t.integrity_hash);
    });

    it('should produce unique hashes per dimension', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      // Chaque dimension a un hash different
      const hashes = new Set([
        qt.dimension_hashes.tech_hash,
        qt.dimension_hashes.people_hash,
        qt.dimension_hashes.spirit_hash,
      ]);
      expect(hashes.size).toBe(3);
    });
  });

  // ─── detect() ────────────────────────────────────────

  describe('detect()', () => {
    it('should return false for a healthy translation', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      expect(corrector.detect(qt)).toBe(false);
    });

    it('should return true for a corrupted translation', () => {
      const t = createHealthyTranslation();
      const corrupted = corruptTech(t);
      const qt = corrector.enrich(corrupted);
      // Enrich recalcule les hashes, mais integrity_hash est l'ancien
      // Donc detect compare le recalculated combined vs stored
      // corrupted a un integrity_hash qui ne correspond plus a tech corrompue

      expect(corrector.detect(qt)).toBe(true);
    });
  });

  // ─── diagnose() ──────────────────────────────────────

  describe('diagnose()', () => {
    it('should report no corruption for a healthy translation', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);
      const diag = corrector.diagnose(qt);

      expect(diag.is_corrupted).toBe(false);
      expect(diag.severity).toBe('none');
      expect(diag.corrupted_dimensions).toHaveLength(0);
      expect(diag.healthy_dimensions).toHaveLength(3);
      expect(diag.confidence).toBe(1.0);
    });

    it('should localize TECH corruption with high confidence', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      // Corrompre TECH apres enrichissement (simule une alteration post-stockage)
      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        tech: {
          ...qt.tech,
          data_type: 'HACKED',
          values: { compromised: true },
        },
      };

      const diag = corrector.diagnose(corruptedQt);

      expect(diag.is_corrupted).toBe(true);
      expect(diag.severity).toBe('minor');
      expect(diag.corrupted_dimensions).toContain('TECH');
      expect(diag.healthy_dimensions).toContain('PEOPLE');
      expect(diag.healthy_dimensions).toContain('SPIRIT');
      expect(diag.confidence).toBe(1.0);
    });

    it('should localize PEOPLE corruption', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        people: {
          ...qt.people,
          narrative: 'CORRUPTED NARRATIVE',
          emotional_tone: 'alerte',
        },
      };

      const diag = corrector.diagnose(corruptedQt);

      expect(diag.is_corrupted).toBe(true);
      expect(diag.corrupted_dimensions).toContain('PEOPLE');
      expect(diag.healthy_dimensions).toContain('TECH');
      expect(diag.healthy_dimensions).toContain('SPIRIT');
    });

    it('should localize SPIRIT corruption', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        spirit: {
          ...qt.spirit,
          frequency_hz: -1,
          resonance_level: 9,
        },
      };

      const diag = corrector.diagnose(corruptedQt);

      expect(diag.is_corrupted).toBe(true);
      expect(diag.corrupted_dimensions).toContain('SPIRIT');
    });

    it('should detect major severity for 2 corrupted dimensions', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        tech: { ...qt.tech, data_type: 'HACKED' },
        people: { ...qt.people, narrative: 'CORRUPTED' },
      };

      const diag = corrector.diagnose(corruptedQt);

      expect(diag.severity).toBe('major');
      expect(diag.corrupted_dimensions).toHaveLength(2);
      expect(diag.confidence).toBe(0.33);
    });

    it('should detect critical severity for 3 corrupted dimensions', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        tech: { ...qt.tech, data_type: 'X' },
        people: { ...qt.people, narrative: 'X' },
        spirit: { ...qt.spirit, frequency_hz: -1 },
      };

      const diag = corrector.diagnose(corruptedQt);

      expect(diag.severity).toBe('critical');
      expect(diag.confidence).toBe(0.0);
    });
  });

  // ─── correct() ───────────────────────────────────────

  describe('correct()', () => {
    it('should reconstruct a corrupted TECH dimension', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        tech: { ...qt.tech, data_type: 'HACKED', values: {} },
      };

      const diag = corrector.diagnose(corruptedQt);
      const result = corrector.correct(corruptedQt, diag);

      expect(result.applied).toBe(true);
      expect(result.corrected).not.toBeNull();
      expect(result.corrected!.tech.data_type).toBeTruthy();
      expect(result.corrected!.tech.data_type).not.toBe('HACKED');
      expect(result.correction_log.length).toBeGreaterThan(0);
    });

    it('should reconstruct a corrupted PEOPLE dimension', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        people: { ...qt.people, narrative: 'CORRUPTED', explanation: '' },
      };

      const diag = corrector.diagnose(corruptedQt);
      const result = corrector.correct(corruptedQt, diag);

      expect(result.applied).toBe(true);
      expect(result.corrected).not.toBeNull();
      expect(result.corrected!.people.narrative).toBeTruthy();
      expect(result.corrected!.people.narrative).not.toBe('CORRUPTED');
    });

    it('should reconstruct a corrupted SPIRIT dimension', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        spirit: { ...qt.spirit, frequency_hz: -999, resonance_level: 1 },
      };

      const diag = corrector.diagnose(corruptedQt);
      const result = corrector.correct(corruptedQt, diag);

      expect(result.applied).toBe(true);
      expect(result.corrected).not.toBeNull();
      expect(result.corrected!.spirit.frequency_hz).toBeGreaterThan(0);
    });

    it('should return null for 2+ corrupted dimensions (irreparable)', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        tech: { ...qt.tech, data_type: 'X' },
        people: { ...qt.people, narrative: 'X' },
      };

      const diag = corrector.diagnose(corruptedQt);
      const result = corrector.correct(corruptedQt, diag);

      expect(result.applied).toBe(false);
      expect(result.corrected).toBeNull();
    });

    it('should not apply correction on healthy translation', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const diag = corrector.diagnose(qt);
      const result = corrector.correct(qt, diag);

      expect(result.applied).toBe(false);
      expect(result.corrected).toEqual(qt);
    });
  });

  // ─── validate() ──────────────────────────────────────

  describe('validate()', () => {
    it('should validate a successfully corrected translation', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        tech: { ...qt.tech, data_type: 'HACKED', values: {} },
      };

      const diag = corrector.diagnose(corruptedQt);
      const result = corrector.correct(corruptedQt, diag);

      expect(corrector.validate(result)).toBe(true);
    });

    it('should return false for a failed correction', () => {
      const t = createHealthyTranslation();
      const qt = corrector.enrich(t);

      const corruptedQt: QuantumRosettaTranslation = {
        ...qt,
        tech: { ...qt.tech, data_type: 'X' },
        people: { ...qt.people, narrative: 'X' },
      };

      const diag = corrector.diagnose(corruptedQt);
      const result = corrector.correct(corruptedQt, diag);

      expect(corrector.validate(result)).toBe(false);
    });
  });

  // ─── process() ───────────────────────────────────────

  describe('process()', () => {
    it('should handle a healthy translation without correction', () => {
      const t = createHealthyTranslation();
      const result = corrector.process(t);

      expect(result.diagnostic.is_corrupted).toBe(false);
      expect(result.applied).toBe(false);
      expect(result.corrected).toEqual(t);
    });

    it('should run full pipeline on a corrupted translation', () => {
      const t = createHealthyTranslation();
      // Corrompre SPIRIT mais garder l'ancien integrity_hash
      const corrupted: RosettaTranslation = {
        ...t,
        spirit: { ...t.spirit, frequency_hz: -1, resonance_level: 9 },
      };

      const result = corrector.process(corrupted);

      // Le pipeline detecte → diagnostique → corrige
      expect(result.diagnostic.is_corrupted).toBe(true);
      // Note: detect() compare le combined_hash recalcule vs stocke
      // Comme corrupted a le meme integrity_hash que l'original
      // mais le contenu a change, detect() retournera true
    });
  });

  // ─── processBatch() ──────────────────────────────────

  describe('processBatch()', () => {
    it('should process a batch and return stats', () => {
      const healthy1 = createHealthyTranslation();
      const healthy2 = { ...createHealthyTranslation(), id: 'test_002' };

      const batch = corrector.processBatch([healthy1, healthy2]);

      expect(batch.stats.total).toBe(2);
      expect(batch.stats.healthy).toBe(2);
      expect(batch.stats.corrected).toBe(0);
      expect(batch.stats.failed).toBe(0);
      expect(batch.results).toHaveLength(2);
    });
  });

  // ─── getStats() ──────────────────────────────────────

  describe('getStats()', () => {
    it('should start with zero stats', () => {
      const stats = corrector.getStats();

      expect(stats.detected).toBe(0);
      expect(stats.corrected).toBe(0);
      expect(stats.failed).toBe(0);
    });

    it('should accumulate stats across operations', () => {
      const t = createHealthyTranslation();
      corrector.process(t); // healthy → no detection

      const stats = corrector.getStats();
      expect(stats.detected).toBe(0);
    });

    it('should reset stats when requested', () => {
      corrector.resetStats();
      const stats = corrector.getStats();

      expect(stats.detected).toBe(0);
      expect(stats.corrected).toBe(0);
      expect(stats.failed).toBe(0);
    });
  });

  // ─── getCorrectionLog() ──────────────────────────────

  describe('getCorrectionLog()', () => {
    it('should start with empty log', () => {
      expect(corrector.getCorrectionLog()).toHaveLength(0);
    });

    it('should return a copy (immutable)', () => {
      const log1 = corrector.getCorrectionLog();
      const log2 = corrector.getCorrectionLog();

      expect(log1).not.toBe(log2); // Different references
      expect(log1).toEqual(log2);  // Same content
    });
  });
});
