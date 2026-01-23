/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *       ██╗   ██╗███████╗ █████╗  ██████╗ ███████╗
 *       ██║   ██║██╔════╝██╔══██╗██╔════╝ ██╔════╝
 *       ██║   ██║███████╗███████║██║  ███╗█████╗
 *       ██║   ██║╚════██║██╔══██║██║   ██║██╔══╝
 *       ╚██████╔╝███████║██║  ██║╚██████╔╝███████╗
 *        ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
 *
 *              USAGE TRACKER - Visualisation des Credits de Resonance
 *                           AT.OM / CHE.NU V76
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const PLAN_COLORS = {
  citoyen: { primary: '#6B7280', secondary: '#374151' },
  fondateur: { primary: '#D4AF37', secondary: '#B8860B' },
  souverain: { primary: '#FFFFFF', secondary: '#E5E7EB' }
};

const PLAN_ICONS = {
  citoyen: '👤',
  fondateur: '🌟',
  souverain: '👑'
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: BARRE DE PROGRESSION
// ═══════════════════════════════════════════════════════════════════════════════

const ProgressBar = ({ value, max, color = '#D4AF37' }) => {
  const percent = max === -1 ? 0 : Math.min(100, (value / max) * 100);

  return (
    <div className="h-3 bg-gray-800 rounded-full overflow-hidden">
      <div
        className="h-full transition-all duration-500 rounded-full"
        style={{
          width: `${percent}%`,
          background: `linear-gradient(90deg, ${color}80, ${color})`
        }}
      />
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MINI USAGE (Widget compact)
// ═══════════════════════════════════════════════════════════════════════════════

export const MiniUsageWidget = () => {
  const { user } = useAuth();
  const [credits, setCredits] = useState(null);

  useEffect(() => {
    if (!user) return;

    const loadCredits = async () => {
      const { data } = await supabase.rpc('check_user_credits', {
        p_user_id: user.id
      });
      if (data) setCredits(data);
    };

    loadCredits();
  }, [user]);

  if (!credits) return null;

  const isUnlimited = credits.limit === -1;
  const percent = isUnlimited ? 0 : Math.round((credits.used / credits.limit) * 100);
  const planColor = PLAN_COLORS[credits.plan]?.primary || PLAN_COLORS.citoyen.primary;

  return (
    <div className="px-3 py-2 bg-black/30 rounded-lg border border-gray-800">
      <div className="flex items-center gap-2 mb-1">
        <span className="text-sm">{PLAN_ICONS[credits.plan]}</span>
        <span className="text-xs text-gray-400">Credits</span>
      </div>
      {isUnlimited ? (
        <div className="text-xs" style={{ color: planColor }}>Illimite</div>
      ) : (
        <>
          <ProgressBar value={credits.used} max={credits.limit} color={planColor} />
          <div className="text-xs text-gray-500 mt-1">
            {(credits.remaining / 1000).toFixed(0)}K restants
          </div>
        </>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: USAGE TRACKER COMPLET
// ═══════════════════════════════════════════════════════════════════════════════

const UsageTracker = ({ showHistory = true }) => {
  const { user } = useAuth();
  const [credits, setCredits] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    if (!user) return;

    setLoading(true);
    try {
      // Charger les credits
      const { data: creditsData } = await supabase.rpc('check_user_credits', {
        p_user_id: user.id
      });
      if (creditsData) setCredits(creditsData);

      // Charger l'historique recent
      if (showHistory) {
        const { data: historyData } = await supabase
          .from('api_requests')
          .select('*')
          .eq('user_id', user.id)
          .order('created_at', { ascending: false })
          .limit(20);

        if (historyData) setHistory(historyData);
      }
    } catch (err) {
      console.error('Erreur chargement usage:', err);
    } finally {
      setLoading(false);
    }
  }, [user, showHistory]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-32 bg-gray-800 rounded-xl" />
      </div>
    );
  }

  if (!credits) {
    return (
      <div className="text-center py-8 text-gray-500">
        Impossible de charger les donnees d'utilisation
      </div>
    );
  }

  const isUnlimited = credits.limit === -1;
  const planColor = PLAN_COLORS[credits.plan]?.primary || PLAN_COLORS.citoyen.primary;
  const percent = isUnlimited ? 0 : Math.round((credits.used / credits.limit) * 100);

  return (
    <div className="space-y-6">
      {/* Carte principale */}
      <div
        className="rounded-xl p-6 border"
        style={{
          background: `linear-gradient(135deg, ${planColor}10, transparent)`,
          borderColor: `${planColor}30`
        }}
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">{PLAN_ICONS[credits.plan]}</span>
              <h3 className="text-lg font-bold text-white capitalize">{credits.plan}</h3>
            </div>
            <p className="text-gray-400 text-sm">Credits de Resonance</p>
          </div>

          {!isUnlimited && (
            <div className="text-right">
              <div className="text-3xl font-bold" style={{ color: planColor }}>
                {percent}%
              </div>
              <div className="text-gray-500 text-sm">utilise</div>
            </div>
          )}
        </div>

        {isUnlimited ? (
          <div className="text-center py-4">
            <div className="text-4xl mb-2">∞</div>
            <div style={{ color: planColor }}>Credits Illimites</div>
          </div>
        ) : (
          <>
            <ProgressBar value={credits.used} max={credits.limit} color={planColor} />

            <div className="flex justify-between mt-3 text-sm">
              <div>
                <span className="text-gray-500">Utilise: </span>
                <span className="text-white">{(credits.used / 1000).toFixed(1)}K tokens</span>
              </div>
              <div>
                <span className="text-gray-500">Restant: </span>
                <span style={{ color: planColor }}>{(credits.remaining / 1000).toFixed(1)}K tokens</span>
              </div>
            </div>

            <div className="mt-3 text-xs text-gray-600 text-center">
              Renouvellement le 1er du mois
            </div>
          </>
        )}
      </div>

      {/* Statistiques rapides */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-black/50 rounded-lg p-4 border border-gray-800 text-center">
          <div className="text-2xl mb-1">🤖</div>
          <div className="text-white font-medium">{history.length}</div>
          <div className="text-gray-500 text-xs">Requetes recentes</div>
        </div>
        <div className="bg-black/50 rounded-lg p-4 border border-gray-800 text-center">
          <div className="text-2xl mb-1">⚡</div>
          <div className="text-white font-medium">
            {history.length > 0 ? Math.round(history.reduce((acc, r) => acc + (r.latency_ms || 0), 0) / history.length) : 0}ms
          </div>
          <div className="text-gray-500 text-xs">Latence moy.</div>
        </div>
        <div className="bg-black/50 rounded-lg p-4 border border-gray-800 text-center">
          <div className="text-2xl mb-1">🧠</div>
          <div className="text-white font-medium">
            {history.length > 0 ? [...new Set(history.map(r => r.model))].length : 0}
          </div>
          <div className="text-gray-500 text-xs">Modeles utilises</div>
        </div>
      </div>

      {/* Historique des requetes */}
      {showHistory && history.length > 0 && (
        <div className="bg-black/50 rounded-xl border border-gray-800">
          <div className="p-4 border-b border-gray-800">
            <h4 className="text-white font-medium">Historique Recent</h4>
          </div>
          <div className="max-h-64 overflow-y-auto">
            {history.map(request => (
              <div
                key={request.id}
                className="px-4 py-3 border-b border-gray-800/50 last:border-0 flex items-center gap-4"
              >
                <div className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center text-sm">
                  {request.model?.includes('claude') ? '🟣' : request.model?.includes('gpt') ? '🟢' : '🔵'}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-white text-sm truncate">{request.model}</div>
                  <div className="text-gray-500 text-xs">
                    {request.total_tokens} tokens
                    {request.latency_ms && ` • ${request.latency_ms}ms`}
                  </div>
                </div>
                <div className="text-gray-500 text-xs">
                  {new Date(request.created_at).toLocaleTimeString('fr-FR', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Info sur le plan */}
      {credits.plan === 'citoyen' && (
        <div className="bg-gradient-to-r from-yellow-900/20 to-yellow-600/10 border border-yellow-600/30 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <span className="text-2xl">🌟</span>
            <div>
              <h4 className="text-yellow-400 font-medium">Devenir Membre Fondateur</h4>
              <p className="text-gray-400 text-sm mt-1">
                Multiplie tes credits par 10 et accede a la Grid Energetique mondiale.
              </p>
              <a
                href="/invitation"
                className="inline-block mt-3 px-4 py-2 bg-yellow-600 text-black text-sm font-medium rounded-lg hover:bg-yellow-500"
              >
                En savoir plus
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UsageTracker;
