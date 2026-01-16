/**
 * GENIE DE DEMAIN - Module Education
 * ===================================
 *
 * CANON AT·OM - Terminal Education
 * Chemin: /genie
 *
 * Interface collaborative, tableaux blancs infinis, sans grilles rigides.
 *
 * PHILOSOPHIE:
 * "L'education n'est pas un remplissage de vase, mais l'allumage d'un feu"
 *
 * ANTI-PATTERNS (INTERDITS):
 * - PAS de ranking
 * - PAS de notes
 * - PAS de comparaison entre apprenants
 *
 * PILIERS:
 * 1. Clan (groupes par passion, pas par age)
 * 2. Agent Mentor (IA adaptee au genie individuel)
 * 3. Apprentissage Reel (integration avec modules AT·OM)
 */

import React, { useState, useRef, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// =============================================================================
// CONSTANTS - Canon AT·OM
// =============================================================================

const COLORS = {
  black: '#000000',
  gold: '#D4AF37',
  cobalt: '#0047AB',
  white: '#FFFFFF',
  warmYellow: '#FFD700',
};

// Passion domains for Clans
const PASSION_DOMAINS = [
  { id: 'creation', name: 'Creation', icon: '🎨', color: '#9B59B6' },
  { id: 'nature', name: 'Nature', icon: '🌿', color: '#27AE60' },
  { id: 'technology', name: 'Technologie', icon: '⚡', color: '#3498DB' },
  { id: 'movement', name: 'Mouvement', icon: '🏃', color: '#E74C3C' },
  { id: 'sound', name: 'Son', icon: '🎵', color: '#F39C12' },
  { id: 'stories', name: 'Histoires', icon: '📖', color: '#1ABC9C' },
  { id: 'numbers', name: 'Nombres', icon: '🔢', color: '#607D8B' },
  { id: 'building', name: 'Construction', icon: '🔧', color: '#795548' },
];

// =============================================================================
// TYPES
// =============================================================================

interface CanvasPoint {
  x: number;
  y: number;
  color: string;
  size: number;
}

interface Idea {
  id: string;
  x: number;
  y: number;
  text: string;
  color: string;
  connections: string[];
}

// =============================================================================
// GENIE COMPONENT
// =============================================================================

export function Genie() {
  const navigate = useNavigate();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [drawingPoints, setDrawingPoints] = useState<CanvasPoint[]>([]);
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [selectedClan, setSelectedClan] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'canvas' | 'clans' | 'mentor'>('canvas');

  // Canvas drawing
  const handleCanvasMouseDown = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    setIsDrawing(true);
    const rect = canvasRef.current?.getBoundingClientRect();
    if (rect) {
      setDrawingPoints(prev => [...prev, {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
        color: COLORS.warmYellow,
        size: 3,
      }]);
    }
  }, []);

  const handleCanvasMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;
    const rect = canvasRef.current?.getBoundingClientRect();
    if (rect) {
      setDrawingPoints(prev => [...prev, {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
        color: COLORS.warmYellow,
        size: 3,
      }]);
    }
  }, [isDrawing]);

  const handleCanvasMouseUp = useCallback(() => {
    setIsDrawing(false);
  }, []);

  // Draw on canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear
    ctx.fillStyle = COLORS.black;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw points
    drawingPoints.forEach((point, i) => {
      if (i === 0) return;
      const prevPoint = drawingPoints[i - 1];

      ctx.beginPath();
      ctx.moveTo(prevPoint.x, prevPoint.y);
      ctx.lineTo(point.x, point.y);
      ctx.strokeStyle = point.color;
      ctx.lineWidth = point.size;
      ctx.lineCap = 'round';
      ctx.stroke();
    });

    // Draw ideas
    ideas.forEach(idea => {
      // Glow
      const gradient = ctx.createRadialGradient(idea.x, idea.y, 0, idea.x, idea.y, 40);
      gradient.addColorStop(0, idea.color + '40');
      gradient.addColorStop(1, 'transparent');
      ctx.beginPath();
      ctx.arc(idea.x, idea.y, 40, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();

      // Circle
      ctx.beginPath();
      ctx.arc(idea.x, idea.y, 20, 0, Math.PI * 2);
      ctx.fillStyle = idea.color;
      ctx.fill();

      // Text
      ctx.font = '12px monospace';
      ctx.fillStyle = COLORS.white;
      ctx.textAlign = 'center';
      ctx.fillText(idea.text, idea.x, idea.y + 35);
    });
  }, [drawingPoints, ideas]);

  // Add idea on double click
  const handleDoubleClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;

    const text = prompt('Quelle est ton idee?');
    if (text) {
      setIdeas(prev => [...prev, {
        id: Date.now().toString(),
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
        text: text.substring(0, 20),
        color: PASSION_DOMAINS[Math.floor(Math.random() * PASSION_DOMAINS.length)].color,
        connections: [],
      }]);
    }
  }, []);

  // Canvas view
  const renderCanvasView = () => (
    <div style={{ flex: 1, position: 'relative' }}>
      <canvas
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight - 100}
        style={{ display: 'block', cursor: 'crosshair' }}
        onMouseDown={handleCanvasMouseDown}
        onMouseMove={handleCanvasMouseMove}
        onMouseUp={handleCanvasMouseUp}
        onMouseLeave={handleCanvasMouseUp}
        onDoubleClick={handleDoubleClick}
      />

      {/* Instructions */}
      <div style={{
        position: 'absolute',
        bottom: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        color: 'rgba(255, 255, 255, 0.4)',
        fontFamily: 'monospace',
        fontSize: '12px',
        textAlign: 'center',
      }}>
        Dessine librement | Double-clic pour ajouter une idee
      </div>

      {/* Clear button */}
      <button
        onClick={() => { setDrawingPoints([]); setIdeas([]); }}
        style={{
          position: 'absolute',
          bottom: 20,
          right: 20,
          background: 'transparent',
          border: `1px solid ${COLORS.cobalt}`,
          color: COLORS.cobalt,
          padding: '8px 16px',
          fontFamily: 'monospace',
          fontSize: '11px',
          cursor: 'pointer',
          borderRadius: '4px',
        }}
      >
        EFFACER
      </button>
    </div>
  );

  // Clans view
  const renderClansView = () => (
    <div style={{
      flex: 1,
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '30px',
      padding: '40px',
    }}>
      {PASSION_DOMAINS.map(domain => (
        <button
          key={domain.id}
          onClick={() => setSelectedClan(domain.id)}
          style={{
            width: '150px',
            height: '150px',
            backgroundColor: selectedClan === domain.id ? domain.color + '40' : 'transparent',
            border: `2px solid ${domain.color}`,
            borderRadius: '50%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
          }}
        >
          <span style={{ fontSize: '40px' }}>{domain.icon}</span>
          <span style={{
            color: domain.color,
            fontFamily: 'monospace',
            fontSize: '12px',
            marginTop: '10px',
            letterSpacing: '0.1em',
          }}>
            {domain.name.toUpperCase()}
          </span>
        </button>
      ))}

      {/* No ranking notice */}
      <div style={{
        position: 'absolute',
        bottom: 40,
        left: '50%',
        transform: 'translateX(-50%)',
        color: COLORS.gold,
        fontFamily: 'monospace',
        fontSize: '11px',
        textAlign: 'center',
        letterSpacing: '0.2em',
      }}>
        PAS DE RANKING | PAS DE NOTES | PAS DE COMPARAISON
      </div>
    </div>
  );

  // Mentor view
  const renderMentorView = () => (
    <div style={{
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px',
    }}>
      {/* Mentor avatar */}
      <div style={{
        width: '120px',
        height: '120px',
        borderRadius: '50%',
        background: `linear-gradient(135deg, ${COLORS.cobalt}, ${COLORS.gold})`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: '30px',
        boxShadow: `0 0 40px ${COLORS.cobalt}40`,
      }}>
        <span style={{ fontSize: '50px' }}>🌟</span>
      </div>

      <h2 style={{
        color: COLORS.white,
        fontFamily: 'monospace',
        fontSize: '24px',
        marginBottom: '10px',
        letterSpacing: '0.2em',
      }}>
        AGENT MENTOR
      </h2>

      <p style={{
        color: 'rgba(255, 255, 255, 0.6)',
        fontFamily: 'monospace',
        fontSize: '14px',
        textAlign: 'center',
        maxWidth: '500px',
        lineHeight: 1.8,
      }}>
        Je m'adapte a ton genie unique. Pas de programme rigide.
        Ensemble, nous explorons ce qui t'anime vraiment.
      </p>

      {/* Chat input */}
      <div style={{
        marginTop: '40px',
        width: '100%',
        maxWidth: '500px',
        display: 'flex',
        gap: '10px',
      }}>
        <input
          type="text"
          placeholder="Qu'est-ce qui te passionne?"
          style={{
            flex: 1,
            backgroundColor: 'transparent',
            border: `1px solid ${COLORS.cobalt}`,
            color: COLORS.white,
            padding: '15px 20px',
            fontFamily: 'monospace',
            fontSize: '14px',
            borderRadius: '4px',
          }}
        />
        <button style={{
          backgroundColor: COLORS.cobalt,
          border: 'none',
          color: COLORS.white,
          padding: '15px 25px',
          fontFamily: 'monospace',
          fontSize: '14px',
          cursor: 'pointer',
          borderRadius: '4px',
        }}>
          ➤
        </button>
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
      {/* Header */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '15px 30px',
        borderBottom: `1px solid rgba(255, 255, 255, 0.1)`,
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
            color: COLORS.warmYellow,
            fontFamily: 'monospace',
            fontSize: '18px',
            letterSpacing: '0.2em',
          }}>
            GENIE DE DEMAIN
          </h1>
        </div>

        {/* View switcher */}
        <div style={{ display: 'flex', gap: '10px' }}>
          {(['canvas', 'clans', 'mentor'] as const).map(mode => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                backgroundColor: viewMode === mode ? COLORS.warmYellow + '30' : 'transparent',
                border: `1px solid ${viewMode === mode ? COLORS.warmYellow : 'rgba(255, 255, 255, 0.2)'}`,
                color: viewMode === mode ? COLORS.warmYellow : 'rgba(255, 255, 255, 0.5)',
                padding: '8px 16px',
                fontFamily: 'monospace',
                fontSize: '11px',
                cursor: 'pointer',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
              }}
            >
              {mode === 'canvas' ? 'TABLEAU' : mode === 'clans' ? 'CLANS' : 'MENTOR'}
            </button>
          ))}
        </div>
      </header>

      {/* Main content */}
      {viewMode === 'canvas' && renderCanvasView()}
      {viewMode === 'clans' && renderClansView()}
      {viewMode === 'mentor' && renderMentorView()}
    </div>
  );
}

export default Genie;
