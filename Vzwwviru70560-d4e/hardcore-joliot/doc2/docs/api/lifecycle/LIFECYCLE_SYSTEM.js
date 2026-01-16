/**
 * CHE·NU™ LIFECYCLE SYSTEM
 * Version 1.0 – CANONICAL
 * 
 * CORE PRINCIPLE:
 * CHE·NU evolves information through EXPLICIT STATES.
 * Nothing becomes "important", "final", or "shared" by accident.
 * 
 * ALL transitions are:
 * - intentional
 * - traceable
 * - reversible (when possible)
 * - governed
 * 
 * If intent is unclear, the system MUST ask.
 */

// ═══════════════════════════════════════════════════════════════
// LIFECYCLE OBJECT TYPES
// ═══════════════════════════════════════════════════════════════

const LIFECYCLE_OBJECTS = [
  'note',
  'task',
  'project',
  'thread',
  'document',
  'meeting',
  'skill',
  'agent',
  'permission',
  'budget'
];

// ═══════════════════════════════════════════════════════════════
// NOTE LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const NOTE_LIFECYCLE = {
  object_type: 'note',
  
  states: {
    DRAFT: {
      name: 'Draft',
      description: 'Entry Bureau or Sphere, not contextualized',
      location: 'Entry Bureau or Sphere',
      agent_usage: false,
      reversible_from: []
    },
    CONTEXTUALIZED: {
      name: 'Contextualized',
      description: 'Assigned to a Sphere',
      location: 'Sphere',
      agent_usage: false,
      requires_validation: true,
      reversible_from: ['DRAFT']
    },
    LINKED: {
      name: 'Linked',
      description: 'Attached to Thread or Project',
      location: 'Thread/Project',
      agent_usage: true,
      note: 'Linking never duplicates content',
      reversible_from: ['CONTEXTUALIZED']
    },
    ARCHIVED: {
      name: 'Archived',
      description: 'Readable but not active',
      location: 'Archive',
      agent_usage: false,
      read_only: true,
      reversible_from: ['DRAFT', 'CONTEXTUALIZED', 'LINKED']
    }
  },
  
  initial_state: 'DRAFT',
  
  transitions: [
    { from: 'DRAFT', to: 'CONTEXTUALIZED', requires: 'user_validation' },
    { from: 'DRAFT', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'CONTEXTUALIZED', to: 'LINKED', requires: 'user_action' },
    { from: 'CONTEXTUALIZED', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'LINKED', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'ARCHIVED', to: 'DRAFT', requires: 'user_confirmation', reversible: true }
  ],
  
  rules: [
    'Draft notes are never used by agents',
    'Contextualization requires user validation',
    'Linking never duplicates content',
    'Archived notes remain readable, not active'
  ]
};

// ═══════════════════════════════════════════════════════════════
// TASK LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const TASK_LIFECYCLE = {
  object_type: 'task',
  
  states: {
    PENDING: {
      name: 'Pending',
      description: 'Created but not scheduled',
      can_execute: false
    },
    PLANNED: {
      name: 'Planned',
      description: 'Scheduled for execution',
      can_execute: false
    },
    IN_PROGRESS: {
      name: 'In Progress',
      description: 'Currently being worked on',
      can_execute: true
    },
    BLOCKED: {
      name: 'Blocked',
      description: 'Cannot proceed, waiting for dependency',
      can_execute: false,
      requires_reason: true
    },
    COMPLETED: {
      name: 'Completed',
      description: 'Finished successfully',
      can_execute: false,
      note: 'Completion does not imply deletion'
    },
    ARCHIVED: {
      name: 'Archived',
      description: 'Historical record',
      can_execute: false,
      immutable: true
    }
  },
  
  initial_state: 'PENDING',
  
  transitions: [
    { from: 'PENDING', to: 'PLANNED', requires: 'user_action' },
    { from: 'PENDING', to: 'IN_PROGRESS', requires: 'user_action' },
    { from: 'PENDING', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'PLANNED', to: 'IN_PROGRESS', requires: 'user_action' },
    { from: 'PLANNED', to: 'BLOCKED', requires: 'reason' },
    { from: 'IN_PROGRESS', to: 'BLOCKED', requires: 'reason' },
    { from: 'IN_PROGRESS', to: 'COMPLETED', requires: 'user_confirmation' },
    { from: 'BLOCKED', to: 'IN_PROGRESS', requires: 'user_action' },
    { from: 'BLOCKED', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'COMPLETED', to: 'ARCHIVED', requires: 'user_confirmation' }
  ],
  
  rules: [
    'Tasks may exist without projects',
    'Completion does not imply deletion',
    'Archived tasks are immutable'
  ]
};

// ═══════════════════════════════════════════════════════════════
// PROJECT LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const PROJECT_LIFECYCLE = {
  object_type: 'project',
  
  states: {
    DRAFT: {
      name: 'Draft',
      description: 'Being defined',
      can_have_tasks: true,
      active: false
    },
    ACTIVE: {
      name: 'Active',
      description: 'Currently running',
      can_have_tasks: true,
      active: true
    },
    PAUSED: {
      name: 'Paused',
      description: 'Temporarily stopped',
      can_have_tasks: true,
      active: false,
      reversible_to_active: true
    },
    COMPLETED: {
      name: 'Completed',
      description: 'Finished successfully',
      can_have_tasks: false,
      active: false
    },
    ARCHIVED: {
      name: 'Archived',
      description: 'Historical record',
      can_have_tasks: false,
      active: false,
      note: 'Archiving does not delete data'
    }
  },
  
  initial_state: 'DRAFT',
  
  transitions: [
    { from: 'DRAFT', to: 'ACTIVE', requires: 'user_confirmation' },
    { from: 'DRAFT', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'ACTIVE', to: 'PAUSED', requires: 'user_action' },
    { from: 'ACTIVE', to: 'COMPLETED', requires: 'user_confirmation' },
    { from: 'PAUSED', to: 'ACTIVE', requires: 'user_action', reversible: true },
    { from: 'PAUSED', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'COMPLETED', to: 'ARCHIVED', requires: 'user_confirmation' }
  ],
  
  rules: [
    'A project aggregates tasks and threads',
    'Projects define temporal scope',
    'Archiving a project does not delete its data'
  ]
};

// ═══════════════════════════════════════════════════════════════
// THREAD (.chenu) LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const THREAD_LIFECYCLE = {
  object_type: 'thread',
  
  states: {
    OPEN: {
      name: 'Open',
      description: 'Created, awaiting first exchange',
      can_add_messages: true,
      decisions_recorded: false
    },
    ACTIVE: {
      name: 'Active',
      description: 'Ongoing conversation',
      can_add_messages: true,
      decisions_recorded: false
    },
    DECISION_RECORDED: {
      name: 'Decision Recorded',
      description: 'Contains explicit decision',
      can_add_messages: true,
      decisions_recorded: true,
      note: 'Decisions must be explicit'
    },
    CLOSED: {
      name: 'Closed',
      description: 'Conversation ended',
      can_add_messages: false,
      read_only: true,
      note: 'Closed threads are read-only'
    },
    ARCHIVED: {
      name: 'Archived',
      description: 'Historical record',
      can_add_messages: false,
      read_only: true,
      auditable: true,
      note: 'Archived threads remain auditable'
    }
  },
  
  initial_state: 'OPEN',
  
  transitions: [
    { from: 'OPEN', to: 'ACTIVE', requires: 'first_message' },
    { from: 'OPEN', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'ACTIVE', to: 'DECISION_RECORDED', requires: 'explicit_decision' },
    { from: 'ACTIVE', to: 'CLOSED', requires: 'user_confirmation' },
    { from: 'DECISION_RECORDED', to: 'CLOSED', requires: 'user_confirmation' },
    { from: 'CLOSED', to: 'ARCHIVED', requires: 'user_confirmation' }
  ],
  
  rules: [
    'Threads are the unit of truth',
    'Decisions must be explicit',
    'Closed threads are read-only',
    'Archived threads remain auditable'
  ]
};

// ═══════════════════════════════════════════════════════════════
// DOCUMENT LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const DOCUMENT_LIFECYCLE = {
  object_type: 'document',
  
  states: {
    DRAFT: {
      name: 'Draft',
      description: 'User-created, in progress',
      location: 'user_space',
      versioned: false
    },
    GENERATED: {
      name: 'Generated',
      description: 'Agent output, awaiting review',
      location: 'agent_output',
      requires_integration: true,
      note: 'Starts outside user space'
    },
    REVIEWED: {
      name: 'Reviewed',
      description: 'User has reviewed agent output',
      location: 'agent_output',
      ready_for_integration: true
    },
    INTEGRATED: {
      name: 'Integrated',
      description: 'Added to user space',
      location: 'user_space',
      note: 'Integration requires explicit user action'
    },
    VERSIONED: {
      name: 'Versioned',
      description: 'Multiple versions tracked',
      location: 'user_space',
      history_preserved: true,
      note: 'Versioning preserves history and diff'
    },
    ARCHIVED: {
      name: 'Archived',
      description: 'Historical record',
      location: 'archive',
      read_only: true
    }
  },
  
  initial_state: 'DRAFT',
  
  transitions: [
    { from: 'DRAFT', to: 'VERSIONED', requires: 'user_action' },
    { from: 'DRAFT', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'GENERATED', to: 'REVIEWED', requires: 'user_review' },
    { from: 'REVIEWED', to: 'INTEGRATED', requires: 'explicit_user_action' },
    { from: 'REVIEWED', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'INTEGRATED', to: 'VERSIONED', requires: 'user_action' },
    { from: 'INTEGRATED', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'VERSIONED', to: 'ARCHIVED', requires: 'user_confirmation' }
  ],
  
  rules: [
    'Agent-generated documents start outside user space',
    'Integration requires explicit user action',
    'Versioning preserves history and diff'
  ]
};

// ═══════════════════════════════════════════════════════════════
// MEETING LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const MEETING_LIFECYCLE = {
  object_type: 'meeting',
  
  states: {
    SCHEDULED: {
      name: 'Scheduled',
      description: 'Planned for future',
      can_join: false,
      outputs_required: false
    },
    LIVE: {
      name: 'Live',
      description: 'Currently happening',
      can_join: true,
      outputs_required: false
    },
    RECORDED: {
      name: 'Recorded',
      description: 'Finished, recording available',
      can_join: false,
      outputs_required: true,
      has_recording: true
    },
    SUMMARIZED: {
      name: 'Summarized',
      description: 'Summary and notes created',
      can_join: false,
      outputs_required: true,
      has_summary: true
    },
    ACTIONED: {
      name: 'Actioned',
      description: 'Decisions extracted and linked',
      can_join: false,
      outputs_required: true,
      note: 'Decisions become threads'
    },
    ARCHIVED: {
      name: 'Archived',
      description: 'Historical record',
      can_join: false,
      read_only: true
    }
  },
  
  initial_state: 'SCHEDULED',
  
  transitions: [
    { from: 'SCHEDULED', to: 'LIVE', requires: 'meeting_start' },
    { from: 'SCHEDULED', to: 'ARCHIVED', requires: 'user_confirmation' },
    { from: 'LIVE', to: 'RECORDED', requires: 'meeting_end' },
    { from: 'RECORDED', to: 'SUMMARIZED', requires: 'summary_generation' },
    { from: 'SUMMARIZED', to: 'ACTIONED', requires: 'decision_extraction' },
    { from: 'ACTIONED', to: 'ARCHIVED', requires: 'user_confirmation' }
  ],
  
  rules: [
    'Meetings must produce traceable outputs',
    'Decisions extracted become linked to threads'
  ]
};

// ═══════════════════════════════════════════════════════════════
// SKILL (IA LABS) LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const SKILL_LIFECYCLE = {
  object_type: 'skill',
  
  states: {
    EXPERIMENTAL: {
      name: 'Experimental',
      description: 'In IA Labs',
      location: 'IA Labs',
      affects_production: false,
      note: 'Never affects production'
    },
    TESTED: {
      name: 'Tested',
      description: 'Experiments completed',
      location: 'IA Labs',
      affects_production: false,
      ready_for_validation: true
    },
    VALIDATED: {
      name: 'Validated',
      description: 'Safety and performance confirmed',
      location: 'IA Labs',
      affects_production: false,
      ready_for_promotion: true,
      note: 'Promotion requires validation'
    },
    PRODUCTION_READY: {
      name: 'Production-Ready',
      description: 'Available in production',
      location: 'Production',
      affects_production: true
    },
    DEPRECATED: {
      name: 'Deprecated',
      description: 'No longer recommended',
      location: 'Archive',
      affects_production: false,
      documented: true,
      note: 'Deprecated skills remain documented'
    }
  },
  
  initial_state: 'EXPERIMENTAL',
  
  transitions: [
    { from: 'EXPERIMENTAL', to: 'TESTED', requires: 'experiments_complete' },
    { from: 'TESTED', to: 'VALIDATED', requires: 'validation_passed' },
    { from: 'VALIDATED', to: 'PRODUCTION_READY', requires: 'promotion_approval' },
    { from: 'PRODUCTION_READY', to: 'DEPRECATED', requires: 'deprecation_notice' },
    { from: 'DEPRECATED', to: 'PRODUCTION_READY', requires: 'undeprecation_approval', reversible: true }
  ],
  
  rules: [
    'Experimental skills never affect production',
    'Promotion requires validation',
    'Deprecated skills remain documented'
  ]
};

// ═══════════════════════════════════════════════════════════════
// AGENT LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const AGENT_LIFECYCLE = {
  object_type: 'agent',
  
  states: {
    AVAILABLE: {
      name: 'Available',
      description: 'Ready to be engaged',
      can_receive_tasks: true,
      active: false
    },
    ENGAGED: {
      name: 'Engaged',
      description: 'Assigned to task',
      can_receive_tasks: false,
      active: false
    },
    EXECUTING: {
      name: 'Executing',
      description: 'Currently working',
      can_receive_tasks: false,
      active: true,
      note: 'Agents never self-initiate tasks'
    },
    WAITING_APPROVAL: {
      name: 'Waiting Approval',
      description: 'Task complete, awaiting user review',
      can_receive_tasks: false,
      active: false,
      requires_user_action: true
    },
    COMPLETED: {
      name: 'Completed',
      description: 'Task finished and approved',
      can_receive_tasks: true,
      active: false
    },
    DISABLED: {
      name: 'Disabled',
      description: 'Not available for tasks',
      can_receive_tasks: false,
      active: false,
      note: 'May be disabled at any time'
    }
  },
  
  initial_state: 'AVAILABLE',
  
  transitions: [
    { from: 'AVAILABLE', to: 'ENGAGED', requires: 'task_assignment' },
    { from: 'AVAILABLE', to: 'DISABLED', requires: 'user_action' },
    { from: 'ENGAGED', to: 'EXECUTING', requires: 'task_start' },
    { from: 'EXECUTING', to: 'WAITING_APPROVAL', requires: 'task_complete' },
    { from: 'EXECUTING', to: 'DISABLED', requires: 'user_action' },
    { from: 'WAITING_APPROVAL', to: 'COMPLETED', requires: 'user_approval' },
    { from: 'WAITING_APPROVAL', to: 'EXECUTING', requires: 'revision_requested' },
    { from: 'COMPLETED', to: 'AVAILABLE', requires: 'task_finalized' },
    { from: 'DISABLED', to: 'AVAILABLE', requires: 'user_action', reversible: true }
  ],
  
  rules: [
    'Agents never self-initiate tasks',
    'Agents never self-escalate levels',
    'Agents may be disabled at any time'
  ]
};

// ═══════════════════════════════════════════════════════════════
// PERMISSION & SCOPE LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const PERMISSION_LIFECYCLE = {
  object_type: 'permission',
  
  states: {
    REQUESTED: {
      name: 'Requested',
      description: 'Permission requested, pending approval',
      active: false,
      scoped: false
    },
    GRANTED: {
      name: 'Granted',
      description: 'Approved but not active',
      active: false,
      scoped: true,
      note: 'Permissions are always scoped'
    },
    ACTIVE: {
      name: 'Active',
      description: 'Currently in use',
      active: true,
      scoped: true
    },
    LIMITED: {
      name: 'Limited',
      description: 'Restricted temporarily',
      active: true,
      scoped: true,
      restricted: true
    },
    REVOKED: {
      name: 'Revoked',
      description: 'Permission removed',
      active: false,
      scoped: false,
      note: 'Revocation is immediate',
      audit_note: 'Historical actions remain auditable'
    }
  },
  
  initial_state: 'REQUESTED',
  
  transitions: [
    { from: 'REQUESTED', to: 'GRANTED', requires: 'approval' },
    { from: 'REQUESTED', to: 'REVOKED', requires: 'rejection' },
    { from: 'GRANTED', to: 'ACTIVE', requires: 'first_use' },
    { from: 'GRANTED', to: 'REVOKED', requires: 'revocation', immediate: true },
    { from: 'ACTIVE', to: 'LIMITED', requires: 'restriction' },
    { from: 'ACTIVE', to: 'REVOKED', requires: 'revocation', immediate: true },
    { from: 'LIMITED', to: 'ACTIVE', requires: 'unrestriction' },
    { from: 'LIMITED', to: 'REVOKED', requires: 'revocation', immediate: true }
  ],
  
  rules: [
    'Permissions are always scoped',
    'Revocation is immediate',
    'Historical actions remain auditable'
  ]
};

// ═══════════════════════════════════════════════════════════════
// BUDGET LIFECYCLE
// ═══════════════════════════════════════════════════════════════

const BUDGET_LIFECYCLE = {
  object_type: 'budget',
  
  states: {
    DEFINED: {
      name: 'Defined',
      description: 'Budget amount set',
      can_execute: false,
      allocated: false
    },
    ALLOCATED: {
      name: 'Allocated',
      description: 'Budget assigned to scope',
      can_execute: true,
      allocated: true,
      available: true,
      note: 'Checked BEFORE execution'
    },
    CONSUMING: {
      name: 'Consuming',
      description: 'Budget being used',
      can_execute: true,
      allocated: true,
      in_use: true
    },
    THRESHOLD_REACHED: {
      name: 'Threshold Reached',
      description: 'Warning threshold hit',
      can_execute: true,
      allocated: true,
      warning_triggered: true,
      note: 'Triggers warnings, not overruns'
    },
    BLOCKED: {
      name: 'Blocked',
      description: 'Budget exhausted',
      can_execute: false,
      allocated: true,
      note: 'Stops execution immediately'
    },
    RESET: {
      name: 'Reset',
      description: 'Budget refreshed',
      can_execute: true,
      allocated: true
    },
    CLOSED: {
      name: 'Closed',
      description: 'Budget period ended',
      can_execute: false,
      allocated: false
    }
  },
  
  initial_state: 'DEFINED',
  
  transitions: [
    { from: 'DEFINED', to: 'ALLOCATED', requires: 'allocation' },
    { from: 'ALLOCATED', to: 'CONSUMING', requires: 'first_execution' },
    { from: 'CONSUMING', to: 'THRESHOLD_REACHED', requires: 'threshold_check' },
    { from: 'CONSUMING', to: 'BLOCKED', requires: 'budget_exhausted', immediate: true },
    { from: 'THRESHOLD_REACHED', to: 'BLOCKED', requires: 'budget_exhausted', immediate: true },
    { from: 'BLOCKED', to: 'RESET', requires: 'budget_refresh' },
    { from: 'RESET', to: 'CONSUMING', requires: 'execution_resume' },
    { from: 'ALLOCATED', to: 'CLOSED', requires: 'period_end' },
    { from: 'CONSUMING', to: 'CLOSED', requires: 'period_end' },
    { from: 'BLOCKED', to: 'CLOSED', requires: 'period_end' }
  ],
  
  rules: [
    'Budgets are checked BEFORE execution',
    'Thresholds trigger warnings, not overruns',
    'Blocked budgets stop execution immediately'
  ]
};

// ═══════════════════════════════════════════════════════════════
// LIFECYCLE REGISTRY
// ═══════════════════════════════════════════════════════════════

const LIFECYCLE_REGISTRY = {
  note: NOTE_LIFECYCLE,
  task: TASK_LIFECYCLE,
  project: PROJECT_LIFECYCLE,
  thread: THREAD_LIFECYCLE,
  document: DOCUMENT_LIFECYCLE,
  meeting: MEETING_LIFECYCLE,
  skill: SKILL_LIFECYCLE,
  agent: AGENT_LIFECYCLE,
  permission: PERMISSION_LIFECYCLE,
  budget: BUDGET_LIFECYCLE
};

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  LIFECYCLE_OBJECTS,
  LIFECYCLE_REGISTRY,
  NOTE_LIFECYCLE,
  TASK_LIFECYCLE,
  PROJECT_LIFECYCLE,
  THREAD_LIFECYCLE,
  DOCUMENT_LIFECYCLE,
  MEETING_LIFECYCLE,
  SKILL_LIFECYCLE,
  AGENT_LIFECYCLE,
  PERMISSION_LIFECYCLE,
  BUDGET_LIFECYCLE
};
