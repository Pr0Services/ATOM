/* =====================================================
   CHE·NU — UNIFIED TYPES INDEX
   /types/index.ts
   
   CENTRAL TYPE DEFINITIONS
   All types should be imported from here.
   
   SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
   ===================================================== */

// ─────────────────────────────────────────────────────
// SPHERE TYPES (11 Official Spheres)
// ─────────────────────────────────────────────────────

/**
 * Official 11 Spheres of CHE·NU
 * 
 * Core 7 (User-facing spaces):
 * - maison: Personal home space
 * - entreprise: Business operations
 * - projets: Project management
 * - creative_studio: Creative expression
 * - gouvernement: Government/Admin
 * - immobilier: Real estate
 * - associations: Collaborative organizations
 * 
 * Extended 4 (Functional spaces):
 * - scholar: Learning and research
 * - finance: Financial management
 * - wellness: Health and wellbeing
 * - sandbox: Experimentation
 */
export const OFFICIAL_SPHERES = {
  // Core 7 Spaces (from User Memory)
  MAISON: 'maison',
  ENTREPRISE: 'entreprise',
  PROJETS: 'projets',
  CREATIVE_STUDIO: 'creative_studio',
  GOUVERNEMENT: 'gouvernement',
  IMMOBILIER: 'immobilier',
  ASSOCIATIONS: 'associations',
  
  // Extended 4 Spaces (Technical)
  SCHOLAR: 'scholar',
  FINANCE: 'finance',
  WELLNESS: 'wellness',
  SANDBOX: 'sandbox',
} as const;

export type SphereId = typeof OFFICIAL_SPHERES[keyof typeof OFFICIAL_SPHERES];

export const SPHERE_COUNT = 11;

/**
 * Sphere configuration
 */
export interface SphereConfig {
  id: SphereId;
  name: string;
  emoji: string;
  description: string;
  color: string;
  agentsEnabled: boolean;
  interSphereAllowed: boolean;
}

/**
 * All sphere configurations
 */
export const SPHERE_CONFIGS: Record<SphereId, SphereConfig> = {
  maison: {
    id: 'maison',
    name: 'Maison',
    emoji: '🏠',
    description: 'Espace personnel privé',
    color: '#D8B26A', // Sacred Gold
    agentsEnabled: true,
    interSphereAllowed: false,
  },
  entreprise: {
    id: 'entreprise',
    name: 'Entreprise',
    emoji: '💼',
    description: 'Opérations commerciales',
    color: '#3F7249', // Jungle Emerald
    agentsEnabled: true,
    interSphereAllowed: true,
  },
  projets: {
    id: 'projets',
    name: 'Projets',
    emoji: '📋',
    description: 'Gestion de projets',
    color: '#3EB4A2', // Cenote Turquoise
    agentsEnabled: true,
    interSphereAllowed: true,
  },
  creative_studio: {
    id: 'creative_studio',
    name: 'Creative Studio',
    emoji: '🎨',
    description: 'Expression créative',
    color: '#7A593A', // Earth Ember
    agentsEnabled: true,
    interSphereAllowed: false,
  },
  gouvernement: {
    id: 'gouvernement',
    name: 'Gouvernement',
    emoji: '🏛️',
    description: 'Administration et gouvernance',
    color: '#8D8371', // Ancient Stone
    agentsEnabled: true,
    interSphereAllowed: true,
  },
  immobilier: {
    id: 'immobilier',
    name: 'Immobilier',
    emoji: '🏗️',
    description: 'Gestion immobilière',
    color: '#2F4C39', // Shadow Moss
    agentsEnabled: true,
    interSphereAllowed: true,
  },
  associations: {
    id: 'associations',
    name: 'Associations',
    emoji: '🤝',
    description: 'Organisations collaboratives',
    color: '#E9E4D6', // Soft Sand
    agentsEnabled: true,
    interSphereAllowed: true,
  },
  scholar: {
    id: 'scholar',
    name: 'Scholar',
    emoji: '📚',
    description: 'Apprentissage et recherche',
    color: '#4A90D9', // Scholar Blue
    agentsEnabled: true,
    interSphereAllowed: false,
  },
  finance: {
    id: 'finance',
    name: 'Finance',
    emoji: '💰',
    description: 'Gestion financière',
    color: '#2E8B57', // Money Green
    agentsEnabled: true,
    interSphereAllowed: true,
  },
  wellness: {
    id: 'wellness',
    name: 'Wellness',
    emoji: '🌿',
    description: 'Santé et bien-être',
    color: '#98D8C8', // Wellness Mint
    agentsEnabled: true,
    interSphereAllowed: false,
  },
  sandbox: {
    id: 'sandbox',
    name: 'Sandbox',
    emoji: '🧪',
    description: 'Expérimentation sécurisée',
    color: '#FFB347', // Sandbox Orange
    agentsEnabled: true,
    interSphereAllowed: false,
  },
};

// ─────────────────────────────────────────────────────
// AGENT TYPES (Unified)
// ─────────────────────────────────────────────────────

/**
 * Agent hierarchy levels
 */
export type AgentLevel = 'L0' | 'L1' | 'L2' | 'L3' | 'L4' | 'L5';

/**
 * Agent role types
 */
export type AgentRole = 
  // L0 - Supreme
  | 'orchestrator'
  
  // L1 - Directors
  | 'strategic_director'
  | 'operations_director'
  | 'creative_director'
  | 'knowledge_director'
  
  // L2 - Managers
  | 'sphere_manager'
  | 'project_manager'
  | 'team_coordinator'
  
  // L3 - Analysts
  | 'decision_analyst'
  | 'context_analyzer'
  | 'preset_advisor'
  | 'data_analyst'
  | 'research_analyst'
  | 'market_analyst'
  | 'financial_analyst'
  | 'methodology_analyst'
  | 'memory_analyst'
  
  // L4 - Executors
  | 'task_executor'
  | 'content_creator'
  | 'document_generator'
  | 'code_executor'
  
  // L5 - Observers
  | 'audit_observer'
  | 'memory_keeper'
  | 'compliance_monitor'
  | 'performance_tracker';

/**
 * Agent status
 */
export type AgentStatus = 
  | 'idle'
  | 'thinking'
  | 'working'
  | 'waiting_approval'
  | 'paused'
  | 'error'
  | 'offline';

/**
 * Unified Agent interface
 * This is the SINGLE source of truth for Agent type.
 */
export interface Agent {
  // Identity
  id: string;
  name: string;
  displayName: string;
  description: string;
  
  // Classification
  level: AgentLevel;
  role: AgentRole;
  sphere: SphereId | 'trunk';  // trunk = cross-sphere
  
  // Capabilities
  capabilities: AgentCapability[];
  limitations: string[];
  
  // State
  status: AgentStatus;
  influenceLevel: number;  // 0-1, used for visual positioning
  
  // Visual
  avatar: AgentAvatar;
  
  // Governance
  permissions: AgentPermission[];
  requiresHumanApproval: boolean;
  auditLevel: 'minimal' | 'standard' | 'full';
}

/**
 * Agent capability
 */
export interface AgentCapability {
  id: string;
  name: string;
  description: string;
  category: CapabilityCategory;
  requiresApproval: boolean;
}

export type CapabilityCategory = 
  | 'analysis'
  | 'generation'
  | 'communication'
  | 'execution'
  | 'monitoring'
  | 'memory'
  | 'coordination';

/**
 * Agent permission
 */
export interface AgentPermission {
  resource: string;
  actions: PermissionAction[];
  scope: PermissionScope;
  expiresAt?: Date;
}

export type PermissionAction = 'read' | 'write' | 'execute' | 'delete' | 'share';

export interface PermissionScope {
  spheres?: SphereId[];
  projects?: string[];
  users?: string[];
  global?: boolean;
}

/**
 * Agent avatar
 */
export interface AgentAvatar {
  type: 'icon' | 'image' | 'generated' | '3d';
  icon?: string;
  imageUrl?: string;
  modelUrl?: string;
  color: string;
  accentColor?: string;
  animation?: AvatarAnimation;
}

export type AvatarAnimation = 'pulse' | 'orbit' | 'breathe' | 'glow' | 'none';

// ─────────────────────────────────────────────────────
// AGENT OUTPUT TYPES
// ─────────────────────────────────────────────────────

/**
 * Confidence level for agent outputs
 */
export type ConfidenceLevel = 'high' | 'medium' | 'low' | 'uncertain';

/**
 * Generic agent output
 */
export interface AgentOutput<T = unknown> {
  agentId: string;
  timestamp: number;
  confidence: ConfidenceLevel;
  explanation: string;
  data?: T;
  suggestions?: AgentSuggestion[];
  warnings?: string[];
}

/**
 * Agent suggestion
 */
export interface AgentSuggestion {
  id: string;
  text: string;
  context?: Record<string, unknown>;
  priority?: number;
}

// ─────────────────────────────────────────────────────
// ORCHESTRATOR TYPES
// ─────────────────────────────────────────────────────

/**
 * Orchestrator input
 */
export interface OrchestratorInput {
  userIntention: string;
  context?: Record<string, unknown>;
  targetAgents?: string[];
  currentSphere?: SphereId;
}

/**
 * Orchestrator output
 */
export interface OrchestratorOutput {
  synthesis: string;
  options: NeutralOption[];
  consultedAgents: string[];
  requiresValidation: boolean;
}

/**
 * Neutral option presented to user
 */
export interface NeutralOption {
  id: string;
  description: string;
  sourceAgent: string;
  context?: Record<string, unknown>;
}

// ─────────────────────────────────────────────────────
// SDK LAYER TYPES
// ─────────────────────────────────────────────────────

/**
 * Base model for all SDK layers
 */
export interface BaseModel {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  metadata?: Record<string, unknown>;
}

/**
 * SDK Layer identifiers
 */
export type SDKLayerId = 
  | 'project'
  | 'mission'
  | 'process'
  | 'knowledge'
  | 'xr'
  | 'simulation'
  | 'persona'
  | 'context'
  | 'template_factory'
  | 'tool';

export const SDK_LAYERS: SDKLayerId[] = [
  'project',
  'mission',
  'process',
  'knowledge',
  'xr',
  'simulation',
  'persona',
  'context',
  'template_factory',
  'tool',
];

export const SDK_LAYER_COUNT = 10;

// ─────────────────────────────────────────────────────
// BRAND COLORS
// ─────────────────────────────────────────────────────

export const BRAND_COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
} as const;

export type BrandColor = keyof typeof BRAND_COLORS;

// ─────────────────────────────────────────────────────
// SAFE COMPLIANCE
// ─────────────────────────────────────────────────────

export const SAFE_COMPLIANCE = {
  isRepresentational: true,
  noAutonomy: true,
  noExecution: true,
  noRealPlans: true,
  noAPI: true,
  noSystemCommands: true,
  noExternalIntegrations: true,
} as const;

// ─────────────────────────────────────────────────────
// UTILITY TYPES
// ─────────────────────────────────────────────────────

export type UUID = string;
export type Timestamp = number;
export type ISODateString = string;

/**
 * Make all properties optional recursively
 */
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

/**
 * Extract keys that are strings
 */
export type StringKeys<T> = Extract<keyof T, string>;

// ─────────────────────────────────────────────────────
// VERSION
// ─────────────────────────────────────────────────────

export const CHENU_VERSION = '2.0.0';
export const TYPES_VERSION = '1.0.0';
