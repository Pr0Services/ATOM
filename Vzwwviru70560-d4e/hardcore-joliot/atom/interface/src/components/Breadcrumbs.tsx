/**
 * BREADCRUMBS - FIL D'ARIANE
 * ==========================
 *
 * Composant de navigation contextuelle pour AT·OM.
 * Affiche le chemin de navigation et permet de revenir en arrière.
 *
 * ACCESSIBILITE:
 * - ARIA breadcrumb pattern
 * - Navigation clavier
 * - Annonces screen reader
 */

import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { COLORS, TOUCH, TYPOGRAPHY } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface BreadcrumbItem {
  label: string;
  path: string;
  icon?: string;
}

interface BreadcrumbsProps {
  items?: BreadcrumbItem[];
  showHome?: boolean;
}

// =============================================================================
// ROUTE CONFIGURATION
// =============================================================================

const ROUTE_CONFIG: Record<string, { label: string; icon: string; parent?: string }> = {
  '/': { label: 'Le Sceau', icon: '⚡' },
  '/essaim': { label: "L'Essaim", icon: '✨', parent: '/' },
  '/swarm': { label: "L'Essaim", icon: '✨', parent: '/' },
  '/dashboard': { label: 'Dashboard', icon: '📊', parent: '/essaim' },
  '/genie': { label: 'Genie', icon: '🎓', parent: '/essaim' },
  '/alchimie': { label: 'Alchimie', icon: '⚗️', parent: '/essaim' },
  '/flux': { label: 'Flux', icon: '💫', parent: '/essaim' },
  '/sante': { label: 'Santé', icon: '❤️', parent: '/essaim' },
  '/sovereign': { label: 'Sovereign', icon: '👁️', parent: '/essaim' },
  '/admin': { label: 'Admin', icon: '🔧', parent: '/sovereign' },
  '/protocol-999': { label: 'Protocol-999', icon: '🚨', parent: '/sovereign' },
  '/workspace': { label: 'Bureau', icon: '🖥️', parent: '/essaim' },
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function buildBreadcrumbPath(pathname: string): BreadcrumbItem[] {
  const items: BreadcrumbItem[] = [];
  let currentPath = pathname;

  // Handle sphere routes
  if (pathname.startsWith('/sphere/')) {
    const sphereId = pathname.replace('/sphere/', '');
    items.unshift({
      label: sphereId.charAt(0).toUpperCase() + sphereId.slice(1),
      path: pathname,
      icon: '🔮',
    });
    currentPath = '/essaim';
  }

  // Handle workspace routes
  if (pathname.startsWith('/workspace/')) {
    const agentId = pathname.replace('/workspace/', '');
    items.unshift({
      label: `Bureau: ${agentId}`,
      path: pathname,
      icon: '🖥️',
    });
    currentPath = '/essaim';
  }

  // Build path from current to root
  while (currentPath && ROUTE_CONFIG[currentPath]) {
    const config = ROUTE_CONFIG[currentPath];
    items.unshift({
      label: config.label,
      path: currentPath,
      icon: config.icon,
    });
    currentPath = config.parent || '';
  }

  return items;
}

// =============================================================================
// BREADCRUMBS COMPONENT
// =============================================================================

export function Breadcrumbs({ items, showHome = true }: BreadcrumbsProps) {
  const navigate = useNavigate();
  const location = useLocation();

  // Use provided items or auto-generate from current route
  const breadcrumbItems = items || buildBreadcrumbPath(location.pathname);

  // Don't show on root page
  if (location.pathname === '/' && !items) {
    return null;
  }

  return (
    <nav
      aria-label="Fil d'Ariane"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 50,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        backdropFilter: 'blur(8px)',
        borderBottom: `1px solid ${COLORS.border.subtle}`,
        padding: '0 16px',
      }}
    >
      <ol
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          margin: 0,
          padding: 0,
          listStyle: 'none',
          height: TOUCH.minTarget,
          fontFamily: TYPOGRAPHY.fontFamily.mono,
          fontSize: TYPOGRAPHY.fontSize.sm,
          overflow: 'auto',
        }}
      >
        {breadcrumbItems.map((item, index) => {
          const isLast = index === breadcrumbItems.length - 1;
          const isFirst = index === 0;

          return (
            <li
              key={item.path}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
              }}
            >
              {/* Separator */}
              {!isFirst && (
                <span
                  aria-hidden="true"
                  style={{
                    color: COLORS.text.muted,
                    padding: '0 4px',
                  }}
                >
                  /
                </span>
              )}

              {/* Breadcrumb link or current page */}
              {isLast ? (
                <span
                  aria-current="page"
                  style={{
                    color: COLORS.gold,
                    fontWeight: TYPOGRAPHY.fontWeight.bold,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '8px 12px',
                    borderRadius: '4px',
                    backgroundColor: 'rgba(212, 175, 55, 0.1)',
                  }}
                >
                  {item.icon && (
                    <span role="img" aria-hidden="true">
                      {item.icon}
                    </span>
                  )}
                  {item.label}
                </span>
              ) : (
                <button
                  onClick={() => navigate(item.path)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '8px 12px',
                    minHeight: '36px',
                    background: 'transparent',
                    border: 'none',
                    color: COLORS.text.secondary,
                    fontFamily: TYPOGRAPHY.fontFamily.mono,
                    fontSize: TYPOGRAPHY.fontSize.sm,
                    cursor: 'pointer',
                    borderRadius: '4px',
                    transition: 'all 0.15s ease',
                    whiteSpace: 'nowrap',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                    e.currentTarget.style.color = COLORS.text.primary;
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                    e.currentTarget.style.color = COLORS.text.secondary;
                  }}
                >
                  {item.icon && (
                    <span role="img" aria-hidden="true">
                      {item.icon}
                    </span>
                  )}
                  {item.label}
                </button>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export default Breadcrumbs;
