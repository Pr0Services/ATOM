/**
 * FUNNEL TRACKING SERVICE - Unified Analytics for User Journey
 * =============================================================
 *
 * Service centralisé pour tracker le parcours utilisateur:
 * - Pré-inscription (landing → signup)
 * - Onboarding (steps completion)
 * - Activation (first value moment)
 * - Rétention (return visits)
 *
 * Objectif audit: "Instrumenter chaque étape du funnel"
 */

// =============================================================================
// TYPES
// =============================================================================

export type FunnelStage =
  | 'landing_view'
  | 'landing_scroll'
  | 'landing_cta_click'
  | 'signup_start'
  | 'signup_step_1'
  | 'signup_step_2'
  | 'signup_complete'
  | 'onboarding_start'
  | 'onboarding_step'
  | 'onboarding_skip'
  | 'onboarding_complete'
  | 'platform_enter'
  | 'first_action'
  | 'first_success'
  | 'feature_use'
  | 'session_end';

export interface FunnelEvent {
  stage: FunnelStage;
  timestamp: number;
  sessionId: string;
  userId?: string;
  metadata?: Record<string, unknown>;
}

export interface FunnelMetrics {
  totalSessions: number;
  conversionRates: Record<string, number>;
  dropOffPoints: Array<{ stage: FunnelStage; rate: number }>;
  averageTimeToValue: number;
  completionRateOnboarding: number;
}

export interface SessionData {
  id: string;
  startTime: number;
  events: FunnelEvent[];
  userId?: string;
  userAgent: string;
  referrer: string;
  landingPage: string;
  isNewUser: boolean;
}

// =============================================================================
// FUNNEL TRACKING SERVICE
// =============================================================================

class FunnelTrackingService {
  private static instance: FunnelTrackingService;
  private currentSession: SessionData | null = null;
  private eventQueue: FunnelEvent[] = [];
  private flushInterval: ReturnType<typeof setInterval> | null = null;
  private config = {
    enabled: true,
    batchSize: 10,
    flushIntervalMs: 30000, // 30 seconds
    endpoint: '/api/analytics/funnel',
    debug: import.meta.env.DEV,
  };

  private constructor() {
    this.initSession();
    this.setupFlushInterval();
    this.setupVisibilityTracking();
  }

  static getInstance(): FunnelTrackingService {
    if (!FunnelTrackingService.instance) {
      FunnelTrackingService.instance = new FunnelTrackingService();
    }
    return FunnelTrackingService.instance;
  }

  // ---------------------------------------------------------------------------
  // SESSION MANAGEMENT
  // ---------------------------------------------------------------------------

  private initSession(): void {
    const sessionId = this.getOrCreateSessionId();
    const isNewUser = !localStorage.getItem('atom_returning_user');

    this.currentSession = {
      id: sessionId,
      startTime: Date.now(),
      events: [],
      userAgent: navigator.userAgent,
      referrer: document.referrer,
      landingPage: window.location.pathname,
      isNewUser,
    };

    // Mark as returning user for future visits
    localStorage.setItem('atom_returning_user', 'true');

    if (this.config.debug) {
      console.log('[Funnel] Session initialized:', this.currentSession.id);
    }
  }

  private getOrCreateSessionId(): string {
    const stored = sessionStorage.getItem('atom_session_id');
    if (stored) return stored;

    const newId = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
    sessionStorage.setItem('atom_session_id', newId);
    return newId;
  }

  setUserId(userId: string): void {
    if (this.currentSession) {
      this.currentSession.userId = userId;
    }
  }

  // ---------------------------------------------------------------------------
  // EVENT TRACKING
  // ---------------------------------------------------------------------------

  track(stage: FunnelStage, metadata?: Record<string, unknown>): void {
    if (!this.config.enabled || !this.currentSession) return;

    const event: FunnelEvent = {
      stage,
      timestamp: Date.now(),
      sessionId: this.currentSession.id,
      userId: this.currentSession.userId,
      metadata,
    };

    this.currentSession.events.push(event);
    this.eventQueue.push(event);

    if (this.config.debug) {
      console.log('[Funnel] Event tracked:', stage, metadata);
    }

    // Auto-flush if batch size reached
    if (this.eventQueue.length >= this.config.batchSize) {
      this.flush();
    }
  }

  // Convenience methods for common events
  trackLandingView(): void {
    this.track('landing_view', {
      referrer: document.referrer,
      utm_source: new URLSearchParams(window.location.search).get('utm_source'),
      utm_campaign: new URLSearchParams(window.location.search).get('utm_campaign'),
    });
  }

  trackLandingScroll(depth: number): void {
    this.track('landing_scroll', { scrollDepth: depth });
  }

  trackCTAClick(ctaId: string, ctaText: string): void {
    this.track('landing_cta_click', { ctaId, ctaText });
  }

  trackSignupStart(method: 'email' | 'social' | 'waitlist'): void {
    this.track('signup_start', { method });
  }

  trackSignupStep(step: number, data?: Record<string, unknown>): void {
    this.track(step === 1 ? 'signup_step_1' : 'signup_step_2', {
      step,
      ...data,
    });
  }

  trackSignupComplete(userType: string): void {
    this.track('signup_complete', {
      userType,
      timeToComplete: this.getTimeSinceSessionStart(),
    });
  }

  trackOnboardingStart(): void {
    this.track('onboarding_start');
  }

  trackOnboardingStep(step: number, stepName: string): void {
    this.track('onboarding_step', { step, stepName });
  }

  trackOnboardingSkip(atStep: number): void {
    this.track('onboarding_skip', {
      skippedAtStep: atStep,
      timeInOnboarding: this.getTimeSinceEvent('onboarding_start'),
    });
  }

  trackOnboardingComplete(): void {
    this.track('onboarding_complete', {
      totalTime: this.getTimeSinceEvent('onboarding_start'),
    });
  }

  trackPlatformEnter(): void {
    this.track('platform_enter', {
      timeSinceStart: this.getTimeSinceSessionStart(),
    });
  }

  trackFirstAction(actionType: string, actionTarget: string): void {
    this.track('first_action', {
      actionType,
      actionTarget,
      timeToFirstAction: this.getTimeSinceEvent('platform_enter'),
    });
  }

  trackFirstSuccess(successType: string, details?: Record<string, unknown>): void {
    this.track('first_success', {
      successType,
      timeToValue: this.getTimeSinceSessionStart(),
      ...details,
    });
  }

  trackFeatureUse(featureName: string, featureCategory: string): void {
    this.track('feature_use', { featureName, featureCategory });
  }

  // ---------------------------------------------------------------------------
  // TIME CALCULATIONS
  // ---------------------------------------------------------------------------

  private getTimeSinceSessionStart(): number {
    if (!this.currentSession) return 0;
    return Date.now() - this.currentSession.startTime;
  }

  private getTimeSinceEvent(stage: FunnelStage): number {
    if (!this.currentSession) return 0;
    const event = this.currentSession.events.find((e) => e.stage === stage);
    if (!event) return 0;
    return Date.now() - event.timestamp;
  }

  // ---------------------------------------------------------------------------
  // DATA PERSISTENCE & TRANSMISSION
  // ---------------------------------------------------------------------------

  private setupFlushInterval(): void {
    this.flushInterval = setInterval(() => {
      this.flush();
    }, this.config.flushIntervalMs);
  }

  private setupVisibilityTracking(): void {
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') {
        this.track('session_end', {
          totalDuration: this.getTimeSinceSessionStart(),
          totalEvents: this.currentSession?.events.length || 0,
        });
        this.flush();
      }
    });

    window.addEventListener('beforeunload', () => {
      this.flush();
    });
  }

  async flush(): Promise<void> {
    if (this.eventQueue.length === 0) return;

    const eventsToSend = [...this.eventQueue];
    this.eventQueue = [];

    // Store locally as backup
    this.persistToLocalStorage(eventsToSend);

    // Send to backend
    try {
      if (this.config.endpoint && !this.config.debug) {
        await fetch(this.config.endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session: this.currentSession,
            events: eventsToSend,
          }),
          keepalive: true,
        });
      }

      if (this.config.debug) {
        console.log('[Funnel] Events flushed:', eventsToSend.length);
      }
    } catch (error) {
      // Re-queue on failure
      this.eventQueue = [...eventsToSend, ...this.eventQueue];
      console.warn('[Funnel] Flush failed, events re-queued');
    }
  }

  private persistToLocalStorage(events: FunnelEvent[]): void {
    try {
      const key = `atom_funnel_${this.currentSession?.id}`;
      const existing = JSON.parse(localStorage.getItem(key) || '[]');
      const updated = [...existing, ...events].slice(-100); // Keep last 100 events
      localStorage.setItem(key, JSON.stringify(updated));
    } catch {
      // Storage full or unavailable
    }
  }

  // ---------------------------------------------------------------------------
  // ANALYTICS & REPORTING
  // ---------------------------------------------------------------------------

  getSessionEvents(): FunnelEvent[] {
    return this.currentSession?.events || [];
  }

  getConversionFunnel(): Array<{ stage: FunnelStage; count: number; rate: number }> {
    const events = this.getSessionEvents();
    const stages: FunnelStage[] = [
      'landing_view',
      'landing_cta_click',
      'signup_start',
      'signup_complete',
      'onboarding_start',
      'onboarding_complete',
      'platform_enter',
      'first_action',
      'first_success',
    ];

    const counts = stages.map((stage) => ({
      stage,
      count: events.filter((e) => e.stage === stage).length,
    }));

    const firstCount = counts[0]?.count || 1;
    return counts.map((item) => ({
      ...item,
      rate: Math.round((item.count / firstCount) * 100),
    }));
  }

  // ---------------------------------------------------------------------------
  // CLEANUP
  // ---------------------------------------------------------------------------

  destroy(): void {
    if (this.flushInterval) {
      clearInterval(this.flushInterval);
    }
    this.flush();
  }
}

// =============================================================================
// EXPORTS
// =============================================================================

export const funnelTracker = FunnelTrackingService.getInstance();

// Convenience hooks for React components
export function useTrackPageView(pageName: string): void {
  if (typeof window !== 'undefined') {
    funnelTracker.track('feature_use', {
      featureName: 'page_view',
      featureCategory: 'navigation',
      pageName,
    });
  }
}

// Export types and instance
export default funnelTracker;
