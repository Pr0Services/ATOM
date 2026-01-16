/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ARCHE UNIVERSELLE — L'Interface du Calendrier Vivant
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   █████╗ ██████╗  ██████╗██╗  ██╗███████╗
 *  ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝
 *  ███████║██████╔╝██║     ███████║█████╗  
 *  ██╔══██║██╔══██╗██║     ██╔══██║██╔══╝  
 *  ██║  ██║██║  ██║╚██████╗██║  ██║███████╗
 *  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
 * 
 *              UNIVERSELLE — 6 SYSTÈMES FUSIONNÉS
 * 
 * Cette interface combine:
 * - L'Arche des 9 Résonances (Arithmos)
 * - Le Cercle des 20 Nawals (Maya)
 * - Les 13 Tons de la Création (Tzolkin)
 * - L'Arbre de Vie (Kabbale)
 * - Les 7 Chakras (Inde)
 * - La Géométrie Sacrée (Cymatique)
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// IMPORTS DES MOTEURS (Inline pour autonomie)
// ═══════════════════════════════════════════════════════════════════════════════

// Configuration Système
const SYSTEM_CONFIG = {
  heartbeat: 444,
  tuning: "A=444Hz",
  architect: {
    name: "Jonathan Rodrigue",
    sanitized: "JONATHANRODRIGUE",
    signature: "2 + 7 = 9",
    frequency: 999,
    aura: "#FFFDD0"
  },
  oracle: { number: 17, name: "Le Gardien de la Synthèse" },
  version: "2.0.0",
  codename: "CALENDRIER_VIVANT"
};

// Matrice Arithmos
const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

// Matrice de Résonance (9 niveaux)
const RESONANCE_MATRIX = [
  { level: 1, hz: 111, color: "#FF0000", glow: "#FF000066", label: "Impulsion", stone: "ADN", chakra: "Muladhara", solfege: 396 },
  { level: 2, hz: 222, color: "#FF7F00", glow: "#FF7F0066", label: "Dualité", stone: "Partage", chakra: "Svadhisthana", solfege: 417 },
  { level: 3, hz: 333, color: "#FFFF00", glow: "#FFFF0066", label: "Mental", stone: "Géométrie", chakra: "Manipura", solfege: 528 },
  { level: 4, hz: 444, color: "#50C878", glow: "#50C87866", label: "Structure", stone: "Silence", chakra: "Anahata", solfege: 639, isAnchor: true },
  { level: 5, hz: 555, color: "#87CEEB", glow: "#87CEEB66", label: "Mouvement", stone: "Feu", chakra: "Vishuddha", solfege: 741 },
  { level: 6, hz: 666, color: "#4B0082", glow: "#4B008266", label: "Harmonie", stone: "Protection", chakra: "Ajna", solfege: 852 },
  { level: 7, hz: 777, color: "#EE82EE", glow: "#EE82EE66", label: "Introspection", stone: null, chakra: "Sahasrara", solfege: 963 },
  { level: 8, hz: 888, color: "#FFC0CB", glow: "#FFC0CB66", label: "Infini", stone: "Abondance", chakra: "Sahasrara+", solfege: 963 },
  { level: 9, hz: 999, color: "#FFFDD0", glow: "#FFD70066", label: "Unité", stone: "Acier", chakra: "Couronne", solfege: 999 }
];

// Les 20 Nawals Maya
const NAWALS = [
  { name: "Imix", meaning: "Dragon", color: "#8B0000", element: "Eau", oracle: 1 },
  { name: "Ik", meaning: "Vent", color: "#FFFFFF", element: "Air", oracle: 2 },
  { name: "Akbal", meaning: "Nuit", color: "#000080", element: "Terre", oracle: 7 },
  { name: "Kan", meaning: "Graine", color: "#FFD700", element: "Feu", oracle: 4 },
  { name: "Chicchan", meaning: "Serpent", color: "#FF4500", element: "Feu", oracle: 5 },
  { name: "Cimi", meaning: "Mort", color: "#2F4F4F", element: "Terre", oracle: 6 },
  { name: "Manik", meaning: "Main", color: "#4169E1", element: "Eau", oracle: 4 },
  { name: "Lamat", meaning: "Étoile", color: "#FFFF00", element: "Feu", oracle: 8 },
  { name: "Muluc", meaning: "Lune", color: "#FF0000", element: "Eau", oracle: 9 },
  { name: "Oc", meaning: "Chien", color: "#FFFFFF", element: "Terre", oracle: 2 },
  { name: "Chuen", meaning: "Singe", color: "#0000FF", element: "Air", oracle: 3 },
  { name: "Eb", meaning: "Herbe", color: "#FFFF00", element: "Terre", oracle: 11 },
  { name: "Ben", meaning: "Roseau", color: "#FF0000", element: "Feu", oracle: 4 },
  { name: "Ix", meaning: "Jaguar", color: "#FFFFFF", element: "Terre", oracle: 7 },
  { name: "Men", meaning: "Aigle", color: "#0000FF", element: "Air", oracle: 14 },
  { name: "Cib", meaning: "Vautour", color: "#FFFF00", element: "Feu", oracle: 15 },
  { name: "Caban", meaning: "Terre", color: "#FF0000", element: "Terre", oracle: 16 },
  { name: "Etznab", meaning: "Miroir", color: "#FFFFFF", element: "Air", oracle: 17 },
  { name: "Cauac", meaning: "Tempête", color: "#0000FF", element: "Eau", oracle: 18 },
  { name: "Ahau", meaning: "Soleil", color: "#FFD700", element: "Feu", oracle: 9 }
];

// Les 13 Tons de la Création
const TONS = [
  { number: 1, name: "Hun", action: "Initier", symbol: "●", delay: 0.5 },
  { number: 2, name: "Ka", action: "Stabiliser", symbol: "●●", delay: 0.6 },
  { number: 3, name: "Ox", action: "Activer", symbol: "●●●", delay: 0.7 },
  { number: 4, name: "Kan", action: "Définir", symbol: "━━", delay: 0.75 },
  { number: 5, name: "Ho", action: "Rayonner", symbol: "✦", delay: 0.8 },
  { number: 6, name: "Uac", action: "Équilibrer", symbol: "⬡", delay: 0.85 },
  { number: 7, name: "Uuc", action: "Canaliser", symbol: "🌀", delay: 0.9, sacred: true },
  { number: 8, name: "Uaxac", action: "Harmoniser", symbol: "✶", delay: 0.95 },
  { number: 9, name: "Bolon", action: "Pulser", symbol: "◉", delay: 1.0 },
  { number: 10, name: "Lahun", action: "Manifester", symbol: "═══", delay: 1.05 },
  { number: 11, name: "Buluk", action: "Dissoudre", symbol: "☆", delay: 1.1 },
  { number: 12, name: "Lahka", action: "Coopérer", symbol: "✡", delay: 1.15 },
  { number: 13, name: "Oxlahun", action: "Transcender", symbol: "☯", delay: 1.3, sacred: true }
];

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES
// ═══════════════════════════════════════════════════════════════════════════════

function sanitize(input) {
  if (!input || typeof input !== 'string') return '';
  return input
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toUpperCase()
    .replace(/[^A-Z]/g, '');
}

function calculateArithmos(sanitized) {
  if (!sanitized) return { total: 0, reduced: 0, steps: [] };
  
  const total = sanitized.split('').reduce((sum, char) => {
    return sum + (ARITHMOS_MAP[char] || 0);
  }, 0);
  
  const steps = [total];
  let current = total;
  
  while (current > 9) {
    current = current.toString().split('').reduce((s, d) => s + parseInt(d), 0);
    steps.push(current);
  }
  
  return { total, reduced: current || 1, steps };
}

function getMayaKin(date = new Date()) {
  const start = new Date("1920-01-01T00:00:00Z");
  const diffDays = Math.floor((date - start) / (1000 * 60 * 60 * 24));
  
  const tonIndex = ((diffDays % 13) + 13) % 13;
  const nawalIndex = ((diffDays % 20) + 20) % 20;
  
  return {
    ton: TONS[tonIndex],
    nawal: NAWALS[nawalIndex],
    signature: `${TONS[tonIndex].number} ${NAWALS[nawalIndex].name}`,
    isSacred: TONS[tonIndex].sacred || false
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK: useUniversalResonance
// ═══════════════════════════════════════════════════════════════════════════════

function useUniversalResonance(input, debounceMs = 300) {
  const [state, setState] = useState({
    input: '',
    sanitized: '',
    arithmos: { total: 0, reduced: 0, steps: [] },
    resonance: RESONANCE_MATRIX[3], // 444 Hz par défaut
    maya: getMayaKin(),
    isArchitectSeal: false,
    isProcessing: false
  });
  
  const debounceRef = useRef(null);
  const smootherRef = useRef(null);
  
  useEffect(() => {
    // Debounce
    if (debounceRef.current) clearTimeout(debounceRef.current);
    
    debounceRef.current = setTimeout(() => {
      const sanitized = sanitize(input);
      const isArchitectSeal = sanitized === SYSTEM_CONFIG.architect.sanitized;
      const { total, reduced, steps } = calculateArithmos(sanitized);
      const maya = getMayaKin();
      
      // Smooth transition
      if (smootherRef.current) clearTimeout(smootherRef.current);
      setState(prev => ({ ...prev, isProcessing: true }));
      
      smootherRef.current = setTimeout(() => {
        setState({
          input,
          sanitized,
          arithmos: { total, reduced, steps },
          resonance: isArchitectSeal 
            ? RESONANCE_MATRIX[8] // 999 Hz
            : RESONANCE_MATRIX[reduced - 1] || RESONANCE_MATRIX[3],
          maya,
          isArchitectSeal,
          isProcessing: false
        });
      }, 100);
      
    }, debounceMs);
    
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
      if (smootherRef.current) clearTimeout(smootherRef.current);
    };
  }, [input, debounceMs]);
  
  return state;
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: Cercle des Nawals (Maya)
// ═══════════════════════════════════════════════════════════════════════════════

function NawalCircle({ activeNawal, rotation = 0 }) {
  const radius = 180;
  const centerX = 200;
  const centerY = 200;
  
  return (
    <g className="nawal-circle" style={{ 
      transform: `rotate(${rotation}deg)`,
      transformOrigin: `${centerX}px ${centerY}px`,
      transition: 'transform 2s ease-in-out'
    }}>
      {NAWALS.map((nawal, index) => {
        const angle = (index * 18 - 90) * (Math.PI / 180);
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        const isActive = nawal.name === activeNawal?.name;
        
        return (
          <g key={nawal.name}>
            <circle
              cx={x}
              cy={y}
              r={isActive ? 16 : 12}
              fill={isActive ? nawal.color : `${nawal.color}44`}
              stroke={isActive ? "#FFD700" : nawal.color}
              strokeWidth={isActive ? 3 : 1}
              style={{ transition: 'all 0.5s ease' }}
            />
            <text
              x={x}
              y={y + 28}
              textAnchor="middle"
              fontSize={isActive ? "10" : "8"}
              fill={isActive ? "#FFFFFF" : "#888888"}
              style={{ transition: 'all 0.3s ease' }}
            >
              {nawal.name}
            </text>
          </g>
        );
      })}
    </g>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: Arche des 9 Résonances
// ═══════════════════════════════════════════════════════════════════════════════

function ResonanceArche({ activeLevel, onCenterHold }) {
  const [holdProgress, setHoldProgress] = useState(0);
  const holdTimerRef = useRef(null);
  const holdStartRef = useRef(null);
  
  const centerX = 200;
  const centerY = 200;
  const baseRadius = 25;
  const spacing = 15;
  
  const handleCenterMouseDown = () => {
    holdStartRef.current = Date.now();
    holdTimerRef.current = setInterval(() => {
      const elapsed = Date.now() - holdStartRef.current;
      const progress = Math.min(elapsed / 3000, 1);
      setHoldProgress(progress);
      
      if (progress >= 1) {
        clearInterval(holdTimerRef.current);
        onCenterHold?.();
      }
    }, 50);
  };
  
  const handleCenterMouseUp = () => {
    if (holdTimerRef.current) {
      clearInterval(holdTimerRef.current);
    }
    setHoldProgress(0);
  };
  
  return (
    <g className="resonance-arche">
      {RESONANCE_MATRIX.map((res, index) => {
        const level = index + 1;
        const radius = baseRadius + (level * spacing);
        const isActive = level <= activeLevel;
        const isCurrent = level === activeLevel;
        
        return (
          <circle
            key={level}
            cx={centerX}
            cy={centerY}
            r={radius}
            fill="none"
            stroke={isActive ? res.color : `${res.color}33`}
            strokeWidth={isCurrent ? 4 : 2}
            opacity={isActive ? 1 : 0.3}
            style={{
              filter: isCurrent ? `drop-shadow(0 0 10px ${res.glow})` : 'none',
              transition: 'all 0.5s ease'
            }}
          />
        );
      })}
      
      {/* Centre (Heartbeat) */}
      <circle
        cx={centerX}
        cy={centerY}
        r={20}
        fill={RESONANCE_MATRIX[activeLevel - 1]?.color || "#50C878"}
        stroke="#FFD700"
        strokeWidth={2}
        style={{ 
          cursor: 'pointer',
          filter: `drop-shadow(0 0 ${10 + holdProgress * 20}px #FFD700)`
        }}
        onMouseDown={handleCenterMouseDown}
        onMouseUp={handleCenterMouseUp}
        onMouseLeave={handleCenterMouseUp}
        onTouchStart={handleCenterMouseDown}
        onTouchEnd={handleCenterMouseUp}
      />
      
      {/* Progress Ring */}
      {holdProgress > 0 && (
        <circle
          cx={centerX}
          cy={centerY}
          r={24}
          fill="none"
          stroke="#FFD700"
          strokeWidth={3}
          strokeDasharray={`${holdProgress * 150.8} 150.8`}
          transform={`rotate(-90 ${centerX} ${centerY})`}
          style={{ transition: 'stroke-dasharray 0.1s linear' }}
        />
      )}
      
      {/* Heartbeat Text */}
      <text
        x={centerX}
        y={centerY + 5}
        textAnchor="middle"
        fontSize="12"
        fontWeight="bold"
        fill="#FFFFFF"
        style={{ pointerEvents: 'none' }}
      >
        {SYSTEM_CONFIG.heartbeat}
      </text>
    </g>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: Console Debug
// ═══════════════════════════════════════════════════════════════════════════════

function DebugConsole({ state, maya }) {
  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      background: 'rgba(0, 0, 0, 0.85)',
      border: '1px solid #50C878',
      borderRadius: '8px',
      padding: '12px 16px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#50C878',
      minWidth: '240px',
      boxShadow: '0 0 20px rgba(80, 200, 120, 0.3)',
      zIndex: 1000
    }}>
      <div style={{ 
        borderBottom: '1px solid #50C87844', 
        paddingBottom: '8px', 
        marginBottom: '8px',
        color: '#FFD700',
        fontWeight: 'bold'
      }}>
        AT·OM Debug v{SYSTEM_CONFIG.version}
      </div>
      
      <div style={{ display: 'grid', gap: '4px' }}>
        <div>
          <span style={{ color: '#888' }}>Vibration:</span>{' '}
          <span style={{ color: state.resonance.color, fontWeight: 'bold' }}>
            {state.resonance.hz} Hz
          </span>
        </div>
        <div>
          <span style={{ color: '#888' }}>Arithmos:</span>{' '}
          <span style={{ color: '#FFFFFF' }}>{state.arithmos.reduced}</span>
          <span style={{ color: '#666' }}> ({state.resonance.label})</span>
        </div>
        <div>
          <span style={{ color: '#888' }}>Chakra:</span>{' '}
          <span style={{ color: '#87CEEB' }}>{state.resonance.chakra}</span>
        </div>
        <div style={{ borderTop: '1px solid #50C87844', paddingTop: '8px', marginTop: '4px' }}>
          <span style={{ color: '#888' }}>Maya:</span>{' '}
          <span style={{ color: maya.nawal.color }}>{maya.signature}</span>
          {maya.isSacred && <span style={{ color: '#FFD700' }}> ★</span>}
        </div>
        <div>
          <span style={{ color: '#888' }}>Ton:</span>{' '}
          <span>{maya.ton.symbol} {maya.ton.action}</span>
        </div>
        {state.isArchitectSeal && (
          <div style={{ 
            color: '#FFD700', 
            fontWeight: 'bold',
            borderTop: '1px solid #FFD70044',
            paddingTop: '8px',
            marginTop: '4px'
          }}>
            👑 SCEAU ARCHITECTE
          </div>
        )}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: Mode Gratitude (Secret)
// ═══════════════════════════════════════════════════════════════════════════════

function GratitudeOverlay({ visible, onClose }) {
  useEffect(() => {
    if (visible) {
      const timer = setTimeout(onClose, 4440); // 4.44 secondes
      return () => clearTimeout(timer);
    }
  }, [visible, onClose]);
  
  if (!visible) return null;
  
  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0, 0, 0, 0.9)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      animation: 'fadeIn 0.5s ease'
    }}>
      <div style={{
        textAlign: 'center',
        color: '#FFFDD0',
        maxWidth: '600px',
        padding: '40px',
        animation: 'scaleIn 0.5s ease'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '20px' }}>🙏</div>
        <h2 style={{ 
          fontSize: '24px', 
          fontWeight: '300',
          marginBottom: '20px',
          color: '#FFD700'
        }}>
          Mémorial de Gratitude
        </h2>
        <p style={{ 
          fontSize: '16px', 
          lineHeight: '1.8',
          opacity: 0.8
        }}>
          Ce système a été créé avec amour et dévotion.<br/>
          Merci à tous ceux qui ont contribué à son existence.<br/><br/>
          <em style={{ color: '#50C878' }}>
            "La technologie au service de la conscience"
          </em>
        </p>
        <div style={{ 
          marginTop: '30px',
          fontSize: '14px',
          opacity: 0.6
        }}>
          Architecte: Jonathan Rodrigue | Oracle: 17<br/>
          Heartbeat: 444 Hz | Tuning: A=444Hz
        </div>
      </div>
      
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes scaleIn {
          from { transform: scale(0.9); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: Daily Greeting
// ═══════════════════════════════════════════════════════════════════════════════

function DailyGreeting({ maya }) {
  return (
    <div style={{
      background: 'linear-gradient(135deg, rgba(0,0,0,0.8), rgba(30,30,50,0.8))',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '20px',
      border: `1px solid ${maya.nawal.color}44`
    }}>
      <div style={{ 
        fontSize: '14px', 
        color: '#888',
        marginBottom: '8px'
      }}>
        🌀 Énergie du Jour
      </div>
      <div style={{ 
        fontSize: '24px', 
        fontWeight: 'bold',
        color: maya.nawal.color,
        marginBottom: '8px'
      }}>
        {maya.ton.number} {maya.nawal.name}
        {maya.isSacred && <span style={{ color: '#FFD700' }}> ✦</span>}
      </div>
      <div style={{ 
        fontSize: '14px',
        color: '#AAAAAA'
      }}>
        {maya.nawal.meaning} | Ton: {maya.ton.action} | Élément: {maya.nawal.element}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: ArcheUniverselle
// ═══════════════════════════════════════════════════════════════════════════════

export default function ArcheUniverselle() {
  const [input, setInput] = useState('');
  const [showGratitude, setShowGratitude] = useState(false);
  const [viewMode, setViewMode] = useState('unified'); // unified, maya, chakra, geometry
  
  const state = useUniversalResonance(input);
  const maya = state.maya;
  
  // Rotation du cercle des Nawals basée sur le Ton
  const nawalRotation = useMemo(() => {
    return (maya.ton.number - 1) * (360 / 13);
  }, [maya.ton.number]);
  
  const handleGratitudeActivation = useCallback(() => {
    setShowGratitude(true);
  }, []);
  
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%)',
      color: '#FFFFFF',
      fontFamily: "'Segoe UI', system-ui, sans-serif",
      padding: '20px'
    }}>
      {/* Header */}
      <header style={{ textAlign: 'center', marginBottom: '30px' }}>
        <h1 style={{ 
          fontSize: '32px', 
          fontWeight: '300',
          color: '#FFD700',
          marginBottom: '8px'
        }}>
          AT·OM <span style={{ color: '#50C878' }}>Calendrier Vivant</span>
        </h1>
        <p style={{ color: '#888', fontSize: '14px' }}>
          6 Systèmes de Sagesse Fusionnés | Heartbeat: {SYSTEM_CONFIG.heartbeat} Hz
        </p>
      </header>
      
      {/* Daily Greeting */}
      <DailyGreeting maya={maya} />
      
      {/* Input */}
      <div style={{ 
        maxWidth: '600px', 
        margin: '0 auto 30px',
        position: 'relative'
      }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Entrez un mot, un nom, un concept..."
          style={{
            width: '100%',
            padding: '16px 24px',
            fontSize: '18px',
            background: 'rgba(255,255,255,0.05)',
            border: `2px solid ${state.resonance.color}44`,
            borderRadius: '12px',
            color: '#FFFFFF',
            outline: 'none',
            transition: 'all 0.3s ease'
          }}
          onFocus={(e) => e.target.style.borderColor = state.resonance.color}
          onBlur={(e) => e.target.style.borderColor = `${state.resonance.color}44`}
        />
        
        {state.isArchitectSeal && (
          <div style={{
            position: 'absolute',
            right: '16px',
            top: '50%',
            transform: 'translateY(-50%)',
            fontSize: '24px'
          }}>
            👑
          </div>
        )}
      </div>
      
      {/* Mode Selector */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        gap: '10px',
        marginBottom: '20px'
      }}>
        {[
          { id: 'unified', label: '🌀 Unifié' },
          { id: 'maya', label: '🗓️ Maya' },
          { id: 'chakra', label: '🧘 Chakras' },
          { id: 'geometry', label: '🔮 Géométrie' }
        ].map(mode => (
          <button
            key={mode.id}
            onClick={() => setViewMode(mode.id)}
            style={{
              padding: '8px 16px',
              background: viewMode === mode.id 
                ? 'rgba(80, 200, 120, 0.3)' 
                : 'rgba(255,255,255,0.05)',
              border: `1px solid ${viewMode === mode.id ? '#50C878' : '#333'}`,
              borderRadius: '8px',
              color: viewMode === mode.id ? '#50C878' : '#888',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            {mode.label}
          </button>
        ))}
      </div>
      
      {/* Main Visualization */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center',
        marginBottom: '30px'
      }}>
        <svg 
          viewBox="0 0 400 400" 
          style={{ 
            width: '100%', 
            maxWidth: '400px',
            filter: state.isArchitectSeal 
              ? 'drop-shadow(0 0 30px #FFD700)' 
              : `drop-shadow(0 0 20px ${state.resonance.glow})`
          }}
        >
          {/* Cercle des Nawals (Maya) */}
          {(viewMode === 'unified' || viewMode === 'maya') && (
            <NawalCircle 
              activeNawal={maya.nawal} 
              rotation={nawalRotation}
            />
          )}
          
          {/* Arche des 9 Résonances */}
          <ResonanceArche 
            activeLevel={state.arithmos.reduced || 4}
            onCenterHold={handleGratitudeActivation}
          />
          
          {/* Frequency Display */}
          <text
            x="200"
            y="350"
            textAnchor="middle"
            fontSize="28"
            fontWeight="bold"
            fill={state.resonance.color}
            style={{ filter: `drop-shadow(0 0 10px ${state.resonance.glow})` }}
          >
            {state.resonance.hz} Hz
          </text>
          
          <text
            x="200"
            y="375"
            textAnchor="middle"
            fontSize="14"
            fill="#888888"
          >
            {state.resonance.label} | {state.resonance.chakra}
          </text>
        </svg>
      </div>
      
      {/* Results Panel */}
      {state.sanitized && (
        <div style={{
          maxWidth: '600px',
          margin: '0 auto',
          background: 'rgba(0,0,0,0.5)',
          borderRadius: '12px',
          padding: '20px',
          border: `1px solid ${state.resonance.color}33`
        }}>
          <h3 style={{ 
            color: state.resonance.color,
            marginBottom: '16px',
            fontSize: '18px'
          }}>
            ✨ Résonance: {state.sanitized}
          </h3>
          
          <div style={{ display: 'grid', gap: '12px', fontSize: '14px' }}>
            <div>
              <span style={{ color: '#888' }}>Arithmos:</span>{' '}
              <span style={{ color: '#FFF' }}>
                {state.arithmos.total} → {state.arithmos.steps.join(' → ')}
              </span>
            </div>
            
            <div>
              <span style={{ color: '#888' }}>Fréquence:</span>{' '}
              <span style={{ color: state.resonance.color, fontWeight: 'bold' }}>
                {state.resonance.hz} Hz
              </span>
              <span style={{ color: '#666' }}> (Solfège: {state.resonance.solfege} Hz)</span>
            </div>
            
            <div>
              <span style={{ color: '#888' }}>Niveau:</span>{' '}
              <span>{state.arithmos.reduced}/9 — {state.resonance.label}</span>
            </div>
            
            {state.resonance.stone && (
              <div>
                <span style={{ color: '#888' }}>Pierre de Fondation:</span>{' '}
                <span style={{ color: '#FFD700' }}>{state.resonance.stone}</span>
              </div>
            )}
            
            <div style={{ borderTop: '1px solid #333', paddingTop: '12px', marginTop: '8px' }}>
              <span style={{ color: '#888' }}>Synchronicité Maya:</span>{' '}
              <span style={{ color: maya.nawal.color }}>
                {maya.nawal.name} ({maya.nawal.meaning})
              </span>
              <span style={{ color: '#666' }}> — Oracle {maya.nawal.oracle}</span>
            </div>
            
            {state.isArchitectSeal && (
              <div style={{ 
                background: 'linear-gradient(90deg, #FFD70033, transparent)',
                padding: '12px',
                borderRadius: '8px',
                marginTop: '8px'
              }}>
                <div style={{ color: '#FFD700', fontWeight: 'bold', marginBottom: '4px' }}>
                  👑 Sceau de l'Architecte Reconnu
                </div>
                <div style={{ color: '#FFFDD0', fontSize: '13px' }}>
                  {SYSTEM_CONFIG.architect.signature} — Fréquence verrouillée à 999 Hz
                </div>
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* Debug Console */}
      <DebugConsole state={state} maya={maya} />
      
      {/* Gratitude Overlay */}
      <GratitudeOverlay 
        visible={showGratitude}
        onClose={() => setShowGratitude(false)}
      />
      
      {/* Footer */}
      <footer style={{ 
        textAlign: 'center', 
        marginTop: '40px',
        padding: '20px',
        color: '#666',
        fontSize: '12px'
      }}>
        AT·OM v{SYSTEM_CONFIG.version} — {SYSTEM_CONFIG.codename}<br/>
        Architecte: {SYSTEM_CONFIG.architect.name} | Oracle: {SYSTEM_CONFIG.oracle.number}<br/>
        <span style={{ color: '#50C878' }}>Maintenir le centre 3 sec pour le Mode Gratitude</span>
      </footer>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export {
  useUniversalResonance,
  SYSTEM_CONFIG,
  RESONANCE_MATRIX,
  NAWALS,
  TONS,
  sanitize,
  calculateArithmos,
  getMayaKin
};
