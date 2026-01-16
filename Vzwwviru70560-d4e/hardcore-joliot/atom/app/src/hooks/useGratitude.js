/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *      ██╗   ██╗███████╗███████╗ ██████╗ ██████╗  █████╗ ████████╗██╗████████╗██╗   ██╗██████╗ ███████╗
 *      ██║   ██║██╔════╝██╔════╝██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
 *      ██║   ██║███████╗█████╗  ██║  ███╗██████╔╝███████║   ██║   ██║   ██║   ██║   ██║██║  ██║█████╗
 *      ██║   ██║╚════██║██╔══╝  ██║   ██║██╔══██╗██╔══██║   ██║   ██║   ██║   ██║   ██║██║  ██║██╔══╝
 *      ╚██████╔╝███████║███████╗╚██████╔╝██║  ██║██║  ██║   ██║   ██║   ██║   ╚██████╔╝██████╔╝███████╗
 *       ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝
 *
 *                                    HOOK GRATITUDE
 *                              Mode de reconnaissance divine
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *   Fonctionnalités:
 *   - Activation du mode Gratitude par pression longue (3 secondes)
 *   - Barre de progression visuelle
 *   - Auto-désactivation après 10 secondes
 *   - Gestionnaires tactiles et souris
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { useState, useCallback, useRef, useEffect } from 'react';

/**
 * Hook pour activer le Mode Gratitude par pression longue
 *
 * @param {Function} onGratitudeActivate - Callback appelé lors de l'activation
 * @param {number} delay - Durée de pression requise en ms (défaut: 3000)
 * @returns {Object} États et gestionnaires d'événements
 */
export const useGratitude = (onGratitudeActivate, delay = 3000) => {
  const [isPressed, setIsPressed] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isGratitudeMode, setIsGratitudeMode] = useState(false);
  const timerRef = useRef(null);
  const intervalRef = useRef(null);

  /**
   * Démarre le compteur de pression longue
   */
  const startPress = useCallback(() => {
    setIsPressed(true);
    setProgress(0);

    const startTime = Date.now();

    // Mise à jour du progress bar
    intervalRef.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min((elapsed / delay) * 100, 100);
      setProgress(newProgress);
    }, 50);

    // Timer pour activer le mode gratitude
    timerRef.current = setTimeout(() => {
      setIsGratitudeMode(true);
      setProgress(100);

      if (onGratitudeActivate) {
        onGratitudeActivate();
      }

      // Auto-désactivation après 10 secondes
      setTimeout(() => {
        setIsGratitudeMode(false);
      }, 10000);
    }, delay);
  }, [delay, onGratitudeActivate]);

  /**
   * Termine la pression et réinitialise
   */
  const endPress = useCallback(() => {
    setIsPressed(false);
    setProgress(0);

    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }

    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  /**
   * Active manuellement le mode gratitude
   */
  const activateGratitude = useCallback(() => {
    setIsGratitudeMode(true);

    if (onGratitudeActivate) {
      onGratitudeActivate();
    }

    // Auto-désactivation après 10 secondes
    setTimeout(() => {
      setIsGratitudeMode(false);
    }, 10000);
  }, [onGratitudeActivate]);

  /**
   * Désactive manuellement le mode gratitude
   */
  const deactivateGratitude = useCallback(() => {
    setIsGratitudeMode(false);
  }, []);

  // Nettoyage des timers au démontage
  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  return {
    // États
    isPressed,
    progress,
    isGratitudeMode,

    // Actions manuelles
    setIsGratitudeMode,
    activateGratitude,
    deactivateGratitude,

    // Gestionnaires d'événements pour composants
    handlers: {
      onMouseDown: startPress,
      onMouseUp: endPress,
      onMouseLeave: endPress,
      onTouchStart: startPress,
      onTouchEnd: endPress
    }
  };
};

export default useGratitude;
