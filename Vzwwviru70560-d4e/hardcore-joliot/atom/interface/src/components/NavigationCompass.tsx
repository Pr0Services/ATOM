/**
 * NAVIGATION COMPASS - Persistent Navigation Helper
 * ==================================================
 *
 * Boussole de navigation persistante affichant:
 * - Où je suis (contexte actuel)
 * - Ce que je peux faire maintenant
 * - Prochaine étape recommandée
 *
 * Objectif: Réduire le coût d'orientation et le temps de recherche
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAtomStore } from '@/stores/atom.store';
import { getRouteLabel, getRouteDescription } from '@/services/navigation-labels.service';
import { COLORS, TYPOGRAPHY, TOUCH } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface NavigationContext {
  currentPage: string;
  currentDescription: string;
  possibleActions: Action[];
  recommendedNext: Action | null;
}

interface Action {
  id: string;
  label: string;
  description: string;
  path: string;
  icon: string;
  priority: 'primary' | 'secondary' | 'tertiary';
}

// =============================================================================
// ROUTE CONTEXT CONFIGURATION
// =============================================================================

const ROUTE_ACTIONS: Record<string, { actions: Omit<Action, 'priority'>[]; recommended: string }> = {
  '/': {
    actions: [
      { id: 'explore', label: 'Explorer l\'Essaim', description: 'Découvrir les 350 agents', path: '/essaim', icon: '🐝' },
      { id: 'dashboard', label: 'Tableau de bord', description: 'Vue d\'ensemble', path: '/dashboard', icon: '📊' },
      { id: 'register', label: 'Créer un compte', description: 'Sauvegarder vos progrès', path: '/register', icon: '✨' },
    ],
    recommended: 'explore',
  },
  '/essaim': {
    actions: [
      { id: 'home', label: 'Retour accueil', description: 'Page principale', path: '/', icon: '🏠' },
      { id: 'workspace', label: 'Créer un espace', description: 'Assembler votre équipe', path: '/workspace/new', icon: '🛠️' },
      { id: 'dashboard', label: 'Tableau de bord', description: 'Voir les métriques', path: '/dashboard', icon: '📊' },
    ],
    recommended: 'workspace',
  },
  '/dashboard': {
    actions: [
      { id: 'essaim', label: 'Voir l\'Essaim', description: 'Explorer les agents', path: '/essaim', icon: '🐝' },
      { id: 'genie', label: 'Éducation', description: 'Module Génie', path: '/genie', icon: '🎓' },
      { id: 'sante', label: 'Santé', description: 'Module Guérison', path: '/sante', icon: '💚' },
    ],
    recommended: 'essaim',
  },
  '/landing': {
    actions: [
      { id: 'enter', label: 'Entrer', description: 'Accéder à la plateforme', path: '/', icon: '🚀' },
      { id: 'register', label: 'S\'inscrire', description: 'Créer un compte', path: '/register', icon: '✨' },
    ],
    recommended: 'enter',
  },
  '/register': {
    actions: [
      { id: 'home', label: 'Retour', description: 'Page principale', path: '/', icon: '🏠' },
      { id: 'explore', label: 'Explorer d\'abord', description: 'Essayer sans compte', path: '/essaim', icon: '🐝' },
    ],
    recommended: 'explore',
  },
};

// Default actions for unknown routes
const DEFAULT_ACTIONS: { actions: Omit<Action, 'priority'>[]; recommended: string } = {
  actions: [
    { id: 'home', label: 'Accueil', description: 'Page principale', path: '/', icon: '🏠' },
    { id: 'essaim', label: 'Essaim', description: 'Explorer les agents', path: '/essaim', icon: '🐝' },
    { id: 'dashboard', label: 'Tableau de bord', description: 'Vue d\'ensemble', path: '/dashboard', icon: '📊' },
  ],
  recommended: 'home',
};

// =============================================================================
// NAVIGATION COMPASS COMPONENT
// =============================================================================

interface NavigationCompassProps {
  position?: 'bottom-right' | 'bottom-left' | 'top-right';
  defaultExpanded?: boolean;
}

export function NavigationCompass({
  position = 'bottom-right',
  defaultExpanded = false,
}: NavigationCompassProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const language = useAtomStore((state) => state.ui.language);
  const experienceMode = useAtomStore((state) => state.ui.experienceMode);

  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [isMinimized, setIsMinimized] = useState(false);

  // Get navigation context for current route
  const context = useMemo<NavigationContext>(() => {
    const path = location.pathname;
    const routeConfig = ROUTE_ACTIONS[path] || DEFAULT_ACTIONS;

    // Add priorities to actions
    const actionsWithPriority: Action[] = routeConfig.actions.map((action, index) => ({
      ...action,
      priority: action.id === routeConfig.recommended
        ? 'primary'
        : index < 2
          ? 'secondary'
          : 'tertiary',
    }));

    const recommended = actionsWithPriority.find(a => a.id === routeConfig.recommended) || null;

    return {
      currentPage: getRouteLabel(path, language),
      currentDescription: getRouteDescription(path, language),
      possibleActions: actionsWithPriority,
      recommendedNext: recommended,
    };
  }, [location.pathname, language]);

  // Don't show in expert mode unless expanded
  if (experienceMode === 'expert' && !isExpanded) {
    return (
      <button
        onClick={() => setIsExpanded(true)}
        style={{
          position: 'fixed',
          [position.includes('bottom') ? 'bottom' : 'top']: '100px',
          [position.includes('right') ? 'right' : 'left']: '20px',
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          border: `1px solid ${COLORS.gold}40`,
          color: COLORS.gold,
          fontSize: '20px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 900,
        }}
        title="Ouvrir la boussole"
      >
        🧭
      </button>
    );
  }

  if (isMinimized) {
    return (
      <button
        onClick={() => setIsMinimized(false)}
        style={{
          position: 'fixed',
          [position.includes('bottom') ? 'bottom' : 'top']: '100px',
          [position.includes('right') ? 'right' : 'left']: '20px',
          padding: '12px 16px',
          borderRadius: '24px',
          backgroundColor: 'rgba(0, 0, 0, 0.9)',
          border: `1px solid ${COLORS.gold}40`,
          color: '#fff',
          fontSize: '14px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          zIndex: 900,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
        }}
      >
        <span>🧭</span>
        <span style={{ color: COLORS.gold }}>{context.currentPage}</span>
      </button>
    );
  }

  const positionStyles = {
    'bottom-right': { bottom: '100px', right: '20px' },
    'bottom-left': { bottom: '100px', left: '20px' },
    'top-right': { top: '80px', right: '20px' },
  };

  return (
    <div
      style={{
        position: 'fixed',
        ...positionStyles[position],
        width: '280px',
        backgroundColor: 'rgba(0, 0, 0, 0.95)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: '16px',
        overflow: 'hidden',
        zIndex: 900,
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
        fontFamily: TYPOGRAPHY.fontFamily.system,
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: '12px 16px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '16px' }}>🧭</span>
          <span
            style={{
              color: COLORS.gold,
              fontSize: '11px',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              letterSpacing: '0.1em',
            }}
          >
            BOUSSOLE
          </span>
        </div>
        <button
          onClick={() => setIsMinimized(true)}
          style={{
            padding: '4px 8px',
            backgroundColor: 'transparent',
            border: 'none',
            color: 'rgba(255, 255, 255, 0.4)',
            cursor: 'pointer',
            fontSize: '12px',
          }}
        >
          Réduire
        </button>
      </div>

      {/* Current Location */}
      <div style={{ padding: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
        <div
          style={{
            color: 'rgba(255, 255, 255, 0.5)',
            fontSize: '10px',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            marginBottom: '4px',
          }}
        >
          Vous êtes ici
        </div>
        <div style={{ color: '#fff', fontSize: '16px', fontWeight: 500 }}>
          {context.currentPage}
        </div>
        {context.currentDescription && (
          <div style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '13px', marginTop: '4px' }}>
            {context.currentDescription}
          </div>
        )}
      </div>

      {/* Recommended Action */}
      {context.recommendedNext && (
        <div style={{ padding: '12px 16px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
          <div
            style={{
              color: COLORS.gold,
              fontSize: '10px',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              marginBottom: '8px',
            }}
          >
            Prochaine étape recommandée
          </div>
          <button
            onClick={() => navigate(context.recommendedNext!.path)}
            style={{
              width: '100%',
              padding: '12px',
              backgroundColor: `${COLORS.gold}15`,
              border: `1px solid ${COLORS.gold}40`,
              borderRadius: '8px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              textAlign: 'left',
            }}
          >
            <span style={{ fontSize: '20px' }}>{context.recommendedNext.icon}</span>
            <div>
              <div style={{ color: COLORS.gold, fontWeight: 500, fontSize: '14px' }}>
                {context.recommendedNext.label}
              </div>
              <div style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '12px' }}>
                {context.recommendedNext.description}
              </div>
            </div>
            <span style={{ color: COLORS.gold, marginLeft: 'auto' }}>→</span>
          </button>
        </div>
      )}

      {/* Other Actions */}
      <div style={{ padding: '12px 16px' }}>
        <div
          style={{
            color: 'rgba(255, 255, 255, 0.4)',
            fontSize: '10px',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            marginBottom: '8px',
          }}
        >
          Autres actions possibles
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {context.possibleActions
            .filter(a => a.id !== context.recommendedNext?.id)
            .slice(0, 3)
            .map((action) => (
              <button
                key={action.id}
                onClick={() => navigate(action.path)}
                style={{
                  padding: '10px 12px',
                  backgroundColor: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  textAlign: 'left',
                }}
              >
                <span style={{ fontSize: '16px' }}>{action.icon}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ color: '#fff', fontSize: '13px' }}>{action.label}</div>
                </div>
                <span style={{ color: 'rgba(255, 255, 255, 0.3)', fontSize: '12px' }}>→</span>
              </button>
            ))}
        </div>
      </div>

      {/* Keyboard shortcut hint */}
      <div
        style={{
          padding: '8px 16px',
          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <span style={{ color: 'rgba(255, 255, 255, 0.3)', fontSize: '11px' }}>
          Cmd+K pour plus d'actions
        </span>
      </div>
    </div>
  );
}

export default NavigationCompass;
