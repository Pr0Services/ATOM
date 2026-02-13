/**
 * MISSION CONSOLE - Next Best Step Dashboard
 * ==========================================
 *
 * Dashboard personnalisé montrant:
 * - Objectif actuel de l'utilisateur
 * - Prochaine action recommandée
 * - Checklist de progression (3 max)
 * - État des services impactants
 *
 * Objectif: Navigation "mission" plutôt que "catalogue"
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyticsService } from '@/services/analytics.service';
import { COLORS, TYPOGRAPHY, TOUCH } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface Mission {
  id: string;
  title: string;
  description: string;
  progress: number;
  steps: MissionStep[];
}

interface MissionStep {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  action?: {
    label: string;
    path: string;
  };
}

interface ServiceStatus {
  id: string;
  name: string;
  status: 'operational' | 'degraded' | 'down';
  latency?: number;
}

// =============================================================================
// STORAGE
// =============================================================================

const MISSION_STORAGE_KEY = 'atom_user_mission';
const PROGRESS_STORAGE_KEY = 'atom_mission_progress';

function getStoredMission(): Mission | null {
  try {
    const raw = localStorage.getItem(MISSION_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function storeMission(mission: Mission): void {
  localStorage.setItem(MISSION_STORAGE_KEY, JSON.stringify(mission));
}

function getCompletedSteps(): string[] {
  try {
    const raw = localStorage.getItem(PROGRESS_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function storeCompletedSteps(steps: string[]): void {
  localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(steps));
}

// =============================================================================
// DEFAULT MISSIONS
// =============================================================================

const DEFAULT_MISSIONS: Record<string, Mission> = {
  explorer: {
    id: 'explorer',
    title: 'Découvrir l\'Essaim',
    description: 'Explorez les 350 agents et trouvez ceux qui correspondent à vos besoins.',
    progress: 0,
    steps: [
      {
        id: 'view-essaim',
        title: 'Visiter l\'Essaim',
        description: 'Découvrez les 9 sphères thématiques.',
        completed: false,
        action: { label: 'Ouvrir l\'Essaim', path: '/essaim' },
      },
      {
        id: 'select-sphere',
        title: 'Choisir une sphère',
        description: 'Sélectionnez un domaine qui vous intéresse.',
        completed: false,
      },
      {
        id: 'interact-agent',
        title: 'Interagir avec un agent',
        description: 'Testez un agent avec votre première requête.',
        completed: false,
      },
    ],
  },
  deployer: {
    id: 'deployer',
    title: 'Déployer votre équipe',
    description: 'Configurez vos agents pour automatiser vos tâches quotidiennes.',
    progress: 0,
    steps: [
      {
        id: 'create-workspace',
        title: 'Créer un espace de travail',
        description: 'Organisez vos agents en équipe dédiée.',
        completed: false,
        action: { label: 'Créer espace', path: '/workspace/new' },
      },
      {
        id: 'add-agents',
        title: 'Ajouter des agents',
        description: 'Sélectionnez 2-3 agents complémentaires.',
        completed: false,
      },
      {
        id: 'first-task',
        title: 'Lancer une première tâche',
        description: 'Déléguez votre première mission à l\'équipe.',
        completed: false,
      },
    ],
  },
  partner: {
    id: 'partner',
    title: 'Devenir Partenaire',
    description: 'Accédez aux fonctionnalités avancées et à la gouvernance.',
    progress: 0,
    steps: [
      {
        id: 'create-account',
        title: 'Créer un compte',
        description: 'Débloquez les fonctionnalités premium.',
        completed: false,
        action: { label: 'S\'inscrire', path: '/auth/register' },
      },
      {
        id: 'verify-email',
        title: 'Vérifier votre email',
        description: 'Confirmez votre adresse pour la sécurité.',
        completed: false,
      },
      {
        id: 'accept-governance',
        title: 'Accepter la gouvernance',
        description: 'Comprenez et acceptez les règles de l\'écosystème.',
        completed: false,
      },
    ],
  },
};

// =============================================================================
// MISSION CONSOLE COMPONENT
// =============================================================================

interface MissionConsoleProps {
  compact?: boolean;
  onMissionSelect?: (missionId: string) => void;
}

export function MissionConsole({ compact = false, onMissionSelect }: MissionConsoleProps) {
  const navigate = useNavigate();
  const [currentMission, setCurrentMission] = useState<Mission | null>(null);
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [serviceStatuses, setServiceStatuses] = useState<ServiceStatus[]>([]);
  const [showMissionSelector, setShowMissionSelector] = useState(false);

  // Load mission and progress
  useEffect(() => {
    const stored = getStoredMission();
    const progress = getCompletedSteps();
    setCompletedSteps(progress);

    if (stored) {
      // Update steps with completion status
      const updatedMission = {
        ...stored,
        steps: stored.steps.map(step => ({
          ...step,
          completed: progress.includes(step.id),
        })),
      };
      updatedMission.progress = Math.round(
        (updatedMission.steps.filter(s => s.completed).length / updatedMission.steps.length) * 100
      );
      setCurrentMission(updatedMission);
    }

    // Simulate service status check
    setServiceStatuses([
      { id: 'api', name: 'API', status: 'operational', latency: 45 },
      { id: 'agents', name: 'Agents', status: 'operational', latency: 120 },
      { id: 'storage', name: 'Stockage', status: 'operational' },
    ]);
  }, []);

  const handleSelectMission = (missionId: string) => {
    const mission = DEFAULT_MISSIONS[missionId];
    if (mission) {
      const updatedMission = {
        ...mission,
        steps: mission.steps.map(step => ({
          ...step,
          completed: completedSteps.includes(step.id),
        })),
      };
      updatedMission.progress = Math.round(
        (updatedMission.steps.filter(s => s.completed).length / updatedMission.steps.length) * 100
      );
      setCurrentMission(updatedMission);
      storeMission(updatedMission);
      setShowMissionSelector(false);
      analyticsService.track('cta_click', { cta: 'mission_select', mission: missionId });
      onMissionSelect?.(missionId);
    }
  };

  const handleCompleteStep = (stepId: string) => {
    const newCompleted = [...completedSteps, stepId];
    setCompletedSteps(newCompleted);
    storeCompletedSteps(newCompleted);

    if (currentMission) {
      const updatedMission = {
        ...currentMission,
        steps: currentMission.steps.map(step => ({
          ...step,
          completed: newCompleted.includes(step.id),
        })),
      };
      updatedMission.progress = Math.round(
        (updatedMission.steps.filter(s => s.completed).length / updatedMission.steps.length) * 100
      );
      setCurrentMission(updatedMission);
      storeMission(updatedMission);
      analyticsService.track('cta_click', { cta: 'mission_step_complete', step: stepId });
    }
  };

  const handleActionClick = (path: string) => {
    analyticsService.track('cta_click', { cta: 'mission_action', path });
    navigate(path);
  };

  const nextStep = currentMission?.steps.find(s => !s.completed);

  // Compact version for sidebar/widget
  if (compact) {
    return (
      <div style={{
        padding: '16px',
        backgroundColor: 'rgba(212, 175, 55, 0.05)',
        border: '1px solid rgba(212, 175, 55, 0.2)',
        borderRadius: '8px',
      }}>
        {currentMission ? (
          <>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '12px',
            }}>
              <span style={{
                color: COLORS.gold,
                fontSize: '12px',
                fontFamily: TYPOGRAPHY.fontFamily.mono,
                letterSpacing: '0.05em',
              }}>
                MISSION EN COURS
              </span>
              <span style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '12px' }}>
                {currentMission.progress}%
              </span>
            </div>
            <h4 style={{ color: '#fff', fontSize: '14px', margin: '0 0 8px 0' }}>
              {nextStep?.title || 'Mission complète!'}
            </h4>
            {nextStep?.action && (
              <button
                onClick={() => handleActionClick(nextStep.action!.path)}
                style={{
                  width: '100%',
                  padding: '8px',
                  backgroundColor: COLORS.gold,
                  color: '#000',
                  border: 'none',
                  borderRadius: '4px',
                  fontSize: '12px',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                {nextStep.action.label}
              </button>
            )}
          </>
        ) : (
          <button
            onClick={() => setShowMissionSelector(true)}
            style={{
              width: '100%',
              padding: '12px',
              backgroundColor: 'transparent',
              color: COLORS.gold,
              border: `1px solid ${COLORS.gold}`,
              borderRadius: '4px',
              fontSize: '13px',
              fontWeight: 500,
              cursor: 'pointer',
            }}
          >
            Choisir un objectif
          </button>
        )}
      </div>
    );
  }

  // Full version
  return (
    <div style={{
      padding: '32px',
      backgroundColor: 'rgba(0, 0, 0, 0.3)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '16px',
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '24px',
      }}>
        <div>
          <h2 style={{
            color: COLORS.gold,
            fontSize: '14px',
            fontFamily: TYPOGRAPHY.fontFamily.mono,
            letterSpacing: '0.1em',
            margin: '0 0 8px 0',
          }}>
            MISSION CONSOLE
          </h2>
          {currentMission ? (
            <h3 style={{ color: '#fff', fontSize: '24px', margin: 0 }}>
              {currentMission.title}
            </h3>
          ) : (
            <h3 style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '20px', margin: 0 }}>
              Aucune mission sélectionnée
            </h3>
          )}
        </div>

        <button
          onClick={() => setShowMissionSelector(!showMissionSelector)}
          style={{
            padding: '8px 16px',
            backgroundColor: 'transparent',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '6px',
            color: 'rgba(255, 255, 255, 0.6)',
            fontSize: '13px',
            cursor: 'pointer',
          }}
        >
          {currentMission ? 'Changer' : 'Choisir'}
        </button>
      </div>

      {/* Mission Selector */}
      {showMissionSelector && (
        <div style={{
          marginBottom: '24px',
          padding: '20px',
          backgroundColor: 'rgba(255, 255, 255, 0.02)',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}>
          <h4 style={{ color: '#fff', fontSize: '16px', margin: '0 0 16px 0' }}>
            Que voulez-vous accomplir ?
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {Object.values(DEFAULT_MISSIONS).map((mission) => (
              <button
                key={mission.id}
                onClick={() => handleSelectMission(mission.id)}
                style={{
                  padding: '16px',
                  backgroundColor: currentMission?.id === mission.id
                    ? 'rgba(212, 175, 55, 0.1)'
                    : 'transparent',
                  border: currentMission?.id === mission.id
                    ? `1px solid ${COLORS.gold}`
                    : '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  textAlign: 'left',
                  cursor: 'pointer',
                }}
              >
                <div style={{ color: '#fff', fontWeight: 500, marginBottom: '4px' }}>
                  {mission.title}
                </div>
                <div style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '13px' }}>
                  {mission.description}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Progress & Steps */}
      {currentMission && !showMissionSelector && (
        <>
          {/* Progress Bar */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: '8px',
            }}>
              <span style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '13px' }}>
                Progression
              </span>
              <span style={{ color: COLORS.gold, fontSize: '13px', fontWeight: 600 }}>
                {currentMission.progress}%
              </span>
            </div>
            <div style={{
              height: '6px',
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '3px',
              overflow: 'hidden',
            }}>
              <div style={{
                height: '100%',
                width: `${currentMission.progress}%`,
                backgroundColor: COLORS.gold,
                borderRadius: '3px',
                transition: 'width 0.3s ease',
              }} />
            </div>
          </div>

          {/* Next Step Highlight */}
          {nextStep && (
            <div style={{
              padding: '20px',
              backgroundColor: 'rgba(212, 175, 55, 0.1)',
              border: '1px solid rgba(212, 175, 55, 0.3)',
              borderRadius: '12px',
              marginBottom: '24px',
            }}>
              <div style={{
                color: COLORS.gold,
                fontSize: '11px',
                fontFamily: TYPOGRAPHY.fontFamily.mono,
                letterSpacing: '0.1em',
                marginBottom: '8px',
              }}>
                PROCHAINE ÉTAPE
              </div>
              <h4 style={{ color: '#fff', fontSize: '18px', margin: '0 0 8px 0' }}>
                {nextStep.title}
              </h4>
              <p style={{ color: 'rgba(255, 255, 255, 0.6)', margin: '0 0 16px 0', fontSize: '14px' }}>
                {nextStep.description}
              </p>
              {nextStep.action && (
                <button
                  onClick={() => handleActionClick(nextStep.action!.path)}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: COLORS.gold,
                    color: '#000',
                    border: 'none',
                    borderRadius: '6px',
                    fontWeight: 600,
                    cursor: 'pointer',
                    fontSize: '14px',
                  }}
                >
                  {nextStep.action.label} →
                </button>
              )}
            </div>
          )}

          {/* Steps Checklist */}
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
          }}>
            {currentMission.steps.map((step, index) => (
              <div
                key={step.id}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px',
                  padding: '12px',
                  backgroundColor: step.completed
                    ? 'rgba(39, 174, 96, 0.05)'
                    : 'transparent',
                  borderRadius: '8px',
                  opacity: step.completed ? 0.7 : 1,
                }}
              >
                <div style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  backgroundColor: step.completed
                    ? '#27AE60'
                    : 'rgba(255, 255, 255, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                }}>
                  {step.completed ? (
                    <span style={{ color: '#fff', fontSize: '12px' }}>✓</span>
                  ) : (
                    <span style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '12px' }}>
                      {index + 1}
                    </span>
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{
                    color: step.completed ? 'rgba(255, 255, 255, 0.5)' : '#fff',
                    fontWeight: 500,
                    textDecoration: step.completed ? 'line-through' : 'none',
                  }}>
                    {step.title}
                  </div>
                  <div style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '13px' }}>
                    {step.description}
                  </div>
                </div>
                {!step.completed && step === nextStep && (
                  <button
                    onClick={() => handleCompleteStep(step.id)}
                    style={{
                      padding: '6px 12px',
                      backgroundColor: 'transparent',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '4px',
                      color: 'rgba(255, 255, 255, 0.6)',
                      fontSize: '12px',
                      cursor: 'pointer',
                    }}
                  >
                    Marquer fait
                  </button>
                )}
              </div>
            ))}
          </div>
        </>
      )}

      {/* Service Status */}
      <div style={{
        marginTop: '24px',
        paddingTop: '24px',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <div style={{
          color: 'rgba(255, 255, 255, 0.4)',
          fontSize: '11px',
          fontFamily: TYPOGRAPHY.fontFamily.mono,
          letterSpacing: '0.05em',
          marginBottom: '12px',
        }}>
          ÉTAT DES SERVICES
        </div>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          {serviceStatuses.map((service) => (
            <div key={service.id} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <div style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: service.status === 'operational'
                  ? '#27AE60'
                  : service.status === 'degraded'
                    ? '#F39C12'
                    : '#E74C3C',
              }} />
              <span style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '13px' }}>
                {service.name}
              </span>
              {service.latency && (
                <span style={{ color: 'rgba(255, 255, 255, 0.3)', fontSize: '11px' }}>
                  {service.latency}ms
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default MissionConsole;
