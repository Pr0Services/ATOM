############################################################
#                                                          #
#       CHE·NU CONTEXT LAYER                               #
#       PATTERNS + SCHEMA + FRONTEND                       #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION A7 — CONTEXT PATTERN LIBRARY
============================================================

--- FILE: /che-nu-sdk/core/context/context_patterns.ts

/**
 * CHE·NU Context Pattern Library
 * ===============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Predefined context patterns/templates for common scenarios.
 * 
 * @version 1.0.0
 */

import { ContextModel, ContextInput } from '../context';

// ============================================================
// TYPES
// ============================================================

export type ContextPatternId = 
  | 'creative_studio'
  | 'research'
  | 'xr_production'
  | 'team_collaboration'
  | 'strategic_planning'
  | 'personal_reflection'
  | 'workshop'
  | 'review_session';

export interface ContextPattern {
  id: ContextPatternId;
  name: string;
  description: string;
  icon: string;
  category: string;
  template: Partial<ContextInput>;
}

// ============================================================
// CONTEXT PATTERNS
// ============================================================

export const CONTEXT_PATTERNS: Record<ContextPatternId, ContextPattern> = {
  creative_studio: {
    id: 'creative_studio',
    name: 'Creative Studio Context',
    description: 'Context for creative work and ideation',
    icon: '🎨',
    category: 'creative',
    template: {
      name: 'Creative Studio',
      description: 'A creative environment for ideation and design work',
      environment: {
        name: 'Creative Studio',
        category: 'workshop',
        description: 'Open, flexible creative space',
        attributes: {
          lighting: 'mixed',
          noise_level: 'moderate',
          accessibility: 'restricted',
          connectivity: 'hybrid',
        },
      },
      situation: {
        name: 'Creative Session',
        type: 'creative',
        description: 'Open-ended creative exploration',
        participants: [],
        objectives: ['Generate ideas', 'Explore possibilities', 'Create prototypes'],
      },
      scene: {
        name: 'Creative Workspace',
        description: 'An inspiring workspace for creative work',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Ideation Board', description: 'Central idea capture', priority: 10 },
          { name: 'Prototype Area', description: 'Hands-on creation space', priority: 8 },
        ],
        energy: 'dynamic',
        topology: 'clustered',
      },
      conditions: [
        { name: 'Creative Freedom', state: 'stable', description: 'Open to exploration', factors: [] },
      ],
      constraints: [
        { name: 'Time Box', type: 'time', severity: 'low', description: 'Soft time boundaries', impact_areas: ['schedule'] },
      ],
      engine_links: ['TemplateFactoryEngine', 'XREngine'],
      sphere_links: ['creative'],
    },
  },
  
  research: {
    id: 'research',
    name: 'Research Context',
    description: 'Context for research and discovery',
    icon: '🔬',
    category: 'analytical',
    template: {
      name: 'Research Context',
      description: 'An analytical environment for research and discovery',
      environment: {
        name: 'Research Lab',
        category: 'digital',
        description: 'Digital research environment',
        attributes: {
          lighting: 'artificial',
          noise_level: 'quiet',
          accessibility: 'restricted',
          connectivity: 'online',
        },
      },
      situation: {
        name: 'Research Session',
        type: 'exploratory',
        description: 'Systematic exploration and discovery',
        participants: [],
        objectives: ['Gather information', 'Analyze data', 'Document findings'],
      },
      scene: {
        name: 'Research Environment',
        description: 'Focused research workspace',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Knowledge Base', description: 'Central information repository', priority: 10 },
          { name: 'Analysis Tools', description: 'Data analysis interface', priority: 8 },
        ],
        energy: 'medium',
        topology: 'radial',
      },
      conditions: [
        { name: 'Data Availability', state: 'stable', description: 'Access to information', factors: [] },
      ],
      constraints: [
        { name: 'Accuracy Requirement', type: 'clarity', severity: 'high', description: 'High accuracy needed', impact_areas: ['quality'] },
      ],
      engine_links: ['KnowledgeEngine', 'SimulationEngine'],
      sphere_links: ['knowledge'],
    },
  },
  
  xr_production: {
    id: 'xr_production',
    name: 'XR Production Context',
    description: 'Context for XR scene creation',
    icon: '🥽',
    category: 'technical',
    template: {
      name: 'XR Production',
      description: 'A digital environment for XR content creation',
      environment: {
        name: 'XR Studio',
        category: 'digital',
        description: 'Immersive digital production space',
        attributes: {
          lighting: 'artificial',
          noise_level: 'silent',
          accessibility: 'restricted',
          connectivity: 'online',
        },
      },
      situation: {
        name: 'XR Build Session',
        type: 'creative',
        description: 'Building immersive experiences',
        participants: [],
        objectives: ['Design scene', 'Build assets', 'Test experience'],
      },
      scene: {
        name: 'XR Workstation',
        description: 'XR development environment',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Scene Editor', description: '3D scene manipulation', priority: 10 },
          { name: 'Preview Portal', description: 'Real-time preview', priority: 9 },
          { name: 'Asset Library', description: 'Available assets', priority: 7 },
        ],
        energy: 'high',
        topology: 'radial',
      },
      conditions: [
        { name: 'Technical Readiness', state: 'stable', description: 'Tools and systems ready', factors: [] },
      ],
      constraints: [
        { name: 'Performance Budget', type: 'technical', severity: 'medium', description: 'Performance constraints', impact_areas: ['design', 'optimization'] },
      ],
      engine_links: ['XREngine', 'TemplateFactoryEngine'],
      sphere_links: ['xr', 'creative'],
    },
  },
  
  team_collaboration: {
    id: 'team_collaboration',
    name: 'Team Collaboration Context',
    description: 'Context for team-based work',
    icon: '👥',
    category: 'collaborative',
    template: {
      name: 'Team Collaboration',
      description: 'A collaborative environment for team work',
      environment: {
        name: 'Collaboration Space',
        category: 'hybrid',
        description: 'Hybrid physical-digital collaboration space',
        attributes: {
          lighting: 'mixed',
          noise_level: 'moderate',
          accessibility: 'restricted',
          connectivity: 'hybrid',
        },
      },
      situation: {
        name: 'Team Session',
        type: 'collaborative',
        description: 'Collaborative team work session',
        participants: [],
        objectives: ['Align on goals', 'Coordinate work', 'Make decisions'],
      },
      scene: {
        name: 'Team Room',
        description: 'Collaborative team space',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Shared Board', description: 'Central collaboration surface', priority: 10 },
          { name: 'Task View', description: 'Work tracking', priority: 8 },
        ],
        energy: 'medium',
        topology: 'clustered',
      },
      conditions: [
        { name: 'Team Availability', state: 'dynamic', description: 'Team member participation', factors: [] },
      ],
      constraints: [
        { name: 'Schedule Alignment', type: 'time', severity: 'medium', description: 'Coordination needs', impact_areas: ['schedule', 'communication'] },
      ],
      engine_links: ['ProjectEngine', 'MissionEngine'],
      sphere_links: ['project', 'team'],
    },
  },
  
  strategic_planning: {
    id: 'strategic_planning',
    name: 'Strategic Planning Context',
    description: 'Context for strategic decision-making',
    icon: '♟️',
    category: 'strategic',
    template: {
      name: 'Strategic Planning',
      description: 'An environment for strategic planning and decision-making',
      environment: {
        name: 'Strategy Room',
        category: 'indoor',
        description: 'Formal planning environment',
        attributes: {
          lighting: 'artificial',
          noise_level: 'quiet',
          accessibility: 'restricted',
          connectivity: 'online',
        },
      },
      situation: {
        name: 'Strategy Session',
        type: 'analytical',
        description: 'Strategic analysis and planning',
        participants: [],
        objectives: ['Analyze situation', 'Evaluate options', 'Define strategy'],
      },
      scene: {
        name: 'Planning Environment',
        description: 'Strategic planning workspace',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Strategy Map', description: 'Visual strategy representation', priority: 10 },
          { name: 'Data Dashboard', description: 'Key metrics and data', priority: 9 },
        ],
        energy: 'medium',
        topology: 'hierarchical',
      },
      conditions: [
        { name: 'Information Quality', state: 'stable', description: 'Reliable data available', factors: [] },
      ],
      constraints: [
        { name: 'Decision Timeline', type: 'time', severity: 'high', description: 'Decision deadline', impact_areas: ['planning', 'execution'] },
      ],
      engine_links: ['SimulationEngine', 'KnowledgeEngine'],
      sphere_links: ['strategy', 'business'],
    },
  },
  
  personal_reflection: {
    id: 'personal_reflection',
    name: 'Personal Reflection Context',
    description: 'Context for individual reflection',
    icon: '🧘',
    category: 'personal',
    template: {
      name: 'Personal Reflection',
      description: 'A quiet environment for personal reflection',
      environment: {
        name: 'Reflection Space',
        category: 'abstract',
        description: 'Quiet, personal space',
        attributes: {
          lighting: 'natural',
          noise_level: 'silent',
          accessibility: 'private',
          connectivity: 'offline',
        },
      },
      situation: {
        name: 'Reflection Session',
        type: 'exploratory',
        description: 'Personal exploration and reflection',
        participants: [],
        objectives: ['Review experiences', 'Identify patterns', 'Set intentions'],
      },
      scene: {
        name: 'Personal Space',
        description: 'Individual reflection environment',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Journal', description: 'Personal documentation', priority: 10 },
          { name: 'Timeline', description: 'Personal history view', priority: 7 },
        ],
        energy: 'low',
        topology: 'linear',
      },
      conditions: [
        { name: 'Mental Clarity', state: 'neutral', description: 'Open mental state', factors: [] },
      ],
      constraints: [],
      engine_links: ['PersonaEngine'],
      sphere_links: ['personal'],
    },
  },
  
  workshop: {
    id: 'workshop',
    name: 'Workshop Context',
    description: 'Context for hands-on workshops',
    icon: '🛠️',
    category: 'workshop',
    template: {
      name: 'Workshop',
      description: 'A hands-on environment for workshops',
      environment: {
        name: 'Workshop Space',
        category: 'workshop',
        description: 'Practical workshop environment',
        attributes: {
          lighting: 'mixed',
          noise_level: 'moderate',
          accessibility: 'restricted',
          connectivity: 'hybrid',
        },
      },
      situation: {
        name: 'Workshop Session',
        type: 'collaborative',
        description: 'Hands-on collaborative workshop',
        participants: [],
        objectives: ['Learn skills', 'Practice techniques', 'Build outputs'],
      },
      scene: {
        name: 'Workshop Room',
        description: 'Practical workshop space',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Demo Area', description: 'Demonstration space', priority: 10 },
          { name: 'Work Stations', description: 'Individual work areas', priority: 8 },
          { name: 'Materials', description: 'Workshop materials', priority: 6 },
        ],
        energy: 'high',
        topology: 'clustered',
      },
      conditions: [
        { name: 'Material Availability', state: 'stable', description: 'Materials ready', factors: [] },
      ],
      constraints: [
        { name: 'Session Duration', type: 'time', severity: 'medium', description: 'Workshop time limit', impact_areas: ['schedule'] },
      ],
      engine_links: ['ProcessEngine', 'TemplateFactoryEngine'],
      sphere_links: ['learning', 'project'],
    },
  },
  
  review_session: {
    id: 'review_session',
    name: 'Review Session Context',
    description: 'Context for reviews and retrospectives',
    icon: '📋',
    category: 'review',
    template: {
      name: 'Review Session',
      description: 'An environment for reviews and retrospectives',
      environment: {
        name: 'Review Room',
        category: 'indoor',
        description: 'Formal review environment',
        attributes: {
          lighting: 'artificial',
          noise_level: 'quiet',
          accessibility: 'restricted',
          connectivity: 'online',
        },
      },
      situation: {
        name: 'Review Meeting',
        type: 'analytical',
        description: 'Systematic review and evaluation',
        participants: [],
        objectives: ['Review progress', 'Identify issues', 'Plan improvements'],
      },
      scene: {
        name: 'Review Environment',
        description: 'Review meeting space',
        actors: [],
        objects: [],
        focal_points: [
          { name: 'Progress Board', description: 'Progress visualization', priority: 10 },
          { name: 'Issue Tracker', description: 'Issue documentation', priority: 8 },
          { name: 'Action Items', description: 'Next steps', priority: 9 },
        ],
        energy: 'medium',
        topology: 'linear',
      },
      conditions: [
        { name: 'Data Completeness', state: 'stable', description: 'Review data ready', factors: [] },
      ],
      constraints: [
        { name: 'Meeting Time', type: 'time', severity: 'medium', description: 'Meeting duration', impact_areas: ['schedule'] },
      ],
      engine_links: ['ProjectEngine', 'SimulationEngine'],
      sphere_links: ['project', 'process'],
    },
  },
};

// ============================================================
// PATTERN ENGINE
// ============================================================

export const ContextPatternLibrary = {
  name: 'ContextPatternLibrary',
  version: '1.0.0',
  
  /**
   * List all available patterns
   */
  listPatterns(): ContextPattern[] {
    return Object.values(CONTEXT_PATTERNS);
  },
  
  /**
   * Get pattern by ID
   */
  getPattern(id: ContextPatternId): ContextPattern | null {
    return CONTEXT_PATTERNS[id] || null;
  },
  
  /**
   * Get pattern IDs by category
   */
  getPatternsByCategory(category: string): ContextPattern[] {
    return Object.values(CONTEXT_PATTERNS).filter(p => p.category === category);
  },
  
  /**
   * Get all categories
   */
  listCategories(): string[] {
    return [...new Set(Object.values(CONTEXT_PATTERNS).map(p => p.category))];
  },
  
  /**
   * Apply pattern (get template for context creation)
   */
  applyPattern(id: ContextPatternId): Partial<ContextInput> | null {
    const pattern = CONTEXT_PATTERNS[id];
    return pattern?.template || null;
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      pattern_count: Object.keys(CONTEXT_PATTERNS).length,
      categories: this.listCategories(),
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default ContextPatternLibrary;

============================================================
SECTION A8 — CONTEXT SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/context.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/context.schema.json",
  "title": "CHE·NU Context Schema",
  "description": "JSON Schema for CHE·NU representational contexts",
  "type": "object",
  "required": ["id", "name", "safe"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique context identifier",
      "pattern": "^ctx_[a-z0-9]+_[a-z0-9]+$"
    },
    "name": {
      "type": "string",
      "description": "Context name"
    },
    "description": {
      "type": "string",
      "description": "Context description"
    },
    "environment": {
      "$ref": "#/definitions/environment",
      "description": "Environment model"
    },
    "situation": {
      "$ref": "#/definitions/situation",
      "description": "Situation model"
    },
    "scene": {
      "$ref": "#/definitions/scene",
      "description": "Scene model"
    },
    "conditions": {
      "type": "array",
      "description": "Condition models",
      "items": {
        "$ref": "#/definitions/condition"
      }
    },
    "constraints": {
      "type": "array",
      "description": "Constraint models",
      "items": {
        "$ref": "#/definitions/constraint"
      }
    },
    "sphere_links": {
      "type": "array",
      "description": "Linked spheres",
      "items": { "type": "string" }
    },
    "engine_links": {
      "type": "array",
      "description": "Linked engines",
      "items": { "type": "string" }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_at": { "type": "string", "format": "date-time" },
        "updated_at": { "type": "string", "format": "date-time" },
        "template_source": { "type": "string" },
        "version": { "type": "string" }
      }
    },
    "safe": {
      "$ref": "#/definitions/safe_compliance"
    }
  },
  "definitions": {
    "environment": {
      "type": "object",
      "required": ["id", "name", "category"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "category": {
          "type": "string",
          "enum": ["indoor", "outdoor", "digital", "abstract", "workshop", "hybrid"]
        },
        "description": { "type": "string" },
        "attributes": {
          "type": "object",
          "properties": {
            "lighting": { "enum": ["natural", "artificial", "mixed", "none"] },
            "noise_level": { "enum": ["silent", "quiet", "moderate", "loud"] },
            "accessibility": { "enum": ["open", "restricted", "private"] },
            "connectivity": { "enum": ["online", "offline", "hybrid"] }
          }
        },
        "metadata": { "type": "object" }
      }
    },
    "situation": {
      "type": "object",
      "required": ["id", "name", "type"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["collaborative", "exploratory", "analytical", "creative", "operational", "strategic", "learning", "review"]
        },
        "description": { "type": "string" },
        "participants": {
          "type": "array",
          "items": { "type": "string" }
        },
        "objectives": {
          "type": "array",
          "items": { "type": "string" }
        },
        "metadata": { "type": "object" }
      }
    },
    "scene": {
      "type": "object",
      "required": ["id", "name"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "actors": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "role": { "enum": ["protagonist", "supporting", "observer", "facilitator"] },
              "description": { "type": "string" },
              "position": { "type": "string" }
            }
          }
        },
        "objects": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "type": { "type": "string" },
              "significance": { "enum": ["primary", "secondary", "background"] },
              "description": { "type": "string" }
            }
          }
        },
        "focal_points": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "description": { "type": "string" },
              "priority": { "type": "number", "minimum": 1, "maximum": 10 }
            }
          }
        },
        "energy": { "enum": ["low", "medium", "high", "dynamic"] },
        "topology": { "enum": ["linear", "radial", "clustered", "distributed", "hierarchical"] },
        "metadata": { "type": "object" }
      }
    },
    "condition": {
      "type": "object",
      "required": ["id", "name", "state"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "state": { "enum": ["stable", "unstable", "dynamic", "neutral", "transitional"] },
        "description": { "type": "string" },
        "factors": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "value": { "type": "string" },
              "impact": { "enum": ["positive", "negative", "neutral"] },
              "weight": { "type": "number", "minimum": 0, "maximum": 1 }
            }
          }
        },
        "metadata": { "type": "object" }
      }
    },
    "constraint": {
      "type": "object",
      "required": ["id", "name", "type", "severity"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "type": { "enum": ["time", "resources", "complexity", "clarity", "scope", "dependency", "technical", "organizational"] },
        "severity": { "enum": ["low", "medium", "high", "critical"] },
        "description": { "type": "string" },
        "impact_areas": {
          "type": "array",
          "items": { "type": "string" }
        },
        "metadata": { "type": "object" }
      }
    },
    "safe_compliance": {
      "type": "object",
      "required": ["isRepresentational", "noAutonomy", "noExecution"],
      "properties": {
        "isRepresentational": { "type": "boolean", "const": true },
        "noAutonomy": { "type": "boolean", "const": true },
        "noExecution": { "type": "boolean", "const": true }
      }
    }
  },
  "additionalProperties": false
}

============================================================
SECTION A9 — FRONTEND: CONTEXT PAGE
============================================================

--- FILE: /che-nu-frontend/pages/context.tsx

/**
 * CHE·NU Frontend — Context Builder Page
 * =======================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Create and manage representational contexts.
 * 
 * @version 1.0.0
 */

import React, { useState, useMemo } from 'react';
import { ContextViewer } from '../components/ContextViewer';

// ============================================================
// CONSTANTS
// ============================================================

const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

const PATTERN_ICONS: Record<string, string> = {
  creative_studio: '🎨',
  research: '🔬',
  xr_production: '🥽',
  team_collaboration: '👥',
  strategic_planning: '♟️',
  personal_reflection: '🧘',
  workshop: '🛠️',
  review_session: '📋',
};

const ENVIRONMENT_ICONS: Record<string, string> = {
  indoor: '🏠',
  outdoor: '🌳',
  digital: '💻',
  abstract: '🔮',
  workshop: '🛠️',
  hybrid: '🔄',
};

const SITUATION_ICONS: Record<string, string> = {
  collaborative: '👥',
  exploratory: '🧭',
  analytical: '📊',
  creative: '🎨',
  operational: '⚙️',
  strategic: '♟️',
  learning: '📚',
  review: '📋',
};

// ============================================================
// TYPE DEFINITIONS
// ============================================================

interface ContextPattern {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
}

interface ContextModel {
  id: string;
  name: string;
  description: string;
  environment: any;
  situation: any;
  scene: any;
  conditions: any[];
  constraints: any[];
  sphere_links: string[];
  engine_links: string[];
}

// ============================================================
// SAMPLE DATA
// ============================================================

const PATTERNS: ContextPattern[] = [
  { id: 'creative_studio', name: 'Creative Studio', description: 'Context for creative work', icon: '🎨', category: 'creative' },
  { id: 'research', name: 'Research', description: 'Context for research and discovery', icon: '🔬', category: 'analytical' },
  { id: 'xr_production', name: 'XR Production', description: 'Context for XR creation', icon: '🥽', category: 'technical' },
  { id: 'team_collaboration', name: 'Team Collaboration', description: 'Context for teamwork', icon: '👥', category: 'collaborative' },
  { id: 'strategic_planning', name: 'Strategic Planning', description: 'Context for strategy', icon: '♟️', category: 'strategic' },
  { id: 'personal_reflection', name: 'Personal Reflection', description: 'Context for reflection', icon: '🧘', category: 'personal' },
  { id: 'workshop', name: 'Workshop', description: 'Context for workshops', icon: '🛠️', category: 'workshop' },
  { id: 'review_session', name: 'Review Session', description: 'Context for reviews', icon: '📋', category: 'review' },
];

const SAMPLE_CONTEXT: ContextModel = {
  id: 'ctx_abc123_def456',
  name: 'Project Planning Session',
  description: 'A collaborative context for project planning',
  environment: {
    id: 'env_001',
    name: 'Virtual Meeting Room',
    category: 'digital',
    description: 'Digital collaboration space',
    attributes: { lighting: 'artificial', noise_level: 'quiet', accessibility: 'restricted', connectivity: 'online' },
  },
  situation: {
    id: 'sit_001',
    name: 'Planning Meeting',
    type: 'collaborative',
    description: 'Team planning session',
    participants: ['Team Lead', 'Designer', 'Developer'],
    objectives: ['Define scope', 'Assign tasks', 'Set timeline'],
  },
  scene: {
    id: 'scn_001',
    name: 'Planning Room',
    description: 'Virtual planning space',
    actors: [
      { id: 'actor_1', name: 'Facilitator', role: 'protagonist', description: 'Leads the session' },
    ],
    objects: [
      { id: 'obj_1', name: 'Whiteboard', type: 'tool', significance: 'primary', description: 'Collaboration surface' },
    ],
    focal_points: [
      { id: 'fp_1', name: 'Roadmap', description: 'Project roadmap visualization', priority: 10 },
    ],
    energy: 'medium',
    topology: 'clustered',
  },
  conditions: [
    { id: 'cond_1', name: 'Team Availability', state: 'stable', description: 'Team members present', factors: [] },
  ],
  constraints: [
    { id: 'const_1', name: 'Meeting Duration', type: 'time', severity: 'medium', description: '1 hour limit', impact_areas: ['schedule'] },
  ],
  sphere_links: ['project', 'team'],
  engine_links: ['ProjectEngine', 'MissionEngine'],
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export function ContextPage() {
  const [contexts, setContexts] = useState<ContextModel[]>([SAMPLE_CONTEXT]);
  const [selectedContext, setSelectedContext] = useState<ContextModel | null>(SAMPLE_CONTEXT);
  const [viewMode, setViewMode] = useState<'overview' | 'detail' | 'builder'>('detail');
  const [showPatterns, setShowPatterns] = useState(false);
  
  // Create from pattern
  const handleCreateFromPattern = (patternId: string) => {
    const pattern = PATTERNS.find(p => p.id === patternId);
    if (!pattern) return;
    
    const newContext: ContextModel = {
      id: `ctx_${Date.now().toString(36)}_new`,
      name: `New ${pattern.name}`,
      description: pattern.description,
      environment: null,
      situation: null,
      scene: null,
      conditions: [],
      constraints: [],
      sphere_links: [],
      engine_links: [],
    };
    
    setContexts([...contexts, newContext]);
    setSelectedContext(newContext);
    setShowPatterns(false);
    setViewMode('builder');
  };
  
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      backgroundColor: COLORS.uiSlate,
      color: COLORS.softSand,
    }}>
      {/* Header */}
      <div style={{
        padding: '20px 24px',
        borderBottom: `1px solid ${COLORS.shadowMoss}`,
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ 
              margin: 0, 
              fontSize: '24px', 
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
            }}>
              <span>🌐</span>
              Context Builder
            </h1>
            <p style={{ margin: '8px 0 0', color: COLORS.ancientStone, fontSize: '14px' }}>
              Create representational contexts for CHE·NU workflows
            </p>
          </div>
          <button
            onClick={() => setShowPatterns(true)}
            style={{
              padding: '10px 20px',
              backgroundColor: COLORS.sacredGold,
              color: COLORS.uiSlate,
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            + New Context
          </button>
        </div>
        
        {/* View Mode Toggle */}
        <div style={{ 
          marginTop: '20px', 
          display: 'flex', 
          gap: '16px', 
          alignItems: 'center',
        }}>
          <div style={{ 
            display: 'flex', 
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '8px',
            overflow: 'hidden',
          }}>
            {(['overview', 'detail', 'builder'] as const).map(mode => (
              <button
                key={mode}
                onClick={() => setViewMode(mode)}
                style={{
                  padding: '10px 16px',
                  backgroundColor: viewMode === mode ? COLORS.sacredGold : 'transparent',
                  color: viewMode === mode ? COLORS.uiSlate : COLORS.softSand,
                  border: 'none',
                  cursor: 'pointer',
                  fontWeight: viewMode === mode ? 600 : 400,
                }}
              >
                {mode === 'overview' ? '📋' : mode === 'detail' ? '👁️' : '🔧'} {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </button>
            ))}
          </div>
          
          {/* Stats */}
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '16px', fontSize: '13px' }}>
            <span style={{ color: COLORS.cenoteTurquoise }}>{contexts.length} contexts</span>
            {selectedContext && (
              <>
                <span style={{ color: COLORS.jungleEmerald }}>{selectedContext.conditions.length} conditions</span>
                <span style={{ color: COLORS.earthEmber }}>{selectedContext.constraints.length} constraints</span>
              </>
            )}
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Sidebar */}
        <div style={{
          width: '280px',
          borderRight: `1px solid ${COLORS.shadowMoss}`,
          overflowY: 'auto',
          padding: '16px',
        }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '14px', color: COLORS.ancientStone }}>
            My Contexts
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {contexts.map(ctx => (
              <div
                key={ctx.id}
                onClick={() => setSelectedContext(ctx)}
                style={{
                  padding: '12px',
                  backgroundColor: selectedContext?.id === ctx.id 
                    ? `${COLORS.sacredGold}20` 
                    : COLORS.shadowMoss,
                  borderRadius: '8px',
                  cursor: 'pointer',
                  borderLeft: selectedContext?.id === ctx.id 
                    ? `3px solid ${COLORS.sacredGold}` 
                    : '3px solid transparent',
                }}
              >
                <div style={{ fontWeight: 600, fontSize: '14px', marginBottom: '4px' }}>
                  {ctx.name}
                </div>
                <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>
                  {ctx.environment?.category || 'No environment'} • {ctx.situation?.type || 'No situation'}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Main View */}
        <div style={{ flex: 1, overflow: 'hidden' }}>
          {viewMode === 'detail' && selectedContext && (
            <ContextViewer context={selectedContext} />
          )}
          {viewMode === 'overview' && (
            <ContextOverviewView contexts={contexts} onSelect={setSelectedContext} />
          )}
          {viewMode === 'builder' && selectedContext && (
            <ContextBuilderView context={selectedContext} />
          )}
          {!selectedContext && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: COLORS.ancientStone,
            }}>
              <div style={{ textAlign: 'center' }}>
                <span style={{ fontSize: '48px', display: 'block', marginBottom: '16px' }}>🌐</span>
                <p>Select a context or create a new one</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Pattern Modal */}
      {showPatterns && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <div style={{
            backgroundColor: COLORS.uiSlate,
            borderRadius: '16px',
            padding: '24px',
            width: '700px',
            maxHeight: '80vh',
            overflowY: 'auto',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, fontSize: '20px' }}>Choose a Context Pattern</h2>
              <button
                onClick={() => setShowPatterns(false)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: COLORS.ancientStone,
                  cursor: 'pointer',
                  fontSize: '20px',
                }}
              >
                ✕
              </button>
            </div>
            
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(2, 1fr)', 
              gap: '12px',
            }}>
              {PATTERNS.map(pattern => (
                <div
                  key={pattern.id}
                  onClick={() => handleCreateFromPattern(pattern.id)}
                  style={{
                    padding: '16px',
                    backgroundColor: COLORS.shadowMoss,
                    borderRadius: '12px',
                    cursor: 'pointer',
                    border: '2px solid transparent',
                    transition: 'border-color 0.2s',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = COLORS.sacredGold}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'transparent'}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                    <span style={{ fontSize: '32px' }}>{pattern.icon}</span>
                    <div>
                      <div style={{ fontWeight: 600 }}>{pattern.name}</div>
                      <div style={{ fontSize: '11px', color: COLORS.cenoteTurquoise }}>{pattern.category}</div>
                    </div>
                  </div>
                  <p style={{ margin: 0, fontSize: '13px', color: COLORS.ancientStone }}>
                    {pattern.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
      
      {/* SAFE Notice */}
      <div style={{
        padding: '12px 24px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        borderTop: `1px solid ${COLORS.jungleEmerald}30`,
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
      }}>
        <span>🔒</span>
        <span style={{ fontSize: '12px', color: COLORS.jungleEmerald }}>
          SAFE · NON-AUTONOMOUS · Contexts are representational structures only
        </span>
      </div>
    </div>
  );
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

function ContextOverviewView({ contexts, onSelect }: { contexts: ContextModel[], onSelect: (c: ContextModel) => void }) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
        {contexts.map(ctx => (
          <div
            key={ctx.id}
            onClick={() => onSelect(ctx)}
            style={{
              padding: '20px',
              backgroundColor: COLORS.shadowMoss,
              borderRadius: '12px',
              cursor: 'pointer',
            }}
          >
            <h3 style={{ margin: '0 0 8px', fontSize: '16px' }}>{ctx.name}</h3>
            <p style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>{ctx.description}</p>
            <div style={{ display: 'flex', gap: '12px', fontSize: '12px' }}>
              {ctx.environment && (
                <span style={{ color: COLORS.cenoteTurquoise }}>
                  {ENVIRONMENT_ICONS[ctx.environment.category]} {ctx.environment.category}
                </span>
              )}
              {ctx.situation && (
                <span style={{ color: COLORS.earthEmber }}>
                  {SITUATION_ICONS[ctx.situation.type]} {ctx.situation.type}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ContextBuilderView({ context }: { context: ContextModel }) {
  return (
    <div style={{ padding: '20px', overflowY: 'auto', height: '100%' }}>
      <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px', marginBottom: '20px' }}>
        <h2 style={{ margin: '0 0 8px', fontSize: '20px' }}>{context.name}</h2>
        <p style={{ margin: 0, color: COLORS.ancientStone }}>{context.description}</p>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
        {/* Environment */}
        <div style={{ padding: '20px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '16px' }}>🏠 Environment</h3>
          {context.environment ? (
            <div>
              <div style={{ fontWeight: 600 }}>{context.environment.name}</div>
              <div style={{ fontSize: '13px', color: COLORS.ancientStone }}>{context.environment.category}</div>
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No environment set</div>
          )}
        </div>
        
        {/* Situation */}
        <div style={{ padding: '20px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '16px' }}>👥 Situation</h3>
          {context.situation ? (
            <div>
              <div style={{ fontWeight: 600 }}>{context.situation.name}</div>
              <div style={{ fontSize: '13px', color: COLORS.ancientStone }}>{context.situation.type}</div>
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No situation set</div>
          )}
        </div>
        
        {/* Conditions */}
        <div style={{ padding: '20px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '16px' }}>📊 Conditions ({context.conditions.length})</h3>
          {context.conditions.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {context.conditions.map(c => (
                <div key={c.id} style={{ padding: '8px', backgroundColor: COLORS.uiSlate, borderRadius: '6px' }}>
                  <div style={{ fontWeight: 500 }}>{c.name}</div>
                  <div style={{ fontSize: '11px', color: COLORS.cenoteTurquoise }}>{c.state}</div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No conditions</div>
          )}
        </div>
        
        {/* Constraints */}
        <div style={{ padding: '20px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '16px' }}>⚠️ Constraints ({context.constraints.length})</h3>
          {context.constraints.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {context.constraints.map(c => (
                <div key={c.id} style={{ padding: '8px', backgroundColor: COLORS.uiSlate, borderRadius: '6px' }}>
                  <div style={{ fontWeight: 500 }}>{c.name}</div>
                  <div style={{ fontSize: '11px', color: COLORS.earthEmber }}>{c.type} • {c.severity}</div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No constraints</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ContextPage;

============================================================
SECTION A10 — FRONTEND: CONTEXT VIEWER COMPONENT
============================================================

--- FILE: /che-nu-frontend/components/ContextViewer.tsx

/**
 * CHE·NU Frontend — Context Viewer Component
 * ==========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays a complete context with all components.
 * 
 * @version 1.0.0
 */

import React from 'react';

const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

interface ContextViewerProps {
  context: any;
}

export function ContextViewer({ context }: ContextViewerProps) {
  return (
    <div style={{ padding: '24px', overflowY: 'auto', height: '100%', backgroundColor: '#16171a' }}>
      {/* Header */}
      <div style={{
        padding: '32px',
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '16px',
        marginBottom: '24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '80px',
            height: '80px',
            backgroundColor: COLORS.uiSlate,
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '36px',
          }}>
            🌐
          </div>
          <div style={{ flex: 1 }}>
            <h1 style={{ margin: '0 0 8px', fontSize: '28px', fontWeight: 700 }}>{context.name}</h1>
            <p style={{ margin: 0, color: COLORS.ancientStone }}>{context.description}</p>
          </div>
        </div>
      </div>
      
      {/* Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
        {/* Environment */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>🏠</span> Environment
          </h3>
          {context.environment ? (
            <div>
              <div style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>
                {context.environment.name}
              </div>
              <div style={{
                display: 'inline-block',
                padding: '4px 12px',
                backgroundColor: `${COLORS.cenoteTurquoise}20`,
                color: COLORS.cenoteTurquoise,
                borderRadius: '6px',
                fontSize: '12px',
                textTransform: 'capitalize',
                marginBottom: '12px',
              }}>
                {context.environment.category}
              </div>
              <p style={{ margin: 0, fontSize: '13px', color: COLORS.ancientStone }}>
                {context.environment.description}
              </p>
              {context.environment.attributes && (
                <div style={{ marginTop: '12px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {Object.entries(context.environment.attributes).map(([key, val]) => (
                    <span key={key} style={{
                      padding: '4px 8px',
                      backgroundColor: COLORS.uiSlate,
                      borderRadius: '4px',
                      fontSize: '11px',
                    }}>
                      {key}: {val as string}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No environment defined</div>
          )}
        </div>
        
        {/* Situation */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>👥</span> Situation
          </h3>
          {context.situation ? (
            <div>
              <div style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>
                {context.situation.name}
              </div>
              <div style={{
                display: 'inline-block',
                padding: '4px 12px',
                backgroundColor: `${COLORS.sacredGold}20`,
                color: COLORS.sacredGold,
                borderRadius: '6px',
                fontSize: '12px',
                textTransform: 'capitalize',
                marginBottom: '12px',
              }}>
                {context.situation.type}
              </div>
              <p style={{ margin: '0 0 12px', fontSize: '13px', color: COLORS.ancientStone }}>
                {context.situation.description}
              </p>
              {context.situation.objectives?.length > 0 && (
                <div>
                  <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '6px' }}>Objectives:</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {context.situation.objectives.map((obj: string, i: number) => (
                      <span key={i} style={{
                        padding: '4px 8px',
                        backgroundColor: COLORS.uiSlate,
                        borderRadius: '4px',
                        fontSize: '11px',
                      }}>
                        {obj}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No situation defined</div>
          )}
        </div>
        
        {/* Scene */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px', gridColumn: 'span 2' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>🎬</span> Scene
          </h3>
          {context.scene ? (
            <div>
              <div style={{ display: 'flex', gap: '24px', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontSize: '18px', fontWeight: 600 }}>{context.scene.name}</div>
                  <p style={{ margin: '4px 0 0', fontSize: '13px', color: COLORS.ancientStone }}>
                    {context.scene.description}
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '12px' }}>
                  <div style={{
                    padding: '8px 16px',
                    backgroundColor: COLORS.uiSlate,
                    borderRadius: '8px',
                    textAlign: 'center',
                  }}>
                    <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>Energy</div>
                    <div style={{ fontWeight: 600, color: COLORS.earthEmber, textTransform: 'capitalize' }}>
                      {context.scene.energy}
                    </div>
                  </div>
                  <div style={{
                    padding: '8px 16px',
                    backgroundColor: COLORS.uiSlate,
                    borderRadius: '8px',
                    textAlign: 'center',
                  }}>
                    <div style={{ fontSize: '11px', color: COLORS.ancientStone }}>Topology</div>
                    <div style={{ fontWeight: 600, color: COLORS.jungleEmerald, textTransform: 'capitalize' }}>
                      {context.scene.topology}
                    </div>
                  </div>
                </div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
                {/* Actors */}
                <div>
                  <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
                    Actors ({context.scene.actors?.length || 0})
                  </div>
                  {context.scene.actors?.map((a: any) => (
                    <div key={a.id} style={{
                      padding: '8px',
                      backgroundColor: COLORS.uiSlate,
                      borderRadius: '6px',
                      marginBottom: '6px',
                    }}>
                      <div style={{ fontWeight: 500, fontSize: '13px' }}>{a.name}</div>
                      <div style={{ fontSize: '11px', color: COLORS.cenoteTurquoise }}>{a.role}</div>
                    </div>
                  ))}
                </div>
                
                {/* Objects */}
                <div>
                  <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
                    Objects ({context.scene.objects?.length || 0})
                  </div>
                  {context.scene.objects?.map((o: any) => (
                    <div key={o.id} style={{
                      padding: '8px',
                      backgroundColor: COLORS.uiSlate,
                      borderRadius: '6px',
                      marginBottom: '6px',
                    }}>
                      <div style={{ fontWeight: 500, fontSize: '13px' }}>{o.name}</div>
                      <div style={{ fontSize: '11px', color: COLORS.sacredGold }}>{o.significance}</div>
                    </div>
                  ))}
                </div>
                
                {/* Focal Points */}
                <div>
                  <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>
                    Focal Points ({context.scene.focal_points?.length || 0})
                  </div>
                  {context.scene.focal_points?.map((fp: any) => (
                    <div key={fp.id} style={{
                      padding: '8px',
                      backgroundColor: COLORS.uiSlate,
                      borderRadius: '6px',
                      marginBottom: '6px',
                    }}>
                      <div style={{ fontWeight: 500, fontSize: '13px' }}>{fp.name}</div>
                      <div style={{ fontSize: '11px', color: COLORS.earthEmber }}>Priority: {fp.priority}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No scene defined</div>
          )}
        </div>
        
        {/* Conditions */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>📊</span> Conditions ({context.conditions?.length || 0})
          </h3>
          {context.conditions?.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {context.conditions.map((c: any) => (
                <div key={c.id} style={{
                  padding: '12px',
                  backgroundColor: COLORS.uiSlate,
                  borderRadius: '8px',
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600 }}>{c.name}</span>
                    <span style={{
                      padding: '2px 8px',
                      backgroundColor: `${COLORS.cenoteTurquoise}20`,
                      color: COLORS.cenoteTurquoise,
                      borderRadius: '4px',
                      fontSize: '11px',
                    }}>
                      {c.state}
                    </span>
                  </div>
                  <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>{c.description}</div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No conditions defined</div>
          )}
        </div>
        
        {/* Constraints */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>⚠️</span> Constraints ({context.constraints?.length || 0})
          </h3>
          {context.constraints?.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {context.constraints.map((c: any) => {
                const severityColors: Record<string, string> = {
                  low: COLORS.jungleEmerald,
                  medium: COLORS.sacredGold,
                  high: COLORS.earthEmber,
                  critical: '#E74C3C',
                };
                return (
                  <div key={c.id} style={{
                    padding: '12px',
                    backgroundColor: COLORS.uiSlate,
                    borderRadius: '8px',
                    borderLeft: `3px solid ${severityColors[c.severity] || COLORS.ancientStone}`,
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span style={{ fontWeight: 600 }}>{c.name}</span>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <span style={{
                          padding: '2px 8px',
                          backgroundColor: COLORS.shadowMoss,
                          borderRadius: '4px',
                          fontSize: '11px',
                        }}>
                          {c.type}
                        </span>
                        <span style={{
                          padding: '2px 8px',
                          backgroundColor: `${severityColors[c.severity]}20`,
                          color: severityColors[c.severity],
                          borderRadius: '4px',
                          fontSize: '11px',
                        }}>
                          {c.severity}
                        </span>
                      </div>
                    </div>
                    <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>{c.description}</div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div style={{ color: COLORS.ancientStone, fontStyle: 'italic' }}>No constraints defined</div>
          )}
        </div>
        
        {/* Engine Links */}
        <div style={{ padding: '24px', backgroundColor: COLORS.shadowMoss, borderRadius: '12px', gridColumn: 'span 2' }}>
          <h3 style={{ margin: '0 0 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>⚙️</span> Linked Engines & Spheres
          </h3>
          <div style={{ display: 'flex', gap: '32px' }}>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>Engines</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {context.engine_links?.map((e: string) => (
                  <span key={e} style={{
                    padding: '6px 12px',
                    backgroundColor: `${COLORS.sacredGold}20`,
                    color: COLORS.sacredGold,
                    borderRadius: '6px',
                    fontSize: '12px',
                  }}>
                    {e}
                  </span>
                ))}
                {(!context.engine_links || context.engine_links.length === 0) && (
                  <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '13px' }}>
                    No engines linked
                  </span>
                )}
              </div>
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '12px', color: COLORS.ancientStone, marginBottom: '8px' }}>Spheres</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {context.sphere_links?.map((s: string) => (
                  <span key={s} style={{
                    padding: '6px 12px',
                    backgroundColor: `${COLORS.jungleEmerald}20`,
                    color: COLORS.jungleEmerald,
                    borderRadius: '6px',
                    fontSize: '12px',
                  }}>
                    {s}
                  </span>
                ))}
                {(!context.sphere_links || context.sphere_links.length === 0) && (
                  <span style={{ color: COLORS.ancientStone, fontStyle: 'italic', fontSize: '13px' }}>
                    No spheres linked
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ContextViewer;

============================================================
END OF CONTEXT LAYER PATTERNS + SCHEMA + FRONTEND
============================================================
