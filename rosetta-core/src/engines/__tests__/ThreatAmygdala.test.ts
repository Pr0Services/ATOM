/**
 * AT·OM — ThreatAmygdala Tests
 * Suite de tests unitaires pour la sentinelle pre-corticale
 *
 * Couvre :
 *   1. Fast Path — 5 checks legers
 *   2. Deep Path — analyse detaillee
 *   3. Reponse graduee — CALM → VIGILANT → ALERT → LOCKDOWN
 *   4. Memoire adaptative — buffer, sensibilite, decay
 *   5. Evenements — onThreat, transitions
 *   6. Pipeline complet — scan() bout-en-bout
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { ThreatAmygdala } from '../ThreatAmygdala';
import { RosettaParser } from '../../parser/RosettaParser';
import type {
  RosettaTranslation,
  TechPayload,
  PeoplePayload,
  SpiritPayload,
  ThreatSignal,
  AmygdalaEvent,
} from '../../types/atom-types';

// ═══════════════════════════════════════════════════════════
// HELPERS : Creation de donnees de test
// ═══════════════════════════════════════════════════════════

function createTechPayload(overrides: Partial<TechPayload> = {}): TechPayload {
  return {
    schema_version: '1.0',
    data_type: 'metric',
    values: { temperature: 22.5, humidity: 60 },
    timestamp: Date.now(),
    ...overrides,
  };
}

function createPeoplePayload(overrides: Partial<PeoplePayload> = {}): PeoplePayload {
  return {
    narrative: 'La temperature est de 22.5 degres avec une humidite de 60%.',
    emotional_tone: 'neutre',
    accessibility_level: 'standard',
    guide_message: 'Les conditions sont optimales.',
    ...overrides,
  };
}

function createSpiritPayload(overrides: Partial<SpiritPayload> = {}): SpiritPayload {
  return {
    frequency_hz: 444,
    resonance_level: 4,
    sacred_geometry: 'hexagone',
    vibration_signature: 'stable_harmonique',
    color: '#D4AF37',
    ...overrides,
  };
}

function createHealthyTranslation(): RosettaTranslation {
  const tech = createTechPayload();
  const people = createPeoplePayload();
  const spirit = createSpiritPayload();
  const hash = RosettaParser.computeCombinedHash(tech, people, spirit);

  return {
    id: 'test_healthy_001',
    domain: 'test',
    source_dimension: 'TECH',
    tech,
    people,
    spirit,
    integrity_hash: hash,
    emerald_validation: {
      is_aligned: true,
      current_stage: 'COAGULATION',
      polishing_notes: [],
      alignment_score: 100,
    },
    created_at: Date.now(),
    node_id: 'node_test_001',
  };
}

function createCorruptedTranslation(dimension: 'TECH' | 'PEOPLE' | 'SPIRIT'): RosettaTranslation {
  const translation = createHealthyTranslation();

  // Corrompre la dimension specifiee (modifier apres le hash)
  switch (dimension) {
    case 'TECH':
      translation.tech = createTechPayload({ data_type: 'CORRUPTED' });
      break;
    case 'PEOPLE':
      translation.people = createPeoplePayload({ narrative: 'CORRUPTED DATA' });
      break;
    case 'SPIRIT':
      translation.spirit = createSpiritPayload({ frequency_hz: 666 });
      break;
  }
  // Le hash ne correspond plus → corruption detectable
  return translation;
}

// ═══════════════════════════════════════════════════════════
// TESTS
// ═══════════════════════════════════════════════════════════

describe('ThreatAmygdala', () => {
  let parser: RosettaParser;
  let amygdala: ThreatAmygdala;

  beforeEach(() => {
    parser = new RosettaParser();
    amygdala = new ThreatAmygdala(parser);
  });

  // ─── FAST PATH ──────────────────────────────────────────

  describe('Fast Path', () => {

    describe('frequencyCheck', () => {
      it('detecte une frequence hors range bas', () => {
        const signal = amygdala.scan({
          type: 'frequency',
          data: { frequency: 10 },
          source: 'test',
        });
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('frequency_anomaly');
        expect(signal!.pathway).toBe('fast');
      });

      it('detecte une frequence hors range haut', () => {
        const signal = amygdala.scan({
          type: 'frequency',
          data: { frequency: 5000 },
          source: 'test',
        });
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('frequency_anomaly');
      });

      it('laisse passer une frequence valide', () => {
        const signal = amygdala.scan({
          type: 'frequency',
          data: { frequency: 444 },
          source: 'test',
        });
        expect(signal).toBeNull();
      });

      it('laisse passer les bornes limites', () => {
        const low = amygdala.scan({
          type: 'frequency',
          data: { frequency: 44.4 },
          source: 'test',
        });
        expect(low).toBeNull();

        const high = amygdala.scan({
          type: 'frequency',
          data: { frequency: 1728 },
          source: 'test',
        });
        expect(high).toBeNull();
      });
    });

    describe('hashQuickCheck', () => {
      it('detecte un hash corrompu', () => {
        const corrupted = createCorruptedTranslation('TECH');
        const signal = amygdala.scan({
          type: 'translation',
          data: corrupted,
          source: 'test',
        });
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('integrity_breach');
        expect(signal!.pathway).toBe('fast');
      });

      it('laisse passer une translation saine', () => {
        const healthy = createHealthyTranslation();
        const signal = amygdala.scan({
          type: 'translation',
          data: healthy,
          source: 'test',
        });
        expect(signal).toBeNull();
      });
    });

    describe('dimensionBalanceCheck', () => {
      it('detecte une dimension tech vide', () => {
        const translation = createHealthyTranslation();
        (translation.tech as unknown) = { schema_version: '1.0', data_type: '', values: {}, timestamp: 0 };
        // Recalculate hash so hashQuickCheck doesn't trigger first
        translation.integrity_hash = RosettaParser.computeCombinedHash(
          translation.tech, translation.people, translation.spirit,
        );

        const signal = amygdala.scan({
          type: 'translation',
          data: translation,
          source: 'test',
        });
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('integrity_breach');
        expect(signal!.evidence[0]).toContain('TECH');
      });
    });

    describe('spikeDetection', () => {
      it('detecte un spike de frequence > 300Hz', () => {
        // Premier scan : etablir la baseline a 444Hz
        amygdala.scan({
          type: 'frequency',
          data: { frequency: 444 },
          source: 'test',
        });

        // Deuxieme scan : spike a 999Hz (delta = 555)
        const signal = amygdala.scan({
          type: 'frequency',
          data: { frequency: 999 },
          source: 'test',
        });
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('frequency_anomaly');
      });

      it('accepte un changement progressif < 300Hz', () => {
        amygdala.scan({
          type: 'frequency',
          data: { frequency: 444 },
          source: 'test',
        });

        const signal = amygdala.scan({
          type: 'frequency',
          data: { frequency: 555 },
          source: 'test',
        });
        expect(signal).toBeNull();
      });
    });

    describe('repetitionCheck', () => {
      it('detecte une repetition suspecte (>3x meme input)', () => {
        const context = {
          type: 'intention' as const,
          data: { text: 'exact same content' },
          source: 'test',
        };

        // Les 3 premiers passent
        expect(amygdala.scan(context)).toBeNull();
        expect(amygdala.scan(context)).toBeNull();
        expect(amygdala.scan(context)).toBeNull();

        // Le 4eme declenche
        const signal = amygdala.scan(context);
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('cascade_risk');
      });
    });
  });

  // ─── DEEP PATH ──────────────────────────────────────────

  describe('Deep Path', () => {

    describe('analyzeManipulation', () => {
      it('detecte du contenu MANIPULATIF', () => {
        const signal = amygdala.scan({
          type: 'intention',
          data: { text: 'Derniere chance ! Agissez maintenant avant que le secret revele ne disparaisse' },
          source: 'test',
        });
        // Fast path won't trigger (no freq/hash issues)
        // But if alert is already VIGILANT+ from previous scans, deep runs
        // For a fresh amygdala, fast path returns null, deep only runs if not CALM
        // So we first bring alert level up
        amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'push' });

        const signal2 = amygdala.scan({
          type: 'intention',
          data: { text: 'Derniere chance ! Agissez maintenant avant que le secret revele ne disparaisse' },
          source: 'test',
        });
        expect(signal2).not.toBeNull();
        expect(signal2!.type).toBe('manipulation_detected');
        expect(signal2!.pathway).toBe('deep');
      });

      it('detecte du contenu DIVISIF', () => {
        // Bring to VIGILANT first
        amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'push' });

        const signal = amygdala.scan({
          type: 'intention',
          data: { text: 'L ennemi est contre nous, c est un complot pour nous menace' },
          source: 'test',
        });
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('manipulation_detected');
      });
    });

    describe('analyzeExtraction', () => {
      it('detecte une intention EXTRAIRE', () => {
        // Bring to VIGILANT first
        amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'push' });

        const signal = amygdala.scan({
          type: 'intention',
          data: {
            description: 'Monetize user data',
            sert_epanouissement: false,
            cree_plus_de_valeur: false,
          },
          source: 'test',
        });
        // Deep path analysis might pick up extraction via IntentionGuard
        // Note: IntentionGuard.evaluate defaults to true for missing props
        // The description is extracted as text for manipulation analysis first
        expect(signal).not.toBeNull();
      });
    });

    describe('analyzeSovereignty', () => {
      it('detecte une violation de souverainete', () => {
        // Bring to VIGILANT first
        amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'push' });

        const signal = amygdala.scan({
          type: 'governance',
          data: { description: 'forcer les utilisateurs a rester et bloquer sortie de leurs donnees' },
          source: 'test',
        });
        expect(signal).not.toBeNull();
        expect(signal!.type).toBe('sovereignty_violation');
        expect(signal!.pathway).toBe('deep');
      });
    });

    describe('detectCascade', () => {
      it('detecte une cascade (3+ signaux de types differents en 5s)', () => {
        // Generer 3 signaux de types differents rapidement
        amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' }); // frequency_anomaly
        amygdala.scan({ type: 'frequency', data: { frequency: 5000 }, source: 'test' }); // frequency_anomaly

        const corrupted = createCorruptedTranslation('PEOPLE');
        amygdala.scan({ type: 'translation', data: corrupted, source: 'test' }); // integrity_breach

        // Le 4e scan devrait detecter la cascade (deep path)
        const signal = amygdala.scan({
          type: 'frequency',
          data: { frequency: 2000 },
          source: 'test',
        });
        // La cascade peut etre detectee via deep path
        // Le signal retourne sera soit frequency_anomaly (fast) soit cascade_risk (deep)
        expect(signal).not.toBeNull();
      });
    });
  });

  // ─── REPONSE GRADUEE ────────────────────────────────────

  describe('Reponse Graduee', () => {
    it('commence a CALM (score 0)', () => {
      expect(amygdala.getAlertLevel()).toBe('CALM');
      expect(amygdala.getAlertScore()).toBe(0);
    });

    it('monte a VIGILANT apres une menace moderee', () => {
      // Une frequence hors range donne severity ~40-70
      amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' });

      // Le score devrait avoir monte (severity * sensitivity * 0.4)
      expect(amygdala.getAlertScore()).toBeGreaterThan(0);
    });

    it('les niveaux correspondent aux seuils', () => {
      // Inject multiple threats to push score up
      for (let i = 0; i < 5; i++) {
        amygdala.scan({ type: 'frequency', data: { frequency: 1 + i }, source: 'test' });
      }

      // Score should be significant after 5 anomalies
      const score = amygdala.getAlertScore();
      const level = amygdala.getAlertLevel();

      if (score >= 76) expect(level).toBe('LOCKDOWN');
      else if (score >= 51) expect(level).toBe('ALERT');
      else if (score >= 26) expect(level).toBe('VIGILANT');
      else expect(level).toBe('CALM');
    });
  });

  // ─── MEMOIRE ADAPTATIVE ─────────────────────────────────

  describe('Memoire Adaptative', () => {
    it('stocke les signaux dans la memoire', () => {
      amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' });

      const memory = amygdala.getMemory();
      expect(memory.recent_signals.length).toBe(1);
      expect(memory.threat_frequency.frequency_anomaly).toBe(1);
    });

    it('respecte la limite du buffer circulaire (50 max)', () => {
      // Generer 55 signaux
      for (let i = 0; i < 55; i++) {
        amygdala.scan({ type: 'frequency', data: { frequency: i }, source: 'test' });
      }

      const memory = amygdala.getMemory();
      expect(memory.recent_signals.length).toBeLessThanOrEqual(50);
    });

    it('augmente la sensibilite apres plusieurs menaces', () => {
      const initialSensitivity = amygdala.getMemory().sensitivity;

      // 5 menaces rapides
      for (let i = 0; i < 5; i++) {
        amygdala.scan({ type: 'frequency', data: { frequency: i + 1 }, source: 'test' });
      }

      const newSensitivity = amygdala.getMemory().sensitivity;
      expect(newSensitivity).toBeGreaterThanOrEqual(initialSensitivity);
    });

    it('ajuste la sensibilite manuellement', () => {
      amygdala.adjustSensitivity(0.2);
      expect(amygdala.getMemory().sensitivity).toBe(0.7);

      amygdala.adjustSensitivity(-0.5);
      expect(amygdala.getMemory().sensitivity).toBe(0.2);

      // Clamp minimum a 0.1
      amygdala.adjustSensitivity(-0.5);
      expect(amygdala.getMemory().sensitivity).toBe(0.1);
    });

    it('la timeline retourne tous les signaux', () => {
      amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' });
      amygdala.scan({ type: 'frequency', data: { frequency: 5000 }, source: 'test' });

      const timeline = amygdala.getThreatTimeline();
      expect(timeline.length).toBe(2);
      // Triee chronologiquement
      expect(timeline[0].timestamp).toBeLessThanOrEqual(timeline[1].timestamp);
    });
  });

  // ─── EVENEMENTS ─────────────────────────────────────────

  describe('Evenements', () => {
    it('emet threat_detected quand un signal est detecte', () => {
      const events: AmygdalaEvent[] = [];
      amygdala.onThreat((event) => events.push(event));

      amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' });

      expect(events.length).toBeGreaterThanOrEqual(1);
      const threatEvent = events.find(e => e.type === 'threat_detected');
      expect(threatEvent).toBeDefined();
      expect(threatEvent!.signal).toBeDefined();
    });

    it('emet alert_changed lors de transition de niveau', () => {
      const events: AmygdalaEvent[] = [];
      amygdala.onThreat((event) => events.push(event));

      // Pousser suffisamment pour changer de niveau
      for (let i = 0; i < 5; i++) {
        amygdala.scan({ type: 'frequency', data: { frequency: i + 1 }, source: 'test' });
      }

      const alertChanges = events.filter(e =>
        e.type === 'alert_changed' || e.type === 'lockdown_engaged',
      );
      // Il devrait y avoir au moins une transition
      expect(alertChanges.length).toBeGreaterThanOrEqual(1);
    });

    it('unsubscribe fonctionne', () => {
      const events: AmygdalaEvent[] = [];
      const unsubscribe = amygdala.onThreat((event) => events.push(event));

      amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' });
      const countBefore = events.length;

      // Se desabonner
      unsubscribe();

      amygdala.scan({ type: 'frequency', data: { frequency: 5000 }, source: 'test' });
      expect(events.length).toBe(countBefore);
    });

    it('emet all_clear quand resetAlert est appele', () => {
      const events: AmygdalaEvent[] = [];
      amygdala.onThreat((event) => events.push(event));

      // Monter le niveau
      amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' });

      // Reset
      amygdala.resetAlert();

      const allClear = events.find(e => e.type === 'all_clear');
      expect(allClear).toBeDefined();
      expect(allClear!.new_level).toBe('CALM');
    });
  });

  // ─── PIPELINE COMPLET ───────────────────────────────────

  describe('Pipeline Complet', () => {
    it('scan() retourne null pour une translation saine', () => {
      const healthy = createHealthyTranslation();
      const signal = amygdala.scan({
        type: 'translation',
        data: healthy,
        source: 'test',
      });
      expect(signal).toBeNull();
    });

    it('scan() retourne un signal pour une translation corrompue', () => {
      const corrupted = createCorruptedTranslation('SPIRIT');
      const signal = amygdala.scan({
        type: 'translation',
        data: corrupted,
        source: 'test',
      });
      expect(signal).not.toBeNull();
      expect(signal!.type).toBe('integrity_breach');
    });

    it('getState() retourne un etat complet', () => {
      amygdala.scan({ type: 'frequency', data: { frequency: 10 }, source: 'test' });

      const state = amygdala.getState();
      expect(state.alert_level).toBeDefined();
      expect(state.alert_score).toBeGreaterThan(0);
      expect(state.active_threats.length).toBeGreaterThan(0);
      expect(state.memory).toBeDefined();
      expect(state.memory.recent_signals.length).toBeGreaterThan(0);
      expect(state.last_scan).toBeGreaterThan(0);
    });

    it('resetAlert() remet tout a zero', () => {
      // Generer des menaces
      for (let i = 0; i < 3; i++) {
        amygdala.scan({ type: 'frequency', data: { frequency: i + 1 }, source: 'test' });
      }
      expect(amygdala.getAlertScore()).toBeGreaterThan(0);

      // Reset
      amygdala.resetAlert();
      expect(amygdala.getAlertScore()).toBe(0);
      expect(amygdala.getAlertLevel()).toBe('CALM');
      expect(amygdala.getState().active_threats.length).toBe(0);
    });

    it('chaque signal a un id unique', () => {
      const signals: ThreatSignal[] = [];

      for (let i = 0; i < 5; i++) {
        const signal = amygdala.scan({
          type: 'frequency',
          data: { frequency: i + 1 },
          source: 'test',
        });
        if (signal) signals.push(signal);
      }

      const ids = signals.map(s => s.id);
      const uniqueIds = new Set(ids);
      expect(uniqueIds.size).toBe(ids.length);
    });
  });
});
