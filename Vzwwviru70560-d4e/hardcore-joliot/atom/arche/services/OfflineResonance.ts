/**
 * ═══════════════════════════════════════════════════════════════════
 * OFFLINE RESONANCE SERVICE
 * Local Storage Buffer & Self-Healing Mode
 * ═══════════════════════════════════════════════════════════════════
 * 
 * MIRROR DEV PROTOCOL - ROUND 1 - VALIDATED
 * 
 * Corrections Applied:
 * ✅ CORRECTION 2: Persistent buffer with localStorage
 * ✅ Burst transmission on reconnection (no backend saturation)
 * ✅ Self-healing mode when offline
 */

// ═══════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════

interface BufferedMessage {
  id: string;
  type: string;
  payload: any;
  timestamp: number;
  retryCount: number;
}

interface OfflineConfig {
  bufferKey: string;
  maxBufferSize: number;
  flushBatchSize: number;
  flushInterval: number;
  selfHealingInterval: number;
}

interface OfflineState {
  isOffline: boolean;
  bufferedCount: number;
  lastSync: number;
  selfHealingActive: boolean;
}

// ═══════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════

const DEFAULT_CONFIG: OfflineConfig = {
  bufferKey: 'atom_resonance_buffer',
  maxBufferSize: 100,
  flushBatchSize: 10,        // Send 10 messages per batch
  flushInterval: 100,        // 100ms between batches (prevents saturation)
  selfHealingInterval: 4440, // 4.44 seconds
};

// ═══════════════════════════════════════════════════════════════════
// OFFLINE RESONANCE CLASS
// ═══════════════════════════════════════════════════════════════════

class OfflineResonance {
  private config: OfflineConfig;
  private state: OfflineState;
  private buffer: BufferedMessage[] = [];
  private selfHealingTimer: ReturnType<typeof setInterval> | null = null;
  private flushInProgress: boolean = false;
  private sendCallback: ((msg: BufferedMessage) => Promise<boolean>) | null = null;
  
  constructor(config: Partial<OfflineConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.state = {
      isOffline: !navigator.onLine,
      bufferedCount: 0,
      lastSync: Date.now(),
      selfHealingActive: false,
    };
    
    this.loadBuffer();
    this.setupNetworkListeners();
  }
  
  // ═══════════════════════════════════════════════════════════════
  // PUBLIC METHODS
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Initialize with send callback
   */
  init(sendCallback: (msg: BufferedMessage) => Promise<boolean>): void {
    this.sendCallback = sendCallback;
    
    if (this.state.isOffline) {
      this.enterOfflineMode();
    }
  }
  
  /**
   * Buffer a message for later transmission
   */
  bufferMessage(type: string, payload: any): string {
    const message: BufferedMessage = {
      id: this.generateId(),
      type,
      payload,
      timestamp: Date.now(),
      retryCount: 0,
    };
    
    // Add to buffer
    this.buffer.push(message);
    
    // Enforce max size (remove oldest)
    while (this.buffer.length > this.config.maxBufferSize) {
      this.buffer.shift();
    }
    
    // Save to localStorage
    this.saveBuffer();
    
    this.state.bufferedCount = this.buffer.length;
    
    console.log(`[OFFLINE] Buffered message ${message.id} (total: ${this.buffer.length})`);
    
    return message.id;
  }
  
  /**
   * Flush buffer to server (with rate limiting)
   */
  async flushBuffer(): Promise<number> {
    if (this.flushInProgress) {
      console.log('[OFFLINE] Flush already in progress');
      return 0;
    }
    
    if (this.buffer.length === 0) {
      console.log('[OFFLINE] Buffer empty');
      return 0;
    }
    
    if (!this.sendCallback) {
      console.warn('[OFFLINE] No send callback configured');
      return 0;
    }
    
    this.flushInProgress = true;
    let sentCount = 0;
    
    console.log(`[OFFLINE] Starting buffer flush (${this.buffer.length} messages)`);
    
    // Process in batches to prevent backend saturation
    while (this.buffer.length > 0) {
      const batch = this.buffer.splice(0, this.config.flushBatchSize);
      
      for (const message of batch) {
        try {
          const success = await this.sendCallback(message);
          
          if (success) {
            sentCount++;
          } else {
            // Put back in buffer for retry
            message.retryCount++;
            if (message.retryCount < 3) {
              this.buffer.unshift(message);
            }
          }
        } catch (error) {
          console.error(`[OFFLINE] Failed to send ${message.id}:`, error);
          message.retryCount++;
          if (message.retryCount < 3) {
            this.buffer.unshift(message);
          }
        }
      }
      
      // Wait between batches to prevent saturation
      if (this.buffer.length > 0) {
        await this.sleep(this.config.flushInterval);
      }
    }
    
    // Clear localStorage
    this.saveBuffer();
    
    this.flushInProgress = false;
    this.state.bufferedCount = this.buffer.length;
    this.state.lastSync = Date.now();
    
    console.log(`[OFFLINE] Flush complete: ${sentCount} messages sent`);
    
    return sentCount;
  }
  
  /**
   * Get current state
   */
  getState(): OfflineState {
    return { ...this.state };
  }
  
  /**
   * Get buffered messages (for inspection)
   */
  getBuffer(): BufferedMessage[] {
    return [...this.buffer];
  }
  
  /**
   * Clear buffer (emergency)
   */
  clearBuffer(): void {
    this.buffer = [];
    localStorage.removeItem(this.config.bufferKey);
    this.state.bufferedCount = 0;
    console.log('[OFFLINE] Buffer cleared');
  }
  
  // ═══════════════════════════════════════════════════════════════
  // PRIVATE METHODS
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Setup network event listeners
   */
  private setupNetworkListeners(): void {
    window.addEventListener('online', () => this.onOnline());
    window.addEventListener('offline', () => this.onOffline());
  }
  
  /**
   * Handle going online
   */
  private async onOnline(): Promise<void> {
    console.log('[OFFLINE] Network restored');
    this.state.isOffline = false;
    this.exitOfflineMode();
    
    // Flush buffer after short delay (let connection stabilize)
    await this.sleep(500);
    await this.flushBuffer();
    
    window.dispatchEvent(new CustomEvent('atom:online'));
  }
  
  /**
   * Handle going offline
   */
  private onOffline(): void {
    console.log('[OFFLINE] Network lost');
    this.state.isOffline = true;
    this.enterOfflineMode();
    
    window.dispatchEvent(new CustomEvent('atom:offline'));
  }
  
  /**
   * Enter offline/self-healing mode
   */
  private enterOfflineMode(): void {
    if (this.state.selfHealingActive) return;
    
    this.state.selfHealingActive = true;
    
    console.log('[OFFLINE] Entering self-healing mode');
    
    // Start self-healing cycle
    this.selfHealingTimer = setInterval(() => {
      this.selfHealingCycle();
    }, this.config.selfHealingInterval);
    
    window.dispatchEvent(new CustomEvent('atom:selfhealing:start'));
  }
  
  /**
   * Exit offline/self-healing mode
   */
  private exitOfflineMode(): void {
    if (!this.state.selfHealingActive) return;
    
    this.state.selfHealingActive = false;
    
    if (this.selfHealingTimer) {
      clearInterval(this.selfHealingTimer);
      this.selfHealingTimer = null;
    }
    
    console.log('[OFFLINE] Exiting self-healing mode');
    
    window.dispatchEvent(new CustomEvent('atom:selfhealing:stop'));
  }
  
  /**
   * Self-healing cycle (maintain local state)
   */
  private selfHealingCycle(): void {
    // Emit local vibration event (agents continue vibrating)
    window.dispatchEvent(new CustomEvent('atom:selfhealing:tick', {
      detail: {
        timestamp: Date.now(),
        bufferedCount: this.buffer.length,
        frequency: 444, // Anchor frequency
      }
    }));
    
    console.log(`[OFFLINE] Self-healing tick (buffered: ${this.buffer.length})`);
  }
  
  /**
   * Load buffer from localStorage
   */
  private loadBuffer(): void {
    try {
      const stored = localStorage.getItem(this.config.bufferKey);
      if (stored) {
        this.buffer = JSON.parse(stored);
        this.state.bufferedCount = this.buffer.length;
        console.log(`[OFFLINE] Loaded ${this.buffer.length} buffered messages`);
      }
    } catch (error) {
      console.error('[OFFLINE] Failed to load buffer:', error);
      this.buffer = [];
    }
  }
  
  /**
   * Save buffer to localStorage
   */
  private saveBuffer(): void {
    try {
      localStorage.setItem(this.config.bufferKey, JSON.stringify(this.buffer));
    } catch (error) {
      console.error('[OFFLINE] Failed to save buffer:', error);
      // If localStorage is full, trim buffer
      if (this.buffer.length > 10) {
        this.buffer = this.buffer.slice(-10);
        try {
          localStorage.setItem(this.config.bufferKey, JSON.stringify(this.buffer));
        } catch {
          // Give up on persistence
          console.error('[OFFLINE] localStorage full, buffer not persisted');
        }
      }
    }
  }
  
  /**
   * Generate unique message ID
   */
  private generateId(): string {
    return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  }
  
  /**
   * Sleep utility
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ═══════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════

const offlineResonance = new OfflineResonance();

// ═══════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════

export { OfflineResonance, offlineResonance, BufferedMessage, OfflineState };
export default offlineResonance;
