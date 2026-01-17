/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * CHE·NU™ / AT·OM — HARMONISEUR COMPONENT
 * ═══════════════════════════════════════════════════════════════════════════════
 * [AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12
 * 
 * Composant React qui affiche les Séquences d'Activation en boucle continue.
 * Se synchronise avec le signal WebSocket 4.44s du backend.
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const SIGNAL_INTERVAL = 4440; // 4.44 secondes en ms
const ANCHOR_FREQUENCY = 444;

const ACTIVATION_SEQUENCES = {
  past: {
    code: "781901942",
    intent: "J'Harmonise notre passé",
    frequency: 111,
    color: "#8B5CF6",
    element: "Terre",
    icon: "◀"
  },
  present: {
    code: "71042",
    intent: "J'harmonise notre présent",
    frequency: 444,
    color: "#10B981",
    element: "Cœur",
    icon: "●"
  },
  future: {
    code: "14872191",
    intent: "J'harmonise notre futur",
    frequency: 777,
    color: "#3B82F6",
    element: "Vision",
    icon: "▶"
  },
  restoration: {
    code: "8888848888819751",
    intent: "Pour notre rétablissement",
    frequency: 999,
    color: "#F59E0B",
    element: "Source",
    icon: "✧"
  }
};

const PHASE_ORDER = ['past', 'present', 'future', 'restoration'];

// ═══════════════════════════════════════════════════════════════════════════════
// STYLES
// ═══════════════════════════════════════════════════════════════════════════════

const styles = {
  container: {
    position: 'fixed',
    bottom: 0,
    left: 0,
    right: 0,
    background: 'linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.8) 100%)',
    padding: '20px',
    zIndex: 9999,
    fontFamily: "'Inter', -apple-system, sans-serif"
  },
  
  inner: {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '20px'
  },
  
  phaseIndicators: {
    display: 'flex',
    gap: '8px'
  },
  
  phaseIndicator: (isActive, color) => ({
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    background: isActive ? color : 'rgba(255,255,255,0.2)',
    boxShadow: isActive ? `0 0 10px ${color}` : 'none',
    transition: 'all 0.3s ease'
  }),
  
  mainDisplay: {
    flex: 1,
    textAlign: 'center'
  },
  
  code: (color) => ({
    fontSize: '24px',
    fontWeight: 'bold',
    fontFamily: "'JetBrains Mono', monospace",
    color: color,
    letterSpacing: '3px',
    textShadow: `0 0 20px ${color}`,
    marginBottom: '4px'
  }),
  
  intent: {
    fontSize: '14px',
    color: 'rgba(255,255,255,0.8)',
    fontStyle: 'italic'
  },
  
  frequency: (color) => ({
    fontSize: '12px',
    color: color,
    opacity: 0.8
  }),
  
  signalInfo: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
    gap: '4px'
  },
  
  tick: {
    fontSize: '10px',
    color: 'rgba(255,255,255,0.5)',
    fontFamily: "'JetBrains Mono', monospace"
  },
  
  pulse: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#10B981',
    animation: 'pulse 4.44s infinite'
  },
  
  // Version minimale pour mobile
  minimalContainer: {
    position: 'fixed',
    bottom: '10px',
    left: '50%',
    transform: 'translateX(-50%)',
    background: 'rgba(0,0,0,0.7)',
    padding: '8px 16px',
    borderRadius: '20px',
    zIndex: 9999,
    backdropFilter: 'blur(10px)'
  },
  
  minimalCode: (color) => ({
    fontSize: '14px',
    fontWeight: 'bold',
    fontFamily: "'JetBrains Mono', monospace",
    color: color,
    letterSpacing: '2px'
  })
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const Harmoniseur = ({ 
  minimal = false, 
  websocket = null,
  onPhaseChange = null 
}) => {
  const [currentPhaseIndex, setCurrentPhaseIndex] = useState(0);
  const [tick, setTick] = useState(0);
  const [isConnected, setIsConnected] = useState(false);
  const intervalRef = useRef(null);
  
  const currentPhase = PHASE_ORDER[currentPhaseIndex];
  const sequence = ACTIVATION_SEQUENCES[currentPhase];

  // ─────────────────────────────────────────────────────────────────────────────
  // Synchronisation WebSocket
  // ─────────────────────────────────────────────────────────────────────────────
  
  useEffect(() => {
    if (websocket) {
      const handleMessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === 'heartbeat' && data.harmonization) {
            const phaseIndex = PHASE_ORDER.indexOf(data.harmonization.phase);
            if (phaseIndex !== -1) {
              setCurrentPhaseIndex(phaseIndex);
              setTick(data.tick);
              setIsConnected(true);
              
              if (onPhaseChange) {
                onPhaseChange(data.harmonization);
              }
            }
          }
        } catch (e) {
          console.error('[Harmoniseur] Parse error:', e);
        }
      };
      
      websocket.addEventListener('message', handleMessage);
      
      return () => {
        websocket.removeEventListener('message', handleMessage);
      };
    }
  }, [websocket, onPhaseChange]);

  // ─────────────────────────────────────────────────────────────────────────────
  // Fallback: Timer local si pas de WebSocket
  // ─────────────────────────────────────────────────────────────────────────────
  
  useEffect(() => {
    if (!websocket || !isConnected) {
      intervalRef.current = setInterval(() => {
        setCurrentPhaseIndex(prev => (prev + 1) % PHASE_ORDER.length);
        setTick(prev => prev + 1);
      }, SIGNAL_INTERVAL);
      
      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [websocket, isConnected]);

  // ─────────────────────────────────────────────────────────────────────────────
  // Rendu minimal (mobile)
  // ─────────────────────────────────────────────────────────────────────────────
  
  if (minimal) {
    return (
      <div style={styles.minimalContainer}>
        <span style={styles.minimalCode(sequence.color)}>
          {sequence.icon} {sequence.code}
        </span>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // Rendu complet
  // ─────────────────────────────────────────────────────────────────────────────
  
  return (
    <div style={styles.container}>
      <div style={styles.inner}>
        
        {/* Indicateurs de phase */}
        <div style={styles.phaseIndicators}>
          {PHASE_ORDER.map((phase, index) => (
            <div 
              key={phase}
              style={styles.phaseIndicator(
                index === currentPhaseIndex,
                ACTIVATION_SEQUENCES[phase].color
              )}
              title={ACTIVATION_SEQUENCES[phase].intent}
            />
          ))}
        </div>
        
        {/* Affichage principal */}
        <div style={styles.mainDisplay}>
          <div style={styles.code(sequence.color)}>
            {sequence.icon} {sequence.code} {sequence.icon}
          </div>
          <div style={styles.intent}>
            {sequence.intent}
          </div>
          <div style={styles.frequency(sequence.color)}>
            {sequence.frequency}Hz • {sequence.element}
          </div>
        </div>
        
        {/* Info signal */}
        <div style={styles.signalInfo}>
          <div style={styles.pulse} />
          <div style={styles.tick}>
            {ANCHOR_FREQUENCY}Hz • 4.44s
          </div>
          <div style={styles.tick}>
            Tick #{tick}
          </div>
        </div>
        
      </div>
      
      {/* Keyframe animation */}
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(1.5); }
        }
      `}</style>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK PERSONNALISÉ
// ═══════════════════════════════════════════════════════════════════════════════

export const useHarmonization = () => {
  const [phase, setPhase] = useState('present');
  const [sequence, setSequence] = useState(ACTIVATION_SEQUENCES.present);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setPhase(prev => {
        const currentIndex = PHASE_ORDER.indexOf(prev);
        const nextIndex = (currentIndex + 1) % PHASE_ORDER.length;
        const nextPhase = PHASE_ORDER[nextIndex];
        setSequence(ACTIVATION_SEQUENCES[nextPhase]);
        return nextPhase;
      });
    }, SIGNAL_INTERVAL);
    
    return () => clearInterval(interval);
  }, []);
  
  return { phase, sequence, ACTIVATION_SEQUENCES };
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export { ACTIVATION_SEQUENCES, PHASE_ORDER, SIGNAL_INTERVAL, ANCHOR_FREQUENCY };
export default Harmoniseur;
