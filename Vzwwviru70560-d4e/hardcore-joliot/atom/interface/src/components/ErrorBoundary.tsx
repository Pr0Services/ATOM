// ═══════════════════════════════════════════════════════════════════════════
// AT·OM ERROR BOUNDARY
// Error handling and recovery for React components
// ═══════════════════════════════════════════════════════════════════════════

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, RefreshCw, Home, Bug } from 'lucide-react';

// ─────────────────────────────────────────────────────────────────────────────
// TYPES
// ─────────────────────────────────────────────────────────────────────────────

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

// ─────────────────────────────────────────────────────────────────────────────
// ERROR BOUNDARY CLASS
// ─────────────────────────────────────────────────────────────────────────────

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error, errorInfo: null };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({ errorInfo });
    
    // Call optional error handler
    this.props.onError?.(error, errorInfo);

    // Log to external service (in production)
    if (import.meta.env.PROD) {
      // Send to error tracking service
      // logErrorToService(error, errorInfo);
    }
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  private handleReload = () => {
    window.location.reload();
  };

  private handleGoHome = () => {
    window.location.href = '/';
  };

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <ErrorScreen
          error={this.state.error}
          errorInfo={this.state.errorInfo}
          onReset={this.handleReset}
          onReload={this.handleReload}
          onGoHome={this.handleGoHome}
        />
      );
    }

    return this.props.children;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// ERROR SCREEN
// ─────────────────────────────────────────────────────────────────────────────

interface ErrorScreenProps {
  error: Error | null;
  errorInfo: ErrorInfo | null;
  onReset: () => void;
  onReload: () => void;
  onGoHome: () => void;
}

function ErrorScreen({ error, errorInfo, onReset, onReload, onGoHome }: ErrorScreenProps) {
  const [showDetails, setShowDetails] = React.useState(false);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      {/* Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-radial from-red-600/5 to-transparent" />
      </div>

      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="relative max-w-lg w-full bg-slate-900/80 backdrop-blur-xl rounded-2xl border border-red-500/20 p-8"
      >
        {/* Icon */}
        <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-red-500/20 flex items-center justify-center">
          <AlertTriangle className="w-8 h-8 text-red-400" />
        </div>

        {/* Title */}
        <h1 className="text-2xl font-bold text-white text-center mb-2">
          Quelque chose s'est mal passé
        </h1>
        <p className="text-white/50 text-center mb-8">
          Une erreur inattendue s'est produite. Vos données sont en sécurité.
        </p>

        {/* Actions */}
        <div className="flex flex-col gap-3 mb-6">
          <button
            onClick={onReset}
            className="w-full flex items-center justify-center gap-2 py-3 bg-atom-600 hover:bg-atom-700 rounded-xl font-medium text-white transition-colors"
          >
            <RefreshCw className="w-5 h-5" />
            Réessayer
          </button>

          <div className="flex gap-3">
            <button
              onClick={onReload}
              className="flex-1 flex items-center justify-center gap-2 py-3 bg-white/10 hover:bg-white/20 rounded-xl font-medium text-white transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              Recharger
            </button>
            <button
              onClick={onGoHome}
              className="flex-1 flex items-center justify-center gap-2 py-3 bg-white/10 hover:bg-white/20 rounded-xl font-medium text-white transition-colors"
            >
              <Home className="w-4 h-4" />
              Accueil
            </button>
          </div>
        </div>

        {/* Error details toggle */}
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="w-full flex items-center justify-center gap-2 py-2 text-sm text-white/40 hover:text-white/60 transition-colors"
        >
          <Bug className="w-4 h-4" />
          {showDetails ? 'Masquer les détails' : 'Afficher les détails'}
        </button>

        {/* Error details */}
        {showDetails && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            className="mt-4 p-4 bg-black/30 rounded-xl overflow-hidden"
          >
            <div className="mb-4">
              <h3 className="text-sm font-medium text-red-400 mb-1">Erreur:</h3>
              <pre className="text-xs text-white/60 whitespace-pre-wrap break-all font-mono">
                {error?.message || 'Unknown error'}
              </pre>
            </div>
            
            {error?.stack && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-red-400 mb-1">Stack trace:</h3>
                <pre className="text-xs text-white/40 whitespace-pre-wrap break-all font-mono max-h-40 overflow-y-auto">
                  {error.stack}
                </pre>
              </div>
            )}

            {errorInfo?.componentStack && (
              <div>
                <h3 className="text-sm font-medium text-red-400 mb-1">Component stack:</h3>
                <pre className="text-xs text-white/40 whitespace-pre-wrap break-all font-mono max-h-40 overflow-y-auto">
                  {errorInfo.componentStack}
                </pre>
              </div>
            )}

            <button
              onClick={() => {
                const errorText = `Error: ${error?.message}\n\nStack: ${error?.stack}\n\nComponent Stack: ${errorInfo?.componentStack}`;
                navigator.clipboard.writeText(errorText);
              }}
              className="mt-4 text-xs text-atom-400 hover:text-atom-300 transition-colors"
            >
              Copier les détails
            </button>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// SIMPLE ERROR FALLBACK
// ─────────────────────────────────────────────────────────────────────────────

interface ErrorFallbackProps {
  error?: Error;
  resetErrorBoundary?: () => void;
}

export function ErrorFallback({ error, resetErrorBoundary }: ErrorFallbackProps) {
  return (
    <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
      <div className="flex items-center gap-3 mb-3">
        <AlertTriangle className="w-5 h-5 text-red-400" />
        <h3 className="font-medium text-red-400">Erreur</h3>
      </div>
      <p className="text-sm text-white/60 mb-4">
        {error?.message || 'Une erreur inattendue s\'est produite'}
      </p>
      {resetErrorBoundary && (
        <button
          onClick={resetErrorBoundary}
          className="text-sm text-atom-400 hover:text-atom-300 transition-colors"
        >
          Réessayer
        </button>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HOOK FOR ERROR HANDLING
// ─────────────────────────────────────────────────────────────────────────────

export function useErrorHandler() {
  const [error, setError] = React.useState<Error | null>(null);

  const handleError = React.useCallback((error: Error) => {
    console.error('Error caught:', error);
    setError(error);
  }, []);

  const clearError = React.useCallback(() => {
    setError(null);
  }, []);

  // Throw error to be caught by ErrorBoundary
  if (error) {
    throw error;
  }

  return { handleError, clearError };
}

export default ErrorBoundary;
