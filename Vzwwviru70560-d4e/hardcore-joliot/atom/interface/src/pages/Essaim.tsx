/**
 * L'ESSAIM - HUB DES 350 AGENTS
 * ==============================
 *
 * CANON AT·OM - Le Hub des 350 Agents
 * Chemin: /essaim ou /swarm
 *
 * Contenu: Visualisation dynamique des 350 points de lumiere.
 * Fonctionnalite: Vue d'ensemble. Possibilite de "zoomer" sur un groupe
 * d'agents (ex: les 25 agents de l'Environnement).
 *
 * VERIFICATION:
 * - Chaque point doit etre cliquable
 * - Reveler sa fonction specifique sans texte lourd
 * - Navigation gestuelle (swipe pour naviguer)
 */

import React, { useState, useRef, useCallback, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';

// =============================================================================
// CONSTANTS - Canon AT·OM
// =============================================================================

const COLORS = {
  black: '#000000',
  gold: '#D4AF37',
  cobalt: '#0047AB',
  white: '#FFFFFF',
};

// Agent distribution per sphere (350 total)
const SPHERES = {
  personal: { count: 28, color: '#4A90D9', name: 'Personnel', icon: 'user', path: '/sphere/personal' },
  business: { count: 43, color: '#D4AF37', name: 'Entreprise', icon: 'briefcase', path: '/sphere/business' },
  government: { count: 18, color: '#8B4513', name: 'Gouvernement', icon: 'landmark', path: '/sphere/government' },
  creative_studio: { count: 42, color: '#9B59B6', name: 'Creation', icon: 'palette', path: '/sphere/creative' },
  community: { count: 12, color: '#27AE60', name: 'Communaute', icon: 'users', path: '/sphere/community' },
  social_media: { count: 15, color: '#3498DB', name: 'Social', icon: 'share', path: '/sphere/social' },
  entertainment: { count: 8, color: '#F39C12', name: 'Divertissement', icon: 'gamepad', path: '/sphere/entertainment' },
  my_team: { count: 35, color: '#E74C3C', name: 'Mon Equipe', icon: 'users-cog', path: '/sphere/team' },
  scholar: { count: 25, color: '#1ABC9C', name: 'Academique', icon: 'graduation-cap', path: '/sphere/scholar' },
  transport: { count: 50, color: '#00CED1', name: 'Transport', icon: 'car', path: '/flux' },
  societal: { count: 20, color: '#FF6B6B', name: 'Societal', icon: 'balance-scale', path: '/sphere/societal' },
  environment: { count: 25, color: '#2ECC71', name: 'Environnement', icon: 'leaf', path: '/sphere/environment' },
  privacy: { count: 8, color: '#9B59B6', name: 'Vie Privee', icon: 'shield', path: '/sphere/privacy' },
  jeunesse: { count: 15, color: '#FFD700', name: 'Jeunesse', icon: 'child', path: '/genie' },
  dashboard: { count: 6, color: '#607D8B', name: 'Dashboard', icon: 'chart-pie', path: '/dashboard' },
};

const TOTAL_AGENTS = 350;

// =============================================================================
// TYPES
// =============================================================================

interface Agent {
  id: number;
  sphereKey: string;
  x: number;
  y: number;
  baseX: number;
  baseY: number;
  size: number;
  color: string;
  name: string;
  isHovered: boolean;
}

interface ViewState {
  zoom: number;
  offsetX: number;
  offsetY: number;
  focusedSphere: string | null;
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

  const [hoveredAgent, setHoveredAgent] = useState<Agent | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Generate all agents
  const agents = useMemo(() => {
    const result: Agent[] = [];
    let agentId = 0;

    const sphereKeys = Object.keys(SPHERES);
    const totalSpheres = sphereKeys.length;

    sphereKeys.forEach((sphereKey, sphereIndex) => {
      const sphere = SPHERES[sphereKey as keyof typeof SPHERES];
      const sphereAngle = (sphereIndex / totalSpheres) * Math.PI * 2;
      const sphereRadius = 250;

      // Sphere center position
      const sphereCenterX = Math.cos(sphereAngle) * sphereRadius;
      const sphereCenterY = Math.sin(sphereAngle) * sphereRadius;

      // Distribute agents within sphere cluster
      for (let i = 0; i < sphere.count; i++) {
        const agentAngle = (i / sphere.count) * Math.PI * 2;
        const agentRadius = 30 + Math.random() * 50;

        const x = sphereCenterX + Math.cos(agentAngle) * agentRadius;
        const y = sphereCenterY + Math.sin(agentAngle) * agentRadius;

        result.push({
          id: agentId++,
          sphereKey,
          x,
          y,
          baseX: x,
          baseY: y,
          size: 3 + Math.random() * 2,
          color: sphere.color,
          name: `${sphere.name} Agent ${i + 1}`,
          isHovered: false,
        });
      }
    });

    return result;
  }, []);

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
      const sphereKeys = Object.keys(SPHERES);
      const totalSpheres = sphereKeys.length;

      sphereKeys.forEach((sphereKey, sphereIndex) => {
        const sphere = SPHERES[sphereKey as keyof typeof SPHERES];
        const angle = (sphereIndex / totalSpheres) * Math.PI * 2;
        const labelRadius = 320;

        const x = centerX + Math.cos(angle) * labelRadius * viewState.zoom;
        const y = centerY + Math.sin(angle) * labelRadius * viewState.zoom;

        ctx.font = '12px monospace';
        ctx.fillStyle = sphere.color;
        ctx.textAlign = 'center';
        ctx.fillText(sphere.name, x, y);
        ctx.font = '10px monospace';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.fillText(`${sphere.count} agents`, x, y + 14);
      });
    }

    // Center indicator
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
    ctx.fillStyle = COLORS.gold;
    ctx.fill();

    // Total count
    ctx.font = '14px monospace';
    ctx.fillStyle = COLORS.white;
    ctx.textAlign = 'center';
    ctx.fillText(`L'ESSAIM: ${TOTAL_AGENTS} AGENTS`, centerX, canvas.height - 40);

    // Frequency indicator
    ctx.fillStyle = COLORS.cobalt;
    ctx.fillText('999 Hz', centerX, canvas.height - 20);

    animationRef.current = requestAnimationFrame(animate);
  }, [agents, viewState, hoveredAgent]);

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
      const sphere = SPHERES[hoveredAgent.sphereKey as keyof typeof SPHERES];
      navigate(sphere.path);
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
            backgroundColor: 'rgba(0, 0, 0, 0.9)',
            border: `1px solid ${hoveredAgent.color}`,
            padding: '8px 12px',
            borderRadius: '4px',
            pointerEvents: 'none',
          }}
        >
          <div style={{ color: hoveredAgent.color, fontFamily: 'monospace', fontSize: '12px' }}>
            {hoveredAgent.name}
          </div>
          <div style={{ color: 'rgba(255, 255, 255, 0.5)', fontFamily: 'monospace', fontSize: '10px', marginTop: '4px' }}>
            {SPHERES[hoveredAgent.sphereKey as keyof typeof SPHERES].name}
          </div>
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
