/**
 * AT·OM — ATOMLayout
 * Layout principal de l'OS — Assemblage des 3 Hubs
 *
 *   ┌─────────────────────────────────────────┐
 *   │              TopBar (Conscience)         │  ← Fréquence, Mode, État
 *   ├──────────┬──────────────────────────────┤
 *   │ Sphere   │                              │
 *   │ Navigator│     DataExplorer             │  ← Ratio Phi (38.2% / 61.8%)
 *   │ (9 ⚙️)   │  (Optimal vs Actuel)         │
 *   │          │                              │
 *   ├──────────┴──────────────────────────────┤
 *   │           BottomTaskbar (Exécution)     │  ← Commandes, Onglets
 *   └─────────────────────────────────────────┘
 */

import React from 'react';
import { ATOMProvider } from '../../context/GlobalStateContext';
import { TopBar } from './TopBar';
import { MainEngine } from './MainEngine';
import { BottomTaskbar } from './BottomTaskbar';

export function ATOMLayout() {
  return (
    <ATOMProvider>
      <div
        className="fixed inset-0 overflow-hidden"
        style={{
          background: '#050505',
          fontFamily: "'Inter', 'Segoe UI', system-ui, sans-serif",
        }}
      >
        <TopBar />
        <MainEngine />
        <BottomTaskbar />
      </div>
    </ATOMProvider>
  );
}

export default ATOMLayout;
