/**
 * CONTEXTUAL GLOSSARY - Smart Terminology Helper
 * ==============================================
 *
 * Glossaire intelligent qui:
 * - Détecte les termes techniques dans le contexte actuel
 * - Affiche des définitions au survol/clic
 * - S'adapte au mode linguistique (Symbolique/Clair)
 * - Propose des liens vers la documentation
 *
 * Objectif: Réduire la barrière cognitive pour les nouveaux utilisateurs
 */

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { useAtomStore } from '@/stores/atom.store';
import { COLORS, TYPOGRAPHY } from '@/styles/tokens';

// =============================================================================
// TYPES
// =============================================================================

interface GlossaryTerm {
  id: string;
  termSymbolique: string;
  termClair: string;
  definitionSimple: string;
  definitionDetailed: string;
  category: 'concept' | 'navigation' | 'action' | 'system';
  relatedTerms?: string[];
  learnMoreUrl?: string;
}

interface TooltipPosition {
  x: number;
  y: number;
  placement: 'top' | 'bottom';
}

// =============================================================================
// GLOSSARY DATA
// =============================================================================

const GLOSSARY_TERMS: GlossaryTerm[] = [
  // Navigation terms
  {
    id: 'essaim',
    termSymbolique: "L'Essaim",
    termClair: 'Agents IA',
    definitionSimple: 'Collection de 350+ assistants IA spécialisés',
    definitionDetailed: "L'Essaim représente l'ensemble des agents IA disponibles sur AT·OM. Chaque agent est spécialisé dans un domaine et peut vous assister dans vos tâches quotidiennes.",
    category: 'navigation',
    relatedTerms: ['agent', 'sphere'],
  },
  {
    id: 'sceau',
    termSymbolique: 'Le Sceau',
    termClair: 'Accueil',
    definitionSimple: 'Page principale de la plateforme',
    definitionDetailed: 'Le Sceau est votre point de départ, le centre de votre expérience AT·OM. Il vous donne une vue d\'ensemble et un accès rapide à toutes les fonctionnalités.',
    category: 'navigation',
  },
  {
    id: 'nexus',
    termSymbolique: 'Le Nexus',
    termClair: 'Tableau de bord',
    definitionSimple: 'Vue d\'ensemble de vos activités et métriques',
    definitionDetailed: 'Le Nexus centralise toutes vos informations importantes : statistiques, tâches en cours, notifications et recommandations personnalisées.',
    category: 'navigation',
    relatedTerms: ['arithmos'],
  },

  // Concept terms
  {
    id: 'sphere',
    termSymbolique: 'Sphère',
    termClair: 'Domaine',
    definitionSimple: 'Catégorie thématique regroupant des agents similaires',
    definitionDetailed: 'AT·OM organise ses agents en 9 sphères thématiques : Santé, Finance, Éducation, Gouvernance, Énergie, Communication, Justice, Logistique et Alimentation.',
    category: 'concept',
    relatedTerms: ['essaim', 'agent'],
  },
  {
    id: 'agent',
    termSymbolique: 'Agent',
    termClair: 'Assistant IA',
    definitionSimple: 'Intelligence artificielle spécialisée pour une tâche',
    definitionDetailed: 'Un agent AT·OM est une IA entraînée pour exceller dans un domaine précis. Il peut répondre à vos questions, effectuer des recherches, et vous guider dans vos décisions.',
    category: 'concept',
    relatedTerms: ['essaim', 'sphere'],
  },
  {
    id: 'arithmos',
    termSymbolique: 'Arithmos',
    termClair: 'Métriques',
    definitionSimple: 'Système de mesure et d\'équilibre',
    definitionDetailed: 'L\'Arithmos est le système de métriques d\'AT·OM qui calcule votre indice harmonique, mesurant l\'équilibre entre vos différentes sphères d\'activité.',
    category: 'concept',
    relatedTerms: ['nexus', 'sphere'],
  },
  {
    id: 'heartbeat',
    termSymbolique: 'Heartbeat',
    termClair: 'Synchronisation',
    definitionSimple: 'Battement de cœur du système',
    definitionDetailed: 'Le Heartbeat est le rythme de synchronisation d\'AT·OM. Il vérifie régulièrement l\'état des services et maintient vos données à jour.',
    category: 'system',
  },

  // Action terms
  {
    id: 'workspace',
    termSymbolique: 'Espace de Travail',
    termClair: 'Équipe d\'agents',
    definitionSimple: 'Configuration personnalisée d\'agents collaborant ensemble',
    definitionDetailed: 'Un Espace de Travail vous permet d\'assembler plusieurs agents pour travailler ensemble sur un projet ou objectif commun.',
    category: 'action',
    relatedTerms: ['agent', 'essaim'],
  },
  {
    id: 'sovereignty',
    termSymbolique: 'Souveraineté',
    termClair: 'Contrôle des données',
    definitionSimple: 'Votre contrôle total sur vos données personnelles',
    definitionDetailed: 'La souveraineté AT·OM signifie que vous gardez le contrôle complet de vos données. Vous pouvez les exporter, les supprimer, et choisir ce qui est partagé.',
    category: 'concept',
  },
  {
    id: 'identity',
    termSymbolique: 'Identité Souveraine',
    termClair: 'Profil sécurisé',
    definitionSimple: 'Votre identité numérique protégée',
    definitionDetailed: 'Votre Identité Souveraine est votre profil sur AT·OM, protégé par un chiffrement fort. Elle vous authentifie sans dépendre de tiers.',
    category: 'system',
    relatedTerms: ['sovereignty'],
  },

  // System terms
  {
    id: 'offline',
    termSymbolique: 'Mode Hors-ligne',
    termClair: 'Sans connexion',
    definitionSimple: 'Fonctionnement sans Internet',
    definitionDetailed: 'AT·OM fonctionne même sans connexion Internet. Vos données sont stockées localement et synchronisées automatiquement au retour de la connexion.',
    category: 'system',
    relatedTerms: ['heartbeat'],
  },
  {
    id: 'simulation',
    termSymbolique: 'Mode Simulation',
    termClair: 'Mode Test',
    definitionSimple: 'Fonctionnement avec données simulées',
    definitionDetailed: 'En mode simulation, AT·OM utilise des données fictives pour vous permettre d\'explorer sans risque. Les actions ne sont pas persistées.',
    category: 'system',
  },
];

// =============================================================================
// CONTEXT-AWARE TERM DETECTION
// =============================================================================

const ROUTE_RELEVANT_TERMS: Record<string, string[]> = {
  '/': ['sceau', 'essaim', 'sphere', 'agent'],
  '/essaim': ['essaim', 'agent', 'sphere', 'workspace'],
  '/dashboard': ['nexus', 'arithmos', 'sphere', 'heartbeat'],
  '/sphere': ['sphere', 'agent', 'essaim'],
  '/settings': ['sovereignty', 'identity', 'offline'],
  '/register': ['sovereignty', 'identity', 'agent'],
};

// =============================================================================
// GLOSSARY TOOLTIP COMPONENT
// =============================================================================

interface GlossaryTooltipProps {
  term: GlossaryTerm;
  position: TooltipPosition;
  language: 'symbolique' | 'clair';
  onClose: () => void;
  onRelatedClick: (termId: string) => void;
}

function GlossaryTooltip({
  term,
  position,
  language,
  onClose,
  onRelatedClick,
}: GlossaryTooltipProps) {
  const [showDetailed, setShowDetailed] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (tooltipRef.current && !tooltipRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [onClose]);

  const displayTerm = language === 'symbolique' ? term.termSymbolique : term.termClair;
  const alternateTerm = language === 'symbolique' ? term.termClair : term.termSymbolique;

  return (
    <div
      ref={tooltipRef}
      style={{
        position: 'fixed',
        left: Math.min(position.x, window.innerWidth - 320),
        [position.placement === 'top' ? 'bottom' : 'top']:
          position.placement === 'top'
            ? window.innerHeight - position.y + 10
            : position.y + 10,
        width: '300px',
        backgroundColor: 'rgba(0, 0, 0, 0.95)',
        border: '1px solid rgba(255, 255, 255, 0.15)',
        borderRadius: '12px',
        overflow: 'hidden',
        zIndex: 10000,
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
        fontFamily: TYPOGRAPHY.fontFamily.system,
      }}
      role="tooltip"
    >
      {/* Header */}
      <div
        style={{
          padding: '12px 16px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
        }}
      >
        <div>
          <div style={{ color: COLORS.gold, fontSize: '14px', fontWeight: 600 }}>
            {displayTerm}
          </div>
          <div style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '11px', marginTop: '2px' }}>
            {alternateTerm}
          </div>
        </div>
        <button
          onClick={onClose}
          style={{
            padding: '4px',
            backgroundColor: 'transparent',
            border: 'none',
            color: 'rgba(255, 255, 255, 0.4)',
            cursor: 'pointer',
            fontSize: '16px',
            lineHeight: 1,
          }}
          aria-label="Fermer"
        >
          ×
        </button>
      </div>

      {/* Definition */}
      <div style={{ padding: '12px 16px' }}>
        <p style={{ color: '#fff', fontSize: '13px', lineHeight: 1.5, margin: 0 }}>
          {showDetailed ? term.definitionDetailed : term.definitionSimple}
        </p>

        {!showDetailed && term.definitionDetailed !== term.definitionSimple && (
          <button
            onClick={() => setShowDetailed(true)}
            style={{
              marginTop: '8px',
              padding: 0,
              backgroundColor: 'transparent',
              border: 'none',
              color: COLORS.gold,
              fontSize: '12px',
              cursor: 'pointer',
              textDecoration: 'underline',
            }}
          >
            En savoir plus
          </button>
        )}
      </div>

      {/* Related terms */}
      {term.relatedTerms && term.relatedTerms.length > 0 && (
        <div
          style={{
            padding: '10px 16px',
            borderTop: '1px solid rgba(255, 255, 255, 0.05)',
          }}
        >
          <div
            style={{
              color: 'rgba(255, 255, 255, 0.4)',
              fontSize: '10px',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              marginBottom: '6px',
            }}
          >
            Termes liés
          </div>
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            {term.relatedTerms.map((relatedId) => {
              const relatedTerm = GLOSSARY_TERMS.find((t) => t.id === relatedId);
              if (!relatedTerm) return null;
              return (
                <button
                  key={relatedId}
                  onClick={() => onRelatedClick(relatedId)}
                  style={{
                    padding: '4px 10px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '12px',
                    color: 'rgba(255, 255, 255, 0.7)',
                    fontSize: '11px',
                    cursor: 'pointer',
                  }}
                >
                  {language === 'symbolique'
                    ? relatedTerm.termSymbolique
                    : relatedTerm.termClair}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Category badge */}
      <div
        style={{
          padding: '8px 16px',
          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span
          style={{
            padding: '2px 8px',
            backgroundColor: getCategoryColor(term.category),
            borderRadius: '4px',
            color: '#fff',
            fontSize: '10px',
            textTransform: 'uppercase',
          }}
        >
          {getCategoryLabel(term.category)}
        </span>
        {term.learnMoreUrl && (
          <a
            href={term.learnMoreUrl}
            style={{
              color: COLORS.gold,
              fontSize: '11px',
              textDecoration: 'none',
            }}
          >
            Documentation →
          </a>
        )}
      </div>
    </div>
  );
}

function getCategoryColor(category: GlossaryTerm['category']): string {
  const colors: Record<GlossaryTerm['category'], string> = {
    concept: 'rgba(139, 92, 246, 0.4)',
    navigation: 'rgba(59, 130, 246, 0.4)',
    action: 'rgba(34, 197, 94, 0.4)',
    system: 'rgba(249, 115, 22, 0.4)',
  };
  return colors[category];
}

function getCategoryLabel(category: GlossaryTerm['category']): string {
  const labels: Record<GlossaryTerm['category'], string> = {
    concept: 'Concept',
    navigation: 'Navigation',
    action: 'Action',
    system: 'Système',
  };
  return labels[category];
}

// =============================================================================
// GLOSSARY PANEL COMPONENT
// =============================================================================

interface GlossaryPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function GlossaryPanel({ isOpen, onClose }: GlossaryPanelProps) {
  const location = useLocation();
  const language = useAtomStore((state) => state.ui.language);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<GlossaryTerm['category'] | 'all'>('all');
  const [selectedTerm, setSelectedTerm] = useState<GlossaryTerm | null>(null);

  const contextTermIds = useMemo(() => {
    const path = location.pathname.split('/').slice(0, 2).join('/');
    return ROUTE_RELEVANT_TERMS[path] || ROUTE_RELEVANT_TERMS['/'];
  }, [location.pathname]);

  const filteredTerms = useMemo(() => {
    let terms = GLOSSARY_TERMS;

    if (selectedCategory !== 'all') {
      terms = terms.filter((t) => t.category === selectedCategory);
    }

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      terms = terms.filter(
        (t) =>
          t.termSymbolique.toLowerCase().includes(query) ||
          t.termClair.toLowerCase().includes(query) ||
          t.definitionSimple.toLowerCase().includes(query)
      );
    }

    // Sort: context-relevant first
    return terms.sort((a, b) => {
      const aRelevant = contextTermIds.includes(a.id);
      const bRelevant = contextTermIds.includes(b.id);
      if (aRelevant && !bRelevant) return -1;
      if (!aRelevant && bRelevant) return 1;
      return 0;
    });
  }, [searchQuery, selectedCategory, contextTermIds]);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        right: 0,
        bottom: 0,
        width: '360px',
        backgroundColor: 'rgba(0, 0, 0, 0.95)',
        borderLeft: '1px solid rgba(255, 255, 255, 0.1)',
        zIndex: 950,
        display: 'flex',
        flexDirection: 'column',
        fontFamily: TYPOGRAPHY.fontFamily.system,
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: '16px 20px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '20px' }}>📖</span>
          <span
            style={{
              color: COLORS.gold,
              fontSize: '12px',
              fontFamily: TYPOGRAPHY.fontFamily.mono,
              letterSpacing: '0.1em',
            }}
          >
            GLOSSAIRE
          </span>
        </div>
        <button
          onClick={onClose}
          style={{
            padding: '6px 12px',
            backgroundColor: 'transparent',
            border: 'none',
            color: 'rgba(255, 255, 255, 0.4)',
            cursor: 'pointer',
            fontSize: '12px',
          }}
        >
          Fermer
        </button>
      </div>

      {/* Search */}
      <div style={{ padding: '12px 20px' }}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Rechercher un terme..."
          style={{
            width: '100%',
            padding: '10px 14px',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '8px',
            color: '#fff',
            fontSize: '14px',
            outline: 'none',
          }}
        />
      </div>

      {/* Category filters */}
      <div
        style={{
          padding: '0 20px 12px',
          display: 'flex',
          gap: '6px',
          flexWrap: 'wrap',
        }}
      >
        {(['all', 'concept', 'navigation', 'action', 'system'] as const).map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{
              padding: '4px 10px',
              backgroundColor:
                selectedCategory === cat
                  ? 'rgba(255, 255, 255, 0.15)'
                  : 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '12px',
              color: selectedCategory === cat ? '#fff' : 'rgba(255, 255, 255, 0.6)',
              fontSize: '11px',
              cursor: 'pointer',
            }}
          >
            {cat === 'all' ? 'Tous' : getCategoryLabel(cat)}
          </button>
        ))}
      </div>

      {/* Context hint */}
      <div
        style={{
          padding: '8px 20px',
          backgroundColor: 'rgba(255, 215, 0, 0.05)',
          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
        }}
      >
        <span style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '11px' }}>
          💡 Termes pertinents pour cette page affichés en premier
        </span>
      </div>

      {/* Terms list */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '12px 20px' }}>
        {filteredTerms.map((term) => {
          const isContextRelevant = contextTermIds.includes(term.id);
          const displayTerm = language === 'symbolique' ? term.termSymbolique : term.termClair;
          const alternateTerm = language === 'symbolique' ? term.termClair : term.termSymbolique;

          return (
            <button
              key={term.id}
              onClick={() => setSelectedTerm(selectedTerm?.id === term.id ? null : term)}
              style={{
                width: '100%',
                padding: '12px',
                marginBottom: '8px',
                backgroundColor:
                  selectedTerm?.id === term.id
                    ? 'rgba(255, 255, 255, 0.1)'
                    : 'rgba(255, 255, 255, 0.02)',
                border: isContextRelevant
                  ? `1px solid ${COLORS.gold}30`
                  : '1px solid rgba(255, 255, 255, 0.05)',
                borderRadius: '8px',
                cursor: 'pointer',
                textAlign: 'left',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ color: '#fff', fontSize: '14px', fontWeight: 500 }}>
                  {displayTerm}
                </div>
                {isContextRelevant && (
                  <span style={{ color: COLORS.gold, fontSize: '10px' }}>Pertinent</span>
                )}
              </div>
              <div style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '11px', marginTop: '2px' }}>
                {alternateTerm}
              </div>
              {selectedTerm?.id === term.id && (
                <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
                  <p style={{ color: 'rgba(255, 255, 255, 0.8)', fontSize: '13px', lineHeight: 1.5, margin: 0 }}>
                    {term.definitionDetailed}
                  </p>
                  {term.relatedTerms && (
                    <div style={{ marginTop: '8px', display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                      {term.relatedTerms.map((relatedId) => {
                        const related = GLOSSARY_TERMS.find((t) => t.id === relatedId);
                        return related ? (
                          <span
                            key={relatedId}
                            style={{
                              padding: '2px 6px',
                              backgroundColor: 'rgba(255, 255, 255, 0.1)',
                              borderRadius: '4px',
                              color: 'rgba(255, 255, 255, 0.6)',
                              fontSize: '10px',
                            }}
                          >
                            {language === 'symbolique' ? related.termSymbolique : related.termClair}
                          </span>
                        ) : null;
                      })}
                    </div>
                  )}
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Footer */}
      <div
        style={{
          padding: '12px 20px',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          textAlign: 'center',
        }}
      >
        <span style={{ color: 'rgba(255, 255, 255, 0.3)', fontSize: '11px' }}>
          {filteredTerms.length} termes • Mode {language === 'symbolique' ? 'Symbolique' : 'Clair'}
        </span>
      </div>
    </div>
  );
}

// =============================================================================
// GLOSSARY TRIGGER BUTTON
// =============================================================================

interface GlossaryTriggerProps {
  position?: 'bottom-left' | 'bottom-right';
}

export function GlossaryTrigger({ position = 'bottom-left' }: GlossaryTriggerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const experienceMode = useAtomStore((state) => state.ui.experienceMode);

  // Only show for beginners by default
  if (experienceMode === 'expert' && !isOpen) {
    return null;
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed',
          bottom: '100px',
          [position.includes('right') ? 'right' : 'left']: '20px',
          padding: '12px 16px',
          backgroundColor: 'rgba(0, 0, 0, 0.9)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '24px',
          color: '#fff',
          fontSize: '14px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          zIndex: 900,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
        }}
        title="Ouvrir le glossaire"
      >
        <span>📖</span>
        <span style={{ color: 'rgba(255, 255, 255, 0.7)' }}>Glossaire</span>
      </button>

      <GlossaryPanel isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
}

// =============================================================================
// INLINE TERM HIGHLIGHT (for use in text)
// =============================================================================

interface HighlightedTermProps {
  termId: string;
  children?: React.ReactNode;
}

export function HighlightedTerm({ termId, children }: HighlightedTermProps) {
  const language = useAtomStore((state) => state.ui.language);
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState<TooltipPosition>({
    x: 0,
    y: 0,
    placement: 'bottom',
  });
  const elementRef = useRef<HTMLSpanElement>(null);

  const term = useMemo(() => GLOSSARY_TERMS.find((t) => t.id === termId), [termId]);

  const handleClick = useCallback(() => {
    if (elementRef.current) {
      const rect = elementRef.current.getBoundingClientRect();
      const spaceBelow = window.innerHeight - rect.bottom;
      const placement = spaceBelow > 200 ? 'bottom' : 'top';

      setTooltipPosition({
        x: rect.left,
        y: placement === 'bottom' ? rect.bottom : rect.top,
        placement,
      });
      setShowTooltip(true);
    }
  }, []);

  if (!term) {
    return <span>{children}</span>;
  }

  const displayTerm = children || (language === 'symbolique' ? term.termSymbolique : term.termClair);

  return (
    <>
      <span
        ref={elementRef}
        onClick={handleClick}
        style={{
          color: COLORS.gold,
          borderBottom: '1px dotted currentColor',
          cursor: 'help',
        }}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && handleClick()}
      >
        {displayTerm}
      </span>

      {showTooltip && (
        <GlossaryTooltip
          term={term}
          position={tooltipPosition}
          language={language}
          onClose={() => setShowTooltip(false)}
          onRelatedClick={(relatedId) => {
            const relatedTerm = GLOSSARY_TERMS.find((t) => t.id === relatedId);
            if (relatedTerm) {
              // Keep position, just update term shown
              setShowTooltip(false);
              setTimeout(() => {
                setShowTooltip(true);
              }, 100);
            }
          }}
        />
      )}
    </>
  );
}

// =============================================================================
// EXPORTS
// =============================================================================

export { GLOSSARY_TERMS };
export default GlossaryPanel;
