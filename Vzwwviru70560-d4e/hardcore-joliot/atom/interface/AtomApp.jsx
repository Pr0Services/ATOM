/**
 * AT·OM — AtomApp.jsx
 * EXEMPLE D'INTÉGRATION
 * 
 * Ce composant montre comment connecter useAtomResonance à l'Arche des Résonances.
 * 
 * @version 1.0.0
 */

import React, { useState, useEffect } from 'react';
import useAtomResonance, { 
  useResonanceTransition, 
  runAllTests,
  RESONANCE_MATRIX 
} from './useAtomResonance';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const AtomApp = () => {
  const [inputValue, setInputValue] = useState('');
  const [showTests, setShowTests] = useState(false);
  
  // Hook de résonance avec debounce automatique
  const resonance = useAtomResonance(inputValue, {
    debounceMs: 300,
    enableLogging: true, // Logs stylisés dans la console
  });
  
  // Hook de transition pour les styles CSS fluides
  const transitionStyles = useResonanceTransition(resonance);
  
  // Lancer les tests au montage (optionnel)
  useEffect(() => {
    if (showTests) {
      runAllTests();
    }
  }, [showTests]);
  
  return (
    <div 
      className="atom-app"
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%)',
        color: 'white',
        padding: '2rem',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      {/* En-tête */}
      <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '3rem', 
          fontWeight: 200,
          letterSpacing: '0.5em',
          color: resonance?.color || '#50C878',
          transition: 'color 600ms ease-out',
        }}>
          AT·OM
        </h1>
        <p style={{ color: '#888', fontSize: '0.9rem' }}>
          Système de Résonance Vibratoire | 444 Hz
        </p>
      </header>
      
      {/* Champ de saisie */}
      <div style={{ 
        maxWidth: '600px', 
        margin: '0 auto 2rem',
        position: 'relative',
      }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Entrez un mot..."
          style={{
            width: '100%',
            padding: '1rem 1.5rem',
            fontSize: '1.5rem',
            background: 'rgba(255,255,255,0.05)',
            border: `2px solid ${resonance?.color || '#333'}`,
            borderRadius: '12px',
            color: 'white',
            outline: 'none',
            transition: 'all 600ms ease-out',
            boxShadow: resonance ? `0 0 30px ${resonance.color}30` : 'none',
          }}
        />
        
        {/* Indicateur de frappe */}
        {resonance?.isTransitioning && (
          <div style={{
            position: 'absolute',
            right: '1rem',
            top: '50%',
            transform: 'translateY(-50%)',
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: resonance.color,
            animation: 'pulse 600ms ease-out',
          }} />
        )}
      </div>
      
      {/* Feedback de Résonance */}
      {resonance && (
        <div 
          style={{
            maxWidth: '600px',
            margin: '0 auto 2rem',
            padding: '1.5rem',
            background: `${resonance.color}10`,
            border: `1px solid ${resonance.color}30`,
            borderRadius: '12px',
            ...transitionStyles,
          }}
        >
          {/* Mot nettoyé */}
          <div style={{ 
            fontSize: '2rem', 
            fontWeight: 600, 
            color: resonance.color,
            marginBottom: '1rem',
            textAlign: 'center',
          }}>
            {resonance.word}
          </div>
          
          {/* Grille d'informations */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '1rem',
            textAlign: 'center',
          }}>
            <div>
              <div style={{ color: '#888', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                Niveau
              </div>
              <div style={{ 
                fontSize: '2rem', 
                fontWeight: 700, 
                color: resonance.color 
              }}>
                {resonance.level}
              </div>
            </div>
            <div>
              <div style={{ color: '#888', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                Résonance
              </div>
              <div style={{ 
                fontSize: '2rem', 
                fontWeight: 700, 
                color: resonance.color 
              }}>
                {resonance.hz} Hz
              </div>
            </div>
            <div>
              <div style={{ color: '#888', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                Delay
              </div>
              <div style={{ 
                fontSize: '2rem', 
                fontWeight: 700, 
                color: resonance.color 
              }}>
                {resonance.delay}ms
              </div>
            </div>
          </div>
          
          {/* Label */}
          <div style={{ 
            marginTop: '1rem', 
            textAlign: 'center',
            padding: '0.5rem',
            background: `${resonance.color}20`,
            borderRadius: '8px',
          }}>
            <span style={{ color: resonance.color }}>
              {resonance.type === 'foundation_stone' && '🧱 '}
              {resonance.type === 'transition_node' && '🌀 '}
              {resonance.type === 'standard' && '📝 '}
              {resonance.label}
            </span>
          </div>
        </div>
      )}
      
      {/* Visualisation de la Matrice */}
      <div style={{
        maxWidth: '800px',
        margin: '0 auto 2rem',
      }}>
        <h3 style={{ color: '#888', fontSize: '0.9rem', marginBottom: '1rem', textAlign: 'center' }}>
          MATRICE DE RÉSONANCE
        </h3>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '0.5rem',
          flexWrap: 'wrap',
        }}>
          {RESONANCE_MATRIX.map(item => (
            <div
              key={item.level}
              style={{
                width: '60px',
                padding: '0.75rem 0.5rem',
                background: resonance?.level === item.level ? item.color : `${item.color}20`,
                borderRadius: '8px',
                textAlign: 'center',
                transition: 'all 600ms ease-out',
                transform: resonance?.level === item.level ? 'scale(1.1)' : 'scale(1)',
                boxShadow: resonance?.level === item.level ? `0 0 20px ${item.color}` : 'none',
              }}
            >
              <div style={{ 
                fontSize: '1.25rem', 
                fontWeight: 700,
                color: resonance?.level === item.level ? '#000' : item.color,
              }}>
                {item.level}
              </div>
              <div style={{ 
                fontSize: '0.65rem',
                color: resonance?.level === item.level ? '#333' : '#888',
              }}>
                {item.hz}Hz
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Bouton de test */}
      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <button
          onClick={() => {
            setShowTests(true);
            runAllTests();
          }}
          style={{
            padding: '0.75rem 2rem',
            background: 'transparent',
            border: '1px solid #50C878',
            borderRadius: '8px',
            color: '#50C878',
            cursor: 'pointer',
            fontSize: '0.9rem',
            transition: 'all 200ms',
          }}
          onMouseOver={(e) => {
            e.target.style.background = '#50C878';
            e.target.style.color = '#000';
          }}
          onMouseOut={(e) => {
            e.target.style.background = 'transparent';
            e.target.style.color = '#50C878';
          }}
        >
          🧪 Lancer les Tests (voir console)
        </button>
      </div>
      
      {/* Footer */}
      <footer style={{ 
        textAlign: 'center', 
        marginTop: '4rem', 
        color: '#444',
        fontSize: '0.8rem',
      }}>
        <p>AT·OM Resonance System v1.0 | Architecte: Jonathan Rodrigue (999 Hz)</p>
        <p style={{ marginTop: '0.5rem' }}>
          Ouvrez la console (F12) pour voir les logs de résonance en temps réel
        </p>
      </footer>
      
      {/* Styles globaux */}
      <style>{`
        @keyframes pulse {
          0% { transform: translateY(-50%) scale(1); opacity: 1; }
          100% { transform: translateY(-50%) scale(2); opacity: 0; }
        }
        
        input::placeholder {
          color: #666;
        }
        
        * {
          box-sizing: border-box;
        }
      `}</style>
    </div>
  );
};

export default AtomApp;
