/**
 * AGENT WORKSPACE - BUREAUX DES AGENTS
 * =====================================
 *
 * CANON AT·OM - Environnement de Travail Isolé
 * Chemin: /workspace/:agentId
 *
 * Chaque agent orchestrateur-gestionnaire a son propre bureau.
 * Les sous-agents travaillent sous surveillance dans des bureaux alloués.
 *
 * ARCHITECTURE:
 * - Bureau Principal (Orchestrateur)
 *   - Bureaux Alloués (Sous-Agents)
 *   - Données Isolées (Sandbox)
 *   - Monitoring Temps Réel
 *
 * PHILOSOPHIE:
 * "L'agent voit ce qui se passe en temps réel -
 *  c'est son instrument pour jouer de la musique!"
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { agentsService, Agent } from '@/services/agents.service';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { COLORS, TYPOGRAPHY, TOUCH } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface Desk {
  id: string;
  agentId: string;
  agentName: string;
  status: 'active' | 'idle' | 'processing' | 'waiting';
  tasks: Task[];
  dataUsage: number; // 0-100%
  lastActivity: Date;
  color: string;
}

interface Task {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  timestamp: Date;
}

interface ActivityLog {
  id: string;
  agentId: string;
  action: string;
  timestamp: Date;
  type: 'info' | 'success' | 'warning' | 'error';
}

// =============================================================================
// MOCK DATA - Will be replaced by real API
// =============================================================================

const generateMockDesks = (orchestratorId: string): Desk[] => {
  const subAgents = [
    { id: 'data-collector-1', name: 'Data Collector Alpha', color: '#3498DB' },
    { id: 'analyzer-1', name: 'Pattern Analyzer', color: '#9B59B6' },
    { id: 'reporter-1', name: 'Report Generator', color: '#27AE60' },
    { id: 'validator-1', name: 'Data Validator', color: '#F39C12' },
  ];

  return subAgents.map((agent, i) => ({
    id: `desk-${agent.id}`,
    agentId: agent.id,
    agentName: agent.name,
    status: (['active', 'idle', 'processing', 'waiting'] as const)[i % 4],
    tasks: [
      {
        id: `task-${i}-1`,
        name: 'Collecte de données',
        status: 'completed' as const,
        progress: 100,
        timestamp: new Date(Date.now() - 60000 * i),
      },
      {
        id: `task-${i}-2`,
        name: 'Analyse en cours',
        status: 'running' as const,
        progress: 45 + i * 10,
        timestamp: new Date(),
      },
    ],
    dataUsage: 20 + i * 15,
    lastActivity: new Date(Date.now() - 1000 * i * 30),
    color: agent.color,
  }));
};

const generateMockLogs = (): ActivityLog[] => {
  const actions = [
    { action: 'Données collectées: 1,234 entrées', type: 'success' as const },
    { action: 'Analyse de pattern initiée', type: 'info' as const },
    { action: 'Validation en attente d\'approbation', type: 'warning' as const },
    { action: 'Rapport généré: rapport_2024.pdf', type: 'success' as const },
    { action: 'Connexion établie avec source externe', type: 'info' as const },
  ];

  return actions.map((log, i) => ({
    id: `log-${i}`,
    agentId: `agent-${i % 4}`,
    action: log.action,
    timestamp: new Date(Date.now() - 1000 * 60 * i),
    type: log.type,
  }));
};

// =============================================================================
// AGENT WORKSPACE COMPONENT
// =============================================================================

export function AgentWorkspace() {
  const navigate = useNavigate();
  const { agentId } = useParams<{ agentId: string }>();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();

  const [orchestrator, setOrchestrator] = useState<Agent | null>(null);
  const [desks, setDesks] = useState<Desk[]>([]);
  const [logs, setLogs] = useState<ActivityLog[]>([]);
  const [selectedDesk, setSelectedDesk] = useState<Desk | null>(null);
  const [viewMode, setViewMode] = useState<'visual' | 'list' | 'logs'>('visual');
  const [loading, setLoading] = useState(true);

  // Fetch orchestrator agent data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        if (agentId) {
          const agent = await agentsService.getAgent(agentId);
          setOrchestrator(agent);
          setDesks(generateMockDesks(agentId));
          setLogs(generateMockLogs());
        }
      } catch (err) {
        console.error('[AgentWorkspace] Error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [agentId]);

  // Real-time simulation - activity updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate desk activity
      setDesks(prev => prev.map(desk => ({
        ...desk,
        lastActivity: Math.random() > 0.7 ? new Date() : desk.lastActivity,
        tasks: desk.tasks.map(task => ({
          ...task,
          progress: task.status === 'running'
            ? Math.min(100, task.progress + Math.random() * 5)
            : task.progress,
          status: task.progress >= 100 && task.status === 'running'
            ? 'completed' as const
            : task.status,
        })),
      })));

      // Add random log entry occasionally
      if (Math.random() > 0.8) {
        const actions = [
          'Nouvelle donnée reçue',
          'Traitement terminé',
          'Synchronisation en cours',
          'Validation réussie',
        ];
        setLogs(prev => [{
          id: `log-${Date.now()}`,
          agentId: `agent-${Math.floor(Math.random() * 4)}`,
          action: actions[Math.floor(Math.random() * actions.length)],
          timestamp: new Date(),
          type: (['info', 'success'] as const)[Math.floor(Math.random() * 2)],
        }, ...prev.slice(0, 49)]);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Visual workspace animation
  const animate = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const time = Date.now() / 1000;

    // Clear
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Draw orchestrator in center
    const orchRadius = 60;
    const orchGlow = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, orchRadius * 2);
    orchGlow.addColorStop(0, COLORS.gold + '40');
    orchGlow.addColorStop(1, 'transparent');
    ctx.beginPath();
    ctx.arc(centerX, centerY, orchRadius * 2, 0, Math.PI * 2);
    ctx.fillStyle = orchGlow;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(centerX, centerY, orchRadius, 0, Math.PI * 2);
    ctx.fillStyle = COLORS.gold;
    ctx.fill();

    ctx.font = 'bold 14px monospace';
    ctx.fillStyle = '#000';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('ORCHESTRATEUR', centerX, centerY - 8);
    ctx.font = '11px monospace';
    ctx.fillText(orchestrator?.name || 'Loading...', centerX, centerY + 10);

    // Draw desks around orchestrator
    desks.forEach((desk, i) => {
      const angle = (i / desks.length) * Math.PI * 2 - Math.PI / 2;
      const deskRadius = 200;
      const x = centerX + Math.cos(angle) * deskRadius;
      const y = centerY + Math.sin(angle) * deskRadius;

      // Connection line with data flow animation
      const flowOffset = (time * 2 + i) % 1;
      const gradient = ctx.createLinearGradient(centerX, centerY, x, y);
      gradient.addColorStop(Math.max(0, flowOffset - 0.1), 'transparent');
      gradient.addColorStop(flowOffset, desk.color);
      gradient.addColorStop(Math.min(1, flowOffset + 0.1), 'transparent');

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.strokeStyle = desk.status === 'active' ? gradient : desk.color + '30';
      ctx.lineWidth = desk.status === 'active' ? 3 : 1;
      ctx.stroke();

      // Desk node
      const deskSize = 45;
      const isSelected = selectedDesk?.id === desk.id;
      const pulseSize = isSelected ? deskSize + 5 * Math.sin(time * 3) : deskSize;

      // Status glow
      const statusColors: Record<string, string> = {
        active: '#27AE60',
        processing: '#3498DB',
        waiting: '#F39C12',
        idle: '#7F8C8D',
      };

      ctx.beginPath();
      ctx.arc(x, y, pulseSize + 10, 0, Math.PI * 2);
      ctx.fillStyle = statusColors[desk.status] + '30';
      ctx.fill();

      // Desk circle
      ctx.beginPath();
      ctx.arc(x, y, pulseSize, 0, Math.PI * 2);
      ctx.fillStyle = isSelected ? desk.color : desk.color + 'CC';
      ctx.fill();

      // Data usage indicator
      ctx.beginPath();
      ctx.arc(x, y, pulseSize + 3, -Math.PI / 2, -Math.PI / 2 + (desk.dataUsage / 100) * Math.PI * 2);
      ctx.strokeStyle = statusColors[desk.status];
      ctx.lineWidth = 3;
      ctx.stroke();

      // Agent name
      ctx.font = '10px monospace';
      ctx.fillStyle = '#FFF';
      ctx.textAlign = 'center';
      ctx.fillText(desk.agentName.split(' ')[0], x, y - 5);
      ctx.fillText(desk.agentName.split(' ').slice(1).join(' '), x, y + 8);

      // Status indicator
      ctx.font = '8px monospace';
      ctx.fillStyle = statusColors[desk.status];
      ctx.fillText(desk.status.toUpperCase(), x, y + pulseSize + 15);
    });

    animationRef.current = requestAnimationFrame(animate);
  }, [desks, selectedDesk, orchestrator]);

  // Start animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || viewMode !== 'visual') return;

    const resize = () => {
      canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      canvas.height = canvas.parentElement?.clientHeight || 500;
    };
    resize();
    window.addEventListener('resize', resize);

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('resize', resize);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [animate, viewMode]);

  // Handle canvas click
  const handleCanvasClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Check if clicked on a desk
    desks.forEach((desk, i) => {
      const angle = (i / desks.length) * Math.PI * 2 - Math.PI / 2;
      const deskRadius = 200;
      const deskX = centerX + Math.cos(angle) * deskRadius;
      const deskY = centerY + Math.sin(angle) * deskRadius;

      const distance = Math.hypot(x - deskX, y - deskY);
      if (distance < 50) {
        setSelectedDesk(selectedDesk?.id === desk.id ? null : desk);
      }
    });
  }, [desks, selectedDesk]);

  const getStatusColor = (status: Desk['status']) => {
    const colors: Record<Desk['status'], string> = {
      active: '#27AE60',
      processing: '#3498DB',
      waiting: '#F39C12',
      idle: '#7F8C8D',
    };
    return colors[status];
  };

  const getLogTypeColor = (type: ActivityLog['type']) => {
    const colors: Record<ActivityLog['type'], string> = {
      info: '#3498DB',
      success: '#27AE60',
      warning: '#F39C12',
      error: '#E74C3C',
    };
    return colors[type];
  };

  if (loading) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: '#000',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <div style={{ color: COLORS.gold, fontFamily: 'monospace' }}>
          Chargement du bureau...
        </div>
      </div>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      backgroundColor: '#000',
      display: 'flex',
      flexDirection: 'column',
    }}>
      <Breadcrumbs />

      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '15px 30px',
        paddingTop: '60px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <button
            onClick={() => navigate('/essaim')}
            style={{
              background: 'transparent',
              border: 'none',
              color: COLORS.cobalt,
              fontFamily: 'monospace',
              fontSize: '14px',
              cursor: 'pointer',
            }}
          >
            ← ESSAIM
          </button>
          <h1 style={{
            color: COLORS.gold,
            fontFamily: 'monospace',
            fontSize: '18px',
            letterSpacing: '0.2em',
          }}>
            BUREAU: {orchestrator?.name || agentId}
          </h1>
        </div>

        {/* View switcher */}
        <div style={{ display: 'flex', gap: '10px' }}>
          {(['visual', 'list', 'logs'] as const).map(mode => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                backgroundColor: viewMode === mode ? COLORS.gold + '30' : 'transparent',
                border: `1px solid ${viewMode === mode ? COLORS.gold : 'rgba(255, 255, 255, 0.2)'}`,
                color: viewMode === mode ? COLORS.gold : 'rgba(255, 255, 255, 0.5)',
                padding: '10px 18px',
                minHeight: TOUCH.minTarget,
                fontFamily: 'monospace',
                fontSize: '12px',
                cursor: 'pointer',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              {mode === 'visual' ? 'VISUEL' : mode === 'list' ? 'BUREAUX' : 'ACTIVITÉ'}
            </button>
          ))}
        </div>
      </header>

      {/* Main content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Visual view */}
        {viewMode === 'visual' && (
          <div style={{ flex: 1, position: 'relative' }}>
            <canvas
              ref={canvasRef}
              style={{ display: 'block', width: '100%', height: '100%' }}
              onClick={handleCanvasClick}
            />

            {/* Selected desk details */}
            {selectedDesk && (
              <div style={{
                position: 'absolute',
                bottom: 20,
                left: 20,
                right: 20,
                backgroundColor: 'rgba(0, 0, 0, 0.9)',
                border: `1px solid ${selectedDesk.color}`,
                borderRadius: '8px',
                padding: '20px',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div>
                    <h3 style={{ color: selectedDesk.color, fontFamily: 'monospace', margin: 0 }}>
                      {selectedDesk.agentName}
                    </h3>
                    <div style={{
                      color: getStatusColor(selectedDesk.status),
                      fontFamily: 'monospace',
                      fontSize: '12px',
                      marginTop: '5px',
                    }}>
                      Status: {selectedDesk.status.toUpperCase()}
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedDesk(null)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      color: 'rgba(255, 255, 255, 0.5)',
                      fontSize: '20px',
                      cursor: 'pointer',
                    }}
                  >
                    ×
                  </button>
                </div>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: '15px',
                  marginTop: '15px',
                }}>
                  {selectedDesk.tasks.map(task => (
                    <div key={task.id} style={{
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: '4px',
                      padding: '12px',
                    }}>
                      <div style={{
                        color: '#fff',
                        fontFamily: 'monospace',
                        fontSize: '12px',
                      }}>
                        {task.name}
                      </div>
                      <div style={{
                        marginTop: '8px',
                        height: '4px',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderRadius: '2px',
                        overflow: 'hidden',
                      }}>
                        <div style={{
                          width: `${task.progress}%`,
                          height: '100%',
                          backgroundColor: task.status === 'completed' ? '#27AE60' : selectedDesk.color,
                          transition: 'width 0.3s ease',
                        }} />
                      </div>
                      <div style={{
                        color: 'rgba(255, 255, 255, 0.5)',
                        fontFamily: 'monospace',
                        fontSize: '10px',
                        marginTop: '5px',
                      }}>
                        {Math.round(task.progress)}% - {task.status}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* List view */}
        {viewMode === 'list' && (
          <div style={{
            flex: 1,
            padding: '20px',
            overflowY: 'auto',
          }}>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
              gap: '20px',
            }}>
              {desks.map(desk => (
                <div
                  key={desk.id}
                  style={{
                    backgroundColor: 'rgba(255, 255, 255, 0.03)',
                    border: `1px solid ${desk.color}40`,
                    borderRadius: '8px',
                    padding: '20px',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                  onClick={() => setSelectedDesk(desk)}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h3 style={{
                      color: desk.color,
                      fontFamily: 'monospace',
                      fontSize: '14px',
                      margin: 0,
                    }}>
                      {desk.agentName}
                    </h3>
                    <span style={{
                      backgroundColor: getStatusColor(desk.status) + '30',
                      color: getStatusColor(desk.status),
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontFamily: 'monospace',
                      fontSize: '10px',
                    }}>
                      {desk.status.toUpperCase()}
                    </span>
                  </div>

                  <div style={{
                    marginTop: '15px',
                    color: 'rgba(255, 255, 255, 0.6)',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                  }}>
                    <div>Data: {desk.dataUsage}%</div>
                    <div>Tasks: {desk.tasks.length}</div>
                    <div>Last: {desk.lastActivity.toLocaleTimeString()}</div>
                  </div>

                  <div style={{
                    marginTop: '10px',
                    height: '4px',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    borderRadius: '2px',
                  }}>
                    <div style={{
                      width: `${desk.dataUsage}%`,
                      height: '100%',
                      backgroundColor: desk.color,
                      borderRadius: '2px',
                    }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Logs view */}
        {viewMode === 'logs' && (
          <div style={{
            flex: 1,
            padding: '20px',
            overflowY: 'auto',
          }}>
            <div style={{
              backgroundColor: 'rgba(255, 255, 255, 0.02)',
              borderRadius: '8px',
              padding: '10px',
            }}>
              {logs.map(log => (
                <div
                  key={log.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '15px',
                    padding: '12px',
                    borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
                  }}
                >
                  <span style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    backgroundColor: getLogTypeColor(log.type),
                    flexShrink: 0,
                  }} />
                  <span style={{
                    color: 'rgba(255, 255, 255, 0.4)',
                    fontFamily: 'monospace',
                    fontSize: '11px',
                    width: '80px',
                    flexShrink: 0,
                  }}>
                    {log.timestamp.toLocaleTimeString()}
                  </span>
                  <span style={{
                    color: 'rgba(255, 255, 255, 0.8)',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    flex: 1,
                  }}>
                    {log.action}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer status bar */}
      <footer style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 20px',
        backgroundColor: 'rgba(255, 255, 255, 0.02)',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <div style={{
          color: 'rgba(255, 255, 255, 0.4)',
          fontFamily: 'monospace',
          fontSize: '11px',
        }}>
          {desks.length} bureaux actifs | {desks.filter(d => d.status === 'processing').length} en traitement
        </div>
        <div style={{
          color: COLORS.gold,
          fontFamily: 'monospace',
          fontSize: '11px',
        }}>
          TEMPS RÉEL: {new Date().toLocaleTimeString()}
        </div>
      </footer>
    </div>
  );
}

export default AgentWorkspace;
