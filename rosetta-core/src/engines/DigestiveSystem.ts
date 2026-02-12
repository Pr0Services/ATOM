/**
 * AT·OM — DigestiveSystem
 * Le Système Digestif de l'Arbre des Connaissances
 *
 * "L'arbre ne pousse pas de l'extérieur — il digère la lumière."
 *
 * Chaque donnée Internet entre comme "nourriture brute" et ressort
 * soit comme NUTRIMENT (ATOMNode dans l'Arbre des Connaissances)
 * soit comme DÉCHET (rejeté avec traçabilité complète).
 *
 * Pipeline en 7 étapes biologiques :
 *
 *   👄 BOUCHE (Ingestion)     → Fetch + parse depuis URL/RSS/API
 *   🦷 MASTICATION (Broyage)  → Décomposer en morceaux structurés
 *   🫁 ESTOMAC (Digestion)    → Traduire en 3D Rosetta via KnowledgeTemplate
 *   🧪 INTESTIN (Absorption)  → InformationFilter + ThreatAmygdala
 *   🫀 SANG (Distribution)    → Router vers Sphère + MappingLayer
 *   🧬 CELLULE (Stockage)     → Créer ATOMNode dans l'Arbre
 *   🚽 CÔLON (Élimination)    → Rejeter le bruit avec traçabilité
 */

import type {
  FoodSource,
  DigestionStage,
  RawFood,
  ChewedFood,
  DigestedFood,
  DigestiveLogEntry,
  DigestiveStats,
  DigestiveEvent,
  RosettaTranslation,
  InformationResonanceScore,
  ThreatSignal,
  SphereId,
  MappingLayer,
  ATOMNode,
  ResonanceLevel,
} from '../types/atom-types';
import { SACRED_FREQUENCIES, RESONANCE_MATRIX, SPHERES } from '../types/atom-types';
import { RosettaParser } from '../parser/RosettaParser';
import { KnowledgeTemplate } from '../parser/templates/KnowledgeTemplate';
import { InformationFilter } from './PolishingEngine';
import { ThreatAmygdala, type ScanContext } from './ThreatAmygdala';

// ═══════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════

/** Seuil minimal de qualité pour l'absorption (0-100) */
const ABSORPTION_THRESHOLD = 40;

/** Longueur minimale de contenu pour être mâché (en caractères) */
const MIN_CONTENT_LENGTH = 20;

/** Nombre maximum de mots-clés extraits */
const MAX_KEYWORDS = 15;

/** Taille de l'archive de déchets */
const MAX_WASTE_ARCHIVE = 200;

// ── Classification Sphère — mots-clés → sphère ──────────

const SPHERE_KEYWORDS: Record<SphereId, string[]> = {
  TECHNO:        ['technologie', 'logiciel', 'ia', 'intelligence artificielle', 'algorithme', 'code', 'données', 'robot', 'informatique', 'numérique', 'software', 'hardware', 'tech', 'digital'],
  POLITIQUE:     ['politique', 'gouvernement', 'loi', 'élection', 'parlement', 'démocratie', 'sénat', 'république', 'président', 'vote', 'citoyen', 'constitution'],
  ECONOMIE:      ['économie', 'marché', 'finance', 'monnaie', 'commerce', 'banque', 'pib', 'bourse', 'investissement', 'crypto', 'blockchain', 'bitcoin'],
  EDUCATION:     ['éducation', 'école', 'université', 'formation', 'apprentissage', 'cours', 'enseignement', 'professeur', 'étudiant', 'savoir', 'pédagogie'],
  SANTE:         ['santé', 'médecine', 'hôpital', 'maladie', 'traitement', 'bien-être', 'docteur', 'patient', 'thérapie', 'nutrition', 'fitness'],
  CULTURE:       ['culture', 'art', 'musique', 'cinéma', 'littérature', 'théâtre', 'musée', 'peinture', 'sculpture', 'danse', 'photographie'],
  ENVIRONNEMENT: ['environnement', 'climat', 'écologie', 'biodiversité', 'pollution', 'recyclage', 'énergie', 'solaire', 'forêt', 'océan', 'carbone'],
  JUSTICE:       ['justice', 'droit', 'tribunal', 'avocat', 'procès', 'constitution', 'crime', 'prison', 'police', 'légal', 'juridique'],
  SPIRITUALITE:  ['spiritualité', 'méditation', 'conscience', 'philosophie', 'sagesse', 'yoga', 'chakra', 'énergie', 'âme', 'éveil', 'harmonie'],
};

// ═══════════════════════════════════════════════════════════
// DIGESTIVE SYSTEM
// ═══════════════════════════════════════════════════════════

export class DigestiveSystem {
  private parser: RosettaParser;
  private amygdala: ThreatAmygdala | null;
  private stats: DigestiveStats;
  private wasteArchive: DigestedFood[] = [];
  private listeners: ((event: DigestiveEvent) => void)[] = [];

  constructor(parser: RosettaParser, amygdala?: ThreatAmygdala) {
    this.parser = parser;
    this.amygdala = amygdala ?? null;

    // Enregistrer le KnowledgeTemplate si pas déjà fait
    if (!parser.getTemplate('knowledge')) {
      parser.registerTemplate(KnowledgeTemplate);
    }

    this.stats = this.createEmptyStats();
  }

  // ═══════════════════════════════════════════════════════════
  // PIPELINE COMPLET — Bout en bout
  // ═══════════════════════════════════════════════════════════

  /**
   * Digère un contenu de bout en bout.
   * Retourne un DigestedFood avec toutes les étapes documentées.
   */
  digest(
    source: FoodSource,
    url: string,
    rawContent: string,
    contentType: string = 'text/html',
  ): DigestedFood {
    const log: DigestiveLogEntry[] = [];

    // ── ÉTAPE 1 : BOUCHE (Ingestion) ──
    const rawFood = this.ingest(source, url, rawContent, contentType);
    log.push({ stage: 'INGESTED', timestamp: Date.now(), passed: true, detail: `Source: ${source} | ${rawContent.length} chars` });

    // ── ÉTAPE 2 : MASTICATION (Broyage) ──
    const chewed = this.chew(rawFood);
    if (chewed.word_count < 3) {
      return this.createRejected(chewed.id, 'CHEWED', log, 'Contenu trop court après mastication');
    }
    log.push({ stage: 'CHEWED', timestamp: Date.now(), passed: true, detail: `Titre: "${chewed.title}" | ${chewed.word_count} mots | ${chewed.keywords.length} mots-clés` });

    // ── ÉTAPE 3 : ESTOMAC (Digestion Rosetta) ──
    let rosetta: RosettaTranslation;
    try {
      rosetta = this.digestRosetta(chewed);
    } catch (err) {
      return this.createRejected(chewed.id, 'DIGESTED', log, `Erreur traduction Rosetta: ${(err as Error).message}`);
    }
    log.push({ stage: 'DIGESTED', timestamp: Date.now(), passed: true, detail: `Hash: ${rosetta.integrity_hash}` });

    // ── ÉTAPE 4 : INTESTIN (Absorption) ──
    const absorption = this.absorb(chewed, rosetta);
    log.push({
      stage: 'ABSORBED',
      timestamp: Date.now(),
      passed: absorption.absorbed,
      detail: absorption.absorbed
        ? `Score: ${absorption.score.score_global}/100 | Intention: ${absorption.score.intention_detectee}`
        : `Rejeté: ${absorption.rejection_reason}`,
      score: absorption.score.score_global,
    });

    if (!absorption.absorbed) {
      const rejected = this.createRejected(
        chewed.id, 'ABSORBED', log, absorption.rejection_reason!,
      );
      rejected.information_score = absorption.score;
      rejected.threat_signal = absorption.threat ?? undefined;
      this.eliminate(rejected, absorption.rejection_reason!);
      return rejected;
    }

    // ── ÉTAPE 5 : SANG (Routage) ──
    const routing = this.route(chewed, absorption.score);
    log.push({
      stage: 'ROUTED',
      timestamp: Date.now(),
      passed: true,
      detail: `Sphère: ${routing.sphere} | Layer: ${routing.layer} | Résonance: ${routing.resonance_level}`,
    });

    // ── ÉTAPE 6 : CELLULE (Stockage) ──
    const node = this.store(rosetta, routing.sphere, routing.layer, chewed);
    log.push({
      stage: 'STORED',
      timestamp: Date.now(),
      passed: true,
      detail: `ATOMNode créé: ${node.id}`,
    });

    // Mettre à jour les statistiques
    this.stats.total_ingested++;
    this.stats.total_absorbed++;
    this.stats.top_spheres[routing.sphere] = (this.stats.top_spheres[routing.sphere] ?? 0) + 1;
    this.updateAvgScore(absorption.score.score_global);
    this.stats.absorption_rate = this.stats.total_absorbed / this.stats.total_ingested;

    const result: DigestedFood = {
      id: this.generateId('digested'),
      chewed_food_id: chewed.id,
      stage: 'STORED',
      rosetta,
      information_score: absorption.score,
      threat_signal: absorption.threat ?? undefined,
      target_sphere: routing.sphere,
      target_layer: routing.layer,
      node_id: node.id,
      pipeline_log: log,
    };

    this.notifyListeners({ type: 'food_absorbed', food: result });
    this.notifyListeners({ type: 'digestion_complete', food: result, stats: this.getStats() });

    return result;
  }

  /**
   * Digestion par lot — traite plusieurs items.
   */
  digestBatch(items: { source: FoodSource; url: string; content: string; contentType?: string }[]): {
    absorbed: DigestedFood[];
    eliminated: DigestedFood[];
    stats: DigestiveStats;
  } {
    const absorbed: DigestedFood[] = [];
    const eliminated: DigestedFood[] = [];

    for (const item of items) {
      const result = this.digest(item.source, item.url, item.content, item.contentType);
      if (result.stage === 'STORED') {
        absorbed.push(result);
      } else {
        eliminated.push(result);
      }
    }

    return { absorbed, eliminated, stats: this.getStats() };
  }

  // ═══════════════════════════════════════════════════════════
  // ÉTAPE 1 : BOUCHE (Ingestion)
  // ═══════════════════════════════════════════════════════════

  /** Parse le contenu brut en RawFood */
  ingest(
    source: FoodSource,
    url: string,
    rawContent: string,
    contentType: string = 'text/html',
  ): RawFood {
    return {
      id: this.generateId('raw'),
      source_type: source,
      source_url: url,
      raw_content: rawContent,
      fetched_at: Date.now(),
      content_type: contentType,
    };
  }

  // ═══════════════════════════════════════════════════════════
  // ÉTAPE 2 : MASTICATION (Broyage)
  // ═══════════════════════════════════════════════════════════

  /** Décompose le HTML/JSON/texte en morceaux structurés */
  chew(rawFood: RawFood): ChewedFood {
    const isHtml = rawFood.content_type.includes('html');
    const isJson = rawFood.content_type.includes('json');

    let title: string;
    let body: string;
    let author: string | undefined;
    let publishedAt: number | undefined;

    if (isJson) {
      // Tenter de parser le JSON
      try {
        const json = JSON.parse(rawFood.raw_content);
        title = json.title ?? json.name ?? json.headline ?? 'Sans titre';
        body = json.body ?? json.content ?? json.text ?? json.description ?? JSON.stringify(json);
        author = json.author ?? json.creator ?? json.by;
        publishedAt = json.published_at ?? json.date ? new Date(json.date).getTime() : undefined;
      } catch {
        title = 'Contenu JSON invalide';
        body = rawFood.raw_content;
      }
    } else if (isHtml) {
      title = this.extractTitle(rawFood.raw_content);
      body = this.extractBody(rawFood.raw_content);
      author = this.extractAuthor(rawFood.raw_content);
      publishedAt = this.extractDate(rawFood.raw_content);
    } else {
      // Texte brut
      const lines = rawFood.raw_content.split('\n').filter(l => l.trim());
      title = lines[0]?.substring(0, 120) ?? 'Sans titre';
      body = rawFood.raw_content;
    }

    // Nettoyer le body
    body = this.stripHtml(body).trim();

    // Extraire les mots-clés
    const keywords = this.extractKeywords(body);

    // Détecter la langue (heuristique simple)
    const language = this.detectLanguage(body);

    return {
      id: this.generateId('chewed'),
      raw_food_id: rawFood.id,
      title: title.trim(),
      body,
      author,
      published_at: publishedAt,
      sources: this.extractSources(rawFood.raw_content),
      keywords,
      language,
      word_count: body.split(/\s+/).filter(w => w.length > 0).length,
    };
  }

  // ── Helpers de mastication ──────────────────────────────

  private extractTitle(html: string): string {
    // <title>...</title>
    const titleMatch = html.match(/<title[^>]*>(.*?)<\/title>/is);
    if (titleMatch) return this.stripHtml(titleMatch[1]).trim();

    // <h1>...</h1>
    const h1Match = html.match(/<h1[^>]*>(.*?)<\/h1>/is);
    if (h1Match) return this.stripHtml(h1Match[1]).trim();

    // meta og:title
    const ogMatch = html.match(/<meta[^>]*property=["']og:title["'][^>]*content=["'](.*?)["']/i);
    if (ogMatch) return ogMatch[1].trim();

    return 'Sans titre';
  }

  private extractBody(html: string): string {
    // Priorité : <article>, <main>, <body>
    const articleMatch = html.match(/<article[^>]*>([\s\S]*?)<\/article>/i);
    if (articleMatch) return this.stripHtml(articleMatch[1]);

    const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
    if (mainMatch) return this.stripHtml(mainMatch[1]);

    // Fallback : tout le body
    const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    if (bodyMatch) return this.stripHtml(bodyMatch[1]);

    return this.stripHtml(html);
  }

  private extractAuthor(html: string): string | undefined {
    // meta author
    const metaMatch = html.match(/<meta[^>]*name=["']author["'][^>]*content=["'](.*?)["']/i);
    if (metaMatch) return metaMatch[1].trim();

    // meta article:author
    const ogMatch = html.match(/<meta[^>]*property=["']article:author["'][^>]*content=["'](.*?)["']/i);
    if (ogMatch) return ogMatch[1].trim();

    return undefined;
  }

  private extractDate(html: string): number | undefined {
    // meta article:published_time
    const metaMatch = html.match(/<meta[^>]*property=["']article:published_time["'][^>]*content=["'](.*?)["']/i);
    if (metaMatch) {
      const d = new Date(metaMatch[1]);
      if (!isNaN(d.getTime())) return d.getTime();
    }

    // <time datetime="...">
    const timeMatch = html.match(/<time[^>]*datetime=["'](.*?)["']/i);
    if (timeMatch) {
      const d = new Date(timeMatch[1]);
      if (!isNaN(d.getTime())) return d.getTime();
    }

    return undefined;
  }

  /** Extrait les mots-clés significatifs du texte */
  extractKeywords(text: string): string[] {
    const words = text
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z\s]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length > 3);

    // Compteur de fréquence
    const freq: Record<string, number> = {};
    const stopWords = new Set([
      'dans', 'pour', 'avec', 'cette', 'etre', 'sont', 'plus', 'tout',
      'fait', 'mais', 'comme', 'leur', 'bien', 'aussi', 'autre', 'meme',
      'elle', 'nous', 'vous', 'entre', 'tres', 'alors', 'apres', 'avant',
      'the', 'and', 'that', 'this', 'with', 'from', 'have', 'will',
      'been', 'they', 'their', 'which', 'would', 'there', 'about',
    ]);

    for (const word of words) {
      if (!stopWords.has(word)) {
        freq[word] = (freq[word] ?? 0) + 1;
      }
    }

    // Trier par fréquence et prendre les top N
    return Object.entries(freq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, MAX_KEYWORDS)
      .map(([word]) => word);
  }

  /** Retire toutes les balises HTML */
  stripHtml(html: string): string {
    return html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')    // Remove scripts
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')      // Remove styles
      .replace(/<[^>]+>/g, ' ')                             // Remove tags
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/\s+/g, ' ')                                // Normalize whitespace
      .trim();
  }

  /** Détection de langue simple (fr vs en) */
  private detectLanguage(text: string): string {
    const lower = text.toLowerCase();
    const frMarkers = ['le', 'la', 'les', 'des', 'une', 'est', 'dans', 'pour', 'qui', 'avec'];
    const enMarkers = ['the', 'is', 'are', 'was', 'were', 'has', 'have', 'for', 'with', 'that'];

    const frCount = frMarkers.filter(m => lower.includes(` ${m} `)).length;
    const enCount = enMarkers.filter(m => lower.includes(` ${m} `)).length;

    return frCount >= enCount ? 'fr' : 'en';
  }

  /** Extrait les sources/références du contenu */
  private extractSources(content: string): { reference: string; verified: boolean }[] {
    const sources: { reference: string; verified: boolean }[] = [];

    // Extraire les URLs du contenu
    const urlRegex = /https?:\/\/[^\s"'<>]+/g;
    const urls = content.match(urlRegex) ?? [];

    for (const url of urls.slice(0, 10)) { // Max 10 sources
      sources.push({
        reference: url,
        verified: false, // Par défaut, les sources ne sont pas vérifiées
      });
    }

    return sources;
  }

  // ═══════════════════════════════════════════════════════════
  // ÉTAPE 3 : ESTOMAC (Digestion Rosetta)
  // ═══════════════════════════════════════════════════════════

  /** Traduit le ChewedFood en RosettaTranslation via KnowledgeTemplate */
  digestRosetta(chewed: ChewedFood): RosettaTranslation {
    return this.parser.translate('knowledge', chewed);
  }

  // ═══════════════════════════════════════════════════════════
  // ÉTAPE 4 : INTESTIN (Absorption / Filtrage)
  // ═══════════════════════════════════════════════════════════

  /** Filtre la qualité via InformationFilter + ThreatAmygdala */
  absorb(chewed: ChewedFood, rosetta: RosettaTranslation): {
    absorbed: boolean;
    score: InformationResonanceScore;
    threat: ThreatSignal | null;
    rejection_reason?: string;
  } {
    // Analyse de résonance informationnelle
    const score = InformationFilter.analyzeResonance({
      text: chewed.body,
      author_id: chewed.author,
      sources: chewed.sources,
    });

    // Scan de menace via l'amygdale (si disponible)
    let threat: ThreatSignal | null = null;
    if (this.amygdala) {
      const scanCtx: ScanContext = {
        type: 'intention',
        data: { text: chewed.body, title: chewed.title },
        source: 'DigestiveSystem',
      };
      threat = this.amygdala.scan(scanCtx);
    }

    // Décision d'absorption
    // Rejeté si : score trop bas, contenu MANIPULATIF/DIVISIF, ou menace sévère
    if (score.intention_detectee === 'MANIPULATIF') {
      return {
        absorbed: false,
        score,
        threat,
        rejection_reason: `Contenu MANIPULATIF détecté (score: ${score.score_global}/100)`,
      };
    }

    if (score.intention_detectee === 'DIVISIF') {
      return {
        absorbed: false,
        score,
        threat,
        rejection_reason: `Contenu DIVISIF détecté (score: ${score.score_global}/100)`,
      };
    }

    if (threat && threat.severity >= 60) {
      return {
        absorbed: false,
        score,
        threat,
        rejection_reason: `Menace sévère détectée: ${threat.type} (sévérité: ${threat.severity})`,
      };
    }

    if (score.score_global < ABSORPTION_THRESHOLD) {
      return {
        absorbed: false,
        score,
        threat,
        rejection_reason: `Score de qualité insuffisant: ${score.score_global}/100 (seuil: ${ABSORPTION_THRESHOLD})`,
      };
    }

    return { absorbed: true, score, threat };
  }

  // ═══════════════════════════════════════════════════════════
  // ÉTAPE 5 : SANG (Routage vers Sphère)
  // ═══════════════════════════════════════════════════════════

  /** Classifie le contenu dans la bonne Sphère + MappingLayer */
  route(chewed: ChewedFood, score: InformationResonanceScore): {
    sphere: SphereId;
    layer: MappingLayer;
    resonance_level: ResonanceLevel;
  } {
    const sphere = this.classifySphere(chewed.keywords);
    const layer = this.classifyLayer(score);
    const sphereData = SPHERES[sphere];
    const resonance_level = sphereData.index as ResonanceLevel;

    return { sphere, layer, resonance_level };
  }

  /** Classifie les mots-clés dans une Sphère */
  private classifySphere(keywords: string[]): SphereId {
    const scores: Partial<Record<SphereId, number>> = {};
    const normalizedKw = keywords.map(kw =>
      kw.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''),
    );

    for (const [sphere, sphereKeywords] of Object.entries(SPHERE_KEYWORDS)) {
      const normalizedSphereKw = sphereKeywords.map(sk =>
        sk.normalize('NFD').replace(/[\u0300-\u036f]/g, ''),
      );

      let count = 0;
      for (const kw of normalizedKw) {
        for (const sk of normalizedSphereKw) {
          if (kw.includes(sk) || sk.includes(kw)) {
            count++;
          }
        }
      }
      if (count > 0) {
        scores[sphere as SphereId] = count;
      }
    }

    // Trouver la sphère avec le plus de matchs
    let bestSphere: SphereId = 'EDUCATION'; // Par défaut — l'éducation accueille tout
    let bestScore = 0;

    for (const [sphere, score] of Object.entries(scores)) {
      if ((score ?? 0) > bestScore) {
        bestScore = score ?? 0;
        bestSphere = sphere as SphereId;
      }
    }

    return bestSphere;
  }

  /** Classifie la MappingLayer selon le score de qualité */
  private classifyLayer(score: InformationResonanceScore): MappingLayer {
    // Score élevé + sources vérifiées → EVENEMENTS (faits vérifiables)
    if (score.score_global >= 80 && score.coherence_externe >= 60) {
      return 'EVENEMENTS';
    }

    // Score moyen + persuasif/informatif → NARRATIFS (interprétations)
    if (score.score_global >= 60) {
      if (score.intention_detectee === 'PERSUASIF') return 'NARRATIFS';
      return 'NARRATIFS';
    }

    // Score acceptable → PATTERNS (récurrences)
    if (score.score_global >= ABSORPTION_THRESHOLD) {
      return 'PATTERNS';
    }

    // Default (ne devrait pas arriver si absorb() a filtré)
    return 'PATTERNS';
  }

  // ═══════════════════════════════════════════════════════════
  // ÉTAPE 6 : CELLULE (Stockage ATOMNode)
  // ═══════════════════════════════════════════════════════════

  /** Crée l'ATOMNode dans l'Arbre des Connaissances */
  store(
    rosetta: RosettaTranslation,
    sphere: SphereId,
    _layer: MappingLayer,
    chewed: ChewedFood,
  ): ATOMNode {
    const sphereData = SPHERES[sphere];
    const resonanceLevel = sphereData.index as ResonanceLevel;

    const node: ATOMNode = {
      id: this.generateId('node'),
      parent_id: null,
      sphere_id: sphere,
      title: chewed.title,
      status: 'active',
      depth: 0,
      spiral_position: Math.random() * Math.PI * 2, // Position aléatoire sur le disque de Phaistos
      resonance_level: resonanceLevel,
      rosetta,
      created_by: 'DigestiveSystem',
      created_at: Date.now(),
      updated_at: Date.now(),
    };

    return node;
  }

  // ═══════════════════════════════════════════════════════════
  // ÉTAPE 7 : CÔLON (Élimination)
  // ═══════════════════════════════════════════════════════════

  /** Archive le déchet avec raison du rejet */
  eliminate(food: DigestedFood, reason: string): void {
    food.stage = 'ELIMINATED';
    food.rejection_reason = reason;

    // Archiver dans la poubelle traçable
    this.wasteArchive.push(food);

    // Limiter la taille de l'archive
    if (this.wasteArchive.length > MAX_WASTE_ARCHIVE) {
      this.wasteArchive.shift();
    }

    // Mettre à jour les statistiques
    this.stats.total_ingested++;
    this.stats.total_eliminated++;
    this.stats.absorption_rate = this.stats.total_ingested > 0
      ? this.stats.total_absorbed / this.stats.total_ingested
      : 0;

    this.notifyListeners({ type: 'food_eliminated', food });
  }

  // ═══════════════════════════════════════════════════════════
  // STATISTIQUES
  // ═══════════════════════════════════════════════════════════

  /** Retourne les statistiques du système digestif */
  getStats(): DigestiveStats {
    return { ...this.stats };
  }

  /** Retourne l'archive des déchets */
  getWasteArchive(): DigestedFood[] {
    return [...this.wasteArchive];
  }

  /** Taux d'absorption (0-1) */
  getAbsorptionRate(): number {
    return this.stats.absorption_rate;
  }

  // ═══════════════════════════════════════════════════════════
  // ÉVÉNEMENTS
  // ═══════════════════════════════════════════════════════════

  /** S'abonner aux événements digestifs */
  onDigest(listener: (event: DigestiveEvent) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  private notifyListeners(event: DigestiveEvent): void {
    for (const listener of this.listeners) {
      listener(event);
    }
  }

  // ═══════════════════════════════════════════════════════════
  // INTERNALS
  // ═══════════════════════════════════════════════════════════

  private createEmptyStats(): DigestiveStats {
    return {
      total_ingested: 0,
      total_absorbed: 0,
      total_eliminated: 0,
      absorption_rate: 0,
      top_spheres: {},
      avg_quality_score: 0,
    };
  }

  /** Met à jour la moyenne mobile du score de qualité */
  private updateAvgScore(newScore: number): void {
    const n = this.stats.total_absorbed;
    if (n <= 1) {
      this.stats.avg_quality_score = newScore;
    } else {
      // Moyenne mobile incrémentale
      this.stats.avg_quality_score =
        this.stats.avg_quality_score + (newScore - this.stats.avg_quality_score) / n;
    }
  }

  /** Crée un DigestedFood rejeté */
  private createRejected(
    chewedId: string,
    stage: DigestionStage,
    log: DigestiveLogEntry[],
    reason: string,
  ): DigestedFood {
    log.push({
      stage,
      timestamp: Date.now(),
      passed: false,
      detail: reason,
    });

    return {
      id: this.generateId('digested'),
      chewed_food_id: chewedId,
      stage: 'ELIMINATED',
      rejection_reason: reason,
      pipeline_log: log,
    };
  }

  private generateId(prefix: string): string {
    const ts = Date.now().toString(36);
    const rand = Math.random().toString(36).substring(2, 8);
    return `${prefix}_${ts}_${rand}`;
  }
}
