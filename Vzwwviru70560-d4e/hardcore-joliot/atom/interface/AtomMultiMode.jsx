/**
 * AT·OM — AtomMultiMode.jsx
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * UN MOTEUR, PLUSIEURS PARURES
 * 
 * Modes visuels disponibles:
 * 1. 🔮 SPHÈRES   - Les 9 cercles concentriques élégants
 * 2. 🌀 ORACLES   - L'Arche des 18 Oracles (complet)
 * 3. 📊 MATRICE   - Grille minimaliste 1-9
 * 4. 🧘 ZEN       - Mode méditatif épuré
 * 
 * Tous les modes utilisent le même moteur: useAtomResonance
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION MAÎTRE
// ═══════════════════════════════════════════════════════════════════════════════

const SYSTEM_HEARTBEAT = 444;
const TRANSITION_DURATION = 600;
const DEBOUNCE_DELAY = 300;

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = [
  { level: 1, label: "Impulsion/ADN", hz: 111, color: "#FF0000", delay: 900 },
  { level: 2, label: "Dualité/Partage", hz: 222, color: "#FF7F00", delay: 800 },
  { level: 3, label: "Mental/Géométrie", hz: 333, color: "#FFFF00", delay: 700 },
  { level: 4, label: "Structure/Silence", hz: 444, color: "#50C878", delay: 600, isAnchor: true },
  { level: 5, label: "Mouvement/Feu", hz: 555, color: "#87CEEB", delay: 500 },
  { level: 6, label: "Harmonie/Protection", hz: 666, color: "#4B0082", delay: 400 },
  { level: 7, label: "Introspection", hz: 777, color: "#EE82EE", delay: 300 },
  { level: 8, label: "Infini/Abondance", hz: 888, color: "#FFC0CB", delay: 200 },
  { level: 9, label: "Unité/Acier", hz: 999, color: "#FFFDD0", delay: 100 },
];

const FOUNDATION_STONES = {
  FEU: 5, ACIER: 9, IA: 1, ADN: 1, SILENCE: 4
};

const TRANSITION_NODES = {
  DUALITE: 2, MENTAL: 3, HARMONIE: 6, SPIRITUALITE: 7, INFINI: 8
};

// ═══════════════════════════════════════════════════════════════════════════════
// MOTEUR ARITHMOS (Hook intégré)
// ═══════════════════════════════════════════════════════════════════════════════

const sanitize = (input) => {
  if (!input || typeof input !== 'string') return '';
  return input.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase().replace(/[^A-Z]/g, "");
};

const calculateArithmos = (word) => {
  if (!word) return 0;
  let total = [...word].reduce((sum, char) => sum + (ARITHMOS_MAP[char] || 0), 0);
  while (total > 9) {
    total = [...String(total)].reduce((sum, d) => sum + parseInt(d, 10), 0);
  }
  return total;
};

const getResonance = (level) => RESONANCE_MATRIX.find(r => r.level === level) || RESONANCE_MATRIX[3];

const useAtomResonance = (input) => {
  const [resonance, setResonance] = useState(null);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const debounceRef = useRef(null);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    
    debounceRef.current = setTimeout(() => {
      if (!input?.trim()) {
        setResonance(null);
        return;
      }

      const clean = sanitize(input);
      if (!clean) {
        setResonance(null);
        return;
      }

      // Détection Pierre/Nœud ou calcul standard
      let level;
      let type = 'standard';
      
      if (FOUNDATION_STONES[clean] !== undefined) {
        level = FOUNDATION_STONES[clean];
        type = 'stone';
      } else if (TRANSITION_NODES[clean] !== undefined) {
        level = TRANSITION_NODES[clean];
        type = 'node';
      } else {
        level = calculateArithmos(clean);
      }

      const data = getResonance(level);
      
      setIsTransitioning(true);
      setResonance({
        word: clean,
        level,
        hz: data.hz,
        color: data.color,
        delay: data.delay,
        label: data.label,
        type,
        isAnchor: data.isAnchor || false
      });

      // Log console stylisé
      console.log(
        `%c AT·OM %c ${type === 'stone' ? '🧱' : type === 'node' ? '🌀' : '📝'} %c ${clean} → ${level} → ${data.hz}Hz`,
        'background: #50C878; color: white; padding: 2px 6px; border-radius: 3px;',
        'background: #1a1a2e; color: #888; padding: 2px 4px;',
        `color: ${data.color}; font-weight: bold;`
      );

      setTimeout(() => setIsTransitioning(false), TRANSITION_DURATION);
    }, DEBOUNCE_DELAY);

    return () => clearTimeout(debounceRef.current);
  }, [input]);

  return { resonance, isTransitioning };
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODE 1: SPHÈRES (9 cercles concentriques)
// ═══════════════════════════════════════════════════════════════════════════════

const SpheresMode = ({ resonance, isTransitioning }) => {
  const activeLevel = resonance?.level || 0;
  
  return (
    <div style={{
      position: 'relative',
      width: '400px',
      height: '400px',
      margin: '2rem auto',
    }}>
      {/* Les 9 sphères concentriques */}
      {RESONANCE_MATRIX.map((item, index) => {
        const size = 400 - (index * 40);
        const isActive = item.level <= activeLevel;
        const isCurrent = item.level === activeLevel;
        
        return (
          <div
            key={item.level}
            style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              width: `${size}px`,
              height: `${size}px`,
              transform: 'translate(-50%, -50%)',
              borderRadius: '50%',
              border: `2px solid ${isActive ? item.color : '#333'}`,
              background: isCurrent 
                ? `radial-gradient(circle, ${item.color}40 0%, transparent 70%)`
                : 'transparent',
              boxShadow: isCurrent 
                ? `0 0 30px ${item.color}, inset 0 0 30px ${item.color}30`
                : 'none',
              transition: `all ${TRANSITION_DURATION}ms ease-out`,
              opacity: isActive ? 1 : 0.3,
            }}
          >
            {/* Indicateur de niveau */}
            {isCurrent && (
              <div style={{
                position: 'absolute',
                top: '10px',
                left: '50%',
                transform: 'translateX(-50%)',
                fontSize: '0.7rem',
                color: item.color,
                fontWeight: 'bold',
              }}>
                {item.hz}Hz
              </div>
            )}
          </div>
        );
      })}
      
      {/* Centre - Mot actif */}
      {resonance && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          zIndex: 10,
        }}>
          <div style={{
            fontSize: '1.5rem',
            fontWeight: 'bold',
            color: resonance.color,
            textShadow: `0 0 20px ${resonance.color}`,
          }}>
            {resonance.word}
          </div>
          <div style={{ 
            fontSize: '2.5rem', 
            fontWeight: 200,
            color: resonance.color 
          }}>
            {resonance.level}
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODE 2: ORACLES (18 oracles en cercles)
// ═══════════════════════════════════════════════════════════════════════════════

const OraclesMode = ({ resonance, isTransitioning }) => {
  const activeLevel = resonance?.level || 0;
  
  // Générer les 18 oracles
  const oracles = Array.from({ length: 18 }, (_, i) => ({
    id: i + 1,
    angle: (i * 20) - 90, // 360/18 = 20 degrés
  }));
  
  // Déterminer quels oracles sont actifs selon le niveau
  const getOracleState = (oracleId) => {
    if (!resonance) return 'inactive';
    // Logique: les oracles s'activent par paires selon le niveau
    const oracleLevel = Math.ceil(oracleId / 2);
    if (oracleLevel === activeLevel) return 'primary';
    if (oracleLevel <= activeLevel) return 'active';
    return 'inactive';
  };

  return (
    <div style={{
      position: 'relative',
      width: '450px',
      height: '450px',
      margin: '2rem auto',
    }}>
      {/* Cercles de fond (5 cercles) */}
      {[1, 2, 3, 4, 5].map(circle => (
        <div
          key={circle}
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            width: `${circle * 80}px`,
            height: `${circle * 80}px`,
            transform: 'translate(-50%, -50%)',
            borderRadius: '50%',
            border: `1px solid ${resonance?.color || '#333'}30`,
            transition: `all ${TRANSITION_DURATION}ms ease-out`,
          }}
        />
      ))}
      
      {/* Les 18 Oracles */}
      {oracles.map(oracle => {
        const state = getOracleState(oracle.id);
        const radius = 180;
        const x = Math.cos((oracle.angle * Math.PI) / 180) * radius;
        const y = Math.sin((oracle.angle * Math.PI) / 180) * radius;
        
        return (
          <div
            key={oracle.id}
            style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              width: '36px',
              height: '36px',
              transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
              borderRadius: '50%',
              background: state === 'primary' 
                ? resonance?.color 
                : state === 'active' 
                  ? `${resonance?.color}60`
                  : '#222',
              border: `2px solid ${state !== 'inactive' ? resonance?.color : '#444'}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '0.75rem',
              fontWeight: state === 'primary' ? 'bold' : 'normal',
              color: state === 'primary' ? '#000' : state === 'active' ? resonance?.color : '#666',
              transition: `all ${TRANSITION_DURATION}ms ease-out`,
              boxShadow: state === 'primary' ? `0 0 15px ${resonance?.color}` : 'none',
              cursor: 'pointer',
            }}
          >
            {oracle.id}
          </div>
        );
      })}
      
      {/* Centre */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '100px',
        height: '100px',
        borderRadius: '50%',
        background: resonance ? `${resonance.color}20` : '#1a1a2e',
        border: `3px solid ${resonance?.color || '#444'}`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        transition: `all ${TRANSITION_DURATION}ms ease-out`,
        boxShadow: resonance ? `0 0 30px ${resonance.color}40` : 'none',
      }}>
        {resonance ? (
          <>
            <div style={{ fontSize: '0.7rem', color: '#888' }}>{resonance.hz}Hz</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: resonance.color }}>
              {resonance.level}
            </div>
            <div style={{ fontSize: '0.6rem', color: resonance.color }}>{resonance.word}</div>
          </>
        ) : (
          <div style={{ fontSize: '0.8rem', color: '#666' }}>AT·OM</div>
        )}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODE 3: MATRICE (Grille 3x3)
// ═══════════════════════════════════════════════════════════════════════════════

const MatriceMode = ({ resonance, isTransitioning }) => {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: '0.5rem',
      maxWidth: '300px',
      margin: '2rem auto',
      padding: '1rem',
    }}>
      {RESONANCE_MATRIX.map(item => {
        const isActive = item.level === resonance?.level;
        
        return (
          <div
            key={item.level}
            style={{
              aspectRatio: '1',
              background: isActive ? item.color : `${item.color}20`,
              borderRadius: '12px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              transition: `all ${TRANSITION_DURATION}ms ease-out`,
              transform: isActive ? 'scale(1.1)' : 'scale(1)',
              boxShadow: isActive ? `0 0 25px ${item.color}` : 'none',
              cursor: 'pointer',
            }}
          >
            <div style={{ 
              fontSize: '1.5rem', 
              fontWeight: 'bold',
              color: isActive ? '#000' : item.color,
            }}>
              {item.level}
            </div>
            <div style={{ 
              fontSize: '0.6rem',
              color: isActive ? '#333' : '#888',
            }}>
              {item.hz}Hz
            </div>
          </div>
        );
      })}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODE 4: ZEN (Minimaliste)
// ═══════════════════════════════════════════════════════════════════════════════

const ZenMode = ({ resonance, isTransitioning }) => {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '300px',
      margin: '2rem auto',
    }}>
      {/* Cercle unique pulsant */}
      <div style={{
        width: '200px',
        height: '200px',
        borderRadius: '50%',
        background: resonance 
          ? `radial-gradient(circle, ${resonance.color}60 0%, transparent 70%)`
          : 'radial-gradient(circle, #50C87830 0%, transparent 70%)',
        border: `2px solid ${resonance?.color || '#50C878'}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: `all ${TRANSITION_DURATION}ms ease-out`,
        animation: resonance ? `breathe ${resonance.delay * 4}ms ease-in-out infinite` : 'breathe 2400ms ease-in-out infinite',
      }}>
        <div style={{ textAlign: 'center' }}>
          {resonance ? (
            <>
              <div style={{ 
                fontSize: '4rem', 
                fontWeight: 200,
                color: resonance.color,
                lineHeight: 1,
              }}>
                {resonance.level}
              </div>
              <div style={{ 
                fontSize: '1rem',
                color: resonance.color,
                opacity: 0.8,
              }}>
                {resonance.hz} Hz
              </div>
            </>
          ) : (
            <div style={{ fontSize: '3rem', color: '#50C878', fontWeight: 200 }}>∞</div>
          )}
        </div>
      </div>
      
      {/* Mot en dessous */}
      {resonance && (
        <div style={{
          marginTop: '2rem',
          fontSize: '1.2rem',
          color: resonance.color,
          letterSpacing: '0.3em',
          opacity: isTransitioning ? 0.5 : 1,
          transition: `opacity ${TRANSITION_DURATION}ms ease-out`,
        }}>
          {resonance.word}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const MODES = [
  { id: 'spheres', icon: '🔮', name: 'Sphères', component: SpheresMode },
  { id: 'oracles', icon: '🌀', name: 'Oracles', component: OraclesMode },
  { id: 'matrice', icon: '📊', name: 'Matrice', component: MatriceMode },
  { id: 'zen', icon: '🧘', name: 'Zen', component: ZenMode },
];

const AtomMultiMode = () => {
  const [inputValue, setInputValue] = useState('');
  const [activeMode, setActiveMode] = useState('spheres');
  const { resonance, isTransitioning } = useAtomResonance(inputValue);
  
  const ActiveComponent = MODES.find(m => m.id === activeMode)?.component || SpheresMode;

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%)',
      color: 'white',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      padding: '1rem',
    }}>
      {/* En-tête */}
      <header style={{ textAlign: 'center', marginBottom: '1rem' }}>
        <h1 style={{ 
          fontSize: '2rem', 
          fontWeight: 200,
          letterSpacing: '0.3em',
          color: resonance?.color || '#50C878',
          transition: `color ${TRANSITION_DURATION}ms ease-out`,
          margin: 0,
        }}>
          AT·OM
        </h1>
        <p style={{ color: '#666', fontSize: '0.75rem', margin: '0.25rem 0 0' }}>
          {SYSTEM_HEARTBEAT} Hz
        </p>
      </header>

      {/* Sélecteur de Mode */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '0.5rem',
        marginBottom: '1rem',
      }}>
        {MODES.map(mode => (
          <button
            key={mode.id}
            onClick={() => setActiveMode(mode.id)}
            style={{
              padding: '0.5rem 1rem',
              background: activeMode === mode.id 
                ? (resonance?.color || '#50C878') 
                : 'rgba(255,255,255,0.05)',
              border: `1px solid ${activeMode === mode.id ? 'transparent' : '#333'}`,
              borderRadius: '20px',
              color: activeMode === mode.id ? '#000' : '#888',
              cursor: 'pointer',
              fontSize: '0.85rem',
              transition: `all ${TRANSITION_DURATION}ms ease-out`,
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem',
            }}
          >
            <span>{mode.icon}</span>
            <span>{mode.name}</span>
          </button>
        ))}
      </div>

      {/* Champ de saisie */}
      <div style={{ 
        maxWidth: '400px', 
        margin: '0 auto 1rem',
      }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Entrez un mot..."
          style={{
            width: '100%',
            padding: '0.75rem 1rem',
            fontSize: '1.25rem',
            background: 'rgba(255,255,255,0.05)',
            border: `2px solid ${resonance?.color || '#333'}`,
            borderRadius: '12px',
            color: 'white',
            outline: 'none',
            textAlign: 'center',
            transition: `all ${TRANSITION_DURATION}ms ease-out`,
            boxShadow: resonance ? `0 0 20px ${resonance.color}30` : 'none',
          }}
        />
      </div>

      {/* Boutons rapides */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '0.25rem',
        marginBottom: '1rem',
        flexWrap: 'wrap',
        maxWidth: '500px',
        margin: '0 auto 1rem',
      }}>
        {['FEU', 'ACIER', 'SILENCE', 'AMOUR', 'EAU', 'VIE'].map(word => (
          <button
            key={word}
            onClick={() => setInputValue(word)}
            style={{
              padding: '0.4rem 0.8rem',
              background: inputValue.toUpperCase() === word 
                ? (resonance?.color || '#50C878')
                : 'rgba(255,255,255,0.05)',
              border: 'none',
              borderRadius: '15px',
              color: inputValue.toUpperCase() === word ? '#000' : '#888',
              cursor: 'pointer',
              fontSize: '0.75rem',
              transition: 'all 200ms',
            }}
          >
            {word}
          </button>
        ))}
      </div>

      {/* Zone de visualisation */}
      <ActiveComponent resonance={resonance} isTransitioning={isTransitioning} />

      {/* Feedback */}
      {resonance && (
        <div style={{
          textAlign: 'center',
          padding: '1rem',
          background: `${resonance.color}10`,
          borderRadius: '12px',
          maxWidth: '400px',
          margin: '0 auto',
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            gap: '2rem',
            marginBottom: '0.5rem',
          }}>
            <div>
              <div style={{ color: '#666', fontSize: '0.7rem' }}>NIVEAU</div>
              <div style={{ color: resonance.color, fontSize: '1.5rem', fontWeight: 'bold' }}>
                {resonance.level}
              </div>
            </div>
            <div>
              <div style={{ color: '#666', fontSize: '0.7rem' }}>FRÉQUENCE</div>
              <div style={{ color: resonance.color, fontSize: '1.5rem', fontWeight: 'bold' }}>
                {resonance.hz}Hz
              </div>
            </div>
            <div>
              <div style={{ color: '#666', fontSize: '0.7rem' }}>DÉLAI</div>
              <div style={{ color: resonance.color, fontSize: '1.5rem', fontWeight: 'bold' }}>
                {resonance.delay}ms
              </div>
            </div>
          </div>
          <div style={{ 
            color: resonance.color, 
            fontSize: '0.85rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem',
          }}>
            {resonance.type === 'stone' && '🧱'}
            {resonance.type === 'node' && '🌀'}
            {resonance.type === 'standard' && '📝'}
            {resonance.label}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer style={{ 
        textAlign: 'center', 
        marginTop: '2rem', 
        color: '#444',
        fontSize: '0.7rem',
      }}>
        <p>Architecte: Jonathan Rodrigue (999 Hz) | Oracle 17</p>
      </footer>

      {/* Animation keyframes */}
      <style>{`
        @keyframes breathe {
          0%, 100% { transform: scale(1); opacity: 0.8; }
          50% { transform: scale(1.05); opacity: 1; }
        }
        
        input::placeholder {
          color: #555;
        }
        
        * {
          box-sizing: border-box;
        }
      `}</style>
    </div>
  );
};

export default AtomMultiMode;
