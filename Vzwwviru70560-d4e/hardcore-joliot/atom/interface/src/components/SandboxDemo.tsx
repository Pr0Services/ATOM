/**
 * SANDBOX DEMO - Interactive Preview Without Account
 * ===================================================
 *
 * Démonstration interactive de l'Essaim sans inscription:
 * - Aperçu des 9 sphères
 * - Interaction simulée avec 3 agents
 * - Résultat concret en 90 secondes
 *
 * Objectif: Preuve de valeur avant inscription
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyticsService } from '@/services/analytics.service';
import { COLORS, TYPOGRAPHY, TOUCH, prefersReducedMotion } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface DemoStep {
  id: string;
  title: string;
  description: string;
  action: string;
  duration: number; // seconds
}

interface DemoAgent {
  id: string;
  name: string;
  sphere: string;
  description: string;
  sampleOutput: string;
}

// =============================================================================
// DEMO DATA
// =============================================================================

const DEMO_STEPS: DemoStep[] = [
  {
    id: 'intro',
    title: 'Bienvenue dans l\'Essaim',
    description: '350 agents IA organisés en 9 sphères thématiques. Choisissez une sphère pour commencer.',
    action: 'Choisir une sphère',
    duration: 10,
  },
  {
    id: 'sphere',
    title: 'Explorez les Agents',
    description: 'Chaque sphère contient des agents spécialisés. Sélectionnez un agent pour voir ce qu\'il peut faire.',
    action: 'Sélectionner un agent',
    duration: 15,
  },
  {
    id: 'interact',
    title: 'Interagissez',
    description: 'Posez une question ou décrivez votre besoin. L\'agent vous répond instantanément.',
    action: 'Voir le résultat',
    duration: 20,
  },
];

const DEMO_SPHERES = [
  { id: 'personal', name: 'Personal', icon: '🎯', color: '#FF6B6B', agents: 42 },
  { id: 'business', name: 'Business', icon: '💼', color: '#4ECDC4', agents: 38 },
  { id: 'creative', name: 'Creative', icon: '🎨', color: '#9B59B6', agents: 35 },
  { id: 'scholar', name: 'Scholar', icon: '🎓', color: '#3498DB', agents: 40 },
  { id: 'social', name: 'Social', icon: '🤝', color: '#F39C12', agents: 32 },
  { id: 'health', name: 'Health', icon: '💚', color: '#27AE60', agents: 38 },
  { id: 'tech', name: 'Tech', icon: '⚙️', color: '#1ABC9C', agents: 45 },
  { id: 'meta', name: 'Meta', icon: '🔮', color: '#8E44AD', agents: 40 },
  { id: 'sovereign', name: 'Sovereign', icon: '👑', color: '#D4AF37', agents: 40 },
];

const DEMO_AGENTS: Record<string, DemoAgent[]> = {
  personal: [
    {
      id: 'habit-coach',
      name: 'Habit Coach',
      sphere: 'Personal',
      description: 'Vous aide à construire et maintenir des habitudes positives.',
      sampleOutput: '📋 Votre plan d\'habitude personnalisé:\n\n1. **Réveil** → Méditation 5 min\n2. **Matin** → Exercice 20 min\n3. **Midi** → Revue des objectifs\n4. **Soir** → Journaling 10 min\n\n✅ Commencez petit, progressez régulièrement.',
    },
    {
      id: 'goal-setter',
      name: 'Goal Setter',
      sphere: 'Personal',
      description: 'Transforme vos aspirations en objectifs SMART actionnables.',
      sampleOutput: '🎯 Objectif SMART créé:\n\n**Spécifique**: Perdre 5kg\n**Mesurable**: Pesée hebdomadaire\n**Atteignable**: -0.5kg/semaine\n**Réaliste**: Alimentation + sport\n**Temporel**: D\'ici 10 semaines\n\n📊 Prochain checkpoint: Semaine 1',
    },
  ],
  business: [
    {
      id: 'pitch-crafter',
      name: 'Pitch Crafter',
      sphere: 'Business',
      description: 'Crée des pitchs percutants pour vos projets.',
      sampleOutput: '🎤 Pitch 60 secondes:\n\n"Imaginez pouvoir [PROBLÈME] en seulement [TEMPS].\n\nAujourd\'hui, [STATISTIQUE CHOC].\n\nNotre solution: [PRODUIT] qui [BÉNÉFICE PRINCIPAL].\n\nRésultat: [MÉTRIQUE DE SUCCÈS].\n\nRejoignez les [N] utilisateurs qui ont déjà transformé leur [DOMAINE]."',
    },
  ],
  creative: [
    {
      id: 'story-weaver',
      name: 'Story Weaver',
      sphere: 'Creative',
      description: 'Génère des histoires et concepts créatifs.',
      sampleOutput: '📖 Concept d\'histoire généré:\n\n**Genre**: Science-fiction introspective\n**Prémisse**: Dans un monde où les rêves sont taxés...\n**Protagoniste**: Une archiviste de souvenirs\n**Conflit**: Découvre que ses propres rêves sont falsifiés\n**Thème**: Identité vs. Construction sociale',
    },
  ],
};

// =============================================================================
// SANDBOX DEMO COMPONENT
// =============================================================================

interface SandboxDemoProps {
  onClose: () => void;
  onContinue: () => void;
}

export function SandboxDemo({ onClose, onContinue }: SandboxDemoProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedSphere, setSelectedSphere] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<DemoAgent | null>(null);
  const [showOutput, setShowOutput] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    setReducedMotion(prefersReducedMotion());
    analyticsService.track('cta_click', { cta: 'sandbox_demo_start' });
  }, []);

  const handleSphereSelect = (sphereId: string) => {
    setSelectedSphere(sphereId);
    setCurrentStep(1);
    analyticsService.track('cta_click', { cta: 'demo_sphere_select', sphere: sphereId });
  };

  const handleAgentSelect = (agent: DemoAgent) => {
    setSelectedAgent(agent);
    setCurrentStep(2);
    analyticsService.track('cta_click', { cta: 'demo_agent_select', agent: agent.id });
  };

  const handleShowResult = () => {
    setShowOutput(true);
    analyticsService.track('cta_click', { cta: 'demo_show_result' });
  };

  const handleContinue = () => {
    analyticsService.track('cta_click', { cta: 'demo_continue_to_platform' });
    onContinue();
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.95)',
      zIndex: 1000,
      display: 'flex',
      flexDirection: 'column',
      overflow: 'auto',
    }}>
      {/* Header */}
      <header style={{
        padding: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <div>
          <span style={{
            color: COLORS.gold,
            fontFamily: TYPOGRAPHY.fontFamily.mono,
            fontSize: '14px',
            letterSpacing: '0.1em',
          }}>
            DÉMO SANDBOX
          </span>
          <span style={{
            color: 'rgba(255, 255, 255, 0.4)',
            marginLeft: '16px',
            fontSize: '14px',
          }}>
            Étape {currentStep + 1} / 3
          </span>
        </div>
        <button
          onClick={onClose}
          style={{
            padding: '8px 16px',
            backgroundColor: 'transparent',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '4px',
            color: 'rgba(255, 255, 255, 0.6)',
            cursor: 'pointer',
            fontSize: '14px',
          }}
        >
          Fermer
        </button>
      </header>

      {/* Progress Bar */}
      <div style={{
        height: '3px',
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
      }}>
        <div style={{
          height: '100%',
          width: `${((currentStep + 1) / 3) * 100}%`,
          backgroundColor: COLORS.gold,
          transition: reducedMotion ? 'none' : 'width 0.3s ease',
        }} />
      </div>

      {/* Content */}
      <main style={{
        flex: 1,
        padding: '40px 20px',
        maxWidth: '1000px',
        margin: '0 auto',
        width: '100%',
      }}>
        {/* Step 0: Sphere Selection */}
        {currentStep === 0 && (
          <div>
            <h2 style={{
              fontSize: '28px',
              fontWeight: 600,
              marginBottom: '16px',
              color: '#fff',
              textAlign: 'center',
            }}>
              Choisissez une Sphère
            </h2>
            <p style={{
              color: 'rgba(255, 255, 255, 0.6)',
              textAlign: 'center',
              marginBottom: '40px',
            }}>
              9 domaines de vie, 350 agents spécialisés
            </p>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
              gap: '16px',
            }}>
              {DEMO_SPHERES.map((sphere) => (
                <button
                  key={sphere.id}
                  onClick={() => handleSphereSelect(sphere.id)}
                  style={{
                    padding: '24px 16px',
                    backgroundColor: 'rgba(255, 255, 255, 0.02)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    textAlign: 'center',
                    transition: reducedMotion ? 'none' : 'all 0.2s ease',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = sphere.color;
                    e.currentTarget.style.backgroundColor = `${sphere.color}10`;
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                    e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.02)';
                  }}
                >
                  <div style={{ fontSize: '32px', marginBottom: '8px' }}>{sphere.icon}</div>
                  <div style={{ color: '#fff', fontWeight: 500, marginBottom: '4px' }}>{sphere.name}</div>
                  <div style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '12px' }}>
                    {sphere.agents} agents
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 1: Agent Selection */}
        {currentStep === 1 && selectedSphere && (
          <div>
            <button
              onClick={() => setCurrentStep(0)}
              style={{
                marginBottom: '24px',
                padding: '8px 16px',
                backgroundColor: 'transparent',
                border: 'none',
                color: 'rgba(255, 255, 255, 0.5)',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              ← Retour aux sphères
            </button>

            <h2 style={{
              fontSize: '28px',
              fontWeight: 600,
              marginBottom: '16px',
              color: '#fff',
            }}>
              Agents de la sphère {DEMO_SPHERES.find(s => s.id === selectedSphere)?.name}
            </h2>
            <p style={{
              color: 'rgba(255, 255, 255, 0.6)',
              marginBottom: '40px',
            }}>
              Sélectionnez un agent pour voir ce qu'il peut faire
            </p>

            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '16px',
            }}>
              {(DEMO_AGENTS[selectedSphere] || DEMO_AGENTS.personal).map((agent) => (
                <button
                  key={agent.id}
                  onClick={() => handleAgentSelect(agent)}
                  style={{
                    padding: '24px',
                    backgroundColor: 'rgba(255, 255, 255, 0.02)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: reducedMotion ? 'none' : 'all 0.2s ease',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = COLORS.gold;
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                  }}
                >
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}>
                    <div>
                      <h3 style={{ color: COLORS.gold, fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>
                        {agent.name}
                      </h3>
                      <p style={{ color: 'rgba(255, 255, 255, 0.6)', margin: 0 }}>
                        {agent.description}
                      </p>
                    </div>
                    <span style={{ color: COLORS.gold, fontSize: '24px' }}>→</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Interaction & Result */}
        {currentStep === 2 && selectedAgent && (
          <div>
            <button
              onClick={() => { setCurrentStep(1); setShowOutput(false); }}
              style={{
                marginBottom: '24px',
                padding: '8px 16px',
                backgroundColor: 'transparent',
                border: 'none',
                color: 'rgba(255, 255, 255, 0.5)',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              ← Retour aux agents
            </button>

            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '24px',
            }}>
              {/* Agent Info */}
              <div style={{
                padding: '24px',
                backgroundColor: 'rgba(212, 175, 55, 0.05)',
                border: '1px solid rgba(212, 175, 55, 0.2)',
                borderRadius: '12px',
              }}>
                <h3 style={{ color: COLORS.gold, fontSize: '20px', fontWeight: 600, marginBottom: '8px' }}>
                  {selectedAgent.name}
                </h3>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', marginBottom: '24px' }}>
                  {selectedAgent.description}
                </p>

                {!showOutput && (
                  <button
                    onClick={handleShowResult}
                    style={{
                      width: '100%',
                      padding: '14px',
                      backgroundColor: COLORS.gold,
                      color: '#000',
                      border: 'none',
                      borderRadius: '8px',
                      fontWeight: 600,
                      cursor: 'pointer',
                      fontSize: '16px',
                    }}
                  >
                    Voir un exemple de résultat
                  </button>
                )}
              </div>

              {/* Output */}
              <div style={{
                padding: '24px',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '12px',
                minHeight: '300px',
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '16px',
                  paddingBottom: '16px',
                  borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
                }}>
                  <div style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    backgroundColor: showOutput ? '#27AE60' : 'rgba(255, 255, 255, 0.3)',
                  }} />
                  <span style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '14px' }}>
                    {showOutput ? 'Résultat généré' : 'En attente...'}
                  </span>
                </div>

                {showOutput ? (
                  <pre style={{
                    color: 'rgba(255, 255, 255, 0.8)',
                    fontFamily: TYPOGRAPHY.fontFamily.mono,
                    fontSize: '14px',
                    lineHeight: 1.6,
                    whiteSpace: 'pre-wrap',
                    margin: 0,
                  }}>
                    {selectedAgent.sampleOutput}
                  </pre>
                ) : (
                  <p style={{
                    color: 'rgba(255, 255, 255, 0.3)',
                    textAlign: 'center',
                    marginTop: '60px',
                  }}>
                    Cliquez sur "Voir un exemple" pour découvrir ce que cet agent peut produire.
                  </p>
                )}
              </div>
            </div>

            {/* Continue CTA */}
            {showOutput && (
              <div style={{
                marginTop: '40px',
                padding: '32px',
                backgroundColor: 'rgba(212, 175, 55, 0.05)',
                border: '1px solid rgba(212, 175, 55, 0.2)',
                borderRadius: '12px',
                textAlign: 'center',
              }}>
                <h3 style={{ color: '#fff', fontSize: '20px', fontWeight: 600, marginBottom: '8px' }}>
                  Prêt à explorer l'Essaim complet ?
                </h3>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', marginBottom: '24px' }}>
                  349 autres agents vous attendent. Aucune inscription requise.
                </p>
                <button
                  onClick={handleContinue}
                  style={{
                    padding: '16px 48px',
                    fontSize: '16px',
                    fontWeight: 600,
                    fontFamily: TYPOGRAPHY.fontFamily.mono,
                    backgroundColor: COLORS.gold,
                    color: '#000',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    minHeight: TOUCH.minTarget,
                    letterSpacing: '0.05em',
                  }}
                >
                  CONTINUER VERS L'ESSAIM →
                </button>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default SandboxDemo;
