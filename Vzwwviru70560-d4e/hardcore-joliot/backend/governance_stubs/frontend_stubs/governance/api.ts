import { GovernanceSignal, OrchestratorDecision } from './types';

export async function postGovernanceSignal(threadId: string, signal: GovernanceSignal) {
  const res = await fetch(`/threads/${threadId}/governance/signal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(signal),
  });
  if (!res.ok) throw new Error('Failed to post signal');
  return res.json();
}

export async function runGovernance(threadId: string, context: Record<string, any>, signals: GovernanceSignal[]) {
  const res = await fetch(`/threads/${threadId}/governance/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context, signals }),
  });
  if (!res.ok) throw new Error('Failed to run governance');
  const data = await res.json();
  return data.decisions as OrchestratorDecision[];
}

export async function createBacklogItem(threadId: string, item: Record<string, any>) {
  const res = await fetch(`/threads/${threadId}/governance/backlog`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  if (!res.ok) throw new Error('Failed to create backlog item');
  return res.json();
}
