############################################################
#                                                          #
#       CHE·NU PROJECT & MISSION LAYER                     #
#       PART 6: API SERVICE & WORKFLOWGRID UPDATE          #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 11 — API SERVICE UPDATE
============================================================

--- FILE: /che-nu-api/services/chenu.service.ts
--- ACTION: UPDATE FILE (ADD PROJECT & MISSION ENDPOINTS)

/**
 * CHE·NU API — Main Service
 * ==========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * API service for CHE·NU platform operations.
 * All endpoints return representational data only.
 * 
 * @version 2.6.0
 */

import { Router, Request, Response } from 'express';

// Import engines
import * as ProjectEngine from '@che-nu-sdk/core/project';
import * as MissionEngine from '@che-nu-sdk/core/mission';
import * as GoalsEngine from '@che-nu-sdk/core/project/goals.engine';
import * as TasksEngine from '@che-nu-sdk/core/project/tasks.engine';
import * as MilestoneEngine from '@che-nu-sdk/core/project/milestone.engine';
import * as ResourcesEngine from '@che-nu-sdk/core/project/resources.engine';
import * as CapabilityEngine from '@che-nu-sdk/core/project/capability.engine';
import * as ObjectivesEngine from '@che-nu-sdk/core/mission/objectives.engine';
import * as StepsEngine from '@che-nu-sdk/core/mission/steps.engine';
import * as TimelineEngine from '@che-nu-sdk/core/mission/timeline.engine';
import * as CapabilityMapEngine from '@che-nu-sdk/core/mission/capability_map.engine';

// Import agent modules (from previous delivery)
import { 
  getAllTemplates, 
  getTemplateByName, 
  getTemplatesForSphere,
  getTemplatesUsingEngine 
} from '@che-nu-sdk/core/agent_templates';
import { 
  createAgentRegistry 
} from '@che-nu-sdk/core/agent_registry';

// ============================================================
// SERVICE CONFIGURATION
// ============================================================

const router = Router();

// Initialize agent registry
const agentRegistry = createAgentRegistry();
agentRegistry.registerAgents(getAllTemplates());

// In-memory storage for demo (representational only)
const projectStore: Map<string, ProjectEngine.ProjectModel> = new Map();
const missionStore: Map<string, MissionEngine.MissionModel> = new Map();

// ============================================================
// HEALTH & SYSTEM ENDPOINTS
// ============================================================

/**
 * GET /che-nu/health
 * Health check endpoint
 */
router.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'che-nu-api',
    version: '2.6.0',
    timestamp: new Date().toISOString(),
  });
});

/**
 * GET /che-nu/system
 * Returns system information
 */
router.get('/system', (req: Request, res: Response) => {
  res.json({
    name: 'CHE·NU API',
    version: '2.6.0',
    classification: 'SAFE · NON-AUTONOMOUS · REPRESENTATIONAL',
    modules: {
      core: 13,
      engines: 28,
      subEngines: 67,
      agentTemplates: 12,
      projectSubModules: 5,
      missionSubModules: 4,
    },
    layers: ['agentCapabilityLayer', 'projectMissionLayer'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  });
});

// ============================================================
// PROJECT ENDPOINTS
// ============================================================

/**
 * POST /che-nu/projects
 * Create a new project structure
 * REPRESENTATIONAL ONLY — no actual project creation
 */
router.post('/projects', (req: Request, res: Response) => {
  try {
    const { name, description, context, initial_goals } = req.body;
    
    if (!name || !description) {
      return res.status(400).json({
        success: false,
        error: 'Name and description are required',
      });
    }
    
    const project = ProjectEngine.createProject({
      name,
      description,
      context,
      initial_goals,
    });
    
    // Store in memory (demo only)
    projectStore.set(project.id, project);
    
    res.status(201).json({
      success: true,
      data: project,
      meta: {
        timestamp: new Date().toISOString(),
        safe: {
          isRepresentational: true,
          noAutonomy: true,
          note: 'This is a representational structure only',
        },
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to create project structure',
    });
  }
});

/**
 * GET /che-nu/projects
 * List all project structures
 */
router.get('/projects', (req: Request, res: Response) => {
  try {
    const projects = Array.from(projectStore.values());
    
    res.json({
      success: true,
      data: projects,
      meta: {
        count: projects.length,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve projects',
    });
  }
});

/**
 * GET /che-nu/projects/:id
 * Get specific project structure
 */
router.get('/projects/:id', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const project = projectStore.get(id);
    
    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${id}' not found`,
      });
    }
    
    res.json({
      success: true,
      data: project,
      meta: {
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve project',
    });
  }
});

/**
 * GET /che-nu/projects/:id/summary
 * Get project summary
 */
router.get('/projects/:id/summary', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const project = projectStore.get(id);
    
    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${id}' not found`,
      });
    }
    
    const summary = ProjectEngine.summarizeProject(project);
    
    res.json({
      success: true,
      data: summary,
      meta: {
        project_id: id,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to generate project summary',
    });
  }
});

/**
 * GET /che-nu/projects/:id/capabilities
 * Get capability mapping for project
 */
router.get('/projects/:id/capabilities', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const project = projectStore.get(id);
    
    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${id}' not found`,
      });
    }
    
    const capabilities = ProjectEngine.mapCapabilitiesToProject(project);
    
    res.json({
      success: true,
      data: capabilities,
      meta: {
        project_id: id,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to generate capability mapping',
    });
  }
});

/**
 * POST /che-nu/projects/:id/goals
 * Add goal to project
 */
router.post('/projects/:id/goals', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const project = projectStore.get(id);
    
    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${id}' not found`,
      });
    }
    
    const { title, description, priority, related_engines } = req.body;
    
    ProjectEngine.addGoal(project, {
      title,
      description,
      priority: priority || 'medium',
      related_engines: related_engines || [],
    });
    
    res.status(201).json({
      success: true,
      data: project,
      meta: {
        action: 'goal_added',
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to add goal',
    });
  }
});

/**
 * POST /che-nu/projects/:id/tasks
 * Add task to project
 */
router.post('/projects/:id/tasks', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const project = projectStore.get(id);
    
    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${id}' not found`,
      });
    }
    
    const { name, details, complexity, dependencies, assigned_engine } = req.body;
    
    ProjectEngine.addTask(project, {
      name,
      details,
      complexity: complexity || 'moderate',
      dependencies: dependencies || [],
      assigned_engine,
    });
    
    res.status(201).json({
      success: true,
      data: project,
      meta: {
        action: 'task_added',
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to add task',
    });
  }
});

/**
 * POST /che-nu/projects/:id/milestones
 * Add milestone to project
 */
router.post('/projects/:id/milestones', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const project = projectStore.get(id);
    
    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${id}' not found`,
      });
    }
    
    const { name, marker, due, criteria } = req.body;
    
    ProjectEngine.addMilestone(project, {
      name,
      marker,
      due,
      criteria: criteria || [],
    });
    
    res.status(201).json({
      success: true,
      data: project,
      meta: {
        action: 'milestone_added',
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to add milestone',
    });
  }
});

// ============================================================
// MISSION ENDPOINTS
// ============================================================

/**
 * POST /che-nu/missions
 * Create a new mission structure
 * REPRESENTATIONAL ONLY — no actual mission execution
 */
router.post('/missions', (req: Request, res: Response) => {
  try {
    const { name, objective, urgency, scope, domain_sphere, project_id } = req.body;
    
    if (!name || !objective) {
      return res.status(400).json({
        success: false,
        error: 'Name and objective are required',
      });
    }
    
    const mission = MissionEngine.createMission({
      name,
      objective,
      urgency,
      scope,
      domain_sphere,
      project_id,
    });
    
    // Store in memory (demo only)
    missionStore.set(mission.id, mission);
    
    // Link to project if specified
    if (project_id && projectStore.has(project_id)) {
      const project = projectStore.get(project_id)!;
      ProjectEngine.linkMission(project, mission.id);
    }
    
    res.status(201).json({
      success: true,
      data: mission,
      meta: {
        timestamp: new Date().toISOString(),
        safe: {
          isRepresentational: true,
          noAutonomy: true,
          note: 'This is a representational structure only',
        },
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to create mission structure',
    });
  }
});

/**
 * GET /che-nu/missions
 * List all mission structures
 */
router.get('/missions', (req: Request, res: Response) => {
  try {
    const missions = Array.from(missionStore.values());
    
    res.json({
      success: true,
      data: missions,
      meta: {
        count: missions.length,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve missions',
    });
  }
});

/**
 * GET /che-nu/missions/:id
 * Get specific mission structure
 */
router.get('/missions/:id', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const mission = missionStore.get(id);
    
    if (!mission) {
      return res.status(404).json({
        success: false,
        error: `Mission '${id}' not found`,
      });
    }
    
    res.json({
      success: true,
      data: mission,
      meta: {
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve mission',
    });
  }
});

/**
 * GET /che-nu/missions/:id/summary
 * Get mission summary
 */
router.get('/missions/:id/summary', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const mission = missionStore.get(id);
    
    if (!mission) {
      return res.status(404).json({
        success: false,
        error: `Mission '${id}' not found`,
      });
    }
    
    const summary = MissionEngine.summarizeMission(mission);
    
    res.json({
      success: true,
      data: summary,
      meta: {
        mission_id: id,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to generate mission summary',
    });
  }
});

/**
 * GET /che-nu/missions/:id/capabilities
 * Get capability analysis for mission
 */
router.get('/missions/:id/capabilities', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const mission = missionStore.get(id);
    
    if (!mission) {
      return res.status(404).json({
        success: false,
        error: `Mission '${id}' not found`,
      });
    }
    
    const capabilities = MissionEngine.missionCapabilities(mission);
    
    res.json({
      success: true,
      data: capabilities,
      meta: {
        mission_id: id,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to generate capability analysis',
    });
  }
});

/**
 * POST /che-nu/missions/:id/objectives
 * Add objectives to mission
 */
router.post('/missions/:id/objectives', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const mission = missionStore.get(id);
    
    if (!mission) {
      return res.status(404).json({
        success: false,
        error: `Mission '${id}' not found`,
      });
    }
    
    const { objectives } = req.body;
    
    if (!Array.isArray(objectives)) {
      return res.status(400).json({
        success: false,
        error: 'Objectives must be an array',
      });
    }
    
    MissionEngine.defineObjectives(mission, objectives);
    
    res.status(201).json({
      success: true,
      data: mission,
      meta: {
        action: 'objectives_added',
        count: objectives.length,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to add objectives',
    });
  }
});

/**
 * POST /che-nu/missions/:id/steps
 * Add steps to mission
 */
router.post('/missions/:id/steps', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const mission = missionStore.get(id);
    
    if (!mission) {
      return res.status(404).json({
        success: false,
        error: `Mission '${id}' not found`,
      });
    }
    
    const { steps } = req.body;
    
    if (!Array.isArray(steps)) {
      return res.status(400).json({
        success: false,
        error: 'Steps must be an array',
      });
    }
    
    MissionEngine.defineSteps(mission, steps);
    
    res.status(201).json({
      success: true,
      data: mission,
      meta: {
        action: 'steps_added',
        count: steps.length,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to add steps',
    });
  }
});

/**
 * POST /che-nu/missions/:id/timeline
 * Generate timeline for mission
 */
router.post('/missions/:id/timeline', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const mission = missionStore.get(id);
    
    if (!mission) {
      return res.status(404).json({
        success: false,
        error: `Mission '${id}' not found`,
      });
    }
    
    MissionEngine.missionTimeline(mission);
    
    res.json({
      success: true,
      data: mission,
      meta: {
        action: 'timeline_generated',
        phases: mission.timeline.length,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to generate timeline',
    });
  }
});

/**
 * POST /che-nu/missions/:id/link-project
 * Link mission to a project
 */
router.post('/missions/:id/link-project', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { project_id } = req.body;
    
    const mission = missionStore.get(id);
    if (!mission) {
      return res.status(404).json({
        success: false,
        error: `Mission '${id}' not found`,
      });
    }
    
    const project = projectStore.get(project_id);
    if (!project) {
      return res.status(404).json({
        success: false,
        error: `Project '${project_id}' not found`,
      });
    }
    
    MissionEngine.linkProject(mission, project_id);
    ProjectEngine.linkMission(project, id);
    
    res.json({
      success: true,
      data: {
        mission_id: id,
        project_id: project_id,
        linked: true,
      },
      meta: {
        action: 'project_linked',
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to link project',
    });
  }
});

// ============================================================
// AGENT ENDPOINTS (preserved from previous delivery)
// ============================================================

/**
 * GET /che-nu/agents
 * Returns list of all agent templates
 */
router.get('/agents', (req: Request, res: Response) => {
  try {
    const agents = agentRegistry.listAgents();
    
    res.json({
      success: true,
      data: agents,
      meta: {
        count: agents.length,
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve agents',
    });
  }
});

/**
 * GET /che-nu/agents/:name
 * Returns specific agent template by name
 */
router.get('/agents/:name', (req: Request, res: Response) => {
  try {
    const { name } = req.params;
    const agent = getTemplateByName(decodeURIComponent(name));
    
    if (!agent) {
      return res.status(404).json({
        success: false,
        error: `Agent '${name}' not found`,
      });
    }
    
    res.json({
      success: true,
      data: agent,
      meta: {
        timestamp: new Date().toISOString(),
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve agent',
    });
  }
});

// ============================================================
// EXPORT
// ============================================================

export const chenuService = router;
export default chenuService;

============================================================
SECTION 9 (CONTINUED) — WORKFLOWGRID UPDATE
============================================================

--- FILE: /che-nu-frontend/components/WorkflowGrid.tsx
--- ACTION: UPDATE FILE (ADD PROJECT & MISSION BUTTONS)

/**
 * CHE·NU Frontend — Workflow Grid Component
 * ==========================================
 * UPDATED: Added Project Tools and Mission Tools buttons
 * 
 * @version 2.6.0
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';

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

interface QuickAction {
  id: string;
  label: string;
  icon: string;
  route: string;
  description: string;
  color: string;
  category: 'navigation' | 'tools' | 'layer';
}

// ============================================================
// QUICK ACTIONS DATA
// ============================================================

const quickActions: QuickAction[] = [
  // Navigation
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: '📊',
    route: '/',
    description: 'Main overview',
    color: COLORS.sacredGold,
    category: 'navigation',
  },
  {
    id: 'workspaces',
    label: 'Workspaces',
    icon: '🏠',
    route: '/workspaces',
    description: 'Domain workspaces',
    color: COLORS.jungleEmerald,
    category: 'navigation',
  },
  
  // Tools
  {
    id: 'workflows',
    label: 'Workflows',
    icon: '⚡',
    route: '/workflows',
    description: 'Build workflows',
    color: COLORS.cenoteTurquoise,
    category: 'tools',
  },
  {
    id: 'engines',
    label: 'Engine Explorer',
    icon: '⚙️',
    route: '/engines',
    description: 'Browse engines',
    color: COLORS.ancientStone,
    category: 'tools',
  },
  {
    id: 'memory',
    label: 'Memory System',
    icon: '🧠',
    route: '/memory',
    description: 'External memory',
    color: COLORS.shadowMoss,
    category: 'tools',
  },
  {
    id: 'xr',
    label: 'XR Builder',
    icon: '🥽',
    route: '/xr',
    description: 'XR scene design',
    color: COLORS.cenoteTurquoise,
    category: 'tools',
  },
  
  // Capability Layers
  {
    id: 'agents',
    label: 'Agent Dashboard',
    icon: '🤖',
    route: '/agents',
    description: 'Agent capabilities',
    color: COLORS.sacredGold,
    category: 'layer',
  },
  {
    id: 'projects',
    label: 'Project Tools',
    icon: '📋',
    route: '/projects',
    description: 'Project structures',
    color: COLORS.sacredGold,
    category: 'layer',
  },
  {
    id: 'missions',
    label: 'Mission Tools',
    icon: '🎯',
    route: '/missions',
    description: 'Mission planning',
    color: COLORS.cenoteTurquoise,
    category: 'layer',
  },
  
  // Settings
  {
    id: 'settings',
    label: 'Settings',
    icon: '⚙️',
    route: '/settings',
    description: 'Configuration',
    color: COLORS.ancientStone,
    category: 'navigation',
  },
];

// ============================================================
// COMPONENTS
// ============================================================

interface ActionButtonProps {
  action: QuickAction;
  onClick: () => void;
}

function ActionButton({ action, onClick }: ActionButtonProps) {
  const [isHovered, setIsHovered] = React.useState(false);
  
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px 16px',
        backgroundColor: COLORS.shadowMoss,
        border: `2px solid ${isHovered ? action.color : 'transparent'}`,
        borderRadius: '12px',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        transform: isHovered ? 'translateY(-2px)' : 'translateY(0)',
        boxShadow: isHovered ? `0 4px 12px ${action.color}30` : 'none',
      }}
    >
      <span style={{ fontSize: '28px', marginBottom: '8px' }}>
        {action.icon}
      </span>
      <span style={{
        fontSize: '14px',
        fontWeight: 600,
        color: COLORS.softSand,
        marginBottom: '4px',
      }}>
        {action.label}
      </span>
      <span style={{
        fontSize: '11px',
        color: COLORS.ancientStone,
      }}>
        {action.description}
      </span>
    </button>
  );
}

interface CategorySectionProps {
  title: string;
  actions: QuickAction[];
  onActionClick: (route: string) => void;
}

function CategorySection({ title, actions, onActionClick }: CategorySectionProps) {
  if (actions.length === 0) return null;
  
  return (
    <div style={{ marginBottom: '24px' }}>
      <h3 style={{
        margin: '0 0 12px 0',
        fontSize: '14px',
        fontWeight: 600,
        color: COLORS.ancientStone,
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
      }}>
        {title}
      </h3>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))',
        gap: '12px',
      }}>
        {actions.map((action) => (
          <ActionButton
            key={action.id}
            action={action}
            onClick={() => onActionClick(action.route)}
          />
        ))}
      </div>
    </div>
  );
}

// ============================================================
// MAIN COMPONENT
// ============================================================

export function WorkflowGrid() {
  const navigate = useNavigate();
  
  const handleActionClick = (route: string) => {
    navigate(route);
  };
  
  // Group actions by category
  const navigationActions = quickActions.filter(a => a.category === 'navigation');
  const toolsActions = quickActions.filter(a => a.category === 'tools');
  const layerActions = quickActions.filter(a => a.category === 'layer');
  
  return (
    <div style={{
      padding: '24px',
    }}>
      <h2 style={{
        margin: '0 0 24px 0',
        fontSize: '20px',
        fontWeight: 700,
        color: COLORS.softSand,
      }}>
        Quick Actions
      </h2>
      
      {/* Navigation */}
      <CategorySection
        title="Navigation"
        actions={navigationActions}
        onActionClick={handleActionClick}
      />
      
      {/* Capability Layers */}
      <CategorySection
        title="Capability Layers"
        actions={layerActions}
        onActionClick={handleActionClick}
      />
      
      {/* Tools */}
      <CategorySection
        title="Tools"
        actions={toolsActions}
        onActionClick={handleActionClick}
      />
      
      {/* SAFE Notice */}
      <div style={{
        marginTop: '24px',
        padding: '12px 16px',
        backgroundColor: `${COLORS.jungleEmerald}15`,
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
      }}>
        <span style={{ fontSize: '16px' }}>🔒</span>
        <span style={{
          fontSize: '12px',
          color: COLORS.jungleEmerald,
        }}>
          SAFE · NON-AUTONOMOUS · All actions are user-initiated and representational only
        </span>
      </div>
      
      {/* Layer Status */}
      <div style={{
        marginTop: '16px',
        padding: '16px',
        backgroundColor: `${COLORS.uiSlate}80`,
        borderRadius: '8px',
      }}>
        <h4 style={{
          margin: '0 0 12px 0',
          fontSize: '13px',
          fontWeight: 600,
          color: COLORS.softSand,
        }}>
          Active Layers
        </h4>
        <div style={{
          display: 'flex',
          gap: '8px',
          flexWrap: 'wrap',
        }}>
          <LayerBadge name="Agent Capability" color={COLORS.sacredGold} />
          <LayerBadge name="Project & Mission" color={COLORS.cenoteTurquoise} />
          <LayerBadge name="XR Suite" color={COLORS.jungleEmerald} />
          <LayerBadge name="Memory System" color={COLORS.shadowMoss} />
        </div>
      </div>
    </div>
  );
}

interface LayerBadgeProps {
  name: string;
  color: string;
}

function LayerBadge({ name, color }: LayerBadgeProps) {
  return (
    <span style={{
      padding: '6px 12px',
      backgroundColor: `${color}20`,
      color: color,
      borderRadius: '6px',
      fontSize: '11px',
      fontWeight: 600,
    }}>
      ✓ {name}
    </span>
  );
}

export default WorkflowGrid;
