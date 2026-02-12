/**
 * AT·OM — ContentArea (Panneau Central avec Onglets)
 * Remplace l'appel direct à DataExplorer dans MainEngine
 *
 * Architecture :
 *   ┌─────────────────────────────────────────────┐
 *   │ [Tab1 ×] [Tab2 ×] [Tab3 ×]    (TabBar)     │
 *   ├─────────────────────────────────────────────┤
 *   │                                             │
 *   │   Contenu basé sur l'onglet actif :         │
 *   │   - Sphère  → DataExplorer                  │
 *   │   - Comm    → CommContent (6 canaux)        │
 *   │   - Système → SystemContent (4 dashboards)  │
 *   │   - Aucun   → EmptyState                    │
 *   │                                             │
 *   └─────────────────────────────────────────────┘
 */

import React, { useState } from 'react';
import { useATOM } from '../../context/GlobalStateContext';
import { DataExplorer } from './DataExplorer';
import { COMM_CHANNELS } from '../../types/atom-types';
import type { ContentTab, CommChannelId, HubTab } from '../../types/atom-types';

// ─── ContentArea Principal ──────────────────────────────

export function ContentArea() {
  const { state, activateTab, closeTab } = useATOM();
  const { tabs, active_tab_id } = state;
  const activeTab = tabs.find(t => t.id === active_tab_id) ?? null;

  return (
    <div className="flex flex-col h-full">
      {/* Barre d'onglets */}
      {tabs.length > 0 && (
        <TabBar
          tabs={tabs}
          activeTabId={active_tab_id}
          onActivate={activateTab}
          onClose={closeTab}
        />
      )}

      {/* Contenu */}
      <div className="flex-1 overflow-hidden">
        {activeTab ? (
          <TabContent tab={activeTab} />
        ) : (
          <EmptyState />
        )}
      </div>
    </div>
  );
}

// ─── Barre d'Onglets ────────────────────────────────────

function TabBar({ tabs, activeTabId, onActivate, onClose }: {
  tabs: ContentTab[];
  activeTabId: string | null;
  onActivate: (id: string) => void;
  onClose: (id: string) => void;
}) {
  return (
    <div
      className="flex items-center gap-0.5 px-2 py-1 overflow-x-auto shrink-0"
      style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.06)' }}
    >
      {tabs.map((tab) => {
        const isActive = tab.id === activeTabId;
        return (
          <div
            key={tab.id}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-t text-xs cursor-pointer group transition-all duration-200"
            style={{
              background: isActive ? `${tab.color}15` : 'transparent',
              color: isActive ? tab.color : '#666',
              borderBottom: isActive ? `2px solid ${tab.color}` : '2px solid transparent',
            }}
            onClick={() => onActivate(tab.id)}
          >
            <span>{tab.icon}</span>
            <span className="truncate max-w-[100px]">{tab.label}</span>
            {!tab.is_pinned && (
              <button
                className="opacity-0 group-hover:opacity-100 ml-1 text-gray-600 hover:text-gray-400 text-[10px]"
                onClick={(e) => { e.stopPropagation(); onClose(tab.id); }}
              >
                ✕
              </button>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ─── Routage du Contenu par Onglet ──────────────────────

function TabContent({ tab }: { tab: ContentTab }) {
  switch (tab.source) {
    case 'sphere':
      return <DataExplorer />;
    case 'comm':
      return <CommContent channelId={tab.source_id as CommChannelId} />;
    case 'system':
      return <SystemContent tabId={tab.source_id as HubTab} />;
    default:
      return <EmptyState />;
  }
}

// ═══════════════════════════════════════════════════════════
// COMM CONTENT — 6 Canaux de Communication
// ═══════════════════════════════════════════════════════════

interface MockMessage {
  id: string;
  sender: string;
  avatar: string;
  text: string;
  time: string;
  isOwn?: boolean;
}

interface MockEmail {
  id: string;
  from: string;
  subject: string;
  preview: string;
  date: string;
  read: boolean;
}

interface MockCall {
  id: string;
  name: string;
  number: string;
  duration: string;
  type: 'entrant' | 'sortant' | 'manque';
  date: string;
}

interface MockAgent {
  id: string;
  name: string;
  role: string;
  status: 'actif' | 'veille' | 'erreur';
  progress: number;
}

interface MockMeeting {
  id: string;
  title: string;
  time: string;
  date: string;
  participants: string[];
  status: 'en_cours' | 'a_venir' | 'termine';
}

interface MockService {
  id: string;
  name: string;
  icon: string;
  status: 'actif' | 'inactif' | 'maintenance';
  description: string;
}

// ─── Données Mock ─────────────────────────────────────────

const MOCK_MESSAGES: MockMessage[] = [
  { id: 'm1', sender: 'Aria', avatar: '🤖', text: 'Bienvenue dans le hub de communication AT·OM.', time: '09:00', },
  { id: 'm2', sender: 'System', avatar: '⚡', text: 'Connexion au réseau souverain établie. Fréquence: 444Hz.', time: '09:01', },
  { id: 'm3', sender: 'Gabriel', avatar: '👤', text: 'La sphère Technologie a reçu 3 nouvelles contributions.', time: '09:15', },
  { id: 'm4', sender: 'Moi', avatar: '🔵', text: 'Merci, je vais vérifier les alignements.', time: '09:16', isOwn: true },
  { id: 'm5', sender: 'Aria', avatar: '🤖', text: 'Le PolishingEngine a terminé la validation — 5/7 étapes passées.', time: '09:20', },
];

const MOCK_EMAILS: MockEmail[] = [
  { id: 'e1', from: 'conseil@atom.org', subject: 'Nouvelle proposition de gouvernance', preview: 'Le Conseil des 144 propose une modification...', date: '10:30', read: false },
  { id: 'e2', from: 'flowkeeper@atom.org', subject: 'Rapport FlowKeeper — Équilibre', preview: 'Vélocité 30j: 4.8 — Status: EQUILIBRE', date: '09:00', read: true },
  { id: 'e3', from: 'genie@atom.org', subject: 'Nouveau parcours disponible', preview: 'Le parcours Souveraineté Numérique est maintenant...', date: 'Hier', read: true },
  { id: 'e4', from: 'securite@atom.org', subject: 'Audit de sécurité mensuel', preview: 'Résultats: 98.5% de conformité...', date: 'Hier', read: false },
  { id: 'e5', from: 'essaim@atom.org', subject: 'Rapport des agents — Semaine 12', preview: '312/350 agents actifs. Taux de complétion: 94%', date: '2j', read: true },
];

const MOCK_CALLS: MockCall[] = [
  { id: 'c1', name: 'Gabriel Martin', number: '+1-555-0101', duration: '12:34', type: 'entrant', date: '10:45' },
  { id: 'c2', name: 'Aria (IA)', number: 'agent://aria', duration: '03:21', type: 'sortant', date: '09:30' },
  { id: 'c3', name: 'Conseil-144', number: 'room://conseil', duration: '45:00', type: 'entrant', date: 'Hier' },
  { id: 'c4', name: 'Support Technique', number: '+1-555-0999', duration: '--', type: 'manque', date: 'Hier' },
];

const MOCK_AGENTS: MockAgent[] = [
  { id: 'a1', name: 'Aria', role: 'Assistant Principal', status: 'actif', progress: 100 },
  { id: 'a2', name: 'Scribe', role: 'Documentation', status: 'actif', progress: 78 },
  { id: 'a3', name: 'Sentinel', role: 'Sécurité', status: 'actif', progress: 95 },
  { id: 'a4', name: 'Alchemist', role: 'Polissage Données', status: 'veille', progress: 42 },
  { id: 'a5', name: 'Oracle', role: 'Prédictions', status: 'veille', progress: 0 },
  { id: 'a6', name: 'Phoenix', role: 'Récupération', status: 'erreur', progress: 33 },
];

const MOCK_MEETINGS: MockMeeting[] = [
  { id: 'mt1', title: 'Stand-up AT·OM', time: '09:00', date: "Aujourd'hui", participants: ['Gabriel', 'Aria', 'Scribe'], status: 'termine' },
  { id: 'mt2', title: 'Conseil Gouvernance', time: '14:00', date: "Aujourd'hui", participants: ['Conseil-144'], status: 'a_venir' },
  { id: 'mt3', title: 'Review Sphère Technologie', time: '16:00', date: "Aujourd'hui", participants: ['Gabriel', 'Sentinel'], status: 'a_venir' },
  { id: 'mt4', title: 'Alchimie Sprint Planning', time: '10:00', date: 'Demain', participants: ['Alchemist', 'Scribe', 'Oracle'], status: 'a_venir' },
];

const MOCK_SERVICES: MockService[] = [
  { id: 's1', name: 'Forum', icon: '💬', status: 'actif', description: 'Forum communautaire souverain' },
  { id: 's2', name: 'Marketplace', icon: '🛒', status: 'actif', description: 'Marché en Unités de Résonance' },
  { id: 's3', name: 'Stream', icon: '📺', status: 'actif', description: 'Diffusion en direct' },
  { id: 's4', name: 'Wiki', icon: '📖', status: 'actif', description: 'Base de connaissances' },
  { id: 's5', name: 'Code', icon: '💻', status: 'actif', description: 'Forge de code souveraine' },
  { id: 's6', name: 'Analytics', icon: '📊', status: 'maintenance', description: 'Tableaux de bord analytiques' },
  { id: 's7', name: 'Backup', icon: '💾', status: 'actif', description: 'Sauvegarde décentralisée' },
  { id: 's8', name: 'Bridge', icon: '🌉', status: 'inactif', description: 'Pont Hedera Hashgraph' },
];

// ─── CommContent — Routeur par canal ─────────────────────

function CommContent({ channelId }: { channelId: CommChannelId }) {
  switch (channelId) {
    case 'CHAT':
      return <ChatPanel />;
    case 'COURRIEL':
      return <EmailPanel />;
    case 'TELEPHONE':
      return <PhonePanel />;
    case 'AGENTS':
      return <AgentPanel />;
    case 'MEETING':
      return <MeetingPanel />;
    case 'SERVICES':
      return <ServicePanel />;
    default:
      return <ChannelPlaceholder channelId={channelId} />;
  }
}

// ─── CHAT Panel ──────────────────────────────────────────

function ChatPanel() {
  const [messages, setMessages] = useState<MockMessage[]>(MOCK_MESSAGES);
  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (!input.trim()) return;
    const msg: MockMessage = {
      id: `m_${Date.now()}`,
      sender: 'Moi',
      avatar: '🔵',
      text: input.trim(),
      time: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }),
      isOwn: true,
    };
    setMessages([...messages, msg]);
    setInput('');
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-4 py-2 shrink-0" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <div className="flex items-center gap-2">
          <span className="text-sm">💬</span>
          <span className="text-xs font-medium text-white/70">Chat AT·OM</span>
          <span className="text-[10px] text-white/20 ml-auto">{messages.length} messages</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-2 ${msg.isOwn ? 'flex-row-reverse' : ''}`}
          >
            <div className="text-lg shrink-0">{msg.avatar}</div>
            <div
              className="max-w-[70%] px-3 py-2 rounded-lg"
              style={{
                background: msg.isOwn ? 'rgba(0, 71, 171, 0.15)' : 'rgba(255,255,255,0.04)',
                border: msg.isOwn ? '1px solid rgba(0, 71, 171, 0.25)' : '1px solid rgba(255,255,255,0.06)',
              }}
            >
              {!msg.isOwn && (
                <div className="text-[10px] text-white/40 mb-0.5">{msg.sender}</div>
              )}
              <p className="text-xs text-white/70">{msg.text}</p>
              <div className="text-[9px] text-white/20 mt-1 text-right">{msg.time}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="p-3 shrink-0" style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Écrire un message..."
            className="flex-1 bg-white/5 rounded-lg px-3 py-2 text-xs text-white/80 placeholder-white/20 outline-none focus:bg-white/8 transition-colors"
            style={{ border: '1px solid rgba(255,255,255,0.08)' }}
          />
          <button
            onClick={sendMessage}
            className="px-3 py-2 rounded-lg text-xs font-medium transition-all"
            style={{
              background: input.trim() ? 'rgba(0, 71, 171, 0.3)' : 'rgba(255,255,255,0.05)',
              color: input.trim() ? '#4488FF' : '#555',
              border: '1px solid rgba(0, 71, 171, 0.2)',
            }}
          >
            Envoyer
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── EMAIL Panel ──────────────────────────────────────────

function EmailPanel() {
  const [selectedEmail, setSelectedEmail] = useState<MockEmail | null>(null);

  if (selectedEmail) {
    return (
      <div className="flex flex-col h-full">
        <div className="px-4 py-2 shrink-0 flex items-center gap-3" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
          <button
            onClick={() => setSelectedEmail(null)}
            className="text-xs text-white/30 hover:text-white/60 transition-colors"
          >
            ← Retour
          </button>
          <span className="text-xs font-medium text-white/60">{selectedEmail.subject}</span>
        </div>
        <div className="flex-1 p-4 overflow-y-auto">
          <div className="text-xs text-white/30 mb-2">De: {selectedEmail.from}</div>
          <div className="text-xs text-white/20 mb-4">{selectedEmail.date}</div>
          <h2 className="text-sm font-medium text-white/80 mb-4">{selectedEmail.subject}</h2>
          <p className="text-xs text-white/50 leading-relaxed">{selectedEmail.preview}</p>
          <p className="text-xs text-white/40 leading-relaxed mt-3">
            Ce message fait partie du réseau de communication souverain AT·OM.
            Toutes les communications sont chiffrées et vérifiées.
          </p>
          <div className="flex gap-2 mt-6">
            {['Répondre', 'Transférer', 'Archiver'].map((action) => (
              <button
                key={action}
                className="px-3 py-1.5 rounded text-[10px] text-white/40 transition-all hover:text-white/60"
                style={{ border: '1px solid rgba(255,255,255,0.08)' }}
              >
                {action}
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">📧</span>
        <span className="text-xs font-medium text-white/70">Courriel Souverain</span>
        <span className="text-[10px] text-white/20 ml-auto">
          {MOCK_EMAILS.filter(e => !e.read).length} non lus
        </span>
      </div>
      <div className="flex-1 overflow-y-auto">
        {MOCK_EMAILS.map((email) => (
          <button
            key={email.id}
            onClick={() => setSelectedEmail(email)}
            className="w-full text-left px-4 py-3 transition-all hover:bg-white/[0.03]"
            style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}
          >
            <div className="flex items-center gap-2">
              {!email.read && <div className="w-1.5 h-1.5 rounded-full bg-blue-400 shrink-0" />}
              <span className={`text-xs ${email.read ? 'text-white/40' : 'text-white/70 font-medium'} truncate`}>
                {email.subject}
              </span>
              <span className="text-[10px] text-white/20 ml-auto shrink-0">{email.date}</span>
            </div>
            <div className="text-[10px] text-white/20 mt-0.5 ml-3.5">{email.from}</div>
            <div className="text-[10px] text-white/15 mt-0.5 ml-3.5 truncate">{email.preview}</div>
          </button>
        ))}
      </div>
    </div>
  );
}

// ─── PHONE Panel ──────────────────────────────────────────

function PhonePanel() {
  const typeIcons = { entrant: '📥', sortant: '📤', manque: '📵' };
  const typeColors = { entrant: '#50C878', sortant: '#4488FF', manque: '#FF4444' };

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">📞</span>
        <span className="text-xs font-medium text-white/70">Journal d'Appels</span>
      </div>
      <div className="flex-1 overflow-y-auto">
        {MOCK_CALLS.map((call) => (
          <div
            key={call.id}
            className="px-4 py-3 flex items-center gap-3"
            style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}
          >
            <span className="text-sm">{typeIcons[call.type]}</span>
            <div className="flex-1 min-w-0">
              <div className="text-xs text-white/70">{call.name}</div>
              <div className="text-[10px] text-white/25">{call.number}</div>
            </div>
            <div className="text-right shrink-0">
              <div className="text-[10px]" style={{ color: typeColors[call.type] }}>
                {call.duration}
              </div>
              <div className="text-[9px] text-white/20">{call.date}</div>
            </div>
          </div>
        ))}
      </div>
      {/* Bouton appeler */}
      <div className="p-3 shrink-0" style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
        <button className="w-full py-2.5 rounded-lg text-xs font-medium transition-all" style={{ background: 'rgba(80, 200, 120, 0.15)', border: '1px solid rgba(80, 200, 120, 0.3)', color: '#50C878' }}>
          📞 Appeler
        </button>
      </div>
    </div>
  );
}

// ─── AGENTS Panel ─────────────────────────────────────────

function AgentPanel() {
  const statusConfig = {
    actif: { color: '#50C878', label: 'Actif', dot: 'bg-green-500' },
    veille: { color: '#FFA500', label: 'Veille', dot: 'bg-yellow-500' },
    erreur: { color: '#FF4444', label: 'Erreur', dot: 'bg-red-500' },
  };

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">🤖</span>
        <span className="text-xs font-medium text-white/70">Agents AT·OM</span>
        <span className="text-[10px] text-white/20 ml-auto">
          {MOCK_AGENTS.filter(a => a.status === 'actif').length}/{MOCK_AGENTS.length} actifs
        </span>
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {MOCK_AGENTS.map((agent) => {
          const cfg = statusConfig[agent.status];
          return (
            <div
              key={agent.id}
              className="p-3 rounded-lg"
              style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}
            >
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-2 h-2 rounded-full ${cfg.dot}`} />
                <span className="text-xs font-medium text-white/70">{agent.name}</span>
                <span className="text-[10px] text-white/25">{agent.role}</span>
                <span className="text-[10px] ml-auto" style={{ color: cfg.color }}>{cfg.label}</span>
              </div>
              <div className="h-1 rounded-full bg-white/5 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{ width: `${agent.progress}%`, background: cfg.color, opacity: 0.6 }}
                />
              </div>
              <div className="flex gap-2 mt-2">
                {['Démarrer', 'Pause', 'Arrêter'].map((action) => (
                  <button key={action} className="text-[9px] text-white/20 hover:text-white/40 transition-colors">
                    {action}
                  </button>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── MEETING Panel ────────────────────────────────────────

function MeetingPanel() {
  const statusConfig = {
    en_cours: { color: '#50C878', label: 'En cours', dot: 'animate-pulse' },
    a_venir: { color: '#4488FF', label: 'À venir', dot: '' },
    termine: { color: '#666', label: 'Terminé', dot: '' },
  };

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">📅</span>
        <span className="text-xs font-medium text-white/70">Réunions</span>
        <span className="text-[10px] text-white/20 ml-auto">
          {MOCK_MEETINGS.filter(m => m.status === 'a_venir').length} à venir
        </span>
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {MOCK_MEETINGS.map((meeting) => {
          const cfg = statusConfig[meeting.status];
          return (
            <div
              key={meeting.id}
              className="p-3 rounded-lg"
              style={{
                background: 'rgba(255,255,255,0.02)',
                border: `1px solid ${meeting.status === 'a_venir' ? 'rgba(68, 136, 255, 0.15)' : 'rgba(255,255,255,0.05)'}`,
              }}
            >
              <div className="flex items-center gap-2 mb-1">
                <div className={`w-2 h-2 rounded-full ${cfg.dot}`} style={{ background: cfg.color }} />
                <span className="text-xs font-medium text-white/70">{meeting.title}</span>
              </div>
              <div className="flex items-center gap-3 text-[10px] text-white/30">
                <span>{meeting.time}</span>
                <span>{meeting.date}</span>
                <span className="ml-auto" style={{ color: cfg.color }}>{cfg.label}</span>
              </div>
              <div className="flex gap-1 mt-2">
                {meeting.participants.map((p) => (
                  <span key={p} className="px-1.5 py-0.5 rounded text-[9px] text-white/30" style={{ background: 'rgba(255,255,255,0.04)' }}>
                    {p}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── SERVICES Panel ───────────────────────────────────────

function ServicePanel() {
  const statusConfig = {
    actif: { color: '#50C878', label: 'Actif' },
    inactif: { color: '#666', label: 'Inactif' },
    maintenance: { color: '#FFA500', label: 'Maintenance' },
  };

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">🔧</span>
        <span className="text-xs font-medium text-white/70">Services AT·OM</span>
        <span className="text-[10px] text-white/20 ml-auto">
          {MOCK_SERVICES.filter(s => s.status === 'actif').length}/{MOCK_SERVICES.length} actifs
        </span>
      </div>
      <div className="flex-1 overflow-y-auto p-3">
        <div className="grid grid-cols-2 gap-2">
          {MOCK_SERVICES.map((service) => {
            const cfg = statusConfig[service.status];
            return (
              <div
                key={service.id}
                className="p-3 rounded-lg transition-all hover:bg-white/[0.04] cursor-pointer"
                style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{service.icon}</span>
                  <span className="text-xs font-medium text-white/70">{service.name}</span>
                </div>
                <p className="text-[10px] text-white/25 mb-2">{service.description}</p>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    <div className="w-1.5 h-1.5 rounded-full" style={{ background: cfg.color }} />
                    <span className="text-[9px]" style={{ color: cfg.color }}>{cfg.label}</span>
                  </div>
                  {service.status === 'actif' && (
                    <button className="text-[9px] text-white/20 hover:text-white/40 transition-colors">
                      Ouvrir
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ─── Placeholder générique ────────────────────────────────

function ChannelPlaceholder({ channelId }: { channelId: CommChannelId }) {
  const channel = COMM_CHANNELS[channelId];
  return (
    <div className="flex items-center justify-center h-full">
      <div className="text-center space-y-3">
        <div
          className="w-16 h-16 rounded-full flex items-center justify-center text-2xl mx-auto"
          style={{ background: `${channel.color}15`, border: `2px solid ${channel.color}44` }}
        >
          {channel.icon}
        </div>
        <h3 className="text-sm font-medium" style={{ color: channel.color }}>{channel.label}</h3>
        <p className="text-xs text-gray-600">{channel.description}</p>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// SYSTEM CONTENT — 4 Dashboards
// ═══════════════════════════════════════════════════════════

function SystemContent({ tabId }: { tabId: HubTab }) {
  switch (tabId) {
    case 'projet':
      return <ProjetDashboard />;
    case 'execution':
      return <ExecutionDashboard />;
    case 'app':
      return <AppDashboard />;
    case 'rezo':
      return <RezoDashboard />;
    default:
      return (
        <div className="flex items-center justify-center h-full">
          <p className="text-xs text-gray-600">Dashboard: {tabId}</p>
        </div>
      );
  }
}

// ─── Projet Dashboard ─────────────────────────────────────

function ProjetDashboard() {
  const milestones = [
    { label: 'Rosetta Core', progress: 85, color: '#50C878' },
    { label: 'Interface App', progress: 35, color: '#4488FF' },
    { label: 'Hedera Bridge', progress: 10, color: '#D4AF37' },
    { label: 'Agent Framework', progress: 5, color: '#9B59B6' },
  ];

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">📋</span>
        <span className="text-xs font-medium text-white/70">AT·OM v0.1.0 — Projet</span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Stats rapides */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Fichiers', value: '85+', color: '#4488FF' },
            { label: 'Lignes TS', value: '12,770', color: '#50C878' },
            { label: 'Lignes SQL', value: '2,945', color: '#D4AF37' },
          ].map((s) => (
            <div key={s.label} className="p-3 rounded-lg text-center" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div className="text-lg font-bold" style={{ color: s.color }}>{s.value}</div>
              <div className="text-[10px] text-white/30">{s.label}</div>
            </div>
          ))}
        </div>

        {/* Milestones */}
        <div className="space-y-3">
          <h3 className="text-[10px] text-white/30 uppercase tracking-wider">Milestones</h3>
          {milestones.map((m) => (
            <div key={m.label}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-white/50">{m.label}</span>
                <span style={{ color: m.color }}>{m.progress}%</span>
              </div>
              <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                <div className="h-full rounded-full transition-all" style={{ width: `${m.progress}%`, background: m.color, opacity: 0.7 }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Execution Dashboard ──────────────────────────────────

function ExecutionDashboard() {
  const metrics = [
    { label: 'CPU', value: '12%', bar: 12, color: '#50C878' },
    { label: 'Mémoire', value: '340MB', bar: 42, color: '#4488FF' },
    { label: 'Latence', value: '23ms', bar: 8, color: '#D4AF37' },
    { label: 'Uptime', value: '99.9%', bar: 99, color: '#50C878' },
  ];

  const processes = [
    { name: 'RosettaParser', status: 'actif', cpu: '3%', mem: '45MB' },
    { name: 'VibrationalMotor', status: 'actif', cpu: '1%', mem: '12MB' },
    { name: 'PolishingEngine', status: 'idle', cpu: '0%', mem: '8MB' },
    { name: 'FlowKeeperEngine', status: 'actif', cpu: '2%', mem: '22MB' },
    { name: 'HeartbeatService', status: 'actif', cpu: '0.5%', mem: '4MB' },
  ];

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">⚡</span>
        <span className="text-xs font-medium text-white/70">Exécution</span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Métriques */}
        <div className="grid grid-cols-2 gap-3">
          {metrics.map((m) => (
            <div key={m.label} className="p-3 rounded-lg" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div className="text-[10px] text-white/30 mb-1">{m.label}</div>
              <div className="text-sm font-bold" style={{ color: m.color }}>{m.value}</div>
              <div className="h-1 rounded-full bg-white/5 mt-2 overflow-hidden">
                <div className="h-full rounded-full" style={{ width: `${m.bar}%`, background: m.color, opacity: 0.5 }} />
              </div>
            </div>
          ))}
        </div>

        {/* Processus */}
        <div>
          <h3 className="text-[10px] text-white/30 uppercase tracking-wider mb-2">Processus Actifs</h3>
          <div className="space-y-1">
            {processes.map((p) => (
              <div key={p.name} className="flex items-center gap-3 px-3 py-1.5 rounded text-xs" style={{ background: 'rgba(255,255,255,0.02)' }}>
                <div className={`w-1.5 h-1.5 rounded-full ${p.status === 'actif' ? 'bg-green-500' : 'bg-gray-600'}`} />
                <span className="text-white/50 flex-1">{p.name}</span>
                <span className="text-white/25 w-10 text-right">{p.cpu}</span>
                <span className="text-white/25 w-14 text-right">{p.mem}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── App Dashboard ────────────────────────────────────────

function AppDashboard() {
  const healthChecks = [
    { name: 'Rosetta Core', status: true },
    { name: 'State Context', status: true },
    { name: 'Tab System', status: true },
    { name: 'Hedera Bridge', status: false },
    { name: 'WebSocket', status: false },
  ];

  const logs = [
    '[09:20] PolishingEngine — Validation batch complete (42 nodes)',
    '[09:15] RosettaParser — SphereEventTemplate triggered for TECHNO',
    '[09:01] VibrationalMotor — Frequency anchored at 444Hz',
    '[09:00] ATOMProvider — Initialization complete',
    '[08:59] System — Boot sequence started',
  ];

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">📱</span>
        <span className="text-xs font-medium text-white/70">Application</span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Info */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Version', value: 'v0.1.0' },
            { label: 'Build', value: 'dev' },
            { label: 'Canon', value: 'AT·OM' },
          ].map((i) => (
            <div key={i.label} className="p-3 rounded-lg text-center" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div className="text-xs font-medium text-white/60">{i.value}</div>
              <div className="text-[9px] text-white/20">{i.label}</div>
            </div>
          ))}
        </div>

        {/* Health */}
        <div>
          <h3 className="text-[10px] text-white/30 uppercase tracking-wider mb-2">Health Checks</h3>
          <div className="space-y-1">
            {healthChecks.map((h) => (
              <div key={h.name} className="flex items-center gap-2 px-3 py-1.5 rounded text-xs" style={{ background: 'rgba(255,255,255,0.02)' }}>
                <div className={`w-2 h-2 rounded-full ${h.status ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-white/50">{h.name}</span>
                <span className={`ml-auto text-[10px] ${h.status ? 'text-green-500' : 'text-red-400'}`}>
                  {h.status ? 'OK' : 'Down'}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Logs */}
        <div>
          <h3 className="text-[10px] text-white/30 uppercase tracking-wider mb-2">Derniers Logs</h3>
          <div className="space-y-0.5 font-mono">
            {logs.map((log, i) => (
              <p key={i} className="text-[10px] text-white/25 truncate">{log}</p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Rezo Dashboard ───────────────────────────────────────

function RezoDashboard() {
  const connections = [
    { peer: 'Node-Alpha', latency: '12ms', status: 'connecte' },
    { peer: 'Node-Beta', latency: '34ms', status: 'connecte' },
    { peer: 'Node-Gamma', latency: '156ms', status: 'instable' },
    { peer: 'Hedera-Mainnet', latency: '--', status: 'deconnecte' },
    { peer: 'IPFS-Gateway', latency: '89ms', status: 'connecte' },
  ];

  const statusColors = { connecte: '#50C878', instable: '#FFA500', deconnecte: '#FF4444' };
  const statusLabels = { connecte: 'Connecté', instable: 'Instable', deconnecte: 'Déconnecté' };

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-2 shrink-0 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-sm">🌐</span>
        <span className="text-xs font-medium text-white/70">Réseau</span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Stats réseau */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Status', value: 'En ligne', color: '#50C878' },
            { label: 'Latence Moy.', value: '45ms', color: '#4488FF' },
            { label: 'Peers', value: '3/5', color: '#D4AF37' },
          ].map((s) => (
            <div key={s.label} className="p-3 rounded-lg text-center" style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div className="text-xs font-bold" style={{ color: s.color }}>{s.value}</div>
              <div className="text-[9px] text-white/20">{s.label}</div>
            </div>
          ))}
        </div>

        {/* Connexions */}
        <div>
          <h3 className="text-[10px] text-white/30 uppercase tracking-wider mb-2">Connexions</h3>
          <div className="space-y-1">
            {connections.map((c) => (
              <div key={c.peer} className="flex items-center gap-3 px-3 py-2 rounded text-xs" style={{ background: 'rgba(255,255,255,0.02)' }}>
                <div className="w-2 h-2 rounded-full" style={{ background: statusColors[c.status as keyof typeof statusColors] }} />
                <span className="text-white/50 flex-1">{c.peer}</span>
                <span className="text-white/25 w-14 text-right">{c.latency}</span>
                <span className="text-[10px] w-20 text-right" style={{ color: statusColors[c.status as keyof typeof statusColors] }}>
                  {statusLabels[c.status as keyof typeof statusLabels]}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── État Vide ──────────────────────────────────────────

function EmptyState() {
  return (
    <div className="flex items-center justify-center h-full">
      <div className="text-center space-y-3">
        <div className="text-4xl opacity-20">✦</div>
        <h3 className="text-sm text-gray-500">
          Sélectionne une sphère ou un canal
        </h3>
        <p className="text-xs text-gray-600">
          Panneau gauche : sphères  |  Panneau droit : communication
        </p>
      </div>
    </div>
  );
}
