/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *      ███████╗██████╗ ██████╗  ██████╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗██████╗  █████╗ ██████╗ ██╗   ██╗
 *      ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
 *      █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║  ██║███████║██████╔╝ ╚████╔╝
 *      ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║  ██║██╔══██║██╔══██╗  ╚██╔╝
 *      ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝██║  ██║██║  ██║   ██║
 *      ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
 *
 *                              🛡️ ERROR BOUNDARY & ERROR HANDLING CHE·NU 🛡️
 *                        Gestion globale des erreurs avec UI de récupération
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { Component, createContext, useContext, useState, useCallback } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXTE D'ERREUR GLOBAL
// ═══════════════════════════════════════════════════════════════════════════════

const ErrorContext = createContext(null);

export const useError = () => {
  const context = useContext(ErrorContext);
  if (!context) {
    throw new Error('useError must be used within ErrorProvider');
  }
  return context;
};

// ═══════════════════════════════════════════════════════════════════════════════
// PROVIDER D'ERREUR
// ═══════════════════════════════════════════════════════════════════════════════

export const ErrorProvider = ({ children }) => {
  const [errors, setErrors] = useState([]);
  const [notifications, setNotifications] = useState([]);

  // Ajouter une erreur
  const addError = useCallback((error, options = {}) => {
    const errorObj = {
      id: `error_${Date.now()}`,
      message: error.message || String(error),
      type: options.type || 'error',
      code: error.code || error.statusCode,
      timestamp: new Date().toISOString(),
      dismissible: options.dismissible !== false,
      autoHide: options.autoHide || false,
      duration: options.duration || 5000
    };

    setErrors(prev => [...prev, errorObj]);

    // Log l'erreur
    console.error('[ErrorProvider]', errorObj);

    // Auto-hide si configuré
    if (errorObj.autoHide) {
      setTimeout(() => {
        dismissError(errorObj.id);
      }, errorObj.duration);
    }

    return errorObj.id;
  }, []);

  // Supprimer une erreur
  const dismissError = useCallback((errorId) => {
    setErrors(prev => prev.filter(e => e.id !== errorId));
  }, []);

  // Vider toutes les erreurs
  const clearErrors = useCallback(() => {
    setErrors([]);
  }, []);

  // Ajouter une notification
  const addNotification = useCallback((message, type = 'info', options = {}) => {
    const notification = {
      id: `notif_${Date.now()}`,
      message,
      type,
      timestamp: new Date().toISOString(),
      duration: options.duration || 4000
    };

    setNotifications(prev => [...prev, notification]);

    // Auto-dismiss
    setTimeout(() => {
      dismissNotification(notification.id);
    }, notification.duration);

    return notification.id;
  }, []);

  // Supprimer une notification
  const dismissNotification = useCallback((notifId) => {
    setNotifications(prev => prev.filter(n => n.id !== notifId));
  }, []);

  // Handlers pour différents types d'erreurs
  const handleNetworkError = useCallback((error) => {
    return addError(error, {
      type: 'network',
      autoHide: true,
      duration: 8000
    });
  }, [addError]);

  const handleValidationError = useCallback((error) => {
    return addError(error, {
      type: 'validation',
      autoHide: true,
      duration: 5000
    });
  }, [addError]);

  const handleAuthError = useCallback((error) => {
    return addError(error, {
      type: 'auth',
      autoHide: false
    });
  }, [addError]);

  const value = {
    errors,
    notifications,
    addError,
    dismissError,
    clearErrors,
    addNotification,
    dismissNotification,
    handleNetworkError,
    handleValidationError,
    handleAuthError
  };

  return (
    <ErrorContext.Provider value={value}>
      {children}
      <ErrorDisplay errors={errors} onDismiss={dismissError} />
      <NotificationDisplay notifications={notifications} onDismiss={dismissNotification} />
    </ErrorContext.Provider>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: AFFICHAGE DES ERREURS
// ═══════════════════════════════════════════════════════════════════════════════

const ErrorDisplay = ({ errors, onDismiss }) => {
  if (errors.length === 0) return null;

  const getErrorStyle = (type) => {
    switch (type) {
      case 'network':
        return { bg: 'bg-orange-500/10', border: 'border-orange-500', icon: '🌐', color: 'text-orange-400' };
      case 'validation':
        return { bg: 'bg-yellow-500/10', border: 'border-yellow-500', icon: '⚠️', color: 'text-yellow-400' };
      case 'auth':
        return { bg: 'bg-red-500/10', border: 'border-red-500', icon: '🔐', color: 'text-red-400' };
      default:
        return { bg: 'bg-red-500/10', border: 'border-red-500', icon: '❌', color: 'text-red-400' };
    }
  };

  return (
    <div className="fixed bottom-20 right-4 z-50 space-y-2 max-w-md">
      {errors.map(error => {
        const style = getErrorStyle(error.type);
        return (
          <div
            key={error.id}
            className={`${style.bg} border ${style.border} rounded-lg p-4 shadow-lg animate-slide-in`}
          >
            <div className="flex items-start gap-3">
              <span className="text-xl">{style.icon}</span>
              <div className="flex-1">
                <p className={`text-sm ${style.color}`}>{error.message}</p>
                {error.code && (
                  <p className="text-xs text-gray-500 mt-1">Code: {error.code}</p>
                )}
              </div>
              {error.dismissible && (
                <button
                  onClick={() => onDismiss(error.id)}
                  className="text-gray-500 hover:text-white transition-colors"
                >
                  ✕
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: AFFICHAGE DES NOTIFICATIONS
// ═══════════════════════════════════════════════════════════════════════════════

const NotificationDisplay = ({ notifications, onDismiss }) => {
  if (notifications.length === 0) return null;

  const getNotifStyle = (type) => {
    switch (type) {
      case 'success':
        return { bg: 'bg-green-500/10', border: 'border-green-500', icon: '✓', color: 'text-green-400' };
      case 'warning':
        return { bg: 'bg-yellow-500/10', border: 'border-yellow-500', icon: '⚠', color: 'text-yellow-400' };
      case 'error':
        return { bg: 'bg-red-500/10', border: 'border-red-500', icon: '✕', color: 'text-red-400' };
      default:
        return { bg: 'bg-blue-500/10', border: 'border-blue-500', icon: 'ℹ', color: 'text-blue-400' };
    }
  };

  return (
    <div className="fixed top-20 right-4 z-50 space-y-2 max-w-md">
      {notifications.map(notif => {
        const style = getNotifStyle(notif.type);
        return (
          <div
            key={notif.id}
            className={`${style.bg} border ${style.border} rounded-lg p-3 shadow-lg animate-slide-in`}
          >
            <div className="flex items-center gap-3">
              <span className={style.color}>{style.icon}</span>
              <p className={`text-sm ${style.color}`}>{notif.message}</p>
              <button
                onClick={() => onDismiss(notif.id)}
                className="ml-auto text-gray-500 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ERROR BOUNDARY (CLASS COMPONENT)
// ═══════════════════════════════════════════════════════════════════════════════

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });

    // Log l'erreur
    console.error('[ErrorBoundary] Caught error:', error, errorInfo);

    // Envoyer à un service de monitoring (si configuré)
    this.reportError(error, errorInfo);
  }

  reportError(error, errorInfo) {
    // Ici vous pouvez envoyer l'erreur à Sentry, LogRocket, etc.
    try {
      const errorReport = {
        message: error.message,
        stack: error.stack,
        componentStack: errorInfo?.componentStack,
        timestamp: new Date().toISOString(),
        url: window.location.href,
        userAgent: navigator.userAgent
      };

      // Sauvegarder localement pour debug
      const reports = JSON.parse(localStorage.getItem('chenu_error_reports') || '[]');
      reports.push(errorReport);
      localStorage.setItem('chenu_error_reports', JSON.stringify(reports.slice(-50)));

    } catch (e) {
      console.error('[ErrorBoundary] Failed to report error:', e);
    }
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  handleReload = () => {
    window.location.reload();
  };

  handleGoHome = () => {
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      // UI de fallback personnalisée
      return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-gray-900 rounded-2xl border border-red-500/30 p-8 text-center">
            {/* Icon */}
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-red-500/10 flex items-center justify-center">
              <span className="text-4xl">⚠️</span>
            </div>

            {/* Titre */}
            <h1 className="text-xl font-bold text-white mb-2">
              Oups ! Une erreur s'est produite
            </h1>

            <p className="text-gray-400 text-sm mb-6">
              L'application a rencontré un problème inattendu.
              Nos équipes en sont informées.
            </p>

            {/* Détails de l'erreur (mode debug) */}
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details className="mb-6 text-left">
                <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-400">
                  Détails techniques
                </summary>
                <pre className="mt-2 p-3 bg-black/50 rounded-lg text-xs text-red-400 overflow-auto max-h-40">
                  {this.state.error.toString()}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </details>
            )}

            {/* Actions */}
            <div className="space-y-3">
              <button
                onClick={this.handleRetry}
                className="w-full px-4 py-3 bg-yellow-600 text-black font-medium rounded-lg
                  hover:bg-yellow-500 transition-colors"
              >
                Réessayer
              </button>

              <button
                onClick={this.handleReload}
                className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg
                  hover:bg-gray-700 transition-colors"
              >
                Recharger la page
              </button>

              <button
                onClick={this.handleGoHome}
                className="w-full px-4 py-3 text-gray-400 hover:text-white transition-colors text-sm"
              >
                Retour à l'accueil
              </button>
            </div>

            {/* Footer */}
            <p className="mt-6 text-xs text-gray-600">
              CHE·NU V76 • Code erreur: {this.state.error?.code || 'UNKNOWN'}
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOC POUR WRAPPER LES COMPOSANTS
// ═══════════════════════════════════════════════════════════════════════════════

export const withErrorBoundary = (WrappedComponent, fallback = null) => {
  return function WithErrorBoundary(props) {
    return (
      <ErrorBoundary>
        <WrappedComponent {...props} />
      </ErrorBoundary>
    );
  };
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK POUR TRY-CATCH ASYNC
// ═══════════════════════════════════════════════════════════════════════════════

export const useAsyncError = () => {
  const { addError, handleNetworkError } = useError();

  const handleAsync = useCallback(async (asyncFn, options = {}) => {
    try {
      return await asyncFn();
    } catch (error) {
      if (error.name === 'NetworkError') {
        handleNetworkError(error);
      } else {
        addError(error, options);
      }

      if (options.rethrow) {
        throw error;
      }

      return options.fallback !== undefined ? options.fallback : null;
    }
  }, [addError, handleNetworkError]);

  return handleAsync;
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: LOADER AVEC ERREUR
// ═══════════════════════════════════════════════════════════════════════════════

export const LoadingState = ({ isLoading, error, children, onRetry }) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="w-10 h-10 border-2 border-yellow-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-400 text-sm">Chargement...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <span className="text-4xl mb-4 block">❌</span>
          <p className="text-red-400 text-sm mb-4">{error.message || 'Une erreur est survenue'}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 text-sm"
            >
              Réessayer
            </button>
          )}
        </div>
      </div>
    );
  }

  return children;
};

// ═══════════════════════════════════════════════════════════════════════════════
// CSS ANIMATIONS (à ajouter dans index.css ou tailwind)
// ═══════════════════════════════════════════════════════════════════════════════

const styles = `
@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slide-in {
  animation: slide-in 0.3s ease-out;
}
`;

// Injecter les styles
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}

export default ErrorBoundary;
