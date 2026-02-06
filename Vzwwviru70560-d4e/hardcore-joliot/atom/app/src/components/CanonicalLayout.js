/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       ██████╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗██╗ ██████╗ █████╗ ██╗
 *      ██╔════╝██╔══██╗████╗  ██║██╔═══██╗████╗  ██║██║██╔════╝██╔══██╗██║
 *      ██║     ███████║██╔██╗ ██║██║   ██║██╔██╗ ██║██║██║     ███████║██║
 *      ██║     ██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║██║██║     ██╔══██║██║
 *      ╚██████╗██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║██║╚██████╗██║  ██║███████╗
 *       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
 *
 *                          🏛️ LAYOUT CANONIQUE CHE·NU 🏛️
 *                    3 Hubs: LEFT (Navigation) | CENTER (Workspace) | RIGHT (Intelligence)
 *
 *   VÉRITÉS CANONIQUES RESPECTÉES:
 *   - 3 Hubs: LEFT/CENTER/RIGHT (ou BOTTOM sur mobile)
 *   - 10 Sphères FROZEN dans Hub LEFT
 *   - 6 Sections Bureau MAX (HARD LIMIT)
 *   - Nova Is System (toujours présent dans Hub RIGHT)
 *   - Onglets flexibles style Windows
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useCallback, createContext, useContext, lazy, Suspense } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { ChromeTabBar, BrowserTabContent } from './BrowserTab';

// Lazy load AgentConversation pour éviter les imports circulaires
const AgentConversation = lazy(() => import('./AgentConversation'));

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES CANONIQUES (FROZEN)
// ═══════════════════════════════════════════════════════════════════════════════

// Les 10 Sphères - FROZEN - NE JAMAIS MODIFIER
// Source de vérité: 01_PUBLIC_HARMONY.md + lib/point0.js
export const SPHERES = [
  { id: 'personal',      name: 'Personnel',       icon: '🏠', color: '#22C55E' },
  { id: 'team',          name: 'Mon Équipe',      icon: '🤝', color: '#10B981' },
  { id: 'business',      name: 'Entreprise',      icon: '💼', color: '#3B82F6' },
  { id: 'government',    name: 'Gouvernement',    icon: '🏛️', color: '#8B5CF6' },
  { id: 'studio',        name: 'Studio Créatif',  icon: '🎨', color: '#EC4899' },
  { id: 'community',     name: 'Communauté',      icon: '👥', color: '#F59E0B' },
  { id: 'social',        name: 'Social & Médias', icon: '📱', color: '#06B6D4' },
  { id: 'entertainment', name: 'Divertissement',  icon: '🎬', color: '#EF4444' },
  { id: 'erudition',     name: 'Érudition',       icon: '📚', color: '#8B5CF6' },
  { id: 'mapping',       name: 'AT-OM Mapping',   icon: '🗺️', color: '#D4AF37' },
];

// Les 6 Sections Bureau - HARD LIMIT - NE JAMAIS DÉPASSER
export const BUREAU_SECTIONS = [
  { id: 'quick_capture', name: 'Capture Rapide', icon: '📝' },
  { id: 'resume_workspace', name: 'Reprendre', icon: '▶️' },
  { id: 'threads', name: 'Threads', icon: '💬' },
  { id: 'data_files', name: 'Données', icon: '📁' },
  { id: 'active_agents', name: 'Agents Actifs', icon: '🤖' },
  { id: 'meetings', name: 'Réunions', icon: '📅' }
];

// Agents QuickConnect par défaut
export const DEFAULT_AGENTS = [
  { id: 'nova', name: 'Nova', icon: '🌟', role: 'system', color: '#D4AF37', description: 'Intelligence Système' },
  { id: 'aria', name: 'Aria', icon: '🎭', role: 'assistant', color: '#EC4899', description: 'Assistant Créatif' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTE DU LAYOUT CANONIQUE
// ═══════════════════════════════════════════════════════════════════════════════

const CanonicalLayoutContext = createContext(null);

export const useCanonicalLayout = () => {
  const context = useContext(CanonicalLayoutContext);
  if (!context) {
    throw new Error('useCanonicalLayout must be used within CanonicalLayoutProvider');
  }
  return context;
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: ONGLET WINDOWS STYLE
// ═══════════════════════════════════════════════════════════════════════════════

const WindowTab = ({ tab, isActive, onSelect, onClose, onDragStart, onDragOver, onDrop }) => {
  return (
    <div
      draggable
      onDragStart={(e) => onDragStart(e, tab.id)}
      onDragOver={onDragOver}
      onDrop={(e) => onDrop(e, tab.id)}
      onClick={() => onSelect(tab.id)}
      className={`flex items-center gap-2 px-3 py-2 rounded-t-lg cursor-pointer select-none
        transition-all duration-200 min-w-[120px] max-w-[200px] group
        ${isActive
          ? 'bg-gray-900 border-t border-l border-r border-yellow-500/30 text-white'
          : 'bg-gray-950 border-t border-l border-r border-gray-800 text-gray-500 hover:text-gray-300 hover:bg-gray-900/50'
        }`}
    >
      <span className="text-sm">{tab.icon}</span>
      <span className="text-xs truncate flex-1">{tab.name}</span>
      {tab.closable !== false && (
        <button
          onClick={(e) => { e.stopPropagation(); onClose(tab.id); }}
          className="opacity-0 group-hover:opacity-100 hover:text-red-400 text-xs transition-opacity"
        >
          ✕
        </button>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BARRE D'ONGLETS FLEXIBLE
// ═══════════════════════════════════════════════════════════════════════════════

const TabBar = ({ tabs, activeTabId, onSelectTab, onCloseTab, onReorderTabs }) => {
  const [draggedId, setDraggedId] = useState(null);

  const handleDragStart = (e, id) => {
    setDraggedId(id);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e, targetId) => {
    e.preventDefault();
    if (draggedId && draggedId !== targetId) {
      onReorderTabs(draggedId, targetId);
    }
    setDraggedId(null);
  };

  return (
    <div className="flex items-end gap-1 px-2 pt-2 bg-black border-b border-gray-800 overflow-x-auto">
      {tabs.map(tab => (
        <WindowTab
          key={tab.id}
          tab={tab}
          isActive={tab.id === activeTabId}
          onSelect={onSelectTab}
          onClose={onCloseTab}
          onDragStart={handleDragStart}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        />
      ))}
      <div className="flex-1" />
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HUB LEFT - NAVIGATION (10 Sphères)
// ═══════════════════════════════════════════════════════════════════════════════

const HubLeft = ({ activeSphere, onSelectSphere, collapsed, onToggleCollapse }) => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className={`flex flex-col bg-gray-950 border-r border-gray-800 transition-all duration-300 ${
      collapsed ? 'w-16' : 'w-56'
    }`}>
      {/* Header */}
      <div className="p-3 border-b border-gray-800 flex items-center justify-between">
        {!collapsed && (
          <span className="text-xs text-gray-500 uppercase tracking-wider">Sphères</span>
        )}
        <button
          onClick={onToggleCollapse}
          className="text-gray-500 hover:text-white transition-colors p-1"
        >
          {collapsed ? '→' : '←'}
        </button>
      </div>

      {/* Recherche Globale */}
      {!collapsed && (
        <div className="p-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Rechercher..."
            className="w-full px-3 py-2 bg-black border border-gray-800 rounded-lg text-sm text-white
              placeholder-gray-600 focus:outline-none focus:border-yellow-500/50"
          />
        </div>
      )}

      {/* Les 10 Sphères (FROZEN) */}
      <div className="flex-1 overflow-y-auto py-2">
        {SPHERES.map(sphere => (
          <button
            key={sphere.id}
            onClick={() => onSelectSphere(sphere.id)}
            className={`w-full flex items-center gap-3 px-3 py-2 transition-all ${
              activeSphere === sphere.id
                ? 'bg-gray-900 border-l-2'
                : 'hover:bg-gray-900/50 border-l-2 border-transparent'
            }`}
            style={{ borderLeftColor: activeSphere === sphere.id ? sphere.color : 'transparent' }}
            title={sphere.name}
          >
            <span className="text-xl">{sphere.icon}</span>
            {!collapsed && (
              <span className={`text-sm ${activeSphere === sphere.id ? 'text-white' : 'text-gray-400'}`}>
                {sphere.name}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Indicateur Point 0 — Ancrage fréquentiel */}
      <div className="p-3 border-t border-gray-800 text-center">
        <div className="text-xs text-emerald-500/60">
          {collapsed ? '●' : '● Point 0 — 444 Hz'}
        </div>
        <div className="text-xs text-gray-700 mt-0.5">
          {collapsed ? '' : '↕ 111 Hz ↔ 999 Hz'}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HUB RIGHT - INTELLIGENCE (Nova, Agents, QuickConnect)
// ═══════════════════════════════════════════════════════════════════════════════

const HubRight = ({ agents, onAddAgent, onSelectAgent, collapsed, onToggleCollapse, tokens }) => {
  const [showAddAgent, setShowAddAgent] = useState(false);

  return (
    <div className={`flex flex-col bg-gray-950 border-l border-gray-800 transition-all duration-300 ${
      collapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Header */}
      <div className="p-3 border-b border-gray-800 flex items-center justify-between">
        <button
          onClick={onToggleCollapse}
          className="text-gray-500 hover:text-white transition-colors p-1"
        >
          {collapsed ? '←' : '→'}
        </button>
        {!collapsed && (
          <span className="text-xs text-gray-500 uppercase tracking-wider">Intelligence</span>
        )}
      </div>

      {/* QuickConnect Agents */}
      <div className="flex-1 overflow-y-auto">
        {/* Agents Principaux */}
        <div className={`p-2 ${collapsed ? 'space-y-2' : 'space-y-1'}`}>
          {!collapsed && (
            <div className="text-xs text-gray-600 px-2 py-1">QuickConnect</div>
          )}

          {agents.map(agent => (
            <button
              key={agent.id}
              onClick={() => onSelectAgent(agent)}
              className={`w-full flex items-center gap-3 p-2 rounded-lg transition-all
                hover:bg-gray-900 group ${collapsed ? 'justify-center' : ''}`}
              title={agent.name}
            >
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center text-xl
                  ring-2 ring-offset-2 ring-offset-gray-950 transition-all group-hover:scale-110"
                style={{
                  backgroundColor: `${agent.color}20`,
                  ringColor: agent.color
                }}
              >
                {agent.icon}
              </div>
              {!collapsed && (
                <div className="flex-1 text-left">
                  <div className="text-sm text-white">{agent.name}</div>
                  <div className="text-xs text-gray-500">{agent.description}</div>
                </div>
              )}
            </button>
          ))}

          {/* Bouton Ajouter Agent */}
          <button
            onClick={() => setShowAddAgent(true)}
            className={`w-full flex items-center gap-3 p-2 rounded-lg transition-all
              border border-dashed border-gray-700 hover:border-yellow-500/50 hover:bg-gray-900/50
              ${collapsed ? 'justify-center' : ''}`}
            title="Ajouter un agent"
          >
            <div className="w-10 h-10 rounded-full flex items-center justify-center text-xl
              bg-gray-900 text-gray-500">
              +
            </div>
            {!collapsed && (
              <span className="text-sm text-gray-500">Ajouter agent</span>
            )}
          </button>
        </div>

        {/* Agents Actifs */}
        {!collapsed && (
          <div className="p-2 border-t border-gray-800">
            <div className="text-xs text-gray-600 px-2 py-1">Agents Actifs</div>
            <div className="text-center py-4 text-gray-700 text-sm">
              Aucun agent actif
            </div>
          </div>
        )}
      </div>

      {/* Tokens Status */}
      <div className="p-3 border-t border-gray-800">
        {collapsed ? (
          <div className="text-center text-yellow-500 text-sm">🪙</div>
        ) : (
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500">Tokens</span>
            <span className="text-sm text-yellow-500 font-mono">{tokens || 1000}</span>
          </div>
        )}
      </div>

      {/* Notifications */}
      {!collapsed && (
        <div className="p-3 border-t border-gray-800">
          <div className="text-xs text-gray-600 mb-2">Notifications</div>
          <div className="text-center py-2 text-gray-700 text-xs">
            Aucune notification
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HUB CENTER - WORKSPACE PRINCIPAL (Style Navigateur)
// ═══════════════════════════════════════════════════════════════════════════════

const HubCenter = ({ children, tabs, activeTabId, onSelectTab, onCloseTab, onReorderTabs, onNewTab }) => {
  const activeTab = tabs?.find(t => t.id === activeTabId);

  return (
    <div className="flex-1 flex flex-col bg-gray-900 min-w-0">
      {/* Barre d'onglets style navigateur */}
      {tabs && tabs.length > 0 && (
        <ChromeTabBar
          tabs={tabs}
          activeTabId={activeTabId}
          onSelectTab={onSelectTab}
          onCloseTab={onCloseTab}
          onReorderTabs={onReorderTabs}
          onNewTab={onNewTab}
        />
      )}

      {/* Contenu avec navigation intégrée */}
      <BrowserTabContent tab={activeTab || { id: 'default', name: 'Accueil', color: '#D4AF37' }}>
        {children}
      </BrowserTabContent>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: HEADER CANONIQUE
// ═══════════════════════════════════════════════════════════════════════════════

const CanonicalHeader = ({ user, onAuthClick }) => {
  return (
    <header className="h-12 bg-black border-b border-gray-800 flex items-center justify-between px-4">
      {/* Logo */}
      <Link to="/" className="flex items-center gap-2">
        <span className="text-xl">🔱</span>
        <span className="text-lg font-bold tracking-widest text-yellow-500">AT·OM</span>
      </Link>

      {/* Centre - Titre contextuel */}
      <div className="text-sm text-gray-500">
        CHE·NU V76 • Mode Souverain
      </div>

      {/* Droite - User */}
      <button
        onClick={onAuthClick}
        className="flex items-center gap-2 px-3 py-1 rounded-lg hover:bg-gray-900 transition-colors"
      >
        <span className="text-sm text-gray-400">{user?.email || 'Connexion'}</span>
        <div className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center">
          {user ? user.email?.[0]?.toUpperCase() : '👤'}
        </div>
      </button>
    </header>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MODAL SPHÈRE AVEC AGENT
// ═══════════════════════════════════════════════════════════════════════════════

export const SphereAgentModal = ({ agent, sphere, onClose, children }) => {
  if (!agent) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <div
        className="w-full max-w-3xl h-[85vh] bg-gray-900 rounded-2xl border overflow-hidden flex flex-col"
        style={{ borderColor: `${agent.color}50` }}
      >
        {/* Conversation Agent Intégrée */}
        <Suspense fallback={
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <span className="text-4xl mb-4 block animate-pulse">{agent.icon}</span>
              <p className="text-gray-400">Chargement de {agent.name}...</p>
            </div>
          </div>
        }>
          <AgentConversation initialAgentId={agent.id} onClose={onClose} />
        </Suspense>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// LAYOUT CANONIQUE PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

const CanonicalLayout = ({ children }) => {
  // États
  const [activeSphere, setActiveSphere] = useState('personal');
  const [leftCollapsed, setLeftCollapsed] = useState(false);
  const [rightCollapsed, setRightCollapsed] = useState(false);
  const [agents, setAgents] = useState(DEFAULT_AGENTS);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [showAuthPortal, setShowAuthPortal] = useState(false);
  const [tokens, setTokens] = useState(1000);

  // Onglets
  const [tabs, setTabs] = useState([
    { id: 'home', name: 'Accueil', icon: '🏠', closable: false }
  ]);
  const [activeTabId, setActiveTabId] = useState('home');

  // Handlers
  const handleSelectSphere = useCallback((sphereId) => {
    setActiveSphere(sphereId);
    const sphere = SPHERES.find(s => s.id === sphereId);

    // Ajouter ou activer l'onglet de la sphère
    const existingTab = tabs.find(t => t.id === `sphere-${sphereId}`);
    if (!existingTab) {
      setTabs(prev => [...prev, {
        id: `sphere-${sphereId}`,
        name: sphere.name,
        icon: sphere.icon,
        closable: true
      }]);
    }
    setActiveTabId(`sphere-${sphereId}`);
  }, [tabs]);

  const handleSelectAgent = useCallback((agent) => {
    setSelectedAgent(agent);
  }, []);

  const handleCloseTab = useCallback((tabId) => {
    setTabs(prev => prev.filter(t => t.id !== tabId));
    if (activeTabId === tabId) {
      setActiveTabId(tabs[0]?.id || 'home');
    }
  }, [activeTabId, tabs]);

  const handleReorderTabs = useCallback((draggedId, targetId) => {
    setTabs(prev => {
      const newTabs = [...prev];
      const draggedIndex = newTabs.findIndex(t => t.id === draggedId);
      const targetIndex = newTabs.findIndex(t => t.id === targetId);
      const [removed] = newTabs.splice(draggedIndex, 1);
      newTabs.splice(targetIndex, 0, removed);
      return newTabs;
    });
  }, []);

  const handleAddAgent = useCallback((agent) => {
    setAgents(prev => [...prev, agent]);
  }, []);

  // Créer un nouvel onglet
  const handleNewTab = useCallback(() => {
    const newTabId = `tab-${Date.now()}`;
    const newTab = {
      id: newTabId,
      name: 'Nouvel onglet',
      icon: '📄',
      color: '#6B7280',
      closable: true
    };
    setTabs(prev => [...prev, newTab]);
    setActiveTabId(newTabId);
  }, []);

  // Contexte
  const contextValue = {
    activeSphere,
    setActiveSphere: handleSelectSphere,
    agents,
    addAgent: handleAddAgent,
    tabs,
    activeTabId,
    openTab: (tab) => {
      const existing = tabs.find(t => t.id === tab.id);
      if (!existing) {
        setTabs(prev => [...prev, tab]);
      }
      setActiveTabId(tab.id);
    },
    closeTab: handleCloseTab,
    tokens,
    setTokens
  };

  return (
    <CanonicalLayoutContext.Provider value={contextValue}>
      <div className="h-screen flex flex-col bg-black text-white overflow-hidden">
        {/* Header */}
        <CanonicalHeader
          onAuthClick={() => setShowAuthPortal(true)}
        />

        {/* Corps principal: 3 Hubs */}
        <div className="flex-1 flex overflow-hidden">
          {/* HUB LEFT: Navigation */}
          <HubLeft
            activeSphere={activeSphere}
            onSelectSphere={handleSelectSphere}
            collapsed={leftCollapsed}
            onToggleCollapse={() => setLeftCollapsed(!leftCollapsed)}
          />

          {/* HUB CENTER: Workspace */}
          <HubCenter
            tabs={tabs}
            activeTabId={activeTabId}
            onSelectTab={setActiveTabId}
            onCloseTab={handleCloseTab}
            onReorderTabs={handleReorderTabs}
            onNewTab={handleNewTab}
          >
            {children}
          </HubCenter>

          {/* HUB RIGHT: Intelligence */}
          <HubRight
            agents={agents}
            onAddAgent={handleAddAgent}
            onSelectAgent={handleSelectAgent}
            collapsed={rightCollapsed}
            onToggleCollapse={() => setRightCollapsed(!rightCollapsed)}
            tokens={tokens}
          />
        </div>

        {/* Modal Agent (QuickConnect) */}
        {selectedAgent && (
          <SphereAgentModal
            agent={selectedAgent}
            sphere={activeSphere}
            onClose={() => setSelectedAgent(null)}
          />
        )}
      </div>
    </CanonicalLayoutContext.Provider>
  );
};

export default CanonicalLayout;
