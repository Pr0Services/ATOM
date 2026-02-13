// ═══════════════════════════════════════════════════════════════════════════
// AT·OM INTERFACE - MAIN APPLICATION
// Sovereign Identity & Productivity Platform
// ═══════════════════════════════════════════════════════════════════════════

import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from '@/components/Dashboard';
// Canon AT·OM Pages
import { LeSceau } from '@/pages/LeSceau';
import { Essaim } from '@/pages/Essaim';
import { Protocol999 } from '@/pages/Protocol999';
import { Genie } from '@/pages/Genie';
import { Alchimie } from '@/pages/Alchimie';
import { Flux } from '@/pages/Flux';
import { Sante } from '@/pages/Sante';
import { Sovereign } from '@/pages/Sovereign';
import { AdminCockpit } from '@/pages/AdminCockpit';
import { AgentWorkspace } from '@/pages/AgentWorkspace';
import { Landing } from '@/pages/Landing';
import { ProgressiveRegister } from '@/pages/Register';
import { AnalyticsDashboard } from '@/pages/AnalyticsDashboard';
import { CGU } from '@/pages/legal/CGU';
import { Privacy } from '@/pages/legal/Privacy';
import { Mentions } from '@/pages/legal/Mentions';
// Components
import { ContextualAssistant } from '@/components/ContextualAssistant';
import { OnboardingWizard, hasCompletedOnboarding } from '@/components/OnboardingWizard';
import { useAtomStore } from '@/stores/atom.store';
import {
  initializeRealTimeServices,
  shutdownRealTimeServices,
  heartbeatService,
  arithmosService,
} from '@/services/realtime.service';
import { OfflineService } from '@/services/offline.service';
import { EncryptionService } from '@/services/encryption.service';
import { errorMonitor } from '@/services/error-monitor.service';
import { FloatingHealthIndicator } from '@/components/ServiceHealthWidget';

// ─────────────────────────────────────────────────────────────────────────────
// QUERY CLIENT
// ─────────────────────────────────────────────────────────────────────────────

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

// ─────────────────────────────────────────────────────────────────────────────
// APP INITIALIZATION
// ─────────────────────────────────────────────────────────────────────────────

function useAppInitialization() {
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { updateHeartbeat, updateArithmos, updateOffline, setIdentity } = useAtomStore();

  useEffect(() => {
    const initialize = async () => {
      try {
        console.log('[App] Initializing AT·OM Interface...');

        // Initialize error monitoring
        errorMonitor.init({
          enabled: true,
          reportEndpoint: import.meta.env.VITE_ERROR_REPORT_URL || undefined,
        });

        // Initialize offline service and network monitoring
        OfflineService.onNetworkChange((isOnline) => {
          updateOffline({ isOnline });
        });

        // Get initial offline state
        const offlineState = await OfflineService.getOfflineState();
        updateOffline(offlineState);

        // Check for stored identity
        if (EncryptionService.hasStoredIdentity()) {
          console.log('[App] Stored identity found');
          // Would prompt for password in real app
        }

        // Initialize real-time services
        const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
        initializeRealTimeServices(wsUrl);

        // Subscribe to real-time updates
        heartbeatService.subscribe((state) => {
          updateHeartbeat(state);
        });

        arithmosService.subscribe((state) => {
          updateArithmos(state);
        });

        // Try to sync pending operations if online
        if (navigator.onLine) {
          const syncResult = await OfflineService.syncPendingOperations();
          console.log('[App] Initial sync result:', syncResult);
        }

        console.log('[App] Initialization complete');
        setIsInitialized(true);
      } catch (err) {
        console.error('[App] Initialization failed:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      }
    };

    initialize();

    // Cleanup on unmount
    return () => {
      shutdownRealTimeServices();
    };
  }, [updateHeartbeat, updateArithmos, updateOffline, setIdentity]);

  return { isInitialized, error };
}

// ─────────────────────────────────────────────────────────────────────────────
// LOADING SCREEN
// ─────────────────────────────────────────────────────────────────────────────

function LoadingScreen() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-center">
        {/* Logo */}
        <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-atom-500 to-atom-700 flex items-center justify-center animate-pulse">
          <svg
            className="w-10 h-10 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
        </div>

        {/* Text */}
        <h1 className="text-2xl font-bold text-white mb-2">AT·OM</h1>
        <p className="text-white/50">Initialisation...</p>

        {/* Loading indicator */}
        <div className="mt-6 w-48 h-1 bg-white/10 rounded-full overflow-hidden mx-auto">
          <div className="h-full bg-atom-500 rounded-full animate-loading" />
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ERROR SCREEN
// ─────────────────────────────────────────────────────────────────────────────

function ErrorScreen({ error }: { error: string }) {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-center max-w-md px-4">
        <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-red-500/20 flex items-center justify-center">
          <svg
            className="w-8 h-8 text-red-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <h1 className="text-xl font-bold text-white mb-2">Erreur d'initialisation</h1>
        <p className="text-white/50 mb-6">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-3 bg-atom-600 hover:bg-atom-700 rounded-lg transition-colors text-white font-medium"
        >
          Réessayer
        </button>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN APP COMPONENT
// ─────────────────────────────────────────────────────────────────────────────

function AppContent() {
  const { isInitialized, error } = useAppInitialization();
  const [showOnboarding, setShowOnboarding] = useState(() => !hasCompletedOnboarding());

  if (error) {
    return <ErrorScreen error={error} />;
  }

  if (!isInitialized) {
    return <LoadingScreen />;
  }

  return (
    <BrowserRouter>
      {/* Contextual Assistant - available on all pages */}
      <ContextualAssistant />

      {/* Floating Health Indicator - only shows if services are degraded */}
      <FloatingHealthIndicator />

      {/* Onboarding Wizard - shows on first visit */}
      {showOnboarding && (
        <OnboardingWizard
          onComplete={() => setShowOnboarding(false)}
          onSkip={() => setShowOnboarding(false)}
        />
      )}
      <Routes>
        {/* Canon AT·OM Routes */}
        {/* 1. L'Interface Maitresse - Le Sceau de l'Engagement */}
        <Route path="/" element={<LeSceau />} />

        {/* 2. Le Hub des 350 Agents - L'Essaim */}
        <Route path="/essaim" element={<Essaim />} />
        <Route path="/swarm" element={<Essaim />} />

        {/* 3. Dashboard Principal */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/sphere/:sphereId" element={<Dashboard />} />

        {/* 4. Terminaux de Modules - Canon AT·OM */}
        <Route path="/genie" element={<Genie />} />          {/* Education - Genie de Demain */}
        <Route path="/alchimie" element={<Alchimie />} />    {/* Transmutation */}
        <Route path="/flux" element={<Flux />} />            {/* Economie - Transport */}
        <Route path="/sante" element={<Sante />} />          {/* Guerison */}

        {/* 5. Protocol-999 - Kill-Switch (INVISIBLE/CACHE) */}
        <Route path="/protocol-999" element={<Protocol999 />} />

        {/* 6. Sovereign Dashboard - Monitoring Frequentiel (PRIVE) */}
        <Route path="/sovereign" element={<Sovereign />} />

        {/* 7. Admin Cockpit - God Mode (ULTRA-PRIVE) */}
        <Route path="/admin" element={<AdminCockpit />} />

        {/* 8. Agent Workspaces - Bureaux Isolés (ORCHESTRATEURS) */}
        <Route path="/workspace/:agentId" element={<AgentWorkspace />} />

        {/* 9. Landing Page - Point d'entrée marketing */}
        <Route path="/landing" element={<Landing />} />
        <Route path="/welcome" element={<Landing />} />

        {/* 10. Analytics Dashboard - Funnel & Metrics (ADMIN) */}
        <Route path="/analytics" element={<AnalyticsDashboard />} />

        {/* 11. Authentication - Register/Login */}
        <Route path="/register" element={<ProgressiveRegister />} />
        <Route path="/auth/register" element={<ProgressiveRegister />} />

        {/* 12. Pages Légales */}
        <Route path="/legal/cgu" element={<CGU />} />
        <Route path="/legal/privacy" element={<Privacy />} />
        <Route path="/legal/mentions" element={<Mentions />} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// ROOT APP WITH PROVIDERS
// ─────────────────────────────────────────────────────────────────────────────

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;
