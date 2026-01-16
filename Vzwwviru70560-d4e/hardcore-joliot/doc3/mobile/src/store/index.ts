/**
 * CHE·NU Mobile - Global Store (Zustand)
 * Gestion d'état complète pour l'application
 */
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { 
  User, SphereId, Sphere, Agent, Thread, Message, 
  Project, Task, Notification, Contact, Meeting 
} from '../types';

// ============== SPHERES DATA ==============
export const SPHERES_DATA: Sphere[] = [
  {
    id: 'personal',
    name: 'Personal',
    nameFr: 'Personnel',
    icon: '👤',
    color: '#6366F1',
    gradient: ['#6366F1', '#8B5CF6'],
    description: 'Vie personnelle, santé, finances',
    agents: [],
    modules: ['calendar', 'notes', 'health', 'finance'],
    isActive: true,
  },
  {
    id: 'social',
    name: 'Social & Entertainment',
    nameFr: 'Social & Divertissement',
    icon: '🎉',
    color: '#EC4899',
    gradient: ['#EC4899', '#F472B6'],
    description: 'Réseaux sociaux, événements, loisirs',
    agents: [],
    modules: ['social', 'events', 'streaming'],
    isActive: true,
  },
  {
    id: 'scholar',
    name: 'Scholar',
    nameFr: 'Études',
    icon: '📚',
    color: '#14B8A6',
    gradient: ['#14B8A6', '#2DD4BF'],
    description: 'Recherche, apprentissage, documentation',
    agents: [],
    modules: ['research', 'courses', 'library'],
    isActive: true,
  },
  {
    id: 'maison',
    name: 'Home',
    nameFr: 'Maison',
    icon: '🏠',
    color: '#F59E0B',
    gradient: ['#F59E0B', '#FBBF24'],
    description: 'Gestion domestique, famille',
    agents: [],
    modules: ['home', 'family', 'shopping'],
    isActive: true,
  },
  {
    id: 'business',
    name: 'Business',
    nameFr: 'Entreprise',
    icon: '🏢',
    color: '#3B82F6',
    gradient: ['#3B82F6', '#60A5FA'],
    description: 'Gestion d\'entreprise, RH, comptabilité',
    agents: [],
    modules: ['hr', 'accounting', 'operations'],
    isActive: true,
  },
  {
    id: 'projects',
    name: 'Projects',
    nameFr: 'Projets',
    icon: '📋',
    color: '#10B981',
    gradient: ['#10B981', '#34D399'],
    description: 'Gestion de projets, tâches, équipes',
    agents: [],
    modules: ['kanban', 'timeline', 'resources'],
    isActive: true,
  },
  {
    id: 'creative',
    name: 'Creative Studio',
    nameFr: 'Studio Créatif',
    icon: '🎨',
    color: '#8B5CF6',
    gradient: ['#8B5CF6', '#A78BFA'],
    description: 'Design, médias, création',
    agents: [],
    modules: ['design', 'media', 'branding'],
    isActive: true,
  },
  {
    id: 'cinema',
    name: 'Cinema',
    nameFr: 'Cinéma',
    icon: '🎬',
    color: '#EF4444',
    gradient: ['#EF4444', '#F87171'],
    description: 'Production vidéo, streaming',
    agents: [],
    modules: ['video', 'editing', 'streaming'],
    isActive: true,
  },
  {
    id: 'government',
    name: 'Government',
    nameFr: 'Gouvernement',
    icon: '🏛️',
    color: '#64748B',
    gradient: ['#64748B', '#94A3B8'],
    description: 'Administration, conformité, légal',
    agents: [],
    modules: ['compliance', 'legal', 'permits'],
    isActive: true,
  },
  {
    id: 'realestate',
    name: 'Real Estate',
    nameFr: 'Immobilier',
    icon: '🏗️',
    color: '#0EA5E9',
    gradient: ['#0EA5E9', '#38BDF8'],
    description: 'Construction, immobilier, chantiers',
    agents: [],
    modules: ['construction', 'sites', 'safety'],
    isActive: true,
  },
  {
    id: 'associations',
    name: 'Associations',
    nameFr: 'Associations',
    icon: '🤝',
    color: '#22C55E',
    gradient: ['#22C55E', '#4ADE80'],
    description: 'OBNL, bénévolat, communauté',
    agents: [],
    modules: ['members', 'donations', 'events'],
    isActive: true,
  },
];

// ============== AUTH STORE ==============
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  token: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (data: RegisterData) => Promise<boolean>;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
  setLoading: (loading: boolean) => void;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
  company?: string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      token: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true });
        try {
          // API call simulation
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          const mockUser: User = {
            id: '1',
            email,
            name: email.split('@')[0],
            role: 'admin',
            subscription: 'pro',
            createdAt: new Date(),
            preferences: {
              theme: 'dark',
              language: 'fr',
              notifications: { push: true, email: true, sms: false, tasks: true, meetings: true, agents: true },
              defaultSphere: 'business',
              expertMode: false,
              voiceEnabled: true,
              hapticFeedback: true,
            },
          };
          
          set({ user: mockUser, isAuthenticated: true, token: 'mock-token', isLoading: false });
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true });
        try {
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          const newUser: User = {
            id: Date.now().toString(),
            email: data.email,
            name: data.name,
            company: data.company,
            role: 'user',
            subscription: 'free',
            createdAt: new Date(),
            preferences: {
              theme: 'auto',
              language: 'fr',
              notifications: { push: true, email: true, sms: false, tasks: true, meetings: true, agents: true },
              defaultSphere: 'personal',
              expertMode: false,
              voiceEnabled: true,
              hapticFeedback: true,
            },
          };
          
          set({ user: newUser, isAuthenticated: true, token: 'mock-token', isLoading: false });
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      logout: () => {
        set({ user: null, isAuthenticated: false, token: null });
      },

      updateUser: (data: Partial<User>) => {
        const { user } = get();
        if (user) {
          set({ user: { ...user, ...data } });
        }
      },

      setLoading: (loading: boolean) => set({ isLoading: loading }),
    }),
    {
      name: 'chenu-auth',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// ============== SPHERES STORE ==============
interface SpheresState {
  spheres: Sphere[];
  currentSphere: SphereId;
  setCurrentSphere: (id: SphereId) => void;
  toggleSphere: (id: SphereId) => void;
  getSphere: (id: SphereId) => Sphere | undefined;
}

export const useSpheresStore = create<SpheresState>((set, get) => ({
  spheres: SPHERES_DATA,
  currentSphere: 'business',

  setCurrentSphere: (id: SphereId) => set({ currentSphere: id }),

  toggleSphere: (id: SphereId) => {
    const { spheres } = get();
    set({
      spheres: spheres.map(s => 
        s.id === id ? { ...s, isActive: !s.isActive } : s
      ),
    });
  },

  getSphere: (id: SphereId) => get().spheres.find(s => s.id === id),
}));

// ============== THREADS STORE ==============
interface ThreadsState {
  threads: Thread[];
  currentThread: Thread | null;
  isLoading: boolean;
  fetchThreads: (sphereId?: SphereId) => Promise<void>;
  createThread: (title: string, sphereId: SphereId) => Promise<Thread>;
  sendMessage: (threadId: string, content: string) => Promise<Message>;
  setCurrentThread: (thread: Thread | null) => void;
}

export const useThreadsStore = create<ThreadsState>((set, get) => ({
  threads: [],
  currentThread: null,
  isLoading: false,

  fetchThreads: async (sphereId?: SphereId) => {
    set({ isLoading: true });
    try {
      await new Promise(resolve => setTimeout(resolve, 500));
      // Mock threads
      const mockThreads: Thread[] = [
        {
          id: '1',
          title: 'Planification Q1 2025',
          sphere: 'business',
          participants: [
            { id: 'user1', type: 'user', name: 'Vous' },
            { id: 'nova', type: 'agent', name: 'Nova', role: 'Assistant IA' },
          ],
          messages: [],
          status: 'active',
          createdAt: new Date(),
          updatedAt: new Date(),
        },
        {
          id: '2',
          title: 'Analyse de marché',
          sphere: 'business',
          participants: [
            { id: 'user1', type: 'user', name: 'Vous' },
            { id: 'market-agent', type: 'agent', name: 'MarketAnalyst', role: 'Analyste' },
          ],
          messages: [],
          status: 'active',
          createdAt: new Date(),
          updatedAt: new Date(),
        },
      ];
      
      const filtered = sphereId 
        ? mockThreads.filter(t => t.sphere === sphereId)
        : mockThreads;
      
      set({ threads: filtered, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
    }
  },

  createThread: async (title: string, sphereId: SphereId) => {
    const newThread: Thread = {
      id: Date.now().toString(),
      title,
      sphere: sphereId,
      participants: [
        { id: 'user1', type: 'user', name: 'Vous' },
        { id: 'nova', type: 'agent', name: 'Nova', role: 'Assistant IA' },
      ],
      messages: [],
      status: 'active',
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    set(state => ({ threads: [newThread, ...state.threads] }));
    return newThread;
  },

  sendMessage: async (threadId: string, content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      threadId,
      senderId: 'user1',
      senderType: 'user',
      content,
      timestamp: new Date(),
      status: 'sent',
    };

    // Add user message
    set(state => ({
      threads: state.threads.map(t => 
        t.id === threadId 
          ? { ...t, messages: [...t.messages, userMessage], updatedAt: new Date() }
          : t
      ),
      currentThread: state.currentThread?.id === threadId
        ? { ...state.currentThread, messages: [...state.currentThread.messages, userMessage] }
        : state.currentThread,
    }));

    // Simulate AI response
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const aiResponse: Message = {
      id: (Date.now() + 1).toString(),
      threadId,
      senderId: 'nova',
      senderType: 'agent',
      content: `Je comprends votre demande concernant "${content.slice(0, 50)}...". Voici mon analyse et mes recommandations...`,
      timestamp: new Date(),
      status: 'sent',
      metadata: { tokens: 150, model: 'claude-3.5-sonnet', processingTime: 1.2 },
    };

    set(state => ({
      threads: state.threads.map(t => 
        t.id === threadId 
          ? { ...t, messages: [...t.messages, aiResponse], updatedAt: new Date() }
          : t
      ),
      currentThread: state.currentThread?.id === threadId
        ? { ...state.currentThread, messages: [...state.currentThread.messages, aiResponse] }
        : state.currentThread,
    }));

    return aiResponse;
  },

  setCurrentThread: (thread: Thread | null) => set({ currentThread: thread }),
}));

// ============== PROJECTS STORE ==============
interface ProjectsState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  fetchProjects: (sphereId?: SphereId) => Promise<void>;
  createProject: (data: Partial<Project>) => Promise<Project>;
  updateProject: (id: string, data: Partial<Project>) => void;
  deleteProject: (id: string) => void;
  addTask: (projectId: string, task: Partial<Task>) => void;
  updateTask: (projectId: string, taskId: string, data: Partial<Task>) => void;
}

export const useProjectsStore = create<ProjectsState>((set, get) => ({
  projects: [],
  currentProject: null,
  isLoading: false,

  fetchProjects: async (sphereId?: SphereId) => {
    set({ isLoading: true });
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const mockProjects: Project[] = [
      {
        id: '1',
        name: 'Rénovation Bureau Principal',
        description: 'Rénovation complète des bureaux du siège social',
        sphere: 'realestate',
        status: 'active',
        priority: 'high',
        progress: 65,
        budget: { total: 150000, spent: 97500, currency: 'CAD', categories: [] },
        team: [],
        tasks: [
          { id: 't1', title: 'Démolition', status: 'done', priority: 'high', createdAt: new Date() },
          { id: 't2', title: 'Électricité', status: 'in_progress', priority: 'high', createdAt: new Date() },
          { id: 't3', title: 'Peinture', status: 'todo', priority: 'medium', createdAt: new Date() },
        ],
        milestones: [],
        startDate: new Date('2024-01-15'),
        endDate: new Date('2024-06-30'),
        createdAt: new Date(),
      },
      {
        id: '2',
        name: 'Application Mobile CHE·NU',
        description: 'Développement de l\'application mobile',
        sphere: 'projects',
        status: 'active',
        priority: 'critical',
        progress: 80,
        team: [],
        tasks: [],
        milestones: [],
        startDate: new Date('2024-03-01'),
        createdAt: new Date(),
      },
    ];

    const filtered = sphereId 
      ? mockProjects.filter(p => p.sphere === sphereId)
      : mockProjects;

    set({ projects: filtered, isLoading: false });
  },

  createProject: async (data: Partial<Project>) => {
    const newProject: Project = {
      id: Date.now().toString(),
      name: data.name || 'Nouveau projet',
      description: data.description || '',
      sphere: data.sphere || 'projects',
      status: 'draft',
      priority: data.priority || 'medium',
      progress: 0,
      team: [],
      tasks: [],
      milestones: [],
      startDate: new Date(),
      createdAt: new Date(),
      ...data,
    };
    
    set(state => ({ projects: [newProject, ...state.projects] }));
    return newProject;
  },

  updateProject: (id: string, data: Partial<Project>) => {
    set(state => ({
      projects: state.projects.map(p => p.id === id ? { ...p, ...data } : p),
    }));
  },

  deleteProject: (id: string) => {
    set(state => ({
      projects: state.projects.filter(p => p.id !== id),
    }));
  },

  addTask: (projectId: string, task: Partial<Task>) => {
    const newTask: Task = {
      id: Date.now().toString(),
      title: task.title || 'Nouvelle tâche',
      status: 'todo',
      priority: task.priority || 'medium',
      createdAt: new Date(),
      ...task,
    };

    set(state => ({
      projects: state.projects.map(p => 
        p.id === projectId 
          ? { ...p, tasks: [...p.tasks, newTask] }
          : p
      ),
    }));
  },

  updateTask: (projectId: string, taskId: string, data: Partial<Task>) => {
    set(state => ({
      projects: state.projects.map(p => 
        p.id === projectId 
          ? { 
              ...p, 
              tasks: p.tasks.map(t => t.id === taskId ? { ...t, ...data } : t) 
            }
          : p
      ),
    }));
  },
}));

// ============== NOTIFICATIONS STORE ==============
interface NotificationsState {
  notifications: Notification[];
  unreadCount: number;
  addNotification: (notification: Omit<Notification, 'id' | 'createdAt' | 'isRead'>) => void;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
}

export const useNotificationsStore = create<NotificationsState>((set, get) => ({
  notifications: [],
  unreadCount: 0,

  addNotification: (notification) => {
    const newNotif: Notification = {
      id: Date.now().toString(),
      ...notification,
      isRead: false,
      createdAt: new Date(),
    };
    
    set(state => ({
      notifications: [newNotif, ...state.notifications],
      unreadCount: state.unreadCount + 1,
    }));
  },

  markAsRead: (id: string) => {
    set(state => ({
      notifications: state.notifications.map(n => 
        n.id === id ? { ...n, isRead: true } : n
      ),
      unreadCount: Math.max(0, state.unreadCount - 1),
    }));
  },

  markAllAsRead: () => {
    set(state => ({
      notifications: state.notifications.map(n => ({ ...n, isRead: true })),
      unreadCount: 0,
    }));
  },

  removeNotification: (id: string) => {
    set(state => {
      const notif = state.notifications.find(n => n.id === id);
      return {
        notifications: state.notifications.filter(n => n.id !== id),
        unreadCount: notif && !notif.isRead 
          ? Math.max(0, state.unreadCount - 1) 
          : state.unreadCount,
      };
    });
  },

  clearAll: () => set({ notifications: [], unreadCount: 0 }),
}));

// ============== UI STORE ==============
interface UIState {
  theme: 'light' | 'dark';
  language: 'fr' | 'en';
  isDrawerOpen: boolean;
  isSearchOpen: boolean;
  isVoiceActive: boolean;
  setTheme: (theme: 'light' | 'dark') => void;
  setLanguage: (lang: 'fr' | 'en') => void;
  toggleDrawer: () => void;
  toggleSearch: () => void;
  toggleVoice: () => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      theme: 'dark',
      language: 'fr',
      isDrawerOpen: false,
      isSearchOpen: false,
      isVoiceActive: false,

      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
      toggleDrawer: () => set(state => ({ isDrawerOpen: !state.isDrawerOpen })),
      toggleSearch: () => set(state => ({ isSearchOpen: !state.isSearchOpen })),
      toggleVoice: () => set(state => ({ isVoiceActive: !state.isVoiceActive })),
    }),
    {
      name: 'chenu-ui',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
