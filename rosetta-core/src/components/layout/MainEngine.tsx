/**
 * AT·OM — MainEngine (Navigation)
 * Zone centrale de l'OS — Layout 3 panneaux symétriques
 *
 * Layout :
 *   ┌────────┬──────────────────────────────┬────────┐
 *   │  Nav   │       ContentArea            │  Comm  │
 *   │ (56px) │    (flex-1, onglets)         │ (56px) │
 *   │ 9+1    │                              │  6+3   │
 *   │ icônes │                              │ icônes │
 *   └────────┴──────────────────────────────┴────────┘
 *
 * Le même principe des deux côtés :
 *   Gauche = Sphères (navigation par domaine)
 *   Droite = Communication (navigation par canal)
 *   Centre = Contenu avec onglets dynamiques
 */

import React from 'react';
import { useATOM } from '../../context/GlobalStateContext';
import { SphereNavigator } from './SphereNavigator';
import { ContentArea } from './ContentArea';
import { CommHub } from './CommHub';

const SIDE_PANEL_WIDTH = '56px';

export function MainEngine() {
  const { state } = useATOM();

  return (
    <main
      className="fixed left-0 right-0 flex gap-1 p-1"
      style={{
        top: '48px',      // Sous TopBar
        bottom: '48px',   // Au-dessus BottomTaskbar
      }}
    >
      {/* Panneau Gauche — SphereNavigator (icônes) */}
      {state.sphere_navigator_open && (
        <div style={{ width: SIDE_PANEL_WIDTH, flexShrink: 0 }}>
          <SphereNavigator />
        </div>
      )}

      {/* Panneau Central — ContentArea (onglets) */}
      <div
        className="flex-1 rounded-lg overflow-hidden"
        style={{
          background: 'rgba(5, 5, 5, 0.4)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(255, 255, 255, 0.06)',
        }}
      >
        <ContentArea />
      </div>

      {/* Panneau Droit — CommHub (icônes) */}
      {state.comm_hub_open && (
        <div style={{ width: SIDE_PANEL_WIDTH, flexShrink: 0 }}>
          <CommHub />
        </div>
      )}
    </main>
  );
}
