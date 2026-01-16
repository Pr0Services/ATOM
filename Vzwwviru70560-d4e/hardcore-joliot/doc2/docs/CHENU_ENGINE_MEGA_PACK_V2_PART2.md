############################################################
#                                                          #
#              ENGINE 7: PROJECT ENGINE                    #
#                                                          #
############################################################

============================================================
7.1 — PROJECT ENGINE (MAIN MODULE)
============================================================

--- FILE: /che-nu-sdk/core/project.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Project Engine
 * ============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * CLASSIFICATION: OPERATIONAL MODULE (NOT A SPHERE)
 * 
 * Provides representational structures for project management.
 * NO real project creation. NO external tools. Structure only.
 * 
 * @module ProjectEngine
 * @version 1.0.0
 */

import { PhaseEngine } from './project/phase.engine';
import { MilestoneEngine } from './project/milestone.engine';
import { ResourceEngine } from './project/resource.engine';
import { TimelineEngine } from './project/timeline.engine';
import { RiskEngine } from './project/risk.engine';

// ============================================================
// TYPES
// ============================================================

export interface ProjectStructure {
  id: string;
  name: string;
  type: 'waterfall' | 'agile' | 'hybrid' | 'kanban' | 'custom';
  status: 'planning' | 'active' | 'on-hold' | 'completed' | 'cancelled';
  phases: ProjectPhase[];
  milestones: ProjectMilestone[];
  resources: ResourceAllocation;
  timeline: ProjectTimeline;
  risks: ProjectRisk[];
  meta: ProjectMeta;
}

export interface ProjectPhase {
  id: string;
  name: string;
  order: number;
  status: 'pending' | 'active' | 'completed' | 'blocked';
  deliverables: string[];
  dependencies: string[];
  estimatedDuration: string;
  completionCriteria: string[];
}

export interface ProjectMilestone {
  id: string;
  name: string;
  phaseId: string;
  type: 'checkpoint' | 'deliverable' | 'decision' | 'review';
  status: 'pending' | 'achieved' | 'missed' | 'at-risk';
  criteria: string[];
  dependencies: string[];
}

export interface ResourceAllocation {
  id: string;
  categories: ResourceCategory[];
  constraints: string[];
  optimization: string[];
}

export interface ResourceCategory {
  id: string;
  type: 'human' | 'financial' | 'technical' | 'material' | 'time';
  allocated: string;
  available: string;
  utilization: 'under' | 'optimal' | 'over';
}

export interface ProjectTimeline {
  id: string;
  startDate: string;
  endDate: string;
  duration: string;
  phases: TimelinePhase[];
  criticalPath: string[];
  buffer: string;
}

export interface TimelinePhase {
  phaseId: string;
  start: string;
  end: string;
  isCritical: boolean;
  dependencies: string[];
}

export interface ProjectRisk {
  id: string;
  name: string;
  category: 'technical' | 'resource' | 'schedule' | 'scope' | 'external' | 'quality';
  probability: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high';
  mitigation: string[];
  contingency: string[];
  status: 'identified' | 'monitoring' | 'mitigating' | 'resolved';
}

export interface ProjectMeta {
  source: string;
  generated: string;
  version: string;
  moduleType: 'operational_module';
  classification: 'not_a_sphere';
  safe: {
    isRepresentational: boolean;
    noRealProjectCreation: boolean;
    noExternalTools: boolean;
  };
}

// ============================================================
// PROJECT ENGINE CLASS
// ============================================================

export class ProjectEngine {
  private readonly VERSION = '1.0.0';

  private phase: PhaseEngine;
  private milestone: MilestoneEngine;
  private resource: ResourceEngine;
  private timeline: TimelineEngine;
  private risk: RiskEngine;

  constructor() {
    this.phase = new PhaseEngine();
    this.milestone = new MilestoneEngine();
    this.resource = new ResourceEngine();
    this.timeline = new TimelineEngine();
    this.risk = new RiskEngine();
  }

  /**
   * Structure a complete project
   */
  structureProject(input: string | Record<string, unknown>): ProjectStructure {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);

    return {
      id: `proj-${Date.now()}`,
      name: this.extractProjectName(inputStr),
      type: this.determineProjectType(inputStr),
      status: 'planning',
      phases: this.phase.generate(inputStr),
      milestones: this.milestone.generate(inputStr),
      resources: this.resource.allocate(inputStr),
      timeline: this.timeline.create(inputStr),
      risks: this.risk.identify(inputStr),
      meta: this.createMeta(inputStr),
    };
  }

  /**
   * Generate project phases
   */
  generatePhases(input: string | Record<string, unknown>): ProjectPhase[] {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.phase.generate(inputStr);
  }

  /**
   * Define milestones
   */
  defineMilestones(input: string | Record<string, unknown>): ProjectMilestone[] {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.milestone.generate(inputStr);
  }

  /**
   * Plan resources
   */
  planResources(input: string | Record<string, unknown>): ResourceAllocation {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.resource.allocate(inputStr);
  }

  /**
   * Create timeline
   */
  createTimeline(input: string | Record<string, unknown>): ProjectTimeline {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.timeline.create(inputStr);
  }

  /**
   * Assess risks
   */
  assessRisks(input: string | Record<string, unknown>): ProjectRisk[] {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.risk.identify(inputStr);
  }

  meta(): Record<string, unknown> {
    return {
      name: 'ProjectEngine',
      version: this.VERSION,
      description: 'Representational project management structures for CHE·NU',
      classification: {
        type: 'operational_module',
        isNotASphere: true,
        category: 'project_operational',
      },
      safe: {
        isRepresentational: true,
        noRealProjectCreation: true,
        noExternalTools: true,
      },
      subEngines: [
        'PhaseEngine',
        'MilestoneEngine',
        'ResourceEngine',
        'TimelineEngine',
        'RiskEngine'
      ],
      capabilities: [
        'structureProject',
        'generatePhases',
        'defineMilestones',
        'planResources',
        'createTimeline',
        'assessRisks',
      ],
    };
  }

  private extractProjectName(input: string): string {
    return 'Project - To Be Named';
  }

  private determineProjectType(input: string): ProjectStructure['type'] {
    const lowerInput = input.toLowerCase();
    if (lowerInput.includes('agile') || lowerInput.includes('sprint')) return 'agile';
    if (lowerInput.includes('waterfall') || lowerInput.includes('sequential')) return 'waterfall';
    if (lowerInput.includes('kanban')) return 'kanban';
    if (lowerInput.includes('hybrid')) return 'hybrid';
    return 'custom';
  }

  private createMeta(source: string): ProjectMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: {
        isRepresentational: true,
        noRealProjectCreation: true,
        noExternalTools: true,
      },
    };
  }
}

export function createProjectEngine(): ProjectEngine {
  return new ProjectEngine();
}

export default ProjectEngine;

============================================================
7.2 — PHASE SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/project/phase.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Phase Engine
 * ==========================
 * SAFE · REPRESENTATIONAL
 */

import type { ProjectPhase } from '../project';

export class PhaseEngine {
  private readonly VERSION = '1.0.0';

  generate(input: string): ProjectPhase[] {
    const lowerInput = input.toLowerCase();
    const isAgile = lowerInput.includes('agile') || lowerInput.includes('sprint');

    if (isAgile) {
      return this.generateAgilePhases();
    }
    return this.generateStandardPhases();
  }

  private generateStandardPhases(): ProjectPhase[] {
    return [
      {
        id: 'phase-1',
        name: 'Initiation',
        order: 1,
        status: 'pending',
        deliverables: ['Project charter', 'Stakeholder register', 'Initial scope'],
        dependencies: [],
        estimatedDuration: '1-2 weeks',
        completionCriteria: ['Charter approved', 'Stakeholders identified'],
      },
      {
        id: 'phase-2',
        name: 'Planning',
        order: 2,
        status: 'pending',
        deliverables: ['Project plan', 'Risk register', 'Resource plan', 'Schedule'],
        dependencies: ['phase-1'],
        estimatedDuration: '2-4 weeks',
        completionCriteria: ['Plan approved', 'Resources allocated'],
      },
      {
        id: 'phase-3',
        name: 'Execution',
        order: 3,
        status: 'pending',
        deliverables: ['Work products', 'Progress reports', 'Quality deliverables'],
        dependencies: ['phase-2'],
        estimatedDuration: 'Variable',
        completionCriteria: ['Deliverables completed', 'Quality standards met'],
      },
      {
        id: 'phase-4',
        name: 'Monitoring & Control',
        order: 4,
        status: 'pending',
        deliverables: ['Status reports', 'Change requests', 'Performance data'],
        dependencies: ['phase-3'],
        estimatedDuration: 'Ongoing',
        completionCriteria: ['Metrics tracked', 'Issues resolved'],
      },
      {
        id: 'phase-5',
        name: 'Closure',
        order: 5,
        status: 'pending',
        deliverables: ['Final report', 'Lessons learned', 'Archive'],
        dependencies: ['phase-3', 'phase-4'],
        estimatedDuration: '1-2 weeks',
        completionCriteria: ['Sign-off received', 'Documentation complete'],
      },
    ];
  }

  private generateAgilePhases(): ProjectPhase[] {
    return [
      {
        id: 'phase-1',
        name: 'Product Backlog Creation',
        order: 1,
        status: 'pending',
        deliverables: ['User stories', 'Product backlog', 'Initial prioritization'],
        dependencies: [],
        estimatedDuration: '1 week',
        completionCriteria: ['Backlog created', 'Stories estimated'],
      },
      {
        id: 'phase-2',
        name: 'Sprint Planning',
        order: 2,
        status: 'pending',
        deliverables: ['Sprint backlog', 'Sprint goal', 'Capacity plan'],
        dependencies: ['phase-1'],
        estimatedDuration: '1 day per sprint',
        completionCriteria: ['Sprint backlog defined', 'Team committed'],
      },
      {
        id: 'phase-3',
        name: 'Sprint Execution',
        order: 3,
        status: 'pending',
        deliverables: ['Increment', 'Daily updates', 'Impediment log'],
        dependencies: ['phase-2'],
        estimatedDuration: '1-4 weeks per sprint',
        completionCriteria: ['Increment delivered', 'Definition of Done met'],
      },
      {
        id: 'phase-4',
        name: 'Sprint Review',
        order: 4,
        status: 'pending',
        deliverables: ['Demo', 'Feedback', 'Updated backlog'],
        dependencies: ['phase-3'],
        estimatedDuration: '2-4 hours',
        completionCriteria: ['Increment reviewed', 'Feedback collected'],
      },
      {
        id: 'phase-5',
        name: 'Sprint Retrospective',
        order: 5,
        status: 'pending',
        deliverables: ['Improvement actions', 'Process updates'],
        dependencies: ['phase-4'],
        estimatedDuration: '1-3 hours',
        completionCriteria: ['Actions identified', 'Team aligned'],
      },
    ];
  }

  meta(): Record<string, unknown> {
    return {
      name: 'PhaseEngine',
      version: this.VERSION,
      parent: 'ProjectEngine',
      type: 'sub_engine',
      safe: { isRepresentational: true },
    };
  }
}

export default PhaseEngine;

============================================================
7.3 — MILESTONE SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/project/milestone.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Milestone Engine
 * ==============================
 * SAFE · REPRESENTATIONAL
 */

import type { ProjectMilestone } from '../project';

export class MilestoneEngine {
  private readonly VERSION = '1.0.0';

  generate(input: string): ProjectMilestone[] {
    return [
      {
        id: 'ms-1',
        name: 'Project Kickoff',
        phaseId: 'phase-1',
        type: 'checkpoint',
        status: 'pending',
        criteria: ['Team assembled', 'Resources confirmed', 'Goals aligned'],
        dependencies: [],
      },
      {
        id: 'ms-2',
        name: 'Requirements Complete',
        phaseId: 'phase-2',
        type: 'deliverable',
        status: 'pending',
        criteria: ['Requirements documented', 'Stakeholder sign-off', 'Scope baseline'],
        dependencies: ['ms-1'],
      },
      {
        id: 'ms-3',
        name: 'Design Approval',
        phaseId: 'phase-2',
        type: 'decision',
        status: 'pending',
        criteria: ['Design reviewed', 'Technical feasibility confirmed', 'Approval received'],
        dependencies: ['ms-2'],
      },
      {
        id: 'ms-4',
        name: 'Development Complete',
        phaseId: 'phase-3',
        type: 'deliverable',
        status: 'pending',
        criteria: ['Code complete', 'Unit tests passed', 'Documentation ready'],
        dependencies: ['ms-3'],
      },
      {
        id: 'ms-5',
        name: 'Testing Complete',
        phaseId: 'phase-3',
        type: 'checkpoint',
        status: 'pending',
        criteria: ['Test cases executed', 'Bugs resolved', 'Quality metrics met'],
        dependencies: ['ms-4'],
      },
      {
        id: 'ms-6',
        name: 'Go-Live Decision',
        phaseId: 'phase-4',
        type: 'decision',
        status: 'pending',
        criteria: ['Readiness review', 'Risk assessment', 'Stakeholder approval'],
        dependencies: ['ms-5'],
      },
      {
        id: 'ms-7',
        name: 'Project Closure',
        phaseId: 'phase-5',
        type: 'review',
        status: 'pending',
        criteria: ['Deliverables accepted', 'Lessons documented', 'Resources released'],
        dependencies: ['ms-6'],
      },
    ];
  }

  meta(): Record<string, unknown> {
    return {
      name: 'MilestoneEngine',
      version: this.VERSION,
      parent: 'ProjectEngine',
      type: 'sub_engine',
      safe: { isRepresentational: true },
    };
  }
}

export default MilestoneEngine;

============================================================
7.4 — RESOURCE SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/project/resource.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Resource Engine
 * =============================
 * SAFE · REPRESENTATIONAL · NO REAL ALLOCATIONS
 */

import type { ResourceAllocation, ResourceCategory } from '../project';

export class ResourceEngine {
  private readonly VERSION = '1.0.0';

  allocate(input: string): ResourceAllocation {
    return {
      id: `resource-${Date.now()}`,
      categories: this.generateCategories(input),
      constraints: this.identifyConstraints(input),
      optimization: this.suggestOptimizations(input),
    };
  }

  private generateCategories(input: string): ResourceCategory[] {
    return [
      {
        id: 'res-human',
        type: 'human',
        allocated: 'Team members - To be defined',
        available: 'Based on capacity',
        utilization: 'optimal',
      },
      {
        id: 'res-financial',
        type: 'financial',
        allocated: 'Budget - To be defined',
        available: 'Based on approval',
        utilization: 'optimal',
      },
      {
        id: 'res-technical',
        type: 'technical',
        allocated: 'Tools & infrastructure',
        available: 'Based on requirements',
        utilization: 'optimal',
      },
      {
        id: 'res-material',
        type: 'material',
        allocated: 'Physical resources',
        available: 'Based on procurement',
        utilization: 'optimal',
      },
      {
        id: 'res-time',
        type: 'time',
        allocated: 'Project duration',
        available: 'Based on schedule',
        utilization: 'optimal',
      },
    ];
  }

  private identifyConstraints(input: string): string[] {
    return [
      'Budget limitations',
      'Timeline constraints',
      'Resource availability',
      'Technical dependencies',
      'Skill requirements',
    ];
  }

  private suggestOptimizations(input: string): string[] {
    return [
      'Cross-training for flexibility',
      'Resource leveling',
      'Prioritization of critical path',
      'Buffer management',
      'Parallel task execution where possible',
    ];
  }

  meta(): Record<string, unknown> {
    return {
      name: 'ResourceEngine',
      version: this.VERSION,
      parent: 'ProjectEngine',
      type: 'sub_engine',
      safe: { isRepresentational: true, noRealAllocations: true },
    };
  }
}

export default ResourceEngine;

============================================================
7.5 — TIMELINE SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/project/timeline.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Timeline Engine
 * =============================
 * SAFE · REPRESENTATIONAL
 */

import type { ProjectTimeline, TimelinePhase } from '../project';

export class TimelineEngine {
  private readonly VERSION = '1.0.0';

  create(input: string): ProjectTimeline {
    return {
      id: `timeline-${Date.now()}`,
      startDate: 'To be defined',
      endDate: 'To be defined',
      duration: this.estimateDuration(input),
      phases: this.generateTimelinePhases(input),
      criticalPath: this.identifyCriticalPath(input),
      buffer: this.calculateBuffer(input),
    };
  }

  private estimateDuration(input: string): string {
    const lowerInput = input.toLowerCase();
    if (lowerInput.includes('short') || lowerInput.includes('quick')) return '1-3 months';
    if (lowerInput.includes('long') || lowerInput.includes('complex')) return '12+ months';
    if (lowerInput.includes('medium')) return '3-6 months';
    return '6-12 months';
  }

  private generateTimelinePhases(input: string): TimelinePhase[] {
    return [
      { phaseId: 'phase-1', start: 'Week 1', end: 'Week 2', isCritical: true, dependencies: [] },
      { phaseId: 'phase-2', start: 'Week 3', end: 'Week 6', isCritical: true, dependencies: ['phase-1'] },
      { phaseId: 'phase-3', start: 'Week 7', end: 'Week 16', isCritical: true, dependencies: ['phase-2'] },
      { phaseId: 'phase-4', start: 'Week 7', end: 'Week 16', isCritical: false, dependencies: ['phase-2'] },
      { phaseId: 'phase-5', start: 'Week 17', end: 'Week 18', isCritical: true, dependencies: ['phase-3', 'phase-4'] },
    ];
  }

  private identifyCriticalPath(input: string): string[] {
    return ['phase-1', 'phase-2', 'phase-3', 'phase-5'];
  }

  private calculateBuffer(input: string): string {
    return '10-20% of total duration';
  }

  meta(): Record<string, unknown> {
    return {
      name: 'TimelineEngine',
      version: this.VERSION,
      parent: 'ProjectEngine',
      type: 'sub_engine',
      safe: { isRepresentational: true },
    };
  }
}

export default TimelineEngine;

============================================================
7.6 — RISK SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/project/risk.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Risk Engine
 * =========================
 * SAFE · REPRESENTATIONAL
 */

import type { ProjectRisk } from '../project';

export class RiskEngine {
  private readonly VERSION = '1.0.0';

  identify(input: string): ProjectRisk[] {
    return [
      {
        id: 'risk-1',
        name: 'Scope Creep',
        category: 'scope',
        probability: 'high',
        impact: 'high',
        mitigation: ['Clear change process', 'Regular scope reviews', 'Stakeholder alignment'],
        contingency: ['Reprioritization', 'Scope reduction', 'Timeline adjustment'],
        status: 'identified',
      },
      {
        id: 'risk-2',
        name: 'Resource Availability',
        category: 'resource',
        probability: 'medium',
        impact: 'high',
        mitigation: ['Early commitment', 'Cross-training', 'Backup resources'],
        contingency: ['Outsourcing', 'Scope adjustment', 'Timeline extension'],
        status: 'identified',
      },
      {
        id: 'risk-3',
        name: 'Technical Complexity',
        category: 'technical',
        probability: 'medium',
        impact: 'medium',
        mitigation: ['Prototyping', 'Expert consultation', 'Technical reviews'],
        contingency: ['Alternative solutions', 'Simplified approach', 'Expert hiring'],
        status: 'identified',
      },
      {
        id: 'risk-4',
        name: 'Schedule Delays',
        category: 'schedule',
        probability: 'high',
        impact: 'medium',
        mitigation: ['Buffer time', 'Critical path focus', 'Regular tracking'],
        contingency: ['Fast-tracking', 'Crashing', 'Scope reduction'],
        status: 'identified',
      },
      {
        id: 'risk-5',
        name: 'Quality Issues',
        category: 'quality',
        probability: 'low',
        impact: 'high',
        mitigation: ['Quality standards', 'Testing strategy', 'Reviews'],
        contingency: ['Rework allocation', 'Expert review', 'Release criteria'],
        status: 'identified',
      },
      {
        id: 'risk-6',
        name: 'External Dependencies',
        category: 'external',
        probability: 'medium',
        impact: 'medium',
        mitigation: ['Early engagement', 'Contracts', 'Monitoring'],
        contingency: ['Alternative vendors', 'In-house development', 'Workarounds'],
        status: 'identified',
      },
    ];
  }

  assessRiskLevel(risk: ProjectRisk): string {
    const matrix: Record<string, Record<string, string>> = {
      high: { high: 'critical', medium: 'high', low: 'medium' },
      medium: { high: 'high', medium: 'medium', low: 'low' },
      low: { high: 'medium', medium: 'low', low: 'minimal' },
    };
    return matrix[risk.probability][risk.impact];
  }

  meta(): Record<string, unknown> {
    return {
      name: 'RiskEngine',
      version: this.VERSION,
      parent: 'ProjectEngine',
      type: 'sub_engine',
      safe: { isRepresentational: true },
    };
  }
}

export default RiskEngine;

============================================================
7.7 — PROJECT INDEX
============================================================

--- FILE: /che-nu-sdk/core/project/index.ts
--- ACTION: CREATE NEW FILE

export { PhaseEngine } from './phase.engine';
export { MilestoneEngine } from './milestone.engine';
export { ResourceEngine } from './resource.engine';
export { TimelineEngine } from './timeline.engine';
export { RiskEngine } from './risk.engine';

============================================================
7.8 — PROJECT SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/project.schema.json
--- ACTION: CREATE NEW FILE

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.io/schemas/project.schema.json",
  "title": "CHE·NU Project Schema",
  "description": "OPERATIONAL MODULE - NOT A SPHERE. Representational project structures.",
  "type": "object",
  "definitions": {
    "ProjectPhase": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "order": { "type": "integer" },
        "status": { "type": "string", "enum": ["pending", "active", "completed", "blocked"] },
        "deliverables": { "type": "array", "items": { "type": "string" } },
        "dependencies": { "type": "array", "items": { "type": "string" } },
        "estimatedDuration": { "type": "string" },
        "completionCriteria": { "type": "array", "items": { "type": "string" } }
      }
    },
    "ProjectMilestone": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "phaseId": { "type": "string" },
        "type": { "type": "string", "enum": ["checkpoint", "deliverable", "decision", "review"] },
        "status": { "type": "string", "enum": ["pending", "achieved", "missed", "at-risk"] },
        "criteria": { "type": "array" },
        "dependencies": { "type": "array" }
      }
    },
    "ProjectRisk": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "category": { "type": "string", "enum": ["technical", "resource", "schedule", "scope", "external", "quality"] },
        "probability": { "type": "string", "enum": ["low", "medium", "high"] },
        "impact": { "type": "string", "enum": ["low", "medium", "high"] },
        "mitigation": { "type": "array" },
        "contingency": { "type": "array" },
        "status": { "type": "string" }
      }
    }
  },
  "properties": {
    "phases": { "type": "array", "items": { "$ref": "#/definitions/ProjectPhase" } },
    "milestones": { "type": "array", "items": { "$ref": "#/definitions/ProjectMilestone" } },
    "resources": { "type": "object" },
    "timeline": { "type": "object" },
    "risks": { "type": "array", "items": { "$ref": "#/definitions/ProjectRisk" } },
    "meta": { "type": "object" }
  }
}

############################################################
#                                                          #
#              ENGINE 8: LEARNING ENGINE                   #
#                                                          #
############################################################

============================================================
8.1 — LEARNING ENGINE (MAIN MODULE)
============================================================

--- FILE: /che-nu-sdk/core/learning.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Learning Engine
 * =============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * CLASSIFICATION: OPERATIONAL MODULE (NOT A SPHERE)
 * 
 * Provides representational structures for learning & development.
 * NO real content delivery. NO assessments with scores. Structure only.
 * 
 * @module LearningEngine
 * @version 1.0.0
 */

import { PathEngine } from './learning/path.engine';
import { ProgressEngine } from './learning/progress.engine';
import { RetentionEngine } from './learning/retention.engine';
import { AssessmentEngine } from './learning/assessment.engine';
import { LearningResourceEngine } from './learning/resource.engine';

// ============================================================
// TYPES
// ============================================================

export interface LearningPath {
  id: string;
  name: string;
  domain: string;
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  stages: LearningStage[];
  prerequisites: string[];
  estimatedDuration: string;
  outcomes: string[];
  meta: LearningMeta;
}

export interface LearningStage {
  id: string;
  name: string;
  order: number;
  type: 'foundation' | 'core' | 'application' | 'mastery';
  topics: LearningTopic[];
  completionCriteria: string[];
  estimatedDuration: string;
}

export interface LearningTopic {
  id: string;
  name: string;
  type: 'concept' | 'skill' | 'practice' | 'project';
  priority: 'essential' | 'important' | 'optional';
  resources: ResourceReference[];
  activities: string[];
}

export interface ResourceReference {
  type: 'reading' | 'video' | 'practice' | 'project' | 'discussion';
  format: string;
  estimatedTime: string;
}

export interface LearningProgress {
  id: string;
  pathId: string;
  currentStage: string;
  completedTopics: string[];
  pendingTopics: string[];
  progressPercentage: number;
  nextSteps: string[];
  meta: LearningMeta;
}

export interface RetentionPlan {
  id: string;
  strategy: 'spaced-repetition' | 'active-recall' | 'interleaving' | 'elaboration';
  schedule: RetentionSchedule[];
  techniques: string[];
  meta: LearningMeta;
}

export interface RetentionSchedule {
  interval: string;
  activity: string;
  focus: string;
}

export interface AssessmentStructure {
  id: string;
  type: 'self-assessment' | 'knowledge-check' | 'skill-evaluation' | 'project-review';
  criteria: AssessmentCriterion[];
  format: string;
  meta: LearningMeta;
}

export interface AssessmentCriterion {
  id: string;
  name: string;
  description: string;
  level: 'basic' | 'proficient' | 'advanced';
}

export interface LearningMeta {
  source: string;
  generated: string;
  version: string;
  moduleType: 'operational_module';
  classification: 'not_a_sphere';
  safe: {
    isRepresentational: boolean;
    noRealContentDelivery: boolean;
    noRealAssessments: boolean;
  };
}

// ============================================================
// LEARNING ENGINE CLASS
// ============================================================

export class LearningEngine {
  private readonly VERSION = '1.0.0';

  private path: PathEngine;
  private progress: ProgressEngine;
  private retention: RetentionEngine;
  private assessment: AssessmentEngine;
  private resource: LearningResourceEngine;

  constructor() {
    this.path = new PathEngine();
    this.progress = new ProgressEngine();
    this.retention = new RetentionEngine();
    this.assessment = new AssessmentEngine();
    this.resource = new LearningResourceEngine();
  }

  /**
   * Create learning path
   */
  createLearningPath(input: string | Record<string, unknown>): LearningPath {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.path.create(inputStr);
  }

  /**
   * Track progress
   */
  trackProgress(input: string | Record<string, unknown>): LearningProgress {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.progress.track(inputStr);
  }

  /**
   * Plan retention
   */
  planRetention(input: string | Record<string, unknown>): RetentionPlan {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.retention.plan(inputStr);
  }

  /**
   * Structure assessment
   */
  structureAssessment(input: string | Record<string, unknown>): AssessmentStructure {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.assessment.structure(inputStr);
  }

  /**
   * Suggest resources
   */
  suggestResources(input: string | Record<string, unknown>): ResourceReference[] {
    const inputStr = typeof input === 'string' ? input : JSON.stringify(input);
    return this.resource.suggest(inputStr);
  }

  meta(): Record<string, unknown> {
    return {
      name: 'LearningEngine',
      version: this.VERSION,
      description: 'Representational learning structures for CHE·NU',
      classification: {
        type: 'operational_module',
        isNotASphere: true,
        category: 'learning_operational',
      },
      safe: {
        isRepresentational: true,
        noRealContentDelivery: true,
        noRealAssessments: true,
      },
      subEngines: [
        'PathEngine',
        'ProgressEngine',
        'RetentionEngine',
        'AssessmentEngine',
        'ResourceEngine'
      ],
    };
  }
}

export function createLearningEngine(): LearningEngine {
  return new LearningEngine();
}

export default LearningEngine;

============================================================
8.2 — PATH SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/learning/path.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Learning Path Engine
 * ==================================
 * SAFE · REPRESENTATIONAL
 */

import type { LearningPath, LearningStage, LearningTopic, LearningMeta } from '../learning';

export class PathEngine {
  private readonly VERSION = '1.0.0';

  create(input: string): LearningPath {
    const lowerInput = input.toLowerCase();

    return {
      id: `path-${Date.now()}`,
      name: this.extractPathName(lowerInput),
      domain: this.identifyDomain(lowerInput),
      level: this.determineLevel(lowerInput),
      stages: this.generateStages(lowerInput),
      prerequisites: this.identifyPrerequisites(lowerInput),
      estimatedDuration: this.estimateDuration(lowerInput),
      outcomes: this.defineOutcomes(lowerInput),
      meta: this.createMeta(input),
    };
  }

  private extractPathName(input: string): string {
    return 'Learning Path - To Be Named';
  }

  private identifyDomain(input: string): string {
    if (input.includes('programming') || input.includes('code')) return 'Technical';
    if (input.includes('design')) return 'Creative';
    if (input.includes('business') || input.includes('management')) return 'Business';
    if (input.includes('language')) return 'Language';
    return 'General';
  }

  private determineLevel(input: string): LearningPath['level'] {
    if (input.includes('beginner') || input.includes('start')) return 'beginner';
    if (input.includes('advanced') || input.includes('deep')) return 'advanced';
    if (input.includes('expert') || input.includes('master')) return 'expert';
    return 'intermediate';
  }

  private generateStages(input: string): LearningStage[] {
    return [
      {
        id: 'stage-1',
        name: 'Foundation',
        order: 1,
        type: 'foundation',
        topics: this.generateTopics('foundation'),
        completionCriteria: ['Core concepts understood', 'Basic terminology mastered'],
        estimatedDuration: '2-4 weeks',
      },
      {
        id: 'stage-2',
        name: 'Core Skills',
        order: 2,
        type: 'core',
        topics: this.generateTopics('core'),
        completionCriteria: ['Key skills demonstrated', 'Practical exercises completed'],
        estimatedDuration: '4-8 weeks',
      },
      {
        id: 'stage-3',
        name: 'Application',
        order: 3,
        type: 'application',
        topics: this.generateTopics('application'),
        completionCriteria: ['Real-world application', 'Project completed'],
        estimatedDuration: '4-6 weeks',
      },
      {
        id: 'stage-4',
        name: 'Mastery',
        order: 4,
        type: 'mastery',
        topics: this.generateTopics('mastery'),
        completionCriteria: ['Advanced concepts mastered', 'Teaching ability'],
        estimatedDuration: 'Ongoing',
      },
    ];
  }

  private generateTopics(stageType: string): LearningTopic[] {
    const topicTemplates: Record<string, LearningTopic[]> = {
      foundation: [
        {
          id: 'topic-f1',
          name: 'Core Concepts',
          type: 'concept',
          priority: 'essential',
          resources: [{ type: 'reading', format: 'article', estimatedTime: '30 min' }],
          activities: ['Read fundamentals', 'Take notes', 'Review terminology'],
        },
        {
          id: 'topic-f2',
          name: 'Basic Principles',
          type: 'concept',
          priority: 'essential',
          resources: [{ type: 'video', format: 'tutorial', estimatedTime: '1 hour' }],
          activities: ['Watch introduction', 'Summarize key points'],
        },
      ],
      core: [
        {
          id: 'topic-c1',
          name: 'Key Skills',
          type: 'skill',
          priority: 'essential',
          resources: [{ type: 'practice', format: 'exercises', estimatedTime: '2 hours' }],
          activities: ['Practice exercises', 'Apply techniques'],
        },
        {
          id: 'topic-c2',
          name: 'Problem Solving',
          type: 'skill',
          priority: 'important',
          resources: [{ type: 'practice', format: 'challenges', estimatedTime: '3 hours' }],
          activities: ['Solve problems', 'Review solutions'],
        },
      ],
      application: [
        {
          id: 'topic-a1',
          name: 'Project Work',
          type: 'project',
          priority: 'essential',
          resources: [{ type: 'project', format: 'guided', estimatedTime: '10 hours' }],
          activities: ['Plan project', 'Execute', 'Review'],
        },
      ],
      mastery: [
        {
          id: 'topic-m1',
          name: 'Advanced Topics',
          type: 'concept',
          priority: 'important',
          resources: [{ type: 'reading', format: 'advanced', estimatedTime: '5 hours' }],
          activities: ['Deep study', 'Research', 'Synthesis'],
        },
      ],
    };

    return topicTemplates[stageType] || topicTemplates.foundation;
  }

  private identifyPrerequisites(input: string): string[] {
    return ['Basic understanding of domain', 'Time commitment', 'Learning resources access'];
  }

  private estimateDuration(input: string): string {
    return '3-6 months';
  }

  private defineOutcomes(input: string): string[] {
    return [
      'Core competency in subject area',
      'Practical application skills',
      'Foundation for advanced learning',
      'Portfolio of completed work',
    ];
  }

  private createMeta(source: string): LearningMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noRealContentDelivery: true, noRealAssessments: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'PathEngine', version: this.VERSION, parent: 'LearningEngine' };
  }
}

export default PathEngine;

============================================================
8.3-8.6 — LEARNING SUB-ENGINES (COMPACT)
============================================================

--- FILE: /che-nu-sdk/core/learning/progress.engine.ts

import type { LearningProgress, LearningMeta } from '../learning';

export class ProgressEngine {
  private readonly VERSION = '1.0.0';

  track(input: string): LearningProgress {
    return {
      id: `progress-${Date.now()}`,
      pathId: 'path-current',
      currentStage: 'stage-1',
      completedTopics: [],
      pendingTopics: ['topic-f1', 'topic-f2'],
      progressPercentage: 0,
      nextSteps: ['Begin with core concepts', 'Set learning schedule', 'Gather resources'],
      meta: this.createMeta(input),
    };
  }

  private createMeta(source: string): LearningMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noRealContentDelivery: true, noRealAssessments: true },
    };
  }

  meta() { return { name: 'ProgressEngine', version: this.VERSION, parent: 'LearningEngine' }; }
}

--- FILE: /che-nu-sdk/core/learning/retention.engine.ts

import type { RetentionPlan, RetentionSchedule, LearningMeta } from '../learning';

export class RetentionEngine {
  private readonly VERSION = '1.0.0';

  plan(input: string): RetentionPlan {
    return {
      id: `retention-${Date.now()}`,
      strategy: this.selectStrategy(input),
      schedule: this.generateSchedule(input),
      techniques: [
        'Active recall through self-testing',
        'Spaced repetition intervals',
        'Interleaved practice',
        'Elaborative interrogation',
        'Concrete examples',
      ],
      meta: this.createMeta(input),
    };
  }

  private selectStrategy(input: string): RetentionPlan['strategy'] {
    if (input.includes('memorize') || input.includes('remember')) return 'spaced-repetition';
    if (input.includes('understand') || input.includes('deep')) return 'elaboration';
    return 'active-recall';
  }

  private generateSchedule(input: string): RetentionSchedule[] {
    return [
      { interval: 'Day 1', activity: 'Initial learning', focus: 'First exposure' },
      { interval: 'Day 2', activity: 'Review', focus: 'Recall practice' },
      { interval: 'Day 4', activity: 'Review', focus: 'Spaced practice' },
      { interval: 'Day 7', activity: 'Review + Application', focus: 'Consolidation' },
      { interval: 'Day 14', activity: 'Review', focus: 'Long-term retention' },
      { interval: 'Day 30', activity: 'Comprehensive review', focus: 'Mastery check' },
    ];
  }

  private createMeta(source: string): LearningMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noRealContentDelivery: true, noRealAssessments: true },
    };
  }

  meta() { return { name: 'RetentionEngine', version: this.VERSION, parent: 'LearningEngine' }; }
}

--- FILE: /che-nu-sdk/core/learning/assessment.engine.ts

import type { AssessmentStructure, AssessmentCriterion, LearningMeta } from '../learning';

export class AssessmentEngine {
  private readonly VERSION = '1.0.0';

  structure(input: string): AssessmentStructure {
    return {
      id: `assess-${Date.now()}`,
      type: this.determineType(input),
      criteria: this.generateCriteria(input),
      format: this.selectFormat(input),
      meta: this.createMeta(input),
    };
  }

  private determineType(input: string): AssessmentStructure['type'] {
    if (input.includes('self')) return 'self-assessment';
    if (input.includes('project')) return 'project-review';
    if (input.includes('skill')) return 'skill-evaluation';
    return 'knowledge-check';
  }

  private generateCriteria(input: string): AssessmentCriterion[] {
    return [
      { id: 'crit-1', name: 'Core Knowledge', description: 'Understanding of fundamental concepts', level: 'basic' },
      { id: 'crit-2', name: 'Application', description: 'Ability to apply knowledge', level: 'proficient' },
      { id: 'crit-3', name: 'Problem Solving', description: 'Solving novel problems', level: 'proficient' },
      { id: 'crit-4', name: 'Synthesis', description: 'Combining concepts creatively', level: 'advanced' },
    ];
  }

  private selectFormat(input: string): string {
    return 'Self-reflection with guiding questions';
  }

  private createMeta(source: string): LearningMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true, noRealContentDelivery: true, noRealAssessments: true },
    };
  }

  meta() { return { name: 'AssessmentEngine', version: this.VERSION, parent: 'LearningEngine' }; }
}

--- FILE: /che-nu-sdk/core/learning/resource.engine.ts

import type { ResourceReference } from '../learning';

export class LearningResourceEngine {
  private readonly VERSION = '1.0.0';

  suggest(input: string): ResourceReference[] {
    return [
      { type: 'reading', format: 'Books & Articles', estimatedTime: 'Variable' },
      { type: 'video', format: 'Video Tutorials', estimatedTime: '1-2 hours each' },
      { type: 'practice', format: 'Exercises & Drills', estimatedTime: '30 min - 2 hours' },
      { type: 'project', format: 'Hands-on Projects', estimatedTime: '5-20 hours' },
      { type: 'discussion', format: 'Community & Forums', estimatedTime: 'Ongoing' },
    ];
  }

  meta() { return { name: 'LearningResourceEngine', version: this.VERSION, parent: 'LearningEngine' }; }
}

============================================================
8.7 — LEARNING INDEX
============================================================

--- FILE: /che-nu-sdk/core/learning/index.ts

export { PathEngine } from './path.engine';
export { ProgressEngine } from './progress.engine';
export { RetentionEngine } from './retention.engine';
export { AssessmentEngine } from './assessment.engine';
export { LearningResourceEngine } from './resource.engine';

============================================================
8.8 — LEARNING SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/learning.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.io/schemas/learning.schema.json",
  "title": "CHE·NU Learning Schema",
  "description": "OPERATIONAL MODULE - NOT A SPHERE. Representational learning structures.",
  "type": "object",
  "properties": {
    "path": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "domain": { "type": "string" },
        "level": { "type": "string", "enum": ["beginner", "intermediate", "advanced", "expert"] },
        "stages": { "type": "array" },
        "prerequisites": { "type": "array" },
        "estimatedDuration": { "type": "string" },
        "outcomes": { "type": "array" }
      }
    },
    "progress": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "pathId": { "type": "string" },
        "currentStage": { "type": "string" },
        "progressPercentage": { "type": "number" },
        "nextSteps": { "type": "array" }
      }
    },
    "retention": { "type": "object" },
    "assessment": { "type": "object" },
    "meta": { "type": "object" }
  }
}
