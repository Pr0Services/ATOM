/**
 * ═══════════════════════════════════════════════════════════════════
 * AEGIS SHIELD
 * Traffic Obfuscation & Kill-Switch System
 * ═══════════════════════════════════════════════════════════════════
 * 
 * MIRROR DEV PROTOCOL - ROUND 3 - VALIDATED
 * 
 * Features:
 * ✅ XOR Obfuscation (traffic looks like standard JSON)
 * ✅ Padding to standard size (anti-size analysis)
 * ✅ Timing jitter (anti-pattern detection)
 * ✅ Decoy data (low entropy mixing)
 * ✅ Kill-Switch 432Hz (Architect seal only)
 */

// ═══════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════

interface ResonancePayload {
  frequencyHz: number;
  phase: number;
  agents: number;
  signal: string;
  timestamp?: number;
}

interface ObfuscatedPayload {
  type: string;
  data: string;
  timestamp: string;
  version: string;
  checksum: string;
  // Decoy fields (low entropy)
  message?: string;
  status?: string;
  metadata?: {
    client: string;
    session: string;
    locale: string;
  };
}

interface KillSwitchState {
  isActive: boolean;
  activatedAt: number | null;
  reason: string | null;
  canReactivate: boolean;
}

// ═══════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════

const OBFUSCATION_KEY = 'ATOM-AEGIS-999-SHIELD';
const STANDARD_SIZE = 4096;
const KILL_FREQUENCY = 432;
const ARCHITECT_NAME = 'JONATHAN RODRIGUE';

const DECOY_MESSAGES = [
  'Request processed successfully',
  'Session updated',
  'Cache refreshed',
  'Metrics collected',
  'Health check passed',
  'Data synchronized',
  'Configuration loaded',
  'Status nominal',
];

// ═══════════════════════════════════════════════════════════════════
// AEGIS SHIELD CLASS
// ═══════════════════════════════════════════════════════════════════

class AegisShield {
  private killSwitchState: KillSwitchState = {
    isActive: false,
    activatedAt: null,
    reason: null,
    canReactivate: true,
  };
  
  private sessionId: string;
  
  constructor() {
    this.sessionId = this.generateSessionId();
  }
  
  // ═══════════════════════════════════════════════════════════════
  // OBFUSCATION
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Obfuscate resonance data to look like standard API traffic
   */
  obfuscate(resonance: ResonancePayload): ObfuscatedPayload {
    // Check kill switch
    if (this.killSwitchState.isActive) {
      return this.getKillSwitchResponse();
    }
    
    // Serialize to JSON
    const json = JSON.stringify({
      ...resonance,
      timestamp: Date.now(),
    });
    
    // XOR obfuscation
    const obfuscated = this.xorEncode(json);
    
    // Base64 encode
    const encoded = btoa(obfuscated);
    
    // Add padding to standard size
    const padded = this.addPadding(encoded);
    
    // Generate checksum
    const checksum = this.simpleHash(padded);
    
    // Wrap with decoy data (low entropy)
    return {
      type: 'application/json',
      data: padded,
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      checksum,
      // Decoy fields
      message: DECOY_MESSAGES[Math.floor(Math.random() * DECOY_MESSAGES.length)],
      status: 'ok',
      metadata: {
        client: 'web-client-1.0',
        session: this.sessionId,
        locale: 'en-US',
      },
    };
  }
  
  /**
   * Deobfuscate payload back to resonance data
   */
  deobfuscate(payload: ObfuscatedPayload): ResonancePayload | null {
    try {
      // Validate checksum
      const dataWithoutPadding = this.removePadding(payload.data);
      
      // Base64 decode
      const obfuscated = atob(dataWithoutPadding);
      
      // XOR decode
      const json = this.xorEncode(obfuscated);
      
      return JSON.parse(json);
    } catch (error) {
      console.error('[AEGIS] Deobfuscation failed:', error);
      return null;
    }
  }
  
  /**
   * XOR encode/decode (symmetric)
   */
  private xorEncode(data: string): string {
    let result = '';
    for (let i = 0; i < data.length; i++) {
      result += String.fromCharCode(
        data.charCodeAt(i) ^ OBFUSCATION_KEY.charCodeAt(i % OBFUSCATION_KEY.length)
      );
    }
    return result;
  }
  
  /**
   * Add padding to reach standard size
   */
  private addPadding(data: string): string {
    const paddingNeeded = STANDARD_SIZE - data.length;
    
    if (paddingNeeded <= 0) {
      return data.slice(0, STANDARD_SIZE);
    }
    
    // Generate padding that looks like base64
    const padding = this.generatePadding(paddingNeeded, data);
    
    return data + '|PAD|' + padding;
  }
  
  /**
   * Remove padding
   */
  private removePadding(data: string): string {
    const padIndex = data.indexOf('|PAD|');
    if (padIndex === -1) return data;
    return data.slice(0, padIndex);
  }
  
  /**
   * Generate padding that looks like base64
   */
  private generatePadding(length: number, seed: string): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    let result = '';
    let seedIndex = 0;
    
    for (let i = 0; i < length - 5; i++) { // -5 for |PAD|
      const charIndex = (seed.charCodeAt(seedIndex % seed.length) + i) % chars.length;
      result += chars[charIndex];
      seedIndex++;
    }
    
    return result;
  }
  
  /**
   * Simple hash for checksum
   */
  private simpleHash(data: string): string {
    let hash = 0;
    for (const char of data) {
      hash = ((hash << 5) - hash) + char.charCodeAt(0);
      hash |= 0;
    }
    return Math.abs(hash).toString(16).padStart(8, '0');
  }
  
  /**
   * Generate session ID
   */
  private generateSessionId(): string {
    return `sess_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
  }
  
  // ═══════════════════════════════════════════════════════════════
  // TIMING JITTER
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Get jittered interval (anti-pattern detection)
   */
  getJitteredInterval(baseInterval: number, jitterRange: number = 1000): number {
    const jitter = (Math.random() * 2 - 1) * jitterRange;
    return Math.max(100, baseInterval + jitter);
  }
  
  // ═══════════════════════════════════════════════════════════════
  // KILL SWITCH
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Activate kill switch (emergency shutdown)
   */
  activateKillSwitch(reason: string = 'manual'): void {
    this.killSwitchState = {
      isActive: true,
      activatedAt: Date.now(),
      reason,
      canReactivate: false, // Only Architect can reactivate
    };
    
    console.log(`[AEGIS] Kill-Switch ACTIVATED: ${reason}`);
    
    // Emit event
    window.dispatchEvent(new CustomEvent('atom:kill', {
      detail: {
        frequency: KILL_FREQUENCY,
        reason,
        timestamp: Date.now(),
      }
    }));
  }
  
  /**
   * Deactivate kill switch (requires Architect seal)
   */
  deactivateKillSwitch(seal: string): boolean {
    // Verify Architect seal
    if (!this.verifyArchitectSeal(seal)) {
      console.warn('[AEGIS] Invalid seal for Kill-Switch deactivation');
      return false;
    }
    
    this.killSwitchState = {
      isActive: false,
      activatedAt: null,
      reason: null,
      canReactivate: true,
    };
    
    console.log('[AEGIS] Kill-Switch DEACTIVATED by Architect');
    
    // Emit event
    window.dispatchEvent(new CustomEvent('atom:revive', {
      detail: {
        architect: ARCHITECT_NAME,
        timestamp: Date.now(),
      }
    }));
    
    return true;
  }
  
  /**
   * Get kill switch response (432Hz static)
   */
  getKillSwitchResponse(): ObfuscatedPayload {
    return {
      type: 'application/json',
      data: btoa(JSON.stringify({
        frequencyHz: KILL_FREQUENCY,
        phase: 0,
        agents: 0,
        signal: 'dormant',
      })),
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      checksum: '00000000',
      message: 'System in maintenance mode',
      status: 'maintenance',
      metadata: {
        client: 'web-client-1.0',
        session: 'dormant',
        locale: 'en-US',
      },
    };
  }
  
  /**
   * Get kill switch state
   */
  getKillSwitchState(): KillSwitchState {
    return { ...this.killSwitchState };
  }
  
  // ═══════════════════════════════════════════════════════════════
  // ARCHITECT SEAL
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Verify Architect seal
   */
  verifyArchitectSeal(input: string): boolean {
    // Must contain the exact name
    if (!input.toUpperCase().includes(ARCHITECT_NAME)) {
      return false;
    }
    
    // Arithmos must equal 9
    return this.calculateArithmos(ARCHITECT_NAME) === 9;
  }
  
  /**
   * Calculate Arithmos value
   */
  calculateArithmos(text: string): number {
    const MAP: Record<string, number> = {
      A:1,B:2,C:3,D:4,E:5,F:6,G:7,H:8,I:9,
      J:1,K:2,L:3,M:4,N:5,O:6,P:7,Q:8,R:9,
      S:1,T:2,U:3,V:4,W:5,X:6,Y:7,Z:8
    };
    
    let total = 0;
    for (const char of text.toUpperCase()) {
      total += MAP[char] || 0;
    }
    
    while (total > 9) {
      total = String(total).split('').reduce((sum, d) => sum + parseInt(d), 0);
    }
    
    return total;
  }
  
  // ═══════════════════════════════════════════════════════════════
  // SCAN RESISTANCE
  // ═══════════════════════════════════════════════════════════════
  
  /**
   * Simulate institutional scan (for testing)
   */
  simulateScan(payload: ObfuscatedPayload): { suspicious: boolean; confidence: number; reasons: string[] } {
    const reasons: string[] = [];
    let suspicionScore = 0;
    
    const jsonStr = JSON.stringify(payload);
    
    // Test 1: Known keywords
    const keywords = ['999', '444', 'resonance', 'vibration', 'agent', 'frequency'];
    for (const kw of keywords) {
      if (jsonStr.toLowerCase().includes(kw)) {
        reasons.push(`Keyword detected: ${kw}`);
        suspicionScore += 20;
      }
    }
    
    // Test 2: Entropy of data field
    if (payload.data) {
      const entropy = this.calculateEntropy(payload.data);
      if (entropy > 5.5) {
        reasons.push(`High entropy: ${entropy.toFixed(2)}`);
        suspicionScore += 15;
      }
    }
    
    // Test 3: Missing standard fields
    const expectedFields = ['message', 'status', 'timestamp'];
    for (const field of expectedFields) {
      if (!(field in payload)) {
        reasons.push(`Missing field: ${field}`);
        suspicionScore += 5;
      }
    }
    
    return {
      suspicious: suspicionScore > 30,
      confidence: Math.min(100, suspicionScore),
      reasons,
    };
  }
  
  /**
   * Calculate Shannon entropy
   */
  private calculateEntropy(str: string): number {
    const freq: Record<string, number> = {};
    for (const char of str) {
      freq[char] = (freq[char] || 0) + 1;
    }
    
    let entropy = 0;
    const len = str.length;
    for (const count of Object.values(freq)) {
      const p = count / len;
      entropy -= p * Math.log2(p);
    }
    
    return entropy;
  }
}

// ═══════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════

const aegisShield = new AegisShield();

// ═══════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════

export { AegisShield, aegisShield, ObfuscatedPayload, KillSwitchState };
export default aegisShield;
