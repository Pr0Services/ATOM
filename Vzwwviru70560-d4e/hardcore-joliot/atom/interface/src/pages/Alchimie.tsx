/**
 * ALCHIMIE - Module Transmutation
 * ================================
 *
 * CANON AT·OM - Terminal Transmutation
 * Chemin: /alchimie
 *
 * Visualiseur de frequences et de structures moleculaires.
 *
 * FONCTIONNALITES:
 * - Visualisation des frequences (432Hz - 999Hz)
 * - Structures moleculaires interactives
 * - Correspondances symboliques
 * - Transformation d'energie
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
  purple: '#9B59B6',
};

// Sacred frequencies
const FREQUENCIES = [
  { hz: 432, name: 'Harmonie Naturelle', color: '#27AE60' },
  { hz: 528, name: 'Transformation', color: '#3498DB' },
  { hz: 639, name: 'Connexion', color: '#E74C3C' },
  { hz: 741, name: 'Expression', color: '#9B59B6' },
  { hz: 852, name: 'Intuition', color: '#F39C12' },
  { hz: 963, name: 'Unite', color: '#1ABC9C' },
  { hz: 999, name: 'AT·OM Resonance', color: '#D4AF37' },
];

// Elements for molecular structures
const ELEMENTS = [
  { symbol: 'H', name: 'Hydrogene', color: '#FFFFFF' },
  { symbol: 'C', name: 'Carbone', color: '#333333' },
  { symbol: 'O', name: 'Oxygene', color: '#E74C3C' },
  { symbol: 'N', name: 'Azote', color: '#3498DB' },
  { symbol: 'Au', name: 'Or', color: '#D4AF37' },
  { symbol: 'Ag', name: 'Argent', color: '#C0C0C0' },
];

// =============================================================================
// ALCHIMIE COMPONENT
// =============================================================================

export function Alchimie() {
  const navigate = useNavigate();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const oscillatorRef = useRef<OscillatorNode | null>(null);

  const [currentFrequency, setCurrentFrequency] = useState(432);
  const [isPlaying, setIsPlaying] = useState(false);
  const [viewMode, setViewMode] = useState<'frequency' | 'molecular' | 'transmute'>('frequency');
  const [selectedElement, setSelectedElement] = useState<string | null>(null);

  // Initialize audio context
  useEffect(() => {
    audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    return () => {
      audioContextRef.current?.close();
    };
  }, []);

  // Play frequency
  const playFrequency = useCallback((hz: number) => {
    if (!audioContextRef.current) return;

    // Stop previous
    if (oscillatorRef.current) {
      oscillatorRef.current.stop();
      oscillatorRef.current.disconnect();
    }

    const oscillator = audioContextRef.current.createOscillator();
    const gainNode = audioContextRef.current.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(hz, audioContextRef.current.currentTime);
    gainNode.gain.setValueAtTime(0.1, audioContextRef.current.currentTime);

    oscillator.connect(gainNode);
    gainNode.connect(audioContextRef.current.destination);
    oscillator.start();

    oscillatorRef.current = oscillator;
    setCurrentFrequency(hz);
    setIsPlaying(true);
  }, []);

  const stopFrequency = useCallback(() => {
    if (oscillatorRef.current) {
      oscillatorRef.current.stop();
      oscillatorRef.current.disconnect();
      oscillatorRef.current = null;
    }
    setIsPlaying(false);
  }, []);

  // Frequency visualization
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || viewMode !== 'frequency') return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const animate = () => {
      ctx.fillStyle = COLORS.black;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      // Draw frequency waves
      const freqData = FREQUENCIES.find(f => f.hz === currentFrequency) || FREQUENCIES[0];
      const amplitude = 100 + (isPlaying ? 50 * Math.sin(time * 0.1) : 0);

      // Multiple wave layers
      for (let layer = 0; layer < 3; layer++) {
        ctx.beginPath();
        ctx.strokeStyle = freqData.color + (layer === 0 ? 'FF' : layer === 1 ? '80' : '40');
        ctx.lineWidth = 3 - layer;

        for (let x = 0; x < canvas.width; x++) {
          const frequency = currentFrequency / 100;
          const y = centerY + Math.sin((x + time * (layer + 1)) * frequency * 0.02) * (amplitude - layer * 20);

          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        ctx.stroke();
      }

      // Central resonance point
      const pulseSize = 30 + (isPlaying ? 10 * Math.sin(time * 0.2) : 0);
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, pulseSize * 2);
      gradient.addColorStop(0, freqData.color);
      gradient.addColorStop(0.5, freqData.color + '40');
      gradient.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize * 2, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();

      // Frequency text
      ctx.font = 'bold 48px monospace';
      ctx.fillStyle = COLORS.white;
      ctx.textAlign = 'center';
      ctx.fillText(`${currentFrequency} Hz`, centerX, centerY + 5);

      ctx.font = '14px monospace';
      ctx.fillStyle = freqData.color;
      ctx.fillText(freqData.name, centerX, centerY + 30);

      time++;
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [viewMode, currentFrequency, isPlaying]);

  // Molecular visualization
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || viewMode !== 'molecular') return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const animate = () => {
      ctx.fillStyle = COLORS.black;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      // Draw molecular structure (simple representation)
      ELEMENTS.forEach((element, i) => {
        const angle = (i / ELEMENTS.length) * Math.PI * 2 + time * 0.01;
        const radius = 150;
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;

        // Connection to center
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.strokeStyle = element.color + '40';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Element circle
        const isSelected = selectedElement === element.symbol;
        const elementRadius = isSelected ? 35 : 25;

        ctx.beginPath();
        ctx.arc(x, y, elementRadius, 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? element.color : element.color + '80';
        ctx.fill();

        // Element symbol
        ctx.font = `bold ${isSelected ? 18 : 14}px monospace`;
        ctx.fillStyle = element.color === '#FFFFFF' ? COLORS.black : COLORS.white;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(element.symbol, x, y);
      });

      // Central nucleus
      const nucleusGradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 50);
      nucleusGradient.addColorStop(0, COLORS.gold);
      nucleusGradient.addColorStop(0.5, COLORS.gold + '60');
      nucleusGradient.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.arc(centerX, centerY, 50, 0, Math.PI * 2);
      ctx.fillStyle = nucleusGradient;
      ctx.fill();

      ctx.font = 'bold 20px monospace';
      ctx.fillStyle = COLORS.black;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('Au', centerX, centerY);

      time++;
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [viewMode, selectedElement]);

  // Frequency view
  const renderFrequencyView = () => (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <canvas
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight - 200}
        style={{ flex: 1 }}
      />

      {/* Frequency selector */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '10px',
        padding: '20px',
        flexWrap: 'wrap',
      }}>
        {FREQUENCIES.map(freq => (
          <button
            key={freq.hz}
            onClick={() => isPlaying ? (currentFrequency === freq.hz ? stopFrequency() : playFrequency(freq.hz)) : playFrequency(freq.hz)}
            style={{
              backgroundColor: currentFrequency === freq.hz && isPlaying ? freq.color + '40' : 'transparent',
              border: `2px solid ${freq.color}`,
              color: freq.color,
              padding: '10px 20px',
              fontFamily: 'monospace',
              fontSize: '12px',
              cursor: 'pointer',
              borderRadius: '4px',
              minWidth: '100px',
            }}
          >
            {freq.hz} Hz
            <div style={{ fontSize: '9px', marginTop: '4px', opacity: 0.7 }}>
              {freq.name}
            </div>
          </button>
        ))}
      </div>

      {/* Play/Stop */}
      <div style={{ textAlign: 'center', paddingBottom: '20px' }}>
        <button
          onClick={() => isPlaying ? stopFrequency() : playFrequency(currentFrequency)}
          style={{
            backgroundColor: isPlaying ? COLORS.gold : 'transparent',
            border: `2px solid ${COLORS.gold}`,
            color: isPlaying ? COLORS.black : COLORS.gold,
            padding: '15px 40px',
            fontFamily: 'monospace',
            fontSize: '14px',
            cursor: 'pointer',
            borderRadius: '4px',
            letterSpacing: '0.2em',
          }}
        >
          {isPlaying ? 'ARRETER' : 'JOUER'}
        </button>
      </div>
    </div>
  );

  // Molecular view
  const renderMolecularView = () => (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <canvas
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight - 150}
        style={{ flex: 1 }}
      />

      {/* Element selector */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '15px',
        padding: '20px',
      }}>
        {ELEMENTS.map(element => (
          <button
            key={element.symbol}
            onClick={() => setSelectedElement(selectedElement === element.symbol ? null : element.symbol)}
            style={{
              width: '60px',
              height: '60px',
              backgroundColor: selectedElement === element.symbol ? element.color + '40' : 'transparent',
              border: `2px solid ${element.color}`,
              borderRadius: '50%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
            }}
          >
            <span style={{ color: element.color, fontFamily: 'monospace', fontWeight: 'bold' }}>
              {element.symbol}
            </span>
            <span style={{ color: 'rgba(255,255,255,0.5)', fontFamily: 'monospace', fontSize: '8px' }}>
              {element.name}
            </span>
          </button>
        ))}
      </div>
    </div>
  );

  // Transmute view
  const renderTransmuteView = () => (
    <div style={{
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px',
    }}>
      <div style={{
        fontSize: '60px',
        marginBottom: '30px',
      }}>
        ⚗️
      </div>

      <h2 style={{
        color: COLORS.purple,
        fontFamily: 'monospace',
        fontSize: '24px',
        letterSpacing: '0.3em',
        marginBottom: '20px',
      }}>
        TRANSMUTATION
      </h2>

      <p style={{
        color: 'rgba(255, 255, 255, 0.6)',
        fontFamily: 'monospace',
        fontSize: '14px',
        textAlign: 'center',
        maxWidth: '500px',
        lineHeight: 1.8,
      }}>
        La transmutation est le processus de transformation.
        Comme l'alchimiste transforme le plomb en or,
        tu transformes l'energie brute en creation pure.
      </p>

      <div style={{
        marginTop: '40px',
        display: 'flex',
        alignItems: 'center',
        gap: '30px',
      }}>
        <div style={{
          width: '80px',
          height: '80px',
          borderRadius: '50%',
          backgroundColor: '#333',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'monospace',
          color: 'rgba(255,255,255,0.5)',
        }}>
          Pb
        </div>

        <div style={{ color: COLORS.gold, fontSize: '30px' }}>→</div>

        <div style={{
          width: '80px',
          height: '80px',
          borderRadius: '50%',
          backgroundColor: COLORS.gold,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'monospace',
          color: COLORS.black,
          fontWeight: 'bold',
        }}>
          Au
        </div>
      </div>
    </div>
  );

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
            color: COLORS.purple,
            fontFamily: 'monospace',
            fontSize: '18px',
            letterSpacing: '0.2em',
          }}>
            ALCHIMIE
          </h1>
        </div>

        {/* View switcher */}
        <div style={{ display: 'flex', gap: '10px' }}>
          {(['frequency', 'molecular', 'transmute'] as const).map(mode => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                backgroundColor: viewMode === mode ? COLORS.purple + '30' : 'transparent',
                border: `1px solid ${viewMode === mode ? COLORS.purple : 'rgba(255, 255, 255, 0.2)'}`,
                color: viewMode === mode ? COLORS.purple : 'rgba(255, 255, 255, 0.5)',
                padding: '8px 16px',
                fontFamily: 'monospace',
                fontSize: '11px',
                cursor: 'pointer',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              {mode === 'frequency' ? 'FREQUENCES' : mode === 'molecular' ? 'MOLECULAIRE' : 'TRANSMUTER'}
            </button>
          ))}
        </div>
      </header>

      {/* Main content */}
      {viewMode === 'frequency' && renderFrequencyView()}
      {viewMode === 'molecular' && renderMolecularView()}
      {viewMode === 'transmute' && renderTransmuteView()}
    </div>
  );
}

export default Alchimie;
