/**
 * LANDING PAGE - Point d'entrée optimisé
 * =======================================
 *
 * Page d'atterrissage avec:
 * - Proposition de valeur claire en 3 niveaux
 * - CTA unifié (un flux dominant)
 * - Waitlist connectée au backend
 * - Instrumentation analytics complète
 *
 * STRUCTURE:
 * 1. Hero (1 proposition, 1 CTA primaire)
 * 2. 3 Bénéfices concrets
 * 3. Comment ça marche (3 étapes)
 * 4. Waitlist CTA
 * 5. Footer légal
 */

import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyticsService } from '@/services/analytics.service';
import { waitlistService } from '@/services/waitlist.service';
import { abTestingService } from '@/services/ab-testing.service';
import { COLORS, TYPOGRAPHY, TOUCH, prefersReducedMotion } from '@/styles/tokens';

// =============================================================================
// CONSTANTS
// =============================================================================

// Quick Comprehension Blocks (20 seconds)
const QUICK_BLOCKS = [
  {
    id: 'what',
    question: "C'est quoi AT·OM ?",
    answer: "Une plateforme d'intelligence collective avec 350 agents IA organisés en 9 domaines de vie (santé, finance, créativité, etc.). Chaque agent est spécialisé pour vous aider concrètement.",
    icon: '🌐',
  },
  {
    id: 'benefit',
    question: "Qu'est-ce que j'obtiens en 5 minutes ?",
    answer: "Accès immédiat à l'Essaim d'agents. Vous pouvez explorer, interagir et obtenir des résultats sans créer de compte. Votre première valeur : une recommandation personnalisée.",
    icon: '⚡',
  },
  {
    id: 'governance',
    question: "Pourquoi la gouvernance ?",
    answer: "Vos données restent souveraines. Nous ne vendons rien, ne trackons pas. La gouvernance vous donne le contrôle total sur ce que les agents peuvent faire ou non.",
    icon: '🛡️',
  },
];

const BENEFITS = [
  {
    icon: '🤖',
    title: '350+ Agents IA',
    description: 'Accédez à une intelligence collective prête à vous assister dans 9 domaines de vie.',
  },
  {
    icon: '🔐',
    title: 'Souveraineté Totale',
    description: 'Vos données restent les vôtres. Aucun compte requis pour explorer.',
  },
  {
    icon: '⚡',
    title: 'Activation Instantanée',
    description: 'Entrez en 30 secondes. Pas de formulaire, pas d\'attente.',
  },
];

// FAQ - Objection-oriented
const FAQ_ITEMS = [
  {
    question: "Est-ce vraiment gratuit ?",
    answer: "Oui. L'exploration de l'Essaim et l'interaction avec les agents de base sont entièrement gratuites. Des fonctionnalités premium existeront pour les usages avancés.",
  },
  {
    question: "Dois-je créer un compte ?",
    answer: "Non. Vous pouvez explorer et utiliser les agents sans inscription. Un compte optionnel permet de sauvegarder vos préférences et historiques.",
  },
  {
    question: "Mes données sont-elles sécurisées ?",
    answer: "Absolument. Aucune donnée n'est partagée avec des tiers. Le système de gouvernance vous permet de contrôler précisément ce que chaque agent peut accéder.",
  },
  {
    question: "C'est quoi les 9 sphères ?",
    answer: "Les domaines de vie couverts : Personal, Business, Creative, Scholar, Social, Health, Tech, Meta et Sovereign. Chaque sphère contient des agents spécialisés.",
  },
];

const STEPS = [
  {
    step: 1,
    title: 'Activez le Sceau',
    description: 'Maintenez pour ouvrir le portail vers l\'Essaim.',
  },
  {
    step: 2,
    title: 'Explorez les Agents',
    description: 'Découvrez 350 agents organisés en 9 sphères thématiques.',
  },
  {
    step: 3,
    title: 'Créez votre Équipe',
    description: 'Assemblez vos agents pour accomplir vos objectifs.',
  },
];

// =============================================================================
// LANDING PAGE COMPONENT
// =============================================================================

export function Landing() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [waitlistStatus, setWaitlistStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [waitlistMessage, setWaitlistMessage] = useState('');
  const [reducedMotion, setReducedMotion] = useState(false);

  // A/B Testing - Get variant configs
  const heroConfig = useMemo(() => ({
    headline: abTestingService.getConfig('landing_hero_v1', 'headline', "L'Intelligence Collective"),
    subheadline: abTestingService.getConfig('landing_hero_v1', 'subheadline', 'à Votre Service'),
    ctaText: abTestingService.getConfig('landing_hero_v1', 'ctaText', 'ENTRER MAINTENANT'),
    ctaColor: abTestingService.getConfig('landing_hero_v1', 'ctaColor', COLORS.gold),
  }), []);

  const socialProofConfig = useMemo(() => ({
    showSocialProof: abTestingService.getConfig('landing_social_proof', 'showSocialProof', false),
    socialProofText: abTestingService.getConfig('landing_social_proof', 'socialProofText', ''),
  }), []);

  const urgencyConfig = useMemo(() => ({
    showUrgency: abTestingService.getConfig('cta_urgency', 'showUrgency', false),
    urgencyText: abTestingService.getConfig('cta_urgency', 'urgencyText', ''),
  }), []);

  // Track landing view with variant info
  useEffect(() => {
    const assignments = abTestingService.getAssignments();
    analyticsService.track('landing_view', {
      referrer: document.referrer,
      utm_source: new URLSearchParams(window.location.search).get('utm_source'),
      utm_campaign: new URLSearchParams(window.location.search).get('utm_campaign'),
      ab_variants: assignments.map(a => `${a.experimentId}:${a.variantId}`).join(','),
    });
    setReducedMotion(prefersReducedMotion());
  }, []);

  // Handle demo sandbox click
  const handleTryDemo = () => {
    analyticsService.track('cta_click', { cta: 'try_demo', location: 'quick_blocks' });
    navigate('/essaim?demo=true');
  };

  // Handle primary CTA click
  const handleEnterPlatform = () => {
    // Track conversion for A/B tests
    abTestingService.trackConversion('landing_hero_v1', 'cta_click');
    abTestingService.trackConversion('landing_social_proof', 'cta_click');
    abTestingService.trackConversion('cta_urgency', 'cta_click');

    analyticsService.track('cta_click', { cta: 'enter_platform', location: 'hero' });
    navigate('/');
  };

  // Handle waitlist submission
  const handleWaitlistSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;

    setWaitlistStatus('loading');

    const campaign = new URLSearchParams(window.location.search).get('utm_campaign') || undefined;
    const result = await waitlistService.submit(email, 'landing', campaign);

    if (result.success) {
      setWaitlistStatus('success');
      setWaitlistMessage(result.message);
      setEmail('');
    } else {
      setWaitlistStatus('error');
      setWaitlistMessage(result.message);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#000',
      color: '#fff',
      fontFamily: TYPOGRAPHY.fontFamily.system,
    }}>
      {/* ================================================================== */}
      {/* HERO SECTION */}
      {/* ================================================================== */}
      <section style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px 20px',
        textAlign: 'center',
        background: 'radial-gradient(ellipse at center, rgba(0, 71, 171, 0.1) 0%, transparent 70%)',
      }}>
        {/* Logo */}
        <div style={{
          fontSize: '48px',
          fontFamily: TYPOGRAPHY.fontFamily.mono,
          fontWeight: 700,
          color: COLORS.gold,
          marginBottom: '16px',
          letterSpacing: '0.2em',
        }}>
          AT·OM
        </div>

        {/* Tagline - A/B Tested */}
        <h1 style={{
          fontSize: 'clamp(24px, 5vw, 48px)',
          fontWeight: 600,
          maxWidth: '800px',
          marginBottom: '24px',
          lineHeight: 1.2,
        }}>
          {heroConfig.headline}
          <br />
          <span style={{ color: heroConfig.ctaColor }}>{heroConfig.subheadline}</span>
        </h1>

        {/* Social Proof - A/B Tested */}
        {socialProofConfig.showSocialProof && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            marginBottom: '16px',
            padding: '8px 16px',
            backgroundColor: 'rgba(39, 174, 96, 0.1)',
            borderRadius: '20px',
            border: '1px solid rgba(39, 174, 96, 0.3)',
          }}>
            <span style={{ color: '#27AE60', fontSize: '14px' }}>●</span>
            <span style={{ color: '#27AE60', fontSize: '14px', fontFamily: TYPOGRAPHY.fontFamily.mono }}>
              {socialProofConfig.socialProofText}
            </span>
          </div>
        )}

        {/* Value proposition */}
        <p style={{
          fontSize: '18px',
          color: 'rgba(255, 255, 255, 0.7)',
          maxWidth: '600px',
          marginBottom: '40px',
          lineHeight: 1.6,
        }}>
          350 agents IA prêts à vous assister. 9 domaines de vie couverts.
          <br />
          Aucun compte requis pour commencer.
        </p>

        {/* Urgency Badge - A/B Tested */}
        {urgencyConfig.showUrgency && (
          <div style={{
            marginBottom: '16px',
            padding: '6px 12px',
            backgroundColor: 'rgba(231, 76, 60, 0.1)',
            borderRadius: '4px',
            border: '1px solid rgba(231, 76, 60, 0.3)',
          }}>
            <span style={{
              color: '#E74C3C',
              fontSize: '12px',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              letterSpacing: '0.05em',
            }}>
              {urgencyConfig.urgencyText}
            </span>
          </div>
        )}

        {/* Primary CTA - A/B Tested */}
        <button
          onClick={handleEnterPlatform}
          style={{
            padding: '18px 48px',
            fontSize: '18px',
            fontWeight: 600,
            fontFamily: TYPOGRAPHY.fontFamily.mono,
            backgroundColor: heroConfig.ctaColor,
            color: heroConfig.ctaColor === COLORS.gold ? '#000' : '#fff',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            minHeight: TOUCH.comfortable,
            letterSpacing: '0.1em',
            transition: reducedMotion ? 'none' : 'all 0.2s ease',
            boxShadow: `0 0 30px ${heroConfig.ctaColor}40`,
          }}
          onMouseEnter={(e) => {
            if (!reducedMotion) {
              e.currentTarget.style.transform = 'scale(1.05)';
              e.currentTarget.style.boxShadow = `0 0 50px ${heroConfig.ctaColor}60`;
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = `0 0 30px ${heroConfig.ctaColor}40`;
          }}
        >
          {heroConfig.ctaText}
        </button>

        {/* Secondary info */}
        <p style={{
          marginTop: '16px',
          fontSize: '14px',
          color: 'rgba(255, 255, 255, 0.4)',
        }}>
          Accès gratuit · Pas d'inscription · 30 secondes
        </p>

        {/* Scroll indicator */}
        <div style={{
          position: 'absolute',
          bottom: '40px',
          left: '50%',
          transform: 'translateX(-50%)',
          animation: reducedMotion ? 'none' : 'bounce 2s infinite',
        }}>
          <span style={{ color: 'rgba(255, 255, 255, 0.3)', fontSize: '24px' }}>↓</span>
        </div>
      </section>

      {/* ================================================================== */}
      {/* QUICK COMPREHENSION - AT·OM en 20 secondes */}
      {/* ================================================================== */}
      <section style={{
        padding: '80px 20px',
        backgroundColor: 'rgba(212, 175, 55, 0.03)',
        borderTop: '1px solid rgba(212, 175, 55, 0.1)',
        borderBottom: '1px solid rgba(212, 175, 55, 0.1)',
      }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
          <h2 style={{
            textAlign: 'center',
            fontSize: '28px',
            fontWeight: 600,
            marginBottom: '16px',
            color: COLORS.gold,
          }}>
            AT·OM en 20 secondes
          </h2>
          <p style={{
            textAlign: 'center',
            color: 'rgba(255, 255, 255, 0.5)',
            marginBottom: '50px',
            fontSize: '16px',
          }}>
            Les 3 questions essentielles avant de commencer
          </p>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '24px',
          }}>
            {QUICK_BLOCKS.map((block) => (
              <div
                key={block.id}
                style={{
                  padding: '28px',
                  backgroundColor: 'rgba(0, 0, 0, 0.4)',
                  borderRadius: '12px',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                }}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  marginBottom: '16px',
                }}>
                  <span style={{ fontSize: '28px' }}>{block.icon}</span>
                  <h3 style={{
                    fontSize: '18px',
                    fontWeight: 600,
                    color: '#fff',
                    margin: 0,
                  }}>
                    {block.question}
                  </h3>
                </div>
                <p style={{
                  color: 'rgba(255, 255, 255, 0.7)',
                  lineHeight: 1.7,
                  fontSize: '15px',
                  margin: 0,
                }}>
                  {block.answer}
                </p>
              </div>
            ))}
          </div>

          {/* Demo CTA */}
          <div style={{ textAlign: 'center', marginTop: '40px' }}>
            <button
              onClick={handleTryDemo}
              style={{
                padding: '14px 32px',
                fontSize: '15px',
                fontWeight: 500,
                fontFamily: TYPOGRAPHY.fontFamily.mono,
                backgroundColor: 'transparent',
                color: COLORS.gold,
                border: `1px solid ${COLORS.gold}`,
                borderRadius: '6px',
                cursor: 'pointer',
                minHeight: TOUCH.minTarget,
                letterSpacing: '0.05em',
                transition: reducedMotion ? 'none' : 'all 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'rgba(212, 175, 55, 0.1)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              ESSAYER SANS COMPTE →
            </button>
            <p style={{
              marginTop: '12px',
              fontSize: '13px',
              color: 'rgba(255, 255, 255, 0.4)',
            }}>
              Aperçu de l'Essaim en 90 secondes
            </p>
          </div>
        </div>
      </section>

      {/* ================================================================== */}
      {/* BENEFITS SECTION */}
      {/* ================================================================== */}
      <section style={{
        padding: '100px 20px',
        maxWidth: '1200px',
        margin: '0 auto',
      }}>
        <h2 style={{
          textAlign: 'center',
          fontSize: '32px',
          fontWeight: 600,
          marginBottom: '60px',
        }}>
          Pourquoi <span style={{ color: COLORS.gold }}>AT·OM</span> ?
        </h2>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '40px',
        }}>
          {BENEFITS.map((benefit, i) => (
            <div
              key={i}
              style={{
                padding: '40px',
                backgroundColor: 'rgba(255, 255, 255, 0.02)',
                borderRadius: '12px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                textAlign: 'center',
              }}
            >
              <div style={{ fontSize: '48px', marginBottom: '20px' }}>
                {benefit.icon}
              </div>
              <h3 style={{
                fontSize: '20px',
                fontWeight: 600,
                marginBottom: '12px',
                color: COLORS.gold,
              }}>
                {benefit.title}
              </h3>
              <p style={{
                color: 'rgba(255, 255, 255, 0.6)',
                lineHeight: 1.6,
              }}>
                {benefit.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ================================================================== */}
      {/* HOW IT WORKS SECTION */}
      {/* ================================================================== */}
      <section style={{
        padding: '100px 20px',
        backgroundColor: 'rgba(0, 71, 171, 0.05)',
      }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
          <h2 style={{
            textAlign: 'center',
            fontSize: '32px',
            fontWeight: 600,
            marginBottom: '60px',
          }}>
            Comment ça marche ?
          </h2>

          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '40px',
          }}>
            {STEPS.map((step) => (
              <div
                key={step.step}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '30px',
                  padding: '30px',
                  backgroundColor: 'rgba(0, 0, 0, 0.3)',
                  borderRadius: '12px',
                  border: '1px solid rgba(212, 175, 55, 0.2)',
                }}
              >
                <div style={{
                  width: '60px',
                  height: '60px',
                  borderRadius: '50%',
                  backgroundColor: COLORS.gold,
                  color: '#000',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '24px',
                  fontWeight: 700,
                  flexShrink: 0,
                }}>
                  {step.step}
                </div>
                <div>
                  <h3 style={{
                    fontSize: '20px',
                    fontWeight: 600,
                    marginBottom: '8px',
                  }}>
                    {step.title}
                  </h3>
                  <p style={{
                    color: 'rgba(255, 255, 255, 0.6)',
                    margin: 0,
                  }}>
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Secondary CTA */}
          <div style={{ textAlign: 'center', marginTop: '60px' }}>
            <button
              onClick={handleEnterPlatform}
              style={{
                padding: '16px 40px',
                fontSize: '16px',
                fontWeight: 600,
                fontFamily: TYPOGRAPHY.fontFamily.mono,
                backgroundColor: 'transparent',
                color: COLORS.gold,
                border: `2px solid ${COLORS.gold}`,
                borderRadius: '8px',
                cursor: 'pointer',
                minHeight: TOUCH.minTarget,
                letterSpacing: '0.1em',
                transition: reducedMotion ? 'none' : 'all 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = COLORS.gold;
                e.currentTarget.style.color = '#000';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
                e.currentTarget.style.color = COLORS.gold;
              }}
            >
              COMMENCER GRATUITEMENT
            </button>
          </div>
        </div>
      </section>

      {/* ================================================================== */}
      {/* WAITLIST SECTION */}
      {/* ================================================================== */}
      <section style={{
        padding: '100px 20px',
        textAlign: 'center',
      }}>
        <h2 style={{
          fontSize: '28px',
          fontWeight: 600,
          marginBottom: '16px',
        }}>
          Restez Informé
        </h2>
        <p style={{
          color: 'rgba(255, 255, 255, 0.6)',
          marginBottom: '40px',
          maxWidth: '500px',
          margin: '0 auto 40px',
        }}>
          Inscrivez-vous pour recevoir les mises à jour et les nouvelles fonctionnalités.
        </p>

        <form
          onSubmit={handleWaitlistSubmit}
          style={{
            display: 'flex',
            gap: '12px',
            maxWidth: '500px',
            margin: '0 auto',
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}
        >
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="votre@email.com"
            disabled={waitlistStatus === 'loading' || waitlistStatus === 'success'}
            style={{
              flex: '1 1 250px',
              padding: '16px 20px',
              fontSize: '16px',
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: '8px',
              color: '#fff',
              minHeight: TOUCH.minTarget,
              outline: 'none',
            }}
          />
          <button
            type="submit"
            disabled={waitlistStatus === 'loading' || waitlistStatus === 'success'}
            style={{
              padding: '16px 32px',
              fontSize: '16px',
              fontWeight: 600,
              backgroundColor: waitlistStatus === 'success' ? '#27AE60' : COLORS.cobalt,
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              cursor: waitlistStatus === 'loading' ? 'wait' : 'pointer',
              minHeight: TOUCH.minTarget,
              opacity: waitlistStatus === 'loading' ? 0.7 : 1,
            }}
          >
            {waitlistStatus === 'loading' ? 'Envoi...' :
             waitlistStatus === 'success' ? '✓ Inscrit' :
             'S\'inscrire'}
          </button>
        </form>

        {waitlistMessage && (
          <p style={{
            marginTop: '16px',
            color: waitlistStatus === 'success' ? '#27AE60' : '#E74C3C',
            fontSize: '14px',
          }}>
            {waitlistMessage}
          </p>
        )}
      </section>

      {/* ================================================================== */}
      {/* FAQ SECTION */}
      {/* ================================================================== */}
      <section style={{
        padding: '80px 20px',
        backgroundColor: 'rgba(0, 71, 171, 0.03)',
      }}>
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <h2 style={{
            textAlign: 'center',
            fontSize: '28px',
            fontWeight: 600,
            marginBottom: '50px',
          }}>
            Questions Fréquentes
          </h2>

          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
          }}>
            {FAQ_ITEMS.map((item, i) => (
              <details
                key={i}
                style={{
                  padding: '20px 24px',
                  backgroundColor: 'rgba(0, 0, 0, 0.3)',
                  borderRadius: '8px',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  cursor: 'pointer',
                }}
              >
                <summary style={{
                  fontSize: '16px',
                  fontWeight: 500,
                  color: '#fff',
                  listStyle: 'none',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}>
                  {item.question}
                  <span style={{ color: COLORS.gold, fontSize: '20px' }}>+</span>
                </summary>
                <p style={{
                  marginTop: '16px',
                  color: 'rgba(255, 255, 255, 0.7)',
                  lineHeight: 1.7,
                  paddingTop: '16px',
                  borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                }}>
                  {item.answer}
                </p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* ================================================================== */}
      {/* FOOTER */}
      {/* ================================================================== */}
      <footer style={{
        padding: '40px 20px',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        textAlign: 'center',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '30px',
          marginBottom: '20px',
          flexWrap: 'wrap',
        }}>
          <a href="/legal/cgu" style={{ color: 'rgba(255, 255, 255, 0.4)', textDecoration: 'none', fontSize: '14px' }}>
            CGU
          </a>
          <a href="/legal/privacy" style={{ color: 'rgba(255, 255, 255, 0.4)', textDecoration: 'none', fontSize: '14px' }}>
            Confidentialité
          </a>
          <a href="/legal/mentions" style={{ color: 'rgba(255, 255, 255, 0.4)', textDecoration: 'none', fontSize: '14px' }}>
            Mentions Légales
          </a>
        </div>
        <p style={{
          color: 'rgba(255, 255, 255, 0.3)',
          fontSize: '12px',
        }}>
          © 2026 AT·OM · Jonathan Rodrigue · 999 Hz
        </p>
      </footer>

      {/* Animations */}
      <style>{`
        @keyframes bounce {
          0%, 100% { transform: translateX(-50%) translateY(0); }
          50% { transform: translateX(-50%) translateY(-10px); }
        }

        @media (prefers-reduced-motion: reduce) {
          * {
            animation: none !important;
            transition: none !important;
          }
        }
      `}</style>
    </div>
  );
}

export default Landing;
