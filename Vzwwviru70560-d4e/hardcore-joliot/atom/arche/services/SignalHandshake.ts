/**
 * ═══════════════════════════════════════════════════════════════════
 * SIGNAL HANDSHAKE SERVICE
 * WebSocket Synchronization with Backend
 * ═══════════════════════════════════════════════════════════════════
 * 
 * MIRROR DEV PROTOCOL - ROUND 1 - VALIDATED
 * 
 * Responsibilities:
 * - Establish and maintain WebSocket connection
 * - Transmit Arithmos calculations in real-time
 * - Handle acknowledgments and latency tracking
 * - Manage reconnection with exponential backoff
 */

// ═══════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════

interface HandshakeConfig {
  wsUrl: string;
  reconnectDelay: number;
  maxReconnectDelay: number;
  backoffMultiplier: number;
  maxReconnectAttempts: number;
  heartbeatInterval: number;
}

interface ResonancePayload {
  inputText: string;
  arithmosValue: number;
  frequencyHz: number;
  level: number;
  timestamp: number;
  sequence: number;
  checksum: string;
}

interface HandshakeMessage {
  type: 'RESONANCE_EMIT' | 'RESONANCE_ACK' | 'HEARTBEAT' | 'HEARTBEAT_ACK';
  payload: Partial<ResonancePayload> & Record<string, any>;
}

interface ConnectionState {
  isConnected: boolean;
  reconnectAttempts: number;
  lastMessageTime: number;
  latencyMs: number;
  pendingAcks: Map<number, number>;
}

// ═══════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════

const DEFAULT_CONFIG: HandshakeConfig = {
  wsUrl: 'wss://api.chenu.io/resonance',
  reconnectDelay: 1000,
  maxReconnectDelay: 30000,
  backoffMultiplier: 2,
  maxReconnectAttempts: 10,
  heartbeatInterval: 4440,
};

// ═══════════════════════════════════════════════════════════════════
// SIGNAL HANDSHAKE CLASS
// ═══════════════════════════════════════════════════════════════════

class SignalHandshake {
  private config: HandshakeConfig;
  private ws: WebSocket | null = null;
  private state: ConnectionState;
  private sequenceCounter: number = 0;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null;
  private messageCallbacks: Map<string, (msg: HandshakeMessage) => void> = new Map();
  
  constructor(config: Partial<HandshakeConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.state = {
      isConnected: false,
      reconnectAttempts: 0,
      lastMessageTime: 0,
      latencyMs: 0,
      pendingAcks: new Map(),
    };
  }
  
  // ═══════════════════════════════════════════════════════════════
  // PUBLIC METHODS
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Initialize and connect
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        console.log(`[HANDSHAKE] Connecting to ${this.config.wsUrl}`);
        
        this.ws = new WebSocket(this.config.wsUrl);
        
        this.ws.onopen = () => {
          console.log('[HANDSHAKE] Connected');
          this.state.isConnected = true;
          this.state.reconnectAttempts = 0;
          this.startHeartbeat();
          this.emit('connected', {});
          resolve();
        };
        
        this.ws.onmessage = (event) => {
          this.handleMessage(JSON.parse(event.data));
        };
        
        this.ws.onclose = (event) => {
          console.log(`[HANDSHAKE] Disconnected (code: ${event.code})`);
          this.state.isConnected = false;
          this.stopHeartbeat();
          this.emit('disconnected', { code: event.code });
          this.scheduleReconnect();
        };
        
        this.ws.onerror = (error) => {
          console.error('[HANDSHAKE] Error:', error);
          this.emit('error', { error });
          reject(error);
        };
        
      } catch (error) {
        console.error('[HANDSHAKE] Failed to create WebSocket:', error);
        reject(error);
      }
    });
  }
  
  /**
   * Disconnect and cleanup
   */
  disconnect(): void {
    this.stopHeartbeat();
    
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
    }
    
    this.state.isConnected = false;
    console.log('[HANDSHAKE] Disconnected manually');
  }
  
  /**
   * Send resonance data
   */
  sendResonance(inputText: string, arithmosValue: number, frequencyHz: number, level: number): void {
    const sequence = ++this.sequenceCounter;
    const timestamp = Date.now();
    
    const payload: ResonancePayload = {
      inputText,
      arithmosValue,
      frequencyHz,
      level,
      timestamp,
      sequence,
      checksum: this.generateChecksum({ arithmosValue, frequencyHz, timestamp, sequence }),
    };
    
    this.send('RESONANCE_EMIT', payload);
    
    // Track for ACK
    this.state.pendingAcks.set(sequence, timestamp);
  }
  
  /**
   * Register callback for message type
   */
  on(type: string, callback: (msg: HandshakeMessage) => void): void {
    this.messageCallbacks.set(type, callback);
  }
  
  /**
   * Get connection state
   */
  getState(): ConnectionState {
    return { ...this.state, pendingAcks: new Map(this.state.pendingAcks) };
  }
  
  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.state.isConnected && this.ws?.readyState === WebSocket.OPEN;
  }
  
  // ═══════════════════════════════════════════════════════════════
  // PRIVATE METHODS
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Send message through WebSocket
   */
  private send(type: string, payload: any): void {
    if (!this.isConnected()) {
      console.warn('[HANDSHAKE] Not connected, message queued');
      return;
    }
    
    const message: HandshakeMessage = { type: type as any, payload };
    this.ws!.send(JSON.stringify(message));
  }
  
  /**
   * Handle incoming message
   */
  private handleMessage(message: HandshakeMessage): void {
    this.state.lastMessageTime = Date.now();
    
    switch (message.type) {
      case 'RESONANCE_ACK':
        this.handleResonanceAck(message.payload);
        break;
        
      case 'HEARTBEAT_ACK':
        this.handleHeartbeatAck(message.payload);
        break;
        
      default:
        // Custom callback
        const callback = this.messageCallbacks.get(message.type);
        if (callback) callback(message);
    }
  }
  
  /**
   * Handle resonance acknowledgment
   */
  private handleResonanceAck(payload: any): void {
    const sequence = payload.sequence;
    const sentTime = this.state.pendingAcks.get(sequence);
    
    if (sentTime) {
      this.state.latencyMs = Date.now() - sentTime;
      this.state.pendingAcks.delete(sequence);
      
      console.log(`[HANDSHAKE] ACK #${sequence}, latency: ${this.state.latencyMs}ms`);
    }
    
    this.emit('resonance_ack', payload);
  }
  
  /**
   * Handle heartbeat acknowledgment
   */
  private handleHeartbeatAck(payload: any): void {
    // Server is alive
    this.emit('heartbeat_ack', payload);
  }
  
  /**
   * Start heartbeat
   */
  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      this.send('HEARTBEAT', {
        timestamp: Date.now(),
        frequency: 444,
      });
    }, this.config.heartbeatInterval);
  }
  
  /**
   * Stop heartbeat
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }
  
  /**
   * Schedule reconnection with exponential backoff
   */
  private scheduleReconnect(): void {
    if (this.state.reconnectAttempts >= this.config.maxReconnectAttempts) {
      console.error('[HANDSHAKE] Max reconnect attempts reached');
      this.emit('max_reconnect', {});
      return;
    }
    
    const delay = Math.min(
      this.config.reconnectDelay * Math.pow(this.config.backoffMultiplier, this.state.reconnectAttempts),
      this.config.maxReconnectDelay
    );
    
    // Add jitter (±25%)
    const jitter = delay * 0.25 * (Math.random() * 2 - 1);
    const actualDelay = Math.round(delay + jitter);
    
    this.state.reconnectAttempts++;
    
    console.log(`[HANDSHAKE] Reconnecting in ${actualDelay}ms (attempt ${this.state.reconnectAttempts})`);
    
    this.reconnectTimer = setTimeout(() => {
      this.connect().catch(() => {});
    }, actualDelay);
  }
  
  /**
   * Emit event
   */
  private emit(type: string, payload: any): void {
    window.dispatchEvent(new CustomEvent(`handshake:${type}`, { detail: payload }));
    
    const callback = this.messageCallbacks.get(type);
    if (callback) callback({ type: type as any, payload });
  }
  
  /**
   * Generate checksum for payload integrity
   */
  private generateChecksum(data: { arithmosValue: number; frequencyHz: number; timestamp: number; sequence: number }): string {
    const str = `${data.arithmosValue}-${data.frequencyHz}-${data.timestamp}-${data.sequence}`;
    let hash = 0;
    for (const char of str) {
      hash = ((hash << 5) - hash) + char.charCodeAt(0);
      hash |= 0;
    }
    return Math.abs(hash).toString(16).padStart(8, '0');
  }
}

// ═══════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════

const signalHandshake = new SignalHandshake();

// ═══════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════

export { SignalHandshake, signalHandshake, ResonancePayload, ConnectionState };
export default signalHandshake;
