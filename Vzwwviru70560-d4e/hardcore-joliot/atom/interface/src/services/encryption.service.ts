// ═══════════════════════════════════════════════════════════════════════════
// AT·OM ENCRYPTION SERVICE
// End-to-end encryption for sovereign identity
// ═══════════════════════════════════════════════════════════════════════════

import nacl from 'tweetnacl';
import { encodeBase64, decodeBase64, encodeUTF8, decodeUTF8 } from 'tweetnacl-util';
import type { SplitIdentity, EncryptedPayload, KeyPair } from '@/types';

// ─────────────────────────────────────────────────────────────────────────────
// KEY GENERATION
// ─────────────────────────────────────────────────────────────────────────────

export function generateKeyPair(): KeyPair {
  const keyPair = nacl.box.keyPair();
  return {
    publicKey: keyPair.publicKey,
    secretKey: keyPair.secretKey,
  };
}

export function generateSigningKeyPair(): KeyPair {
  const keyPair = nacl.sign.keyPair();
  return {
    publicKey: keyPair.publicKey,
    secretKey: keyPair.secretKey,
  };
}

export function generateRandomBytes(length: number): Uint8Array {
  return nacl.randomBytes(length);
}

// ─────────────────────────────────────────────────────────────────────────────
// IDENTITY CREATION
// ─────────────────────────────────────────────────────────────────────────────

export function createSplitIdentity(): SplitIdentity {
  const keyPair = generateKeyPair();
  const publicId = generatePublicId(keyPair.publicKey);
  
  return {
    publicId,
    privateKey: keyPair.secretKey,
    publicKey: keyPair.publicKey,
    createdAt: new Date(),
    lastAccess: new Date(),
    recoverySetup: false,
  };
}

function generatePublicId(publicKey: Uint8Array): string {
  // Create a deterministic but anonymous public ID
  const hash = nacl.hash(publicKey);
  const shortened = hash.slice(0, 16);
  return `atom_${encodeBase64(shortened).replace(/[+/=]/g, '').slice(0, 16)}`;
}

// ─────────────────────────────────────────────────────────────────────────────
// SYMMETRIC ENCRYPTION (for local storage)
// ─────────────────────────────────────────────────────────────────────────────

export function encryptSymmetric(data: string, key: Uint8Array): EncryptedPayload {
  const nonce = nacl.randomBytes(nacl.secretbox.nonceLength);
  const messageUint8 = decodeUTF8(data);
  const ciphertext = nacl.secretbox(messageUint8, nonce, key);
  
  return {
    nonce: encodeBase64(nonce),
    ciphertext: encodeBase64(ciphertext),
    timestamp: Date.now(),
  };
}

export function decryptSymmetric(payload: EncryptedPayload, key: Uint8Array): string | null {
  try {
    const nonce = decodeBase64(payload.nonce);
    const ciphertext = decodeBase64(payload.ciphertext);
    const decrypted = nacl.secretbox.open(ciphertext, nonce, key);
    
    if (!decrypted) return null;
    return encodeUTF8(decrypted);
  } catch {
    return null;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// ASYMMETRIC ENCRYPTION (for sharing)
// ─────────────────────────────────────────────────────────────────────────────

export function encryptAsymmetric(
  data: string,
  recipientPublicKey: Uint8Array,
  senderSecretKey: Uint8Array
): EncryptedPayload {
  const nonce = nacl.randomBytes(nacl.box.nonceLength);
  const messageUint8 = decodeUTF8(data);
  const ciphertext = nacl.box(messageUint8, nonce, recipientPublicKey, senderSecretKey);
  
  return {
    nonce: encodeBase64(nonce),
    ciphertext: encodeBase64(ciphertext),
    timestamp: Date.now(),
  };
}

export function decryptAsymmetric(
  payload: EncryptedPayload,
  senderPublicKey: Uint8Array,
  recipientSecretKey: Uint8Array
): string | null {
  try {
    const nonce = decodeBase64(payload.nonce);
    const ciphertext = decodeBase64(payload.ciphertext);
    const decrypted = nacl.box.open(ciphertext, nonce, senderPublicKey, recipientSecretKey);
    
    if (!decrypted) return null;
    return encodeUTF8(decrypted);
  } catch {
    return null;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// SIGNING (for verification)
// ─────────────────────────────────────────────────────────────────────────────

export function signMessage(message: string, secretKey: Uint8Array): string {
  const messageUint8 = decodeUTF8(message);
  const signature = nacl.sign.detached(messageUint8, secretKey);
  return encodeBase64(signature);
}

export function verifySignature(
  message: string,
  signature: string,
  publicKey: Uint8Array
): boolean {
  try {
    const messageUint8 = decodeUTF8(message);
    const signatureUint8 = decodeBase64(signature);
    return nacl.sign.detached.verify(messageUint8, signatureUint8, publicKey);
  } catch {
    return false;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// KEY DERIVATION (from password)
// ─────────────────────────────────────────────────────────────────────────────

export async function deriveKeyFromPassword(
  password: string,
  salt: Uint8Array
): Promise<Uint8Array> {
  const encoder = new TextEncoder();
  const passwordBuffer = encoder.encode(password);
  
  // Use Web Crypto API for PBKDF2
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    passwordBuffer,
    'PBKDF2',
    false,
    ['deriveBits']
  );
  
  const derivedBits = await crypto.subtle.deriveBits(
    {
      name: 'PBKDF2',
      salt: salt,
      iterations: 100000,
      hash: 'SHA-256',
    },
    keyMaterial,
    256 // 32 bytes for NaCl secretbox
  );
  
  return new Uint8Array(derivedBits);
}

// ─────────────────────────────────────────────────────────────────────────────
// IDENTITY STORAGE (secure local storage)
// ─────────────────────────────────────────────────────────────────────────────

const STORAGE_KEY = 'atom_identity_encrypted';
const SALT_KEY = 'atom_identity_salt';

export async function saveIdentitySecurely(
  identity: SplitIdentity,
  password: string
): Promise<boolean> {
  try {
    // Generate or retrieve salt
    let salt = localStorage.getItem(SALT_KEY);
    let saltBytes: Uint8Array;
    
    if (!salt) {
      saltBytes = generateRandomBytes(16);
      localStorage.setItem(SALT_KEY, encodeBase64(saltBytes));
    } else {
      saltBytes = decodeBase64(salt);
    }
    
    // Derive encryption key from password
    const key = await deriveKeyFromPassword(password, saltBytes);
    
    // Serialize identity (excluding functions)
    const identityData = JSON.stringify({
      publicId: identity.publicId,
      privateKey: encodeBase64(identity.privateKey),
      publicKey: encodeBase64(identity.publicKey),
      createdAt: identity.createdAt.toISOString(),
      lastAccess: new Date().toISOString(),
      recoverySetup: identity.recoverySetup,
    });
    
    // Encrypt and store
    const encrypted = encryptSymmetric(identityData, key);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(encrypted));
    
    return true;
  } catch (error) {
    console.error('Failed to save identity:', error);
    return false;
  }
}

export async function loadIdentitySecurely(
  password: string
): Promise<SplitIdentity | null> {
  try {
    const encryptedStr = localStorage.getItem(STORAGE_KEY);
    const saltStr = localStorage.getItem(SALT_KEY);
    
    if (!encryptedStr || !saltStr) return null;
    
    const saltBytes = decodeBase64(saltStr);
    const key = await deriveKeyFromPassword(password, saltBytes);
    const encrypted = JSON.parse(encryptedStr) as EncryptedPayload;
    
    const decrypted = decryptSymmetric(encrypted, key);
    if (!decrypted) return null;
    
    const data = JSON.parse(decrypted);
    
    return {
      publicId: data.publicId,
      privateKey: decodeBase64(data.privateKey),
      publicKey: decodeBase64(data.publicKey),
      createdAt: new Date(data.createdAt),
      lastAccess: new Date(),
      recoverySetup: data.recoverySetup,
    };
  } catch (error) {
    console.error('Failed to load identity:', error);
    return null;
  }
}

export function clearStoredIdentity(): void {
  localStorage.removeItem(STORAGE_KEY);
  localStorage.removeItem(SALT_KEY);
}

export function hasStoredIdentity(): boolean {
  return localStorage.getItem(STORAGE_KEY) !== null;
}

// ─────────────────────────────────────────────────────────────────────────────
// UTILITY EXPORTS
// ─────────────────────────────────────────────────────────────────────────────

export const EncryptionService = {
  // Key generation
  generateKeyPair,
  generateSigningKeyPair,
  generateRandomBytes,
  
  // Identity
  createSplitIdentity,
  
  // Encryption
  encryptSymmetric,
  decryptSymmetric,
  encryptAsymmetric,
  decryptAsymmetric,
  
  // Signing
  signMessage,
  verifySignature,
  
  // Key derivation
  deriveKeyFromPassword,
  
  // Storage
  saveIdentitySecurely,
  loadIdentitySecurely,
  clearStoredIdentity,
  hasStoredIdentity,
  
  // Base64 utilities
  encodeBase64,
  decodeBase64,
};

export default EncryptionService;
