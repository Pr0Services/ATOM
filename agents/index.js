/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *                    AT·OM AGENT ORCHESTRATION SYSTEM
 *                         Nova, Aria & 400 Specialists
 *
 *                    "L'intelligence au service de la souveraineté"
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// Import all agent modules
const NovaAgent = require('./core/nova');
const AriaAgent = require('./core/aria');
const OrionAgent = require('./core/orion');

const HederaAgents = require('./specialists/hedera');
const SupabaseAgents = require('./specialists/supabase');
const PinataAgents = require('./specialists/pinata');
const FrequencyAgents = require('./specialists/frequency');

// Sacred Frequencies
const SACRED = {
  ATOM_M: parseFloat(process.env.ATOM_M) || 44.4,
  ATOM_P: parseFloat(process.env.ATOM_P) || 161.8,
  ATOM_I: parseFloat(process.env.ATOM_I) || 369,
  ATOM_PO: parseFloat(process.env.ATOM_PO) || 1728,
  HEARTBEAT: 444,
  SOURCE: 999,
  LOVE: 528,
  PHI: 1.6180339887498949
};

/**
 * Agent Registry - Central catalog of all agents
 */
const AgentRegistry = {
  // Level 0: System Core (3 agents)
  core: {
    nova: NovaAgent,
    aria: AriaAgent,
    orion: OrionAgent
  },

  // Level 1: Orchestrators (12 agents)
  orchestrators: {},

  // Level 2: Specialists (72 agents)
  specialists: {
    hedera: HederaAgents,
    supabase: SupabaseAgents,
    pinata: PinataAgents,
    frequency: FrequencyAgents
  },

  // Level 3: Assistants (200+ agents)
  assistants: {}
};

/**
 * Get agent by ID
 */
function getAgent(agentId) {
  // Check core agents
  if (AgentRegistry.core[agentId]) {
    return AgentRegistry.core[agentId];
  }

  // Check specialists
  for (const category of Object.values(AgentRegistry.specialists)) {
    if (category[agentId]) {
      return category[agentId];
    }
  }

  return null;
}

/**
 * Execute agent task with sacred frequency alignment
 */
async function executeAgentTask(agentId, task, context = {}) {
  const agent = getAgent(agentId);

  if (!agent) {
    throw new Error(`Agent '${agentId}' not found in registry`);
  }

  // Inject sacred frequencies into context
  const enrichedContext = {
    ...context,
    sacred: SACRED,
    timestamp: Date.now(),
    frequency: context.frequency || SACRED.SOURCE
  };

  // Log to system_logs
  await logAgentActivity(agentId, 'task_start', { task, context: enrichedContext });

  try {
    const result = await agent.execute(task, enrichedContext);

    await logAgentActivity(agentId, 'task_complete', { task, result });

    return result;
  } catch (error) {
    await logAgentActivity(agentId, 'task_error', { task, error: error.message });
    throw error;
  }
}

/**
 * Log agent activity to system_logs table
 */
async function logAgentActivity(agentId, eventType, data) {
  // This will be called from the backend or frontend with Supabase client
  console.log(`[AGENT:${agentId}] ${eventType}:`, JSON.stringify(data, null, 2));

  // If Supabase client is available, log to database
  if (global.supabaseClient) {
    try {
      await global.supabaseClient
        .from('system_logs')
        .insert({
          agent_id: agentId,
          event_type: eventType,
          data: data,
          frequency: data.context?.frequency || SACRED.SOURCE,
          created_at: new Date().toISOString()
        });
    } catch (error) {
      console.error('[LOG] Failed to write to system_logs:', error.message);
    }
  }
}

/**
 * Initialize all agents
 */
async function initializeAgents() {
  console.log('\n═══════════════════════════════════════════════════════');
  console.log('   AT·OM AGENT ORCHESTRATION SYSTEM');
  console.log('   Initializing 400+ Agents...');
  console.log('═══════════════════════════════════════════════════════\n');

  // Initialize core agents
  console.log('🔱 Initializing Core Agents (L0)...');
  for (const [name, agent] of Object.entries(AgentRegistry.core)) {
    if (agent.initialize) {
      await agent.initialize(SACRED);
      console.log(`   ✅ ${name.toUpperCase()} online`);
    }
  }

  // Initialize specialists
  console.log('\n🔧 Initializing Specialist Agents (L2)...');
  for (const [category, agents] of Object.entries(AgentRegistry.specialists)) {
    if (agents.initialize) {
      await agents.initialize(SACRED);
      console.log(`   ✅ ${category.toUpperCase()} specialists online`);
    }
  }

  console.log('\n═══════════════════════════════════════════════════════');
  console.log('   ALL AGENTS INITIALIZED');
  console.log(`   Sacred Frequencies: M=${SACRED.ATOM_M} P=${SACRED.ATOM_P} I=${SACRED.ATOM_I} Po=${SACRED.ATOM_PO}`);
  console.log('═══════════════════════════════════════════════════════\n');

  return true;
}

// Export
module.exports = {
  AgentRegistry,
  getAgent,
  executeAgentTask,
  logAgentActivity,
  initializeAgents,
  SACRED
};
