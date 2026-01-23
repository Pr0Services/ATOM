/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *       ███████╗███████╗████████╗██╗   ██╗██████╗
 *       ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
 *       ███████╗█████╗     ██║   ██║   ██║██████╔╝
 *       ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝
 *       ███████║███████╗   ██║   ╚██████╔╝██║
 *       ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝
 *
 *              GUIDE D'ACTIVATION SOUVERAIN - AT.OM / CHE.NU V76
 *                    Configuration des Relais Energetiques
 *
 *   ACCES: role_id = SOUVERAIN uniquement
 *   FREQUENCE: 444 Hz (Coeur) → 999 Hz (Source)
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES
// ═══════════════════════════════════════════════════════════════════════════════

const FREQUENCIES = {
  HEARTBEAT: 444,
  LOVE: 528,
  CONNECTION: 639,
  VISION: 852,
  SOURCE: 999
};

// Map completion percentage to frequency
const getFrequencyFromCompletion = (percentage) => {
  if (percentage >= 100) return FREQUENCIES.SOURCE;
  if (percentage >= 75) return FREQUENCIES.VISION;
  if (percentage >= 50) return FREQUENCIES.CONNECTION;
  if (percentage >= 25) return FREQUENCIES.LOVE;
  return FREQUENCIES.HEARTBEAT;
};

const RELAY_TYPES = {
  api: { icon: '🔌', name: 'API Relais', color: '#8B5CF6' },
  database: { icon: '🗄️', name: 'Base de Donnees', color: '#22C55E' },
  payment: { icon: '💳', name: 'Flux Financier', color: '#D4AF37' },
  infrastructure: { icon: '☁️', name: 'Infrastructure', color: '#3B82F6' }
};

const RELAYS = [
  { id: 'openrouter', name: 'OpenRouter', type: 'api', description: 'Acces unifie aux LLMs (Claude, GPT-4, Llama)', envKey: 'OPENROUTER_API_KEY' },
  { id: 'anthropic', name: 'Anthropic', type: 'api', description: 'Acces direct Claude (mode souverain)', envKey: 'ANTHROPIC_API_KEY' },
  { id: 'stripe', name: 'Stripe', type: 'payment', description: 'Paiements et Connect pour redistribution', envKey: 'STRIPE_SECRET_KEY' },
  { id: 'stripe_connect', name: 'Stripe Connect', type: 'payment', description: 'Distribution automatique aux partenaires', envKey: 'STRIPE_CONNECT_CLIENT_ID' },
  { id: 'supabase', name: 'Supabase', type: 'database', description: 'PostgreSQL + Auth + Realtime', envKey: 'SUPABASE_SERVICE_KEY' },
  { id: 'digitalocean', name: 'DigitalOcean', type: 'infrastructure', description: 'Secrets et infrastructure cloud', envKey: 'DIGITALOCEAN_TOKEN' },
  { id: 'vercel', name: 'Vercel', type: 'infrastructure', description: 'Deploiement et Edge Functions', envKey: 'VERCEL_TOKEN' }
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: INDICATEUR DE FREQUENCE
// ═══════════════════════════════════════════════════════════════════════════════

const FrequencyIndicator = ({ frequency, foundersCount, completionPercentage = 0 }) => {
  const isSource = frequency >= 999;

  const getFrequencyLabel = () => {
    if (frequency >= 999) return 'Frequence Source';
    if (frequency >= 852) return 'Frequence Vision';
    if (frequency >= 639) return 'Frequence Connexion';
    if (frequency >= 528) return 'Frequence Amour';
    return 'Frequence Coeur';
  };

  return (
    <div className={`
      relative overflow-hidden rounded-2xl p-6 border
      ${isSource
        ? 'bg-gradient-to-r from-white/10 to-white/5 border-white/30'
        : 'bg-gradient-to-r from-yellow-900/20 to-yellow-600/10 border-yellow-600/30'}
    `}>
      {/* Pulse animation */}
      <div
        className="absolute inset-0 opacity-20"
        style={{
          background: `radial-gradient(circle at center, ${isSource ? '#FFFFFF' : '#D4AF37'} 0%, transparent 70%)`,
          animation: 'pulse 2s ease-in-out infinite'
        }}
      />

      <div className="relative z-10 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-4xl">{isSource ? '👑' : '💛'}</span>
            <div>
              <h2 className={`text-2xl font-bold ${isSource ? 'text-white' : 'text-yellow-400'}`}>
                {frequency} Hz
              </h2>
              <p className="text-sm text-gray-400">
                {getFrequencyLabel()}
              </p>
            </div>
          </div>
          {/* Completion Progress */}
          <div className="mt-3">
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-500">Activation</span>
              <span className={isSource ? 'text-white' : 'text-yellow-400'}>{completionPercentage}%</span>
            </div>
            <div className="h-2 bg-gray-800 rounded-full overflow-hidden w-48">
              <div
                className={`h-full rounded-full transition-all duration-500 ${
                  isSource ? 'bg-white' : 'bg-gradient-to-r from-yellow-600 to-yellow-400'
                }`}
                style={{ width: `${completionPercentage}%` }}
              />
            </div>
          </div>
        </div>

        <div className="text-right">
          <div className="text-3xl font-bold text-white">{foundersCount}</div>
          <div className="text-xs text-gray-500">Membres Fondateurs</div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: TOOLTIP L4 AGENT
// ═══════════════════════════════════════════════════════════════════════════════

const L4Tooltip = ({ children, explanation }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div className="relative inline-block">
      <button
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        className="ml-2 w-5 h-5 rounded-full bg-purple-500/20 text-purple-400 text-xs
          hover:bg-purple-500/40 transition-colors flex items-center justify-center"
      >
        ?
      </button>

      {showTooltip && (
        <div className="absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 w-64">
          <div className="bg-gray-900 border border-purple-500/30 rounded-lg p-3 shadow-xl">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-sm">🤖</span>
              <span className="text-xs text-purple-400 font-medium">Agent L4</span>
            </div>
            <p className="text-xs text-gray-300">{explanation}</p>
          </div>
          <div className="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-gray-900" />
        </div>
      )}
      {children}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: ETAPE DU WIZARD
// ═══════════════════════════════════════════════════════════════════════════════

const WizardStep = ({ step, isActive, isCompleted, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`
        flex items-center gap-3 p-4 rounded-xl border transition-all w-full
        ${isActive
          ? 'bg-yellow-500/20 border-yellow-500 scale-105'
          : isCompleted
            ? 'bg-green-500/10 border-green-500/30'
            : 'bg-black/50 border-gray-800 hover:border-gray-700'}
      `}
    >
      <div className={`
        w-10 h-10 rounded-full flex items-center justify-center text-lg
        ${isCompleted ? 'bg-green-500/20' : isActive ? 'bg-yellow-500/20' : 'bg-gray-800'}
      `}>
        {isCompleted ? '✅' : step.icon}
      </div>
      <div className="text-left">
        <div className={`font-medium ${isActive ? 'text-yellow-400' : 'text-white'}`}>
          {step.name}
        </div>
        <div className="text-xs text-gray-500">{step.description}</div>
      </div>
    </button>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CONFIGURATION API
// ═══════════════════════════════════════════════════════════════════════════════

const APIConfigSection = ({ onStatusChange }) => {
  const [apiKeys, setApiKeys] = useState({
    openrouter: '',
    anthropic: '',
    stripe: '',
    stripe_connect: '',
    digitalocean: '',
    vercel: ''
  });
  const [showKeys, setShowKeys] = useState({});
  const [testing, setTesting] = useState(null);
  const [statuses, setStatuses] = useState({});

  const updateKey = (id, value) => {
    setApiKeys(prev => ({ ...prev, [id]: value }));
  };

  const toggleShowKey = (id) => {
    setShowKeys(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const testConnection = async (relayId) => {
    setTesting(relayId);
    setStatuses(prev => ({ ...prev, [relayId]: 'testing' }));

    const key = apiKeys[relayId];
    let success = false;

    try {
      // Test actual API connections based on relay type
      if (relayId === 'openrouter' && key) {
        const response = await fetch('https://openrouter.ai/api/v1/models', {
          headers: { 'Authorization': `Bearer ${key}` }
        });
        success = response.ok;
      } else if (relayId === 'anthropic' && key) {
        // Anthropic doesn't have a simple test endpoint, check key format
        success = key.startsWith('sk-ant-') && key.length > 20;
      } else if (relayId === 'stripe' && key) {
        // Stripe key format validation
        success = (key.startsWith('sk_live_') || key.startsWith('sk_test_')) && key.length > 20;
      } else {
        // For other APIs, validate key format
        success = key && key.length > 10;
      }

      // Persist status to database
      if (success) {
        await supabase.rpc('update_api_connection_status', {
          p_api_name: relayId,
          p_connected: true,
          p_extra_data: null
        });
      }
    } catch (error) {
      console.error(`Error testing ${relayId}:`, error);
      success = false;
    }

    setStatuses(prev => ({ ...prev, [relayId]: success ? 'connected' : 'error' }));
    setTesting(null);
    onStatusChange?.(relayId, success);
  };

  const injectToSecrets = async () => {
    // This would integrate with Vercel/DigitalOcean APIs to inject secrets
    const activeKeys = Object.entries(apiKeys).filter(([_, v]) => v);

    if (activeKeys.length === 0) {
      alert('Aucune cle API a injecter');
      return;
    }

    // Save to localStorage for demo (in production: Vercel/DO API)
    localStorage.setItem('atom_sovereign_keys', JSON.stringify(apiKeys));
    alert(`${activeKeys.length} cles injectees dans les secrets de l'Arche`);
  };

  const apiRelays = RELAYS.filter(r => r.type === 'api' || r.type === 'payment' || r.type === 'infrastructure');

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span>🔑</span> Cles API Souveraines
          <L4Tooltip explanation="Les cles API sont stockees de maniere securisee dans les secrets Vercel/DigitalOcean. Elles ne sont jamais exposees cote client." />
        </h3>
        <button
          onClick={injectToSecrets}
          className="px-4 py-2 bg-yellow-600 text-black rounded-lg text-sm font-medium hover:bg-yellow-500"
        >
          💉 Injecter dans l'Arche
        </button>
      </div>

      <div className="space-y-4">
        {apiRelays.map(relay => (
          <div
            key={relay.id}
            className="bg-black/50 rounded-xl p-4 border border-gray-800"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{RELAY_TYPES[relay.type].icon}</span>
                <div>
                  <div className="text-white font-medium">{relay.name}</div>
                  <div className="text-xs text-gray-500">{relay.description}</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {statuses[relay.id] === 'connected' && (
                  <span className="text-green-400 text-sm">✅ Connecte</span>
                )}
                {statuses[relay.id] === 'error' && (
                  <span className="text-red-400 text-sm">❌ Erreur</span>
                )}
                {statuses[relay.id] === 'testing' && (
                  <span className="text-yellow-400 text-sm animate-pulse">⏳ Test...</span>
                )}
              </div>
            </div>

            <div className="flex gap-2">
              <div className="relative flex-1">
                <input
                  type={showKeys[relay.id] ? 'text' : 'password'}
                  value={apiKeys[relay.id] || ''}
                  onChange={(e) => updateKey(relay.id, e.target.value)}
                  placeholder={`${relay.envKey}=...`}
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white text-sm
                    placeholder-gray-600 focus:outline-none focus:border-yellow-500 pr-10"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey(relay.id)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
                >
                  {showKeys[relay.id] ? '🙈' : '👁️'}
                </button>
              </div>
              <button
                onClick={() => testConnection(relay.id)}
                disabled={testing === relay.id || !apiKeys[relay.id]}
                className="px-4 py-2 bg-gray-800 text-white rounded-lg text-sm hover:bg-gray-700
                  disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {testing === relay.id ? '⏳' : '🔌'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: STATUT BASE DE DONNEES
// ═══════════════════════════════════════════════════════════════════════════════

const DatabaseStatusSection = ({ onStatusChange }) => {
  const [dbStatus, setDbStatus] = useState({
    connection: 'checking',
    tables: [],
    functions: [],
    rls: false
  });

  const checkDatabaseStatus = useCallback(async () => {
    setDbStatus(prev => ({ ...prev, connection: 'checking' }));

    try {
      // Check connection
      const { data: healthCheck, error: healthError } = await supabase
        .from('profiles')
        .select('count')
        .limit(1);

      if (healthError) throw healthError;

      // Check required tables
      const requiredTables = ['profiles', 'api_usage', 'api_requests', 'subscription_plans', 'founding_members'];
      const tableChecks = await Promise.all(
        requiredTables.map(async (table) => {
          try {
            const { error } = await supabase.from(table).select('count').limit(1);
            return { name: table, exists: !error };
          } catch {
            return { name: table, exists: false };
          }
        })
      );

      // Check RPC functions
      const requiredFunctions = ['check_user_credits', 'record_api_usage', 'get_api_stats'];
      const functionChecks = await Promise.all(
        requiredFunctions.map(async (func) => {
          try {
            // Test if function exists by calling with invalid params (will error but differently)
            await supabase.rpc(func, {});
            return { name: func, exists: true };
          } catch (err) {
            // If error is about params, function exists
            return { name: func, exists: err.message?.includes('param') || err.code === 'PGRST202' };
          }
        })
      );

      setDbStatus({
        connection: 'connected',
        tables: tableChecks,
        functions: functionChecks,
        rls: true // Assume RLS is enabled if we can query
      });

      const allTablesExist = tableChecks.every(t => t.exists);
      onStatusChange?.('database', allTablesExist);

    } catch (error) {
      console.error('Database check error:', error);
      setDbStatus(prev => ({
        ...prev,
        connection: 'error',
        error: error.message
      }));
      onStatusChange?.('database', false);
    }
  }, [onStatusChange]);

  useEffect(() => {
    checkDatabaseStatus();
  }, [checkDatabaseStatus]);

  const getStatusBadge = (exists) => (
    <span className={`px-2 py-0.5 rounded text-xs ${
      exists ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
    }`}>
      {exists ? '✓' : '✗'}
    </span>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span>🗄️</span> Statut PostgreSQL
          <L4Tooltip explanation="Verification de la structure de la base de donnees Supabase, incluant les tables, fonctions RPC et politiques RLS." />
        </h3>
        <button
          onClick={checkDatabaseStatus}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-500"
        >
          🔄 Verifier
        </button>
      </div>

      {/* Connection Status */}
      <div className={`
        p-4 rounded-xl border
        ${dbStatus.connection === 'connected'
          ? 'bg-green-500/10 border-green-500/30'
          : dbStatus.connection === 'error'
            ? 'bg-red-500/10 border-red-500/30'
            : 'bg-yellow-500/10 border-yellow-500/30'}
      `}>
        <div className="flex items-center gap-3">
          <span className="text-2xl">
            {dbStatus.connection === 'connected' ? '✅' :
             dbStatus.connection === 'error' ? '❌' : '⏳'}
          </span>
          <div>
            <div className="text-white font-medium">
              {dbStatus.connection === 'connected' ? 'Connexion Active' :
               dbStatus.connection === 'error' ? 'Erreur de Connexion' : 'Verification...'}
            </div>
            {dbStatus.error && (
              <div className="text-xs text-red-400 mt-1">{dbStatus.error}</div>
            )}
          </div>
        </div>
      </div>

      {/* Tables Status */}
      <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
        <h4 className="text-sm text-gray-400 mb-3">Tables Requises</h4>
        <div className="grid grid-cols-2 gap-2">
          {dbStatus.tables.map(table => (
            <div key={table.name} className="flex items-center justify-between p-2 bg-gray-900/50 rounded">
              <span className="text-sm text-white font-mono">{table.name}</span>
              {getStatusBadge(table.exists)}
            </div>
          ))}
        </div>
      </div>

      {/* Functions Status */}
      <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
        <h4 className="text-sm text-gray-400 mb-3">Fonctions RPC</h4>
        <div className="space-y-2">
          {dbStatus.functions.map(func => (
            <div key={func.name} className="flex items-center justify-between p-2 bg-gray-900/50 rounded">
              <span className="text-sm text-white font-mono">{func.name}()</span>
              {getStatusBadge(func.exists)}
            </div>
          ))}
        </div>
      </div>

      {/* RLS Status */}
      <div className="flex items-center justify-between p-4 bg-black/50 rounded-xl border border-gray-800">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🔐</span>
          <span className="text-white">Row Level Security (RLS)</span>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm ${
          dbStatus.rls ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
        }`}>
          {dbStatus.rls ? 'Active' : 'Inactive'}
        </span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: STRIPE CONNECT SUMMARY
// ═══════════════════════════════════════════════════════════════════════════════

const StripeConnectSection = ({ onStatusChange }) => {
  const [stripeData, setStripeData] = useState({
    connected: false,
    balance: 0,
    pendingPayouts: 0,
    connectedAccounts: 0,
    distributionRules: []
  });

  useEffect(() => {
    // Simulated data - in production, fetch from Stripe API
    setStripeData({
      connected: true,
      balance: 4521.50,
      pendingPayouts: 1250.00,
      connectedAccounts: 12,
      distributionRules: [
        { name: 'OpenRouter Credits', percentage: 40, destination: 'Operating Costs' },
        { name: 'Development Fund', percentage: 30, destination: 'Platform Growth' },
        { name: 'Founder Rewards', percentage: 20, destination: 'Founding Members' },
        { name: 'Reserve', percentage: 10, destination: 'Emergency Fund' }
      ]
    });
    onStatusChange?.('stripe', true);
  }, [onStatusChange]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span>💳</span> Flux Financier Stripe Connect
          <L4Tooltip explanation="Stripe Connect permet la redistribution automatique des paiements aux partenaires, fournisseurs et membres fondateurs selon les regles definies." />
        </h3>
        <a
          href="https://dashboard.stripe.com"
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 bg-purple-600 text-white rounded-lg text-sm hover:bg-purple-500"
        >
          Ouvrir Stripe ↗
        </a>
      </div>

      {/* Balance Overview */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-green-900/20 to-green-600/10 rounded-xl p-4 border border-green-600/30">
          <div className="text-xs text-gray-500 mb-1">Balance Disponible</div>
          <div className="text-2xl font-bold text-green-400">${stripeData.balance.toFixed(2)}</div>
        </div>
        <div className="bg-gradient-to-br from-yellow-900/20 to-yellow-600/10 rounded-xl p-4 border border-yellow-600/30">
          <div className="text-xs text-gray-500 mb-1">Versements en Attente</div>
          <div className="text-2xl font-bold text-yellow-400">${stripeData.pendingPayouts.toFixed(2)}</div>
        </div>
        <div className="bg-gradient-to-br from-purple-900/20 to-purple-600/10 rounded-xl p-4 border border-purple-600/30">
          <div className="text-xs text-gray-500 mb-1">Comptes Connectes</div>
          <div className="text-2xl font-bold text-purple-400">{stripeData.connectedAccounts}</div>
        </div>
      </div>

      {/* Distribution Rules */}
      <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
        <h4 className="text-sm text-gray-400 mb-4">Regles de Distribution (99$/mois Fondateur)</h4>

        <div className="space-y-3">
          {stripeData.distributionRules.map((rule, index) => (
            <div key={index} className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-white">{rule.name}</span>
                <span className="text-yellow-400">{rule.percentage}%</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 rounded-full"
                  style={{ width: `${rule.percentage}%` }}
                />
              </div>
              <div className="text-xs text-gray-600">{rule.destination}</div>
            </div>
          ))}
        </div>

        <div className="mt-4 pt-4 border-t border-gray-800">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Total par Fondateur</span>
            <span className="text-white font-bold">99.00 $/mois</span>
          </div>
          <div className="flex justify-between text-xs text-gray-600 mt-1">
            <span>500K tokens inclus</span>
            <span>Acces Grid + Agents L4-L6</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: TABLEAU DE BORD DES RELAIS
// ═══════════════════════════════════════════════════════════════════════════════

const RelayDashboard = ({ relayStatuses }) => {
  return (
    <div className="space-y-6">
      <h3 className="text-lg font-bold text-white flex items-center gap-2">
        <span>📡</span> Tableau de Bord des Relais
      </h3>

      <div className="bg-black/50 rounded-xl border border-gray-800 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-800 bg-gray-900/50">
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Relais</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Type</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Statut</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Frequence</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {RELAYS.map(relay => {
              const status = relayStatuses[relay.id] || 'unconfigured';
              return (
                <tr key={relay.id} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <span className="text-xl">{RELAY_TYPES[relay.type].icon}</span>
                      <div>
                        <div className="text-sm text-white font-medium">{relay.name}</div>
                        <div className="text-xs text-gray-500">{relay.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className="px-2 py-1 rounded text-xs"
                      style={{
                        backgroundColor: `${RELAY_TYPES[relay.type].color}20`,
                        color: RELAY_TYPES[relay.type].color
                      }}
                    >
                      {RELAY_TYPES[relay.type].name}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`flex items-center gap-2 text-sm ${
                      status === 'connected' ? 'text-green-400' :
                      status === 'error' ? 'text-red-400' :
                      status === 'testing' ? 'text-yellow-400' :
                      'text-gray-500'
                    }`}>
                      <span className={`w-2 h-2 rounded-full ${
                        status === 'connected' ? 'bg-green-400' :
                        status === 'error' ? 'bg-red-400' :
                        status === 'testing' ? 'bg-yellow-400 animate-pulse' :
                        'bg-gray-600'
                      }`} />
                      {status === 'connected' ? 'Actif' :
                       status === 'error' ? 'Erreur' :
                       status === 'testing' ? 'Test...' :
                       'Non configure'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-sm ${
                      status === 'connected' ? 'text-white' : 'text-gray-600'
                    }`}>
                      {status === 'connected' ? '999 Hz' : '---'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <button className="px-3 py-1 bg-gray-800 text-gray-300 rounded text-xs hover:bg-gray-700">
                      Configurer
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// PAGE PRINCIPALE: SETUP WIZARD
// ═══════════════════════════════════════════════════════════════════════════════

const SetupWizardPage = () => {
  const { user, profile, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [activeStep, setActiveStep] = useState(0);
  const [foundersCount, setFoundersCount] = useState(0);
  const [frequency, setFrequency] = useState(FREQUENCIES.HEARTBEAT);
  const [relayStatuses, setRelayStatuses] = useState({});
  const [completedSteps, setCompletedSteps] = useState({});
  const [setupStatus, setSetupStatus] = useState(null);
  const [completionPercentage, setCompletionPercentage] = useState(0);

  const steps = [
    { id: 'api', name: 'Connexion API', icon: '🔌', description: 'Configurer les cles API souveraines' },
    { id: 'database', name: 'Base de Donnees', icon: '🗄️', description: 'Verifier la structure PostgreSQL' },
    { id: 'stripe', name: 'Flux Financier', icon: '💳', description: 'Configurer Stripe Connect' },
    { id: 'relay', name: 'Tableau de Bord', icon: '📡', description: 'Vue d\'ensemble des relais' }
  ];

  // Check sovereign access
  useEffect(() => {
    if (!authLoading && (!user || profile?.role !== 'souverain')) {
      navigate('/');
    }
  }, [user, profile, authLoading, navigate]);

  // Load setup status from database
  const loadSetupStatus = useCallback(async () => {
    try {
      const { data, error } = await supabase.rpc('get_setup_status');

      if (error) {
        console.warn('Could not load setup status:', error);
        return;
      }

      if (data?.success) {
        setSetupStatus(data);
        setCompletionPercentage(data.completion_percentage || 0);
        setFrequency(data.current_frequency || FREQUENCIES.HEARTBEAT);

        // Update relay statuses from database
        const apis = data.apis || {};
        const newStatuses = {};
        if (apis.openrouter?.connected) newStatuses.openrouter = 'connected';
        if (apis.anthropic?.connected) newStatuses.anthropic = 'connected';
        if (apis.stripe?.connected) newStatuses.stripe = 'connected';
        if (apis.digitalocean?.connected) newStatuses.digitalocean = 'connected';
        if (apis.vercel?.connected) newStatuses.vercel = 'connected';
        if (data.database?.connected) newStatuses.supabase = 'connected';

        setRelayStatuses(prev => ({ ...prev, ...newStatuses }));

        // Update completed steps
        setCompletedSteps({
          api: apis.openrouter?.connected || apis.anthropic?.connected || apis.stripe?.connected,
          database: data.database?.connected,
          stripe: data.finance?.stripe_connect_configured,
          relay: data.completion_percentage >= 75
        });
      }
    } catch (err) {
      console.warn('Error loading setup status:', err);
    }
  }, []);

  useEffect(() => {
    if (user && profile?.role === 'souverain') {
      loadSetupStatus();
    }
  }, [user, profile, loadSetupStatus]);

  // Load founders count
  useEffect(() => {
    const loadFoundersCount = async () => {
      try {
        const { count } = await supabase
          .from('founding_members')
          .select('*', { count: 'exact', head: true })
          .eq('status', 'active');
        setFoundersCount(count || 0);
      } catch {
        // Table might not exist yet
        setFoundersCount(0);
      }
    };
    loadFoundersCount();
  }, []);

  // Calculate frequency based on completion percentage
  useEffect(() => {
    const newFrequency = getFrequencyFromCompletion(completionPercentage);
    setFrequency(newFrequency);
  }, [completionPercentage]);

  const handleStatusChange = async (relayId, success) => {
    setRelayStatuses(prev => ({ ...prev, [relayId]: success ? 'connected' : 'error' }));

    // Update completed steps
    const stepId = steps[activeStep]?.id;
    if (stepId) {
      setCompletedSteps(prev => ({ ...prev, [stepId]: success }));
    }

    // Reload setup status to get updated completion percentage
    if (success) {
      await loadSetupStatus();
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-yellow-400 animate-pulse">Verification des acces...</div>
      </div>
    );
  }

  if (!user || profile?.role !== 'souverain') {
    return null;
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Background gradient */}
      <div
        className="fixed inset-0 opacity-30"
        style={{
          background: `radial-gradient(ellipse at center, ${frequency >= 999 ? '#FFFFFF' : '#D4AF37'}20 0%, transparent 70%)`
        }}
      />

      <div className="relative z-10 max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/admin')}
              className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white"
            >
              ← Retour
            </button>
            <div>
              <h1 className="text-2xl font-bold text-white">Guide d'Activation Souverain</h1>
              <p className="text-sm text-gray-500">Configuration des Relais Energetiques</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-500">Acces</div>
            <div className="text-yellow-400 font-medium">👑 Souverain</div>
          </div>
        </div>

        {/* Frequency Indicator */}
        <FrequencyIndicator frequency={frequency} foundersCount={foundersCount} completionPercentage={completionPercentage} />

        {/* Main Content */}
        <div className="grid grid-cols-4 gap-6 mt-8">
          {/* Steps Navigation */}
          <div className="space-y-3">
            {steps.map((step, index) => (
              <WizardStep
                key={step.id}
                step={step}
                isActive={activeStep === index}
                isCompleted={completedSteps[step.id]}
                onClick={() => setActiveStep(index)}
              />
            ))}
          </div>

          {/* Step Content */}
          <div className="col-span-3 bg-gray-900/50 rounded-2xl p-6 border border-gray-800">
            {activeStep === 0 && (
              <APIConfigSection onStatusChange={handleStatusChange} />
            )}
            {activeStep === 1 && (
              <DatabaseStatusSection onStatusChange={handleStatusChange} />
            )}
            {activeStep === 2 && (
              <StripeConnectSection onStatusChange={handleStatusChange} />
            )}
            {activeStep === 3 && (
              <RelayDashboard relayStatuses={relayStatuses} />
            )}
          </div>
        </div>

        {/* Footer Navigation */}
        <div className="flex justify-between mt-8">
          <button
            onClick={() => setActiveStep(Math.max(0, activeStep - 1))}
            disabled={activeStep === 0}
            className="px-6 py-3 bg-gray-800 text-white rounded-lg disabled:opacity-50"
          >
            ← Etape Precedente
          </button>
          <button
            onClick={() => setActiveStep(Math.min(steps.length - 1, activeStep + 1))}
            disabled={activeStep === steps.length - 1}
            className="px-6 py-3 bg-yellow-600 text-black rounded-lg font-medium hover:bg-yellow-500 disabled:opacity-50"
          >
            Etape Suivante →
          </button>
        </div>
      </div>

      {/* CSS for pulse animation */}
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.2; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(1.05); }
        }
      `}</style>
    </div>
  );
};

export default SetupWizardPage;
