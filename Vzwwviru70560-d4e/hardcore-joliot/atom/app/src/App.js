/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *       █████╗ ████████╗    ██████╗ ███╗   ███╗     █████╗ ██████╗ ██████╗ 
 *      ██╔══██╗╚══██╔══╝   ██╔═══██╗████╗ ████║    ██╔══██╗██╔══██╗██╔══██╗
 *      ███████║   ██║      ██║   ██║██╔████╔██║    ███████║██████╔╝██████╔╝
 *      ██╔══██║   ██║      ██║   ██║██║╚██╔╝██║    ██╔══██║██╔═══╝ ██╔═══╝ 
 *      ██║  ██║   ██║   ██╗╚██████╔╝██║ ╚═╝ ██║    ██║  ██║██║     ██║     
 *      ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝╚═╝     ╚═╝     
 *                                                                                          
 *                          🔱 L'ARCHE DES RÉSONANCES UNIVERSELLES 🔱
 *                                   APPLICATION PRINCIPALE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *   Navigation par les 4 Éléments (Points Cardinaux):
 *   
 *   /         (NEXUS)   → Le Centre - Page d'accueil avec l'Arche
 *   /annales  (TERRE)   → Le Sud - Historique des mots testés
 *   /lexique  (AIR)     → L'Est - Description des Oracles et Fréquences
 *   /flux     (EAU)     → L'Ouest - Visualisation des connexions
 *   /forge    (FEU)     → Le Nord - Configuration et paramètres
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';

// ═══════════════════════════════════════════════════════════════════════════════
// IMPORTS DES COMPOSANTS
// ═══════════════════════════════════════════════════════════════════════════════

import TorusBackground from './components/TorusBackground';
import { useArithmos } from './hooks/useArithmos';
import { useGratitude } from './hooks/useGratitude';

// Authentification
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AuthPortal, { UserProfileButton } from './components/AuthPortal';

// Error Handling
import { ErrorBoundary, ErrorProvider } from './components/ErrorBoundary';

// Pages
import NexusPage from './pages/NexusPage';
import AnnalesPage from './pages/AnnalesPage';
import LexiquePage from './pages/LexiquePage';
import FluxPage from './pages/FluxPage';
import ForgePage from './pages/ForgePage';
import BesoinsPage from './pages/BesoinsPage';
import GratitudePage from './pages/GratitudePage';
import AccreditationPage from './pages/AccreditationPage';
import EntreePage from './pages/EntreePage';
import TableauDeBordPage from './pages/TableauDeBordPage';
import AdminCockpit from './components/AdminCockpit';
import AgentConversation from './components/AgentConversation';
import InvitationPortal from './components/InvitationPortal';
import CerclePage from './pages/CerclePage';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES GLOBALES
// ═══════════════════════════════════════════════════════════════════════════════

export const PHI = 1.6180339887498949;
export const HEARTBEAT = 444;
export const SOURCE = 999;
export const ARCHITECT_NAME = "JONATHAN RODRIGUE";
export const ARCHITECT_ORACLE = 17;

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTE GLOBAL AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

export const ATOMContext = createContext(null);

export const ATOMProvider = ({ children }) => {
  // États globaux
  const [frequency, setFrequency] = useState(HEARTBEAT);
  const [isArchitectMode, setIsArchitectMode] = useState(false);
  const [isGratitudeMode, setIsGratitudeMode] = useState(false);
  const [annales, setAnnales] = useState([]);
  const [torusSpeed, setTorusSpeed] = useState(1);
  
  // Configuration
  const [config, setConfig] = useState({
    animationSpeed: 1,
    frequencyOffset: 0,
    soundEnabled: true,
    particleCount: 50,
    colorScheme: 'gold'
  });

  // Ajouter une entrée aux Annales
  const addToAnnales = (entry) => {
    const newEntry = {
      ...entry,
      id: Date.now(),
      timestamp: new Date().toISOString()
    };
    setAnnales(prev => [newEntry, ...prev].slice(0, 1000)); // Max 1000 entrées
    
    // Sauvegarder en localStorage
    try {
      const stored = JSON.parse(localStorage.getItem('atom_annales') || '[]');
      localStorage.setItem('atom_annales', JSON.stringify([newEntry, ...stored].slice(0, 1000)));
    } catch (e) {
      console.warn('Erreur localStorage:', e);
    }
  };

  // Charger les Annales au démarrage
  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem('atom_annales') || '[]');
      setAnnales(stored);
    } catch (e) {
      console.warn('Erreur chargement Annales:', e);
    }
  }, []);

  // Activer le Mode Architecte
  const activateArchitectMode = () => {
    setIsArchitectMode(true);
    setFrequency(SOURCE);
    setTorusSpeed(PHI * 2);
  };

  // Désactiver le Mode Architecte
  const deactivateArchitectMode = () => {
    setIsArchitectMode(false);
    setFrequency(HEARTBEAT);
    setTorusSpeed(1);
  };

  const value = {
    // États
    frequency,
    setFrequency,
    isArchitectMode,
    setIsArchitectMode,
    isGratitudeMode,
    setIsGratitudeMode,
    annales,
    setAnnales,
    torusSpeed,
    setTorusSpeed,
    config,
    setConfig,
    
    // Actions
    addToAnnales,
    activateArchitectMode,
    deactivateArchitectMode,
    
    // Constantes
    PHI,
    HEARTBEAT,
    SOURCE,
    ARCHITECT_NAME,
    ARCHITECT_ORACLE
  };

  return (
    <ATOMContext.Provider value={value}>
      {children}
    </ATOMContext.Provider>
  );
};

// Hook pour utiliser le contexte
export const useATOMContext = () => {
  const context = useContext(ATOMContext);
  if (!context) {
    throw new Error('useATOMContext must be used within ATOMProvider');
  }
  return context;
};

// ═══════════════════════════════════════════════════════════════════════════════
// NAVIGATION PAR LES 4 ÉLÉMENTS
// ═══════════════════════════════════════════════════════════════════════════════

const Navigation = () => {
  const location = useLocation();
  const { isArchitectMode, frequency } = useATOMContext();
  
  const navItems = [
    { path: '/', name: 'NEXUS', element: '🔱', direction: 'Centre', color: '#D4AF37' },
    { path: '/annales', name: 'ANNALES', element: '🌍', direction: 'Terre (Sud)', color: '#8B4513' },
    { path: '/lexique', name: 'LEXIQUE', element: '💨', direction: 'Air (Est)', color: '#87CEEB' },
    { path: '/besoins', name: 'BESOINS', element: '📊', direction: 'Civilisation', color: '#22C55E' },
    { path: '/accreditation', name: 'PORTAIL', element: '🏛️', direction: 'Partenaires', color: '#8B5CF6' },
    { path: '/gratitude', name: 'MERCI', element: '💌', direction: 'Gratitude', color: '#EC4899' },
    { path: '/flux', name: 'FLUX', element: '🌊', direction: 'Eau (Ouest)', color: '#4169E1' },
    { path: '/forge', name: 'FORGE', element: '🔥', direction: 'Feu (Nord)', color: '#FF4500' }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-t border-yellow-900/50">
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex justify-around items-center h-16">
          {navItems.map(item => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex flex-col items-center transition-all duration-300 ${
                  isActive ? 'scale-110' : 'opacity-60 hover:opacity-100'
                }`}
                title={item.direction}
              >
                <span 
                  className="text-2xl"
                  style={{ 
                    filter: isActive ? `drop-shadow(0 0 10px ${item.color})` : 'none'
                  }}
                >
                  {item.element}
                </span>
                <span 
                  className={`text-xs mt-1 ${isActive ? 'text-yellow-400' : 'text-gray-500'}`}
                  style={{ color: isActive ? item.color : undefined }}
                >
                  {item.name}
                </span>
              </Link>
            );
          })}
        </div>
      </div>
      
      {/* Indicateur de fréquence */}
      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-full">
        <div 
          className={`px-3 py-1 rounded-t-lg text-xs ${
            isArchitectMode ? 'bg-white text-black' : 'bg-yellow-900/80 text-yellow-400'
          }`}
        >
          {frequency} Hz {isArchitectMode && '★'}
        </div>
      </div>
    </nav>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// HEADER
// ═══════════════════════════════════════════════════════════════════════════════

const Header = ({ onAuthClick }) => {
  const { isArchitectMode, isGratitudeMode, frequency } = useATOMContext();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-yellow-900/50">
      <div className="max-w-4xl mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2">
            <span className={`text-2xl ${isArchitectMode ? 'animate-pulse' : ''}`}>
              🔱
            </span>
            <div>
              <h1 className={`text-xl font-bold tracking-widest ${
                isArchitectMode ? 'text-white' : 'text-yellow-500'
              }`}>
                AT·OM
              </h1>
              <p className="text-xs text-gray-500">L'Arche des Résonances</p>
            </div>
          </Link>

          <div className="flex items-center gap-4">
            {/* Indicateur de Mode */}
            {isGratitudeMode && (
              <span className="text-green-400 text-sm animate-pulse">
                ☯ GRATITUDE
              </span>
            )}
            {isArchitectMode && (
              <span className="text-white text-sm animate-pulse">
                ★ MODE DIVIN
              </span>
            )}

            {/* Bouton Authentification */}
            <UserProfileButton onClick={onAuthClick} />
          </div>
        </div>
      </div>
    </header>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYOUT PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const Layout = ({ children }) => {
  const { isArchitectMode, torusSpeed } = useATOMContext();
  const [showAuthPortal, setShowAuthPortal] = useState(false);

  return (
    <div className={`min-h-screen relative ${
      isArchitectMode ? 'bg-gradient-to-b from-white/10 to-black' : 'bg-black'
    }`}>
      {/* Fond Toroïdal */}
      <TorusBackground speed={torusSpeed} isArchitectMode={isArchitectMode} />

      {/* Header avec bouton Auth */}
      <Header onAuthClick={() => setShowAuthPortal(true)} />

      {/* Contenu Principal */}
      <main className="pt-20 pb-24 px-4 relative z-10">
        <div className="max-w-4xl mx-auto">
          {children}
        </div>
      </main>

      {/* Navigation */}
      <Navigation />

      {/* Portail d'Authentification */}
      {showAuthPortal && (
        <AuthPortal onClose={() => setShowAuthPortal(false)} />
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// APPLICATION PRINCIPALE
// ═══════════════════════════════════════════════════════════════════════════════

const App = () => {
  return (
    <ErrorBoundary>
      <ErrorProvider>
        <AuthProvider>
          <ATOMProvider>
            <Router>
              <Routes>
                {/* Routes Canoniques Publiques (sans Layout Souverain) */}
                <Route path="/entree" element={<EntreePage />} />
                <Route path="/tableau-de-bord" element={<TableauDeBordPage />} />

                {/* Route Admin Cockpit (accès restreint) */}
                <Route path="/admin" element={<AdminCockpit />} />

                {/* Route Agent Conversation */}
                <Route path="/agent/:agentId" element={<AgentConversation />} />
                <Route path="/agent" element={<AgentConversation initialAgentId="nova" />} />

                {/* Routes Membres Fondateurs */}
                <Route path="/invitation" element={<InvitationPortal />} />
                <Route path="/cercle" element={<CerclePage />} />

                {/* Routes Souveraines (avec Layout complet) */}
                <Route path="/*" element={
                  <Layout>
                    <Routes>
                      <Route path="/" element={<NexusPage />} />
                      <Route path="/annales" element={<AnnalesPage />} />
                      <Route path="/lexique" element={<LexiquePage />} />
                      <Route path="/flux" element={<FluxPage />} />
                      <Route path="/forge" element={<ForgePage />} />
                      <Route path="/besoins" element={<BesoinsPage />} />
                      <Route path="/gratitude" element={<GratitudePage />} />
                      <Route path="/accreditation" element={<AccreditationPage />} />
                    </Routes>
                  </Layout>
                } />
              </Routes>
            </Router>
          </ATOMProvider>
        </AuthProvider>
      </ErrorProvider>
    </ErrorBoundary>
  );
};

export default App;
