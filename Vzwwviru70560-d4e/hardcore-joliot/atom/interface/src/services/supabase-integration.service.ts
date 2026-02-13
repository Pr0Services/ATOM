/**
 * SUPABASE INTEGRATION SERVICE
 * ============================
 *
 * Service d'intégration qui connecte les fonctionnalités AT·OM
 * aux tables Supabase réelles:
 *
 * - Waitlist/Inscription
 * - Funnel tracking (analytics)
 * - Profils utilisateurs
 * - Messages communautaires
 * - Besoins locaux / gouvernance
 * - Logs système
 */

import { supabase, db, auth, isSupabaseConfigured, checkSupabaseConnection } from '@/lib/supabase';
import { funnelTracker } from './funnel-tracking.service';
import { errorMonitor } from './error-monitor.service';

// =============================================================================
// TYPES
// =============================================================================

export interface WaitlistEntry {
  email: string;
  name?: string;
  role: 'citoyen' | 'collaborateur' | 'investisseur';
  interests?: string[];
  referralSource?: string;
}

export interface UserProfile {
  id: string;
  email: string;
  displayName: string | null;
  avatarUrl: string | null;
  role: 'citoyen' | 'collaborateur' | 'investisseur' | 'admin';
  onboardingStatus: 'not_started' | 'in_progress' | 'completed';
  preferences: Record<string, unknown>;
  createdAt: string;
}

export interface AnalyticsEvent {
  eventType: string;
  eventData: Record<string, unknown>;
  sessionId: string;
  userId?: string;
  timestamp: string;
}

// =============================================================================
// WAITLIST SERVICE (replaces localStorage)
// =============================================================================

export const waitlistService = {
  /**
   * Add email to waitlist with profile data
   */
  async addToWaitlist(entry: WaitlistEntry): Promise<{ success: boolean; error?: string }> {
    if (!isSupabaseConfigured()) {
      // Fallback to localStorage
      const existing = JSON.parse(localStorage.getItem('atom_waitlist') || '[]');
      existing.push({ ...entry, createdAt: new Date().toISOString() });
      localStorage.setItem('atom_waitlist', JSON.stringify(existing));
      return { success: true };
    }

    try {
      // Check if email already exists
      const { data: existing } = await db.profiles()
        .select('email')
        .eq('email', entry.email)
        .single();

      if (existing) {
        return { success: false, error: 'Email déjà inscrit' };
      }

      // Insert into profiles with waitlist status
      const { error } = await db.profiles().insert({
        email: entry.email,
        display_name: entry.name || null,
        role: entry.role,
        onboarding_status: 'not_started',
        preferences: {
          interests: entry.interests || [],
          referralSource: entry.referralSource,
          waitlistDate: new Date().toISOString(),
        },
      });

      if (error) {
        console.error('[Waitlist] Insert error:', error);
        return { success: false, error: error.message };
      }

      // Track in funnel
      funnelTracker.track('signup_complete', {
        method: 'waitlist',
        role: entry.role,
      });

      return { success: true };
    } catch (err) {
      errorMonitor.captureError(err);
      return { success: false, error: 'Erreur de connexion' };
    }
  },

  /**
   * Check if email is already on waitlist
   */
  async checkEmail(email: string): Promise<boolean> {
    if (!isSupabaseConfigured()) {
      const existing = JSON.parse(localStorage.getItem('atom_waitlist') || '[]');
      return existing.some((e: { email: string }) => e.email === email);
    }

    const { data } = await db.profiles()
      .select('email')
      .eq('email', email)
      .single();

    return Boolean(data);
  },
};

// =============================================================================
// USER PROFILE SERVICE
// =============================================================================

export const profileService = {
  /**
   * Get current user profile
   */
  async getCurrentProfile(): Promise<UserProfile | null> {
    if (!isSupabaseConfigured()) return null;

    const { data: { user } } = await auth.getUser();
    if (!user) return null;

    const { data, error } = await db.profiles()
      .select('*')
      .eq('id', user.id)
      .single();

    if (error || !data) return null;

    return {
      id: data.id,
      email: data.email,
      displayName: data.display_name,
      avatarUrl: data.avatar_url,
      role: data.role,
      onboardingStatus: data.onboarding_status,
      preferences: data.preferences || {},
      createdAt: data.created_at,
    };
  },

  /**
   * Update user profile
   */
  async updateProfile(updates: Partial<UserProfile>): Promise<{ success: boolean; error?: string }> {
    if (!isSupabaseConfigured()) return { success: false, error: 'Not configured' };

    const { data: { user } } = await auth.getUser();
    if (!user) return { success: false, error: 'Not authenticated' };

    const { error } = await db.profiles()
      .update({
        display_name: updates.displayName,
        avatar_url: updates.avatarUrl,
        preferences: updates.preferences,
        onboarding_status: updates.onboardingStatus,
        updated_at: new Date().toISOString(),
      })
      .eq('id', user.id);

    if (error) return { success: false, error: error.message };
    return { success: true };
  },

  /**
   * Complete onboarding
   */
  async completeOnboarding(): Promise<void> {
    await this.updateProfile({ onboardingStatus: 'completed' });
    localStorage.setItem('atom_onboarding_complete', 'true');
  },
};

// =============================================================================
// ANALYTICS SERVICE (persists to Supabase)
// =============================================================================

export const analyticsService = {
  /**
   * Track event to system_logs table
   */
  async trackEvent(event: AnalyticsEvent): Promise<void> {
    if (!isSupabaseConfigured()) {
      // Store locally for later sync
      const pending = JSON.parse(localStorage.getItem('atom_pending_analytics') || '[]');
      pending.push(event);
      localStorage.setItem('atom_pending_analytics', JSON.stringify(pending.slice(-100)));
      return;
    }

    try {
      await db.systemLogs().insert({
        level: 'info',
        message: event.eventType,
        source: 'web-analytics',
        metadata: {
          ...event.eventData,
          sessionId: event.sessionId,
          userId: event.userId,
          timestamp: event.timestamp,
        },
      });
    } catch (err) {
      console.warn('[Analytics] Failed to track event:', err);
    }
  },

  /**
   * Sync pending local analytics
   */
  async syncPendingEvents(): Promise<number> {
    if (!isSupabaseConfigured()) return 0;

    const pending = JSON.parse(localStorage.getItem('atom_pending_analytics') || '[]');
    if (pending.length === 0) return 0;

    let synced = 0;
    for (const event of pending) {
      try {
        await this.trackEvent(event);
        synced++;
      } catch {
        break; // Stop on first failure
      }
    }

    // Remove synced events
    const remaining = pending.slice(synced);
    localStorage.setItem('atom_pending_analytics', JSON.stringify(remaining));

    return synced;
  },

  /**
   * Get funnel metrics
   */
  async getFunnelMetrics(days: number = 7): Promise<Record<string, number>> {
    if (!isSupabaseConfigured()) return {};

    const since = new Date();
    since.setDate(since.getDate() - days);

    const { data, error } = await db.systemLogs()
      .select('message, metadata')
      .eq('source', 'web-analytics')
      .gte('created_at', since.toISOString());

    if (error || !data) return {};

    // Aggregate by event type
    const counts: Record<string, number> = {};
    data.forEach((row) => {
      counts[row.message] = (counts[row.message] || 0) + 1;
    });

    return counts;
  },
};

// =============================================================================
// COMMUNITY SERVICE
// =============================================================================

export const communityService = {
  /**
   * Get recent messages
   */
  async getMessages(channel: string, limit: number = 50): Promise<unknown[]> {
    if (!isSupabaseConfigured()) return [];

    const { data } = await db.communityMessages()
      .select('*, profiles(display_name, avatar_url)')
      .eq('channel', channel)
      .order('created_at', { ascending: false })
      .limit(limit);

    return data || [];
  },

  /**
   * Send message
   */
  async sendMessage(channel: string, content: string): Promise<{ success: boolean }> {
    if (!isSupabaseConfigured()) return { success: false };

    const { data: { user } } = await auth.getUser();
    if (!user) return { success: false };

    const { error } = await db.communityMessages().insert({
      author_id: user.id,
      content,
      channel,
      metadata: {},
    });

    return { success: !error };
  },

  /**
   * Subscribe to new messages
   */
  subscribeToChannel(channel: string, onMessage: (msg: unknown) => void): () => void {
    if (!isSupabaseConfigured()) return () => {};

    const subscription = supabase
      .channel(`messages:${channel}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'community_messages',
          filter: `channel=eq.${channel}`,
        },
        (payload) => onMessage(payload.new)
      )
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  },
};

// =============================================================================
// GOVERNANCE SERVICE (local needs, votes)
// =============================================================================

export const governanceService = {
  /**
   * Get local needs
   */
  async getLocalNeeds(status?: string): Promise<unknown[]> {
    if (!isSupabaseConfigured()) return [];

    let query = db.localNeeds()
      .select('*, profiles(display_name), need_votes(vote_type)')
      .order('priority', { ascending: false });

    if (status) {
      query = query.eq('status', status);
    }

    const { data } = await query.limit(100);
    return data || [];
  },

  /**
   * Create new need
   */
  async createNeed(need: {
    title: string;
    description: string;
    category: string;
    location?: string;
  }): Promise<{ success: boolean; id?: string }> {
    if (!isSupabaseConfigured()) return { success: false };

    const { data: { user } } = await auth.getUser();
    if (!user) return { success: false };

    const { data, error } = await db.localNeeds()
      .insert({
        title: need.title,
        description: need.description,
        category: need.category,
        location: need.location || null,
        status: 'open',
        author_id: user.id,
        priority: 0,
      })
      .select('id')
      .single();

    if (error) return { success: false };
    return { success: true, id: data?.id };
  },

  /**
   * Vote on a need
   */
  async voteOnNeed(needId: string, voteType: 'up' | 'down'): Promise<{ success: boolean }> {
    if (!isSupabaseConfigured()) return { success: false };

    const { data: { user } } = await auth.getUser();
    if (!user) return { success: false };

    // Upsert vote
    const { error } = await db.needVotes().upsert(
      {
        need_id: needId,
        user_id: user.id,
        vote_type: voteType,
      },
      { onConflict: 'need_id,user_id' }
    );

    return { success: !error };
  },
};

// =============================================================================
// HEALTH CHECK
// =============================================================================

export const healthService = {
  /**
   * Check all services status
   */
  async checkHealth(): Promise<{
    supabase: { connected: boolean; latency: number };
    auth: { authenticated: boolean };
    realtime: { connected: boolean };
  }> {
    const supabaseStatus = await checkSupabaseConnection();
    const { data: { session } } = await supabase.auth.getSession();

    return {
      supabase: {
        connected: supabaseStatus.connected,
        latency: supabaseStatus.latency,
      },
      auth: {
        authenticated: Boolean(session),
      },
      realtime: {
        connected: supabase.realtime.isConnected(),
      },
    };
  },
};

// =============================================================================
// INITIALIZATION
// =============================================================================

export async function initializeSupabaseIntegration(): Promise<void> {
  if (!isSupabaseConfigured()) {
    console.warn('[Supabase] Not configured - running in offline mode');
    return;
  }

  console.log('[Supabase] Initializing integration...');

  // Check connection
  const status = await checkSupabaseConnection();
  if (status.connected) {
    console.log(`[Supabase] Connected (${status.latency}ms)`);
  } else {
    console.warn('[Supabase] Connection failed:', status.error);
  }

  // Sync pending analytics
  const synced = await analyticsService.syncPendingEvents();
  if (synced > 0) {
    console.log(`[Supabase] Synced ${synced} pending analytics events`);
  }
}

// =============================================================================
// EXPORTS
// =============================================================================

export default {
  waitlist: waitlistService,
  profile: profileService,
  analytics: analyticsService,
  community: communityService,
  governance: governanceService,
  health: healthService,
  initialize: initializeSupabaseIntegration,
};
