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

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTE GLOBAL — Source unique (élimine la dépendance circulaire)
// ═══════════════════════════════════════════════════════════════════════════════

import { ATOMProvider, useATOMContext } from './contexts/ATOMContext';

// ═══════════════════════════════════════════════════════════════════════════════
// IMPORTS DES COMPOSANTS
// ═══════════════════════════════════════════════════════════════════════════════

import TorusBackground from './components/TorusBackground';

// Authentification
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AuthPortal, { UserProfileButton } from './components/AuthPortal';

// Error Handling
import { ErrorBoundary, ErrorProvider } from './components/ErrorBoundary';

// Route Guards
import ProtectedRoute, { SovereignRoute } from './components/ProtectedRoute';

// Navigation & Widgets
import { NavigationHistoryProvider, NavigationButtons } from './components/WindowControls';
import { MiniUsageWidget } from './components/UsageTracker';
import { Point0Badge, Point0StatusBar } from './components/Point0Badge';

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
import SetupWizardPage from './pages/SetupWizardPage';
import GridPage from './pages/GridPage';
import FounderPage from './pages/FounderPage';
import ProgresoPage from './pages/ProgresoPage';
import ProfilPage from './pages/ProfilPage';
import InscriptionPage from './pages/InscriptionPage';
import ArbreDeViePage from './pages/ArbreDeViePage';
import MapLumineusePage from './pages/MapLumineusePage';

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
  const { isAuthenticated, isSovereign } = useAuth();
  const [showMenu, setShowMenu] = useState(false);

  const menuItems = [
    { path: '/tableau-de-bord', label: 'Bureau', icon: '🏛️', auth: true },
    { path: '/profil', label: 'Profil', icon: '👤', auth: true },
    { path: '/agent', label: 'Agent Nova', icon: '🤖', auth: true },
    { path: '/carte-gaia', label: 'Carte Gaïa', icon: '🗺️', auth: false },
    { path: '/arbre-de-vie', label: 'Arbre de Vie', icon: '🌳', auth: false },
    { path: '/grid', label: 'Grille 144', icon: '🌍', auth: false },
    { path: '/cercle', label: 'Cercle', icon: '⭕', auth: true },
    ...(isSovereign() ? [{ path: '/admin', label: 'Admin', icon: '⚡', auth: true }] : []),
  ];

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

          <div className="flex items-center gap-3">
            {/* Point 0 — Ancrage fréquentiel */}
            <Point0Badge frequency={frequency} />

            {/* Navigation Back/Forward */}
            <NavigationButtons />

            {/* Widget Usage */}
            <MiniUsageWidget />

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

            {/* Menu Secondaire */}
            <div className="relative">
              <button
                onClick={() => setShowMenu(!showMenu)}
                className="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-all"
              >
                ☰
              </button>
              {showMenu && (
                <>
                  <div className="fixed inset-0 z-40" onClick={() => setShowMenu(false)} />
                  <div className="absolute right-0 top-full mt-2 w-48 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl z-50 overflow-hidden">
                    {menuItems
                      .filter(item => !item.auth || isAuthenticated)
                      .map(item => (
                        <Link
                          key={item.path}
                          to={item.path}
                          onClick={() => setShowMenu(false)}
                          className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                        >
                          <span>{item.icon}</span>
                          <span>{item.label}</span>
                        </Link>
                      ))}
                    {!isAuthenticated && (
                      <Link
                        to="/inscription"
                        onClick={() => setShowMenu(false)}
                        className="flex items-center gap-3 px-4 py-2.5 text-sm text-yellow-400 hover:bg-yellow-900/20 transition-colors border-t border-gray-800"
                      >
                        <span>✨</span>
                        <span>S'inscrire</span>
                      </Link>
                    )}
                  </div>
                </>
              )}
            </div>

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
  const { isArchitectMode, torusSpeed, frequency } = useATOMContext();
  const [showAuthPortal, setShowAuthPortal] = useState(false);
  const location = useLocation();

  // Nom de la page pour la StatusBar
  const pageNames = {
    '/': 'NEXUS',
    '/annales': 'ANNALES',
    '/lexique': 'LEXIQUE',
    '/flux': 'FLUX',
    '/forge': 'FORGE',
    '/besoins': 'BESOINS',
    '/gratitude': 'GRATITUDE',
    '/accreditation': 'PORTAIL',
  };

  return (
    <div className={`min-h-screen relative flex flex-col ${
      isArchitectMode ? 'bg-gradient-to-b from-white/10 to-black' : 'bg-black'
    }`}>
      {/* Fond Toroïdal */}
      <TorusBackground speed={torusSpeed} isArchitectMode={isArchitectMode} />

      {/* Header avec bouton Auth */}
      <Header onAuthClick={() => setShowAuthPortal(true)} />

      {/* Contenu Principal */}
      <main className="flex-1 pt-20 pb-24 px-4 relative z-10">
        <div className="max-w-4xl mx-auto">
          {children}
        </div>
      </main>

      {/* StatusBar Point 0 — Connexion permanente au cœur */}
      <Point0StatusBar
        frequency={frequency}
        pageName={pageNames[location.pathname] || ''}
      />

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
              <NavigationHistoryProvider>
              <Routes>
                {/* ═══ ROUTES PUBLIQUES (Aucune auth requise) ═══ */}
                <Route path="/entree" element={<EntreePage />} />
                <Route path="/inscription" element={<InscriptionPage />} />

                {/* ═══ ROUTES PROTÉGÉES (Auth requise) ═══ */}
                <Route path="/tableau-de-bord" element={
                  <ProtectedRoute><TableauDeBordPage /></ProtectedRoute>
                } />
                <Route path="/profil" element={
                  <ProtectedRoute><ProfilPage /></ProtectedRoute>
                } />
                <Route path="/agent/:agentId" element={
                  <ProtectedRoute><AgentConversation /></ProtectedRoute>
                } />
                <Route path="/agent" element={
                  <ProtectedRoute><AgentConversation initialAgentId="nova" /></ProtectedRoute>
                } />
                <Route path="/cercle" element={
                  <ProtectedRoute><CerclePage /></ProtectedRoute>
                } />
                <Route path="/founder" element={
                  <ProtectedRoute><FounderPage /></ProtectedRoute>
                } />

                {/* ═══ ROUTES SOUVERAIN (Admin uniquement) ═══ */}
                <Route path="/admin" element={
                  <SovereignRoute><AdminCockpit /></SovereignRoute>
                } />
                <Route path="/admin/setup" element={
                  <SovereignRoute><SetupWizardPage /></SovereignRoute>
                } />

                {/* ═══ ROUTES SEMI-PUBLIQUES (Visibles mais interaction auth) ═══ */}
                <Route path="/invitation" element={<InvitationPortal />} />
                <Route path="/grid" element={<GridPage />} />

                {/* Arbre de Vie — Séphiroth */}
                <Route path="/arbre-de-vie" element={<ArbreDeViePage />} />
                <Route path="/sephiroth" element={<ArbreDeViePage />} />

                {/* Carte du Potentiel Lumineux */}
                <Route path="/carte-gaia" element={<MapLumineusePage />} />
                <Route path="/potentiel-lumineux" element={<MapLumineusePage />} />

                {/* Landing Page Progreso 2026 - Publique */}
                <Route path="/progreso" element={<ProgresoPage />} />
                <Route path="/arche" element={<ProgresoPage />} />

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
              </NavigationHistoryProvider>
            </Router>
          </ATOMProvider>
        </AuthProvider>
      </ErrorProvider>
    </ErrorBoundary>
  );
};

export default App;
