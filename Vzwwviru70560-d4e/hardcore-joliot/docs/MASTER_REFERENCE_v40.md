# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU™ MASTER REFERENCE v40
# ═══════════════════════════════════════════════════════════════════════════════
# SINGLE SOURCE OF TRUTH FOR ALL DEVELOPMENT
# ═══════════════════════════════════════════════════════════════════════════════

## 🔒 FROZEN CONSTANTS

```typescript
// ═══════════════════════════════════════════════════════════════════════════════
// THESE VALUES ARE FROZEN AND MUST NOT BE CHANGED
// ═══════════════════════════════════════════════════════════════════════════════

export const CHENU_VERSION = '40.0.0';
export const SPHERE_COUNT = 9;
export const BUREAU_SECTION_COUNT = 6;
export const GOVERNANCE_LAW_COUNT = 10;
export const AGENT_LEVEL_COUNT = 4;
export const TOTAL_AGENT_COUNT = 226;
```

---

## 📦 SPHERE DEFINITIONS

### Complete Sphere Array

```typescript
export const SPHERES = [
  {
    id: 'personal',
    name: 'Personal',
    icon: '🏠',
    color: '#76E6C7',
    order: 1,
    description: 'Health, finances, family, home management',
    agentCount: 25,
  },
  {
    id: 'business',
    name: 'Business',
    icon: '💼',
    color: '#5BA9FF',
    order: 2,
    description: 'Work, clients, projects, invoicing',
    agentCount: 32,
  },
  {
    id: 'government',
    name: 'Government & Institutions',
    icon: '🏛️',
    color: '#D08FFF',
    order: 3,
    description: 'Legal, taxes, permits, compliance',
    agentCount: 20,
  },
  {
    id: 'creative',
    name: 'Studio de Création',
    icon: '🎨',
    color: '#FF8BAA',
    order: 4,
    description: 'Design, writing, music, art',
    agentCount: 27,
  },
  {
    id: 'community',
    name: 'Community',
    icon: '👥',
    color: '#22C55E',
    order: 5,
    description: 'Local groups, events, volunteering',
    agentCount: 18,
  },
  {
    id: 'social',
    name: 'Social & Media',
    icon: '📱',
    color: '#66D06F',
    order: 6,
    description: 'Social networks, messaging, contacts',
    agentCount: 23,
  },
  {
    id: 'entertainment',
    name: 'Entertainment',
    icon: '🎬',
    color: '#FFB04D',
    order: 7,
    description: 'Media, streaming, gaming',
    agentCount: 20,
  },
  {
    id: 'team',
    name: 'My Team',
    icon: '🤝',
    color: '#5ED8FF',
    order: 8,
    description: 'Collaboration, IA Labs, Skills & Tools',
    agentCount: 34,
  },
  {
    id: 'scholar',
    name: 'Scholar',
    icon: '📚',
    color: '#9B59B6',
    order: 9,
    description: 'Learning, research, knowledge management',
    agentCount: 25,
  },
] as const;

export type SphereId = typeof SPHERES[number]['id'];
```

### Sphere ID Enum

```typescript
export enum SphereIds {
  PERSONAL = 'personal',
  BUSINESS = 'business',
  GOVERNMENT = 'government',
  CREATIVE = 'creative',
  COMMUNITY = 'community',
  SOCIAL = 'social',
  ENTERTAINMENT = 'entertainment',
  TEAM = 'team',
  SCHOLAR = 'scholar',
}
```

---

## 📁 BUREAU SECTION DEFINITIONS

### Complete Bureau Array

```typescript
export const BUREAU_SECTIONS = [
  {
    id: 'quick_capture',
    key: 'QUICK_CAPTURE',
    name: 'Quick Capture',
    icon: '⚡',
    hierarchy: 1,
    description: 'Inbox, quick notes, rapid entry',
  },
  {
    id: 'resume_workspace',
    key: 'RESUME_WORKSPACE',
    name: 'Resume Workspace',
    icon: '▶️',
    hierarchy: 2,
    description: 'Continue work, active projects, tasks',
  },
  {
    id: 'threads',
    key: 'THREADS',
    name: 'Threads',
    icon: '💬',
    hierarchy: 3,
    description: '.chenu conversations, history',
  },
  {
    id: 'data_files',
    key: 'DATA_FILES',
    name: 'Data & Files',
    icon: '📁',
    hierarchy: 4,
    description: 'Files, documents, DataSpaces',
  },
  {
    id: 'active_agents',
    key: 'ACTIVE_AGENTS',
    name: 'Active Agents',
    icon: '🤖',
    hierarchy: 5,
    description: 'Running agents, delegations',
  },
  {
    id: 'meetings',
    key: 'MEETINGS',
    name: 'Meetings',
    icon: '📅',
    hierarchy: 6,
    description: 'Calendar, scheduled meetings',
  },
] as const;

export type BureauSectionId = typeof BUREAU_SECTIONS[number]['id'];
export type BureauSectionKey = typeof BUREAU_SECTIONS[number]['key'];
```

### Bureau Section Keys Enum

```typescript
export enum BureauSectionKeys {
  QUICK_CAPTURE = 'QUICK_CAPTURE',
  RESUME_WORKSPACE = 'RESUME_WORKSPACE',
  THREADS = 'THREADS',
  DATA_FILES = 'DATA_FILES',
  ACTIVE_AGENTS = 'ACTIVE_AGENTS',
  MEETINGS = 'MEETINGS',
}
```

---

## ⚖️ GOVERNANCE LAW DEFINITIONS

### Complete Governance Array

```typescript
export const GOVERNANCE_LAWS = [
  {
    id: 'L1',
    code: 'CONSENT_PRIMACY',
    name: 'Consent Primacy',
    description: 'No action without explicit user consent',
    enforcement: 'hard',
  },
  {
    id: 'L2',
    code: 'TEMPORAL_SOVEREIGNTY',
    name: 'Temporal Sovereignty',
    description: 'User controls their time and attention',
    enforcement: 'hard',
  },
  {
    id: 'L3',
    code: 'CONTEXTUAL_FIDELITY',
    name: 'Contextual Fidelity',
    description: 'Actions respect sphere context',
    enforcement: 'hard',
  },
  {
    id: 'L4',
    code: 'HIERARCHICAL_RESPECT',
    name: 'Hierarchical Respect',
    description: 'Agents respect their level (L0-L3)',
    enforcement: 'hard',
  },
  {
    id: 'L5',
    code: 'AUDIT_COMPLETENESS',
    name: 'Audit Completeness',
    description: 'All actions are logged immutably',
    enforcement: 'hard',
  },
  {
    id: 'L6',
    code: 'ENCODING_TRANSPARENCY',
    name: 'Encoding Transparency',
    description: 'Semantic encoding is visible and verifiable',
    enforcement: 'soft',
  },
  {
    id: 'L7',
    code: 'AGENT_NON_AUTONOMY',
    name: 'Agent Non-Autonomy',
    description: 'Agents do not act without approval',
    enforcement: 'hard',
  },
  {
    id: 'L8',
    code: 'BUDGET_ACCOUNTABILITY',
    name: 'Budget Accountability',
    description: 'Token costs are transparent and controlled',
    enforcement: 'hard',
  },
  {
    id: 'L9',
    code: 'CROSS_SPHERE_ISOLATION',
    name: 'Cross-Sphere Isolation',
    description: 'Data stays within sphere boundaries',
    enforcement: 'hard',
  },
  {
    id: 'L10',
    code: 'DELETION_COMPLETENESS',
    name: 'Deletion Completeness',
    description: 'Deletions are total and verified',
    enforcement: 'hard',
  },
] as const;

export type GovernanceLawId = typeof GOVERNANCE_LAWS[number]['id'];
export type GovernanceLawCode = typeof GOVERNANCE_LAWS[number]['code'];
```

---

## 🤖 AGENT DEFINITIONS

### Agent Levels

```typescript
export const AGENT_LEVELS = [
  {
    level: 'L0',
    name: 'System Intelligence',
    count: 1,
    description: 'Nova only - system-level intelligence',
    permissions: 'all',
  },
  {
    level: 'L1',
    name: 'Orchestrator',
    count: 1,
    description: 'User Orchestrator - coordinates agents',
    permissions: 'elevated',
  },
  {
    level: 'L2',
    name: 'Specialists',
    count: 25,
    description: 'Domain experts per sphere',
    permissions: 'domain',
  },
  {
    level: 'L3',
    name: 'Workers',
    count: 199,
    description: 'Task executors',
    permissions: 'task',
  },
] as const;

export type AgentLevel = typeof AGENT_LEVELS[number]['level'];
```

### Nova Configuration

```typescript
export const NOVA_CONFIG = {
  id: 'nova',
  name: 'Nova',
  level: 'L0' as AgentLevel,
  sphere_id: 'system',
  
  // Absolute rules
  is_system: true,
  is_hired: false,       // NEVER hired
  is_always_present: true,
  is_disabled: false,    // CANNOT be disabled
  
  capabilities: [
    'guidance',
    'memory',
    'governance',
    'supervision',
    'database_management',
    'thread_management',
    'agent_orchestration',
    'encoding_validation',
    'budget_management',
  ],
  
  permissions: ['*'],
  token_cost: 0,
};
```

### Agent Count Summary

```typescript
export const AGENT_COUNTS = {
  // By level
  L0_system: 1,
  L1_orchestrator: 1,
  L2_specialists: 25,
  L3_workers: 199,
  
  // By sphere
  personal: 25,
  business: 32,
  government: 20,
  creative: 27,
  community: 18,
  social: 23,
  entertainment: 20,
  team: 34,
  scholar: 25,
  system: 2,
  
  // Total
  TOTAL: 226,
};
```

---

## 🔄 EXECUTION PIPELINE

### Pipeline Steps

```typescript
export const EXECUTION_PIPELINE_STEPS = [
  { step: 1, name: 'INTENT_CAPTURE', required: true },
  { step: 2, name: 'SEMANTIC_ENCODING', required: true },
  { step: 3, name: 'ENCODING_VALIDATION', required: true },
  { step: 4, name: 'TOKEN_ESTIMATION', required: true },
  { step: 5, name: 'SCOPE_LOCKING', required: true },
  { step: 6, name: 'BUDGET_VERIFICATION', required: true },
  { step: 7, name: 'AGENT_COMPATIBILITY', required: true },
  { step: 8, name: 'HUMAN_APPROVAL', required: true },
  { step: 9, name: 'EXECUTION', required: true },
  { step: 10, name: 'AUDIT_LOGGING', required: true },
] as const;

export const PIPELINE_STEP_COUNT = 10;
```

---

## 🎨 DESIGN TOKENS

### Brand Colors

```typescript
export const BRAND_COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};
```

### Sphere Colors

```typescript
export const SPHERE_COLORS = {
  personal: '#76E6C7',
  business: '#5BA9FF',
  government: '#D08FFF',
  creative: '#FF8BAA',
  community: '#22C55E',
  social: '#66D06F',
  entertainment: '#FFB04D',
  team: '#5ED8FF',
  scholar: '#9B59B6',
};
```

---

## 💰 TOKEN DEFAULTS

```typescript
export const TOKEN_DEFAULTS = {
  // Thread budgets
  thread_standard: 10000,
  thread_complex: 25000,
  thread_minimal: 5000,
  
  // Meeting budgets
  meeting_standard: 25000,
  meeting_extended: 50000,
  
  // Agent costs
  agent_activation: 1000,
  agent_per_message: 100,
  
  // User allocations
  user_monthly_free: 50000,
  user_monthly_pro: 200000,
  user_monthly_enterprise: 1000000,
};
```

---

## 📊 VALIDATION FUNCTIONS

```typescript
export function validateSphereId(id: string): id is SphereId {
  return SPHERES.some(s => s.id === id);
}

export function validateBureauSectionId(id: string): id is BureauSectionId {
  return BUREAU_SECTIONS.some(s => s.id === id);
}

export function validateAgentLevel(level: string): level is AgentLevel {
  return AGENT_LEVELS.some(l => l.level === level);
}

export function validateGovernanceLaw(code: string): code is GovernanceLawCode {
  return GOVERNANCE_LAWS.some(l => l.code === code);
}

export function getSphereById(id: SphereId) {
  return SPHERES.find(s => s.id === id);
}

export function getBureauSectionById(id: BureauSectionId) {
  return BUREAU_SECTIONS.find(s => s.id === id);
}

export function getGovernanceLawByCode(code: GovernanceLawCode) {
  return GOVERNANCE_LAWS.find(l => l.code === code);
}
```

---

## 🔍 QUICK REFERENCE

```
╔══════════════════════════════════════════════════════════════════╗
║                   CHE·NU™ v40 QUICK REFERENCE                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  SPHERES:           9 (FROZEN)                                   ║
║  ├── personal, business, government, creative                    ║
║  ├── community, social, entertainment                            ║
║  └── team, scholar                                               ║
║                                                                  ║
║  BUREAU SECTIONS:   6 (HARD LIMIT)                              ║
║  ├── quick_capture, resume_workspace, threads                    ║
║  └── data_files, active_agents, meetings                         ║
║                                                                  ║
║  GOVERNANCE LAWS:   10                                           ║
║  ├── L1-L5: Consent, Temporal, Context, Hierarchy, Audit        ║
║  └── L6-L10: Encoding, Non-Autonomy, Budget, Isolation, Delete  ║
║                                                                  ║
║  AGENTS:            226 total                                    ║
║  ├── L0: 1 (Nova)                                               ║
║  ├── L1: 1 (Orchestrator)                                       ║
║  ├── L2: 25 (Specialists)                                       ║
║  └── L3: 199 (Workers)                                          ║
║                                                                  ║
║  PIPELINE:          10 steps (all required)                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

*CHE·NU™ Master Reference v40*
*Last Updated: December 20, 2025*
*Status: FROZEN*
