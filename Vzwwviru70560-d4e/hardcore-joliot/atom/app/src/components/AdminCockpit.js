/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗     ██████╗ ██████╗  ██████╗██╗  ██╗██████╗ ██╗████████╗
 *      ██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║    ██╔════╝██╔═══██╗██╔════╝██║ ██╔╝██╔══██╗██║╚══██╔══╝
 *      ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║    ██║     ██║   ██║██║     █████╔╝ ██████╔╝██║   ██║
 *      ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║    ██║     ██║   ██║██║     ██╔═██╗ ██╔═══╝ ██║   ██║
 *      ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║    ╚██████╗╚██████╔╝╚██████╗██║  ██╗██║     ██║   ██║
 *      ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝
 *
 *                              🎛️ COCKPIT ADMINISTRATEUR CHE·NU 🎛️
 *                    Centre de Commande Complet pour Administrateurs Système
 *
 *   MODULES INCLUS:
 *   ├── 📊 Analytics Dashboard (métriques temps réel)
 *   ├── 👥 User Management (gestion utilisateurs)
 *   ├── 🤖 Agent Orchestrator (contrôle des 287 agents)
 *   ├── 🌐 XR Environment Control (génération environnements)
 *   ├── 🎤 Voice/Avatar Manager (voix et avatars)
 *   ├── 📝 Prompt Engineering Lab (création prompts)
 *   ├── 🔐 Security Center (audit et sécurité)
 *   └── ⚙️ System Configuration (paramètres système)
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useCallback, createContext, useContext } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTE ADMIN COCKPIT
// ═══════════════════════════════════════════════════════════════════════════════

const AdminCockpitContext = createContext(null);

export const useAdminCockpit = () => {
  const context = useContext(AdminCockpitContext);
  if (!context) {
    throw new Error('useAdminCockpit must be used within AdminCockpitProvider');
  }
  return context;
};

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES SYSTÈME
// ═══════════════════════════════════════════════════════════════════════════════

export const AGENT_LEVELS = {
  L0: { name: 'System Core', color: '#FFFFFF', icon: '⚡', count: 3 },
  L1: { name: 'Orchestrator', color: '#D4AF37', icon: '🎯', count: 12 },
  L2: { name: 'Specialist', color: '#8B5CF6', icon: '🔧', count: 72 },
  L3: { name: 'Assistant', color: '#22C55E', icon: '💬', count: 200 }
};

export const XR_ENVIRONMENTS = [
  { id: 'nexus', name: 'Nexus Central', type: 'hub', frequency: 999 },
  { id: 'forge', name: 'Forge Créative', type: 'workspace', frequency: 528 },
  { id: 'sanctuaire', name: 'Sanctuaire', type: 'meditation', frequency: 432 },
  { id: 'bibliotheque', name: 'Bibliothèque Akashique', type: 'knowledge', frequency: 741 },
  { id: 'jardin', name: 'Jardin Quantique', type: 'relaxation', frequency: 396 },
  { id: 'observatoire', name: 'Observatoire Cosmique', type: 'exploration', frequency: 852 }
];

export const VOICE_PROFILES = [
  { id: 'nova', name: 'Nova', gender: 'neutral', tone: 'professional', pitch: 1.0 },
  { id: 'aria', name: 'Aria', gender: 'feminine', tone: 'warm', pitch: 1.1 },
  { id: 'orion', name: 'Orion', gender: 'masculine', tone: 'deep', pitch: 0.9 },
  { id: 'echo', name: 'Echo', gender: 'neutral', tone: 'ethereal', pitch: 1.05 },
  { id: 'sage', name: 'Sage', gender: 'neutral', tone: 'wise', pitch: 0.95 }
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MÉTRIQUES EN TEMPS RÉEL
// ═══════════════════════════════════════════════════════════════════════════════

const RealTimeMetric = ({ label, value, unit, trend, color = '#D4AF37' }) => {
  const trendIcon = trend > 0 ? '↑' : trend < 0 ? '↓' : '→';
  const trendColor = trend > 0 ? '#22C55E' : trend < 0 ? '#EF4444' : '#6B7280';

  return (
    <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
      <div className="text-xs text-gray-500 mb-1">{label}</div>
      <div className="flex items-end gap-2">
        <span className="text-2xl font-bold" style={{ color }}>{value}</span>
        <span className="text-sm text-gray-500 mb-1">{unit}</span>
        <span className="text-sm ml-auto" style={{ color: trendColor }}>
          {trendIcon} {Math.abs(trend)}%
        </span>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: ANALYTICS DASHBOARD
// ═══════════════════════════════════════════════════════════════════════════════

const AnalyticsDashboard = () => {
  const [metrics, setMetrics] = useState({
    activeUsers: 1247,
    agentsRunning: 156,
    requestsPerMin: 342,
    avgResponseTime: 0.8,
    systemLoad: 67,
    memoryUsage: 54,
    errorRate: 0.02,
    uptime: 99.97
  });

  const [activityLog, setActivityLog] = useState([
    { id: 1, time: '14:32:15', type: 'agent', message: 'Nova: Analyse terminée pour Sphère Business' },
    { id: 2, time: '14:31:42', type: 'user', message: 'Nouvel utilisateur inscrit: user_8847' },
    { id: 3, time: '14:30:58', type: 'system', message: 'XR Environment "Sanctuaire" généré' },
    { id: 4, time: '14:29:33', type: 'agent', message: 'Aria: Thread créatif ouvert avec 3 participants' },
    { id: 5, time: '14:28:01', type: 'security', message: 'Authentification MFA réussie: admin_principal' }
  ]);

  // Simulation de mise à jour en temps réel
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        activeUsers: prev.activeUsers + Math.floor(Math.random() * 10 - 5),
        requestsPerMin: prev.requestsPerMin + Math.floor(Math.random() * 20 - 10),
        avgResponseTime: Math.max(0.1, prev.avgResponseTime + (Math.random() * 0.2 - 0.1)),
        systemLoad: Math.min(100, Math.max(0, prev.systemLoad + Math.random() * 10 - 5))
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>📊</span> Analytics Dashboard
        </h2>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs text-green-500">Live</span>
        </div>
      </div>

      {/* Métriques principales */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <RealTimeMetric label="Utilisateurs Actifs" value={metrics.activeUsers} unit="" trend={5.2} />
        <RealTimeMetric label="Agents en Cours" value={metrics.agentsRunning} unit="/287" trend={12.3} color="#8B5CF6" />
        <RealTimeMetric label="Requêtes/min" value={metrics.requestsPerMin} unit="req" trend={-2.1} color="#22C55E" />
        <RealTimeMetric label="Temps Réponse" value={metrics.avgResponseTime.toFixed(2)} unit="s" trend={-8.5} color="#3B82F6" />
      </div>

      {/* Graphique système */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
          <h3 className="text-sm text-gray-400 mb-3">Charge Système</h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-gray-500">CPU</span>
                <span className="text-white">{metrics.systemLoad.toFixed(0)}%</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-green-500 to-yellow-500 transition-all duration-500"
                  style={{ width: `${metrics.systemLoad}%` }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-gray-500">Mémoire</span>
                <span className="text-white">{metrics.memoryUsage}%</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                  style={{ width: `${metrics.memoryUsage}%` }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-gray-500">Uptime</span>
                <span className="text-green-400">{metrics.uptime}%</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-green-500"
                  style={{ width: `${metrics.uptime}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Log d'activité */}
        <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
          <h3 className="text-sm text-gray-400 mb-3">Activité Récente</h3>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {activityLog.map(log => (
              <div key={log.id} className="flex items-start gap-2 text-xs">
                <span className="text-gray-600 font-mono">{log.time}</span>
                <span className={`px-1.5 py-0.5 rounded text-xs ${
                  log.type === 'agent' ? 'bg-purple-500/20 text-purple-400' :
                  log.type === 'user' ? 'bg-blue-500/20 text-blue-400' :
                  log.type === 'security' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-gray-500/20 text-gray-400'
                }`}>
                  {log.type}
                </span>
                <span className="text-gray-300 flex-1">{log.message}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: USER MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════════

const UserManagement = () => {
  const [users, setUsers] = useState([
    { id: 1, name: 'Jonathan Rodrigue', email: 'architect@che-nu.io', role: 'architect', status: 'active', spheres: 8 },
    { id: 2, name: 'Admin Principal', email: 'admin@che-nu.io', role: 'admin', status: 'active', spheres: 8 },
    { id: 3, name: 'Marie Dubois', email: 'marie@enterprise.com', role: 'enterprise', status: 'active', spheres: 4 },
    { id: 4, name: 'Service Public', email: 'contact@gouv.qc.ca', role: 'public_service', status: 'pending', spheres: 2 }
  ]);

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRole, setSelectedRole] = useState('all');

  const roles = {
    architect: { label: 'Architecte', color: '#FFFFFF', icon: '👑' },
    admin: { label: 'Admin', color: '#D4AF37', icon: '⚙️' },
    enterprise: { label: 'Entreprise', color: '#3B82F6', icon: '🏢' },
    public_service: { label: 'Service Public', color: '#22C55E', icon: '🏛️' },
    subcontractor: { label: 'Sous-traitant', color: '#8B5CF6', icon: '🔧' },
    user: { label: 'Utilisateur', color: '#6B7280', icon: '👤' }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = selectedRole === 'all' || user.role === selectedRole;
    return matchesSearch && matchesRole;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>👥</span> Gestion Utilisateurs
        </h2>
        <button className="px-4 py-2 bg-yellow-600 text-black rounded-lg text-sm hover:bg-yellow-500">
          + Nouvel Utilisateur
        </button>
      </div>

      {/* Filtres */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Rechercher..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 bg-black/50 border border-gray-700 rounded-lg px-4 py-2 text-white text-sm
            placeholder-gray-500 focus:outline-none focus:border-yellow-500"
        />
        <select
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
          className="bg-black/50 border border-gray-700 rounded-lg px-4 py-2 text-white text-sm
            focus:outline-none focus:border-yellow-500"
        >
          <option value="all">Tous les rôles</option>
          {Object.entries(roles).map(([key, { label }]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </select>
      </div>

      {/* Liste utilisateurs */}
      <div className="bg-black/50 rounded-xl border border-gray-800 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-800">
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Utilisateur</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Rôle</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Sphères</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Statut</th>
              <th className="px-4 py-3 text-left text-xs text-gray-500 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map(user => (
              <tr key={user.id} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                <td className="px-4 py-3">
                  <div>
                    <div className="text-sm text-white">{user.name}</div>
                    <div className="text-xs text-gray-500">{user.email}</div>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span
                    className="px-2 py-1 rounded text-xs"
                    style={{
                      backgroundColor: `${roles[user.role]?.color}20`,
                      color: roles[user.role]?.color
                    }}
                  >
                    {roles[user.role]?.icon} {roles[user.role]?.label}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className="text-sm text-gray-400">{user.spheres}/8</span>
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded text-xs ${
                    user.status === 'active' ? 'bg-green-500/20 text-green-400' :
                    user.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  }`}>
                    {user.status === 'active' ? 'Actif' : user.status === 'pending' ? 'En attente' : 'Inactif'}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex gap-2">
                    <button className="p-1.5 rounded hover:bg-gray-700 text-gray-400 hover:text-white">
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.5">
                        <path d="M7 1v12M1 7h12" />
                      </svg>
                    </button>
                    <button className="p-1.5 rounded hover:bg-gray-700 text-gray-400 hover:text-white">
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.5">
                        <circle cx="7" cy="7" r="6" />
                        <path d="M7 4v6M4 7h6" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: AGENT ORCHESTRATOR
// ═══════════════════════════════════════════════════════════════════════════════

const AgentOrchestrator = () => {
  const [agents, setAgents] = useState([
    { id: 'nova', name: 'Nova', level: 'L0', status: 'active', tasks: 12, accuracy: 98.5 },
    { id: 'aria', name: 'Aria', level: 'L1', status: 'active', tasks: 8, accuracy: 97.2 },
    { id: 'orion', name: 'Orion', level: 'L1', status: 'idle', tasks: 0, accuracy: 96.8 },
    { id: 'sage', name: 'Sage', level: 'L2', status: 'active', tasks: 23, accuracy: 95.4 },
    { id: 'echo', name: 'Echo', level: 'L2', status: 'processing', tasks: 5, accuracy: 94.1 }
  ]);

  const [selectedAgent, setSelectedAgent] = useState(null);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#22C55E';
      case 'processing': return '#3B82F6';
      case 'idle': return '#6B7280';
      case 'error': return '#EF4444';
      default: return '#6B7280';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>🤖</span> Agent Orchestrator
        </h2>
        <div className="flex gap-2">
          <button className="px-3 py-1.5 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700">
            Tout Activer
          </button>
          <button className="px-3 py-1.5 bg-yellow-600 text-black rounded-lg text-sm hover:bg-yellow-500">
            + Nouvel Agent
          </button>
        </div>
      </div>

      {/* Statistiques par niveau */}
      <div className="grid grid-cols-4 gap-4">
        {Object.entries(AGENT_LEVELS).map(([level, config]) => (
          <div
            key={level}
            className="bg-black/50 rounded-xl p-4 border border-gray-800"
            style={{ borderLeftColor: config.color, borderLeftWidth: 3 }}
          >
            <div className="flex items-center gap-2 mb-2">
              <span>{config.icon}</span>
              <span className="text-sm font-medium text-white">{level}</span>
            </div>
            <div className="text-xs text-gray-500">{config.name}</div>
            <div className="text-lg font-bold mt-1" style={{ color: config.color }}>
              {agents.filter(a => a.level === level).length}/{config.count}
            </div>
          </div>
        ))}
      </div>

      {/* Liste des agents */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map(agent => (
          <div
            key={agent.id}
            onClick={() => setSelectedAgent(agent)}
            className={`bg-black/50 rounded-xl p-4 border cursor-pointer transition-all ${
              selectedAgent?.id === agent.id ? 'border-yellow-500' : 'border-gray-800 hover:border-gray-700'
            }`}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div
                  className="w-10 h-10 rounded-full flex items-center justify-center text-lg"
                  style={{ backgroundColor: `${AGENT_LEVELS[agent.level]?.color}20` }}
                >
                  {agent.name[0]}
                </div>
                <div>
                  <div className="text-sm font-medium text-white">{agent.name}</div>
                  <div className="text-xs text-gray-500">{agent.level} - {AGENT_LEVELS[agent.level]?.name}</div>
                </div>
              </div>
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: getStatusColor(agent.status) }}
              />
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-gray-900/50 rounded p-2">
                <div className="text-gray-500">Tâches actives</div>
                <div className="text-white font-medium">{agent.tasks}</div>
              </div>
              <div className="bg-gray-900/50 rounded p-2">
                <div className="text-gray-500">Précision</div>
                <div className="text-green-400 font-medium">{agent.accuracy}%</div>
              </div>
            </div>

            <div className="flex gap-2 mt-3">
              <button className="flex-1 px-3 py-1.5 bg-gray-800 text-gray-300 rounded text-xs hover:bg-gray-700">
                Configurer
              </button>
              <button className="flex-1 px-3 py-1.5 bg-purple-600 text-white rounded text-xs hover:bg-purple-500">
                Dialogue
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: XR ENVIRONMENT CONTROL
// ═══════════════════════════════════════════════════════════════════════════════

const XREnvironmentControl = () => {
  const [environments, setEnvironments] = useState(XR_ENVIRONMENTS);
  const [activeEnv, setActiveEnv] = useState(null);
  const [generatingEnv, setGeneratingEnv] = useState(null);

  const generateEnvironment = async (envId) => {
    setGeneratingEnv(envId);
    // Simulation de génération
    await new Promise(resolve => setTimeout(resolve, 3000));
    setGeneratingEnv(null);
    setActiveEnv(envId);
  };

  const envTypes = {
    hub: { icon: '🌐', color: '#D4AF37' },
    workspace: { icon: '🔧', color: '#3B82F6' },
    meditation: { icon: '🧘', color: '#8B5CF6' },
    knowledge: { icon: '📚', color: '#22C55E' },
    relaxation: { icon: '🌿', color: '#10B981' },
    exploration: { icon: '🔭', color: '#EC4899' }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>🌐</span> XR Environment Control
        </h2>
        <button className="px-4 py-2 bg-purple-600 text-white rounded-lg text-sm hover:bg-purple-500">
          + Créer Environnement
        </button>
      </div>

      {/* Prévisualisation active */}
      {activeEnv && (
        <div className="bg-gradient-to-br from-purple-900/50 to-black rounded-xl p-6 border border-purple-500/30">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-bold text-white">
                {environments.find(e => e.id === activeEnv)?.name}
              </h3>
              <p className="text-sm text-gray-400">
                Fréquence: {environments.find(e => e.id === activeEnv)?.frequency} Hz
              </p>
            </div>
            <button
              onClick={() => setActiveEnv(null)}
              className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-500"
            >
              Fermer
            </button>
          </div>

          {/* Canvas 3D Placeholder */}
          <div className="aspect-video bg-black/50 rounded-lg flex items-center justify-center border border-gray-800">
            <div className="text-center">
              <div className="text-6xl mb-4">🌌</div>
              <p className="text-gray-400">Environnement XR Actif</p>
              <p className="text-sm text-gray-600 mt-2">WebXR / Three.js Canvas</p>
            </div>
          </div>

          {/* Contrôles XR */}
          <div className="grid grid-cols-4 gap-4 mt-4">
            <button className="p-3 bg-gray-800 rounded-lg text-center hover:bg-gray-700">
              <span className="block text-xl mb-1">🎮</span>
              <span className="text-xs text-gray-400">VR Mode</span>
            </button>
            <button className="p-3 bg-gray-800 rounded-lg text-center hover:bg-gray-700">
              <span className="block text-xl mb-1">📱</span>
              <span className="text-xs text-gray-400">AR Mode</span>
            </button>
            <button className="p-3 bg-gray-800 rounded-lg text-center hover:bg-gray-700">
              <span className="block text-xl mb-1">🔊</span>
              <span className="text-xs text-gray-400">Spatial Audio</span>
            </button>
            <button className="p-3 bg-gray-800 rounded-lg text-center hover:bg-gray-700">
              <span className="block text-xl mb-1">👥</span>
              <span className="text-xs text-gray-400">Multi-User</span>
            </button>
          </div>
        </div>
      )}

      {/* Grille des environnements */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {environments.map(env => (
          <div
            key={env.id}
            className={`bg-black/50 rounded-xl p-4 border transition-all ${
              activeEnv === env.id ? 'border-purple-500' : 'border-gray-800 hover:border-gray-700'
            }`}
          >
            <div className="flex items-center gap-3 mb-3">
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                style={{ backgroundColor: `${envTypes[env.type]?.color}20` }}
              >
                {envTypes[env.type]?.icon}
              </div>
              <div>
                <h3 className="text-sm font-medium text-white">{env.name}</h3>
                <p className="text-xs text-gray-500">{env.frequency} Hz</p>
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => generateEnvironment(env.id)}
                disabled={generatingEnv === env.id}
                className={`flex-1 px-3 py-2 rounded-lg text-sm transition-all ${
                  generatingEnv === env.id
                    ? 'bg-purple-600/50 text-purple-300'
                    : 'bg-purple-600 text-white hover:bg-purple-500'
                }`}
              >
                {generatingEnv === env.id ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Génération...
                  </span>
                ) : (
                  'Générer'
                )}
              </button>
              <button className="px-3 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700">
                ⚙️
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: VOICE/AVATAR MANAGER
// ═══════════════════════════════════════════════════════════════════════════════

const VoiceAvatarManager = () => {
  const [voices, setVoices] = useState(VOICE_PROFILES);
  const [selectedVoice, setSelectedVoice] = useState(null);
  const [testText, setTestText] = useState('Bienvenue dans l\'univers CHE·NU');
  const [isPlaying, setIsPlaying] = useState(false);

  const testVoice = (voiceId) => {
    setIsPlaying(voiceId);
    // Simulation de lecture audio
    setTimeout(() => setIsPlaying(null), 3000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>🎤</span> Voice & Avatar Manager
        </h2>
        <button className="px-4 py-2 bg-pink-600 text-white rounded-lg text-sm hover:bg-pink-500">
          + Nouvelle Voix
        </button>
      </div>

      {/* Test de voix */}
      <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
        <h3 className="text-sm text-gray-400 mb-3">Test de Synthèse Vocale</h3>
        <div className="flex gap-4">
          <input
            type="text"
            value={testText}
            onChange={(e) => setTestText(e.target.value)}
            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white text-sm
              placeholder-gray-500 focus:outline-none focus:border-pink-500"
            placeholder="Texte à synthétiser..."
          />
          <button
            disabled={!selectedVoice}
            className={`px-4 py-2 rounded-lg text-sm ${
              selectedVoice
                ? 'bg-pink-600 text-white hover:bg-pink-500'
                : 'bg-gray-800 text-gray-600 cursor-not-allowed'
            }`}
          >
            🔊 Tester
          </button>
        </div>
      </div>

      {/* Profils de voix */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {voices.map(voice => (
          <div
            key={voice.id}
            onClick={() => setSelectedVoice(voice.id)}
            className={`bg-black/50 rounded-xl p-4 border cursor-pointer transition-all ${
              selectedVoice === voice.id ? 'border-pink-500' : 'border-gray-800 hover:border-gray-700'
            }`}
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="w-14 h-14 rounded-full bg-gradient-to-br from-pink-500/20 to-purple-500/20
                flex items-center justify-center text-2xl">
                {voice.gender === 'feminine' ? '👩' : voice.gender === 'masculine' ? '👨' : '🤖'}
              </div>
              <div>
                <h3 className="text-sm font-medium text-white">{voice.name}</h3>
                <p className="text-xs text-gray-500 capitalize">{voice.tone}</p>
              </div>
            </div>

            {/* Paramètres voix */}
            <div className="space-y-2">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-500">Pitch</span>
                  <span className="text-white">{voice.pitch}</span>
                </div>
                <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-pink-500"
                    style={{ width: `${voice.pitch * 50}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="flex gap-2 mt-4">
              <button
                onClick={(e) => { e.stopPropagation(); testVoice(voice.id); }}
                className={`flex-1 px-3 py-2 rounded-lg text-sm transition-all ${
                  isPlaying === voice.id
                    ? 'bg-pink-600/50 text-pink-300'
                    : 'bg-pink-600 text-white hover:bg-pink-500'
                }`}
              >
                {isPlaying === voice.id ? '🔊 Lecture...' : '▶️ Écouter'}
              </button>
              <button className="px-3 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700">
                ⚙️
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Avatar 3D Preview */}
      <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
        <h3 className="text-sm text-gray-400 mb-3">Avatar 3D Preview</h3>
        <div className="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4">🧑‍💻</div>
            <p className="text-gray-400">Sélectionnez une voix pour voir l'avatar</p>
            <p className="text-sm text-gray-600 mt-2">Lip-sync & expressions faciales</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: PROMPT ENGINEERING LAB
// ═══════════════════════════════════════════════════════════════════════════════

const PromptEngineeringLab = () => {
  const [prompts, setPrompts] = useState([
    {
      id: 1,
      name: 'Analyse Arithmos',
      category: 'calculation',
      template: 'Analyse le mot "{input}" selon la méthode Arithmos pythagoricienne...',
      variables: ['input'],
      usage: 1247
    },
    {
      id: 2,
      name: 'Génération Environnement XR',
      category: 'xr',
      template: 'Génère un environnement 3D basé sur la fréquence {frequency}Hz avec l\'ambiance {mood}...',
      variables: ['frequency', 'mood'],
      usage: 432
    },
    {
      id: 3,
      name: 'Dialogue Agent',
      category: 'agent',
      template: 'Tu es {agent_name}, un agent {level} spécialisé en {specialty}. Réponds à: {query}',
      variables: ['agent_name', 'level', 'specialty', 'query'],
      usage: 3521
    }
  ]);

  const [activePrompt, setActivePrompt] = useState(null);
  const [testVariables, setTestVariables] = useState({});
  const [testResult, setTestResult] = useState('');

  const categories = {
    calculation: { label: 'Calcul', color: '#D4AF37', icon: '🔢' },
    xr: { label: 'XR/3D', color: '#8B5CF6', icon: '🌐' },
    agent: { label: 'Agent', color: '#22C55E', icon: '🤖' },
    voice: { label: 'Voix', color: '#EC4899', icon: '🎤' },
    analysis: { label: 'Analyse', color: '#3B82F6', icon: '📊' }
  };

  const testPrompt = () => {
    if (!activePrompt) return;
    let result = activePrompt.template;
    Object.entries(testVariables).forEach(([key, value]) => {
      result = result.replace(`{${key}}`, value || `[${key}]`);
    });
    setTestResult(result);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>📝</span> Prompt Engineering Lab
        </h2>
        <button className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-500">
          + Nouveau Prompt
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Liste des prompts */}
        <div className="space-y-4">
          <h3 className="text-sm text-gray-400">Bibliothèque de Prompts</h3>
          {prompts.map(prompt => (
            <div
              key={prompt.id}
              onClick={() => {
                setActivePrompt(prompt);
                setTestVariables({});
                setTestResult('');
              }}
              className={`bg-black/50 rounded-xl p-4 border cursor-pointer transition-all ${
                activePrompt?.id === prompt.id ? 'border-green-500' : 'border-gray-800 hover:border-gray-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span
                    className="px-2 py-0.5 rounded text-xs"
                    style={{
                      backgroundColor: `${categories[prompt.category]?.color}20`,
                      color: categories[prompt.category]?.color
                    }}
                  >
                    {categories[prompt.category]?.icon} {categories[prompt.category]?.label}
                  </span>
                  <span className="text-sm font-medium text-white">{prompt.name}</span>
                </div>
                <span className="text-xs text-gray-500">{prompt.usage} utilisations</span>
              </div>
              <p className="text-xs text-gray-500 line-clamp-2">{prompt.template}</p>
              <div className="flex gap-1 mt-2">
                {prompt.variables.map(v => (
                  <span key={v} className="px-1.5 py-0.5 bg-gray-800 rounded text-xs text-gray-400">
                    {`{${v}}`}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Zone de test */}
        <div className="space-y-4">
          <h3 className="text-sm text-gray-400">Zone de Test</h3>
          {activePrompt ? (
            <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
              <h4 className="text-sm font-medium text-white mb-4">{activePrompt.name}</h4>

              {/* Variables */}
              <div className="space-y-3 mb-4">
                {activePrompt.variables.map(variable => (
                  <div key={variable}>
                    <label className="block text-xs text-gray-500 mb-1">{variable}</label>
                    <input
                      type="text"
                      value={testVariables[variable] || ''}
                      onChange={(e) => setTestVariables(prev => ({ ...prev, [variable]: e.target.value }))}
                      className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white
                        placeholder-gray-600 focus:outline-none focus:border-green-500"
                      placeholder={`Valeur pour {${variable}}`}
                    />
                  </div>
                ))}
              </div>

              <button
                onClick={testPrompt}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-500 mb-4"
              >
                ▶️ Exécuter le Prompt
              </button>

              {/* Résultat */}
              {testResult && (
                <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
                  <h5 className="text-xs text-gray-500 mb-2">Résultat:</h5>
                  <p className="text-sm text-white whitespace-pre-wrap">{testResult}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-black/50 rounded-xl p-8 border border-gray-800 text-center">
              <span className="text-4xl block mb-4">📝</span>
              <p className="text-gray-400">Sélectionnez un prompt pour le tester</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: SECURITY CENTER
// ═══════════════════════════════════════════════════════════════════════════════

const SecurityCenter = () => {
  const [auditLogs, setAuditLogs] = useState([
    { id: 1, time: '14:32:15', user: 'admin@che-nu.io', action: 'LOGIN', status: 'success', ip: '192.168.1.1' },
    { id: 2, time: '14:28:42', user: 'marie@enterprise.com', action: 'ACCESS_DENIED', status: 'blocked', ip: '10.0.0.45' },
    { id: 3, time: '14:25:18', user: 'system', action: 'BACKUP_COMPLETE', status: 'success', ip: 'localhost' },
    { id: 4, time: '14:20:33', user: 'admin@che-nu.io', action: 'USER_CREATE', status: 'success', ip: '192.168.1.1' },
    { id: 5, time: '14:15:01', user: 'unknown', action: 'LOGIN_ATTEMPT', status: 'failed', ip: '203.0.113.42' }
  ]);

  const [securityScore, setSecurityScore] = useState(94);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>🔐</span> Security Center
        </h2>
        <button className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-500">
          🚨 Mode Alerte
        </button>
      </div>

      {/* Score de sécurité */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-black/50 rounded-xl p-6 border border-gray-800 text-center">
          <div className="text-5xl font-bold mb-2" style={{
            color: securityScore >= 90 ? '#22C55E' : securityScore >= 70 ? '#EAB308' : '#EF4444'
          }}>
            {securityScore}
          </div>
          <p className="text-sm text-gray-400">Score de Sécurité</p>
        </div>
        <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
          <h3 className="text-sm text-gray-400 mb-3">Menaces Détectées</h3>
          <div className="text-3xl font-bold text-yellow-500">3</div>
          <p className="text-xs text-gray-500 mt-1">Dernières 24h</p>
        </div>
        <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
          <h3 className="text-sm text-gray-400 mb-3">Tentatives Bloquées</h3>
          <div className="text-3xl font-bold text-red-500">12</div>
          <p className="text-xs text-gray-500 mt-1">Dernières 24h</p>
        </div>
      </div>

      {/* Journal d'audit */}
      <div className="bg-black/50 rounded-xl border border-gray-800 overflow-hidden">
        <div className="p-4 border-b border-gray-800">
          <h3 className="text-sm font-medium text-white">Journal d'Audit</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-800">
                <th className="px-4 py-3 text-left text-xs text-gray-500">Heure</th>
                <th className="px-4 py-3 text-left text-xs text-gray-500">Utilisateur</th>
                <th className="px-4 py-3 text-left text-xs text-gray-500">Action</th>
                <th className="px-4 py-3 text-left text-xs text-gray-500">Statut</th>
                <th className="px-4 py-3 text-left text-xs text-gray-500">IP</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.map(log => (
                <tr key={log.id} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                  <td className="px-4 py-3 text-sm text-gray-400 font-mono">{log.time}</td>
                  <td className="px-4 py-3 text-sm text-white">{log.user}</td>
                  <td className="px-4 py-3 text-sm text-gray-300">{log.action}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      log.status === 'success' ? 'bg-green-500/20 text-green-400' :
                      log.status === 'blocked' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-red-500/20 text-red-400'
                    }`}>
                      {log.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500 font-mono">{log.ip}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: SETUP WIZARD - CONFIGURATION DES CONNEXIONS
// ═══════════════════════════════════════════════════════════════════════════════

const SetupWizard = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [connectionStatus, setConnectionStatus] = useState({
    supabase: { status: 'unconfigured', message: '' },
    llm: { status: 'unconfigured', message: '' },
    websocket: { status: 'unconfigured', message: '' },
    storage: { status: 'unconfigured', message: '' },
    analytics: { status: 'unconfigured', message: '' }
  });

  const [config, setConfig] = useState({
    // Supabase
    supabaseUrl: process.env.REACT_APP_SUPABASE_URL || '',
    supabaseAnonKey: process.env.REACT_APP_SUPABASE_ANON_KEY || '',

    // LLM API
    llmProvider: 'openai',
    llmApiKey: process.env.REACT_APP_LLM_API_KEY || '',
    llmModel: 'gpt-4',
    llmEndpoint: '',

    // WebSocket
    websocketUrl: process.env.REACT_APP_WS_URL || 'wss://api.che-nu.io/ws',

    // Storage
    storageProvider: 'supabase',
    storageBucket: 'atom-files',

    // Analytics
    analyticsEndpoint: process.env.REACT_APP_ANALYTICS_URL || ''
  });

  const [testing, setTesting] = useState(null);
  const [showKeys, setShowKeys] = useState({});

  const steps = [
    { id: 'supabase', name: 'Supabase', icon: '🗄️', description: 'Base de données et authentification' },
    { id: 'llm', name: 'LLM API', icon: '🤖', description: 'Intelligence artificielle (OpenAI, Anthropic, etc.)' },
    { id: 'websocket', name: 'WebSocket', icon: '🔌', description: 'Communication temps réel' },
    { id: 'storage', name: 'Storage', icon: '💾', description: 'Stockage de fichiers' },
    { id: 'analytics', name: 'Analytics', icon: '📈', description: 'Suivi et métriques' }
  ];

  const updateConfig = (key, value) => {
    setConfig(prev => ({ ...prev, [key]: value }));
  };

  const testConnection = async (service) => {
    setTesting(service);
    setConnectionStatus(prev => ({
      ...prev,
      [service]: { status: 'testing', message: 'Test en cours...' }
    }));

    try {
      let result = { success: false, message: '' };

      switch (service) {
        case 'supabase':
          if (!config.supabaseUrl || !config.supabaseAnonKey) {
            result = { success: false, message: 'URL et Anon Key requis' };
          } else {
            // Test real Supabase connection
            const response = await fetch(`${config.supabaseUrl}/rest/v1/`, {
              headers: {
                'apikey': config.supabaseAnonKey,
                'Authorization': `Bearer ${config.supabaseAnonKey}`
              }
            });
            result = response.ok
              ? { success: true, message: 'Connexion Supabase réussie!' }
              : { success: false, message: `Erreur: ${response.status}` };
          }
          break;

        case 'llm':
          if (!config.llmApiKey) {
            result = { success: false, message: 'Clé API requise' };
          } else {
            // Test LLM API
            const endpoint = config.llmProvider === 'openai'
              ? 'https://api.openai.com/v1/models'
              : config.llmProvider === 'anthropic'
              ? 'https://api.anthropic.com/v1/messages'
              : config.llmEndpoint;

            const headers = config.llmProvider === 'openai'
              ? { 'Authorization': `Bearer ${config.llmApiKey}` }
              : config.llmProvider === 'anthropic'
              ? { 'x-api-key': config.llmApiKey, 'anthropic-version': '2023-06-01' }
              : { 'Authorization': `Bearer ${config.llmApiKey}` };

            try {
              const response = await fetch(endpoint, { method: 'GET', headers });
              result = response.ok || response.status === 405
                ? { success: true, message: `Connexion ${config.llmProvider} réussie!` }
                : { success: false, message: `Erreur API: ${response.status}` };
            } catch (e) {
              result = { success: false, message: 'Erreur de connexion API' };
            }
          }
          break;

        case 'websocket':
          if (!config.websocketUrl) {
            result = { success: false, message: 'URL WebSocket requise' };
          } else {
            try {
              const ws = new WebSocket(config.websocketUrl);
              await new Promise((resolve, reject) => {
                ws.onopen = () => { ws.close(); resolve(); };
                ws.onerror = reject;
                setTimeout(() => reject(new Error('Timeout')), 5000);
              });
              result = { success: true, message: 'Connexion WebSocket réussie!' };
            } catch (e) {
              result = { success: false, message: 'Impossible de se connecter au WebSocket' };
            }
          }
          break;

        case 'storage':
          if (config.storageProvider === 'supabase' && config.supabaseUrl) {
            result = { success: true, message: 'Storage Supabase configuré' };
          } else {
            result = { success: false, message: 'Configuration storage requise' };
          }
          break;

        case 'analytics':
          if (!config.analyticsEndpoint) {
            result = { success: true, message: 'Analytics désactivé (optionnel)' };
          } else {
            try {
              const response = await fetch(config.analyticsEndpoint, { method: 'HEAD' });
              result = response.ok
                ? { success: true, message: 'Endpoint analytics accessible' }
                : { success: false, message: 'Endpoint non accessible' };
            } catch (e) {
              result = { success: false, message: 'Erreur connexion analytics' };
            }
          }
          break;

        default:
          result = { success: false, message: 'Service inconnu' };
      }

      setConnectionStatus(prev => ({
        ...prev,
        [service]: {
          status: result.success ? 'connected' : 'error',
          message: result.message
        }
      }));
    } catch (error) {
      setConnectionStatus(prev => ({
        ...prev,
        [service]: { status: 'error', message: error.message }
      }));
    }

    setTesting(null);
  };

  const testAllConnections = async () => {
    for (const step of steps) {
      await testConnection(step.id);
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  };

  const saveConfiguration = () => {
    // Save to localStorage for persistence
    localStorage.setItem('atom_api_config', JSON.stringify(config));

    // Create .env content for user to copy
    const envContent = `# AT·OM API Configuration
# Generated: ${new Date().toISOString()}

# Supabase
REACT_APP_SUPABASE_URL=${config.supabaseUrl}
REACT_APP_SUPABASE_ANON_KEY=${config.supabaseAnonKey}

# LLM API
REACT_APP_LLM_PROVIDER=${config.llmProvider}
REACT_APP_LLM_API_KEY=${config.llmApiKey}
REACT_APP_LLM_MODEL=${config.llmModel}
${config.llmEndpoint ? `REACT_APP_LLM_ENDPOINT=${config.llmEndpoint}` : ''}

# WebSocket
REACT_APP_WS_URL=${config.websocketUrl}

# Storage
REACT_APP_STORAGE_PROVIDER=${config.storageProvider}
REACT_APP_STORAGE_BUCKET=${config.storageBucket}

# Analytics
${config.analyticsEndpoint ? `REACT_APP_ANALYTICS_URL=${config.analyticsEndpoint}` : '# REACT_APP_ANALYTICS_URL='}
`;

    // Copy to clipboard
    navigator.clipboard?.writeText(envContent);
    alert('Configuration sauvegardée! Contenu .env copié dans le presse-papier.');
  };

  const exportConfig = () => {
    const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'atom-config.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const importConfig = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const imported = JSON.parse(e.target?.result);
          setConfig(prev => ({ ...prev, ...imported }));
        } catch (err) {
          alert('Erreur lors de l\'import du fichier');
        }
      };
      reader.readAsText(file);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'connected': return '✅';
      case 'error': return '❌';
      case 'testing': return '⏳';
      default: return '⚪';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'connected': return '#22C55E';
      case 'error': return '#EF4444';
      case 'testing': return '#EAB308';
      default: return '#6B7280';
    }
  };

  // Load saved config on mount
  useEffect(() => {
    const saved = localStorage.getItem('atom_api_config');
    if (saved) {
      try {
        setConfig(prev => ({ ...prev, ...JSON.parse(saved) }));
      } catch (e) {
        console.warn('Failed to load saved config');
      }
    }
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>🔧</span> Setup Wizard - Configuration des Connexions
        </h2>
        <div className="flex gap-2">
          <button
            onClick={testAllConnections}
            disabled={testing !== null}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-500 disabled:opacity-50"
          >
            🔄 Tester Tout
          </button>
          <button
            onClick={saveConfiguration}
            className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-500"
          >
            💾 Sauvegarder
          </button>
        </div>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-5 gap-4">
        {steps.map((step, index) => (
          <button
            key={step.id}
            onClick={() => setActiveStep(index)}
            className={`p-4 rounded-xl border transition-all ${
              activeStep === index
                ? 'bg-yellow-500/20 border-yellow-500'
                : 'bg-black/50 border-gray-800 hover:border-gray-700'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">{step.icon}</span>
              <span>{getStatusIcon(connectionStatus[step.id].status)}</span>
            </div>
            <div className="text-sm font-medium text-white text-left">{step.name}</div>
            <div
              className="text-xs mt-1 text-left truncate"
              style={{ color: getStatusColor(connectionStatus[step.id].status) }}
            >
              {connectionStatus[step.id].message || 'Non configuré'}
            </div>
          </button>
        ))}
      </div>

      {/* Step Content */}
      <div className="bg-black/50 rounded-xl p-6 border border-gray-800">
        {/* Supabase Configuration */}
        {activeStep === 0 && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">🗄️</span>
              <div>
                <h3 className="text-lg font-bold text-white">Configuration Supabase</h3>
                <p className="text-sm text-gray-500">Base de données PostgreSQL et authentification</p>
              </div>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Supabase URL</label>
              <input
                type="text"
                value={config.supabaseUrl}
                onChange={(e) => updateConfig('supabaseUrl', e.target.value)}
                placeholder="https://xxxx.supabase.co"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                  placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Anon Key (Public)</label>
              <div className="relative">
                <input
                  type={showKeys.supabaseAnonKey ? 'text' : 'password'}
                  value={config.supabaseAnonKey}
                  onChange={(e) => updateConfig('supabaseAnonKey', e.target.value)}
                  placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                    placeholder-gray-600 focus:outline-none focus:border-yellow-500 pr-12"
                />
                <button
                  type="button"
                  onClick={() => setShowKeys(prev => ({ ...prev, supabaseAnonKey: !prev.supabaseAnonKey }))}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
                >
                  {showKeys.supabaseAnonKey ? '🙈' : '👁️'}
                </button>
              </div>
            </div>

            <div className="p-4 bg-gray-900/50 rounded-lg border border-gray-800">
              <h4 className="text-sm font-medium text-white mb-2">📘 Instructions</h4>
              <ol className="text-xs text-gray-400 space-y-1 list-decimal list-inside">
                <li>Créez un projet sur <span className="text-blue-400">supabase.com</span></li>
                <li>Allez dans Settings → API</li>
                <li>Copiez l'URL du projet et l'Anon Key</li>
                <li>Exécutez le script SQL pour créer les tables (voir supabase-schema.sql)</li>
              </ol>
            </div>

            <button
              onClick={() => testConnection('supabase')}
              disabled={testing === 'supabase'}
              className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-500 disabled:opacity-50"
            >
              {testing === 'supabase' ? '⏳ Test en cours...' : '🔌 Tester la Connexion'}
            </button>
          </div>
        )}

        {/* LLM API Configuration */}
        {activeStep === 1 && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">🤖</span>
              <div>
                <h3 className="text-lg font-bold text-white">Configuration LLM API</h3>
                <p className="text-sm text-gray-500">Intelligence artificielle pour les agents</p>
              </div>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Fournisseur LLM</label>
              <select
                value={config.llmProvider}
                onChange={(e) => updateConfig('llmProvider', e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                  focus:outline-none focus:border-yellow-500"
              >
                <option value="openai">OpenAI (GPT-4, GPT-3.5)</option>
                <option value="anthropic">Anthropic (Claude)</option>
                <option value="local">Local / Self-Hosted</option>
                <option value="custom">Custom Endpoint</option>
              </select>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Clé API</label>
              <div className="relative">
                <input
                  type={showKeys.llmApiKey ? 'text' : 'password'}
                  value={config.llmApiKey}
                  onChange={(e) => updateConfig('llmApiKey', e.target.value)}
                  placeholder={config.llmProvider === 'openai' ? 'sk-...' : 'sk-ant-...'}
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                    placeholder-gray-600 focus:outline-none focus:border-yellow-500 pr-12"
                />
                <button
                  type="button"
                  onClick={() => setShowKeys(prev => ({ ...prev, llmApiKey: !prev.llmApiKey }))}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
                >
                  {showKeys.llmApiKey ? '🙈' : '👁️'}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Modèle</label>
              <select
                value={config.llmModel}
                onChange={(e) => updateConfig('llmModel', e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                  focus:outline-none focus:border-yellow-500"
              >
                {config.llmProvider === 'openai' && (
                  <>
                    <option value="gpt-4">GPT-4 (Recommandé)</option>
                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                  </>
                )}
                {config.llmProvider === 'anthropic' && (
                  <>
                    <option value="claude-3-opus">Claude 3 Opus</option>
                    <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                    <option value="claude-3-haiku">Claude 3 Haiku</option>
                  </>
                )}
                {(config.llmProvider === 'local' || config.llmProvider === 'custom') && (
                  <option value="custom">Custom Model</option>
                )}
              </select>
            </div>

            {(config.llmProvider === 'local' || config.llmProvider === 'custom') && (
              <div>
                <label className="block text-xs text-gray-500 mb-2">Endpoint URL</label>
                <input
                  type="text"
                  value={config.llmEndpoint}
                  onChange={(e) => updateConfig('llmEndpoint', e.target.value)}
                  placeholder="http://localhost:8000/v1/chat/completions"
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                    placeholder-gray-600 focus:outline-none focus:border-yellow-500"
                />
              </div>
            )}

            <button
              onClick={() => testConnection('llm')}
              disabled={testing === 'llm'}
              className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-500 disabled:opacity-50"
            >
              {testing === 'llm' ? '⏳ Test en cours...' : '🔌 Tester la Connexion'}
            </button>
          </div>
        )}

        {/* WebSocket Configuration */}
        {activeStep === 2 && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">🔌</span>
              <div>
                <h3 className="text-lg font-bold text-white">Configuration WebSocket</h3>
                <p className="text-sm text-gray-500">Communication temps réel bidirectionnelle</p>
              </div>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">WebSocket URL</label>
              <input
                type="text"
                value={config.websocketUrl}
                onChange={(e) => updateConfig('websocketUrl', e.target.value)}
                placeholder="wss://api.example.com/ws"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                  placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>

            <div className="p-4 bg-gray-900/50 rounded-lg border border-gray-800">
              <h4 className="text-sm font-medium text-white mb-2">💡 Note</h4>
              <p className="text-xs text-gray-400">
                Le WebSocket est optionnel. Sans WebSocket, l'application fonctionnera en mode polling
                pour les mises à jour temps réel (moins performant mais fonctionnel).
              </p>
            </div>

            <button
              onClick={() => testConnection('websocket')}
              disabled={testing === 'websocket'}
              className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-500 disabled:opacity-50"
            >
              {testing === 'websocket' ? '⏳ Test en cours...' : '🔌 Tester la Connexion'}
            </button>
          </div>
        )}

        {/* Storage Configuration */}
        {activeStep === 3 && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">💾</span>
              <div>
                <h3 className="text-lg font-bold text-white">Configuration Storage</h3>
                <p className="text-sm text-gray-500">Stockage de fichiers et médias</p>
              </div>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Fournisseur Storage</label>
              <select
                value={config.storageProvider}
                onChange={(e) => updateConfig('storageProvider', e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                  focus:outline-none focus:border-yellow-500"
              >
                <option value="supabase">Supabase Storage (Recommandé)</option>
                <option value="s3">Amazon S3</option>
                <option value="cloudflare">Cloudflare R2</option>
                <option value="local">Local Storage</option>
              </select>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Bucket Name</label>
              <input
                type="text"
                value={config.storageBucket}
                onChange={(e) => updateConfig('storageBucket', e.target.value)}
                placeholder="atom-files"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                  placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>

            <div className="p-4 bg-green-900/20 rounded-lg border border-green-800">
              <h4 className="text-sm font-medium text-green-400 mb-2">✨ Recommandation</h4>
              <p className="text-xs text-gray-400">
                Si vous utilisez Supabase pour la base de données, utilisez également Supabase Storage
                pour simplifier la gestion et bénéficier de la même authentification.
              </p>
            </div>

            <button
              onClick={() => testConnection('storage')}
              disabled={testing === 'storage'}
              className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-500 disabled:opacity-50"
            >
              {testing === 'storage' ? '⏳ Test en cours...' : '🔌 Tester la Configuration'}
            </button>
          </div>
        )}

        {/* Analytics Configuration */}
        {activeStep === 4 && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">📈</span>
              <div>
                <h3 className="text-lg font-bold text-white">Configuration Analytics</h3>
                <p className="text-sm text-gray-500">Suivi et métriques d'utilisation</p>
              </div>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Analytics Endpoint (Optionnel)</label>
              <input
                type="text"
                value={config.analyticsEndpoint}
                onChange={(e) => updateConfig('analyticsEndpoint', e.target.value)}
                placeholder="https://analytics.example.com/collect"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white
                  placeholder-gray-600 focus:outline-none focus:border-yellow-500"
              />
            </div>

            <div className="p-4 bg-gray-900/50 rounded-lg border border-gray-800">
              <h4 className="text-sm font-medium text-white mb-2">💡 Note</h4>
              <p className="text-xs text-gray-400">
                L'analytics est optionnel. Laissez vide pour désactiver le suivi.
                Vous pouvez utiliser un service comme Plausible, Umami, ou votre propre endpoint.
              </p>
            </div>

            <button
              onClick={() => testConnection('analytics')}
              disabled={testing === 'analytics'}
              className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-500 disabled:opacity-50"
            >
              {testing === 'analytics' ? '⏳ Test en cours...' : '🔌 Tester la Configuration'}
            </button>
          </div>
        )}
      </div>

      {/* Navigation and Actions */}
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          <button
            onClick={() => setActiveStep(Math.max(0, activeStep - 1))}
            disabled={activeStep === 0}
            className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700 disabled:opacity-50"
          >
            ← Précédent
          </button>
          <button
            onClick={() => setActiveStep(Math.min(steps.length - 1, activeStep + 1))}
            disabled={activeStep === steps.length - 1}
            className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700 disabled:opacity-50"
          >
            Suivant →
          </button>
        </div>

        <div className="flex gap-2">
          <label className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700 cursor-pointer">
            📥 Importer
            <input type="file" accept=".json" onChange={importConfig} className="hidden" />
          </label>
          <button
            onClick={exportConfig}
            className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg text-sm hover:bg-gray-700"
          >
            📤 Exporter
          </button>
        </div>
      </div>

      {/* Summary */}
      <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
        <h3 className="text-sm font-medium text-white mb-3">📋 Résumé de Configuration</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
          {steps.map(step => (
            <div key={step.id} className="flex items-center gap-2">
              <span>{getStatusIcon(connectionStatus[step.id].status)}</span>
              <span className="text-gray-400">{step.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE: SYSTEM CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const SystemConfiguration = () => {
  const [config, setConfig] = useState({
    systemFrequency: 444,
    maxAgents: 287,
    xrQuality: 'high',
    voiceEngine: 'neural',
    backupFrequency: 'daily',
    logLevel: 'info',
    maintenanceMode: false
  });

  const updateConfig = (key, value) => {
    setConfig(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>⚙️</span> System Configuration
        </h2>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-500">
          💾 Sauvegarder
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Paramètres Système */}
        <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
          <h3 className="text-sm text-gray-400 mb-4">Paramètres Système</h3>

          <div className="space-y-4">
            <div>
              <label className="block text-xs text-gray-500 mb-2">Fréquence Système (Hz)</label>
              <input
                type="number"
                value={config.systemFrequency}
                onChange={(e) => updateConfig('systemFrequency', parseInt(e.target.value))}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white
                  focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Agents Maximum</label>
              <input
                type="number"
                value={config.maxAgents}
                onChange={(e) => updateConfig('maxAgents', parseInt(e.target.value))}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white
                  focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Qualité XR</label>
              <select
                value={config.xrQuality}
                onChange={(e) => updateConfig('xrQuality', e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white
                  focus:outline-none focus:border-blue-500"
              >
                <option value="low">Basse</option>
                <option value="medium">Moyenne</option>
                <option value="high">Haute</option>
                <option value="ultra">Ultra</option>
              </select>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Moteur Vocal</label>
              <select
                value={config.voiceEngine}
                onChange={(e) => updateConfig('voiceEngine', e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white
                  focus:outline-none focus:border-blue-500"
              >
                <option value="basic">Basique</option>
                <option value="neural">Neural</option>
                <option value="premium">Premium</option>
              </select>
            </div>
          </div>
        </div>

        {/* Paramètres Avancés */}
        <div className="bg-black/50 rounded-xl p-4 border border-gray-800">
          <h3 className="text-sm text-gray-400 mb-4">Paramètres Avancés</h3>

          <div className="space-y-4">
            <div>
              <label className="block text-xs text-gray-500 mb-2">Fréquence Backup</label>
              <select
                value={config.backupFrequency}
                onChange={(e) => updateConfig('backupFrequency', e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white
                  focus:outline-none focus:border-blue-500"
              >
                <option value="hourly">Toutes les heures</option>
                <option value="daily">Quotidien</option>
                <option value="weekly">Hebdomadaire</option>
              </select>
            </div>

            <div>
              <label className="block text-xs text-gray-500 mb-2">Niveau de Log</label>
              <select
                value={config.logLevel}
                onChange={(e) => updateConfig('logLevel', e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white
                  focus:outline-none focus:border-blue-500"
              >
                <option value="error">Erreurs seulement</option>
                <option value="warn">Avertissements</option>
                <option value="info">Info</option>
                <option value="debug">Debug</option>
              </select>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-900 rounded-lg">
              <div>
                <div className="text-sm text-white">Mode Maintenance</div>
                <div className="text-xs text-gray-500">Désactive l'accès utilisateur</div>
              </div>
              <button
                onClick={() => updateConfig('maintenanceMode', !config.maintenanceMode)}
                className={`w-12 h-6 rounded-full transition-colors ${
                  config.maintenanceMode ? 'bg-red-500' : 'bg-gray-700'
                }`}
              >
                <div className={`w-5 h-5 bg-white rounded-full transition-transform ${
                  config.maintenanceMode ? 'translate-x-6' : 'translate-x-0.5'
                }`} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Actions système */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button className="p-4 bg-gray-800 rounded-xl text-center hover:bg-gray-700 transition-colors">
          <span className="text-2xl block mb-2">🔄</span>
          <span className="text-sm text-gray-300">Redémarrer</span>
        </button>
        <button className="p-4 bg-gray-800 rounded-xl text-center hover:bg-gray-700 transition-colors">
          <span className="text-2xl block mb-2">💾</span>
          <span className="text-sm text-gray-300">Backup Now</span>
        </button>
        <button className="p-4 bg-gray-800 rounded-xl text-center hover:bg-gray-700 transition-colors">
          <span className="text-2xl block mb-2">🧹</span>
          <span className="text-sm text-gray-300">Clear Cache</span>
        </button>
        <button className="p-4 bg-gray-800 rounded-xl text-center hover:bg-gray-700 transition-colors">
          <span className="text-2xl block mb-2">📤</span>
          <span className="text-sm text-gray-300">Export Logs</span>
        </button>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: ADMIN COCKPIT
// ═══════════════════════════════════════════════════════════════════════════════

const COCKPIT_MODULES = [
  { id: 'setup', name: 'Setup Wizard', icon: '🔧', component: SetupWizard },
  { id: 'analytics', name: 'Analytics', icon: '📊', component: AnalyticsDashboard },
  { id: 'users', name: 'Utilisateurs', icon: '👥', component: UserManagement },
  { id: 'agents', name: 'Agents', icon: '🤖', component: AgentOrchestrator },
  { id: 'xr', name: 'XR Env', icon: '🌐', component: XREnvironmentControl },
  { id: 'voice', name: 'Voice/Avatar', icon: '🎤', component: VoiceAvatarManager },
  { id: 'prompts', name: 'Prompts', icon: '📝', component: PromptEngineeringLab },
  { id: 'security', name: 'Sécurité', icon: '🔐', component: SecurityCenter },
  { id: 'config', name: 'Config', icon: '⚙️', component: SystemConfiguration }
];

const AdminCockpit = () => {
  const [activeModule, setActiveModule] = useState('setup');
  const [isCollapsed, setIsCollapsed] = useState(false);

  const ActiveComponent = COCKPIT_MODULES.find(m => m.id === activeModule)?.component || AnalyticsDashboard;

  return (
    <div className="min-h-screen bg-gray-950 flex">
      {/* Sidebar */}
      <div className={`${isCollapsed ? 'w-16' : 'w-64'} bg-black border-r border-gray-800 transition-all duration-300`}>
        <div className="p-4 border-b border-gray-800">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🎛️</span>
            {!isCollapsed && (
              <div>
                <h1 className="text-sm font-bold text-white">Admin Cockpit</h1>
                <p className="text-xs text-gray-500">CHE·NU Control</p>
              </div>
            )}
          </div>
        </div>

        <nav className="p-2">
          {COCKPIT_MODULES.map(module => (
            <button
              key={module.id}
              onClick={() => setActiveModule(module.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg mb-1 transition-all ${
                activeModule === module.id
                  ? 'bg-yellow-500/20 text-yellow-500'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <span className="text-lg">{module.icon}</span>
              {!isCollapsed && <span className="text-sm">{module.name}</span>}
            </button>
          ))}
        </nav>

        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute bottom-4 left-4 p-2 rounded-lg bg-gray-800 text-gray-400 hover:text-white"
        >
          {isCollapsed ? '→' : '←'}
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6 overflow-auto">
        <ActiveComponent />
      </div>
    </div>
  );
};

export default AdminCockpit;
