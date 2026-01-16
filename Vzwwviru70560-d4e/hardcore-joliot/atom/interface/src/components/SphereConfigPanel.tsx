// ═══════════════════════════════════════════════════════════════════════════
// AT·OM SPHERE CONFIGURATION PANEL
// Detailed sphere settings and API connections
// ═══════════════════════════════════════════════════════════════════════════

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  Plus,
  Trash2,
  RefreshCw,
  Link,
  Unlink,
  Shield,
  Activity,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  ExternalLink,
  Settings,
  Key,
  Globe,
  Wallet,
} from 'lucide-react';
import { useAtomStore, SPHERE_CONFIG } from '@/stores/atom.store';
import { SPHERE_API_TEMPLATES, apiConnectionManager } from '@/services/api.service';
import type { SphereId, Sphere, ApiConnection, ApiAuthType } from '@/types';
import { cn, formatRelativeTime } from '@/utils';

// ─────────────────────────────────────────────────────────────────────────────
// TYPES
// ─────────────────────────────────────────────────────────────────────────────

interface SphereConfigPanelProps {
  sphereId: SphereId;
  onClose: () => void;
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────────────────────────────────────

export function SphereConfigPanel({ sphereId, onClose }: SphereConfigPanelProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'apis' | 'settings'>('overview');
  const sphere = useAtomStore((state) => state.spheres[sphereId]);
  const balance = useAtomStore((state) => state.arithmos.sphereBalances[sphereId] ?? 0);
  const config = SPHERE_CONFIG[sphereId];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-3xl max-h-[85vh] bg-slate-900 rounded-2xl border border-white/10 overflow-hidden flex flex-col"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <div className="flex items-center gap-4">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center"
              style={{ backgroundColor: `${config.color}20` }}
            >
              <div
                className="w-6 h-6 rounded-full"
                style={{ backgroundColor: config.color }}
              />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">{config.name}</h2>
              <p className="text-sm text-white/50">Configuration de la sphère</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-white/60" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-white/10">
          {[
            { id: 'overview', label: 'Vue d\'ensemble', icon: Activity },
            { id: 'apis', label: 'Connexions API', icon: Link },
            { id: 'settings', label: 'Paramètres', icon: Settings },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as typeof activeTab)}
              className={cn(
                'flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors',
                activeTab === tab.id
                  ? 'text-white border-b-2 border-atom-500'
                  : 'text-white/50 hover:text-white/70'
              )}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          <AnimatePresence mode="wait">
            {activeTab === 'overview' && (
              <OverviewTab key="overview" sphere={sphere} balance={balance} />
            )}
            {activeTab === 'apis' && (
              <ApisTab key="apis" sphere={sphere} sphereId={sphereId} />
            )}
            {activeTab === 'settings' && (
              <SettingsTab key="settings" sphere={sphere} sphereId={sphereId} />
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// OVERVIEW TAB
// ─────────────────────────────────────────────────────────────────────────────

function OverviewTab({ sphere, balance }: { sphere: Sphere; balance: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-6"
    >
      {/* Metrics Grid */}
      <div className="grid grid-cols-3 gap-4">
        <MetricCard
          label="Stabilité"
          value={sphere.stability}
          suffix="%"
          icon={Shield}
          color={sphere.stability >= 70 ? 'emerald' : sphere.stability >= 40 ? 'yellow' : 'red'}
        />
        <MetricCard
          label="Efficacité"
          value={sphere.efficiency}
          suffix="%"
          icon={TrendingUp}
          color={sphere.efficiency >= 70 ? 'emerald' : sphere.efficiency >= 40 ? 'yellow' : 'red'}
        />
        <MetricCard
          label="Balance"
          value={balance}
          suffix="%"
          icon={Activity}
          color={balance >= 70 ? 'emerald' : balance >= 40 ? 'yellow' : 'red'}
        />
      </div>

      {/* Activity */}
      <div className="p-4 bg-white/5 rounded-xl">
        <h3 className="text-sm font-medium text-white/60 mb-3">Activité</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-2xl font-bold text-white">{sphere.metrics.totalItems}</div>
            <div className="text-sm text-white/50">Total éléments</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white">{sphere.metrics.activeItems}</div>
            <div className="text-sm text-white/50">Éléments actifs</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white">{sphere.metrics.pendingActions}</div>
            <div className="text-sm text-white/50">Actions en attente</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white">{sphere.apiConnections.length}</div>
            <div className="text-sm text-white/50">APIs connectées</div>
          </div>
        </div>
      </div>

      {/* Status */}
      <div className="p-4 bg-white/5 rounded-xl">
        <h3 className="text-sm font-medium text-white/60 mb-3">État du système</h3>
        <div className="space-y-3">
          <StatusRow
            label="Dernière synchronisation"
            value={sphere.lastSync ? formatRelativeTime(sphere.lastSync) : 'Jamais'}
            status={sphere.lastSync ? 'success' : 'warning'}
          />
          <StatusRow
            label="Score de santé"
            value={`${sphere.metrics.healthScore}%`}
            status={sphere.metrics.healthScore >= 70 ? 'success' : sphere.metrics.healthScore >= 40 ? 'warning' : 'error'}
          />
          <StatusRow
            label="Tendance"
            value={sphere.metrics.trendDirection === 'up' ? 'En hausse' : sphere.metrics.trendDirection === 'down' ? 'En baisse' : 'Stable'}
            status={sphere.metrics.trendDirection === 'up' ? 'success' : sphere.metrics.trendDirection === 'down' ? 'error' : 'warning'}
          />
        </div>
      </div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// APIS TAB
// ─────────────────────────────────────────────────────────────────────────────

function ApisTab({ sphere, sphereId }: { sphere: Sphere; sphereId: SphereId }) {
  const [showAddApi, setShowAddApi] = useState(false);
  const templates = SPHERE_API_TEMPLATES[sphereId] || [];
  const { addApiConnection, removeApiConnection } = useAtomStore();

  const handleConnect = async (template: typeof templates[0]) => {
    // In real app, this would initiate OAuth flow or show API key input
    const connection: ApiConnection = {
      id: crypto.randomUUID(),
      name: template.name,
      provider: template.provider,
      sphereId,
      authType: template.authType,
      status: 'pending',
      lastSync: null,
      config: {
        baseUrl: `https://api.${template.provider}.com`,
        endpoints: {},
      },
      permissions: [],
    };
    
    addApiConnection(sphereId, connection);
    setShowAddApi(false);
  };

  const handleDisconnect = (connectionId: string) => {
    removeApiConnection(sphereId, connectionId);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-6"
    >
      {/* Connected APIs */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-white/60">APIs Connectées</h3>
          <button
            onClick={() => setShowAddApi(true)}
            className="flex items-center gap-2 px-3 py-1.5 bg-atom-600 hover:bg-atom-700 rounded-lg text-sm font-medium transition-colors"
          >
            <Plus className="w-4 h-4" />
            Ajouter
          </button>
        </div>

        {sphere.apiConnections.length > 0 ? (
          <div className="space-y-3">
            {sphere.apiConnections.map((conn) => (
              <ApiConnectionCard
                key={conn.id}
                connection={conn}
                onDisconnect={() => handleDisconnect(conn.id)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-white/40">
            <Link className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>Aucune API connectée</p>
            <p className="text-sm mt-1">Ajoutez des connexions pour synchroniser vos données</p>
          </div>
        )}
      </div>

      {/* Add API Modal */}
      <AnimatePresence>
        {showAddApi && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-60 flex items-center justify-center p-4 bg-black/60"
            onClick={() => setShowAddApi(false)}
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              onClick={(e) => e.stopPropagation()}
              className="w-full max-w-md bg-slate-800 rounded-xl border border-white/10 p-6"
            >
              <h3 className="text-lg font-bold text-white mb-4">Ajouter une connexion</h3>
              <div className="space-y-3">
                {templates.map((template) => (
                  <button
                    key={template.provider}
                    onClick={() => handleConnect(template)}
                    className="w-full flex items-center gap-4 p-4 bg-white/5 hover:bg-white/10 rounded-xl transition-colors text-left"
                  >
                    <div className="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center">
                      {template.authType === 'oauth2' ? (
                        <Key className="w-5 h-5 text-white/60" />
                      ) : template.authType === 'web3' ? (
                        <Wallet className="w-5 h-5 text-white/60" />
                      ) : (
                        <Globe className="w-5 h-5 text-white/60" />
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-white">{template.name}</div>
                      <div className="text-sm text-white/50">{template.authType.toUpperCase()}</div>
                    </div>
                    <ExternalLink className="w-4 h-4 text-white/30" />
                  </button>
                ))}
              </div>
              <button
                onClick={() => setShowAddApi(false)}
                className="w-full mt-4 py-2 text-white/50 hover:text-white/70 text-sm"
              >
                Annuler
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function ApiConnectionCard({
  connection,
  onDisconnect,
}: {
  connection: ApiConnection;
  onDisconnect: () => void;
}) {
  const statusColors = {
    connected: 'bg-emerald-500',
    disconnected: 'bg-gray-500',
    error: 'bg-red-500',
    pending: 'bg-yellow-500',
  };

  return (
    <div className="flex items-center gap-4 p-4 bg-white/5 rounded-xl">
      <div className="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center">
        {connection.authType === 'oauth2' ? (
          <Key className="w-5 h-5 text-white/60" />
        ) : connection.authType === 'web3' ? (
          <Wallet className="w-5 h-5 text-white/60" />
        ) : (
          <Globe className="w-5 h-5 text-white/60" />
        )}
      </div>
      
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="font-medium text-white">{connection.name}</span>
          <div className={cn('w-2 h-2 rounded-full', statusColors[connection.status])} />
        </div>
        <div className="text-sm text-white/50">
          {connection.lastSync
            ? `Sync: ${formatRelativeTime(connection.lastSync)}`
            : 'Jamais synchronisé'}
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button className="p-2 hover:bg-white/10 rounded-lg transition-colors">
          <RefreshCw className="w-4 h-4 text-white/50" />
        </button>
        <button
          onClick={onDisconnect}
          className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
        >
          <Trash2 className="w-4 h-4 text-red-400" />
        </button>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SETTINGS TAB
// ─────────────────────────────────────────────────────────────────────────────

function SettingsTab({ sphere, sphereId }: { sphere: Sphere; sphereId: SphereId }) {
  const updateSphere = useAtomStore((state) => state.updateSphere);

  const handleToggleActive = () => {
    updateSphere(sphereId, { isActive: !sphere.isActive });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-6"
    >
      {/* General Settings */}
      <div className="p-4 bg-white/5 rounded-xl space-y-4">
        <h3 className="text-sm font-medium text-white/60">Paramètres généraux</h3>
        
        <SettingToggle
          label="Sphère active"
          description="Activer ou désactiver cette sphère"
          checked={sphere.isActive}
          onChange={handleToggleActive}
        />

        <SettingToggle
          label="Notifications"
          description="Recevoir des alertes pour cette sphère"
          checked={true}
          onChange={() => {}}
        />

        <SettingToggle
          label="Synchronisation automatique"
          description="Synchroniser les données en arrière-plan"
          checked={true}
          onChange={() => {}}
        />
      </div>

      {/* Danger Zone */}
      <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
        <h3 className="text-sm font-medium text-red-400 mb-3">Zone dangereuse</h3>
        <p className="text-sm text-white/50 mb-4">
          Ces actions sont irréversibles. Procédez avec prudence.
        </p>
        <div className="flex gap-3">
          <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm text-white/70 transition-colors">
            Réinitialiser les données
          </button>
          <button className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-sm text-red-400 transition-colors">
            Supprimer toutes les connexions
          </button>
        </div>
      </div>
    </motion.div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HELPER COMPONENTS
// ─────────────────────────────────────────────────────────────────────────────

function MetricCard({
  label,
  value,
  suffix,
  icon: Icon,
  color,
}: {
  label: string;
  value: number;
  suffix: string;
  icon: React.ElementType;
  color: 'emerald' | 'yellow' | 'red';
}) {
  const colorClasses = {
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    red: 'bg-red-500/10 text-red-400 border-red-500/20',
  };

  return (
    <div className={cn('p-4 rounded-xl border', colorClasses[color])}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm opacity-70">{label}</span>
        <Icon className="w-4 h-4" />
      </div>
      <div className="text-2xl font-bold">
        {value}
        <span className="text-sm opacity-60">{suffix}</span>
      </div>
    </div>
  );
}

function StatusRow({
  label,
  value,
  status,
}: {
  label: string;
  value: string;
  status: 'success' | 'warning' | 'error';
}) {
  const icons = {
    success: CheckCircle,
    warning: AlertTriangle,
    error: AlertTriangle,
  };
  const colors = {
    success: 'text-emerald-400',
    warning: 'text-yellow-400',
    error: 'text-red-400',
  };
  const Icon = icons[status];

  return (
    <div className="flex items-center justify-between">
      <span className="text-white/50">{label}</span>
      <div className={cn('flex items-center gap-2', colors[status])}>
        <Icon className="w-4 h-4" />
        <span className="text-sm">{value}</span>
      </div>
    </div>
  );
}

function SettingToggle({
  label,
  description,
  checked,
  onChange,
}: {
  label: string;
  description: string;
  checked: boolean;
  onChange: () => void;
}) {
  return (
    <div className="flex items-center justify-between">
      <div>
        <div className="font-medium text-white">{label}</div>
        <div className="text-sm text-white/50">{description}</div>
      </div>
      <button
        onClick={onChange}
        className={cn(
          'w-12 h-6 rounded-full transition-colors relative',
          checked ? 'bg-atom-600' : 'bg-white/20'
        )}
      >
        <div
          className={cn(
            'absolute top-1 w-4 h-4 rounded-full bg-white transition-transform',
            checked ? 'left-7' : 'left-1'
          )}
        />
      </button>
    </div>
  );
}

export default SphereConfigPanel;
