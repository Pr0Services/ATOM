/**
 * AT-OM -- PolishingEngine Tests
 * Suite de tests unitaires pour le moteur de validation alchimique
 *
 * Couvre :
 *   1. PolishingEngine     -- 7 etapes alchimiques + batch + stats
 *   2. InformationFilter   -- Analyse de resonance informationnelle
 *   3. IntentionGuard      -- Filtre SERVIR vs EXTRAIRE
 *   4. UniversalLawValidator -- Validation des 7 lois universelles
 */

import { describe, it, expect, beforeEach } from 'vitest';
import {
  PolishingEngine,
  InformationFilter,
  IntentionGuard,
  UniversalLawValidator,
} from '../PolishingEngine';
import type { ATOMNode, RosettaTranslation } from '../../types/atom-types';
import { SACRED_FREQUENCIES } from '../../types/atom-types';
import type { PolishingInput } from '../PolishingEngine';

// ===============================================================
// HELPERS : Donnees de test valides
// ===============================================================

/** Cree un ATOMNode minimal valide qui passe toutes les etapes */
function createValidNode(): ATOMNode {
  return {
    id: 'node-test-001',
    parent_id: null,
    sphere_id: 'TECHNO',
    title: 'Test Node Alchimique',
    status: 'active',
    depth: 1,
    spiral_position: 0,
    resonance_level: 4,
    rosetta: createValidRosetta(),
    created_by: 'test-user',
    created_at: Date.now(),
    updated_at: Date.now(),
  };
}

/** Cree une RosettaTranslation minimale valide qui passe toutes les etapes */
function createValidRosetta(): RosettaTranslation {
  return {
    id: 'rosetta-test-001',
    node_id: 'node-test-001',
    tech: {
      schema_version: '1.0',
      data_type: 'test',
      values: { key: 'value' },
      timestamp: Date.now(),
    },
    people: {
      narrative: 'Une description humaine suffisamment longue pour passer la validation.',
      explanation: 'Explication technique accessible.',
      emotional_tone: 'neutre',
      language: 'fr',
    },
    spirit: {
      frequency_hz: 444,
      resonance_level: 4,
      color: '#00FF00',
      sacred_geometry: 'tetrahedron',
      vibration_signature: [44.4, 161.8, 369, 1728],
      phi_ratio: SACRED_FREQUENCIES.PHI,
    },
    created_at: Date.now(),
    source_dimension: 'TECH',
    integrity_hash: 'abc123',
  };
}

/** Combine node + rosetta en PolishingInput */
function createValidInput(): PolishingInput {
  const node = createValidNode();
  const rosetta = createValidRosetta();
  return { node, rosetta };
}

// ===============================================================
// 1. POLISHING ENGINE
// ===============================================================

describe('PolishingEngine', () => {
  let engine: PolishingEngine;

  beforeEach(() => {
    engine = new PolishingEngine();
  });

  it('should create with default rules for all 7 stages', () => {
    const rules = PolishingEngine.createDefaultRules();
    expect(rules).toHaveLength(7);
    expect(rules.map(r => r.stage)).toEqual([
      'CALCINATION',
      'DISSOLUTION',
      'SEPARATION',
      'CONJUNCTION',
      'FERMENTATION',
      'DISTILLATION',
      'COAGULATION',
    ]);
  });

  it('CALCINATION: should pass with valid node and rosetta', () => {
    const input = createValidInput();
    const result = engine.polishData(input);
    // If CALCINATION passes, stage_index should be beyond 1
    expect(result.transformation_log[0].passed).toBe(true);
  });

  it('CALCINATION: should fail when node.id is missing', () => {
    const input = createValidInput();
    input.node.id = '';
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('CALCINATION');
    expect(result.stage_index).toBe(1);
  });

  it('CALCINATION: should fail when node.title is missing', () => {
    const input = createValidInput();
    input.node.title = '';
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('CALCINATION');
  });

  it('DISSOLUTION: should fail when tech.data_type is missing', () => {
    const input = createValidInput();
    input.rosetta.tech.data_type = '';
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('DISSOLUTION');
    expect(result.stage_index).toBe(2);
  });

  it('SEPARATION: should fail when frequency does not match resonance_level * 111', () => {
    const input = createValidInput();
    input.rosetta.spirit.frequency_hz = 999; // Expected: 4 * 111 = 444
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('SEPARATION');
    expect(result.stage_index).toBe(3);
  });

  it('CONJUNCTION: should fail when narrative is too short (< 10 chars)', () => {
    const input = createValidInput();
    input.rosetta.people.narrative = 'Court';
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('CONJUNCTION');
    expect(result.stage_index).toBe(4);
  });

  it('FERMENTATION: should fail when node status is archived', () => {
    const input = createValidInput();
    input.node.status = 'archived';
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('FERMENTATION');
    expect(result.stage_index).toBe(5);
  });

  it('DISTILLATION: should fail when integrity_hash is missing', () => {
    const input = createValidInput();
    input.rosetta.integrity_hash = '';
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('DISTILLATION');
    expect(result.stage_index).toBe(6);
  });

  it('COAGULATION: should fail when node status is polishing', () => {
    const input = createValidInput();
    input.node.status = 'polishing';
    const result = engine.polishData(input);
    expect(result.is_aligned).toBe(false);
    expect(result.current_stage).toBe('COAGULATION');
    expect(result.stage_index).toBe(7);
  });

  it('isAligned() should return true for perfectly valid data', () => {
    const input = createValidInput();
    expect(engine.isAligned(input)).toBe(true);
  });

  it('diagnose() should return null when data is fully aligned', () => {
    const input = createValidInput();
    expect(engine.diagnose(input)).toBeNull();
  });

  it('diagnose() should return the first failure stage and reason', () => {
    const input = createValidInput();
    input.rosetta.tech.data_type = '';
    const diag = engine.diagnose(input);
    expect(diag).not.toBeNull();
    expect(diag!.stage).toBe('DISSOLUTION');
    expect(diag!.reason).toContain('TECH');
  });

  it('polishBatch() should separate aligned and toPolish results', () => {
    const good = createValidInput();
    const bad = createValidInput();
    bad.node.id = '';
    const batch = engine.polishBatch([good, bad]);
    expect(batch.aligned).toHaveLength(1);
    expect(batch.toPolish).toHaveLength(1);
    expect(batch.aligned[0].is_aligned).toBe(true);
    expect(batch.toPolish[0].is_aligned).toBe(false);
  });

  it('getStats() should compute correct statistics', () => {
    const good = createValidInput();
    const bad1 = createValidInput();
    bad1.node.id = '';
    const bad2 = createValidInput();
    bad2.rosetta.tech.data_type = '';

    const results = [good, bad1, bad2].map(i => engine.polishData(i));
    const stats = engine.getStats(results);

    expect(stats.total).toBe(3);
    expect(stats.aligned).toBe(1);
    expect(stats.toPolish).toBe(2);
    expect(stats.alignment_ratio).toBeCloseTo(1 / 3, 5);
    expect(stats.stage_distribution['COAGULATION']).toBe(1);
    expect(stats.stage_distribution['CALCINATION']).toBe(1);
    expect(stats.stage_distribution['DISSOLUTION']).toBe(1);
  });
});

// ===============================================================
// 2. INFORMATION FILTER
// ===============================================================

describe('InformationFilter', () => {
  it('analyzeResonance: rich content with verified sources should yield high score', () => {
    const score = InformationFilter.analyzeResonance({
      text: 'Un article detaille et bien structure sur les avancees scientifiques. '
        + 'Les donnees sont corroborees par plusieurs etudes independantes. '
        + 'La methodologie est transparente et reproductible par la communaute.',
      author_id: 'author-42',
      sources: [
        { reference: 'Nature 2025', verified: true },
        { reference: 'Science Direct', verified: true },
        { reference: 'PubMed Study', verified: true },
        { reference: 'ArXiv Preprint', verified: true },
        { reference: 'IEEE Paper', verified: true },
      ],
      methodology_disclosed: true,
      author_history_score: 90,
    });

    // With 5 verified sources, good length, methodology, high author score
    expect(score.score_global).toBeGreaterThanOrEqual(70);
    expect(score.coherence_externe).toBe(100);
    expect(score.diversite_sources).toBe(100);
    expect(score.transparence_methodo).toBe(80);
    expect(score.fiabilite_auteur).toBe(90);
    expect(score.intention_detectee).toBe('INFORMATIF');
  });

  it('analyzeResonance: empty/minimal content should yield low score', () => {
    const score = InformationFilter.analyzeResonance({
      text: 'Court',
    });

    expect(score.score_global).toBeLessThan(30);
    expect(score.coherence_externe).toBe(0);
    expect(score.diversite_sources).toBe(0);
    expect(score.transparence_methodo).toBe(20);
  });

  it('detectIntention: should return DIVISIF with >= 2 divisif markers', () => {
    const intention = InformationFilter.detectIntention(
      'Les ennemi sont partout, ils veulent tout detruire. La menace est reelle!',
    );
    expect(intention).toBe('DIVISIF');
  });

  it('detectIntention: should return MANIPULATIF with >= 2 manipulatif markers', () => {
    const intention = InformationFilter.detectIntention(
      'C\'est votre derniere chance ! Agissez maintenant avant qu\'il ne soit trop tard. Secret revele !',
    );
    // Note: the source checks lowercase, markers use accented chars
    // 'derniere chance' vs 'dernière chance' -- let's use exact markers
    const intention2 = InformationFilter.detectIntention(
      'C\'est la dernière chance ! Le secret révélé va vous choquer. Incroyable !',
    );
    expect(intention2).toBe('MANIPULATIF');
  });

  it('detectIntention: should return COMMERCIAL with >= 2 commercial markers', () => {
    const intention = InformationFilter.detectIntention(
      'Achetez maintenant cette promotion exceptionnelle ! Prix imbattable !',
    );
    expect(intention).toBe('COMMERCIAL');
  });

  it('detectIntention: should return PERSUASIF with >= 2 persuasif markers', () => {
    const intention = InformationFilter.detectIntention(
      'Je pense que nous devons agir maintenant. Il est clair que la solution est evidente.',
    );
    expect(intention).toBe('PERSUASIF');
  });

  it('meetsResonanceThreshold: passes when score >= 50 and not MANIPULATIF', () => {
    const highScore = InformationFilter.analyzeResonance({
      text: 'Un article detaille et bien structure sur les avancees scientifiques. '
        + 'Les recherches approfondies demontrent des resultats reproductibles.',
      author_id: 'author-1',
      sources: [
        { reference: 'Source A', verified: true },
        { reference: 'Source B', verified: true },
        { reference: 'Source C', verified: true },
      ],
      methodology_disclosed: true,
      author_history_score: 80,
    });

    expect(InformationFilter.meetsResonanceThreshold(highScore)).toBe(true);

    // Even with high score, MANIPULATIF should fail
    const manipScore = { ...highScore, intention_detectee: 'MANIPULATIF' as const, score_global: 80 };
    expect(InformationFilter.meetsResonanceThreshold(manipScore)).toBe(false);

    // Low score should fail even if INFORMATIF
    const lowScore = { ...highScore, score_global: 30 };
    expect(InformationFilter.meetsResonanceThreshold(lowScore)).toBe(false);
  });
});

// ===============================================================
// 3. INTENTION GUARD
// ===============================================================

describe('IntentionGuard', () => {
  it('evaluate: should return SERVIR when all criteria are true', () => {
    const result = IntentionGuard.evaluate({
      description: 'Offrir un outil educatif gratuit',
      sert_epanouissement: true,
      respecte_souverainete: true,
      est_transparent: true,
      cree_plus_de_valeur: true,
      aligne_spheres: true,
      visible_par_tous: true,
    });
    expect(result.verdict).toBe('SERVIR');
    expect(result.action).toBe('Offrir un outil educatif gratuit');
  });

  it('evaluate: should return SERVIR when all defaults (not provided)', () => {
    const result = IntentionGuard.evaluate({
      description: 'Action par defaut',
    });
    expect(result.verdict).toBe('SERVIR');
  });

  it('evaluate: should return EXTRAIRE when any criterion is false', () => {
    const result = IntentionGuard.evaluate({
      description: 'Collecter des donnees sans consentement',
      respecte_souverainete: false,
    });
    expect(result.verdict).toBe('EXTRAIRE');
  });

  it('checkPrinciples: clean action should have respects = true', () => {
    const result = IntentionGuard.checkPrinciples('Publier un article educatif');
    expect(result.respects).toBe(true);
    expect(result.violations).toHaveLength(0);
  });

  it('checkPrinciples: "supprimer donnees utilisateur" triggers Souverainete violation', () => {
    const result = IntentionGuard.checkPrinciples(
      'Supprimer les données utilisateur sans leur accord',
    );
    expect(result.respects).toBe(false);
    expect(result.violations).toContainEqual(
      expect.stringContaining('Souverainet'),
    );
  });

  it('checkPrinciples: "forcer" triggers Consentement violation', () => {
    const result = IntentionGuard.checkPrinciples(
      'Forcer les utilisateurs a accepter les conditions',
    );
    expect(result.respects).toBe(false);
    expect(result.violations).toContainEqual(
      expect.stringContaining('Consentement'),
    );
  });

  it('IMMUTABLE_PRINCIPLES should contain exactly 7 items', () => {
    expect(IntentionGuard.IMMUTABLE_PRINCIPLES).toHaveLength(7);
  });
});

// ===============================================================
// 4. UNIVERSAL LAW VALIDATOR
// ===============================================================

describe('UniversalLawValidator', () => {
  it('checkCorrespondance: true when frequency matches resonance_level * 111', () => {
    const node = createValidNode();
    const rosetta = createValidRosetta();
    // resonance_level = 4, frequency_hz = 444 => 4 * 111 = 444
    expect(UniversalLawValidator.checkCorrespondance(node, rosetta)).toBe(true);
  });

  it('checkCorrespondance: false when frequency does not match', () => {
    const node = createValidNode();
    const rosetta = createValidRosetta();
    rosetta.spirit.frequency_hz = 333;
    expect(UniversalLawValidator.checkCorrespondance(node, rosetta)).toBe(false);
  });

  it('checkVibration: true for 444, false for 100 or 1000', () => {
    const rosetta = createValidRosetta();

    rosetta.spirit.frequency_hz = 444;
    expect(UniversalLawValidator.checkVibration(rosetta)).toBe(true);

    rosetta.spirit.frequency_hz = 100;
    expect(UniversalLawValidator.checkVibration(rosetta)).toBe(false);

    rosetta.spirit.frequency_hz = 1000;
    expect(UniversalLawValidator.checkVibration(rosetta)).toBe(false);
  });

  it('checkPolarite: true when all 3 dimensions present, false when missing', () => {
    const rosetta = createValidRosetta();
    expect(UniversalLawValidator.checkPolarite(rosetta)).toBe(true);

    const incomplete = createValidRosetta();
    incomplete.tech.data_type = '';
    expect(UniversalLawValidator.checkPolarite(incomplete)).toBe(false);
  });

  it('checkCauseEffet: true with hash, false without', () => {
    const rosetta = createValidRosetta();
    expect(UniversalLawValidator.checkCauseEffet(rosetta)).toBe(true);

    const noHash = createValidRosetta();
    noHash.integrity_hash = '';
    expect(UniversalLawValidator.checkCauseEffet(noHash)).toBe(false);
  });

  it('fullAudit: score 100 when all laws pass', () => {
    const node = createValidNode();
    const rosetta = createValidRosetta();
    const audit = UniversalLawValidator.fullAudit(node, rosetta);

    expect(audit.score).toBe(100);
    expect(audit.passed).toHaveLength(7);
    expect(audit.failed).toHaveLength(0);
    expect(audit.passed).toContain('CORRESPONDANCE');
    expect(audit.passed).toContain('VIBRATION');
    expect(audit.passed).toContain('POLARITE');
    expect(audit.passed).toContain('CAUSE_EFFET');
    expect(audit.passed).toContain('RYTHME');
    expect(audit.passed).toContain('GENRE');
    expect(audit.passed).toContain('MENTALISME');
  });

  it('fullAudit: score < 100 when some laws fail', () => {
    const node = createValidNode();
    const rosetta = createValidRosetta();
    rosetta.spirit.frequency_hz = 333; // Breaks CORRESPONDANCE and VIBRATION stays valid (333 % 111 = 0)
    rosetta.integrity_hash = '';       // Breaks CAUSE_EFFET

    const audit = UniversalLawValidator.fullAudit(node, rosetta);

    expect(audit.score).toBeLessThan(100);
    expect(audit.failed).toContain('CORRESPONDANCE');
    expect(audit.failed).toContain('CAUSE_EFFET');
    // VIBRATION should still pass (333 is between 111-999 and 333 % 111 === 0)
    expect(audit.passed).toContain('VIBRATION');
    // RYTHME, GENRE, MENTALISME always pass
    expect(audit.passed).toContain('RYTHME');
    expect(audit.passed).toContain('GENRE');
    expect(audit.passed).toContain('MENTALISME');
  });
});
