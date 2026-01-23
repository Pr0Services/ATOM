/* ═══════════════════════════════════════════════════════════════════════════════
 *
 *       ██╗███╗   ██╗██╗   ██╗██╗████████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
 *       ██║████╗  ██║██║   ██║██║╚══██╔══╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
 *       ██║██╔██╗ ██║██║   ██║██║   ██║   ███████║   ██║   ██║██║   ██║██╔██╗ ██║
 *       ██║██║╚██╗██║╚██╗ ██╔╝██║   ██║   ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
 *       ██║██║ ╚████║ ╚████╔╝ ██║   ██║   ██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 *       ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
 *
 *                    PORTAIL D'INVITATION - MEMBRES FONDATEURS
 *                  Points de Lumiere Internationaux - AT.OM / CHE.NU V76
 *
 * ═══════════════════════════════════════════════════════════════════════════════ */

import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const FOUNDER_TYPES = {
  lumiere: {
    name: 'Point de Lumiere',
    icon: '🌟',
    color: '#FFD700',
    description: 'Porteur de lumiere internationale, ambassadeur de la vision'
  },
  gardien: {
    name: 'Gardien de l\'Arche',
    icon: '🛡️',
    color: '#4A90D9',
    description: 'Protecteur des valeurs et de l\'integrite du systeme'
  },
  architecte: {
    name: 'Architecte de Civilisation',
    icon: '🏛️',
    color: '#9B59B6',
    description: 'Batisseur de structures et de fondations durables'
  },
  tisserand: {
    name: 'Tisserand de Liens',
    icon: '🕸️',
    color: '#2ECC71',
    description: 'Createur de connexions et de synergies entre membres'
  },
  porteur: {
    name: 'Porteur de Flamme',
    icon: '🔥',
    color: '#E74C3C',
    description: 'Gardien de l\'energie et de la passion collective'
  }
};

const ELEMENTS = [
  { id: 'feu', name: 'Feu', icon: '🔥', color: '#E74C3C' },
  { id: 'eau', name: 'Eau', icon: '💧', color: '#3498DB' },
  { id: 'terre', name: 'Terre', icon: '🌍', color: '#8B4513' },
  { id: 'air', name: 'Air', icon: '💨', color: '#BDC3C7' },
  { id: 'ether', name: 'Ether', icon: '✨', color: '#9B59B6' }
];

// Signatures energetiques disponibles
const ENERGY_SIGNATURES = [
  { value: 111, name: 'Eveil', description: 'Debut du chemin spirituel' },
  { value: 222, name: 'Equilibre', description: 'Harmonie et partenariat' },
  { value: 333, name: 'Guidance', description: 'Protection des maitres' },
  { value: 444, name: 'Heartbeat', description: 'Frequence cardiaque de l\'Arche' },
  { value: 528, name: 'Amour', description: 'Frequence de transformation' },
  { value: 639, name: 'Connexion', description: 'Harmonisation relationnelle' },
  { value: 741, name: 'Expression', description: 'Eveil de l\'intuition' },
  { value: 852, name: 'Vision', description: 'Retour a l\'ordre spirituel' },
  { value: 963, name: 'Unite', description: 'Connexion a la Source' },
  { value: 999, name: 'Source', description: 'Frequence souveraine' }
];

// Types de contribution
const CONTRIBUTION_TYPES = [
  { id: 'energetic', name: 'Energetique', icon: '✨', description: 'Contribution energetique pure' },
  { id: 'material', name: 'Materiel', icon: '💎', description: 'Ressources materielles' },
  { id: 'scientific', name: 'Scientifique', icon: '🔬', description: 'Expertise technique' },
  { id: 'creative', name: 'Creatif', icon: '🎨', description: 'Arts et creation' },
  { id: 'healing', name: 'Guerison', icon: '💚', description: 'Bien-etre et sante' },
  { id: 'bridge', name: 'Pont', icon: '🌉', description: 'Connexion entre mondes' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: PORTAIL D'INVITATION
// ═══════════════════════════════════════════════════════════════════════════════

const InvitationPortal = ({ onComplete }) => {
  const { user } = useAuth();

  // Etapes du portail
  const [step, setStep] = useState('code'); // code | welcome | profile | complete
  const [invitationCode, setInvitationCode] = useState('');
  const [invitation, setInvitation] = useState(null);
  const [founderData, setFounderData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Donnees du profil fondateur
  const [profile, setProfile] = useState({
    story: '',
    intention: '',
    gifts: [],
    seeking: [],
    location_country: '',
    location_city: '',
    element: '',
    spirit_animal: '',
    // Grid energetique
    grid_latitude: null,
    grid_longitude: null,
    grid_location_name: '',
    energy_signature: 444,
    contribution_type: 'energetic'
  });

  // Etat pour la geolocalisation
  const [geoLoading, setGeoLoading] = useState(false);
  const [geoError, setGeoError] = useState('');

  const [giftInput, setGiftInput] = useState('');
  const [seekingInput, setSeekingInput] = useState('');

  // ═══════════════════════════════════════════════════════════════════════════════
  // VERIFICATION DU CODE
  // ═══════════════════════════════════════════════════════════════════════════════

  const verifyCode = useCallback(async () => {
    if (!invitationCode.trim()) {
      setError('Veuillez entrer votre code d\'invitation');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const { data, error: rpcError } = await supabase.rpc('verify_invitation_code', {
        invitation_code: invitationCode.trim().toUpperCase()
      });

      if (rpcError) throw rpcError;

      if (data?.valid) {
        setInvitation(data);
        setStep('welcome');
      } else {
        setError('Code d\'invitation invalide, expire ou deja utilise');
      }
    } catch (err) {
      console.error('Erreur verification:', err);
      setError('Erreur lors de la verification du code');
    } finally {
      setLoading(false);
    }
  }, [invitationCode]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // ACCEPTATION DE L'INVITATION
  // ═══════════════════════════════════════════════════════════════════════════════

  const acceptInvitation = useCallback(async () => {
    if (!user) {
      setError('Vous devez etre connecte pour accepter l\'invitation');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const { data, error: rpcError } = await supabase.rpc('use_invitation_code', {
        invitation_code: invitationCode.trim().toUpperCase()
      });

      if (rpcError) throw rpcError;

      if (data?.success) {
        setFounderData(data);
        setStep('profile');
      } else {
        setError(data?.error || 'Erreur lors de l\'acceptation');
      }
    } catch (err) {
      console.error('Erreur acceptation:', err);
      setError('Erreur lors de l\'acceptation de l\'invitation');
    } finally {
      setLoading(false);
    }
  }, [user, invitationCode]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // SAUVEGARDE DU PROFIL FONDATEUR
  // ═══════════════════════════════════════════════════════════════════════════════

  const saveFounderProfile = useCallback(async () => {
    if (!user) return;

    setLoading(true);
    setError('');

    try {
      const { error: updateError } = await supabase
        .from('founders')
        .update({
          story: profile.story,
          intention: profile.intention,
          gifts: profile.gifts,
          seeking: profile.seeking,
          location_country: profile.location_country,
          location_city: profile.location_city,
          element: profile.element || null,
          spirit_animal: profile.spirit_animal,
          // Grid energetique
          grid_latitude: profile.grid_latitude,
          grid_longitude: profile.grid_longitude,
          grid_location_name: profile.grid_location_name,
          energy_signature: profile.energy_signature,
          contribution_type: profile.contribution_type,
          updated_at: new Date().toISOString()
        })
        .eq('user_id', user.id);

      if (updateError) throw updateError;

      setStep('complete');

      // Notifier le parent apres un delai
      setTimeout(() => {
        onComplete?.();
      }, 5000);
    } catch (err) {
      console.error('Erreur sauvegarde profil:', err);
      setError('Erreur lors de la sauvegarde du profil');
    } finally {
      setLoading(false);
    }
  }, [user, profile, onComplete]);

  // ═══════════════════════════════════════════════════════════════════════════════
  // GESTION DES TAGS (DONS ET RECHERCHES)
  // ═══════════════════════════════════════════════════════════════════════════════

  const addGift = () => {
    if (giftInput.trim() && !profile.gifts.includes(giftInput.trim())) {
      setProfile(prev => ({
        ...prev,
        gifts: [...prev.gifts, giftInput.trim()]
      }));
      setGiftInput('');
    }
  };

  const removeGift = (gift) => {
    setProfile(prev => ({
      ...prev,
      gifts: prev.gifts.filter(g => g !== gift)
    }));
  };

  const addSeeking = () => {
    if (seekingInput.trim() && !profile.seeking.includes(seekingInput.trim())) {
      setProfile(prev => ({
        ...prev,
        seeking: [...prev.seeking, seekingInput.trim()]
      }));
      setSeekingInput('');
    }
  };

  const removeSeeking = (item) => {
    setProfile(prev => ({
      ...prev,
      seeking: prev.seeking.filter(s => s !== item)
    }));
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // GEOLOCALISATION POUR LA GRID
  // ═══════════════════════════════════════════════════════════════════════════════

  const requestGeolocation = useCallback(() => {
    if (!navigator.geolocation) {
      setGeoError('Geolocalisation non supportee par votre navigateur');
      return;
    }

    setGeoLoading(true);
    setGeoError('');

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;

        setProfile(prev => ({
          ...prev,
          grid_latitude: latitude,
          grid_longitude: longitude
        }));

        // Essayer de geocoder l'adresse (reverse geocoding)
        try {
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`
          );
          const data = await response.json();

          if (data.address) {
            const city = data.address.city || data.address.town || data.address.village || '';
            const country = data.address.country || '';

            setProfile(prev => ({
              ...prev,
              grid_location_name: city ? `${city}, ${country}` : country,
              location_city: city,
              location_country: country
            }));
          }
        } catch (err) {
          console.warn('Reverse geocoding failed:', err);
        }

        setGeoLoading(false);
      },
      (error) => {
        console.error('Geolocation error:', error);
        setGeoError('Impossible d\'obtenir votre position. Vous pouvez entrer manuellement.');
        setGeoLoading(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDU: ETAPE CODE
  // ═══════════════════════════════════════════════════════════════════════════════

  if (step === 'code') {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          {/* En-tete */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🌟</div>
            <h1 className="text-2xl font-bold text-white mb-2">
              Portail des Fondateurs
            </h1>
            <p className="text-gray-400">
              Bienvenue, ame resonante. Entre ton code d'invitation pour rejoindre
              le cercle des membres fondateurs.
            </p>
          </div>

          {/* Formulaire */}
          <div className="bg-gradient-to-b from-gray-900 to-black border border-yellow-600/30 rounded-2xl p-6">
            <div className="mb-4">
              <label className="block text-gray-400 text-sm mb-2">
                Code d'Invitation
              </label>
              <input
                type="text"
                value={invitationCode}
                onChange={(e) => setInvitationCode(e.target.value.toUpperCase())}
                placeholder="ATOM-XXXX-XXXX"
                className="w-full px-4 py-4 bg-black/50 border border-yellow-900/50 rounded-lg
                  text-yellow-100 text-center text-xl tracking-widest font-mono
                  placeholder-gray-600 focus:outline-none focus:border-yellow-500"
                maxLength={14}
              />
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-900/30 border border-red-500/50 rounded-lg">
                <p className="text-red-400 text-sm text-center">{error}</p>
              </div>
            )}

            <button
              onClick={verifyCode}
              disabled={loading || !invitationCode.trim()}
              className="w-full py-4 bg-gradient-to-r from-yellow-600 to-yellow-500
                text-black font-bold rounded-lg hover:from-yellow-500 hover:to-yellow-400
                transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Verification...' : 'Verifier le Code'}
            </button>
          </div>

          {/* Message d'aide */}
          <p className="text-center text-gray-600 text-sm mt-6">
            Tu as recu ce code personnellement du Souverain.
            <br />
            Si tu n'as pas de code, l'acces n'est pas encore ouvert pour toi.
          </p>
        </div>
      </div>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDU: ETAPE BIENVENUE
  // ═══════════════════════════════════════════════════════════════════════════════

  if (step === 'welcome') {
    const founderType = FOUNDER_TYPES[invitation?.founder_type] || FOUNDER_TYPES.lumiere;

    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="max-w-lg w-full">
          {/* Animation d'accueil */}
          <div className="text-center mb-8">
            <div className="text-8xl mb-4 animate-pulse">{founderType.icon}</div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Bienvenue, {invitation?.invited_name}
            </h1>
            <p className="text-xl" style={{ color: founderType.color }}>
              {founderType.name}
            </p>
          </div>

          {/* Message personnel */}
          {invitation?.personal_message && (
            <div className="bg-gradient-to-b from-gray-900 to-black border border-yellow-600/30 rounded-2xl p-6 mb-6">
              <div className="flex items-start gap-3">
                <span className="text-2xl">💌</span>
                <div>
                  <p className="text-gray-400 text-sm mb-2">Message du Souverain:</p>
                  <p className="text-yellow-100 italic">"{invitation.personal_message}"</p>
                </div>
              </div>
            </div>
          )}

          {/* Description du role */}
          <div className="bg-black/50 border border-gray-800 rounded-xl p-6 mb-6">
            <h3 className="text-white font-medium mb-2">Ton Role dans l'Arche</h3>
            <p className="text-gray-400 text-sm">{founderType.description}</p>
          </div>

          {/* Bouton accepter */}
          {!user ? (
            <div className="text-center">
              <p className="text-gray-400 mb-4">
                Pour accepter cette invitation, tu dois d'abord te connecter ou creer un compte.
              </p>
              <a
                href="/entree"
                className="inline-block px-6 py-3 bg-yellow-600 text-black font-bold rounded-lg
                  hover:bg-yellow-500 transition-colors"
              >
                Se Connecter / S'inscrire
              </a>
            </div>
          ) : (
            <div>
              {error && (
                <div className="mb-4 p-3 bg-red-900/30 border border-red-500/50 rounded-lg">
                  <p className="text-red-400 text-sm text-center">{error}</p>
                </div>
              )}

              <button
                onClick={acceptInvitation}
                disabled={loading}
                className="w-full py-4 bg-gradient-to-r from-yellow-600 to-yellow-500
                  text-black font-bold text-lg rounded-lg hover:from-yellow-500 hover:to-yellow-400
                  transition-all disabled:opacity-50"
              >
                {loading ? 'Activation...' : 'Accepter et Rejoindre le Cercle'}
              </button>

              <p className="text-center text-gray-500 text-sm mt-4">
                En acceptant, tu deviens membre fondateur #{invitation?.founder_number || '?'}
              </p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDU: ETAPE PROFIL
  // ═══════════════════════════════════════════════════════════════════════════════

  if (step === 'profile') {
    return (
      <div className="min-h-screen bg-black py-8 px-4">
        <div className="max-w-2xl mx-auto">
          {/* En-tete */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-yellow-600/20 rounded-full mb-4">
              <span className="text-yellow-500">Fondateur #{founderData?.founder_number}</span>
            </div>
            <h1 className="text-2xl font-bold text-white mb-2">
              Presente-toi au Cercle
            </h1>
            <p className="text-gray-400">
              Partage qui tu es pour que la communaute puisse te connaitre.
            </p>
          </div>

          {/* Formulaire de profil */}
          <div className="space-y-6">
            {/* Histoire */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                🌱 Ton Histoire
              </label>
              <p className="text-gray-500 text-sm mb-3">
                Partage ton parcours, ce qui t'a amene ici, ta connexion avec le projet.
              </p>
              <textarea
                value={profile.story}
                onChange={(e) => setProfile(p => ({ ...p, story: e.target.value }))}
                placeholder="Je suis..."
                rows={4}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg
                  text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500
                  resize-none"
              />
            </div>

            {/* Intention */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                🎯 Ton Intention
              </label>
              <p className="text-gray-500 text-sm mb-3">
                Quelle est ton intention en rejoignant cette communaute?
              </p>
              <textarea
                value={profile.intention}
                onChange={(e) => setProfile(p => ({ ...p, intention: e.target.value }))}
                placeholder="Mon intention est de..."
                rows={3}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg
                  text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500
                  resize-none"
              />
            </div>

            {/* Dons et talents */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                🎁 Tes Dons a Partager
              </label>
              <p className="text-gray-500 text-sm mb-3">
                Quels talents, competences ou ressources peux-tu offrir a la communaute?
              </p>
              <div className="flex gap-2 mb-3">
                <input
                  type="text"
                  value={giftInput}
                  onChange={(e) => setGiftInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addGift()}
                  placeholder="Ajouter un don..."
                  className="flex-1 px-4 py-2 bg-black/50 border border-gray-700 rounded-lg
                    text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
                />
                <button
                  onClick={addGift}
                  className="px-4 py-2 bg-yellow-600 text-black rounded-lg hover:bg-yellow-500"
                >
                  +
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {profile.gifts.map((gift, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1 px-3 py-1 bg-yellow-600/20
                      text-yellow-400 rounded-full text-sm"
                  >
                    {gift}
                    <button
                      onClick={() => removeGift(gift)}
                      className="ml-1 text-yellow-600 hover:text-yellow-300"
                    >
                      x
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Ce que tu cherches */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                🔍 Ce que Tu Cherches
              </label>
              <p className="text-gray-500 text-sm mb-3">
                Qu'esperes-tu trouver ou recevoir de cette communaute?
              </p>
              <div className="flex gap-2 mb-3">
                <input
                  type="text"
                  value={seekingInput}
                  onChange={(e) => setSeekingInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addSeeking()}
                  placeholder="Ajouter..."
                  className="flex-1 px-4 py-2 bg-black/50 border border-gray-700 rounded-lg
                    text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
                />
                <button
                  onClick={addSeeking}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500"
                >
                  +
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {profile.seeking.map((item, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1 px-3 py-1 bg-blue-600/20
                      text-blue-400 rounded-full text-sm"
                  >
                    {item}
                    <button
                      onClick={() => removeSeeking(item)}
                      className="ml-1 text-blue-600 hover:text-blue-300"
                    >
                      x
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* ═══════════════════════════════════════════════════════════════════ */}
            {/* SECTION GRID ENERGETIQUE */}
            {/* ═══════════════════════════════════════════════════════════════════ */}

            <div className="border-t border-yellow-600/30 pt-6 mt-6">
              <h2 className="text-xl font-bold text-yellow-500 mb-4 flex items-center gap-2">
                🌐 Position dans la Grid Energetique
              </h2>
              <p className="text-gray-400 text-sm mb-6">
                Ta position geographique te connectera a la Grid planetaire des Points de Lumiere.
              </p>
            </div>

            {/* Geolocalisation */}
            <div className="bg-gradient-to-r from-yellow-900/20 to-yellow-600/10 border border-yellow-600/30 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                📍 Point d'Ancrage sur la Grid
              </label>
              <p className="text-gray-500 text-sm mb-4">
                Ta position geographique servira de point d'ancrage pour la Grid energetique mondiale.
              </p>

              {/* Bouton de geolocalisation */}
              <button
                type="button"
                onClick={requestGeolocation}
                disabled={geoLoading}
                className="w-full py-3 mb-4 bg-yellow-600/20 border border-yellow-600/50 text-yellow-400
                  rounded-lg hover:bg-yellow-600/30 transition-colors disabled:opacity-50
                  flex items-center justify-center gap-2"
              >
                {geoLoading ? (
                  <>
                    <span className="animate-spin">🌀</span>
                    Detection en cours...
                  </>
                ) : (
                  <>
                    <span>🛰️</span>
                    Detecter Ma Position Automatiquement
                  </>
                )}
              </button>

              {geoError && (
                <p className="text-red-400 text-sm mb-4">{geoError}</p>
              )}

              {/* Coordonnees detectees ou manuelles */}
              {profile.grid_latitude && profile.grid_longitude && (
                <div className="bg-black/30 rounded-lg p-4 mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400 text-sm">Coordonnees:</span>
                    <span className="text-green-400 text-sm">Detecte</span>
                  </div>
                  <div className="font-mono text-yellow-400">
                    {profile.grid_latitude.toFixed(4)}, {profile.grid_longitude.toFixed(4)}
                  </div>
                  {profile.grid_location_name && (
                    <div className="text-gray-300 mt-2">
                      {profile.grid_location_name}
                    </div>
                  )}
                </div>
              )}

              {/* Saisie manuelle de la localisation */}
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  value={profile.location_country}
                  onChange={(e) => setProfile(p => ({ ...p, location_country: e.target.value }))}
                  placeholder="Pays"
                  className="px-4 py-2 bg-black/50 border border-gray-700 rounded-lg
                    text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
                />
                <input
                  type="text"
                  value={profile.location_city}
                  onChange={(e) => setProfile(p => ({ ...p, location_city: e.target.value }))}
                  placeholder="Ville"
                  className="px-4 py-2 bg-black/50 border border-gray-700 rounded-lg
                    text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
                />
              </div>
            </div>

            {/* Signature Energetique */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                🔊 Ta Signature Energetique
              </label>
              <p className="text-gray-500 text-sm mb-4">
                Quelle frequence resonne le plus avec ton etre? Elle sera calibree par le Souverain.
              </p>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                {ENERGY_SIGNATURES.map(sig => (
                  <button
                    key={sig.value}
                    type="button"
                    onClick={() => setProfile(p => ({ ...p, energy_signature: sig.value }))}
                    className={`p-3 rounded-xl border transition-all text-center ${
                      profile.energy_signature === sig.value
                        ? 'bg-yellow-600/20 border-yellow-500 text-yellow-400'
                        : 'bg-black/30 border-gray-700 hover:border-gray-600 text-gray-400'
                    }`}
                  >
                    <div className="text-lg font-bold">{sig.value}</div>
                    <div className="text-xs opacity-75">{sig.name}</div>
                  </button>
                ))}
              </div>
              <p className="text-gray-600 text-xs mt-3 text-center">
                Note: Ta signature sera validee et potentiellement ajustee lors de ton activation dans la Grid.
              </p>
            </div>

            {/* Type de Contribution */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                🤝 Type de Contribution
              </label>
              <p className="text-gray-500 text-sm mb-4">
                Comment contribues-tu principalement a la communaute?
              </p>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {CONTRIBUTION_TYPES.map(ct => (
                  <button
                    key={ct.id}
                    type="button"
                    onClick={() => setProfile(p => ({ ...p, contribution_type: ct.id }))}
                    className={`p-4 rounded-xl border transition-all text-left ${
                      profile.contribution_type === ct.id
                        ? 'bg-purple-600/20 border-purple-500'
                        : 'bg-black/30 border-gray-700 hover:border-gray-600'
                    }`}
                  >
                    <div className="text-2xl mb-1">{ct.icon}</div>
                    <div className={`font-medium ${
                      profile.contribution_type === ct.id ? 'text-purple-400' : 'text-gray-300'
                    }`}>
                      {ct.name}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">{ct.description}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Element */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                ✨ Ton Element
              </label>
              <p className="text-gray-500 text-sm mb-3">
                Avec quel element te sens-tu le plus en resonance?
              </p>
              <div className="grid grid-cols-5 gap-2">
                {ELEMENTS.map(el => (
                  <button
                    key={el.id}
                    onClick={() => setProfile(p => ({ ...p, element: el.id }))}
                    className={`p-4 rounded-xl border transition-all ${
                      profile.element === el.id
                        ? 'bg-gray-800 border-yellow-500'
                        : 'bg-black/30 border-gray-700 hover:border-gray-600'
                    }`}
                  >
                    <div className="text-2xl mb-1">{el.icon}</div>
                    <div className="text-xs text-gray-400">{el.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Animal totem */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <label className="block text-white font-medium mb-2">
                🦁 Ton Animal Totem
              </label>
              <p className="text-gray-500 text-sm mb-3">
                Quel animal represente ton esprit? (optionnel)
              </p>
              <input
                type="text"
                value={profile.spirit_animal}
                onChange={(e) => setProfile(p => ({ ...p, spirit_animal: e.target.value }))}
                placeholder="Ex: Loup, Aigle, Papillon..."
                className="w-full px-4 py-2 bg-black/50 border border-gray-700 rounded-lg
                  text-white placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>

            {/* Erreur */}
            {error && (
              <div className="p-3 bg-red-900/30 border border-red-500/50 rounded-lg">
                <p className="text-red-400 text-sm text-center">{error}</p>
              </div>
            )}

            {/* Bouton sauvegarder */}
            <button
              onClick={saveFounderProfile}
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-yellow-600 to-yellow-500
                text-black font-bold text-lg rounded-lg hover:from-yellow-500 hover:to-yellow-400
                transition-all disabled:opacity-50"
            >
              {loading ? 'Sauvegarde...' : 'Completer Mon Profil Fondateur'}
            </button>

            <p className="text-center text-gray-500 text-sm">
              Tu pourras modifier ces informations plus tard
            </p>
          </div>
        </div>
      </div>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDU: ETAPE COMPLETE
  // ═══════════════════════════════════════════════════════════════════════════════

  if (step === 'complete') {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="max-w-lg w-full text-center">
          {/* Animation de celebration */}
          <div className="relative mb-8">
            <div className="text-8xl animate-bounce">🎉</div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-32 h-32 rounded-full bg-yellow-500/20 animate-ping" />
            </div>
          </div>

          <h1 className="text-3xl font-bold text-white mb-4">
            Bienvenue dans le Cercle!
          </h1>

          <p className="text-xl text-yellow-500 mb-6">
            Fondateur #{founderData?.founder_number}
          </p>

          <div className="bg-gradient-to-b from-gray-900 to-black border border-yellow-600/30 rounded-2xl p-6 mb-8">
            <p className="text-gray-300 leading-relaxed">
              Tu fais maintenant partie des premiers membres fondateurs de cette
              nouvelle civilisation. Ta presence, ton energie et ta contribution
              sont precieuses.
            </p>
          </div>

          <div className="space-y-4">
            <a
              href="/cercle"
              className="block w-full py-4 bg-gradient-to-r from-yellow-600 to-yellow-500
                text-black font-bold rounded-lg hover:from-yellow-500 hover:to-yellow-400
                transition-all"
            >
              Entrer dans le Cercle des Fondateurs
            </a>

            <a
              href="/tableau-de-bord"
              className="block w-full py-3 bg-gray-800 text-gray-300
                rounded-lg hover:bg-gray-700 transition-colors"
            >
              Aller au Tableau de Bord
            </a>
          </div>

          <p className="text-gray-600 text-sm mt-8">
            Redirection automatique dans quelques secondes...
          </p>
        </div>
      </div>
    );
  }

  return null;
};

export default InvitationPortal;
