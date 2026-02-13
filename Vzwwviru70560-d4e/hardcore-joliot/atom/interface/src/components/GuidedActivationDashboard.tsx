/**
 * GUIDED ACTIVATION DASHBOARD
 * ============================
 *
 * Composant "premier écran" qui guide l'utilisateur vers ses 3 actions prioritaires.
 * Objectif audit: "Dashboard d'accueil guidé (3 actions principales)"
 *
 * Principes:
 * - Réduction cognitive: 3 actions max, pas plus
 * - Orientation valeur: chaque action montre le bénéfice attendu
 * - Progression visible: statut et temps estimé
 * - Personnalisation: s'adapte au profil utilisateur
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAtomStore } from '@/stores/atom.store';
import { COLORS, TYPOGRAPHY } from '@/styles/tokens';
import { funnelTracker } from '@/services/funnel-tracking.service';

// =============================================================================
// TYPES
// =============================================================================

interface ActivationAction {
  id: string;
  title: string;
  description: string;
  benefit: string;
  estimatedTime: string;
  icon: string;
  route: string;
  category: 'discover' | 'configure' | 'create' | 'connect';
  priority: number;
  isCompleted: boolean;
  completionKey: string; // localStorage key to track completion
}

interface UserProfile {
  type: 'citoyen' | 'collaborateur' | 'investisseur' | 'nouveau';
  interests: string[];
  completedActions: string[];
}

// =============================================================================
// ACTIVATION ACTIONS CATALOG
// =============================================================================

const ALL_ACTIONS: ActivationAction[] = [
  // Discovery actions
  {
    id: 'explore-agents',
    title: 'Explorer les Agents',
    description: 'Découvrez les 350+ assistants IA spécialisés',
    benefit: 'Trouvez l\'agent parfait pour vos besoins',
    estimatedTime: '2 min',
    icon: '🤖',
    route: '/essaim',
    category: 'discover',
    priority: 1,
    isCompleted: false,
    completionKey: 'atom_action_explore_agents',
  },
  {
    id: 'understand-spheres',
    title: 'Comprendre les Sphères',
    description: 'Les 9 domaines thématiques d\'AT·OM',
    benefit: 'Organisez vos activités par contexte',
    estimatedTime: '3 min',
    icon: '🌐',
    route: '/dashboard',
    category: 'discover',
    priority: 2,
    isCompleted: false,
    completionKey: 'atom_action_understand_spheres',
  },
  {
    id: 'try-demo',
    title: 'Essayer la Démo',
    description: 'Testez un agent sans créer de compte',
    benefit: 'Voyez la valeur en 60 secondes',
    estimatedTime: '1 min',
    icon: '▶️',
    route: '/landing#demo',
    category: 'discover',
    priority: 1,
    isCompleted: false,
    completionKey: 'atom_action_try_demo',
  },

  // Configuration actions
  {
    id: 'setup-profile',
    title: 'Configurer mon Profil',
    description: 'Personnalisez votre expérience AT·OM',
    benefit: 'Recevez des recommandations pertinentes',
    estimatedTime: '3 min',
    icon: '⚙️',
    route: '/settings',
    category: 'configure',
    priority: 2,
    isCompleted: false,
    completionKey: 'atom_action_setup_profile',
  },
  {
    id: 'choose-spheres',
    title: 'Choisir mes Sphères',
    description: 'Sélectionnez vos domaines d\'intérêt',
    benefit: 'Interface adaptée à vos priorités',
    estimatedTime: '2 min',
    icon: '🎯',
    route: '/dashboard?onboard=spheres',
    category: 'configure',
    priority: 1,
    isCompleted: false,
    completionKey: 'atom_action_choose_spheres',
  },

  // Creation actions
  {
    id: 'first-workspace',
    title: 'Créer mon premier Espace',
    description: 'Assemblez une équipe d\'agents',
    benefit: 'Automatisez vos tâches récurrentes',
    estimatedTime: '5 min',
    icon: '🏗️',
    route: '/workspace/new',
    category: 'create',
    priority: 3,
    isCompleted: false,
    completionKey: 'atom_action_first_workspace',
  },
  {
    id: 'ask-first-question',
    title: 'Poser ma première question',
    description: 'Interagissez avec un agent',
    benefit: 'Obtenez une réponse intelligente',
    estimatedTime: '1 min',
    icon: '💬',
    route: '/essaim?action=ask',
    category: 'create',
    priority: 1,
    isCompleted: false,
    completionKey: 'atom_action_first_question',
  },

  // Connection actions
  {
    id: 'join-governance',
    title: 'Rejoindre la Gouvernance',
    description: 'Participez aux décisions collectives',
    benefit: 'Votre voix compte dans l\'évolution',
    estimatedTime: '3 min',
    icon: '🗳️',
    route: '/sovereign',
    category: 'connect',
    priority: 3,
    isCompleted: false,
    completionKey: 'atom_action_join_governance',
  },
];

// =============================================================================
// ACTION SELECTION LOGIC
// =============================================================================

function getRecommendedActions(
  profile: UserProfile,
  allActions: ActivationAction[]
): ActivationAction[] {
  // Filter out completed actions
  const availableActions = allActions.filter(
    (action) => !profile.completedActions.includes(action.id)
  );

  // Sort by priority and profile relevance
  const scored = availableActions.map((action) => {
    let score = 10 - action.priority; // Lower priority number = higher score

    // Boost based on profile type
    if (profile.type === 'nouveau') {
      if (action.category === 'discover') score += 5;
    } else if (profile.type === 'citoyen') {
      if (action.id === 'join-governance') score += 3;
      if (action.category === 'create') score += 2;
    } else if (profile.type === 'collaborateur') {
      if (action.category === 'create') score += 3;
      if (action.id === 'first-workspace') score += 2;
    }

    // Boost based on interests
    if (profile.interests.includes('agents') && action.id.includes('agent')) {
      score += 2;
    }

    return { action, score };
  });

  // Sort by score and return top 3
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, 3).map((s) => s.action);
}

function loadCompletedActions(): string[] {
  try {
    return JSON.parse(localStorage.getItem('atom_completed_actions') || '[]');
  } catch {
    return [];
  }
}

function saveCompletedAction(actionId: string): void {
  const completed = loadCompletedActions();
  if (!completed.includes(actionId)) {
    completed.push(actionId);
    localStorage.setItem('atom_completed_actions', JSON.stringify(completed));
  }
}

// =============================================================================
// ACTIVATION CARD COMPONENT
// =============================================================================

interface ActionCardProps {
  action: ActivationAction;
  index: number;
  onStart: () => void;
  onComplete: () => void;
}

function ActionCard({ action, index, onStart, onComplete }: ActionCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  const categoryColors: Record<ActivationAction['category'], string> = {
    discover: '#3B82F6',
    configure: '#8B5CF6',
    create: '#10B981',
    connect: '#F59E0B',
  };

  const categoryLabels: Record<ActivationAction['category'], string> = {
    discover: 'Découvrir',
    configure: 'Configurer',
    create: 'Créer',
    connect: 'Connecter',
  };

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        padding: '20px',
        backgroundColor: isHovered ? 'rgba(255, 255, 255, 0.08)' : 'rgba(255, 255, 255, 0.03)',
        border: `1px solid ${isHovered ? COLORS.gold + '40' : 'rgba(255, 255, 255, 0.1)'}`,
        borderRadius: '16px',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        transform: isHovered ? 'translateY(-2px)' : 'none',
      }}
      onClick={onStart}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onStart()}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div
            style={{
              width: '40px',
              height: '40px',
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '10px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px',
            }}
          >
            {action.icon}
          </div>
          <div>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                marginBottom: '2px',
              }}
            >
              <span
                style={{
                  color: '#fff',
                  fontSize: '16px',
                  fontWeight: 600,
                  fontFamily: TYPOGRAPHY.fontFamily.system,
                }}
              >
                {action.title}
              </span>
            </div>
            <span
              style={{
                padding: '2px 8px',
                backgroundColor: categoryColors[action.category] + '20',
                color: categoryColors[action.category],
                fontSize: '10px',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}
            >
              {categoryLabels[action.category]}
            </span>
          </div>
        </div>
        <div
          style={{
            width: '28px',
            height: '28px',
            backgroundColor: COLORS.gold + '20',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: COLORS.gold,
            fontSize: '12px',
            fontWeight: 700,
          }}
        >
          {index + 1}
        </div>
      </div>

      {/* Description */}
      <p
        style={{
          color: 'rgba(255, 255, 255, 0.7)',
          fontSize: '14px',
          lineHeight: 1.5,
          margin: '0 0 12px 0',
        }}
      >
        {action.description}
      </p>

      {/* Benefit highlight */}
      <div
        style={{
          padding: '10px 12px',
          backgroundColor: 'rgba(255, 215, 0, 0.05)',
          borderRadius: '8px',
          borderLeft: `3px solid ${COLORS.gold}`,
          marginBottom: '12px',
        }}
      >
        <span style={{ color: COLORS.gold, fontSize: '12px', fontWeight: 500 }}>
          ✨ {action.benefit}
        </span>
      </div>

      {/* Footer */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '12px' }}>
          ⏱️ {action.estimatedTime}
        </span>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onStart();
          }}
          style={{
            padding: '8px 16px',
            backgroundColor: isHovered ? COLORS.gold : 'rgba(255, 255, 255, 0.1)',
            color: isHovered ? '#000' : '#fff',
            border: 'none',
            borderRadius: '8px',
            fontSize: '13px',
            fontWeight: 500,
            cursor: 'pointer',
            transition: 'all 0.2s ease',
          }}
        >
          Commencer →
        </button>
      </div>
    </div>
  );
}

// =============================================================================
// PROGRESS INDICATOR
// =============================================================================

interface ProgressIndicatorProps {
  completed: number;
  total: number;
}

function ProgressIndicator({ completed, total }: ProgressIndicatorProps) {
  const percentage = Math.round((completed / total) * 100);

  return (
    <div style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '13px' }}>
          Progression d'activation
        </span>
        <span style={{ color: COLORS.gold, fontSize: '13px', fontWeight: 500 }}>
          {completed}/{total} actions
        </span>
      </div>
      <div
        style={{
          height: '6px',
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '3px',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${percentage}%`,
            height: '100%',
            backgroundColor: COLORS.gold,
            borderRadius: '3px',
            transition: 'width 0.3s ease',
          }}
        />
      </div>
    </div>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

interface GuidedActivationDashboardProps {
  onDismiss?: () => void;
  showProgress?: boolean;
}

export function GuidedActivationDashboard({
  onDismiss,
  showProgress = true,
}: GuidedActivationDashboardProps) {
  const navigate = useNavigate();
  const experienceMode = useAtomStore((state) => state.ui.experienceMode);
  const [completedActions, setCompletedActions] = useState<string[]>([]);

  useEffect(() => {
    setCompletedActions(loadCompletedActions());
  }, []);

  const userProfile: UserProfile = useMemo(
    () => ({
      type: 'nouveau',
      interests: [],
      completedActions,
    }),
    [completedActions]
  );

  const recommendedActions = useMemo(() => {
    const actionsWithStatus = ALL_ACTIONS.map((action) => ({
      ...action,
      isCompleted: completedActions.includes(action.id),
    }));
    return getRecommendedActions(userProfile, actionsWithStatus);
  }, [userProfile, completedActions]);

  const handleStartAction = (action: ActivationAction) => {
    // Track in funnel
    funnelTracker.trackFirstAction('activation_action', action.id);

    // Navigate
    navigate(action.route);
  };

  const handleCompleteAction = (actionId: string) => {
    saveCompletedAction(actionId);
    setCompletedActions((prev) => [...prev, actionId]);
    funnelTracker.trackFirstSuccess('activation_action', { actionId });
  };

  // Don't show for expert users unless they haven't completed basics
  if (experienceMode === 'expert' && completedActions.length >= 3) {
    return null;
  }

  return (
    <div
      style={{
        padding: '24px',
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        borderRadius: '20px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        fontFamily: TYPOGRAPHY.fontFamily.system,
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
        <div>
          <h2
            style={{
              color: '#fff',
              fontSize: '20px',
              fontWeight: 600,
              margin: '0 0 4px 0',
            }}
          >
            🚀 Vos 3 prochaines actions
          </h2>
          <p
            style={{
              color: 'rgba(255, 255, 255, 0.5)',
              fontSize: '14px',
              margin: 0,
            }}
          >
            Obtenez de la valeur en moins de 5 minutes
          </p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            style={{
              padding: '6px 12px',
              backgroundColor: 'transparent',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '6px',
              color: 'rgba(255, 255, 255, 0.4)',
              fontSize: '12px',
              cursor: 'pointer',
            }}
          >
            Masquer
          </button>
        )}
      </div>

      {/* Progress */}
      {showProgress && (
        <ProgressIndicator completed={completedActions.length} total={ALL_ACTIONS.length} />
      )}

      {/* Actions */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {recommendedActions.map((action, index) => (
          <ActionCard
            key={action.id}
            action={action}
            index={index}
            onStart={() => handleStartAction(action)}
            onComplete={() => handleCompleteAction(action.id)}
          />
        ))}
      </div>

      {/* Footer tip */}
      <div
        style={{
          marginTop: '16px',
          padding: '12px',
          backgroundColor: 'rgba(255, 255, 255, 0.02)',
          borderRadius: '8px',
          textAlign: 'center',
        }}
      >
        <span style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '12px' }}>
          💡 Complétez ces actions pour débloquer des fonctionnalités avancées
        </span>
      </div>
    </div>
  );
}

// =============================================================================
// COMPACT VERSION (for sidebar/widget)
// =============================================================================

export function ActivationWidget() {
  const navigate = useNavigate();
  const [isExpanded, setIsExpanded] = useState(false);
  const [completedActions] = useState<string[]>(() => loadCompletedActions());

  const nextAction = useMemo(() => {
    const available = ALL_ACTIONS.filter((a) => !completedActions.includes(a.id));
    return available.sort((a, b) => a.priority - b.priority)[0];
  }, [completedActions]);

  if (!nextAction || completedActions.length >= 5) {
    return null;
  }

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '180px',
        right: '20px',
        width: isExpanded ? '320px' : '200px',
        backgroundColor: 'rgba(0, 0, 0, 0.95)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: '12px',
        overflow: 'hidden',
        zIndex: 900,
        transition: 'width 0.2s ease',
        fontFamily: TYPOGRAPHY.fontFamily.system,
      }}
    >
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        style={{
          width: '100%',
          padding: '12px 16px',
          backgroundColor: 'transparent',
          border: 'none',
          borderBottom: isExpanded ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
          color: '#fff',
          fontSize: '13px',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span>🎯 Prochaine action</span>
        <span style={{ color: 'rgba(255, 255, 255, 0.4)' }}>
          {isExpanded ? '−' : '+'}
        </span>
      </button>

      {isExpanded && (
        <div style={{ padding: '12px 16px' }}>
          <div style={{ marginBottom: '8px' }}>
            <span style={{ fontSize: '20px', marginRight: '8px' }}>{nextAction.icon}</span>
            <span style={{ color: '#fff', fontWeight: 500 }}>{nextAction.title}</span>
          </div>
          <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '12px', margin: '0 0 12px 0' }}>
            {nextAction.description}
          </p>
          <button
            onClick={() => navigate(nextAction.route)}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: COLORS.gold,
              color: '#000',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 500,
              cursor: 'pointer',
            }}
          >
            Commencer ({nextAction.estimatedTime})
          </button>
        </div>
      )}
    </div>
  );
}

export default GuidedActivationDashboard;
