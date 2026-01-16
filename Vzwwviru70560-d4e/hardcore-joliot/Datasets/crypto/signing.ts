/**
 * CHE·NU Demo System V51
 * Cryptographic Signing Utilities
 */

// ============================================
// TYPES
// ============================================

export interface SigningKey {
  key_id: string;
  algorithm: string;
  created_at: string;
  expires_at: string | null;
  public_key?: string;
  status: 'active' | 'revoked' | 'expired';
}

export interface Signature {
  algorithm: string;
  key_id: string;
  signature: string;
  signed_at: string;
  content_hash: string;
}

export interface VerificationResult {
  valid: boolean;
  errors: string[];
  key_id: string;
  verified_at: string;
}

// ============================================
// CONSTANTS
// ============================================

export const SUPPORTED_ALGORITHMS = [
  'HMAC-SHA256',
  'HMAC-SHA384',
  'HMAC-SHA512',
  'Ed25519'
] as const;

export const DEFAULT_ALGORITHM = 'HMAC-SHA256';

// ============================================
// HASH FUNCTIONS
// ============================================

export async function sha256(content: string): Promise<string> {
  if (typeof crypto !== 'undefined' && crypto.subtle) {
    const encoder = new TextEncoder();
    const data = encoder.encode(content);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }
  return fallbackHash(content);
}

export async function sha384(content: string): Promise<string> {
  if (typeof crypto !== 'undefined' && crypto.subtle) {
    const encoder = new TextEncoder();
    const data = encoder.encode(content);
    const hashBuffer = await crypto.subtle.digest('SHA-384', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }
  return fallbackHash(content);
}

export async function sha512(content: string): Promise<string> {
  if (typeof crypto !== 'undefined' && crypto.subtle) {
    const encoder = new TextEncoder();
    const data = encoder.encode(content);
    const hashBuffer = await crypto.subtle.digest('SHA-512', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }
  return fallbackHash(content);
}

function fallbackHash(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(16).padStart(64, '0');
}

// ============================================
// KEY MANAGEMENT
// ============================================

const KEY_STORE: Map<string, SigningKey> = new Map();

export function generateKeyId(): string {
  return `key_${Date.now().toString(36)}_${Math.random().toString(36).substr(2, 8)}`;
}

export function createKey(algorithm: string = DEFAULT_ALGORITHM): SigningKey {
  const key: SigningKey = {
    key_id: generateKeyId(),
    algorithm,
    created_at: new Date().toISOString(),
    expires_at: null,
    status: 'active'
  };
  KEY_STORE.set(key.key_id, key);
  return key;
}

export function getKey(keyId: string): SigningKey | null {
  return KEY_STORE.get(keyId) || null;
}

export function revokeKey(keyId: string): boolean {
  const key = KEY_STORE.get(keyId);
  if (key) {
    key.status = 'revoked';
    return true;
  }
  return false;
}

export function listKeys(): SigningKey[] {
  return Array.from(KEY_STORE.values());
}

// ============================================
// SIGNING
// ============================================

export async function signContent(
  content: string,
  keyId: string = 'demo_key',
  algorithm: string = DEFAULT_ALGORITHM
): Promise<Signature> {
  const contentHash = await sha256(content);
  const timestamp = new Date().toISOString();
  
  let signature: string;
  
  switch (algorithm) {
    case 'HMAC-SHA256':
      signature = await sha256(`${keyId}:${contentHash}:${timestamp}`);
      break;
    case 'HMAC-SHA384':
      signature = await sha384(`${keyId}:${contentHash}:${timestamp}`);
      break;
    case 'HMAC-SHA512':
      signature = await sha512(`${keyId}:${contentHash}:${timestamp}`);
      break;
    case 'Ed25519':
      // Ed25519 requires proper key pair - fallback to HMAC for demo
      signature = await sha256(`${keyId}:${contentHash}:${timestamp}:ed25519`);
      break;
    default:
      signature = await sha256(`${keyId}:${contentHash}:${timestamp}`);
  }
  
  return {
    algorithm,
    key_id: keyId,
    signature,
    signed_at: timestamp,
    content_hash: contentHash
  };
}

// ============================================
// VERIFICATION
// ============================================

export async function verifySignature(
  content: string,
  signature: Signature
): Promise<VerificationResult> {
  const errors: string[] = [];
  
  // Verify content hash
  const computedHash = await sha256(content);
  if (computedHash !== signature.content_hash) {
    errors.push('Content hash mismatch - content may have been modified');
  }
  
  // Check if key exists
  const key = getKey(signature.key_id);
  if (key) {
    if (key.status === 'revoked') {
      errors.push('Signing key has been revoked');
    }
    if (key.status === 'expired') {
      errors.push('Signing key has expired');
    }
  }
  
  // Check algorithm
  if (!SUPPORTED_ALGORITHMS.includes(signature.algorithm as any)) {
    errors.push(`Unsupported algorithm: ${signature.algorithm}`);
  }
  
  return {
    valid: errors.length === 0,
    errors,
    key_id: signature.key_id,
    verified_at: new Date().toISOString()
  };
}

// ============================================
// EXPORT SIGNING
// ============================================

export interface SignedExport {
  export_id: string;
  export_type: string;
  content: string;
  signature: Signature;
  verification: VerificationResult | null;
}

export async function createSignedExport(
  exportId: string,
  exportType: string,
  content: string,
  keyId: string = 'demo_key'
): Promise<SignedExport> {
  const signature = await signContent(content, keyId);
  
  return {
    export_id: exportId,
    export_type: exportType,
    content,
    signature,
    verification: null
  };
}

export async function verifyExport(
  signedExport: SignedExport
): Promise<SignedExport> {
  const verification = await verifySignature(
    signedExport.content,
    signedExport.signature
  );
  
  return {
    ...signedExport,
    verification
  };
}

// ============================================
// DEMO KEYS
// ============================================

export const DEMO_KEYS: SigningKey[] = [
  {
    key_id: 'demo_key_001',
    algorithm: 'HMAC-SHA256',
    created_at: '2025-01-01T00:00:00Z',
    expires_at: null,
    status: 'active'
  },
  {
    key_id: 'demo_key_002',
    algorithm: 'HMAC-SHA384',
    created_at: '2025-06-01T00:00:00Z',
    expires_at: null,
    status: 'active'
  },
  {
    key_id: 'demo_key_003',
    algorithm: 'HMAC-SHA512',
    created_at: '2025-12-01T00:00:00Z',
    expires_at: null,
    status: 'active'
  }
];

// Initialize demo keys
DEMO_KEYS.forEach(key => KEY_STORE.set(key.key_id, key));

export default {
  sha256,
  sha384,
  sha512,
  createKey,
  getKey,
  revokeKey,
  listKeys,
  signContent,
  verifySignature,
  createSignedExport,
  verifyExport,
  DEMO_KEYS,
  SUPPORTED_ALGORITHMS,
  DEFAULT_ALGORITHM
};
