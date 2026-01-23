/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ██████╗ ██████╗  ██████╗ ██╗    ██╗███████╗███████╗██████╗     ████████╗ █████╗ ██████╗
 *      ██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗
 *      ██████╔╝██████╔╝██║   ██║██║ █╗ ██║███████╗█████╗  ██████╔╝       ██║   ███████║██████╔╝
 *      ██╔══██╗██╔══██╗██║   ██║██║███╗██║╚════██║██╔══╝  ██╔══██╗       ██║   ██╔══██║██╔══██╗
 *      ██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████║███████╗██║  ██║       ██║   ██║  ██║██████╔╝
 *      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═════╝
 *
 *                          🌐 ONGLET NAVIGATEUR STYLE BROWSER 🌐
 *              Chaque onglet = Mini navigateur avec Back/Forward/Refresh/Options
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useCallback, useEffect } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BARRE D'ADRESSE / NAVIGATION (Style Chrome/Firefox)
// ═══════════════════════════════════════════════════════════════════════════════

const BrowserNavBar = ({
  canGoBack,
  canGoForward,
  onBack,
  onForward,
  onRefresh,
  onHome,
  currentPath,
  onNavigate,
  tabColor
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [inputValue, setInputValue] = useState(currentPath);

  useEffect(() => {
    setInputValue(currentPath);
  }, [currentPath]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onNavigate(inputValue);
    setIsEditing(false);
  };

  return (
    <div className="h-10 bg-gray-900 border-b border-gray-800 flex items-center gap-2 px-2">
      {/* Boutons Navigation */}
      <div className="flex items-center gap-1">
        {/* Back */}
        <button
          onClick={onBack}
          disabled={!canGoBack}
          className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
            canGoBack
              ? 'hover:bg-gray-700 text-gray-400 hover:text-white'
              : 'text-gray-700 cursor-not-allowed'
          }`}
          title="Retour"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M9 2L4 7l5 5" />
          </svg>
        </button>

        {/* Forward */}
        <button
          onClick={onForward}
          disabled={!canGoForward}
          className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
            canGoForward
              ? 'hover:bg-gray-700 text-gray-400 hover:text-white'
              : 'text-gray-700 cursor-not-allowed'
          }`}
          title="Avancer"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M5 2l5 5-5 5" />
          </svg>
        </button>

        {/* Refresh */}
        <button
          onClick={onRefresh}
          className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
          title="Actualiser"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M1 7a6 6 0 1011.5 2.5" />
            <path d="M12 3v4h-4" />
          </svg>
        </button>

        {/* Home */}
        <button
          onClick={onHome}
          className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
          title="Accueil"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M2 7l5-5 5 5" />
            <path d="M3 6v6h3V9h2v3h3V6" />
          </svg>
        </button>
      </div>

      {/* Barre d'adresse */}
      <form onSubmit={handleSubmit} className="flex-1">
        <div
          className={`flex items-center h-8 px-3 rounded-full transition-colors ${
            isEditing ? 'bg-gray-800 ring-1 ring-yellow-500/50' : 'bg-gray-800/50 hover:bg-gray-800'
          }`}
          style={{ borderLeft: `3px solid ${tabColor || '#D4AF37'}` }}
        >
          {/* Icône sécurité */}
          <span className="text-gray-600 mr-2 text-xs">🔒</span>

          {/* Input */}
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onFocus={() => setIsEditing(true)}
            onBlur={() => setIsEditing(false)}
            className="flex-1 bg-transparent text-sm text-gray-300 outline-none"
            placeholder="Naviguer..."
          />
        </div>
      </form>

      {/* Boutons droite */}
      <div className="flex items-center gap-1">
        {/* Bookmark */}
        <button
          className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-700 text-gray-500 hover:text-white transition-colors"
          title="Marquer"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M7 1l1.5 3 3.5.5-2.5 2.5.5 3.5L7 9l-3 1.5.5-3.5L2 4.5l3.5-.5z" />
          </svg>
        </button>

        {/* Menu Options */}
        <TabOptionsMenu tabColor={tabColor} />
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MENU OPTIONS DE L'ONGLET
// ═══════════════════════════════════════════════════════════════════════════════

const TabOptionsMenu = ({ tabColor }) => {
  const [isOpen, setIsOpen] = useState(false);

  const menuItems = [
    { id: 'new-tab', label: 'Nouvel onglet', icon: '➕', shortcut: 'Ctrl+T' },
    { id: 'duplicate', label: 'Dupliquer l\'onglet', icon: '📋' },
    { divider: true },
    { id: 'pin', label: 'Épingler l\'onglet', icon: '📌' },
    { id: 'mute', label: 'Couper le son', icon: '🔇' },
    { divider: true },
    { id: 'reload', label: 'Actualiser', icon: '🔄', shortcut: 'Ctrl+R' },
    { id: 'hard-reload', label: 'Actualiser sans cache', icon: '⚡', shortcut: 'Ctrl+Shift+R' },
    { divider: true },
    { id: 'close', label: 'Fermer l\'onglet', icon: '✕', shortcut: 'Ctrl+W' },
    { id: 'close-others', label: 'Fermer les autres', icon: '🗂️' }
  ];

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
          isOpen ? 'bg-gray-700 text-white' : 'hover:bg-gray-700 text-gray-500 hover:text-white'
        }`}
        title="Options"
      >
        <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor">
          <circle cx="7" cy="2" r="1.5" />
          <circle cx="7" cy="7" r="1.5" />
          <circle cx="7" cy="12" r="1.5" />
        </svg>
      </button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 top-full mt-1 w-56 bg-gray-900 border border-gray-700 rounded-lg shadow-xl z-50 py-1">
            {menuItems.map((item, index) => (
              item.divider ? (
                <div key={index} className="border-t border-gray-800 my-1" />
              ) : (
                <button
                  key={item.id}
                  onClick={() => setIsOpen(false)}
                  className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                >
                  <span className="w-5 text-center">{item.icon}</span>
                  <span className="flex-1 text-left">{item.label}</span>
                  {item.shortcut && (
                    <span className="text-xs text-gray-600">{item.shortcut}</span>
                  )}
                </button>
              )
            ))}
          </div>
        </>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: ONGLET INDIVIDUEL (Style Chrome)
// ═══════════════════════════════════════════════════════════════════════════════

export const ChromeTab = ({
  tab,
  isActive,
  onSelect,
  onClose,
  onDragStart,
  onDragOver,
  onDrop
}) => {
  return (
    <div
      draggable
      onDragStart={(e) => onDragStart?.(e, tab.id)}
      onDragOver={(e) => { e.preventDefault(); onDragOver?.(e); }}
      onDrop={(e) => onDrop?.(e, tab.id)}
      onClick={() => onSelect(tab.id)}
      className={`group relative flex items-center gap-2 px-3 h-9 rounded-t-lg cursor-pointer select-none
        transition-all duration-150 min-w-[100px] max-w-[200px]
        ${isActive
          ? 'bg-gray-900 text-white z-10'
          : 'bg-gray-950 text-gray-500 hover:text-gray-300 hover:bg-gray-900/50'
        }`}
      style={{
        borderTop: isActive ? `2px solid ${tab.color || '#D4AF37'}` : '2px solid transparent'
      }}
    >
      {/* Favicon */}
      <span className="text-sm flex-shrink-0">{tab.icon}</span>

      {/* Titre */}
      <span className="text-xs truncate flex-1">{tab.name}</span>

      {/* Loading indicator */}
      {tab.loading && (
        <span className="w-3 h-3 border-2 border-gray-600 border-t-yellow-500 rounded-full animate-spin" />
      )}

      {/* Close button */}
      {tab.closable !== false && (
        <button
          onClick={(e) => { e.stopPropagation(); onClose(tab.id); }}
          className="w-5 h-5 rounded-full flex items-center justify-center
            opacity-0 group-hover:opacity-100 hover:bg-gray-700 transition-all"
        >
          <svg width="8" height="8" viewBox="0 0 8 8" stroke="currentColor" strokeWidth="1.5">
            <line x1="1" y1="1" x2="7" y2="7" />
            <line x1="7" y1="1" x2="1" y2="7" />
          </svg>
        </button>
      )}

      {/* Courbes style Chrome */}
      {isActive && (
        <>
          <div className="absolute -left-2 bottom-0 w-2 h-2 bg-gray-900 rounded-br-lg" />
          <div className="absolute -right-2 bottom-0 w-2 h-2 bg-gray-900 rounded-bl-lg" />
        </>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BARRE D'ONGLETS (Style Chrome)
// ═══════════════════════════════════════════════════════════════════════════════

export const ChromeTabBar = ({
  tabs,
  activeTabId,
  onSelectTab,
  onCloseTab,
  onNewTab,
  onReorderTabs
}) => {
  const [draggedId, setDraggedId] = useState(null);

  const handleDragStart = (e, id) => {
    setDraggedId(id);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDrop = (e, targetId) => {
    e.preventDefault();
    if (draggedId && draggedId !== targetId) {
      onReorderTabs?.(draggedId, targetId);
    }
    setDraggedId(null);
  };

  return (
    <div className="h-10 bg-gray-950 flex items-end px-2 gap-0.5">
      {/* Onglets */}
      {tabs.map(tab => (
        <ChromeTab
          key={tab.id}
          tab={tab}
          isActive={tab.id === activeTabId}
          onSelect={onSelectTab}
          onClose={onCloseTab}
          onDragStart={handleDragStart}
          onDragOver={() => {}}
          onDrop={handleDrop}
        />
      ))}

      {/* Bouton Nouvel Onglet */}
      <button
        onClick={onNewTab}
        className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-gray-800 text-gray-500 hover:text-white transition-colors ml-1"
        title="Nouvel onglet (Ctrl+T)"
      >
        <svg width="14" height="14" viewBox="0 0 14 14" stroke="currentColor" strokeWidth="2">
          <line x1="7" y1="2" x2="7" y2="12" />
          <line x1="2" y1="7" x2="12" y2="7" />
        </svg>
      </button>

      {/* Espace flexible */}
      <div className="flex-1" />

      {/* Contrôles fenêtre (optionnel) */}
      <div className="flex items-center gap-1 mb-1">
        <button className="w-6 h-6 rounded hover:bg-gray-800 text-gray-600 hover:text-white transition-colors flex items-center justify-center">
          <svg width="10" height="1" viewBox="0 0 10 1"><rect width="10" height="1" fill="currentColor"/></svg>
        </button>
        <button className="w-6 h-6 rounded hover:bg-gray-800 text-gray-600 hover:text-white transition-colors flex items-center justify-center">
          <svg width="8" height="8" viewBox="0 0 8 8" stroke="currentColor" fill="none"><rect x="0.5" y="0.5" width="7" height="7"/></svg>
        </button>
        <button className="w-6 h-6 rounded hover:bg-red-600 text-gray-600 hover:text-white transition-colors flex items-center justify-center">
          <svg width="8" height="8" viewBox="0 0 8 8" stroke="currentColor" strokeWidth="1.5"><line x1="1" y1="1" x2="7" y2="7"/><line x1="7" y1="1" x2="1" y2="7"/></svg>
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CONTENU D'UN ONGLET BROWSER
// ═══════════════════════════════════════════════════════════════════════════════

export const BrowserTabContent = ({ tab, children }) => {
  // Historique local de l'onglet
  const [history, setHistory] = useState([tab.initialPath || '/']);
  const [historyIndex, setHistoryIndex] = useState(0);
  const [currentPath, setCurrentPath] = useState(tab.initialPath || '/');

  const canGoBack = historyIndex > 0;
  const canGoForward = historyIndex < history.length - 1;

  const handleBack = useCallback(() => {
    if (canGoBack) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setCurrentPath(history[newIndex]);
    }
  }, [canGoBack, historyIndex, history]);

  const handleForward = useCallback(() => {
    if (canGoForward) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setCurrentPath(history[newIndex]);
    }
  }, [canGoForward, historyIndex, history]);

  const handleNavigate = useCallback((path) => {
    // Couper l'historique forward et ajouter le nouveau chemin
    const newHistory = [...history.slice(0, historyIndex + 1), path];
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
    setCurrentPath(path);
  }, [history, historyIndex]);

  const handleRefresh = useCallback(() => {
    // Simuler un refresh
    console.log('Refresh:', currentPath);
  }, [currentPath]);

  const handleHome = useCallback(() => {
    handleNavigate('/');
  }, [handleNavigate]);

  return (
    <div className="flex flex-col h-full bg-gray-900">
      {/* Barre de navigation du tab */}
      <BrowserNavBar
        canGoBack={canGoBack}
        canGoForward={canGoForward}
        onBack={handleBack}
        onForward={handleForward}
        onRefresh={handleRefresh}
        onHome={handleHome}
        currentPath={currentPath}
        onNavigate={handleNavigate}
        tabColor={tab.color}
      />

      {/* Contenu */}
      <div className="flex-1 overflow-auto">
        {children}
      </div>

      {/* Barre de statut (optionnel) */}
      <div className="h-6 bg-gray-950 border-t border-gray-800 flex items-center justify-between px-3 text-xs text-gray-600">
        <span>{currentPath}</span>
        <span>CHE·NU V76</span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  BrowserNavBar,
  TabOptionsMenu,
  ChromeTab,
  ChromeTabBar,
  BrowserTabContent
};
