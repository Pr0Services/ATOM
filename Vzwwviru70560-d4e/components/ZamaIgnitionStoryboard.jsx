/**
 * ZAMA IGNITION Storyboard v1.0
 * Interface React pour l'activation RA de l'armure bio-résonante
 *
 * Ce composant simule l'activation RA synchronisée sur le BPM
 * et guide l'utilisateur à travers les phases d'activation.
 *
 * @author AT·OM Collective
 * @version 1.0.0
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';

// ==================== CONSTANTES ====================

const PHI = 1.61803398875;

const PHASES = {
  CALIBRATION: 'calibration',
  NOYAU: 'noyau',
  ANCRAGE: 'ancrage',
  SENSEURS: 'senseurs',
  ACTIVATION: 'activation'
};

const PHASE_CONFIG = {
  [PHASES.CALIBRATION]: {
    name: 'Calibration',
    description: 'Extraction des mesures biométriques',
    color: '#FFD700',
    symbols: []
  },
  [PHASES.NOYAU]: {
    name: 'Phase 1: Noyau',
    description: 'Activation du centre énergétique',
    color: '#9370DB',
    symbols: ['cube_metatron', 'fleur_de_vie']
  },
  [PHASES.ANCRAGE]: {
    name: 'Phase 2: Ancrage',
    description: 'Protection périphérique',
    color: '#20B2AA',
    symbols: ['triskel', 'sceau_protection']
  },
  [PHASES.SENSEURS]: {
    name: 'Phase 3: Senseurs',
    description: 'Vigilance active',
    color: '#FF6347',
    symbols: ['oeil_horus'],
    requiresIris: true
  },
  [PHASES.ACTIVATION]: {
    name: 'Activation Complète',
    description: 'Armure synchronisée',
    color: '#00FF7F',
    symbols: []
  }
};

// ==================== COMPOSANTS UTILITAIRES ====================

/**
 * Indicateur de BPM animé
 */
const BPMIndicator = ({ bpm, isActive }) => {
  const [pulse, setPulse] = useState(false);

  useEffect(() => {
    if (!isActive || !bpm) return;

    const interval = 60000 / bpm;
    const timer = setInterval(() => {
      setPulse(true);
      setTimeout(() => setPulse(false), 100);
    }, interval);

    return () => clearInterval(timer);
  }, [bpm, isActive]);

  return (
    <div className={`bpm-indicator ${pulse ? 'pulse' : ''}`}>
      <div className="heart-icon">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
        </svg>
      </div>
      <span className="bpm-value">{bpm || '--'} BPM</span>
    </div>
  );
};

/**
 * Symbole sacré animé
 */
const SacredSymbol = ({ type, size, isActive, bpmSync }) => {
  const symbols = {
    cube_metatron: '⬡',
    fleur_de_vie: '✿',
    triskel: '☯',
    sceau_protection: '∞',
    oeil_horus: '👁'
  };

  return (
    <div
      className={`sacred-symbol ${isActive ? 'active' : ''} ${bpmSync ? 'bpm-sync' : ''}`}
      style={{
        width: `${size}px`,
        height: `${size}px`,
        fontSize: `${size * 0.6}px`
      }}
    >
      <span>{symbols[type] || '◉'}</span>
    </div>
  );
};

/**
 * Barre de progression des phases
 */
const PhaseProgress = ({ currentPhase, completedPhases }) => {
  const phases = Object.keys(PHASE_CONFIG);

  return (
    <div className="phase-progress">
      {phases.map((phase, index) => {
        const config = PHASE_CONFIG[phase];
        const isCompleted = completedPhases.includes(phase);
        const isCurrent = currentPhase === phase;

        return (
          <div
            key={phase}
            className={`phase-item ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''}`}
          >
            <div
              className="phase-dot"
              style={{ backgroundColor: isCompleted || isCurrent ? config.color : '#444' }}
            />
            <span className="phase-label">{config.name}</span>
            {index < phases.length - 1 && <div className="phase-connector" />}
          </div>
        );
      })}
    </div>
  );
};

/**
 * Panneau de mesures biométriques
 */
const BiometricsPanel = ({ measures, onValidate, validated }) => {
  if (!measures) return null;

  const calculateDimension = (base, power) => {
    return (base * Math.pow(PHI, power)).toFixed(2);
  };

  return (
    <div className={`biometrics-panel ${validated ? 'validated' : ''}`}>
      <h3>Mesures Biométriques</h3>

      <div className="measures-grid">
        <div className="measure-item">
          <span className="label">Module (M)</span>
          <span className="value">{measures.M} cm</span>
        </div>
        <div className="measure-item">
          <span className="label">Paume (P)</span>
          <span className="value">{measures.P} cm</span>
        </div>
        <div className="measure-item">
          <span className="label">Index (I)</span>
          <span className="value">{measures.I} cm</span>
        </div>
        <div className="measure-item">
          <span className="label">Poing (Po)</span>
          <span className="value">{measures.Po} cm</span>
        </div>
      </div>

      <div className="calculated-dimensions">
        <h4>Dimensions Calculées (φ)</h4>
        <div className="dimension-item">
          <span>Petits Symboles:</span>
          <span>{calculateDimension(measures.M, 1)} cm</span>
        </div>
        <div className="dimension-item">
          <span>Symboles Moyens:</span>
          <span>{calculateDimension(measures.M, 2)} cm</span>
        </div>
        <div className="dimension-item">
          <span>Grands Symboles:</span>
          <span>{calculateDimension(measures.M, 3)} cm</span>
        </div>
      </div>

      {!validated && (
        <button className="validate-button" onClick={onValidate}>
          ✓ Valider la Bio-Résonance
        </button>
      )}

      {validated && (
        <div className="validation-badge">
          ✓ Mesures Scellées
        </div>
      )}
    </div>
  );
};

// ==================== COMPOSANT PRINCIPAL ====================

/**
 * Storyboard principal ZAMA IGNITION
 */
const ZamaIgnitionStoryboard = ({
  initialMeasures = null,
  onArmorComplete = () => {},
  onMintRequest = () => {}
}) => {
  // États
  const [currentPhase, setCurrentPhase] = useState(PHASES.CALIBRATION);
  const [completedPhases, setCompletedPhases] = useState([]);
  const [measures, setMeasures] = useState(initialMeasures);
  const [measuresValidated, setMeasuresValidated] = useState(false);
  const [bpm, setBpm] = useState(null);
  const [bpmConnected, setBpmConnected] = useState(false);
  const [irisValidated, setIrisValidated] = useState(false);
  const [activeSymbols, setActiveSymbols] = useState([]);
  const [isAnimating, setIsAnimating] = useState(false);

  // Refs
  const animationRef = useRef(null);

  // ==================== LOGIQUE DE PHASE ====================

  /**
   * Passe à la phase suivante
   */
  const advancePhase = useCallback(() => {
    const phases = Object.keys(PHASE_CONFIG);
    const currentIndex = phases.indexOf(currentPhase);

    if (currentIndex < phases.length - 1) {
      setCompletedPhases(prev => [...prev, currentPhase]);
      setCurrentPhase(phases[currentIndex + 1]);
    }
  }, [currentPhase]);

  /**
   * Active les symboles d'une phase
   */
  const activatePhaseSymbols = useCallback((phase) => {
    const config = PHASE_CONFIG[phase];
    if (!config?.symbols) return;

    setIsAnimating(true);

    config.symbols.forEach((symbol, index) => {
      setTimeout(() => {
        setActiveSymbols(prev => [...prev, symbol]);
      }, index * 500);
    });

    setTimeout(() => {
      setIsAnimating(false);
    }, config.symbols.length * 500 + 500);
  }, []);

  // ==================== HANDLERS ====================

  /**
   * Valide les mesures biométriques
   */
  const handleValidateMeasures = () => {
    setMeasuresValidated(true);
    advancePhase();
    activatePhaseSymbols(PHASES.NOYAU);
  };

  /**
   * Simule la connexion BPM
   */
  const handleConnectBPM = () => {
    setBpmConnected(true);
    // Simuler un BPM
    const simulatedBPM = 60 + Math.floor(Math.random() * 20);
    setBpm(simulatedBPM);
  };

  /**
   * Simule la validation iris
   */
  const handleValidateIris = () => {
    setIrisValidated(true);
    advancePhase();
    activatePhaseSymbols(PHASES.SENSEURS);
  };

  /**
   * Complète l'activation de l'armure
   */
  const handleCompleteActivation = () => {
    advancePhase();
    onArmorComplete({
      measures,
      bpm,
      phases: completedPhases,
      symbols: activeSymbols
    });
  };

  /**
   * Demande le minting sur Hedera
   */
  const handleMintRequest = () => {
    onMintRequest({
      measures,
      bpm,
      phases: completedPhases,
      symbols: activeSymbols
    });
  };

  // ==================== EFFETS ====================

  useEffect(() => {
    if (initialMeasures) {
      setMeasures(initialMeasures);
    }
  }, [initialMeasures]);

  // ==================== RENDU ====================

  const currentConfig = PHASE_CONFIG[currentPhase];

  return (
    <div className="zama-ignition-storyboard">
      {/* Header */}
      <header className="storyboard-header">
        <h1>ZAMA IGNITION</h1>
        <p className="subtitle">Activation de l'Armure Bio-Résonante</p>
        <BPMIndicator bpm={bpm} isActive={bpmConnected} />
      </header>

      {/* Progress */}
      <PhaseProgress
        currentPhase={currentPhase}
        completedPhases={completedPhases}
      />

      {/* Main Content */}
      <main className="storyboard-main">
        {/* Phase Info */}
        <div
          className="phase-info"
          style={{ borderColor: currentConfig.color }}
        >
          <h2 style={{ color: currentConfig.color }}>{currentConfig.name}</h2>
          <p>{currentConfig.description}</p>
        </div>

        {/* Symbols Display */}
        <div className="symbols-display">
          {activeSymbols.map((symbol, index) => (
            <SacredSymbol
              key={symbol}
              type={symbol}
              size={60 + index * 10}
              isActive={true}
              bpmSync={bpmConnected}
            />
          ))}
        </div>

        {/* Phase-specific content */}
        {currentPhase === PHASES.CALIBRATION && (
          <div className="calibration-section">
            <BiometricsPanel
              measures={measures}
              onValidate={handleValidateMeasures}
              validated={measuresValidated}
            />

            {!measures && (
              <div className="calibration-instructions">
                <p>Placez votre main avec un objet de référence (carte de crédit)</p>
                <button
                  onClick={() => setMeasures({ M: 2.1, P: 8.5, I: 7.2, Po: 9.5 })}
                >
                  Simuler Mesures
                </button>
              </div>
            )}
          </div>
        )}

        {currentPhase === PHASES.NOYAU && (
          <div className="noyau-section">
            <p>Les symboles du Noyau s'activent...</p>

            {!bpmConnected && (
              <button onClick={handleConnectBPM} className="connect-bpm-button">
                Connecter Capteur BPM
              </button>
            )}

            {bpmConnected && (
              <button onClick={advancePhase} className="advance-button">
                Continuer vers Ancrage
              </button>
            )}
          </div>
        )}

        {currentPhase === PHASES.ANCRAGE && (
          <div className="ancrage-section">
            <p>Protection périphérique en cours d'activation...</p>

            {!irisValidated && (
              <button onClick={handleValidateIris} className="iris-button">
                Scanner Iris pour Phase 3
              </button>
            )}
          </div>
        )}

        {currentPhase === PHASES.SENSEURS && (
          <div className="senseurs-section">
            <p>Senseurs activés - Vigilance maximale</p>
            <button onClick={handleCompleteActivation} className="complete-button">
              Finaliser Activation
            </button>
          </div>
        )}

        {currentPhase === PHASES.ACTIVATION && (
          <div className="activation-complete">
            <div className="success-icon">✓</div>
            <h2>Armure Activée</h2>
            <p>Toutes les phases sont synchronisées avec votre bio-résonance.</p>

            <button onClick={handleMintRequest} className="mint-button">
              Graver sur Hedera
            </button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="storyboard-footer">
        <span>AT·OM Collective</span>
        <span>•</span>
        <span>φ = {PHI.toFixed(6)}</span>
      </footer>

      {/* Styles */}
      <style jsx>{`
        .zama-ignition-storyboard {
          min-height: 100vh;
          background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
          color: #fff;
          font-family: 'Segoe UI', system-ui, sans-serif;
          padding: 20px;
        }

        .storyboard-header {
          text-align: center;
          padding: 20px 0;
          border-bottom: 1px solid #333;
        }

        .storyboard-header h1 {
          font-size: 2.5rem;
          background: linear-gradient(135deg, #FFD700, #FFA500);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          margin: 0;
        }

        .subtitle {
          color: #888;
          margin-top: 5px;
        }

        .bpm-indicator {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
          margin-top: 15px;
        }

        .bpm-indicator.pulse .heart-icon {
          transform: scale(1.3);
          color: #ff4444;
        }

        .heart-icon {
          width: 24px;
          height: 24px;
          color: #888;
          transition: all 0.1s ease;
        }

        .bpm-value {
          font-size: 1.2rem;
          font-weight: bold;
        }

        .phase-progress {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 10px;
          padding: 30px 0;
          flex-wrap: wrap;
        }

        .phase-item {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .phase-dot {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          transition: all 0.3s ease;
        }

        .phase-item.current .phase-dot {
          box-shadow: 0 0 10px currentColor;
        }

        .phase-label {
          font-size: 0.8rem;
          color: #888;
        }

        .phase-item.current .phase-label,
        .phase-item.completed .phase-label {
          color: #fff;
        }

        .phase-connector {
          width: 30px;
          height: 2px;
          background: #333;
        }

        .storyboard-main {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }

        .phase-info {
          text-align: center;
          padding: 20px;
          border: 2px solid;
          border-radius: 10px;
          margin-bottom: 30px;
        }

        .phase-info h2 {
          margin: 0 0 10px 0;
        }

        .phase-info p {
          margin: 0;
          color: #aaa;
        }

        .symbols-display {
          display: flex;
          justify-content: center;
          gap: 20px;
          padding: 30px 0;
          flex-wrap: wrap;
        }

        .sacred-symbol {
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 50%;
          transition: all 0.3s ease;
          opacity: 0.5;
        }

        .sacred-symbol.active {
          opacity: 1;
          animation: symbolAppear 0.5s ease;
        }

        .sacred-symbol.bpm-sync {
          animation: bpmPulse 1s infinite;
        }

        @keyframes symbolAppear {
          from { transform: scale(0); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }

        @keyframes bpmPulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.1); }
        }

        .biometrics-panel {
          background: rgba(255, 255, 255, 0.05);
          padding: 20px;
          border-radius: 10px;
          border: 1px solid #333;
        }

        .biometrics-panel h3 {
          margin: 0 0 15px 0;
          color: #FFD700;
        }

        .measures-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 15px;
          margin-bottom: 20px;
        }

        .measure-item {
          display: flex;
          flex-direction: column;
          padding: 10px;
          background: rgba(0, 0, 0, 0.3);
          border-radius: 5px;
        }

        .measure-item .label {
          font-size: 0.8rem;
          color: #888;
        }

        .measure-item .value {
          font-size: 1.4rem;
          font-weight: bold;
          color: #fff;
        }

        .calculated-dimensions {
          padding: 15px;
          background: rgba(147, 112, 219, 0.1);
          border-radius: 5px;
          margin-bottom: 20px;
        }

        .calculated-dimensions h4 {
          margin: 0 0 10px 0;
          color: #9370DB;
          font-size: 0.9rem;
        }

        .dimension-item {
          display: flex;
          justify-content: space-between;
          padding: 5px 0;
          font-size: 0.9rem;
        }

        .validate-button,
        .connect-bpm-button,
        .advance-button,
        .iris-button,
        .complete-button,
        .mint-button {
          display: block;
          width: 100%;
          padding: 15px;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .validate-button {
          background: linear-gradient(135deg, #FFD700, #FFA500);
          color: #000;
        }

        .connect-bpm-button {
          background: linear-gradient(135deg, #ff6b6b, #ff4444);
          color: #fff;
          margin-top: 20px;
        }

        .advance-button,
        .complete-button {
          background: linear-gradient(135deg, #4ecdc4, #44bd32);
          color: #fff;
          margin-top: 20px;
        }

        .iris-button {
          background: linear-gradient(135deg, #667eea, #764ba2);
          color: #fff;
          margin-top: 20px;
        }

        .mint-button {
          background: linear-gradient(135deg, #00b894, #00cec9);
          color: #fff;
          margin-top: 20px;
        }

        .validation-badge {
          padding: 15px;
          background: rgba(0, 255, 127, 0.2);
          border: 1px solid #00FF7F;
          border-radius: 8px;
          text-align: center;
          color: #00FF7F;
          font-weight: bold;
        }

        .activation-complete {
          text-align: center;
          padding: 40px;
        }

        .success-icon {
          width: 80px;
          height: 80px;
          margin: 0 auto 20px;
          background: linear-gradient(135deg, #00FF7F, #00CED1);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 2.5rem;
        }

        .storyboard-footer {
          text-align: center;
          padding: 20px;
          color: #666;
          font-size: 0.8rem;
          display: flex;
          justify-content: center;
          gap: 10px;
        }

        .calibration-instructions {
          text-align: center;
          padding: 30px;
          color: #888;
        }

        .calibration-instructions button {
          margin-top: 15px;
          padding: 10px 20px;
          background: #333;
          border: 1px solid #555;
          color: #fff;
          border-radius: 5px;
          cursor: pointer;
        }
      `}</style>
    </div>
  );
};

export default ZamaIgnitionStoryboard;
