/**
 * AT·OM — Route Protégée
 * Garde les routes privées derrière l'authentification et les rôles
 */

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: ÉCRAN DE CHARGEMENT
// ═══════════════════════════════════════════════════════════════════════════════

const LoadingScreen = () => (
  <div className="min-h-screen bg-black flex items-center justify-center">
    <div className="text-center">
      <div className="text-4xl animate-pulse mb-4">🔱</div>
      <p className="text-yellow-400 text-sm">Vérification d'accès...</p>
      <div className="mt-4 w-32 h-1 bg-gray-800 rounded-full mx-auto overflow-hidden">
        <div className="h-full bg-yellow-500 rounded-full animate-pulse" style={{ width: '60%' }} />
      </div>
    </div>
  </div>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: ÉCRAN D'ACCÈS REFUSÉ
// ═══════════════════════════════════════════════════════════════════════════════

const AccessDenied = ({ requiredRole, currentRole }) => (
  <div className="min-h-screen bg-black flex items-center justify-center px-4">
    <div className="text-center max-w-md">
      <div className="text-6xl mb-4">🚫</div>
      <h1 className="text-2xl font-bold text-red-400 mb-2">Accès Restreint</h1>
      <p className="text-gray-400 mb-4">
        Cette zone nécessite un niveau d'accréditation supérieur.
      </p>
      <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-4 mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-500">Votre rôle</span>
          <span className="text-yellow-400">{currentRole || 'Citoyen'}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-500">Requis</span>
          <span className="text-red-400">{requiredRole}</span>
        </div>
      </div>
      <a
        href="/accreditation"
        className="inline-block px-6 py-3 bg-yellow-600 text-black rounded-lg font-bold hover:bg-yellow-500 transition-colors"
      >
        Demander l'Accréditation →
      </a>
    </div>
  </div>
);

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: ROUTE PROTÉGÉE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * ProtectedRoute — Enveloppe une route avec vérification d'authentification
 *
 * Props:
 *   children      — Le composant à rendre si autorisé
 *   requiredRole  — Rôle minimum requis (optionnel: 'SOUVERAIN', 'COLLABORATEUR', 'CITOYEN')
 *   redirectTo    — Où rediriger si non authentifié (défaut: '/entree')
 *   requireAuth   — Si true, exige une connexion (défaut: true)
 */
const ProtectedRoute = ({
  children,
  requiredRole = null,
  redirectTo = '/entree',
  requireAuth = true
}) => {
  const { user, loading, isAuthenticated, getRole, ROLES } = useAuth();
  const location = useLocation();

  // Pendant le chargement, afficher l'écran de chargement
  if (loading) {
    return <LoadingScreen />;
  }

  // Si authentification requise mais pas connecté
  if (requireAuth && !isAuthenticated) {
    return <Navigate to={redirectTo} state={{ from: location.pathname }} replace />;
  }

  // Si un rôle spécifique est requis
  if (requiredRole && isAuthenticated) {
    const currentRole = getRole();

    // Hiérarchie des rôles: SOUVERAIN > COLLABORATEUR > CITOYEN
    const roleHierarchy = {
      [ROLES.SOUVERAIN]: 3,
      [ROLES.COLLABORATEUR]: 2,
      [ROLES.CITOYEN]: 1,
    };

    const userLevel = roleHierarchy[currentRole] || 0;
    const requiredLevel = roleHierarchy[requiredRole] || 0;

    if (userLevel < requiredLevel) {
      return <AccessDenied requiredRole={requiredRole} currentRole={currentRole} />;
    }
  }

  // Tout est bon — rendre le contenu
  return children;
};

// ═══════════════════════════════════════════════════════════════════════════════
// VARIANTES RACCOURCIES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Route réservée au Souverain uniquement
 */
export const SovereignRoute = ({ children }) => (
  <ProtectedRoute requiredRole="SOUVERAIN">
    {children}
  </ProtectedRoute>
);

/**
 * Route réservée aux Collaborateurs et au-dessus
 */
export const CollaboratorRoute = ({ children }) => (
  <ProtectedRoute requiredRole="COLLABORATEUR">
    {children}
  </ProtectedRoute>
);

/**
 * Route réservée à tout utilisateur authentifié
 */
export const AuthenticatedRoute = ({ children, redirectTo }) => (
  <ProtectedRoute redirectTo={redirectTo}>
    {children}
  </ProtectedRoute>
);

export default ProtectedRoute;
