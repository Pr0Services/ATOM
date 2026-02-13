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
import { prefersReducedMotion, isTouchDevice } from '@/styles/tokens';
import { Breadcrumbs } from '@/components/Breadcrumbs';

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
  const [reducedMotion, setReducedMotion] = useState(false);
  const [isTouch, setIsTouch] = useState(false);
  const [tappedAgent, setTappedAgent] = useState<VisualAgent | null>(null);

  // Detect user preferences
  useEffect(() => {
    setReducedMotion(prefersReducedMotion());
    setIsTouch(isTouchDevice());

    // Listen for changes
    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handleMotionChange = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    motionQuery.addEventListener('change', handleMotionChange);

    return () => motionQuery.removeEventListener('change', handleMotionChange);
  }, []);

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
      // Gentle floating animation (disabled if user prefers reduced motion)
      const floatX = reducedMotion ? 0 : Math.sin(time + agent.id * 0.1) * 2;
      const floatY = reducedMotion ? 0 : Math.cos(time + agent.id * 0.15) * 2;

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
  }, [agents, viewState, hoveredAgent, sphereGroups, totalAgents, loading, error, reducedMotion]);

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

  // Click to navigate to sphere (desktop: direct, touch: double-tap)
  const handleClick = useCallback((e: React.MouseEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = canvas.width / 2 + viewState.offsetX;
    const centerY = canvas.height / 2 + viewState.offsetY;

    // Find clicked agent
    const clickedAgent = agents.find(agent => {
      const agentX = centerX + agent.x * viewState.zoom;
      const agentY = centerY + agent.y * viewState.zoom;
      const distance = Math.hypot(x - agentX, y - agentY);
      return distance < 15;
    });

    if (isTouch) {
      // Touch: first tap shows tooltip, second tap navigates
      if (clickedAgent) {
        if (tappedAgent?.id === clickedAgent.id) {
          // Second tap - navigate
          const path = SPHERE_PATHS[clickedAgent.sphereKey] || '/dashboard';
          navigate(path);
        } else {
          // First tap - show tooltip
          setTappedAgent(clickedAgent);
          setMousePos({ x, y });
        }
      } else {
        // Tap outside - dismiss tooltip
        setTappedAgent(null);
      }
    } else {
      // Desktop: direct navigation
      if (hoveredAgent) {
        const path = SPHERE_PATHS[hoveredAgent.sphereKey] || '/dashboard';
        navigate(path);
      }
    }
  }, [hoveredAgent, tappedAgent, navigate, agents, viewState, isTouch]);

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
      {/* Breadcrumbs navigation */}
      <Breadcrumbs />

      <canvas
        ref={canvasRef}
        style={{ display: 'block', width: '100%', height: '100%' }}
        onMouseMove={handleMouseMove}
        onClick={handleClick}
        onWheel={handleWheel}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
      />

      {/* Agent tooltip - Works with hover (desktop) or tap (touch) */}
      {(() => {
        const activeAgent = isTouch ? tappedAgent : hoveredAgent;
        if (!activeAgent) return null;
        return (
          <div
            role="tooltip"
            aria-live="polite"
            style={{
              position: 'absolute',
              left: Math.min(mousePos.x + 15, window.innerWidth - 300),
              top: Math.max(mousePos.y - 30, 10),
              backgroundColor: 'rgba(0, 0, 0, 0.95)',
              border: `1px solid ${activeAgent.color}`,
              padding: '12px 16px',
              borderRadius: '8px',
              pointerEvents: isTouch ? 'auto' : 'none',
              maxWidth: '280px',
              zIndex: 100,
            }}
          >
            <div style={{ color: activeAgent.color, fontFamily: 'monospace', fontSize: '14px', fontWeight: 'bold' }}>
              {activeAgent.displayName}
            </div>
            <div style={{ color: 'rgba(255, 255, 255, 0.6)', fontFamily: 'monospace', fontSize: '11px', marginTop: '4px' }}>
              {sphereGroups[activeAgent.sphereKey]?.name || activeAgent.sphereKey}
            </div>
            <div style={{
              color: 'rgba(255, 255, 255, 0.4)',
              fontFamily: 'monospace',
              fontSize: '10px',
              marginTop: '8px',
              display: 'flex',
              flexWrap: 'wrap',
              gap: '4px'
            }}>
              {activeAgent.capabilities.slice(0, 3).map(cap => (
                <span key={cap} style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  padding: '3px 8px',
                  borderRadius: '4px'
                }}>
                  {cap}
                </span>
              ))}
            </div>
            {activeAgent.requiresHumanGate && (
              <div style={{
                color: COLORS.gold,
                fontFamily: 'monospace',
                fontSize: '10px',
                marginTop: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                🔐 Approbation humaine requise
              </div>
            )}
            {isTouch && (
              <div style={{
                color: 'rgba(255, 255, 255, 0.5)',
                fontFamily: 'monospace',
                fontSize: '10px',
                marginTop: '10px',
                textAlign: 'center',
                borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                paddingTop: '8px',
              }}>
                Tapez à nouveau pour ouvrir
              </div>
            )}
          </div>
        );
      })()}

      {/* Navigation hint */}
      <div
        style={{
          position: 'absolute',
          top: 20,
          left: 20,
          color: 'rgba(255, 255, 255, 0.4)',
          fontFamily: 'monospace',
          fontSize: '13px',
        }}
      >
        <div>Scroll: Zoom | Drag: Pan | Click: Select</div>
        <div style={{ marginTop: '8px', color: COLORS.gold }}>
          {totalAgents} agents · 9 sphères
        </div>
      </div>

      {/* Error banner with retry */}
      {error && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            backgroundColor: 'rgba(0, 0, 0, 0.9)',
            border: '1px solid #E74C3C',
            borderRadius: '12px',
            padding: '30px 40px',
            textAlign: 'center',
            maxWidth: '400px',
          }}
        >
          <div style={{ fontSize: '40px', marginBottom: '15px' }}>⚠️</div>
          <div style={{
            color: '#E74C3C',
            fontFamily: 'monospace',
            fontSize: '16px',
            fontWeight: 'bold',
            marginBottom: '10px',
          }}>
            CONNEXION PERDUE
          </div>
          <div style={{
            color: 'rgba(255, 255, 255, 0.6)',
            fontFamily: 'monospace',
            fontSize: '13px',
            marginBottom: '20px',
          }}>
            {error}
          </div>
          <button
            onClick={() => {
              setError(null);
              setLoading(true);
              agentsService.getAllAgents(true).then(agents => {
                setApiAgents(agents);
                setTotalAgents(agents.length);
                setLoading(false);
              }).catch(err => {
                setError('Impossible de se reconnecter. Vérifiez votre connexion.');
                setLoading(false);
              });
            }}
            style={{
              backgroundColor: COLORS.gold,
              border: 'none',
              color: COLORS.black,
              padding: '14px 28px',
              fontFamily: 'monospace',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer',
              borderRadius: '8px',
              letterSpacing: '0.1em',
            }}
          >
            🔄 RÉESSAYER
          </button>
        </div>
      )}

      {/* Loading overlay */}
      {loading && !error && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center',
          }}
        >
          <div style={{
            width: '60px',
            height: '60px',
            border: `3px solid ${COLORS.gold}30`,
            borderTop: `3px solid ${COLORS.gold}`,
            borderRadius: '50%',
            margin: '0 auto 20px',
            animation: 'spin 1s linear infinite',
          }} />
          <div style={{
            color: COLORS.gold,
            fontFamily: 'monospace',
            fontSize: '14px',
            letterSpacing: '0.2em',
          }}>
            CHARGEMENT DES AGENTS...
          </div>
        </div>
      )}

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        @media (prefers-reduced-motion: reduce) {
          * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
      `}</style>

      {/* Back to Sceau */}
      <button
        onClick={() => navigate('/')}
        aria-label="Retour au Sceau d'entrée"
        style={{
          position: 'absolute',
          top: 20,
          right: 20,
          background: 'transparent',
          border: `1px solid ${COLORS.cobalt}`,
          color: COLORS.cobalt,
          padding: '12px 24px',
          minHeight: '44px',
          fontFamily: 'monospace',
          fontSize: '14px',
          cursor: 'pointer',
          borderRadius: '6px',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = COLORS.cobalt + '20';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = 'transparent';
        }}
      >
        ← LE SCEAU
      </button>

      {/* Module navigation - Touch-friendly */}
      <nav
        aria-label="Navigation des modules"
        style={{
          position: 'absolute',
          bottom: 80,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: '12px',
          flexWrap: 'wrap',
          justifyContent: 'center',
          maxWidth: '90vw',
          padding: '0 20px',
        }}
      >
        {[
          { path: '/genie', label: 'GENIE', icon: '🎓', color: '#FFD700', desc: 'Education' },
          { path: '/alchimie', label: 'ALCHIMIE', icon: '⚗️', color: '#9B59B6', desc: 'Transmutation' },
          { path: '/flux', label: 'FLUX', icon: '💫', color: '#00CED1', desc: 'Économie' },
          { path: '/sante', label: 'SANTÉ', icon: '❤️', color: '#E74C3C', desc: 'Guérison' },
        ].map(module => (
          <button
            key={module.path}
            onClick={() => navigate(module.path)}
            aria-label={`${module.label} - ${module.desc}`}
            title={module.desc}
            style={{
              background: 'rgba(0, 0, 0, 0.5)',
              border: `2px solid ${module.color}`,
              color: module.color,
              padding: '14px 20px',
              minWidth: '100px',
              minHeight: '48px',
              fontFamily: 'monospace',
              fontSize: '13px',
              fontWeight: 'bold',
              cursor: 'pointer',
              borderRadius: '8px',
              letterSpacing: '0.1em',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = module.color + '30';
              e.currentTarget.style.transform = 'scale(1.05)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            <span role="img" aria-hidden="true">{module.icon}</span>
            {module.label}
          </button>
        ))}
      </nav>
    </div>
  );
}

export default Essaim;
