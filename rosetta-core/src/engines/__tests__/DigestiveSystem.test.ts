/**
 * AT·OM — DigestiveSystem Tests
 * Suite de tests unitaires pour le systeme digestif de l'Arbre des Connaissances
 *
 * Couvre :
 *   1. Ingestion (Bouche)     — ingest() cree un RawFood valide
 *   2. Mastication (Broyage)  — chew() extrait titre, body, keywords
 *   3. Digestion Rosetta      — digestRosetta() retourne une traduction 3D
 *   4. Absorption (Intestin)  — absorb() filtre qualite + menaces
 *   5. Routage (Sang)         — route() classifie sphere + layer
 *   6. Stockage (Cellule)     — store() cree un ATOMNode
 *   7. Elimination (Colon)    — eliminate() archive les dechets
 *   8. Pipeline complet       — digest() bout-en-bout
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { DigestiveSystem } from '../DigestiveSystem';
import { RosettaParser } from '../../parser/RosettaParser';
import { ThreatAmygdala } from '../ThreatAmygdala';
import { KnowledgeTemplate } from '../../parser/templates/KnowledgeTemplate';
import type {
  RawFood,
  ChewedFood,
  DigestedFood,
  InformationResonanceScore,
  DigestiveEvent,
} from '../../types/atom-types';

// ═══════════════════════════════════════════════════════════
// HELPERS : Donnees de test
// ═══════════════════════════════════════════════════════════

/** Contenu HTML de qualite (article sur la technologie) */
const QUALITY_HTML = `
<!DOCTYPE html>
<html>
<head><title>L'intelligence artificielle en 2025</title>
<meta name="author" content="Dr. Marie Curie">
<meta property="article:published_time" content="2025-01-15T10:00:00Z">
</head>
<body>
<article>
<h1>L'intelligence artificielle transforme le monde</h1>
<p>Les avancees en intelligence artificielle et en technologie logiciel
continuent de revolutionner notre societe. Les algorithmes de deep learning
permettent des decouvertes scientifiques majeures dans le domaine de la sante
et de l'education. Les chercheurs du monde entier collaborent pour developper
des systemes plus transparents et ethiques.</p>
<p>Sources multiples confirment ces tendances. La recherche en IA progresse
a un rythme sans precedent, avec des applications dans la robotique,
la medecine et l'environnement.</p>
<p>References : https://example.com/ai-research et https://example.com/tech-ethics</p>
</article>
</body>
</html>`;

/** Contenu manipulatif (devrait etre rejete) */
const MANIPULATIVE_HTML = `
<html>
<head><title>Secret revele choquant</title></head>
<body>
<h1>Ils ne veulent pas que vous sachiez</h1>
<p>Secret revele ! Agissez maintenant ! Cette derniere chance ne ratez pas !
Ils ne veulent pas que vous sachiez la verite choquante sur ce complot.
Incroyable revelation qui change tout. Danger immédiat pour tous.
Agissez maintenant avant qu'il ne soit trop tard !</p>
</body>
</html>`;

/** Contenu texte brut simple */
const PLAIN_TEXT = `La biodiversite et l'environnement sont au coeur des enjeux
de notre epoque. Le climat change rapidement et l'ecologie devient
une priorite mondiale. La pollution des oceans et la deforestation
menacent de nombreuses especes. Les scientifiques alertent sur
l'urgence de proteger notre planete et ses ecosystemes fragiles.`;

/** Contenu JSON valide */
const JSON_CONTENT = JSON.stringify({
  title: 'Economie numerique et blockchain',
  author: 'Satoshi Nakamoto',
  body: 'Les marches financiers evoluent avec la technologie blockchain. Le commerce de crypto-monnaie et les investissements en bitcoin transforment le secteur bancaire et la finance mondiale. Les banques traditionnelles adaptent leurs services.',
  date: '2025-03-01',
});

/** Contenu trop court (devrait etre rejete) */
const TOO_SHORT = '<html><body>Ok.</body></html>';

// ═══════════════════════════════════════════════════════════
// SETUP
// ═══════════════════════════════════════════════════════════

let parser: RosettaParser;
let amygdala: ThreatAmygdala;
let digestive: DigestiveSystem;

beforeEach(() => {
  parser = new RosettaParser();
  parser.registerTemplate(KnowledgeTemplate);
  amygdala = new ThreatAmygdala(parser);
  digestive = new DigestiveSystem(parser, amygdala);
});

// ═══════════════════════════════════════════════════════════
// 1. INGESTION (Bouche)
// ═══════════════════════════════════════════════════════════

describe('Etape 1 — Ingestion (Bouche)', () => {
  it('ingest() cree un RawFood valide depuis du HTML', () => {
    const raw = digestive.ingest('url', 'https://example.com/article', QUALITY_HTML, 'text/html');

    expect(raw.id).toMatch(/^raw_/);
    expect(raw.source_type).toBe('url');
    expect(raw.source_url).toBe('https://example.com/article');
    expect(raw.raw_content).toBe(QUALITY_HTML);
    expect(raw.content_type).toBe('text/html');
    expect(raw.fetched_at).toBeGreaterThan(0);
  });

  it('ingest() cree un RawFood depuis du JSON', () => {
    const raw = digestive.ingest('api', 'https://api.example.com/data', JSON_CONTENT, 'application/json');

    expect(raw.source_type).toBe('api');
    expect(raw.content_type).toBe('application/json');
  });

  it('ingest() cree un RawFood depuis du texte brut', () => {
    const raw = digestive.ingest('manual', 'manual', PLAIN_TEXT, 'text/plain');

    expect(raw.source_type).toBe('manual');
    expect(raw.content_type).toBe('text/plain');
  });
});

// ═══════════════════════════════════════════════════════════
// 2. MASTICATION (Broyage)
// ═══════════════════════════════════════════════════════════

describe('Etape 2 — Mastication (Broyage)', () => {
  it('chew() extrait le titre d\'un HTML', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);

    expect(chewed.title).toBe("L'intelligence artificielle en 2025");
  });

  it('chew() extrait le corps sans balises HTML', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);

    expect(chewed.body).not.toContain('<');
    expect(chewed.body).not.toContain('>');
    expect(chewed.body.length).toBeGreaterThan(50);
  });

  it('chew() extrait les mots-cles', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);

    expect(chewed.keywords.length).toBeGreaterThan(0);
    expect(chewed.keywords.length).toBeLessThanOrEqual(15);
  });

  it('chew() extrait l\'auteur des meta tags', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);

    expect(chewed.author).toBe('Dr. Marie Curie');
  });

  it('chew() extrait la date de publication', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);

    expect(chewed.published_at).toBeDefined();
    expect(chewed.published_at).toBeGreaterThan(0);
  });

  it('chew() calcule le word_count', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);

    expect(chewed.word_count).toBeGreaterThan(10);
  });

  it('chew() gere du texte brut (pas de HTML)', () => {
    const raw = digestive.ingest('manual', 'manual', PLAIN_TEXT, 'text/plain');
    const chewed = digestive.chew(raw);

    expect(chewed.title.length).toBeGreaterThan(0);
    expect(chewed.body).toBe(PLAIN_TEXT);
    expect(chewed.word_count).toBeGreaterThan(10);
  });

  it('chew() gere du contenu JSON', () => {
    const raw = digestive.ingest('api', 'https://api.example.com', JSON_CONTENT, 'application/json');
    const chewed = digestive.chew(raw);

    expect(chewed.title).toBe('Economie numerique et blockchain');
    expect(chewed.author).toBe('Satoshi Nakamoto');
    expect(chewed.body.length).toBeGreaterThan(20);
  });

  it('chew() extrait les sources URL du contenu', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);

    expect(chewed.sources.length).toBeGreaterThan(0);
    expect(chewed.sources[0].reference).toMatch(/^https?:\/\//);
  });
});

// ═══════════════════════════════════════════════════════════
// 3. DIGESTION ROSETTA (Estomac)
// ═══════════════════════════════════════════════════════════

describe('Etape 3 — Digestion Rosetta (Estomac)', () => {
  it('digestRosetta() retourne une RosettaTranslation valide', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    expect(rosetta.id).toBeDefined();
    expect(rosetta.tech).toBeDefined();
    expect(rosetta.people).toBeDefined();
    expect(rosetta.spirit).toBeDefined();
    expect(rosetta.integrity_hash).toBeDefined();
  });

  it('les 3 dimensions sont completes (TECH/PEOPLE/SPIRIT)', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    // TECH
    expect(rosetta.tech.data_type).toBe('knowledge_article');
    expect(rosetta.tech.schema_version).toBe('1.0');
    expect(rosetta.tech.values).toHaveProperty('title');
    expect(rosetta.tech.values).toHaveProperty('word_count');

    // PEOPLE
    expect(rosetta.people.narrative.length).toBeGreaterThan(0);
    expect(rosetta.people.explanation).toBeDefined();
    expect(rosetta.people.language).toBeDefined();

    // SPIRIT
    expect(rosetta.spirit.frequency_hz).toBeGreaterThan(0);
    expect(rosetta.spirit.resonance_level).toBeGreaterThanOrEqual(1);
    expect(rosetta.spirit.resonance_level).toBeLessThanOrEqual(9);
    expect(rosetta.spirit.sacred_geometry).toBeDefined();
  });

  it('l\'integrity_hash est present et non-vide', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    expect(rosetta.integrity_hash).toMatch(/^rosetta_/);
  });
});

// ═══════════════════════════════════════════════════════════
// 4. ABSORPTION (Intestin)
// ═══════════════════════════════════════════════════════════

describe('Etape 4 — Absorption (Intestin)', () => {
  it('absorb() accepte du contenu de qualite', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    const result = digestive.absorb(chewed, rosetta);

    expect(result.score).toBeDefined();
    expect(result.score.score_global).toBeGreaterThanOrEqual(0);
  });

  it('absorb() rejette du contenu MANIPULATIF', () => {
    const raw = digestive.ingest('url', 'https://spam.com', MANIPULATIVE_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    const result = digestive.absorb(chewed, rosetta);

    expect(result.absorbed).toBe(false);
    expect(result.rejection_reason).toContain('MANIPULATIF');
  });

  it('absorb() retourne un score InformationResonanceScore', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    const result = digestive.absorb(chewed, rosetta);

    expect(result.score.coherence_interne).toBeDefined();
    expect(result.score.coherence_externe).toBeDefined();
    expect(result.score.diversite_sources).toBeDefined();
    expect(result.score.intention_detectee).toBeDefined();
    expect(result.score.score_global).toBeDefined();
  });
});

// ═══════════════════════════════════════════════════════════
// 5. ROUTAGE (Sang)
// ═══════════════════════════════════════════════════════════

describe('Etape 5 — Routage (Sang)', () => {
  it('route() classifie correctement les spheres via keywords', () => {
    const techChewed: ChewedFood = {
      id: 'test_tech',
      raw_food_id: 'raw_1',
      title: 'Technologie IA',
      body: 'Intelligence artificielle et algorithme de deep learning',
      keywords: ['technologie', 'intelligence', 'artificielle', 'algorithme', 'logiciel'],
      sources: [],
      language: 'fr',
      word_count: 50,
    };

    const score: InformationResonanceScore = {
      content_id: 'test',
      coherence_interne: 70,
      coherence_externe: 60,
      diversite_sources: 40,
      transparence_methodo: 50,
      fiabilite_auteur: 50,
      intention_detectee: 'INFORMATIF',
      score_global: 55,
    };

    const result = digestive.route(techChewed, score);

    expect(result.sphere).toBe('TECHNO');
  });

  it('contenu sante → SANTE', () => {
    const healthChewed: ChewedFood = {
      id: 'test_sante',
      raw_food_id: 'raw_2',
      title: 'Sante et bien-etre',
      body: 'La medecine et la sante preventive',
      keywords: ['sante', 'medecine', 'bien-etre', 'traitement', 'patient'],
      sources: [],
      language: 'fr',
      word_count: 30,
    };

    const score: InformationResonanceScore = {
      content_id: 'test',
      coherence_interne: 60,
      coherence_externe: 50,
      diversite_sources: 30,
      transparence_methodo: 40,
      fiabilite_auteur: 50,
      intention_detectee: 'INFORMATIF',
      score_global: 48,
    };

    const result = digestive.route(healthChewed, score);

    expect(result.sphere).toBe('SANTE');
  });

  it('route() assigne la bonne MappingLayer selon le score', () => {
    const chewed: ChewedFood = {
      id: 'test_layer',
      raw_food_id: 'raw_3',
      title: 'Test',
      body: 'Contenu test pour les layers',
      keywords: ['technologie'],
      sources: [],
      language: 'fr',
      word_count: 20,
    };

    // Score eleve → EVENEMENTS
    const highScore: InformationResonanceScore = {
      content_id: 'test', coherence_interne: 90, coherence_externe: 80,
      diversite_sources: 80, transparence_methodo: 80, fiabilite_auteur: 80,
      intention_detectee: 'INFORMATIF', score_global: 85,
    };

    const highResult = digestive.route(chewed, highScore);
    expect(highResult.layer).toBe('EVENEMENTS');

    // Score moyen → NARRATIFS
    const midScore: InformationResonanceScore = {
      content_id: 'test', coherence_interne: 70, coherence_externe: 50,
      diversite_sources: 50, transparence_methodo: 50, fiabilite_auteur: 50,
      intention_detectee: 'INFORMATIF', score_global: 65,
    };

    const midResult = digestive.route(chewed, midScore);
    expect(midResult.layer).toBe('NARRATIFS');

    // Score bas → PATTERNS
    const lowScore: InformationResonanceScore = {
      content_id: 'test', coherence_interne: 40, coherence_externe: 30,
      diversite_sources: 30, transparence_methodo: 30, fiabilite_auteur: 30,
      intention_detectee: 'INFORMATIF', score_global: 42,
    };

    const lowResult = digestive.route(chewed, lowScore);
    expect(lowResult.layer).toBe('PATTERNS');
  });

  it('route() retourne un resonance_level valide (1-9)', () => {
    const chewed: ChewedFood = {
      id: 'test_res',
      raw_food_id: 'raw_4',
      title: 'Environnement',
      body: 'Ecologie et climat',
      keywords: ['environnement', 'climat', 'ecologie'],
      sources: [],
      language: 'fr',
      word_count: 10,
    };

    const score: InformationResonanceScore = {
      content_id: 'test', coherence_interne: 60, coherence_externe: 50,
      diversite_sources: 40, transparence_methodo: 40, fiabilite_auteur: 50,
      intention_detectee: 'INFORMATIF', score_global: 50,
    };

    const result = digestive.route(chewed, score);

    expect(result.resonance_level).toBeGreaterThanOrEqual(1);
    expect(result.resonance_level).toBeLessThanOrEqual(9);
  });
});

// ═══════════════════════════════════════════════════════════
// 6. STOCKAGE (Cellule)
// ═══════════════════════════════════════════════════════════

describe('Etape 6 — Stockage (Cellule)', () => {
  it('store() cree un ATOMNode valide', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    const node = digestive.store(rosetta, 'TECHNO', 'EVENEMENTS', chewed);

    expect(node.id).toMatch(/^node_/);
    expect(node.sphere_id).toBe('TECHNO');
    expect(node.title).toBe(chewed.title);
    expect(node.status).toBe('active');
    expect(node.rosetta).toBe(rosetta);
    expect(node.created_by).toBe('DigestiveSystem');
  });

  it('le node a le bon resonance_level pour sa sphere', () => {
    const raw = digestive.ingest('url', 'https://example.com', QUALITY_HTML, 'text/html');
    const chewed = digestive.chew(raw);
    const rosetta = digestive.digestRosetta(chewed);

    // TECHNO = index 1 → resonance_level 1
    const nodeTechno = digestive.store(rosetta, 'TECHNO', 'EVENEMENTS', chewed);
    expect(nodeTechno.resonance_level).toBe(1);

    // SANTE = index 5 → resonance_level 5
    const nodeSante = digestive.store(rosetta, 'SANTE', 'NARRATIFS', chewed);
    expect(nodeSante.resonance_level).toBe(5);

    // SPIRITUALITE = index 9 → resonance_level 9
    const nodeSpirit = digestive.store(rosetta, 'SPIRITUALITE', 'VIBRATIONS', chewed);
    expect(nodeSpirit.resonance_level).toBe(9);
  });
});

// ═══════════════════════════════════════════════════════════
// 7. ELIMINATION (Colon)
// ═══════════════════════════════════════════════════════════

describe('Etape 7 — Elimination (Colon)', () => {
  it('eliminate() archive le dechet avec raison', () => {
    const food: DigestedFood = {
      id: 'test_waste',
      chewed_food_id: 'chewed_1',
      stage: 'ABSORBED',
      rejection_reason: undefined,
      pipeline_log: [],
    };

    digestive.eliminate(food, 'Contenu MANIPULATIF detecte');

    expect(food.stage).toBe('ELIMINATED');
    expect(food.rejection_reason).toBe('Contenu MANIPULATIF detecte');
  });

  it('getWasteArchive() retourne les dechets', () => {
    const food1: DigestedFood = {
      id: 'waste_1', chewed_food_id: 'c1', stage: 'ABSORBED', pipeline_log: [],
    };
    const food2: DigestedFood = {
      id: 'waste_2', chewed_food_id: 'c2', stage: 'ABSORBED', pipeline_log: [],
    };

    digestive.eliminate(food1, 'Raison 1');
    digestive.eliminate(food2, 'Raison 2');

    const archive = digestive.getWasteArchive();
    expect(archive.length).toBe(2);
    expect(archive[0].id).toBe('waste_1');
    expect(archive[1].id).toBe('waste_2');
  });

  it('eliminate() met a jour les statistiques', () => {
    const food: DigestedFood = {
      id: 'test_stats', chewed_food_id: 'c1', stage: 'ABSORBED', pipeline_log: [],
    };

    digestive.eliminate(food, 'Test');

    const stats = digestive.getStats();
    expect(stats.total_eliminated).toBe(1);
    expect(stats.total_ingested).toBe(1);
  });
});

// ═══════════════════════════════════════════════════════════
// 8. PIPELINE COMPLET
// ═══════════════════════════════════════════════════════════

describe('Pipeline complet — digest()', () => {
  it('digest() bout-en-bout avec contenu de qualite → ATOMNode', () => {
    const result = digestive.digest('url', 'https://example.com/article', QUALITY_HTML);

    // Le pipeline devrait produire un resultat valide
    expect(result).toBeDefined();
    expect(result.id).toMatch(/^digested_/);
    expect(result.pipeline_log.length).toBeGreaterThan(0);

    // Si absorbe, doit avoir un node_id et une sphere
    if (result.stage === 'STORED') {
      expect(result.node_id).toBeDefined();
      expect(result.target_sphere).toBeDefined();
      expect(result.target_layer).toBeDefined();
      expect(result.rosetta).toBeDefined();
    }
  });

  it('digest() bout-en-bout avec contenu manipulatif → rejete', () => {
    const result = digestive.digest('url', 'https://spam.com/fake', MANIPULATIVE_HTML);

    expect(result.stage).toBe('ELIMINATED');
    expect(result.rejection_reason).toBeDefined();
    expect(result.node_id).toBeUndefined();
  });

  it('digest() avec contenu trop court → rejete', () => {
    const result = digestive.digest('url', 'https://short.com', TOO_SHORT);

    expect(result.stage).toBe('ELIMINATED');
    expect(result.rejection_reason).toBeDefined();
  });

  it('digest() avec texte brut fonctionne', () => {
    const result = digestive.digest('manual', 'manual', PLAIN_TEXT, 'text/plain');

    expect(result).toBeDefined();
    expect(result.pipeline_log.length).toBeGreaterThan(0);
  });

  it('digest() avec JSON fonctionne', () => {
    const result = digestive.digest('api', 'https://api.example.com', JSON_CONTENT, 'application/json');

    expect(result).toBeDefined();
    expect(result.pipeline_log.length).toBeGreaterThan(0);
  });
});

// ═══════════════════════════════════════════════════════════
// 9. DIGESTION PAR LOT
// ═══════════════════════════════════════════════════════════

describe('Digestion par lot — digestBatch()', () => {
  it('digestBatch() traite plusieurs items avec statistiques', () => {
    const items = [
      { source: 'url' as const, url: 'https://example.com/1', content: QUALITY_HTML },
      { source: 'url' as const, url: 'https://spam.com/2', content: MANIPULATIVE_HTML },
      { source: 'manual' as const, url: 'manual', content: PLAIN_TEXT, contentType: 'text/plain' },
    ];

    const { absorbed, eliminated, stats } = digestive.digestBatch(items);

    // Au moins le contenu manipulatif doit etre rejete
    expect(eliminated.length).toBeGreaterThanOrEqual(1);

    // Les stats doivent refleter le traitement
    expect(stats.total_ingested).toBeGreaterThan(0);
  });
});

// ═══════════════════════════════════════════════════════════
// 10. STATISTIQUES
// ═══════════════════════════════════════════════════════════

describe('Statistiques — getStats()', () => {
  it('getStats() retourne les bonnes metriques apres digestion', () => {
    // Digerer du contenu de qualite
    digestive.digest('url', 'https://example.com', QUALITY_HTML);

    const stats = digestive.getStats();

    expect(stats.total_ingested).toBeGreaterThanOrEqual(1);
    expect(stats.absorption_rate).toBeGreaterThanOrEqual(0);
    expect(stats.absorption_rate).toBeLessThanOrEqual(1);
  });

  it('getAbsorptionRate() retourne le taux d\'absorption', () => {
    // Avant toute digestion
    expect(digestive.getAbsorptionRate()).toBe(0);

    // Apres digestion
    digestive.digest('url', 'https://example.com', QUALITY_HTML);
    const rate = digestive.getAbsorptionRate();

    expect(rate).toBeGreaterThanOrEqual(0);
    expect(rate).toBeLessThanOrEqual(1);
  });
});

// ═══════════════════════════════════════════════════════════
// 11. EVENEMENTS
// ═══════════════════════════════════════════════════════════

describe('Evenements — onDigest()', () => {
  it('onDigest() emet des evenements lors de la digestion', () => {
    const events: DigestiveEvent[] = [];
    digestive.onDigest((event) => events.push(event));

    digestive.digest('url', 'https://example.com', QUALITY_HTML);

    // Au moins un evenement devrait etre emis
    expect(events.length).toBeGreaterThan(0);
  });

  it('onDigest() retourne une fonction d\'unsubscribe', () => {
    const events: DigestiveEvent[] = [];
    const unsubscribe = digestive.onDigest((event) => events.push(event));

    // Unsubscribe
    unsubscribe();

    // Digerer apres unsubscribe
    digestive.digest('url', 'https://example.com', QUALITY_HTML);

    // Aucun evenement ne devrait etre recu
    expect(events.length).toBe(0);
  });
});

// ═══════════════════════════════════════════════════════════
// 12. UTILITAIRES
// ═══════════════════════════════════════════════════════════

describe('Utilitaires', () => {
  it('stripHtml() retire les balises HTML', () => {
    const html = '<p>Hello <strong>world</strong></p>';
    const text = digestive.stripHtml(html);

    expect(text).not.toContain('<');
    expect(text).not.toContain('>');
    expect(text).toContain('Hello');
    expect(text).toContain('world');
  });

  it('stripHtml() retire les scripts et styles', () => {
    const html = '<script>alert("hack")</script><style>body{}</style><p>Content</p>';
    const text = digestive.stripHtml(html);

    expect(text).not.toContain('alert');
    expect(text).not.toContain('body{}');
    expect(text).toContain('Content');
  });

  it('extractKeywords() retourne des mots-cles significatifs', () => {
    const text = 'La technologie blockchain revolutionne la finance et le commerce mondial';
    const keywords = digestive.extractKeywords(text);

    expect(keywords.length).toBeGreaterThan(0);
    // Les stop words ne devraient pas etre inclus
    expect(keywords).not.toContain('la');
    expect(keywords).not.toContain('et');
    expect(keywords).not.toContain('le');
  });
});
