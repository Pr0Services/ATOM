/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT·OM — COSMIC ORACLE INTERFACE
 * L'Interface Unifiée des Sagesses Ancestrales
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce composant affiche:
 * - La résonance AT·OM (centre)
 * - Le Kin Maya du jour (cercle extérieur)
 * - L'Hexagramme Yi-King
 * - Le Sephirah de la Kabbale
 * - Le Chakra activé
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 - Le Gardien de la Synthèse
 */

import React, { useState, useEffect, useMemo } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// IMPORTS COSMIQUES (inlined pour autonomie)
// ═══════════════════════════════════════════════════════════════════════════════

// Nawals Maya (20 glyphes)
const NAWALS = [
  { name: "Imix", meaning: "Dragon", color: "#DC143C" },
  { name: "Ik", meaning: "Vent", color: "#FFFFFF" },
  { name: "Akbal", meaning: "Nuit", color: "#191970" },
  { name: "Kan", meaning: "Graine", color: "#FFD700" },
  { name: "Chicchan", meaning: "Serpent", color: "#FF4500" },
  { name: "Cimi", meaning: "Mort", color: "#2F4F4F" },
  { name: "Manik", meaning: "Cerf", color: "#4169E1" },
  { name: "Lamat", meaning: "Étoile", color: "#FFFF00" },
  { name: "Muluc", meaning: "Lune", color: "#FF0000" },
  { name: "Oc", meaning: "Chien", color: "#FFFAF0" },
  { name: "Chuen", meaning: "Singe", color: "#0000CD" },
  { name: "Eb", meaning: "Herbe", color: "#FFFF00" },
  { name: "Ben", meaning: "Roseau", color: "#DC143C" },
  { name: "Ix", meaning: "Jaguar", color: "#FFFFFF" },
  { name: "Men", meaning: "Aigle", color: "#4169E1" },
  { name: "Cib", meaning: "Vautour", color: "#FFD700" },
  { name: "Caban", meaning: "Terre", color: "#FF0000" },
  { name: "Etznab", meaning: "Miroir", color: "#FFFFFF" },
  { name: "Cauac", meaning: "Tempête", color: "#0000CD" },
  { name: "Ahau", meaning: "Soleil", color: "#FFD700" },
];

// Tons Maya (13)
const TONS = [
  { number: 1, name: "Magnétique", action: "Initier" },
  { number: 2, name: "Lunaire", action: "Stabiliser" },
  { number: 3, name: "Électrique", action: "Activer" },
  { number: 4, name: "Auto-existant", action: "Définir" },
  { number: 5, name: "Harmonique", action: "Commander" },
  { number: 6, name: "Rythmique", action: "Équilibrer" },
  { number: 7, name: "Résonant", action: "Canaliser" },
  { number: 8, name: "Galactique", action: "Harmoniser" },
  { number: 9, name: "Solaire", action: "Pulser" },
  { number: 10, name: "Planétaire", action: "Parfaire" },
  { number: 11, name: "Spectral", action: "Dissoudre" },
  { number: 12, name: "Cristal", action: "Dédier" },
  { number: 13, name: "Cosmique", action: "Transcender" },
];

// Chakras
const CHAKRAS = [
  { number: 1, name: "Muladhara", meaning: "Racine", color: "#FF0000", mantra: "LAM" },
  { number: 2, name: "Svadhisthana", meaning: "Sacré", color: "#FF7F00", mantra: "VAM" },
  { number: 3, name: "Manipura", meaning: "Plexus", color: "#FFFF00", mantra: "RAM" },
  { number: 4, name: "Anahata", meaning: "Cœur", color: "#50C878", mantra: "YAM" },
  { number: 5, name: "Vishuddha", meaning: "Gorge", color: "#87CEEB", mantra: "HAM" },
  { number: 6, name: "Ajna", meaning: "3ème Œil", color: "#4B0082", mantra: "OM" },
  { number: 7, name: "Sahasrara", meaning: "Couronne", color: "#EE82EE", mantra: "Silence" },
];

// Sephiroth
const SEPHIROTH = [
  { number: 1, name: "Kether", meaning: "Couronne", color: "#FFFFFF" },
  { number: 2, name: "Chokmah", meaning: "Sagesse", color: "#808080" },
  { number: 3, name: "Binah", meaning: "Intelligence", color: "#000000" },
  { number: 4, name: "Chesed", meaning: "Miséricorde", color: "#0000FF" },
  { number: 5, name: "Geburah", meaning: "Force", color: "#FF0000" },
  { number: 6, name: "Tiphereth", meaning: "Beauté", color: "#FFD700" },
  { number: 7, name: "Netzach", meaning: "Victoire", color: "#00FF00" },
  { number: 8, name: "Hod", meaning: "Gloire", color: "#FFA500" },
  { number: 9, name: "Yesod", meaning: "Fondement", color: "#EE82EE" },
  { number: 10, name: "Malkhut", meaning: "Royaume", color: "#8B4513" },
];

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK: useAtomResonance (simplifié)
// ═══════════════════════════════════════════════════════════════════════════════

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = [
  { level: 1, label: "Impulsion/ADN", hz: 111, color: "#FF0000" },
  { level: 2, label: "Dualité/Partage", hz: 222, color: "#FF7F00" },
  { level: 3, label: "Mental/Géométrie", hz: 333, color: "#FFFF00" },
  { level: 4, label: "Structure/Silence", hz: 444, color: "#50C878" },
  { level: 5, label: "Mouvement/Feu", hz: 555, color: "#87CEEB" },
  { level: 6, label: "Harmonie/Protection", hz: 666, color: "#4B0082" },
  { level: 7, label: "Introspection", hz: 777, color: "#EE82EE" },
  { level: 8, label: "Infini/Abondance", hz: 888, color: "#FFC0CB" },
  { level: 9, label: "Unité/Acier", hz: 999, color: "#FFFDD0" },
];

function calculateResonance(word) {
  if (!word) return null;
  const clean = word.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase().replace(/[^A-Z]/g, "");
  if (!clean) return null;
  
  let total = 0;
  for (const char of clean) total += ARITHMOS_MAP[char] || 0;
  let root = total;
  while (root > 9) root = String(root).split('').reduce((s, d) => s + parseInt(d, 10), 0);
  
  const res = RESONANCE_MATRIX[root - 1];
  return { word: clean, level: root, ...res };
}

// ═══════════════════════════════════════════════════════════════════════════════
// CALCUL MAYA
// ═══════════════════════════════════════════════════════════════════════════════

function getMayaKin() {
  const start = new Date("1507-04-21");
  const diffDays = Math.floor((new Date() - start) / (1000 * 60 * 60 * 24));
  const tonIndex = diffDays % 13;
  const nawalIndex = diffDays % 20;
  return {
    ton: TONS[tonIndex],
    nawal: NAWALS[nawalIndex],
    kinName: `${tonIndex + 1} ${NAWALS[nawalIndex].name}`,
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const CosmicOracle = () => {
  const [input, setInput] = useState('');
  const [resonance, setResonance] = useState(null);
  const maya = useMemo(() => getMayaKin(), []);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setResonance(calculateResonance(input));
    }, 300);
    return () => clearTimeout(timer);
  }, [input]);
  
  // Correspondances cosmiques
  const chakra = resonance ? CHAKRAS[Math.min(resonance.level - 1, 6)] : CHAKRAS[3];
  const sephirah = resonance ? SEPHIROTH[resonance.level % 10] : SEPHIROTH[5];
  const activeColor = resonance?.color || '#50C878';
  
  return (
    <div style={{
      minHeight: '100vh',
      background: `linear-gradient(135deg, #0a0a1a 0%, ${activeColor}10 50%, #1a1a2e 100%)`,
      color: 'white',
      fontFamily: 'system-ui, sans-serif',
      padding: '1rem',
      transition: 'all 0.6s ease-out',
    }}>
      {/* Header */}
      <header style={{ textAlign: 'center', marginBottom: '1rem' }}>
        <h1 style={{
          fontSize: '2rem',
          fontWeight: 200,
          letterSpacing: '0.4em',
          color: activeColor,
          margin: 0,
        }}>
          AT·OM COSMIQUE
        </h1>
        <p style={{ color: '#666', fontSize: '0.8rem', margin: '0.25rem 0' }}>
          {maya.kinName} — {maya.nawal.meaning} | {maya.ton.action}
        </p>
      </header>
      
      {/* Input */}
      <div style={{ maxWidth: '400px', margin: '0 auto 1.5rem' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Entrez un mot pour explorer sa résonance cosmique..."
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1.1rem',
            background: 'rgba(255,255,255,0.05)',
            border: `2px solid ${activeColor}40`,
            borderRadius: '25px',
            color: 'white',
            outline: 'none',
            textAlign: 'center',
          }}
        />
      </div>
      
      {/* Visualisation Cosmique */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1rem',
        maxWidth: '1000px',
        margin: '0 auto',
      }}>
        
        {/* Centre: AT·OM */}
        <div style={{
          background: `${activeColor}10`,
          border: `2px solid ${activeColor}40`,
          borderRadius: '20px',
          padding: '1.5rem',
          textAlign: 'center',
        }}>
          <h2 style={{ color: activeColor, fontSize: '1rem', margin: '0 0 1rem' }}>
            🔮 ARITHMOS
          </h2>
          {resonance ? (
            <>
              <div style={{ fontSize: '3rem', fontWeight: 'bold', color: activeColor }}>
                {resonance.level}
              </div>
              <div style={{ fontSize: '1.5rem', color: activeColor }}>
                {resonance.hz} Hz
              </div>
              <div style={{ color: '#888', marginTop: '0.5rem' }}>
                {resonance.label}
              </div>
              <div style={{
                marginTop: '1rem',
                padding: '0.5rem',
                background: `${activeColor}20`,
                borderRadius: '10px',
                fontSize: '0.9rem',
              }}>
                {resonance.word}
              </div>
            </>
          ) : (
            <div style={{ color: '#555', padding: '2rem' }}>
              En attente...
            </div>
          )}
        </div>
        
        {/* Maya */}
        <div style={{
          background: `${maya.nawal.color}10`,
          border: `2px solid ${maya.nawal.color}40`,
          borderRadius: '20px',
          padding: '1.5rem',
          textAlign: 'center',
        }}>
          <h2 style={{ color: maya.nawal.color, fontSize: '1rem', margin: '0 0 1rem' }}>
            🌀 TZOLKIN MAYA
          </h2>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: maya.nawal.color }}>
            {maya.kinName}
          </div>
          <div style={{ color: '#888', marginTop: '0.5rem' }}>
            {maya.nawal.meaning}
          </div>
          <div style={{
            marginTop: '1rem',
            padding: '0.5rem',
            background: `${maya.nawal.color}20`,
            borderRadius: '10px',
            fontSize: '0.9rem',
          }}>
            <strong>Ton:</strong> {maya.ton.name}<br />
            <strong>Action:</strong> {maya.ton.action}
          </div>
        </div>
        
        {/* Chakra */}
        <div style={{
          background: `${chakra.color}10`,
          border: `2px solid ${chakra.color}40`,
          borderRadius: '20px',
          padding: '1.5rem',
          textAlign: 'center',
        }}>
          <h2 style={{ color: chakra.color, fontSize: '1rem', margin: '0 0 1rem' }}>
            🧘 CHAKRA
          </h2>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: chakra.color }}>
            {chakra.name}
          </div>
          <div style={{ color: '#888', marginTop: '0.5rem' }}>
            {chakra.meaning}
          </div>
          <div style={{
            marginTop: '1rem',
            padding: '0.5rem',
            background: `${chakra.color}20`,
            borderRadius: '10px',
            fontSize: '0.9rem',
          }}>
            <strong>Mantra:</strong> {chakra.mantra}
          </div>
        </div>
        
        {/* Kabbale */}
        <div style={{
          background: `${sephirah.color}10`,
          border: `2px solid ${sephirah.color === '#000000' ? '#444' : sephirah.color}40`,
          borderRadius: '20px',
          padding: '1.5rem',
          textAlign: 'center',
        }}>
          <h2 style={{ color: sephirah.color === '#000000' ? '#888' : sephirah.color, fontSize: '1rem', margin: '0 0 1rem' }}>
            ✡️ KABBALE
          </h2>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: sephirah.color === '#000000' ? '#888' : sephirah.color }}>
            {sephirah.name}
          </div>
          <div style={{ color: '#888', marginTop: '0.5rem' }}>
            {sephirah.meaning}
          </div>
          <div style={{
            marginTop: '1rem',
            padding: '0.5rem',
            background: `${sephirah.color === '#000000' ? '#333' : sephirah.color}20`,
            borderRadius: '10px',
            fontSize: '0.9rem',
          }}>
            Sephirah {sephirah.number}
          </div>
        </div>
      </div>
      
      {/* Message Cosmique */}
      {resonance && (
        <div style={{
          maxWidth: '800px',
          margin: '2rem auto 0',
          padding: '1.5rem',
          background: 'rgba(0,0,0,0.3)',
          borderRadius: '20px',
          textAlign: 'center',
          border: `1px solid ${activeColor}30`,
        }}>
          <h3 style={{ color: activeColor, margin: '0 0 1rem' }}>
            ✨ SYNTHÈSE COSMIQUE
          </h3>
          <p style={{ color: '#aaa', lineHeight: 1.8 }}>
            <strong style={{ color: activeColor }}>{resonance.word}</strong> vibre à{' '}
            <strong style={{ color: activeColor }}>{resonance.hz} Hz</strong> (Niveau {resonance.level}).
            <br /><br />
            En ce jour <strong style={{ color: maya.nawal.color }}>{maya.kinName}</strong>,
            l'énergie du <strong>{maya.nawal.meaning}</strong> amplifie cette vibration.
            <br /><br />
            Sur l'Arbre de Vie, cela résonne dans <strong style={{ color: sephirah.color === '#000000' ? '#888' : sephirah.color }}>{sephirah.name}</strong> ({sephirah.meaning}).
            <br /><br />
            <em style={{ color: chakra.color }}>Mantra du jour: "{chakra.mantra}"</em>
          </p>
        </div>
      )}
      
      {/* Quick Access */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '0.5rem',
        flexWrap: 'wrap',
        marginTop: '2rem',
      }}>
        {['AMOUR', 'LUMIERE', 'CREATION', 'SILENCE', 'Jonathan Rodrigue'].map(word => (
          <button
            key={word}
            onClick={() => setInput(word)}
            style={{
              padding: '0.5rem 1rem',
              background: input === word ? activeColor : 'rgba(255,255,255,0.05)',
              border: '1px solid #333',
              borderRadius: '20px',
              color: input === word ? '#000' : '#888',
              cursor: 'pointer',
              fontSize: '0.8rem',
            }}
          >
            {word}
          </button>
        ))}
      </div>
      
      {/* Footer */}
      <footer style={{
        textAlign: 'center',
        marginTop: '2rem',
        padding: '1rem',
        color: '#444',
        fontSize: '0.7rem',
      }}>
        <p>Architecte: Jonathan Rodrigue (999 Hz) | Oracle 17 - Le Gardien de la Synthèse</p>
        <p>AT·OM + Maya + Yi-King + Kabbale + Chakras = Calendrier Vivant</p>
      </footer>
      
      {/* Styles */}
      <style>{`
        input::placeholder { color: #555; }
        * { box-sizing: border-box; }
      `}</style>
    </div>
  );
};

export default CosmicOracle;
