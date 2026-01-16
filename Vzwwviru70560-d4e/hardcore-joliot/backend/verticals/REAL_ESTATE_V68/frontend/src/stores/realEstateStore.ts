/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ REAL ESTATE STORE — V68                           ║
 * ║                                                                              ║
 * ║  Zustand state management for property management.                           ║
 * ║  Quebec-first with RBQ compliance features.                                  ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export type PropertyType = 
  | 'residential'
  | 'commercial'
  | 'industrial'
  | 'land'
  | 'multi_family'
  | 'condo'
  | 'duplex'
  | 'triplex';

export type PropertyStatus = 
  | 'available'
  | 'rented'
  | 'for_sale'
  | 'under_contract'
  | 'renovation'
  | 'off_market';

export type LeaseStatus = 'active' | 'pending' | 'expired' | 'terminated' | 'renewed';

export type MaintenanceStatus = 
  | 'open'
  | 'in_progress'
  | 'waiting_parts'
  | 'scheduled'
  | 'completed'
  | 'cancelled';

export type MaintenancePriority = 'emergency' | 'high' | 'medium' | 'low';

export interface Property {
  id: string;
  name: string;
  address: string;
  city: string;
  province: string;
  postal_code: string;
  property_type: PropertyType;
  status: PropertyStatus;
  units: number;
  bedrooms?: number;
  bathrooms?: number;
  square_feet?: number;
  year_built?: number;
  purchase_price?: number;
  current_value?: number;
  monthly_rent?: number;
  monthly_expenses?: number;
  municipal_tax?: number;
  school_tax?: number;
  description?: string;
  features: string[];
  created_at: string;
}

export interface Tenant {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  property_id?: string;
  unit_number?: string;
  lease_start?: string;
  lease_end?: string;
  monthly_rent?: number;
  is_active: boolean;
  balance: number;
  created_at: string;
}

export interface Lease {
  id: string;
  property_id: string;
  tenant_id: string;
  unit_number?: string;
  start_date: string;
  end_date: string;
  monthly_rent: number;
  security_deposit: number;
  status: LeaseStatus;
  is_renewed: boolean;
  created_at: string;
}

export interface MaintenanceRequest {
  id: string;
  property_id: string;
  tenant_id?: string;
  unit_number?: string;
  title: string;
  description: string;
  category: string;
  priority: MaintenancePriority;
  status: MaintenanceStatus;
  reported_date: string;
  scheduled_date?: string;
  completed_date?: string;
  contractor_id?: string;
  contractor_name?: string;
  estimated_cost?: number;
  actual_cost?: number;
}

export interface Contractor {
  id: string;
  name: string;
  company?: string;
  phone: string;
  email?: string;
  categories: string[];
  rbq_license?: string;
  rbq_verified: boolean;
  rbq_valid_until?: string;
  rating: number;
  completed_jobs: number;
  is_active: boolean;
}

export interface Payment {
  id: string;
  property_id: string;
  tenant_id: string;
  lease_id: string;
  amount: number;
  payment_date: string;
  payment_method: string;
  period_start: string;
  period_end: string;
  is_late: boolean;
  late_fee: number;
  created_at: string;
}

export interface PropertyAnalysis {
  property_id: string;
  cap_rate: number;
  cash_on_cash: number;
  gross_rent_multiplier: number;
  monthly_cash_flow: number;
  annual_roi: number;
  market_value_estimate: number;
  rent_estimate: number;
  price_per_sqft?: number;
  insights: string[];
  improvements: string[];
  risks: string[];
  market_position: string;
  analyzed_at: string;
}

export interface RentIncrease {
  current_rent: number;
  allowed_increase_percent: number;
  increase_amount: number;
  new_rent: number;
  year: number;
  source: string;
  note: string;
}

export interface PortfolioStats {
  properties: {
    total: number;
    total_units: number;
    occupied: number;
    vacancy_rate: number;
  };
  tenants: {
    total: number;
    active: number;
  };
  financials: {
    total_portfolio_value: number;
    monthly_income: number;
    monthly_expenses: number;
    monthly_cash_flow: number;
    annual_income: number;
  };
  maintenance: {
    open_requests: number;
    emergency: number;
  };
  leases: {
    active: number;
    expiring_soon: number;
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE INTERFACE
// ═══════════════════════════════════════════════════════════════════════════════

interface RealEstateState {
  // Data
  properties: Property[];
  tenants: Tenant[];
  leases: Lease[];
  maintenance: MaintenanceRequest[];
  contractors: Contractor[];
  payments: Payment[];
  stats: PortfolioStats | null;
  
  // Selected items
  selectedProperty: Property | null;
  selectedTenant: Tenant | null;
  selectedLease: Lease | null;
  selectedMaintenance: MaintenanceRequest | null;
  
  // Analysis
  propertyAnalysis: PropertyAnalysis | null;
  rentIncrease: RentIncrease | null;
  
  // UI State
  activeTab: 'properties' | 'tenants' | 'leases' | 'maintenance' | 'payments' | 'stats';
  filters: {
    propertyType?: PropertyType;
    propertyStatus?: PropertyStatus;
    city?: string;
    maintenancePriority?: MaintenancePriority;
    maintenanceStatus?: MaintenanceStatus;
  };
  isLoading: boolean;
  error: string | null;
  
  // Actions - Properties
  fetchProperties: () => Promise<void>;
  createProperty: (data: Partial<Property>) => Promise<Property>;
  updateProperty: (id: string, data: Partial<Property>) => Promise<void>;
  analyzeProperty: (id: string) => Promise<void>;
  selectProperty: (property: Property | null) => void;
  
  // Actions - Tenants
  fetchTenants: () => Promise<void>;
  createTenant: (data: Partial<Tenant>) => Promise<Tenant>;
  selectTenant: (tenant: Tenant | null) => void;
  
  // Actions - Leases
  fetchLeases: () => Promise<void>;
  createLease: (data: Partial<Lease>) => Promise<Lease>;
  calculateRentIncrease: (leaseId: string, year: number) => Promise<void>;
  selectLease: (lease: Lease | null) => void;
  
  // Actions - Maintenance
  fetchMaintenance: () => Promise<void>;
  createMaintenance: (data: Partial<MaintenanceRequest>) => Promise<MaintenanceRequest>;
  updateMaintenanceStatus: (id: string, status: MaintenanceStatus) => Promise<void>;
  selectMaintenance: (request: MaintenanceRequest | null) => void;
  
  // Actions - Contractors
  fetchContractors: () => Promise<void>;
  createContractor: (data: Partial<Contractor>) => Promise<Contractor>;
  verifyContractorRBQ: (id: string) => Promise<void>;
  
  // Actions - Payments
  fetchPayments: () => Promise<void>;
  recordPayment: (data: Partial<Payment>) => Promise<Payment>;
  
  // Actions - Stats
  fetchStats: () => Promise<void>;
  
  // UI Actions
  setActiveTab: (tab: RealEstateState['activeTab']) => void;
  setFilters: (filters: RealEstateState['filters']) => void;
  clearError: () => void;
}

// ═══════════════════════════════════════════════════════════════════════════════
// API HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

const API_BASE = '/api/v2/immobilier';

async function apiCall<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `API Error: ${response.status}`);
  }
  
  return response.json();
}

// ═══════════════════════════════════════════════════════════════════════════════
// STORE
// ═══════════════════════════════════════════════════════════════════════════════

export const useRealEstateStore = create<RealEstateState>()(
  persist(
    (set, get) => ({
      // Initial state
      properties: [],
      tenants: [],
      leases: [],
      maintenance: [],
      contractors: [],
      payments: [],
      stats: null,
      selectedProperty: null,
      selectedTenant: null,
      selectedLease: null,
      selectedMaintenance: null,
      propertyAnalysis: null,
      rentIncrease: null,
      activeTab: 'properties',
      filters: {},
      isLoading: false,
      error: null,
      
      // ═══════════════════════════════════════════════════════════════════════
      // PROPERTY ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      fetchProperties: async () => {
        set({ isLoading: true, error: null });
        try {
          const { filters } = get();
          const params = new URLSearchParams();
          if (filters.propertyType) params.append('property_type', filters.propertyType);
          if (filters.propertyStatus) params.append('status', filters.propertyStatus);
          if (filters.city) params.append('city', filters.city);
          
          const properties = await apiCall<Property[]>(`/properties?${params}`);
          set({ properties, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createProperty: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const property = await apiCall<Property>('/properties', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set((state) => ({
            properties: [...state.properties, property],
            isLoading: false,
          }));
          return property;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      updateProperty: async (id, data) => {
        set({ isLoading: true, error: null });
        try {
          const updated = await apiCall<Property>(`/properties/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
          });
          set((state) => ({
            properties: state.properties.map((p) => (p.id === id ? updated : p)),
            selectedProperty: state.selectedProperty?.id === id ? updated : state.selectedProperty,
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      analyzeProperty: async (id) => {
        set({ isLoading: true, error: null });
        try {
          const analysis = await apiCall<PropertyAnalysis>(`/properties/${id}/analyze`, {
            method: 'POST',
          });
          set({ propertyAnalysis: analysis, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      selectProperty: (property) => {
        set({ selectedProperty: property, propertyAnalysis: null });
      },
      
      // ═══════════════════════════════════════════════════════════════════════
      // TENANT ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      fetchTenants: async () => {
        set({ isLoading: true, error: null });
        try {
          const tenants = await apiCall<Tenant[]>('/tenants');
          set({ tenants, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createTenant: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const tenant = await apiCall<Tenant>('/tenants', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set((state) => ({
            tenants: [...state.tenants, tenant],
            isLoading: false,
          }));
          return tenant;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      selectTenant: (tenant) => {
        set({ selectedTenant: tenant });
      },
      
      // ═══════════════════════════════════════════════════════════════════════
      // LEASE ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      fetchLeases: async () => {
        set({ isLoading: true, error: null });
        try {
          const leases = await apiCall<Lease[]>('/leases');
          set({ leases, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createLease: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const lease = await apiCall<Lease>('/leases', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set((state) => ({
            leases: [...state.leases, lease],
            isLoading: false,
          }));
          // Refresh properties and tenants as they may be updated
          get().fetchProperties();
          get().fetchTenants();
          return lease;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      calculateRentIncrease: async (leaseId, year) => {
        set({ isLoading: true, error: null });
        try {
          const result = await apiCall<RentIncrease>(
            `/leases/${leaseId}/rent-increase?year=${year}`,
            { method: 'POST' }
          );
          set({ rentIncrease: result, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      selectLease: (lease) => {
        set({ selectedLease: lease, rentIncrease: null });
      },
      
      // ═══════════════════════════════════════════════════════════════════════
      // MAINTENANCE ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      fetchMaintenance: async () => {
        set({ isLoading: true, error: null });
        try {
          const { filters } = get();
          const params = new URLSearchParams();
          if (filters.maintenancePriority) params.append('priority', filters.maintenancePriority);
          if (filters.maintenanceStatus) params.append('status', filters.maintenanceStatus);
          
          const maintenance = await apiCall<MaintenanceRequest[]>(`/maintenance?${params}`);
          set({ maintenance, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createMaintenance: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const request = await apiCall<MaintenanceRequest>('/maintenance', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set((state) => ({
            maintenance: [request, ...state.maintenance],
            isLoading: false,
          }));
          return request;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      updateMaintenanceStatus: async (id, status) => {
        set({ isLoading: true, error: null });
        try {
          await apiCall(`/maintenance/${id}/status?status=${status}`, {
            method: 'PUT',
          });
          set((state) => ({
            maintenance: state.maintenance.map((m) =>
              m.id === id ? { ...m, status } : m
            ),
            isLoading: false,
          }));
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      selectMaintenance: (request) => {
        set({ selectedMaintenance: request });
      },
      
      // ═══════════════════════════════════════════════════════════════════════
      // CONTRACTOR ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      fetchContractors: async () => {
        set({ isLoading: true, error: null });
        try {
          const contractors = await apiCall<Contractor[]>('/contractors');
          set({ contractors, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      createContractor: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const contractor = await apiCall<Contractor>('/contractors', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set((state) => ({
            contractors: [...state.contractors, contractor],
            isLoading: false,
          }));
          return contractor;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      verifyContractorRBQ: async (id) => {
        set({ isLoading: true, error: null });
        try {
          await apiCall(`/contractors/${id}/verify-rbq`, { method: 'POST' });
          get().fetchContractors();
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      // ═══════════════════════════════════════════════════════════════════════
      // PAYMENT ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      fetchPayments: async () => {
        set({ isLoading: true, error: null });
        try {
          const payments = await apiCall<Payment[]>('/payments');
          set({ payments, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      recordPayment: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const payment = await apiCall<Payment>('/payments', {
            method: 'POST',
            body: JSON.stringify(data),
          });
          set((state) => ({
            payments: [payment, ...state.payments],
            isLoading: false,
          }));
          // Refresh tenants for balance update
          get().fetchTenants();
          return payment;
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
          throw error;
        }
      },
      
      // ═══════════════════════════════════════════════════════════════════════
      // STATS ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      fetchStats: async () => {
        set({ isLoading: true, error: null });
        try {
          const stats = await apiCall<PortfolioStats>('/stats');
          set({ stats, isLoading: false });
        } catch (error) {
          set({ error: (error as Error).message, isLoading: false });
        }
      },
      
      // ═══════════════════════════════════════════════════════════════════════
      // UI ACTIONS
      // ═══════════════════════════════════════════════════════════════════════
      
      setActiveTab: (tab) => {
        set({ activeTab: tab });
      },
      
      setFilters: (filters) => {
        set({ filters });
      },
      
      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'chenu-real-estate-storage',
      partialize: (state) => ({
        activeTab: state.activeTab,
        filters: state.filters,
      }),
    }
  )
);

export default useRealEstateStore;
