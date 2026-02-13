/**
 * ANALYTICS DASHBOARD - Tableau de bord funnel
 * =============================================
 *
 * Dashboard admin pour visualiser:
 * - Funnel de conversion (5 étapes)
 * - Taux de conversion entre étapes
 * - Sessions actives
 * - Métriques temps réel
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { COLORS, TYPOGRAPHY, TOUCH } from '@/styles/tokens';
import { Breadcrumbs } from '@/components/Breadcrumbs';

// =============================================================================
// TYPES
// =============================================================================

interface FunnelStep {
  name: string;
  label: string;
  count: number;
  conversionRate: number;
  avgDuration: number; // seconds
}

interface SessionStat {
  sessionId: string;
  eventsCount: number;
  funnelProgress: number;
  lastActivity: string;
  source: string;
}

interface DashboardStats {
  totalSessions: number;
  activeSessions: number;
  totalEvents: number;
  avgFunnelProgress: number;
  topSources: { name: string; count: number }[];
}

// =============================================================================
// MOCK DATA (will be replaced by API calls)
// =============================================================================

const MOCK_FUNNEL: FunnelStep[] = [
  { name: 'landing_view', label: 'Landing View', count: 1247, conversionRate: 100, avgDuration: 0 },
  { name: 'cta_click', label: 'CTA Click', count: 834, conversionRate: 66.9, avgDuration: 12 },
  { name: 'sceau_activate', label: 'Sceau Activated', count: 621, conversionRate: 74.5, avgDuration: 8 },
  { name: 'essaim_view', label: 'Essaim View', count: 589, conversionRate: 94.8, avgDuration: 3 },
  { name: 'module_enter', label: 'Module Enter', count: 342, conversionRate: 58.1, avgDuration: 45 },
];

const MOCK_SESSIONS: SessionStat[] = [
  { sessionId: 'sess_abc123', eventsCount: 15, funnelProgress: 100, lastActivity: '2 min ago', source: 'direct' },
  { sessionId: 'sess_def456', eventsCount: 8, funnelProgress: 60, lastActivity: '5 min ago', source: 'twitter' },
  { sessionId: 'sess_ghi789', eventsCount: 23, funnelProgress: 80, lastActivity: '1 min ago', source: 'google' },
  { sessionId: 'sess_jkl012', eventsCount: 4, funnelProgress: 40, lastActivity: '10 min ago', source: 'direct' },
  { sessionId: 'sess_mno345', eventsCount: 12, funnelProgress: 100, lastActivity: '3 min ago', source: 'linkedin' },
];

const MOCK_STATS: DashboardStats = {
  totalSessions: 1247,
  activeSessions: 89,
  totalEvents: 15832,
  avgFunnelProgress: 67,
  topSources: [
    { name: 'direct', count: 523 },
    { name: 'google', count: 312 },
    { name: 'twitter', count: 198 },
    { name: 'linkedin', count: 147 },
    { name: 'other', count: 67 },
  ],
};

// =============================================================================
// ADMIN TOKEN
// =============================================================================

const ADMIN_TOKEN = 'atomanalytics';

// =============================================================================
// ANALYTICS DASHBOARD COMPONENT
// =============================================================================

export function AnalyticsDashboard() {
  const navigate = useNavigate();
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [funnel, setFunnel] = useState<FunnelStep[]>([]);
  const [sessions, setSessions] = useState<SessionStat[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState<'today' | 'week' | 'month'>('today');

  // Check authorization
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    if (token === ADMIN_TOKEN) {
      setIsAuthorized(true);
      // Load data
      loadData();
    } else {
      setIsAuthorized(false);
      setLoading(false);
    }
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // TODO: Replace with actual API calls
      // const funnelData = await fetch('/api/v1/analytics/funnel').then(r => r.json());
      // const sessionData = await fetch('/api/v1/analytics/sessions').then(r => r.json());

      // Using mock data for now
      await new Promise(resolve => setTimeout(resolve, 500));
      setFunnel(MOCK_FUNNEL);
      setSessions(MOCK_SESSIONS);
      setStats(MOCK_STATS);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  // Unauthorized view
  if (!isAuthorized && !loading) {
    return (
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#000',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
      }}>
        <div style={{
          textAlign: 'center',
          maxWidth: '400px',
        }}>
          <div style={{ fontSize: '48px', marginBottom: '20px' }}>🔒</div>
          <h1 style={{
            color: '#fff',
            fontSize: '24px',
            marginBottom: '16px',
          }}>
            Accès Restreint
          </h1>
          <p style={{
            color: 'rgba(255, 255, 255, 0.6)',
            marginBottom: '24px',
          }}>
            Ce dashboard nécessite une autorisation admin.
          </p>
          <button
            onClick={() => navigate('/')}
            style={{
              padding: '12px 24px',
              backgroundColor: COLORS.cobalt,
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
            }}
          >
            Retour à l'accueil
          </button>
        </div>
      </div>
    );
  }

  // Loading
  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#000',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <div style={{ color: COLORS.gold, fontFamily: TYPOGRAPHY.fontFamily.mono }}>
          Chargement des analytics...
        </div>
      </div>
    );
  }

  const maxFunnelCount = Math.max(...funnel.map(f => f.count));

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#000',
      color: '#fff',
      fontFamily: TYPOGRAPHY.fontFamily.system,
    }}>
      <Breadcrumbs />

      {/* Header */}
      <header style={{
        padding: '20px 30px',
        paddingTop: '70px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <div>
          <h1 style={{
            fontSize: '24px',
            fontWeight: 600,
            color: COLORS.gold,
            marginBottom: '4px',
          }}>
            Analytics Dashboard
          </h1>
          <p style={{
            fontSize: '14px',
            color: 'rgba(255, 255, 255, 0.5)',
          }}>
            Funnel de conversion et métriques
          </p>
        </div>

        {/* Date range selector */}
        <div style={{ display: 'flex', gap: '8px' }}>
          {(['today', 'week', 'month'] as const).map(range => (
            <button
              key={range}
              onClick={() => setDateRange(range)}
              style={{
                padding: '8px 16px',
                backgroundColor: dateRange === range ? COLORS.gold : 'transparent',
                color: dateRange === range ? '#000' : 'rgba(255, 255, 255, 0.6)',
                border: `1px solid ${dateRange === range ? COLORS.gold : 'rgba(255, 255, 255, 0.2)'}`,
                borderRadius: '6px',
                cursor: 'pointer',
                fontFamily: TYPOGRAPHY.fontFamily.mono,
                fontSize: '12px',
              }}
            >
              {range === 'today' ? 'Aujourd\'hui' : range === 'week' ? '7 jours' : '30 jours'}
            </button>
          ))}
        </div>
      </header>

      <div style={{ padding: '30px' }}>
        {/* Stats cards */}
        {stats && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '20px',
            marginBottom: '40px',
          }}>
            <StatCard
              label="Sessions Totales"
              value={stats.totalSessions.toLocaleString()}
              icon="👥"
              color={COLORS.cobalt}
            />
            <StatCard
              label="Sessions Actives"
              value={stats.activeSessions.toString()}
              icon="🟢"
              color="#27AE60"
            />
            <StatCard
              label="Événements"
              value={stats.totalEvents.toLocaleString()}
              icon="📊"
              color={COLORS.gold}
            />
            <StatCard
              label="Progression Moyenne"
              value={`${stats.avgFunnelProgress}%`}
              icon="📈"
              color="#9B59B6"
            />
          </div>
        )}

        {/* Funnel visualization */}
        <section style={{
          marginBottom: '40px',
          padding: '24px',
          backgroundColor: 'rgba(255, 255, 255, 0.02)',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}>
          <h2 style={{
            fontSize: '18px',
            fontWeight: 600,
            marginBottom: '24px',
            color: COLORS.gold,
          }}>
            Funnel de Conversion
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {funnel.map((step, index) => (
              <div key={step.name}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '8px',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      backgroundColor: COLORS.cobalt,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '12px',
                      fontWeight: 600,
                    }}>
                      {index + 1}
                    </span>
                    <span style={{ fontSize: '14px' }}>{step.label}</span>
                  </div>
                  <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                    <span style={{
                      fontSize: '14px',
                      fontWeight: 600,
                      fontFamily: TYPOGRAPHY.fontFamily.mono,
                    }}>
                      {step.count.toLocaleString()}
                    </span>
                    {index > 0 && (
                      <span style={{
                        fontSize: '12px',
                        color: step.conversionRate > 70 ? '#27AE60' : step.conversionRate > 50 ? '#F39C12' : '#E74C3C',
                        fontFamily: TYPOGRAPHY.fontFamily.mono,
                      }}>
                        {step.conversionRate.toFixed(1)}%
                      </span>
                    )}
                  </div>
                </div>
                <div style={{
                  height: '8px',
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  borderRadius: '4px',
                  overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${(step.count / maxFunnelCount) * 100}%`,
                    backgroundColor: COLORS.cobalt,
                    borderRadius: '4px',
                    transition: 'width 0.5s ease',
                  }} />
                </div>
                {index < funnel.length - 1 && (
                  <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    padding: '8px 0',
                  }}>
                    <span style={{ color: 'rgba(255, 255, 255, 0.3)', fontSize: '12px' }}>
                      ↓ {step.avgDuration}s avg
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Recent sessions */}
        <section style={{
          padding: '24px',
          backgroundColor: 'rgba(255, 255, 255, 0.02)',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}>
          <h2 style={{
            fontSize: '18px',
            fontWeight: 600,
            marginBottom: '24px',
            color: COLORS.gold,
          }}>
            Sessions Récentes
          </h2>

          <div style={{ overflowX: 'auto' }}>
            <table style={{
              width: '100%',
              borderCollapse: 'collapse',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              fontSize: '13px',
            }}>
              <thead>
                <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                  <th style={{ textAlign: 'left', padding: '12px', color: 'rgba(255, 255, 255, 0.5)' }}>Session</th>
                  <th style={{ textAlign: 'left', padding: '12px', color: 'rgba(255, 255, 255, 0.5)' }}>Events</th>
                  <th style={{ textAlign: 'left', padding: '12px', color: 'rgba(255, 255, 255, 0.5)' }}>Progress</th>
                  <th style={{ textAlign: 'left', padding: '12px', color: 'rgba(255, 255, 255, 0.5)' }}>Source</th>
                  <th style={{ textAlign: 'left', padding: '12px', color: 'rgba(255, 255, 255, 0.5)' }}>Last Activity</th>
                </tr>
              </thead>
              <tbody>
                {sessions.map(session => (
                  <tr key={session.sessionId} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                    <td style={{ padding: '12px' }}>{session.sessionId.slice(0, 12)}...</td>
                    <td style={{ padding: '12px' }}>{session.eventsCount}</td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{
                          width: '60px',
                          height: '6px',
                          backgroundColor: 'rgba(255, 255, 255, 0.1)',
                          borderRadius: '3px',
                        }}>
                          <div style={{
                            width: `${session.funnelProgress}%`,
                            height: '100%',
                            backgroundColor: session.funnelProgress === 100 ? '#27AE60' : COLORS.cobalt,
                            borderRadius: '3px',
                          }} />
                        </div>
                        <span>{session.funnelProgress}%</span>
                      </div>
                    </td>
                    <td style={{ padding: '12px' }}>{session.source}</td>
                    <td style={{ padding: '12px', color: 'rgba(255, 255, 255, 0.5)' }}>{session.lastActivity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}

// =============================================================================
// STAT CARD COMPONENT
// =============================================================================

function StatCard({ label, value, icon, color }: {
  label: string;
  value: string;
  icon: string;
  color: string;
}) {
  return (
    <div style={{
      padding: '24px',
      backgroundColor: 'rgba(255, 255, 255, 0.02)',
      borderRadius: '12px',
      border: `1px solid ${color}30`,
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '12px',
      }}>
        <span style={{ fontSize: '24px' }}>{icon}</span>
        <span style={{
          fontSize: '10px',
          color,
          fontFamily: TYPOGRAPHY.fontFamily.mono,
        }}>
          LIVE
        </span>
      </div>
      <div style={{
        fontSize: '28px',
        fontWeight: 700,
        color,
        fontFamily: TYPOGRAPHY.fontFamily.mono,
        marginBottom: '4px',
      }}>
        {value}
      </div>
      <div style={{
        fontSize: '12px',
        color: 'rgba(255, 255, 255, 0.5)',
      }}>
        {label}
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
