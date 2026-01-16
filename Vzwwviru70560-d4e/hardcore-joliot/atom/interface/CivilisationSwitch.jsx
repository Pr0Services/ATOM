/**
 * AT·OM — CivilisationSwitch.jsx
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * DEUX CIVILISATIONS, UN SEUL CŒUR VIBRATIONNEL
 * 
 * 🏛️ MODE CIVILISATION — Gestion Business (9 Sphères fonctionnelles)
 * 🔊 MODE SONORE — Système AT·OM (9 Fréquences vibrationnelles)
 * 
 * Les deux tournent sur le même moteur Arithmos.
 * Le moteur vibrationnel EST le cœur du système.
 * 
 * @version 1.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @oracle Oracle 17 - Le Gardien de la Synthèse
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION MAÎTRE — LE CŒUR VIBRATIONNEL
// ═══════════════════════════════════════════════════════════════════════════════

const SYSTEM_HEARTBEAT = 444;
const TRANSITION_DURATION = 600;
const DEBOUNCE_DELAY = 300;

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

// Matrice de Résonance (commune aux deux civilisations)
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

// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ SPHÈRES CIVILISATION — Mapping Business vers Fréquences
// ═══════════════════════════════════════════════════════════════════════════════

const CIVILISATION_SPHERES = [
  { 
    id: 1, 
    name: "Fournisseurs", 
    icon: "🏭",
    keyword: "FOURNISSEUR",
    description: "Gestion des partenaires",
    features: ["Liste fournisseurs", "Contacts", "Évaluations"],
    level: 1, // Impulsion - Le début de la chaîne
  },
  { 
    id: 2, 
    name: "Matériaux", 
    icon: "🧱",
    keyword: "MATERIAU",
    description: "Base de données matériaux",
    features: ["Catalogue", "Spécifications", "Stock"],
    level: 2, // Dualité - Choix entre matériaux
  },
  { 
    id: 3, 
    name: "Prix", 
    icon: "💰",
    keyword: "PRIX",
    description: "Comparaison et analyse",
    features: ["Listes de prix", "Historique", "Tendances"],
    level: 3, // Mental - Calculs et analyse
  },
  { 
    id: 4, 
    name: "Projets", 
    icon: "📋",
    keyword: "PROJET",
    description: "Gestion des chantiers",
    features: ["Planification", "Ressources", "Suivi"],
    level: 4, // Structure/Silence - L'ancre centrale ★
  },
  { 
    id: 5, 
    name: "Transport", 
    icon: "🚚",
    keyword: "TRANSPORT",
    description: "Logistique et livraisons",
    features: ["Calcul trajets", "Optimisation", "Coûts"],
    level: 5, // Mouvement/Feu - L'action
  },
  { 
    id: 6, 
    name: "Adresses", 
    icon: "📍",
    keyword: "ADRESSE",
    description: "Localisation des travaux",
    features: ["Géolocalisation", "Zones", "Distances"],
    level: 6, // Harmonie - Organisation spatiale
  },
  { 
    id: 7, 
    name: "Historique", 
    icon: "📜",
    keyword: "HISTORIQUE",
    description: "Archives et traçabilité",
    features: ["Transactions", "Modifications", "Audit"],
    level: 7, // Introspection - Regarder en arrière
  },
  { 
    id: 8, 
    name: "Communications", 
    icon: "📧",
    keyword: "COURRIEL",
    description: "Courriels et téléphone",
    features: ["Extraction auto", "Historique", "Contacts"],
    level: 8, // Infini - Flux continu
  },
  { 
    id: 9, 
    name: "Documents", 
    icon: "☁️",
    keyword: "DOCUMENT",
    description: "OneDrive et fichiers",
    features: ["Synchronisation", "Partage", "Versioning"],
    level: 9, // Unité - Tout connecté
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// 🔊 SPHÈRES SONORES — Système AT·OM pur
// ═══════════════════════════════════════════════════════════════════════════════

const SONORE_SPHERES = RESONANCE_MATRIX.map((res, index) => ({
  id: res.level,
  name: res.label.split('/')[0],
  subtitle: res.label.split('/')[1] || '',
  icon: ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '💜', '🩷', '⭐'][index],
  hz: res.hz,
  color: res.color,
  delay: res.delay,
  level: res.level,
  isAnchor: res.isAnchor || false,
}));

// Pierres de Fondation et Nœuds de Transition
const FOUNDATION_STONES = { FEU: 5, ACIER: 9, IA: 1, ADN: 1, SILENCE: 4 };
const TRANSITION_NODES = { DUALITE: 2, MENTAL: 3, HARMONIE: 6, SPIRITUALITE: 7, INFINI: 8 };

// ═══════════════════════════════════════════════════════════════════════════════
// 🔧 MOTEUR VIBRATIONNEL (Hook commun aux deux civilisations)
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

const useVibrationEngine = (input, sphereLevel = null) => {
  const [resonance, setResonance] = useState(null);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const debounceRef = useRef(null);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    
    debounceRef.current = setTimeout(() => {
      let level;
      let type = 'standard';
      let word = '';

      // Si on a un niveau de sphère directement (clic sur sphère)
      if (sphereLevel !== null) {
        level = sphereLevel;
        type = 'sphere';
        word = `SPHERE-${level}`;
      } 
      // Sinon, calcul depuis l'input texte
      else if (input?.trim()) {
        word = sanitize(input);
        if (!word) {
          setResonance(null);
          return;
        }

        if (FOUNDATION_STONES[word] !== undefined) {
          level = FOUNDATION_STONES[word];
          type = 'stone';
        } else if (TRANSITION_NODES[word] !== undefined) {
          level = TRANSITION_NODES[word];
          type = 'node';
        } else {
          level = calculateArithmos(word);
        }
      } else {
        setResonance(null);
        return;
      }

      const data = getResonance(level);
      
      setIsTransitioning(true);
      setResonance({
        word,
        level,
        hz: data.hz,
        color: data.color,
        delay: data.delay,
        label: data.label,
        type,
        isAnchor: data.isAnchor || false
      });

      // Log console stylisé
      const typeIcon = type === 'stone' ? '🧱' : type === 'node' ? '🌀' : type === 'sphere' ? '⭕' : '📝';
      console.log(
        `%c AT·OM %c ${typeIcon} %c ${word} → ${level} → ${data.hz}Hz`,
        'background: #50C878; color: white; padding: 2px 6px; border-radius: 3px;',
        'background: #1a1a2e; padding: 2px 4px;',
        `color: ${data.color}; font-weight: bold;`
      );

      setTimeout(() => setIsTransitioning(false), TRANSITION_DURATION);
    }, DEBOUNCE_DELAY);

    return () => clearTimeout(debounceRef.current);
  }, [input, sphereLevel]);

  return { resonance, isTransitioning };
};

// ═══════════════════════════════════════════════════════════════════════════════
// 🏛️ COMPOSANT CIVILISATION (Interface Business)
// ═══════════════════════════════════════════════════════════════════════════════

const CivilisationMode = ({ resonance, isTransitioning, onSphereClick, activeSphere }) => {
  return (
    <div style={{ padding: '1rem' }}>
      {/* Grille des 9 Sphères Business */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '1rem',
        maxWidth: '600px',
        margin: '0 auto',
      }}>
        {CIVILISATION_SPHERES.map(sphere => {
          const res = getResonance(sphere.level);
          const isActive = activeSphere === sphere.id || resonance?.level === sphere.level;
          
          return (
            <div
              key={sphere.id}
              onClick={() => onSphereClick(sphere)}
              style={{
                background: isActive 
                  ? `linear-gradient(135deg, ${res.color}40 0%, ${res.color}20 100%)`
                  : 'rgba(255,255,255,0.03)',
                border: `2px solid ${isActive ? res.color : '#333'}`,
                borderRadius: '16px',
                padding: '1.25rem',
                cursor: 'pointer',
                transition: `all ${TRANSITION_DURATION}ms ease-out`,
                transform: isActive ? 'scale(1.02)' : 'scale(1)',
                boxShadow: isActive ? `0 0 30px ${res.color}40` : 'none',
              }}
            >
              {/* En-tête */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem',
                marginBottom: '0.5rem',
              }}>
                <span style={{ fontSize: '1.5rem' }}>{sphere.icon}</span>
                <span style={{ 
                  fontWeight: 'bold', 
                  color: isActive ? res.color : '#fff',
                  fontSize: '1rem',
                }}>
                  {sphere.name}
                </span>
              </div>
              
              {/* Description */}
              <p style={{ 
                color: '#888', 
                fontSize: '0.75rem',
                margin: '0 0 0.5rem 0',
              }}>
                {sphere.description}
              </p>
              
              {/* Indicateur de fréquence */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginTop: '0.5rem',
                paddingTop: '0.5rem',
                borderTop: `1px solid ${isActive ? res.color : '#333'}40`,
              }}>
                <span style={{ 
                  fontSize: '0.65rem', 
                  color: res.color,
                  fontWeight: 'bold',
                }}>
                  {res.hz}Hz
                </span>
                <span style={{ 
                  fontSize: '0.65rem', 
                  color: '#666',
                }}>
                  Niveau {sphere.level}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Panneau de détails (si sphère active) */}
      {activeSphere && (
        <div style={{
          marginTop: '2rem',
          padding: '1.5rem',
          background: `${getResonance(CIVILISATION_SPHERES[activeSphere - 1].level).color}10`,
          border: `1px solid ${getResonance(CIVILISATION_SPHERES[activeSphere - 1].level).color}30`,
          borderRadius: '16px',
          maxWidth: '600px',
          margin: '2rem auto 0',
        }}>
          {(() => {
            const sphere = CIVILISATION_SPHERES[activeSphere - 1];
            const res = getResonance(sphere.level);
            return (
              <>
                <h3 style={{ 
                  color: res.color, 
                  margin: '0 0 1rem 0',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                }}>
                  {sphere.icon} {sphere.name}
                  <span style={{ 
                    fontSize: '0.8rem', 
                    fontWeight: 'normal',
                    color: '#888',
                  }}>
                    — {res.hz}Hz
                  </span>
                </h3>
                <div style={{ 
                  display: 'flex', 
                  gap: '0.5rem', 
                  flexWrap: 'wrap' 
                }}>
                  {sphere.features.map((feature, i) => (
                    <span
                      key={i}
                      style={{
                        padding: '0.4rem 0.8rem',
                        background: `${res.color}20`,
                        border: `1px solid ${res.color}40`,
                        borderRadius: '20px',
                        fontSize: '0.8rem',
                        color: res.color,
                      }}
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </>
            );
          })()}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// 🔊 COMPOSANT SONORE (Interface AT·OM)
// ═══════════════════════════════════════════════════════════════════════════════

const SonoreMode = ({ resonance, isTransitioning, onSphereClick, activeSphere }) => {
  return (
    <div style={{ padding: '1rem' }}>
      {/* Les 9 Sphères Sonores en cercle */}
      <div style={{
        position: 'relative',
        width: '400px',
        height: '400px',
        margin: '0 auto',
      }}>
        {/* Cercles de fond */}
        {[1, 2, 3].map(i => (
          <div
            key={i}
            style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              width: `${i * 120}px`,
              height: `${i * 120}px`,
              transform: 'translate(-50%, -50%)',
              borderRadius: '50%',
              border: `1px solid ${resonance?.color || '#333'}20`,
              transition: `all ${TRANSITION_DURATION}ms ease-out`,
            }}
          />
        ))}

        {/* Les 9 Sphères */}
        {SONORE_SPHERES.map((sphere, index) => {
          const angle = (index * 40) - 90; // Répartition en cercle
          const radius = 150;
          const x = Math.cos((angle * Math.PI) / 180) * radius;
          const y = Math.sin((angle * Math.PI) / 180) * radius;
          const isActive = activeSphere === sphere.id || resonance?.level === sphere.level;
          
          return (
            <div
              key={sphere.id}
              onClick={() => onSphereClick(sphere)}
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                width: '60px',
                height: '60px',
                transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
                borderRadius: '50%',
                background: isActive 
                  ? `radial-gradient(circle, ${sphere.color} 0%, ${sphere.color}80 100%)`
                  : `${sphere.color}20`,
                border: `3px solid ${isActive ? sphere.color : sphere.color + '60'}`,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                transition: `all ${TRANSITION_DURATION}ms ease-out`,
                boxShadow: isActive ? `0 0 25px ${sphere.color}` : 'none',
                transform: isActive 
                  ? `translate(calc(-50% + ${x}px), calc(-50% + ${y}px)) scale(1.15)`
                  : `translate(calc(-50% + ${x}px), calc(-50% + ${y}px)) scale(1)`,
              }}
            >
              <span style={{ 
                fontSize: '1.2rem', 
                fontWeight: 'bold',
                color: isActive ? '#000' : sphere.color,
              }}>
                {sphere.level}
              </span>
              <span style={{ 
                fontSize: '0.55rem',
                color: isActive ? '#333' : '#888',
              }}>
                {sphere.hz}Hz
              </span>
            </div>
          );
        })}

        {/* Centre */}
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '90px',
          height: '90px',
          borderRadius: '50%',
          background: resonance ? `${resonance.color}30` : '#1a1a2e',
          border: `3px solid ${resonance?.color || '#444'}`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          transition: `all ${TRANSITION_DURATION}ms ease-out`,
          boxShadow: resonance ? `0 0 40px ${resonance.color}40` : 'none',
        }}>
          {resonance ? (
            <>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: resonance.color }}>
                {resonance.level}
              </div>
              <div style={{ fontSize: '0.7rem', color: resonance.color }}>
                {resonance.hz}Hz
              </div>
            </>
          ) : (
            <div style={{ fontSize: '0.8rem', color: '#666' }}>AT·OM</div>
          )}
        </div>
      </div>

      {/* Info sur la sphère active */}
      {resonance && (
        <div style={{
          textAlign: 'center',
          marginTop: '1.5rem',
          padding: '1rem',
          background: `${resonance.color}10`,
          borderRadius: '12px',
          maxWidth: '300px',
          margin: '1.5rem auto 0',
        }}>
          <div style={{ 
            fontSize: '1.2rem', 
            fontWeight: 'bold', 
            color: resonance.color,
            marginBottom: '0.25rem',
          }}>
            {resonance.label}
          </div>
          <div style={{ color: '#888', fontSize: '0.8rem' }}>
            Délai: {resonance.delay}ms | Type: {resonance.type}
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// 🎭 COMPOSANT PRINCIPAL — LE SWITCH
// ═══════════════════════════════════════════════════════════════════════════════

const CivilisationSwitch = () => {
  const [mode, setMode] = useState('civilisation'); // 'civilisation' ou 'sonore'
  const [inputValue, setInputValue] = useState('');
  const [activeSphere, setActiveSphere] = useState(null);
  const [sphereLevel, setSphereLevel] = useState(null);
  
  // Le moteur vibrationnel unique
  const { resonance, isTransitioning } = useVibrationEngine(
    sphereLevel === null ? inputValue : null,
    sphereLevel
  );

  const handleSphereClick = useCallback((sphere) => {
    setActiveSphere(sphere.id);
    setSphereLevel(sphere.level);
    setInputValue(''); // Reset input quand on clique sur une sphère
  }, []);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    setActiveSphere(null);
    setSphereLevel(null);
  };

  // Couleur du thème basée sur la résonance
  const themeColor = resonance?.color || '#50C878';

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%)',
      color: 'white',
      fontFamily: 'system-ui, -apple-system, sans-serif',
    }}>
      {/* Header avec Switch */}
      <header style={{
        padding: '1rem',
        borderBottom: `1px solid ${themeColor}20`,
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          maxWidth: '800px',
          margin: '0 auto',
        }}>
          {/* Logo */}
          <h1 style={{ 
            margin: 0,
            fontSize: '1.5rem',
            fontWeight: 200,
            letterSpacing: '0.2em',
            color: themeColor,
            transition: `color ${TRANSITION_DURATION}ms ease-out`,
          }}>
            AT·OM
          </h1>

          {/* Switch de Civilisation */}
          <div style={{
            display: 'flex',
            background: 'rgba(255,255,255,0.05)',
            borderRadius: '25px',
            padding: '4px',
          }}>
            <button
              onClick={() => setMode('civilisation')}
              style={{
                padding: '0.5rem 1.25rem',
                border: 'none',
                borderRadius: '20px',
                background: mode === 'civilisation' ? themeColor : 'transparent',
                color: mode === 'civilisation' ? '#000' : '#888',
                cursor: 'pointer',
                fontSize: '0.85rem',
                fontWeight: mode === 'civilisation' ? 'bold' : 'normal',
                transition: `all ${TRANSITION_DURATION}ms ease-out`,
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
              }}
            >
              <span>🏛️</span>
              <span>Civilisation</span>
            </button>
            <button
              onClick={() => setMode('sonore')}
              style={{
                padding: '0.5rem 1.25rem',
                border: 'none',
                borderRadius: '20px',
                background: mode === 'sonore' ? themeColor : 'transparent',
                color: mode === 'sonore' ? '#000' : '#888',
                cursor: 'pointer',
                fontSize: '0.85rem',
                fontWeight: mode === 'sonore' ? 'bold' : 'normal',
                transition: `all ${TRANSITION_DURATION}ms ease-out`,
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
              }}
            >
              <span>🔊</span>
              <span>Sonore</span>
            </button>
          </div>

          {/* Indicateur de fréquence */}
          <div style={{
            textAlign: 'right',
            fontSize: '0.8rem',
          }}>
            <div style={{ color: themeColor, fontWeight: 'bold' }}>
              {resonance ? `${resonance.hz} Hz` : `${SYSTEM_HEARTBEAT} Hz`}
            </div>
            <div style={{ color: '#666', fontSize: '0.7rem' }}>
              {resonance?.label || 'En attente...'}
            </div>
          </div>
        </div>
      </header>

      {/* Barre de recherche universelle */}
      <div style={{
        padding: '1rem',
        maxWidth: '500px',
        margin: '0 auto',
      }}>
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder={mode === 'civilisation' 
            ? "Rechercher un fournisseur, matériau, projet..." 
            : "Entrez un mot pour calculer sa fréquence..."
          }
          style={{
            width: '100%',
            padding: '0.75rem 1.25rem',
            fontSize: '1rem',
            background: 'rgba(255,255,255,0.05)',
            border: `2px solid ${themeColor}40`,
            borderRadius: '25px',
            color: 'white',
            outline: 'none',
            textAlign: 'center',
            transition: `all ${TRANSITION_DURATION}ms ease-out`,
          }}
        />
      </div>

      {/* Zone principale selon le mode */}
      {mode === 'civilisation' ? (
        <CivilisationMode 
          resonance={resonance}
          isTransitioning={isTransitioning}
          onSphereClick={handleSphereClick}
          activeSphere={activeSphere}
        />
      ) : (
        <SonoreMode
          resonance={resonance}
          isTransitioning={isTransitioning}
          onSphereClick={handleSphereClick}
          activeSphere={activeSphere}
        />
      )}

      {/* Feedback de résonance (commun aux deux modes) */}
      {resonance && (
        <div style={{
          position: 'fixed',
          bottom: '1rem',
          left: '50%',
          transform: 'translateX(-50%)',
          background: `${resonance.color}20`,
          border: `1px solid ${resonance.color}40`,
          borderRadius: '25px',
          padding: '0.5rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          backdropFilter: 'blur(10px)',
        }}>
          <div style={{ 
            width: '12px', 
            height: '12px', 
            borderRadius: '50%',
            background: resonance.color,
            boxShadow: `0 0 10px ${resonance.color}`,
            animation: isTransitioning ? 'pulse 600ms ease-out' : 'none',
          }} />
          <span style={{ color: resonance.color, fontWeight: 'bold' }}>
            {resonance.word}
          </span>
          <span style={{ color: '#888' }}>→</span>
          <span style={{ color: resonance.color }}>
            {resonance.level}
          </span>
          <span style={{ color: '#888' }}>→</span>
          <span style={{ color: resonance.color, fontWeight: 'bold' }}>
            {resonance.hz}Hz
          </span>
        </div>
      )}

      {/* Footer */}
      <footer style={{
        position: 'fixed',
        bottom: '0',
        left: '0',
        right: '0',
        padding: '0.5rem',
        textAlign: 'center',
        background: 'linear-gradient(transparent, #0a0a1a)',
        color: '#444',
        fontSize: '0.7rem',
      }}>
        Architecte: Jonathan Rodrigue (999 Hz) | Moteur Vibrationnel v1.0
      </footer>

      {/* Animations */}
      <style>{`
        @keyframes pulse {
          0% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.5); opacity: 0.5; }
          100% { transform: scale(1); opacity: 1; }
        }
        
        input::placeholder {
          color: #555;
        }
        
        * {
          box-sizing: border-box;
        }
        
        ::-webkit-scrollbar {
          width: 8px;
        }
        
        ::-webkit-scrollbar-track {
          background: #1a1a2e;
        }
        
        ::-webkit-scrollbar-thumb {
          background: ${themeColor}40;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};

export default CivilisationSwitch;
