############################################################
#                                                          #
#       CHE·NU AGENT CAPABILITY & PROFILE SYSTEM           #
#       CONNECT ENGINES TO AGENT PROFILES                  #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 1 — AGENT PROFILE CORE MODULE
============================================================

--- FILE: /che-nu-sdk/core/agent_profile.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Agent Profile Engine
 * ==================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Define standard structure for agent profiles.
 * Describe which engines are attached to which agent.
 * Describe focus, strengths, and limitations.
 * 
 * ⚠️ THIS IS NOT AN AUTONOMOUS AGENT!
 * This is a REPRESENTATIONAL data structure only.
 * 
 * @module AgentProfileEngine
 * @version 1.0.0
 */

// ============================================================
// CORE TYPES
// ============================================================

export type CapabilityLevel = 'novice' | 'low' | 'medium' | 'high' | 'expert';

export type DomainSphere = 
  | 'Personal'
  | 'Business'
  | 'Creative'
  | 'Scholar'
  | 'Social'
  | 'Community'
  | 'XR'
  | 'MyTeam'
  | 'Gouvernement'
  | 'Immobilier'
  | 'Associations'
  | 'Projets';

export type AgentRole =
  | 'researcher'
  | 'architect'
  | 'coach'
  | 'analyst'
  | 'coordinator'
  | 'specialist'
  | 'generalist'
  | 'mentor'
  | 'curator'
  | 'creator'
  | 'planner'
  | 'reviewer'
  | 'facilitator';

export interface AgentCapability {
  /** Engine name (e.g., "HealthEngine", "FinanceEngine") */
  engine: string;
  /** Capability level for this engine */
  level: CapabilityLevel;
  /** Specific focus areas within the engine */
  focus: string[];
  /** Which sub-engines are primarily used */
  subEngines?: string[];
  /** Additional notes about this capability */
  notes?: string;
}

export interface AgentProfile {
  /** Unique identifier */
  id: string;
  /** Display name */
  name: string;
  /** Functional role */
  role: AgentRole;
  /** Description of the agent's purpose */
  description: string;
  /** Domain spheres this agent operates in */
  domainSpheres: DomainSphere[];
  /** List of attached capabilities */
  capabilities: AgentCapability[];
  /** Primary engines for quick access */
  preferredEngines: string[];
  /** Secondary/support engines */
  supportEngines: string[];
  /** Known limitations */
  limitations: string[];
  /** Typical use cases */
  useCases: string[];
  /** Collaboration hints with other agents */
  collaboratesWith: string[];
  /** Tags for filtering */
  tags: string[];
  /** Metadata */
  meta: AgentProfileMeta;
}

export interface AgentProfileMeta {
  source: string;
  generated: string;
  version: string;
  moduleType: 'agent_profile';
  classification: 'representational_only';
  safe: {
    isRepresentational: boolean;
    noAutonomy: boolean;
    noExecution: boolean;
    noPersistence: boolean;
  };
}

export interface ProfileSummary {
  summary: string;
  engines: string[];
  primarySphere: DomainSphere;
  capabilityCount: number;
  strengths: string[];
}

export interface ProfileInput {
  name: string;
  role: AgentRole;
  description?: string;
  domainSpheres: DomainSphere[];
  tags?: string[];
}

// ============================================================
// AGENT PROFILE ENGINE CLASS
// ============================================================

export class AgentProfileEngine {
  private readonly VERSION = '1.0.0';

  // ============================================================
  // PROFILE CREATION METHODS
  // ============================================================

  /**
   * Create a new agent profile from input
   * REPRESENTATIONAL ONLY - no execution
   */
  createProfile(input: ProfileInput): AgentProfile {
    const id = `agent-${input.name.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`;
    
    return {
      id,
      name: input.name,
      role: input.role,
      description: input.description || `${input.name} - ${input.role} agent`,
      domainSpheres: input.domainSpheres,
      capabilities: [],
      preferredEngines: [],
      supportEngines: [],
      limitations: [],
      useCases: [],
      collaboratesWith: [],
      tags: input.tags || [],
      meta: this.createMeta(input.name),
    };
  }

  /**
   * Attach an engine capability to a profile
   * Returns NEW profile (immutable pattern)
   */
  attachEngine(
    profile: AgentProfile,
    engineName: string,
    level: CapabilityLevel,
    focus: string[],
    options?: {
      subEngines?: string[];
      notes?: string;
      isPrimary?: boolean;
    }
  ): AgentProfile {
    const capability: AgentCapability = {
      engine: engineName,
      level,
      focus,
      subEngines: options?.subEngines,
      notes: options?.notes,
    };

    const newCapabilities = [...profile.capabilities, capability];
    
    const newPreferred = options?.isPrimary !== false
      ? [...new Set([...profile.preferredEngines, engineName])]
      : profile.preferredEngines;

    const newSupport = options?.isPrimary === false
      ? [...new Set([...profile.supportEngines, engineName])]
      : profile.supportEngines;

    return {
      ...profile,
      capabilities: newCapabilities,
      preferredEngines: newPreferred,
      supportEngines: newSupport,
      meta: {
        ...profile.meta,
        generated: new Date().toISOString(),
      },
    };
  }

  /**
   * Attach multiple engines at once
   */
  attachEngines(
    profile: AgentProfile,
    engines: Array<{
      name: string;
      level: CapabilityLevel;
      focus: string[];
      subEngines?: string[];
      isPrimary?: boolean;
    }>
  ): AgentProfile {
    let result = profile;
    for (const engine of engines) {
      result = this.attachEngine(
        result,
        engine.name,
        engine.level,
        engine.focus,
        {
          subEngines: engine.subEngines,
          isPrimary: engine.isPrimary,
        }
      );
    }
    return result;
  }

  /**
   * Set limitations for a profile
   */
  setLimitations(profile: AgentProfile, limitations: string[]): AgentProfile {
    return {
      ...profile,
      limitations,
      meta: { ...profile.meta, generated: new Date().toISOString() },
    };
  }

  /**
   * Set use cases for a profile
   */
  setUseCases(profile: AgentProfile, useCases: string[]): AgentProfile {
    return {
      ...profile,
      useCases,
      meta: { ...profile.meta, generated: new Date().toISOString() },
    };
  }

  /**
   * Set collaboration hints
   */
  setCollaborations(profile: AgentProfile, collaboratesWith: string[]): AgentProfile {
    return {
      ...profile,
      collaboratesWith,
      meta: { ...profile.meta, generated: new Date().toISOString() },
    };
  }

  // ============================================================
  // QUERY METHODS
  // ============================================================

  /**
   * List all capabilities for a profile
   */
  listCapabilities(profile: AgentProfile): AgentCapability[] {
    return profile.capabilities;
  }

  /**
   * Get capability for specific engine
   */
  getCapability(profile: AgentProfile, engineName: string): AgentCapability | null {
    return profile.capabilities.find(c => c.engine === engineName) || null;
  }

  /**
   * Check if profile has capability for engine
   */
  hasCapability(profile: AgentProfile, engineName: string): boolean {
    return profile.capabilities.some(c => c.engine === engineName);
  }

  /**
   * Get capabilities at or above a certain level
   */
  getCapabilitiesAtLevel(profile: AgentProfile, minLevel: CapabilityLevel): AgentCapability[] {
    const levelOrder: CapabilityLevel[] = ['novice', 'low', 'medium', 'high', 'expert'];
    const minIndex = levelOrder.indexOf(minLevel);
    return profile.capabilities.filter(c => levelOrder.indexOf(c.level) >= minIndex);
  }

  /**
   * Generate a summary description of the profile
   */
  describeProfile(profile: AgentProfile): ProfileSummary {
    const highCapabilities = this.getCapabilitiesAtLevel(profile, 'high');
    const strengths = highCapabilities.map(c => c.engine);

    return {
      summary: `${profile.name} is a ${profile.role} agent specializing in ${profile.domainSpheres.join(', ')}. ` +
               `Primary engines: ${profile.preferredEngines.join(', ')}. ` +
               `${profile.capabilities.length} total capabilities.`,
      engines: [...profile.preferredEngines, ...profile.supportEngines],
      primarySphere: profile.domainSpheres[0],
      capabilityCount: profile.capabilities.length,
      strengths,
    };
  }

  /**
   * Get engine usage statistics for a profile
   */
  getEngineStats(profile: AgentProfile): Record<string, {
    level: CapabilityLevel;
    focusCount: number;
    subEngineCount: number;
  }> {
    const stats: Record<string, any> = {};
    
    for (const cap of profile.capabilities) {
      stats[cap.engine] = {
        level: cap.level,
        focusCount: cap.focus.length,
        subEngineCount: cap.subEngines?.length || 0,
      };
    }

    return stats;
  }

  // ============================================================
  // VALIDATION METHODS
  // ============================================================

  /**
   * Validate a profile structure
   */
  validateProfile(profile: AgentProfile): {
    isValid: boolean;
    errors: string[];
    warnings: string[];
  } {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Required fields
    if (!profile.id) errors.push('Missing profile ID');
    if (!profile.name) errors.push('Missing profile name');
    if (!profile.role) errors.push('Missing profile role');
    if (!profile.domainSpheres.length) errors.push('At least one domain sphere required');

    // Recommendations
    if (!profile.capabilities.length) warnings.push('No capabilities attached');
    if (!profile.preferredEngines.length) warnings.push('No preferred engines specified');
    if (!profile.limitations.length) warnings.push('Consider adding limitations for clarity');
    if (!profile.useCases.length) warnings.push('Consider adding use cases');

    // Check SAFE compliance
    if (!profile.meta.safe.isRepresentational) errors.push('Profile must be representational');
    if (!profile.meta.safe.noAutonomy) errors.push('Profile must have no autonomy');

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  }

  // ============================================================
  // UTILITY METHODS
  // ============================================================

  /**
   * Clone a profile with new ID
   */
  cloneProfile(profile: AgentProfile, newName?: string): AgentProfile {
    const name = newName || `${profile.name} (Copy)`;
    return {
      ...profile,
      id: `agent-${name.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`,
      name,
      meta: this.createMeta(name),
    };
  }

  /**
   * Merge capabilities from another profile
   */
  mergeCapabilities(base: AgentProfile, source: AgentProfile): AgentProfile {
    const existingEngines = new Set(base.capabilities.map(c => c.engine));
    const newCapabilities = source.capabilities.filter(c => !existingEngines.has(c.engine));

    return {
      ...base,
      capabilities: [...base.capabilities, ...newCapabilities],
      preferredEngines: [...new Set([...base.preferredEngines, ...source.preferredEngines])],
      supportEngines: [...new Set([...base.supportEngines, ...source.supportEngines])],
      meta: { ...base.meta, generated: new Date().toISOString() },
    };
  }

  /**
   * Export profile to JSON
   */
  exportProfile(profile: AgentProfile): string {
    return JSON.stringify(profile, null, 2);
  }

  /**
   * Import profile from JSON
   */
  importProfile(json: string): AgentProfile {
    const parsed = JSON.parse(json);
    // Ensure SAFE compliance
    parsed.meta = this.createMeta(parsed.name);
    return parsed as AgentProfile;
  }

  // ============================================================
  // PRIVATE METHODS
  // ============================================================

  private createMeta(source: string): AgentProfileMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'agent_profile',
      classification: 'representational_only',
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        noExecution: true,
        noPersistence: true,
      },
    };
  }

  // ============================================================
  // MODULE METADATA
  // ============================================================

  meta(): Record<string, unknown> {
    return {
      name: 'AgentProfileEngine',
      version: this.VERSION,
      description: 'Representational agent profile and capability management',
      classification: {
        type: 'agent_capability_layer',
        isNotASphere: true,
        isNotAutonomous: true,
      },
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        noExecution: true,
        noPersistence: true,
        noNetworkCalls: true,
      },
      capabilities: [
        'createProfile',
        'attachEngine',
        'listCapabilities',
        'describeProfile',
        'validateProfile',
        'cloneProfile',
        'mergeCapabilities',
      ],
    };
  }
}

// ============================================================
// FACTORY & EXPORTS
// ============================================================

export function createAgentProfileEngine(): AgentProfileEngine {
  return new AgentProfileEngine();
}

export default AgentProfileEngine;
