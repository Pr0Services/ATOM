/**
 * L'ESSAIM - HUB DES 226 AGENTS REELS
 * ====================================
 *
 * CANON AT·OM - Le Hub des Agents NOVA-999
 * Chemin: /essaim ou /swarm
 *
 * Contenu: Visualisation dynamique des 226 agents reels du registre.
 * Les agents sont recuperes depuis l'API backend DigitalOcean.
 *
 * FONCTIONNALITES:
 * - Chaque point represente un vrai agent avec ses capacites
 * - Clic pour reveler la fonction specifique
 * - Navigation gestuelle (swipe/zoom)
 * - Connexion temps reel avec le backend
 */

import React, { useState, useRef, useCallback, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { agentsService, Agent } from '@/services/agents.service';

// =============================================================================
// CONSTANTS - Canon AT·OM
// =============================================================================

const COLORS = {
  black: '#000000',
  gold: '#D4AF37',
  cobalt: '#0047AB',
  white: '#FFFFFF',
};

// Sphere paths for navigation
const SPHERE_PATHS: Record<string, string> = {
  personal: '/sphere/personal',
  business: '/sphere/business',
  government: '/sphere/government',
  creative_studio: '/sphere/creative',
  community: '/sphere/community',
  social_media: '/sphere/social',
  entertainment: '/sphere/entertainment',
  my_team: '/sphere/team',
  scholar: '/sphere/scholar',
};

// =============================================================================
// TYPES
// =============================================================================

interface VisualAgent {
  id: string;
  sphereKey: string;
  x: number;
  y: number;
  baseX: number;
  baseY: number;
  size: number;
  color: string;
  name: string;
  displayName: string;
  capabilities: string[];
  requiresHumanGate: boolean;
  isHovered: boolean;
}

interface ViewState {
  zoom: number;
  offsetX: number;
  offsetY: number;
  focusedSphere: string | null;
}

interface SphereGroup {
  key: string;
  name: string;
  color: string;
  count: number;
  agents: Agent[];
}

// =============================================================================
// ESSAIM COMPONENT
// =============================================================================

export function Essaim() {
  const navigate = useNavigate();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();

  const [viewState, setViewState] = useState<ViewState>({
    zoom: 1,
    offsetX: 0,
    offsetY: 0,
    focusedSphere: null,
  });

  const [hoveredAgent, setHoveredAgent] = useState<VisualAgent | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [apiAgents, setApiAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalAgents, setTotalAgents] = useState(0);

  // Fetch agents from API
  useEffect(() => {
    const fetchAgents = async () => {
      try {
        setLoading(true);
        setError(null);
        const agents = await agentsService.getAllAgents();
        setApiAgents(agents);
        setTotalAgents(agents.length);
        console.log(`[Essaim] Loaded ${agents.length} agents from API`);
      } catch (err) {
        console.error('[Essaim] Failed to fetch agents:', err);
        setError('Connexion au serveur impossible. Mode hors-ligne.');
        // Continue with empty array - will show fallback
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  // Group agents by sphere
  const sphereGroups = useMemo(() => {
    const groups: Record<string, SphereGroup> = {};

    apiAgents.forEach(agent => {
      const sphereKey = agent.sphere;
      if (!groups[sphereKey]) {
        groups[sphereKey] = {
          key: sphereKey,
          name: agent.sphere_name,
          color: agent.sphere_color,
          count: 0,
          agents: [],
        };
      }
      groups[sphereKey].agents.push(agent);
      groups[sphereKey].count++;
    });

    return groups;
  }, [apiAgents]);

  // Generate visual agents from API data
  const agents = useMemo(() => {
    const result: VisualAgent[] = [];
    const sphereKeys = Object.keys(sphereGroups);
    const totalSpheres = sphereKeys.length || 1;

    sphereKeys.forEach((sphereKey, sphereIndex) => {
      const group = sphereGroups[sphereKey];
      const sphereAngle = (sphereIndex / totalSpheres) * Math.PI * 2;
      const sphereRadius = 250;

      // Sphere center position
      const sphereCenterX = Math.cos(sphereAngle) * sphereRadius;
      const sphereCenterY = Math.sin(sphereAngle) * sphereRadius;

      // Distribute agents within sphere cluster
      group.agents.forEach((agent, i) => {
        const agentAngle = (i / group.count) * Math.PI * 2;
        const agentRadius = 30 + (Math.abs(agent.id.charCodeAt(0) % 50));

        const x = sphereCenterX + Math.cos(agentAngle) * agentRadius;
        const y = sphereCenterY + Math.sin(agentAngle) * agentRadius;

        result.push({
          id: agent.id,
          sphereKey,
          x,
          y,
          baseX: x,
          baseY: y,
          size: agent.requires_human_gate ? 4 : 3 + (agent.capabilities.length * 0.3),
          color: group.color,
          name: agent.id,
          displayName: agent.name,
          capabilities: agent.capabilities,
          requiresHumanGate: agent.requires_human_gate,
          isHovered: false,
        });
      });
    });

    return result;
  }, [sphereGroups]);

  // Animation and interaction
  const animate = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const time = Date.now() / 1000;
    const centerX = canvas.width / 2 + viewState.offsetX;
    const centerY = canvas.height / 2 + viewState.offsetY;

    // Clear with black
    ctx.fillStyle = COLORS.black;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw connections between agents of same sphere (subtle)
    ctx.globalAlpha = 0.1;
    agents.forEach((agent, i) => {
      const nearbyAgents = agents.filter(
        (a, j) =>
          j !== i &&
          a.sphereKey === agent.sphereKey &&
          Math.hypot(a.x - agent.x, a.y - agent.y) < 60
      );

      nearbyAgents.forEach(nearby => {
        ctx.beginPath();
        ctx.moveTo(centerX + agent.x * viewState.zoom, centerY + agent.y * viewState.zoom);
        ctx.lineTo(centerX + nearby.x * viewState.zoom, centerY + nearby.y * viewState.zoom);
        ctx.strokeStyle = agent.color;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      });
    });
    ctx.globalAlpha = 1;

    // Draw agents
    agents.forEach(agent => {
      // Gentle floating animation
      const floatX = Math.sin(time + agent.id * 0.1) * 2;
      const floatY = Math.cos(time + agent.id * 0.15) * 2;

      const x = centerX + (agent.baseX + floatX) * viewState.zoom;
      const y = centerY + (agent.baseY + floatY) * viewState.zoom;

      // Update agent position for hover detection
      agent.x = agent.baseX + floatX;
      agent.y = agent.baseY + floatY;

      // Glow effect for hovered agent
      if (hoveredAgent?.id === agent.id) {
        const glowGradient = ctx.createRadialGradient(x, y, 0, x, y, 30);
        glowGradient.addColorStop(0, agent.color);
        glowGradient.addColorStop(1, 'transparent');
        ctx.beginPath();
        ctx.arc(x, y, 30, 0, Math.PI * 2);
        ctx.fillStyle = glowGradient;
        ctx.fill();
      }

      // Draw agent point
      ctx.beginPath();
      ctx.arc(x, y, agent.size * viewState.zoom, 0, Math.PI * 2);
      ctx.fillStyle = hoveredAgent?.id === agent.id ? COLORS.white : agent.color;
      ctx.fill();
    });

    // Draw sphere labels if zoomed out
    if (viewState.zoom <= 1) {
      const sphereKeys = Object.keys(sphereGroups);
      const totalSpheres = sphereKeys.length || 1;

      sphereKeys.forEach((sphereKey, sphereIndex) => {
        const group = sphereGroups[sphereKey];
        const angle = (sphereIndex / totalSpheres) * Math.PI * 2;
        const labelRadius = 320;

        const x = centerX + Math.cos(angle) * labelRadius * viewState.zoom;
        const y = centerY + Math.sin(angle) * labelRadius * viewState.zoom;

        ctx.font = '12px monospace';
        ctx.fillStyle = group.color;
        ctx.textAlign = 'center';
        ctx.fillText(group.name, x, y);
        ctx.font = '10px monospace';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.fillText(`${group.count} agents`, x, y + 14);
      });
    }

    // Center indicator
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
    ctx.fillStyle = COLORS.gold;
    ctx.fill();

    // Total count - use real count from API
    ctx.font = '14px monospace';
    ctx.fillStyle = COLORS.white;
    ctx.textAlign = 'center';
    ctx.fillText(`L'ESSAIM: ${totalAgents} AGENTS`, centerX, canvas.height - 40);

    // Status indicator
    ctx.fillStyle = loading ? COLORS.gold : (error ? '#FF6B6B' : COLORS.cobalt);
    ctx.fillText(loading ? 'Chargement...' : (error ? 'Mode Hors-ligne' : 'NOVA-999 Hz'), centerX, canvas.height - 20);

    animationRef.current = requestAnimationFrame(animate);
  }, [agents, viewState, hoveredAgent, sphereGroups, totalAgents, loading, error]);

  // Setup canvas and animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate]);

  // Mouse interaction
  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      setMousePos({ x, y });

      const centerX = canvas.width / 2 + viewState.offsetX;
      const centerY = canvas.height / 2 + viewState.offsetY;

      // Find hovered agent
      const hovered = agents.find(agent => {
        const agentX = centerX + agent.x * viewState.zoom;
        const agentY = centerY + agent.y * viewState.zoom;
        const distance = Math.hypot(x - agentX, y - agentY);
        return distance < 15;
      });

      setHoveredAgent(hovered || null);
    },
    [agents, viewState]
  );

  // Click to navigate to sphere
  const handleClick = useCallback(() => {
    if (hoveredAgent) {
      const path = SPHERE_PATHS[hoveredAgent.sphereKey] || '/dashboard';
      navigate(path);
    }
  }, [hoveredAgent, navigate]);

  // Wheel zoom
  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const zoomDelta = e.deltaY > 0 ? 0.9 : 1.1;
    setViewState(prev => ({
      ...prev,
      zoom: Math.max(0.5, Math.min(3, prev.zoom * zoomDelta)),
    }));
  }, []);

  // Gesture navigation (swipe)
  const touchStartRef = useRef({ x: 0, y: 0 });

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      touchStartRef.current = {
        x: e.touches[0].clientX,
        y: e.touches[0].clientY,
      };
    }
  }, []);

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      const deltaX = e.touches[0].clientX - touchStartRef.current.x;
      const deltaY = e.touches[0].clientY - touchStartRef.current.y;

      setViewState(prev => ({
        ...prev,
        offsetX: prev.offsetX + deltaX * 0.5,
        offsetY: prev.offsetY + deltaY * 0.5,
      }));

      touchStartRef.current = {
        x: e.touches[0].clientX,
        y: e.touches[0].clientY,
      };
    }
  }, []);

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: COLORS.black,
        overflow: 'hidden',
        cursor: hoveredAgent ? 'pointer' : 'default',
      }}
    >
      <canvas
        ref={canvasRef}
        style={{ display: 'block', width: '100%', height: '100%' }}
        onMouseMove={handleMouseMove}
        onClick={handleClick}
        onWheel={handleWheel}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
      />

      {/* Agent tooltip */}
      {hoveredAgent && (
        <div
          style={{
            position: 'absolute',
            left: mousePos.x + 15,
            top: mousePos.y - 30,
            backgroundColor: 'rgba(0, 0, 0, 0.95)',
            border: `1px solid ${hoveredAgent.color}`,
            padding: '10px 14px',
            borderRadius: '6px',
            pointerEvents: 'none',
            maxWidth: '280px',
          }}
        >
          <div style={{ color: hoveredAgent.color, fontFamily: 'monospace', fontSize: '13px', fontWeight: 'bold' }}>
            {hoveredAgent.displayName}
          </div>
          <div style={{ color: 'rgba(255, 255, 255, 0.6)', fontFamily: 'monospace', fontSize: '10px', marginTop: '4px' }}>
            {sphereGroups[hoveredAgent.sphereKey]?.name || hoveredAgent.sphereKey}
          </div>
          <div style={{
            color: 'rgba(255, 255, 255, 0.4)',
            fontFamily: 'monospace',
            fontSize: '9px',
            marginTop: '6px',
            display: 'flex',
            flexWrap: 'wrap',
            gap: '4px'
          }}>
            {hoveredAgent.capabilities.slice(0, 3).map(cap => (
              <span key={cap} style={{
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                padding: '2px 6px',
                borderRadius: '3px'
              }}>
                {cap}
              </span>
            ))}
          </div>
          {hoveredAgent.requiresHumanGate && (
            <div style={{
              color: COLORS.gold,
              fontFamily: 'monospace',
              fontSize: '9px',
              marginTop: '6px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              🔐 Approbation humaine requise
            </div>
          )}
        </div>
      )}

      {/* Navigation hint */}
      <div
        style={{
          position: 'absolute',
          top: 20,
          left: 20,
          color: 'rgba(255, 255, 255, 0.3)',
          fontFamily: 'monospace',
          fontSize: '12px',
        }}
      >
        Scroll: Zoom | Drag: Pan | Click: Select
      </div>

      {/* Back to Sceau */}
      <button
        onClick={() => navigate('/')}
        style={{
          position: 'absolute',
          top: 20,
          right: 20,
          background: 'transparent',
          border: `1px solid ${COLORS.cobalt}`,
          color: COLORS.cobalt,
          padding: '8px 16px',
          fontFamily: 'monospace',
          fontSize: '12px',
          cursor: 'pointer',
          borderRadius: '4px',
        }}
      >
        LE SCEAU
      </button>

      {/* Module navigation */}
      <div
        style={{
          position: 'absolute',
          bottom: 80,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: '20px',
        }}
      >
        {[
          { path: '/genie', label: 'GENIE', color: '#FFD700' },
          { path: '/alchimie', label: 'ALCHIMIE', color: '#9B59B6' },
          { path: '/flux', label: 'FLUX', color: '#00CED1' },
          { path: '/sante', label: 'SANTE', color: '#E74C3C' },
        ].map(module => (
          <button
            key={module.path}
            onClick={() => navigate(module.path)}
            style={{
              background: 'transparent',
              border: `1px solid ${module.color}`,
              color: module.color,
              padding: '8px 16px',
              fontFamily: 'monospace',
              fontSize: '11px',
              cursor: 'pointer',
              borderRadius: '4px',
              letterSpacing: '0.1em',
            }}
          >
            {module.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Essaim;
