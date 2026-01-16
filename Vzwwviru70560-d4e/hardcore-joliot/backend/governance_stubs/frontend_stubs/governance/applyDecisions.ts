// Example hook-style adapter (framework-agnostic)
// Wire into your state management (Zustand/Redux/etc.)

import { GovernanceSignal } from './types';
import { runGovernance } from './api';
import { postThreadEvent } from '../thread/threadEvents';

export async function applyGovernanceDecisions(threadId: string, context: Record<string, any>, signals: GovernanceSignal[]) {
  const decisions = await runGovernance(threadId, context, signals);

  for (const d of decisions) {
    if (d.action === 'PATCH' && d.payload?.patch) {
      // Patch is an instruction to the executor. Depending on your executor integration,
      // you can send it as a system message/event into the thread.
      await postThreadEvent(threadId, 'PATCH_INSTRUCTION', d.payload.patch);
    }
    if (d.action === 'BLOCK') {
      await postThreadEvent(threadId, 'EXECUTION_BLOCKED', { reason: d.reason, scope: d.scope });
    }
    if (d.action === 'ESCALATE') {
      await postThreadEvent(threadId, 'ESCALATION_TRIGGERED', { reason: d.reason, scope: d.scope, payload: d.payload });
    }
  }

  return decisions;
}
