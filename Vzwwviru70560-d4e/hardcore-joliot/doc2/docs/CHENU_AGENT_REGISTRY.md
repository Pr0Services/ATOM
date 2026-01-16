============================================================
SECTION 2 — AGENT CAPABILITY REGISTRY
============================================================

--- FILE: /che-nu-sdk/core/agent_registry.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Agent Registry
 * ============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Hold a representational list of AgentProfiles.
 * Provide simple functions to query and filter.
 * 
 * ⚠️ THIS IS NOT A PERSISTENT DATABASE!
 * This is an in-memory representational registry.
 * 
 * @module AgentRegistry
 * @version 1.0.0
 */

import type { 
  AgentProfile, 
  AgentCapability, 
  DomainSphere, 
  AgentRole,
  CapabilityLevel 
} from './agent_profile';

// ============================================================
// REGISTRY TYPES
// ============================================================

export interface RegistryStats {
  totalAgents: number;
  byRole: Record<string, number>;
  bySphere: Record<string, number>;
  byEngine: Record<string, number>;
  totalCapabilities: number;
}

export interface SearchCriteria {
  role?: AgentRole;
  sphere?: DomainSphere;
  engine?: string;
  minCapabilityLevel?: CapabilityLevel;
  tags?: string[];
  nameContains?: string;
}

export interface RegistryMeta {
  source: string;
  generated: string;
  version: string;
  agentCount: number;
  safe: {
    isRepresentational: boolean;
    noAutonomy: boolean;
    inMemoryOnly: boolean;
  };
}

// ============================================================
// AGENT REGISTRY CLASS
// ============================================================

export class AgentRegistry {
  private readonly VERSION = '1.0.0';
  private agents: Map<string, AgentProfile> = new Map();

  // ============================================================
  // REGISTRATION METHODS
  // ============================================================

  /**
   * Register an agent profile in the registry
   * REPRESENTATIONAL - in-memory only
   */
  registerAgent(profile: AgentProfile): void {
    this.agents.set(profile.id, profile);
  }

  /**
   * Register multiple agents at once
   */
  registerAgents(profiles: AgentProfile[]): void {
    profiles.forEach(p => this.registerAgent(p));
  }

  /**
   * Unregister an agent by ID
   */
  unregisterAgent(agentId: string): boolean {
    return this.agents.delete(agentId);
  }

  /**
   * Update an existing agent profile
   */
  updateAgent(profile: AgentProfile): boolean {
    if (this.agents.has(profile.id)) {
      this.agents.set(profile.id, profile);
      return true;
    }
    return false;
  }

  /**
   * Clear all agents from registry
   */
  clearRegistry(): void {
    this.agents.clear();
  }

  // ============================================================
  // QUERY METHODS
  // ============================================================

  /**
   * List all registered agents
   */
  listAgents(): AgentProfile[] {
    return Array.from(this.agents.values());
  }

  /**
   * Get agent by ID
   */
  getAgent(agentId: string): AgentProfile | null {
    return this.agents.get(agentId) || null;
  }

  /**
   * Get agent by name (first match)
   */
  getAgentByName(name: string): AgentProfile | null {
    return this.listAgents().find(a => a.name === name) || null;
  }

  /**
   * Find agents by role
   */
  findByRole(role: AgentRole): AgentProfile[] {
    return this.listAgents().filter(a => a.role === role);
  }

  /**
   * Find agents by domain sphere
   */
  findBySphere(sphere: DomainSphere): AgentProfile[] {
    return this.listAgents().filter(a => a.domainSpheres.includes(sphere));
  }

  /**
   * Find agents that have capability for a specific engine
   */
  findByEngine(engineName: string): AgentProfile[] {
    return this.listAgents().filter(a => 
      a.capabilities.some(c => c.engine === engineName)
    );
  }

  /**
   * Find agents by multiple criteria
   */
  search(criteria: SearchCriteria): AgentProfile[] {
    let results = this.listAgents();

    if (criteria.role) {
      results = results.filter(a => a.role === criteria.role);
    }

    if (criteria.sphere) {
      results = results.filter(a => a.domainSpheres.includes(criteria.sphere));
    }

    if (criteria.engine) {
      results = results.filter(a => 
        a.capabilities.some(c => c.engine === criteria.engine)
      );
    }

    if (criteria.minCapabilityLevel) {
      const levelOrder: CapabilityLevel[] = ['novice', 'low', 'medium', 'high', 'expert'];
      const minIndex = levelOrder.indexOf(criteria.minCapabilityLevel);
      results = results.filter(a =>
        a.capabilities.some(c => levelOrder.indexOf(c.level) >= minIndex)
      );
    }

    if (criteria.tags?.length) {
      results = results.filter(a =>
        criteria.tags!.some(tag => a.tags.includes(tag))
      );
    }

    if (criteria.nameContains) {
      const search = criteria.nameContains.toLowerCase();
      results = results.filter(a => 
        a.name.toLowerCase().includes(search)
      );
    }

    return results;
  }

  /**
   * Find agents that collaborate with a specific agent
   */
  findCollaborators(agentId: string): AgentProfile[] {
    const agent = this.getAgent(agentId);
    if (!agent) return [];

    return this.listAgents().filter(a => 
      a.id !== agentId && 
      (agent.collaboratesWith.includes(a.name) || a.collaboratesWith.includes(agent.name))
    );
  }

  /**
   * Find agents with complementary capabilities
   */
  findComplementary(agentId: string): AgentProfile[] {
    const agent = this.getAgent(agentId);
    if (!agent) return [];

    const agentEngines = new Set(agent.capabilities.map(c => c.engine));
    
    return this.listAgents()
      .filter(a => a.id !== agentId)
      .filter(a => {
        // Has engines the original agent doesn't have
        const hasNew = a.capabilities.some(c => !agentEngines.has(c.engine));
        // Shares at least one sphere
        const sharesSphere = a.domainSpheres.some(s => agent.domainSpheres.includes(s));
        return hasNew && sharesSphere;
      });
  }

  // ============================================================
  // STATISTICS METHODS
  // ============================================================

  /**
   * Get registry statistics
   */
  getStats(): RegistryStats {
    const agents = this.listAgents();
    
    const byRole: Record<string, number> = {};
    const bySphere: Record<string, number> = {};
    const byEngine: Record<string, number> = {};
    let totalCapabilities = 0;

    agents.forEach(agent => {
      // Count by role
      byRole[agent.role] = (byRole[agent.role] || 0) + 1;

      // Count by sphere
      agent.domainSpheres.forEach(sphere => {
        bySphere[sphere] = (bySphere[sphere] || 0) + 1;
      });

      // Count by engine
      agent.capabilities.forEach(cap => {
        byEngine[cap.engine] = (byEngine[cap.engine] || 0) + 1;
        totalCapabilities++;
      });
    });

    return {
      totalAgents: agents.length,
      byRole,
      bySphere,
      byEngine,
      totalCapabilities,
    };
  }

  /**
   * Get engine coverage - which engines are used by how many agents
   */
  getEngineCoverage(): Array<{
    engine: string;
    agentCount: number;
    agents: string[];
    averageLevel: string;
  }> {
    const engineMap: Map<string, { agents: string[]; levels: CapabilityLevel[] }> = new Map();

    this.listAgents().forEach(agent => {
      agent.capabilities.forEach(cap => {
        if (!engineMap.has(cap.engine)) {
          engineMap.set(cap.engine, { agents: [], levels: [] });
        }
        const entry = engineMap.get(cap.engine)!;
        entry.agents.push(agent.name);
        entry.levels.push(cap.level);
      });
    });

    const levelOrder: CapabilityLevel[] = ['novice', 'low', 'medium', 'high', 'expert'];
    
    return Array.from(engineMap.entries()).map(([engine, data]) => {
      const avgIndex = Math.round(
        data.levels.reduce((sum, l) => sum + levelOrder.indexOf(l), 0) / data.levels.length
      );
      return {
        engine,
        agentCount: data.agents.length,
        agents: data.agents,
        averageLevel: levelOrder[avgIndex],
      };
    }).sort((a, b) => b.agentCount - a.agentCount);
  }

  /**
   * Get sphere coverage
   */
  getSphereCoverage(): Array<{
    sphere: DomainSphere;
    agentCount: number;
    agents: string[];
  }> {
    const sphereMap: Map<DomainSphere, string[]> = new Map();

    this.listAgents().forEach(agent => {
      agent.domainSpheres.forEach(sphere => {
        if (!sphereMap.has(sphere)) {
          sphereMap.set(sphere, []);
        }
        sphereMap.get(sphere)!.push(agent.name);
      });
    });

    return Array.from(sphereMap.entries())
      .map(([sphere, agents]) => ({
        sphere,
        agentCount: agents.length,
        agents,
      }))
      .sort((a, b) => b.agentCount - a.agentCount);
  }

  // ============================================================
  // EXPORT / IMPORT
  // ============================================================

  /**
   * Export registry to JSON
   */
  exportRegistry(): string {
    return JSON.stringify({
      agents: this.listAgents(),
      meta: this.getMeta(),
    }, null, 2);
  }

  /**
   * Import registry from JSON
   */
  importRegistry(json: string): void {
    const data = JSON.parse(json);
    if (data.agents && Array.isArray(data.agents)) {
      this.registerAgents(data.agents);
    }
  }

  // ============================================================
  // METADATA
  // ============================================================

  getMeta(): RegistryMeta {
    return {
      source: 'AgentRegistry',
      generated: new Date().toISOString(),
      version: this.VERSION,
      agentCount: this.agents.size,
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        inMemoryOnly: true,
      },
    };
  }

  meta(): Record<string, unknown> {
    return {
      name: 'AgentRegistry',
      version: this.VERSION,
      description: 'In-memory registry for agent profiles',
      classification: {
        type: 'agent_capability_layer',
        isNotASphere: true,
        isNotAutonomous: true,
        isNotPersistent: true,
      },
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        inMemoryOnly: true,
        noDatabase: true,
      },
      methods: [
        'registerAgent',
        'listAgents',
        'findByRole',
        'findByEngine',
        'findBySphere',
        'search',
        'getStats',
      ],
    };
  }
}

// ============================================================
// SINGLETON INSTANCE (Optional)
// ============================================================

let registryInstance: AgentRegistry | null = null;

export function getAgentRegistry(): AgentRegistry {
  if (!registryInstance) {
    registryInstance = new AgentRegistry();
  }
  return registryInstance;
}

export function createAgentRegistry(): AgentRegistry {
  return new AgentRegistry();
}

export default AgentRegistry;
