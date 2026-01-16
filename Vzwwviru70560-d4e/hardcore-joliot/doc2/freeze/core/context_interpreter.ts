/* =====================================================
   CHE·NU — CONTEXT INTERPRETER (FREEZE 1.5 — VERSION FINALE)
   
   🔒 Interprets user input and maps to 10 official spheres
   
   SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
   ===================================================== */

import {
  UniverseOS,
  OfficialSphere,
  OFFICIAL_SPHERES,
  SPHERE_INFO,
  isInvalidSphereName,
} from './universe_os';

// ─────────────────────────────────────────────────────
// CONTEXT TYPES
// ─────────────────────────────────────────────────────

export interface ContextInput {
  text: string;
  locale?: string;
  previousContext?: InterpretedContext;
}

export interface InterpretedContext {
  detectedSphere: OfficialSphere;
  detectedSubSphere?: string;
  confidence: number;
  keywords: string[];
  intent: ContextIntent;
  entities: ContextEntity[];
  languageHints: LanguageHint[];
}

export type ContextIntent =
  | 'query'
  | 'action'
  | 'navigation'
  | 'creation'
  | 'update'
  | 'delete'
  | 'search'
  | 'unknown';

export interface ContextEntity {
  type: string;
  value: string;
  confidence: number;
}

export interface LanguageHint {
  pattern: string;
  suggestedSphere: OfficialSphere;
  weight: number;
}

// ─────────────────────────────────────────────────────
// CONTEXT INTERPRETER CLASS
// ─────────────────────────────────────────────────────

/**
 * CHE·NU Context Interpreter
 * Analyzes user input and determines the appropriate sphere context.
 * 
 * CRITICAL RULES:
 * - ONLY maps to the 10 official spheres
 * - Methodology, Skill, Finance, Health are NOT spheres
 * - Uses language patterns to infer sphere membership
 */
export class ContextInterpreter {
  private static instance: ContextInterpreter;

  private constructor() {}

  static getInstance(): ContextInterpreter {
    if (!ContextInterpreter.instance) {
      ContextInterpreter.instance = new ContextInterpreter();
    }
    return ContextInterpreter.instance;
  }

  /**
   * Interpret user input and return context
   */
  interpret(input: ContextInput): InterpretedContext {
    const text = input.text.toLowerCase();
    const keywords = this.extractKeywords(text);
    const intent = this.detectIntent(text);
    const entities = this.extractEntities(text);
    
    // Find matching sphere
    const sphereMatch = this.matchSphere(text, keywords);
    
    // Find matching sub-sphere
    const subSphereMatch = this.matchSubSphere(sphereMatch.sphere, text);

    return {
      detectedSphere: sphereMatch.sphere,
      detectedSubSphere: subSphereMatch,
      confidence: sphereMatch.confidence,
      keywords,
      intent,
      entities,
      languageHints: sphereMatch.hints,
    };
  }

  /**
   * Match input to a sphere
   */
  private matchSphere(text: string, keywords: string[]): {
    sphere: OfficialSphere;
    confidence: number;
    hints: LanguageHint[];
  } {
    const scores: Map<OfficialSphere, number> = new Map();
    const hints: LanguageHint[] = [];

    // Check each sphere's patterns
    for (const sphere of OFFICIAL_SPHERES) {
      const patterns = SPHERE_PATTERNS[sphere];
      let score = 0;

      for (const pattern of patterns) {
        if (text.includes(pattern.pattern)) {
          score += pattern.weight;
          hints.push({
            pattern: pattern.pattern,
            suggestedSphere: sphere,
            weight: pattern.weight,
          });
        }
      }

      // Check for keyword matches
      const sphereInfo = SPHERE_INFO[sphere];
      for (const subSphere of sphereInfo.subSpheres) {
        const subKeywords = subSphere.name.toLowerCase().split(/[\s\/&]+/);
        for (const kw of subKeywords) {
          if (keywords.includes(kw)) {
            score += 0.5;
          }
        }
      }

      scores.set(sphere, score);
    }

    // Find highest scoring sphere
    let bestSphere: OfficialSphere = 'Personal';
    let bestScore = 0;

    for (const [sphere, score] of scores) {
      if (score > bestScore) {
        bestScore = score;
        bestSphere = sphere;
      }
    }

    // Calculate confidence
    const confidence = Math.min(0.95, 0.3 + (bestScore * 0.15));

    return {
      sphere: bestSphere,
      confidence,
      hints,
    };
  }

  /**
   * Match sub-sphere within a sphere
   */
  private matchSubSphere(sphere: OfficialSphere, text: string): string | undefined {
    const sphereInfo = SPHERE_INFO[sphere];

    for (const subSphere of sphereInfo.subSpheres) {
      const keywords = subSphere.name.toLowerCase().split(/[\s\/&]+/);
      if (keywords.some(kw => text.includes(kw))) {
        return subSphere.id;
      }
    }

    return undefined;
  }

  /**
   * Extract keywords from text
   */
  private extractKeywords(text: string): string[] {
    // Remove common words
    const stopWords = new Set([
      'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
      'would', 'could', 'should', 'may', 'might', 'must', 'shall',
      'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
      'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
      'through', 'during', 'before', 'after', 'above', 'below',
      'between', 'under', 'again', 'further', 'then', 'once',
      'i', 'me', 'my', 'myself', 'we', 'our', 'you', 'your',
      'he', 'him', 'his', 'she', 'her', 'it', 'its', 'they', 'their',
      'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
      'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
      'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    ]);

    const words = text.split(/\s+/).filter(w => w.length > 2);
    return words.filter(w => !stopWords.has(w));
  }

  /**
   * Detect user intent
   */
  private detectIntent(text: string): ContextIntent {
    const intentPatterns: Record<ContextIntent, string[]> = {
      query: ['what', 'how', 'why', 'when', 'where', 'who', 'which', '?'],
      action: ['do', 'make', 'perform', 'execute', 'run', 'start', 'begin'],
      navigation: ['go', 'navigate', 'open', 'show', 'display', 'view'],
      creation: ['create', 'new', 'add', 'generate', 'build', 'design'],
      update: ['update', 'edit', 'modify', 'change', 'set'],
      delete: ['delete', 'remove', 'clear', 'erase'],
      search: ['find', 'search', 'look', 'discover', 'locate'],
      unknown: [],
    };

    for (const [intent, patterns] of Object.entries(intentPatterns)) {
      if (patterns.some(p => text.includes(p))) {
        return intent as ContextIntent;
      }
    }

    return 'unknown';
  }

  /**
   * Extract entities from text
   */
  private extractEntities(text: string): ContextEntity[] {
    const entities: ContextEntity[] = [];

    // Date patterns
    const datePattern = /\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})\b/g;
    let match;
    while ((match = datePattern.exec(text)) !== null) {
      entities.push({ type: 'date', value: match[1], confidence: 0.9 });
    }

    // Time patterns
    const timePattern = /\b(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[ap]m)?)\b/gi;
    while ((match = timePattern.exec(text)) !== null) {
      entities.push({ type: 'time', value: match[1], confidence: 0.9 });
    }

    // Currency patterns
    const currencyPattern = /\$[\d,]+(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars?|euros?|CAD|USD|EUR)/gi;
    while ((match = currencyPattern.exec(text)) !== null) {
      entities.push({ type: 'currency', value: match[0], confidence: 0.85 });
    }

    // Email patterns
    const emailPattern = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
    while ((match = emailPattern.exec(text)) !== null) {
      entities.push({ type: 'email', value: match[0], confidence: 0.95 });
    }

    return entities;
  }

  /**
   * Check if an input is trying to reference an invalid sphere
   */
  checkInvalidSphereReference(text: string): {
    isInvalid: boolean;
    invalidTerm?: string;
    correction?: string;
  } {
    const text_lower = text.toLowerCase();
    
    // Check for invalid sphere references
    const invalidMappings: Record<string, { sphere: OfficialSphere; engine: string }> = {
      'methodology': { sphere: 'Scholar', engine: 'MethodologyEngine' },
      'skill': { sphere: 'Personal', engine: 'SkillEngine' },
      'finance': { sphere: 'Personal', engine: 'FinanceEngine' },
      'health': { sphere: 'Personal', engine: 'HealthEngine' },
      'productivity': { sphere: 'Personal', engine: 'ProductivityEngine' },
      'tools': { sphere: 'AILab', engine: 'ToolsEngine' },
      'simulation': { sphere: 'AILab', engine: 'SimulationEngine' },
      'persona': { sphere: 'Personal', engine: 'PersonaEngine' },
      'process': { sphere: 'Business', engine: 'ProcessEngine' },
    };

    for (const [term, mapping] of Object.entries(invalidMappings)) {
      if (text_lower.includes(`${term} sphere`) || text_lower.includes(`${term}sphere`)) {
        return {
          isInvalid: true,
          invalidTerm: term,
          correction: `"${term}" is not a sphere. Use ${mapping.sphere} sphere and invoke ${mapping.engine}.`,
        };
      }
    }

    return { isInvalid: false };
  }
}

// ─────────────────────────────────────────────────────
// SPHERE PATTERNS (for detection)
// ─────────────────────────────────────────────────────

interface SpherePattern {
  pattern: string;
  weight: number;
}

/**
 * Language patterns that indicate specific spheres
 * These help the interpreter map natural language to spheres
 */
const SPHERE_PATTERNS: Record<OfficialSphere, SpherePattern[]> = {
  Personal: [
    { pattern: 'my life', weight: 2 },
    { pattern: 'personal', weight: 2 },
    { pattern: 'myself', weight: 1.5 },
    { pattern: 'health', weight: 1.5 },
    { pattern: 'wellbeing', weight: 1.5 },
    { pattern: 'wellness', weight: 1.5 },
    { pattern: 'habit', weight: 1.5 },
    { pattern: 'lifestyle', weight: 1.5 },
    { pattern: 'self improvement', weight: 2 },
    { pattern: 'my finances', weight: 1.5 },
    { pattern: 'personal finance', weight: 2 },
    { pattern: 'self development', weight: 2 },
    { pattern: 'my growth', weight: 1.5 },
    { pattern: 'journal', weight: 1 },
    { pattern: 'diary', weight: 1 },
    { pattern: 'reflection', weight: 1 },
  ],
  Business: [
    { pattern: 'business', weight: 2 },
    { pattern: 'company', weight: 2 },
    { pattern: 'startup', weight: 2 },
    { pattern: 'enterprise', weight: 2 },
    { pattern: 'commerce', weight: 1.5 },
    { pattern: 'operations', weight: 1.5 },
    { pattern: 'logistics', weight: 1.5 },
    { pattern: 'supply chain', weight: 2 },
    { pattern: 'construction', weight: 1.5 },
    { pattern: 'industrial', weight: 1.5 },
    { pattern: 'client', weight: 1 },
    { pattern: 'customer', weight: 1 },
    { pattern: 'revenue', weight: 1.5 },
    { pattern: 'profit', weight: 1.5 },
    { pattern: 'invoice', weight: 1 },
    { pattern: 'b2b', weight: 1.5 },
  ],
  Creative: [
    { pattern: 'creative', weight: 2 },
    { pattern: 'art', weight: 1.5 },
    { pattern: 'design', weight: 1.5 },
    { pattern: 'music', weight: 1.5 },
    { pattern: 'video', weight: 1 },
    { pattern: 'photo', weight: 1 },
    { pattern: 'imagination', weight: 1.5 },
    { pattern: 'concept', weight: 1 },
    { pattern: 'artistic', weight: 1.5 },
    { pattern: 'create', weight: 1 },
    { pattern: 'draw', weight: 1 },
    { pattern: 'paint', weight: 1.5 },
    { pattern: 'compose', weight: 1.5 },
    { pattern: 'craft', weight: 1 },
    { pattern: 'expression', weight: 1 },
  ],
  Scholar: [
    { pattern: 'study', weight: 2 },
    { pattern: 'research', weight: 2 },
    { pattern: 'learn', weight: 1.5 },
    { pattern: 'knowledge', weight: 1.5 },
    { pattern: 'education', weight: 1.5 },
    { pattern: 'documentation', weight: 1.5 },
    { pattern: 'information', weight: 1 },
    { pattern: 'academic', weight: 2 },
    { pattern: 'science', weight: 1.5 },
    { pattern: 'paper', weight: 1 },
    { pattern: 'thesis', weight: 2 },
    { pattern: 'course', weight: 1 },
    { pattern: 'lecture', weight: 1.5 },
    { pattern: 'bibliography', weight: 1.5 },
  ],
  SocialNetworkMedia: [
    { pattern: 'social media', weight: 2.5 },
    { pattern: 'social network', weight: 2.5 },
    { pattern: 'post', weight: 1 },
    { pattern: 'share', weight: 1 },
    { pattern: 'followers', weight: 1.5 },
    { pattern: 'feed', weight: 1.5 },
    { pattern: 'profile', weight: 1 },
    { pattern: 'like', weight: 0.5 },
    { pattern: 'comment', weight: 0.5 },
    { pattern: 'message', weight: 1 },
    { pattern: 'dm', weight: 1 },
    { pattern: 'timeline', weight: 1.5 },
    { pattern: 'stories', weight: 1 },
    { pattern: 'reels', weight: 1 },
    { pattern: 'tweet', weight: 1.5 },
    { pattern: 'influencer', weight: 1.5 },
  ],
  Community: [
    { pattern: 'community', weight: 2.5 },
    { pattern: 'group', weight: 1.5 },
    { pattern: 'forum', weight: 2 },
    { pattern: 'reddit', weight: 2 },
    { pattern: 'discussion', weight: 1.5 },
    { pattern: 'announcement', weight: 1.5 },
    { pattern: 'public', weight: 1 },
    { pattern: 'civic', weight: 1.5 },
    { pattern: 'neighborhood', weight: 1.5 },
    { pattern: 'local', weight: 1 },
    { pattern: 'pages', weight: 1 },
    { pattern: 'members', weight: 1 },
    { pattern: 'moderator', weight: 1.5 },
    { pattern: 'subreddit', weight: 2 },
    { pattern: 'thread', weight: 1 },
  ],
  XR: [
    { pattern: 'vr', weight: 2 },
    { pattern: 'ar', weight: 2 },
    { pattern: 'xr', weight: 2.5 },
    { pattern: 'virtual reality', weight: 2.5 },
    { pattern: 'augmented', weight: 2 },
    { pattern: '3d', weight: 1.5 },
    { pattern: 'spatial', weight: 1.5 },
    { pattern: 'immersive', weight: 1.5 },
    { pattern: 'metaverse', weight: 2 },
    { pattern: 'avatar', weight: 1.5 },
    { pattern: 'scene', weight: 1 },
    { pattern: 'world building', weight: 2 },
    { pattern: 'mixed reality', weight: 2 },
  ],
  MyTeam: [
    { pattern: 'team', weight: 2 },
    { pattern: 'collaboration', weight: 2 },
    { pattern: 'colleague', weight: 1.5 },
    { pattern: 'coworker', weight: 1.5 },
    { pattern: 'delegate', weight: 1.5 },
    { pattern: 'coordinate', weight: 1.5 },
    { pattern: 'roles', weight: 1 },
    { pattern: 'project team', weight: 2 },
    { pattern: 'teamwork', weight: 2 },
    { pattern: 'sprint', weight: 1 },
    { pattern: 'standup', weight: 1.5 },
    { pattern: 'meeting', weight: 1 },
    { pattern: 'assign', weight: 1 },
  ],
  AILab: [
    { pattern: 'ai', weight: 2 },
    { pattern: 'artificial intelligence', weight: 2.5 },
    { pattern: 'machine learning', weight: 2.5 },
    { pattern: 'ml', weight: 2 },
    { pattern: 'sandbox', weight: 1.5 },
    { pattern: 'experiment', weight: 1.5 },
    { pattern: 'cognitive', weight: 1.5 },
    { pattern: 'neural', weight: 1.5 },
    { pattern: 'model', weight: 1 },
    { pattern: 'training', weight: 1 },
    { pattern: 'simulation', weight: 1.5 },
    { pattern: 'lab', weight: 1 },
    { pattern: 'algorithm', weight: 1.5 },
    { pattern: 'prompt', weight: 1 },
  ],
  Entertainment: [
    { pattern: 'entertainment', weight: 2.5 },
    { pattern: 'fun', weight: 1 },
    { pattern: 'game', weight: 2 },
    { pattern: 'play', weight: 1 },
    { pattern: 'streaming', weight: 2 },
    { pattern: 'video', weight: 1 },
    { pattern: 'watch', weight: 1.5 },
    { pattern: 'movie', weight: 1.5 },
    { pattern: 'show', weight: 1 },
    { pattern: 'series', weight: 1 },
    { pattern: 'audience', weight: 1.5 },
    { pattern: 'immersion', weight: 1.5 },
    { pattern: 'interactive', weight: 1 },
    { pattern: 'netflix', weight: 1.5 },
    { pattern: 'youtube', weight: 1.5 },
    { pattern: 'twitch', weight: 1.5 },
  ],
};

// ─────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────

export default ContextInterpreter;
