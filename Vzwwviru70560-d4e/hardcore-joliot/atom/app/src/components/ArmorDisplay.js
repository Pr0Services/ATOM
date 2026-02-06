/**
 * ===============================================================================
 *
 *      █████╗ ██████╗ ███╗   ███╗ ██████╗ ██████╗
 *     ██╔══██╗██╔══██╗████╗ ████║██╔═══██╗██╔══██╗
 *     ███████║██████╔╝██╔████╔██║██║   ██║██████╔╝
 *     ██╔══██║██╔══██╗██║╚██╔╝██║██║   ██║██╔══██╗
 *     ██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝██║  ██║
 *     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝
 *
 *                  ARMOR DISPLAY COMPONENT
 *               Affichage de l'AT-OM : Back to Light
 *                    CHE·NU V76 - AT·OM
 *
 * ===============================================================================
 */

import React, { useState, useEffect } from 'react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';

// Sacred Values from environment
const SACRED_VALUES = {
  M: process.env.REACT_APP_ATOM_M || '44.4',
  P: process.env.REACT_APP_ATOM_P || '161.8',
  I: process.env.REACT_APP_ATOM_I || '369',
  Po: process.env.REACT_APP_ATOM_PO || '1728'
};

const HEDERA_TOKEN_ID = process.env.REACT_APP_HEDERA_TOKEN_ID || '0.0.7780104';
const HEDERA_NETWORK = process.env.REACT_APP_HEDERA_NETWORK || 'testnet';

// ===============================================================================
// COMPOSANT: SACRED VALUE DISPLAY
// ===============================================================================

const SacredValue = ({ label, value, description, color }) => (
  <div className="flex flex-col items-center p-3 bg-black/30 rounded-lg border border-gray-800">
    <span className="text-xs text-gray-500 mb-1">{label}</span>
    <span className={`text-2xl font-bold ${color}`}>{value}</span>
    <span className="text-xs text-gray-600 mt-1 text-center">{description}</span>
  </div>
);

// ===============================================================================
// COMPOSANT: ARMOR IMAGE
// ===============================================================================

const ArmorImage = ({ imageUrl, isLoading }) => {
  const [error, setError] = useState(false);

  if (isLoading) {
    return (
      <div className="w-full aspect-square bg-gray-900/50 rounded-xl flex items-center justify-center">
        <div className="animate-pulse text-gray-600">
          <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1}
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>
    );
  }

  if (error || !imageUrl) {
    return (
      <div className="w-full aspect-square bg-gradient-to-br from-yellow-900/20 to-black rounded-xl flex flex-col items-center justify-center border border-yellow-600/30">
        <span className="text-6xl mb-4">🛡️</span>
        <span className="text-yellow-500 text-sm">AT-OM : Back to Light</span>
        <span className="text-gray-600 text-xs mt-1">NFT #{HEDERA_TOKEN_ID}</span>
      </div>
    );
  }

  return (
    <div className="w-full aspect-square rounded-xl overflow-hidden border border-yellow-600/30">
      <img
        src={imageUrl}
        alt="AT-OM : Back to Light"
        className="w-full h-full object-cover"
        onError={() => setError(true)}
      />
    </div>
  );
};

// ===============================================================================
// COMPOSANT: HEDERA BADGE
// ===============================================================================

const HederaBadge = ({ tokenId, network }) => (
  <a
    href={`https://hashscan.io/${network}/token/${tokenId}`}
    target="_blank"
    rel="noopener noreferrer"
    className="inline-flex items-center gap-2 px-3 py-1.5 bg-purple-900/30 border border-purple-500/30 rounded-lg
      hover:bg-purple-900/50 transition-all group"
  >
    <span className="text-purple-400 text-sm">HEDERA</span>
    <span className="text-gray-500 text-xs font-mono">{tokenId}</span>
    <svg className="w-4 h-4 text-purple-400 group-hover:translate-x-0.5 transition-transform"
      fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
    </svg>
  </a>
);

// ===============================================================================
// COMPOSANT PRINCIPAL: ARMOR DISPLAY
// ===============================================================================

const ArmorDisplay = ({ userId, compact = false }) => {
  const [armor, setArmor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [imageUrl, setImageUrl] = useState(null);

  // Fetch armor data from Supabase
  useEffect(() => {
    const fetchArmor = async () => {
      if (!isSupabaseConfigured) {
        setLoading(false);
        return;
      }

      try {
        // Fetch from armors table
        const { data, error } = await supabase
          .from('armors')
          .select('*')
          .eq('token_id', HEDERA_TOKEN_ID)
          .single();

        if (error && error.code !== 'PGRST116') {
          console.error('[ARMOR] Erreur fetch:', error);
        }

        if (data) {
          setArmor(data);

          // Try to get image from storage bucket
          if (data.image_path) {
            const { data: urlData } = supabase.storage
              .from('zama-assets')
              .getPublicUrl(data.image_path);

            if (urlData?.publicUrl) {
              setImageUrl(urlData.publicUrl);
            }
          }
        }
      } catch (err) {
        console.error('[ARMOR] Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchArmor();
  }, [userId]);

  // Compact view for sidebar/cards
  if (compact) {
    return (
      <div className="bg-gray-900/50 rounded-xl p-4 border border-yellow-600/20">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-lg overflow-hidden bg-gradient-to-br from-yellow-900/30 to-black flex items-center justify-center">
            {imageUrl ? (
              <img src={imageUrl} alt="Armor" className="w-full h-full object-cover" />
            ) : (
              <span className="text-2xl">🛡️</span>
            )}
          </div>
          <div className="flex-1">
            <h4 className="text-yellow-400 font-medium text-sm">AT-OM : Back to Light</h4>
            <p className="text-gray-500 text-xs mt-0.5">NFT Hedera #{HEDERA_TOKEN_ID.split('.').pop()}</p>
            <div className="flex gap-2 mt-2">
              <span className="px-2 py-0.5 bg-yellow-900/30 text-yellow-500 text-xs rounded">
                M: {SACRED_VALUES.M}
              </span>
              <span className="px-2 py-0.5 bg-purple-900/30 text-purple-400 text-xs rounded">
                {HEDERA_NETWORK}
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Full display
  return (
    <div className="bg-gradient-to-b from-gray-900/80 to-black rounded-2xl p-6 border border-yellow-600/30">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-yellow-400 flex items-center gap-2">
            <span>🛡️</span> AT-OM : Back to Light
          </h3>
          <p className="text-gray-500 text-sm mt-1">
            Triple Sceau: Physique + Fréquentiel + Numérique
          </p>
        </div>
        <HederaBadge tokenId={HEDERA_TOKEN_ID} network={HEDERA_NETWORK} />
      </div>

      {/* Image */}
      <div className="mb-6">
        <ArmorImage imageUrl={imageUrl} isLoading={loading} />
      </div>

      {/* Sacred Values Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <SacredValue
          label="M (Masse)"
          value={SACRED_VALUES.M}
          description="444/10"
          color="text-yellow-400"
        />
        <SacredValue
          label="P (Phi)"
          value={SACRED_VALUES.P}
          description="Phi × 100"
          color="text-emerald-400"
        />
        <SacredValue
          label="I (Tesla)"
          value={SACRED_VALUES.I}
          description="3-6-9"
          color="text-blue-400"
        />
        <SacredValue
          label="Po (Cube)"
          value={SACRED_VALUES.Po}
          description="12³"
          color="text-purple-400"
        />
      </div>

      {/* Biometric Hash */}
      {armor?.biometric_hash && (
        <div className="p-4 bg-black/50 rounded-xl border border-gray-800">
          <p className="text-xs text-gray-500 mb-2">Hash Biométrique SHA-256</p>
          <p className="font-mono text-xs text-gray-400 break-all">
            {armor.biometric_hash}
          </p>
        </div>
      )}

      {/* Status */}
      <div className="mt-6 flex items-center justify-between text-sm">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-gray-400">NFT Actif</span>
        </div>
        <span className="text-gray-600">
          Serial #{armor?.serial || '1'}
        </span>
      </div>
    </div>
  );
};

export default ArmorDisplay;
