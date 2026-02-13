/**
 * ANALYTICS SERVICE - Instrumentation UX
 * =======================================
 *
 * Service d'instrumentation pour le funnel de conversion.
 * Capture les événements critiques pour mesurer l'efficacité UX.
 *
 * ÉVÉNEMENTS CRITIQUES (Phase 0):
 * 1. landing_view - Vue de la landing page
 * 2. cta_click - Clic sur CTA principal
 * 3. auth_enter - Entrée dans le sas d'accès
 * 4. waitlist_submit - Soumission waitlist
 * 5. index_first_action - Première action après entrée
 *
 * ROADMAP:
 * - Phase 1: Intégration backend (POST /api/v1/analytics/events)
 * - Phase 2: Segments utilisateur
 * - Phase 3: A/B testing
 */

// =============================================================================
// TYPES
// =============================================================================

export type EventName =
  | 'landing_view'
  | 'cta_click'
  | 'auth_enter'
  | 'waitlist_submit'
  | 'index_first_action'
  | 'sceau_hold'
  | 'sceau_activate'
  | 'essaim_view'
  | 'agent_hover'
  | 'agent_click'
  | 'module_enter'
  | 'workspace_view'
  | 'error_displayed'
  | 'retry_action';

export interface AnalyticsEvent {
  name: EventName;
  timestamp: string;
  sessionId: string;
  userId?: string;
  properties?: Record<string, unknown>;
  page?: string;
  referrer?: string;
  userAgent?: string;
  screenSize?: string;
}

export interface FunnelStep {
  step: number;
  name: string;
  completed: boolean;
  timestamp?: string;
  duration?: number; // ms depuis étape précédente
}

// =============================================================================
// SESSION MANAGEMENT
// =============================================================================

const SESSION_KEY = 'atom_session_id';
const EVENTS_KEY = 'atom_events_queue';
const FUNNEL_KEY = 'atom_funnel_state';

function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
}

function getOrCreateSessionId(): string {
  let sessionId = sessionStorage.getItem(SESSION_KEY);
  if (!sessionId) {
    sessionId = generateSessionId();
    sessionStorage.setItem(SESSION_KEY, sessionId);
  }
  return sessionId;
}

// =============================================================================
// EVENT QUEUE (localStorage fallback)
// =============================================================================

function getEventQueue(): AnalyticsEvent[] {
  try {
    const raw = localStorage.getItem(EVENTS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveEventQueue(events: AnalyticsEvent[]): void {
  try {
    // Garder seulement les 500 derniers événements
    const trimmed = events.slice(-500);
    localStorage.setItem(EVENTS_KEY, JSON.stringify(trimmed));
  } catch {
    // localStorage full - clear and retry
    localStorage.removeItem(EVENTS_KEY);
  }
}

// =============================================================================
// FUNNEL TRACKING
// =============================================================================

const FUNNEL_STEPS: { name: EventName; label: string }[] = [
  { name: 'landing_view', label: 'Landing View' },
  { name: 'cta_click', label: 'CTA Click' },
  { name: 'sceau_activate', label: 'Sceau Activated' },
  { name: 'essaim_view', label: 'Essaim View' },
  { name: 'module_enter', label: 'Module Enter' },
];

function getFunnelState(): FunnelStep[] {
  try {
    const raw = localStorage.getItem(FUNNEL_KEY);
    return raw ? JSON.parse(raw) : FUNNEL_STEPS.map((s, i) => ({
      step: i + 1,
      name: s.label,
      completed: false,
    }));
  } catch {
    return FUNNEL_STEPS.map((s, i) => ({
      step: i + 1,
      name: s.label,
      completed: false,
    }));
  }
}

function saveFunnelState(state: FunnelStep[]): void {
  try {
    localStorage.setItem(FUNNEL_KEY, JSON.stringify(state));
  } catch {
    // Ignore
  }
}

function updateFunnel(eventName: EventName): void {
  const stepIndex = FUNNEL_STEPS.findIndex(s => s.name === eventName);
  if (stepIndex === -1) return;

  const state = getFunnelState();
  const previousStep = stepIndex > 0 ? state[stepIndex - 1] : null;

  state[stepIndex] = {
    ...state[stepIndex],
    completed: true,
    timestamp: new Date().toISOString(),
    duration: previousStep?.timestamp
      ? Date.now() - new Date(previousStep.timestamp).getTime()
      : undefined,
  };

  saveFunnelState(state);
}

// =============================================================================
// ANALYTICS SERVICE
// =============================================================================

class AnalyticsServiceClass {
  private sessionId: string;
  private apiEndpoint: string;
  private isEnabled: boolean;

  constructor() {
    this.sessionId = getOrCreateSessionId();
    this.apiEndpoint = `${import.meta.env.VITE_API_URL || 'https://atom-backend-fmywd.ondigitalocean.app'}/api/v1/analytics/events`;
    this.isEnabled = true;

    // Flush queue on page unload
    if (typeof window !== 'undefined') {
      window.addEventListener('beforeunload', () => this.flush());
      window.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
          this.flush();
        }
      });
    }
  }

  /**
   * Track an event
   */
  track(name: EventName, properties?: Record<string, unknown>): void {
    if (!this.isEnabled) return;

    const event: AnalyticsEvent = {
      name,
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId,
      properties,
      page: typeof window !== 'undefined' ? window.location.pathname : undefined,
      referrer: typeof document !== 'undefined' ? document.referrer : undefined,
      userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : undefined,
      screenSize: typeof window !== 'undefined'
        ? `${window.innerWidth}x${window.innerHeight}`
        : undefined,
    };

    // Add to queue
    const queue = getEventQueue();
    queue.push(event);
    saveEventQueue(queue);

    // Update funnel
    updateFunnel(name);

    // Console log in dev
    if (import.meta.env.DEV) {
      console.log('[Analytics]', name, properties || '');
    }

    // Attempt immediate send if online
    this.sendEvent(event);
  }

  /**
   * Send event to backend
   */
  private async sendEvent(event: AnalyticsEvent): Promise<boolean> {
    if (!navigator.onLine) return false;

    try {
      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event),
        keepalive: true,
      });
      return response.ok;
    } catch {
      // Will retry on flush
      return false;
    }
  }

  /**
   * Flush all queued events to backend
   */
  async flush(): Promise<void> {
    const queue = getEventQueue();
    if (queue.length === 0) return;

    try {
      const response = await fetch(`${this.apiEndpoint}/batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ events: queue }),
        keepalive: true,
      });

      if (response.ok) {
        localStorage.removeItem(EVENTS_KEY);
      }
    } catch {
      // Keep events in queue for next flush
    }
  }

  /**
   * Get funnel state
   */
  getFunnel(): FunnelStep[] {
    return getFunnelState();
  }

  /**
   * Get session stats
   */
  getSessionStats(): {
    sessionId: string;
    eventsCount: number;
    funnelProgress: number;
  } {
    const queue = getEventQueue();
    const funnel = getFunnelState();
    const completedSteps = funnel.filter(s => s.completed).length;

    return {
      sessionId: this.sessionId,
      eventsCount: queue.length,
      funnelProgress: Math.round((completedSteps / funnel.length) * 100),
    };
  }

  /**
   * Disable tracking (for GDPR/privacy)
   */
  disable(): void {
    this.isEnabled = false;
  }

  /**
   * Enable tracking
   */
  enable(): void {
    this.isEnabled = true;
  }
}

// Singleton export
export const analyticsService = new AnalyticsServiceClass();

// Convenience exports
export const track = (name: EventName, properties?: Record<string, unknown>) =>
  analyticsService.track(name, properties);

export default analyticsService;
