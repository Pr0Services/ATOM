/**
 * AT·OM — CommHub (Communication)
 * Panneau droit — Miroir symétrique du SphereNavigator
 *
 * Même principe que le panneau gauche :
 *   - Colonne d'icônes cliquables
 *   - Cliquer ouvre un onglet dans le ContentArea central
 *   - Le flux circule de la même façon des deux côtés
 *
 * Canaux : Courriel, Téléphone, Agents IA, Chat, Meeting, Services
 * Quick  : Notifications (badge), Recherche (overlay), Paramètres (panneau)
 */

import React, { useState, useRef, useEffect } from 'react';
import { useATOM } from '../../context/GlobalStateContext';
import { COMM_CHANNELS, type CommChannelId } from '../../types/atom-types';

const CHANNEL_LIST = Object.values(COMM_CHANNELS);

// ─── Données Mock Notifications ──────────────────────────

const MOCK_NOTIFICATIONS = [
  { id: 'n1', text: 'Nouvelle proposition de gouvernance', time: 'Il y a 5m', color: '#FF7F00', read: false },
  { id: 'n2', text: 'FlowKeeper: Vélocité à 4.8 — Équilibre', time: 'Il y a 15m', color: '#50C878', read: false },
  { id: 'n3', text: 'Agent Sentinel: scan de sécurité terminé', time: 'Il y a 1h', color: '#4488FF', read: true },
  { id: 'n4', text: 'Sphère Technologie: 3 contributions', time: 'Il y a 2h', color: '#FF0000', read: true },
];

// ═══════════════════════════════════════════════════════════
// COMM HUB — Composant Principal
// ═══════════════════════════════════════════════════════════

export function CommHub() {
  const { state, selectCommChannel } = useATOM();
  const [activeOverlay, setActiveOverlay] = useState<'notifications' | 'search' | 'settings' | null>(null);

  const toggleOverlay = (overlay: 'notifications' | 'search' | 'settings') => {
    setActiveOverlay(activeOverlay === overlay ? null : overlay);
  };

  const unreadCount = MOCK_NOTIFICATIONS.filter(n => !n.read).length;

  return (
    <nav
      className="flex flex-col items-center gap-1.5 py-3 rounded-lg h-full overflow-y-auto relative"
      style={{
        background: 'rgba(5, 5, 5, 0.6)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(255, 255, 255, 0.06)',
      }}
    >
      <span className="text-[9px] text-gray-600 uppercase tracking-wider mb-1">
        Comm
      </span>

      {CHANNEL_LIST.map((channel) => {
        const isActive = state.active_comm_channel === channel.id;

        return (
          <button
            key={channel.id}
            onClick={() => selectCommChannel(isActive ? null : channel.id)}
            className="w-10 h-10 rounded-lg flex items-center justify-center text-base transition-all duration-300"
            style={{
              background: isActive ? `${channel.color}22` : 'rgba(255,255,255,0.04)',
              border: isActive ? `2px solid ${channel.color}66` : '2px solid transparent',
              color: isActive ? channel.color : '#555',
              boxShadow: isActive ? `0 0 12px ${channel.color}33` : 'none',
            }}
            title={`${channel.label} — ${channel.description}`}
          >
            {channel.icon}
          </button>
        );
      })}

      {/* Séparateur */}
      <div
        className="w-6 my-1"
        style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}
      />

      <span className="text-[9px] text-gray-600 uppercase tracking-wider mb-1">
        Quick
      </span>

      {/* Notifications — avec badge */}
      <div className="relative">
        <button
          onClick={() => toggleOverlay('notifications')}
          className="w-10 h-10 rounded-lg flex items-center justify-center text-base transition-all duration-300 hover:bg-white/5"
          style={{
            background: activeOverlay === 'notifications' ? 'rgba(255,255,255,0.08)' : 'rgba(255,255,255,0.04)',
            color: activeOverlay === 'notifications' ? '#D4AF37' : '#555',
          }}
          title="Notifications"
        >
          🔔
        </button>
        {unreadCount > 0 && (
          <div
            className="absolute -top-1 -right-1 w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-bold text-white"
            style={{ background: '#FF4444' }}
          >
            {unreadCount}
          </div>
        )}
      </div>

      {/* Recherche */}
      <button
        onClick={() => toggleOverlay('search')}
        className="w-10 h-10 rounded-lg flex items-center justify-center text-base transition-all duration-300 hover:bg-white/5"
        style={{
          background: activeOverlay === 'search' ? 'rgba(255,255,255,0.08)' : 'rgba(255,255,255,0.04)',
          color: activeOverlay === 'search' ? '#4488FF' : '#555',
        }}
        title="Recherche"
      >
        🔍
      </button>

      {/* Paramètres */}
      <button
        onClick={() => toggleOverlay('settings')}
        className="w-10 h-10 rounded-lg flex items-center justify-center text-base transition-all duration-300 hover:bg-white/5"
        style={{
          background: activeOverlay === 'settings' ? 'rgba(255,255,255,0.08)' : 'rgba(255,255,255,0.04)',
          color: activeOverlay === 'settings' ? '#9B59B6' : '#555',
        }}
        title="Paramètres"
      >
        ⚙️
      </button>

      {/* ─── Overlays (positionnés à gauche du hub) ─────── */}
      {activeOverlay && (
        <QuickOverlay type={activeOverlay} onClose={() => setActiveOverlay(null)} />
      )}
    </nav>
  );
}

// ═══════════════════════════════════════════════════════════
// OVERLAY — Panneau flottant pour Quick Actions
// ═══════════════════════════════════════════════════════════

function QuickOverlay({ type, onClose }: { type: 'notifications' | 'search' | 'settings'; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);

  // Fermer en cliquant dehors
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        // Petit délai pour éviter de fermer au clic sur le bouton
        setTimeout(onClose, 50);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [onClose]);

  return (
    <div
      ref={ref}
      className="absolute right-full mr-2 rounded-lg overflow-hidden z-50"
      style={{
        top: type === 'notifications' ? 180 : type === 'search' ? 220 : 260,
        width: 260,
        background: 'rgba(10, 10, 10, 0.95)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
      }}
    >
      {type === 'notifications' && <NotificationOverlay />}
      {type === 'search' && <SearchOverlay />}
      {type === 'settings' && <SettingsOverlay />}
    </div>
  );
}

// ─── Notifications Overlay ───────────────────────────────

function NotificationOverlay() {
  return (
    <div className="max-h-[300px] overflow-y-auto">
      <div className="px-3 py-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-xs font-medium text-white/60">Notifications</span>
      </div>
      {MOCK_NOTIFICATIONS.map((notif) => (
        <div
          key={notif.id}
          className="px-3 py-2.5 transition-all hover:bg-white/[0.03] cursor-pointer"
          style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}
        >
          <div className="flex items-start gap-2">
            {!notif.read && (
              <div className="w-1.5 h-1.5 rounded-full mt-1.5 shrink-0" style={{ background: notif.color }} />
            )}
            <div className="min-w-0">
              <p className={`text-[11px] leading-snug ${notif.read ? 'text-white/30' : 'text-white/60'}`}>
                {notif.text}
              </p>
              <span className="text-[9px] text-white/15">{notif.time}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// ─── Search Overlay ──────────────────────────────────────

function SearchOverlay() {
  const [query, setQuery] = useState('');

  return (
    <div>
      <div className="p-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Rechercher..."
          autoFocus
          className="w-full bg-white/5 rounded px-3 py-1.5 text-xs text-white/80 placeholder-white/20 outline-none"
          style={{ border: '1px solid rgba(255,255,255,0.08)' }}
        />
      </div>
      <div className="px-3 py-4 text-center">
        {query ? (
          <p className="text-[10px] text-white/25">
            Aucun résultat pour &laquo;{query}&raquo;
          </p>
        ) : (
          <p className="text-[10px] text-white/15">
            Tapez pour rechercher dans les sphères, canaux et données
          </p>
        )}
      </div>
    </div>
  );
}

// ─── Settings Overlay ────────────────────────────────────

function SettingsOverlay() {
  const [settings, setSettings] = useState({
    darkMode: true,
    notifications: true,
    sounds: false,
    animations: true,
    vibrationalFeedback: true,
  });

  const toggleSetting = (key: keyof typeof settings) => {
    setSettings({ ...settings, [key]: !settings[key] });
  };

  const items = [
    { key: 'darkMode' as const, label: 'Mode sombre', locked: true },
    { key: 'notifications' as const, label: 'Notifications', locked: false },
    { key: 'sounds' as const, label: 'Sons', locked: false },
    { key: 'animations' as const, label: 'Animations', locked: false },
    { key: 'vibrationalFeedback' as const, label: 'Feedback vibratoire', locked: false },
  ];

  return (
    <div>
      <div className="px-3 py-2" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <span className="text-xs font-medium text-white/60">Paramètres</span>
      </div>
      <div className="py-1">
        {items.map((item) => (
          <button
            key={item.key}
            onClick={() => !item.locked && toggleSetting(item.key)}
            className="w-full flex items-center justify-between px-3 py-2 text-xs transition-all hover:bg-white/[0.03]"
            style={{ opacity: item.locked ? 0.5 : 1 }}
          >
            <span className="text-white/50">{item.label}</span>
            <div
              className="w-8 h-4 rounded-full transition-all relative"
              style={{
                background: settings[item.key] ? 'rgba(80, 200, 120, 0.4)' : 'rgba(255,255,255,0.1)',
              }}
            >
              <div
                className="absolute top-0.5 w-3 h-3 rounded-full transition-all"
                style={{
                  left: settings[item.key] ? 16 : 2,
                  background: settings[item.key] ? '#50C878' : '#555',
                }}
              />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
