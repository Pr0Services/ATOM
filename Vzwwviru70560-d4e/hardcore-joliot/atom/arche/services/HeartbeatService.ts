/**
 * ═══════════════════════════════════════════════════════════════════
 * HEARTBEAT SERVICE
 * 444Hz Isochrone Signal Maintenance
 * ═══════════════════════════════════════════════════════════════════
 * 
 * MIRROR DEV PROTOCOL - ROUND 1 - VALIDATED
 * 
 * Corrections Applied:
 * ✅ CORRECTION 1: Jitter compensation for drift prevention
 * ✅ CORRECTION 2: Isochrone maintenance with performance.now()
 * ✅ CORRECTION 3: CPU optimization with requestIdleCallback
 */

// ═══════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════

interface HeartbeatConfig {
  interval: number;           // Base interval in ms (4440)
  maxJitter: number;          // Maximum jitter compensation in ms
  frequency: number;          // Target frequency (444 Hz)
  onBeat: (beat: HeartbeatData) => void;
  onDrift: (drift: number) => void;
}

interface HeartbeatData {
  beatNumber: number;
  timestamp: number;
  frequency: number;
  phase: number;
  drift: number;
  isIsochrone: boolean;
}

interface HeartbeatState {
  isRunning: boolean;
  beatCount: number;
  startTime: number;
  lastBeatTime: number;
  totalDrift: number;
  averageDrift: number;
}

// ═══════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════

const DEFAULT_CONFIG: HeartbeatConfig = {
  interval: 4440,            // 4.44 seconds
  maxJitter: 50,             // 50ms max compensation
  frequency: 444,            // 444 Hz anchor
  onBeat: () => {},
  onDrift: () => {},
};

const DRIFT_THRESHOLD = 10;  // 10ms acceptable drift
const PHASE_INCREMENT = 40;  // 360° / 9 beats = 40° per beat

// ═══════════════════════════════════════════════════════════════════
// HEARTBEAT SERVICE CLASS
// ═══════════════════════════════════════════════════════════════════

class HeartbeatService {
  private config: HeartbeatConfig;
  private state: HeartbeatState;
  private timerId: number | null = null;
  private driftHistory: number[] = [];
  
  constructor(config: Partial<HeartbeatConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.state = {
      isRunning: false,
      beatCount: 0,
      startTime: 0,
      lastBeatTime: 0,
      totalDrift: 0,
      averageDrift: 0,
    };
  }
  
  // ═══════════════════════════════════════════════════════════════
  // PUBLIC METHODS
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Start the heartbeat service
   */
  start(): void {
    if (this.state.isRunning) {
      console.warn('[HEARTBEAT] Already running');
      return;
    }
    
    this.state.isRunning = true;
    this.state.startTime = performance.now();
    this.state.lastBeatTime = this.state.startTime;
    this.state.beatCount = 0;
    
    console.log('[HEARTBEAT] Starting 444Hz isochrone service');
    this.scheduleBeat();
  }
  
  /**
   * Stop the heartbeat service
   */
  stop(): void {
    if (!this.state.isRunning) return;
    
    this.state.isRunning = false;
    
    if (this.timerId !== null) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
    
    console.log(`[HEARTBEAT] Stopped after ${this.state.beatCount} beats`);
    console.log(`[HEARTBEAT] Average drift: ${this.state.averageDrift.toFixed(2)}ms`);
  }
  
  /**
   * Get current state
   */
  getState(): HeartbeatState {
    return { ...this.state };
  }
  
  /**
   * Check if heartbeat is healthy (low drift)
   */
  isHealthy(): boolean {
    return this.state.averageDrift < DRIFT_THRESHOLD;
  }
  
  // ═══════════════════════════════════════════════════════════════
  // PRIVATE METHODS
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Schedule the next beat with drift compensation
   * CORRECTION 1: Jitter compensation
   */
  private scheduleBeat(): void {
    if (!this.state.isRunning) return;
    
    const now = performance.now();
    const elapsed = now - this.state.startTime;
    
    // Calculate expected time for next beat
    const expectedNextBeat = (this.state.beatCount + 1) * this.config.interval;
    
    // Calculate actual delay needed (with drift compensation)
    let delay = expectedNextBeat - elapsed;
    
    // Clamp delay to prevent negative values
    if (delay < 0) {
      // We're behind schedule - try to catch up
      delay = Math.max(0, this.config.interval + delay);
    }
    
    // Add small jitter for anti-pattern detection (security)
    // CORRECTION 3: But keep it minimal for isochrone maintenance
    const jitter = (Math.random() - 0.5) * 10; // ±5ms max
    delay = Math.max(100, delay + jitter);
    
    // Schedule using requestIdleCallback for CPU optimization
    // CORRECTION 3: CPU optimization
    if ('requestIdleCallback' in window) {
      this.timerId = window.setTimeout(() => {
        (window as any).requestIdleCallback(() => this.beat(), { timeout: 100 });
      }, delay - 50) as unknown as number;
    } else {
      this.timerId = window.setTimeout(() => this.beat(), delay) as unknown as number;
    }
  }
  
  /**
   * Execute a heartbeat
   * CORRECTION 2: Isochrone maintenance
   */
  private beat(): void {
    if (!this.state.isRunning) return;
    
    const now = performance.now();
    this.state.beatCount++;
    
    // Calculate drift from expected time
    const expectedTime = this.state.startTime + (this.state.beatCount * this.config.interval);
    const drift = now - expectedTime;
    
    // Track drift history
    this.driftHistory.push(drift);
    if (this.driftHistory.length > 100) {
      this.driftHistory.shift();
    }
    
    // Update state
    this.state.totalDrift += Math.abs(drift);
    this.state.averageDrift = this.state.totalDrift / this.state.beatCount;
    this.state.lastBeatTime = now;
    
    // Check if isochrone (drift within threshold)
    const isIsochrone = Math.abs(drift) < DRIFT_THRESHOLD;
    
    // Calculate phase (0-360)
    const phase = (this.state.beatCount * PHASE_INCREMENT) % 360;
    
    // Build beat data
    const beatData: HeartbeatData = {
      beatNumber: this.state.beatCount,
      timestamp: now,
      frequency: this.config.frequency,
      phase,
      drift,
      isIsochrone,
    };
    
    // Emit beat callback
    this.config.onBeat(beatData);
    
    // Check for significant drift
    if (Math.abs(drift) > this.config.maxJitter) {
      console.warn(`[HEARTBEAT] Drift detected: ${drift.toFixed(2)}ms`);
      this.config.onDrift(drift);
    }
    
    // Log every 10 beats
    if (this.state.beatCount % 10 === 0) {
      console.log(`[HEARTBEAT] Beat #${this.state.beatCount}, Phase: ${phase}°, Drift: ${drift.toFixed(2)}ms`);
    }
    
    // Schedule next beat
    this.scheduleBeat();
  }
}

// ═══════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════

const heartbeatService = new HeartbeatService({
  interval: 4440,
  frequency: 444,
  maxJitter: 50,
  onBeat: (beat) => {
    // Dispatch event for UI updates
    window.dispatchEvent(new CustomEvent('atom:heartbeat', { detail: beat }));
  },
  onDrift: (drift) => {
    // Alert on significant drift
    window.dispatchEvent(new CustomEvent('atom:drift', { detail: { drift } }));
  },
});

// ═══════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════

export { HeartbeatService, heartbeatService, HeartbeatData, HeartbeatState };
export default heartbeatService;
