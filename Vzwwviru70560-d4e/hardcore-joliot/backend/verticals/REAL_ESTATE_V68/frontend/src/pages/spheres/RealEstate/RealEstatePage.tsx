/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ REAL ESTATE PAGE — V68                            ║
 * ║                                                                              ║
 * ║  Complete property management interface with RBQ Quebec compliance.          ║
 * ║  COS: 85/100 — Yardi Competitor                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import React, { useEffect, useState } from 'react';
import { useRealEstateStore } from '../../../stores/realEstateStore';
import type {
  Property,
  Tenant,
  Lease,
  MaintenanceRequest,
  PropertyType,
  PropertyStatus,
  MaintenancePriority,
  MaintenanceStatus,
} from '../../../stores/realEstateStore';

// ═══════════════════════════════════════════════════════════════════════════════
// HELPER COMPONENTS
// ═══════════════════════════════════════════════════════════════════════════════

const StatusBadge: React.FC<{ status: PropertyStatus }> = ({ status }) => {
  const colors: Record<PropertyStatus, string> = {
    available: 'bg-green-100 text-green-800',
    rented: 'bg-blue-100 text-blue-800',
    for_sale: 'bg-purple-100 text-purple-800',
    under_contract: 'bg-yellow-100 text-yellow-800',
    renovation: 'bg-orange-100 text-orange-800',
    off_market: 'bg-gray-100 text-gray-800',
  };
  
  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${colors[status]}`}>
      {status.replace('_', ' ').toUpperCase()}
    </span>
  );
};

const PriorityBadge: React.FC<{ priority: MaintenancePriority }> = ({ priority }) => {
  const colors: Record<MaintenancePriority, string> = {
    emergency: 'bg-red-100 text-red-800',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800',
  };
  
  const icons: Record<MaintenancePriority, string> = {
    emergency: '🚨',
    high: '⚠️',
    medium: '📋',
    low: '📝',
  };
  
  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${colors[priority]}`}>
      {icons[priority]} {priority.toUpperCase()}
    </span>
  );
};

const MaintenanceStatusBadge: React.FC<{ status: MaintenanceStatus }> = ({ status }) => {
  const colors: Record<MaintenanceStatus, string> = {
    open: 'bg-red-100 text-red-800',
    in_progress: 'bg-blue-100 text-blue-800',
    waiting_parts: 'bg-yellow-100 text-yellow-800',
    scheduled: 'bg-purple-100 text-purple-800',
    completed: 'bg-green-100 text-green-800',
    cancelled: 'bg-gray-100 text-gray-800',
  };
  
  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${colors[status]}`}>
      {status.replace('_', ' ').toUpperCase()}
    </span>
  );
};

const RBQBadge: React.FC<{ verified: boolean; validUntil?: string }> = ({ verified, validUntil }) => {
  if (!verified) {
    return (
      <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800">
        ❌ RBQ Non vérifié
      </span>
    );
  }
  
  const isExpiringSoon = validUntil && new Date(validUntil) < new Date(Date.now() + 90 * 24 * 60 * 60 * 1000);
  
  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
      isExpiringSoon ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
    }`}>
      ✅ RBQ Vérifié {isExpiringSoon && '(expire bientôt)'}
    </span>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN PAGE
// ═══════════════════════════════════════════════════════════════════════════════

const RealEstatePage: React.FC = () => {
  const {
    properties,
    tenants,
    leases,
    maintenance,
    contractors,
    payments,
    stats,
    selectedProperty,
    propertyAnalysis,
    rentIncrease,
    activeTab,
    isLoading,
    error,
    fetchProperties,
    fetchTenants,
    fetchLeases,
    fetchMaintenance,
    fetchContractors,
    fetchPayments,
    fetchStats,
    createProperty,
    createTenant,
    createLease,
    createMaintenance,
    updateMaintenanceStatus,
    analyzeProperty,
    calculateRentIncrease,
    selectProperty,
    setActiveTab,
    clearError,
  } = useRealEstateStore();
  
  // Forms state
  const [showPropertyForm, setShowPropertyForm] = useState(false);
  const [showTenantForm, setShowTenantForm] = useState(false);
  const [showLeaseForm, setShowLeaseForm] = useState(false);
  const [showMaintenanceForm, setShowMaintenanceForm] = useState(false);
  
  // Load data on mount
  useEffect(() => {
    fetchProperties();
    fetchTenants();
    fetchLeases();
    fetchMaintenance();
    fetchContractors();
    fetchPayments();
    fetchStats();
  }, []);
  
  // Property form
  const [propertyForm, setPropertyForm] = useState({
    name: '',
    address: '',
    city: '',
    province: 'QC',
    postal_code: '',
    property_type: 'residential' as PropertyType,
    units: 1,
    bedrooms: 0,
    bathrooms: 0,
    square_feet: 0,
    year_built: 2000,
    current_value: 0,
    monthly_rent: 0,
    monthly_expenses: 0,
    municipal_tax: 0,
    school_tax: 0,
  });
  
  // Tenant form
  const [tenantForm, setTenantForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
  });
  
  // Maintenance form
  const [maintenanceForm, setMaintenanceForm] = useState({
    property_id: '',
    title: '',
    description: '',
    category: 'other',
    priority: 'medium' as MaintenancePriority,
  });
  
  const handleCreateProperty = async (e: React.FormEvent) => {
    e.preventDefault();
    await createProperty(propertyForm);
    setShowPropertyForm(false);
    setPropertyForm({
      name: '',
      address: '',
      city: '',
      province: 'QC',
      postal_code: '',
      property_type: 'residential',
      units: 1,
      bedrooms: 0,
      bathrooms: 0,
      square_feet: 0,
      year_built: 2000,
      current_value: 0,
      monthly_rent: 0,
      monthly_expenses: 0,
      municipal_tax: 0,
      school_tax: 0,
    });
  };
  
  const handleCreateTenant = async (e: React.FormEvent) => {
    e.preventDefault();
    await createTenant(tenantForm);
    setShowTenantForm(false);
    setTenantForm({ first_name: '', last_name: '', email: '', phone: '' });
  };
  
  const handleCreateMaintenance = async (e: React.FormEvent) => {
    e.preventDefault();
    await createMaintenance(maintenanceForm);
    setShowMaintenanceForm(false);
    setMaintenanceForm({
      property_id: '',
      title: '',
      description: '',
      category: 'other',
      priority: 'medium',
    });
  };
  
  // ═══════════════════════════════════════════════════════════════════════════
  // RENDER
  // ═══════════════════════════════════════════════════════════════════════════
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                🏠 Immobilier CHE·NU
              </h1>
              <p className="text-sm text-gray-500">
                Gestion immobilière avec conformité RBQ Québec
              </p>
            </div>
            {stats && (
              <div className="flex gap-4 text-sm">
                <div className="text-center">
                  <div className="font-bold text-lg">{stats.properties.total}</div>
                  <div className="text-gray-500">Propriétés</div>
                </div>
                <div className="text-center">
                  <div className="font-bold text-lg">{stats.tenants.active}</div>
                  <div className="text-gray-500">Locataires</div>
                </div>
                <div className="text-center">
                  <div className="font-bold text-lg text-green-600">
                    ${stats.financials.monthly_cash_flow.toLocaleString()}
                  </div>
                  <div className="text-gray-500">Cash Flow/mois</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>
      
      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 m-4">
          <div className="flex justify-between">
            <p className="text-red-700">{error}</p>
            <button onClick={clearError} className="text-red-700 hover:text-red-900">
              ✕
            </button>
          </div>
        </div>
      )}
      
      {/* Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex gap-4">
            {[
              { id: 'properties', label: '🏠 Propriétés', count: properties.length },
              { id: 'tenants', label: '👤 Locataires', count: tenants.length },
              { id: 'leases', label: '📝 Baux', count: leases.length },
              { id: 'maintenance', label: '🔧 Entretien', count: maintenance.filter(m => m.status === 'open').length },
              { id: 'payments', label: '💰 Paiements', count: payments.length },
              { id: 'stats', label: '📊 Stats' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.label}
                {tab.count !== undefined && (
                  <span className="ml-2 bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full text-xs">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>
      
      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {isLoading && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-500">Chargement...</p>
          </div>
        )}
        
        {/* ═══════════════════════════════════════════════════════════════════
            PROPERTIES TAB
        ═══════════════════════════════════════════════════════════════════ */}
        {activeTab === 'properties' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Properties List */}
            <div className="lg:col-span-2 space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold">Mes Propriétés</h2>
                <button
                  onClick={() => setShowPropertyForm(true)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  + Ajouter
                </button>
              </div>
              
              {/* Property Form Modal */}
              {showPropertyForm && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                  <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                    <h3 className="text-lg font-semibold mb-4">Nouvelle Propriété</h3>
                    <form onSubmit={handleCreateProperty} className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <input
                          type="text"
                          placeholder="Nom"
                          value={propertyForm.name}
                          onChange={(e) => setPropertyForm({ ...propertyForm, name: e.target.value })}
                          className="px-3 py-2 border rounded-lg"
                          required
                        />
                        <select
                          value={propertyForm.property_type}
                          onChange={(e) => setPropertyForm({ ...propertyForm, property_type: e.target.value as PropertyType })}
                          className="px-3 py-2 border rounded-lg"
                        >
                          <option value="residential">Résidentiel</option>
                          <option value="condo">Condo</option>
                          <option value="duplex">Duplex</option>
                          <option value="triplex">Triplex</option>
                          <option value="multi_family">Multi-logements</option>
                          <option value="commercial">Commercial</option>
                        </select>
                        <input
                          type="text"
                          placeholder="Adresse"
                          value={propertyForm.address}
                          onChange={(e) => setPropertyForm({ ...propertyForm, address: e.target.value })}
                          className="px-3 py-2 border rounded-lg col-span-2"
                          required
                        />
                        <input
                          type="text"
                          placeholder="Ville"
                          value={propertyForm.city}
                          onChange={(e) => setPropertyForm({ ...propertyForm, city: e.target.value })}
                          className="px-3 py-2 border rounded-lg"
                          required
                        />
                        <input
                          type="text"
                          placeholder="Code postal"
                          value={propertyForm.postal_code}
                          onChange={(e) => setPropertyForm({ ...propertyForm, postal_code: e.target.value })}
                          className="px-3 py-2 border rounded-lg"
                        />
                        <input
                          type="number"
                          placeholder="Unités"
                          value={propertyForm.units}
                          onChange={(e) => setPropertyForm({ ...propertyForm, units: parseInt(e.target.value) })}
                          className="px-3 py-2 border rounded-lg"
                        />
                        <input
                          type="number"
                          placeholder="Chambres"
                          value={propertyForm.bedrooms}
                          onChange={(e) => setPropertyForm({ ...propertyForm, bedrooms: parseInt(e.target.value) })}
                          className="px-3 py-2 border rounded-lg"
                        />
                        <input
                          type="number"
                          placeholder="Valeur actuelle ($)"
                          value={propertyForm.current_value}
                          onChange={(e) => setPropertyForm({ ...propertyForm, current_value: parseInt(e.target.value) })}
                          className="px-3 py-2 border rounded-lg"
                        />
                        <input
                          type="number"
                          placeholder="Loyer mensuel ($)"
                          value={propertyForm.monthly_rent}
                          onChange={(e) => setPropertyForm({ ...propertyForm, monthly_rent: parseInt(e.target.value) })}
                          className="px-3 py-2 border rounded-lg"
                        />
                      </div>
                      <div className="flex gap-2 justify-end">
                        <button
                          type="button"
                          onClick={() => setShowPropertyForm(false)}
                          className="px-4 py-2 border rounded-lg"
                        >
                          Annuler
                        </button>
                        <button
                          type="submit"
                          className="px-4 py-2 bg-blue-600 text-white rounded-lg"
                        >
                          Créer
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              )}
              
              {/* Properties Grid */}
              <div className="grid gap-4">
                {properties.map((property) => (
                  <div
                    key={property.id}
                    onClick={() => selectProperty(property)}
                    className={`bg-white p-4 rounded-lg shadow cursor-pointer hover:shadow-md transition-shadow ${
                      selectedProperty?.id === property.id ? 'ring-2 ring-blue-500' : ''
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold text-lg">{property.name}</h3>
                        <p className="text-gray-500 text-sm">{property.address}, {property.city}</p>
                      </div>
                      <StatusBadge status={property.status} />
                    </div>
                    <div className="mt-3 flex gap-4 text-sm text-gray-600">
                      <span>🏠 {property.property_type}</span>
                      {property.bedrooms && <span>🛏️ {property.bedrooms} ch</span>}
                      {property.square_feet && <span>📐 {property.square_feet} pi²</span>}
                      {property.monthly_rent && (
                        <span className="text-green-600 font-medium">
                          💰 ${property.monthly_rent}/mois
                        </span>
                      )}
                    </div>
                  </div>
                ))}
                
                {properties.length === 0 && !isLoading && (
                  <div className="text-center py-8 text-gray-500">
                    Aucune propriété. Ajoutez votre première propriété!
                  </div>
                )}
              </div>
            </div>
            
            {/* Property Detail */}
            <div className="bg-white rounded-lg shadow p-4">
              {selectedProperty ? (
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">{selectedProperty.name}</h3>
                  <StatusBadge status={selectedProperty.status} />
                  
                  <div className="space-y-2 text-sm">
                    <p><strong>Adresse:</strong> {selectedProperty.address}</p>
                    <p><strong>Ville:</strong> {selectedProperty.city}, {selectedProperty.province}</p>
                    <p><strong>Type:</strong> {selectedProperty.property_type}</p>
                    <p><strong>Unités:</strong> {selectedProperty.units}</p>
                    {selectedProperty.bedrooms && <p><strong>Chambres:</strong> {selectedProperty.bedrooms}</p>}
                    {selectedProperty.square_feet && <p><strong>Superficie:</strong> {selectedProperty.square_feet} pi²</p>}
                    {selectedProperty.year_built && <p><strong>Année:</strong> {selectedProperty.year_built}</p>}
                  </div>
                  
                  <div className="border-t pt-4">
                    <h4 className="font-medium mb-2">Financiers</h4>
                    {selectedProperty.current_value && (
                      <p><strong>Valeur:</strong> ${selectedProperty.current_value.toLocaleString()}</p>
                    )}
                    {selectedProperty.monthly_rent && (
                      <p><strong>Loyer:</strong> ${selectedProperty.monthly_rent}/mois</p>
                    )}
                    {selectedProperty.municipal_tax && (
                      <p><strong>Taxes municipales:</strong> ${selectedProperty.municipal_tax}/an</p>
                    )}
                  </div>
                  
                  <button
                    onClick={() => analyzeProperty(selectedProperty.id)}
                    className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    📊 Analyser la rentabilité
                  </button>
                  
                  {/* Analysis Results */}
                  {propertyAnalysis && propertyAnalysis.property_id === selectedProperty.id && (
                    <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                      <h4 className="font-medium">Analyse Financière</h4>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-gray-500">Cap Rate:</span>
                          <span className="ml-2 font-medium">{propertyAnalysis.cap_rate}%</span>
                        </div>
                        <div>
                          <span className="text-gray-500">ROI:</span>
                          <span className="ml-2 font-medium">{propertyAnalysis.annual_roi}%</span>
                        </div>
                        <div>
                          <span className="text-gray-500">Cash Flow:</span>
                          <span className={`ml-2 font-medium ${propertyAnalysis.monthly_cash_flow >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            ${propertyAnalysis.monthly_cash_flow}/mois
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-500">GRM:</span>
                          <span className="ml-2 font-medium">{propertyAnalysis.gross_rent_multiplier}</span>
                        </div>
                      </div>
                      {propertyAnalysis.insights.length > 0 && (
                        <div>
                          <p className="text-sm font-medium text-green-700">✅ Points positifs:</p>
                          <ul className="text-xs text-gray-600 list-disc ml-4">
                            {propertyAnalysis.insights.map((i, idx) => <li key={idx}>{i}</li>)}
                          </ul>
                        </div>
                      )}
                      {propertyAnalysis.risks.length > 0 && (
                        <div>
                          <p className="text-sm font-medium text-red-700">⚠️ Risques:</p>
                          <ul className="text-xs text-gray-600 list-disc ml-4">
                            {propertyAnalysis.risks.map((r, idx) => <li key={idx}>{r}</li>)}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  Sélectionnez une propriété pour voir les détails
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* ═══════════════════════════════════════════════════════════════════
            TENANTS TAB
        ═══════════════════════════════════════════════════════════════════ */}
        {activeTab === 'tenants' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Locataires</h2>
              <button
                onClick={() => setShowTenantForm(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                + Ajouter
              </button>
            </div>
            
            {/* Tenant Form Modal */}
            {showTenantForm && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-lg p-6 w-full max-w-md">
                  <h3 className="text-lg font-semibold mb-4">Nouveau Locataire</h3>
                  <form onSubmit={handleCreateTenant} className="space-y-4">
                    <input
                      type="text"
                      placeholder="Prénom"
                      value={tenantForm.first_name}
                      onChange={(e) => setTenantForm({ ...tenantForm, first_name: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    />
                    <input
                      type="text"
                      placeholder="Nom"
                      value={tenantForm.last_name}
                      onChange={(e) => setTenantForm({ ...tenantForm, last_name: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    />
                    <input
                      type="email"
                      placeholder="Courriel"
                      value={tenantForm.email}
                      onChange={(e) => setTenantForm({ ...tenantForm, email: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    />
                    <input
                      type="tel"
                      placeholder="Téléphone"
                      value={tenantForm.phone}
                      onChange={(e) => setTenantForm({ ...tenantForm, phone: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                    />
                    <div className="flex gap-2 justify-end">
                      <button
                        type="button"
                        onClick={() => setShowTenantForm(false)}
                        className="px-4 py-2 border rounded-lg"
                      >
                        Annuler
                      </button>
                      <button
                        type="submit"
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg"
                      >
                        Créer
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
            
            {/* Tenants List */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Locataire</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Contact</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Propriété</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Loyer</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Balance</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Statut</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {tenants.map((tenant) => (
                    <tr key={tenant.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <div className="font-medium">{tenant.first_name} {tenant.last_name}</div>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        <div>{tenant.email}</div>
                        {tenant.phone && <div>{tenant.phone}</div>}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {tenant.property_id ? (
                          <span>Unité {tenant.unit_number || '-'}</span>
                        ) : (
                          <span className="text-gray-400">Non assigné</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {tenant.monthly_rent ? `$${tenant.monthly_rent}/mois` : '-'}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span className={tenant.balance > 0 ? 'text-red-600' : 'text-green-600'}>
                          ${tenant.balance}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          tenant.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {tenant.is_active ? 'Actif' : 'Inactif'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {tenants.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Aucun locataire
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* ═══════════════════════════════════════════════════════════════════
            MAINTENANCE TAB
        ═══════════════════════════════════════════════════════════════════ */}
        {activeTab === 'maintenance' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Demandes d'entretien</h2>
              <button
                onClick={() => setShowMaintenanceForm(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                + Nouvelle demande
              </button>
            </div>
            
            {/* Maintenance Form Modal */}
            {showMaintenanceForm && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-lg p-6 w-full max-w-md">
                  <h3 className="text-lg font-semibold mb-4">Nouvelle Demande</h3>
                  <form onSubmit={handleCreateMaintenance} className="space-y-4">
                    <select
                      value={maintenanceForm.property_id}
                      onChange={(e) => setMaintenanceForm({ ...maintenanceForm, property_id: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    >
                      <option value="">Sélectionner propriété...</option>
                      {properties.map((p) => (
                        <option key={p.id} value={p.id}>{p.name}</option>
                      ))}
                    </select>
                    <input
                      type="text"
                      placeholder="Titre"
                      value={maintenanceForm.title}
                      onChange={(e) => setMaintenanceForm({ ...maintenanceForm, title: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                      required
                    />
                    <textarea
                      placeholder="Description"
                      value={maintenanceForm.description}
                      onChange={(e) => setMaintenanceForm({ ...maintenanceForm, description: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                      rows={3}
                      required
                    />
                    <select
                      value={maintenanceForm.category}
                      onChange={(e) => setMaintenanceForm({ ...maintenanceForm, category: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg"
                    >
                      <option value="plumbing">Plomberie</option>
                      <option value="electrical">Électricité</option>
                      <option value="hvac">Chauffage/Climatisation</option>
                      <option value="appliance">Électroménagers</option>
                      <option value="structural">Structure</option>
                      <option value="other">Autre</option>
                    </select>
                    <select
                      value={maintenanceForm.priority}
                      onChange={(e) => setMaintenanceForm({ ...maintenanceForm, priority: e.target.value as MaintenancePriority })}
                      className="w-full px-3 py-2 border rounded-lg"
                    >
                      <option value="low">Basse</option>
                      <option value="medium">Moyenne</option>
                      <option value="high">Haute</option>
                      <option value="emergency">Urgence</option>
                    </select>
                    <div className="flex gap-2 justify-end">
                      <button
                        type="button"
                        onClick={() => setShowMaintenanceForm(false)}
                        className="px-4 py-2 border rounded-lg"
                      >
                        Annuler
                      </button>
                      <button
                        type="submit"
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg"
                      >
                        Créer
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
            
            {/* Maintenance List */}
            <div className="grid gap-4">
              {maintenance.map((request) => (
                <div key={request.id} className="bg-white p-4 rounded-lg shadow">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">{request.title}</h3>
                      <p className="text-sm text-gray-500">{request.description}</p>
                    </div>
                    <div className="flex gap-2">
                      <PriorityBadge priority={request.priority} />
                      <MaintenanceStatusBadge status={request.status} />
                    </div>
                  </div>
                  <div className="mt-3 flex gap-4 text-sm text-gray-600">
                    <span>📍 {request.category}</span>
                    <span>📅 {new Date(request.reported_date).toLocaleDateString('fr-CA')}</span>
                    {request.estimated_cost && <span>💰 ~${request.estimated_cost}</span>}
                  </div>
                  {request.status === 'open' && (
                    <div className="mt-3 flex gap-2">
                      <button
                        onClick={() => updateMaintenanceStatus(request.id, 'in_progress')}
                        className="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded"
                      >
                        Commencer
                      </button>
                      <button
                        onClick={() => updateMaintenanceStatus(request.id, 'completed')}
                        className="px-3 py-1 text-sm bg-green-100 text-green-800 rounded"
                      >
                        Compléter
                      </button>
                    </div>
                  )}
                </div>
              ))}
              
              {maintenance.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Aucune demande d'entretien
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* ═══════════════════════════════════════════════════════════════════
            STATS TAB
        ═══════════════════════════════════════════════════════════════════ */}
        {activeTab === 'stats' && stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Portfolio Value */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Valeur du Portfolio</h3>
              <p className="text-3xl font-bold text-gray-900">
                ${stats.financials.total_portfolio_value.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {stats.properties.total} propriétés, {stats.properties.total_units} unités
              </p>
            </div>
            
            {/* Monthly Income */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Revenus Mensuels</h3>
              <p className="text-3xl font-bold text-green-600">
                ${stats.financials.monthly_income.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                ${stats.financials.annual_income.toLocaleString()}/an
              </p>
            </div>
            
            {/* Cash Flow */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Cash Flow Mensuel</h3>
              <p className={`text-3xl font-bold ${stats.financials.monthly_cash_flow >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ${stats.financials.monthly_cash_flow.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Dépenses: ${stats.financials.monthly_expenses.toLocaleString()}/mois
              </p>
            </div>
            
            {/* Occupancy */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Taux d'Occupation</h3>
              <p className="text-3xl font-bold text-blue-600">
                {(100 - stats.properties.vacancy_rate).toFixed(1)}%
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {stats.properties.occupied}/{stats.properties.total} occupées
              </p>
            </div>
            
            {/* Tenants */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Locataires</h3>
              <p className="text-3xl font-bold text-gray-900">
                {stats.tenants.active}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {stats.tenants.total} total
              </p>
            </div>
            
            {/* Maintenance */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Entretien</h3>
              <p className="text-3xl font-bold text-orange-600">
                {stats.maintenance.open_requests}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                demandes ouvertes
                {stats.maintenance.emergency > 0 && (
                  <span className="text-red-600"> ({stats.maintenance.emergency} urgences)</span>
                )}
              </p>
            </div>
            
            {/* Leases */}
            <div className="bg-white rounded-lg shadow p-6 col-span-full">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Baux</h3>
              <div className="flex gap-8">
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.leases.active}</p>
                  <p className="text-sm text-gray-500">Actifs</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-yellow-600">{stats.leases.expiring_soon}</p>
                  <p className="text-sm text-gray-500">Expirent bientôt (60 jours)</p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Leases Tab */}
        {activeTab === 'leases' && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Baux</h2>
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Propriété</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Locataire</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Période</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Loyer</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Statut</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {leases.map((lease) => (
                    <tr key={lease.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm">
                        {properties.find(p => p.id === lease.property_id)?.name || lease.property_id}
                        {lease.unit_number && ` - Unité ${lease.unit_number}`}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {(() => {
                          const tenant = tenants.find(t => t.id === lease.tenant_id);
                          return tenant ? `${tenant.first_name} ${tenant.last_name}` : lease.tenant_id;
                        })()}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {lease.start_date} → {lease.end_date}
                      </td>
                      <td className="px-4 py-3 text-sm font-medium">
                        ${lease.monthly_rent}/mois
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          lease.status === 'active' ? 'bg-green-100 text-green-800' :
                          lease.status === 'expired' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {lease.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {leases.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Aucun bail
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Payments Tab */}
        {activeTab === 'payments' && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Historique des paiements</h2>
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Date</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Locataire</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Montant</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Méthode</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Période</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Statut</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {payments.map((payment) => (
                    <tr key={payment.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm">{payment.payment_date}</td>
                      <td className="px-4 py-3 text-sm">
                        {(() => {
                          const tenant = tenants.find(t => t.id === payment.tenant_id);
                          return tenant ? `${tenant.first_name} ${tenant.last_name}` : payment.tenant_id;
                        })()}
                      </td>
                      <td className="px-4 py-3 text-sm font-medium">${payment.amount}</td>
                      <td className="px-4 py-3 text-sm">{payment.payment_method}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {payment.period_start} - {payment.period_end}
                      </td>
                      <td className="px-4 py-3">
                        {payment.is_late ? (
                          <span className="px-2 py-1 text-xs rounded-full bg-red-100 text-red-800">
                            En retard (+${payment.late_fee})
                          </span>
                        ) : (
                          <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                            À temps
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {payments.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Aucun paiement enregistré
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default RealEstatePage;
