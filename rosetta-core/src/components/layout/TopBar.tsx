/**
 * AT·OM — TopBar (Conscience)
 * Barre d'action fixe — Logo centré, profil à gauche, services à droite
 *
 * Layout :
 *   [Avatar + Nom + Modes]  |  [AT·OM centré + Freq Hz]  |  [Services + Compte]
 */

import React from 'react';
import { useATOM } from '../../context/GlobalStateContext';
import { SERVICE_SHORTCUTS } from '../../types/atom-types';

export function TopBar() {
  const { state, setMode } = useATOM();

  const modes = [
    { id: 'exploration' as const, label: 'Explorer', icon: '🔭' },
    { id: 'polissage' as const, label: 'Polissage', icon: '💎' },
    { id: 'creation' as const, label: 'Création', icon: '⚡' },
    { id: 'meditation' as const, label: 'Méditation', icon: '🕊️' },
    { id: 'genesis' as const, label: 'Genesis', icon: '✨' },
  ];

  const displayName = state.user_profile?.display_name ?? 'Anonyme';
  const initials = displayName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

  return (
    <header
      className="fixed top-0 left-0 right-0 z-50 h-12 flex items-center justify-between px-3"
      style={{
        background: 'rgba(5, 5, 5, 0.85)',
        backdropFilter: 'blur(20px)',
        borderBottom: `1px solid ${state.resonance_color}33`,
      }}
    >
      {/* GAUCHE : Avatar + Nom + Modes */}
      <div className="flex items-center gap-2 min-w-0">
        {/* Avatar */}
        <div
          className="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0"
          style={{
            background: `${state.resonance_color}22`,
            border: `1px solid ${state.resonance_color}44`,
            color: state.resonance_color,
          }}
        >
          {initials}
        </div>
        <span className="text-xs text-gray-400 truncate max-w-[100px] hidden sm:inline">
          {displayName}
        </span>

        {/* Séparateur */}
        <div
          className="w-px h-5 shrink-0"
          style={{ background: 'rgba(255,255,255,0.08)' }}
        />

        {/* Modes (compact, icône seule) */}
        <div className="flex gap-0.5">
          {modes.map((m) => (
            <button
              key={m.id}
              onClick={() => setMode(m.id)}
              className="w-7 h-7 rounded flex items-center justify-center text-xs transition-all duration-300"
              style={{
                background: state.mode === m.id ? `${state.resonance_color}22` : 'transparent',
                color: state.mode === m.id ? state.resonance_color : '#555',
                border: state.mode === m.id ? `1px solid ${state.resonance_color}44` : '1px solid transparent',
              }}
              title={m.label}
            >
              {m.icon}
            </button>
          ))}
        </div>
      </div>

      {/* CENTRE : Logo AT·OM + Fréquence (absolument centré) */}
      <div className="absolute left-1/2 -translate-x-1/2 flex items-center gap-3">
        <span
          className="text-sm font-bold tracking-widest"
          style={{ color: state.resonance_color }}
        >
          AT·OM
        </span>
        <div
          className="w-2 h-2 rounded-full animate-pulse"
          style={{ backgroundColor: state.resonance_color }}
        />
        <span
          className="text-sm font-mono font-bold"
          style={{ color: state.resonance_color }}
        >
          {state.system_frequency}Hz
        </span>
        <span className="text-xs text-gray-500 hidden md:inline">
          {state.resonance_label}
        </span>

        {/* Indicateur Point Zéro */}
        {state.vibrational.is_in_crater && (
          <div
            className="px-2 py-0.5 rounded text-[10px] font-bold animate-pulse"
            style={{
              background: 'rgba(255, 215, 0, 0.15)',
              color: '#FFD700',
              border: '1px solid rgba(255, 215, 0, 0.3)',
            }}
          >
            POINT ZÉRO
          </div>
        )}
      </div>

      {/* DROITE : Services + Compte */}
      <div className="flex items-center gap-1">
        {SERVICE_SHORTCUTS.map((s) => (
          <button
            key={s.id}
            className="w-7 h-7 rounded flex items-center justify-center text-xs text-gray-500 hover:text-gray-300 hover:bg-white/5 transition-all duration-200"
            title={s.label}
          >
            {s.icon}
          </button>
        ))}

        {/* Séparateur */}
        <div
          className="w-px h-5 shrink-0"
          style={{ background: 'rgba(255,255,255,0.08)' }}
        />

        <button className="text-[10px] text-gray-500 hover:text-gray-400 px-1.5 py-1 rounded hover:bg-white/5 transition-all">
          Mon Compte
        </button>
      </div>
    </header>
  );
}
