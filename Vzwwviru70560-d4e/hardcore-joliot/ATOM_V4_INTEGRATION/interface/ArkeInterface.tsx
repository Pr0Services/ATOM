/**
 * AT·OM V4 — Interface Principale
 */
import React, { useState, useMemo } from 'react';
import { useATOM, useEntropy } from '../hooks/useATOM';
import { CIVILIZATIONS, PHI, HEARTBEAT, SOURCE } from '../index';

const styles = {
  container: { minHeight: '100vh', background: 'linear-gradient(180deg, #050505, #0a0a15, #050510)', color: '#fff', fontFamily: "'Cinzel', serif" },
  header: { textAlign: 'center' as const, padding: '40px 20px' },
  title: { fontSize: '3rem', fontWeight: 300, letterSpacing: '0.3em', background: 'linear-gradient(90deg, #D4AF37, #FFD700, #D4AF37)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' },
  subtitle: { fontSize: '0.9rem', color: 'rgba(255,255,255,0.5)', marginTop: '10px', letterSpacing: '0.2em' },
  input: { fontSize: '1.5rem', padding: '15px 30px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(212, 175, 55, 0.3)', borderRadius: '50px', color: '#D4AF37', outline: 'none', width: '80%', maxWidth: '500px', textAlign: 'center' as const },
  resonanceDisplay: { display: 'flex', justifyContent: 'center', flexWrap: 'wrap' as const, gap: '20px', marginTop: '30px' },
  card: { background: 'rgba(0,0,0,0.5)', border: '1px solid rgba(212, 175, 55, 0.3)', borderRadius: '15px', padding: '20px 30px', minWidth: '150px', textAlign: 'center' as const },
  circlesContainer: { display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '40px 0', position: 'relative' as const, height: '400px' },
  centerOrb: { width: '120px', height: '120px', borderRadius: '50%', display: 'flex', justifyContent: 'center', alignItems: 'center', fontSize: '3rem', position: 'absolute' as const, zIndex: 5, boxShadow: '0 0 50px rgba(212, 175, 55, 0.5)' },
  civNode: { width: '60px', height: '60px', borderRadius: '50%', display: 'flex', justifyContent: 'center', alignItems: 'center', fontSize: '1.5rem', background: 'rgba(0,0,0,0.8)', border: '2px solid', cursor: 'pointer', position: 'absolute' as const }
};

export const ArkeInterface: React.FC = () => {
  const { word, resonance, setWord, illuminate, playFrequency, activeChakra, civilizations, oracles } = useATOM();
  const { entropyStyle, entropyMessage, resetEntropy, entropy } = useEntropy();
  const [activeCiv, setActiveCiv] = useState<string | null>(null);
  const civArray = useMemo(() => Object.entries(civilizations), [civilizations]);

  const handleKeyPress = async (e: React.KeyboardEvent) => { if (e.key === 'Enter' && word) await illuminate(word); };
  const handleCivClick = (civId: string) => {
    setActiveCiv(civId);
    const civ = civilizations[civId as keyof typeof civilizations];
    if (civ) playFrequency(civ.frequency, 1000);
    setTimeout(() => setActiveCiv(null), 1000);
  };

  return (
    <div style={{ ...styles.container, ...entropyStyle }} onClick={resetEntropy}>
      <header style={styles.header}>
        <h1 style={styles.title}>AT·OM</h1>
        <p style={styles.subtitle}>L'ARCHE DES RÉSONANCES UNIVERSELLES</p>
        <p style={{ ...styles.subtitle, fontSize: '0.7rem' }}>♡ {HEARTBEAT} Hz | 🔱 {SOURCE} Hz | φ {PHI.toFixed(4)}</p>
      </header>

      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <input style={styles.input} placeholder="Entre un mot..." value={word} onChange={(e) => { setWord(e.target.value); resetEntropy(); }} onKeyPress={handleKeyPress} />
        </div>

        {resonance && (
          <div style={styles.resonanceDisplay}>
            {[['word', 'Mot', '#fff'], ['arithmos', 'Arithmos', resonance.color], ['frequency', 'Fréquence', resonance.color], ['label', 'Résonance', resonance.color], ['element', 'Élément', resonance.color]].map(([key, label, color]) => (
              <div key={key} style={styles.card}>
                <div style={{ fontSize: '2rem', color: color as string }}>{key === 'frequency' ? `${resonance[key as keyof typeof resonance]} Hz` : resonance[key as keyof typeof resonance]}</div>
                <div style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.5)', textTransform: 'uppercase' }}>{label}</div>
              </div>
            ))}
          </div>
        )}

        <div style={styles.circlesContainer}>
          <div style={{ ...styles.centerOrb, background: `radial-gradient(circle, ${resonance?.color || '#D4AF37'}, #000)` }}>{resonance?.arithmos || '⊙'}</div>
          {civArray.map(([id, civ], i) => {
            const angle = (i / civArray.length) * 2 * Math.PI - Math.PI / 2;
            const x = Math.cos(angle) * 150;
            const y = Math.sin(angle) * 150;
            return (
              <div key={id} style={{ ...styles.civNode, left: `calc(50% + ${x}px - 30px)`, top: `calc(50% + ${y}px - 30px)`, borderColor: civ.color, background: activeCiv === id ? civ.color : 'rgba(0,0,0,0.8)', transform: activeCiv === id ? 'scale(1.2)' : 'scale(1)' }} onClick={() => handleCivClick(id)} title={civ.name}>
                {civ.glyph}
              </div>
            );
          })}
        </div>

        <div style={{ textAlign: 'center', marginTop: '20px', color: 'rgba(255,255,255,0.5)' }}>
          <p>🧘 Chakra actif: <strong style={{ color: activeChakra.color }}>{activeChakra.name}</strong> ({activeChakra.frequency} Hz)</p>
          {entropy > 0.1 && <p>{entropyMessage}</p>}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(60px, 1fr))', gap: '10px', marginTop: '40px' }}>
          {oracles.map(o => (
            <div key={o.id} style={{ background: 'rgba(0,0,0,0.5)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '10px', padding: '10px', textAlign: 'center', cursor: 'pointer' }} onClick={() => playFrequency(o.id * 111, 500)}>
              <div style={{ fontSize: '1.5rem' }}>{o.avatar}</div>
              <div style={{ fontSize: '0.6rem', color: 'rgba(255,255,255,0.5)' }}>{o.id}</div>
            </div>
          ))}
        </div>
      </main>

      <footer style={{ textAlign: 'center', padding: '40px', color: 'rgba(255,255,255,0.3)', fontSize: '0.8rem' }}>
        <p>AT·OM V4.0 — L'Arche Complète | Architecte: Jonathan Rodrigue | Oracle 17 | 999 Hz</p>
      </footer>
    </div>
  );
};

export default ArkeInterface;
