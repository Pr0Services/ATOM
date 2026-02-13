/**
 * PROGRESSIVE REGISTER - 2-Step Registration with Reassurance
 * ============================================================
 *
 * Inscription progressive en 2 étapes:
 * - Étape A: Création de compte (email, mot de passe)
 * - Étape B: Consentements avec explications contextualisées
 *
 * Features:
 * - Messages de réassurance à chaque étape
 * - Temps estimé affiché
 * - Explication "valeur ↔ consentement"
 * - Microcopie anti-abandon
 */

import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { analyticsService } from '@/services/analytics.service';
import { COLORS, TYPOGRAPHY, TOUCH, prefersReducedMotion } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface FormData {
  email: string;
  password: string;
  confirmPassword: string;
  name?: string;
  consentTerms: boolean;
  consentGovernance: boolean;
  consentData: boolean;
  consentNewsletter: boolean;
}

interface ValidationError {
  field: string;
  message: string;
}

// =============================================================================
// VALIDATION
// =============================================================================

function validateEmail(email: string): string | null {
  if (!email) return 'L\'email est requis';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Format d\'email invalide';
  return null;
}

function validatePassword(password: string): string | null {
  if (!password) return 'Le mot de passe est requis';
  if (password.length < 8) return 'Minimum 8 caractères';
  if (!/[A-Z]/.test(password)) return 'Au moins une majuscule requise';
  if (!/[0-9]/.test(password)) return 'Au moins un chiffre requis';
  return null;
}

function validateConfirmPassword(password: string, confirm: string): string | null {
  if (password !== confirm) return 'Les mots de passe ne correspondent pas';
  return null;
}

// =============================================================================
// CONSENT EXPLANATIONS
// =============================================================================

const CONSENTS = [
  {
    id: 'consentTerms',
    label: 'J\'accepte les Conditions Générales d\'Utilisation',
    required: true,
    explanation: 'Les règles de base pour utiliser AT·OM : respect mutuel, usage responsable des agents, propriété intellectuelle.',
    benefit: 'Vous protège et garantit un environnement sain pour tous.',
    link: '/legal/cgu',
  },
  {
    id: 'consentGovernance',
    label: 'J\'accepte la Charte de Gouvernance',
    required: true,
    explanation: 'Comment les décisions sont prises dans l\'écosystème AT·OM. Votre voix compte.',
    benefit: 'Vous donne un droit de vote sur les évolutions majeures de la plateforme.',
    link: '/legal/governance',
  },
  {
    id: 'consentData',
    label: 'J\'accepte la Politique de Confidentialité',
    required: true,
    explanation: 'Comment vos données sont protégées : chiffrement, non-partage, contrôle total.',
    benefit: 'Vos données restent vôtres. Aucune vente à des tiers, jamais.',
    link: '/legal/privacy',
  },
  {
    id: 'consentNewsletter',
    label: 'Recevoir les actualités AT·OM (optionnel)',
    required: false,
    explanation: 'Maximum 2 emails par mois : nouveaux agents, fonctionnalités, événements.',
    benefit: 'Restez informé sans spam. Désabonnement en 1 clic.',
    link: null,
  },
];

// =============================================================================
// REASSURANCE MESSAGES
// =============================================================================

const REASSURANCE_STEP1 = [
  { icon: '⏱️', text: 'Inscription en 2 minutes' },
  { icon: '🔐', text: 'Données chiffrées' },
  { icon: '🚫', text: 'Pas de spam' },
];

const REASSURANCE_STEP2 = [
  { icon: '📖', text: 'Lisez avant d\'accepter' },
  { icon: '🛡️', text: 'Vos droits protégés' },
  { icon: '↩️', text: 'Révocable à tout moment' },
];

// =============================================================================
// PROGRESSIVE REGISTER COMPONENT
// =============================================================================

export function ProgressiveRegister() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    consentTerms: false,
    consentGovernance: false,
    consentData: false,
    consentNewsletter: false,
  });
  const [errors, setErrors] = useState<ValidationError[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const [expandedConsent, setExpandedConsent] = useState<string | null>(null);

  useEffect(() => {
    setReducedMotion(prefersReducedMotion());
    analyticsService.track('auth_enter', { step: 1, source: searchParams.get('source') });
  }, [searchParams]);

  const handleInputChange = (field: keyof FormData, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error for this field
    setErrors(prev => prev.filter(e => e.field !== field));
  };

  const validateStep1 = (): boolean => {
    const newErrors: ValidationError[] = [];

    const emailError = validateEmail(formData.email);
    if (emailError) newErrors.push({ field: 'email', message: emailError });

    const passwordError = validatePassword(formData.password);
    if (passwordError) newErrors.push({ field: 'password', message: passwordError });

    const confirmError = validateConfirmPassword(formData.password, formData.confirmPassword);
    if (confirmError) newErrors.push({ field: 'confirmPassword', message: confirmError });

    setErrors(newErrors);
    return newErrors.length === 0;
  };

  const validateStep2 = (): boolean => {
    const newErrors: ValidationError[] = [];

    CONSENTS.forEach(consent => {
      if (consent.required && !formData[consent.id as keyof FormData]) {
        newErrors.push({ field: consent.id, message: 'Ce consentement est requis' });
      }
    });

    setErrors(newErrors);
    return newErrors.length === 0;
  };

  const handleNextStep = () => {
    if (validateStep1()) {
      setStep(2);
      analyticsService.track('auth_enter', { step: 2 });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateStep2()) return;

    setIsSubmitting(true);
    analyticsService.track('cta_click', { cta: 'register_submit' });

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      // In production, this would call the actual registration API
      console.log('Registration data:', formData);

      analyticsService.track('cta_click', { cta: 'register_success' });

      // Redirect to success or onboarding
      navigate('/?registered=true');
    } catch (error) {
      setErrors([{ field: 'submit', message: 'Une erreur est survenue. Veuillez réessayer.' }]);
      analyticsService.track('error_displayed', { error: 'registration_failed' });
    } finally {
      setIsSubmitting(false);
    }
  };

  const getFieldError = (field: string): string | undefined => {
    return errors.find(e => e.field === field)?.message;
  };

  const inputStyle = (field: string) => ({
    width: '100%',
    padding: '14px 16px',
    fontSize: '16px',
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    border: `1px solid ${getFieldError(field) ? '#E74C3C' : 'rgba(255, 255, 255, 0.2)'}`,
    borderRadius: '8px',
    color: '#fff',
    outline: 'none',
    minHeight: TOUCH.minTarget,
    transition: reducedMotion ? 'none' : 'border-color 0.2s ease',
  });

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#000',
      color: '#fff',
      display: 'flex',
      flexDirection: 'column',
      fontFamily: TYPOGRAPHY.fontFamily.system,
    }}>
      {/* Header */}
      <header style={{
        padding: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      }}>
        <button
          onClick={() => step === 1 ? navigate(-1) : setStep(1)}
          style={{
            padding: '8px 16px',
            backgroundColor: 'transparent',
            border: 'none',
            color: 'rgba(255, 255, 255, 0.6)',
            cursor: 'pointer',
            fontSize: '14px',
          }}
        >
          ← {step === 1 ? 'Retour' : 'Étape précédente'}
        </button>
        <span style={{
          color: COLORS.gold,
          fontFamily: TYPOGRAPHY.fontFamily.mono,
          fontSize: '20px',
          letterSpacing: '0.1em',
        }}>
          AT·OM
        </span>
        <div style={{ width: '100px' }} /> {/* Spacer */}
      </header>

      {/* Progress Bar */}
      <div style={{
        display: 'flex',
        padding: '0 20px',
        gap: '8px',
      }}>
        <div style={{
          flex: 1,
          height: '4px',
          backgroundColor: COLORS.gold,
          borderRadius: '2px',
        }} />
        <div style={{
          flex: 1,
          height: '4px',
          backgroundColor: step >= 2 ? COLORS.gold : 'rgba(255, 255, 255, 0.1)',
          borderRadius: '2px',
          transition: reducedMotion ? 'none' : 'background-color 0.3s ease',
        }} />
      </div>

      {/* Main Content */}
      <main style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '40px 20px',
        maxWidth: '480px',
        margin: '0 auto',
        width: '100%',
      }}>
        {/* Step Indicator */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '24px',
        }}>
          <span style={{
            color: 'rgba(255, 255, 255, 0.4)',
            fontSize: '14px',
            fontFamily: TYPOGRAPHY.fontFamily.mono,
          }}>
            ÉTAPE {step}/2
          </span>
          <span style={{
            color: 'rgba(255, 255, 255, 0.2)',
            fontSize: '14px',
          }}>
            •
          </span>
          <span style={{
            color: 'rgba(255, 255, 255, 0.4)',
            fontSize: '14px',
          }}>
            {step === 1 ? '~1 minute' : '~30 secondes'}
          </span>
        </div>

        {/* Step 1: Account Creation */}
        {step === 1 && (
          <>
            <h1 style={{
              fontSize: '28px',
              fontWeight: 600,
              marginBottom: '8px',
              textAlign: 'center',
            }}>
              Créez votre compte
            </h1>
            <p style={{
              color: 'rgba(255, 255, 255, 0.6)',
              marginBottom: '32px',
              textAlign: 'center',
            }}>
              Rejoignez l'écosystème AT·OM
            </p>

            {/* Reassurance badges */}
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              gap: '16px',
              marginBottom: '32px',
              flexWrap: 'wrap',
            }}>
              {REASSURANCE_STEP1.map((item, i) => (
                <div key={i} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '6px 12px',
                  backgroundColor: 'rgba(255, 255, 255, 0.02)',
                  borderRadius: '20px',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                }}>
                  <span style={{ fontSize: '14px' }}>{item.icon}</span>
                  <span style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '13px' }}>
                    {item.text}
                  </span>
                </div>
              ))}
            </div>

            <form onSubmit={(e) => { e.preventDefault(); handleNextStep(); }} style={{ width: '100%' }}>
              {/* Name (optional) */}
              <div style={{ marginBottom: '20px' }}>
                <label style={{
                  display: 'block',
                  color: 'rgba(255, 255, 255, 0.7)',
                  fontSize: '14px',
                  marginBottom: '8px',
                }}>
                  Nom (optionnel)
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="Comment voulez-vous qu'on vous appelle ?"
                  style={inputStyle('name')}
                />
              </div>

              {/* Email */}
              <div style={{ marginBottom: '20px' }}>
                <label style={{
                  display: 'block',
                  color: 'rgba(255, 255, 255, 0.7)',
                  fontSize: '14px',
                  marginBottom: '8px',
                }}>
                  Email *
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  placeholder="votre@email.com"
                  required
                  style={inputStyle('email')}
                />
                {getFieldError('email') && (
                  <p style={{ color: '#E74C3C', fontSize: '13px', marginTop: '6px' }}>
                    {getFieldError('email')}
                  </p>
                )}
              </div>

              {/* Password */}
              <div style={{ marginBottom: '20px' }}>
                <label style={{
                  display: 'block',
                  color: 'rgba(255, 255, 255, 0.7)',
                  fontSize: '14px',
                  marginBottom: '8px',
                }}>
                  Mot de passe *
                </label>
                <div style={{ position: 'relative' }}>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    placeholder="Minimum 8 caractères"
                    required
                    style={{ ...inputStyle('password'), paddingRight: '50px' }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: 'absolute',
                      right: '12px',
                      top: '50%',
                      transform: 'translateY(-50%)',
                      backgroundColor: 'transparent',
                      border: 'none',
                      color: 'rgba(255, 255, 255, 0.4)',
                      cursor: 'pointer',
                      fontSize: '14px',
                    }}
                  >
                    {showPassword ? '🙈' : '👁️'}
                  </button>
                </div>
                {getFieldError('password') && (
                  <p style={{ color: '#E74C3C', fontSize: '13px', marginTop: '6px' }}>
                    {getFieldError('password')}
                  </p>
                )}
                <p style={{
                  color: 'rgba(255, 255, 255, 0.4)',
                  fontSize: '12px',
                  marginTop: '6px',
                }}>
                  8+ caractères, 1 majuscule, 1 chiffre
                </p>
              </div>

              {/* Confirm Password */}
              <div style={{ marginBottom: '32px' }}>
                <label style={{
                  display: 'block',
                  color: 'rgba(255, 255, 255, 0.7)',
                  fontSize: '14px',
                  marginBottom: '8px',
                }}>
                  Confirmer le mot de passe *
                </label>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={formData.confirmPassword}
                  onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                  placeholder="Répétez le mot de passe"
                  required
                  style={inputStyle('confirmPassword')}
                />
                {getFieldError('confirmPassword') && (
                  <p style={{ color: '#E74C3C', fontSize: '13px', marginTop: '6px' }}>
                    {getFieldError('confirmPassword')}
                  </p>
                )}
              </div>

              {/* Submit Step 1 */}
              <button
                type="submit"
                style={{
                  width: '100%',
                  padding: '16px',
                  fontSize: '16px',
                  fontWeight: 600,
                  backgroundColor: COLORS.gold,
                  color: '#000',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  minHeight: TOUCH.comfortable,
                }}
              >
                CONTINUER →
              </button>
            </form>

            {/* Already have account */}
            <p style={{
              marginTop: '24px',
              color: 'rgba(255, 255, 255, 0.5)',
              fontSize: '14px',
            }}>
              Déjà un compte ?{' '}
              <a href="/login" style={{ color: COLORS.gold, textDecoration: 'none' }}>
                Se connecter
              </a>
            </p>
          </>
        )}

        {/* Step 2: Consents */}
        {step === 2 && (
          <>
            <h1 style={{
              fontSize: '28px',
              fontWeight: 600,
              marginBottom: '8px',
              textAlign: 'center',
            }}>
              Vos droits & engagements
            </h1>
            <p style={{
              color: 'rgba(255, 255, 255, 0.6)',
              marginBottom: '32px',
              textAlign: 'center',
            }}>
              Comprenez ce que vous acceptez
            </p>

            {/* Reassurance badges */}
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              gap: '16px',
              marginBottom: '32px',
              flexWrap: 'wrap',
            }}>
              {REASSURANCE_STEP2.map((item, i) => (
                <div key={i} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '6px 12px',
                  backgroundColor: 'rgba(255, 255, 255, 0.02)',
                  borderRadius: '20px',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                }}>
                  <span style={{ fontSize: '14px' }}>{item.icon}</span>
                  <span style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '13px' }}>
                    {item.text}
                  </span>
                </div>
              ))}
            </div>

            <form onSubmit={handleSubmit} style={{ width: '100%' }}>
              {/* Consent Items */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '32px' }}>
                {CONSENTS.map((consent) => (
                  <div
                    key={consent.id}
                    style={{
                      padding: '16px',
                      backgroundColor: 'rgba(255, 255, 255, 0.02)',
                      borderRadius: '12px',
                      border: `1px solid ${getFieldError(consent.id) ? '#E74C3C' : 'rgba(255, 255, 255, 0.1)'}`,
                    }}
                  >
                    <label style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '12px',
                      cursor: 'pointer',
                    }}>
                      <input
                        type="checkbox"
                        checked={formData[consent.id as keyof FormData] as boolean}
                        onChange={(e) => handleInputChange(consent.id as keyof FormData, e.target.checked)}
                        style={{
                          width: '20px',
                          height: '20px',
                          marginTop: '2px',
                          accentColor: COLORS.gold,
                        }}
                      />
                      <div style={{ flex: 1 }}>
                        <span style={{ color: '#fff', fontSize: '15px' }}>
                          {consent.label}
                          {consent.required && <span style={{ color: '#E74C3C' }}> *</span>}
                        </span>
                        <button
                          type="button"
                          onClick={() => setExpandedConsent(expandedConsent === consent.id ? null : consent.id)}
                          style={{
                            display: 'block',
                            marginTop: '8px',
                            backgroundColor: 'transparent',
                            border: 'none',
                            color: COLORS.gold,
                            fontSize: '13px',
                            cursor: 'pointer',
                            padding: 0,
                          }}
                        >
                          {expandedConsent === consent.id ? '▼ Masquer les détails' : '▶ Pourquoi ce consentement ?'}
                        </button>

                        {expandedConsent === consent.id && (
                          <div style={{
                            marginTop: '12px',
                            padding: '12px',
                            backgroundColor: 'rgba(0, 0, 0, 0.3)',
                            borderRadius: '8px',
                          }}>
                            <p style={{
                              color: 'rgba(255, 255, 255, 0.7)',
                              fontSize: '13px',
                              margin: '0 0 8px 0',
                              lineHeight: 1.5,
                            }}>
                              <strong>Ce que ça couvre :</strong> {consent.explanation}
                            </p>
                            <p style={{
                              color: '#27AE60',
                              fontSize: '13px',
                              margin: 0,
                              lineHeight: 1.5,
                            }}>
                              <strong>Ce que vous y gagnez :</strong> {consent.benefit}
                            </p>
                            {consent.link && (
                              <a
                                href={consent.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                  display: 'inline-block',
                                  marginTop: '8px',
                                  color: COLORS.gold,
                                  fontSize: '12px',
                                  textDecoration: 'none',
                                }}
                              >
                                Lire le document complet →
                              </a>
                            )}
                          </div>
                        )}
                      </div>
                    </label>
                    {getFieldError(consent.id) && (
                      <p style={{ color: '#E74C3C', fontSize: '12px', marginTop: '8px', marginLeft: '32px' }}>
                        {getFieldError(consent.id)}
                      </p>
                    )}
                  </div>
                ))}
              </div>

              {/* Submit Error */}
              {getFieldError('submit') && (
                <div style={{
                  padding: '12px 16px',
                  backgroundColor: 'rgba(231, 76, 60, 0.1)',
                  border: '1px solid rgba(231, 76, 60, 0.3)',
                  borderRadius: '8px',
                  marginBottom: '20px',
                }}>
                  <p style={{ color: '#E74C3C', fontSize: '14px', margin: 0 }}>
                    {getFieldError('submit')}
                  </p>
                </div>
              )}

              {/* Submit Step 2 */}
              <button
                type="submit"
                disabled={isSubmitting}
                style={{
                  width: '100%',
                  padding: '16px',
                  fontSize: '16px',
                  fontWeight: 600,
                  backgroundColor: isSubmitting ? 'rgba(212, 175, 55, 0.5)' : COLORS.gold,
                  color: '#000',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: isSubmitting ? 'wait' : 'pointer',
                  minHeight: TOUCH.comfortable,
                }}
              >
                {isSubmitting ? 'Création en cours...' : 'CRÉER MON COMPTE'}
              </button>

              {/* Final reassurance */}
              <p style={{
                marginTop: '16px',
                color: 'rgba(255, 255, 255, 0.4)',
                fontSize: '12px',
                textAlign: 'center',
                lineHeight: 1.5,
              }}>
                En créant votre compte, vous pouvez révoquer ces consentements à tout moment
                depuis vos paramètres. Vos données ne seront jamais vendues.
              </p>
            </form>
          </>
        )}
      </main>
    </div>
  );
}

export default ProgressiveRegister;
