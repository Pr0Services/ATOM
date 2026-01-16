############################################################
#                                                          #
#       CHE·NU AGENT CAPABILITY SYSTEM                     #
#       FRONTEND PAGES & COMPONENTS                        #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 5 — FRONTEND: AGENT DASHBOARD
============================================================

--- FILE: /che-nu-frontend/pages/agents.tsx
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU Frontend — Agent Capability Dashboard
 * =============================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Display agent profiles and their capabilities.
 * This is a VIEW ONLY - no agent execution.
 */

import React, { useState, useMemo } from 'react';
import { AgentList } from '../components/AgentList';
import { AgentDetail } from '../components/AgentDetail';
import { getAllTemplates, getTemplatesForSphere, getTemplatesUsingEngine } from '@che-nu-sdk/core/agent_templates';
import type { AgentProfile, DomainSphere } from '@che-nu-sdk/core/agent_profile';

// CHE·NU Brand Colors
const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

type FilterType = 'all' | 'sphere' | 'engine';

interface AgentsPageProps {
  initialAgents?: AgentProfile[];
}

export default function AgentsPage({ initialAgents }: AgentsPageProps) {
  const [selectedAgent, setSelectedAgent] = useState<AgentProfile | null>(null);
  const [filterType, setFilterType] = useState<FilterType>('all');
  const [filterValue, setFilterValue] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState('');

  // Get all agents
  const allAgents = useMemo(() => {
    return initialAgents || getAllTemplates();
  }, [initialAgents]);

  // Filter agents
  const filteredAgents = useMemo(() => {
    let agents = allAgents;

    // Apply type filter
    if (filterType === 'sphere' && filterValue) {
      agents = getTemplatesForSphere(filterValue as DomainSphere);
    } else if (filterType === 'engine' && filterValue) {
      agents = getTemplatesUsingEngine(filterValue);
    }

    // Apply search
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      agents = agents.filter(a =>
        a.name.toLowerCase().includes(term) ||
        a.description.toLowerCase().includes(term) ||
        a.tags.some(t => t.toLowerCase().includes(term))
      );
    }

    return agents;
  }, [allAgents, filterType, filterValue, searchTerm]);

  // Get unique spheres and engines for filters
  const spheres = useMemo(() => {
    const set = new Set<string>();
    allAgents.forEach(a => a.domainSpheres.forEach(s => set.add(s)));
    return Array.from(set).sort();
  }, [allAgents]);

  const engines = useMemo(() => {
    const set = new Set<string>();
    allAgents.forEach(a => a.capabilities.forEach(c => set.add(c.engine)));
    return Array.from(set).sort();
  }, [allAgents]);

  const handleAgentSelect = (agent: AgentProfile) => {
    setSelectedAgent(agent);
  };

  const handleBack = () => {
    setSelectedAgent(null);
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: COLORS.uiSlate,
      color: COLORS.softSand,
      fontFamily: "'Inter', -apple-system, sans-serif",
    }}>
      {/* Header */}
      <header style={{
        padding: '24px 32px',
        borderBottom: `1px solid ${COLORS.shadowMoss}`,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <div>
          <h1 style={{
            margin: 0,
            fontSize: '28px',
            fontWeight: 600,
            color: COLORS.sacredGold,
          }}>
            🤖 Agent Capability Dashboard
          </h1>
          <p style={{
            margin: '8px 0 0 0',
            fontSize: '14px',
            color: COLORS.ancientStone,
          }}>
            Explore agent profiles and their attached engines
            <span style={{
              marginLeft: '12px',
              padding: '2px 8px',
              backgroundColor: COLORS.shadowMoss,
              borderRadius: '4px',
              fontSize: '12px',
            }}>
              REPRESENTATIONAL ONLY
            </span>
          </p>
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <span style={{ color: COLORS.cenoteTurquoise, fontSize: '14px' }}>
            {filteredAgents.length} agents
          </span>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ padding: '24px 32px', display: 'flex', gap: '24px' }}>
        {/* Sidebar Filters */}
        <aside style={{
          width: '280px',
          flexShrink: 0,
        }}>
          {/* Search */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              fontSize: '12px',
              fontWeight: 600,
              color: COLORS.ancientStone,
              textTransform: 'uppercase',
            }}>
              Search
            </label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search agents..."
              style={{
                width: '100%',
                padding: '10px 12px',
                backgroundColor: COLORS.shadowMoss,
                border: `1px solid ${COLORS.ancientStone}33`,
                borderRadius: '6px',
                color: COLORS.softSand,
                fontSize: '14px',
              }}
            />
          </div>

          {/* Filter by Type */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              fontSize: '12px',
              fontWeight: 600,
              color: COLORS.ancientStone,
              textTransform: 'uppercase',
            }}>
              Filter By
            </label>
            <select
              value={filterType}
              onChange={(e) => {
                setFilterType(e.target.value as FilterType);
                setFilterValue('');
              }}
              style={{
                width: '100%',
                padding: '10px 12px',
                backgroundColor: COLORS.shadowMoss,
                border: `1px solid ${COLORS.ancientStone}33`,
                borderRadius: '6px',
                color: COLORS.softSand,
                fontSize: '14px',
              }}
            >
              <option value="all">All Agents</option>
              <option value="sphere">By Domain Sphere</option>
              <option value="engine">By Engine</option>
            </select>
          </div>

          {/* Filter Value */}
          {filterType === 'sphere' && (
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '12px',
                fontWeight: 600,
                color: COLORS.ancientStone,
                textTransform: 'uppercase',
              }}>
                Domain Sphere
              </label>
              <select
                value={filterValue}
                onChange={(e) => setFilterValue(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  backgroundColor: COLORS.shadowMoss,
                  border: `1px solid ${COLORS.ancientStone}33`,
                  borderRadius: '6px',
                  color: COLORS.softSand,
                  fontSize: '14px',
                }}
              >
                <option value="">Select sphere...</option>
                {spheres.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          )}

          {filterType === 'engine' && (
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '12px',
                fontWeight: 600,
                color: COLORS.ancientStone,
                textTransform: 'uppercase',
              }}>
                Engine
              </label>
              <select
                value={filterValue}
                onChange={(e) => setFilterValue(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  backgroundColor: COLORS.shadowMoss,
                  border: `1px solid ${COLORS.ancientStone}33`,
                  borderRadius: '6px',
                  color: COLORS.softSand,
                  fontSize: '14px',
                }}
              >
                <option value="">Select engine...</option>
                {engines.map(e => (
                  <option key={e} value={e}>{e}</option>
                ))}
              </select>
            </div>
          )}

          {/* Stats */}
          <div style={{
            padding: '16px',
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '8px',
            marginTop: '24px',
          }}>
            <h3 style={{
              margin: '0 0 12px 0',
              fontSize: '14px',
              color: COLORS.sacredGold,
            }}>
              📊 Statistics
            </h3>
            <div style={{ fontSize: '13px', lineHeight: 1.8 }}>
              <div>Total Agents: <span style={{ color: COLORS.cenoteTurquoise }}>{allAgents.length}</span></div>
              <div>Total Spheres: <span style={{ color: COLORS.cenoteTurquoise }}>{spheres.length}</span></div>
              <div>Total Engines: <span style={{ color: COLORS.cenoteTurquoise }}>{engines.length}</span></div>
            </div>
          </div>

          {/* SAFE Notice */}
          <div style={{
            padding: '16px',
            backgroundColor: `${COLORS.jungleEmerald}22`,
            borderRadius: '8px',
            marginTop: '16px',
            border: `1px solid ${COLORS.jungleEmerald}44`,
          }}>
            <h4 style={{
              margin: '0 0 8px 0',
              fontSize: '12px',
              color: COLORS.jungleEmerald,
            }}>
              ✓ SAFE COMPLIANCE
            </h4>
            <p style={{
              margin: 0,
              fontSize: '11px',
              color: COLORS.ancientStone,
              lineHeight: 1.6,
            }}>
              Agent profiles are representational only.
              No autonomous behavior. No execution.
              Profiles describe capabilities, not actions.
            </p>
          </div>
        </aside>

        {/* Main Content Area */}
        <div style={{ flex: 1 }}>
          {selectedAgent ? (
            <AgentDetail agent={selectedAgent} onBack={handleBack} />
          ) : (
            <AgentList agents={filteredAgents} onSelect={handleAgentSelect} />
          )}
        </div>
      </main>
    </div>
  );
}

============================================================
--- FILE: /che-nu-frontend/components/AgentList.tsx
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU Frontend — Agent List Component
 * =======================================
 * Display list of agent profiles
 */

import React from 'react';
import type { AgentProfile } from '@che-nu-sdk/core/agent_profile';

const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

interface AgentListProps {
  agents: AgentProfile[];
  onSelect: (agent: AgentProfile) => void;
}

export function AgentList({ agents, onSelect }: AgentListProps) {
  if (agents.length === 0) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '48px',
        color: COLORS.ancientStone,
      }}>
        <p style={{ fontSize: '18px' }}>No agents found</p>
        <p style={{ fontSize: '14px' }}>Try adjusting your filters</p>
      </div>
    );
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
      gap: '20px',
    }}>
      {agents.map((agent) => (
        <AgentCard key={agent.id} agent={agent} onClick={() => onSelect(agent)} />
      ))}
    </div>
  );
}

interface AgentCardProps {
  agent: AgentProfile;
  onClick: () => void;
}

function AgentCard({ agent, onClick }: AgentCardProps) {
  const roleEmoji: Record<string, string> = {
    researcher: '🔬',
    architect: '🏗️',
    coach: '🎯',
    analyst: '📊',
    coordinator: '🤝',
    specialist: '⚡',
    generalist: '🌐',
    mentor: '🧭',
    curator: '📚',
    creator: '🎨',
    planner: '📋',
    reviewer: '✅',
    facilitator: '🎪',
  };

  const levelColor: Record<string, string> = {
    novice: '#9CA3AF',
    low: '#60A5FA',
    medium: '#34D399',
    high: COLORS.sacredGold,
    expert: '#F472B6',
  };

  return (
    <div
      onClick={onClick}
      style={{
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
        padding: '20px',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        border: `1px solid transparent`,
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = COLORS.sacredGold;
        e.currentTarget.style.transform = 'translateY(-2px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = 'transparent';
        e.currentTarget.style.transform = 'translateY(0)';
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginBottom: '12px' }}>
        <span style={{ fontSize: '32px' }}>{roleEmoji[agent.role] || '🤖'}</span>
        <div style={{ flex: 1 }}>
          <h3 style={{
            margin: 0,
            fontSize: '16px',
            fontWeight: 600,
            color: COLORS.softSand,
          }}>
            {agent.name}
          </h3>
          <p style={{
            margin: '4px 0 0 0',
            fontSize: '12px',
            color: COLORS.ancientStone,
            textTransform: 'capitalize',
          }}>
            {agent.role}
          </p>
        </div>
      </div>

      {/* Description */}
      <p style={{
        margin: '0 0 12px 0',
        fontSize: '13px',
        color: COLORS.ancientStone,
        lineHeight: 1.5,
        display: '-webkit-box',
        WebkitLineClamp: 2,
        WebkitBoxOrient: 'vertical',
        overflow: 'hidden',
      }}>
        {agent.description}
      </p>

      {/* Spheres */}
      <div style={{ marginBottom: '12px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {agent.domainSpheres.map((sphere) => (
            <span
              key={sphere}
              style={{
                padding: '3px 8px',
                backgroundColor: `${COLORS.cenoteTurquoise}22`,
                borderRadius: '4px',
                fontSize: '11px',
                color: COLORS.cenoteTurquoise,
              }}
            >
              {sphere}
            </span>
          ))}
        </div>
      </div>

      {/* Capabilities Summary */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingTop: '12px',
        borderTop: `1px solid ${COLORS.uiSlate}`,
      }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          {agent.capabilities.slice(0, 3).map((cap) => (
            <span
              key={cap.engine}
              style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: levelColor[cap.level],
              }}
              title={`${cap.engine}: ${cap.level}`}
            />
          ))}
          {agent.capabilities.length > 3 && (
            <span style={{ fontSize: '11px', color: COLORS.ancientStone }}>
              +{agent.capabilities.length - 3}
            </span>
          )}
        </div>
        <span style={{
          fontSize: '11px',
          color: COLORS.sacredGold,
        }}>
          {agent.capabilities.length} engines →
        </span>
      </div>
    </div>
  );
}

export default AgentList;

============================================================
--- FILE: /che-nu-frontend/components/AgentDetail.tsx
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU Frontend — Agent Detail Component
 * =========================================
 * Display detailed agent profile view
 */

import React from 'react';
import type { AgentProfile, AgentCapability } from '@che-nu-sdk/core/agent_profile';

const COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};

interface AgentDetailProps {
  agent: AgentProfile;
  onBack: () => void;
}

export function AgentDetail({ agent, onBack }: AgentDetailProps) {
  const levelColor: Record<string, string> = {
    novice: '#9CA3AF',
    low: '#60A5FA',
    medium: '#34D399',
    high: COLORS.sacredGold,
    expert: '#F472B6',
  };

  const roleEmoji: Record<string, string> = {
    researcher: '🔬',
    architect: '🏗️',
    coach: '🎯',
    analyst: '📊',
    coordinator: '🤝',
    specialist: '⚡',
    generalist: '🌐',
    mentor: '🧭',
    curator: '📚',
    creator: '🎨',
    planner: '📋',
    reviewer: '✅',
    facilitator: '🎪',
  };

  return (
    <div>
      {/* Back Button */}
      <button
        onClick={onBack}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 16px',
          backgroundColor: 'transparent',
          border: `1px solid ${COLORS.ancientStone}44`,
          borderRadius: '6px',
          color: COLORS.ancientStone,
          cursor: 'pointer',
          marginBottom: '24px',
          fontSize: '14px',
        }}
      >
        ← Back to list
      </button>

      {/* Agent Header */}
      <div style={{
        backgroundColor: COLORS.shadowMoss,
        borderRadius: '12px',
        padding: '24px',
        marginBottom: '24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '20px' }}>
          <span style={{ fontSize: '48px' }}>{roleEmoji[agent.role] || '🤖'}</span>
          <div style={{ flex: 1 }}>
            <h1 style={{
              margin: 0,
              fontSize: '28px',
              fontWeight: 600,
              color: COLORS.sacredGold,
            }}>
              {agent.name}
            </h1>
            <p style={{
              margin: '8px 0',
              fontSize: '14px',
              color: COLORS.ancientStone,
              textTransform: 'capitalize',
            }}>
              {agent.role} Agent
            </p>
            <p style={{
              margin: '12px 0 0 0',
              fontSize: '15px',
              color: COLORS.softSand,
              lineHeight: 1.6,
            }}>
              {agent.description}
            </p>
          </div>
        </div>

        {/* Domain Spheres */}
        <div style={{ marginTop: '20px' }}>
          <h4 style={{
            margin: '0 0 12px 0',
            fontSize: '12px',
            fontWeight: 600,
            color: COLORS.ancientStone,
            textTransform: 'uppercase',
          }}>
            Domain Spheres
          </h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {agent.domainSpheres.map((sphere) => (
              <span
                key={sphere}
                style={{
                  padding: '6px 12px',
                  backgroundColor: `${COLORS.cenoteTurquoise}22`,
                  borderRadius: '6px',
                  fontSize: '13px',
                  color: COLORS.cenoteTurquoise,
                }}
              >
                {sphere}
              </span>
            ))}
          </div>
        </div>

        {/* Tags */}
        {agent.tags.length > 0 && (
          <div style={{ marginTop: '16px' }}>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {agent.tags.map((tag) => (
                <span
                  key={tag}
                  style={{
                    padding: '3px 8px',
                    backgroundColor: COLORS.uiSlate,
                    borderRadius: '4px',
                    fontSize: '11px',
                    color: COLORS.ancientStone,
                  }}
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Two Column Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Capabilities */}
        <div style={{
          backgroundColor: COLORS.shadowMoss,
          borderRadius: '12px',
          padding: '24px',
        }}>
          <h2 style={{
            margin: '0 0 20px 0',
            fontSize: '18px',
            fontWeight: 600,
            color: COLORS.sacredGold,
          }}>
            ⚙️ Capabilities
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {agent.capabilities.map((cap) => (
              <CapabilityCard key={cap.engine} capability={cap} levelColor={levelColor} />
            ))}
          </div>
        </div>

        {/* Use Cases & Limitations */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Use Cases */}
          <div style={{
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '12px',
            padding: '24px',
          }}>
            <h2 style={{
              margin: '0 0 16px 0',
              fontSize: '18px',
              fontWeight: 600,
              color: COLORS.jungleEmerald,
            }}>
              ✓ Use Cases
            </h2>
            <ul style={{
              margin: 0,
              padding: '0 0 0 20px',
              color: COLORS.softSand,
              fontSize: '14px',
              lineHeight: 1.8,
            }}>
              {agent.useCases.map((useCase, i) => (
                <li key={i}>{useCase}</li>
              ))}
            </ul>
          </div>

          {/* Limitations */}
          <div style={{
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '12px',
            padding: '24px',
          }}>
            <h2 style={{
              margin: '0 0 16px 0',
              fontSize: '18px',
              fontWeight: 600,
              color: COLORS.earthEmber,
            }}>
              ⚠️ Limitations
            </h2>
            <ul style={{
              margin: 0,
              padding: '0 0 0 20px',
              color: COLORS.ancientStone,
              fontSize: '14px',
              lineHeight: 1.8,
            }}>
              {agent.limitations.map((limitation, i) => (
                <li key={i}>{limitation}</li>
              ))}
            </ul>
          </div>

          {/* Collaborates With */}
          {agent.collaboratesWith.length > 0 && (
            <div style={{
              backgroundColor: COLORS.shadowMoss,
              borderRadius: '12px',
              padding: '24px',
            }}>
              <h2 style={{
                margin: '0 0 16px 0',
                fontSize: '18px',
                fontWeight: 600,
                color: COLORS.cenoteTurquoise,
              }}>
                🤝 Collaborates With
              </h2>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {agent.collaboratesWith.map((name) => (
                  <span
                    key={name}
                    style={{
                      padding: '6px 12px',
                      backgroundColor: `${COLORS.cenoteTurquoise}15`,
                      border: `1px solid ${COLORS.cenoteTurquoise}33`,
                      borderRadius: '6px',
                      fontSize: '13px',
                      color: COLORS.cenoteTurquoise,
                    }}
                  >
                    {name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* SAFE Notice */}
      <div style={{
        marginTop: '24px',
        padding: '16px 24px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        borderRadius: '8px',
        border: `1px solid ${COLORS.jungleEmerald}33`,
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
      }}>
        <span style={{ fontSize: '24px' }}>🔒</span>
        <div>
          <h4 style={{
            margin: '0 0 4px 0',
            fontSize: '14px',
            color: COLORS.jungleEmerald,
          }}>
            SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
          </h4>
          <p style={{
            margin: 0,
            fontSize: '12px',
            color: COLORS.ancientStone,
          }}>
            This agent profile is a capability descriptor only. 
            No autonomous actions or real executions are performed.
            User initiates all workflows through designated interfaces.
          </p>
        </div>
      </div>
    </div>
  );
}

interface CapabilityCardProps {
  capability: AgentCapability;
  levelColor: Record<string, string>;
}

function CapabilityCard({ capability, levelColor }: CapabilityCardProps) {
  return (
    <div style={{
      padding: '16px',
      backgroundColor: COLORS.uiSlate,
      borderRadius: '8px',
      borderLeft: `3px solid ${levelColor[capability.level]}`,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <span style={{ fontWeight: 600, fontSize: '14px', color: COLORS.softSand }}>
          {capability.engine}
        </span>
        <span style={{
          padding: '2px 8px',
          backgroundColor: `${levelColor[capability.level]}22`,
          borderRadius: '4px',
          fontSize: '11px',
          color: levelColor[capability.level],
          textTransform: 'uppercase',
        }}>
          {capability.level}
        </span>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
        {capability.focus.map((f) => (
          <span
            key={f}
            style={{
              padding: '2px 6px',
              backgroundColor: COLORS.shadowMoss,
              borderRadius: '3px',
              fontSize: '11px',
              color: COLORS.ancientStone,
            }}
          >
            {f}
          </span>
        ))}
      </div>

      {capability.subEngines && capability.subEngines.length > 0 && (
        <div style={{ marginTop: '8px', fontSize: '11px', color: COLORS.ancientStone }}>
          Sub-engines: {capability.subEngines.join(', ')}
        </div>
      )}

      {capability.notes && (
        <div style={{ marginTop: '8px', fontSize: '12px', color: COLORS.ancientStone, fontStyle: 'italic' }}>
          {capability.notes}
        </div>
      )}
    </div>
  );
}

export default AgentDetail;
