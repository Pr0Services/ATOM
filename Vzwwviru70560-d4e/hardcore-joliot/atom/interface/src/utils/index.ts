// ═══════════════════════════════════════════════════════════════════════════
// AT·OM INTERFACE - UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import type { SphereId } from '@/types';

// ─────────────────────────────────────────────────────────────────────────────
// CLASS NAME UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Merge Tailwind CSS classes with conflict resolution
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// ─────────────────────────────────────────────────────────────────────────────
// DATE & TIME UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Format date relative to now (e.g., "il y a 5 minutes")
 */
export function formatRelativeTime(date: Date | string | number): string {
  const d = new Date(date);
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  
  if (seconds < 60) return 'à l\'instant';
  if (minutes < 60) return `il y a ${minutes} minute${minutes > 1 ? 's' : ''}`;
  if (hours < 24) return `il y a ${hours} heure${hours > 1 ? 's' : ''}`;
  if (days < 7) return `il y a ${days} jour${days > 1 ? 's' : ''}`;
  
  return d.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: d.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
  });
}

/**
 * Format date in French locale
 */
export function formatDate(date: Date | string | number, options?: Intl.DateTimeFormatOptions): string {
  return new Date(date).toLocaleDateString('fr-FR', options ?? {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

/**
 * Format time
 */
export function formatTime(date: Date | string | number): string {
  return new Date(date).toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// NUMBER UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Format number with thousand separators
 */
export function formatNumber(num: number, decimals: number = 0): string {
  return num.toLocaleString('fr-FR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * Format percentage
 */
export function formatPercent(value: number, decimals: number = 0): string {
  return `${formatNumber(value, decimals)}%`;
}

/**
 * Format bytes to human readable
 */
export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}

/**
 * Clamp a number between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

// ─────────────────────────────────────────────────────────────────────────────
// STRING UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3) + '...';
}

/**
 * Capitalize first letter
 */
export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

/**
 * Generate initials from name
 */
export function getInitials(name: string): string {
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

/**
 * Slugify a string
 */
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

// ─────────────────────────────────────────────────────────────────────────────
// COLOR UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Get stability color based on value
 */
export function getStabilityColor(value: number): string {
  if (value >= 80) return '#22c55e'; // Green
  if (value >= 60) return '#84cc16'; // Lime
  if (value >= 40) return '#eab308'; // Yellow
  if (value >= 20) return '#f97316'; // Orange
  return '#ef4444'; // Red
}

/**
 * Get stability level name
 */
export function getStabilityLevel(value: number): string {
  if (value >= 80) return 'optimal';
  if (value >= 60) return 'bon';
  if (value >= 40) return 'modéré';
  if (value >= 20) return 'faible';
  return 'critique';
}

/**
 * Sphere colors
 */
export const SPHERE_COLORS: Record<SphereId, string> = {
  health: '#10b981',
  finance: '#f59e0b',
  education: '#8b5cf6',
  governance: '#3b82f6',
  energy: '#ef4444',
  communication: '#06b6d4',
  justice: '#6366f1',
  logistics: '#f97316',
  food: '#22c55e',
  technology: '#a855f7',
};

/**
 * Hex to RGB
 */
export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

/**
 * Get contrasting text color (black or white)
 */
export function getContrastColor(hexColor: string): string {
  const rgb = hexToRgb(hexColor);
  if (!rgb) return '#ffffff';
  
  const luminance = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b) / 255;
  return luminance > 0.5 ? '#000000' : '#ffffff';
}

// ─────────────────────────────────────────────────────────────────────────────
// ARRAY UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Group array by key
 */
export function groupBy<T>(array: T[], key: keyof T): Record<string, T[]> {
  return array.reduce((result, item) => {
    const groupKey = String(item[key]);
    (result[groupKey] = result[groupKey] || []).push(item);
    return result;
  }, {} as Record<string, T[]>);
}

/**
 * Remove duplicates from array
 */
export function unique<T>(array: T[]): T[] {
  return [...new Set(array)];
}

/**
 * Sort array by key
 */
export function sortBy<T>(array: T[], key: keyof T, direction: 'asc' | 'desc' = 'asc'): T[] {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    
    if (aVal < bVal) return direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return direction === 'asc' ? 1 : -1;
    return 0;
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// OBJECT UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Deep clone an object
 */
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Check if object is empty
 */
export function isEmpty(obj: object): boolean {
  return Object.keys(obj).length === 0;
}

/**
 * Pick specific keys from object
 */
export function pick<T extends object, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  return keys.reduce((result, key) => {
    if (key in obj) result[key] = obj[key];
    return result;
  }, {} as Pick<T, K>);
}

/**
 * Omit specific keys from object
 */
export function omit<T extends object, K extends keyof T>(obj: T, keys: K[]): Omit<T, K> {
  const result = { ...obj };
  keys.forEach(key => delete result[key]);
  return result;
}

// ─────────────────────────────────────────────────────────────────────────────
// VALIDATION UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/**
 * Validate URL format
 */
export function isValidUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// ASYNC UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Sleep for specified milliseconds
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Retry an async function
 */
export async function retry<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  delayMs: number = 1000
): Promise<T> {
  let lastError: Error | undefined;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxAttempts) {
        await sleep(delayMs * attempt);
      }
    }
  }
  
  throw lastError;
}

/**
 * Debounce a function
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

/**
 * Throttle a function
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false;
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// ID GENERATION
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Generate UUID v4
 */
export function uuid(): string {
  return crypto.randomUUID();
}

/**
 * Generate short ID
 */
export function shortId(length: number = 8): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// ─────────────────────────────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────────────────────────────

export default {
  // Class names
  cn,
  
  // Date/Time
  formatRelativeTime,
  formatDate,
  formatTime,
  
  // Numbers
  formatNumber,
  formatPercent,
  formatBytes,
  clamp,
  
  // Strings
  truncate,
  capitalize,
  getInitials,
  slugify,
  
  // Colors
  getStabilityColor,
  getStabilityLevel,
  SPHERE_COLORS,
  hexToRgb,
  getContrastColor,
  
  // Arrays
  groupBy,
  unique,
  sortBy,
  
  // Objects
  deepClone,
  isEmpty,
  pick,
  omit,
  
  // Validation
  isValidEmail,
  isValidUrl,
  
  // Async
  sleep,
  retry,
  debounce,
  throttle,
  
  // IDs
  uuid,
  shortId,
};
