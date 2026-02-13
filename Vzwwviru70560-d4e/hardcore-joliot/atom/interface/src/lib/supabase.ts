/**
 * SUPABASE CLIENT - AT·OM Database Connection
 * ============================================
 *
 * Configuration centralisée du client Supabase pour:
 * - Authentification
 * - Base de données (21 tables)
 * - Realtime subscriptions
 * - Storage
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

// =============================================================================
// CONFIGURATION
// =============================================================================

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('[Supabase] Missing configuration - running in offline mode');
}

// =============================================================================
// CLIENT INITIALIZATION
// =============================================================================

export const supabase: SupabaseClient = createClient(
  supabaseUrl || 'https://placeholder.supabase.co',
  supabaseAnonKey || 'placeholder-key',
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true,
      storage: localStorage,
    },
    realtime: {
      params: {
        eventsPerSecond: 10,
      },
    },
    global: {
      headers: {
        'x-atom-client': 'web-interface',
        'x-atom-version': '1.0.0',
      },
    },
  }
);

// =============================================================================
// CONNECTION STATUS
// =============================================================================

export function isSupabaseConfigured(): boolean {
  return Boolean(supabaseUrl && supabaseAnonKey);
}

export async function checkSupabaseConnection(): Promise<{
  connected: boolean;
  latency: number;
  error?: string;
}> {
  if (!isSupabaseConfigured()) {
    return { connected: false, latency: 0, error: 'Not configured' };
  }

  const start = performance.now();
  try {
    const { error } = await supabase.from('system_logs').select('count').limit(1);
    const latency = Math.round(performance.now() - start);

    if (error) {
      return { connected: false, latency, error: error.message };
    }

    return { connected: true, latency };
  } catch (err) {
    return {
      connected: false,
      latency: Math.round(performance.now() - start),
      error: err instanceof Error ? err.message : 'Unknown error',
    };
  }
}

// =============================================================================
// DATABASE TYPES (based on existing tables)
// =============================================================================

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          created_at: string;
          updated_at: string;
          email: string;
          display_name: string | null;
          avatar_url: string | null;
          role: 'citoyen' | 'collaborateur' | 'investisseur' | 'admin';
          onboarding_status: 'not_started' | 'in_progress' | 'completed';
          preferences: Record<string, unknown>;
        };
        Insert: Omit<Database['public']['Tables']['profiles']['Row'], 'id' | 'created_at' | 'updated_at'>;
        Update: Partial<Database['public']['Tables']['profiles']['Insert']>;
      };
      workspaces: {
        Row: {
          id: string;
          created_at: string;
          name: string;
          description: string | null;
          owner_id: string;
          settings: Record<string, unknown>;
        };
        Insert: Omit<Database['public']['Tables']['workspaces']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['workspaces']['Insert']>;
      };
      workspace_members: {
        Row: {
          id: string;
          workspace_id: string;
          user_id: string;
          role: 'owner' | 'admin' | 'member' | 'viewer';
          joined_at: string;
        };
        Insert: Omit<Database['public']['Tables']['workspace_members']['Row'], 'id' | 'joined_at'>;
        Update: Partial<Database['public']['Tables']['workspace_members']['Insert']>;
      };
      community_messages: {
        Row: {
          id: string;
          created_at: string;
          author_id: string;
          content: string;
          channel: string;
          metadata: Record<string, unknown>;
        };
        Insert: Omit<Database['public']['Tables']['community_messages']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['community_messages']['Insert']>;
      };
      local_needs: {
        Row: {
          id: string;
          created_at: string;
          title: string;
          description: string;
          category: string;
          status: 'open' | 'in_progress' | 'resolved';
          author_id: string;
          location: string | null;
          priority: number;
        };
        Insert: Omit<Database['public']['Tables']['local_needs']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['local_needs']['Insert']>;
      };
      need_votes: {
        Row: {
          id: string;
          need_id: string;
          user_id: string;
          vote_type: 'up' | 'down';
          created_at: string;
        };
        Insert: Omit<Database['public']['Tables']['need_votes']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['need_votes']['Insert']>;
      };
      system_logs: {
        Row: {
          id: string;
          created_at: string;
          level: 'info' | 'warn' | 'error' | 'debug';
          message: string;
          source: string;
          metadata: Record<string, unknown>;
        };
        Insert: Omit<Database['public']['Tables']['system_logs']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['system_logs']['Insert']>;
      };
      // Add more tables as needed
    };
  };
}

// =============================================================================
// TYPED HELPERS
// =============================================================================

export const db = {
  profiles: () => supabase.from('profiles'),
  workspaces: () => supabase.from('workspaces'),
  workspaceMembers: () => supabase.from('workspace_members'),
  communityMessages: () => supabase.from('community_messages'),
  localNeeds: () => supabase.from('local_needs'),
  needVotes: () => supabase.from('need_votes'),
  systemLogs: () => supabase.from('system_logs'),
  perceptions: () => supabase.from('perceptions'),
  privateThreads: () => supabase.from('private_threads'),
  threadMessages: () => supabase.from('thread_messages'),
  territoryProjects: () => supabase.from('territory_projects'),
  atomMapping: () => supabase.from('atom_mapping'),
  accreditations: () => supabase.from('accreditations'),
  annales: () => supabase.from('annales'),
  armors: () => supabase.from('armors'),
  arsenalTransmutation: () => supabase.from('arsenal_transmutation'),
  balanceInvestigations: () => supabase.from('balance_investigations'),
  gratitudeLetter: () => supabase.from('gratitude_letter'),
  pinataAssets: () => supabase.from('pinata_assets'),
  resourceTransmutation: () => supabase.from('resource_transmutation'),
  succesHumanite: () => supabase.from('succes_humanite'),
};

// =============================================================================
// AUTH HELPERS
// =============================================================================

export const auth = {
  signUp: async (email: string, password: string, metadata?: Record<string, unknown>) => {
    return supabase.auth.signUp({
      email,
      password,
      options: { data: metadata },
    });
  },

  signIn: async (email: string, password: string) => {
    return supabase.auth.signInWithPassword({ email, password });
  },

  signOut: async () => {
    return supabase.auth.signOut();
  },

  getUser: async () => {
    return supabase.auth.getUser();
  },

  getSession: async () => {
    return supabase.auth.getSession();
  },

  onAuthStateChange: (callback: (event: string, session: unknown) => void) => {
    return supabase.auth.onAuthStateChange(callback);
  },
};

// =============================================================================
// REALTIME HELPERS
// =============================================================================

export const realtime = {
  subscribeToTable: (
    table: string,
    callback: (payload: unknown) => void,
    filter?: string
  ) => {
    const channel = supabase
      .channel(`public:${table}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table,
          filter,
        },
        callback
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  },

  subscribeToChannel: (channelName: string) => {
    return supabase.channel(channelName);
  },
};

// =============================================================================
// EXPORT
// =============================================================================

export default supabase;
