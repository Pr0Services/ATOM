/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║              CHE·NU™ PERSONAL PRODUCTIVITY — ZUSTAND STORE                   ║
 * ║                                                                              ║
 * ║  State management for notes, tasks, and productivity features.              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export type NoteType = 'note' | 'meeting' | 'journal' | 'idea' | 'reference' | 'todo';
export type NoteStatus = 'draft' | 'active' | 'archived' | 'pinned';

export type TaskPriority = 'urgent' | 'high' | 'medium' | 'low' | 'someday';
export type TaskStatus = 'todo' | 'in_progress' | 'blocked' | 'done' | 'cancelled';
export type RecurrenceType = 'none' | 'daily' | 'weekly' | 'biweekly' | 'monthly' | 'yearly';

export interface Note {
  id: string;
  title: string;
  content: string;
  type: NoteType;
  status: NoteStatus;
  tags: string[];
  folder: string | null;
  summary: string | null;
  created_at: string;
  updated_at: string;
  word_count: number;
  ai_enhanced: boolean;
  metadata: Record<string, any>;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  priority: TaskPriority;
  status: TaskStatus;
  due_date: string | null;
  due_time: string | null;
  estimated_minutes: number | null;
  actual_minutes: number | null;
  project_id: string | null;
  tags: string[];
  subtasks: string[];
  parent_id: string | null;
  recurrence: RecurrenceType;
  completed_at: string | null;
  created_at: string;
  ai_score: number | null;
  metadata: Record<string, any>;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  color: string;
  icon: string | null;
  task_count: number;
  completed_count: number;
  created_at: string;
  archived: boolean;
}

export interface Folder {
  name: string;
  count: number;
}

export interface Tag {
  name: string;
  count: number;
}

export interface TodayView {
  date: string;
  overdue: Task[];
  due_today: Task[];
  high_priority: Task[];
  completed_today: Task[];
  stats: {
    overdue_count: number;
    due_today_count: number;
    completed_count: number;
  };
}

export interface NoteStats {
  total_notes: number;
  total_words: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  folders_count: number;
  tags_count: number;
}

export interface TaskStats {
  total: number;
  completed: number;
  completion_rate: number;
  by_status: Record<string, number>;
  by_priority: Record<string, number>;
  overdue: number;
}

// ═══════════════════════════════════════════════════════════════════════════════
// STORE STATE
// ═══════════════════════════════════════════════════════════════════════════════

interface PersonalProductivityState {
  // Notes
  notes: Note[];
  currentNote: Note | null;
  folders: Folder[];
  noteTags: Tag[];
  noteStats: NoteStats | null;
  
  // Tasks
  tasks: Task[];
  currentTask: Task | null;
  projects: Project[];
  todayView: TodayView | null;
  taskStats: TaskStats | null;
  
  // UI State
  activeTab: 'notes' | 'tasks' | 'today' | 'stats';
  noteFilter: {
    folder: string | null;
    tag: string | null;
    type: NoteType | null;
    search: string;
  };
  taskFilter: {
    project_id: string | null;
    status: TaskStatus | null;
    priority: TaskPriority | null;
    due_today: boolean;
    overdue: boolean;
    search: string;
  };
  
  // Loading states
  isLoading: boolean;
  error: string | null;
  
  // User
  userId: string;
  
  // Actions - Notes
  fetchNotes: () => Promise<void>;
  createNote: (content: string, autoEnhance?: boolean) => Promise<Note>;
  updateNote: (noteId: string, updates: Partial<Note>) => Promise<void>;
  deleteNote: (noteId: string) => Promise<void>;
  enhanceNote: (noteId: string) => Promise<void>;
  setCurrentNote: (note: Note | null) => void;
  setNoteFilter: (filter: Partial<PersonalProductivityState['noteFilter']>) => void;
  
  // Actions - Tasks
  fetchTasks: () => Promise<void>;
  createTask: (title: string, autoSuggest?: boolean) => Promise<Task>;
  updateTask: (taskId: string, updates: Partial<Task>) => Promise<void>;
  completeTask: (taskId: string, actualMinutes?: number) => Promise<void>;
  deleteTask: (taskId: string) => Promise<void>;
  setCurrentTask: (task: Task | null) => void;
  setTaskFilter: (filter: Partial<PersonalProductivityState['taskFilter']>) => void;
  fetchTodayView: () => Promise<void>;
  
  // Actions - Projects
  fetchProjects: () => Promise<void>;
  createProject: (name: string, color?: string) => Promise<Project>;
  
  // Actions - Stats
  fetchStats: () => Promise<void>;
  
  // UI Actions
  setActiveTab: (tab: PersonalProductivityState['activeTab']) => void;
  clearError: () => void;
}

// ═══════════════════════════════════════════════════════════════════════════════
// API CLIENT
// ═══════════════════════════════════════════════════════════════════════════════

const API_BASE = '/api/v2/personal';

async function apiCall<T>(
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

// ═══════════════════════════════════════════════════════════════════════════════
// STORE
// ═══════════════════════════════════════════════════════════════════════════════

export const usePersonalProductivityStore = create<PersonalProductivityState>()(
  persist(
    (set, get) => ({
      // Initial state
      notes: [],
      currentNote: null,
      folders: [],
      noteTags: [],
      noteStats: null,
      
      tasks: [],
      currentTask: null,
      projects: [],
      todayView: null,
      taskStats: null,
      
      activeTab: 'today',
      noteFilter: {
        folder: null,
        tag: null,
        type: null,
        search: '',
      },
      taskFilter: {
        project_id: null,
        status: null,
        priority: null,
        due_today: false,
        overdue: false,
        search: '',
      },
      
      isLoading: false,
      error: null,
      userId: 'default_user',
      
      // ═══════════════════════════════════════════════════════════════════════════
      // NOTE ACTIONS
      // ═══════════════════════════════════════════════════════════════════════════
      
      fetchNotes: async () => {
        const { noteFilter, userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const params = new URLSearchParams({ user_id: userId });
          if (noteFilter.folder) params.append('folder', noteFilter.folder);
          if (noteFilter.tag) params.append('tag', noteFilter.tag);
          if (noteFilter.type) params.append('note_type', noteFilter.type);
          if (noteFilter.search) params.append('search', noteFilter.search);
          
          const notes = await apiCall<Note[]>(`/notes?${params}`);
          const folders = await apiCall<Folder[]>(`/notes/folders/list?user_id=${userId}`);
          const tags = await apiCall<Tag[]>(`/notes/tags/list?user_id=${userId}`);
          
          set({ notes, folders, noteTags: tags, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createNote: async (content: string, autoEnhance = true) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const note = await apiCall<Note>('/notes', {
            method: 'POST',
            body: JSON.stringify({
              content,
              auto_enhance: autoEnhance,
              user_id: userId,
            }),
          });
          
          set(state => ({
            notes: [note, ...state.notes],
            currentNote: note,
            isLoading: false,
          }));
          
          return note;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      updateNote: async (noteId: string, updates: Partial<Note>) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const note = await apiCall<Note>(`/notes/${noteId}?user_id=${userId}`, {
            method: 'PUT',
            body: JSON.stringify(updates),
          });
          
          set(state => ({
            notes: state.notes.map(n => n.id === noteId ? note : n),
            currentNote: state.currentNote?.id === noteId ? note : state.currentNote,
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      deleteNote: async (noteId: string) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          await apiCall(`/notes/${noteId}?user_id=${userId}`, { method: 'DELETE' });
          
          set(state => ({
            notes: state.notes.filter(n => n.id !== noteId),
            currentNote: state.currentNote?.id === noteId ? null : state.currentNote,
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      enhanceNote: async (noteId: string) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const note = await apiCall<Note>(`/notes/${noteId}/enhance?user_id=${userId}`, {
            method: 'POST',
          });
          
          set(state => ({
            notes: state.notes.map(n => n.id === noteId ? note : n),
            currentNote: state.currentNote?.id === noteId ? note : state.currentNote,
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      setCurrentNote: (note) => set({ currentNote: note }),
      
      setNoteFilter: (filter) => set(state => ({
        noteFilter: { ...state.noteFilter, ...filter },
      })),
      
      // ═══════════════════════════════════════════════════════════════════════════
      // TASK ACTIONS
      // ═══════════════════════════════════════════════════════════════════════════
      
      fetchTasks: async () => {
        const { taskFilter, userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const params = new URLSearchParams({ user_id: userId });
          if (taskFilter.project_id) params.append('project_id', taskFilter.project_id);
          if (taskFilter.status) params.append('status', taskFilter.status);
          if (taskFilter.priority) params.append('priority', taskFilter.priority);
          if (taskFilter.due_today) params.append('due_today', 'true');
          if (taskFilter.overdue) params.append('overdue', 'true');
          if (taskFilter.search) params.append('search', taskFilter.search);
          
          const tasks = await apiCall<Task[]>(`/tasks?${params}`);
          
          set({ tasks, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createTask: async (title: string, autoSuggest = true) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const task = await apiCall<Task>('/tasks', {
            method: 'POST',
            body: JSON.stringify({
              title,
              auto_suggest: autoSuggest,
              user_id: userId,
            }),
          });
          
          set(state => ({
            tasks: [task, ...state.tasks],
            currentTask: task,
            isLoading: false,
          }));
          
          return task;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      updateTask: async (taskId: string, updates: Partial<Task>) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const task = await apiCall<Task>(`/tasks/${taskId}?user_id=${userId}`, {
            method: 'PUT',
            body: JSON.stringify(updates),
          });
          
          set(state => ({
            tasks: state.tasks.map(t => t.id === taskId ? task : t),
            currentTask: state.currentTask?.id === taskId ? task : state.currentTask,
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      completeTask: async (taskId: string, actualMinutes?: number) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const task = await apiCall<Task>(`/tasks/${taskId}/complete?user_id=${userId}`, {
            method: 'POST',
            body: JSON.stringify({ actual_minutes: actualMinutes }),
          });
          
          set(state => ({
            tasks: state.tasks.map(t => t.id === taskId ? task : t),
            currentTask: state.currentTask?.id === taskId ? task : state.currentTask,
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      deleteTask: async (taskId: string) => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          await apiCall(`/tasks/${taskId}?user_id=${userId}`, { method: 'DELETE' });
          
          set(state => ({
            tasks: state.tasks.filter(t => t.id !== taskId),
            currentTask: state.currentTask?.id === taskId ? null : state.currentTask,
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      setCurrentTask: (task) => set({ currentTask: task }),
      
      setTaskFilter: (filter) => set(state => ({
        taskFilter: { ...state.taskFilter, ...filter },
      })),
      
      fetchTodayView: async () => {
        const { userId } = get();
        set({ isLoading: true, error: null });
        
        try {
          const todayView = await apiCall<TodayView>(`/tasks/today?user_id=${userId}`);
          set({ todayView, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      // ═══════════════════════════════════════════════════════════════════════════
      // PROJECT ACTIONS
      // ═══════════════════════════════════════════════════════════════════════════
      
      fetchProjects: async () => {
        const { userId } = get();
        
        try {
          const projects = await apiCall<Project[]>(`/projects?user_id=${userId}`);
          set({ projects });
        } catch (error) {
          set({ error: (error as Error).message });
        }
      },
      
      createProject: async (name: string, color = '#3B82F6') => {
        const { userId } = get();
        
        try {
          const project = await apiCall<Project>('/projects', {
            method: 'POST',
            body: JSON.stringify({ name, color, user_id: userId }),
          });
          
          set(state => ({ projects: [...state.projects, project] }));
          return project;
        } catch (error) {
          set({ error: (error as Error).message });
          throw error;
        }
      },
      
      // ═══════════════════════════════════════════════════════════════════════════
      // STATS ACTIONS
      // ═══════════════════════════════════════════════════════════════════════════
      
      fetchStats: async () => {
        const { userId } = get();
        
        try {
          const [noteStats, taskStats] = await Promise.all([
            apiCall<NoteStats>(`/stats/notes?user_id=${userId}`),
            apiCall<TaskStats>(`/stats/tasks?user_id=${userId}`),
          ]);
          
          set({ noteStats, taskStats });
        } catch (error) {
          set({ error: (error as Error).message });
        }
      },
      
      // ═══════════════════════════════════════════════════════════════════════════
      // UI ACTIONS
      // ═══════════════════════════════════════════════════════════════════════════
      
      setActiveTab: (tab) => set({ activeTab: tab }),
      clearError: () => set({ error: null }),
    }),
    {
      name: 'chenu-personal-productivity',
      partialize: (state) => ({
        activeTab: state.activeTab,
        noteFilter: state.noteFilter,
        taskFilter: state.taskFilter,
        userId: state.userId,
      }),
    }
  )
);
