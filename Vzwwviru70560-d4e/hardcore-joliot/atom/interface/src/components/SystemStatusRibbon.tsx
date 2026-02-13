/**
 * SYSTEM STATUS RIBBON - Visible System State
 * ============================================
 *
 * Ruban persistant affichant l'état du système:
 * - Normal: pas d'affichage (ou discret)
 * - Beta: bandeau informatif
 * - Dégradé: avertissement avec détails
 * - Simulation: indication claire
 * - Maintenance: alerte avec temps estimé
 *
 * Objectif: Transparence totale sur l'état du système
 */

import React, { useState, useEffect } from 'react';
import { SYSTEM_STATUS, FEATURES } from '@/constants/product.constants';
import { COLORS, TYPOGRAPHY } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

type RibbonType = 'info' | 'warning' | 'error' | 'success' | 'simulation';

interface RibbonConfig {
  type: RibbonType;
  message: string;
  dismissable: boolean;
  action?: {
    label: string;
    onClick: () => void;
  };
}

// =============================================================================
// STATUS COLORS
// =============================================================================

const RIBBON_COLORS: Record<RibbonType, { bg: string; border: string; text: string }> = {
  info: {
    bg: 'rgba(0, 71, 171, 0.15)',
    border: 'rgba(0, 71, 171, 0.3)',
    text: '#5B9BD5',
  },
  warning: {
    bg: 'rgba(243, 156, 18, 0.15)',
    border: 'rgba(243, 156, 18, 0.3)',
    text: '#F39C12',
  },
  error: {
    bg: 'rgba(231, 76, 60, 0.15)',
    border: 'rgba(231, 76, 60, 0.3)',
    text: '#E74C3C',
  },
  success: {
    bg: 'rgba(39, 174, 96, 0.15)',
    border: 'rgba(39, 174, 96, 0.3)',
    text: '#27AE60',
  },
  simulation: {
    bg: 'rgba(142, 68, 173, 0.15)',
    border: 'rgba(142, 68, 173, 0.3)',
    text: '#9B59B6',
  },
};

// =============================================================================
// SYSTEM STATUS RIBBON COMPONENT
// =============================================================================

interface SystemStatusRibbonProps {
  forceShow?: boolean;
  customMessage?: string;
  customType?: RibbonType;
}

export function SystemStatusRibbon({
  forceShow = false,
  customMessage,
  customType,
}: SystemStatusRibbonProps) {
  const [isDismissed, setIsDismissed] = useState(false);
  const [currentConfig, setCurrentConfig] = useState<RibbonConfig | null>(null);

  useEffect(() => {
    // Check session storage for dismissed state
    const dismissedKey = `atom_ribbon_dismissed_${SYSTEM_STATUS.currentMode}`;
    const wasDismissed = sessionStorage.getItem(dismissedKey) === 'true';
    setIsDismissed(wasDismissed);

    // Determine ribbon config based on system status
    const config = getRibbonConfig();
    setCurrentConfig(config);
  }, []);

  const getRibbonConfig = (): RibbonConfig | null => {
    // Custom message takes priority
    if (customMessage) {
      return {
        type: customType || 'info',
        message: customMessage,
        dismissable: true,
      };
    }

    // System mode based config
    switch (SYSTEM_STATUS.currentMode) {
      case 'beta':
        return {
          type: 'info',
          message: SYSTEM_STATUS.messages.beta || 'Version bêta',
          dismissable: true,
        };

      case 'simulation':
        return {
          type: 'simulation',
          message: SYSTEM_STATUS.messages.simulation || 'Mode simulation actif',
          dismissable: false,
          action: {
            label: 'En savoir plus',
            onClick: () => {
              // Could open a modal or navigate to documentation
              console.log('Simulation mode info requested');
            },
          },
        };

      case 'maintenance':
        return {
          type: 'warning',
          message: SYSTEM_STATUS.messages.maintenance || 'Maintenance en cours',
          dismissable: false,
        };

      case 'production':
      default:
        return null; // No ribbon in production unless forced
    }
  };

  const handleDismiss = () => {
    const dismissedKey = `atom_ribbon_dismissed_${SYSTEM_STATUS.currentMode}`;
    sessionStorage.setItem(dismissedKey, 'true');
    setIsDismissed(true);
  };

  // Don't show if feature disabled
  if (!FEATURES.showSystemStatus && !forceShow) {
    return null;
  }

  // Don't show if dismissed or no config
  if ((isDismissed && currentConfig?.dismissable) || !currentConfig) {
    return null;
  }

  const colors = RIBBON_COLORS[currentConfig.type];

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 9999,
        backgroundColor: colors.bg,
        borderBottom: `1px solid ${colors.border}`,
        padding: '8px 16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '16px',
        fontFamily: TYPOGRAPHY.fontFamily.system,
      }}
      role="banner"
      aria-live="polite"
    >
      {/* Status indicator */}
      <span
        style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          backgroundColor: colors.text,
          flexShrink: 0,
        }}
      />

      {/* Message */}
      <span
        style={{
          color: colors.text,
          fontSize: '13px',
          fontWeight: 500,
        }}
      >
        {currentConfig.message}
      </span>

      {/* Action button */}
      {currentConfig.action && (
        <button
          onClick={currentConfig.action.onClick}
          style={{
            padding: '4px 12px',
            backgroundColor: 'transparent',
            border: `1px solid ${colors.text}`,
            borderRadius: '4px',
            color: colors.text,
            fontSize: '12px',
            cursor: 'pointer',
            fontWeight: 500,
          }}
        >
          {currentConfig.action.label}
        </button>
      )}

      {/* Dismiss button */}
      {currentConfig.dismissable && (
        <button
          onClick={handleDismiss}
          style={{
            padding: '4px 8px',
            backgroundColor: 'transparent',
            border: 'none',
            color: colors.text,
            fontSize: '16px',
            cursor: 'pointer',
            opacity: 0.7,
            marginLeft: 'auto',
          }}
          aria-label="Fermer"
        >
          ×
        </button>
      )}
    </div>
  );
}

// =============================================================================
// DEGRADED STATUS RIBBON
// =============================================================================

interface DegradedStatusRibbonProps {
  services: Array<{
    name: string;
    status: 'operational' | 'degraded' | 'down';
  }>;
  onRetry?: () => void;
}

export function DegradedStatusRibbon({ services, onRetry }: DegradedStatusRibbonProps) {
  const degradedServices = services.filter(s => s.status !== 'operational');

  if (degradedServices.length === 0) {
    return null;
  }

  const isDown = degradedServices.some(s => s.status === 'down');
  const colors = RIBBON_COLORS[isDown ? 'error' : 'warning'];

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 9999,
        backgroundColor: colors.bg,
        borderBottom: `1px solid ${colors.border}`,
        padding: '10px 16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '16px',
        fontFamily: TYPOGRAPHY.fontFamily.system,
      }}
      role="alert"
    >
      <span
        style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          backgroundColor: colors.text,
          animation: 'pulse 2s infinite',
        }}
      />

      <span style={{ color: colors.text, fontSize: '13px' }}>
        {isDown ? 'Service indisponible' : 'Services ralentis'}
        {' — '}
        {degradedServices.map(s => s.name).join(', ')}
      </span>

      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            padding: '4px 12px',
            backgroundColor: colors.text,
            border: 'none',
            borderRadius: '4px',
            color: '#fff',
            fontSize: '12px',
            cursor: 'pointer',
            fontWeight: 500,
          }}
        >
          Réessayer
        </button>
      )}

      <span style={{ color: colors.text, fontSize: '12px', opacity: 0.8 }}>
        Vos actions sont sauvegardées localement
      </span>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}

export default SystemStatusRibbon;
