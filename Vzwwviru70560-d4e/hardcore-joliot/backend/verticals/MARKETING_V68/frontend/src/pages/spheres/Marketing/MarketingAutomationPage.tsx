/**
 * CHE·NU™ V68 - Marketing Automation Page
 * HubSpot/Mailchimp killer at $29/mo vs $800+/mo
 */

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Mail,
  Users,
  Send,
  Zap,
  FileText,
  BarChart3,
  Plus,
  Search,
  Filter,
  MoreVertical,
  Play,
  Pause,
  Clock,
  TrendingUp,
  Target,
  Sparkles,
  Calendar,
  Eye,
  MousePointer,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  XCircle,
  ChevronRight,
  Settings,
  Trash2,
  Edit,
  Copy,
  ExternalLink,
  Tag,
  Globe,
  FormInput,
  Bot,
  Brain,
  Lightbulb,
} from 'lucide-react';
import { useMarketingStore } from '../../../stores/marketingStore';
import type {
  Contact,
  Campaign,
  Automation,
  Segment,
  LandingPage,
  Form,
  DashboardStats,
  CampaignStatus,
  LeadScoreCategory,
} from '../../../stores/marketingStore';

// ============================================================================
// COMPONENTS
// ============================================================================

// Tab Navigation
const TabNavigation: React.FC = () => {
  const { activeTab, setActiveTab } = useMarketingStore();
  
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'contacts', label: 'Contacts', icon: Users },
    { id: 'campaigns', label: 'Campaigns', icon: Mail },
    { id: 'automations', label: 'Automations', icon: Zap },
    { id: 'pages', label: 'Landing Pages', icon: Globe },
    { id: 'forms', label: 'Forms', icon: FormInput },
  ] as const;

  return (
    <div className="flex space-x-1 bg-gray-100 dark:bg-gray-800 p-1 rounded-xl">
      {tabs.map(tab => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === tab.id
              ? 'bg-white dark:bg-gray-700 text-indigo-600 dark:text-indigo-400 shadow-sm'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
          }`}
        >
          <tab.icon className="w-4 h-4" />
          <span>{tab.label}</span>
        </button>
      ))}
    </div>
  );
};

// Stat Card
const StatCard: React.FC<{
  title: string;
  value: string | number;
  change?: number;
  icon: React.ElementType;
  color: string;
}> = ({ title, value, change, icon: Icon, color }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
  >
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
        <p className="text-2xl font-bold mt-1 text-gray-900 dark:text-white">{value}</p>
        {change !== undefined && (
          <div className={`flex items-center mt-2 text-sm ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            <TrendingUp className={`w-4 h-4 mr-1 ${change < 0 ? 'rotate-180' : ''}`} />
            <span>{Math.abs(change)}% from last month</span>
          </div>
        )}
      </div>
      <div className={`p-3 rounded-xl ${color}`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
    </div>
  </motion.div>
);

// Status Badge
const StatusBadge: React.FC<{ status: CampaignStatus | string }> = ({ status }) => {
  const styles: Record<string, string> = {
    draft: 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300',
    scheduled: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300',
    sending: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300',
    sent: 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300',
    paused: 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300',
    active: 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300',
    inactive: 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300',
  };

  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${styles[status] || styles.draft}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

// Lead Score Badge
const LeadScoreBadge: React.FC<{ score: number; category: LeadScoreCategory }> = ({ score, category }) => {
  const colors: Record<LeadScoreCategory, string> = {
    cold: 'bg-blue-100 text-blue-700 border-blue-300',
    warm: 'bg-yellow-100 text-yellow-700 border-yellow-300',
    hot: 'bg-orange-100 text-orange-700 border-orange-300',
    qualified: 'bg-green-100 text-green-700 border-green-300',
  };

  return (
    <div className={`flex items-center space-x-2 px-2 py-1 rounded-lg border ${colors[category]}`}>
      <Target className="w-3 h-3" />
      <span className="text-xs font-medium">{score}</span>
    </div>
  );
};

// ============================================================================
// DASHBOARD TAB
// ============================================================================

const DashboardTab: React.FC = () => {
  const { dashboardStats, fetchDashboard, isLoading } = useMarketingStore();

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  if (isLoading || !dashboardStats) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
      </div>
    );
  }

  const stats = dashboardStats;

  return (
    <div className="space-y-6">
      {/* Main Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Contacts"
          value={stats.contacts.total.toLocaleString()}
          change={stats.contacts.growth_rate}
          icon={Users}
          color="bg-indigo-500"
        />
        <StatCard
          title="Emails Sent"
          value={stats.campaigns.emails_sent.toLocaleString()}
          icon={Send}
          color="bg-blue-500"
        />
        <StatCard
          title="Avg Open Rate"
          value={`${stats.campaigns.avg_open_rate.toFixed(1)}%`}
          icon={Eye}
          color="bg-green-500"
        />
        <StatCard
          title="Avg Click Rate"
          value={`${stats.campaigns.avg_click_rate.toFixed(1)}%`}
          icon={MousePointer}
          color="bg-purple-500"
        />
      </div>

      {/* Secondary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">Campaigns</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Total</span>
              <span className="font-medium text-gray-900 dark:text-white">{stats.campaigns.total}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Sent</span>
              <span className="font-medium text-gray-900 dark:text-white">{stats.campaigns.sent}</span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">Automations</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Active</span>
              <span className="font-medium text-green-600">{stats.automations.active}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Enrolled</span>
              <span className="font-medium text-gray-900 dark:text-white">{stats.automations.contacts_enrolled}</span>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">Lead Generation</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Forms</span>
              <span className="font-medium text-gray-900 dark:text-white">{stats.forms.total}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Submissions</span>
              <span className="font-medium text-gray-900 dark:text-white">{stats.forms.submissions_this_month}</span>
            </div>
          </div>
        </div>
      </div>

      {/* AI Insights Section */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl p-6 text-white">
        <div className="flex items-center space-x-3 mb-4">
          <Brain className="w-6 h-6" />
          <h3 className="text-lg font-semibold">AI-Powered Insights</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white/10 rounded-lg p-4">
            <Sparkles className="w-5 h-5 mb-2" />
            <p className="text-sm font-medium">Subject Optimization</p>
            <p className="text-xs opacity-80 mt-1">AI-powered subject line scoring</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <Clock className="w-5 h-5 mb-2" />
            <p className="text-sm font-medium">Send Time Prediction</p>
            <p className="text-xs opacity-80 mt-1">Best times to reach your audience</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <Target className="w-5 h-5 mb-2" />
            <p className="text-sm font-medium">Auto-Segmentation</p>
            <p className="text-xs opacity-80 mt-1">Behavioral contact grouping</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// CONTACTS TAB
// ============================================================================

const ContactsTab: React.FC = () => {
  const { contacts, fetchContacts, toggleModal, isLoading } = useMarketingStore();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  useEffect(() => {
    fetchContacts({ search, status: statusFilter as any });
  }, [fetchContacts, search, statusFilter]);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div className="flex items-center space-x-2 flex-1">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search contacts..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          >
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="unsubscribed">Unsubscribed</option>
            <option value="bounced">Bounced</option>
          </select>
        </div>
        <button
          onClick={() => toggleModal('contact', true)}
          className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Add Contact</span>
        </button>
      </div>

      {/* Contacts Table */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Contact</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Tags</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Lead Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Engagement</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {contacts.map((contact) => (
              <motion.tr
                key={contact.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="hover:bg-gray-50 dark:hover:bg-gray-700/50"
              >
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {contact.first_name || contact.last_name 
                        ? `${contact.first_name || ''} ${contact.last_name || ''}`.trim()
                        : 'Unknown'}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">{contact.email}</p>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={contact.status} />
                </td>
                <td className="px-6 py-4">
                  <div className="flex flex-wrap gap-1">
                    {contact.tags.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded text-xs"
                      >
                        {tag}
                      </span>
                    ))}
                    {contact.tags.length > 3 && (
                      <span className="px-2 py-0.5 text-gray-500 text-xs">+{contact.tags.length - 3}</span>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-16 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${
                          contact.lead_score > 80 ? 'bg-green-500' :
                          contact.lead_score > 50 ? 'bg-orange-500' :
                          contact.lead_score > 20 ? 'bg-yellow-500' : 'bg-blue-500'
                        }`}
                        style={{ width: `${contact.lead_score}%` }}
                      />
                    </div>
                    <span className="text-sm text-gray-600 dark:text-gray-400">{contact.lead_score}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center space-x-3 text-sm text-gray-500 dark:text-gray-400">
                    <span title="Emails opened">{contact.email_stats.opened} opens</span>
                    <span title="Links clicked">{contact.email_stats.clicked} clicks</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-right">
                  <button className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                    <MoreVertical className="w-4 h-4 text-gray-500" />
                  </button>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
        {contacts.length === 0 && !isLoading && (
          <div className="text-center py-12">
            <Users className="w-12 h-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No contacts found</p>
            <button
              onClick={() => toggleModal('contact', true)}
              className="mt-4 text-indigo-600 hover:text-indigo-700 font-medium"
            >
              Add your first contact
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// CAMPAIGNS TAB
// ============================================================================

const CampaignsTab: React.FC = () => {
  const { campaigns, fetchCampaigns, toggleModal, sendCampaign, pauseCampaign, isLoading } = useMarketingStore();
  const [statusFilter, setStatusFilter] = useState<string>('');

  useEffect(() => {
    fetchCampaigns(statusFilter as any);
  }, [fetchCampaigns, statusFilter]);

  const handleSend = async (campaignId: string) => {
    if (window.confirm('Are you sure you want to send this campaign?')) {
      await sendCampaign(campaignId);
    }
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          >
            <option value="">All Campaigns</option>
            <option value="draft">Drafts</option>
            <option value="scheduled">Scheduled</option>
            <option value="sent">Sent</option>
          </select>
        </div>
        <button
          onClick={() => toggleModal('campaign', true)}
          className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Create Campaign</span>
        </button>
      </div>

      {/* Campaigns Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {campaigns.map((campaign) => (
          <motion.div
            key={campaign.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
          >
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 dark:text-white truncate">{campaign.name}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-1">{campaign.subject}</p>
                </div>
                <StatusBadge status={campaign.status} />
              </div>

              {campaign.status === 'sent' && (
                <div className="grid grid-cols-3 gap-2 mb-4">
                  <div className="text-center">
                    <p className="text-lg font-bold text-gray-900 dark:text-white">
                      {campaign.stats.open_rate?.toFixed(1) || 0}%
                    </p>
                    <p className="text-xs text-gray-500">Open Rate</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold text-gray-900 dark:text-white">
                      {campaign.stats.click_rate?.toFixed(1) || 0}%
                    </p>
                    <p className="text-xs text-gray-500">Click Rate</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold text-gray-900 dark:text-white">
                      {campaign.stats.sent.toLocaleString()}
                    </p>
                    <p className="text-xs text-gray-500">Sent</p>
                  </div>
                </div>
              )}

              {campaign.scheduled_at && campaign.status === 'scheduled' && (
                <div className="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-4">
                  <Clock className="w-4 h-4 mr-2" />
                  <span>Scheduled for {new Date(campaign.scheduled_at).toLocaleString()}</span>
                </div>
              )}

              <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex space-x-2">
                  <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" title="Edit">
                    <Edit className="w-4 h-4 text-gray-500" />
                  </button>
                  <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" title="Duplicate">
                    <Copy className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
                {campaign.status === 'draft' && (
                  <button
                    onClick={() => handleSend(campaign.id)}
                    className="flex items-center space-x-1 px-3 py-1.5 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700"
                  >
                    <Send className="w-3 h-3" />
                    <span>Send</span>
                  </button>
                )}
                {campaign.status === 'sending' && (
                  <button
                    onClick={() => pauseCampaign(campaign.id)}
                    className="flex items-center space-x-1 px-3 py-1.5 bg-orange-500 text-white rounded-lg text-sm hover:bg-orange-600"
                  >
                    <Pause className="w-3 h-3" />
                    <span>Pause</span>
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {campaigns.length === 0 && !isLoading && (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
          <Mail className="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500 dark:text-gray-400">No campaigns yet</p>
          <button
            onClick={() => toggleModal('campaign', true)}
            className="mt-4 text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Create your first campaign
          </button>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// AUTOMATIONS TAB
// ============================================================================

const AutomationsTab: React.FC = () => {
  const { automations, fetchAutomations, toggleModal, activateAutomation, deactivateAutomation, isLoading } = useMarketingStore();
  const [showActiveOnly, setShowActiveOnly] = useState(false);

  useEffect(() => {
    fetchAutomations(showActiveOnly);
  }, [fetchAutomations, showActiveOnly]);

  const getTriggerIcon = (trigger: string) => {
    const icons: Record<string, React.ElementType> = {
      signup: Users,
      tag_added: Tag,
      form_submit: FormInput,
      email_opened: Eye,
      email_clicked: MousePointer,
      purchase: Target,
    };
    return icons[trigger] || Zap;
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <label className="flex items-center space-x-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showActiveOnly}
            onChange={(e) => setShowActiveOnly(e.target.checked)}
            className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
          />
          <span className="text-gray-700 dark:text-gray-300">Show active only</span>
        </label>
        <button
          onClick={() => toggleModal('automation', true)}
          className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Create Automation</span>
        </button>
      </div>

      {/* Automations List */}
      <div className="space-y-4">
        {automations.map((automation) => {
          const TriggerIcon = getTriggerIcon(automation.trigger);
          return (
            <motion.div
              key={automation.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-xl ${automation.is_active ? 'bg-green-100 dark:bg-green-900' : 'bg-gray-100 dark:bg-gray-700'}`}>
                    <TriggerIcon className={`w-6 h-6 ${automation.is_active ? 'text-green-600' : 'text-gray-500'}`} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">{automation.name}</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      Trigger: {automation.trigger.replace('_', ' ')}
                    </p>
                    <div className="flex items-center space-x-4 mt-3 text-sm">
                      <span className="text-gray-500 dark:text-gray-400">
                        {automation.steps.length} steps
                      </span>
                      <span className="text-gray-500 dark:text-gray-400">
                        {automation.stats.enrolled} enrolled
                      </span>
                      <span className="text-gray-500 dark:text-gray-400">
                        {automation.stats.completed} completed
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <StatusBadge status={automation.is_active ? 'active' : 'inactive'} />
                  {automation.is_active ? (
                    <button
                      onClick={() => deactivateAutomation(automation.id)}
                      className="p-2 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg text-red-600"
                      title="Deactivate"
                    >
                      <Pause className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={() => activateAutomation(automation.id)}
                      className="p-2 hover:bg-green-100 dark:hover:bg-green-900/30 rounded-lg text-green-600"
                      title="Activate"
                    >
                      <Play className="w-4 h-4" />
                    </button>
                  )}
                  <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
                    <MoreVertical className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
              </div>

              {/* Steps Preview */}
              {automation.steps.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center space-x-2 overflow-x-auto pb-2">
                    <div className="flex items-center space-x-1 text-sm text-gray-500 shrink-0">
                      <TriggerIcon className="w-4 h-4" />
                      <span>Trigger</span>
                    </div>
                    {automation.steps.map((step, idx) => (
                      <React.Fragment key={step.id}>
                        <ChevronRight className="w-4 h-4 text-gray-400 shrink-0" />
                        <div className="flex items-center space-x-1 px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded text-sm shrink-0">
                          {step.action === 'send_email' && <Mail className="w-3 h-3" />}
                          {step.action === 'wait' && <Clock className="w-3 h-3" />}
                          {step.action === 'add_tag' && <Tag className="w-3 h-3" />}
                          <span>{step.action.replace('_', ' ')}</span>
                        </div>
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          );
        })}
      </div>

      {automations.length === 0 && !isLoading && (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
          <Zap className="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500 dark:text-gray-400">No automations yet</p>
          <button
            onClick={() => toggleModal('automation', true)}
            className="mt-4 text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Create your first automation
          </button>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// LANDING PAGES TAB
// ============================================================================

const LandingPagesTab: React.FC = () => {
  const { landingPages, fetchLandingPages, toggleModal, publishPage, unpublishPage, isLoading } = useMarketingStore();

  useEffect(() => {
    fetchLandingPages();
  }, [fetchLandingPages]);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-end">
        <button
          onClick={() => toggleModal('page', true)}
          className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Create Page</span>
        </button>
      </div>

      {/* Pages Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {landingPages.map((page) => (
          <motion.div
            key={page.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
          >
            {/* Preview */}
            <div className="h-32 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 flex items-center justify-center">
              <Globe className="w-12 h-12 text-gray-400" />
            </div>

            <div className="p-4">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">{page.name}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">/{page.slug}</p>
                </div>
                <StatusBadge status={page.is_published ? 'active' : 'draft'} />
              </div>

              <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400 mb-4">
                <span className="flex items-center space-x-1">
                  <Eye className="w-4 h-4" />
                  <span>{page.stats.views}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Users className="w-4 h-4" />
                  <span>{page.stats.unique_visitors}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Target className="w-4 h-4" />
                  <span>{page.stats.conversions}</span>
                </span>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex space-x-2">
                  <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" title="Edit">
                    <Edit className="w-4 h-4 text-gray-500" />
                  </button>
                  <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" title="View">
                    <ExternalLink className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
                {page.is_published ? (
                  <button
                    onClick={() => unpublishPage(page.id)}
                    className="text-sm text-red-600 hover:text-red-700 font-medium"
                  >
                    Unpublish
                  </button>
                ) : (
                  <button
                    onClick={() => publishPage(page.id)}
                    className="text-sm text-green-600 hover:text-green-700 font-medium"
                  >
                    Publish
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {landingPages.length === 0 && !isLoading && (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
          <Globe className="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500 dark:text-gray-400">No landing pages yet</p>
          <button
            onClick={() => toggleModal('page', true)}
            className="mt-4 text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Create your first landing page
          </button>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// FORMS TAB
// ============================================================================

const FormsTab: React.FC = () => {
  const { forms, fetchForms, toggleModal, isLoading } = useMarketingStore();

  useEffect(() => {
    fetchForms();
  }, [fetchForms]);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-end">
        <button
          onClick={() => toggleModal('form', true)}
          className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Create Form</span>
        </button>
      </div>

      {/* Forms List */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Form</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fields</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Submissions</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Tags</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Automation</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {forms.map((form) => (
              <motion.tr
                key={form.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="hover:bg-gray-50 dark:hover:bg-gray-700/50"
              >
                <td className="px-6 py-4">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
                      <FormInput className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                    </div>
                    <span className="font-medium text-gray-900 dark:text-white">{form.name}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-gray-500 dark:text-gray-400">
                  {form.fields.length} fields
                </td>
                <td className="px-6 py-4">
                  <span className="font-medium text-gray-900 dark:text-white">{form.submissions_count}</span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex flex-wrap gap-1">
                    {form.tags_to_add.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded text-xs"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="px-6 py-4">
                  {form.automation_id ? (
                    <span className="flex items-center space-x-1 text-green-600">
                      <Zap className="w-4 h-4" />
                      <span className="text-sm">Connected</span>
                    </span>
                  ) : (
                    <span className="text-gray-400 text-sm">None</span>
                  )}
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex items-center justify-end space-x-2">
                    <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" title="Edit">
                      <Edit className="w-4 h-4 text-gray-500" />
                    </button>
                    <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg" title="Embed">
                      <Copy className="w-4 h-4 text-gray-500" />
                    </button>
                  </div>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
        {forms.length === 0 && !isLoading && (
          <div className="text-center py-12">
            <FormInput className="w-12 h-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No forms yet</p>
            <button
              onClick={() => toggleModal('form', true)}
              className="mt-4 text-indigo-600 hover:text-indigo-700 font-medium"
            >
              Create your first form
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// MAIN PAGE COMPONENT
// ============================================================================

const MarketingAutomationPage: React.FC = () => {
  const { activeTab, error, clearError } = useMarketingStore();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center space-x-2">
                <Mail className="w-7 h-7 text-indigo-600" />
                <span>Marketing Automation</span>
              </h1>
              <p className="text-gray-500 dark:text-gray-400 mt-1">
                Email campaigns, automations, and lead generation
              </p>
            </div>
            <TabNavigation />
          </div>
        </div>
      </div>

      {/* Error Alert */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4"
          >
            <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-center justify-between">
              <div className="flex items-center space-x-2 text-red-700 dark:text-red-400">
                <AlertCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
              <button onClick={clearError} className="text-red-700 dark:text-red-400 hover:text-red-900">
                <XCircle className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
          >
            {activeTab === 'dashboard' && <DashboardTab />}
            {activeTab === 'contacts' && <ContactsTab />}
            {activeTab === 'campaigns' && <CampaignsTab />}
            {activeTab === 'automations' && <AutomationsTab />}
            {activeTab === 'pages' && <LandingPagesTab />}
            {activeTab === 'forms' && <FormsTab />}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* AI Assistant Button */}
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="fixed bottom-6 right-6 p-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full shadow-lg hover:shadow-xl transition-shadow"
        title="AI Assistant"
      >
        <Bot className="w-6 h-6" />
      </motion.button>
    </div>
  );
};

export default MarketingAutomationPage;
