/**
 * AT·OM — Page Profil Utilisateur
 * Auto-remplissage depuis OAuth, gestion du profil, connexion de comptes sociaux
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { supabase, isSupabaseConfigured, uploadAvatar, updateProfile, linkSocialAccount } from '../lib/supabase';
import SocialAuthButtons from '../components/SocialAuthButtons';

// ═══════════════════════════════════════════════════════════════════════════════
// PROFIL PAGE
// ═══════════════════════════════════════════════════════════════════════════════

const ProfilPage = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, loading: authLoading, logout } = useAuth();

  const [profile, setProfile] = useState({
    full_name: '',
    email: '',
    phone: '',
    avatar_url: '',
    bio: '',
    location: '',
    role: 'citoyen',
    categories: [],
    hedera_account_id: '',
    facebook_url: '',
    youtube_channel_url: '',
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);
  const [linkedProviders, setLinkedProviders] = useState([]);

  // ─── Fetch profile on mount ─────────────────────────────────────────

  useEffect(() => {
    if (authLoading) return;

    if (!isAuthenticated) {
      navigate('/entree');
      return;
    }

    const fetchProfile = async () => {
      try {
        // Récupérer les providers liés
        const identities = user?.identities || [];
        setLinkedProviders(identities.map(i => i.provider));

        // Récupérer le profil Supabase
        if (isSupabaseConfigured && user?.id) {
          const { data, error } = await supabase
            .from('profiles')
            .select('*')
            .eq('id', user.id)
            .single();

          if (data) {
            setProfile(prev => ({
              ...prev,
              ...data,
              email: user.email || data.email || '',
            }));
          } else {
            // Auto-fill from OAuth metadata
            const meta = user.user_metadata || {};
            setProfile(prev => ({
              ...prev,
              full_name: meta.full_name || meta.name || meta.display_name || '',
              email: user.email || '',
              avatar_url: meta.avatar_url || meta.picture || '',
              role: meta.role || 'citoyen',
            }));
          }
        }
      } catch (err) {
        console.error('[PROFIL] Erreur chargement:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [user, authLoading, isAuthenticated, navigate]);

  // ─── Save profile ───────────────────────────────────────────────────

  const handleSave = useCallback(async () => {
    if (!user?.id) return;
    setSaving(true);
    setMessage(null);

    try {
      const result = await updateProfile(user.id, {
        full_name: profile.full_name,
        phone: profile.phone,
        bio: profile.bio,
        location: profile.location,
        avatar_url: profile.avatar_url,
        facebook_url: profile.facebook_url,
        youtube_channel_url: profile.youtube_channel_url,
        categories: profile.categories,
      });

      if (result.success) {
        setMessage({ type: 'success', text: 'Profil sauvegardé avec succès' });
      } else {
        setMessage({ type: 'error', text: result.error || 'Erreur de sauvegarde' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setSaving(false);
    }
  }, [user, profile]);

  // ─── Avatar upload ──────────────────────────────────────────────────

  const handleAvatarUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file || !user?.id) return;

    if (file.size > 2 * 1024 * 1024) {
      setMessage({ type: 'error', text: 'Image trop grande (max 2 Mo)' });
      return;
    }

    try {
      const result = await uploadAvatar(user.id, file);
      if (result.success) {
        setProfile(prev => ({ ...prev, avatar_url: result.url }));
        setMessage({ type: 'success', text: 'Avatar mis à jour' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Erreur upload avatar' });
    }
  };

  // ─── Link social account success ───────────────────────────────────

  const handleLinkSuccess = (provider) => {
    setLinkedProviders(prev => [...prev, provider]);
    setMessage({ type: 'success', text: `Compte ${provider} connecté` });
  };

  // ─── Categories toggle ─────────────────────────────────────────────

  const toggleCategory = (cat) => {
    setProfile(prev => ({
      ...prev,
      categories: prev.categories?.includes(cat)
        ? prev.categories.filter(c => c !== cat)
        : [...(prev.categories || []), cat],
    }));
  };

  // ─── Loading state ─────────────────────────────────────────────────

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-yellow-400 animate-pulse text-lg">Chargement du profil...</div>
      </div>
    );
  }

  // ─── Render ─────────────────────────────────────────────────────────

  const roleLabels = {
    citoyen: { label: 'Citoyen', color: 'text-yellow-400 bg-yellow-900/30 border-yellow-500/30' },
    collaborateur: { label: 'Collaborateur', color: 'text-emerald-400 bg-emerald-900/30 border-emerald-500/30' },
    souverain: { label: 'Souverain', color: 'text-white bg-white/10 border-white/30' },
  };

  const categories = ['citoyen', 'collaborateur', 'investisseur'];

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="bg-gradient-to-b from-gray-900 to-black border-b border-yellow-900/30">
        <div className="max-w-2xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate(-1)}
              className="text-gray-400 hover:text-yellow-400 transition-colors"
            >
              ← Retour
            </button>
            <h1 className="text-xl font-bold text-yellow-400 tracking-wider">MON PROFIL</h1>
            <button
              onClick={logout}
              className="text-gray-500 hover:text-red-400 text-sm transition-colors"
            >
              Déconnexion
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 py-8 space-y-8">
        {/* Message */}
        {message && (
          <div className={`p-3 rounded-lg text-sm text-center border ${
            message.type === 'success'
              ? 'bg-emerald-900/30 border-emerald-500/30 text-emerald-400'
              : 'bg-red-900/30 border-red-500/30 text-red-400'
          }`}>
            {message.text}
          </div>
        )}

        {/* ═══ Avatar & Role ═══ */}
        <div className="flex items-center gap-6">
          {/* Avatar */}
          <div className="relative group">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-yellow-600/30 to-black border-2 border-yellow-600/50 overflow-hidden flex items-center justify-center text-4xl">
              {profile.avatar_url ? (
                <img src={profile.avatar_url} alt="Avatar" className="w-full h-full object-cover" />
              ) : (
                <span>👤</span>
              )}
            </div>
            <label className="absolute inset-0 flex items-center justify-center bg-black/60 rounded-full opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity">
              <span className="text-yellow-400 text-xs">Changer</span>
              <input type="file" accept="image/*" onChange={handleAvatarUpload} className="hidden" />
            </label>
          </div>

          {/* Name & Role */}
          <div className="flex-1">
            <h2 className="text-xl font-bold text-yellow-400">
              {profile.full_name || 'Nouveau Citoyen'}
            </h2>
            <p className="text-gray-500 text-sm">{profile.email}</p>
            <div className="mt-2">
              <span className={`px-3 py-1 rounded-lg text-xs border ${roleLabels[profile.role]?.color || roleLabels.citoyen.color}`}>
                {roleLabels[profile.role]?.label || 'Citoyen'}
              </span>
            </div>
          </div>
        </div>

        {/* ═══ Informations Personnelles ═══ */}
        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
          <h3 className="text-yellow-400 font-bold mb-4 text-sm tracking-wider">INFORMATIONS</h3>

          <div className="space-y-4">
            <div>
              <label className="block text-gray-400 text-sm mb-1">Nom complet</label>
              <input
                type="text"
                value={profile.full_name}
                onChange={(e) => setProfile(p => ({ ...p, full_name: e.target.value }))}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
                placeholder="Votre nom"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1">Email</label>
              <input
                type="email"
                value={profile.email}
                disabled
                className="w-full px-4 py-3 bg-black/30 border border-gray-800 rounded-lg text-gray-500 cursor-not-allowed"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1">Téléphone</label>
              <input
                type="tel"
                value={profile.phone || ''}
                onChange={(e) => setProfile(p => ({ ...p, phone: e.target.value }))}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
                placeholder="+1 (514) 000-0000"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1">Localisation</label>
              <input
                type="text"
                value={profile.location || ''}
                onChange={(e) => setProfile(p => ({ ...p, location: e.target.value }))}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none"
                placeholder="Ville, Province/État"
              />
            </div>

            <div>
              <label className="block text-gray-400 text-sm mb-1">Bio</label>
              <textarea
                value={profile.bio || ''}
                onChange={(e) => setProfile(p => ({ ...p, bio: e.target.value }))}
                rows={3}
                maxLength={500}
                className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-yellow-100 focus:border-yellow-500 focus:outline-none resize-none"
                placeholder="Quelques mots sur vous..."
              />
            </div>
          </div>
        </div>

        {/* ═══ Catégories de Participation ═══ */}
        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
          <h3 className="text-yellow-400 font-bold mb-4 text-sm tracking-wider">MES RÔLES</h3>
          <p className="text-gray-500 text-xs mb-4">Sélectionnez vos catégories de participation</p>

          <div className="space-y-3">
            {categories.map(cat => {
              const isSelected = profile.categories?.includes(cat);
              const catInfo = {
                citoyen: { icon: '🏛️', label: 'Citoyen', desc: 'Participer à la communauté locale' },
                collaborateur: { icon: '🔬', label: 'Collaborateur', desc: 'Contribuer avec vos compétences' },
                investisseur: { icon: '💎', label: 'Investisseur', desc: 'Soutenir le développement économique' },
              };

              return (
                <button
                  key={cat}
                  onClick={() => toggleCategory(cat)}
                  className={`w-full flex items-center gap-4 p-4 rounded-lg border transition-all text-left ${
                    isSelected
                      ? 'bg-yellow-900/20 border-yellow-500/50'
                      : 'bg-black/30 border-gray-700 hover:border-gray-600'
                  }`}
                >
                  <span className="text-2xl">{catInfo[cat].icon}</span>
                  <div className="flex-1">
                    <p className={`font-medium ${isSelected ? 'text-yellow-400' : 'text-gray-300'}`}>
                      {catInfo[cat].label}
                    </p>
                    <p className="text-gray-500 text-xs">{catInfo[cat].desc}</p>
                  </div>
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
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
        </div>

        {/* ═══ Comptes Connectés ═══ */}
        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
          <h3 className="text-yellow-400 font-bold mb-4 text-sm tracking-wider">COMPTES CONNECTÉS</h3>

          {/* Providers liés */}
          <div className="space-y-2 mb-4">
            {['email', 'facebook', 'google', 'apple'].map(provider => {
              const isLinked = provider === 'email' ? true : linkedProviders.includes(provider);
              const icons = {
                email: '📧',
                facebook: '📘',
                google: '🔵',
                apple: '🍎',
              };

              return (
                <div key={provider} className="flex items-center justify-between py-2 px-3 rounded-lg bg-black/30">
                  <div className="flex items-center gap-3">
                    <span>{icons[provider]}</span>
                    <span className="text-gray-300 text-sm capitalize">{provider}</span>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded ${
                    isLinked
                      ? 'text-emerald-400 bg-emerald-900/30'
                      : 'text-gray-500'
                  }`}>
                    {isLinked ? 'Connecté' : 'Non connecté'}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Link new accounts */}
          <SocialAuthButtons
            mode="link"
            compact={true}
            showDivider={false}
            onSuccess={handleLinkSuccess}
            onError={(provider, err) => setMessage({ type: 'error', text: `Erreur: ${err}` })}
          />
        </div>

        {/* ═══ Hedera Wallet ═══ */}
        {profile.hedera_account_id && (
          <div className="bg-purple-900/20 rounded-xl p-6 border border-purple-500/30">
            <h3 className="text-purple-400 font-bold mb-4 text-sm tracking-wider">COMPTE HEDERA</h3>
            <div className="flex items-center justify-between">
              <span className="text-gray-400 font-mono text-sm">{profile.hedera_account_id}</span>
              <a
                href={`https://hashscan.io/${process.env.REACT_APP_HEDERA_NETWORK || 'testnet'}/account/${profile.hedera_account_id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-purple-400 text-xs hover:text-purple-300"
              >
                Explorer →
              </a>
            </div>
          </div>
        )}

        {/* ═══ Save Button ═══ */}
        <button
          onClick={handleSave}
          disabled={saving}
          className={`w-full py-4 rounded-lg font-bold text-lg transition-all ${
            saving
              ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-yellow-600 to-yellow-500 text-black hover:from-yellow-500 hover:to-yellow-400 shadow-lg shadow-yellow-600/20'
          }`}
        >
          {saving ? 'Sauvegarde...' : 'SAUVEGARDER MON PROFIL'}
        </button>

        {/* ═══ Navigation vers inscription progressive ═══ */}
        {profile.categories?.includes('investisseur') && (
          <button
            onClick={() => navigate('/inscription')}
            className="w-full py-3 rounded-lg font-medium text-sm bg-gradient-to-r from-purple-600 to-purple-500 text-white hover:from-purple-500 hover:to-purple-400 transition-all"
          >
            💎 Compléter mon parcours Investisseur
          </button>
        )}
      </div>
    </div>
  );
};

export default ProfilPage;
