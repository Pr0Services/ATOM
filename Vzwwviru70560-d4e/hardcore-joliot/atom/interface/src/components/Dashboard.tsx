// ═══════════════════════════════════════════════════════════════════════════
// AT·OM DASHBOARD - Main Interface
// The 10 Spheres of Civilization
// ═══════════════════════════════════════════════════════════════════════════

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Heart,
  Wallet,
  GraduationCap,
  Building2,
  Zap,
  MessageCircle,
  Scale,
  Truck,
  Utensils,
  Cpu,
  Activity,
  TrendingUp,
  Wifi,
  WifiOff,
  RefreshCw,
  Settings,
  Bell,
  ChevronRight,
  BarChart3,
  Shield,
  Clock,
} from 'lucide-react';
import { useAtomStore, SPHERE_CONFIG } from '@/stores/atom.store';
import type { SphereId, Sphere } from '@/types';

// ─────────────────────────────────────────────────────────────────────────────
// ICON MAP
// ─────────────────────────────────────────────────────────────────────────────

const ICON_MAP: Record<string, React.ElementType> = {
  Heart,
  Wallet,
  GraduationCap,
  Building2,
  Zap,
  MessageCircle,
  Scale,
  Truck,
  Utensils,
  Cpu,
};

// ─────────────────────────────────────────────────────────────────────────────
// DASHBOARD COMPONENT
// ─────────────────────────────────────────────────────────────────────────────

export function Dashboard() {
  const {
    spheres,
    activeSphere,
    setActiveSphere,
    heartbeat,
    arithmos,
    offline,
    alerts,
    ui,
  } = useAtomStore();

  const unacknowledgedAlerts = alerts.filter((a) => !a.acknowledged);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <DashboardHeader
        isOnline={offline.isOnline}
        isConnected={heartbeat.isConnected}
        alertCount={unacknowledgedAlerts.length}
        notificationCount={ui.notifications.filter((n) => !n.read).length}
      />

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* System Status Banner */}
        <SystemStatusBanner
          stability={heartbeat.systemStability}
          efficiency={heartbeat.systemEfficiency}
          globalBalance={arithmos.globalBalance}
          harmonicIndex={arithmos.harmonicIndex}
          cycleNumber={heartbeat.cycleNumber}
          isConnected={heartbeat.isConnected}
        />

        {/* 10 Spheres Grid */}
        <section className="mt-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-semibold text-white/90">
              Les 10 Sphères
            </h2>
            <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg transition-colors text-sm text-white/60">
              <Settings className="w-4 h-4" />
              Configuration
            </button>
          </div>

          <SpheresGrid
            spheres={spheres}
            activeSphere={activeSphere}
            onSphereClick={setActiveSphere}
            sphereBalances={arithmos.sphereBalances}
          />
        </section>

        {/* Active Sphere Detail */}
        <AnimatePresence>
          {activeSphere && (
            <SphereDetail
              sphere={spheres[activeSphere]}
              balance={arithmos.sphereBalances[activeSphere] ?? 0}
              onClose={() => setActiveSphere(null)}
            />
          )}
        </AnimatePresence>

        {/* Recommendations */}
        {arithmos.recommendations.length > 0 && (
          <RecommendationsPanel recommendations={arithmos.recommendations} />
        )}

        {/* Offline Status */}
        {!offline.isOnline && (
          <OfflineStatusPanel
            pendingCount={offline.pendingOperations.length}
            lastOnline={offline.lastOnline}
          />
        )}
      </main>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HEADER
// ─────────────────────────────────────────────────────────────────────────────

function DashboardHeader({
  isOnline,
  isConnected,
  alertCount,
  notificationCount,
}: {
  isOnline: boolean;
  isConnected: boolean;
  alertCount: number;
  notificationCount: number;
}) {
  return (
    <header className="border-b border-white/10 bg-slate-900/50 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-atom-500 to-atom-700 flex items-center justify-center">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">AT·OM</h1>
            <p className="text-xs text-white/40">Interface de Productivité</p>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex items-center gap-4">
          {/* Connection Status */}
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm ${
            isOnline && isConnected
              ? 'bg-emerald-500/10 text-emerald-400'
              : isOnline
              ? 'bg-yellow-500/10 text-yellow-400'
              : 'bg-red-500/10 text-red-400'
          }`}>
            {isOnline ? (
              <Wifi className="w-4 h-4" />
            ) : (
              <WifiOff className="w-4 h-4" />
            )}
            <span>
              {isOnline && isConnected
                ? 'Connecté'
                : isOnline
                ? 'Hors ligne partiel'
                : 'Hors ligne'}
            </span>
          </div>

          {/* Alerts */}
          {alertCount > 0 && (
            <button className="relative p-2 bg-red-500/10 hover:bg-red-500/20 rounded-lg transition-colors">
              <Bell className="w-5 h-5 text-red-400" />
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs flex items-center justify-center text-white">
                {alertCount}
              </span>
            </button>
          )}

          {/* Notifications */}
          <button className="relative p-2 bg-white/5 hover:bg-white/10 rounded-lg transition-colors">
            <Bell className="w-5 h-5 text-white/60" />
            {notificationCount > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-atom-500 rounded-full text-xs flex items-center justify-center text-white">
                {notificationCount}
              </span>
            )}
          </button>

          {/* Settings */}
          <button className="p-2 bg-white/5 hover:bg-white/10 rounded-lg transition-colors">
            <Settings className="w-5 h-5 text-white/60" />
          </button>
        </div>
      </div>
    </header>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SYSTEM STATUS BANNER
// ─────────────────────────────────────────────────────────────────────────────

function SystemStatusBanner({
  stability,
  efficiency,
  globalBalance,
  harmonicIndex,
  cycleNumber,
  isConnected,
}: {
  stability: number;
  efficiency: number;
  globalBalance: number;
  harmonicIndex: number;
  cycleNumber: number;
  isConnected: boolean;
}) {
  return (
    <div className="grid grid-cols-4 gap-4">
      {/* Stability */}
      <StatusCard
        label="Stabilité"
        value={stability}
        icon={Shield}
        color={stability >= 80 ? 'emerald' : stability >= 50 ? 'yellow' : 'red'}
      />

      {/* Efficiency */}
      <StatusCard
        label="Efficacité"
        value={efficiency}
        icon={TrendingUp}
        color={efficiency >= 80 ? 'emerald' : efficiency >= 50 ? 'yellow' : 'red'}
      />

      {/* Global Balance */}
      <StatusCard
        label="Balance Globale"
        value={globalBalance}
        icon={BarChart3}
        color={globalBalance >= 80 ? 'emerald' : globalBalance >= 50 ? 'yellow' : 'red'}
      />

      {/* Harmonic Index */}
      <StatusCard
        label="Index Harmonique"
        value={harmonicIndex}
        icon={Activity}
        color={harmonicIndex >= 80 ? 'emerald' : harmonicIndex >= 50 ? 'yellow' : 'red'}
        suffix=""
      />
    </div>
  );
}

function StatusCard({
  label,
  value,
  icon: Icon,
  color,
  suffix = '%',
}: {
  label: string;
  value: number;
  icon: React.ElementType;
  color: 'emerald' | 'yellow' | 'red';
  suffix?: string;
}) {
  const colorClasses = {
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    red: 'bg-red-500/10 text-red-400 border-red-500/20',
  };

  return (
    <div className={`p-4 rounded-xl border ${colorClasses[color]}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm opacity-70">{label}</span>
        <Icon className="w-4 h-4" />
      </div>
      <div className="text-3xl font-bold">
        {value}
        <span className="text-lg opacity-60">{suffix}</span>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SPHERES GRID
// ─────────────────────────────────────────────────────────────────────────────

function SpheresGrid({
  spheres,
  activeSphere,
  onSphereClick,
  sphereBalances,
}: {
  spheres: Record<SphereId, Sphere>;
  activeSphere: SphereId | null;
  onSphereClick: (id: SphereId) => void;
  sphereBalances: Record<SphereId, number>;
}) {
  const sphereIds: SphereId[] = [
    'health', 'finance', 'education', 'governance', 'energy',
    'communication', 'justice', 'logistics', 'food', 'technology',
  ];

  return (
    <div className="grid grid-cols-5 gap-4">
      {sphereIds.map((id) => (
        <SphereCard
          key={id}
          sphere={spheres[id]}
          isActive={activeSphere === id}
          balance={sphereBalances[id] ?? 0}
          onClick={() => onSphereClick(id)}
        />
      ))}
    </div>
  );
}

function SphereCard({
  sphere,
  isActive,
  balance,
  onClick,
}: {
  sphere: Sphere;
  isActive: boolean;
  balance: number;
  onClick: () => void;
}) {
  const Icon = ICON_MAP[sphere.icon] || Activity;
  const balanceColor = balance >= 80 ? 'text-emerald-400' : balance >= 50 ? 'text-yellow-400' : 'text-red-400';

  return (
    <motion.button
      onClick={onClick}
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      className={`relative p-6 rounded-2xl border transition-all duration-300 text-left ${
        isActive
          ? 'bg-white/10 border-white/20 shadow-lg shadow-white/5'
          : 'bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/15'
      }`}
    >
      {/* Icon */}
      <div
        className="w-12 h-12 rounded-xl flex items-center justify-center mb-4"
        style={{ backgroundColor: `${sphere.color}20` }}
      >
        <Icon className="w-6 h-6" style={{ color: sphere.color }} />
      </div>

      {/* Name */}
      <h3 className="text-lg font-medium text-white mb-1">{sphere.name}</h3>

      {/* Description */}
      <p className="text-sm text-white/50 mb-4 line-clamp-2">
        {sphere.description}
      </p>

      {/* Metrics */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1">
          <span className={`text-lg font-bold ${balanceColor}`}>{balance}%</span>
          <span className="text-xs text-white/40">balance</span>
        </div>
        <ChevronRight className="w-4 h-4 text-white/30" />
      </div>

      {/* Status Indicator */}
      <div className="absolute top-4 right-4">
        <div
          className={`w-2 h-2 rounded-full ${
            sphere.stability >= 80
              ? 'bg-emerald-400'
              : sphere.stability >= 50
              ? 'bg-yellow-400'
              : 'bg-red-400'
          }`}
        />
      </div>

      {/* API Connections Count */}
      {sphere.apiConnections.length > 0 && (
        <div className="absolute bottom-4 right-4 px-2 py-0.5 bg-white/10 rounded text-xs text-white/50">
          {sphere.apiConnections.length} API
        </div>
      )}
    </motion.button>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SPHERE DETAIL PANEL
// ─────────────────────────────────────────────────────────────────────────────

function SphereDetail({
  sphere,
  balance,
  onClose,
}: {
  sphere: Sphere;
  balance: number;
  onClose: () => void;
}) {
  const Icon = ICON_MAP[sphere.icon] || Activity;

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="mt-8 p-6 bg-white/5 rounded-2xl border border-white/10"
    >
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-4">
          <div
            className="w-14 h-14 rounded-xl flex items-center justify-center"
            style={{ backgroundColor: `${sphere.color}20` }}
          >
            <Icon className="w-7 h-7" style={{ color: sphere.color }} />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white">{sphere.name}</h3>
            <p className="text-white/50">{sphere.description}</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-2 bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
        >
          ✕
        </button>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <MetricBox label="Stabilité" value={sphere.stability} suffix="%" />
        <MetricBox label="Efficacité" value={sphere.efficiency} suffix="%" />
        <MetricBox label="Balance" value={balance} suffix="%" />
        <MetricBox
          label="Score Santé"
          value={sphere.metrics.healthScore}
          suffix="%"
        />
      </div>

      {/* API Connections */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-white/60 mb-3">
          Connexions API ({sphere.apiConnections.length})
        </h4>
        {sphere.apiConnections.length > 0 ? (
          <div className="space-y-2">
            {sphere.apiConnections.map((conn) => (
              <div
                key={conn.id}
                className="flex items-center justify-between p-3 bg-white/5 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      conn.status === 'connected'
                        ? 'bg-emerald-400'
                        : conn.status === 'error'
                        ? 'bg-red-400'
                        : 'bg-yellow-400'
                    }`}
                  />
                  <span className="text-white/80">{conn.name}</span>
                  <span className="text-xs text-white/40">{conn.provider}</span>
                </div>
                <span className="text-xs text-white/40">{conn.authType}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-white/40">
            <p>Aucune API connectée</p>
            <button className="mt-2 px-4 py-2 bg-atom-600 hover:bg-atom-700 rounded-lg transition-colors text-sm text-white">
              + Ajouter une connexion
            </button>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <button className="flex-1 py-3 bg-atom-600 hover:bg-atom-700 rounded-lg transition-colors font-medium">
          Configurer
        </button>
        <button className="px-4 py-3 bg-white/5 hover:bg-white/10 rounded-lg transition-colors">
          <RefreshCw className="w-5 h-5" />
        </button>
      </div>
    </motion.section>
  );
}

function MetricBox({
  label,
  value,
  suffix,
}: {
  label: string;
  value: number;
  suffix: string;
}) {
  return (
    <div className="p-4 bg-white/5 rounded-lg">
      <div className="text-sm text-white/50 mb-1">{label}</div>
      <div className="text-2xl font-bold text-white">
        {value}
        <span className="text-sm text-white/50">{suffix}</span>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// RECOMMENDATIONS PANEL
// ─────────────────────────────────────────────────────────────────────────────

function RecommendationsPanel({
  recommendations,
}: {
  recommendations: Array<{
    id: string;
    priority: string;
    sphereId: SphereId;
    action: string;
    impact: number;
    estimatedTime: string;
  }>;
}) {
  return (
    <section className="mt-8">
      <h3 className="text-lg font-medium text-white/80 mb-4">
        Recommandations Prioritaires
      </h3>
      <div className="space-y-3">
        {recommendations.map((rec) => {
          const config = SPHERE_CONFIG[rec.sphereId];
          const Icon = ICON_MAP[config.icon] || Activity;

          return (
            <div
              key={rec.id}
              className="flex items-center gap-4 p-4 bg-white/5 rounded-xl border border-white/10 hover:bg-white/10 transition-colors cursor-pointer"
            >
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ backgroundColor: `${config.color}20` }}
              >
                <Icon className="w-5 h-5" style={{ color: config.color }} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white/90 truncate">{rec.action}</p>
                <div className="flex items-center gap-3 mt-1 text-sm text-white/50">
                  <span>{config.name}</span>
                  <span>•</span>
                  <span>Impact: +{rec.impact}%</span>
                  <span>•</span>
                  <span>{rec.estimatedTime}</span>
                </div>
              </div>
              <div
                className={`px-2 py-1 rounded text-xs font-medium ${
                  rec.priority === 'high'
                    ? 'bg-red-500/20 text-red-400'
                    : rec.priority === 'medium'
                    ? 'bg-yellow-500/20 text-yellow-400'
                    : 'bg-emerald-500/20 text-emerald-400'
                }`}
              >
                {rec.priority === 'high'
                  ? 'Urgent'
                  : rec.priority === 'medium'
                  ? 'Important'
                  : 'Normal'}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// OFFLINE STATUS PANEL
// ─────────────────────────────────────────────────────────────────────────────

function OfflineStatusPanel({
  pendingCount,
  lastOnline,
}: {
  pendingCount: number;
  lastOnline: Date | null;
}) {
  return (
    <div className="fixed bottom-4 right-4 p-4 bg-yellow-500/20 backdrop-blur-xl border border-yellow-500/30 rounded-xl max-w-sm">
      <div className="flex items-start gap-3">
        <WifiOff className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="font-medium text-yellow-400">Mode Hors Ligne</h4>
          <p className="text-sm text-white/60 mt-1">
            {pendingCount} opération(s) en attente de synchronisation
          </p>
          {lastOnline && (
            <p className="text-xs text-white/40 mt-2 flex items-center gap-1">
              <Clock className="w-3 h-3" />
              Dernière connexion: {new Date(lastOnline).toLocaleString('fr-FR')}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
