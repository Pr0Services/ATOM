/**
 * ERROR MESSAGES SERVICE - Standardized UX Error Handling
 * =========================================================
 *
 * Service centralisé pour des messages d'erreur:
 * - Actionnables (l'utilisateur sait quoi faire)
 * - Cohérents (même ton, même structure)
 * - Localisés (français par défaut)
 * - Contextuels (adaptés au parcours)
 *
 * Objectif audit: "Standardisation messages d'erreurs UX"
 */

// =============================================================================
// TYPES
// =============================================================================

export type ErrorCategory =
  | 'network'
  | 'auth'
  | 'validation'
  | 'permission'
  | 'notFound'
  | 'rateLimit'
  | 'server'
  | 'timeout'
  | 'offline'
  | 'unknown';

export type ErrorSeverity = 'info' | 'warning' | 'error' | 'critical';

export interface UserFriendlyError {
  title: string;
  message: string;
  suggestion: string;
  action?: {
    label: string;
    handler: () => void;
  };
  severity: ErrorSeverity;
  category: ErrorCategory;
  retryable: boolean;
  technical?: string; // For debugging
}

export interface ErrorContext {
  operation: string;
  resource?: string;
  userId?: string;
  attempt?: number;
}

// =============================================================================
// ERROR TEMPLATES
// =============================================================================

const ERROR_TEMPLATES: Record<ErrorCategory, Omit<UserFriendlyError, 'technical' | 'action'>> = {
  network: {
    title: 'Connexion interrompue',
    message: 'Impossible de joindre nos serveurs.',
    suggestion: 'Vérifiez votre connexion internet et réessayez.',
    severity: 'warning',
    category: 'network',
    retryable: true,
  },
  auth: {
    title: 'Session expirée',
    message: 'Votre session a expiré pour des raisons de sécurité.',
    suggestion: 'Reconnectez-vous pour continuer.',
    severity: 'warning',
    category: 'auth',
    retryable: false,
  },
  validation: {
    title: 'Données invalides',
    message: 'Certaines informations sont incorrectes.',
    suggestion: 'Vérifiez les champs en rouge et corrigez-les.',
    severity: 'info',
    category: 'validation',
    retryable: true,
  },
  permission: {
    title: 'Accès refusé',
    message: 'Vous n\'avez pas les droits pour cette action.',
    suggestion: 'Contactez un administrateur si nécessaire.',
    severity: 'warning',
    category: 'permission',
    retryable: false,
  },
  notFound: {
    title: 'Ressource introuvable',
    message: 'L\'élément demandé n\'existe pas ou a été supprimé.',
    suggestion: 'Retournez à la page précédente.',
    severity: 'info',
    category: 'notFound',
    retryable: false,
  },
  rateLimit: {
    title: 'Trop de requêtes',
    message: 'Vous avez atteint la limite d\'utilisation.',
    suggestion: 'Patientez quelques minutes avant de réessayer.',
    severity: 'warning',
    category: 'rateLimit',
    retryable: true,
  },
  server: {
    title: 'Erreur serveur',
    message: 'Nos serveurs rencontrent un problème.',
    suggestion: 'Réessayez dans quelques instants.',
    severity: 'error',
    category: 'server',
    retryable: true,
  },
  timeout: {
    title: 'Délai dépassé',
    message: 'L\'opération a pris trop de temps.',
    suggestion: 'Réessayez ou simplifiez votre demande.',
    severity: 'warning',
    category: 'timeout',
    retryable: true,
  },
  offline: {
    title: 'Mode hors-ligne',
    message: 'Vous êtes actuellement déconnecté.',
    suggestion: 'Cette action sera synchronisée au retour de la connexion.',
    severity: 'info',
    category: 'offline',
    retryable: false,
  },
  unknown: {
    title: 'Erreur inattendue',
    message: 'Quelque chose s\'est mal passé.',
    suggestion: 'Rafraîchissez la page ou réessayez plus tard.',
    severity: 'error',
    category: 'unknown',
    retryable: true,
  },
};

// =============================================================================
// OPERATION-SPECIFIC MESSAGES
// =============================================================================

const OPERATION_MESSAGES: Record<string, Partial<Record<ErrorCategory, string>>> = {
  login: {
    auth: 'Email ou mot de passe incorrect.',
    network: 'Impossible de vérifier vos identifiants.',
    rateLimit: 'Trop de tentatives. Attendez 5 minutes.',
  },
  signup: {
    validation: 'Vérifiez votre email et mot de passe.',
    server: 'Inscription temporairement indisponible.',
  },
  loadAgents: {
    network: 'Impossible de charger les agents.',
    timeout: 'Le chargement des agents a pris trop de temps.',
  },
  saveWorkspace: {
    permission: 'Vous ne pouvez pas modifier cet espace.',
    server: 'Impossible de sauvegarder. Vos modifications sont conservées localement.',
  },
  apiCall: {
    rateLimit: 'Limite d\'appels API atteinte. Revenez demain ou passez Premium.',
    timeout: 'L\'agent met trop de temps à répondre.',
  },
  sync: {
    network: 'Synchronisation en pause. Reprise automatique.',
    server: 'Synchronisation échouée. Données sauvegardées localement.',
  },
};

// =============================================================================
// ERROR CLASSIFICATION
// =============================================================================

function classifyError(error: unknown): ErrorCategory {
  // HTTP status codes
  if (error instanceof Response || (error as { status?: number })?.status) {
    const status = (error as { status: number }).status;
    if (status === 401 || status === 403) return 'auth';
    if (status === 404) return 'notFound';
    if (status === 422 || status === 400) return 'validation';
    if (status === 429) return 'rateLimit';
    if (status >= 500) return 'server';
  }

  // Error messages
  const message = error instanceof Error ? error.message.toLowerCase() : String(error).toLowerCase();

  if (message.includes('network') || message.includes('fetch') || message.includes('connection')) {
    return 'network';
  }
  if (message.includes('timeout') || message.includes('timed out')) {
    return 'timeout';
  }
  if (message.includes('offline') || !navigator.onLine) {
    return 'offline';
  }
  if (message.includes('unauthorized') || message.includes('forbidden')) {
    return 'auth';
  }
  if (message.includes('not found')) {
    return 'notFound';
  }
  if (message.includes('permission') || message.includes('denied')) {
    return 'permission';
  }
  if (message.includes('rate limit') || message.includes('quota')) {
    return 'rateLimit';
  }
  if (message.includes('invalid') || message.includes('required')) {
    return 'validation';
  }

  return 'unknown';
}

// =============================================================================
// ERROR MESSAGE SERVICE
// =============================================================================

class ErrorMessageService {
  private static instance: ErrorMessageService;

  private constructor() {}

  static getInstance(): ErrorMessageService {
    if (!ErrorMessageService.instance) {
      ErrorMessageService.instance = new ErrorMessageService();
    }
    return ErrorMessageService.instance;
  }

  /**
   * Convert any error to a user-friendly format
   */
  toUserFriendly(
    error: unknown,
    context?: ErrorContext
  ): UserFriendlyError {
    const category = classifyError(error);
    const template = { ...ERROR_TEMPLATES[category] };

    // Apply operation-specific message if available
    if (context?.operation && OPERATION_MESSAGES[context.operation]?.[category]) {
      template.message = OPERATION_MESSAGES[context.operation][category]!;
    }

    // Add retry context
    if (context?.attempt && context.attempt > 1) {
      template.suggestion = `Tentative ${context.attempt} échouée. ${template.suggestion}`;
    }

    return {
      ...template,
      technical: error instanceof Error ? error.message : String(error),
    };
  }

  /**
   * Create a simple toast message
   */
  toToast(error: unknown, context?: ErrorContext): { message: string; type: 'info' | 'warning' | 'error' } {
    const friendly = this.toUserFriendly(error, context);
    return {
      message: `${friendly.title}: ${friendly.message}`,
      type: friendly.severity === 'critical' ? 'error' : friendly.severity,
    };
  }

  /**
   * Create an inline error message for forms
   */
  toInline(error: unknown, fieldName?: string): string {
    const category = classifyError(error);

    if (category === 'validation' && fieldName) {
      const fieldMessages: Record<string, string> = {
        email: 'Adresse email invalide',
        password: 'Mot de passe trop court (min. 8 caractères)',
        name: 'Nom requis',
        phone: 'Numéro de téléphone invalide',
      };
      return fieldMessages[fieldName] || 'Valeur invalide';
    }

    return ERROR_TEMPLATES[category].message;
  }

  /**
   * Get recovery actions based on error type
   */
  getRecoveryActions(
    category: ErrorCategory
  ): Array<{ label: string; action: string }> {
    const actions: Record<ErrorCategory, Array<{ label: string; action: string }>> = {
      network: [
        { label: 'Réessayer', action: 'retry' },
        { label: 'Mode hors-ligne', action: 'offline' },
      ],
      auth: [
        { label: 'Se reconnecter', action: 'login' },
      ],
      validation: [
        { label: 'Corriger', action: 'focus' },
      ],
      permission: [
        { label: 'Contacter support', action: 'support' },
      ],
      notFound: [
        { label: 'Retour', action: 'back' },
        { label: 'Accueil', action: 'home' },
      ],
      rateLimit: [
        { label: 'Passer Premium', action: 'upgrade' },
      ],
      server: [
        { label: 'Réessayer', action: 'retry' },
        { label: 'Signaler', action: 'report' },
      ],
      timeout: [
        { label: 'Réessayer', action: 'retry' },
        { label: 'Simplifier', action: 'simplify' },
      ],
      offline: [
        { label: 'Continuer hors-ligne', action: 'continue' },
      ],
      unknown: [
        { label: 'Réessayer', action: 'retry' },
        { label: 'Rafraîchir', action: 'refresh' },
      ],
    };

    return actions[category] || actions.unknown;
  }

  /**
   * Check if error is recoverable by retry
   */
  isRetryable(error: unknown): boolean {
    const category = classifyError(error);
    return ERROR_TEMPLATES[category].retryable;
  }

  /**
   * Get appropriate retry delay
   */
  getRetryDelay(error: unknown, attempt: number): number {
    const category = classifyError(error);
    const baseDelay = category === 'rateLimit' ? 60000 : 1000;
    return Math.min(baseDelay * Math.pow(2, attempt - 1), 30000);
  }
}

// =============================================================================
// REACT ERROR BOUNDARY HELPER
// =============================================================================

export function getErrorFallback(
  error: Error,
  resetError: () => void
): {
  title: string;
  message: string;
  actions: Array<{ label: string; onClick: () => void }>;
} {
  const friendly = errorMessages.toUserFriendly(error);

  return {
    title: friendly.title,
    message: friendly.message,
    actions: [
      {
        label: 'Réessayer',
        onClick: resetError,
      },
      {
        label: 'Retour à l\'accueil',
        onClick: () => {
          window.location.href = '/';
        },
      },
    ],
  };
}

// =============================================================================
// EXPORTS
// =============================================================================

export const errorMessages = ErrorMessageService.getInstance();
export { classifyError };
export default errorMessages;
