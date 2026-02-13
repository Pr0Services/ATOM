/**
 * ERROR MONITORING SERVICE - Frontend Error Tracking
 * ===================================================
 *
 * Service Sentry-like pour capturer et reporter les erreurs frontend:
 * - Erreurs JS non gérées
 * - Erreurs de rendu React
 * - Erreurs réseau
 * - Erreurs de performance
 *
 * Features:
 * - Capture automatique window.onerror / unhandledrejection
 * - Contexte enrichi (user, route, session)
 * - Déduplication
 * - Alertes sur hausse erreurs
 * - Corrélation avec sessions analytics
 */

// =============================================================================
// TYPES
// =============================================================================

export type ErrorSeverity = 'low' | 'medium' | 'high' | 'critical';
export type ErrorCategory = 'javascript' | 'network' | 'react' | 'performance' | 'custom';

export interface CapturedError {
  id: string;
  timestamp: string;
  message: string;
  stack?: string;
  severity: ErrorSeverity;
  category: ErrorCategory;
  context: ErrorContext;
  fingerprint: string;
  count: number;
}

interface ErrorContext {
  url: string;
  route: string;
  userAgent: string;
  sessionId: string;
  userId?: string;
  extra?: Record<string, unknown>;
}

interface ErrorMonitorConfig {
  maxErrors: number;
  deduplicationWindow: number; // ms
  alertThreshold: number;     // errors per minute
  reportEndpoint?: string;
  enabled: boolean;
}

// =============================================================================
// ERROR MONITOR SERVICE
// =============================================================================

class ErrorMonitorService {
  private errors: CapturedError[] = [];
  private config: ErrorMonitorConfig;
  private sessionId: string;
  private isInitialized = false;
  private errorRateWindow: number[] = [];
  private listeners: Array<(error: CapturedError) => void> = [];

  constructor() {
    this.config = {
      maxErrors: 200,
      deduplicationWindow: 60000,
      alertThreshold: 10,
      enabled: true,
    };
    this.sessionId = this.generateSessionId();
  }

  /**
   * Initialize error monitoring (call once at app start)
   */
  init(config?: Partial<ErrorMonitorConfig>): void {
    if (this.isInitialized) return;

    if (config) {
      this.config = { ...this.config, ...config };
    }

    if (!this.config.enabled) return;

    // Global error handler
    window.addEventListener('error', (event) => {
      this.captureError({
        message: event.message || 'Unknown error',
        stack: event.error?.stack,
        severity: 'high',
        category: 'javascript',
        extra: {
          filename: event.filename,
          lineno: event.lineno,
          colno: event.colno,
        },
      });
    });

    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      const reason = event.reason;
      this.captureError({
        message: reason?.message || String(reason) || 'Unhandled promise rejection',
        stack: reason?.stack,
        severity: 'high',
        category: 'javascript',
        extra: { type: 'unhandledrejection' },
      });
    });

    // Performance observer for long tasks
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (entry.duration > 100) {
              this.captureError({
                message: `Long task detected: ${Math.round(entry.duration)}ms`,
                severity: entry.duration > 500 ? 'medium' : 'low',
                category: 'performance',
                extra: {
                  duration: entry.duration,
                  startTime: entry.startTime,
                  name: entry.name,
                },
              });
            }
          }
        });
        observer.observe({ entryTypes: ['longtask'] });
      } catch {
        // PerformanceObserver not supported for longtask
      }
    }

    this.isInitialized = true;
    console.log('[ErrorMonitor] Initialized');
  }

  /**
   * Capture an error manually
   */
  captureError(params: {
    message: string;
    stack?: string;
    severity?: ErrorSeverity;
    category?: ErrorCategory;
    extra?: Record<string, unknown>;
  }): CapturedError {
    const fingerprint = this.generateFingerprint(params.message, params.stack);

    // Deduplicate
    const existing = this.errors.find(
      (e) =>
        e.fingerprint === fingerprint &&
        Date.now() - new Date(e.timestamp).getTime() < this.config.deduplicationWindow
    );

    if (existing) {
      existing.count++;
      existing.timestamp = new Date().toISOString();
      return existing;
    }

    const error: CapturedError = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      message: params.message,
      stack: params.stack,
      severity: params.severity || 'medium',
      category: params.category || 'custom',
      fingerprint,
      count: 1,
      context: {
        url: window.location.href,
        route: window.location.pathname,
        userAgent: navigator.userAgent,
        sessionId: this.sessionId,
        extra: params.extra,
      },
    };

    this.errors.unshift(error);

    // Trim to max
    if (this.errors.length > this.config.maxErrors) {
      this.errors = this.errors.slice(0, this.config.maxErrors);
    }

    // Track error rate
    this.errorRateWindow.push(Date.now());
    this.errorRateWindow = this.errorRateWindow.filter(
      (t) => Date.now() - t < 60000
    );

    // Alert on high error rate
    if (this.errorRateWindow.length >= this.config.alertThreshold) {
      this.onHighErrorRate();
    }

    // Report to backend if configured
    if (this.config.reportEndpoint) {
      this.reportError(error);
    }

    // Notify listeners
    this.listeners.forEach((fn) => fn(error));

    // Console log (dev)
    if (import.meta.env.DEV) {
      console.warn(
        `[ErrorMonitor] [${error.severity}] ${error.category}: ${error.message}`
      );
    }

    return error;
  }

  /**
   * Capture a network error
   */
  captureNetworkError(url: string, status: number, method = 'GET'): CapturedError {
    return this.captureError({
      message: `Network error: ${method} ${url} → ${status}`,
      severity: status >= 500 ? 'high' : 'medium',
      category: 'network',
      extra: { url, status, method },
    });
  }

  /**
   * Capture a React component error
   */
  captureReactError(
    error: Error,
    componentStack: string,
    componentName?: string
  ): CapturedError {
    return this.captureError({
      message: `React error in ${componentName || 'unknown'}: ${error.message}`,
      stack: error.stack,
      severity: 'critical',
      category: 'react',
      extra: { componentStack, componentName },
    });
  }

  /**
   * Subscribe to new errors
   */
  onError(listener: (error: CapturedError) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((fn) => fn !== listener);
    };
  }

  /**
   * Get all captured errors
   */
  getErrors(filter?: {
    severity?: ErrorSeverity;
    category?: ErrorCategory;
    since?: Date;
  }): CapturedError[] {
    let result = [...this.errors];

    if (filter?.severity) {
      result = result.filter((e) => e.severity === filter.severity);
    }
    if (filter?.category) {
      result = result.filter((e) => e.category === filter.category);
    }
    if (filter?.since) {
      result = result.filter(
        (e) => new Date(e.timestamp) >= filter.since!
      );
    }

    return result;
  }

  /**
   * Get error statistics
   */
  getStats(): {
    total: number;
    bySeverity: Record<ErrorSeverity, number>;
    byCategory: Record<ErrorCategory, number>;
    errorsPerMinute: number;
    uniqueErrors: number;
  } {
    const bySeverity = { low: 0, medium: 0, high: 0, critical: 0 };
    const byCategory = { javascript: 0, network: 0, react: 0, performance: 0, custom: 0 };

    this.errors.forEach((e) => {
      bySeverity[e.severity]++;
      byCategory[e.category]++;
    });

    const fingerprints = new Set(this.errors.map((e) => e.fingerprint));

    return {
      total: this.errors.length,
      bySeverity,
      byCategory,
      errorsPerMinute: this.errorRateWindow.filter(
        (t) => Date.now() - t < 60000
      ).length,
      uniqueErrors: fingerprints.size,
    };
  }

  /**
   * Clear all captured errors
   */
  clear(): void {
    this.errors = [];
    this.errorRateWindow = [];
  }

  // Private methods

  private generateFingerprint(message: string, stack?: string): string {
    const key = `${message}|${(stack || '').split('\n')[0]}`;
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      const char = key.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(36);
  }

  private generateSessionId(): string {
    const stored = sessionStorage.getItem('atom_error_session');
    if (stored) return stored;
    const id = crypto.randomUUID();
    sessionStorage.setItem('atom_error_session', id);
    return id;
  }

  private onHighErrorRate(): void {
    console.error(
      `[ErrorMonitor] HIGH ERROR RATE: ${this.errorRateWindow.length} errors in the last minute`
    );
  }

  private async reportError(error: CapturedError): Promise<void> {
    if (!this.config.reportEndpoint) return;

    try {
      await fetch(this.config.reportEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(error),
        keepalive: true,
      });
    } catch {
      // Silently fail - don't create error loops
    }
  }
}

// =============================================================================
// SINGLETON & EXPORTS
// =============================================================================

export const errorMonitor = new ErrorMonitorService();

/**
 * Convenience: capture error
 */
export function captureError(
  message: string,
  extra?: Record<string, unknown>
): void {
  errorMonitor.captureError({ message, extra });
}

/**
 * Convenience: wrap async function with error capture
 */
export function withErrorCapture<T extends (...args: unknown[]) => Promise<unknown>>(
  fn: T,
  context?: string
): T {
  return (async (...args: unknown[]) => {
    try {
      return await fn(...args);
    } catch (error) {
      errorMonitor.captureError({
        message: error instanceof Error ? error.message : String(error),
        stack: error instanceof Error ? error.stack : undefined,
        severity: 'high',
        extra: { context, args: args.length },
      });
      throw error;
    }
  }) as T;
}

export default errorMonitor;
