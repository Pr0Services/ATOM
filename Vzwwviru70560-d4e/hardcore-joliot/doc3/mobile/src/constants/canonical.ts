/* ═══════════════════════════════════════════════════════════════════════════════
   CHE·NU™ MOBILE — CANONICAL CONSTANTS v40
   9 SPHÈRES + 6 SECTIONS BUREAU
   ═══════════════════════════════════════════════════════════════════════════════ */

import type { Sphere, BureauSection, SphereId, BureauSectionId } from '../types';

// ════════════════════════════════════════════════════════════════════════════════
// 9 SPHÈRES (FROZEN)
// ════════════════════════════════════════════════════════════════════════════════

export const SPHERES: Sphere[] = [
  {
    id: 'personal',
    name: 'Personal',
    nameFr: 'Personnel',
    nameEs: 'Personal',
    icon: '🏠',
    color: '#D8B26A',
    gradient: ['#D8B26A', '#C9A45B'],
    description: 'Your private life management',
    descriptionFr: 'Gestion de votre vie privée',
    agents: [],
    modules: ['calendar', 'notes', 'health', 'finance'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'business',
    name: 'Business',
    nameFr: 'Affaires',
    nameEs: 'Negocios',
    icon: '💼',
    color: '#8D8371',
    gradient: ['#8D8371', '#7E7462'],
    description: 'Professional and enterprise',
    descriptionFr: 'Professionnel et entreprise',
    agents: [],
    modules: ['hr', 'accounting', 'operations'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'government',
    name: 'Government & Institutions',
    nameFr: 'Gouvernement & Institutions',
    nameEs: 'Gobierno e Instituciones',
    icon: '🏛️',
    color: '#2F4C39',
    gradient: ['#2F4C39', '#203D2A'],
    description: 'Administrative and legal affairs',
    descriptionFr: 'Affaires administratives et légales',
    agents: [],
    modules: ['legal', 'taxes', 'permits'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'creative',
    name: 'Creative Studio',
    nameFr: 'Studio de création',
    nameEs: 'Estudio Creativo',
    icon: '🎨',
    color: '#7A593A',
    gradient: ['#7A593A', '#6B4A2B'],
    description: 'Creative projects and design',
    descriptionFr: 'Projets créatifs et design',
    agents: [],
    modules: ['design', 'art', 'music', 'video'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'community',
    name: 'Community',
    nameFr: 'Communauté',
    nameEs: 'Comunidad',
    icon: '👥',
    color: '#3F7249',
    gradient: ['#3F7249', '#30633A'],
    description: 'Groups and associations',
    descriptionFr: 'Groupes et associations',
    agents: [],
    modules: ['groups', 'events', 'volunteer'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'social',
    name: 'Social & Media',
    nameFr: 'Social & Médias',
    nameEs: 'Social y Medios',
    icon: '📱',
    color: '#3EB4A2',
    gradient: ['#3EB4A2', '#2FA593'],
    description: 'Social networks and communications',
    descriptionFr: 'Réseaux sociaux et communications',
    agents: [],
    modules: ['social', 'messaging', 'content'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'entertainment',
    name: 'Entertainment',
    nameFr: 'Divertissement',
    nameEs: 'Entretenimiento',
    icon: '🎬',
    color: '#E9E4D6',
    gradient: ['#E9E4D6', '#DAD5C7'],
    description: 'Leisure and entertainment',
    descriptionFr: 'Loisirs et divertissement',
    agents: [],
    modules: ['streaming', 'gaming', 'sports'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'team',
    name: 'My Team',
    nameFr: 'Mon Équipe',
    nameEs: 'Mi Equipo',
    icon: '🤝',
    color: '#1E1F22',
    gradient: ['#1E1F22', '#0F1013'],
    description: 'AI agents and skills management',
    descriptionFr: 'Gestion des agents IA et compétences',
    agents: [],
    modules: ['agents', 'skills', 'tools', 'labs'],
    isActive: true,
    isUnlocked: true,
  },
  {
    id: 'scholar',
    name: 'Scholar',
    nameFr: 'Académique',
    nameEs: 'Académico',
    icon: '📚',
    color: '#E0C46B',
    gradient: ['#E0C46B', '#D1B55C'],
    description: 'Learning, research, and academic pursuits',
    descriptionFr: 'Apprentissage, recherche et parcours académique',
    agents: [],
    modules: ['research', 'courses', 'library', 'citations'],
    isActive: true,
    isUnlocked: true,
  },
];

// ════════════════════════════════════════════════════════════════════════════════
// 6 SECTIONS BUREAU FLEXIBLES (FROZEN)
// ════════════════════════════════════════════════════════════════════════════════

export const BUREAU_SECTIONS: BureauSection[] = [
  {
    id: 'quick_capture',
    name: 'Quick Capture',
    nameFr: 'Capture rapide',
    icon: '📝',
    hierarchyLevel: 1,
    maxItems: 5,
  },
  {
    id: 'resume_workspace',
    name: 'Resume Work',
    nameFr: 'Reprendre',
    icon: '▶️',
    hierarchyLevel: 2,
    maxItems: 8,
  },
  {
    id: 'threads',
    name: 'Threads',
    nameFr: 'Fils',
    icon: '💬',
    hierarchyLevel: 3,
  },
  {
    id: 'data_files',
    name: 'Data & Files',
    nameFr: 'Données & Fichiers',
    icon: '📁',
    hierarchyLevel: 4,
  },
  {
    id: 'active_agents',
    name: 'Active Agents',
    nameFr: 'Agents actifs',
    icon: '🤖',
    hierarchyLevel: 5,
  },
  {
    id: 'meetings',
    name: 'Meetings',
    nameFr: 'Réunions',
    icon: '📅',
    hierarchyLevel: 6,
  },
];

// ════════════════════════════════════════════════════════════════════════════════
// HELPERS
// ════════════════════════════════════════════════════════════════════════════════

export const getSphereById = (id: SphereId): Sphere | undefined =>
  SPHERES.find((s) => s.id === id);

export const getSectionById = (id: BureauSectionId): BureauSection | undefined =>
  BUREAU_SECTIONS.find((s) => s.id === id);

export const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
  scholarGold: '#E0C46B',
  background: '#0c0a09',
};

export default { SPHERES, BUREAU_SECTIONS, COLORS };
