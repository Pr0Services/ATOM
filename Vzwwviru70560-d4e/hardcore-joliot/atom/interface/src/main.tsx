// ═══════════════════════════════════════════════════════════════════════════
// AT·OM INTERFACE - ENTRY POINT
// ═══════════════════════════════════════════════════════════════════════════

import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import './styles/globals.css';

// Register service worker for offline support
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').then(
      (registration) => {
        console.log('[SW] Registration successful:', registration.scope);
      },
      (error) => {
        console.error('[SW] Registration failed:', error);
      }
    );
  });
}

// Render app
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
