/**
 * CONTEXTUAL ASSISTANT - Mini-assistant "Je vous guide"
 * ======================================================
 *
 * Assistant flottant qui aide l'utilisateur selon le contexte.
 * - FAQ dynamique selon la page
 * - Suggestions contextuelles
 * - Diagnostic de besoin rapide
 */

import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { analyticsService } from '@/services/analytics.service';
import { COLORS, TYPOGRAPHY, TOUCH } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface FAQ {
  question: string;
  answer: string;
  action?: {
    label: string;
    route: string;
  };
}

interface ContextualHelp {
  title: string;
  description: string;
  faqs: FAQ[];
  suggestions: {
    label: string;
    route: string;
    icon: string;
  }[];
}

// =============================================================================
// CONTEXTUAL HELP DATA
// =============================================================================

const CONTEXTUAL_HELP: Record<string, ContextualHelp> = {
  '/': {
    title: 'Le Sceau',
    description: 'Point d\'entrée vers l\'Essaim',
    faqs: [
      {
        question: 'Comment activer le Sceau?',
        answer: 'Maintenez appuyé n\'importe où sur l\'écran pendant 2 secondes pour activer le Sceau et entrer dans l\'Essaim.',
      },
      {
        question: 'Qu\'est-ce que l\'Essaim?',
        answer: 'L\'Essaim est le hub central où vivent les 350 agents IA, organisés en 9 sphères thématiques.',
        action: { label: 'Voir l\'Essaim', route: '/essaim' },
      },
    ],
    suggestions: [
      { label: 'Découvrir les agents', route: '/essaim', icon: '✨' },
      { label: 'Module Éducation', route: '/genie', icon: '🎓' },
    ],
  },
  '/essaim': {
    title: 'L\'Essaim',
    description: 'Hub des 350 agents',
    faqs: [
      {
        question: 'Comment interagir avec un agent?',
        answer: 'Survolez un point lumineux pour voir les détails de l\'agent. Cliquez pour accéder à sa sphère.',
      },
      {
        question: 'Que sont les sphères?',
        answer: 'Les 9 sphères regroupent les agents par domaine: Personal, Business, Government, Creative, Community, Social Media, Entertainment, My Team, Scholar.',
      },
      {
        question: 'Comment zoomer?',
        answer: 'Utilisez la molette de la souris ou pincez sur mobile pour zoomer/dézoomer sur l\'Essaim.',
      },
    ],
    suggestions: [
      { label: 'Retour au Sceau', route: '/', icon: '⚡' },
      { label: 'Module Genie', route: '/genie', icon: '🎓' },
      { label: 'Module Flux', route: '/flux', icon: '💫' },
    ],
  },
  '/genie': {
    title: 'Genie de Demain',
    description: 'Module Éducation',
    faqs: [
      {
        question: 'Comment fonctionne Genie?',
        answer: 'Genie est un espace d\'apprentissage collaboratif basé sur les passions, pas les notes. Dessinez librement, rejoignez des clans thématiques, et interagissez avec votre Agent Mentor.',
      },
      {
        question: 'Qu\'est-ce qu\'un Clan?',
        answer: 'Les Clans regroupent les apprenants par passion (Création, Nature, Technologie, etc.) plutôt que par âge.',
      },
    ],
    suggestions: [
      { label: 'Retour à l\'Essaim', route: '/essaim', icon: '✨' },
      { label: 'Module Santé', route: '/sante', icon: '❤️' },
    ],
  },
  '/flux': {
    title: 'Flux Économique',
    description: 'Module Transport & Économie',
    faqs: [
      {
        question: 'Que fait le module Flux?',
        answer: 'Flux visualise et optimise les flux économiques et de transport, avec des agents spécialisés dans la logistique et la finance.',
      },
    ],
    suggestions: [
      { label: 'Retour à l\'Essaim', route: '/essaim', icon: '✨' },
      { label: 'Module Alchimie', route: '/alchimie', icon: '⚗️' },
    ],
  },
  '/sante': {
    title: 'Santé & Guérison',
    description: 'Module Bio-feedback',
    faqs: [
      {
        question: 'Comment fonctionne le module Santé?',
        answer: 'Le module Santé utilise des fréquences de guérison et du bio-feedback pour optimiser votre bien-être. Visualisez vos métriques de vitalité en temps réel.',
      },
    ],
    suggestions: [
      { label: 'Retour à l\'Essaim', route: '/essaim', icon: '✨' },
      { label: 'Module Genie', route: '/genie', icon: '🎓' },
    ],
  },
};

const DEFAULT_HELP: ContextualHelp = {
  title: 'Aide',
  description: 'Comment puis-je vous aider?',
  faqs: [
    {
      question: 'Comment naviguer dans AT·OM?',
      answer: 'Utilisez le Sceau (/) pour entrer, l\'Essaim pour explorer les agents, et les modules pour des fonctionnalités spécifiques.',
      action: { label: 'Aller au Sceau', route: '/' },
    },
    {
      question: 'Où trouver les agents?',
      answer: 'Tous les 350 agents sont visibles dans l\'Essaim, organisés en 9 sphères thématiques.',
      action: { label: 'Voir l\'Essaim', route: '/essaim' },
    },
  ],
  suggestions: [
    { label: 'Le Sceau', route: '/', icon: '⚡' },
    { label: 'L\'Essaim', route: '/essaim', icon: '✨' },
  ],
};

// =============================================================================
// STORAGE
// =============================================================================

const ASSISTANT_STATE_KEY = 'atom_assistant_dismissed';

function isAssistantDismissed(): boolean {
  return sessionStorage.getItem(ASSISTANT_STATE_KEY) === 'true';
}

function dismissAssistant(): void {
  sessionStorage.setItem(ASSISTANT_STATE_KEY, 'true');
}

// =============================================================================
// CONTEXTUAL ASSISTANT COMPONENT
// =============================================================================

export function ContextualAssistant() {
  const location = useLocation();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(true);
  const [selectedFaq, setSelectedFaq] = useState<number | null>(null);

  // Get contextual help for current route
  const help = CONTEXTUAL_HELP[location.pathname] || DEFAULT_HELP;

  // Don't show if dismissed this session
  useEffect(() => {
    if (isAssistantDismissed()) {
      setIsMinimized(true);
    }
  }, []);

  // Track assistant interactions
  const trackInteraction = (action: string, data?: Record<string, unknown>) => {
    analyticsService.track('cta_click', {
      cta: 'assistant',
      action,
      page: location.pathname,
      ...data,
    });
  };

  const handleToggle = () => {
    if (isMinimized) {
      setIsMinimized(false);
      setIsOpen(true);
      trackInteraction('open');
    } else {
      setIsOpen(!isOpen);
      trackInteraction(isOpen ? 'collapse' : 'expand');
    }
  };

  const handleDismiss = () => {
    dismissAssistant();
    setIsMinimized(true);
    setIsOpen(false);
    trackInteraction('dismiss');
  };

  const handleFaqClick = (index: number) => {
    setSelectedFaq(selectedFaq === index ? null : index);
    trackInteraction('faq_click', { faq: help.faqs[index].question });
  };

  const handleSuggestionClick = (route: string) => {
    trackInteraction('suggestion_click', { route });
    navigate(route);
  };

  const handleActionClick = (route: string) => {
    trackInteraction('action_click', { route });
    navigate(route);
  };

  // Minimized state - just the icon
  if (isMinimized) {
    return (
      <button
        onClick={handleToggle}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          backgroundColor: COLORS.cobalt,
          border: 'none',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 20px rgba(0, 71, 171, 0.4)',
          zIndex: 999,
          transition: 'transform 0.2s ease',
        }}
        onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.1)'; }}
        onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)'; }}
        aria-label="Ouvrir l'assistant"
      >
        <span style={{ fontSize: '24px' }}>💡</span>
      </button>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: isOpen ? '340px' : '200px',
      backgroundColor: 'rgba(10, 10, 10, 0.98)',
      borderRadius: '16px',
      border: `1px solid ${COLORS.cobalt}40`,
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
      zIndex: 999,
      overflow: 'hidden',
      transition: 'width 0.2s ease, height 0.2s ease',
    }}>
      {/* Header */}
      <div
        onClick={handleToggle}
        style={{
          padding: '16px',
          backgroundColor: COLORS.cobalt,
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '20px' }}>💡</span>
          <span style={{
            fontFamily: TYPOGRAPHY.fontFamily.mono,
            fontSize: '14px',
            fontWeight: 600,
            color: '#fff',
          }}>
            Je vous guide
          </span>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={(e) => { e.stopPropagation(); handleDismiss(); }}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'rgba(255, 255, 255, 0.6)',
              cursor: 'pointer',
              padding: '4px',
              fontSize: '16px',
            }}
            aria-label="Fermer l'assistant"
          >
            ×
          </button>
        </div>
      </div>

      {/* Content (when open) */}
      {isOpen && (
        <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
          {/* Context info */}
          <div style={{
            padding: '16px',
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          }}>
            <div style={{
              fontSize: '12px',
              color: COLORS.gold,
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              marginBottom: '4px',
            }}>
              {help.title}
            </div>
            <div style={{
              fontSize: '14px',
              color: 'rgba(255, 255, 255, 0.6)',
            }}>
              {help.description}
            </div>
          </div>

          {/* FAQs */}
          <div style={{ padding: '12px' }}>
            <div style={{
              fontSize: '11px',
              color: 'rgba(255, 255, 255, 0.4)',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              marginBottom: '8px',
              paddingLeft: '4px',
            }}>
              QUESTIONS FRÉQUENTES
            </div>
            {help.faqs.map((faq, index) => (
              <div key={index} style={{ marginBottom: '8px' }}>
                <button
                  onClick={() => handleFaqClick(index)}
                  style={{
                    width: '100%',
                    padding: '12px',
                    backgroundColor: selectedFaq === index
                      ? 'rgba(255, 255, 255, 0.08)'
                      : 'rgba(255, 255, 255, 0.03)',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    textAlign: 'left',
                    color: '#fff',
                    fontSize: '13px',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span>{faq.question}</span>
                    <span style={{ color: 'rgba(255, 255, 255, 0.3)' }}>
                      {selectedFaq === index ? '−' : '+'}
                    </span>
                  </div>
                </button>
                {selectedFaq === index && (
                  <div style={{
                    padding: '12px',
                    fontSize: '12px',
                    color: 'rgba(255, 255, 255, 0.7)',
                    lineHeight: 1.6,
                  }}>
                    {faq.answer}
                    {faq.action && (
                      <button
                        onClick={() => handleActionClick(faq.action!.route)}
                        style={{
                          display: 'block',
                          marginTop: '10px',
                          padding: '8px 12px',
                          backgroundColor: COLORS.gold,
                          color: '#000',
                          border: 'none',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: 600,
                          cursor: 'pointer',
                        }}
                      >
                        {faq.action.label} →
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Suggestions */}
          <div style={{
            padding: '12px',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          }}>
            <div style={{
              fontSize: '11px',
              color: 'rgba(255, 255, 255, 0.4)',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              marginBottom: '8px',
              paddingLeft: '4px',
            }}>
              SUGGESTIONS
            </div>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {help.suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion.route)}
                  style={{
                    padding: '8px 12px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '20px',
                    cursor: 'pointer',
                    color: '#fff',
                    fontSize: '12px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <span>{suggestion.icon}</span>
                  {suggestion.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ContextualAssistant;
