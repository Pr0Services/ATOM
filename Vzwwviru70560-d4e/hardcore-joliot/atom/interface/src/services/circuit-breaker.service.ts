/**
 * CIRCUIT BREAKER SERVICE - Resilience for External Calls
 * ========================================================
 *
 * Pattern circuit-breaker pour protéger contre les défaillances en cascade:
 * - CLOSED: Requêtes passent normalement
 * - OPEN: Requêtes bloquées, fallback retourné
 * - HALF-OPEN: Une requête test est permise
 *
 * Features:
 * - Seuil configurable d'échecs
 * - Timeout automatique
 * - Fallback gracieux UX
 * - Métriques par circuit
 */

// =============================================================================
// TYPES
// =============================================================================

type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

interface CircuitConfig {
  name: string;
  failureThreshold: number;   // Failures before opening
  recoveryTimeout: number;    // ms before trying half-open
  requestTimeout: number;     // ms before individual request timeout
  onStateChange?: (name: string, from: CircuitState, to: CircuitState) => void;
}

interface CircuitMetrics {
  totalRequests: number;
  successCount: number;
  failureCount: number;
  lastFailureTime: number | null;
  lastSuccessTime: number | null;
  consecutiveFailures: number;
  state: CircuitState;
  stateChangedAt: number;
}

// =============================================================================
// CIRCUIT BREAKER
// =============================================================================

class CircuitBreaker {
  private state: CircuitState = 'CLOSED';
  private failureCount = 0;
  private lastFailureTime: number | null = null;
  private lastSuccessTime: number | null = null;
  private totalRequests = 0;
  private successCount = 0;
  private stateChangedAt = Date.now();

  constructor(private config: CircuitConfig) {}

  /**
   * Execute a function through the circuit breaker
   */
  async execute<T>(fn: () => Promise<T>, fallback?: () => T): Promise<T> {
    this.totalRequests++;

    // Check if circuit is OPEN
    if (this.state === 'OPEN') {
      // Check if recovery timeout has elapsed
      if (Date.now() - (this.lastFailureTime || 0) >= this.config.recoveryTimeout) {
        this.transitionTo('HALF_OPEN');
      } else {
        // Return fallback or throw
        if (fallback) return fallback();
        throw new CircuitBreakerError(
          `Circuit "${this.config.name}" is OPEN. Service unavailable.`,
          this.config.name
        );
      }
    }

    try {
      // Execute with timeout
      const result = await this.withTimeout(fn(), this.config.requestTimeout);
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      if (fallback) return fallback();
      throw error;
    }
  }

  private async withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
    return Promise.race([
      promise,
      new Promise<never>((_, reject) =>
        setTimeout(
          () => reject(new Error(`Request timeout after ${timeoutMs}ms`)),
          timeoutMs
        )
      ),
    ]);
  }

  private onSuccess(): void {
    this.successCount++;
    this.lastSuccessTime = Date.now();

    if (this.state === 'HALF_OPEN') {
      this.transitionTo('CLOSED');
      this.failureCount = 0;
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.state === 'HALF_OPEN') {
      this.transitionTo('OPEN');
    } else if (this.failureCount >= this.config.failureThreshold) {
      this.transitionTo('OPEN');
    }
  }

  private transitionTo(newState: CircuitState): void {
    const oldState = this.state;
    this.state = newState;
    this.stateChangedAt = Date.now();

    console.log(
      `[CircuitBreaker] ${this.config.name}: ${oldState} → ${newState}`
    );

    this.config.onStateChange?.(this.config.name, oldState, newState);
  }

  getMetrics(): CircuitMetrics {
    return {
      totalRequests: this.totalRequests,
      successCount: this.successCount,
      failureCount: this.failureCount,
      lastFailureTime: this.lastFailureTime,
      lastSuccessTime: this.lastSuccessTime,
      consecutiveFailures: this.failureCount,
      state: this.state,
      stateChangedAt: this.stateChangedAt,
    };
  }

  getState(): CircuitState {
    return this.state;
  }

  reset(): void {
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.stateChangedAt = Date.now();
  }
}

// =============================================================================
// CUSTOM ERROR
// =============================================================================

export class CircuitBreakerError extends Error {
  constructor(
    message: string,
    public readonly circuitName: string
  ) {
    super(message);
    this.name = 'CircuitBreakerError';
  }
}

// =============================================================================
// CIRCUIT BREAKER REGISTRY
// =============================================================================

class CircuitBreakerRegistry {
  private circuits = new Map<string, CircuitBreaker>();
  private stateChangeListeners: Array<
    (name: string, from: CircuitState, to: CircuitState) => void
  > = [];

  /**
   * Get or create a circuit breaker
   */
  getCircuit(name: string, config?: Partial<Omit<CircuitConfig, 'name'>>): CircuitBreaker {
    if (!this.circuits.has(name)) {
      this.circuits.set(
        name,
        new CircuitBreaker({
          name,
          failureThreshold: config?.failureThreshold ?? 5,
          recoveryTimeout: config?.recoveryTimeout ?? 30000,
          requestTimeout: config?.requestTimeout ?? 10000,
          onStateChange: (n, from, to) => {
            this.stateChangeListeners.forEach((fn) => fn(n, from, to));
          },
        })
      );
    }
    return this.circuits.get(name)!;
  }

  /**
   * Execute through a named circuit
   */
  async execute<T>(
    name: string,
    fn: () => Promise<T>,
    fallback?: () => T
  ): Promise<T> {
    return this.getCircuit(name).execute(fn, fallback);
  }

  /**
   * Subscribe to state changes
   */
  onStateChange(
    listener: (name: string, from: CircuitState, to: CircuitState) => void
  ): () => void {
    this.stateChangeListeners.push(listener);
    return () => {
      this.stateChangeListeners = this.stateChangeListeners.filter(
        (fn) => fn !== listener
      );
    };
  }

  /**
   * Get metrics for all circuits
   */
  getAllMetrics(): Record<string, CircuitMetrics> {
    const metrics: Record<string, CircuitMetrics> = {};
    this.circuits.forEach((circuit, name) => {
      metrics[name] = circuit.getMetrics();
    });
    return metrics;
  }

  /**
   * Check if any circuit is open
   */
  hasOpenCircuits(): boolean {
    for (const circuit of this.circuits.values()) {
      if (circuit.getState() === 'OPEN') return true;
    }
    return false;
  }

  /**
   * Reset all circuits
   */
  resetAll(): void {
    this.circuits.forEach((circuit) => circuit.reset());
  }
}

// =============================================================================
// PRECONFIGURED CIRCUITS
// =============================================================================

export const circuitBreakers = new CircuitBreakerRegistry();

// API calls
export const apiCircuit = circuitBreakers.getCircuit('api', {
  failureThreshold: 5,
  recoveryTimeout: 30000,
  requestTimeout: 10000,
});

// Agent service calls
export const agentCircuit = circuitBreakers.getCircuit('agents', {
  failureThreshold: 3,
  recoveryTimeout: 60000,
  requestTimeout: 30000,
});

// Analytics/tracking (low priority)
export const analyticsCircuit = circuitBreakers.getCircuit('analytics', {
  failureThreshold: 10,
  recoveryTimeout: 120000,
  requestTimeout: 5000,
});

// Database/storage
export const storageCircuit = circuitBreakers.getCircuit('storage', {
  failureThreshold: 3,
  recoveryTimeout: 15000,
  requestTimeout: 8000,
});

// =============================================================================
// CONVENIENCE WRAPPER
// =============================================================================

/**
 * Wrap a fetch call with circuit breaker
 */
export async function resilientFetch<T>(
  circuitName: string,
  url: string,
  options?: RequestInit,
  fallback?: () => T
): Promise<T> {
  return circuitBreakers.execute(
    circuitName,
    async () => {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return response.json() as Promise<T>;
    },
    fallback
  );
}

export default circuitBreakers;
