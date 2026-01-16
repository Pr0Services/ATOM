/**
 * CHE·NU™ V68 - Project Management Page
 * Complete PM interface with Kanban, Sprints, Time Tracking
 */

import React, { useEffect, useState } from 'react';
import { useProjectManagementStore } from '../../../stores/projectManagementStore';
import type {
  Project, Task, Sprint, Milestone, TeamMember, TimeEntry,
  ProjectStatus, TaskStatus, TaskPriority, SprintStatus, MilestoneStatus, RiskLevel
} from '../../../stores/projectManagementStore';

// ============================================================================
// BADGE COMPONENTS
// ============================================================================

const StatusBadge: React.FC<{ status: ProjectStatus }> = ({ status }) => {
  const colors: Record<ProjectStatus, string> = {
    planning: 'bg-gray-100 text-gray-800',
    active: 'bg-green-100 text-green-800',
    on_hold: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-blue-100 text-blue-800',
    cancelled: 'bg-red-100 text-red-800',
    archived: 'bg-gray-200 text-gray-600',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
      {status.replace('_', ' ')}
    </span>
  );
};

const TaskStatusBadge: React.FC<{ status: TaskStatus }> = ({ status }) => {
  const colors: Record<TaskStatus, string> = {
    backlog: 'bg-gray-100 text-gray-800',
    todo: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    in_review: 'bg-purple-100 text-purple-800',
    blocked: 'bg-red-100 text-red-800',
    done: 'bg-green-100 text-green-800',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
      {status.replace('_', ' ')}
    </span>
  );
};

const PriorityBadge: React.FC<{ priority: TaskPriority }> = ({ priority }) => {
  const colors: Record<TaskPriority, string> = {
    critical: 'bg-red-500 text-white',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-blue-100 text-blue-800',
    low: 'bg-gray-100 text-gray-800',
  };
  const icons: Record<TaskPriority, string> = {
    critical: '🔴',
    high: '🟠',
    medium: '🔵',
    low: '⚪',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[priority]}`}>
      {icons[priority]} {priority}
    </span>
  );
};

const SprintStatusBadge: React.FC<{ status: SprintStatus }> = ({ status }) => {
  const colors: Record<SprintStatus, string> = {
    planned: 'bg-gray-100 text-gray-800',
    active: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>
      {status}
    </span>
  );
};

const HealthScoreBadge: React.FC<{ score: number }> = ({ score }) => {
  const color = score >= 80 ? 'text-green-600' : score >= 60 ? 'text-yellow-600' : 'text-red-600';
  const bg = score >= 80 ? 'bg-green-100' : score >= 60 ? 'bg-yellow-100' : 'bg-red-100';
  return (
    <span className={`px-3 py-1 rounded-full text-sm font-bold ${bg} ${color}`}>
      {score}/100
    </span>
  );
};

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const ProjectManagementPage: React.FC = () => {
  const store = useProjectManagementStore();
  const [showCreateProject, setShowCreateProject] = useState(false);
  const [showCreateTask, setShowCreateTask] = useState(false);
  const [showCreateSprint, setShowCreateSprint] = useState(false);
  const [showLogTime, setShowLogTime] = useState(false);
  const [showAddMember, setShowAddMember] = useState(false);

  useEffect(() => {
    store.fetchDashboard();
    store.fetchProjects();
  }, []);

  useEffect(() => {
    if (store.selectedProject) {
      store.fetchTasks(store.selectedProject.id);
      store.fetchSprints(store.selectedProject.id);
      store.fetchMilestones(store.selectedProject.id);
      store.fetchTeam(store.selectedProject.id);
      if (store.activeTab === 'kanban') {
        store.fetchKanban(store.selectedProject.id);
      }
    }
  }, [store.selectedProject?.id, store.activeTab]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                📊 Project Management
              </h1>
              <p className="text-sm text-gray-500">
                CHE·NU™ V68 — Monday.com killer at $29/mo
              </p>
            </div>
            <button
              onClick={() => setShowCreateProject(true)}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              + New Project
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Dashboard Summary */}
        {store.dashboard && !store.selectedProject && (
          <div className="grid grid-cols-4 gap-4 mb-6">
            <DashboardCard
              title="Projects"
              value={store.dashboard.projects.total}
              subtitle={`${store.dashboard.projects.active} active`}
              icon="📁"
            />
            <DashboardCard
              title="Tasks"
              value={store.dashboard.tasks.total}
              subtitle={`${store.dashboard.tasks.overdue} overdue`}
              icon="✅"
              alert={store.dashboard.tasks.overdue > 0}
            />
            <DashboardCard
              title="Due This Week"
              value={store.dashboard.tasks.due_this_week}
              subtitle="tasks"
              icon="📅"
            />
            <DashboardCard
              title="Hours This Week"
              value={store.dashboard.time.hours_this_week}
              subtitle="logged"
              icon="⏱️"
            />
          </div>
        )}

        {/* Project Selection or Detail View */}
        {!store.selectedProject ? (
          <ProjectList
            projects={store.projects}
            onSelect={(p) => store.setSelectedProject(p)}
          />
        ) : (
          <div>
            {/* Back button and project header */}
            <div className="flex items-center gap-4 mb-6">
              <button
                onClick={() => store.setSelectedProject(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ← Back to Projects
              </button>
              <h2 className="text-xl font-bold">{store.selectedProject.name}</h2>
              <StatusBadge status={store.selectedProject.status} />
              <button
                onClick={() => store.analyzeProject(store.selectedProject!.id)}
                className="ml-auto px-3 py-1 bg-purple-100 text-purple-700 rounded-lg text-sm hover:bg-purple-200"
              >
                🤖 AI Analysis
              </button>
            </div>

            {/* AI Analysis Panel */}
            {store.projectAnalysis && (
              <AnalysisPanel analysis={store.projectAnalysis} />
            )}

            {/* Tabs */}
            <div className="flex gap-2 mb-6 border-b">
              {(['tasks', 'kanban', 'sprints', 'milestones', 'time', 'team'] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => store.setActiveTab(tab)}
                  className={`px-4 py-2 font-medium capitalize ${
                    store.activeTab === tab
                      ? 'border-b-2 border-indigo-600 text-indigo-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            {store.activeTab === 'tasks' && (
              <TaskList
                tasks={store.tasks}
                onCreateTask={() => setShowCreateTask(true)}
                onMoveTask={(taskId, status) => 
                  store.moveTask(store.selectedProject!.id, taskId, status)
                }
              />
            )}

            {store.activeTab === 'kanban' && store.kanbanBoard && (
              <KanbanBoard
                board={store.kanbanBoard}
                onMoveTask={(taskId, status) =>
                  store.moveTask(store.selectedProject!.id, taskId, status)
                }
              />
            )}

            {store.activeTab === 'sprints' && (
              <SprintList
                sprints={store.sprints}
                onCreateSprint={() => setShowCreateSprint(true)}
                onStartSprint={(id) => store.startSprint(store.selectedProject!.id, id)}
                onCompleteSprint={(id) => store.completeSprint(store.selectedProject!.id, id)}
              />
            )}

            {store.activeTab === 'milestones' && (
              <MilestoneList
                milestones={store.milestones}
                onComplete={(id) => store.completeMilestone(store.selectedProject!.id, id)}
              />
            )}

            {store.activeTab === 'time' && (
              <TimeTrackingView
                entries={store.timeEntries}
                onLogTime={() => setShowLogTime(true)}
              />
            )}

            {store.activeTab === 'team' && (
              <TeamView
                members={store.team}
                onAddMember={() => setShowAddMember(true)}
                onRemoveMember={(id) => store.removeTeamMember(store.selectedProject!.id, id)}
              />
            )}
          </div>
        )}
      </div>

      {/* Modals */}
      {showCreateProject && (
        <CreateProjectModal
          onClose={() => setShowCreateProject(false)}
          onCreate={async (data) => {
            await store.createProject(data);
            setShowCreateProject(false);
          }}
        />
      )}

      {showCreateTask && store.selectedProject && (
        <CreateTaskModal
          projectId={store.selectedProject.id}
          team={store.team}
          sprints={store.sprints}
          onClose={() => setShowCreateTask(false)}
          onCreate={async (data) => {
            await store.createTask(store.selectedProject!.id, data);
            setShowCreateTask(false);
          }}
        />
      )}

      {showCreateSprint && store.selectedProject && (
        <CreateSprintModal
          onClose={() => setShowCreateSprint(false)}
          onCreate={async (data) => {
            await store.createSprint(store.selectedProject!.id, data);
            setShowCreateSprint(false);
          }}
        />
      )}

      {showLogTime && store.selectedProject && (
        <LogTimeModal
          tasks={store.tasks}
          onClose={() => setShowLogTime(false)}
          onLog={async (taskId, data) => {
            await store.logTime(store.selectedProject!.id, taskId, data);
            setShowLogTime(false);
          }}
        />
      )}

      {showAddMember && store.selectedProject && (
        <AddTeamMemberModal
          onClose={() => setShowAddMember(false)}
          onAdd={async (data) => {
            await store.addTeamMember(store.selectedProject!.id, data);
            setShowAddMember(false);
          }}
        />
      )}

      {/* Error Toast */}
      {store.error && (
        <div className="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg">
          {store.error}
          <button onClick={() => store.clearError()} className="ml-2">✕</button>
        </div>
      )}

      {/* Loading Overlay */}
      {store.isLoading && (
        <div className="fixed inset-0 bg-black/20 flex items-center justify-center">
          <div className="bg-white p-4 rounded-lg shadow-lg">
            <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// SUB-COMPONENTS
// ============================================================================

const DashboardCard: React.FC<{
  title: string;
  value: number;
  subtitle: string;
  icon: string;
  alert?: boolean;
}> = ({ title, value, subtitle, icon, alert }) => (
  <div className={`bg-white p-4 rounded-lg shadow ${alert ? 'border-l-4 border-red-500' : ''}`}>
    <div className="flex items-center gap-3">
      <span className="text-2xl">{icon}</span>
      <div>
        <p className="text-sm text-gray-500">{title}</p>
        <p className="text-2xl font-bold">{value}</p>
        <p className="text-xs text-gray-400">{subtitle}</p>
      </div>
    </div>
  </div>
);

const ProjectList: React.FC<{
  projects: Project[];
  onSelect: (p: Project) => void;
}> = ({ projects, onSelect }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {projects.map((project) => (
      <div
        key={project.id}
        onClick={() => onSelect(project)}
        className="bg-white p-4 rounded-lg shadow hover:shadow-md cursor-pointer transition"
      >
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold">{project.name}</h3>
          <StatusBadge status={project.status} />
        </div>
        <p className="text-sm text-gray-500 mb-3 line-clamp-2">{project.description}</p>
        <div className="flex items-center justify-between text-xs text-gray-400">
          <span>Target: {project.target_date || 'Not set'}</span>
          {project.budget && (
            <span>${project.spent.toFixed(0)} / ${project.budget.toFixed(0)}</span>
          )}
        </div>
        {project.tags.length > 0 && (
          <div className="flex gap-1 mt-2">
            {project.tags.slice(0, 3).map((tag) => (
              <span key={tag} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    ))}
    {projects.length === 0 && (
      <div className="col-span-full text-center py-12 text-gray-500">
        No projects yet. Create your first project to get started!
      </div>
    )}
  </div>
);

const AnalysisPanel: React.FC<{ analysis: any }> = ({ analysis }) => (
  <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-4 rounded-lg mb-6 border border-purple-200">
    <div className="flex items-center gap-4 mb-4">
      <span className="text-2xl">🤖</span>
      <h3 className="font-semibold">AI Project Analysis</h3>
      <HealthScoreBadge score={analysis.health_score} />
      <span className={`px-2 py-1 rounded text-xs ${
        analysis.risk_level === 'low' ? 'bg-green-100 text-green-800' :
        analysis.risk_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
        'bg-red-100 text-red-800'
      }`}>
        {analysis.risk_level} risk
      </span>
      <span className="text-sm text-gray-500">
        {analysis.completion_percentage.toFixed(0)}% complete
      </span>
    </div>
    
    {analysis.recommendations.length > 0 && (
      <div className="space-y-1">
        <p className="text-sm font-medium text-gray-700">Recommendations:</p>
        {analysis.recommendations.map((rec: string, i: number) => (
          <p key={i} className="text-sm text-gray-600 pl-4">{rec}</p>
        ))}
      </div>
    )}
  </div>
);

const TaskList: React.FC<{
  tasks: Task[];
  onCreateTask: () => void;
  onMoveTask: (taskId: string, status: TaskStatus) => void;
}> = ({ tasks, onCreateTask, onMoveTask }) => (
  <div>
    <div className="flex justify-between items-center mb-4">
      <h3 className="font-semibold">Tasks ({tasks.length})</h3>
      <button
        onClick={onCreateTask}
        className="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
      >
        + Add Task
      </button>
    </div>
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-xs text-gray-500">Task</th>
            <th className="px-4 py-2 text-left text-xs text-gray-500">Status</th>
            <th className="px-4 py-2 text-left text-xs text-gray-500">Priority</th>
            <th className="px-4 py-2 text-left text-xs text-gray-500">Assignee</th>
            <th className="px-4 py-2 text-left text-xs text-gray-500">Due</th>
            <th className="px-4 py-2 text-left text-xs text-gray-500">Hours</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id} className="border-t hover:bg-gray-50">
              <td className="px-4 py-3">
                <p className="font-medium">{task.title}</p>
                {task.tags.length > 0 && (
                  <div className="flex gap-1 mt-1">
                    {task.tags.map((tag) => (
                      <span key={tag} className="text-xs bg-gray-100 px-1 rounded">{tag}</span>
                    ))}
                  </div>
                )}
              </td>
              <td className="px-4 py-3">
                <select
                  value={task.status}
                  onChange={(e) => onMoveTask(task.id, e.target.value as TaskStatus)}
                  className="text-xs border rounded px-2 py-1"
                >
                  {['backlog', 'todo', 'in_progress', 'in_review', 'blocked', 'done'].map((s) => (
                    <option key={s} value={s}>{s.replace('_', ' ')}</option>
                  ))}
                </select>
              </td>
              <td className="px-4 py-3">
                <PriorityBadge priority={task.priority} />
              </td>
              <td className="px-4 py-3 text-sm">{task.assignee_name || '—'}</td>
              <td className="px-4 py-3 text-sm">{task.due_date || '—'}</td>
              <td className="px-4 py-3 text-sm">
                {task.actual_hours}/{task.estimated_hours || '?'}h
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {tasks.length === 0 && (
        <div className="text-center py-8 text-gray-500">No tasks yet</div>
      )}
    </div>
  </div>
);

const KanbanBoard: React.FC<{
  board: any;
  onMoveTask: (taskId: string, status: TaskStatus) => void;
}> = ({ board, onMoveTask }) => {
  const columns: { key: TaskStatus; label: string; color: string }[] = [
    { key: 'backlog', label: 'Backlog', color: 'bg-gray-200' },
    { key: 'todo', label: 'To Do', color: 'bg-blue-200' },
    { key: 'in_progress', label: 'In Progress', color: 'bg-yellow-200' },
    { key: 'in_review', label: 'In Review', color: 'bg-purple-200' },
    { key: 'done', label: 'Done', color: 'bg-green-200' },
  ];

  return (
    <div className="flex gap-4 overflow-x-auto pb-4">
      {columns.map((col) => (
        <div key={col.key} className="flex-shrink-0 w-72">
          <div className={`${col.color} px-3 py-2 rounded-t-lg font-medium text-sm`}>
            {col.label} ({board[col.key]?.length || 0})
          </div>
          <div className="bg-gray-100 rounded-b-lg p-2 min-h-96 space-y-2">
            {(board[col.key] || []).map((task: Task) => (
              <div
                key={task.id}
                className="bg-white p-3 rounded shadow-sm hover:shadow cursor-move"
                draggable
              >
                <div className="flex items-center justify-between mb-1">
                  <PriorityBadge priority={task.priority} />
                </div>
                <p className="font-medium text-sm">{task.title}</p>
                {task.assignee_name && (
                  <p className="text-xs text-gray-500 mt-1">👤 {task.assignee_name}</p>
                )}
                {task.due_date && (
                  <p className="text-xs text-gray-400 mt-1">📅 {task.due_date}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

const SprintList: React.FC<{
  sprints: Sprint[];
  onCreateSprint: () => void;
  onStartSprint: (id: string) => void;
  onCompleteSprint: (id: string) => void;
}> = ({ sprints, onCreateSprint, onStartSprint, onCompleteSprint }) => (
  <div>
    <div className="flex justify-between items-center mb-4">
      <h3 className="font-semibold">Sprints ({sprints.length})</h3>
      <button
        onClick={onCreateSprint}
        className="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
      >
        + New Sprint
      </button>
    </div>
    <div className="space-y-3">
      {sprints.map((sprint) => (
        <div key={sprint.id} className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2">
                <h4 className="font-semibold">{sprint.name}</h4>
                <SprintStatusBadge status={sprint.status} />
              </div>
              <p className="text-sm text-gray-500">{sprint.goal}</p>
              <p className="text-xs text-gray-400 mt-1">
                {sprint.start_date} → {sprint.end_date}
              </p>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold">
                {sprint.velocity_actual} / {sprint.velocity_planned}
              </p>
              <p className="text-xs text-gray-500">velocity</p>
              {sprint.status === 'planned' && (
                <button
                  onClick={() => onStartSprint(sprint.id)}
                  className="mt-2 px-3 py-1 bg-green-500 text-white rounded text-xs hover:bg-green-600"
                >
                  Start Sprint
                </button>
              )}
              {sprint.status === 'active' && (
                <button
                  onClick={() => onCompleteSprint(sprint.id)}
                  className="mt-2 px-3 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600"
                >
                  Complete Sprint
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
      {sprints.length === 0 && (
        <div className="text-center py-8 text-gray-500">No sprints yet</div>
      )}
    </div>
  </div>
);

const MilestoneList: React.FC<{
  milestones: Milestone[];
  onComplete: (id: string) => void;
}> = ({ milestones, onComplete }) => (
  <div className="space-y-3">
    {milestones.map((milestone) => (
      <div key={milestone.id} className="bg-white p-4 rounded-lg shadow">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🏁</span>
              <h4 className="font-semibold">{milestone.name}</h4>
              <span className={`px-2 py-1 rounded text-xs ${
                milestone.status === 'completed' ? 'bg-green-100 text-green-800' :
                milestone.status === 'missed' ? 'bg-red-100 text-red-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {milestone.status}
              </span>
            </div>
            <p className="text-sm text-gray-500">{milestone.description}</p>
            <p className="text-xs text-gray-400 mt-1">Due: {milestone.due_date}</p>
          </div>
          {milestone.status !== 'completed' && (
            <button
              onClick={() => onComplete(milestone.id)}
              className="px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600"
            >
              ✓ Complete
            </button>
          )}
        </div>
        {milestone.deliverables.length > 0 && (
          <div className="mt-2 flex gap-2">
            {milestone.deliverables.map((d, i) => (
              <span key={i} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
                {d}
              </span>
            ))}
          </div>
        )}
      </div>
    ))}
    {milestones.length === 0 && (
      <div className="text-center py-8 text-gray-500">No milestones yet</div>
    )}
  </div>
);

const TimeTrackingView: React.FC<{
  entries: TimeEntry[];
  onLogTime: () => void;
}> = ({ entries, onLogTime }) => {
  const totalHours = entries.reduce((sum, e) => sum + e.hours, 0);
  const billableHours = entries.filter((e) => e.billable).reduce((sum, e) => sum + e.hours, 0);

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <div className="flex gap-6">
          <div>
            <p className="text-sm text-gray-500">Total Hours</p>
            <p className="text-2xl font-bold">{totalHours.toFixed(1)}h</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Billable</p>
            <p className="text-2xl font-bold text-green-600">{billableHours.toFixed(1)}h</p>
          </div>
        </div>
        <button
          onClick={onLogTime}
          className="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
        >
          + Log Time
        </button>
      </div>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left text-xs text-gray-500">Date</th>
              <th className="px-4 py-2 text-left text-xs text-gray-500">Hours</th>
              <th className="px-4 py-2 text-left text-xs text-gray-500">Description</th>
              <th className="px-4 py-2 text-left text-xs text-gray-500">Billable</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry) => (
              <tr key={entry.id} className="border-t">
                <td className="px-4 py-3 text-sm">{entry.date}</td>
                <td className="px-4 py-3 font-medium">{entry.hours}h</td>
                <td className="px-4 py-3 text-sm text-gray-600">{entry.description || '—'}</td>
                <td className="px-4 py-3">
                  {entry.billable ? (
                    <span className="text-green-600">✓</span>
                  ) : (
                    <span className="text-gray-400">—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {entries.length === 0 && (
          <div className="text-center py-8 text-gray-500">No time entries yet</div>
        )}
      </div>
    </div>
  );
};

const TeamView: React.FC<{
  members: TeamMember[];
  onAddMember: () => void;
  onRemoveMember: (id: string) => void;
}> = ({ members, onAddMember, onRemoveMember }) => (
  <div>
    <div className="flex justify-between items-center mb-4">
      <h3 className="font-semibold">Team ({members.length})</h3>
      <button
        onClick={onAddMember}
        className="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
      >
        + Add Member
      </button>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {members.map((member) => (
        <div key={member.id} className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold">
              {member.name.charAt(0)}
            </div>
            <div className="flex-1">
              <p className="font-medium">{member.name}</p>
              <p className="text-sm text-gray-500">{member.role}</p>
              <p className="text-xs text-gray-400">{member.email}</p>
            </div>
            <button
              onClick={() => onRemoveMember(member.id)}
              className="text-red-500 hover:text-red-700"
            >
              ✕
            </button>
          </div>
          <div className="mt-3 flex justify-between text-xs text-gray-500">
            <span>{member.capacity_hours_week}h/week</span>
            {member.hourly_rate && <span>${member.hourly_rate}/hr</span>}
          </div>
        </div>
      ))}
    </div>
    {members.length === 0 && (
      <div className="text-center py-8 text-gray-500">No team members yet</div>
    )}
  </div>
);

// ============================================================================
// MODALS
// ============================================================================

const CreateProjectModal: React.FC<{
  onClose: () => void;
  onCreate: (data: any) => Promise<void>;
}> = ({ onClose, onCreate }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [targetDate, setTargetDate] = useState('');
  const [budget, setBudget] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onCreate({
      name,
      description,
      target_date: targetDate || null,
      budget: budget ? parseFloat(budget) : null,
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Create Project</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border rounded px-3 py-2"
              rows={3}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Target Date</label>
              <input
                type="date"
                value={targetDate}
                onChange={(e) => setTargetDate(e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Budget ($)</label>
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>
          </div>
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
            >
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const CreateTaskModal: React.FC<{
  projectId: string;
  team: TeamMember[];
  sprints: Sprint[];
  onClose: () => void;
  onCreate: (data: any) => Promise<void>;
}> = ({ team, sprints, onClose, onCreate }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [assigneeId, setAssigneeId] = useState('');
  const [sprintId, setSprintId] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [estimatedHours, setEstimatedHours] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const assignee = team.find((m) => m.id === assigneeId);
    await onCreate({
      title,
      description,
      priority,
      assignee_id: assigneeId || null,
      assignee_name: assignee?.name || null,
      sprint_id: sprintId || null,
      due_date: dueDate || null,
      estimated_hours: estimatedHours ? parseFloat(estimatedHours) : null,
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-lg">
        <h2 className="text-xl font-bold mb-4">Create Task</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Title *</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border rounded px-3 py-2"
              rows={2}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="w-full border rounded px-3 py-2"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Assignee</label>
              <select
                value={assigneeId}
                onChange={(e) => setAssigneeId(e.target.value)}
                className="w-full border rounded px-3 py-2"
              >
                <option value="">Unassigned</option>
                {team.map((m) => (
                  <option key={m.id} value={m.id}>{m.name}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Sprint</label>
              <select
                value={sprintId}
                onChange={(e) => setSprintId(e.target.value)}
                className="w-full border rounded px-3 py-2"
              >
                <option value="">Backlog</option>
                {sprints.map((s) => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Due Date</label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Est. Hours</label>
              <input
                type="number"
                value={estimatedHours}
                onChange={(e) => setEstimatedHours(e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>
          </div>
          <div className="flex justify-end gap-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-gray-600">
              Cancel
            </button>
            <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded">
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const CreateSprintModal: React.FC<{
  onClose: () => void;
  onCreate: (data: any) => Promise<void>;
}> = ({ onClose, onCreate }) => {
  const [name, setName] = useState('');
  const [goal, setGoal] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [velocity, setVelocity] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onCreate({
      name,
      goal,
      start_date: startDate,
      end_date: endDate,
      velocity_planned: velocity ? parseInt(velocity) : 0,
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Create Sprint</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full border rounded px-3 py-2"
              placeholder="Sprint 1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Goal</label>
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              className="w-full border rounded px-3 py-2"
              placeholder="What's the sprint goal?"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Start Date *</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">End Date *</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                required
                className="w-full border rounded px-3 py-2"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Planned Velocity</label>
            <input
              type="number"
              value={velocity}
              onChange={(e) => setVelocity(e.target.value)}
              className="w-full border rounded px-3 py-2"
              placeholder="Story points"
            />
          </div>
          <div className="flex justify-end gap-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-gray-600">
              Cancel
            </button>
            <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded">
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const LogTimeModal: React.FC<{
  tasks: Task[];
  onClose: () => void;
  onLog: (taskId: string, data: any) => Promise<void>;
}> = ({ tasks, onClose, onLog }) => {
  const [taskId, setTaskId] = useState('');
  const [hours, setHours] = useState('');
  const [description, setDescription] = useState('');
  const [billable, setBillable] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onLog(taskId, {
      hours: parseFloat(hours),
      description,
      billable,
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Log Time</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Task *</label>
            <select
              value={taskId}
              onChange={(e) => setTaskId(e.target.value)}
              required
              className="w-full border rounded px-3 py-2"
            >
              <option value="">Select task...</option>
              {tasks.map((t) => (
                <option key={t.id} value={t.id}>{t.title}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Hours *</label>
            <input
              type="number"
              step="0.5"
              value={hours}
              onChange={(e) => setHours(e.target.value)}
              required
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border rounded px-3 py-2"
              placeholder="What did you work on?"
            />
          </div>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={billable}
              onChange={(e) => setBillable(e.target.checked)}
              id="billable"
            />
            <label htmlFor="billable" className="text-sm">Billable</label>
          </div>
          <div className="flex justify-end gap-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-gray-600">
              Cancel
            </button>
            <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded">
              Log Time
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const AddTeamMemberModal: React.FC<{
  onClose: () => void;
  onAdd: (data: any) => Promise<void>;
}> = ({ onClose, onAdd }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('member');
  const [hourlyRate, setHourlyRate] = useState('');
  const [capacity, setCapacity] = useState('40');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onAdd({
      name,
      email,
      role,
      hourly_rate: hourlyRate ? parseFloat(hourlyRate) : null,
      capacity_hours_week: parseFloat(capacity),
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Add Team Member</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email *</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full border rounded px-3 py-2"
              >
                <option value="member">Member</option>
                <option value="lead">Lead</option>
                <option value="manager">Manager</option>
                <option value="developer">Developer</option>
                <option value="designer">Designer</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Capacity (h/week)</label>
              <input
                type="number"
                value={capacity}
                onChange={(e) => setCapacity(e.target.value)}
                className="w-full border rounded px-3 py-2"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Hourly Rate ($)</label>
            <input
              type="number"
              value={hourlyRate}
              onChange={(e) => setHourlyRate(e.target.value)}
              className="w-full border rounded px-3 py-2"
              placeholder="Optional"
            />
          </div>
          <div className="flex justify-end gap-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-gray-600">
              Cancel
            </button>
            <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded">
              Add Member
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProjectManagementPage;
