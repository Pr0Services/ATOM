/**
 * AT·OM ENGINE — Moteur Parallèle Autonome
 * 
 * AT·OM = Instrument / Piano
 * CHE·NU = Orchestre / Cité
 * 
 * SÉPARATION OFFICIELLE:
 * - AT·OM: Exploration, Recherche, Fréquences, Correspondances
 * - CHE·NU: Application gouvernée, Interface publique
 * 
 * LAYOUT AT·OM ENGINE:
 * ┌─────────────────────────────────────────────────────────────────┐
 * │ [🔮Logo]  [Action Bar / Services]           [🔔] [Octave: 5]   │
 * ├──┬───────────────────────────────────────────────────────────┬──┤
 * │S │                                                           │T │
 * │P │              W O R K S P A C E                            │A │
 * │H │                                                           │B │
 * │E │  ┌─────────┐    [🌍 Map View Mobile]                      │S │
 * │R │  │ NAV HUB │                                              │  │
 * │E │  │  ~25%   │    🎹 PIANO VISUALIZER                       │  │
 * │S │  └─────────┘    📊 FREQUENCY GRAPH                        │  │
 * │  │                 🔗 CORRESPONDANCES                        │  │
 * ├──┴───────────────────────────────────────────────────────────┴──┤
 * │ [💬NOVA] [🤖Agents] [🔮Spheres]          [Communication Tabs]   │
 * └─────────────────────────────────────────────────────────────────┘
 * 
 * OCTAVE SWITCHER (9 Octaves):
 * 1. Physique    | 4. Cognitive    | 7. Vibratoire
 * 2. Biologique  | 5. Symbolique   | 8. Historique
 * 3. Sociale     | 6. Mathématique | 9. Métastructure
 * 
 * RÈGLE: Les SPHÈRES restent constantes. Seule l'INTERPRÉTATION change.
 */

import React, { useState, useCallback } from 'react';
import './styles/AtomEngine.css';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

type SphereId = 'personal' | 'business' | 'government' | 'creative' | 
                'community' | 'social' | 'entertainment' | 'my_team' | 
                'scholar' | 'atom';

type OctaveLevel = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;

interface Octave {
  level: OctaveLevel;
  name: string;
  name_fr: string;
  description: string;
  color: string;
}

interface WorkspaceTab {
  id: string;
  type: 'welcome' | 'piano' | 'frequency' | 'correspondence' | 'timeline' | 'graph' | 'agent-chat';
  title: string;
  icon: string;
  isClosable?: boolean;
}

interface CommTab {
  id: string;
  type: 'nova' | 'agent' | 'sphere';
  title: string;
  icon: string;
}

// ═══════════════════════════════════════════════════════════════════════════════
// DATA — 9 OCTAVES
// ═══════════════════════════════════════════════════════════════════════════════

const OCTAVES: Octave[] = [
  { level: 1, name: 'Physical', name_fr: 'Physique', description: 'Matière, énergie, forces', color: '#E74C3C' },
  { level: 2, name: 'Biological', name_fr: 'Biologique', description: 'Vie, organismes, évolution', color: '#27AE60' },
  { level: 3, name: 'Social', name_fr: 'Sociale', description: 'Sociétés, cultures, civilisations', color: '#3498DB' },
  { level: 4, name: 'Cognitive', name_fr: 'Cognitive', description: 'Pensée, conscience, intelligence', color: '#9B59B6' },
  { level: 5, name: 'Symbolic', name_fr: 'Symbolique', description: 'Symboles, mythes, archétypes', color: '#F39C12' },
  { level: 6, name: 'Mathematical', name_fr: 'Mathématique', description: 'Nombres, structures, patterns', color: '#1ABC9C' },
  { level: 7, name: 'Vibrational', name_fr: 'Vibratoire', description: 'Fréquences, résonances, harmoniques', color: '#E91E63' },
  { level: 8, name: 'Historical', name_fr: 'Historique', description: 'Temps, événements, cycles', color: '#795548' },
  { level: 9, name: 'Metastructure', name_fr: 'Métastructure', description: 'Patterns de patterns, lois universelles', color: '#607D8B' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// DATA — 10 SPHERES (CONSTANTES dans toutes les octaves)
// ═══════════════════════════════════════════════════════════════════════════════

const SPHERES = [
  { id: 'personal' as SphereId, name: 'Personnel', icon: '👤', color: '#4A90D9' },
  { id: 'business' as SphereId, name: 'Entreprise', icon: '💼', color: '#D4AF37' },
  { id: 'government' as SphereId, name: 'Gouvernement', icon: '🏛️', color: '#8B4513' },
  { id: 'creative' as SphereId, name: 'Création', icon: '🎨', color: '#9B59B6' },
  { id: 'community' as SphereId, name: 'Communauté', icon: '🤝', color: '#27AE60' },
  { id: 'social' as SphereId, name: 'Social', icon: '📱', color: '#3498DB' },
  { id: 'entertainment' as SphereId, name: 'Divertissement', icon: '🎮', color: '#F39C12' },
  { id: 'my_team' as SphereId, name: 'Mon Équipe', icon: '👥', color: '#E74C3C' },
  { id: 'scholar' as SphereId, name: 'Académique', icon: '📚', color: '#1ABC9C' },
  { id: 'atom' as SphereId, name: 'AT·OM Core', icon: '🔮', color: '#8E44AD' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// PIANO KEYS DATA (12 notes × 9 octaves)
// ═══════════════════════════════════════════════════════════════════════════════

const NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const BASE_FREQUENCY = 16.35; // C0

const calculateFrequency = (note: number, octave: number): number => {
  return BASE_FREQUENCY * Math.pow(2, (octave + note / 12));
};

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN AT·OM ENGINE COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

export default function AtomEngine() {
  // State
  const [currentOctave, setCurrentOctave] = useState<OctaveLevel>(5);
  const [activeSphere, setActiveSphere] = useState<SphereId | null>(null);
  const [navHubOpen, setNavHubOpen] = useState(false);
  const [activeNote, setActiveNote] = useState<number | null>(null);
  
  const [workspaceTabs, setWorkspaceTabs] = useState<WorkspaceTab[]>([
    { id: 'welcome', type: 'welcome', title: 'AT·OM', icon: '🔮', isClosable: false },
    { id: 'piano', type: 'piano', title: 'Piano', icon: '🎹', isClosable: false },
  ]);
  const [activeWorkspaceTab, setActiveWorkspaceTab] = useState('welcome');
  
  const [commTabs, setCommTabs] = useState<CommTab[]>([
    { id: 'nova', type: 'nova', title: 'NOVA', icon: '🌟' },
  ]);
  const [activeCommTab, setActiveCommTab] = useState<string | null>(null);

  // Current octave data
  const octaveData = OCTAVES.find(o => o.level === currentOctave)!;

  // Handlers
  const handleSphereClick = useCallback((sphereId: SphereId) => {
    if (activeSphere === sphereId && navHubOpen) {
      setNavHubOpen(false);
    } else {
      setActiveSphere(sphereId);
      setNavHubOpen(true);
    }
  }, [activeSphere, navHubOpen]);

  const handleNotePlay = useCallback((noteIndex: number) => {
    setActiveNote(noteIndex);
    const freq = calculateFrequency(noteIndex, currentOctave);
    console.log(`Note: ${NOTES[noteIndex % 12]}${currentOctave}, Frequency: ${freq.toFixed(2)} Hz`);
    
    // Auto-clear after 300ms
    setTimeout(() => setActiveNote(null), 300);
  }, [currentOctave]);

  const openWorkspaceTab = useCallback((type: WorkspaceTab['type'], title: string, icon: string) => {
    const id = `${type}-${Date.now()}`;
    const existing = workspaceTabs.find(t => t.type === type);
    if (existing) {
      setActiveWorkspaceTab(existing.id);
    } else {
      setWorkspaceTabs(prev => [...prev, { id, type, title, icon, isClosable: true }]);
      setActiveWorkspaceTab(id);
    }
  }, [workspaceTabs]);

  const closeWorkspaceTab = useCallback((tabId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const tab = workspaceTabs.find(t => t.id === tabId);
    if (tab?.isClosable === false) return;
    
    const newTabs = workspaceTabs.filter(t => t.id !== tabId);
    setWorkspaceTabs(newTabs);
    if (activeWorkspaceTab === tabId) {
      setActiveWorkspaceTab(newTabs[newTabs.length - 1]?.id || 'welcome');
    }
  }, [workspaceTabs, activeWorkspaceTab]);

  const currentSphere = SPHERES.find(s => s.id === activeSphere);
  const activeWsTab = workspaceTabs.find(t => t.id === activeWorkspaceTab);

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDER
  // ═══════════════════════════════════════════════════════════════════════════════

  return (
    <div className="atom-engine" style={{ '--octave-color': octaveData.color } as React.CSSProperties}>
      
      {/* ═══ TOP BAR ═══ */}
      <header className="atom-topbar">
        <div className="topbar-left">
          <div className="atom-logo">🔮</div>
          <span className="atom-title">AT·OM ENGINE</span>
        </div>
        
        <div className="topbar-center">
          <button className="action-btn" onClick={() => openWorkspaceTab('piano', 'Piano', '🎹')}>🎹 Piano</button>
          <button className="action-btn" onClick={() => openWorkspaceTab('frequency', 'Fréquences', '📊')}>📊 Fréquences</button>
          <button className="action-btn" onClick={() => openWorkspaceTab('correspondence', 'Correspondances', '🔗')}>🔗 Correspondances</button>
          <button className="action-btn" onClick={() => openWorkspaceTab('timeline', 'Timeline', '📜')}>📜 Timeline</button>
        </div>
        
        <div className="topbar-right">
          <button className="notification-btn">🔔</button>
          
          {/* OCTAVE SWITCHER */}
          <div className="octave-switcher">
            <button 
              className="octave-btn prev"
              onClick={() => setCurrentOctave(prev => Math.max(1, prev - 1) as OctaveLevel)}
              disabled={currentOctave === 1}
            >
              ◀
            </button>
            <div className="octave-display" style={{ borderColor: octaveData.color }}>
              <span className="octave-level">O{currentOctave}</span>
              <span className="octave-name">{octaveData.name_fr}</span>
            </div>
            <button 
              className="octave-btn next"
              onClick={() => setCurrentOctave(prev => Math.min(9, prev + 1) as OctaveLevel)}
              disabled={currentOctave === 9}
            >
              ▶
            </button>
          </div>
        </div>
      </header>

      {/* ═══ MIDDLE SECTION ═══ */}
      <div className="atom-middle">
        
        {/* ─── SPHERE BAR (left) ─── */}
        <aside className="sphere-bar">
          {SPHERES.map(sphere => (
            <button
              key={sphere.id}
              className={`sphere-btn ${activeSphere === sphere.id ? 'active' : ''}`}
              style={{ '--sphere-color': sphere.color } as React.CSSProperties}
              onClick={() => handleSphereClick(sphere.id)}
              title={`${sphere.name} (Octave ${currentOctave}: ${octaveData.name_fr})`}
            >
              {sphere.icon}
            </button>
          ))}
        </aside>

        {/* ─── WORKSPACE CONTAINER ─── */}
        <div className="workspace-container">
          
          {/* Nav Hub (~25% on sphere click) */}
          {navHubOpen && currentSphere && (
            <aside className="nav-hub">
              <div className="nav-hub-header">
                <span>{currentSphere.icon} {currentSphere.name}</span>
                <span className="nav-octave-badge" style={{ background: octaveData.color }}>
                  O{currentOctave}
                </span>
                <button className="close-btn" onClick={() => setNavHubOpen(false)}>×</button>
              </div>
              <div className="nav-hub-content">
                <div className="octave-interpretation">
                  <h4>Interprétation {octaveData.name_fr}</h4>
                  <p>{octaveData.description}</p>
                </div>
                <div className="nav-section">
                  <h4>📊 Correspondances</h4>
                  <ul>
                    <li>🔢 Valeur numérique: {currentSphere.name.length}</li>
                    <li>🎵 Fréquence base: {calculateFrequency(0, currentOctave).toFixed(2)} Hz</li>
                    <li>🌈 Couleur: {currentSphere.color}</li>
                  </ul>
                </div>
                <div className="nav-section">
                  <h4>📜 Références historiques</h4>
                  <ul>
                    <li>📖 Civilisations anciennes</li>
                    <li>🔮 Systèmes symboliques</li>
                    <li>📐 Structures mathématiques</li>
                  </ul>
                </div>
              </div>
            </aside>
          )}

          {/* Main Workspace */}
          <main className="workspace">
            
            {/* WELCOME VIEW */}
            {activeWsTab?.type === 'welcome' && (
              <div className="workspace-welcome">
                <div className="atom-symbol">🔮</div>
                <h1>AT·OM ENGINE</h1>
                <p className="subtitle">Moteur d'Exploration Vibratoire & Historique</p>
                
                <div className="octave-info">
                  <span className="label">Octave Active:</span>
                  <span className="value" style={{ color: octaveData.color }}>
                    {currentOctave}. {octaveData.name_fr}
                  </span>
                </div>
                
                <div className="quick-actions">
                  <button onClick={() => openWorkspaceTab('piano', 'Piano', '🎹')}>🎹 Piano</button>
                  <button onClick={() => openWorkspaceTab('frequency', 'Fréquences', '📊')}>📊 Fréquences</button>
                  <button onClick={() => openWorkspaceTab('timeline', 'Timeline Historique', '📜')}>📜 Timeline</button>
                </div>

                {/* Mini Map View */}
                <div className="mini-map">
                  <div className="map-label">🌍 Map View</div>
                  <div className="map-spheres">
                    {SPHERES.map(s => (
                      <div 
                        key={s.id} 
                        className="map-sphere"
                        style={{ background: s.color }}
                        title={s.name}
                      >
                        {s.icon}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* PIANO VIEW */}
            {activeWsTab?.type === 'piano' && (
              <div className="workspace-piano">
                <div className="piano-header">
                  <h2>🎹 Piano — Octave {currentOctave} ({octaveData.name_fr})</h2>
                  <p>Exploration des fréquences et correspondances</p>
                </div>
                
                <div className="piano-keyboard">
                  {[...Array(12)].map((_, i) => {
                    const isBlack = [1, 3, 6, 8, 10].includes(i);
                    const freq = calculateFrequency(i, currentOctave);
                    return (
                      <button
                        key={i}
                        className={`piano-key ${isBlack ? 'black' : 'white'} ${activeNote === i ? 'active' : ''}`}
                        onClick={() => handleNotePlay(i)}
                        title={`${NOTES[i]}${currentOctave} — ${freq.toFixed(2)} Hz`}
                      >
                        <span className="note-name">{NOTES[i]}</span>
                        <span className="note-freq">{freq.toFixed(1)}</span>
                      </button>
                    );
                  })}
                </div>

                <div className="frequency-display">
                  {activeNote !== null && (
                    <>
                      <div className="freq-note">{NOTES[activeNote % 12]}{currentOctave}</div>
                      <div className="freq-value">{calculateFrequency(activeNote, currentOctave).toFixed(2)} Hz</div>
                    </>
                  )}
                </div>

                <div className="octave-scale">
                  {OCTAVES.map(o => (
                    <button
                      key={o.level}
                      className={`octave-scale-btn ${o.level === currentOctave ? 'active' : ''}`}
                      style={{ '--oct-color': o.color } as React.CSSProperties}
                      onClick={() => setCurrentOctave(o.level)}
                    >
                      {o.level}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* FREQUENCY VIEW */}
            {activeWsTab?.type === 'frequency' && (
              <div className="workspace-frequency">
                <h2>📊 Fréquences — Octave {currentOctave}</h2>
                <div className="freq-grid">
                  {NOTES.map((note, i) => {
                    const freq = calculateFrequency(i, currentOctave);
                    return (
                      <div key={i} className="freq-card">
                        <div className="freq-note">{note}{currentOctave}</div>
                        <div className="freq-bar" style={{ height: `${(freq / 1000) * 100}%`, background: octaveData.color }} />
                        <div className="freq-value">{freq.toFixed(2)} Hz</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* CORRESPONDENCE VIEW */}
            {activeWsTab?.type === 'correspondence' && (
              <div className="workspace-correspondence">
                <h2>🔗 Correspondances — Octave {currentOctave} ({octaveData.name_fr})</h2>
                <div className="corr-grid">
                  {SPHERES.map(sphere => (
                    <div key={sphere.id} className="corr-card">
                      <div className="corr-icon">{sphere.icon}</div>
                      <div className="corr-name">{sphere.name}</div>
                      <div className="corr-interpretation">
                        Interprétation {octaveData.name_fr}
                      </div>
                      <div className="corr-value" style={{ color: octaveData.color }}>
                        {calculateFrequency(SPHERES.indexOf(sphere), currentOctave).toFixed(2)} Hz
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TIMELINE VIEW */}
            {activeWsTab?.type === 'timeline' && (
              <div className="workspace-timeline">
                <h2>📜 Timeline Historique — Octave {currentOctave}</h2>
                <div className="timeline-axis">
                  <div className="timeline-era">Antiquité</div>
                  <div className="timeline-era">Moyen-Âge</div>
                  <div className="timeline-era">Renaissance</div>
                  <div className="timeline-era">Moderne</div>
                  <div className="timeline-era">Contemporain</div>
                </div>
                <p className="timeline-note">
                  Timeline historique selon l'interprétation {octaveData.name_fr}
                </p>
              </div>
            )}

          </main>
        </div>

        {/* ─── WORKSPACE TABS BAR (right) ─── */}
        <aside className="tabs-bar">
          {workspaceTabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-btn ${activeWorkspaceTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveWorkspaceTab(tab.id)}
              title={tab.title}
            >
              <span className="tab-icon">{tab.icon}</span>
              {tab.isClosable && (
                <span className="tab-close" onClick={(e) => closeWorkspaceTab(tab.id, e)}>×</span>
              )}
            </button>
          ))}
          <button 
            className="tab-btn add" 
            onClick={() => openWorkspaceTab('graph', 'Nouveau', '📈')}
            title="Nouveau"
          >
            +
          </button>
        </aside>
      </div>

      {/* ═══ BOTTOM BAR (Communication) ═══ */}
      <footer className="atom-bottombar">
        <div className="bottombar-left">
          <button 
            className={`quick-connect ${activeCommTab === 'nova' ? 'active' : ''}`}
            onClick={() => setActiveCommTab(activeCommTab === 'nova' ? null : 'nova')}
          >
            💬 NOVA
          </button>
          <button className="quick-connect">🤖 Agents</button>
          <button className="quick-connect">🔮 Spheres</button>
        </div>
        
        <div className="bottombar-center">
          {commTabs.map(tab => (
            <button
              key={tab.id}
              className={`comm-tab ${activeCommTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveCommTab(tab.id)}
            >
              {tab.icon} {tab.title}
            </button>
          ))}
        </div>
        
        <div className="bottombar-right">
          <span className="status">● Connecté</span>
          <span className="version">AT·OM v1.0</span>
        </div>
      </footer>

      {/* Communication Panel (slides up when active) */}
      {activeCommTab && (
        <div className="comm-panel">
          <div className="comm-panel-header">
            <span>💬 NOVA — AT·OM Assistant</span>
            <button onClick={() => setActiveCommTab(null)}>×</button>
          </div>
          <div className="comm-panel-messages">
            <div className="message agent">
              <span className="avatar">🌟</span>
              <div className="bubble">
                Bienvenue dans AT·OM Engine! Je peux vous aider à explorer les fréquences, 
                correspondances et structures historiques. Actuellement en Octave {currentOctave} ({octaveData.name_fr}).
              </div>
            </div>
          </div>
          <div className="comm-panel-input">
            <input type="text" placeholder="Explorez les correspondances..." />
            <button>➤</button>
          </div>
        </div>
      )}
    </div>
  );
}
