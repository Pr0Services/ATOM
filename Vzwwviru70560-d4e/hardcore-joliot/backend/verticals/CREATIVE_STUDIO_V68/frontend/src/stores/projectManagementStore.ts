/**
 * CHE·NU™ V68 - Project Management Store
 * Zustand state management for PM features
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ============================================================================
// TYPES
// ============================================================================

export type ProjectStatus = 'planning' | 'active' | 'on_hold' | 'completed' | 'cancelled' | 'archived';
export type TaskStatus = 'backlog' | 'todo' | 'in_progress' | 'in_review' | 'blocked' | 'done';
export type TaskPriority = 'critical' | 'high' | 'medium' | 'low';
export type SprintStatus = 'planned' | 'active' | 'completed';
export type MilestoneStatus = 'upcoming' | 'in_progress' | 'completed' | 'missed';
export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export interface Project {
  id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  start_date: string | null;
  target_date: string | null;
  budget: number | null;
  spent: number;
  client_name: string | null;
  tags: string[];
  settings: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  project_id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  assignee_id: string | null;
  assignee_name: string | null;
  sprint_id: string | null;
  milestone_id: string | null;
  parent_task_id: string | null;
  due_date: string | null;
  estimated_hours: number | null;
  actual_hours: number;
  tags: string[];
  checklist: ChecklistItem[];
  order: number;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface ChecklistItem {
  id: string;
  text: string;
  completed: boolean;
}

export interface Sprint {
  id: string;
  project_id: string;
  name: string;
  goal: string;
  status: SprintStatus;
  start_date: string;
  end_date: string;
  velocity_planned: number;
  velocity_actual: number;
  created_at: string;
}

export interface Milestone {
  id: string;
  project_id: string;
  name: string;
  description: string;
  status: MilestoneStatus;
  due_date: string;
  completed_date: string | null;
  deliverables: string[];
  created_at: string;
}

export interface TimeEntry {
  id: string;
  task_id: string;
  user_id: string;
  hours: number;
  description: string;
  date: string;
  billable: boolean;
  created_at: string;
}

export interface TeamMember {
  id: string;
  project_id: string;
  name: string;
  email: string;
  role: string;
  hourly_rate: number | null;
  capacity_hours_week: number;
  joined_at: string;
}

export interface Comment {
  id: string;
  task_id: string;
  author_name: string;
  content: string;
  mentions: string[];
  created_at: string;
  updated_at: string;
}

export interface ProjectAnalysis {
  project_id: string;
  health_score: number;
  risk_level: RiskLevel;
  completion_percentage: number;
  estimated_completion_date: string | null;
  budget_status: string;
  velocity_trend: string;
  risks: any[];
  recommendations: string[];
  blockers: any[];
  workload_balance: any;
  generated_at: string;
}

export interface TaskEstimate {
  task_id: string;
  estimated_hours: number;
  confidence: number;
  similar_tasks: any[];
  factors: string[];
  generated_at: string;
}

export interface Dashboard {
  projects: {
    total: number;
    active: number;
    completed: number;
  };
  tasks: {
    total: number;
    by_status: Record<TaskStatus, number>;
    overdue: number;
    due_this_week: number;
  };
  time: {
    hours_this_week: number;
    entries_this_week: number;
  };
  recent_projects: { id: string; name: string; status: string }[];
}

export interface KanbanBoard {
  backlog: Task[];
  todo: Task[];
  in_progress: Task[];
  in_review: Task[];
  blocked: Task[];
  done: Task[];
}

// ============================================================================
// STORE STATE
// ============================================================================

interface ProjectManagementState {
  // Data
  projects: Project[];
  tasks: Task[];
  sprints: Sprint[];
  milestones: Milestone[];
  timeEntries: TimeEntry[];
  team: TeamMember[];
  comments: Comment[];
  dashboard: Dashboard | null;
  
  // Selected items
  selectedProject: Project | null;
  selectedTask: Task | null;
  selectedSprint: Sprint | null;
  
  // Analysis
  projectAnalysis: ProjectAnalysis | null;
  taskEstimate: TaskEstimate | null;
  kanbanBoard: KanbanBoard | null;
  
  // UI State
  activeTab: 'projects' | 'tasks' | 'kanban' | 'sprints' | 'milestones' | 'time' | 'team';
  isLoading: boolean;
  error: string | null;
  
  // Actions - Projects
  fetchProjects: (status?: ProjectStatus, search?: string) => Promise<void>;
  fetchProject: (projectId: string) => Promise<void>;
  createProject: (data: Partial<Project>) => Promise<Project>;
  updateProject: (projectId: string, data: Partial<Project>) => Promise<void>;
  analyzeProject: (projectId: string) => Promise<void>;
  
  // Actions - Tasks
  fetchTasks: (projectId: string, filters?: any) => Promise<void>;
  fetchTask: (projectId: string, taskId: string) => Promise<void>;
  createTask: (projectId: string, data: Partial<Task>) => Promise<Task>;
  updateTask: (projectId: string, taskId: string, data: Partial<Task>) => Promise<void>;
  moveTask: (projectId: string, taskId: string, status: TaskStatus, order?: number) => Promise<void>;
  estimateTask: (projectId: string, taskId: string) => Promise<void>;
  fetchKanban: (projectId: string) => Promise<void>;
  
  // Actions - Sprints
  fetchSprints: (projectId: string) => Promise<void>;
  createSprint: (projectId: string, data: Partial<Sprint>) => Promise<Sprint>;
  updateSprint: (projectId: string, sprintId: string, data: Partial<Sprint>) => Promise<void>;
  startSprint: (projectId: string, sprintId: string) => Promise<void>;
  completeSprint: (projectId: string, sprintId: string) => Promise<void>;
  
  // Actions - Milestones
  fetchMilestones: (projectId: string) => Promise<void>;
  createMilestone: (projectId: string, data: Partial<Milestone>) => Promise<Milestone>;
  completeMilestone: (projectId: string, milestoneId: string) => Promise<void>;
  
  // Actions - Time Tracking
  fetchTimeEntries: (projectId: string, filters?: any) => Promise<void>;
  logTime: (projectId: string, taskId: string, data: { hours: number; description?: string; billable?: boolean }) => Promise<void>;
  
  // Actions - Team
  fetchTeam: (projectId: string) => Promise<void>;
  addTeamMember: (projectId: string, data: Partial<TeamMember>) => Promise<TeamMember>;
  removeTeamMember: (projectId: string, memberId: string) => Promise<void>;
  
  // Actions - Comments
  fetchComments: (projectId: string, taskId: string) => Promise<void>;
  addComment: (projectId: string, taskId: string, data: { author_name: string; content: string; mentions?: string[] }) => Promise<void>;
  
  // Actions - Dashboard
  fetchDashboard: () => Promise<void>;
  
  // UI Actions
  setActiveTab: (tab: ProjectManagementState['activeTab']) => void;
  setSelectedProject: (project: Project | null) => void;
  setSelectedTask: (task: Task | null) => void;
  clearError: () => void;
}

// ============================================================================
// API HELPERS
// ============================================================================

const API_BASE = '/api/v2/projects';

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }
  
  return response.json();
}

// ============================================================================
// STORE
// ============================================================================

export const useProjectManagementStore = create<ProjectManagementState>()(
  persist(
    (set, get) => ({
      // Initial state
      projects: [],
      tasks: [],
      sprints: [],
      milestones: [],
      timeEntries: [],
      team: [],
      comments: [],
      dashboard: null,
      
      selectedProject: null,
      selectedTask: null,
      selectedSprint: null,
      
      projectAnalysis: null,
      taskEstimate: null,
      kanbanBoard: null,
      
      activeTab: 'projects',
      isLoading: false,
      error: null,
      
      // ======================================================================
      // PROJECT ACTIONS
      // ======================================================================
      
      fetchProjects: async (status, search) => {
        set({ isLoading: true, error: null });
        try {
          const params = new URLSearchParams();
          if (status) params.append('status', status);
          if (search) params.append('search', search);
          
          const query = params.toString();
          const { projects } = await apiRequest<{ projects: Project[] }>(
            `/?${query}`
          );
          set({ projects, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      fetchProject: async (projectId) => {
        set({ isLoading: true, error: null });
        try {
          const { project } = await apiRequest<{ project: Project }>(
            `/${projectId}`
          );
          set({ selectedProject: project, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      createProject: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const { project } = await apiRequest<{ project: Project }>('/', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set((state) => ({
            projects: [project, ...state.projects],
            isLoading: false,
          }));
          return project;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },
      
      updateProject: async (projectId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { project } = await apiRequest<{ project: Project }>(
            `/${projectId}`,
            {
              method: 'PUT',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            projects: state.projects.map((p) =>
              p.id === projectId ? project : p
            ),
            selectedProject:
              state.selectedProject?.id === projectId
                ? project
                : state.selectedProject,
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      analyzeProject: async (projectId) => {
        set({ isLoading: true, error: null });
        try {
          const { analysis } = await apiRequest<{ analysis: ProjectAnalysis }>(
            `/${projectId}/analyze`,
            { method: 'POST' }
          );
          set({ projectAnalysis: analysis, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // TASK ACTIONS
      // ======================================================================
      
      fetchTasks: async (projectId, filters) => {
        set({ isLoading: true, error: null });
        try {
          const params = new URLSearchParams();
          if (filters?.status) params.append('status', filters.status);
          if (filters?.assignee_id) params.append('assignee_id', filters.assignee_id);
          if (filters?.sprint_id) params.append('sprint_id', filters.sprint_id);
          if (filters?.priority) params.append('priority', filters.priority);
          
          const query = params.toString();
          const { tasks } = await apiRequest<{ tasks: Task[] }>(
            `/${projectId}/tasks?${query}`
          );
          set({ tasks, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      fetchTask: async (projectId, taskId) => {
        set({ isLoading: true, error: null });
        try {
          const { task } = await apiRequest<{ task: Task }>(
            `/${projectId}/tasks/${taskId}`
          );
          set({ selectedTask: task, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      createTask: async (projectId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { task } = await apiRequest<{ task: Task }>(
            `/${projectId}/tasks`,
            {
              method: 'POST',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            tasks: [...state.tasks, task],
            isLoading: false,
          }));
          return task;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },
      
      updateTask: async (projectId, taskId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { task } = await apiRequest<{ task: Task }>(
            `/${projectId}/tasks/${taskId}`,
            {
              method: 'PUT',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            tasks: state.tasks.map((t) => (t.id === taskId ? task : t)),
            selectedTask:
              state.selectedTask?.id === taskId ? task : state.selectedTask,
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      moveTask: async (projectId, taskId, status, order) => {
        set({ isLoading: true, error: null });
        try {
          const { task } = await apiRequest<{ task: Task }>(
            `/${projectId}/tasks/${taskId}/move`,
            {
              method: 'POST',
              body: JSON.stringify({ status, order }),
            }
          );
          set((state) => ({
            tasks: state.tasks.map((t) => (t.id === taskId ? task : t)),
            isLoading: false,
          }));
          // Refresh kanban if active
          if (get().activeTab === 'kanban') {
            get().fetchKanban(projectId);
          }
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      estimateTask: async (projectId, taskId) => {
        set({ isLoading: true, error: null });
        try {
          const { estimate } = await apiRequest<{ estimate: TaskEstimate }>(
            `/${projectId}/tasks/${taskId}/estimate`,
            { method: 'POST' }
          );
          set({ taskEstimate: estimate, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      fetchKanban: async (projectId) => {
        set({ isLoading: true, error: null });
        try {
          const { kanban } = await apiRequest<{ kanban: KanbanBoard }>(
            `/${projectId}/kanban`
          );
          set({ kanbanBoard: kanban, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // SPRINT ACTIONS
      // ======================================================================
      
      fetchSprints: async (projectId) => {
        set({ isLoading: true, error: null });
        try {
          const { sprints } = await apiRequest<{ sprints: Sprint[] }>(
            `/${projectId}/sprints`
          );
          set({ sprints, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      createSprint: async (projectId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { sprint } = await apiRequest<{ sprint: Sprint }>(
            `/${projectId}/sprints`,
            {
              method: 'POST',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            sprints: [...state.sprints, sprint],
            isLoading: false,
          }));
          return sprint;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },
      
      updateSprint: async (projectId, sprintId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { sprint } = await apiRequest<{ sprint: Sprint }>(
            `/${projectId}/sprints/${sprintId}`,
            {
              method: 'PUT',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            sprints: state.sprints.map((s) => (s.id === sprintId ? sprint : s)),
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      startSprint: async (projectId, sprintId) => {
        set({ isLoading: true, error: null });
        try {
          const { sprint } = await apiRequest<{ sprint: Sprint }>(
            `/${projectId}/sprints/${sprintId}/start`,
            { method: 'POST' }
          );
          set((state) => ({
            sprints: state.sprints.map((s) => (s.id === sprintId ? sprint : s)),
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      completeSprint: async (projectId, sprintId) => {
        set({ isLoading: true, error: null });
        try {
          const { sprint } = await apiRequest<{ sprint: Sprint }>(
            `/${projectId}/sprints/${sprintId}/complete`,
            { method: 'POST' }
          );
          set((state) => ({
            sprints: state.sprints.map((s) => (s.id === sprintId ? sprint : s)),
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // MILESTONE ACTIONS
      // ======================================================================
      
      fetchMilestones: async (projectId) => {
        set({ isLoading: true, error: null });
        try {
          const { milestones } = await apiRequest<{ milestones: Milestone[] }>(
            `/${projectId}/milestones`
          );
          set({ milestones, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      createMilestone: async (projectId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { milestone } = await apiRequest<{ milestone: Milestone }>(
            `/${projectId}/milestones`,
            {
              method: 'POST',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            milestones: [...state.milestones, milestone],
            isLoading: false,
          }));
          return milestone;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },
      
      completeMilestone: async (projectId, milestoneId) => {
        set({ isLoading: true, error: null });
        try {
          const { milestone } = await apiRequest<{ milestone: Milestone }>(
            `/${projectId}/milestones/${milestoneId}/complete`,
            { method: 'POST' }
          );
          set((state) => ({
            milestones: state.milestones.map((m) =>
              m.id === milestoneId ? milestone : m
            ),
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // TIME TRACKING ACTIONS
      // ======================================================================
      
      fetchTimeEntries: async (projectId, filters) => {
        set({ isLoading: true, error: null });
        try {
          const params = new URLSearchParams();
          if (filters?.task_id) params.append('task_id', filters.task_id);
          if (filters?.start_date) params.append('start_date', filters.start_date);
          if (filters?.end_date) params.append('end_date', filters.end_date);
          
          const query = params.toString();
          const { time_entries } = await apiRequest<{ time_entries: TimeEntry[] }>(
            `/${projectId}/time-entries?${query}`
          );
          set({ timeEntries: time_entries, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      logTime: async (projectId, taskId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { time_entry } = await apiRequest<{ time_entry: TimeEntry }>(
            `/${projectId}/tasks/${taskId}/time`,
            {
              method: 'POST',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            timeEntries: [time_entry, ...state.timeEntries],
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // TEAM ACTIONS
      // ======================================================================
      
      fetchTeam: async (projectId) => {
        set({ isLoading: true, error: null });
        try {
          const { team_members } = await apiRequest<{ team_members: TeamMember[] }>(
            `/${projectId}/team`
          );
          set({ team: team_members, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      addTeamMember: async (projectId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { team_member } = await apiRequest<{ team_member: TeamMember }>(
            `/${projectId}/team`,
            {
              method: 'POST',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            team: [...state.team, team_member],
            isLoading: false,
          }));
          return team_member;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },
      
      removeTeamMember: async (projectId, memberId) => {
        set({ isLoading: true, error: null });
        try {
          await apiRequest(`/${projectId}/team/${memberId}`, {
            method: 'DELETE',
          });
          set((state) => ({
            team: state.team.filter((m) => m.id !== memberId),
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // COMMENT ACTIONS
      // ======================================================================
      
      fetchComments: async (projectId, taskId) => {
        set({ isLoading: true, error: null });
        try {
          const { comments } = await apiRequest<{ comments: Comment[] }>(
            `/${projectId}/tasks/${taskId}/comments`
          );
          set({ comments, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      addComment: async (projectId, taskId, data) => {
        set({ isLoading: true, error: null });
        try {
          const { comment } = await apiRequest<{ comment: Comment }>(
            `/${projectId}/tasks/${taskId}/comments`,
            {
              method: 'POST',
              body: JSON.stringify(data),
            }
          );
          set((state) => ({
            comments: [...state.comments, comment],
            isLoading: false,
          }));
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // DASHBOARD ACTIONS
      // ======================================================================
      
      fetchDashboard: async () => {
        set({ isLoading: true, error: null });
        try {
          const { dashboard } = await apiRequest<{ dashboard: Dashboard }>(
            '/dashboard'
          );
          set({ dashboard, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // ======================================================================
      // UI ACTIONS
      // ======================================================================
      
      setActiveTab: (tab) => set({ activeTab: tab }),
      setSelectedProject: (project) => set({ selectedProject: project }),
      setSelectedTask: (task) => set({ selectedTask: task }),
      clearError: () => set({ error: null }),
    }),
    {
      name: 'chenu-project-management',
      partialize: (state) => ({
        activeTab: state.activeTab,
      }),
    }
  )
);

export default useProjectManagementStore;
