/**
 * AT·OM — SphereNavigator (Mode Icônes)
 * Panneau gauche — Colonne étroite de 9+1 icônes
 *
 * Chaque icône représente une sphère.
 * Cliquer ouvre un onglet dans le ContentArea central.
 * Le même principe s'applique au CommHub (panneau droit).
 *
 * Icônes : 9 Sphères + AT·OM Mapping (historique)
 */

import React from 'react';
import { useATOM } from '../../context/GlobalStateContext';
import { SPHERES, RESONANCE_MATRIX, type SphereId } from '../../types/atom-types';

const SPHERE_LIST = Object.values(SPHERES);

export function SphereNavigator() {
  const { state, selectSphere } = useATOM();

  return (
    <nav
      className="flex flex-col items-center gap-1.5 py-3 rounded-lg h-full overflow-y-auto"
      style={{
        background: 'rgba(5, 5, 5, 0.6)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(255, 255, 255, 0.06)',
      }}
    >
      <span className="text-[9px] text-gray-600 uppercase tracking-wider mb-1">
        Nav
      </span>

      {SPHERE_LIST.map((sphere) => {
        const isActive = state.active_sphere === sphere.id;
        const resonance = RESONANCE_MATRIX[sphere.index as keyof typeof RESONANCE_MATRIX];
        const isGearActive = state.antikythera.active_gears.has(sphere.id);

        return (
          <button
            key={sphere.id}
            onClick={() => selectSphere(isActive ? null : sphere.id)}
            className="w-10 h-10 rounded-lg flex items-center justify-center text-base transition-all duration-300"
            style={{
              background: isActive ? `${resonance.color}22` : 'rgba(255,255,255,0.04)',
              border: isActive ? `2px solid ${resonance.color}66` : '2px solid transparent',
              color: isActive ? resonance.color : '#555',
              boxShadow: isActive
                ? `0 0 12px ${resonance.color}33`
                : isGearActive
                  ? `0 0 6px ${resonance.color}22`
                  : 'none',
            }}
            title={`${sphere.label} (${resonance.hz}Hz · ${resonance.label})`}
          >
            {sphere.icon}
          </button>
        );
      })}

      {/* Séparateur */}
      <div
        className="w-6 my-1"
        style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}
      />

      {/* AT·OM Mapping — Navigation historique */}
      <button
        className="w-10 h-10 rounded-lg flex items-center justify-center text-base transition-all duration-300 hover:bg-white/5"
        style={{
          background: 'rgba(255,255,255,0.04)',
          color: '#555',
        }}
        title="AT·OM Mapping — Navigation historique"
      >
        🗺️
      </button>
    </nav>
  );
}
