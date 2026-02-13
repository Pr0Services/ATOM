/**
 * WAITLIST SERVICE - Gestion des inscriptions
 * ============================================
 *
 * Service de gestion de la waitlist avec persistance backend.
 * Remplace le stockage localStorage uniquement.
 *
 * FONCTIONNALITÉS:
 * - Soumission email avec validation
 * - Persistance backend (Supabase/PostgreSQL)
 * - Fallback localStorage si hors-ligne
 * - Déduplication automatique
 * - Tracking source et timestamp
 */

import { analyticsService } from './analytics.service';

// =============================================================================
// TYPES
// =============================================================================

export interface WaitlistEntry {
  email: string;
  source: 'landing' | 'auth' | 'essaim' | 'module' | 'other';
  campaign?: string;
  referrer?: string;
  timestamp: string;
  consentGiven: boolean;
  locale?: string;
  userAgent?: string;
}

export interface WaitlistResponse {
  success: boolean;
  message: string;
  position?: number;
  alreadyExists?: boolean;
}

// =============================================================================
// VALIDATION
// =============================================================================

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateEmail(email: string): boolean {
  return EMAIL_REGEX.test(email.trim().toLowerCase());
}

// =============================================================================
// LOCAL STORAGE FALLBACK
// =============================================================================

const LOCAL_WAITLIST_KEY = 'atom_waitlist_pending';

function getLocalQueue(): WaitlistEntry[] {
  try {
    const raw = localStorage.getItem(LOCAL_WAITLIST_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveToLocalQueue(entry: WaitlistEntry): void {
  try {
    const queue = getLocalQueue();
    // Déduplication
    const exists = queue.some(e => e.email.toLowerCase() === entry.email.toLowerCase());
    if (!exists) {
      queue.push(entry);
      localStorage.setItem(LOCAL_WAITLIST_KEY, JSON.stringify(queue));
    }
  } catch {
    // localStorage full - ignore
  }
}

function clearLocalQueue(): void {
  localStorage.removeItem(LOCAL_WAITLIST_KEY);
}

// =============================================================================
// WAITLIST SERVICE
// =============================================================================

class WaitlistServiceClass {
  private apiEndpoint: string;

  constructor() {
    this.apiEndpoint = `${import.meta.env.VITE_API_URL || 'https://atom-backend-fmywd.ondigitalocean.app'}/api/v1/waitlist`;
  }

  /**
   * Submit email to waitlist
   */
  async submit(
    email: string,
    source: WaitlistEntry['source'] = 'landing',
    campaign?: string
  ): Promise<WaitlistResponse> {
    // Validation
    if (!email || !validateEmail(email)) {
      return {
        success: false,
        message: 'Adresse email invalide',
      };
    }

    const entry: WaitlistEntry = {
      email: email.trim().toLowerCase(),
      source,
      campaign,
      referrer: typeof document !== 'undefined' ? document.referrer : undefined,
      timestamp: new Date().toISOString(),
      consentGiven: true,
      locale: typeof navigator !== 'undefined' ? navigator.language : undefined,
      userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : undefined,
    };

    // Track event
    analyticsService.track('waitlist_submit', {
      source,
      campaign,
      hasReferrer: !!entry.referrer,
    });

    // Try backend first
    if (navigator.onLine) {
      try {
        const response = await fetch(this.apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(entry),
        });

        if (response.ok) {
          const data = await response.json();
          return {
            success: true,
            message: data.message || 'Inscription réussie!',
            position: data.position,
            alreadyExists: data.already_exists,
          };
        }

        // Handle specific errors
        if (response.status === 409) {
          return {
            success: true,
            message: 'Vous êtes déjà inscrit!',
            alreadyExists: true,
          };
        }

        // Fallback to local
        saveToLocalQueue(entry);
        return {
          success: true,
          message: 'Inscription enregistrée (synchronisation en attente)',
        };
      } catch {
        // Network error - save locally
        saveToLocalQueue(entry);
        return {
          success: true,
          message: 'Inscription enregistrée (synchronisation automatique)',
        };
      }
    } else {
      // Offline - save locally
      saveToLocalQueue(entry);
      return {
        success: true,
        message: 'Inscription enregistrée (envoi dès connexion)',
      };
    }
  }

  /**
   * Sync local queue with backend
   */
  async syncPending(): Promise<number> {
    const queue = getLocalQueue();
    if (queue.length === 0 || !navigator.onLine) return 0;

    let synced = 0;

    for (const entry of queue) {
      try {
        const response = await fetch(this.apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(entry),
        });

        if (response.ok || response.status === 409) {
          synced++;
        }
      } catch {
        // Will retry next time
        break;
      }
    }

    if (synced === queue.length) {
      clearLocalQueue();
    } else if (synced > 0) {
      // Remove synced entries
      const remaining = queue.slice(synced);
      localStorage.setItem(LOCAL_WAITLIST_KEY, JSON.stringify(remaining));
    }

    return synced;
  }

  /**
   * Check if email is already in waitlist
   */
  async checkEmail(email: string): Promise<boolean> {
    if (!validateEmail(email)) return false;

    try {
      const response = await fetch(
        `${this.apiEndpoint}/check?email=${encodeURIComponent(email.trim().toLowerCase())}`
      );
      if (response.ok) {
        const data = await response.json();
        return data.exists;
      }
    } catch {
      // Fallback to local check
      const queue = getLocalQueue();
      return queue.some(e => e.email.toLowerCase() === email.toLowerCase());
    }

    return false;
  }

  /**
   * Get waitlist stats (admin only)
   */
  async getStats(): Promise<{
    total: number;
    today: number;
    sources: Record<string, number>;
  } | null> {
    try {
      const response = await fetch(`${this.apiEndpoint}/stats`);
      if (response.ok) {
        return await response.json();
      }
    } catch {
      // Unauthorized or error
    }
    return null;
  }

  /**
   * Get pending local entries count
   */
  getPendingCount(): number {
    return getLocalQueue().length;
  }
}

// Singleton export
export const waitlistService = new WaitlistServiceClass();

export default waitlistService;
