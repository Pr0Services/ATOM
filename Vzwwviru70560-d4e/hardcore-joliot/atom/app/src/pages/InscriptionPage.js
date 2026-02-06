/**
 * AT·OM — Inscription Progressive
 * Formulaire adaptatif: Citoyen → Collaborateur → Investisseur
 * Les questions s'ajoutent selon la sélection (prise de possession progressive)
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { updateProfile } from '../lib/supabase';
import SocialAuthButtons from '../components/SocialAuthButtons';
import { useTokenomics } from '../hooks/useTokenomics';

// ═══════════════════════════════════════════════════════════════════════════════
// STEP DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════════

const STEPS = {
  WELCOME: 'welcome',
  AUTH: 'auth',
  IDENTITY: 'identity',
  CATEGORIES: 'categories',
  CITOYEN: 'citoyen',
  COLLABORATEUR: 'collaborateur',
  INVESTISSEUR: 'investisseur',
  CONFIRMATION: 'confirmation',
};

// ═══════════════════════════════════════════════════════════════════════════════
// INSCRIPTION PAGE
// ═══════════════════════════════════════════════════════════════════════════════

const InscriptionPage = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, register, loginWithSocial, loading: authLoading } = useAuth();
  const { contribute, nftAvailability, loading: tokenLoading } = useTokenomics();

  const [step, setStep] = useState(STEPS.WELCOME);
  const [formData, setFormData] = useState({
    // Identity
    full_name: '',
    email: '',
    password: '',
    phone: '',
    location: '',
    bio: '',

    // Categories
    categories: [],

    // Citoyen
    interests: [],
    local_needs_priority: '',

    // Collaborateur
    profession: '',
    skills: [],
    availability: '',
    portfolio_url: '',

    // Investisseur
    contribution_amount: '',
    nft_tier: '',
    flow_type: '',
    investment_message: '',
  });

  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  // Auto-fill from OAuth if user arrives authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      const meta = user.user_metadata || {};
      setFormData(prev => ({
        ...prev,
        full_name: meta.full_name || meta.name || meta.display_name || prev.full_name,
        email: user.email || prev.email,
      }));
      // Skip to identity or categories if already logged in
      if (step === STEPS.WELCOME || step === STEPS.AUTH) {
        setStep(STEPS.IDENTITY);
      }
    }
  }, [isAuthenticated, user]);

  // ─── Navigation helpers ─────────────────────────────────────────────

  const getSteps = useCallback(() => {
    const steps = [STEPS.WELCOME, STEPS.AUTH, STEPS.IDENTITY, STEPS.CATEGORIES];

    // Add progressive steps based on selected categories
    if (formData.categories.includes('citoyen')) steps.push(STEPS.CITOYEN);
    if (formData.categories.includes('collaborateur')) steps.push(STEPS.COLLABORATEUR);
    if (formData.categories.includes('investisseur')) steps.push(STEPS.INVESTISSEUR);

    steps.push(STEPS.CONFIRMATION);
    return steps;
  }, [formData.categories]);

  const nextStep = () => {
    const steps = getSteps();
    const idx = steps.indexOf(step);
    if (idx < steps.length - 1) {
      setStep(steps[idx + 1]);
      setErrors({});
    }
  };

  const prevStep = () => {
    const steps = getSteps();
    const idx = steps.indexOf(step);
    if (idx > 0) {
      setStep(steps[idx - 1]);
      setErrors({});
    }
  };

  const progress = () => {
    const steps = getSteps();
    const idx = steps.indexOf(step);
    return ((idx) / (steps.length - 1)) * 100;
  };

  // ─── Field updater ──────────────────────────────────────────────────

  const updateField = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setErrors(prev => ({ ...prev, [field]: null }));
  };

  const toggleArrayField = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field]?.includes(value)
        ? prev[field].filter(v => v !== value)
        : [...(prev[field] || []), value],
    }));
  };

  // ─── Email/password registration ────────────────────────────────────

  const handleEmailRegister = async () => {
    if (!formData.email || !formData.password) {
      setErrors({ auth: 'Email et mot de passe requis' });
      return;
    }
    if (formData.password.length < 8) {
      setErrors({ auth: 'Le mot de passe doit contenir au moins 8 caractères' });
      return;
    }

    const result = await register(formData.email, formData.password, formData.full_name);
    if (result.success) {
      nextStep();
    } else {
      setErrors({ auth: result.error || 'Erreur de création de compte' });
    }
  };

  // ─── Final submission ───────────────────────────────────────────────

  const handleSubmit = async () => {
    if (!user?.id) return;
    setSubmitting(true);

    try {
      // 1. Update profile in Supabase
      await updateProfile(user.id, {
        full_name: formData.full_name,
        phone: formData.phone,
        location: formData.location,
        bio: formData.bio,
        categories: formData.categories,
        profession: formData.profession,
        skills: formData.skills,
        availability: formData.availability,
        interests: formData.interests,
      });

      // 2. If investor, process contribution
      if (formData.categories.includes('investisseur') && formData.contribution_amount) {
        try {
          const contributionResult = await contribute(
            parseFloat(formData.contribution_amount),
            formData.flow_type || null,
            formData.investment_message || null,
          );
          setResult({
            success: true,
            contribution: contributionResult,
          });
        } catch (err) {
          setResult({
            success: true, // Profile saved, but contribution had an error
            contributionError: err.message,
          });
        }
      } else {
        setResult({ success: true });
      }

      nextStep();
    } catch (err) {
      setErrors({ submit: err.message });
    } finally {
      setSubmitting(false);
    }
  };

  // ═══════════════════════════════════════════════════════════════════════
  // STEP RENDERERS
  // ═══════════════════════════════════════════════════════════════════════

  const renderWelcome = () => (
    <div className="text-center space-y-6">
      <div className="text-6xl mb-4">🔱</div>
      <h1 className="text-3xl font-bold text-yellow-400 tracking-wider">
        BIENVENUE DANS L'ARCHE
      </h1>
      <p className="text-gray-400 max-w-md mx-auto">
        Rejoignez le mouvement AT·OM et participez à la construction
        d'une économie souveraine pour Progreso 2026.
      </p>
      <div className="space-y-3 max-w-xs mx-auto">
        <button
          onClick={nextStep}
          className="w-full py-4 rounded-lg font-bold text-lg bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400 transition-all shadow-lg"
        >
          COMMENCER L'INSCRIPTION
        </button>
      </div>
    </div>
  );

  const renderAuth = () => (
    <div className="space-y-6 max-w-md mx-auto">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-yellow-400">CRÉER VOTRE COMPTE</h2>
        <p className="text-gray-500 text-sm mt-2">
          Connectez-vous avec un réseau social ou créez un compte
        </p>
      </div>

      {/* Social Auth */}
      <SocialAuthButtons
        mode="signup"
        showDivider={false}
        onSuccess={() => nextStep()}
      />

      {/* Divider */}
      <div className="flex items-center gap-4">
        <div className="flex-1 h-px bg-gray-700" />
        <span className="text-gray-500 text-sm">ou par email</span>
        <div className="flex-1 h-px bg-gray-700" />
      </div>

      {/* Email/Password */}
      <div className="space-y-4">
        <input
          type="text"
          value={formData.full_name}
          onChange={(e) => updateField('full_name', e.target.value)}
          placeholder="Votre nom complet"
          className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
        />
        <input
          type="email"
          value={formData.email}
          onChange={(e) => updateField('email', e.target.value)}
          placeholder="votre@email.com"
          className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
        />
        <input
          type="password"
          value={formData.password}
          onChange={(e) => updateField('password', e.target.value)}
          placeholder="Mot de passe (min. 8 caractères)"
          className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
        />

        {errors.auth && (
          <p className="text-red-400 text-sm text-center">{errors.auth}</p>
        )}

        <button
          onClick={handleEmailRegister}
          disabled={authLoading}
          className="w-full py-3 rounded-lg font-bold bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400 transition-all"
        >
          {authLoading ? 'Création...' : 'CRÉER MON COMPTE'}
        </button>
      </div>
    </div>
  );

  const renderIdentity = () => (
    <div className="space-y-6 max-w-md mx-auto">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-yellow-400">VOS INFORMATIONS</h2>
        <p className="text-gray-500 text-sm mt-2">Complétez votre profil</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-gray-400 text-sm mb-1">Nom complet</label>
          <input
            type="text"
            value={formData.full_name}
            onChange={(e) => updateField('full_name', e.target.value)}
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-gray-400 text-sm mb-1">Téléphone</label>
          <input
            type="tel"
            value={formData.phone}
            onChange={(e) => updateField('phone', e.target.value)}
            placeholder="+1 (514) 000-0000"
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-gray-400 text-sm mb-1">Localisation</label>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => updateField('location', e.target.value)}
            placeholder="Ville, Province"
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-gray-400 text-sm mb-1">Quelques mots sur vous</label>
          <textarea
            value={formData.bio}
            onChange={(e) => updateField('bio', e.target.value)}
            rows={3}
            maxLength={500}
            placeholder="Votre motivation, vos passions..."
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none resize-none"
          />
        </div>
      </div>
    </div>
  );

  const renderCategories = () => (
    <div className="space-y-6 max-w-md mx-auto">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-yellow-400">VOTRE PARTICIPATION</h2>
        <p className="text-gray-500 text-sm mt-2">
          Sélectionnez une ou plusieurs catégories.
          Les questions s'adaptent à vos choix.
        </p>
      </div>

      <div className="space-y-4">
        {[
          {
            id: 'citoyen',
            icon: '🏛️',
            title: 'Citoyen',
            desc: 'Participez à la communauté, votez sur les besoins locaux, rejoignez le forum',
          },
          {
            id: 'collaborateur',
            icon: '🔬',
            title: 'Collaborateur',
            desc: 'Contribuez avec vos compétences professionnelles et rejoignez les équipes',
          },
          {
            id: 'investisseur',
            icon: '💎',
            title: 'Investisseur',
            desc: 'Soutenez le projet économiquement et recevez vos tokens et NFT',
          },
        ].map(cat => {
          const isSelected = formData.categories.includes(cat.id);
          return (
            <button
              key={cat.id}
              onClick={() => toggleArrayField('categories', cat.id)}
              className={`w-full flex items-center gap-4 p-5 rounded-xl border-2 transition-all text-left ${
                isSelected
                  ? 'bg-yellow-900/20 border-yellow-500/60 shadow-lg shadow-yellow-500/10'
                  : 'bg-black/30 border-gray-700 hover:border-gray-500'
              }`}
            >
              <span className="text-3xl">{cat.icon}</span>
              <div className="flex-1">
                <p className={`font-bold text-lg ${isSelected ? 'text-yellow-400' : 'text-gray-300'}`}>
                  {cat.title}
                </p>
                <p className="text-gray-500 text-sm">{cat.desc}</p>
              </div>
              <div className={`w-7 h-7 rounded-full border-2 flex items-center justify-center transition-all ${
                isSelected ? 'border-yellow-500 bg-yellow-500' : 'border-gray-600'
              }`}>
                {isSelected && (
                  <svg className="w-4 h-4 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>
            </button>
          );
        })}
      </div>

      {formData.categories.length === 0 && (
        <p className="text-gray-600 text-xs text-center">Sélectionnez au moins une catégorie pour continuer</p>
      )}
    </div>
  );

  const renderCitoyen = () => (
    <div className="space-y-6 max-w-md mx-auto">
      <div className="text-center">
        <div className="text-4xl mb-2">🏛️</div>
        <h2 className="text-2xl font-bold text-yellow-400">ESPACE CITOYEN</h2>
        <p className="text-gray-500 text-sm mt-2">Quels sont vos centres d'intérêt ?</p>
      </div>

      <div>
        <label className="block text-gray-400 text-sm mb-3">Domaines d'intérêt</label>
        <div className="flex flex-wrap gap-2">
          {['Santé', 'Éducation', 'Environnement', 'Économie', 'Culture', 'Technologie', 'Agriculture', 'Habitat', 'Énergie'].map(interest => {
            const isSelected = formData.interests?.includes(interest);
            return (
              <button
                key={interest}
                onClick={() => toggleArrayField('interests', interest)}
                className={`px-3 py-2 rounded-lg text-sm transition-all border ${
                  isSelected
                    ? 'bg-yellow-900/30 border-yellow-500/50 text-yellow-400'
                    : 'bg-black/30 border-gray-700 text-gray-400 hover:border-gray-500'
                }`}
              >
                {interest}
              </button>
            );
          })}
        </div>
      </div>

      <div>
        <label className="block text-gray-400 text-sm mb-1">Priorité locale</label>
        <select
          value={formData.local_needs_priority}
          onChange={(e) => updateField('local_needs_priority', e.target.value)}
          className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
        >
          <option value="">— Sélectionner —</option>
          <option value="sante">Santé et bien-être</option>
          <option value="education">Éducation et formation</option>
          <option value="environnement">Environnement et nature</option>
          <option value="economie">Économie locale</option>
          <option value="securite">Sécurité et communauté</option>
          <option value="culture">Culture et arts</option>
        </select>
      </div>
    </div>
  );

  const renderCollaborateur = () => (
    <div className="space-y-6 max-w-md mx-auto">
      <div className="text-center">
        <div className="text-4xl mb-2">🔬</div>
        <h2 className="text-2xl font-bold text-emerald-400">ESPACE COLLABORATEUR</h2>
        <p className="text-gray-500 text-sm mt-2">Parlez-nous de vos compétences</p>
      </div>

      <div>
        <label className="block text-gray-400 text-sm mb-1">Profession</label>
        <input
          type="text"
          value={formData.profession}
          onChange={(e) => updateField('profession', e.target.value)}
          placeholder="Ex: Développeur, Designer, Avocat..."
          className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
        />
      </div>

      <div>
        <label className="block text-gray-400 text-sm mb-3">Compétences</label>
        <div className="flex flex-wrap gap-2">
          {['Développement', 'Design', 'Marketing', 'Finance', 'Juridique', 'Gestion de projet', 'Communication', 'Recherche', 'Éducation', 'Santé', 'Agriculture', 'Ingénierie'].map(skill => {
            const isSelected = formData.skills?.includes(skill);
            return (
              <button
                key={skill}
                onClick={() => toggleArrayField('skills', skill)}
                className={`px-3 py-2 rounded-lg text-sm transition-all border ${
                  isSelected
                    ? 'bg-emerald-900/30 border-emerald-500/50 text-emerald-400'
                    : 'bg-black/30 border-gray-700 text-gray-400 hover:border-gray-500'
                }`}
              >
                {skill}
              </button>
            );
          })}
        </div>
      </div>

      <div>
        <label className="block text-gray-400 text-sm mb-1">Disponibilité</label>
        <select
          value={formData.availability}
          onChange={(e) => updateField('availability', e.target.value)}
          className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
        >
          <option value="">— Sélectionner —</option>
          <option value="full_time">Temps plein</option>
          <option value="part_time">Temps partiel</option>
          <option value="weekends">Fins de semaine</option>
          <option value="evenings">Soirées</option>
          <option value="flexible">Flexible / Ponctuel</option>
        </select>
      </div>

      <div>
        <label className="block text-gray-400 text-sm mb-1">Portfolio / LinkedIn (optionnel)</label>
        <input
          type="url"
          value={formData.portfolio_url}
          onChange={(e) => updateField('portfolio_url', e.target.value)}
          placeholder="https://..."
          className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
        />
      </div>
    </div>
  );

  const renderInvestisseur = () => {
    const tiers = [
      { id: 'etincelle', name: 'Étincelle', min: 10, max: 99, nft: 'Graine', icon: '✨' },
      { id: 'flamme', name: 'Flamme', min: 100, max: 499, nft: 'Pousse', icon: '🔥' },
      { id: 'feu', name: 'Feu', min: 500, max: 1999, nft: 'Branche', icon: '☀️' },
      { id: 'brasier', name: 'Brasier', min: 2000, max: 9999, nft: 'Racine', icon: '🌋' },
      { id: 'soleil', name: 'Soleil', min: 10000, max: null, nft: 'Arbre', icon: '🌟' },
    ];

    const flowTypes = [
      { id: 'tech', name: 'Technologie', icon: '💻' },
      { id: 'vie', name: 'Sciences de la Vie', icon: '🧬' },
      { id: 'sagesse', name: 'Sagesse & Éducation', icon: '📚' },
      { id: 'justice', name: 'Justice & Droit', icon: '⚖️' },
      { id: 'graine', name: 'Agriculture & Terre', icon: '🌱' },
      { id: 'terre', name: 'Environnement', icon: '🌍' },
    ];

    return (
      <div className="space-y-6 max-w-md mx-auto">
        <div className="text-center">
          <div className="text-4xl mb-2">💎</div>
          <h2 className="text-2xl font-bold text-purple-400">ESPACE INVESTISSEUR</h2>
          <p className="text-gray-500 text-sm mt-2">
            Choisissez votre niveau de contribution
          </p>
        </div>

        {/* Contribution Tiers */}
        <div>
          <label className="block text-gray-400 text-sm mb-3">Niveau de contribution</label>
          <div className="space-y-2">
            {tiers.map(tier => {
              const isSelected = formData.nft_tier === tier.id;
              return (
                <button
                  key={tier.id}
                  onClick={() => {
                    updateField('nft_tier', tier.id);
                    if (!formData.contribution_amount || parseFloat(formData.contribution_amount) < tier.min) {
                      updateField('contribution_amount', String(tier.min));
                    }
                  }}
                  className={`w-full flex items-center gap-3 p-4 rounded-lg border transition-all text-left ${
                    isSelected
                      ? 'bg-purple-900/20 border-purple-500/50'
                      : 'bg-black/30 border-gray-700 hover:border-gray-500'
                  }`}
                >
                  <span className="text-2xl">{tier.icon}</span>
                  <div className="flex-1">
                    <p className={`font-medium ${isSelected ? 'text-purple-400' : 'text-gray-300'}`}>
                      {tier.name}
                    </p>
                    <p className="text-gray-500 text-xs">
                      {tier.max ? `${tier.min}$ - ${tier.max}$` : `${tier.min}$+`} • NFT {tier.nft}
                    </p>
                  </div>
                  <div className={`w-5 h-5 rounded-full border-2 ${
                    isSelected ? 'border-purple-500 bg-purple-500' : 'border-gray-600'
                  }`} />
                </button>
              );
            })}
          </div>
        </div>

        {/* Amount */}
        {formData.nft_tier && (
          <div>
            <label className="block text-gray-400 text-sm mb-1">Montant (USD)</label>
            <div className="relative">
              <span className="absolute left-4 top-3 text-gray-500">$</span>
              <input
                type="number"
                value={formData.contribution_amount}
                onChange={(e) => updateField('contribution_amount', e.target.value)}
                min={tiers.find(t => t.id === formData.nft_tier)?.min || 10}
                className="w-full pl-8 pr-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-purple-500 focus:outline-none"
              />
            </div>
          </div>
        )}

        {/* Flow Direction */}
        <div>
          <label className="block text-gray-400 text-sm mb-3">
            Direction du flux (optionnel)
          </label>
          <div className="grid grid-cols-2 gap-2">
            {flowTypes.map(flow => {
              const isSelected = formData.flow_type === flow.id;
              return (
                <button
                  key={flow.id}
                  onClick={() => updateField('flow_type', isSelected ? '' : flow.id)}
                  className={`flex items-center gap-2 p-3 rounded-lg border text-sm transition-all ${
                    isSelected
                      ? 'bg-blue-900/20 border-blue-500/50 text-blue-400'
                      : 'bg-black/30 border-gray-700 text-gray-400 hover:border-gray-500'
                  }`}
                >
                  <span>{flow.icon}</span>
                  <span className="text-xs">{flow.name}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Personal Message */}
        <div>
          <label className="block text-gray-400 text-sm mb-1">Message personnel (optionnel)</label>
          <textarea
            value={formData.investment_message}
            onChange={(e) => updateField('investment_message', e.target.value)}
            rows={2}
            maxLength={500}
            placeholder="Votre message sera gravé dans la blockchain..."
            className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-purple-500 focus:outline-none resize-none"
          />
        </div>
      </div>
    );
  };

  const renderConfirmation = () => (
    <div className="space-y-6 max-w-md mx-auto text-center">
      {result?.success ? (
        <>
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-2xl font-bold text-yellow-400">BIENVENUE DANS L'ARCHE !</h2>
          <p className="text-gray-400">
            Votre inscription est complète.
            {formData.categories.includes('investisseur') && result.contribution && (
              <> Votre contribution a été enregistrée.</>
            )}
          </p>

          {result.contributionError && (
            <div className="p-3 bg-yellow-900/30 border border-yellow-500/30 rounded-lg text-yellow-400 text-sm">
              Note: Votre profil est sauvegardé. La contribution sera traitée ultérieurement.
            </div>
          )}

          <div className="space-y-3 pt-4">
            <button
              onClick={() => navigate('/profil')}
              className="w-full py-3 rounded-lg font-bold bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400 transition-all"
            >
              VOIR MON PROFIL
            </button>
            <button
              onClick={() => navigate('/progreso')}
              className="w-full py-3 rounded-lg font-medium border border-gray-700 text-gray-300 hover:border-yellow-500 hover:text-yellow-400 transition-all"
            >
              Explorer Progreso 2026
            </button>
          </div>
        </>
      ) : (
        <>
          <div className="text-6xl mb-4">📋</div>
          <h2 className="text-2xl font-bold text-yellow-400">RÉCAPITULATIF</h2>

          <div className="text-left bg-gray-900/50 rounded-xl p-6 border border-gray-800 space-y-4">
            <div>
              <span className="text-gray-500 text-xs">NOM</span>
              <p className="text-yellow-100">{formData.full_name || '—'}</p>
            </div>
            <div>
              <span className="text-gray-500 text-xs">CATÉGORIES</span>
              <p className="text-yellow-100">
                {formData.categories.map(c => c.charAt(0).toUpperCase() + c.slice(1)).join(', ') || '—'}
              </p>
            </div>
            {formData.categories.includes('collaborateur') && formData.profession && (
              <div>
                <span className="text-gray-500 text-xs">PROFESSION</span>
                <p className="text-yellow-100">{formData.profession}</p>
              </div>
            )}
            {formData.categories.includes('investisseur') && formData.contribution_amount && (
              <div>
                <span className="text-gray-500 text-xs">CONTRIBUTION</span>
                <p className="text-purple-400 font-bold">${formData.contribution_amount} USD</p>
              </div>
            )}
          </div>

          {errors.submit && (
            <p className="text-red-400 text-sm">{errors.submit}</p>
          )}

          <button
            onClick={handleSubmit}
            disabled={submitting}
            className={`w-full py-4 rounded-lg font-bold text-lg transition-all ${
              submitting
                ? 'bg-gray-800 text-gray-500'
                : 'bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400 shadow-lg'
            }`}
          >
            {submitting ? 'Inscription en cours...' : 'CONFIRMER L\'INSCRIPTION'}
          </button>
        </>
      )}
    </div>
  );

  // ═══════════════════════════════════════════════════════════════════════
  // MAIN RENDER
  // ═══════════════════════════════════════════════════════════════════════

  const stepRenderers = {
    [STEPS.WELCOME]: renderWelcome,
    [STEPS.AUTH]: renderAuth,
    [STEPS.IDENTITY]: renderIdentity,
    [STEPS.CATEGORIES]: renderCategories,
    [STEPS.CITOYEN]: renderCitoyen,
    [STEPS.COLLABORATEUR]: renderCollaborateur,
    [STEPS.INVESTISSEUR]: renderInvestisseur,
    [STEPS.CONFIRMATION]: renderConfirmation,
  };

  const canProceed = () => {
    if (step === STEPS.CATEGORIES) return formData.categories.length > 0;
    if (step === STEPS.INVESTISSEUR) return formData.nft_tier && formData.contribution_amount;
    return true;
  };

  const showNavButtons = step !== STEPS.WELCOME && step !== STEPS.CONFIRMATION;
  const isLastBeforeConfirm = () => {
    const steps = getSteps();
    const idx = steps.indexOf(step);
    return steps[idx + 1] === STEPS.CONFIRMATION;
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Progress Bar */}
      {step !== STEPS.WELCOME && (
        <div className="fixed top-0 left-0 right-0 z-50">
          <div className="h-1 bg-gray-800">
            <div
              className="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 transition-all duration-500"
              style={{ width: `${progress()}%` }}
            />
          </div>
        </div>
      )}

      {/* Content */}
      <div className="flex-1 flex items-center justify-center p-6 pt-8">
        <div className="w-full max-w-lg">
          {stepRenderers[step]?.()}
        </div>
      </div>

      {/* Navigation */}
      {showNavButtons && (
        <div className="fixed bottom-0 left-0 right-0 bg-black/90 backdrop-blur-md border-t border-gray-800 p-4">
          <div className="max-w-lg mx-auto flex justify-between items-center">
            <button
              onClick={prevStep}
              className="px-6 py-3 rounded-lg text-gray-400 hover:text-yellow-400 transition-colors"
            >
              ← Retour
            </button>

            {step !== STEPS.AUTH && (
              <button
                onClick={isLastBeforeConfirm() ? nextStep : nextStep}
                disabled={!canProceed()}
                className={`px-8 py-3 rounded-lg font-bold transition-all ${
                  canProceed()
                    ? 'bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400'
                    : 'bg-gray-800 text-gray-500 cursor-not-allowed'
                }`}
              >
                {isLastBeforeConfirm() ? 'Récapitulatif →' : 'Suivant →'}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default InscriptionPage;
