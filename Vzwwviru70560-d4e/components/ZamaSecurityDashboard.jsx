/**
 * ZAMA Security Dashboard v1.0
 * Tableau de Bord de Sécurité pour l'Armure Bio-Résonante
 *
 * Visualise l'état des couches de sécurité, les phases actives,
 * et les témoins de pierres d'ancrage.
 *
 * @author AT·OM Collective
 * @version 1.0.0
 */

import React, { useState, useEffect, useMemo } from 'react';

// ==================== CONSTANTES ====================

const PHI = 1.61803398875;

/**
 * Configuration des couches de sécurité
 */
const SECURITY_LAYERS = {
  GEOMETRY: {
    id: 'geometry',
    name: 'Géométrie Sacrée',
    icon: '⬡',
    color: '#FFD700',
    description: 'Mesures M, P, I, Po calibrées',
    level: 1
  },
  OCULAR: {
    id: 'ocular',
    name: 'Biométrie Oculaire',
    icon: '👁',
    color: '#667eea',
    description: 'Scan iris validé',
    level: 2
  },
  FINGERPRINT: {
    id: 'fingerprint',
    name: 'Empreinte Digitale',
    icon: '🔐',
    color: '#00b894',
    description: 'Signature biométrique',
    level: 3
  },
  BIORESONANCE: {
    id: 'bioresonance',
    name: 'Bio-Résonance',
    icon: '💓',
    color: '#ff6b6b',
    description: 'Synchronisation BPM',
    level: 4
  }
};

/**
 * Configuration des phases d'armure
 */
const ARMOR_PHASES = {
  NOYAU: {
    id: 'noyau',
    name: 'Phase 1: Noyau',
    symbols: ['Cube de Métatron', 'Fleur de Vie'],
    requiredLayers: ['GEOMETRY'],
    color: '#9370DB',
    chakra: 'Plexus Solaire / Cœur'
  },
  ANCRAGE: {
    id: 'ancrage',
    name: 'Phase 2: Ancrage',
    symbols: ['Triskel', 'Sceau de Protection'],
    requiredLayers: ['GEOMETRY'],
    color: '#20B2AA',
    chakra: 'Racine / Sacrum'
  },
  SENSEURS: {
    id: 'senseurs',
    name: 'Phase 3: Senseurs',
    symbols: ['Œil d\'Horus'],
    requiredLayers: ['GEOMETRY', 'OCULAR'],
    color: '#FF6347',
    chakra: '3ème Œil'
  }
};

/**
 * Configuration des pierres d'ancrage
 */
const ANCHOR_STONES = {
  OBSIDIENNE: {
    name: 'Obsidienne Noire',
    location: 'Sacrum',
    chakra: 'Racine',
    function: 'Protection & Ancrage',
    color: '#1a1a1a',
    phase: 'ANCRAGE'
  },
  TOURMALINE: {
    name: 'Tourmaline Noire',
    location: 'Plexus',
    chakra: 'Plexus Solaire',
    function: 'Bouclier EM',
    color: '#2d2d2d',
    phase: 'ANCRAGE'
  },
  CITRINE: {
    name: 'Citrine',
    location: 'Plexus Solaire',
    chakra: 'Manipura',
    function: 'Manifestation',
    color: '#f4a460',
    phase: 'NOYAU'
  },
  AMETHYSTE: {
    name: 'Améthyste',
    location: '3ème Œil',
    chakra: 'Ajna',
    function: 'Intuition',
    color: '#9370DB',
    phase: 'SENSEURS'
  },
  QUARTZ: {
    name: 'Quartz Clair',
    location: 'Couronne',
    chakra: 'Sahasrara',
    function: 'Amplification',
    color: '#f0f0f0',
    phase: 'NOYAU'
  },
  LABRADORITE: {
    name: 'Labradorite',
    location: 'Gorge',
    chakra: 'Vishuddha',
    function: 'Transformation',
    color: '#4a6fa5',
    phase: 'SENSEURS'
  }
};

// ==================== COMPOSANTS ====================

/**
 * Indicateur de couche de sécurité
 */
const SecurityLayerCard = ({ layer, isActive, onActivate }) => {
  const config = SECURITY_LAYERS[layer];

  return (
    <div
      className={`security-layer-card ${isActive ? 'active' : 'inactive'}`}
      onClick={() => !isActive && onActivate(layer)}
    >
      <div
        className="layer-icon"
        style={{ backgroundColor: isActive ? config.color : '#333' }}
      >
        {config.icon}
      </div>
      <div className="layer-info">
        <h4>{config.name}</h4>
        <p>{config.description}</p>
        <span className="layer-level">Niveau {config.level}</span>
      </div>
      <div className={`layer-status ${isActive ? 'active' : ''}`}>
        {isActive ? '✓' : '○'}
      </div>
    </div>
  );
};

/**
 * Carte de phase d'armure
 */
const PhaseCard = ({ phase, isUnlocked, activeLayers }) => {
  const config = ARMOR_PHASES[phase];
  const missingLayers = config.requiredLayers.filter(l => !activeLayers.includes(l));

  return (
    <div
      className={`phase-card ${isUnlocked ? 'unlocked' : 'locked'}`}
      style={{ borderColor: isUnlocked ? config.color : '#333' }}
    >
      <div className="phase-header" style={{ backgroundColor: isUnlocked ? config.color : '#222' }}>
        <h3>{config.name}</h3>
        <span className="chakra-badge">{config.chakra}</span>
      </div>

      <div className="phase-symbols">
        {config.symbols.map(symbol => (
          <div key={symbol} className="symbol-badge">
            {symbol}
          </div>
        ))}
      </div>

      {!isUnlocked && missingLayers.length > 0 && (
        <div className="unlock-requirements">
          <span>Requiert:</span>
          {missingLayers.map(l => (
            <span key={l} className="requirement-badge">
              {SECURITY_LAYERS[l].name}
            </span>
          ))}
        </div>
      )}

      <div className={`phase-status ${isUnlocked ? 'active' : ''}`}>
        {isUnlocked ? 'DÉVERROUILLÉ' : 'VERROUILLÉ'}
      </div>
    </div>
  );
};

/**
 * Témoin de pierre d'ancrage
 */
const StoneWitness = ({ stone, isPresent, onToggle }) => {
  const config = ANCHOR_STONES[stone];

  return (
    <div
      className={`stone-witness ${isPresent ? 'present' : 'absent'}`}
      onClick={() => onToggle(stone)}
    >
      <div
        className="stone-gem"
        style={{
          backgroundColor: config.color,
          boxShadow: isPresent ? `0 0 15px ${config.color}` : 'none'
        }}
      />
      <div className="stone-info">
        <span className="stone-name">{config.name}</span>
        <span className="stone-location">{config.location}</span>
        <span className="stone-function">{config.function}</span>
      </div>
      <div className={`stone-status ${isPresent ? 'active' : ''}`}>
        {isPresent ? '◉' : '○'}
      </div>
    </div>
  );
};

/**
 * Panel des mesures biométriques
 */
const BiometricsLivePanel = ({ measures, harmonicScore }) => {
  if (!measures) return null;

  const dimensions = {
    small: (measures.M * PHI).toFixed(2),
    medium: (measures.M * Math.pow(PHI, 2)).toFixed(2),
    large: (measures.M * Math.pow(PHI, 3)).toFixed(2)
  };

  return (
    <div className="biometrics-live-panel">
      <h3>📐 Mesures Bio-Résonantes</h3>

      <div className="measures-row">
        <div className="measure-box">
          <span className="measure-label">M</span>
          <span className="measure-value">{measures.M}</span>
          <span className="measure-unit">cm</span>
        </div>
        <div className="measure-box">
          <span className="measure-label">P</span>
          <span className="measure-value">{measures.P}</span>
          <span className="measure-unit">cm</span>
        </div>
        <div className="measure-box">
          <span className="measure-label">I</span>
          <span className="measure-value">{measures.I}</span>
          <span className="measure-unit">cm</span>
        </div>
        <div className="measure-box">
          <span className="measure-label">Po</span>
          <span className="measure-value">{measures.Po}</span>
          <span className="measure-unit">cm</span>
        </div>
      </div>

      <div className="dimensions-row">
        <div className="dimension-item">
          <span>Petits (M×φ)</span>
          <span className="dim-value">{dimensions.small} cm</span>
        </div>
        <div className="dimension-item">
          <span>Moyens (M×φ²)</span>
          <span className="dim-value">{dimensions.medium} cm</span>
        </div>
        <div className="dimension-item">
          <span>Grands (M×φ³)</span>
          <span className="dim-value">{dimensions.large} cm</span>
        </div>
      </div>

      {harmonicScore !== undefined && (
        <div className="harmonic-score">
          <span>Score Harmonique</span>
          <div className="score-bar">
            <div
              className="score-fill"
              style={{
                width: `${harmonicScore}%`,
                backgroundColor: harmonicScore > 70 ? '#00FF7F' : harmonicScore > 40 ? '#FFD700' : '#FF6347'
              }}
            />
          </div>
          <span className="score-value">{harmonicScore}/100</span>
        </div>
      )}
    </div>
  );
};

/**
 * Indicateur de statut global
 */
const GlobalStatusIndicator = ({ securityScore, phasesUnlocked, stonesPresent }) => {
  const getStatusLevel = () => {
    if (securityScore >= 75 && phasesUnlocked >= 3 && stonesPresent >= 4) return 'OPTIMAL';
    if (securityScore >= 50 && phasesUnlocked >= 2 && stonesPresent >= 2) return 'ACTIF';
    if (securityScore >= 25 && phasesUnlocked >= 1) return 'PARTIEL';
    return 'INACTIF';
  };

  const statusColors = {
    OPTIMAL: '#00FF7F',
    ACTIF: '#FFD700',
    PARTIEL: '#FFA500',
    INACTIF: '#666'
  };

  const status = getStatusLevel();

  return (
    <div className="global-status" style={{ borderColor: statusColors[status] }}>
      <div className="status-ring" style={{ borderColor: statusColors[status] }}>
        <span className="status-label">{status}</span>
      </div>
      <div className="status-details">
        <div className="detail-item">
          <span>Sécurité</span>
          <span>{securityScore}%</span>
        </div>
        <div className="detail-item">
          <span>Phases</span>
          <span>{phasesUnlocked}/3</span>
        </div>
        <div className="detail-item">
          <span>Pierres</span>
          <span>{stonesPresent}/6</span>
        </div>
      </div>
    </div>
  );
};

// ==================== COMPOSANT PRINCIPAL ====================

/**
 * Dashboard de Sécurité ZAMA
 */
const ZamaSecurityDashboard = ({
  initialMeasures = null,
  onSecurityChange = () => {},
  onMintReady = () => {}
}) => {
  // États
  const [measures, setMeasures] = useState(initialMeasures);
  const [activeLayers, setActiveLayers] = useState(['GEOMETRY']);
  const [presentStones, setPresentStones] = useState(['CITRINE', 'OBSIDIENNE']);
  const [harmonicScore, setHarmonicScore] = useState(72);
  const [bpm, setBpm] = useState(null);

  // Calculs dérivés
  const securityScore = useMemo(() => {
    return Math.round((activeLayers.length / 4) * 100);
  }, [activeLayers]);

  const unlockedPhases = useMemo(() => {
    return Object.keys(ARMOR_PHASES).filter(phase => {
      const config = ARMOR_PHASES[phase];
      return config.requiredLayers.every(l => activeLayers.includes(l));
    });
  }, [activeLayers]);

  // Handlers
  const handleLayerActivate = (layer) => {
    // Vérifier les prérequis
    const layerConfig = SECURITY_LAYERS[layer];
    const prerequisiteMet = layerConfig.level === 1 ||
      activeLayers.includes(Object.keys(SECURITY_LAYERS).find(
        l => SECURITY_LAYERS[l].level === layerConfig.level - 1
      ));

    if (!prerequisiteMet) {
      alert(`Vous devez d'abord activer le niveau ${layerConfig.level - 1}`);
      return;
    }

    setActiveLayers(prev => [...prev, layer]);
    onSecurityChange({ layers: [...activeLayers, layer] });
  };

  const handleStoneToggle = (stone) => {
    setPresentStones(prev =>
      prev.includes(stone)
        ? prev.filter(s => s !== stone)
        : [...prev, stone]
    );
  };

  const handleSimulateBPM = () => {
    const simulatedBPM = 60 + Math.floor(Math.random() * 20);
    setBpm(simulatedBPM);
    if (!activeLayers.includes('BIORESONANCE')) {
      setActiveLayers(prev => [...prev, 'BIORESONANCE']);
    }
  };

  // Vérifier si prêt pour mint
  useEffect(() => {
    if (securityScore >= 50 && unlockedPhases.length >= 2) {
      onMintReady(true);
    }
  }, [securityScore, unlockedPhases, onMintReady]);

  return (
    <div className="zama-security-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <h1>🛡️ ZAMA Security Dashboard</h1>
        <p>Tableau de Bord de l'Armure Bio-Résonante</p>
      </header>

      {/* Status Global */}
      <section className="dashboard-section status-section">
        <GlobalStatusIndicator
          securityScore={securityScore}
          phasesUnlocked={unlockedPhases.length}
          stonesPresent={presentStones.length}
        />
      </section>

      {/* Mesures Biométriques */}
      <section className="dashboard-section biometrics-section">
        <BiometricsLivePanel
          measures={measures || { M: 2.1, P: 8.5, I: 7.2, Po: 9.5 }}
          harmonicScore={harmonicScore}
        />
      </section>

      {/* Couches de Sécurité */}
      <section className="dashboard-section security-section">
        <h2>🔐 Couches de Sécurité</h2>
        <div className="security-layers-grid">
          {Object.keys(SECURITY_LAYERS).map(layer => (
            <SecurityLayerCard
              key={layer}
              layer={layer}
              isActive={activeLayers.includes(layer)}
              onActivate={handleLayerActivate}
            />
          ))}
        </div>
      </section>

      {/* Phases d'Armure */}
      <section className="dashboard-section phases-section">
        <h2>⚡ Phases d'Activation</h2>
        <div className="phases-grid">
          {Object.keys(ARMOR_PHASES).map(phase => (
            <PhaseCard
              key={phase}
              phase={phase}
              isUnlocked={unlockedPhases.includes(phase)}
              activeLayers={activeLayers}
            />
          ))}
        </div>
      </section>

      {/* Témoins de Pierres */}
      <section className="dashboard-section stones-section">
        <h2>💎 Témoins de Pierres d'Ancrage</h2>
        <p className="section-hint">Cliquez pour confirmer la présence physique</p>
        <div className="stones-grid">
          {Object.keys(ANCHOR_STONES).map(stone => (
            <StoneWitness
              key={stone}
              stone={stone}
              isPresent={presentStones.includes(stone)}
              onToggle={handleStoneToggle}
            />
          ))}
        </div>
      </section>

      {/* Actions */}
      <section className="dashboard-section actions-section">
        <button
          className="action-button bpm-button"
          onClick={handleSimulateBPM}
        >
          {bpm ? `💓 ${bpm} BPM` : '💓 Connecter BPM'}
        </button>

        {securityScore >= 50 && (
          <button
            className="action-button mint-button"
            onClick={() => onMintReady({ measures, layers: activeLayers, stones: presentStones })}
          >
            ⛓️ Prêt pour Hedera
          </button>
        )}
      </section>

      {/* Styles */}
      <style jsx>{`
        .zama-security-dashboard {
          min-height: 100vh;
          background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
          color: #fff;
          font-family: 'Segoe UI', system-ui, sans-serif;
          padding: 20px;
        }

        .dashboard-header {
          text-align: center;
          padding: 20px 0 30px;
          border-bottom: 1px solid #333;
          margin-bottom: 30px;
        }

        .dashboard-header h1 {
          font-size: 2rem;
          margin: 0;
          background: linear-gradient(135deg, #FFD700, #FFA500);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .dashboard-header p {
          color: #888;
          margin-top: 5px;
        }

        .dashboard-section {
          max-width: 1000px;
          margin: 0 auto 30px;
          padding: 20px;
          background: rgba(255, 255, 255, 0.02);
          border-radius: 12px;
          border: 1px solid #222;
        }

        .dashboard-section h2 {
          margin: 0 0 20px;
          font-size: 1.2rem;
          color: #aaa;
        }

        .section-hint {
          color: #666;
          font-size: 0.85rem;
          margin: -10px 0 15px;
        }

        /* Global Status */
        .global-status {
          display: flex;
          align-items: center;
          gap: 30px;
          padding: 20px;
          border: 2px solid;
          border-radius: 12px;
          background: rgba(0, 0, 0, 0.3);
        }

        .status-ring {
          width: 100px;
          height: 100px;
          border: 4px solid;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .status-label {
          font-weight: bold;
          font-size: 0.9rem;
        }

        .status-details {
          display: flex;
          gap: 30px;
        }

        .detail-item {
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .detail-item span:first-child {
          color: #888;
          font-size: 0.8rem;
        }

        .detail-item span:last-child {
          font-size: 1.5rem;
          font-weight: bold;
        }

        /* Biometrics Panel */
        .biometrics-live-panel h3 {
          margin: 0 0 15px;
          color: #FFD700;
        }

        .measures-row {
          display: flex;
          gap: 15px;
          margin-bottom: 20px;
        }

        .measure-box {
          flex: 1;
          padding: 15px;
          background: rgba(0, 0, 0, 0.3);
          border-radius: 8px;
          text-align: center;
          border: 1px solid #333;
        }

        .measure-label {
          display: block;
          color: #888;
          font-size: 0.8rem;
        }

        .measure-value {
          display: block;
          font-size: 1.8rem;
          font-weight: bold;
          color: #FFD700;
        }

        .measure-unit {
          color: #666;
          font-size: 0.8rem;
        }

        .dimensions-row {
          display: flex;
          gap: 10px;
          margin-bottom: 15px;
        }

        .dimension-item {
          flex: 1;
          padding: 10px;
          background: rgba(147, 112, 219, 0.1);
          border-radius: 5px;
          display: flex;
          justify-content: space-between;
          font-size: 0.85rem;
        }

        .dim-value {
          color: #9370DB;
          font-weight: bold;
        }

        .harmonic-score {
          display: flex;
          align-items: center;
          gap: 15px;
          padding: 10px;
          background: rgba(0, 0, 0, 0.2);
          border-radius: 5px;
        }

        .score-bar {
          flex: 1;
          height: 8px;
          background: #222;
          border-radius: 4px;
          overflow: hidden;
        }

        .score-fill {
          height: 100%;
          transition: width 0.5s ease;
        }

        .score-value {
          font-weight: bold;
          min-width: 60px;
          text-align: right;
        }

        /* Security Layers */
        .security-layers-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 15px;
        }

        .security-layer-card {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 15px;
          background: rgba(0, 0, 0, 0.3);
          border-radius: 8px;
          border: 1px solid #333;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .security-layer-card:hover {
          border-color: #555;
        }

        .security-layer-card.active {
          border-color: #FFD700;
        }

        .layer-icon {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1.2rem;
        }

        .layer-info h4 {
          margin: 0;
          font-size: 0.9rem;
        }

        .layer-info p {
          margin: 2px 0 0;
          font-size: 0.75rem;
          color: #888;
        }

        .layer-level {
          font-size: 0.7rem;
          color: #666;
        }

        .layer-status {
          margin-left: auto;
          font-size: 1.2rem;
          color: #444;
        }

        .layer-status.active {
          color: #00FF7F;
        }

        /* Phases */
        .phases-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 15px;
        }

        .phase-card {
          border: 2px solid;
          border-radius: 10px;
          overflow: hidden;
          transition: all 0.3s ease;
        }

        .phase-card.locked {
          opacity: 0.6;
        }

        .phase-header {
          padding: 12px 15px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .phase-header h3 {
          margin: 0;
          font-size: 1rem;
        }

        .chakra-badge {
          font-size: 0.7rem;
          padding: 3px 8px;
          background: rgba(0, 0, 0, 0.3);
          border-radius: 10px;
        }

        .phase-symbols {
          padding: 15px;
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .symbol-badge {
          padding: 5px 10px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 5px;
          font-size: 0.8rem;
        }

        .unlock-requirements {
          padding: 10px 15px;
          background: rgba(255, 0, 0, 0.1);
          font-size: 0.8rem;
          color: #ff6b6b;
        }

        .requirement-badge {
          display: inline-block;
          margin-left: 5px;
          padding: 2px 6px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 3px;
        }

        .phase-status {
          padding: 10px 15px;
          text-align: center;
          font-size: 0.75rem;
          font-weight: bold;
          background: rgba(0, 0, 0, 0.2);
          color: #666;
        }

        .phase-status.active {
          color: #00FF7F;
        }

        /* Stones */
        .stones-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 12px;
        }

        .stone-witness {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 12px;
          background: rgba(0, 0, 0, 0.3);
          border-radius: 8px;
          border: 1px solid #333;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .stone-witness:hover {
          border-color: #555;
        }

        .stone-witness.present {
          border-color: #00FF7F;
        }

        .stone-gem {
          width: 30px;
          height: 30px;
          border-radius: 50%;
          transition: all 0.3s ease;
        }

        .stone-info {
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        .stone-name {
          font-size: 0.85rem;
          font-weight: 500;
        }

        .stone-location {
          font-size: 0.7rem;
          color: #888;
        }

        .stone-function {
          font-size: 0.7rem;
          color: #666;
        }

        .stone-status {
          font-size: 1.2rem;
          color: #444;
        }

        .stone-status.active {
          color: #00FF7F;
        }

        /* Actions */
        .actions-section {
          display: flex;
          gap: 15px;
          justify-content: center;
        }

        .action-button {
          padding: 15px 30px;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .bpm-button {
          background: linear-gradient(135deg, #ff6b6b, #ff4444);
          color: #fff;
        }

        .mint-button {
          background: linear-gradient(135deg, #00b894, #00cec9);
          color: #fff;
        }

        .action-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        @media (max-width: 600px) {
          .measures-row {
            flex-wrap: wrap;
          }

          .measure-box {
            flex: 1 1 45%;
          }

          .global-status {
            flex-direction: column;
            text-align: center;
          }

          .status-details {
            width: 100%;
            justify-content: center;
          }
        }
      `}</style>
    </div>
  );
};

export default ZamaSecurityDashboard;
