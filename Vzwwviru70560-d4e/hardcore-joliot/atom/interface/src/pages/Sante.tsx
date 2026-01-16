/**
 * SANTE - Module Guerison
 * ========================
 *
 * CANON AT·OM - Terminal Guerison
 * Chemin: /sante
 *
 * Bio-feedback en temps reel, guides de conditionnement physique.
 *
 * PHILOSOPHIE:
 * La sante est equilibre, pas absence de maladie.
 * Le corps sait guerir quand on lui donne les bonnes frequences.
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

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
  blue: '#3498DB',
};

// Body systems
const BODY_SYSTEMS = [
  { id: 'heart', name: 'Cardiaque', icon: '❤️', color: '#E74C3C', frequency: 528 },
  { id: 'lungs', name: 'Respiratoire', icon: '🫁', color: '#3498DB', frequency: 639 },
  { id: 'brain', name: 'Neuronal', icon: '🧠', color: '#9B59B6', frequency: 852 },
  { id: 'gut', name: 'Digestif', icon: '🌀', color: '#F39C12', frequency: 432 },
  { id: 'immune', name: 'Immunitaire', icon: '🛡️', color: '#27AE60', frequency: 741 },
  { id: 'energy', name: 'Energetique', icon: '⚡', color: '#D4AF37', frequency: 963 },
];

// Wellness indicators
const WELLNESS_METRICS = [
  { id: 'energy', name: 'Energie', value: 75 },
  { id: 'calm', name: 'Calme', value: 60 },
  { id: 'focus', name: 'Focus', value: 80 },
  { id: 'vitality', name: 'Vitalite', value: 70 },
];

// =============================================================================
// SANTE COMPONENT
// =============================================================================

export function Sante() {
  const navigate = useNavigate();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [viewMode, setViewMode] = useState<'biofeedback' | 'systems' | 'breathing'>('biofeedback');
  const [selectedSystem, setSelectedSystem] = useState<string | null>(null);
  const [breathPhase, setBreathPhase] = useState<'inhale' | 'hold' | 'exhale'>('inhale');
  const [breathTimer, setBreathTimer] = useState(0);

  // Simulated heart rate
  const [heartRate, setHeartRate] = useState(72);

  // Heart rate simulation
  useEffect(() => {
    if (viewMode !== 'biofeedback') return;

    const interval = setInterval(() => {
      setHeartRate(prev => {
        const change = (Math.random() - 0.5) * 4;
        return Math.max(60, Math.min(100, prev + change));
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [viewMode]);

  // Breathing exercise
  useEffect(() => {
    if (viewMode !== 'breathing') return;

    const cycleTime = {
      inhale: 4000,
      hold: 4000,
      exhale: 4000,
    };

    const interval = setInterval(() => {
      setBreathTimer(prev => {
        const newTime = prev + 100;
        const currentCycleTime = cycleTime[breathPhase];

        if (newTime >= currentCycleTime) {
          // Move to next phase
          if (breathPhase === 'inhale') setBreathPhase('hold');
          else if (breathPhase === 'hold') setBreathPhase('exhale');
          else setBreathPhase('inhale');
          return 0;
        }
        return newTime;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [viewMode, breathPhase]);

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

      if (viewMode === 'biofeedback') {
        // Heart rate wave
        ctx.beginPath();
        ctx.strokeStyle = COLORS.red;
        ctx.lineWidth = 2;

        for (let x = 0; x < canvas.width; x++) {
          const progress = (x + time * 2) % canvas.width;
          let y = centerY;

          // ECG-like pattern
          const phase = (progress % 100) / 100;
          if (phase < 0.1) {
            y = centerY;
          } else if (phase < 0.15) {
            y = centerY - 50 * Math.sin((phase - 0.1) * 20 * Math.PI);
          } else if (phase < 0.25) {
            y = centerY + 100 * Math.sin((phase - 0.15) * 10 * Math.PI);
          } else if (phase < 0.35) {
            y = centerY - 30 * Math.sin((phase - 0.25) * 10 * Math.PI);
          } else {
            y = centerY;
          }

          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();

        // Heart rate display
        ctx.font = 'bold 72px monospace';
        ctx.fillStyle = COLORS.red;
        ctx.textAlign = 'center';
        ctx.fillText(Math.round(heartRate).toString(), centerX, centerY - 100);

        ctx.font = '16px monospace';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.fillText('BPM', centerX, centerY - 60);

        // Wellness metrics
        const metricsY = centerY + 100;
        const metricsSpacing = 120;
        const startX = centerX - (WELLNESS_METRICS.length - 1) * metricsSpacing / 2;

        WELLNESS_METRICS.forEach((metric, i) => {
          const x = startX + i * metricsSpacing;

          // Background arc
          ctx.beginPath();
          ctx.arc(x, metricsY, 40, Math.PI * 0.75, Math.PI * 2.25);
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
          ctx.lineWidth = 8;
          ctx.stroke();

          // Value arc
          const valueAngle = Math.PI * 0.75 + (metric.value / 100) * Math.PI * 1.5;
          ctx.beginPath();
          ctx.arc(x, metricsY, 40, Math.PI * 0.75, valueAngle);
          ctx.strokeStyle = metric.value > 70 ? COLORS.green : metric.value > 40 ? COLORS.gold : COLORS.red;
          ctx.lineWidth = 8;
          ctx.lineCap = 'round';
          ctx.stroke();

          // Value text
          ctx.font = 'bold 20px monospace';
          ctx.fillStyle = COLORS.white;
          ctx.textAlign = 'center';
          ctx.fillText(metric.value.toString(), x, metricsY + 5);

          // Label
          ctx.font = '10px monospace';
          ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
          ctx.fillText(metric.name, x, metricsY + 60);
        });

      } else if (viewMode === 'systems') {
        // Body systems visualization
        BODY_SYSTEMS.forEach((system, i) => {
          const angle = (i / BODY_SYSTEMS.length) * Math.PI * 2 - Math.PI / 2;
          const radius = 180;
          const x = centerX + Math.cos(angle) * radius;
          const y = centerY + Math.sin(angle) * radius;

          const isSelected = selectedSystem === system.id;

          // Connection to center
          ctx.beginPath();
          ctx.moveTo(centerX, centerY);
          ctx.lineTo(x, y);
          ctx.strokeStyle = isSelected ? system.color : system.color + '40';
          ctx.lineWidth = isSelected ? 3 : 1;
          ctx.stroke();

          // System node
          const nodeRadius = isSelected ? 50 : 40;
          const gradient = ctx.createRadialGradient(x, y, 0, x, y, nodeRadius);
          gradient.addColorStop(0, system.color);
          gradient.addColorStop(0.7, system.color + '80');
          gradient.addColorStop(1, 'transparent');

          ctx.beginPath();
          ctx.arc(x, y, nodeRadius, 0, Math.PI * 2);
          ctx.fillStyle = gradient;
          ctx.fill();

          // Icon
          ctx.font = `${isSelected ? 30 : 24}px serif`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(system.icon, x, y);

          // Name and frequency
          ctx.font = '10px monospace';
          ctx.fillStyle = system.color;
          ctx.fillText(system.name, x, y + nodeRadius + 15);
          ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
          ctx.fillText(`${system.frequency} Hz`, x, y + nodeRadius + 28);
        });

        // Center - body silhouette
        ctx.font = '60px serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🧍', centerX, centerY);

      } else if (viewMode === 'breathing') {
        // Breathing visualization
        const cycleTime = 4000;
        const progress = breathTimer / cycleTime;

        let breathSize: number;
        if (breathPhase === 'inhale') {
          breathSize = 50 + progress * 100;
        } else if (breathPhase === 'hold') {
          breathSize = 150;
        } else {
          breathSize = 150 - progress * 100;
        }

        // Breathing circle
        const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, breathSize);
        gradient.addColorStop(0, COLORS.blue);
        gradient.addColorStop(0.5, COLORS.blue + '60');
        gradient.addColorStop(1, 'transparent');

        ctx.beginPath();
        ctx.arc(centerX, centerY, breathSize, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();

        // Breathing ring
        ctx.beginPath();
        ctx.arc(centerX, centerY, breathSize + 20, 0, Math.PI * 2);
        ctx.strokeStyle = COLORS.blue + '40';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Phase text
        ctx.font = 'bold 24px monospace';
        ctx.fillStyle = COLORS.white;
        ctx.textAlign = 'center';
        ctx.fillText(
          breathPhase === 'inhale' ? 'INSPIREZ' : breathPhase === 'hold' ? 'RETENEZ' : 'EXPIREZ',
          centerX,
          centerY
        );

        // Timer
        ctx.font = '14px monospace';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.fillText(`${Math.ceil((cycleTime - breathTimer) / 1000)}s`, centerX, centerY + 30);

        // Instructions
        ctx.font = '12px monospace';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.fillText('Respiration 4-4-4', centerX, centerY + 200);
      }

      time++;
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [viewMode, heartRate, selectedSystem, breathPhase, breathTimer]);

  // Handle system click
  const handleCanvasClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    if (viewMode !== 'systems') return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Check which system was clicked
    BODY_SYSTEMS.forEach((system, i) => {
      const angle = (i / BODY_SYSTEMS.length) * Math.PI * 2 - Math.PI / 2;
      const radius = 180;
      const nodeX = centerX + Math.cos(angle) * radius;
      const nodeY = centerY + Math.sin(angle) * radius;

      const distance = Math.hypot(x - nodeX, y - nodeY);
      if (distance < 50) {
        setSelectedSystem(selectedSystem === system.id ? null : system.id);
      }
    });
  }, [viewMode, selectedSystem]);

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
      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '15px 30px',
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
            color: COLORS.red,
            fontFamily: 'monospace',
            fontSize: '18px',
            letterSpacing: '0.2em',
          }}>
            SANTE & GUERISON
          </h1>
        </div>

        {/* View switcher */}
        <div style={{ display: 'flex', gap: '10px' }}>
          {(['biofeedback', 'systems', 'breathing'] as const).map(mode => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                backgroundColor: viewMode === mode ? COLORS.red + '30' : 'transparent',
                border: `1px solid ${viewMode === mode ? COLORS.red : 'rgba(255, 255, 255, 0.2)'}`,
                color: viewMode === mode ? COLORS.red : 'rgba(255, 255, 255, 0.5)',
                padding: '8px 16px',
                fontFamily: 'monospace',
                fontSize: '11px',
                cursor: 'pointer',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              {mode === 'biofeedback' ? 'BIO-FEEDBACK' : mode === 'systems' ? 'SYSTEMES' : 'RESPIRATION'}
            </button>
          ))}
        </div>
      </header>

      {/* Main canvas */}
      <canvas
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight - 100}
        style={{ flex: 1, cursor: viewMode === 'systems' ? 'pointer' : 'default' }}
        onClick={handleCanvasClick}
      />

      {/* Philosophy note */}
      <div style={{
        textAlign: 'center',
        padding: '15px 20px',
        color: 'rgba(255, 255, 255, 0.3)',
        fontFamily: 'monospace',
        fontSize: '11px',
        letterSpacing: '0.2em',
      }}>
        LA SANTE EST EQUILIBRE | LE CORPS SAIT GUERIR
      </div>
    </div>
  );
}

export default Sante;
