/**
 * AT·OM — BottomTaskbar (Exécution)
 * Barre inférieure tripartite
 *
 * Layout :
 *   [Projet Exécution App Rezo]  |  [AT·OM centré]  |  [💬 Chat 📧 Mail 📅 Meeting]
 *
 * Gauche  : Onglets système (navigation interne)
 * Centre  : Logo AT·OM cliquable (palette de commandes)
 * Droite  : Raccourcis communication (ouvrent des onglets dans ContentArea)
 */

import React from 'react';
import { useATOM } from '../../context/GlobalStateContext';
import { COMM_CHANNELS } from '../../types/atom-types';
import type { HubTab, CommChannelId } from '../../types/atom-types';

const SYSTEM_TABS: { id: HubTab; label: string; icon: string }[] = [
  { id: 'projet', label: 'Projet', icon: '📋' },
  { id: 'execution', label: 'Exécution', icon: '⚡' },
  { id: 'app', label: 'App', icon: '🔧' },
  { id: 'rezo', label: 'Rezo', icon: '🌐' },
];

const COMM_SHORTCUTS: { id: CommChannelId; label: string }[] = [
  { id: 'CHAT', label: 'Chat' },
  { id: 'COURRIEL', label: 'Mail' },
  { id: 'MEETING', label: 'Meeting' },
];

export function BottomTaskbar() {
  const { state, setTab, selectCommChannel } = useATOM();

  return (
    <footer
      className="fixed bottom-0 left-0 right-0 z-50 h-12 flex items-center px-2"
      style={{
        background: 'rgba(5, 5, 5, 0.9)',
        backdropFilter: 'blur(20px)',
        borderTop: `1px solid ${state.resonance_color}22`,
      }}
    >
      {/* GAUCHE : Onglets Système */}
      <div className="flex gap-1 shrink-0">
        {SYSTEM_TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setTab(tab.id)}
            className="px-3 py-1.5 text-xs rounded transition-all duration-300"
            style={{
              background: state.active_tab === tab.id ? `${state.resonance_color}15` : 'transparent',
              color: state.active_tab === tab.id ? state.resonance_color : '#555',
              border: state.active_tab === tab.id
                ? `1px solid ${state.resonance_color}33`
                : '1px solid transparent',
            }}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* CENTRE : Logo AT·OM */}
      <div className="flex-1 flex justify-center">
        <button
          className="flex items-center gap-2 px-3 py-1 rounded hover:bg-white/5 transition-all"
          title="Palette de commandes (Ctrl+K)"
        >
          <span
            className="text-xs font-bold tracking-widest"
            style={{ color: state.resonance_color }}
          >
            AT·OM
          </span>
          <div
            className="w-1.5 h-1.5 rounded-full"
            style={{
              backgroundColor: state.vibrational.is_in_crater ? '#FFD700' : state.resonance_color,
              boxShadow: state.vibrational.is_in_crater ? '0 0 8px #FFD700' : 'none',
            }}
          />
        </button>
      </div>

      {/* DROITE : Raccourcis Communication */}
      <div className="flex gap-1 shrink-0">
        {COMM_SHORTCUTS.map((cs) => {
          const channel = COMM_CHANNELS[cs.id];
          const isActive = state.active_comm_channel === cs.id;
          return (
            <button
              key={cs.id}
              onClick={() => selectCommChannel(isActive ? null : cs.id)}
              className="px-3 py-1.5 text-xs rounded transition-all duration-300"
              style={{
                background: isActive ? `${channel.color}15` : 'transparent',
                color: isActive ? channel.color : '#555',
                border: isActive
                  ? `1px solid ${channel.color}33`
                  : '1px solid transparent',
              }}
            >
              {channel.icon} {cs.label}
            </button>
          );
        })}
      </div>
    </footer>
  );
}
