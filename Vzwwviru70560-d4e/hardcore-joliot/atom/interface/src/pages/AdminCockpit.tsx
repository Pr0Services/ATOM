/**
 * ADMIN COCKPIT - God Mode
 * =========================
 *
 * Cockpit administrateur privé pour le créateur de AT·OM
 * Accès: /admin?token=atomgod
 *
 * MODULES:
 * - Générateur d'environnements
 * - Éditeur de structures internes
 * - Analyseur de données
 *
 * PHILOSOPHIE:
 * Le créateur voit tout, comprend tout, ajuste tout.
 * God Mode = Vision totale + Contrôle absolu.
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { agentsService, Agent } from '@/services/agents.service';

// =============================================================================
// CONSTANTS
// =============================================================================

const COLORS = {
  black: '#000000',
  gold: '#D4AF37',
  cobalt: '#0047AB',
  white: '#FFFFFF',
  red: '#E74C3C',
  green: '#27AE60',
  cyan: '#00CED1',
  purple: '#9B59B6',
  orange: '#F39C12',
};

// God Mode Access Token
const GOD_TOKEN = 'atomgod';

// Environment Templates
const ENV_TEMPLATES = [
  { id: 'standard', name: 'Standard', description: 'Environnement utilisateur standard', agents: 226, spheres: 9 },
  { id: 'minimal', name: 'Minimal', description: 'Configuration légère', agents: 50, spheres: 3 },
  { id: 'enterprise', name: 'Enterprise', description: 'Configuration entreprise', agents: 350, spheres: 12 },
  { id: 'sovereign', name: 'Sovereign', description: 'Mode souverain complet', agents: 500, spheres: 15 },
];

// Structure Types
const STRUCTURE_TYPES = [
  { id: 'sphere', name: 'Sphère', icon: '⭕', color: COLORS.gold },
  { id: 'agent', name: 'Agent', icon: '🤖', color: COLORS.cyan },
  { id: 'flow', name: 'Flux', icon: '🌊', color: COLORS.cobalt },
  { id: 'gate', name: 'Gate', icon: '🚪', color: COLORS.purple },
  { id: 'frequency', name: 'Fréquence', icon: '〰️', color: COLORS.orange },
];

// Analytics Metrics
const ANALYTICS_CATEGORIES = [
  { id: 'users', name: 'Utilisateurs', icon: '👥' },
  { id: 'agents', name: 'Agents', icon: '🤖' },
  { id: 'frequencies', name: 'Fréquences', icon: '〰️' },
  { id: 'connections', name: 'Connexions', icon: '🔗' },
  { id: 'spheres', name: 'Sphères', icon: '⭕' },
];

// =============================================================================
// TYPES
// =============================================================================

type ViewMode = 'generator' | 'structures' | 'analytics';

interface StructureNode {
  id: string;
  type: string;
  name: string;
  x: number;
  y: number;
  connections: string[];
  data: Record<string, unknown>;
}

interface AnalyticsData {
  category: string;
  values: { label: string; value: number; change: number }[];
}

// =============================================================================
// ADMIN COCKPIT COMPONENT
// =============================================================================

export function AdminCockpit() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Access control
  const [isAuthorized, setIsAuthorized] = useState(false);

  // View state
  const [viewMode, setViewMode] = useState<ViewMode>('generator');

  // Generator state
  const [selectedTemplate, setSelectedTemplate] = useState<string>('standard');
  const [customConfig, setCustomConfig] = useState({
    name: '',
    agents: 226,
    spheres: 9,
    frequencies: true,
    humanGates: true,
  });
  const [generatedEnvs, setGeneratedEnvs] = useState<string[]>([]);

  // Structures state
  const [structures, setStructures] = useState<StructureNode[]>([]);
  const [selectedStructure, setSelectedStructure] = useState<string | null>(null);
  const [editMode, setEditMode] = useState(false);

  // Analytics state
  const [analyticsCategory, setAnalyticsCategory] = useState('users');
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData[]>([]);
  const [realAgents, setRealAgents] = useState<Agent[]>([]);

  // Check authorization
  useEffect(() => {
    const token = searchParams.get('token');
    if (token === GOD_TOKEN) {
      setIsAuthorized(true);
    }
  }, [searchParams]);

  // Load real agents data
  useEffect(() => {
    if (!isAuthorized) return;

    const loadAgents = async () => {
      try {
        const agents = await agentsService.getAllAgents();
        setRealAgents(agents);
      } catch (error) {
        console.error('[AdminCockpit] Failed to load agents:', error);
      }
    };

    loadAgents();
  }, [isAuthorized]);

  // Initialize structures
  useEffect(() => {
    if (!isAuthorized) return;

    // Generate initial structure map based on real agents
    const initialStructures: StructureNode[] = [
      { id: 'core', type: 'sphere', name: 'CORE', x: 0.5, y: 0.5, connections: [], data: {} },
    ];

    // Add sphere nodes
    const spheres = ['personal', 'business', 'government', 'creative', 'community', 'social', 'entertainment', 'team', 'scholar'];
    spheres.forEach((sphere, i) => {
      const angle = (i / spheres.length) * Math.PI * 2 - Math.PI / 2;
      initialStructures.push({
        id: sphere,
        type: 'sphere',
        name: sphere.toUpperCase(),
        x: 0.5 + Math.cos(angle) * 0.35,
        y: 0.5 + Math.sin(angle) * 0.35,
        connections: ['core'],
        data: { agentCount: Math.floor(226 / 9) },
      });
    });

    setStructures(initialStructures);
  }, [isAuthorized]);

  // Generate simulated analytics
  useEffect(() => {
    if (!isAuthorized) return;

    const generateAnalytics = (): AnalyticsData[] => [
      {
        category: 'users',
        values: [
          { label: 'Actifs', value: 1247, change: 12.5 },
          { label: 'Nouveaux', value: 89, change: 23.1 },
          { label: 'Souverains', value: 342, change: 8.7 },
          { label: 'Sessions', value: 4521, change: -2.3 },
        ],
      },
      {
        category: 'agents',
        values: [
          { label: 'Total', value: realAgents.length || 226, change: 0 },
          { label: 'Actifs', value: Math.floor((realAgents.length || 226) * 0.85), change: 5.2 },
          { label: 'Human Gate', value: realAgents.filter(a => a.requires_human_gate).length || 45, change: 0 },
          { label: 'Tâches/h', value: 15420, change: 18.9 },
        ],
      },
      {
        category: 'frequencies',
        values: [
          { label: '999 Hz', value: 98.7, change: 0.3 },
          { label: '432 Hz', value: 95.2, change: 1.1 },
          { label: '528 Hz', value: 97.8, change: 0.5 },
          { label: 'Schumann', value: 99.1, change: 0.1 },
        ],
      },
      {
        category: 'connections',
        values: [
          { label: 'WebSocket', value: 892, change: 15.3 },
          { label: 'API Calls', value: 45230, change: 22.1 },
          { label: 'Sync', value: 1205, change: 8.4 },
          { label: 'Latence ms', value: 45, change: -12.5 },
        ],
      },
      {
        category: 'spheres',
        values: [
          { label: 'Personal', value: 425, change: 10.2 },
          { label: 'Business', value: 312, change: 15.8 },
          { label: 'Creative', value: 289, change: 25.3 },
          { label: 'Community', value: 178, change: 18.7 },
        ],
      },
    ];

    setAnalyticsData(generateAnalytics());
  }, [isAuthorized, realAgents]);

  // Canvas animation for structures view
  useEffect(() => {
    if (viewMode !== 'structures' || !isAuthorized) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const animate = () => {
      ctx.fillStyle = COLORS.black;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 50) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += 50) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Draw connections
      structures.forEach(node => {
        node.connections.forEach(connId => {
          const target = structures.find(s => s.id === connId);
          if (!target) return;

          const fromX = node.x * canvas.width;
          const fromY = node.y * canvas.height;
          const toX = target.x * canvas.width;
          const toY = target.y * canvas.height;

          // Animated line
          ctx.beginPath();
          ctx.moveTo(fromX, fromY);
          ctx.lineTo(toX, toY);
          ctx.strokeStyle = selectedStructure === node.id ? COLORS.gold : 'rgba(212, 175, 55, 0.3)';
          ctx.lineWidth = selectedStructure === node.id ? 2 : 1;
          ctx.stroke();

          // Flow particle
          const progress = (time % 100) / 100;
          const particleX = fromX + (toX - fromX) * progress;
          const particleY = fromY + (toY - fromY) * progress;

          ctx.beginPath();
          ctx.arc(particleX, particleY, 3, 0, Math.PI * 2);
          ctx.fillStyle = COLORS.gold;
          ctx.fill();
        });
      });

      // Draw nodes
      structures.forEach(node => {
        const x = node.x * canvas.width;
        const y = node.y * canvas.height;
        const structureType = STRUCTURE_TYPES.find(t => t.id === node.type);
        const isSelected = selectedStructure === node.id;
        const radius = node.id === 'core' ? 50 : 30;

        // Glow effect
        if (isSelected) {
          const glowGradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2);
          glowGradient.addColorStop(0, (structureType?.color || COLORS.gold) + '40');
          glowGradient.addColorStop(1, 'transparent');
          ctx.beginPath();
          ctx.arc(x, y, radius * 2, 0, Math.PI * 2);
          ctx.fillStyle = glowGradient;
          ctx.fill();
        }

        // Node circle
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? (structureType?.color || COLORS.gold) : (structureType?.color || COLORS.gold) + '60';
        ctx.fill();
        ctx.strokeStyle = structureType?.color || COLORS.gold;
        ctx.lineWidth = isSelected ? 3 : 1;
        ctx.stroke();

        // Node icon
        ctx.font = `${radius * 0.8}px serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(structureType?.icon || '⭕', x, y);

        // Node name
        ctx.font = '10px monospace';
        ctx.fillStyle = COLORS.white;
        ctx.fillText(node.name, x, y + radius + 15);
      });

      // Edit mode indicator
      if (editMode) {
        ctx.font = 'bold 14px monospace';
        ctx.fillStyle = COLORS.red;
        ctx.textAlign = 'left';
        ctx.fillText('MODE ÉDITION ACTIF', 20, 30);
      }

      time++;
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [viewMode, structures, selectedStructure, editMode, isAuthorized]);

  // Handle structure click
  const handleCanvasClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / canvas.width;
    const y = (e.clientY - rect.top) / canvas.height;

    // Find clicked node
    const clickedNode = structures.find(node => {
      const dx = node.x - x;
      const dy = node.y - y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      return distance < 0.05;
    });

    if (clickedNode) {
      setSelectedStructure(selectedStructure === clickedNode.id ? null : clickedNode.id);
    } else if (editMode) {
      // Add new node in edit mode
      const newNode: StructureNode = {
        id: `node_${Date.now()}`,
        type: 'agent',
        name: 'NEW',
        x,
        y,
        connections: selectedStructure ? [selectedStructure] : [],
        data: {},
      };
      setStructures([...structures, newNode]);
    }
  }, [structures, selectedStructure, editMode]);

  // Generate environment
  const generateEnvironment = useCallback(() => {
    const template = ENV_TEMPLATES.find(t => t.id === selectedTemplate);
    const envId = `ENV_${Date.now().toString(36).toUpperCase()}`;

    console.log('[AdminCockpit] Generating environment:', {
      id: envId,
      template: template?.name,
      config: customConfig,
    });

    setGeneratedEnvs([...generatedEnvs, envId]);
  }, [selectedTemplate, customConfig, generatedEnvs]);

  // Unauthorized view
  if (!isAuthorized) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: COLORS.black,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            fontSize: '60px',
            marginBottom: '20px',
          }}>
            🔒
          </div>
          <h1 style={{
            color: COLORS.red,
            fontFamily: 'monospace',
            fontSize: '24px',
            letterSpacing: '0.3em',
            marginBottom: '10px',
          }}>
            ACCÈS REFUSÉ
          </h1>
          <p style={{
            color: 'rgba(255, 255, 255, 0.5)',
            fontFamily: 'monospace',
            fontSize: '12px',
          }}>
            God Mode requiert une autorisation
          </p>
          <button
            onClick={() => navigate('/')}
            style={{
              marginTop: '30px',
              background: 'transparent',
              border: `1px solid ${COLORS.gold}`,
              color: COLORS.gold,
              padding: '10px 30px',
              fontFamily: 'monospace',
              fontSize: '12px',
              cursor: 'pointer',
              borderRadius: '4px',
            }}
          >
            RETOUR
          </button>
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
      backgroundColor: COLORS.black,
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
    }}>
      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '15px 30px',
        borderBottom: '1px solid rgba(212, 175, 55, 0.3)',
        background: 'linear-gradient(180deg, rgba(212, 175, 55, 0.1) 0%, transparent 100%)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <button
            onClick={() => navigate('/sovereign?token=999')}
            style={{
              background: 'transparent',
              border: 'none',
              color: COLORS.cobalt,
              fontFamily: 'monospace',
              fontSize: '14px',
              cursor: 'pointer',
            }}
          >
            ← SOVEREIGN
          </button>
          <h1 style={{
            color: COLORS.gold,
            fontFamily: 'monospace',
            fontSize: '18px',
            letterSpacing: '0.3em',
          }}>
            ADMIN COCKPIT
          </h1>
          <span style={{
            backgroundColor: COLORS.gold,
            color: COLORS.black,
            padding: '4px 12px',
            borderRadius: '12px',
            fontFamily: 'monospace',
            fontSize: '10px',
            fontWeight: 'bold',
          }}>
            GOD MODE
          </span>
        </div>

        {/* Module Switcher */}
        <div style={{ display: 'flex', gap: '10px' }}>
          {([
            { id: 'generator', label: 'GÉNÉRATEUR', icon: '⚡' },
            { id: 'structures', label: 'STRUCTURES', icon: '🏗️' },
            { id: 'analytics', label: 'ANALYTICS', icon: '📊' },
          ] as const).map(module => (
            <button
              key={module.id}
              onClick={() => setViewMode(module.id)}
              style={{
                backgroundColor: viewMode === module.id ? COLORS.gold + '30' : 'transparent',
                border: `1px solid ${viewMode === module.id ? COLORS.gold : 'rgba(255, 255, 255, 0.2)'}`,
                color: viewMode === module.id ? COLORS.gold : 'rgba(255, 255, 255, 0.5)',
                padding: '8px 16px',
                fontFamily: 'monospace',
                fontSize: '11px',
                cursor: 'pointer',
                borderRadius: '4px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
              }}
            >
              <span>{module.icon}</span>
              {module.label}
            </button>
          ))}
        </div>
      </header>

      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* ============================================= */}
        {/* GENERATOR MODULE */}
        {/* ============================================= */}
        {viewMode === 'generator' && (
          <div style={{ flex: 1, display: 'flex', padding: '30px', gap: '30px' }}>
            {/* Templates */}
            <div style={{
              width: '300px',
              display: 'flex',
              flexDirection: 'column',
              gap: '15px',
            }}>
              <h2 style={{
                color: COLORS.gold,
                fontFamily: 'monospace',
                fontSize: '14px',
                letterSpacing: '0.2em',
                marginBottom: '10px',
              }}>
                TEMPLATES
              </h2>

              {ENV_TEMPLATES.map(template => (
                <button
                  key={template.id}
                  onClick={() => setSelectedTemplate(template.id)}
                  style={{
                    backgroundColor: selectedTemplate === template.id ? COLORS.gold + '20' : 'rgba(255, 255, 255, 0.05)',
                    border: `1px solid ${selectedTemplate === template.id ? COLORS.gold : 'rgba(255, 255, 255, 0.1)'}`,
                    borderRadius: '8px',
                    padding: '15px',
                    textAlign: 'left',
                    cursor: 'pointer',
                  }}
                >
                  <div style={{
                    color: selectedTemplate === template.id ? COLORS.gold : COLORS.white,
                    fontFamily: 'monospace',
                    fontSize: '14px',
                    fontWeight: 'bold',
                    marginBottom: '5px',
                  }}>
                    {template.name}
                  </div>
                  <div style={{
                    color: 'rgba(255, 255, 255, 0.5)',
                    fontFamily: 'monospace',
                    fontSize: '11px',
                    marginBottom: '10px',
                  }}>
                    {template.description}
                  </div>
                  <div style={{
                    display: 'flex',
                    gap: '15px',
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontFamily: 'monospace',
                    fontSize: '10px',
                  }}>
                    <span>🤖 {template.agents}</span>
                    <span>⭕ {template.spheres}</span>
                  </div>
                </button>
              ))}
            </div>

            {/* Configuration */}
            <div style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              gap: '20px',
            }}>
              <h2 style={{
                color: COLORS.gold,
                fontFamily: 'monospace',
                fontSize: '14px',
                letterSpacing: '0.2em',
              }}>
                CONFIGURATION
              </h2>

              <div style={{
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '12px',
                padding: '25px',
              }}>
                {/* Name */}
                <div style={{ marginBottom: '20px' }}>
                  <label style={{
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontFamily: 'monospace',
                    fontSize: '11px',
                    display: 'block',
                    marginBottom: '8px',
                  }}>
                    NOM DE L'ENVIRONNEMENT
                  </label>
                  <input
                    type="text"
                    value={customConfig.name}
                    onChange={e => setCustomConfig({ ...customConfig, name: e.target.value })}
                    placeholder="Mon environnement..."
                    style={{
                      width: '100%',
                      backgroundColor: 'rgba(0, 0, 0, 0.5)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '6px',
                      padding: '12px',
                      color: COLORS.white,
                      fontFamily: 'monospace',
                      fontSize: '14px',
                    }}
                  />
                </div>

                {/* Sliders */}
                <div style={{ marginBottom: '20px' }}>
                  <label style={{
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontFamily: 'monospace',
                    fontSize: '11px',
                    display: 'block',
                    marginBottom: '8px',
                  }}>
                    NOMBRE D'AGENTS: {customConfig.agents}
                  </label>
                  <input
                    type="range"
                    min="10"
                    max="500"
                    value={customConfig.agents}
                    onChange={e => setCustomConfig({ ...customConfig, agents: parseInt(e.target.value) })}
                    style={{
                      width: '100%',
                      accentColor: COLORS.gold,
                    }}
                  />
                </div>

                <div style={{ marginBottom: '20px' }}>
                  <label style={{
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontFamily: 'monospace',
                    fontSize: '11px',
                    display: 'block',
                    marginBottom: '8px',
                  }}>
                    NOMBRE DE SPHÈRES: {customConfig.spheres}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="20"
                    value={customConfig.spheres}
                    onChange={e => setCustomConfig({ ...customConfig, spheres: parseInt(e.target.value) })}
                    style={{
                      width: '100%',
                      accentColor: COLORS.gold,
                    }}
                  />
                </div>

                {/* Toggles */}
                <div style={{ display: 'flex', gap: '30px' }}>
                  <label style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    cursor: 'pointer',
                  }}>
                    <input
                      type="checkbox"
                      checked={customConfig.frequencies}
                      onChange={e => setCustomConfig({ ...customConfig, frequencies: e.target.checked })}
                      style={{ accentColor: COLORS.gold }}
                    />
                    <span style={{
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontFamily: 'monospace',
                      fontSize: '12px',
                    }}>
                      Fréquences actives
                    </span>
                  </label>

                  <label style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    cursor: 'pointer',
                  }}>
                    <input
                      type="checkbox"
                      checked={customConfig.humanGates}
                      onChange={e => setCustomConfig({ ...customConfig, humanGates: e.target.checked })}
                      style={{ accentColor: COLORS.gold }}
                    />
                    <span style={{
                      color: 'rgba(255, 255, 255, 0.7)',
                      fontFamily: 'monospace',
                      fontSize: '12px',
                    }}>
                      Human Gates
                    </span>
                  </label>
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateEnvironment}
                style={{
                  backgroundColor: COLORS.gold,
                  border: 'none',
                  borderRadius: '8px',
                  padding: '15px 30px',
                  color: COLORS.black,
                  fontFamily: 'monospace',
                  fontSize: '14px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  letterSpacing: '0.1em',
                }}
              >
                ⚡ GÉNÉRER L'ENVIRONNEMENT
              </button>

              {/* Generated Environments */}
              {generatedEnvs.length > 0 && (
                <div style={{ marginTop: '20px' }}>
                  <h3 style={{
                    color: COLORS.green,
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    marginBottom: '10px',
                  }}>
                    ENVIRONNEMENTS GÉNÉRÉS
                  </h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                    {generatedEnvs.map(env => (
                      <span
                        key={env}
                        style={{
                          backgroundColor: COLORS.green + '20',
                          border: `1px solid ${COLORS.green}`,
                          borderRadius: '4px',
                          padding: '6px 12px',
                          color: COLORS.green,
                          fontFamily: 'monospace',
                          fontSize: '11px',
                        }}
                      >
                        {env}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ============================================= */}
        {/* STRUCTURES MODULE */}
        {/* ============================================= */}
        {viewMode === 'structures' && (
          <div style={{ flex: 1, display: 'flex' }}>
            {/* Canvas */}
            <canvas
              ref={canvasRef}
              width={window.innerWidth - 350}
              height={window.innerHeight - 100}
              style={{ flex: 1, cursor: editMode ? 'crosshair' : 'pointer' }}
              onClick={handleCanvasClick}
            />

            {/* Panel */}
            <div style={{
              width: '350px',
              borderLeft: '1px solid rgba(255, 255, 255, 0.1)',
              padding: '20px',
              overflowY: 'auto',
            }}>
              {/* Edit Mode Toggle */}
              <button
                onClick={() => setEditMode(!editMode)}
                style={{
                  width: '100%',
                  backgroundColor: editMode ? COLORS.red + '30' : 'rgba(255, 255, 255, 0.05)',
                  border: `1px solid ${editMode ? COLORS.red : 'rgba(255, 255, 255, 0.2)'}`,
                  borderRadius: '8px',
                  padding: '12px',
                  color: editMode ? COLORS.red : 'rgba(255, 255, 255, 0.7)',
                  fontFamily: 'monospace',
                  fontSize: '12px',
                  cursor: 'pointer',
                  marginBottom: '20px',
                }}
              >
                {editMode ? '🔓 MODE ÉDITION ACTIF' : '🔒 ACTIVER L\'ÉDITION'}
              </button>

              {/* Structure Types */}
              <h3 style={{
                color: COLORS.gold,
                fontFamily: 'monospace',
                fontSize: '12px',
                letterSpacing: '0.1em',
                marginBottom: '15px',
              }}>
                TYPES DE STRUCTURES
              </h3>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '25px' }}>
                {STRUCTURE_TYPES.map(type => (
                  <span
                    key={type.id}
                    style={{
                      backgroundColor: type.color + '20',
                      border: `1px solid ${type.color}`,
                      borderRadius: '4px',
                      padding: '6px 10px',
                      color: type.color,
                      fontFamily: 'monospace',
                      fontSize: '10px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                    }}
                  >
                    {type.icon} {type.name}
                  </span>
                ))}
              </div>

              {/* Selected Structure */}
              {selectedStructure && (
                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '8px',
                  padding: '15px',
                }}>
                  <h4 style={{
                    color: COLORS.white,
                    fontFamily: 'monospace',
                    fontSize: '14px',
                    marginBottom: '15px',
                  }}>
                    {structures.find(s => s.id === selectedStructure)?.name}
                  </h4>

                  <div style={{
                    color: 'rgba(255, 255, 255, 0.5)',
                    fontFamily: 'monospace',
                    fontSize: '11px',
                    lineHeight: 1.8,
                  }}>
                    <div>ID: {selectedStructure}</div>
                    <div>Type: {structures.find(s => s.id === selectedStructure)?.type}</div>
                    <div>Connexions: {structures.find(s => s.id === selectedStructure)?.connections.length}</div>
                  </div>

                  {editMode && (
                    <button
                      onClick={() => {
                        setStructures(structures.filter(s => s.id !== selectedStructure));
                        setSelectedStructure(null);
                      }}
                      style={{
                        marginTop: '15px',
                        backgroundColor: COLORS.red + '30',
                        border: `1px solid ${COLORS.red}`,
                        borderRadius: '4px',
                        padding: '8px 15px',
                        color: COLORS.red,
                        fontFamily: 'monospace',
                        fontSize: '11px',
                        cursor: 'pointer',
                      }}
                    >
                      SUPPRIMER
                    </button>
                  )}
                </div>
              )}

              {/* Stats */}
              <div style={{ marginTop: '25px' }}>
                <h3 style={{
                  color: COLORS.gold,
                  fontFamily: 'monospace',
                  fontSize: '12px',
                  letterSpacing: '0.1em',
                  marginBottom: '15px',
                }}>
                  STATISTIQUES
                </h3>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '10px',
                }}>
                  <div style={{
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '6px',
                    padding: '12px',
                    textAlign: 'center',
                  }}>
                    <div style={{
                      color: COLORS.gold,
                      fontFamily: 'monospace',
                      fontSize: '24px',
                      fontWeight: 'bold',
                    }}>
                      {structures.length}
                    </div>
                    <div style={{
                      color: 'rgba(255, 255, 255, 0.5)',
                      fontFamily: 'monospace',
                      fontSize: '10px',
                    }}>
                      Structures
                    </div>
                  </div>

                  <div style={{
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '6px',
                    padding: '12px',
                    textAlign: 'center',
                  }}>
                    <div style={{
                      color: COLORS.cyan,
                      fontFamily: 'monospace',
                      fontSize: '24px',
                      fontWeight: 'bold',
                    }}>
                      {structures.reduce((acc, s) => acc + s.connections.length, 0)}
                    </div>
                    <div style={{
                      color: 'rgba(255, 255, 255, 0.5)',
                      fontFamily: 'monospace',
                      fontSize: '10px',
                    }}>
                      Connexions
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ============================================= */}
        {/* ANALYTICS MODULE */}
        {/* ============================================= */}
        {viewMode === 'analytics' && (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '30px' }}>
            {/* Category Tabs */}
            <div style={{
              display: 'flex',
              gap: '10px',
              marginBottom: '30px',
            }}>
              {ANALYTICS_CATEGORIES.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => setAnalyticsCategory(cat.id)}
                  style={{
                    backgroundColor: analyticsCategory === cat.id ? COLORS.gold + '30' : 'rgba(255, 255, 255, 0.05)',
                    border: `1px solid ${analyticsCategory === cat.id ? COLORS.gold : 'rgba(255, 255, 255, 0.1)'}`,
                    borderRadius: '8px',
                    padding: '12px 20px',
                    color: analyticsCategory === cat.id ? COLORS.gold : 'rgba(255, 255, 255, 0.6)',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                >
                  <span>{cat.icon}</span>
                  {cat.name}
                </button>
              ))}
            </div>

            {/* Metrics Cards */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '20px',
              flex: 1,
            }}>
              {analyticsData
                .find(d => d.category === analyticsCategory)
                ?.values.map((metric, i) => (
                  <div
                    key={i}
                    style={{
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: '12px',
                      padding: '25px',
                      display: 'flex',
                      flexDirection: 'column',
                    }}
                  >
                    <div style={{
                      color: 'rgba(255, 255, 255, 0.5)',
                      fontFamily: 'monospace',
                      fontSize: '11px',
                      letterSpacing: '0.1em',
                      marginBottom: '10px',
                    }}>
                      {metric.label.toUpperCase()}
                    </div>

                    <div style={{
                      color: COLORS.white,
                      fontFamily: 'monospace',
                      fontSize: '36px',
                      fontWeight: 'bold',
                      marginBottom: '10px',
                    }}>
                      {typeof metric.value === 'number' && metric.value > 1000
                        ? `${(metric.value / 1000).toFixed(1)}k`
                        : metric.value}
                    </div>

                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                    }}>
                      <span style={{
                        color: metric.change >= 0 ? COLORS.green : COLORS.red,
                        fontFamily: 'monospace',
                        fontSize: '12px',
                      }}>
                        {metric.change >= 0 ? '↑' : '↓'} {Math.abs(metric.change)}%
                      </span>
                      <span style={{
                        color: 'rgba(255, 255, 255, 0.3)',
                        fontFamily: 'monospace',
                        fontSize: '10px',
                      }}>
                        vs hier
                      </span>
                    </div>

                    {/* Mini progress bar */}
                    <div style={{
                      marginTop: 'auto',
                      paddingTop: '15px',
                    }}>
                      <div style={{
                        width: '100%',
                        height: '4px',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderRadius: '2px',
                        overflow: 'hidden',
                      }}>
                        <div style={{
                          width: `${Math.min(100, (typeof metric.value === 'number' ? metric.value : 50) / 50)}%`,
                          height: '100%',
                          backgroundColor: metric.change >= 0 ? COLORS.green : COLORS.orange,
                          borderRadius: '2px',
                        }} />
                      </div>
                    </div>
                  </div>
                ))}
            </div>

            {/* Real Agents Summary */}
            <div style={{
              marginTop: '30px',
              backgroundColor: 'rgba(212, 175, 55, 0.1)',
              borderRadius: '12px',
              padding: '20px',
              border: `1px solid ${COLORS.gold}30`,
            }}>
              <h3 style={{
                color: COLORS.gold,
                fontFamily: 'monospace',
                fontSize: '14px',
                letterSpacing: '0.1em',
                marginBottom: '15px',
              }}>
                AGENTS RÉELS CHARGÉS
              </h3>

              <div style={{
                display: 'flex',
                gap: '30px',
                flexWrap: 'wrap',
              }}>
                <div>
                  <span style={{
                    color: COLORS.white,
                    fontFamily: 'monospace',
                    fontSize: '24px',
                    fontWeight: 'bold',
                  }}>
                    {realAgents.length}
                  </span>
                  <span style={{
                    color: 'rgba(255, 255, 255, 0.5)',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    marginLeft: '8px',
                  }}>
                    total
                  </span>
                </div>

                <div>
                  <span style={{
                    color: COLORS.green,
                    fontFamily: 'monospace',
                    fontSize: '24px',
                    fontWeight: 'bold',
                  }}>
                    {realAgents.filter(a => a.status === 'active').length}
                  </span>
                  <span style={{
                    color: 'rgba(255, 255, 255, 0.5)',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    marginLeft: '8px',
                  }}>
                    actifs
                  </span>
                </div>

                <div>
                  <span style={{
                    color: COLORS.purple,
                    fontFamily: 'monospace',
                    fontSize: '24px',
                    fontWeight: 'bold',
                  }}>
                    {realAgents.filter(a => a.requires_human_gate).length}
                  </span>
                  <span style={{
                    color: 'rgba(255, 255, 255, 0.5)',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    marginLeft: '8px',
                  }}>
                    human gate
                  </span>
                </div>

                <div>
                  <span style={{
                    color: COLORS.cyan,
                    fontFamily: 'monospace',
                    fontSize: '24px',
                    fontWeight: 'bold',
                  }}>
                    9
                  </span>
                  <span style={{
                    color: 'rgba(255, 255, 255, 0.5)',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    marginLeft: '8px',
                  }}>
                    sphères
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer style={{
        padding: '15px 30px',
        borderTop: '1px solid rgba(212, 175, 55, 0.2)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <div style={{
          color: 'rgba(255, 255, 255, 0.3)',
          fontFamily: 'monospace',
          fontSize: '10px',
        }}>
          AT·OM ADMIN COCKPIT v1.0 | GOD MODE ACTIVÉ
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '15px',
        }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: COLORS.green,
            animation: 'pulse 2s infinite',
          }} />
          <span style={{
            color: COLORS.green,
            fontFamily: 'monospace',
            fontSize: '10px',
          }}>
            SYSTÈME OPÉRATIONNEL
          </span>
        </div>
      </footer>

      {/* CSS Animation */}
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}

export default AdminCockpit;
