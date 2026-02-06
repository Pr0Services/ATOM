/**
 * ===============================================================================
 *
 *     ██████╗ ██████╗  ██████╗ ███████╗██╗██╗     ███████╗
 *     ██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║██║     ██╔════╝
 *     ██████╔╝██████╔╝██║   ██║█████╗  ██║██║     █████╗
 *     ██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║██║     ██╔══╝
 *     ██║     ██║  ██║╚██████╔╝██║     ██║███████╗███████╗
 *     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝
 *
 *                  USER PROFILE COMPONENT
 *           Affichage du profil avec données Supabase
 *                    CHE·NU V76 - AT·OM
 *
 * ===============================================================================
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { supabase, isSupabaseConfigured, ROLES } from '../lib/supabase';
import ArmorDisplay from './ArmorDisplay';

// ===============================================================================
// COMPOSANT: PROFILE CARD
// ===============================================================================

const ProfileCard = ({ profile, loading }) => {
  if (loading) {
    return (
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800 animate-pulse">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-gray-800" />
          <div className="flex-1">
            <div className="h-5 bg-gray-800 rounded w-32 mb-2" />
            <div className="h-4 bg-gray-800 rounded w-24" />
          </div>
        </div>
      </div>
    );
  }

  const roleColors = {
    souverain: { bg: 'bg-white/10', border: 'border-white/30', text: 'text-white' },
    collaborateur: { bg: 'bg-emerald-900/30', border: 'border-emerald-500/30', text: 'text-emerald-400' },
    citoyen: { bg: 'bg-yellow-900/30', border: 'border-yellow-500/30', text: 'text-yellow-400' }
  };

  const role = profile?.role || ROLES.CITOYEN;
  const colors = roleColors[role] || roleColors.citoyen;

  return (
    <div className={`rounded-xl p-6 border ${colors.bg} ${colors.border}`}>
      <div className="flex items-center gap-4">
        {/* Avatar */}
        <div className={`w-16 h-16 rounded-full flex items-center justify-center text-2xl
          bg-gradient-to-br from-yellow-600/30 to-black border-2 ${colors.border}`}>
          {profile?.avatar_url ? (
            <img
              src={profile.avatar_url}
              alt="Avatar"
              className="w-full h-full rounded-full object-cover"
            />
          ) : (
            <span>👤</span>
          )}
        </div>

        {/* Info */}
        <div className="flex-1">
          <h3 className={`text-lg font-bold ${colors.text}`}>
            {profile?.full_name || profile?.display_name || 'Utilisateur'}
          </h3>
          <p className="text-gray-500 text-sm">
            {profile?.email || 'Email non disponible'}
          </p>
          <div className="flex items-center gap-2 mt-2">
            <span className={`px-2 py-0.5 rounded text-xs ${colors.bg} ${colors.text} border ${colors.border}`}>
              {role.toUpperCase()}
            </span>
            {profile?.hedera_account_id && (
              <span className="px-2 py-0.5 rounded text-xs bg-purple-900/30 text-purple-400 border border-purple-500/30">
                {profile.hedera_account_id}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Stats */}
      {profile?.frequency && (
        <div className="mt-4 pt-4 border-t border-gray-800">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Fréquence</span>
            <span className="text-yellow-400 font-mono">{profile.frequency} Hz</span>
          </div>
        </div>
      )}
    </div>
  );
};

// ===============================================================================
// COMPOSANT: HEDERA ACCOUNT INFO
// ===============================================================================

const HederaAccountInfo = ({ accountId, network = 'testnet' }) => {
  if (!accountId) return null;

  return (
    <div className="bg-purple-900/20 rounded-xl p-4 border border-purple-500/30">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-purple-400 font-medium text-sm flex items-center gap-2">
            <span>💎</span> Compte Hedera
          </h4>
          <p className="text-gray-400 font-mono text-sm mt-1">{accountId}</p>
        </div>
        <a
          href={`https://hashscan.io/${network}/account/${accountId}`}
          target="_blank"
          rel="noopener noreferrer"
          className="px-3 py-1.5 bg-purple-600/30 text-purple-300 rounded-lg text-xs hover:bg-purple-600/50 transition-colors"
        >
          Explorer →
        </a>
      </div>
    </div>
  );
};

// ===============================================================================
// COMPOSANT PRINCIPAL: USER PROFILE
// ===============================================================================

const UserProfile = ({ showArmor = true, showHedera = true }) => {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch profile from Supabase
  useEffect(() => {
    const fetchProfile = async () => {
      if (!isSupabaseConfigured || !user?.id) {
        setLoading(false);
        return;
      }

      try {
        const { data, error } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', user.id)
          .single();

        if (error && error.code !== 'PGRST116') {
          console.error('[PROFILE] Erreur fetch:', error);
        }

        if (data) {
          setProfile(data);
        } else {
          // Use auth metadata as fallback
          setProfile({
            id: user.id,
            email: user.email,
            full_name: user.user_metadata?.display_name,
            display_name: user.user_metadata?.display_name,
            role: user.user_metadata?.role || ROLES.CITOYEN,
            frequency: user.user_metadata?.frequency || 444
          });
        }
      } catch (err) {
        console.error('[PROFILE] Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    if (!authLoading) {
      fetchProfile();
    }
  }, [user, authLoading]);

  // Not authenticated
  if (!authLoading && !isAuthenticated) {
    return (
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800 text-center">
        <span className="text-4xl mb-4 block">🔱</span>
        <h3 className="text-yellow-400 font-bold mb-2">Bienvenue dans l'Arche</h3>
        <p className="text-gray-500 text-sm mb-4">
          Connectez-vous pour accéder à votre profil et votre Armure Divine.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Profile Card */}
      <ProfileCard profile={profile} loading={loading || authLoading} />

      {/* Hedera Account */}
      {showHedera && profile?.hedera_account_id && (
        <HederaAccountInfo
          accountId={profile.hedera_account_id}
          network={process.env.REACT_APP_HEDERA_NETWORK || 'testnet'}
        />
      )}

      {/* Armor Display */}
      {showArmor && (
        <ArmorDisplay userId={user?.id} compact={false} />
      )}
    </div>
  );
};

// ===============================================================================
// COMPOSANT: PROFILE MINI (for header/sidebar)
// ===============================================================================

export const ProfileMini = () => {
  const { user, isAuthenticated, getRole } = useAuth();
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      if (!isSupabaseConfigured || !user?.id) return;

      try {
        const { data } = await supabase
          .from('profiles')
          .select('full_name, avatar_url, hedera_account_id')
          .eq('id', user.id)
          .single();

        if (data) setProfile(data);
      } catch (err) {
        console.error('[PROFILE_MINI] Erreur:', err);
      }
    };

    if (isAuthenticated) fetchProfile();
  }, [user, isAuthenticated]);

  if (!isAuthenticated) return null;

  const displayName = profile?.full_name ||
    user?.user_metadata?.display_name ||
    user?.email?.split('@')[0];

  return (
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-full bg-yellow-600/20 flex items-center justify-center text-sm">
        {profile?.avatar_url ? (
          <img src={profile.avatar_url} alt="" className="w-full h-full rounded-full object-cover" />
        ) : (
          <span>👤</span>
        )}
      </div>
      <div className="hidden md:block">
        <p className="text-yellow-400 text-sm font-medium truncate max-w-[120px]">
          {displayName}
        </p>
        <p className="text-gray-600 text-xs capitalize">
          {getRole()}
        </p>
      </div>
    </div>
  );
};

export default UserProfile;
