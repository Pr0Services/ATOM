/**
 * LE SCEAU DE L'ENGAGEMENT
 * =========================
 *
 * CANON AT·OM - L'Interface Maitresse (L'Entree)
 * Chemin: / (Root)
 *
 * Contenu: Le Sceau de l'Engagement en plein ecran.
 * Fonctionnalite: Validation Frequentielle.
 *
 * PAS de bouton "Login" classique.
 * Une interaction tactile prolongee qui declenche l'animation de l'Essaim
 * (le cercle qui explose en 226 points de lumiere - vrais agents).
 *
 * VERIFICATION:
 * - Fond noir #000000
 * - Animation fluide (60fps)
 * - Navigation gestuelle uniquement
 */

import React, { useState, useRef, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { agentsService } from '@/services/agents.service';

// =============================================================================
// CONSTANTS - Canon AT·OM
// =============================================================================

const COLORS = {
  black: '#000000',
  gold: '#D4AF37',
  cobalt: '#0047AB',
  white: '#FFFFFF',
};

const ACTIVATION_DURATION = 2000; // 2 seconds hold to activate
const TARGET_FREQUENCY = 999; // Hz - Perfect harmony

// =============================================================================
// TYPES
// =============================================================================

interface Particle {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  opacity: number;
  color: string;
}

interface SealState {
  isHolding: boolean;
  holdProgress: number;
  isActivated: boolean;
  frequency: number;
  particles: Particle[];
}

// =============================================================================
// LE SCEAU COMPONENT
// =============================================================================

export function LeSceau() {
  const navigate = useNavigate();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const holdTimerRef = useRef<NodeJS.Timeout>();
  const holdStartRef = useRef<number>(0);

  const [essaimSize, setEssaimSize] = useState(226); // Default, updated from API

  const [state, setState] = useState<SealState>({
    isHolding: false,
    holdProgress: 0,
    isActivated: false,
    frequency: 432, // Starting frequency
    particles: [],
  });

  // Fetch real agent count from API
  useEffect(() => {
    const fetchAgentCount = async () => {
      try {
        const stats = await agentsService.getStats();
        setEssaimSize(stats.total_agents);
        console.log(`[LeSceau] Essaim size: ${stats.total_agents} agents`);
      } catch {
        console.log('[LeSceau] Using default essaim size: 226');
      }
    };
    fetchAgentCount();
  }, []);

  // Generate particles for the explosion
  const generateParticles = useCallback((centerX: number, centerY: number): Particle[] => {
    return Array.from({ length: essaimSize }, (_, i) => {
      const angle = (i / essaimSize) * Math.PI * 2;
      const speed = 2 + Math.random() * 4;

      return {
        id: i,
        x: centerX,
        y: centerY,
        vx: Math.cos(angle) * speed + (Math.random() - 0.5),
        vy: Math.sin(angle) * speed + (Math.random() - 0.5),
        size: 2 + Math.random() * 3,
        opacity: 1,
        color: i % 7 === 0 ? COLORS.gold : i % 3 === 0 ? COLORS.cobalt : COLORS.white,
      };
    });
  }, [essaimSize]);

  // Animation loop
  const animate = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas with pure black
    ctx.fillStyle = COLORS.black;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    if (!state.isActivated) {
      // Draw the Seal (Le Sceau)
      const sealRadius = Math.min(canvas.width, canvas.height) * 0.15;
      const pulseRadius = sealRadius * (1 + 0.05 * Math.sin(Date.now() / 500));

      // Outer glow
      const gradient = ctx.createRadialGradient(
        centerX, centerY, 0,
        centerX, centerY, pulseRadius * 2
      );
      gradient.addColorStop(0, state.isHolding ? 'rgba(212, 175, 55, 0.3)' : 'rgba(0, 71, 171, 0.2)');
      gradient.addColorStop(0.5, 'rgba(0, 0, 0, 0.1)');
      gradient.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseRadius * 2, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();

      // Main seal circle
      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseRadius, 0, Math.PI * 2);
      ctx.strokeStyle = state.isHolding ? COLORS.gold : COLORS.cobalt;
      ctx.lineWidth = 3;
      ctx.stroke();

      // Progress ring
      if (state.isHolding && state.holdProgress > 0) {
        ctx.beginPath();
        ctx.arc(
          centerX, centerY, pulseRadius + 10,
          -Math.PI / 2,
          -Math.PI / 2 + (state.holdProgress / 100) * Math.PI * 2
        );
        ctx.strokeStyle = COLORS.gold;
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
        ctx.stroke();
      }

      // Inner symbol (AT·OM)
      ctx.font = `${sealRadius * 0.4}px "Courier New", monospace`;
      ctx.fillStyle = COLORS.white;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('AT·OM', centerX, centerY);

      // Frequency display
      ctx.font = '14px monospace';
      ctx.fillStyle = state.isHolding ? COLORS.gold : 'rgba(255, 255, 255, 0.5)';
      ctx.fillText(`${Math.floor(state.frequency)} Hz`, centerX, centerY + sealRadius * 0.6);

    } else {
      // Explosion animation - L'Essaim disperses
      setState(prev => {
        const newParticles = prev.particles.map(p => ({
          ...p,
          x: p.x + p.vx,
          y: p.y + p.vy,
          vx: p.vx * 0.99,
          vy: p.vy * 0.99,
          opacity: Math.max(0, p.opacity - 0.005),
        }));

        // Check if animation is complete
        const allFaded = newParticles.every(p => p.opacity <= 0);
        if (allFaded) {
          navigate('/essaim');
        }

        return { ...prev, particles: newParticles };
      });

      // Draw particles
      state.particles.forEach(p => {
        if (p.opacity <= 0) return;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color.replace(')', `, ${p.opacity})`).replace('rgb', 'rgba');
        ctx.fill();
      });

      // Central flash
      if (state.particles[0]?.opacity > 0.8) {
        const flashGradient = ctx.createRadialGradient(
          centerX, centerY, 0,
          centerX, centerY, 200
        );
        flashGradient.addColorStop(0, `rgba(212, 175, 55, ${state.particles[0].opacity})`);
        flashGradient.addColorStop(1, 'transparent');
        ctx.beginPath();
        ctx.arc(centerX, centerY, 200, 0, Math.PI * 2);
        ctx.fillStyle = flashGradient;
        ctx.fill();
      }
    }

    animationRef.current = requestAnimationFrame(animate);
  }, [state, navigate]);

  // Start animation
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

  // Handle touch/mouse hold
  const startHold = useCallback((e: React.TouchEvent | React.MouseEvent) => {
    e.preventDefault();
    holdStartRef.current = Date.now();

    setState(prev => ({ ...prev, isHolding: true, holdProgress: 0 }));

    // Update progress
    const updateProgress = () => {
      const elapsed = Date.now() - holdStartRef.current;
      const progress = Math.min(100, (elapsed / ACTIVATION_DURATION) * 100);
      const freq = 432 + (progress / 100) * (TARGET_FREQUENCY - 432);

      setState(prev => ({
        ...prev,
        holdProgress: progress,
        frequency: freq,
      }));

      if (progress >= 100) {
        // Activation!
        const canvas = canvasRef.current;
        if (canvas) {
          const particles = generateParticles(canvas.width / 2, canvas.height / 2);
          setState(prev => ({
            ...prev,
            isActivated: true,
            particles,
          }));
        }
      } else if (holdStartRef.current > 0) {
        holdTimerRef.current = setTimeout(updateProgress, 16);
      }
    };

    holdTimerRef.current = setTimeout(updateProgress, 16);
  }, [generateParticles]);

  const endHold = useCallback(() => {
    holdStartRef.current = 0;
    if (holdTimerRef.current) {
      clearTimeout(holdTimerRef.current);
    }

    if (!state.isActivated) {
      setState(prev => ({
        ...prev,
        isHolding: false,
        holdProgress: 0,
        frequency: 432,
      }));
    }
  }, [state.isActivated]);

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
        touchAction: 'none',
        cursor: 'none',
      }}
      onMouseDown={startHold}
      onMouseUp={endHold}
      onMouseLeave={endHold}
      onTouchStart={startHold}
      onTouchEnd={endHold}
    >
      <canvas
        ref={canvasRef}
        style={{
          display: 'block',
          width: '100%',
          height: '100%',
        }}
      />

      {/* Hidden instruction - appears after 3s of inactivity */}
      {!state.isHolding && !state.isActivated && (
        <div
          style={{
            position: 'absolute',
            bottom: '10%',
            left: '50%',
            transform: 'translateX(-50%)',
            color: 'rgba(255, 255, 255, 0.3)',
            fontSize: '14px',
            fontFamily: 'monospace',
            letterSpacing: '0.2em',
            animation: 'fadeIn 2s ease-in 3s forwards',
            opacity: 0,
          }}
        >
          MAINTENEZ POUR ACTIVER
        </div>
      )}

      {/* Frequency indicator */}
      {state.isHolding && !state.isActivated && (
        <div
          style={{
            position: 'absolute',
            top: '5%',
            right: '5%',
            color: state.frequency >= 999 ? COLORS.gold : COLORS.cobalt,
            fontSize: '24px',
            fontFamily: 'monospace',
            fontWeight: 'bold',
          }}
        >
          {Math.floor(state.frequency)} Hz
        </div>
      )}

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      `}</style>
    </div>
  );
}

export default LeSceau;
