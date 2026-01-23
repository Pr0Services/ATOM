/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ██╗    ██╗██╗███╗   ██╗██████╗  ██████╗ ██╗    ██╗███████╗
 *      ██║    ██║██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║██╔════╝
 *      ██║ █╗ ██║██║██╔██╗ ██║██║  ██║██║   ██║██║ █╗ ██║███████╗
 *      ██║███╗██║██║██║╚██╗██║██║  ██║██║   ██║██║███╗██║╚════██║
 *      ╚███╔███╔╝██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝███████║
 *       ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝
 *
 *                    🖥️ CONTRÔLES WINDOWS STYLE 🖥️
 *              Navigation Back/Forward + Menu Options Système
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback, createContext, useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTE DE NAVIGATION HISTORIQUE
// ═══════════════════════════════════════════════════════════════════════════════

const NavigationHistoryContext = createContext(null);

export const NavigationHistoryProvider = ({ children }) => {
  const location = useLocation();
  const [history, setHistory] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [isNavigating, setIsNavigating] = useState(false);

  // Ajouter à l'historique quand la location change
  useEffect(() => {
    if (isNavigating) {
      setIsNavigating(false);
      return;
    }

    setHistory(prev => {
      // Si on navigue après avoir fait "back", on coupe l'historique forward
      const newHistory = prev.slice(0, currentIndex + 1);
      return [...newHistory, location.pathname];
    });
    setCurrentIndex(prev => prev + 1);
  }, [location.pathname]);

  const canGoBack = currentIndex > 0;
  const canGoForward = currentIndex < history.length - 1;

  const value = {
    history,
    currentIndex,
    canGoBack,
    canGoForward,
    setIsNavigating
  };

  return (
    <NavigationHistoryContext.Provider value={value}>
      {children}
    </NavigationHistoryContext.Provider>
  );
};

export const useNavigationHistory = () => {
  const context = useContext(NavigationHistoryContext);
  if (!context) {
    return { canGoBack: false, canGoForward: false, history: [], currentIndex: 0 };
  }
  return context;
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BOUTONS NAVIGATION BACK/FORWARD
// ═══════════════════════════════════════════════════════════════════════════════

export const NavigationButtons = () => {
  const navigate = useNavigate();
  const { canGoBack, canGoForward, setIsNavigating } = useNavigationHistory();

  const handleBack = useCallback(() => {
    if (canGoBack) {
      setIsNavigating?.(true);
      navigate(-1);
    }
  }, [canGoBack, navigate, setIsNavigating]);

  const handleForward = useCallback(() => {
    if (canGoForward) {
      setIsNavigating?.(true);
      navigate(1);
    }
  }, [canGoForward, navigate, setIsNavigating]);

  return (
    <div className="flex items-center gap-1">
      {/* Bouton Back */}
      <button
        onClick={handleBack}
        disabled={!canGoBack}
        className={`w-8 h-8 rounded flex items-center justify-center transition-colors ${
          canGoBack
            ? 'hover:bg-gray-800 text-gray-400 hover:text-white'
            : 'text-gray-700 cursor-not-allowed'
        }`}
        title="Retour (Alt+←)"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M11 2L5 8l6 6" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {/* Bouton Forward */}
      <button
        onClick={handleForward}
        disabled={!canGoForward}
        className={`w-8 h-8 rounded flex items-center justify-center transition-colors ${
          canGoForward
            ? 'hover:bg-gray-800 text-gray-400 hover:text-white'
            : 'text-gray-700 cursor-not-allowed'
        }`}
        title="Avancer (Alt+→)"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M5 2l6 6-6 6" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MENU OPTIONS SYSTÈME (Style Windows)
// ═══════════════════════════════════════════════════════════════════════════════

export const SystemOptionsMenu = ({ isOpen, onClose, onNavigate }) => {
  const navigate = useNavigate();

  const menuSections = [
    {
      title: 'Navigation',
      items: [
        { id: 'home', label: 'Accueil', icon: '🏠', shortcut: 'Alt+H', action: () => navigate('/') },
        { id: 'dashboard', label: 'Tableau de Bord', icon: '📊', shortcut: 'Alt+D', action: () => navigate('/tableau-de-bord') },
        { id: 'entree', label: 'Page d\'Entrée', icon: '🚪', action: () => navigate('/entree') }
      ]
    },
    {
      title: 'Compte',
      items: [
        { id: 'profile', label: 'Mon Profil', icon: '👤', action: () => {} },
        { id: 'settings', label: 'Paramètres', icon: '⚙️', shortcut: 'Alt+S', action: () => navigate('/forge') },
        { id: 'logout', label: 'Déconnexion', icon: '🚪', action: () => {
          localStorage.removeItem('atom_charte_accepted');
          localStorage.removeItem('atom_onboarding_complete');
          navigate('/entree');
        }}
      ]
    },
    {
      title: 'Données',
      items: [
        { id: 'export', label: 'Exporter mes données', icon: '📤', action: () => {} },
        { id: 'reset', label: 'Réinitialiser l\'onboarding', icon: '🔄', action: () => {
          localStorage.removeItem('atom_onboarding_complete');
          localStorage.removeItem('atom_onboarding_data');
          navigate('/entree');
        }},
        { id: 'clear', label: 'Effacer le cache', icon: '🗑️', action: () => {
          localStorage.clear();
          window.location.reload();
        }}
      ]
    },
    {
      title: 'Aide',
      items: [
        { id: 'help', label: 'Aide', icon: '❓', shortcut: 'F1', action: () => {} },
        { id: 'about', label: 'À propos', icon: 'ℹ️', action: () => {} },
        { id: 'version', label: 'Version CHE·NU V76', icon: '📋', disabled: true }
      ]
    }
  ];

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-40"
        onClick={onClose}
      />

      {/* Menu */}
      <div className="fixed top-12 right-4 z-50 w-64 bg-gray-900 border border-gray-700 rounded-lg shadow-xl overflow-hidden">
        {menuSections.map((section, sectionIndex) => (
          <div key={section.title}>
            {sectionIndex > 0 && <div className="border-t border-gray-800" />}
            <div className="px-3 py-2">
              <div className="text-xs text-gray-600 uppercase tracking-wider mb-1">
                {section.title}
              </div>
              {section.items.map(item => (
                <button
                  key={item.id}
                  onClick={() => {
                    if (!item.disabled) {
                      item.action();
                      onClose();
                    }
                  }}
                  disabled={item.disabled}
                  className={`w-full flex items-center gap-3 px-2 py-2 rounded text-sm text-left transition-colors ${
                    item.disabled
                      ? 'text-gray-600 cursor-default'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  }`}
                >
                  <span className="w-5 text-center">{item.icon}</span>
                  <span className="flex-1">{item.label}</span>
                  {item.shortcut && (
                    <span className="text-xs text-gray-600">{item.shortcut}</span>
                  )}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BOUTON MENU OPTIONS
// ═══════════════════════════════════════════════════════════════════════════════

export const SystemOptionsButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-8 h-8 rounded flex items-center justify-center transition-colors ${
          isOpen
            ? 'bg-gray-700 text-white'
            : 'hover:bg-gray-800 text-gray-400 hover:text-white'
        }`}
        title="Options (Alt+O)"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <circle cx="8" cy="3" r="1.5" />
          <circle cx="8" cy="8" r="1.5" />
          <circle cx="8" cy="13" r="1.5" />
        </svg>
      </button>

      <SystemOptionsMenu isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BARRE DE TITRE WINDOWS STYLE
// ═══════════════════════════════════════════════════════════════════════════════

export const WindowTitleBar = ({ title, showNavigation = true }) => {
  const location = useLocation();

  // Générer le breadcrumb
  const getBreadcrumb = () => {
    const paths = location.pathname.split('/').filter(Boolean);
    if (paths.length === 0) return 'Accueil';
    return paths.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' › ');
  };

  return (
    <div className="h-10 bg-gray-950 border-b border-gray-800 flex items-center justify-between px-2">
      {/* Gauche: Navigation + Breadcrumb */}
      <div className="flex items-center gap-2">
        {showNavigation && <NavigationButtons />}
        <div className="h-4 w-px bg-gray-800 mx-1" />
        <span className="text-sm text-gray-500">{getBreadcrumb()}</span>
      </div>

      {/* Centre: Titre (optionnel) */}
      {title && (
        <div className="text-sm text-gray-400">{title}</div>
      )}

      {/* Droite: Options */}
      <div className="flex items-center gap-1">
        <SystemOptionsButton />
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CONTRÔLES DE FENÊTRE (Minimize, Maximize, Close)
// ═══════════════════════════════════════════════════════════════════════════════

export const WindowFrameControls = ({ onMinimize, onMaximize, onClose }) => {
  return (
    <div className="flex items-center">
      {/* Minimize */}
      <button
        onClick={onMinimize}
        className="w-12 h-8 flex items-center justify-center hover:bg-gray-700 transition-colors"
        title="Réduire"
      >
        <svg width="10" height="1" viewBox="0 0 10 1" fill="currentColor">
          <rect width="10" height="1" fill="currentColor" />
        </svg>
      </button>

      {/* Maximize */}
      <button
        onClick={onMaximize}
        className="w-12 h-8 flex items-center justify-center hover:bg-gray-700 transition-colors"
        title="Agrandir"
      >
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor">
          <rect x="0.5" y="0.5" width="9" height="9" strokeWidth="1" />
        </svg>
      </button>

      {/* Close */}
      <button
        onClick={onClose}
        className="w-12 h-8 flex items-center justify-center hover:bg-red-600 transition-colors"
        title="Fermer"
      >
        <svg width="10" height="10" viewBox="0 0 10 10" stroke="currentColor" strokeWidth="1.5">
          <line x1="1" y1="1" x2="9" y2="9" />
          <line x1="9" y1="1" x2="1" y2="9" />
        </svg>
      </button>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK: RACCOURCIS CLAVIER
// ═══════════════════════════════════════════════════════════════════════════════

export const useKeyboardShortcuts = () => {
  const navigate = useNavigate();
  const { canGoBack, canGoForward, setIsNavigating } = useNavigationHistory();

  useEffect(() => {
    const handleKeyDown = (e) => {
      // Alt + Flèche Gauche = Back
      if (e.altKey && e.key === 'ArrowLeft' && canGoBack) {
        e.preventDefault();
        setIsNavigating?.(true);
        navigate(-1);
      }

      // Alt + Flèche Droite = Forward
      if (e.altKey && e.key === 'ArrowRight' && canGoForward) {
        e.preventDefault();
        setIsNavigating?.(true);
        navigate(1);
      }

      // Alt + H = Home
      if (e.altKey && e.key === 'h') {
        e.preventDefault();
        navigate('/');
      }

      // Alt + D = Dashboard
      if (e.altKey && e.key === 'd') {
        e.preventDefault();
        navigate('/tableau-de-bord');
      }

      // Alt + S = Settings
      if (e.altKey && e.key === 's') {
        e.preventDefault();
        navigate('/forge');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [navigate, canGoBack, canGoForward, setIsNavigating]);
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BARRE DE STATUT (Bottom)
// ═══════════════════════════════════════════════════════════════════════════════

export const StatusBar = ({ status, tokens, frequency }) => {
  return (
    <div className="h-6 bg-gray-950 border-t border-gray-800 flex items-center justify-between px-3 text-xs">
      {/* Gauche: Statut */}
      <div className="flex items-center gap-4">
        <span className="text-gray-500">{status || 'Prêt'}</span>
      </div>

      {/* Droite: Infos système */}
      <div className="flex items-center gap-4">
        {tokens !== undefined && (
          <span className="text-yellow-500">🪙 {tokens}</span>
        )}
        {frequency && (
          <span className="text-gray-500">{frequency} Hz</span>
        )}
        <span className="text-gray-600">CHE·NU V76</span>
      </div>
    </div>
  );
};

export default {
  NavigationHistoryProvider,
  NavigationButtons,
  SystemOptionsMenu,
  SystemOptionsButton,
  WindowTitleBar,
  WindowFrameControls,
  StatusBar,
  useNavigationHistory,
  useKeyboardShortcuts
};
