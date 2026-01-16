/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ BUSINESS CRM — PAGE                               ║
 * ║                                                                              ║
 * ║  Complete CRM interface with contacts, deals, pipeline, and activities.     ║
 * ║  COS: 93/100 — Salesforce Competitor ($29/mo vs $300/mo)                     ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import React, { useEffect, useState } from 'react';
import { useCRMStore, Contact, Deal, Activity } from '../../../stores/crmStore';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════════════════════════════════════════

const LeadScoreBadge: React.FC<{ score: number }> = ({ score }) => {
  const getColor = () => {
    if (score >= 70) return 'bg-green-100 text-green-800';
    if (score >= 40) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };
  
  const getLabel = () => {
    if (score >= 70) return 'Hot';
    if (score >= 40) return 'Warm';
    return 'Cold';
  };
  
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getColor()}`}>
      {score} • {getLabel()}
    </span>
  );
};

const StageBadge: React.FC<{ stage: string }> = ({ stage }) => {
  const colors: Record<string, string> = {
    discovery: 'bg-gray-100 text-gray-800',
    qualification: 'bg-blue-100 text-blue-800',
    proposal: 'bg-purple-100 text-purple-800',
    negotiation: 'bg-orange-100 text-orange-800',
    closed_won: 'bg-green-100 text-green-800',
    closed_lost: 'bg-red-100 text-red-800',
  };
  
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[stage] || 'bg-gray-100'}`}>
      {stage.replace('_', ' ').toUpperCase()}
    </span>
  );
};

const ActivityIcon: React.FC<{ type: string }> = ({ type }) => {
  const icons: Record<string, string> = {
    email: '📧',
    call: '📞',
    meeting: '📅',
    note: '📝',
    task: '✓',
  };
  return <span>{icons[type] || '📌'}</span>;
};

// ═══════════════════════════════════════════════════════════════════════════════
// CONTACTS TAB
// ═══════════════════════════════════════════════════════════════════════════════

const ContactsTab: React.FC = () => {
  const {
    contacts,
    selectedContact,
    fetchContacts,
    createContact,
    selectContact,
    scoreContact,
    generateEmail,
    logActivity,
    isLoading,
  } = useCRMStore();
  
  const [showForm, setShowForm] = useState(false);
  const [newContact, setNewContact] = useState({
    first_name: '',
    last_name: '',
    email: '',
    title: '',
    company_name: '',
    lead_source: 'website',
  });
  const [emailDraft, setEmailDraft] = useState<{ subject: string; body: string } | null>(null);
  
  useEffect(() => {
    fetchContacts();
  }, []);
  
  const handleCreate = async () => {
    if (!newContact.first_name || !newContact.last_name || !newContact.email) return;
    
    await createContact(newContact);
    setNewContact({ first_name: '', last_name: '', email: '', title: '', company_name: '', lead_source: 'website' });
    setShowForm(false);
  };
  
  const handleGenerateEmail = async (contactId: string) => {
    const draft = await generateEmail(contactId, 'follow_up');
    setEmailDraft(draft);
  };
  
  const handleLogCall = async (contact: Contact) => {
    await logActivity({
      activity_type: 'call',
      subject: `Call with ${contact.first_name} ${contact.last_name}`,
      contact_id: contact.id,
      outcome: 'Completed',
    });
    alert('Call logged!');
  };
  
  return (
    <div className="flex h-full">
      {/* Contact List */}
      <div className="w-1/2 border-r overflow-y-auto">
        <div className="p-4 border-b bg-gray-50">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Contacts</h2>
            <button
              onClick={() => setShowForm(!showForm)}
              className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              + Add Contact
            </button>
          </div>
          
          {showForm && (
            <div className="bg-white p-4 rounded border mb-4">
              <div className="grid grid-cols-2 gap-2 mb-2">
                <input
                  type="text"
                  placeholder="First name"
                  value={newContact.first_name}
                  onChange={(e) => setNewContact({ ...newContact, first_name: e.target.value })}
                  className="p-2 border rounded text-sm"
                />
                <input
                  type="text"
                  placeholder="Last name"
                  value={newContact.last_name}
                  onChange={(e) => setNewContact({ ...newContact, last_name: e.target.value })}
                  className="p-2 border rounded text-sm"
                />
              </div>
              <input
                type="email"
                placeholder="Email"
                value={newContact.email}
                onChange={(e) => setNewContact({ ...newContact, email: e.target.value })}
                className="w-full p-2 border rounded text-sm mb-2"
              />
              <div className="grid grid-cols-2 gap-2 mb-2">
                <input
                  type="text"
                  placeholder="Title"
                  value={newContact.title}
                  onChange={(e) => setNewContact({ ...newContact, title: e.target.value })}
                  className="p-2 border rounded text-sm"
                />
                <input
                  type="text"
                  placeholder="Company"
                  value={newContact.company_name}
                  onChange={(e) => setNewContact({ ...newContact, company_name: e.target.value })}
                  className="p-2 border rounded text-sm"
                />
              </div>
              <button
                onClick={handleCreate}
                disabled={isLoading}
                className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                {isLoading ? 'Creating...' : 'Create Contact'}
              </button>
            </div>
          )}
        </div>
        
        <div className="divide-y">
          {contacts.map((contact) => (
            <div
              key={contact.id}
              onClick={() => selectContact(contact)}
              className={`p-4 cursor-pointer hover:bg-gray-50 ${
                selectedContact?.id === contact.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
              }`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium">
                    {contact.first_name} {contact.last_name}
                  </h3>
                  <p className="text-sm text-gray-600">{contact.title || 'No title'}</p>
                  <p className="text-sm text-gray-500">{contact.company_name || 'No company'}</p>
                </div>
                <LeadScoreBadge score={contact.lead_score} />
              </div>
              <div className="mt-2 flex gap-2">
                {contact.tags.slice(0, 3).map((tag) => (
                  <span key={tag} className="px-2 py-0.5 bg-gray-100 rounded text-xs">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
          
          {contacts.length === 0 && !isLoading && (
            <div className="p-8 text-center text-gray-500">
              No contacts yet. Add your first contact!
            </div>
          )}
        </div>
      </div>
      
      {/* Contact Detail */}
      <div className="w-1/2 p-4 overflow-y-auto">
        {selectedContact ? (
          <div>
            <div className="mb-6">
              <h2 className="text-xl font-bold">
                {selectedContact.first_name} {selectedContact.last_name}
              </h2>
              <p className="text-gray-600">{selectedContact.title}</p>
              <p className="text-gray-500">{selectedContact.company_name}</p>
              <p className="text-sm text-blue-600">{selectedContact.email}</p>
            </div>
            
            {/* Lead Score */}
            <div className="bg-gray-50 p-4 rounded mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">Lead Score</span>
                <LeadScoreBadge score={selectedContact.lead_score} />
              </div>
              <div className="grid grid-cols-4 gap-2 text-center text-sm">
                {Object.entries(selectedContact.lead_score_breakdown || {}).map(([key, value]) => (
                  <div key={key} className="bg-white p-2 rounded">
                    <div className="font-bold text-blue-600">{value}</div>
                    <div className="text-gray-500 text-xs capitalize">{key}</div>
                  </div>
                ))}
              </div>
              <button
                onClick={() => scoreContact(selectedContact.id)}
                className="mt-2 w-full py-1 border rounded text-sm hover:bg-gray-100"
              >
                🔄 Re-score with AI
              </button>
            </div>
            
            {/* Actions */}
            <div className="grid grid-cols-3 gap-2 mb-4">
              <button
                onClick={() => handleLogCall(selectedContact)}
                className="py-2 bg-green-100 text-green-800 rounded hover:bg-green-200"
              >
                📞 Log Call
              </button>
              <button
                onClick={() => handleGenerateEmail(selectedContact.id)}
                className="py-2 bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
              >
                ✉️ Draft Email
              </button>
              <button className="py-2 bg-purple-100 text-purple-800 rounded hover:bg-purple-200">
                📅 Schedule
              </button>
            </div>
            
            {/* Email Draft Modal */}
            {emailDraft && (
              <div className="bg-blue-50 p-4 rounded mb-4">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-medium">📧 AI Email Draft</h3>
                  <button onClick={() => setEmailDraft(null)} className="text-gray-500">✕</button>
                </div>
                <div className="bg-white p-3 rounded border">
                  <p className="font-medium text-sm">Subject: {emailDraft.subject}</p>
                  <hr className="my-2" />
                  <p className="text-sm whitespace-pre-wrap">{emailDraft.body}</p>
                </div>
                <button className="mt-2 w-full py-2 bg-blue-600 text-white rounded">
                  Open in Email Client
                </button>
              </div>
            )}
            
            {/* Info */}
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Status</span>
                <span className="capitalize">{selectedContact.lead_status}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Source</span>
                <span className="capitalize">{selectedContact.lead_source}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Last Contacted</span>
                <span>{selectedContact.last_contacted ? new Date(selectedContact.last_contacted).toLocaleDateString() : 'Never'}</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            Select a contact to view details
          </div>
        )}
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// DEALS TAB
// ═══════════════════════════════════════════════════════════════════════════════

const DealsTab: React.FC = () => {
  const {
    deals,
    contacts,
    pipelineSummary,
    fetchDeals,
    fetchContacts,
    createDeal,
    updateDealStage,
    fetchPipelineSummary,
    isLoading,
  } = useCRMStore();
  
  const [showForm, setShowForm] = useState(false);
  const [newDeal, setNewDeal] = useState({
    name: '',
    contact_id: '',
    amount: '',
    stage: 'discovery',
  });
  
  useEffect(() => {
    fetchDeals();
    fetchContacts();
    fetchPipelineSummary();
  }, []);
  
  const handleCreate = async () => {
    if (!newDeal.name || !newDeal.contact_id || !newDeal.amount) return;
    
    await createDeal({
      name: newDeal.name,
      contact_id: newDeal.contact_id,
      amount: parseFloat(newDeal.amount),
      stage: newDeal.stage,
    });
    setNewDeal({ name: '', contact_id: '', amount: '', stage: 'discovery' });
    setShowForm(false);
    fetchPipelineSummary();
  };
  
  const stages = ['discovery', 'qualification', 'proposal', 'negotiation'];
  
  return (
    <div className="h-full flex flex-col">
      {/* Pipeline Summary */}
      {pipelineSummary && (
        <div className="p-4 bg-gray-50 border-b">
          <div className="grid grid-cols-4 gap-4 text-center">
            <div className="bg-white p-3 rounded shadow-sm">
              <div className="text-2xl font-bold text-blue-600">
                ${pipelineSummary.total_pipeline_value.toLocaleString()}
              </div>
              <div className="text-sm text-gray-500">Pipeline Value</div>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <div className="text-2xl font-bold text-green-600">
                ${pipelineSummary.weighted_pipeline_value.toLocaleString()}
              </div>
              <div className="text-sm text-gray-500">Weighted Value</div>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <div className="text-2xl font-bold">{pipelineSummary.open_deals}</div>
              <div className="text-sm text-gray-500">Open Deals</div>
            </div>
            <div className="bg-white p-3 rounded shadow-sm">
              <div className="text-2xl font-bold text-green-600">{pipelineSummary.win_rate}%</div>
              <div className="text-sm text-gray-500">Win Rate</div>
            </div>
          </div>
        </div>
      )}
      
      {/* Header */}
      <div className="p-4 border-b flex justify-between items-center">
        <h2 className="text-lg font-semibold">Pipeline</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
        >
          + Add Deal
        </button>
      </div>
      
      {/* New Deal Form */}
      {showForm && (
        <div className="p-4 bg-gray-50 border-b">
          <div className="grid grid-cols-4 gap-2">
            <input
              type="text"
              placeholder="Deal name"
              value={newDeal.name}
              onChange={(e) => setNewDeal({ ...newDeal, name: e.target.value })}
              className="p-2 border rounded text-sm"
            />
            <select
              value={newDeal.contact_id}
              onChange={(e) => setNewDeal({ ...newDeal, contact_id: e.target.value })}
              className="p-2 border rounded text-sm"
            >
              <option value="">Select contact</option>
              {contacts.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.first_name} {c.last_name}
                </option>
              ))}
            </select>
            <input
              type="number"
              placeholder="Amount"
              value={newDeal.amount}
              onChange={(e) => setNewDeal({ ...newDeal, amount: e.target.value })}
              className="p-2 border rounded text-sm"
            />
            <button
              onClick={handleCreate}
              disabled={isLoading}
              className="py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Create
            </button>
          </div>
        </div>
      )}
      
      {/* Kanban Board */}
      <div className="flex-1 overflow-x-auto p-4">
        <div className="flex gap-4 h-full">
          {stages.map((stage) => {
            const stageDeals = deals.filter((d) => d.stage === stage);
            const stageValue = stageDeals.reduce((sum, d) => sum + d.amount, 0);
            
            return (
              <div key={stage} className="w-72 flex-shrink-0 bg-gray-100 rounded">
                <div className="p-3 border-b bg-gray-200 rounded-t">
                  <h3 className="font-medium capitalize">{stage.replace('_', ' ')}</h3>
                  <p className="text-sm text-gray-600">
                    {stageDeals.length} deals • ${stageValue.toLocaleString()}
                  </p>
                </div>
                <div className="p-2 space-y-2 max-h-96 overflow-y-auto">
                  {stageDeals.map((deal) => (
                    <div
                      key={deal.id}
                      className="bg-white p-3 rounded shadow-sm border"
                    >
                      <h4 className="font-medium text-sm">{deal.name}</h4>
                      <p className="text-lg font-bold text-green-600">
                        ${deal.amount.toLocaleString()}
                      </p>
                      <div className="text-xs text-gray-500 mt-1">
                        {deal.probability}% probability
                      </div>
                      <div className="mt-2 flex gap-1">
                        {stage !== 'negotiation' && (
                          <button
                            onClick={() => {
                              const nextStage = stages[stages.indexOf(stage) + 1];
                              if (nextStage) updateDealStage(deal.id, nextStage);
                            }}
                            className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs"
                          >
                            Move →
                          </button>
                        )}
                        <button
                          onClick={() => updateDealStage(deal.id, 'closed_won')}
                          className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs"
                        >
                          Won
                        </button>
                        <button
                          onClick={() => updateDealStage(deal.id, 'closed_lost')}
                          className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs"
                        >
                          Lost
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// ACTIVITIES TAB
// ═══════════════════════════════════════════════════════════════════════════════

const ActivitiesTab: React.FC = () => {
  const { activities, fetchActivities, logActivity, isLoading } = useCRMStore();
  const [newActivity, setNewActivity] = useState({
    activity_type: 'note',
    subject: '',
    description: '',
  });
  
  useEffect(() => {
    fetchActivities();
  }, []);
  
  const handleLog = async () => {
    if (!newActivity.subject) return;
    await logActivity(newActivity);
    setNewActivity({ activity_type: 'note', subject: '', description: '' });
  };
  
  return (
    <div className="h-full flex flex-col">
      {/* Log Activity Form */}
      <div className="p-4 bg-gray-50 border-b">
        <div className="flex gap-2">
          <select
            value={newActivity.activity_type}
            onChange={(e) => setNewActivity({ ...newActivity, activity_type: e.target.value })}
            className="p-2 border rounded text-sm"
          >
            <option value="note">📝 Note</option>
            <option value="call">📞 Call</option>
            <option value="email">📧 Email</option>
            <option value="meeting">📅 Meeting</option>
            <option value="task">✓ Task</option>
          </select>
          <input
            type="text"
            placeholder="Subject"
            value={newActivity.subject}
            onChange={(e) => setNewActivity({ ...newActivity, subject: e.target.value })}
            className="flex-1 p-2 border rounded text-sm"
          />
          <button
            onClick={handleLog}
            disabled={isLoading || !newActivity.subject}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Log Activity
          </button>
        </div>
      </div>
      
      {/* Activity List */}
      <div className="flex-1 overflow-y-auto">
        <div className="divide-y">
          {activities.map((activity) => (
            <div key={activity.id} className="p-4 hover:bg-gray-50">
              <div className="flex items-start gap-3">
                <div className="text-2xl">
                  <ActivityIcon type={activity.activity_type} />
                </div>
                <div className="flex-1">
                  <h4 className="font-medium">{activity.subject}</h4>
                  {activity.description && (
                    <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                  )}
                  <p className="text-xs text-gray-400 mt-2">
                    {new Date(activity.created_at).toLocaleString()}
                  </p>
                </div>
                {activity.outcome && (
                  <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                    {activity.outcome}
                  </span>
                )}
              </div>
            </div>
          ))}
          
          {activities.length === 0 && !isLoading && (
            <div className="p-8 text-center text-gray-500">
              No activities yet. Log your first activity!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// STATS TAB
// ═══════════════════════════════════════════════════════════════════════════════

const StatsTab: React.FC = () => {
  const { stats, fetchStats } = useCRMStore();
  
  useEffect(() => {
    fetchStats();
  }, []);
  
  if (!stats) {
    return <div className="p-8 text-center">Loading stats...</div>;
  }
  
  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold">CRM Dashboard</h2>
      
      {/* Contact Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded shadow border">
          <div className="text-3xl font-bold text-blue-600">{stats.contacts.total}</div>
          <div className="text-gray-500">Total Contacts</div>
        </div>
        <div className="bg-white p-4 rounded shadow border">
          <div className="text-3xl font-bold text-green-600">{stats.contacts.hot_leads}</div>
          <div className="text-gray-500">Hot Leads (70+)</div>
        </div>
        <div className="bg-white p-4 rounded shadow border">
          <div className="text-3xl font-bold text-yellow-600">{stats.contacts.warm_leads}</div>
          <div className="text-gray-500">Warm Leads (40-69)</div>
        </div>
        <div className="bg-white p-4 rounded shadow border">
          <div className="text-3xl font-bold text-red-600">{stats.contacts.cold_leads}</div>
          <div className="text-gray-500">Cold Leads (&lt;40)</div>
        </div>
      </div>
      
      {/* Pipeline Stats */}
      <div className="bg-white p-6 rounded shadow border">
        <h3 className="font-semibold mb-4">Pipeline Summary</h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <div className="text-2xl font-bold text-blue-600">
              ${stats.deals.total_pipeline_value.toLocaleString()}
            </div>
            <div className="text-gray-500">Total Pipeline</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">
              ${stats.deals.won_value.toLocaleString()}
            </div>
            <div className="text-gray-500">Won Revenue</div>
          </div>
          <div>
            <div className="text-2xl font-bold">{stats.deals.win_rate}%</div>
            <div className="text-gray-500">Win Rate</div>
          </div>
        </div>
      </div>
      
      {/* Activity Stats */}
      <div className="bg-white p-6 rounded shadow border">
        <h3 className="font-semibold mb-4">Activity</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-2xl font-bold">{stats.activities.total}</div>
            <div className="text-gray-500">Total Activities</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{stats.activities.this_week}</div>
            <div className="text-gray-500">This Week</div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN PAGE
// ═══════════════════════════════════════════════════════════════════════════════

const BusinessCRMPage: React.FC = () => {
  const { activeTab, setActiveTab, error } = useCRMStore();
  
  const tabs = [
    { id: 'contacts' as const, label: '👥 Contacts', icon: '👥' },
    { id: 'deals' as const, label: '💰 Deals', icon: '💰' },
    { id: 'activities' as const, label: '📋 Activities', icon: '📋' },
    { id: 'stats' as const, label: '📊 Stats', icon: '📊' },
  ];
  
  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="bg-white border-b px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">💼 Business CRM</h1>
            <p className="text-gray-500">AI-Powered Sales Intelligence</p>
          </div>
          <div className="flex items-center gap-4">
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              COS 93/100
            </span>
            <span className="text-sm text-gray-500">vs Salesforce: 90% cheaper</span>
          </div>
        </div>
      </header>
      
      {/* Error Banner */}
      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 p-4 text-red-700">
          {error}
        </div>
      )}
      
      {/* Tabs */}
      <div className="bg-white border-b px-6">
        <nav className="flex gap-4">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 font-medium border-b-2 transition-colors ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>
      
      {/* Content */}
      <main className="flex-1 overflow-hidden">
        {activeTab === 'contacts' && <ContactsTab />}
        {activeTab === 'deals' && <DealsTab />}
        {activeTab === 'activities' && <ActivitiesTab />}
        {activeTab === 'stats' && <StatsTab />}
      </main>
    </div>
  );
};

export default BusinessCRMPage;
