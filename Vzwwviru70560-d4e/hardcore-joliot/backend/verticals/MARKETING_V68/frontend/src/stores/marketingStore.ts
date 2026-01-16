/**
 * CHE·NU™ V68 - Marketing Automation Store
 * Complete state management for HubSpot/Mailchimp killer
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

// ============================================================================
// TYPES
// ============================================================================

export type ContactStatus = 'active' | 'unsubscribed' | 'bounced' | 'complained' | 'pending';
export type CampaignStatus = 'draft' | 'scheduled' | 'sending' | 'sent' | 'paused' | 'cancelled';
export type CampaignType = 'email' | 'sms' | 'push' | 'social';
export type AutomationTrigger = 'signup' | 'tag_added' | 'form_submit' | 'email_opened' | 'email_clicked' | 'page_visited' | 'purchase' | 'date_based' | 'custom';
export type LeadScoreCategory = 'cold' | 'warm' | 'hot' | 'qualified';

export interface Contact {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  company?: string;
  job_title?: string;
  status: ContactStatus;
  tags: string[];
  segments: string[];
  lead_score: number;
  source?: string;
  custom_fields: Record<string, any>;
  email_stats: {
    sent: number;
    opened: number;
    clicked: number;
    bounced: number;
  };
  created_at: string;
  last_activity?: string;
}

export interface Segment {
  id: string;
  name: string;
  description?: string;
  conditions: SegmentCondition[];
  contact_count: number;
  is_dynamic: boolean;
  created_at: string;
}

export interface SegmentCondition {
  field: string;
  operator: string;
  value: any;
}

export interface EmailTemplate {
  id: string;
  name: string;
  subject: string;
  preview_text: string;
  html_content: string;
  text_content: string;
  category: string;
  variables: string[];
  created_at: string;
}

export interface Campaign {
  id: string;
  name: string;
  campaign_type: CampaignType;
  status: CampaignStatus;
  subject: string;
  preview_text: string;
  from_name: string;
  from_email: string;
  html_content: string;
  segment_ids: string[];
  scheduled_at?: string;
  sent_at?: string;
  stats: CampaignStats;
  ab_test?: { id: string; status: string };
  created_at: string;
}

export interface CampaignStats {
  recipients: number;
  sent: number;
  delivered: number;
  opened: number;
  clicked: number;
  bounced: number;
  unsubscribed: number;
  complained: number;
  delivery_rate?: number;
  open_rate?: number;
  click_rate?: number;
}

export interface ABTest {
  id: string;
  campaign_id: string;
  test_type: string;
  variants: ABTestVariant[];
  winner_criteria: string;
  test_size_percent: number;
  status: string;
  winner_id?: string;
  created_at: string;
}

export interface ABTestVariant {
  id: string;
  name: string;
  value: string;
  sent?: number;
  opens?: number;
  clicks?: number;
  open_rate?: number;
  click_rate?: number;
}

export interface Automation {
  id: string;
  name: string;
  description?: string;
  trigger: AutomationTrigger;
  trigger_config: Record<string, any>;
  steps: AutomationStep[];
  is_active: boolean;
  stats: {
    enrolled: number;
    completed: number;
    active: number;
    exited: number;
  };
  created_at: string;
}

export interface AutomationStep {
  id: string;
  action: string;
  config: Record<string, any>;
  created_at: string;
}

export interface LandingPage {
  id: string;
  name: string;
  slug: string;
  html_content: string;
  css_content: string;
  meta_title: string;
  meta_description: string;
  is_published: boolean;
  published_at?: string;
  form_id?: string;
  stats: {
    views: number;
    unique_visitors: number;
    conversions: number;
  };
  created_at: string;
}

export interface Form {
  id: string;
  name: string;
  fields: FormField[];
  submit_button_text: string;
  success_message: string;
  redirect_url?: string;
  tags_to_add: string[];
  automation_id?: string;
  submissions_count: number;
  created_at: string;
}

export interface FormField {
  name: string;
  type: string;
  label: string;
  required: boolean;
  options?: string[];
  placeholder?: string;
}

export interface SubjectOptimization {
  original: {
    subject: string;
    score: number;
    predicted_open_rate: number;
  };
  suggestions: {
    subject: string;
    predicted_open_rate: number;
    improvement: string;
    reasoning: string;
  }[];
  best_practices: string[];
}

export interface SendTimeRecommendation {
  recommended: {
    day: string;
    time: string;
    score: number;
    reason: string;
  };
  alternatives: {
    day: string;
    time: string;
    score: number;
    reason: string;
  }[];
  avoid: {
    day: string;
    time: string;
    reason: string;
  }[];
}

export interface LeadScore {
  score: number;
  category: LeadScoreCategory;
  breakdown: Record<string, number>;
  recommendations: string[];
}

export interface DashboardStats {
  contacts: {
    total: number;
    active: number;
    new_this_month: number;
    growth_rate: number;
  };
  campaigns: {
    total: number;
    sent: number;
    emails_sent: number;
    avg_open_rate: number;
    avg_click_rate: number;
  };
  automations: {
    total: number;
    active: number;
    contacts_enrolled: number;
  };
  segments: {
    total: number;
  };
  forms: {
    total: number;
    submissions_this_month: number;
  };
  landing_pages: {
    total: number;
    published: number;
  };
}

// ============================================================================
// STORE STATE
// ============================================================================

interface MarketingState {
  // Data
  contacts: Contact[];
  segments: Segment[];
  templates: EmailTemplate[];
  campaigns: Campaign[];
  automations: Automation[];
  landingPages: LandingPage[];
  forms: Form[];
  
  // Selected items
  selectedContact: Contact | null;
  selectedCampaign: Campaign | null;
  selectedAutomation: Automation | null;
  
  // AI results
  subjectOptimization: SubjectOptimization | null;
  sendTimeRecommendation: SendTimeRecommendation | null;
  
  // Dashboard
  dashboardStats: DashboardStats | null;
  
  // UI State
  activeTab: 'dashboard' | 'contacts' | 'campaigns' | 'automations' | 'pages' | 'forms';
  isLoading: boolean;
  error: string | null;
  
  // Modals
  showContactModal: boolean;
  showCampaignModal: boolean;
  showAutomationModal: boolean;
  showTemplateModal: boolean;
  showFormModal: boolean;
  showPageModal: boolean;
  showABTestModal: boolean;
  
  // Actions - Contacts
  fetchContacts: (filters?: ContactFilters) => Promise<void>;
  createContact: (contact: CreateContactInput) => Promise<Contact>;
  updateContact: (id: string, updates: Partial<Contact>) => Promise<void>;
  addTags: (contactId: string, tags: string[]) => Promise<void>;
  removeTags: (contactId: string, tags: string[]) => Promise<void>;
  unsubscribeContact: (contactId: string) => Promise<void>;
  getLeadScore: (contactId: string) => Promise<LeadScore>;
  
  // Actions - Segments
  fetchSegments: () => Promise<void>;
  createSegment: (segment: CreateSegmentInput) => Promise<Segment>;
  
  // Actions - Templates
  fetchTemplates: (category?: string) => Promise<void>;
  createTemplate: (template: CreateTemplateInput) => Promise<EmailTemplate>;
  
  // Actions - Campaigns
  fetchCampaigns: (status?: CampaignStatus) => Promise<void>;
  createCampaign: (campaign: CreateCampaignInput) => Promise<Campaign>;
  updateCampaign: (id: string, updates: Partial<Campaign>) => Promise<void>;
  scheduleCampaign: (id: string, scheduledAt: Date) => Promise<void>;
  sendCampaign: (id: string) => Promise<void>;
  pauseCampaign: (id: string) => Promise<void>;
  getCampaignStats: (id: string) => Promise<CampaignStats>;
  
  // Actions - A/B Testing
  createABTest: (campaignId: string, test: CreateABTestInput) => Promise<ABTest>;
  getABTestResults: (testId: string) => Promise<any>;
  
  // Actions - Automations
  fetchAutomations: (activeOnly?: boolean) => Promise<void>;
  createAutomation: (automation: CreateAutomationInput) => Promise<Automation>;
  addAutomationStep: (automationId: string, step: CreateStepInput) => Promise<void>;
  activateAutomation: (id: string) => Promise<void>;
  deactivateAutomation: (id: string) => Promise<void>;
  triggerAutomation: (automationId: string, contactId: string) => Promise<void>;
  
  // Actions - Landing Pages
  fetchLandingPages: () => Promise<void>;
  createLandingPage: (page: CreatePageInput) => Promise<LandingPage>;
  publishPage: (id: string) => Promise<void>;
  unpublishPage: (id: string) => Promise<void>;
  
  // Actions - Forms
  fetchForms: () => Promise<void>;
  createForm: (form: CreateFormInput) => Promise<Form>;
  submitForm: (formId: string, data: Record<string, any>) => Promise<void>;
  
  // Actions - AI
  optimizeSubject: (subject: string) => Promise<SubjectOptimization>;
  getSendTimeRecommendation: () => Promise<SendTimeRecommendation>;
  getContentSuggestions: (topic: string, tone?: string) => Promise<any>;
  autoSegmentContacts: () => Promise<Record<string, string[]>>;
  
  // Actions - Dashboard
  fetchDashboard: () => Promise<void>;
  
  // UI Actions
  setActiveTab: (tab: MarketingState['activeTab']) => void;
  setSelectedContact: (contact: Contact | null) => void;
  setSelectedCampaign: (campaign: Campaign | null) => void;
  setSelectedAutomation: (automation: Automation | null) => void;
  toggleModal: (modal: string, show: boolean) => void;
  clearError: () => void;
}

// Input types
interface ContactFilters {
  status?: ContactStatus;
  tag?: string;
  segment_id?: string;
  search?: string;
}

interface CreateContactInput {
  email: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  company?: string;
  tags?: string[];
  source?: string;
}

interface CreateSegmentInput {
  name: string;
  description?: string;
  conditions?: SegmentCondition[];
}

interface CreateTemplateInput {
  name: string;
  subject: string;
  html_content: string;
  text_content?: string;
  category?: string;
}

interface CreateCampaignInput {
  name: string;
  campaign_type?: CampaignType;
  subject: string;
  from_name: string;
  from_email: string;
  html_content: string;
  segment_ids?: string[];
}

interface CreateABTestInput {
  test_type: string;
  variants: { name: string; value: string }[];
  test_size_percent?: number;
}

interface CreateAutomationInput {
  name: string;
  description?: string;
  trigger: AutomationTrigger;
  trigger_config?: Record<string, any>;
}

interface CreateStepInput {
  action: string;
  config?: Record<string, any>;
  position?: number;
}

interface CreatePageInput {
  name: string;
  slug: string;
  html_content?: string;
  meta_title?: string;
  meta_description?: string;
}

interface CreateFormInput {
  name: string;
  fields?: FormField[];
  submit_button_text?: string;
  tags_to_add?: string[];
  automation_id?: string;
}

// ============================================================================
// API HELPERS
// ============================================================================

const API_BASE = '/api/v2/marketing';

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
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

// ============================================================================
// STORE
// ============================================================================

export const useMarketingStore = create<MarketingState>()(
  devtools(
    (set, get) => ({
      // Initial state
      contacts: [],
      segments: [],
      templates: [],
      campaigns: [],
      automations: [],
      landingPages: [],
      forms: [],
      
      selectedContact: null,
      selectedCampaign: null,
      selectedAutomation: null,
      
      subjectOptimization: null,
      sendTimeRecommendation: null,
      
      dashboardStats: null,
      
      activeTab: 'dashboard',
      isLoading: false,
      error: null,
      
      showContactModal: false,
      showCampaignModal: false,
      showAutomationModal: false,
      showTemplateModal: false,
      showFormModal: false,
      showPageModal: false,
      showABTestModal: false,

      // ========================================================================
      // CONTACTS
      // ========================================================================
      
      fetchContacts: async (filters) => {
        set({ isLoading: true, error: null });
        try {
          const params = new URLSearchParams({ workspace_id: 'default' });
          if (filters?.status) params.append('status', filters.status);
          if (filters?.tag) params.append('tag', filters.tag);
          if (filters?.search) params.append('search', filters.search);
          
          const data = await apiCall<{ contacts: Contact[] }>(`/contacts?${params}`);
          set({ contacts: data.contacts, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },

      createContact: async (input) => {
        set({ isLoading: true, error: null });
        try {
          const data = await apiCall<{ contact: Contact }>('/contacts?user_id=current', {
            method: 'POST',
            body: JSON.stringify(input),
          });
          set(state => ({
            contacts: [data.contact, ...state.contacts],
            isLoading: false,
            showContactModal: false,
          }));
          return data.contact;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },

      updateContact: async (id, updates) => {
        try {
          const data = await apiCall<{ contact: Contact }>(`/contacts/${id}?user_id=current`, {
            method: 'PUT',
            body: JSON.stringify(updates),
          });
          set(state => ({
            contacts: state.contacts.map(c => c.id === id ? data.contact : c),
            selectedContact: state.selectedContact?.id === id ? data.contact : state.selectedContact,
          }));
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      addTags: async (contactId, tags) => {
        try {
          const data = await apiCall<{ contact: Contact }>(`/contacts/${contactId}/tags`, {
            method: 'POST',
            body: JSON.stringify({ tags }),
          });
          set(state => ({
            contacts: state.contacts.map(c => c.id === contactId ? data.contact : c),
          }));
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      removeTags: async (contactId, tags) => {
        try {
          const data = await apiCall<{ contact: Contact }>(`/contacts/${contactId}/tags`, {
            method: 'DELETE',
            body: JSON.stringify({ tags }),
          });
          set(state => ({
            contacts: state.contacts.map(c => c.id === contactId ? data.contact : c),
          }));
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      unsubscribeContact: async (contactId) => {
        try {
          await apiCall(`/contacts/${contactId}/unsubscribe`, { method: 'POST' });
          set(state => ({
            contacts: state.contacts.map(c => 
              c.id === contactId ? { ...c, status: 'unsubscribed' as ContactStatus } : c
            ),
          }));
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      getLeadScore: async (contactId) => {
        const data = await apiCall<LeadScore>(`/contacts/${contactId}/lead-score`);
        return data;
      },

      // ========================================================================
      // SEGMENTS
      // ========================================================================
      
      fetchSegments: async () => {
        try {
          const data = await apiCall<{ segments: Segment[] }>('/workspaces/default/segments');
          set({ segments: data.segments });
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      createSegment: async (input) => {
        const data = await apiCall<{ segment: Segment }>('/workspaces/default/segments?user_id=current', {
          method: 'POST',
          body: JSON.stringify(input),
        });
        set(state => ({ segments: [data.segment, ...state.segments] }));
        return data.segment;
      },

      // ========================================================================
      // TEMPLATES
      // ========================================================================
      
      fetchTemplates: async (category) => {
        try {
          const params = category ? `?category=${category}` : '';
          const data = await apiCall<{ templates: EmailTemplate[] }>(`/workspaces/default/templates${params}`);
          set({ templates: data.templates });
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      createTemplate: async (input) => {
        const data = await apiCall<{ template: EmailTemplate }>('/workspaces/default/templates?user_id=current', {
          method: 'POST',
          body: JSON.stringify(input),
        });
        set(state => ({
          templates: [data.template, ...state.templates],
          showTemplateModal: false,
        }));
        return data.template;
      },

      // ========================================================================
      // CAMPAIGNS
      // ========================================================================
      
      fetchCampaigns: async (status) => {
        set({ isLoading: true });
        try {
          const params = status ? `?status=${status}` : '';
          const data = await apiCall<{ campaigns: Campaign[] }>(`/workspaces/default/campaigns${params}`);
          set({ campaigns: data.campaigns, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },

      createCampaign: async (input) => {
        set({ isLoading: true });
        try {
          const data = await apiCall<{ campaign: Campaign }>('/workspaces/default/campaigns?user_id=current', {
            method: 'POST',
            body: JSON.stringify(input),
          });
          set(state => ({
            campaigns: [data.campaign, ...state.campaigns],
            isLoading: false,
            showCampaignModal: false,
          }));
          return data.campaign;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },

      updateCampaign: async (id, updates) => {
        try {
          const data = await apiCall<{ campaign: Campaign }>(`/campaigns/${id}`, {
            method: 'PUT',
            body: JSON.stringify(updates),
          });
          set(state => ({
            campaigns: state.campaigns.map(c => c.id === id ? data.campaign : c),
            selectedCampaign: state.selectedCampaign?.id === id ? data.campaign : state.selectedCampaign,
          }));
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      scheduleCampaign: async (id, scheduledAt) => {
        try {
          const data = await apiCall<{ campaign: Campaign }>(`/campaigns/${id}/schedule?user_id=current`, {
            method: 'POST',
            body: JSON.stringify({ scheduled_at: scheduledAt.toISOString() }),
          });
          set(state => ({
            campaigns: state.campaigns.map(c => c.id === id ? data.campaign : c),
          }));
        } catch (error: any) {
          set({ error: error.message });
          throw error;
        }
      },

      sendCampaign: async (id) => {
        try {
          const data = await apiCall<{ campaign: Campaign }>(`/campaigns/${id}/send?user_id=current`, {
            method: 'POST',
          });
          set(state => ({
            campaigns: state.campaigns.map(c => c.id === id ? data.campaign : c),
          }));
        } catch (error: any) {
          set({ error: error.message });
          throw error;
        }
      },

      pauseCampaign: async (id) => {
        try {
          const data = await apiCall<{ campaign: Campaign }>(`/campaigns/${id}/pause`, {
            method: 'POST',
          });
          set(state => ({
            campaigns: state.campaigns.map(c => c.id === id ? data.campaign : c),
          }));
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      getCampaignStats: async (id) => {
        return apiCall<CampaignStats>(`/campaigns/${id}/stats`);
      },

      // ========================================================================
      // A/B TESTING
      // ========================================================================
      
      createABTest: async (campaignId, input) => {
        const data = await apiCall<{ ab_test: ABTest }>(`/campaigns/${campaignId}/ab-test?user_id=current`, {
          method: 'POST',
          body: JSON.stringify(input),
        });
        set({ showABTestModal: false });
        return data.ab_test;
      },

      getABTestResults: async (testId) => {
        return apiCall(`/ab-tests/${testId}/results`);
      },

      // ========================================================================
      // AUTOMATIONS
      // ========================================================================
      
      fetchAutomations: async (activeOnly) => {
        try {
          const params = activeOnly ? '?active_only=true' : '';
          const data = await apiCall<{ automations: Automation[] }>(`/workspaces/default/automations${params}`);
          set({ automations: data.automations });
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      createAutomation: async (input) => {
        const data = await apiCall<{ automation: Automation }>('/workspaces/default/automations?user_id=current', {
          method: 'POST',
          body: JSON.stringify(input),
        });
        set(state => ({
          automations: [data.automation, ...state.automations],
          showAutomationModal: false,
        }));
        return data.automation;
      },

      addAutomationStep: async (automationId, step) => {
        const data = await apiCall<{ automation: Automation }>(`/automations/${automationId}/steps`, {
          method: 'POST',
          body: JSON.stringify(step),
        });
        set(state => ({
          automations: state.automations.map(a => a.id === automationId ? data.automation : a),
          selectedAutomation: state.selectedAutomation?.id === automationId ? data.automation : state.selectedAutomation,
        }));
      },

      activateAutomation: async (id) => {
        const data = await apiCall<{ automation: Automation }>(`/automations/${id}/activate`, {
          method: 'POST',
        });
        set(state => ({
          automations: state.automations.map(a => a.id === id ? data.automation : a),
        }));
      },

      deactivateAutomation: async (id) => {
        const data = await apiCall<{ automation: Automation }>(`/automations/${id}/deactivate`, {
          method: 'POST',
        });
        set(state => ({
          automations: state.automations.map(a => a.id === id ? data.automation : a),
        }));
      },

      triggerAutomation: async (automationId, contactId) => {
        await apiCall(`/automations/${automationId}/trigger?contact_id=${contactId}`, {
          method: 'POST',
        });
      },

      // ========================================================================
      // LANDING PAGES
      // ========================================================================
      
      fetchLandingPages: async () => {
        try {
          const data = await apiCall<{ landing_pages: LandingPage[] }>('/workspaces/default/landing-pages');
          set({ landingPages: data.landing_pages });
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      createLandingPage: async (input) => {
        const data = await apiCall<{ landing_page: LandingPage }>('/workspaces/default/landing-pages?user_id=current', {
          method: 'POST',
          body: JSON.stringify(input),
        });
        set(state => ({
          landingPages: [data.landing_page, ...state.landingPages],
          showPageModal: false,
        }));
        return data.landing_page;
      },

      publishPage: async (id) => {
        const data = await apiCall<{ landing_page: LandingPage }>(`/landing-pages/${id}/publish`, {
          method: 'POST',
        });
        set(state => ({
          landingPages: state.landingPages.map(p => p.id === id ? data.landing_page : p),
        }));
      },

      unpublishPage: async (id) => {
        const data = await apiCall<{ landing_page: LandingPage }>(`/landing-pages/${id}/unpublish`, {
          method: 'POST',
        });
        set(state => ({
          landingPages: state.landingPages.map(p => p.id === id ? data.landing_page : p),
        }));
      },

      // ========================================================================
      // FORMS
      // ========================================================================
      
      fetchForms: async () => {
        try {
          const data = await apiCall<{ forms: Form[] }>('/workspaces/default/forms');
          set({ forms: data.forms });
        } catch (error: any) {
          set({ error: error.message });
        }
      },

      createForm: async (input) => {
        const data = await apiCall<{ form: Form }>('/workspaces/default/forms?user_id=current', {
          method: 'POST',
          body: JSON.stringify(input),
        });
        set(state => ({
          forms: [data.form, ...state.forms],
          showFormModal: false,
        }));
        return data.form;
      },

      submitForm: async (formId, data) => {
        await apiCall(`/forms/${formId}/submit`, {
          method: 'POST',
          body: JSON.stringify({ data }),
        });
      },

      // ========================================================================
      // AI FEATURES
      // ========================================================================
      
      optimizeSubject: async (subject) => {
        set({ isLoading: true });
        try {
          const data = await apiCall<SubjectOptimization>('/ai/optimize-subject', {
            method: 'POST',
            body: JSON.stringify({ subject }),
          });
          set({ subjectOptimization: data, isLoading: false });
          return data;
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
          throw error;
        }
      },

      getSendTimeRecommendation: async () => {
        const data = await apiCall<SendTimeRecommendation>('/ai/send-time');
        set({ sendTimeRecommendation: data });
        return data;
      },

      getContentSuggestions: async (topic, tone = 'professional') => {
        return apiCall('/ai/content-suggestions', {
          method: 'POST',
          body: JSON.stringify({ topic, tone }),
        });
      },

      autoSegmentContacts: async () => {
        return apiCall('/ai/auto-segment?workspace_id=default');
      },

      // ========================================================================
      // DASHBOARD
      // ========================================================================
      
      fetchDashboard: async () => {
        set({ isLoading: true });
        try {
          const data = await apiCall<DashboardStats>('/workspaces/default/dashboard');
          set({ dashboardStats: data, isLoading: false });
        } catch (error: any) {
          set({ error: error.message, isLoading: false });
        }
      },

      // ========================================================================
      // UI ACTIONS
      // ========================================================================
      
      setActiveTab: (tab) => set({ activeTab: tab }),
      
      setSelectedContact: (contact) => set({ selectedContact: contact }),
      
      setSelectedCampaign: (campaign) => set({ selectedCampaign: campaign }),
      
      setSelectedAutomation: (automation) => set({ selectedAutomation: automation }),
      
      toggleModal: (modal, show) => {
        const modalKey = `show${modal.charAt(0).toUpperCase() + modal.slice(1)}Modal` as keyof MarketingState;
        set({ [modalKey]: show } as any);
      },
      
      clearError: () => set({ error: null }),
    }),
    { name: 'marketing-store' }
  )
);

export default useMarketingStore;
