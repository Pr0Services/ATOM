/**
 * A/B TESTING SERVICE - Experimentation Framework
 * ================================================
 *
 * Service pour gérer les tests A/B sur la landing page.
 * Features:
 * - Assignment persistant par utilisateur
 * - Tracking des conversions par variant
 * - Configuration des expériences
 * - Intégration avec analytics
 */

import { analyticsService } from './analytics.service';

// =============================================================================
// TYPES
// =============================================================================

export interface Experiment {
  id: string;
  name: string;
  description: string;
  variants: Variant[];
  status: 'active' | 'paused' | 'completed';
  startDate: string;
  endDate?: string;
}

export interface Variant {
  id: string;
  name: string;
  weight: number; // 0-100, percentage allocation
  config: Record<string, unknown>;
}

export interface Assignment {
  experimentId: string;
  variantId: string;
  assignedAt: string;
}

// =============================================================================
// EXPERIMENTS CONFIGURATION
// =============================================================================

const EXPERIMENTS: Experiment[] = [
  {
    id: 'landing_hero_v1',
    name: 'Landing Hero Test',
    description: 'Test différentes propositions de valeur sur le hero',
    status: 'active',
    startDate: '2026-02-13',
    variants: [
      {
        id: 'control',
        name: 'Control - Original',
        weight: 50,
        config: {
          headline: "L'Intelligence Collective",
          subheadline: 'à Votre Service',
          ctaText: 'ENTRER MAINTENANT',
          ctaColor: '#D4AF37', // gold
        },
      },
      {
        id: 'variant_a',
        name: 'Variant A - Action Focus',
        weight: 50,
        config: {
          headline: '350 Agents IA',
          subheadline: 'Prêts à Travailler Pour Vous',
          ctaText: 'ACTIVER MON ESSAIM',
          ctaColor: '#0047AB', // cobalt
        },
      },
    ],
  },
  {
    id: 'landing_social_proof',
    name: 'Social Proof Test',
    description: 'Test avec ou sans preuve sociale',
    status: 'active',
    startDate: '2026-02-13',
    variants: [
      {
        id: 'control',
        name: 'Sans social proof',
        weight: 50,
        config: {
          showSocialProof: false,
        },
      },
      {
        id: 'variant_a',
        name: 'Avec social proof',
        weight: 50,
        config: {
          showSocialProof: true,
          socialProofText: '+1,200 utilisateurs actifs',
        },
      },
    ],
  },
  {
    id: 'cta_urgency',
    name: 'CTA Urgency Test',
    description: 'Test CTA avec/sans urgence',
    status: 'active',
    startDate: '2026-02-13',
    variants: [
      {
        id: 'control',
        name: 'Sans urgence',
        weight: 50,
        config: {
          showUrgency: false,
          urgencyText: '',
        },
      },
      {
        id: 'variant_a',
        name: 'Avec urgence',
        weight: 50,
        config: {
          showUrgency: true,
          urgencyText: 'Accès limité - Places disponibles',
        },
      },
    ],
  },
];

// =============================================================================
// STORAGE
// =============================================================================

const ASSIGNMENTS_KEY = 'atom_ab_assignments';

function getStoredAssignments(): Assignment[] {
  try {
    const raw = localStorage.getItem(ASSIGNMENTS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function storeAssignments(assignments: Assignment[]): void {
  localStorage.setItem(ASSIGNMENTS_KEY, JSON.stringify(assignments));
}

// =============================================================================
// A/B TESTING SERVICE
// =============================================================================

class ABTestingService {
  private assignments: Assignment[] = [];

  constructor() {
    this.assignments = getStoredAssignments();
  }

  /**
   * Get all active experiments
   */
  getActiveExperiments(): Experiment[] {
    return EXPERIMENTS.filter(exp => exp.status === 'active');
  }

  /**
   * Get variant assignment for an experiment
   * Creates new assignment if none exists
   */
  getVariant(experimentId: string): Variant | null {
    const experiment = EXPERIMENTS.find(exp => exp.id === experimentId);
    if (!experiment || experiment.status !== 'active') {
      return null;
    }

    // Check existing assignment
    let assignment = this.assignments.find(a => a.experimentId === experimentId);

    if (!assignment) {
      // Assign new variant
      const variant = this.assignVariant(experiment);
      assignment = {
        experimentId,
        variantId: variant.id,
        assignedAt: new Date().toISOString(),
      };
      this.assignments.push(assignment);
      storeAssignments(this.assignments);

      // Track assignment
      analyticsService.track('cta_click', {
        cta: 'ab_assignment',
        experimentId,
        variantId: variant.id,
      });
    }

    return experiment.variants.find(v => v.id === assignment!.variantId) || null;
  }

  /**
   * Get config value from variant
   */
  getConfig<T>(experimentId: string, key: string, defaultValue: T): T {
    const variant = this.getVariant(experimentId);
    if (!variant) {
      return defaultValue;
    }
    return (variant.config[key] as T) ?? defaultValue;
  }

  /**
   * Track conversion for current variant
   */
  trackConversion(experimentId: string, conversionType: string, value?: number): void {
    const assignment = this.assignments.find(a => a.experimentId === experimentId);
    if (!assignment) {
      return;
    }

    analyticsService.track('cta_click', {
      cta: 'ab_conversion',
      experimentId,
      variantId: assignment.variantId,
      conversionType,
      value,
    });
  }

  /**
   * Assign variant based on weights
   */
  private assignVariant(experiment: Experiment): Variant {
    const random = Math.random() * 100;
    let cumulative = 0;

    for (const variant of experiment.variants) {
      cumulative += variant.weight;
      if (random <= cumulative) {
        return variant;
      }
    }

    // Fallback to last variant
    return experiment.variants[experiment.variants.length - 1];
  }

  /**
   * Get all current assignments (for debugging)
   */
  getAssignments(): Assignment[] {
    return [...this.assignments];
  }

  /**
   * Reset all assignments (for testing)
   */
  resetAssignments(): void {
    this.assignments = [];
    localStorage.removeItem(ASSIGNMENTS_KEY);
  }

  /**
   * Force specific variant (for testing)
   */
  forceVariant(experimentId: string, variantId: string): void {
    const index = this.assignments.findIndex(a => a.experimentId === experimentId);
    const assignment: Assignment = {
      experimentId,
      variantId,
      assignedAt: new Date().toISOString(),
    };

    if (index >= 0) {
      this.assignments[index] = assignment;
    } else {
      this.assignments.push(assignment);
    }

    storeAssignments(this.assignments);
  }
}

// =============================================================================
// SINGLETON EXPORT
// =============================================================================

export const abTestingService = new ABTestingService();

// Convenience function
export function useABTest(experimentId: string): Variant | null {
  return abTestingService.getVariant(experimentId);
}

export default abTestingService;
