// ═══════════════════════════════════════════════════════════════════════════
// AT·OM INTERFACE - CUSTOM HOOKS
// ═══════════════════════════════════════════════════════════════════════════

import { useState, useEffect, useCallback, useRef } from 'react';
import { useAtomStore } from '@/stores/atom.store';
import { OfflineService } from '@/services/offline.service';
import { heartbeatService, arithmosService } from '@/services/realtime.service';
import type { SphereId, HeartbeatState, ArithmosState } from '@/types';

// ─────────────────────────────────────────────────────────────────────────────
// useOnlineStatus - Track network status
// ─────────────────────────────────────────────────────────────────────────────

export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const unsubscribe = OfflineService.onNetworkChange(setIsOnline);
    return unsubscribe;
  }, []);

  return isOnline;
}

// ─────────────────────────────────────────────────────────────────────────────
// useHeartbeat - Subscribe to heartbeat service
// ─────────────────────────────────────────────────────────────────────────────

export function useHeartbeat() {
  const [state, setState] = useState<HeartbeatState>(heartbeatService.getState());

  useEffect(() => {
    const unsubscribe = heartbeatService.subscribe(setState);
    return unsubscribe;
  }, []);

  return state;
}

// ─────────────────────────────────────────────────────────────────────────────
// useArithmos - Subscribe to Arithmos engine
// ─────────────────────────────────────────────────────────────────────────────

export function useArithmos() {
  const [state, setState] = useState<ArithmosState>(arithmosService.getState());

  useEffect(() => {
    const unsubscribe = arithmosService.subscribe(setState);
    return unsubscribe;
  }, []);

  const recalculate = useCallback(async () => {
    return arithmosService.recalculate();
  }, []);

  return { ...state, recalculate };
}

// ─────────────────────────────────────────────────────────────────────────────
// useSphere - Get sphere data with balance
// ─────────────────────────────────────────────────────────────────────────────

export function useSphereData(sphereId: SphereId) {
  const sphere = useAtomStore((state) => state.spheres[sphereId]);
  const balance = useAtomStore((state) => state.arithmos.sphereBalances[sphereId] ?? 0);
  const heartbeatStatus = useAtomStore((state) => state.heartbeat.sphereStatus[sphereId]);

  return {
    sphere,
    balance,
    heartbeatStatus,
    isHealthy: sphere.stability >= 70 && sphere.efficiency >= 70,
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// useLocalStorage - Persistent state with localStorage
// ─────────────────────────────────────────────────────────────────────────────

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`[useLocalStorage] Error setting ${key}:`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// ─────────────────────────────────────────────────────────────────────────────
// useDebounce - Debounce a value
// ─────────────────────────────────────────────────────────────────────────────

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// ─────────────────────────────────────────────────────────────────────────────
// useThrottle - Throttle a callback
// ─────────────────────────────────────────────────────────────────────────────

export function useThrottle<T extends (...args: any[]) => any>(
  callback: T,
  delay: number = 200
) {
  const lastRun = useRef(Date.now());
  const timeoutRef = useRef<NodeJS.Timeout>();

  return useCallback(
    (...args: Parameters<T>) => {
      const now = Date.now();
      const timeSinceLastRun = now - lastRun.current;

      if (timeSinceLastRun >= delay) {
        lastRun.current = now;
        callback(...args);
      } else {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = setTimeout(() => {
          lastRun.current = Date.now();
          callback(...args);
        }, delay - timeSinceLastRun);
      }
    },
    [callback, delay]
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// useMediaQuery - Responsive design helper
// ─────────────────────────────────────────────────────────────────────────────

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => {
    if (typeof window === 'undefined') return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// Preset breakpoints
export const useIsMobile = () => useMediaQuery('(max-width: 640px)');
export const useIsTablet = () => useMediaQuery('(min-width: 641px) and (max-width: 1024px)');
export const useIsDesktop = () => useMediaQuery('(min-width: 1025px)');

// ─────────────────────────────────────────────────────────────────────────────
// useInterval - Declarative interval
// ─────────────────────────────────────────────────────────────────────────────

export function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}

// ─────────────────────────────────────────────────────────────────────────────
// useKeyPress - Keyboard shortcut handler
// ─────────────────────────────────────────────────────────────────────────────

export function useKeyPress(
  targetKey: string,
  handler: () => void,
  options: { ctrl?: boolean; shift?: boolean; alt?: boolean } = {}
) {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key.toLowerCase() !== targetKey.toLowerCase()) return;
      if (options.ctrl && !event.ctrlKey && !event.metaKey) return;
      if (options.shift && !event.shiftKey) return;
      if (options.alt && !event.altKey) return;

      event.preventDefault();
      handler();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [targetKey, handler, options.ctrl, options.shift, options.alt]);
}

// ─────────────────────────────────────────────────────────────────────────────
// usePendingSync - Track offline pending operations
// ─────────────────────────────────────────────────────────────────────────────

export function usePendingSync() {
  const [pendingCount, setPendingCount] = useState(0);
  const [isSyncing, setIsSyncing] = useState(false);

  useEffect(() => {
    const updateCount = async () => {
      const count = await OfflineService.getPendingCount();
      setPendingCount(count);
    };

    updateCount();
    const interval = setInterval(updateCount, 5000);
    return () => clearInterval(interval);
  }, []);

  const sync = useCallback(async () => {
    setIsSyncing(true);
    try {
      const result = await OfflineService.syncPendingOperations();
      const newCount = await OfflineService.getPendingCount();
      setPendingCount(newCount);
      return result;
    } finally {
      setIsSyncing(false);
    }
  }, []);

  return { pendingCount, isSyncing, sync };
}

// ─────────────────────────────────────────────────────────────────────────────
// useClickOutside - Detect clicks outside element
// ─────────────────────────────────────────────────────────────────────────────

export function useClickOutside<T extends HTMLElement>(
  handler: () => void
): React.RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const handleClick = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        handler();
      }
    };

    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [handler]);

  return ref;
}

// ─────────────────────────────────────────────────────────────────────────────
// useAsync - Async operation state management
// ─────────────────────────────────────────────────────────────────────────────

interface AsyncState<T> {
  status: 'idle' | 'loading' | 'success' | 'error';
  data: T | null;
  error: Error | null;
}

export function useAsync<T>() {
  const [state, setState] = useState<AsyncState<T>>({
    status: 'idle',
    data: null,
    error: null,
  });

  const execute = useCallback(async (asyncFn: () => Promise<T>) => {
    setState({ status: 'loading', data: null, error: null });
    try {
      const data = await asyncFn();
      setState({ status: 'success', data, error: null });
      return data;
    } catch (error) {
      setState({ status: 'error', data: null, error: error as Error });
      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({ status: 'idle', data: null, error: null });
  }, []);

  return { ...state, execute, reset };
}

// ─────────────────────────────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────────────────────────────

export default {
  useOnlineStatus,
  useHeartbeat,
  useArithmos,
  useSphereData,
  useLocalStorage,
  useDebounce,
  useThrottle,
  useMediaQuery,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  useInterval,
  useKeyPress,
  usePendingSync,
  useClickOutside,
  useAsync,
};
