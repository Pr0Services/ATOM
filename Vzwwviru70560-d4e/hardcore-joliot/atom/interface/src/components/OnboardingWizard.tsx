/**
 * ONBOARDING WIZARD - Guide 60 secondes
 * ======================================
 *
 * Wizard en 3 questions pour qualifier l'intention utilisateur:
 * 1. Objectif: Que voulez-vous accomplir?
 * 2. Profil: Qui êtes-vous?
 * 3. Urgence: Quand en avez-vous besoin?
 *
 * Routage vers parcours personnalisé selon réponses.
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyticsService } from '@/services/analytics.service';
import { COLORS, TYPOGRAPHY, TOUCH, prefersReducedMotion } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface WizardStep {
  id: string;
  question: string;
  options: {
    id: string;
    label: string;
    icon: string;
    description: string;
    route?: string;
  }[];
}

interface OnboardingState {
  objective: string | null;
  profile: string | null;
  urgency: string | null;
}

// =============================================================================
// WIZARD STEPS
// =============================================================================

const WIZARD_STEPS: WizardStep[] = [
  {
    id: 'objective',
    question: 'Que voulez-vous accomplir?',
    options: [
      {
        id: 'discover',
        label: 'Découvrir',
        icon: '🔍',
        description: 'Explorer la plateforme et ses capacités',
        route: '/essaim',
      },
      {
        id: 'operate',
        label: 'Opérer',
        icon: '⚡',
        description: 'Utiliser les agents pour mes projets',
        route: '/essaim',
      },
      {
        id: 'collaborate',
        label: 'Collaborer',
        icon: '🤝',
        description: 'Travailler avec mon équipe',
        route: '/genie',
      },
      {
        id: 'learn',
        label: 'Apprendre',
        icon: '📚',
        description: 'Comprendre comment ça fonctionne',
        route: '/genie',
      },
    ],
  },
  {
    id: 'profile',
    question: 'Qui êtes-vous?',
    options: [
      {
        id: 'individual',
        label: 'Particulier',
        icon: '👤',
        description: 'Usage personnel',
      },
      {
        id: 'entrepreneur',
        label: 'Entrepreneur',
        icon: '🚀',
        description: 'Startup ou indépendant',
      },
      {
        id: 'business',
        label: 'Entreprise',
        icon: '🏢',
        description: 'Organisation établie',
      },
      {
        id: 'student',
        label: 'Étudiant',
        icon: '🎓',
        description: 'Apprentissage et recherche',
      },
    ],
  },
  {
    id: 'urgency',
    question: 'Quand en avez-vous besoin?',
    options: [
      {
        id: 'now',
        label: 'Maintenant',
        icon: '🔥',
        description: 'J\'ai un projet urgent',
      },
      {
        id: 'soon',
        label: 'Cette semaine',
        icon: '📅',
        description: 'Je planifie à court terme',
      },
      {
        id: 'exploring',
        label: 'J\'explore',
        icon: '🧭',
        description: 'Pas de timeline précise',
      },
      {
        id: 'evaluating',
        label: 'J\'évalue',
        icon: '📊',
        description: 'Je compare les solutions',
      },
    ],
  },
];

// =============================================================================
// STORAGE
// =============================================================================

const ONBOARDING_KEY = 'atom_onboarding_completed';
const ONBOARDING_STATE_KEY = 'atom_onboarding_state';

export function hasCompletedOnboarding(): boolean {
  return localStorage.getItem(ONBOARDING_KEY) === 'true';
}

export function markOnboardingComplete(): void {
  localStorage.setItem(ONBOARDING_KEY, 'true');
}

export function resetOnboarding(): void {
  localStorage.removeItem(ONBOARDING_KEY);
  localStorage.removeItem(ONBOARDING_STATE_KEY);
}

function saveOnboardingState(state: OnboardingState): void {
  localStorage.setItem(ONBOARDING_STATE_KEY, JSON.stringify(state));
}

function getOnboardingState(): OnboardingState | null {
  try {
    const raw = localStorage.getItem(ONBOARDING_STATE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

// =============================================================================
// ROUTING LOGIC
// =============================================================================

function getRecommendedRoute(state: OnboardingState): string {
  // Route based on objective and profile
  if (state.objective === 'learn' || state.profile === 'student') {
    return '/genie';
  }
  if (state.objective === 'collaborate') {
    return '/genie';
  }
  if (state.profile === 'business' || state.profile === 'entrepreneur') {
    return '/flux';
  }
  // Default to Essaim
  return '/essaim';
}

// =============================================================================
// ONBOARDING WIZARD COMPONENT
// =============================================================================

interface OnboardingWizardProps {
  onComplete?: (state: OnboardingState) => void;
  onSkip?: () => void;
}

export function OnboardingWizard({ onComplete, onSkip }: OnboardingWizardProps) {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [state, setState] = useState<OnboardingState>({
    objective: null,
    profile: null,
    urgency: null,
  });
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    setReducedMotion(prefersReducedMotion());
    analyticsService.track('cta_click', { cta: 'onboarding_start' });
  }, []);

  const currentStepData = WIZARD_STEPS[currentStep];
  const isLastStep = currentStep === WIZARD_STEPS.length - 1;
  const progress = ((currentStep + 1) / WIZARD_STEPS.length) * 100;

  const handleOptionSelect = (optionId: string) => {
    const newState = {
      ...state,
      [currentStepData.id]: optionId,
    };
    setState(newState);

    // Track selection
    analyticsService.track('cta_click', {
      cta: 'onboarding_select',
      step: currentStepData.id,
      value: optionId,
    });

    if (isLastStep) {
      // Complete onboarding
      saveOnboardingState(newState);
      markOnboardingComplete();

      analyticsService.track('cta_click', { cta: 'onboarding_complete' });

      if (onComplete) {
        onComplete(newState);
      }

      // Navigate to recommended route
      const route = getRecommendedRoute(newState);
      navigate(route);
    } else {
      // Next step
      setTimeout(() => setCurrentStep(currentStep + 1), 200);
    }
  };

  const handleSkip = () => {
    analyticsService.track('cta_click', { cta: 'onboarding_skip' });
    markOnboardingComplete();
    if (onSkip) {
      onSkip();
    }
    navigate('/essaim');
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.95)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px',
    }}>
      <div style={{
        width: '100%',
        maxWidth: '600px',
        backgroundColor: '#0a0a0a',
        borderRadius: '16px',
        border: `1px solid ${COLORS.gold}30`,
        overflow: 'hidden',
      }}>
        {/* Progress bar */}
        <div style={{
          height: '4px',
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
        }}>
          <div style={{
            height: '100%',
            width: `${progress}%`,
            backgroundColor: COLORS.gold,
            transition: reducedMotion ? 'none' : 'width 0.3s ease',
          }} />
        </div>

        {/* Header */}
        <div style={{
          padding: '30px',
          textAlign: 'center',
        }}>
          <div style={{
            fontSize: '12px',
            color: 'rgba(255, 255, 255, 0.4)',
            fontFamily: TYPOGRAPHY.fontFamily.mono,
            marginBottom: '16px',
          }}>
            {currentStep + 1} / {WIZARD_STEPS.length}
          </div>

          <h2 style={{
            fontSize: '24px',
            fontWeight: 600,
            color: '#fff',
            marginBottom: '8px',
          }}>
            {currentStepData.question}
          </h2>

          <p style={{
            fontSize: '14px',
            color: 'rgba(255, 255, 255, 0.5)',
          }}>
            Sélectionnez l'option qui vous correspond le mieux
          </p>
        </div>

        {/* Options */}
        <div style={{
          padding: '0 30px 30px',
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '12px',
        }}>
          {currentStepData.options.map((option) => (
            <button
              key={option.id}
              onClick={() => handleOptionSelect(option.id)}
              style={{
                padding: '20px',
                backgroundColor: state[currentStepData.id as keyof OnboardingState] === option.id
                  ? `${COLORS.gold}20`
                  : 'rgba(255, 255, 255, 0.03)',
                border: `1px solid ${
                  state[currentStepData.id as keyof OnboardingState] === option.id
                    ? COLORS.gold
                    : 'rgba(255, 255, 255, 0.1)'
                }`,
                borderRadius: '12px',
                cursor: 'pointer',
                textAlign: 'left',
                transition: reducedMotion ? 'none' : 'all 0.2s ease',
                minHeight: TOUCH.comfortable,
              }}
              onMouseEnter={(e) => {
                if (state[currentStepData.id as keyof OnboardingState] !== option.id) {
                  e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.3)';
                  e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
                }
              }}
              onMouseLeave={(e) => {
                if (state[currentStepData.id as keyof OnboardingState] !== option.id) {
                  e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                  e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.03)';
                }
              }}
            >
              <div style={{ fontSize: '28px', marginBottom: '12px' }}>
                {option.icon}
              </div>
              <div style={{
                fontSize: '16px',
                fontWeight: 600,
                color: '#fff',
                marginBottom: '4px',
              }}>
                {option.label}
              </div>
              <div style={{
                fontSize: '12px',
                color: 'rgba(255, 255, 255, 0.5)',
              }}>
                {option.description}
              </div>
            </button>
          ))}
        </div>

        {/* Footer */}
        <div style={{
          padding: '20px 30px',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <button
            onClick={handleBack}
            disabled={currentStep === 0}
            style={{
              background: 'transparent',
              border: 'none',
              color: currentStep === 0 ? 'rgba(255, 255, 255, 0.2)' : COLORS.cobalt,
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              fontSize: '14px',
              cursor: currentStep === 0 ? 'default' : 'pointer',
              padding: '10px',
            }}
          >
            ← Retour
          </button>

          <button
            onClick={handleSkip}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'rgba(255, 255, 255, 0.4)',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              fontSize: '14px',
              cursor: 'pointer',
              padding: '10px',
            }}
          >
            Passer →
          </button>
        </div>
      </div>
    </div>
  );
}

export default OnboardingWizard;
