// ═══════════════════════════════════════════════════════════════════════════
// AT·OM AGENTS SERVICE
// Fetches real agents from the NOVA-999 backend API
// ═══════════════════════════════════════════════════════════════════════════

import axios, { AxiosError } from 'axios';

// ─────────────────────────────────────────────────────────────────────────────
// TYPES
// ─────────────────────────────────────────────────────────────────────────────

export interface Agent {
  id: string;
  name: string;
  capabilities: string[];
  requires_human_gate: boolean;
  sphere: string;
  sphere_name: string;
  sphere_color: string;
  sphere_icon: string;
  status: 'active' | 'standby' | 'offline';
}

export interface SphereInfo {
  name: string;
  color: string;
  icon: string;
}

export interface SphereSummary {
  name: string;
  color: string;
  icon: string;
  agent_count: number;
  agents: { id: string; name: string }[];
}

export interface AgentListResponse {
  data: Agent[];
  pagination: {
    page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
    has_next: boolean;
    has_previous: boolean;
  };
  spheres: Record<string, SphereInfo>;
  meta: {
    agent_system: string;
    total_registered: number;
    spheres_count: number;
  };
}

export interface SpheresResponse {
  spheres: Record<string, SphereSummary>;
  total_agents: number;
  total_spheres: number;
}

export interface AgentStatsResponse {
  total_agents: number;
  spheres_count: number;
  sphere_distribution: Record<string, number>;
  human_gate_agents: number;
  autonomous_agents: number;
  status_distribution: {
    active: number;
    standby: number;
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// API CLIENT
// ─────────────────────────────────────────────────────────────────────────────

const API_BASE_URL = import.meta.env.VITE_ATOM_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[AgentsAPI] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    console.error(`[AgentsAPI] Error: ${error.message}`);
    if (error.response) {
      console.error(`[AgentsAPI] Status: ${error.response.status}`);
    }
    return Promise.reject(error);
  }
);

// ─────────────────────────────────────────────────────────────────────────────
// AGENTS SERVICE
// ─────────────────────────────────────────────────────────────────────────────

class AgentsService {
  private cachedAgents: Agent[] | null = null;
  private cacheTimestamp: number = 0;
  private readonly CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

  /**
   * Fetch all agents from the API
   * Uses caching to reduce API calls
   */
  async getAllAgents(forceRefresh = false): Promise<Agent[]> {
    // Check cache
    if (
      !forceRefresh &&
      this.cachedAgents &&
      Date.now() - this.cacheTimestamp < this.CACHE_TTL_MS
    ) {
      console.log('[AgentsAPI] Returning cached agents');
      return this.cachedAgents;
    }

    try {
      // Fetch all agents (page_size=500 to get all in one request)
      const response = await apiClient.get<AgentListResponse>('/agents', {
        params: { page: 1, page_size: 500 },
      });

      this.cachedAgents = response.data.data;
      this.cacheTimestamp = Date.now();

      console.log(`[AgentsAPI] Fetched ${this.cachedAgents.length} agents`);
      return this.cachedAgents;
    } catch (error) {
      console.error('[AgentsAPI] Failed to fetch agents:', error);
      // Return cached data if available, even if stale
      if (this.cachedAgents) {
        console.log('[AgentsAPI] Returning stale cached agents');
        return this.cachedAgents;
      }
      throw error;
    }
  }

  /**
   * Fetch agents filtered by sphere
   */
  async getAgentsBySphere(sphere: string): Promise<Agent[]> {
    try {
      const response = await apiClient.get<AgentListResponse>('/agents', {
        params: { sphere, page_size: 100 },
      });
      return response.data.data;
    } catch (error) {
      console.error(`[AgentsAPI] Failed to fetch agents for sphere ${sphere}:`, error);
      throw error;
    }
  }

  /**
   * Fetch a single agent by ID
   */
  async getAgent(agentId: string): Promise<Agent> {
    try {
      const response = await apiClient.get<Agent>(`/agents/${agentId}`);
      return response.data;
    } catch (error) {
      console.error(`[AgentsAPI] Failed to fetch agent ${agentId}:`, error);
      throw error;
    }
  }

  /**
   * Fetch sphere summaries with agent counts
   */
  async getSpheresSummary(): Promise<SpheresResponse> {
    try {
      const response = await apiClient.get<SpheresResponse>('/agents/spheres');
      return response.data;
    } catch (error) {
      console.error('[AgentsAPI] Failed to fetch spheres summary:', error);
      throw error;
    }
  }

  /**
   * Fetch agent statistics
   */
  async getStats(): Promise<AgentStatsResponse> {
    try {
      const response = await apiClient.get<AgentStatsResponse>('/agents/stats/overview');
      return response.data;
    } catch (error) {
      console.error('[AgentsAPI] Failed to fetch agent stats:', error);
      throw error;
    }
  }

  /**
   * Clear the agent cache
   */
  clearCache(): void {
    this.cachedAgents = null;
    this.cacheTimestamp = 0;
    console.log('[AgentsAPI] Cache cleared');
  }

  /**
   * Check if the API is reachable
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await apiClient.get('/health', { timeout: 5000 });
      return response.status === 200;
    } catch {
      return false;
    }
  }
}

// Export singleton instance
export const agentsService = new AgentsService();

// ─────────────────────────────────────────────────────────────────────────────
// REACT QUERY HOOKS (optional, for use with @tanstack/react-query)
// ─────────────────────────────────────────────────────────────────────────────

export const agentQueryKeys = {
  all: ['agents'] as const,
  list: () => [...agentQueryKeys.all, 'list'] as const,
  bySphere: (sphere: string) => [...agentQueryKeys.all, 'sphere', sphere] as const,
  detail: (id: string) => [...agentQueryKeys.all, 'detail', id] as const,
  spheres: () => [...agentQueryKeys.all, 'spheres'] as const,
  stats: () => [...agentQueryKeys.all, 'stats'] as const,
};

// ─────────────────────────────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────────────────────────────

export default agentsService;
