############################################################
#                                                          #
#       CHE·NU PROJECT & MISSION LAYER                     #
#       PART 4: FRONTEND PAGES & COMPONENTS                #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 9 — FRONTEND PAGES
============================================================

--- FILE: /che-nu-frontend/pages/projects.tsx
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU Frontend — Projects Page
 * ================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays representational project structures.
 * All interactions are user-initiated.
 */

import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { ProjectViewer } from '../components/ProjectViewer';

// ============================================================
// CONSTANTS
// ============================================================

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

// ============================================================
// TYPES
// ============================================================

interface ProjectSummary {
  id: string;
  name: string;
  description: string;
  status: 'draft' | 'active' | 'paused' | 'completed' | 'archived';
  goalsCount: number;
  tasksCount: number;
  milestonesCount: number;
  enginesCount: number;
  created: string;
}

// ============================================================
// SAMPLE DATA (Representational)
// ============================================================

const SAMPLE_PROJECTS: ProjectSummary[] = [
  {
    id: 'proj_sample1',
    name: 'CHE·NU Platform Development',
    description: 'Full development of the CHE·NU life management platform',
    status: 'active',
    goalsCount: 5,
    tasksCount: 24,
    milestonesCount: 8,
    enginesCount: 12,
    created: '2024-01-15',
  },
  {
    id: 'proj_sample2',
    name: 'Personal Finance Restructure',
    description: 'Reorganize personal finances and investment strategy',
    status: 'draft',
    goalsCount: 3,
    tasksCount: 12,
    milestonesCount: 4,
    enginesCount: 4,
    created: '2024-02-20',
  },
  {
    id: 'proj_sample3',
    name: 'Skill Development Roadmap',
    description: 'Plan for acquiring new technical and soft skills',
    status: 'active',
    goalsCount: 4,
    tasksCount: 18,
    milestonesCount: 6,
    enginesCount: 5,
    created: '2024-03-01',
  },
];

// ============================================================
// STATUS HELPERS
// ============================================================

const STATUS_CONFIG = {
  draft: { label: 'Draft', color: COLORS.ancientStone, emoji: '📝' },
  active: { label: 'Active', color: COLORS.jungleEmerald, emoji: '🚀' },
  paused: { label: 'Paused', color: COLORS.earthEmber, emoji: '⏸️' },
  completed: { label: 'Completed', color: COLORS.cenoteTurquoise, emoji: '✅' },
  archived: { label: 'Archived', color: COLORS.ancientStone, emoji: '📦' },
};

// ============================================================
// COMPONENTS
// ============================================================

interface ProjectCardProps {
  project: ProjectSummary;
  onSelect: (id: string) => void;
  isSelected: boolean;
}

function ProjectCard({ project, onSelect, isSelected }: ProjectCardProps) {
  const statusConfig = STATUS_CONFIG[project.status];
  
  return (
    <div
      onClick={() => onSelect(project.id)}
      style={{
        padding: '20px',
        backgroundColor: isSelected ? COLORS.shadowMoss : `${COLORS.shadowMoss}80`,
        borderRadius: '12px',
        border: `2px solid ${isSelected ? COLORS.sacredGold : 'transparent'}`,
        cursor: 'pointer',
        transition: 'all 0.2s ease',
      }}
    >
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '12px',
      }}>
        <h3 style={{
          margin: 0,
          fontSize: '16px',
          fontWeight: 600,
          color: COLORS.softSand,
        }}>
          {project.name}
        </h3>
        <span style={{
          padding: '4px 8px',
          backgroundColor: `${statusConfig.color}30`,
          color: statusConfig.color,
          borderRadius: '6px',
          fontSize: '11px',
          fontWeight: 600,
        }}>
          {statusConfig.emoji} {statusConfig.label}
        </span>
      </div>
      
      {/* Description */}
      <p style={{
        margin: '0 0 16px 0',
        fontSize: '13px',
        color: COLORS.ancientStone,
        lineHeight: 1.5,
      }}>
        {project.description}
      </p>
      
      {/* Stats */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '8px',
      }}>
        <StatBadge label="Goals" value={project.goalsCount} emoji="🎯" />
        <StatBadge label="Tasks" value={project.tasksCount} emoji="📋" />
        <StatBadge label="Milestones" value={project.milestonesCount} emoji="🏁" />
        <StatBadge label="Engines" value={project.enginesCount} emoji="⚙️" />
      </div>
      
      {/* Created date */}
      <div style={{
        marginTop: '12px',
        fontSize: '11px',
        color: COLORS.ancientStone,
      }}>
        Created: {new Date(project.created).toLocaleDateString()}
      </div>
    </div>
  );
}

interface StatBadgeProps {
  label: string;
  value: number;
  emoji: string;
}

function StatBadge({ label, value, emoji }: StatBadgeProps) {
  return (
    <div style={{
      textAlign: 'center',
      padding: '8px 4px',
      backgroundColor: `${COLORS.uiSlate}80`,
      borderRadius: '6px',
    }}>
      <div style={{ fontSize: '14px' }}>{emoji}</div>
      <div style={{
        fontSize: '16px',
        fontWeight: 700,
        color: COLORS.softSand,
      }}>
        {value}
      </div>
      <div style={{
        fontSize: '10px',
        color: COLORS.ancientStone,
      }}>
        {label}
      </div>
    </div>
  );
}

// ============================================================
// MAIN PAGE COMPONENT
// ============================================================

export function ProjectsPage() {
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Filter projects
  const filteredProjects = useMemo(() => {
    return SAMPLE_PROJECTS.filter(p => {
      const matchesStatus = filterStatus === 'all' || p.status === filterStatus;
      const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          p.description.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesStatus && matchesSearch;
    });
  }, [filterStatus, searchQuery]);
  
  const selectedProject = selectedProjectId 
    ? SAMPLE_PROJECTS.find(p => p.id === selectedProjectId) 
    : null;
  
  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: COLORS.uiSlate,
      color: COLORS.softSand,
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
            fontSize: '24px',
            fontWeight: 700,
            color: COLORS.sacredGold,
          }}>
            📊 Project Tools
          </h1>
          <p style={{
            margin: '4px 0 0 0',
            fontSize: '13px',
            color: COLORS.ancientStone,
          }}>
            SAFE · REPRESENTATIONAL · View and structure project models
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '12px' }}>
          <button style={{
            padding: '10px 20px',
            backgroundColor: COLORS.sacredGold,
            color: COLORS.uiSlate,
            border: 'none',
            borderRadius: '8px',
            fontWeight: 600,
            cursor: 'pointer',
          }}>
            + Create Project
          </button>
          <Link to="/missions" style={{
            padding: '10px 20px',
            backgroundColor: 'transparent',
            color: COLORS.cenoteTurquoise,
            border: `1px solid ${COLORS.cenoteTurquoise}`,
            borderRadius: '8px',
            fontWeight: 600,
            textDecoration: 'none',
          }}>
            View Missions →
          </Link>
        </div>
      </header>
      
      {/* Toolbar */}
      <div style={{
        padding: '16px 32px',
        display: 'flex',
        gap: '16px',
        alignItems: 'center',
        borderBottom: `1px solid ${COLORS.shadowMoss}`,
      }}>
        {/* Search */}
        <input
          type="text"
          placeholder="Search projects..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            padding: '10px 16px',
            backgroundColor: COLORS.shadowMoss,
            border: `1px solid ${COLORS.ancientStone}40`,
            borderRadius: '8px',
            color: COLORS.softSand,
            width: '280px',
            fontSize: '14px',
          }}
        />
        
        {/* Status Filter */}
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          style={{
            padding: '10px 16px',
            backgroundColor: COLORS.shadowMoss,
            border: `1px solid ${COLORS.ancientStone}40`,
            borderRadius: '8px',
            color: COLORS.softSand,
            fontSize: '14px',
          }}
        >
          <option value="all">All Status</option>
          <option value="draft">Draft</option>
          <option value="active">Active</option>
          <option value="paused">Paused</option>
          <option value="completed">Completed</option>
          <option value="archived">Archived</option>
        </select>
        
        {/* Count */}
        <span style={{
          marginLeft: 'auto',
          fontSize: '13px',
          color: COLORS.ancientStone,
        }}>
          {filteredProjects.length} project(s)
        </span>
      </div>
      
      {/* Main Content */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: selectedProject ? '1fr 1fr' : '1fr',
        gap: '24px',
        padding: '24px 32px',
      }}>
        {/* Project List */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
        }}>
          {filteredProjects.map(project => (
            <ProjectCard
              key={project.id}
              project={project}
              onSelect={setSelectedProjectId}
              isSelected={project.id === selectedProjectId}
            />
          ))}
          
          {filteredProjects.length === 0 && (
            <div style={{
              padding: '40px',
              textAlign: 'center',
              color: COLORS.ancientStone,
            }}>
              No projects found matching your criteria.
            </div>
          )}
        </div>
        
        {/* Project Viewer (when selected) */}
        {selectedProject && (
          <div style={{
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '12px',
            padding: '24px',
          }}>
            <ProjectViewer projectId={selectedProject.id} />
          </div>
        )}
      </div>
      
      {/* Action Buttons */}
      <div style={{
        padding: '16px 32px',
        borderTop: `1px solid ${COLORS.shadowMoss}`,
        display: 'flex',
        gap: '12px',
      }}>
        <ActionButton label="View Capabilities" emoji="🧠" color={COLORS.cenoteTurquoise} />
        <ActionButton label="Map Engines" emoji="⚙️" color={COLORS.jungleEmerald} />
        <ActionButton label="Export Structure" emoji="📤" color={COLORS.earthEmber} />
      </div>
      
      {/* SAFE Notice */}
      <div style={{
        padding: '16px 32px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
      }}>
        <span style={{ fontSize: '16px' }}>🔒</span>
        <span style={{ fontSize: '12px', color: COLORS.jungleEmerald }}>
          SAFE · NON-AUTONOMOUS · All project structures are representational only. 
          No execution, no persistence, no real project management.
        </span>
      </div>
    </div>
  );
}

interface ActionButtonProps {
  label: string;
  emoji: string;
  color: string;
}

function ActionButton({ label, emoji, color }: ActionButtonProps) {
  return (
    <button style={{
      padding: '10px 16px',
      backgroundColor: `${color}20`,
      color: color,
      border: `1px solid ${color}40`,
      borderRadius: '8px',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontWeight: 500,
    }}>
      <span>{emoji}</span>
      {label}
    </button>
  );
}

export default ProjectsPage;

============================================================

--- FILE: /che-nu-frontend/pages/missions.tsx
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU Frontend — Missions Page
 * ================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays representational mission structures.
 * All interactions are user-initiated.
 */

import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { MissionViewer } from '../components/MissionViewer';

// ============================================================
// CONSTANTS
// ============================================================

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

// ============================================================
// TYPES
// ============================================================

interface MissionSummary {
  id: string;
  name: string;
  objective: string;
  urgency: 'critical' | 'high' | 'normal' | 'low';
  status: 'draft' | 'active' | 'paused' | 'completed' | 'cancelled';
  objectivesCount: number;
  stepsCount: number;
  projectId: string | null;
  created: string;
}

// ============================================================
// SAMPLE DATA (Representational)
// ============================================================

const SAMPLE_MISSIONS: MissionSummary[] = [
  {
    id: 'miss_sample1',
    name: 'Complete Agent Capability Layer',
    objective: 'Finalize all 12 agent templates and engine mappings',
    urgency: 'high',
    status: 'active',
    objectivesCount: 3,
    stepsCount: 8,
    projectId: 'proj_sample1',
    created: '2024-12-10',
  },
  {
    id: 'miss_sample2',
    name: 'Research Investment Options',
    objective: 'Analyze and compare investment vehicles for Q1 allocation',
    urgency: 'normal',
    status: 'draft',
    objectivesCount: 2,
    stepsCount: 5,
    projectId: 'proj_sample2',
    created: '2024-12-08',
  },
  {
    id: 'miss_sample3',
    name: 'Learn TypeScript Advanced Features',
    objective: 'Master generics, decorators, and utility types',
    urgency: 'low',
    status: 'active',
    objectivesCount: 4,
    stepsCount: 12,
    projectId: 'proj_sample3',
    created: '2024-12-05',
  },
  {
    id: 'miss_sample4',
    name: 'Quick Bug Fix Sprint',
    objective: 'Address critical UI issues before release',
    urgency: 'critical',
    status: 'active',
    objectivesCount: 1,
    stepsCount: 4,
    projectId: null,
    created: '2024-12-12',
  },
];

// ============================================================
// HELPERS
// ============================================================

const URGENCY_CONFIG = {
  critical: { label: 'Critical', color: '#E53E3E', emoji: '🔴' },
  high: { label: 'High', color: COLORS.earthEmber, emoji: '🟠' },
  normal: { label: 'Normal', color: COLORS.cenoteTurquoise, emoji: '🟢' },
  low: { label: 'Low', color: COLORS.ancientStone, emoji: '⚪' },
};

const STATUS_CONFIG = {
  draft: { label: 'Draft', color: COLORS.ancientStone },
  active: { label: 'Active', color: COLORS.jungleEmerald },
  paused: { label: 'Paused', color: COLORS.earthEmber },
  completed: { label: 'Completed', color: COLORS.cenoteTurquoise },
  cancelled: { label: 'Cancelled', color: '#E53E3E' },
};

// ============================================================
// COMPONENTS
// ============================================================

interface MissionCardProps {
  mission: MissionSummary;
  onSelect: (id: string) => void;
  isSelected: boolean;
}

function MissionCard({ mission, onSelect, isSelected }: MissionCardProps) {
  const urgencyConfig = URGENCY_CONFIG[mission.urgency];
  const statusConfig = STATUS_CONFIG[mission.status];
  
  return (
    <div
      onClick={() => onSelect(mission.id)}
      style={{
        padding: '20px',
        backgroundColor: isSelected ? COLORS.shadowMoss : `${COLORS.shadowMoss}80`,
        borderRadius: '12px',
        border: `2px solid ${isSelected ? COLORS.cenoteTurquoise : 'transparent'}`,
        borderLeft: `4px solid ${urgencyConfig.color}`,
        cursor: 'pointer',
        transition: 'all 0.2s ease',
      }}
    >
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '8px',
      }}>
        <h3 style={{
          margin: 0,
          fontSize: '16px',
          fontWeight: 600,
          color: COLORS.softSand,
        }}>
          {urgencyConfig.emoji} {mission.name}
        </h3>
        <span style={{
          padding: '4px 8px',
          backgroundColor: `${statusConfig.color}30`,
          color: statusConfig.color,
          borderRadius: '6px',
          fontSize: '11px',
          fontWeight: 600,
        }}>
          {statusConfig.label}
        </span>
      </div>
      
      {/* Objective */}
      <p style={{
        margin: '0 0 12px 0',
        fontSize: '13px',
        color: COLORS.ancientStone,
        lineHeight: 1.5,
      }}>
        {mission.objective}
      </p>
      
      {/* Stats Row */}
      <div style={{
        display: 'flex',
        gap: '16px',
        alignItems: 'center',
      }}>
        <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>
          🎯 {mission.objectivesCount} objectives
        </span>
        <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>
          📝 {mission.stepsCount} steps
        </span>
        {mission.projectId && (
          <span style={{
            fontSize: '11px',
            padding: '2px 8px',
            backgroundColor: `${COLORS.sacredGold}30`,
            color: COLORS.sacredGold,
            borderRadius: '4px',
          }}>
            📊 Linked to Project
          </span>
        )}
      </div>
    </div>
  );
}

// ============================================================
// MAIN PAGE COMPONENT
// ============================================================

export function MissionsPage() {
  const [selectedMissionId, setSelectedMissionId] = useState<string | null>(null);
  const [filterUrgency, setFilterUrgency] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  
  // Filter missions
  const filteredMissions = useMemo(() => {
    return SAMPLE_MISSIONS.filter(m => {
      const matchesUrgency = filterUrgency === 'all' || m.urgency === filterUrgency;
      const matchesStatus = filterStatus === 'all' || m.status === filterStatus;
      return matchesUrgency && matchesStatus;
    });
  }, [filterUrgency, filterStatus]);
  
  const selectedMission = selectedMissionId
    ? SAMPLE_MISSIONS.find(m => m.id === selectedMissionId)
    : null;
  
  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: COLORS.uiSlate,
      color: COLORS.softSand,
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
            fontSize: '24px',
            fontWeight: 700,
            color: COLORS.cenoteTurquoise,
          }}>
            🎯 Mission Tools
          </h1>
          <p style={{
            margin: '4px 0 0 0',
            fontSize: '13px',
            color: COLORS.ancientStone,
          }}>
            SAFE · REPRESENTATIONAL · Focus on outcomes and objectives
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '12px' }}>
          <button style={{
            padding: '10px 20px',
            backgroundColor: COLORS.cenoteTurquoise,
            color: COLORS.uiSlate,
            border: 'none',
            borderRadius: '8px',
            fontWeight: 600,
            cursor: 'pointer',
          }}>
            + Create Mission
          </button>
          <Link to="/projects" style={{
            padding: '10px 20px',
            backgroundColor: 'transparent',
            color: COLORS.sacredGold,
            border: `1px solid ${COLORS.sacredGold}`,
            borderRadius: '8px',
            fontWeight: 600,
            textDecoration: 'none',
          }}>
            View Projects →
          </Link>
        </div>
      </header>
      
      {/* Toolbar */}
      <div style={{
        padding: '16px 32px',
        display: 'flex',
        gap: '16px',
        alignItems: 'center',
        borderBottom: `1px solid ${COLORS.shadowMoss}`,
      }}>
        {/* Urgency Filter */}
        <select
          value={filterUrgency}
          onChange={(e) => setFilterUrgency(e.target.value)}
          style={{
            padding: '10px 16px',
            backgroundColor: COLORS.shadowMoss,
            border: `1px solid ${COLORS.ancientStone}40`,
            borderRadius: '8px',
            color: COLORS.softSand,
            fontSize: '14px',
          }}
        >
          <option value="all">All Urgency</option>
          <option value="critical">🔴 Critical</option>
          <option value="high">🟠 High</option>
          <option value="normal">🟢 Normal</option>
          <option value="low">⚪ Low</option>
        </select>
        
        {/* Status Filter */}
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          style={{
            padding: '10px 16px',
            backgroundColor: COLORS.shadowMoss,
            border: `1px solid ${COLORS.ancientStone}40`,
            borderRadius: '8px',
            color: COLORS.softSand,
            fontSize: '14px',
          }}
        >
          <option value="all">All Status</option>
          <option value="draft">Draft</option>
          <option value="active">Active</option>
          <option value="paused">Paused</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
        
        {/* Count */}
        <span style={{
          marginLeft: 'auto',
          fontSize: '13px',
          color: COLORS.ancientStone,
        }}>
          {filteredMissions.length} mission(s)
        </span>
      </div>
      
      {/* Main Content */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: selectedMission ? '1fr 1fr' : '1fr',
        gap: '24px',
        padding: '24px 32px',
      }}>
        {/* Mission List */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
        }}>
          {filteredMissions.map(mission => (
            <MissionCard
              key={mission.id}
              mission={mission}
              onSelect={setSelectedMissionId}
              isSelected={mission.id === selectedMissionId}
            />
          ))}
          
          {filteredMissions.length === 0 && (
            <div style={{
              padding: '40px',
              textAlign: 'center',
              color: COLORS.ancientStone,
            }}>
              No missions found matching your criteria.
            </div>
          )}
        </div>
        
        {/* Mission Viewer (when selected) */}
        {selectedMission && (
          <div style={{
            backgroundColor: COLORS.shadowMoss,
            borderRadius: '12px',
            padding: '24px',
          }}>
            <MissionViewer missionId={selectedMission.id} />
          </div>
        )}
      </div>
      
      {/* Action Buttons */}
      <div style={{
        padding: '16px 32px',
        borderTop: `1px solid ${COLORS.shadowMoss}`,
        display: 'flex',
        gap: '12px',
      }}>
        <ActionButton label="Define Objectives" emoji="🎯" color={COLORS.cenoteTurquoise} />
        <ActionButton label="Show Timeline" emoji="📅" color={COLORS.sacredGold} />
        <ActionButton label="Link to Project" emoji="🔗" color={COLORS.jungleEmerald} />
        <ActionButton label="Map Engines" emoji="⚙️" color={COLORS.earthEmber} />
      </div>
      
      {/* SAFE Notice */}
      <div style={{
        padding: '16px 32px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
      }}>
        <span style={{ fontSize: '16px' }}>🔒</span>
        <span style={{ fontSize: '12px', color: COLORS.jungleEmerald }}>
          SAFE · NON-AUTONOMOUS · All mission structures are representational only.
          No execution, no persistence, no real mission planning.
        </span>
      </div>
    </div>
  );
}

interface ActionButtonProps {
  label: string;
  emoji: string;
  color: string;
}

function ActionButton({ label, emoji, color }: ActionButtonProps) {
  return (
    <button style={{
      padding: '10px 16px',
      backgroundColor: `${color}20`,
      color: color,
      border: `1px solid ${color}40`,
      borderRadius: '8px',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontWeight: 500,
    }}>
      <span>{emoji}</span>
      {label}
    </button>
  );
}

export default MissionsPage;

============================================================

--- FILE: /che-nu-frontend/components/ProjectViewer.tsx
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU Frontend — Project Viewer Component
 * ===========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays detailed view of a project structure.
 */

import React, { useState } from 'react';

// ============================================================
// CONSTANTS
// ============================================================

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

// ============================================================
// TYPES
// ============================================================

interface ProjectViewerProps {
  projectId: string;
}

type ViewTab = 'overview' | 'goals' | 'tasks' | 'milestones' | 'resources' | 'engines';

// ============================================================
// SAMPLE PROJECT DATA
// ============================================================

const SAMPLE_PROJECT_DETAIL = {
  id: 'proj_sample1',
  name: 'CHE·NU Platform Development',
  description: 'Full development of the CHE·NU life management platform with all core engines, agent system, and XR capabilities.',
  status: 'active',
  context: {
    domain_sphere: 'Business',
    scale: 'team',
    timeline_type: 'medium_term',
  },
  goals: [
    { id: 'g1', title: 'Complete Core Engine Suite', priority: 'critical', status: 'active', engines: ['ProjectEngine', 'TaskEngine'] },
    { id: 'g2', title: 'Implement Agent System', priority: 'high', status: 'achieved', engines: ['AgentProfileEngine'] },
    { id: 'g3', title: 'Build XR Interface', priority: 'high', status: 'pending', engines: ['XRSceneEngine'] },
    { id: 'g4', title: 'Documentation Complete', priority: 'medium', status: 'active', engines: ['ContentEngine'] },
    { id: 'g5', title: 'API Integration', priority: 'high', status: 'pending', engines: ['DataEngine'] },
  ],
  tasks: [
    { id: 't1', name: 'Design schema', complexity: 'moderate', status: 'done' },
    { id: 't2', name: 'Implement core modules', complexity: 'complex', status: 'done' },
    { id: 't3', name: 'Build frontend pages', complexity: 'moderate', status: 'in_progress' },
    { id: 't4', name: 'Write documentation', complexity: 'simple', status: 'in_progress' },
    { id: 't5', name: 'Testing suite', complexity: 'complex', status: 'todo' },
  ],
  milestones: [
    { id: 'm1', name: 'Alpha Release', marker: 'v0.1.0', status: 'reached' },
    { id: 'm2', name: 'Core Complete', marker: 'v0.5.0', status: 'reached' },
    { id: 'm3', name: 'Beta Release', marker: 'v0.9.0', status: 'upcoming' },
    { id: 'm4', name: 'Production Ready', marker: 'v1.0.0', status: 'upcoming' },
  ],
  resources: [
    { id: 'r1', type: 'human', name: 'Development Team', access: 'available' },
    { id: 'r2', type: 'technical', name: 'Cloud Infrastructure', access: 'available' },
    { id: 'r3', type: 'time', name: 'Development Hours', access: 'limited' },
  ],
  required_engines: [
    'ProjectEngine', 'MissionEngine', 'TaskEngine', 'GoalEngine',
    'XRSceneEngine', 'ContentEngine', 'DataEngine', 'AnalysisEngine',
    'AgentProfileEngine', 'CollaborationEngine', 'SchedulingEngine', 'KnowledgeEngine',
  ],
};

// ============================================================
// COMPONENT
// ============================================================

export function ProjectViewer({ projectId }: ProjectViewerProps) {
  const [activeTab, setActiveTab] = useState<ViewTab>('overview');
  const project = SAMPLE_PROJECT_DETAIL; // In real app, fetch by projectId
  
  const tabs: { key: ViewTab; label: string; emoji: string }[] = [
    { key: 'overview', label: 'Overview', emoji: '📋' },
    { key: 'goals', label: 'Goals', emoji: '🎯' },
    { key: 'tasks', label: 'Tasks', emoji: '📝' },
    { key: 'milestones', label: 'Milestones', emoji: '🏁' },
    { key: 'resources', label: 'Resources', emoji: '📦' },
    { key: 'engines', label: 'Engines', emoji: '⚙️' },
  ];
  
  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{
          margin: 0,
          fontSize: '18px',
          fontWeight: 700,
          color: COLORS.sacredGold,
        }}>
          {project.name}
        </h2>
        <p style={{
          margin: '8px 0 0 0',
          fontSize: '13px',
          color: COLORS.ancientStone,
          lineHeight: 1.5,
        }}>
          {project.description}
        </p>
      </div>
      
      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '8px',
        marginBottom: '20px',
        borderBottom: `1px solid ${COLORS.uiSlate}`,
        paddingBottom: '12px',
      }}>
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              padding: '8px 12px',
              backgroundColor: activeTab === tab.key ? COLORS.sacredGold : 'transparent',
              color: activeTab === tab.key ? COLORS.uiSlate : COLORS.softSand,
              border: 'none',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {tab.emoji} {tab.label}
          </button>
        ))}
      </div>
      
      {/* Content */}
      <div style={{ minHeight: '300px' }}>
        {activeTab === 'overview' && (
          <OverviewTab project={project} />
        )}
        {activeTab === 'goals' && (
          <GoalsTab goals={project.goals} />
        )}
        {activeTab === 'tasks' && (
          <TasksTab tasks={project.tasks} />
        )}
        {activeTab === 'milestones' && (
          <MilestonesTab milestones={project.milestones} />
        )}
        {activeTab === 'resources' && (
          <ResourcesTab resources={project.resources} />
        )}
        {activeTab === 'engines' && (
          <EnginesTab engines={project.required_engines} />
        )}
      </div>
    </div>
  );
}

// ============================================================
// TAB COMPONENTS
// ============================================================

function OverviewTab({ project }: { project: typeof SAMPLE_PROJECT_DETAIL }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '12px',
      }}>
        <StatCard label="Goals" value={project.goals.length} color={COLORS.sacredGold} />
        <StatCard label="Tasks" value={project.tasks.length} color={COLORS.cenoteTurquoise} />
        <StatCard label="Milestones" value={project.milestones.length} color={COLORS.jungleEmerald} />
      </div>
      
      <div style={{
        padding: '16px',
        backgroundColor: `${COLORS.uiSlate}80`,
        borderRadius: '8px',
      }}>
        <h4 style={{ margin: '0 0 12px 0', color: COLORS.softSand, fontSize: '14px' }}>Context</h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          <ContextTag label="Domain" value={project.context.domain_sphere} />
          <ContextTag label="Scale" value={project.context.scale} />
          <ContextTag label="Timeline" value={project.context.timeline_type} />
        </div>
      </div>
      
      <div style={{
        padding: '16px',
        backgroundColor: `${COLORS.uiSlate}80`,
        borderRadius: '8px',
      }}>
        <h4 style={{ margin: '0 0 12px 0', color: COLORS.softSand, fontSize: '14px' }}>
          Progress Summary
        </h4>
        <ProgressBar label="Goals" done={2} total={5} />
        <ProgressBar label="Tasks" done={2} total={5} />
        <ProgressBar label="Milestones" done={2} total={4} />
      </div>
    </div>
  );
}

function GoalsTab({ goals }: { goals: typeof SAMPLE_PROJECT_DETAIL.goals }) {
  const priorityColors: Record<string, string> = {
    critical: '#E53E3E',
    high: COLORS.earthEmber,
    medium: COLORS.cenoteTurquoise,
    low: COLORS.ancientStone,
  };
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {goals.map(goal => (
        <div key={goal.id} style={{
          padding: '12px',
          backgroundColor: `${COLORS.uiSlate}80`,
          borderRadius: '8px',
          borderLeft: `3px solid ${priorityColors[goal.priority]}`,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: COLORS.softSand, fontWeight: 600, fontSize: '14px' }}>
              {goal.title}
            </span>
            <span style={{
              padding: '2px 8px',
              backgroundColor: `${COLORS.jungleEmerald}30`,
              color: COLORS.jungleEmerald,
              borderRadius: '4px',
              fontSize: '11px',
            }}>
              {goal.status}
            </span>
          </div>
          <div style={{ marginTop: '8px', display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
            {goal.engines.map(e => (
              <span key={e} style={{
                padding: '2px 6px',
                backgroundColor: `${COLORS.sacredGold}20`,
                color: COLORS.sacredGold,
                borderRadius: '4px',
                fontSize: '10px',
              }}>
                {e}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function TasksTab({ tasks }: { tasks: typeof SAMPLE_PROJECT_DETAIL.tasks }) {
  const statusColors: Record<string, string> = {
    done: COLORS.jungleEmerald,
    in_progress: COLORS.cenoteTurquoise,
    todo: COLORS.ancientStone,
  };
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {tasks.map(task => (
        <div key={task.id} style={{
          padding: '12px',
          backgroundColor: `${COLORS.uiSlate}80`,
          borderRadius: '8px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <div>
            <span style={{ color: COLORS.softSand, fontSize: '14px' }}>{task.name}</span>
            <span style={{
              marginLeft: '8px',
              padding: '2px 6px',
              backgroundColor: `${COLORS.ancientStone}30`,
              color: COLORS.ancientStone,
              borderRadius: '4px',
              fontSize: '10px',
            }}>
              {task.complexity}
            </span>
          </div>
          <span style={{
            padding: '4px 8px',
            backgroundColor: `${statusColors[task.status]}30`,
            color: statusColors[task.status],
            borderRadius: '4px',
            fontSize: '11px',
            fontWeight: 600,
          }}>
            {task.status.replace('_', ' ')}
          </span>
        </div>
      ))}
    </div>
  );
}

function MilestonesTab({ milestones }: { milestones: typeof SAMPLE_PROJECT_DETAIL.milestones }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {milestones.map((m, idx) => (
        <div key={m.id} style={{
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
        }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            backgroundColor: m.status === 'reached' ? COLORS.jungleEmerald : COLORS.shadowMoss,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: COLORS.softSand,
            fontWeight: 700,
            fontSize: '12px',
          }}>
            {m.status === 'reached' ? '✓' : idx + 1}
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ color: COLORS.softSand, fontWeight: 600, fontSize: '14px' }}>
              {m.name}
            </div>
            <div style={{ color: COLORS.ancientStone, fontSize: '12px' }}>
              {m.marker}
            </div>
          </div>
          <span style={{
            padding: '4px 8px',
            backgroundColor: m.status === 'reached' ? `${COLORS.jungleEmerald}30` : `${COLORS.ancientStone}30`,
            color: m.status === 'reached' ? COLORS.jungleEmerald : COLORS.ancientStone,
            borderRadius: '4px',
            fontSize: '11px',
          }}>
            {m.status}
          </span>
        </div>
      ))}
    </div>
  );
}

function ResourcesTab({ resources }: { resources: typeof SAMPLE_PROJECT_DETAIL.resources }) {
  const typeEmojis: Record<string, string> = {
    human: '👤',
    technical: '💻',
    time: '⏰',
    financial: '💰',
    material: '📦',
    knowledge: '📚',
  };
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {resources.map(r => (
        <div key={r.id} style={{
          padding: '12px',
          backgroundColor: `${COLORS.uiSlate}80`,
          borderRadius: '8px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
        }}>
          <span style={{ fontSize: '20px' }}>{typeEmojis[r.type] || '📦'}</span>
          <div style={{ flex: 1 }}>
            <div style={{ color: COLORS.softSand, fontWeight: 600, fontSize: '14px' }}>
              {r.name}
            </div>
            <div style={{ color: COLORS.ancientStone, fontSize: '12px' }}>
              Type: {r.type}
            </div>
          </div>
          <span style={{
            padding: '4px 8px',
            backgroundColor: r.access === 'available' ? `${COLORS.jungleEmerald}30` : `${COLORS.earthEmber}30`,
            color: r.access === 'available' ? COLORS.jungleEmerald : COLORS.earthEmber,
            borderRadius: '4px',
            fontSize: '11px',
          }}>
            {r.access}
          </span>
        </div>
      ))}
    </div>
  );
}

function EnginesTab({ engines }: { engines: string[] }) {
  return (
    <div>
      <p style={{ color: COLORS.ancientStone, fontSize: '13px', marginBottom: '16px' }}>
        {engines.length} engines mapped to this project:
      </p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {engines.map(engine => (
          <span key={engine} style={{
            padding: '8px 12px',
            backgroundColor: `${COLORS.sacredGold}20`,
            color: COLORS.sacredGold,
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 600,
          }}>
            ⚙️ {engine}
          </span>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// HELPER COMPONENTS
// ============================================================

function StatCard({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div style={{
      padding: '16px',
      backgroundColor: `${COLORS.uiSlate}80`,
      borderRadius: '8px',
      textAlign: 'center',
    }}>
      <div style={{ fontSize: '24px', fontWeight: 700, color }}>{value}</div>
      <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>{label}</div>
    </div>
  );
}

function ContextTag({ label, value }: { label: string; value: string }) {
  return (
    <span style={{
      padding: '4px 10px',
      backgroundColor: `${COLORS.cenoteTurquoise}20`,
      color: COLORS.cenoteTurquoise,
      borderRadius: '6px',
      fontSize: '11px',
    }}>
      {label}: {value}
    </span>
  );
}

function ProgressBar({ label, done, total }: { label: string; done: number; total: number }) {
  const percentage = Math.round((done / total) * 100);
  
  return (
    <div style={{ marginBottom: '12px' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '4px',
      }}>
        <span style={{ fontSize: '12px', color: COLORS.softSand }}>{label}</span>
        <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>{done}/{total}</span>
      </div>
      <div style={{
        height: '6px',
        backgroundColor: COLORS.uiSlate,
        borderRadius: '3px',
        overflow: 'hidden',
      }}>
        <div style={{
          width: `${percentage}%`,
          height: '100%',
          backgroundColor: COLORS.jungleEmerald,
          borderRadius: '3px',
        }} />
      </div>
    </div>
  );
}

export default ProjectViewer;

============================================================

--- FILE: /che-nu-frontend/components/MissionViewer.tsx
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU Frontend — Mission Viewer Component
 * ===========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Displays detailed view of a mission structure.
 */

import React, { useState } from 'react';

// ============================================================
// CONSTANTS
// ============================================================

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

// ============================================================
// TYPES
// ============================================================

interface MissionViewerProps {
  missionId: string;
}

type ViewTab = 'overview' | 'objectives' | 'steps' | 'timeline' | 'capabilities';

// ============================================================
// SAMPLE MISSION DATA
// ============================================================

const SAMPLE_MISSION_DETAIL = {
  id: 'miss_sample1',
  name: 'Complete Agent Capability Layer',
  objective: 'Finalize all 12 agent templates and engine mappings',
  urgency: 'high',
  status: 'active',
  context: {
    scope: 'focused',
    domain_sphere: 'Business',
    success_definition: 'All agent templates functional with complete engine coverage',
  },
  objectives: [
    {
      id: 'obj1',
      statement: 'Create AgentProfileEngine with full type definitions',
      priority: 'primary',
      status: 'achieved',
      key_results: ['Types defined', 'Methods implemented', 'Tests passing'],
    },
    {
      id: 'obj2',
      statement: 'Build 12 agent templates covering all domains',
      priority: 'primary',
      status: 'achieved',
      key_results: ['Templates created', 'Engine mappings complete'],
    },
    {
      id: 'obj3',
      statement: 'Integrate with existing system index',
      priority: 'secondary',
      status: 'in_progress',
      key_results: ['System index updated', 'API routes added'],
    },
  ],
  steps: [
    { id: 's1', order: 1, name: 'Define agent profile types', status: 'completed', engine: 'TypeScript' },
    { id: 's2', order: 2, name: 'Implement core methods', status: 'completed', engine: 'AgentProfileEngine' },
    { id: 's3', order: 3, name: 'Create agent templates', status: 'completed', engine: 'AgentTemplates' },
    { id: 's4', order: 4, name: 'Build registry module', status: 'completed', engine: 'AgentRegistry' },
    { id: 's5', order: 5, name: 'Create frontend components', status: 'active', engine: 'React' },
    { id: 's6', order: 6, name: 'Update system index', status: 'pending', engine: 'Documentation' },
    { id: 's7', order: 7, name: 'Add API endpoints', status: 'pending', engine: 'API' },
    { id: 's8', order: 8, name: 'Write integration tests', status: 'pending', engine: 'Testing' },
  ],
  timeline: [
    { phase: 'Preparation', duration: 'short', status: 'completed' },
    { phase: 'Core Development', duration: 'medium', status: 'completed' },
    { phase: 'Frontend Integration', duration: 'medium', status: 'active' },
    { phase: 'Documentation', duration: 'short', status: 'pending' },
    { phase: 'Completion', duration: 'short', status: 'pending' },
  ],
  capability_map: [
    { engine: 'AgentProfileEngine', level: 'essential', reason: 'Core module' },
    { engine: 'AgentRegistry', level: 'essential', reason: 'Profile storage' },
    { engine: 'TaskEngine', level: 'important', reason: 'Step management' },
    { engine: 'GoalEngine', level: 'important', reason: 'Objective tracking' },
    { engine: 'ContentEngine', level: 'helpful', reason: 'Documentation' },
  ],
  project_id: 'proj_sample1',
};

// ============================================================
// COMPONENT
// ============================================================

export function MissionViewer({ missionId }: MissionViewerProps) {
  const [activeTab, setActiveTab] = useState<ViewTab>('overview');
  const mission = SAMPLE_MISSION_DETAIL; // In real app, fetch by missionId
  
  const tabs: { key: ViewTab; label: string; emoji: string }[] = [
    { key: 'overview', label: 'Overview', emoji: '📋' },
    { key: 'objectives', label: 'Objectives', emoji: '🎯' },
    { key: 'steps', label: 'Steps', emoji: '📝' },
    { key: 'timeline', label: 'Timeline', emoji: '📅' },
    { key: 'capabilities', label: 'Capabilities', emoji: '⚙️' },
  ];
  
  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span style={{
            padding: '4px 8px',
            backgroundColor: `${COLORS.earthEmber}30`,
            color: COLORS.earthEmber,
            borderRadius: '4px',
            fontSize: '11px',
            fontWeight: 600,
          }}>
            🟠 {mission.urgency.toUpperCase()}
          </span>
          {mission.project_id && (
            <span style={{
              padding: '4px 8px',
              backgroundColor: `${COLORS.sacredGold}30`,
              color: COLORS.sacredGold,
              borderRadius: '4px',
              fontSize: '11px',
            }}>
              📊 Linked to Project
            </span>
          )}
        </div>
        <h2 style={{
          margin: 0,
          fontSize: '18px',
          fontWeight: 700,
          color: COLORS.cenoteTurquoise,
        }}>
          {mission.name}
        </h2>
        <p style={{
          margin: '8px 0 0 0',
          fontSize: '13px',
          color: COLORS.ancientStone,
        }}>
          {mission.objective}
        </p>
      </div>
      
      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '8px',
        marginBottom: '20px',
        borderBottom: `1px solid ${COLORS.uiSlate}`,
        paddingBottom: '12px',
      }}>
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              padding: '8px 12px',
              backgroundColor: activeTab === tab.key ? COLORS.cenoteTurquoise : 'transparent',
              color: activeTab === tab.key ? COLORS.uiSlate : COLORS.softSand,
              border: 'none',
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {tab.emoji} {tab.label}
          </button>
        ))}
      </div>
      
      {/* Content */}
      <div style={{ minHeight: '300px' }}>
        {activeTab === 'overview' && <MissionOverviewTab mission={mission} />}
        {activeTab === 'objectives' && <ObjectivesTab objectives={mission.objectives} />}
        {activeTab === 'steps' && <StepsTab steps={mission.steps} />}
        {activeTab === 'timeline' && <TimelineTab timeline={mission.timeline} />}
        {activeTab === 'capabilities' && <CapabilitiesTab capabilities={mission.capability_map} />}
      </div>
    </div>
  );
}

// ============================================================
// TAB COMPONENTS
// ============================================================

function MissionOverviewTab({ mission }: { mission: typeof SAMPLE_MISSION_DETAIL }) {
  const completedSteps = mission.steps.filter(s => s.status === 'completed').length;
  const achievedObjectives = mission.objectives.filter(o => o.status === 'achieved').length;
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '12px',
      }}>
        <StatCard 
          label="Objectives" 
          value={`${achievedObjectives}/${mission.objectives.length}`} 
          color={COLORS.sacredGold} 
        />
        <StatCard 
          label="Steps" 
          value={`${completedSteps}/${mission.steps.length}`} 
          color={COLORS.cenoteTurquoise} 
        />
        <StatCard 
          label="Engines" 
          value={String(mission.capability_map.length)} 
          color={COLORS.jungleEmerald} 
        />
      </div>
      
      <div style={{
        padding: '16px',
        backgroundColor: `${COLORS.uiSlate}80`,
        borderRadius: '8px',
      }}>
        <h4 style={{ margin: '0 0 12px 0', color: COLORS.softSand, fontSize: '14px' }}>
          Mission Context
        </h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          <ContextTag label="Scope" value={mission.context.scope} />
          <ContextTag label="Domain" value={mission.context.domain_sphere} />
        </div>
        <p style={{
          margin: '12px 0 0 0',
          fontSize: '12px',
          color: COLORS.ancientStone,
          lineHeight: 1.5,
        }}>
          <strong>Success Definition:</strong> {mission.context.success_definition}
        </p>
      </div>
      
      {/* Progress */}
      <div style={{
        padding: '16px',
        backgroundColor: `${COLORS.uiSlate}80`,
        borderRadius: '8px',
      }}>
        <h4 style={{ margin: '0 0 12px 0', color: COLORS.softSand, fontSize: '14px' }}>
          Progress
        </h4>
        <ProgressBar label="Objectives" done={achievedObjectives} total={mission.objectives.length} />
        <ProgressBar label="Steps" done={completedSteps} total={mission.steps.length} />
      </div>
    </div>
  );
}

function ObjectivesTab({ objectives }: { objectives: typeof SAMPLE_MISSION_DETAIL.objectives }) {
  const priorityColors: Record<string, string> = {
    primary: COLORS.sacredGold,
    secondary: COLORS.cenoteTurquoise,
    optional: COLORS.ancientStone,
  };
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {objectives.map(obj => (
        <div key={obj.id} style={{
          padding: '16px',
          backgroundColor: `${COLORS.uiSlate}80`,
          borderRadius: '8px',
          borderLeft: `3px solid ${priorityColors[obj.priority]}`,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <span style={{ color: COLORS.softSand, fontWeight: 600, fontSize: '14px' }}>
              {obj.statement}
            </span>
            <span style={{
              padding: '4px 8px',
              backgroundColor: obj.status === 'achieved' ? `${COLORS.jungleEmerald}30` : `${COLORS.cenoteTurquoise}30`,
              color: obj.status === 'achieved' ? COLORS.jungleEmerald : COLORS.cenoteTurquoise,
              borderRadius: '4px',
              fontSize: '11px',
            }}>
              {obj.status}
            </span>
          </div>
          <div style={{ marginTop: '12px' }}>
            <span style={{ fontSize: '11px', color: COLORS.ancientStone }}>Key Results:</span>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '4px' }}>
              {obj.key_results.map((kr, idx) => (
                <span key={idx} style={{
                  padding: '2px 8px',
                  backgroundColor: `${COLORS.shadowMoss}`,
                  color: COLORS.softSand,
                  borderRadius: '4px',
                  fontSize: '11px',
                }}>
                  ✓ {kr}
                </span>
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function StepsTab({ steps }: { steps: typeof SAMPLE_MISSION_DETAIL.steps }) {
  const statusConfig: Record<string, { color: string; emoji: string }> = {
    completed: { color: COLORS.jungleEmerald, emoji: '✅' },
    active: { color: COLORS.cenoteTurquoise, emoji: '🔄' },
    pending: { color: COLORS.ancientStone, emoji: '⏳' },
  };
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {steps.map(step => {
        const config = statusConfig[step.status] || statusConfig.pending;
        return (
          <div key={step.id} style={{
            padding: '12px',
            backgroundColor: `${COLORS.uiSlate}80`,
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
          }}>
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: '50%',
              backgroundColor: step.status === 'completed' ? COLORS.jungleEmerald : COLORS.shadowMoss,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: COLORS.softSand,
              fontSize: '12px',
              fontWeight: 700,
            }}>
              {step.status === 'completed' ? '✓' : step.order}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ color: COLORS.softSand, fontSize: '14px' }}>{step.name}</div>
              <div style={{ color: COLORS.ancientStone, fontSize: '11px' }}>
                Engine: {step.engine}
              </div>
            </div>
            <span style={{
              padding: '4px 8px',
              backgroundColor: `${config.color}30`,
              color: config.color,
              borderRadius: '4px',
              fontSize: '11px',
            }}>
              {config.emoji} {step.status}
            </span>
          </div>
        );
      })}
    </div>
  );
}

function TimelineTab({ timeline }: { timeline: typeof SAMPLE_MISSION_DETAIL.timeline }) {
  return (
    <div style={{ position: 'relative', paddingLeft: '30px' }}>
      {/* Vertical line */}
      <div style={{
        position: 'absolute',
        left: '10px',
        top: '0',
        bottom: '0',
        width: '2px',
        backgroundColor: COLORS.shadowMoss,
      }} />
      
      {timeline.map((phase, idx) => (
        <div key={idx} style={{
          position: 'relative',
          marginBottom: '20px',
          paddingLeft: '20px',
        }}>
          {/* Dot */}
          <div style={{
            position: 'absolute',
            left: '-20px',
            top: '4px',
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: phase.status === 'completed' ? COLORS.jungleEmerald :
                           phase.status === 'active' ? COLORS.cenoteTurquoise : COLORS.shadowMoss,
            border: `2px solid ${COLORS.uiSlate}`,
          }} />
          
          <div style={{
            padding: '12px 16px',
            backgroundColor: `${COLORS.uiSlate}80`,
            borderRadius: '8px',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ color: COLORS.softSand, fontWeight: 600, fontSize: '14px' }}>
                {phase.phase}
              </span>
              <span style={{
                padding: '2px 8px',
                backgroundColor: phase.status === 'completed' ? `${COLORS.jungleEmerald}30` :
                               phase.status === 'active' ? `${COLORS.cenoteTurquoise}30` : `${COLORS.ancientStone}30`,
                color: phase.status === 'completed' ? COLORS.jungleEmerald :
                       phase.status === 'active' ? COLORS.cenoteTurquoise : COLORS.ancientStone,
                borderRadius: '4px',
                fontSize: '10px',
              }}>
                {phase.status}
              </span>
            </div>
            <span style={{ color: COLORS.ancientStone, fontSize: '11px' }}>
              Duration: {phase.duration}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

function CapabilitiesTab({ capabilities }: { capabilities: typeof SAMPLE_MISSION_DETAIL.capability_map }) {
  const levelColors: Record<string, string> = {
    essential: '#E53E3E',
    important: COLORS.earthEmber,
    helpful: COLORS.cenoteTurquoise,
  };
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {capabilities.map((cap, idx) => (
        <div key={idx} style={{
          padding: '12px',
          backgroundColor: `${COLORS.uiSlate}80`,
          borderRadius: '8px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
        }}>
          <span style={{
            fontSize: '20px',
          }}>
            ⚙️
          </span>
          <div style={{ flex: 1 }}>
            <div style={{ color: COLORS.softSand, fontWeight: 600, fontSize: '14px' }}>
              {cap.engine}
            </div>
            <div style={{ color: COLORS.ancientStone, fontSize: '11px' }}>
              {cap.reason}
            </div>
          </div>
          <span style={{
            padding: '4px 8px',
            backgroundColor: `${levelColors[cap.level]}30`,
            color: levelColors[cap.level],
            borderRadius: '4px',
            fontSize: '10px',
            fontWeight: 600,
          }}>
            {cap.level}
          </span>
        </div>
      ))}
    </div>
  );
}

// ============================================================
// HELPER COMPONENTS
// ============================================================

function StatCard({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div style={{
      padding: '16px',
      backgroundColor: `${COLORS.uiSlate}80`,
      borderRadius: '8px',
      textAlign: 'center',
    }}>
      <div style={{ fontSize: '20px', fontWeight: 700, color }}>{value}</div>
      <div style={{ fontSize: '12px', color: COLORS.ancientStone }}>{label}</div>
    </div>
  );
}

function ContextTag({ label, value }: { label: string; value: string }) {
  return (
    <span style={{
      padding: '4px 10px',
      backgroundColor: `${COLORS.cenoteTurquoise}20`,
      color: COLORS.cenoteTurquoise,
      borderRadius: '6px',
      fontSize: '11px',
    }}>
      {label}: {value}
    </span>
  );
}

function ProgressBar({ label, done, total }: { label: string; done: number; total: number }) {
  const percentage = total > 0 ? Math.round((done / total) * 100) : 0;
  
  return (
    <div style={{ marginBottom: '12px' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '4px',
      }}>
        <span style={{ fontSize: '12px', color: COLORS.softSand }}>{label}</span>
        <span style={{ fontSize: '12px', color: COLORS.ancientStone }}>{done}/{total}</span>
      </div>
      <div style={{
        height: '6px',
        backgroundColor: COLORS.uiSlate,
        borderRadius: '3px',
        overflow: 'hidden',
      }}>
        <div style={{
          width: `${percentage}%`,
          height: '100%',
          backgroundColor: COLORS.jungleEmerald,
          borderRadius: '3px',
        }} />
      </div>
    </div>
  );
}

export default MissionViewer;
