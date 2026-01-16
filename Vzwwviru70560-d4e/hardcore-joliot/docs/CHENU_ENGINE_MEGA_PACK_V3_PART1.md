============================================================
CHE·NU — OPERATIONAL ENGINE MEGA PACK V3
VERSION: 3.2.0
DATE: 2025-12-12
============================================================

╔════════════════════════════════════════════════════════════╗
║  CONSOLIDATION AGENT — EXTENDED ENGINE SUITE V3            ║
║  5 NEW ENGINES · 27 SUB-ENGINES · 5 SCHEMAS                ║
║  SAFE · REPRESENTATIONAL · NON-AUTONOMOUS                  ║
╚════════════════════════════════════════════════════════════╝

============================================================
NEW ENGINES IN THIS PACK
============================================================

ENGINE 11: RelationshipEngine (Personal/Professional Relations)
  └── network.engine.ts
  └── communication.engine.ts
  └── boundary.engine.ts
  └── maintenance.engine.ts
  └── conflict.engine.ts

ENGINE 12: CreativityEngine (Creative Process)
  └── ideation.engine.ts
  └── brainstorm.engine.ts
  └── constraint.engine.ts
  └── iteration.engine.ts
  └── evaluation.engine.ts

ENGINE 13: StrategyEngine (Strategic Planning)
  └── vision.engine.ts
  └── analysis.engine.ts
  └── positioning.engine.ts
  └── roadmap.engine.ts
  └── execution.engine.ts
  └── pivot.engine.ts

ENGINE 14: AnalysisEngine (Structured Analysis)
  └── framework.engine.ts
  └── data.engine.ts
  └── pattern.engine.ts
  └── synthesis.engine.ts
  └── recommendation.engine.ts

ENGINE 15: ReflectionEngine (Self-Reflection & Review)
  └── journal.engine.ts
  └── retrospective.engine.ts
  └── insight.engine.ts
  └── growth.engine.ts
  └── gratitude.engine.ts

############################################################
#                                                          #
#           ENGINE 11: RELATIONSHIP ENGINE                 #
#                                                          #
############################################################

============================================================
11.1 — RELATIONSHIP ENGINE (MAIN MODULE)
============================================================

--- FILE: /che-nu-sdk/core/relationship.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Relationship Engine
 * =================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * CLASSIFICATION: OPERATIONAL MODULE (NOT A SPHERE)
 * 
 * Provides representational structures for relationship management.
 * Personal AND professional relationships. NO therapy. Structure only.
 * 
 * Different from EmotionEngine: focuses on relationship MANAGEMENT
 * not emotional analysis.
 * 
 * @module RelationshipEngine
 * @version 1.0.0
 */

import { NetworkEngine } from './relationship/network.engine';
import { RelationCommunicationEngine } from './relationship/communication.engine';
import { BoundaryEngine } from './relationship/boundary.engine';
import { MaintenanceEngine } from './relationship/maintenance.engine';
import { ConflictEngine } from './relationship/conflict.engine';

// ============================================================
// TYPES
// ============================================================

export interface RelationshipNetwork {
  id: string;
  circles: RelationshipCircle[];
  totalConnections: number;
  healthOverview: NetworkHealth;
  meta: RelationshipMeta;
}

export interface RelationshipCircle {
  id: string;
  name: string;
  level: 'inner' | 'close' | 'active' | 'distant' | 'dormant';
  description: string;
  idealSize: string;
  currentSize: number;
  members: RelationshipMember[];
}

export interface RelationshipMember {
  id: string;
  role: string;
  category: 'family' | 'friend' | 'colleague' | 'mentor' | 'mentee' | 'professional' | 'community';
  lastContact: string;
  connectionStrength: 'strong' | 'moderate' | 'weak' | 'new';
  maintenanceNeeded: boolean;
}

export interface NetworkHealth {
  diversity: 'low' | 'moderate' | 'good' | 'excellent';
  balance: 'imbalanced' | 'somewhat-balanced' | 'balanced';
  gaps: string[];
  strengths: string[];
}

export interface CommunicationPlan {
  id: string;
  relationshipId: string;
  style: 'direct' | 'indirect' | 'formal' | 'casual';
  frequency: string;
  channels: string[];
  topics: string[];
  boundaries: string[];
  meta: RelationshipMeta;
}

export interface BoundaryFramework {
  id: string;
  type: 'personal' | 'professional' | 'emotional' | 'time' | 'digital';
  boundaries: Boundary[];
  communicationScript: string[];
  meta: RelationshipMeta;
}

export interface Boundary {
  id: string;
  name: string;
  description: string;
  category: string;
  flexibility: 'firm' | 'flexible' | 'negotiable';
  communicationTips: string[];
}

export interface MaintenancePlan {
  id: string;
  relationshipId: string;
  priority: 'high' | 'medium' | 'low';
  actions: MaintenanceAction[];
  schedule: string;
  meta: RelationshipMeta;
}

export interface MaintenanceAction {
  id: string;
  type: 'reach-out' | 'meet' | 'support' | 'celebrate' | 'check-in';
  description: string;
  frequency: string;
  effortLevel: 'minimal' | 'moderate' | 'significant';
}

export interface ConflictResolution {
  id: string;
  situation: string;
  parties: string[];
  approach: 'collaborative' | 'accommodating' | 'compromising' | 'avoiding' | 'competing';
  steps: ConflictStep[];
  communicationGuide: string[];
  meta: RelationshipMeta;
}

export interface ConflictStep {
  order: number;
  action: string;
  purpose: string;
  tips: string[];
}

export interface RelationshipMeta {
  source: string;
  generated: string;
  version: string;
  moduleType: 'operational_module';
  classification: 'not_a_sphere';
  safe: {
    isRepresentational: boolean;
    noTherapy: boolean;
    noManipulation: boolean;
  };
}

// ============================================================
// RELATIONSHIP ENGINE CLASS
// ============================================================

export class RelationshipEngine {
  private readonly VERSION = '1.0.0';

  private network: NetworkEngine;
  private communication: RelationCommunicationEngine;
  private boundary: BoundaryEngine;
  private maintenance: MaintenanceEngine;
  private conflict: ConflictEngine;

  constructor() {
    this.network = new NetworkEngine();
    this.communication = new RelationCommunicationEngine();
    this.boundary = new BoundaryEngine();
    this.maintenance = new MaintenanceEngine();
    this.conflict = new ConflictEngine();
  }

  /**
   * Map relationship network
   */
  mapNetwork(input: string | Record<string, unknown>): RelationshipNetwork {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.network.map(inputStr);
  }

  /**
   * Plan communication
   */
  planCommunication(input: string | Record<string, unknown>): CommunicationPlan {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.communication.plan(inputStr);
  }

  /**
   * Define boundaries
   */
  defineBoundaries(input: string | Record<string, unknown>): BoundaryFramework {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.boundary.define(inputStr);
  }

  /**
   * Create maintenance plan
   */
  createMaintenancePlan(input: string | Record<string, unknown>): MaintenancePlan {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.maintenance.plan(inputStr);
  }

  /**
   * Structure conflict resolution
   */
  structureConflictResolution(input: string | Record<string, unknown>): ConflictResolution {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.conflict.structure(inputStr);
  }

  meta(): Record<string, unknown> {
    return {
      name: 'RelationshipEngine',
      version: this.VERSION,
      description: 'Representational relationship management structures for CHE·NU',
      classification: {
        type: 'operational_module',
        isNotASphere: true,
        category: 'relationship_operational',
      },
      safe: {
        isRepresentational: true,
        noTherapy: true,
        noManipulation: true,
      },
      subEngines: [
        'NetworkEngine',
        'RelationCommunicationEngine',
        'BoundaryEngine',
        'MaintenanceEngine',
        'ConflictEngine'
      ],
    };
  }
}

export function createRelationshipEngine(): RelationshipEngine {
  return new RelationshipEngine();
}

export default RelationshipEngine;

============================================================
11.2 — NETWORK SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/relationship/network.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Relationship Network Engine
 * =========================================
 * SAFE · REPRESENTATIONAL
 */

import type { RelationshipNetwork, RelationshipCircle, RelationshipMember, NetworkHealth, RelationshipMeta } from '../relationship';

export class NetworkEngine {
  private readonly VERSION = '1.0.0';

  map(input: string): RelationshipNetwork {
    return {
      id: `network-${Date.now()}`,
      circles: this.generateCircles(input),
      totalConnections: 0,
      healthOverview: this.assessHealth(input),
      meta: this.createMeta(input),
    };
  }

  private generateCircles(input: string): RelationshipCircle[] {
    return [
      {
        id: 'circle-1',
        name: 'Inner Circle',
        level: 'inner',
        description: 'Closest relationships - highest trust and intimacy',
        idealSize: '3-5 people',
        currentSize: 0,
        members: [],
      },
      {
        id: 'circle-2',
        name: 'Close Friends & Family',
        level: 'close',
        description: 'Strong bonds - regular meaningful contact',
        idealSize: '10-15 people',
        currentSize: 0,
        members: [],
      },
      {
        id: 'circle-3',
        name: 'Active Connections',
        level: 'active',
        description: 'Regular contact - friends and colleagues',
        idealSize: '30-50 people',
        currentSize: 0,
        members: [],
      },
      {
        id: 'circle-4',
        name: 'Extended Network',
        level: 'distant',
        description: 'Occasional contact - broader network',
        idealSize: '100-150 people',
        currentSize: 0,
        members: [],
      },
      {
        id: 'circle-5',
        name: 'Dormant Connections',
        level: 'dormant',
        description: 'Past connections - potential for reactivation',
        idealSize: 'Variable',
        currentSize: 0,
        members: [],
      },
    ];
  }

  private assessHealth(input: string): NetworkHealth {
    return {
      diversity: 'moderate',
      balance: 'somewhat-balanced',
      gaps: [
        'Consider diversity of perspectives',
        'Professional network development',
        'Community connections',
      ],
      strengths: [
        'Foundation of close relationships',
        'Potential for growth',
      ],
    };
  }

  private createMeta(source: string): RelationshipMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noTherapy: true, noManipulation: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'NetworkEngine', version: this.VERSION, parent: 'RelationshipEngine' };
  }
}

export default NetworkEngine;

============================================================
11.3 — COMMUNICATION SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/relationship/communication.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Relationship Communication Engine
 * ===============================================
 * SAFE · REPRESENTATIONAL
 */

import type { CommunicationPlan, RelationshipMeta } from '../relationship';

export class RelationCommunicationEngine {
  private readonly VERSION = '1.0.0';

  plan(input: string): CommunicationPlan {
    const lowerInput = input.toLowerCase();

    return {
      id: `commplan-${Date.now()}`,
      relationshipId: 'rel-current',
      style: this.determineStyle(lowerInput),
      frequency: this.suggestFrequency(lowerInput),
      channels: this.suggestChannels(lowerInput),
      topics: this.suggestTopics(lowerInput),
      boundaries: this.suggestBoundaries(lowerInput),
      meta: this.createMeta(input),
    };
  }

  private determineStyle(input: string): CommunicationPlan['style'] {
    if (input.includes('work') || input.includes('professional')) return 'formal';
    if (input.includes('close') || input.includes('friend')) return 'casual';
    if (input.includes('direct') || input.includes('clear')) return 'direct';
    return 'indirect';
  }

  private suggestFrequency(input: string): string {
    if (input.includes('close') || input.includes('important')) return 'Weekly or more';
    if (input.includes('professional') || input.includes('colleague')) return 'Bi-weekly to monthly';
    return 'Monthly to quarterly';
  }

  private suggestChannels(input: string): string[] {
    const channels: string[] = [];
    if (input.includes('close') || input.includes('friend')) {
      channels.push('In-person meetings', 'Phone calls', 'Text messages');
    }
    if (input.includes('professional') || input.includes('work')) {
      channels.push('Email', 'Video calls', 'Professional events');
    }
    if (channels.length === 0) {
      channels.push('Appropriate channel based on relationship', 'Mix of synchronous and asynchronous');
    }
    return channels;
  }

  private suggestTopics(input: string): string[] {
    return [
      'Shared interests and experiences',
      'Life updates and milestones',
      'Support and encouragement',
      'Future plans and goals',
      'Appreciation and gratitude',
    ];
  }

  private suggestBoundaries(input: string): string[] {
    return [
      'Response time expectations',
      'Topics to avoid or approach carefully',
      'Availability windows',
      'Communication preferences',
    ];
  }

  private createMeta(source: string): RelationshipMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noTherapy: true, noManipulation: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'RelationCommunicationEngine', version: this.VERSION, parent: 'RelationshipEngine' };
  }
}

export default RelationCommunicationEngine;

============================================================
11.4 — BOUNDARY SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/relationship/boundary.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Boundary Engine
 * =============================
 * SAFE · REPRESENTATIONAL
 */

import type { BoundaryFramework, Boundary, RelationshipMeta } from '../relationship';

export class BoundaryEngine {
  private readonly VERSION = '1.0.0';

  define(input: string): BoundaryFramework {
    const lowerInput = input.toLowerCase();

    return {
      id: `boundary-${Date.now()}`,
      type: this.determineType(lowerInput),
      boundaries: this.generateBoundaries(lowerInput),
      communicationScript: this.generateScript(lowerInput),
      meta: this.createMeta(input),
    };
  }

  private determineType(input: string): BoundaryFramework['type'] {
    if (input.includes('work') || input.includes('professional')) return 'professional';
    if (input.includes('time') || input.includes('schedule')) return 'time';
    if (input.includes('digital') || input.includes('online')) return 'digital';
    if (input.includes('emotion')) return 'emotional';
    return 'personal';
  }

  private generateBoundaries(input: string): Boundary[] {
    return [
      {
        id: 'bound-1',
        name: 'Time Boundaries',
        description: 'Limits on availability and response times',
        category: 'time',
        flexibility: 'flexible',
        communicationTips: [
          'State availability clearly',
          'Provide alternatives when unavailable',
          'Be consistent in enforcement',
        ],
      },
      {
        id: 'bound-2',
        name: 'Emotional Boundaries',
        description: 'Limits on emotional labor and engagement',
        category: 'emotional',
        flexibility: 'firm',
        communicationTips: [
          'Acknowledge feelings while maintaining limits',
          'Redirect to appropriate support when needed',
          'Practice self-care after difficult conversations',
        ],
      },
      {
        id: 'bound-3',
        name: 'Communication Boundaries',
        description: 'Preferences for how and when to communicate',
        category: 'communication',
        flexibility: 'negotiable',
        communicationTips: [
          'Express preferences directly',
          'Be open to compromise',
          'Revisit as needs change',
        ],
      },
      {
        id: 'bound-4',
        name: 'Topic Boundaries',
        description: 'Subjects that are off-limits or sensitive',
        category: 'content',
        flexibility: 'firm',
        communicationTips: [
          'Redirect conversations when needed',
          'Clearly state when a topic is not welcome',
          'Offer alternative topics',
        ],
      },
    ];
  }

  private generateScript(input: string): string[] {
    return [
      '"I appreciate you reaching out. I\'m not available for that right now, but..."',
      '"I understand this is important to you. My boundary is..."',
      '"I care about our relationship, and I need to be honest about what I can offer..."',
      '"Thank you for understanding. Let\'s find a way that works for both of us..."',
      '"I\'m not comfortable discussing that. Can we talk about something else?"',
    ];
  }

  private createMeta(source: string): RelationshipMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noTherapy: true, noManipulation: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'BoundaryEngine', version: this.VERSION, parent: 'RelationshipEngine' };
  }
}

export default BoundaryEngine;

============================================================
11.5 — MAINTENANCE SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/relationship/maintenance.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Relationship Maintenance Engine
 * =============================================
 * SAFE · REPRESENTATIONAL
 */

import type { MaintenancePlan, MaintenanceAction, RelationshipMeta } from '../relationship';

export class MaintenanceEngine {
  private readonly VERSION = '1.0.0';

  plan(input: string): MaintenancePlan {
    const lowerInput = input.toLowerCase();

    return {
      id: `maint-${Date.now()}`,
      relationshipId: 'rel-current',
      priority: this.determinePriority(lowerInput),
      actions: this.generateActions(lowerInput),
      schedule: this.createSchedule(lowerInput),
      meta: this.createMeta(input),
    };
  }

  private determinePriority(input: string): MaintenancePlan['priority'] {
    if (input.includes('important') || input.includes('close') || input.includes('urgent')) return 'high';
    if (input.includes('distant') || input.includes('dormant')) return 'low';
    return 'medium';
  }

  private generateActions(input: string): MaintenanceAction[] {
    return [
      {
        id: 'action-1',
        type: 'check-in',
        description: 'Simple message to stay connected',
        frequency: 'Weekly to monthly',
        effortLevel: 'minimal',
      },
      {
        id: 'action-2',
        type: 'reach-out',
        description: 'Meaningful conversation or call',
        frequency: 'Monthly',
        effortLevel: 'moderate',
      },
      {
        id: 'action-3',
        type: 'meet',
        description: 'In-person meeting or activity',
        frequency: 'Quarterly',
        effortLevel: 'significant',
      },
      {
        id: 'action-4',
        type: 'celebrate',
        description: 'Acknowledge milestones and achievements',
        frequency: 'As occasions arise',
        effortLevel: 'moderate',
      },
      {
        id: 'action-5',
        type: 'support',
        description: 'Be present during challenges',
        frequency: 'As needed',
        effortLevel: 'significant',
      },
    ];
  }

  private createSchedule(input: string): string {
    return 'Regular touchpoints with flexibility for spontaneity';
  }

  private createMeta(source: string): RelationshipMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noTherapy: true, noManipulation: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'MaintenanceEngine', version: this.VERSION, parent: 'RelationshipEngine' };
  }
}

export default MaintenanceEngine;

============================================================
11.6 — CONFLICT SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/relationship/conflict.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Conflict Resolution Engine
 * ========================================
 * SAFE · REPRESENTATIONAL · NO THERAPY
 */

import type { ConflictResolution, ConflictStep, RelationshipMeta } from '../relationship';

export class ConflictEngine {
  private readonly VERSION = '1.0.0';

  structure(input: string): ConflictResolution {
    const lowerInput = input.toLowerCase();

    return {
      id: `conflict-${Date.now()}`,
      situation: 'Conflict situation - To be described',
      parties: ['Party A', 'Party B'],
      approach: this.selectApproach(lowerInput),
      steps: this.generateSteps(lowerInput),
      communicationGuide: this.generateGuide(lowerInput),
      meta: this.createMeta(input),
    };
  }

  private selectApproach(input: string): ConflictResolution['approach'] {
    if (input.includes('win-win') || input.includes('together')) return 'collaborative';
    if (input.includes('compromise') || input.includes('middle')) return 'compromising';
    if (input.includes('yield') || input.includes('relationship')) return 'accommodating';
    if (input.includes('avoid') || input.includes('wait')) return 'avoiding';
    return 'collaborative';
  }

  private generateSteps(input: string): ConflictStep[] {
    return [
      {
        order: 1,
        action: 'Pause and Prepare',
        purpose: 'Create space before engaging',
        tips: ['Take time to calm down', 'Clarify your own needs', 'Choose the right time and place'],
      },
      {
        order: 2,
        action: 'Listen First',
        purpose: 'Understand the other perspective',
        tips: ['Ask open questions', 'Reflect back what you hear', 'Avoid interrupting'],
      },
      {
        order: 3,
        action: 'Express Your Perspective',
        purpose: 'Share your view clearly',
        tips: ['Use "I" statements', 'Focus on impact, not intent', 'Be specific about needs'],
      },
      {
        order: 4,
        action: 'Identify Common Ground',
        purpose: 'Find shared interests',
        tips: ['Look for underlying needs', 'Acknowledge shared goals', 'Build on agreements'],
      },
      {
        order: 5,
        action: 'Explore Solutions',
        purpose: 'Generate options together',
        tips: ['Brainstorm without judgment', 'Consider creative alternatives', 'Evaluate trade-offs'],
      },
      {
        order: 6,
        action: 'Agree and Commit',
        purpose: 'Reach concrete agreement',
        tips: ['Be specific about next steps', 'Set check-in points', 'Document if helpful'],
      },
    ];
  }

  private generateGuide(input: string): string[] {
    return [
      '"I feel [emotion] when [situation] because [impact]..."',
      '"Help me understand your perspective on..."',
      '"What I\'m hearing is... Is that accurate?"',
      '"What would a good outcome look like for you?"',
      '"I think we both want... How can we get there?"',
      '"I appreciate you working through this with me."',
    ];
  }

  private createMeta(source: string): RelationshipMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noTherapy: true, noManipulation: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'ConflictEngine', version: this.VERSION, parent: 'RelationshipEngine' };
  }
}

export default ConflictEngine;

============================================================
11.7 — RELATIONSHIP INDEX & SCHEMA
============================================================

--- FILE: /che-nu-sdk/core/relationship/index.ts

export { NetworkEngine } from './network.engine';
export { RelationCommunicationEngine } from './communication.engine';
export { BoundaryEngine } from './boundary.engine';
export { MaintenanceEngine } from './maintenance.engine';
export { ConflictEngine } from './conflict.engine';

--- FILE: /che-nu-sdk/schemas/relationship.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.io/schemas/relationship.schema.json",
  "title": "CHE·NU Relationship Schema",
  "description": "OPERATIONAL MODULE - NOT A SPHERE. NO therapy. NO manipulation.",
  "type": "object",
  "properties": {
    "network": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "circles": { "type": "array" },
        "totalConnections": { "type": "integer" },
        "healthOverview": { "type": "object" }
      }
    },
    "communicationPlan": {
      "type": "object",
      "properties": {
        "style": { "type": "string", "enum": ["direct", "indirect", "formal", "casual"] },
        "frequency": { "type": "string" },
        "channels": { "type": "array" },
        "boundaries": { "type": "array" }
      }
    },
    "boundaryFramework": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["personal", "professional", "emotional", "time", "digital"] },
        "boundaries": { "type": "array" },
        "communicationScript": { "type": "array" }
      }
    },
    "maintenancePlan": {
      "type": "object",
      "properties": {
        "priority": { "type": "string", "enum": ["high", "medium", "low"] },
        "actions": { "type": "array" },
        "schedule": { "type": "string" }
      }
    },
    "conflictResolution": {
      "type": "object",
      "properties": {
        "approach": { "type": "string", "enum": ["collaborative", "accommodating", "compromising", "avoiding", "competing"] },
        "steps": { "type": "array" },
        "communicationGuide": { "type": "array" }
      }
    },
    "meta": { "type": "object" }
  }
}

############################################################
#                                                          #
#            ENGINE 12: CREATIVITY ENGINE                  #
#                                                          #
############################################################

============================================================
12.1 — CREATIVITY ENGINE (MAIN MODULE)
============================================================

--- FILE: /che-nu-sdk/core/creativity.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Creativity Engine
 * ===============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * CLASSIFICATION: OPERATIONAL MODULE (NOT A SPHERE)
 * 
 * Provides representational structures for creative processes.
 * Frameworks for ideation and creative work. Structure only.
 * 
 * @module CreativityEngine
 * @version 1.0.0
 */

import { IdeationEngine } from './creativity/ideation.engine';
import { BrainstormEngine } from './creativity/brainstorm.engine';
import { ConstraintEngine } from './creativity/constraint.engine';
import { IterationEngine } from './creativity/iteration.engine';
import { EvaluationEngine } from './creativity/evaluation.engine';

// ============================================================
// TYPES
// ============================================================

export interface CreativeProcess {
  id: string;
  name: string;
  phase: 'preparation' | 'incubation' | 'illumination' | 'verification';
  ideation: IdeationSession;
  constraints: CreativeConstraint[];
  iterations: IterationCycle[];
  evaluation: EvaluationCriteria;
  meta: CreativityMeta;
}

export interface IdeationSession {
  id: string;
  technique: 'divergent' | 'convergent' | 'lateral' | 'analogical' | 'random';
  prompts: IdeationPrompt[];
  ideas: IdeaEntry[];
  connections: IdeaConnection[];
}

export interface IdeationPrompt {
  id: string;
  type: 'question' | 'constraint' | 'stimulus' | 'reversal' | 'combination';
  content: string;
  purpose: string;
}

export interface IdeaEntry {
  id: string;
  content: string;
  origin: string;
  category: string;
  potential: 'low' | 'medium' | 'high' | 'breakthrough';
  status: 'raw' | 'developed' | 'evaluated' | 'selected' | 'discarded';
}

export interface IdeaConnection {
  ideaA: string;
  ideaB: string;
  connectionType: 'combines' | 'contrasts' | 'extends' | 'replaces';
}

export interface BrainstormSession {
  id: string;
  type: 'classic' | 'brainwriting' | 'starbursting' | 'scamper' | 'six-hats' | 'mind-map';
  rules: string[];
  phases: BrainstormPhase[];
  output: string[];
  meta: CreativityMeta;
}

export interface BrainstormPhase {
  id: string;
  name: string;
  duration: string;
  focus: string;
  technique: string;
}

export interface CreativeConstraint {
  id: string;
  type: 'resource' | 'time' | 'scope' | 'format' | 'audience' | 'technical';
  description: string;
  impact: 'limiting' | 'enabling' | 'neutral';
  workarounds: string[];
}

export interface IterationCycle {
  id: string;
  version: number;
  changes: string[];
  feedback: string[];
  improvements: string[];
  status: 'draft' | 'review' | 'revised' | 'final';
}

export interface EvaluationCriteria {
  id: string;
  criteria: EvaluationCriterion[];
  method: 'scoring' | 'ranking' | 'voting' | 'discussion';
  weights: Record<string, number>;
}

export interface EvaluationCriterion {
  id: string;
  name: string;
  description: string;
  scale: string;
  weight: number;
}

export interface CreativityMeta {
  source: string;
  generated: string;
  version: string;
  moduleType: 'operational_module';
  classification: 'not_a_sphere';
  safe: {
    isRepresentational: boolean;
  };
}

// ============================================================
// CREATIVITY ENGINE CLASS
// ============================================================

export class CreativityEngine {
  private readonly VERSION = '1.0.0';

  private ideation: IdeationEngine;
  private brainstorm: BrainstormEngine;
  private constraint: ConstraintEngine;
  private iteration: IterationEngine;
  private evaluation: EvaluationEngine;

  constructor() {
    this.ideation = new IdeationEngine();
    this.brainstorm = new BrainstormEngine();
    this.constraint = new ConstraintEngine();
    this.iteration = new IterationEngine();
    this.evaluation = new EvaluationEngine();
  }

  /**
   * Start ideation session
   */
  startIdeation(input: string | Record<string, unknown>): IdeationSession {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.ideation.start(inputStr);
  }

  /**
   * Structure brainstorm session
   */
  structureBrainstorm(input: string | Record<string, unknown>): BrainstormSession {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.brainstorm.structure(inputStr);
  }

  /**
   * Define constraints
   */
  defineConstraints(input: string | Record<string, unknown>): CreativeConstraint[] {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.constraint.define(inputStr);
  }

  /**
   * Plan iteration
   */
  planIteration(input: string | Record<string, unknown>): IterationCycle {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.iteration.plan(inputStr);
  }

  /**
   * Create evaluation framework
   */
  createEvaluationFramework(input: string | Record<string, unknown>): EvaluationCriteria {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.evaluation.create(inputStr);
  }

  /**
   * Get creative prompts
   */
  getCreativePrompts(technique: string): IdeationPrompt[] {
    return this.ideation.getPrompts(technique);
  }

  meta(): Record<string, unknown> {
    return {
      name: 'CreativityEngine',
      version: this.VERSION,
      description: 'Representational creative process structures for CHE·NU',
      classification: {
        type: 'operational_module',
        isNotASphere: true,
        category: 'creativity_operational',
      },
      safe: {
        isRepresentational: true,
      },
      subEngines: [
        'IdeationEngine',
        'BrainstormEngine',
        'ConstraintEngine',
        'IterationEngine',
        'EvaluationEngine'
      ],
    };
  }
}

export function createCreativityEngine(): CreativityEngine {
  return new CreativityEngine();
}

export default CreativityEngine;

============================================================
12.2 — IDEATION SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/creativity/ideation.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Ideation Engine
 * =============================
 * SAFE · REPRESENTATIONAL
 */

import type { IdeationSession, IdeationPrompt, IdeaEntry, CreativityMeta } from '../creativity';

export class IdeationEngine {
  private readonly VERSION = '1.0.0';

  start(input: string): IdeationSession {
    const lowerInput = input.toLowerCase();

    return {
      id: `ideation-${Date.now()}`,
      technique: this.selectTechnique(lowerInput),
      prompts: this.generatePrompts(lowerInput),
      ideas: [],
      connections: [],
    };
  }

  getPrompts(technique: string): IdeationPrompt[] {
    const promptSets: Record<string, IdeationPrompt[]> = {
      divergent: [
        { id: 'p1', type: 'question', content: 'What if there were no constraints?', purpose: 'Remove limitations' },
        { id: 'p2', type: 'question', content: 'How would a child approach this?', purpose: 'Fresh perspective' },
        { id: 'p3', type: 'question', content: 'What is the opposite of the obvious solution?', purpose: 'Challenge assumptions' },
        { id: 'p4', type: 'stimulus', content: 'Combine this with something unrelated', purpose: 'Force connections' },
        { id: 'p5', type: 'reversal', content: 'How could we make this problem worse?', purpose: 'Reverse thinking' },
      ],
      lateral: [
        { id: 'p1', type: 'constraint', content: 'Solve this using only things in nature', purpose: 'Biomimicry' },
        { id: 'p2', type: 'stimulus', content: 'Apply a random word to the problem', purpose: 'Random entry' },
        { id: 'p3', type: 'question', content: 'What would [famous person] do?', purpose: 'Role playing' },
        { id: 'p4', type: 'combination', content: 'Merge two unrelated concepts', purpose: 'Forced association' },
        { id: 'p5', type: 'reversal', content: 'Start from the end and work backwards', purpose: 'Reverse engineering' },
      ],
      analogical: [
        { id: 'p1', type: 'question', content: 'What else works like this?', purpose: 'Find parallels' },
        { id: 'p2', type: 'stimulus', content: 'How is this like a [random object]?', purpose: 'Force metaphor' },
        { id: 'p3', type: 'question', content: 'What solved a similar problem in another field?', purpose: 'Cross-domain' },
        { id: 'p4', type: 'combination', content: 'This is like X meets Y', purpose: 'Hybrid thinking' },
      ],
      default: [
        { id: 'p1', type: 'question', content: 'What problem are we really solving?', purpose: 'Clarify challenge' },
        { id: 'p2', type: 'question', content: 'Who else has this problem?', purpose: 'Expand perspective' },
        { id: 'p3', type: 'question', content: 'What would make this 10x better?', purpose: 'Aim high' },
        { id: 'p4', type: 'constraint', content: 'What if we had unlimited resources?', purpose: 'Remove limits' },
        { id: 'p5', type: 'constraint', content: 'What if we had to solve it today?', purpose: 'Add urgency' },
      ],
    };

    return promptSets[technique] || promptSets.default;
  }

  private selectTechnique(input: string): IdeationSession['technique'] {
    if (input.includes('divergent') || input.includes('many ideas')) return 'divergent';
    if (input.includes('lateral') || input.includes('creative')) return 'lateral';
    if (input.includes('analog') || input.includes('similar')) return 'analogical';
    if (input.includes('random') || input.includes('wild')) return 'random';
    return 'convergent';
  }

  private generatePrompts(input: string): IdeationPrompt[] {
    const technique = this.selectTechnique(input);
    return this.getPrompts(technique);
  }

  meta(): Record<string, unknown> {
    return { name: 'IdeationEngine', version: this.VERSION, parent: 'CreativityEngine' };
  }
}

export default IdeationEngine;

============================================================
12.3 — BRAINSTORM SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/creativity/brainstorm.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Brainstorm Engine
 * ===============================
 * SAFE · REPRESENTATIONAL
 */

import type { BrainstormSession, BrainstormPhase, CreativityMeta } from '../creativity';

export class BrainstormEngine {
  private readonly VERSION = '1.0.0';

  structure(input: string): BrainstormSession {
    const lowerInput = input.toLowerCase();
    const type = this.selectType(lowerInput);

    return {
      id: `brainstorm-${Date.now()}`,
      type,
      rules: this.getRules(type),
      phases: this.getPhases(type),
      output: [],
      meta: this.createMeta(input),
    };
  }

  private selectType(input: string): BrainstormSession['type'] {
    if (input.includes('write') || input.includes('silent')) return 'brainwriting';
    if (input.includes('question') || input.includes('who what')) return 'starbursting';
    if (input.includes('scamper')) return 'scamper';
    if (input.includes('hat') || input.includes('perspective')) return 'six-hats';
    if (input.includes('map') || input.includes('visual')) return 'mind-map';
    return 'classic';
  }

  private getRules(type: string): string[] {
    const baseRules = [
      'No judgment during ideation',
      'Quantity over quality initially',
      'Build on others\' ideas',
      'Encourage wild ideas',
    ];

    const typeRules: Record<string, string[]> = {
      brainwriting: [...baseRules, 'Write silently', 'Pass papers to build on ideas'],
      starbursting: [...baseRules, 'Focus on questions not answers', 'Use Who/What/When/Where/Why/How'],
      scamper: [...baseRules, 'Work through each SCAMPER letter', 'Apply each technique systematically'],
      'six-hats': [...baseRules, 'Wear one hat at a time', 'Everyone uses the same hat together'],
      'mind-map': [...baseRules, 'Start with central concept', 'Branch out freely'],
      classic: baseRules,
    };

    return typeRules[type] || baseRules;
  }

  private getPhases(type: string): BrainstormPhase[] {
    const phaseTemplates: Record<string, BrainstormPhase[]> = {
      classic: [
        { id: 'ph-1', name: 'Warm-up', duration: '5 min', focus: 'Get creative juices flowing', technique: 'Quick ideation exercise' },
        { id: 'ph-2', name: 'Divergent', duration: '20 min', focus: 'Generate many ideas', technique: 'Free association' },
        { id: 'ph-3', name: 'Build', duration: '10 min', focus: 'Combine and extend ideas', technique: 'Yes, and...' },
        { id: 'ph-4', name: 'Converge', duration: '15 min', focus: 'Group and prioritize', technique: 'Affinity mapping' },
      ],
      scamper: [
        { id: 'ph-1', name: 'Substitute', duration: '5 min', focus: 'What can be replaced?', technique: 'SCAMPER-S' },
        { id: 'ph-2', name: 'Combine', duration: '5 min', focus: 'What can be merged?', technique: 'SCAMPER-C' },
        { id: 'ph-3', name: 'Adapt', duration: '5 min', focus: 'What can be adjusted?', technique: 'SCAMPER-A' },
        { id: 'ph-4', name: 'Modify', duration: '5 min', focus: 'What can be changed?', technique: 'SCAMPER-M' },
        { id: 'ph-5', name: 'Put to other use', duration: '5 min', focus: 'Other applications?', technique: 'SCAMPER-P' },
        { id: 'ph-6', name: 'Eliminate', duration: '5 min', focus: 'What can be removed?', technique: 'SCAMPER-E' },
        { id: 'ph-7', name: 'Reverse', duration: '5 min', focus: 'What if reversed?', technique: 'SCAMPER-R' },
      ],
      'six-hats': [
        { id: 'ph-1', name: 'White Hat', duration: '5 min', focus: 'Facts and information', technique: 'Objective data' },
        { id: 'ph-2', name: 'Red Hat', duration: '5 min', focus: 'Emotions and intuition', technique: 'Gut feelings' },
        { id: 'ph-3', name: 'Black Hat', duration: '5 min', focus: 'Caution and risks', technique: 'Critical thinking' },
        { id: 'ph-4', name: 'Yellow Hat', duration: '5 min', focus: 'Benefits and value', technique: 'Optimistic view' },
        { id: 'ph-5', name: 'Green Hat', duration: '10 min', focus: 'Creativity and alternatives', technique: 'New ideas' },
        { id: 'ph-6', name: 'Blue Hat', duration: '5 min', focus: 'Process and next steps', technique: 'Meta-thinking' },
      ],
    };

    return phaseTemplates[type] || phaseTemplates.classic;
  }

  private createMeta(source: string): CreativityMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'BrainstormEngine', version: this.VERSION, parent: 'CreativityEngine' };
  }
}

export default BrainstormEngine;

============================================================
12.4-12.5 — CONSTRAINT, ITERATION, EVALUATION SUB-ENGINES
============================================================

--- FILE: /che-nu-sdk/core/creativity/constraint.engine.ts

import type { CreativeConstraint } from '../creativity';

export class ConstraintEngine {
  private readonly VERSION = '1.0.0';

  define(input: string): CreativeConstraint[] {
    return [
      {
        id: 'const-1',
        type: 'time',
        description: 'Timeline for completion',
        impact: 'limiting',
        workarounds: ['Prioritize ruthlessly', 'Scope reduction', 'Parallel workstreams'],
      },
      {
        id: 'const-2',
        type: 'resource',
        description: 'Available resources (people, budget, tools)',
        impact: 'limiting',
        workarounds: ['Creative resource sharing', 'Phased approach', 'Trade-offs'],
      },
      {
        id: 'const-3',
        type: 'scope',
        description: 'Boundaries of the creative work',
        impact: 'enabling',
        workarounds: ['Focus breeds creativity', 'Clear boundaries free thinking'],
      },
      {
        id: 'const-4',
        type: 'audience',
        description: 'Who the work is for',
        impact: 'enabling',
        workarounds: ['User-centered design', 'Empathy mapping', 'Persona focus'],
      },
      {
        id: 'const-5',
        type: 'format',
        description: 'Output format requirements',
        impact: 'neutral',
        workarounds: ['Embrace the medium', 'Find format-specific advantages'],
      },
    ];
  }

  meta() { return { name: 'ConstraintEngine', version: this.VERSION, parent: 'CreativityEngine' }; }
}

--- FILE: /che-nu-sdk/core/creativity/iteration.engine.ts

import type { IterationCycle } from '../creativity';

export class IterationEngine {
  private readonly VERSION = '1.0.0';

  plan(input: string): IterationCycle {
    return {
      id: `iter-${Date.now()}`,
      version: 1,
      changes: ['Initial creation'],
      feedback: [],
      improvements: ['To be identified through review'],
      status: 'draft',
    };
  }

  getIterationGuidelines(): string[] {
    return [
      'Start rough, refine iteratively',
      'Get feedback early and often',
      'Kill your darlings - be willing to change',
      'Document decisions for future reference',
      'Time-box iterations',
      'Focus each iteration on specific improvements',
    ];
  }

  meta() { return { name: 'IterationEngine', version: this.VERSION, parent: 'CreativityEngine' }; }
}

--- FILE: /che-nu-sdk/core/creativity/evaluation.engine.ts

import type { EvaluationCriteria, EvaluationCriterion } from '../creativity';

export class EvaluationEngine {
  private readonly VERSION = '1.0.0';

  create(input: string): EvaluationCriteria {
    return {
      id: `eval-${Date.now()}`,
      criteria: this.generateCriteria(input),
      method: 'scoring',
      weights: {
        'originality': 0.25,
        'feasibility': 0.25,
        'impact': 0.25,
        'alignment': 0.25,
      },
    };
  }

  private generateCriteria(input: string): EvaluationCriterion[] {
    return [
      { id: 'crit-1', name: 'Originality', description: 'How novel is the idea?', scale: '1-5', weight: 0.25 },
      { id: 'crit-2', name: 'Feasibility', description: 'How achievable is this?', scale: '1-5', weight: 0.25 },
      { id: 'crit-3', name: 'Impact', description: 'What value does it create?', scale: '1-5', weight: 0.25 },
      { id: 'crit-4', name: 'Alignment', description: 'How well does it fit goals?', scale: '1-5', weight: 0.25 },
    ];
  }

  meta() { return { name: 'EvaluationEngine', version: this.VERSION, parent: 'CreativityEngine' }; }
}

============================================================
12.6 — CREATIVITY INDEX & SCHEMA
============================================================

--- FILE: /che-nu-sdk/core/creativity/index.ts

export { IdeationEngine } from './ideation.engine';
export { BrainstormEngine } from './brainstorm.engine';
export { ConstraintEngine } from './constraint.engine';
export { IterationEngine } from './iteration.engine';
export { EvaluationEngine } from './evaluation.engine';

--- FILE: /che-nu-sdk/schemas/creativity.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.io/schemas/creativity.schema.json",
  "title": "CHE·NU Creativity Schema",
  "description": "OPERATIONAL MODULE - NOT A SPHERE. Creative process structures.",
  "type": "object",
  "properties": {
    "ideation": {
      "type": "object",
      "properties": {
        "technique": { "type": "string", "enum": ["divergent", "convergent", "lateral", "analogical", "random"] },
        "prompts": { "type": "array" },
        "ideas": { "type": "array" },
        "connections": { "type": "array" }
      }
    },
    "brainstorm": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["classic", "brainwriting", "starbursting", "scamper", "six-hats", "mind-map"] },
        "rules": { "type": "array" },
        "phases": { "type": "array" }
      }
    },
    "constraints": { "type": "array" },
    "iteration": { "type": "object" },
    "evaluation": { "type": "object" },
    "meta": { "type": "object" }
  }
}
