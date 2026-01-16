/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * UNIVERSAL RESONANCE INTERFACE — L'ARCHE UNIVERSELLE
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   █████╗ ████████╗    ██████╗ ███╗   ███╗
 *  ██╔══██╗╚══██╔══╝   ██╔═══██╗████╗ ████║
 *  ███████║   ██║      ██║   ██║██╔████╔██║
 *  ██╔══██║   ██║      ██║   ██║██║╚██╔╝██║
 *  ██║  ██║   ██║   ██╗╚██████╔╝██║ ╚═╝ ██║
 *  ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝
 * 
 *              UNIVERSAL RESONANCE INTERFACE v2.0
 * 
 * L'interface visuelle complète intégrant:
 * - L'Arche des 9 Résonances (Arithmos)
 * - Le Cercle des 20 Nawals (Maya)
 * - L'Arbre de Vie simplifié (Kabbale)
 * - Les 7 Chakras (Indien)
 * - Motifs Cymatiques animés
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import useUniversalResonance, { 
  RESONANCE_MATRIX, 
  NAWALS, 
  TONS,
  CHAKRAS,
  PHI 
} from './useUniversalResonance';

// ═══════════════════════════════════════════════════════════════════════════════
// STYLES
// ═══════════════════════════════════════════════════════════════════════════════

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%)',
    color: '#ffffff',
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    padding: '20px',
    position: 'relative',
    overflow: 'hidden'
  },
  
  header: {
    textAlign: 'center',
    marginBottom: '20px'
  },
  
  title: {
    fontSize: '2.5rem',
    fontWeight: 300,
    letterSpacing: '0.3em',
    background: 'linear-gradient(90deg, #FFD700, #FFFDD0, #FFD700)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    marginBottom: '10px'
  },
  
  subtitle: {
    fontSize: '0.9rem',
    opacity: 0.7,
    letterSpacing: '0.2em'
  },
  
  mainContent: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '30px'
  },
  
  inputContainer: {
    width: '100%',
    maxWidth: '500px',
    textAlign: 'center'
  },
  
  input: {
    width: '100%',
    padding: '15px 25px',
    fontSize: '1.5rem',
    textAlign: 'center',
    background: 'rgba(255,255,255,0.05)',
    border: '2px solid rgba(255,255,255,0.2)',
    borderRadius: '50px',
    color: '#fff',
    outline: 'none',
    transition: 'all 0.6s ease',
    letterSpacing: '0.1em'
  },
  
  archeContainer: {
    position: 'relative',
    width: '400px',
    height: '400px'
  },
  
  nawalRing: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    borderRadius: '50%',
    border: '1px solid rgba(255,255,255,0.1)'
  },
  
  nawalDot: {
    position: 'absolute',
    width: '24px',
    height: '24px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '10px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    border: '2px solid rgba(255,255,255,0.3)'
  },
  
  resonanceCircle: {
    position: 'absolute',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
    cursor: 'pointer'
  },
  
  centerHub: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '120px',
    height: '120px',
    borderRadius: '50%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    transition: 'all 0.6s ease'
  },
  
  frequencyDisplay: {
    fontSize: '2rem',
    fontWeight: 'bold'
  },
  
  labelDisplay: {
    fontSize: '0.8rem',
    opacity: 0.8,
    marginTop: '5px'
  },
  
  infoPanel: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
    width: '100%',
    maxWidth: '800px'
  },
  
  infoCard: {
    background: 'rgba(255,255,255,0.05)',
    borderRadius: '15px',
    padding: '15px',
    border: '1px solid rgba(255,255,255,0.1)',
    transition: 'all 0.3s ease'
  },
  
  infoTitle: {
    fontSize: '0.75rem',
    opacity: 0.6,
    marginBottom: '5px',
    textTransform: 'uppercase',
    letterSpacing: '0.1em'
  },
  
  infoValue: {
    fontSize: '1.1rem',
    fontWeight: 500
  },
  
  mayaPanel: {
    background: 'rgba(255,215,0,0.1)',
    borderRadius: '15px',
    padding: '20px',
    border: '1px solid rgba(255,215,0,0.3)',
    maxWidth: '400px',
    textAlign: 'center'
  },
  
  chakraBar: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
    padding: '10px',
    background: 'rgba(255,255,255,0.05)',
    borderRadius: '10px'
  },
  
  chakraDot: {
    height: '20px',
    borderRadius: '10px',
    transition: 'all 0.3s ease',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '0.7rem'
  },
  
  debugConsole: {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    background: 'rgba(0,0,0,0.8)',
    border: '1px solid rgba(255,255,255,0.2)',
    borderRadius: '10px',
    padding: '15px',
    fontFamily: 'monospace',
    fontSize: '0.85rem',
    minWidth: '250px',
    zIndex: 1000
  },
  
  debugTitle: {
    fontSize: '0.7rem',
    opacity: 0.5,
    marginBottom: '10px',
    borderBottom: '1px solid rgba(255,255,255,0.2)',
    paddingBottom: '5px'
  },
  
  gratitudeOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0,0,0,0.9)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 2000,
    opacity: 0,
    pointerEvents: 'none',
    transition: 'opacity 0.5s ease'
  },
  
  gratitudeText: {
    textAlign: 'center',
    maxWidth: '600px',
    padding: '40px'
  },
  
  modeSelector: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px'
  },
  
  modeButton: {
    padding: '8px 16px',
    borderRadius: '20px',
    border: '1px solid rgba(255,255,255,0.3)',
    background: 'transparent',
    color: '#fff',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    fontSize: '0.85rem'
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

export default function UniversalResonanceInterface() {
  // ─────────────────────────────────────────────────────────────────────────────
  // HOOK
  // ─────────────────────────────────────────────────────────────────────────────
  
  const {
    input,
    setInput,
    resonance,
    isProcessing,
    mayaKin,
    dailyGreeting,
    gratitudeMode,
    activateGratitude,
    audioEnabled,
    setAudioEnabled,
    RESONANCE_MATRIX: matrix
  } = useUniversalResonance('');
  
  // ─────────────────────────────────────────────────────────────────────────────
  // STATE LOCAL
  // ─────────────────────────────────────────────────────────────────────────────
  
  const [viewMode, setViewMode] = useState('arche'); // arche, maya, systems
  const [hoveredNawal, setHoveredNawal] = useState(null);
  const [showDebug, setShowDebug] = useState(true);
  
  const centerRef = useRef(null);
  const holdTimerRef = useRef(null);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // GRATITUDE MODE (Hold center 3 seconds)
  // ─────────────────────────────────────────────────────────────────────────────
  
  const handleCenterMouseDown = useCallback(() => {
    holdTimerRef.current = setTimeout(() => {
      activateGratitude();
    }, 3000);
  }, [activateGratitude]);
  
  const handleCenterMouseUp = useCallback(() => {
    if (holdTimerRef.current) {
      clearTimeout(holdTimerRef.current);
    }
  }, []);
  
  // ─────────────────────────────────────────────────────────────────────────────
  // INPUT STYLE DYNAMIQUE
  // ─────────────────────────────────────────────────────────────────────────────
  
  const inputStyle = {
    ...styles.input,
    borderColor: resonance?.color || 'rgba(255,255,255,0.2)',
    boxShadow: resonance?.glow ? `0 0 30px ${resonance.glow}` : 'none'
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER ARCHE (9 Cercles)
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderArche = () => {
    const activeLevel = resonance?.arithmos?.reduced || 4;
    
    return (
      <div style={styles.archeContainer}>
        {/* Cercle des 20 Nawals (extérieur) */}
        <div style={styles.nawalRing}>
          {NAWALS.map((nawal, index) => {
            const angle = (index * 18 - 90) * (Math.PI / 180);
            const radius = 185;
            const x = 200 + radius * Math.cos(angle) - 12;
            const y = 200 + radius * Math.sin(angle) - 12;
            
            const isToday = mayaKin?.nawal?.name === nawal.name;
            
            return (
              <div
                key={nawal.name}
                style={{
                  ...styles.nawalDot,
                  left: x,
                  top: y,
                  background: nawal.color,
                  opacity: isToday ? 1 : 0.4,
                  transform: isToday ? 'scale(1.3)' : 'scale(1)',
                  boxShadow: isToday ? `0 0 15px ${nawal.color}` : 'none'
                }}
                onMouseEnter={() => setHoveredNawal(nawal)}
                onMouseLeave={() => setHoveredNawal(null)}
                title={`${nawal.name} — ${nawal.meaning}`}
              >
                {index + 1}
              </div>
            );
          })}
        </div>
        
        {/* 9 Cercles de Résonance */}
        {matrix.map((level, index) => {
          const isActive = index + 1 === activeLevel;
          const angle = (index * 40 - 90) * (Math.PI / 180);
          const radius = isActive ? 100 : 120;
          const size = isActive ? 50 : 35;
          
          const x = 200 + radius * Math.cos(angle) - size / 2;
          const y = 200 + radius * Math.sin(angle) - size / 2;
          
          return (
            <div
              key={level.level}
              style={{
                ...styles.resonanceCircle,
                left: x,
                top: y,
                width: size,
                height: size,
                background: level.color,
                opacity: isActive ? 1 : 0.3,
                boxShadow: isActive ? `0 0 30px ${level.glow}` : 'none',
                transform: isActive ? 'scale(1.2)' : 'scale(1)',
                zIndex: isActive ? 10 : 1
              }}
              title={`${level.hz} Hz — ${level.label}`}
            >
              <span style={{ fontSize: isActive ? '1rem' : '0.8rem', fontWeight: 'bold' }}>
                {level.level}
              </span>
            </div>
          );
        })}
        
        {/* Centre (Heartbeat) */}
        <div
          ref={centerRef}
          style={{
            ...styles.centerHub,
            background: `radial-gradient(circle, ${resonance?.color || '#50C878'} 0%, transparent 70%)`,
            boxShadow: `0 0 50px ${resonance?.glow || 'rgba(80,200,120,0.5)'}`
          }}
          onMouseDown={handleCenterMouseDown}
          onMouseUp={handleCenterMouseUp}
          onMouseLeave={handleCenterMouseUp}
        >
          <div style={styles.frequencyDisplay}>
            {resonance?.frequency || 444}
          </div>
          <div style={styles.labelDisplay}>
            {resonance?.label || 'Hz'}
          </div>
        </div>
      </div>
    );
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER INFO PANELS
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderInfoPanels = () => {
    if (!resonance || resonance.isHeartbeat) return null;
    
    return (
      <div style={styles.infoPanel}>
        {/* Arithmos */}
        <div style={{ ...styles.infoCard, borderColor: resonance.color }}>
          <div style={styles.infoTitle}>🔢 Arithmos</div>
          <div style={styles.infoValue}>
            {resonance.arithmos.reduced} — {resonance.label}
          </div>
          <div style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: '5px' }}>
            {resonance.arithmos.total} → {resonance.arithmos.steps.join(' → ')}
          </div>
        </div>
        
        {/* Maya */}
        {mayaKin && (
          <div style={{ ...styles.infoCard, borderColor: mayaKin.nawal.color }}>
            <div style={styles.infoTitle}>🌀 Maya (Tzolkin)</div>
            <div style={styles.infoValue}>
              {mayaKin.signature}
            </div>
            <div style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: '5px' }}>
              {mayaKin.nawal.meaning}: {mayaKin.nawal.essence}
            </div>
          </div>
        )}
        
        {/* Chakra */}
        {resonance.chakra && (
          <div style={{ ...styles.infoCard, borderColor: resonance.chakra.color }}>
            <div style={styles.infoTitle}>🧘 Chakra</div>
            <div style={styles.infoValue}>
              {resonance.chakra.name}
            </div>
            <div style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: '5px' }}>
              {resonance.chakra.meaning} — {resonance.mantra}
            </div>
          </div>
        )}
        
        {/* Kabbale */}
        {resonance.sephirah && (
          <div style={{ ...styles.infoCard, borderColor: resonance.sephirah.color }}>
            <div style={styles.infoTitle}>🌳 Kabbale</div>
            <div style={styles.infoValue}>
              {resonance.sephirah.name}
            </div>
            <div style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: '5px' }}>
              {resonance.sephirah.meaning}
            </div>
          </div>
        )}
        
        {/* Geometry */}
        <div style={styles.infoCard}>
          <div style={styles.infoTitle}>🔮 Géométrie</div>
          <div style={styles.infoValue}>
            {resonance.isOrganic ? '🌱 Organique' : '⬡ Structuré'}
          </div>
          <div style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: '5px' }}>
            Vitalité φ: {(resonance.vitalityRate * 100).toFixed(0)}%
            {resonance.isFibonacci && ' | Fibonacci ✓'}
          </div>
        </div>
      </div>
    );
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER CHAKRA BAR
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderChakraBar = () => {
    const activeChakra = resonance?.chakra?.number || 4;
    
    return (
      <div style={styles.chakraBar}>
        {CHAKRAS.slice().reverse().map(chakra => {
          const isActive = chakra.number === activeChakra;
          return (
            <div
              key={chakra.number}
              style={{
                ...styles.chakraDot,
                background: chakra.color,
                opacity: isActive ? 1 : 0.3,
                transform: isActive ? 'scaleX(1.1)' : 'scaleX(1)'
              }}
              title={`${chakra.name} — ${chakra.meaning} (${chakra.mantra})`}
            >
              {isActive && chakra.mantra}
            </div>
          );
        })}
      </div>
    );
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER MAYA PANEL
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderMayaPanel = () => {
    if (!mayaKin) return null;
    
    return (
      <div style={styles.mayaPanel}>
        <div style={{ fontSize: '1.5rem', marginBottom: '10px' }}>
          🌀 {mayaKin.signature}
        </div>
        <div style={{ 
          fontSize: '2rem', 
          color: mayaKin.nawal.color,
          textShadow: `0 0 20px ${mayaKin.nawal.color}`
        }}>
          {mayaKin.nawal.meaning}
        </div>
        <div style={{ fontSize: '0.9rem', opacity: 0.8, marginTop: '10px' }}>
          {mayaKin.nawal.essence}
        </div>
        <div style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: '15px' }}>
          Ton {mayaKin.ton.number} ({mayaKin.ton.name}): {mayaKin.ton.action}
        </div>
        {mayaKin.isSacred && (
          <div style={{ 
            marginTop: '15px', 
            padding: '8px', 
            background: 'rgba(255,215,0,0.2)', 
            borderRadius: '8px' 
          }}>
            ✦ JOUR SACRÉ ✦
          </div>
        )}
      </div>
    );
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER DEBUG CONSOLE
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderDebugConsole = () => {
    if (!showDebug) return null;
    
    return (
      <div style={styles.debugConsole}>
        <div style={styles.debugTitle}>
          AT·OM Debug Console
          <span 
            style={{ float: 'right', cursor: 'pointer' }}
            onClick={() => setShowDebug(false)}
          >
            ✕
          </span>
        </div>
        <div>Vibration: <span style={{ color: resonance?.color || '#50C878' }}>
          {resonance?.frequency || 444} Hz
        </span></div>
        <div>Arithmos: <span style={{ color: '#FFD700' }}>
          {resonance?.arithmos?.reduced || 4}
        </span></div>
        <div>Maya: <span style={{ color: mayaKin?.nawal?.color || '#FFF' }}>
          {mayaKin?.signature || 'Loading...'}
        </span></div>
        <div>Chakra: <span style={{ color: resonance?.chakra?.color || '#50C878' }}>
          {resonance?.chakra?.name || 'Anahata'}
        </span></div>
        <div style={{ marginTop: '10px', fontSize: '0.75rem', opacity: 0.5 }}>
          φ = {PHI.toFixed(6)}
        </div>
        <div style={{ fontSize: '0.75rem', opacity: 0.5 }}>
          Heartbeat: 444 Hz | A=444Hz
        </div>
      </div>
    );
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER GRATITUDE OVERLAY
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderGratitudeOverlay = () => (
    <div style={{
      ...styles.gratitudeOverlay,
      opacity: gratitudeMode ? 0.95 : 0,
      pointerEvents: gratitudeMode ? 'all' : 'none'
    }}>
      <div style={styles.gratitudeText}>
        <div style={{ fontSize: '3rem', marginBottom: '20px' }}>🙏</div>
        <div style={{ fontSize: '1.5rem', marginBottom: '20px', color: '#FFD700' }}>
          GRATITUDE
        </div>
        <div style={{ fontSize: '1rem', lineHeight: 1.8, opacity: 0.8 }}>
          Ce système a été conçu avec amour et intention<br />
          par l'Architecte Jonathan Rodrigue.<br /><br />
          Que ces fréquences servent le plus grand bien<br />
          et l'éveil de la conscience collective.<br /><br />
          <span style={{ color: '#50C878' }}>444 Hz — Le Cœur qui bat pour tous</span>
        </div>
        <div style={{ marginTop: '30px', fontSize: '0.9rem', opacity: 0.5 }}>
          Oracle 17 — Le Gardien de la Synthèse
        </div>
      </div>
    </div>
  );
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER ARCHITECT SEAL
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderArchitectSeal = () => {
    if (!resonance?.isArchitectSeal) return null;
    
    return (
      <div style={{
        background: 'linear-gradient(135deg, rgba(255,215,0,0.2) 0%, rgba(255,253,208,0.1) 100%)',
        border: '2px solid #FFD700',
        borderRadius: '20px',
        padding: '30px',
        textAlign: 'center',
        maxWidth: '500px',
        margin: '20px auto',
        boxShadow: '0 0 50px rgba(255,215,0,0.3)'
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '15px' }}>👑</div>
        <div style={{ 
          fontSize: '1.8rem', 
          color: '#FFD700',
          textShadow: '0 0 20px rgba(255,215,0,0.5)',
          marginBottom: '10px'
        }}>
          SCEAU DE L'ARCHITECTE
        </div>
        <div style={{ fontSize: '1.2rem', marginBottom: '15px' }}>
          Jonathan Rodrigue
        </div>
        <div style={{ 
          fontSize: '1rem', 
          opacity: 0.8,
          padding: '10px',
          background: 'rgba(0,0,0,0.3)',
          borderRadius: '10px'
        }}>
          2 + 7 = 9<br />
          <span style={{ fontSize: '0.85rem', opacity: 0.7 }}>
            La Dualité rencontre l'Introspection pour former l'Unité
          </span>
        </div>
        <div style={{ 
          marginTop: '20px', 
          fontSize: '2rem',
          color: '#FFFDD0',
          textShadow: '0 0 30px rgba(255,253,208,0.8)'
        }}>
          999 Hz
        </div>
      </div>
    );
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER HOVERED NAWAL INFO
  // ─────────────────────────────────────────────────────────────────────────────
  
  const renderHoveredNawal = () => {
    if (!hoveredNawal) return null;
    
    return (
      <div style={{
        position: 'fixed',
        top: '20px',
        left: '20px',
        background: 'rgba(0,0,0,0.9)',
        border: `2px solid ${hoveredNawal.color}`,
        borderRadius: '15px',
        padding: '15px',
        zIndex: 1000,
        minWidth: '200px'
      }}>
        <div style={{ color: hoveredNawal.color, fontSize: '1.2rem', marginBottom: '5px' }}>
          {hoveredNawal.name}
        </div>
        <div style={{ fontSize: '1rem', marginBottom: '5px' }}>
          {hoveredNawal.meaning}
        </div>
        <div style={{ fontSize: '0.85rem', opacity: 0.7 }}>
          {hoveredNawal.essence}
        </div>
        <div style={{ fontSize: '0.8rem', opacity: 0.5, marginTop: '10px' }}>
          Élément: {hoveredNawal.element} | Oracle: {hoveredNawal.oracle}
        </div>
      </div>
    );
  };
  
  // ─────────────────────────────────────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────────────────────────────────────
  
  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.title}>AT·OM</h1>
        <p style={styles.subtitle}>UNIVERSAL RESONANCE SYSTEM v2.0</p>
      </header>
      
      {/* Mode Selector */}
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px', gap: '10px' }}>
        {['arche', 'maya', 'systems'].map(mode => (
          <button
            key={mode}
            style={{
              ...styles.modeButton,
              background: viewMode === mode ? 'rgba(255,255,255,0.2)' : 'transparent'
            }}
            onClick={() => setViewMode(mode)}
          >
            {mode === 'arche' ? '🌀 Arche' : mode === 'maya' ? '📅 Maya' : '⚛️ Systèmes'}
          </button>
        ))}
        <button
          style={{
            ...styles.modeButton,
            background: audioEnabled ? 'rgba(80,200,120,0.3)' : 'transparent'
          }}
          onClick={() => setAudioEnabled(!audioEnabled)}
        >
          {audioEnabled ? '🔊' : '🔇'}
        </button>
      </div>
      
      {/* Main Content */}
      <main style={styles.mainContent}>
        {/* Input */}
        <div style={styles.inputContainer}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Entrez un mot..."
            style={inputStyle}
          />
        </div>
        
        {/* Architect Seal */}
        {renderArchitectSeal()}
        
        {/* Content based on mode */}
        <div style={{ display: 'flex', gap: '30px', alignItems: 'flex-start', flexWrap: 'wrap', justifyContent: 'center' }}>
          {/* Arche */}
          {(viewMode === 'arche' || viewMode === 'systems') && renderArche()}
          
          {/* Chakra Bar */}
          {(viewMode === 'arche' || viewMode === 'systems') && (
            <div style={{ marginTop: '50px' }}>
              {renderChakraBar()}
            </div>
          )}
          
          {/* Maya Panel */}
          {(viewMode === 'maya' || viewMode === 'systems') && renderMayaPanel()}
        </div>
        
        {/* Info Panels */}
        {viewMode === 'systems' && renderInfoPanels()}
      </main>
      
      {/* Overlays */}
      {renderHoveredNawal()}
      {renderGratitudeOverlay()}
      {renderDebugConsole()}
      
      {/* Footer */}
      <footer style={{ 
        textAlign: 'center', 
        marginTop: '40px', 
        opacity: 0.5, 
        fontSize: '0.8rem' 
      }}>
        Heartbeat: 444 Hz | Tuning: A=444Hz | Oracle 17<br />
        Maintenir le centre 3 secondes pour le Mode Gratitude
      </footer>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS ADDITIONNELS
// ═══════════════════════════════════════════════════════════════════════════════

export { useUniversalResonance };
