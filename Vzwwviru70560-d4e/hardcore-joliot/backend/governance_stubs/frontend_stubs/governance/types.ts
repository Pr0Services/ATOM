export type SignalLevel = 'WARN' | 'CORRECT' | 'PAUSE' | 'BLOCK' | 'ESCALATE';

export interface Scope {
  segment_id?: string;
  region?: string;
  zone_id?: string;
  item_id?: string;
}

export interface GovernanceSignal {
  level: SignalLevel;
  criterion: string;
  message: string;
  scope?: Scope;
  confidence?: number;
  references?: Record<string, any>;
}

export interface PatchInstruction {
  scope: Scope;
  constraint: string;
  correction: string;
  rationale: string;
  verification_spec_id?: string;
}

export type OrchestratorAction = 'RUN_SPEC' | 'DEFER_SPEC' | 'ESCALATE' | 'PATCH' | 'BLOCK' | 'NOOP';

export interface OrchestratorDecision {
  decision_id: string;
  action: OrchestratorAction;
  reason: string;
  scope?: Scope;
  required_quality?: number;
  budgets?: Record<string, any>;
  payload?: Record<string, any>;
}
