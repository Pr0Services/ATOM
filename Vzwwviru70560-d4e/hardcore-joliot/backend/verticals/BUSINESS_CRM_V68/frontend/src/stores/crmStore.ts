/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ BUSINESS CRM — STORE                              ║
 * ║                                                                              ║
 * ║  Zustand state management for CRM operations.                                ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface Company {
  id: string;
  name: string;
  domain?: string;
  industry?: string;
  size?: string;
  annual_revenue?: number;
  website?: string;
  contact_count: number;
  deal_count: number;
  created_at: string;
}

export interface Contact {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  title?: string;
  company_id?: string;
  company_name?: string;
  contact_type: string;
  lead_status: string;
  lead_source: string;
  lead_score: number;
  lead_score_breakdown: Record<string, number>;
  tags: string[];
  last_contacted?: string;
  created_at: string;
}

export interface Deal {
  id: string;
  name: string;
  contact_id: string;
  company_id?: string;
  stage: string;
  amount: number;
  currency: string;
  probability: number;
  expected_close_date?: string;
  actual_close_date?: string;
  created_at: string;
}

export interface Activity {
  id: string;
  activity_type: string;
  subject: string;
  description?: string;
  contact_id?: string;
  company_id?: string;
  deal_id?: string;
  scheduled_at?: string;
  completed_at?: string;
  duration_minutes?: number;
  outcome?: string;
  created_at: string;
}

export interface LeadScore {
  total_score: number;
  grade: string;
  breakdown: Record<string, number>;
  insights: string[];
  next_actions: string[];
  probability_to_close: number;
}

export interface EmailDraft {
  subject: string;
  body: string;
  tone: string;
  cta: string;
  personalization_points: string[];
}

export interface PipelineSummary {
  by_stage: Record<string, { count: number; value: number }>;
  total_pipeline_value: number;
  weighted_pipeline_value: number;
  open_deals: number;
  won_deals: number;
  won_value: number;
  lost_deals: number;
  win_rate: number;
}

export interface CRMStats {
  contacts: {
    total: number;
    hot_leads: number;
    warm_leads: number;
    cold_leads: number;
    avg_lead_score: number;
  };
  companies: {
    total: number;
  };
  deals: PipelineSummary;
  activities: {
    total: number;
    this_week: number;
  };
}

interface CRMState {
  // Data
  contacts: Contact[];
  companies: Company[];
  deals: Deal[];
  activities: Activity[];
  selectedContact: Contact | null;
  selectedDeal: Deal | null;
  pipelineSummary: PipelineSummary | null;
  stats: CRMStats | null;
  
  // UI State
  activeTab: 'contacts' | 'deals' | 'companies' | 'activities' | 'stats';
  filters: {
    leadStatus?: string;
    leadSource?: string;
    minScore?: number;
    dealStage?: string;
  };
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setActiveTab: (tab: CRMState['activeTab']) => void;
  setFilters: (filters: Partial<CRMState['filters']>) => void;
  
  // Company Actions
  fetchCompanies: () => Promise<void>;
  createCompany: (data: Partial<Company>) => Promise<Company>;
  
  // Contact Actions
  fetchContacts: () => Promise<void>;
  createContact: (data: Partial<Contact> & { first_name: string; last_name: string; email: string }) => Promise<Contact>;
  updateContact: (id: string, data: Partial<Contact>) => Promise<void>;
  deleteContact: (id: string) => Promise<void>;
  scoreContact: (id: string) => Promise<LeadScore>;
  selectContact: (contact: Contact | null) => void;
  
  // Deal Actions
  fetchDeals: () => Promise<void>;
  createDeal: (data: { name: string; contact_id: string; amount: number; stage?: string }) => Promise<Deal>;
  updateDealStage: (id: string, stage: string, lostReason?: string) => Promise<void>;
  selectDeal: (deal: Deal | null) => void;
  fetchPipelineSummary: () => Promise<void>;
  
  // Activity Actions
  fetchActivities: (contactId?: string) => Promise<void>;
  logActivity: (data: {
    activity_type: string;
    subject: string;
    contact_id?: string;
    description?: string;
    outcome?: string;
  }) => Promise<Activity>;
  
  // Email Actions
  generateEmail: (contactId: string, purpose: string) => Promise<EmailDraft>;
  
  // Stats
  fetchStats: () => Promise<void>;
}

// ═══════════════════════════════════════════════════════════════════════════════
// API CLIENT
// ═══════════════════════════════════════════════════════════════════════════════

const API_BASE = '/api/v2/business';

async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
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

export const useCRMStore = create<CRMState>()(
  persist(
    (set, get) => ({
      // Initial State
      contacts: [],
      companies: [],
      deals: [],
      activities: [],
      selectedContact: null,
      selectedDeal: null,
      pipelineSummary: null,
      stats: null,
      activeTab: 'contacts',
      filters: {},
      isLoading: false,
      error: null,
      
      // UI Actions
      setActiveTab: (tab) => set({ activeTab: tab }),
      setFilters: (filters) => set({ filters: { ...get().filters, ...filters } }),
      
      // Company Actions
      fetchCompanies: async () => {
        set({ isLoading: true, error: null });
        try {
          const companies = await apiCall<Company[]>('/companies');
          set({ companies, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createCompany: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const company = await apiCall<Company>('/companies', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set({ companies: [...get().companies, company], isLoading: false });
          return company;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      // Contact Actions
      fetchContacts: async () => {
        set({ isLoading: true, error: null });
        try {
          const { filters } = get();
          const params = new URLSearchParams();
          if (filters.leadStatus) params.append('lead_status', filters.leadStatus);
          if (filters.leadSource) params.append('lead_source', filters.leadSource);
          if (filters.minScore) params.append('min_score', String(filters.minScore));
          
          const contacts = await apiCall<Contact[]>(`/contacts?${params}`);
          set({ contacts, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createContact: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const contact = await apiCall<Contact>('/contacts', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set({ contacts: [...get().contacts, contact], isLoading: false });
          return contact;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      updateContact: async (id, data) => {
        set({ isLoading: true, error: null });
        try {
          const contact = await apiCall<Contact>(`/contacts/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
          });
          set({
            contacts: get().contacts.map(c => c.id === id ? contact : c),
            selectedContact: get().selectedContact?.id === id ? contact : get().selectedContact,
            isLoading: false,
          });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      deleteContact: async (id) => {
        set({ isLoading: true, error: null });
        try {
          await apiCall(`/contacts/${id}`, { method: 'DELETE' });
          set({
            contacts: get().contacts.filter(c => c.id !== id),
            selectedContact: get().selectedContact?.id === id ? null : get().selectedContact,
            isLoading: false,
          });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      scoreContact: async (id) => {
        set({ isLoading: true, error: null });
        try {
          const score = await apiCall<LeadScore>(`/contacts/${id}/score`, {
            method: 'POST',
          });
          // Refresh contact to get updated score
          await get().fetchContacts();
          set({ isLoading: false });
          return score;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      selectContact: (contact) => set({ selectedContact: contact }),
      
      // Deal Actions
      fetchDeals: async () => {
        set({ isLoading: true, error: null });
        try {
          const { filters } = get();
          const params = new URLSearchParams();
          if (filters.dealStage) params.append('stage', filters.dealStage);
          
          const deals = await apiCall<Deal[]>(`/deals?${params}`);
          set({ deals, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createDeal: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const deal = await apiCall<Deal>('/deals', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set({ deals: [...get().deals, deal], isLoading: false });
          return deal;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      updateDealStage: async (id, stage, lostReason) => {
        set({ isLoading: true, error: null });
        try {
          const deal = await apiCall<Deal>(`/deals/${id}/stage`, {
            method: 'PUT',
            body: JSON.stringify({ stage, lost_reason: lostReason }),
          });
          set({
            deals: get().deals.map(d => d.id === id ? deal : d),
            selectedDeal: get().selectedDeal?.id === id ? deal : get().selectedDeal,
            isLoading: false,
          });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      selectDeal: (deal) => set({ selectedDeal: deal }),
      
      fetchPipelineSummary: async () => {
        try {
          const summary = await apiCall<PipelineSummary>('/pipeline/summary');
          set({ pipelineSummary: summary });
        } catch (error) {
          console.error('Failed to fetch pipeline summary:', error);
        }
      },
      
      // Activity Actions
      fetchActivities: async (contactId) => {
        set({ isLoading: true, error: null });
        try {
          const params = contactId ? `?contact_id=${contactId}` : '';
          const activities = await apiCall<Activity[]>(`/activities${params}`);
          set({ activities, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      logActivity: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const activity = await apiCall<Activity>('/activities', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set({ activities: [activity, ...get().activities], isLoading: false });
          return activity;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      // Email Actions
      generateEmail: async (contactId, purpose) => {
        set({ isLoading: true, error: null });
        try {
          const draft = await apiCall<EmailDraft>('/emails/generate', {
            method: 'POST',
            body: JSON.stringify({ contact_id: contactId, purpose }),
          });
          set({ isLoading: false });
          return draft;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      // Stats
      fetchStats: async () => {
        try {
          const stats = await apiCall<CRMStats>('/stats');
          set({ stats });
        } catch (error) {
          console.error('Failed to fetch stats:', error);
        }
      },
    }),
    {
      name: 'chenu-crm-store',
      partialize: (state) => ({
        activeTab: state.activeTab,
        filters: state.filters,
      }),
    }
  )
);

export default useCRMStore;
