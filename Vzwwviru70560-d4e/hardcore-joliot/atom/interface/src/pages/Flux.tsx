/**
 * FLUX - Module Economie / Transport
 * ====================================
 *
 * CANON AT·OM - Terminal Economie
 * Chemin: /flux
 *
 * Graphiques de circulation de valeur.
 * PAS de colonnes debit/credit, mais des flux de particules.
 *
 * PHILOSOPHIE:
 * L'argent est de l'energie en mouvement.
 * Pas de "dette", mais des "flux".
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Breadcrumbs } from '@/components/Breadcrumbs';

// =============================================================================
// CONSTANTS
// =============================================================================

const COLORS = {
  black: '#000000',
  gold: '#D4AF37',
  cobalt: '#0047AB',
  white: '#FFFFFF',
  cyan: '#00CED1',
  green: '#27AE60',
  red: '#E74C3C',
};

// Flow types (NOT debit/credit - FLUX)
const FLOW_TYPES = [
  { id: 'incoming', name: 'Entrant', color: COLORS.green },
  { id: 'outgoing', name: 'Sortant', color: COLORS.cyan },
  { id: 'circular', name: 'Circulaire', color: COLORS.gold },
];

// =============================================================================
// TYPES
// =============================================================================

interface Particle {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  type: 'incoming' | 'outgoing' | 'circular';
  size: number;
  life: number;
}

interface FlowNode {
  id: string;
  name: string;
  x: number;
  y: number;
  value: number;
  color: string;
}

// =============================================================================
// FLUX COMPONENT
// =============================================================================

export function Flux() {
  const navigate = useNavigate();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [particles, setParticles] = useState<Particle[]>([]);
  const [viewMode, setViewMode] = useState<'particles' | 'network' | 'pulse'>('particles');

  // Flow nodes
  const [nodes] = useState<FlowNode[]>([
    { id: 'center', name: 'VOUS', x: 0.5, y: 0.5, value: 1000, color: COLORS.gold },
    { id: 'work', name: 'Travail', x: 0.2, y: 0.3, value: 500, color: COLORS.green },
    { id: 'creation', name: 'Creation', x: 0.8, y: 0.3, value: 300, color: COLORS.cyan },
    { id: 'community', name: 'Communaute', x: 0.2, y: 0.7, value: 200, color: '#9B59B6' },
    { id: 'nature', name: 'Nature', x: 0.8, y: 0.7, value: 150, color: '#27AE60' },
  ]);

  // Generate particles
  const generateParticle = useCallback((type: 'incoming' | 'outgoing' | 'circular'): Particle => {
    const canvas = canvasRef.current;
    const centerX = canvas ? canvas.width / 2 : 400;
    const centerY = canvas ? canvas.height / 2 : 300;

    if (type === 'incoming') {
      const angle = Math.random() * Math.PI * 2;
      const distance = 400;
      return {
        id: Date.now() + Math.random(),
        x: centerX + Math.cos(angle) * distance,
        y: centerY + Math.sin(angle) * distance,
        vx: -Math.cos(angle) * 2,
        vy: -Math.sin(angle) * 2,
        type,
        size: 3 + Math.random() * 2,
        life: 1,
      };
    } else if (type === 'outgoing') {
      const angle = Math.random() * Math.PI * 2;
      return {
        id: Date.now() + Math.random(),
        x: centerX,
        y: centerY,
        vx: Math.cos(angle) * 2,
        vy: Math.sin(angle) * 2,
        type,
        size: 3 + Math.random() * 2,
        life: 1,
      };
    } else {
      // Circular
      const angle = Math.random() * Math.PI * 2;
      const radius = 100 + Math.random() * 100;
      return {
        id: Date.now() + Math.random(),
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius,
        vx: -Math.sin(angle) * 1.5,
        vy: Math.cos(angle) * 1.5,
        type,
        size: 2 + Math.random() * 2,
        life: 1,
      };
    }
  }, []);

  // Particle animation
  useEffect(() => {
    if (viewMode !== 'particles') return;

    const interval = setInterval(() => {
      // Add new particles
      const types: ('incoming' | 'outgoing' | 'circular')[] = ['incoming', 'outgoing', 'circular'];
      const newParticle = generateParticle(types[Math.floor(Math.random() * types.length)]);

      setParticles(prev => {
        const updated = prev
          .map(p => ({
            ...p,
            x: p.x + p.vx,
            y: p.y + p.vy,
            life: p.life - 0.01,
          }))
          .filter(p => p.life > 0);

        if (updated.length < 100) {
          return [...updated, newParticle];
        }
        return updated;
      });
    }, 50);

    return () => clearInterval(interval);
  }, [viewMode, generateParticle]);

  // Canvas animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const animate = () => {
      ctx.fillStyle = COLORS.black;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      if (viewMode === 'particles') {
        // Draw particles
        particles.forEach(p => {
          const flowType = FLOW_TYPES.find(f => f.id === p.type);
          if (!flowType) return;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
          ctx.fillStyle = flowType.color + Math.floor(p.life * 255).toString(16).padStart(2, '0');
          ctx.fill();
        });

        // Central node
        const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 60);
        gradient.addColorStop(0, COLORS.gold);
        gradient.addColorStop(0.5, COLORS.gold + '60');
        gradient.addColorStop(1, 'transparent');

        ctx.beginPath();
        ctx.arc(centerX, centerY, 60, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();

        ctx.font = 'bold 16px monospace';
        ctx.fillStyle = COLORS.black;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('FLUX', centerX, centerY);

      } else if (viewMode === 'network') {
        // Draw network connections
        nodes.forEach(node => {
          if (node.id === 'center') return;

          const fromX = nodes[0].x * canvas.width;
          const fromY = nodes[0].y * canvas.height;
          const toX = node.x * canvas.width;
          const toY = node.y * canvas.height;

          // Animated flow line
          ctx.beginPath();
          ctx.moveTo(fromX, fromY);
          ctx.lineTo(toX, toY);
          ctx.strokeStyle = node.color + '40';
          ctx.lineWidth = 2;
          ctx.stroke();

          // Flow particles on line
          const progress = (time % 100) / 100;
          const particleX = fromX + (toX - fromX) * progress;
          const particleY = fromY + (toY - fromY) * progress;

          ctx.beginPath();
          ctx.arc(particleX, particleY, 5, 0, Math.PI * 2);
          ctx.fillStyle = node.color;
          ctx.fill();
        });

        // Draw nodes
        nodes.forEach(node => {
          const x = node.x * canvas.width;
          const y = node.y * canvas.height;
          const radius = node.id === 'center' ? 50 : 30;

          ctx.beginPath();
          ctx.arc(x, y, radius, 0, Math.PI * 2);
          ctx.fillStyle = node.color + '80';
          ctx.fill();
          ctx.strokeStyle = node.color;
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.font = '12px monospace';
          ctx.fillStyle = COLORS.white;
          ctx.textAlign = 'center';
          ctx.fillText(node.name, x, y - radius - 10);

          ctx.font = '14px monospace';
          ctx.fillText(`${node.value}`, x, y + 5);
        });

      } else if (viewMode === 'pulse') {
        // Pulse visualization
        const pulseCount = 5;
        for (let i = 0; i < pulseCount; i++) {
          const pulsePhase = ((time + i * 20) % 100) / 100;
          const pulseRadius = pulsePhase * Math.min(canvas.width, canvas.height) * 0.4;
          const opacity = 1 - pulsePhase;

          ctx.beginPath();
          ctx.arc(centerX, centerY, pulseRadius, 0, Math.PI * 2);
          ctx.strokeStyle = COLORS.cyan + Math.floor(opacity * 100).toString(16).padStart(2, '0');
          ctx.lineWidth = 3;
          ctx.stroke();
        }

        // Center
        ctx.beginPath();
        ctx.arc(centerX, centerY, 40, 0, Math.PI * 2);
        ctx.fillStyle = COLORS.gold;
        ctx.fill();

        ctx.font = 'bold 18px monospace';
        ctx.fillStyle = COLORS.black;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('999', centerX, centerY);

        ctx.font = '12px monospace';
        ctx.fillStyle = COLORS.gold;
        ctx.fillText('Hz', centerX, centerY + 60);
      }

      time++;
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [viewMode, particles, nodes]);

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
    }}>
      {/* Breadcrumbs */}
      <Breadcrumbs />

      {/* Header - offset for breadcrumbs */}
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
            color: COLORS.cyan,
            fontFamily: 'monospace',
            fontSize: '18px',
            letterSpacing: '0.2em',
          }}>
            FLUX DE VALEUR
          </h1>
        </div>

        {/* View switcher */}
        <div style={{ display: 'flex', gap: '10px' }}>
          {(['particles', 'network', 'pulse'] as const).map(mode => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                backgroundColor: viewMode === mode ? COLORS.cyan + '30' : 'transparent',
                border: `1px solid ${viewMode === mode ? COLORS.cyan : 'rgba(255, 255, 255, 0.2)'}`,
                color: viewMode === mode ? COLORS.cyan : 'rgba(255, 255, 255, 0.5)',
                padding: '8px 16px',
                fontFamily: 'monospace',
                fontSize: '11px',
                cursor: 'pointer',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              {mode === 'particles' ? 'PARTICULES' : mode === 'network' ? 'RESEAU' : 'PULSE'}
            </button>
          ))}
        </div>
      </header>

      {/* Main canvas */}
      <canvas
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight - 150}
        style={{ flex: 1 }}
      />

      {/* Legend */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '30px',
        padding: '20px',
      }}>
        {FLOW_TYPES.map(flow => (
          <div key={flow.id} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              backgroundColor: flow.color,
            }} />
            <span style={{
              color: flow.color,
              fontFamily: 'monospace',
              fontSize: '12px',
            }}>
              {flow.name}
            </span>
          </div>
        ))}
      </div>

      {/* Philosophy note */}
      <div style={{
        textAlign: 'center',
        padding: '10px 20px 20px',
        color: 'rgba(255, 255, 255, 0.3)',
        fontFamily: 'monospace',
        fontSize: '11px',
        letterSpacing: '0.2em',
      }}>
        L'ARGENT EST DE L'ENERGIE EN MOUVEMENT | PAS DE DETTE, MAIS DES FLUX
      </div>
    </div>
  );
}

export default Flux;
