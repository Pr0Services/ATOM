/**
 * SERVICE HEALTH WIDGET - Visible Service Status
 * ===============================================
 *
 * Widget affichant l'état des services en temps réel:
 * - Status API
 * - Status Agents
 * - Status Base de données
 * - Status Blockchain (Hedera)
 *
 * Objectif: Traduire la robustesse technique en confiance UX
 */

import React, { useState, useEffect, useCallback } from 'react';
import { COLORS, TYPOGRAPHY } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

export interface ServiceHealth {
  id: string;
  name: string;
  status: 'operational' | 'degraded' | 'down' | 'unknown';
  latency?: number;
  lastChecked?: Date;
  message?: string;
}

interface HealthCheckResponse {
  status: 'ok' | 'degraded' | 'error';
  services: {
    [key: string]: {
      status: string;
      latency?: number;
      message?: string;
    };
  };
  timestamp: string;
}

// =============================================================================
// STATUS CONFIG
// =============================================================================

const STATUS_CONFIG = {
  operational: {
    color: '#27AE60',
    label: 'Opérationnel',
    icon: '●',
  },
  degraded: {
    color: '#F39C12',
    label: 'Dégradé',
    icon: '◐',
  },
  down: {
    color: '#E74C3C',
    label: 'Indisponible',
    icon: '○',
  },
  unknown: {
    color: 'rgba(255, 255, 255, 0.3)',
    label: 'Inconnu',
    icon: '?',
  },
};

const DEFAULT_SERVICES: ServiceHealth[] = [
  { id: 'api', name: 'API', status: 'unknown' },
  { id: 'agents', name: 'Agents IA', status: 'unknown' },
  { id: 'database', name: 'Base de données', status: 'unknown' },
  { id: 'storage', name: 'Stockage', status: 'unknown' },
];

// =============================================================================
// HEALTH CHECK SERVICE
// =============================================================================

async function checkServiceHealth(): Promise<ServiceHealth[]> {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/health`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      signal: AbortSignal.timeout(5000),
    });

    if (!response.ok) {
      throw new Error('Health check failed');
    }

    const data: HealthCheckResponse = await response.json();

    return Object.entries(data.services).map(([id, service]) => ({
      id,
      name: id.charAt(0).toUpperCase() + id.slice(1),
      status: service.status === 'ok' ? 'operational' :
              service.status === 'degraded' ? 'degraded' : 'down',
      latency: service.latency,
      message: service.message,
      lastChecked: new Date(data.timestamp),
    }));
  } catch (error) {
    // Return simulated "operational" status in dev mode
    if (import.meta.env.DEV) {
      return DEFAULT_SERVICES.map(s => ({
        ...s,
        status: 'operational' as const,
        latency: Math.floor(Math.random() * 100) + 20,
        lastChecked: new Date(),
      }));
    }
    return DEFAULT_SERVICES.map(s => ({ ...s, status: 'unknown' as const }));
  }
}

// =============================================================================
// SERVICE HEALTH WIDGET COMPONENT
// =============================================================================

interface ServiceHealthWidgetProps {
  compact?: boolean;
  showLatency?: boolean;
  refreshInterval?: number; // ms
  onStatusChange?: (services: ServiceHealth[]) => void;
}

export function ServiceHealthWidget({
  compact = false,
  showLatency = true,
  refreshInterval = 60000, // 1 minute
  onStatusChange,
}: ServiceHealthWidgetProps) {
  const [services, setServices] = useState<ServiceHealth[]>(DEFAULT_SERVICES);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [expanded, setExpanded] = useState(false);

  const refreshHealth = useCallback(async () => {
    setIsRefreshing(true);
    const health = await checkServiceHealth();
    setServices(health);
    setLastUpdate(new Date());
    setIsRefreshing(false);
    onStatusChange?.(health);
  }, [onStatusChange]);

  useEffect(() => {
    refreshHealth();
    const interval = setInterval(refreshHealth, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshHealth, refreshInterval]);

  const overallStatus = services.every(s => s.status === 'operational')
    ? 'operational'
    : services.some(s => s.status === 'down')
      ? 'down'
      : services.some(s => s.status === 'degraded')
        ? 'degraded'
        : 'unknown';

  const statusConfig = STATUS_CONFIG[overallStatus];

  // Compact badge version
  if (compact) {
    return (
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          padding: '6px 12px',
          backgroundColor: 'rgba(0, 0, 0, 0.3)',
          border: `1px solid ${statusConfig.color}30`,
          borderRadius: '20px',
          cursor: 'pointer',
        }}
        onClick={() => setExpanded(!expanded)}
        title={`Services: ${statusConfig.label}`}
      >
        <span style={{ color: statusConfig.color, fontSize: '10px' }}>
          {statusConfig.icon}
        </span>
        <span style={{
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: '12px',
          fontFamily: TYPOGRAPHY.fontFamily.mono,
        }}>
          {overallStatus === 'operational' ? 'Tous les services OK' : statusConfig.label}
        </span>
        {isRefreshing && (
          <span style={{
            color: 'rgba(255, 255, 255, 0.3)',
            fontSize: '10px',
            animation: 'spin 1s linear infinite',
          }}>
            ↻
          </span>
        )}
      </div>
    );
  }

  // Full widget version
  return (
    <div style={{
      padding: '20px',
      backgroundColor: 'rgba(0, 0, 0, 0.3)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '12px',
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '16px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{
            color: statusConfig.color,
            fontSize: '16px',
          }}>
            {statusConfig.icon}
          </span>
          <h3 style={{
            color: '#fff',
            fontSize: '16px',
            fontWeight: 600,
            margin: 0,
          }}>
            État des Services
          </h3>
        </div>
        <button
          onClick={refreshHealth}
          disabled={isRefreshing}
          style={{
            padding: '4px 12px',
            backgroundColor: 'transparent',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '4px',
            color: 'rgba(255, 255, 255, 0.5)',
            fontSize: '12px',
            cursor: isRefreshing ? 'wait' : 'pointer',
            opacity: isRefreshing ? 0.5 : 1,
          }}
        >
          {isRefreshing ? '↻' : 'Rafraîchir'}
        </button>
      </div>

      {/* Overall Status Banner */}
      <div style={{
        padding: '12px 16px',
        backgroundColor: `${statusConfig.color}10`,
        border: `1px solid ${statusConfig.color}30`,
        borderRadius: '8px',
        marginBottom: '16px',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <span style={{ color: statusConfig.color, fontWeight: 500 }}>
            {statusConfig.label}
          </span>
          {lastUpdate && (
            <span style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '12px' }}>
              Mis à jour il y a {Math.round((Date.now() - lastUpdate.getTime()) / 1000)}s
            </span>
          )}
        </div>
        {overallStatus !== 'operational' && (
          <p style={{
            color: 'rgba(255, 255, 255, 0.6)',
            fontSize: '13px',
            margin: '8px 0 0 0',
          }}>
            {overallStatus === 'degraded'
              ? 'Certains services peuvent être plus lents que d\'habitude.'
              : overallStatus === 'down'
                ? 'Nous travaillons à rétablir le service. Veuillez réessayer dans quelques minutes.'
                : 'Vérification de l\'état des services en cours...'}
          </p>
        )}
      </div>

      {/* Services List */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
      }}>
        {services.map((service) => {
          const config = STATUS_CONFIG[service.status];
          return (
            <div
              key={service.id}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '10px 12px',
                backgroundColor: 'rgba(255, 255, 255, 0.02)',
                borderRadius: '6px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ color: config.color, fontSize: '12px' }}>
                  {config.icon}
                </span>
                <span style={{ color: '#fff', fontSize: '14px' }}>
                  {service.name}
                </span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                {showLatency && service.latency !== undefined && (
                  <span style={{
                    color: service.latency > 200
                      ? '#F39C12'
                      : 'rgba(255, 255, 255, 0.4)',
                    fontSize: '12px',
                    fontFamily: TYPOGRAPHY.fontFamily.mono,
                  }}>
                    {service.latency}ms
                  </span>
                )}
                <span style={{
                  color: config.color,
                  fontSize: '12px',
                }}>
                  {config.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Degradation Message */}
      {overallStatus !== 'operational' && (
        <div style={{
          marginTop: '16px',
          padding: '12px',
          backgroundColor: 'rgba(255, 255, 255, 0.02)',
          borderRadius: '6px',
          borderLeft: `3px solid ${statusConfig.color}`,
        }}>
          <p style={{
            color: 'rgba(255, 255, 255, 0.7)',
            fontSize: '13px',
            margin: 0,
            lineHeight: 1.5,
          }}>
            <strong>En attendant:</strong> Vos actions sont mises en file d'attente
            et seront traitées automatiquement dès que le service sera rétabli.
          </p>
        </div>
      )}

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

// =============================================================================
// FLOATING STATUS INDICATOR
// =============================================================================

export function FloatingHealthIndicator() {
  const [services, setServices] = useState<ServiceHealth[]>(DEFAULT_SERVICES);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    const check = async () => {
      const health = await checkServiceHealth();
      setServices(health);
    };
    check();
    const interval = setInterval(check, 60000);
    return () => clearInterval(interval);
  }, []);

  const overallStatus = services.every(s => s.status === 'operational')
    ? 'operational'
    : services.some(s => s.status === 'down')
      ? 'down'
      : services.some(s => s.status === 'degraded')
        ? 'degraded'
        : 'unknown';

  // Only show if not operational
  if (overallStatus === 'operational') {
    return null;
  }

  const config = STATUS_CONFIG[overallStatus];

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      left: '20px',
      zIndex: 1000,
    }}>
      <button
        onClick={() => setShowDetails(!showDetails)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '12px 16px',
          backgroundColor: 'rgba(0, 0, 0, 0.9)',
          border: `1px solid ${config.color}`,
          borderRadius: '8px',
          cursor: 'pointer',
          boxShadow: `0 0 20px ${config.color}40`,
        }}
      >
        <span style={{ color: config.color, fontSize: '14px' }}>{config.icon}</span>
        <span style={{ color: '#fff', fontSize: '14px' }}>
          {overallStatus === 'degraded' ? 'Services ralentis' : 'Problème de service'}
        </span>
      </button>

      {showDetails && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: 0,
          marginBottom: '12px',
          width: '300px',
        }}>
          <ServiceHealthWidget compact={false} showLatency={true} />
        </div>
      )}
    </div>
  );
}

export default ServiceHealthWidget;
