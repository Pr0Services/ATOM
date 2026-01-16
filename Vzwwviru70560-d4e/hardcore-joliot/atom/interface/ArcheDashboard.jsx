/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *    █████╗ ██████╗  ██████╗██╗  ██╗███████╗
 *   ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝
 *   ███████║██████╔╝██║     ███████║█████╗  
 *   ██╔══██║██╔══██╗██║     ██╔══██║██╔══╝  
 *   ██║  ██║██║  ██║╚██████╗██║  ██║███████╗
 *   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
 * 
 *         DASHBOARD — LE VISAGE DE L'ARCHE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Interface de Résonance avec:
 * - Anneau Atlante (Visualiseur de Fréquence)
 * - Prisme Grec (Solide de Platon)
 * - Sentinelles (Rapa Nui & Maya)
 * - Matrice de Fond (Cunéiforme défilant)
 * - Halo Électromagnétique
 * 
 * @version 3.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = {
  1: { hz: 111, color: "#FF0000", label: "Impulsion", element: "Feu" },
  2: { hz: 222, color: "#FF7F00", label: "Dualité", element: "Eau" },
  3: { hz: 333, color: "#FFFF00", label: "Mental", element: "Air" },
  4: { hz: 444, color: "#50C878", label: "Structure", element: "Terre", isAnchor: true },
  5: { hz: 555, color: "#87CEEB", label: "Mouvement", element: "Éther" },
  6: { hz: 666, color: "#4B0082", label: "Harmonie", element: "Lumière" },
  7: { hz: 777, color: "#EE82EE", label: "Introspection", element: "Son" },
  8: { hz: 888, color: "#FFC0CB", label: "Infini", element: "Pensée" },
  9: { hz: 999, color: "#FFFDD0", label: "Unité", element: "Conscience" }
};

const PLATONIC_SOLIDS = {
  1: { name: "Tétraèdre", symbol: "🔺", element: "Feu" },
  2: { name: "Icosaèdre", symbol: "💧", element: "Eau" },
  3: { name: "Tétraèdre", symbol: "🔺", element: "Feu" },
  4: { name: "Hexaèdre", symbol: "⬛", element: "Terre" },
  5: { name: "Dodécaèdre", symbol: "⬡", element: "Éther" },
  6: { name: "Icosaèdre", symbol: "💧", element: "Eau" },
  7: { name: "Octaèdre", symbol: "◇", element: "Air" },
  8: { name: "Octaèdre", symbol: "◇", element: "Air" },
  9: { name: "Dodécaèdre", symbol: "⬡", element: "Éther" }
};

const NAWALS = [
  "Imix", "Ik", "Akbal", "Kan", "Chicchan", "Cimi", "Manik", "Lamat",
  "Muluc", "Oc", "Chuen", "Eb", "Ben", "Ix", "Men", "Cib", "Caban",
  "Etznab", "Cauac", "Ahau"
];

const CUNEIFORM_CHARS = "𒀀𒀁𒀂𒀃𒀄𒀅𒀆𒀇𒀈𒀉𒀊𒀋𒀌𒀍𒀎𒀏𒀐𒀑𒀒𒀓𒁹𒌋𒐕";

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK: useArcheEngine
// ═══════════════════════════════════════════════════════════════════════════════

const useArcheEngine = () => {
  const calculateArithmos = useCallback((word) => {
    if (!word) return { reduced: 4, frequency: 444, isArchitect: false };
    
    const sanitized = word
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toUpperCase()
      .replace(/[^A-Z]/g, '');
    
    // Sceau de l'Architecte
    if (sanitized === 'JONATHANRODRIGUE') {
      return { reduced: 9, frequency: 999, isArchitect: true };
    }
    
    const total = sanitized.split('').reduce((sum, char) => sum + (ARITHMOS_MAP[char] || 0), 0);
    let current = total;
    while (current > 9) {
      current = current.toString().split('').reduce((s, d) => s + parseInt(d), 0);
    }
    
    return {
      reduced: current || 1,
      frequency: (current || 1) * 111,
      isArchitect: false
    };
  }, []);
  
  const getMayaSign = useCallback((date = new Date()) => {
    const epoch = new Date("2012-12-21T00:00:00Z");
    const diffDays = Math.floor((date - epoch) / (1000 * 60 * 60 * 24));
    const dayNumber = ((diffDays % 260) + 260) % 260;
    const ton = (dayNumber % 13) + 1;
    const nawalIndex = dayNumber % 20;
    return {
      kin: dayNumber + 1,
      ton,
      nawal: NAWALS[nawalIndex],
      signature: `${ton} ${NAWALS[nawalIndex]}`,
      isSacred: ton === 7 || ton === 13
    };
  }, []);
  
  return { calculateArithmos, getMayaSign };
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CuneiformBackground
// ═══════════════════════════════════════════════════════════════════════════════

const CuneiformBackground = () => {
  const [chars, setChars] = useState([]);
  
  useEffect(() => {
    // Générer une grille de caractères cunéiformes
    const grid = [];
    for (let i = 0; i < 200; i++) {
      grid.push({
        char: CUNEIFORM_CHARS[Math.floor(Math.random() * CUNEIFORM_CHARS.length)],
        x: Math.random() * 100,
        y: Math.random() * 100,
        opacity: Math.random() * 0.3 + 0.05,
        speed: Math.random() * 0.5 + 0.1
      });
    }
    setChars(grid);
  }, []);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setChars(prev => prev.map(c => ({
        ...c,
        y: (c.y + c.speed) % 100
      })));
    }, 100);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      overflow: 'hidden',
      pointerEvents: 'none',
      zIndex: 0
    }}>
      {chars.map((c, i) => (
        <span
          key={i}
          style={{
            position: 'absolute',
            left: `${c.x}%`,
            top: `${c.y}%`,
            color: '#D4AF37',
            opacity: c.opacity,
            fontSize: '14px',
            fontFamily: 'serif'
          }}
        >
          {c.char}
        </span>
      ))}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: VortexVisualizer
// ═══════════════════════════════════════════════════════════════════════════════

const VortexVisualizer = ({ frequency, color, isArchitect }) => {
  const [rotation, setRotation] = useState(0);
  const [pulseScale, setPulseScale] = useState(1);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setRotation(prev => (prev + frequency / 100) % 360);
      setPulseScale(prev => 1 + Math.sin(Date.now() / (1000 - frequency)) * 0.1);
    }, 50);
    return () => clearInterval(interval);
  }, [frequency]);
  
  // Générer les cercles de Fibonacci
  const fibCircles = [1, 2, 3, 5, 8, 13, 21, 34].map((fib, i) => ({
    radius: fib * 2,
    opacity: 0.3 - i * 0.03
  }));
  
  return (
    <div style={{
      position: 'relative',
      width: '300px',
      height: '300px',
      margin: '0 auto'
    }}>
      <svg viewBox="0 0 200 200" style={{ width: '100%', height: '100%' }}>
        <defs>
          <radialGradient id="vortexGradient">
            <stop offset="0%" stopColor={color} stopOpacity="0.8" />
            <stop offset="100%" stopColor={color} stopOpacity="0" />
          </radialGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        
        {/* Cercles de Fibonacci */}
        <g transform={`rotate(${rotation}, 100, 100)`}>
          {fibCircles.map((circle, i) => (
            <circle
              key={i}
              cx="100"
              cy="100"
              r={circle.radius * pulseScale}
              fill="none"
              stroke={color}
              strokeWidth="0.5"
              opacity={circle.opacity}
            />
          ))}
        </g>
        
        {/* Spirale centrale */}
        <g transform={`rotate(${-rotation * 0.5}, 100, 100)`}>
          <path
            d={`M 100,100 
                Q ${100 + Math.cos(rotation * Math.PI / 180) * 30},${100 + Math.sin(rotation * Math.PI / 180) * 30} 
                  ${100 + Math.cos((rotation + 90) * Math.PI / 180) * 50},${100 + Math.sin((rotation + 90) * Math.PI / 180) * 50}`}
            fill="none"
            stroke="cyan"
            strokeWidth="1"
            opacity="0.6"
            filter="url(#glow)"
          />
        </g>
        
        {/* Cercle central pulsant */}
        <circle
          cx="100"
          cy="100"
          r={20 * pulseScale}
          fill="url(#vortexGradient)"
          filter="url(#glow)"
        />
        
        {/* Fréquence au centre */}
        <text
          x="100"
          y="105"
          textAnchor="middle"
          fill="white"
          fontSize="16"
          fontWeight="bold"
          style={{ textShadow: '0 0 10px ' + color }}
        >
          {frequency} Hz
        </text>
        
        {/* Indicateur Architecte */}
        {isArchitect && (
          <text
            x="100"
            y="130"
            textAnchor="middle"
            fill="#FFD700"
            fontSize="10"
          >
            👑 ARCHITECTE
          </text>
        )}
      </svg>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: GeometryDisplay
// ═══════════════════════════════════════════════════════════════════════════════

const GeometryDisplay = ({ arithmos, color }) => {
  const solid = PLATONIC_SOLIDS[arithmos] || PLATONIC_SOLIDS[4];
  const resonance = RESONANCE_MATRIX[arithmos] || RESONANCE_MATRIX[4];
  
  return (
    <div style={{
      background: 'rgba(0,0,0,0.6)',
      borderRadius: '12px',
      padding: '20px',
      border: `1px solid ${color}`,
      boxShadow: `0 0 20px ${color}40`
    }}>
      <h3 style={{ color: '#D4AF37', margin: '0 0 10px 0', fontSize: '14px' }}>
        🏛️ GÉOMÉTRIE SACRÉE
      </h3>
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
        <span style={{ fontSize: '48px' }}>{solid.symbol}</span>
        <div>
          <div style={{ color: 'white', fontWeight: 'bold' }}>{solid.name}</div>
          <div style={{ color: color, fontSize: '12px' }}>
            {solid.element} • {resonance.label}
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: StatusBar
// ═══════════════════════════════════════════════════════════════════════════════

const StatusBar = ({ maya, moaiActive }) => {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      background: 'rgba(0,0,0,0.8)',
      padding: '10px 20px',
      borderRadius: '8px',
      border: '1px solid #333',
      fontSize: '12px'
    }}>
      <span style={{ color: maya.isSacred ? '#FFD700' : '#87CEEB' }}>
        🌀 Maya: <strong>{maya.signature}</strong>
        {maya.isSacred && ' ✨ SACRÉ'}
      </span>
      <span style={{ color: '#50C878' }}>
        🗿 Moaï: <strong>{moaiActive ? 'ACTIF' : 'VEILLE'}</strong>
      </span>
      <span style={{ color: '#D4AF37' }}>
        ⚡ Kin: {maya.kin}/260
      </span>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HaloInput
// ═══════════════════════════════════════════════════════════════════════════════

const HaloInput = ({ value, onChange, color }) => {
  return (
    <div style={{
      position: 'relative',
      margin: '20px 0'
    }}>
      {/* Halo lumineux */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '120%',
        height: '200%',
        background: `radial-gradient(ellipse, ${color}40 0%, transparent 70%)`,
        pointerEvents: 'none',
        zIndex: 0
      }} />
      
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Entrez un mot ou une intention..."
        style={{
          width: '100%',
          padding: '20px',
          fontSize: '24px',
          textAlign: 'center',
          background: 'rgba(0,0,0,0.8)',
          border: `2px solid ${color}`,
          borderRadius: '12px',
          color: 'white',
          outline: 'none',
          boxShadow: `0 0 30px ${color}60, inset 0 0 20px ${color}20`,
          position: 'relative',
          zIndex: 1,
          transition: 'all 0.3s ease'
        }}
      />
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: OraclePanel
// ═══════════════════════════════════════════════════════════════════════════════

const OraclePanel = ({ frequency, geometry, maya, color }) => {
  const solid = PLATONIC_SOLIDS[Math.ceil(frequency / 111)] || PLATONIC_SOLIDS[4];
  
  return (
    <div style={{
      background: 'linear-gradient(135deg, rgba(20,20,30,0.9), rgba(10,10,20,0.95))',
      borderRadius: '16px',
      padding: '20px',
      border: `1px solid ${color}`,
      marginTop: '20px'
    }}>
      <h3 style={{ color: '#D4AF37', margin: '0 0 15px 0' }}>
        📜 ORACLE
      </h3>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '10px',
        fontSize: '14px'
      }}>
        <div style={{ color: '#87CEEB' }}>
          <strong>Fréquence:</strong> {frequency} Hz
        </div>
        <div style={{ color: '#50C878' }}>
          <strong>Géométrie:</strong> {solid.name}
        </div>
        <div style={{ color: '#EE82EE' }}>
          <strong>Cycle Maya:</strong> {maya.signature}
        </div>
        <div style={{ color: '#FFD700' }}>
          <strong>Élément:</strong> {solid.element}
        </div>
      </div>
      
      <div style={{
        marginTop: '15px',
        padding: '15px',
        background: 'rgba(0,0,0,0.5)',
        borderRadius: '8px',
        borderLeft: `4px solid ${color}`
      }}>
        <p style={{ color: 'white', margin: 0, fontStyle: 'italic' }}>
          {solid.symbol} Le {solid.name} ({solid.element}) vibre à {frequency} Hz
          sous l'énergie de {maya.nawal}.
        </p>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: ArcheDashboard
// ═══════════════════════════════════════════════════════════════════════════════

const ArcheDashboard = () => {
  const [inputWord, setInputWord] = useState('');
  const [resonance, setResonance] = useState(null);
  const { calculateArithmos, getMayaSign } = useArcheEngine();
  const [maya, setMaya] = useState({ signature: '', kin: 0, nawal: '', isSacred: false });
  
  // Calculer Maya au chargement
  useEffect(() => {
    setMaya(getMayaSign());
    
    // Mettre à jour à minuit
    const now = new Date();
    const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
    const msUntilMidnight = tomorrow - now;
    
    const timeout = setTimeout(() => {
      setMaya(getMayaSign());
    }, msUntilMidnight);
    
    return () => clearTimeout(timeout);
  }, [getMayaSign]);
  
  // Calculer la résonance quand l'input change
  useEffect(() => {
    const timer = setTimeout(() => {
      if (inputWord.trim()) {
        const result = calculateArithmos(inputWord);
        setResonance({
          ...result,
          resonanceData: RESONANCE_MATRIX[result.reduced] || RESONANCE_MATRIX[4]
        });
      } else {
        setResonance(null);
      }
    }, 300);
    
    return () => clearTimeout(timer);
  }, [inputWord, calculateArithmos]);
  
  const currentColor = resonance?.resonanceData?.color || '#50C878';
  const currentFrequency = resonance?.frequency || 444;
  
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(180deg, #050505 0%, #0a0a15 50%, #050510 100%)',
      color: '#D4AF37',
      fontFamily: "'Cinzel', 'Times New Roman', serif",
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Fond cunéiforme */}
      <CuneiformBackground />
      
      {/* Contenu principal */}
      <div style={{
        position: 'relative',
        zIndex: 1,
        maxWidth: '800px',
        margin: '0 auto',
        padding: '40px 20px'
      }}>
        {/* Header */}
        <header style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{
            fontSize: '36px',
            fontWeight: 'bold',
            margin: 0,
            textShadow: '0 0 30px rgba(212,175,55,0.5)'
          }}>
            ⚡ ARCHE DASHBOARD ⚡
          </h1>
          <p style={{
            color: 'rgba(255,255,255,0.6)',
            fontSize: '14px',
            marginTop: '10px'
          }}>
            Interface de Résonance — 12 Civilisations Unifiées
          </p>
        </header>
        
        {/* Barre de statut Maya/Moaï */}
        <StatusBar maya={maya} moaiActive={true} />
        
        {/* Input avec Halo */}
        <HaloInput
          value={inputWord}
          onChange={setInputWord}
          color={currentColor}
        />
        
        {/* Visualiseur Vortex */}
        <VortexVisualizer
          frequency={currentFrequency}
          color={currentColor}
          isArchitect={resonance?.isArchitect}
        />
        
        {/* Panneau Géométrie */}
        {resonance && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '20px',
            marginTop: '30px'
          }}>
            <GeometryDisplay
              arithmos={resonance.reduced}
              color={currentColor}
            />
            
            <div style={{
              background: 'rgba(0,0,0,0.6)',
              borderRadius: '12px',
              padding: '20px',
              border: `1px solid ${currentColor}`,
              boxShadow: `0 0 20px ${currentColor}40`
            }}>
              <h3 style={{ color: '#D4AF37', margin: '0 0 10px 0', fontSize: '14px' }}>
                🔮 CRISTAL ATLANTE
              </h3>
              <div style={{ color: 'white' }}>
                <div style={{ fontSize: '24px', marginBottom: '5px' }}>💎</div>
                <div>
                  {currentFrequency === 999 ? 'Cristal de Record' :
                   currentFrequency >= 777 ? 'Améthyste Royale' :
                   currentFrequency >= 555 ? 'Aigue-Marine' :
                   currentFrequency >= 444 ? 'Quartz Rose' :
                   'Quartz Clair'}
                </div>
                <div style={{ color: currentColor, fontSize: '12px', marginTop: '5px' }}>
                  Niveau d'Accès: {
                    currentFrequency >= 888 ? 'Temple de Poséidon' :
                    currentFrequency >= 666 ? 'Citadelle des Cristaux' :
                    currentFrequency >= 444 ? 'Zone de Calcul' :
                    'Périphérie'
                  }
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Oracle Panel */}
        {resonance && (
          <OraclePanel
            frequency={currentFrequency}
            geometry={PLATONIC_SOLIDS[resonance.reduced]}
            maya={maya}
            color={currentColor}
          />
        )}
        
        {/* Footer */}
        <footer style={{
          textAlign: 'center',
          marginTop: '40px',
          padding: '20px',
          borderTop: '1px solid rgba(212,175,55,0.2)'
        }}>
          <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: '12px', margin: 0 }}>
            AT·OM v3.0 — Heartbeat: 444 Hz — Architecte: Jonathan Rodrigue (999 Hz)
          </p>
          <p style={{ color: 'rgba(212,175,55,0.6)', fontSize: '10px', marginTop: '5px' }}>
            "Le code est de la pierre liquide. La pierre est du code figé."
          </p>
        </footer>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

export default ArcheDashboard;
export { useArcheEngine, VortexVisualizer, GeometryDisplay, StatusBar, HaloInput };
