/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       █████╗  ██████╗ ██████╗██████╗ ███████╗██████╗ ██╗████████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
 *      ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
 *      ███████║██║     ██║     ██████╔╝█████╗  ██║  ██║██║   ██║   ███████║   ██║   ██║██║   ██║██╔██╗ ██║
 *      ██╔══██║██║     ██║     ██╔══██╗██╔══╝  ██║  ██║██║   ██║   ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
 *      ██║  ██║╚██████╗╚██████╗██║  ██║███████╗██████╔╝██║   ██║   ██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 *      ╚═╝  ╚═╝ ╚═════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
 *
 *                              🏛️ PORTAIL D'ACCRÉDITATION INSTITUTIONNELLE 🏛️
 *                          Filtre de Résonance pour Partenaires & Sous-traitants
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useCallback } from 'react';
import { useArithmos } from '../hooks/useArithmos';
import { useATOMContext } from '../App';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const ENTITY_TYPES = [
  { id: 'public_service', name: 'Service Public', icon: '🏛️', description: 'Municipalités, organismes gouvernementaux, PME MTL, Investissement Québec' },
  { id: 'enterprise', name: 'Entreprise Cliente', icon: '🏢', description: 'Entreprises privées souhaitant utiliser le moteur de résonance' },
  { id: 'subcontractor', name: 'Sous-traitant', icon: '🔧', description: 'Prestataires de services: entretien, construction, guides, énergie' }
];

const ROLE_MAPPING = {
  public_service: 'public_service_auth',
  enterprise: 'enterprise_client_auth',
  subcontractor: 'subcontractor_verified'
};

const SERVICE_CATEGORIES = [
  { id: 'entretien', name: 'Entretien Paysager', icon: '🌿' },
  { id: 'construction', name: 'Construction / Dômes', icon: '🏗️' },
  { id: 'energie', name: 'Énergie Renouvelable', icon: '⚡' },
  { id: 'transport', name: 'Transport / VTT', icon: '🚙' },
  { id: 'guide', name: 'Guide Touristique', icon: '🧭' },
  { id: 'restauration', name: 'Restauration', icon: '🍽️' },
  { id: 'securite', name: 'Sécurité', icon: '🛡️' },
  { id: 'technologie', name: 'Technologie / IT', icon: '💻' },
  { id: 'sante', name: 'Santé / Bien-être', icon: '🏥' },
  { id: 'juridique', name: 'Services Juridiques', icon: '⚖️' }
];

const REGIONS_QUEBEC = [
  'Montréal', 'Québec', 'Laval', 'Longueuil', 'Gatineau',
  'Sherbrooke', 'Trois-Rivières', 'Saguenay', 'Lévis',
  'Laurentides', 'Lanaudière', 'Montérégie', 'Estrie',
  'Mauricie', 'Outaouais', 'Abitibi-Témiscamingue',
  'Côte-Nord', 'Gaspésie', 'Bas-Saint-Laurent', 'Chaudière-Appalaches'
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CALCULATEUR ARITHMOS INTÉGRÉ
// ═══════════════════════════════════════════════════════════════════════════════

const ArithmosPreCheck = ({ entityName, onArithmosCalculated }) => {
  const { calculate } = useArithmos();
  const [result, setResult] = useState(null);

  const handleCalculate = useCallback(() => {
    if (!entityName.trim()) return;
    const arithmosResult = calculate(entityName);
    setResult(arithmosResult);
    onArithmosCalculated(arithmosResult.arithmos);
  }, [entityName, calculate, onArithmosCalculated]);

  return (
    <div className="bg-yellow-900/20 border border-yellow-600/30 rounded-xl p-4 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-yellow-400 font-bold flex items-center gap-2">
          <span>🔢</span>
          Alignement Fréquentiel (Arithmos)
        </h3>
        <button
          onClick={handleCalculate}
          disabled={!entityName.trim()}
          className={`px-4 py-2 rounded-lg text-sm transition-all ${
            entityName.trim()
              ? 'bg-yellow-600 text-black hover:bg-yellow-500'
              : 'bg-gray-800 text-gray-600 cursor-not-allowed'
          }`}
        >
          Calculer
        </button>
      </div>

      {result && (
        <div className="text-center py-4">
          <div className="text-5xl font-mono font-bold text-yellow-400 mb-2">
            {result.arithmos}
          </div>
          <div className="text-sm text-gray-400">
            Valeur numérique de "{entityName}"
          </div>
          <div className={`mt-3 text-sm ${
            result.arithmos % 9 === 0 ? 'text-emerald-400' :
            result.arithmos % 3 === 0 ? 'text-blue-400' : 'text-gray-400'
          }`}>
            {result.arithmos % 9 === 0
              ? '✨ Alignement parfait avec la Source (999)'
              : result.arithmos % 3 === 0
              ? '☯ Harmonie avec le Heartbeat (444)'
              : '○ Résonance neutre'}
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SÉLECTION DU TYPE D'ENTITÉ
// ═══════════════════════════════════════════════════════════════════════════════

const EntityTypeSelector = ({ selected, onSelect }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {ENTITY_TYPES.map(type => (
        <button
          key={type.id}
          onClick={() => onSelect(type.id)}
          className={`p-4 rounded-xl border-2 transition-all text-left ${
            selected === type.id
              ? 'border-yellow-500 bg-yellow-500/10'
              : 'border-gray-700 hover:border-gray-500 bg-black/30'
          }`}
        >
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">{type.icon}</span>
            <span className={`font-bold ${
              selected === type.id ? 'text-yellow-400' : 'text-white'
            }`}>
              {type.name}
            </span>
          </div>
          <p className="text-sm text-gray-500">{type.description}</p>
        </button>
      ))}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: FORMULAIRE D'ENGAGEMENT (PROOF OF RESONANCE)
// ═══════════════════════════════════════════════════════════════════════════════

const EngagementSection = ({ agreements, onToggle }) => {
  const engagements = [
    {
      id: 'frequency_charter',
      title: 'Charte Fréquentielle',
      description: 'Je m\'engage à respecter les fréquences 999 Hz (Source) et 444 Hz (Heartbeat) dans mes interventions avec l\'Arche.',
      icon: '🎵'
    },
    {
      id: 'sovereignty_declaration',
      title: 'Déclaration de Souveraineté',
      description: 'Je reconnais le Mode Souverain qui protège les découvertes et perceptions de l\'Architecte.',
      icon: '🛡️'
    },
    {
      id: 'ethics_agreement',
      title: 'Accord Éthique',
      description: 'Je m\'engage à agir dans l\'intérêt de la civilisation et à respecter la confidentialité des données de l\'Arche.',
      icon: '⚖️'
    }
  ];

  return (
    <div className="bg-black/30 border border-gray-700 rounded-xl p-4 mb-6">
      <h3 className="text-white font-bold mb-4 flex items-center gap-2">
        <span>📜</span>
        Engagements Fréquentiels (Proof of Resonance)
      </h3>

      <div className="space-y-4">
        {engagements.map(eng => (
          <label
            key={eng.id}
            className={`flex items-start gap-3 p-3 rounded-lg cursor-pointer transition-all ${
              agreements[eng.id]
                ? 'bg-emerald-500/10 border border-emerald-500/30'
                : 'bg-gray-900/50 border border-gray-700 hover:border-gray-500'
            }`}
          >
            <input
              type="checkbox"
              checked={agreements[eng.id] || false}
              onChange={() => onToggle(eng.id)}
              className="mt-1 w-5 h-5 rounded border-gray-600 bg-gray-800 text-emerald-500 focus:ring-emerald-500"
            />
            <div>
              <div className="flex items-center gap-2">
                <span>{eng.icon}</span>
                <span className={`font-medium ${
                  agreements[eng.id] ? 'text-emerald-400' : 'text-white'
                }`}>
                  {eng.title}
                </span>
              </div>
              <p className="text-sm text-gray-500 mt-1">{eng.description}</p>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SÉLECTION DES SERVICES (SOUS-TRAITANTS)
// ═══════════════════════════════════════════════════════════════════════════════

const ServiceSelector = ({ selected, onToggle }) => {
  return (
    <div className="bg-black/30 border border-gray-700 rounded-xl p-4 mb-6">
      <h3 className="text-white font-bold mb-4 flex items-center gap-2">
        <span>🔧</span>
        Services Offerts
      </h3>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
        {SERVICE_CATEGORIES.map(service => (
          <button
            key={service.id}
            onClick={() => onToggle(service.id)}
            className={`p-3 rounded-lg border transition-all text-center ${
              selected.includes(service.id)
                ? 'border-blue-500 bg-blue-500/10 text-blue-400'
                : 'border-gray-700 hover:border-gray-500 text-gray-400'
            }`}
          >
            <span className="text-2xl block mb-1">{service.icon}</span>
            <span className="text-xs">{service.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: INDICATEUR DE PROGRESSION
// ═══════════════════════════════════════════════════════════════════════════════

const ProgressIndicator = ({ formData, agreements }) => {
  const checkpoints = [
    { label: 'Type d\'entité', complete: !!formData.entityType },
    { label: 'Nom de l\'entité', complete: !!formData.entityName },
    { label: 'Contact', complete: !!formData.contactEmail },
    { label: 'Charte Fréquentielle', complete: agreements.frequency_charter },
    { label: 'Souveraineté', complete: agreements.sovereignty_declaration },
    { label: 'Éthique', complete: agreements.ethics_agreement }
  ];

  const completed = checkpoints.filter(c => c.complete).length;
  const percentage = Math.round((completed / checkpoints.length) * 100);

  return (
    <div className="bg-black/50 border border-yellow-900/30 rounded-xl p-4 mb-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-400">Progression du dossier</span>
        <span className="text-yellow-400 font-mono">{percentage}%</span>
      </div>
      <div className="h-2 bg-yellow-900/30 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-yellow-600 to-emerald-500 transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="flex flex-wrap gap-2 mt-3">
        {checkpoints.map((cp, i) => (
          <span
            key={i}
            className={`text-xs px-2 py-1 rounded ${
              cp.complete
                ? 'bg-emerald-500/20 text-emerald-400'
                : 'bg-gray-800 text-gray-500'
            }`}
          >
            {cp.complete ? '✓' : '○'} {cp.label}
          </span>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: PORTAIL D'ACCRÉDITATION
// ═══════════════════════════════════════════════════════════════════════════════

const AccreditationPage = () => {
  const { isArchitectMode } = useATOMContext();

  // État du formulaire
  const [formData, setFormData] = useState({
    entityType: '',
    entityName: '',
    registrationNumber: '',
    contactEmail: '',
    contactPhone: '',
    website: '',
    address: '',
    city: 'Montréal',
    region: 'Québec',
    postalCode: '',
    entityArithmos: null
  });

  // Engagements
  const [agreements, setAgreements] = useState({
    frequency_charter: false,
    sovereignty_declaration: false,
    ethics_agreement: false
  });

  // Services (pour sous-traitants)
  const [selectedServices, setSelectedServices] = useState([]);

  // État de soumission
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState(null);

  // Handlers
  const handleFieldChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleAgreementToggle = (id) => {
    setAgreements(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const handleServiceToggle = (id) => {
    setSelectedServices(prev =>
      prev.includes(id)
        ? prev.filter(s => s !== id)
        : [...prev, id]
    );
  };

  const handleArithmosCalculated = (value) => {
    setFormData(prev => ({ ...prev, entityArithmos: value }));
  };

  // Validation
  const isFormValid = () => {
    return (
      formData.entityType &&
      formData.entityName &&
      formData.contactEmail &&
      agreements.frequency_charter &&
      agreements.sovereignty_declaration &&
      agreements.ethics_agreement
    );
  };

  // Soumission
  const handleSubmit = async () => {
    if (!isFormValid()) return;

    setIsSubmitting(true);

    // Simuler l'envoi (à connecter avec Supabase)
    const accreditationData = {
      ...formData,
      requested_role: ROLE_MAPPING[formData.entityType],
      services_offered: selectedServices,
      frequency_charter_signed: agreements.frequency_charter,
      sovereignty_declaration: agreements.sovereignty_declaration,
      ethics_agreement: agreements.ethics_agreement,
      frequency_alignment: formData.entityArithmos % 9 === 0 ? 999 : 444,
      status: 'pending'
    };

    // Sauvegarder en localStorage pour le moment
    try {
      const stored = JSON.parse(localStorage.getItem('atom_accreditations') || '[]');
      stored.push({
        ...accreditationData,
        id: Date.now(),
        created_at: new Date().toISOString()
      });
      localStorage.setItem('atom_accreditations', JSON.stringify(stored));

      setSubmitResult({
        success: true,
        message: 'Votre demande d\'accréditation a été soumise avec succès. Elle sera analysée par nos 287 agents.'
      });
    } catch (e) {
      setSubmitResult({
        success: false,
        message: 'Erreur lors de la soumission. Veuillez réessayer.'
      });
    }

    setIsSubmitting(false);
  };

  // Affichage du résultat
  if (submitResult) {
    return (
      <div className="flex flex-col min-h-[70vh] px-4">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-yellow-500 mb-2">
            🏛️ ACCRÉDITATION
          </h1>
          <p className="text-gray-500">Portail de Résonance Institutionnelle</p>
        </div>

        <div className={`max-w-2xl mx-auto p-8 rounded-xl border-2 ${
          submitResult.success
            ? 'bg-emerald-500/10 border-emerald-500'
            : 'bg-red-500/10 border-red-500'
        }`}>
          <div className="text-center">
            <span className="text-6xl mb-4 block">
              {submitResult.success ? '✅' : '❌'}
            </span>
            <h2 className={`text-2xl font-bold mb-4 ${
              submitResult.success ? 'text-emerald-400' : 'text-red-400'
            }`}>
              {submitResult.success ? 'Demande Soumise' : 'Erreur'}
            </h2>
            <p className="text-gray-300 mb-6">{submitResult.message}</p>

            {submitResult.success && (
              <div className="bg-black/30 rounded-lg p-4 text-left">
                <p className="text-sm text-gray-400 mb-2">Prochaines étapes:</p>
                <ol className="text-sm text-gray-300 space-y-2">
                  <li>1. Les agents L4-L6 analysent votre dossier</li>
                  <li>2. Calcul du score de validation automatique</li>
                  <li>3. Révision par le Souverain si nécessaire</li>
                  <li>4. Notification de votre statut par courriel</li>
                </ol>
              </div>
            )}

            <button
              onClick={() => {
                setSubmitResult(null);
                setFormData({
                  entityType: '',
                  entityName: '',
                  registrationNumber: '',
                  contactEmail: '',
                  contactPhone: '',
                  website: '',
                  address: '',
                  city: 'Montréal',
                  region: 'Québec',
                  postalCode: '',
                  entityArithmos: null
                });
                setAgreements({
                  frequency_charter: false,
                  sovereignty_declaration: false,
                  ethics_agreement: false
                });
                setSelectedServices([]);
              }}
              className="mt-6 px-6 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 transition-all"
            >
              Nouvelle Demande
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-[70vh] px-4">
      {/* Titre */}
      <div className="text-center mb-8">
        <h1 className={`text-3xl font-bold tracking-widest mb-2 ${
          isArchitectMode ? 'text-white' : 'text-yellow-500'
        }`}>
          🏛️ PORTAIL D'ACCRÉDITATION
        </h1>
        <p className="text-gray-500">Filtre de Résonance pour Partenaires Institutionnels</p>
      </div>

      {/* Indicateur de progression */}
      <ProgressIndicator formData={formData} agreements={agreements} />

      {/* Étape 1: Type d'entité */}
      <div className="mb-6">
        <h2 className="text-lg font-bold text-white mb-3">1. Type d'Entité</h2>
        <EntityTypeSelector
          selected={formData.entityType}
          onSelect={(type) => handleFieldChange('entityType', type)}
        />
      </div>

      {/* Étape 2: Informations de base */}
      {formData.entityType && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-white mb-3">2. Informations de l'Entité</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Nom de l'entité *</label>
              <input
                type="text"
                value={formData.entityName}
                onChange={(e) => handleFieldChange('entityName', e.target.value)}
                placeholder="Ex: PME MTL, Éco-Dômes Québec..."
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">NEQ / Numéro d'entreprise</label>
              <input
                type="text"
                value={formData.registrationNumber}
                onChange={(e) => handleFieldChange('registrationNumber', e.target.value)}
                placeholder="1234567890"
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Courriel de contact *</label>
              <input
                type="email"
                value={formData.contactEmail}
                onChange={(e) => handleFieldChange('contactEmail', e.target.value)}
                placeholder="contact@entreprise.ca"
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Téléphone</label>
              <input
                type="tel"
                value={formData.contactPhone}
                onChange={(e) => handleFieldChange('contactPhone', e.target.value)}
                placeholder="514-555-1234"
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Ville</label>
              <input
                type="text"
                value={formData.city}
                onChange={(e) => handleFieldChange('city', e.target.value)}
                placeholder="Montréal"
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Région</label>
              <select
                value={formData.region}
                onChange={(e) => handleFieldChange('region', e.target.value)}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-yellow-500"
              >
                {REGIONS_QUEBEC.map(r => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Site Web</label>
              <input
                type="url"
                value={formData.website}
                onChange={(e) => handleFieldChange('website', e.target.value)}
                placeholder="https://..."
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>
          </div>
        </div>
      )}

      {/* Étape 3: Alignement Arithmos */}
      {formData.entityName && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-white mb-3">3. Alignement Fréquentiel</h2>
          <ArithmosPreCheck
            entityName={formData.entityName}
            onArithmosCalculated={handleArithmosCalculated}
          />
        </div>
      )}

      {/* Étape 4: Services (sous-traitants uniquement) */}
      {formData.entityType === 'subcontractor' && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-white mb-3">4. Services Offerts</h2>
          <ServiceSelector
            selected={selectedServices}
            onToggle={handleServiceToggle}
          />
        </div>
      )}

      {/* Étape 5: Engagements */}
      {formData.entityType && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-white mb-3">
            {formData.entityType === 'subcontractor' ? '5' : '4'}. Engagements Fréquentiels
          </h2>
          <EngagementSection
            agreements={agreements}
            onToggle={handleAgreementToggle}
          />
        </div>
      )}

      {/* Bouton de soumission */}
      <div className="text-center pb-8">
        <button
          onClick={handleSubmit}
          disabled={!isFormValid() || isSubmitting}
          className={`px-8 py-4 rounded-xl font-bold text-lg transition-all ${
            isFormValid() && !isSubmitting
              ? 'bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400 shadow-lg shadow-yellow-500/30'
              : 'bg-gray-800 text-gray-600 cursor-not-allowed'
          }`}
        >
          {isSubmitting ? (
            <span className="flex items-center gap-2">
              <span className="animate-spin">⏳</span>
              Analyse en cours...
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <span>🏛️</span>
              Soumettre la Demande d'Accréditation
            </span>
          )}
        </button>

        {!isFormValid() && formData.entityType && (
          <p className="text-sm text-gray-500 mt-3">
            Complétez tous les champs obligatoires et acceptez les engagements pour soumettre.
          </p>
        )}
      </div>
    </div>
  );
};

export default AccreditationPage;
