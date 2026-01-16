/* =====================================================
   CHE·NU — MISSING FRONTEND PAGES
   
   4 pages manquantes identifiées dans l'audit:
   - ScholarPage.tsx
   - FinancePage.tsx
   - WellnessPage.tsx
   - SandboxPage.tsx
   
   SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
   ===================================================== */

// ============================================================
// FILE 1: ScholarPage.tsx
// ============================================================

/*
--- FILE: /pages/spaces/ScholarPage.tsx
*/

import React, { useState } from 'react';

interface Course {
  id: string;
  title: string;
  progress: number;
  category: string;
  lastAccessed: string;
}

interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
  createdAt: string;
}

interface ResearchProject {
  id: string;
  title: string;
  status: 'active' | 'paused' | 'completed';
  sources: number;
  notes: number;
}

const ScholarPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'courses' | 'notes' | 'research' | 'bibliography'>('courses');
  
  const [courses] = useState<Course[]>([
    { id: '1', title: 'Machine Learning Fundamentals', progress: 45, category: 'AI/ML', lastAccessed: '2025-12-11' },
    { id: '2', title: 'Construction Law Quebec', progress: 72, category: 'Legal', lastAccessed: '2025-12-10' },
    { id: '3', title: 'Project Management Professional', progress: 30, category: 'Management', lastAccessed: '2025-12-09' },
  ]);
  
  const [notes] = useState<Note[]>([
    { id: '1', title: 'Neural Networks Architecture', content: '...', tags: ['AI', 'Deep Learning'], createdAt: '2025-12-11' },
    { id: '2', title: 'RBQ Regulations Summary', content: '...', tags: ['Construction', 'Quebec'], createdAt: '2025-12-10' },
  ]);
  
  const [research] = useState<ResearchProject[]>([
    { id: '1', title: 'AI in Construction Safety', status: 'active', sources: 23, notes: 15 },
    { id: '2', title: 'Sustainable Building Materials', status: 'paused', sources: 12, notes: 8 },
  ]);
  
  return (
    <div className="min-h-screen bg-[#1E1F22] text-[#E9E4D6] p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-4xl">📚</span>
          <h1 className="text-3xl font-bold text-[#D8B26A]">Scholar</h1>
        </div>
        <p className="text-[#8D8371]">Apprentissage et recherche</p>
      </div>
      
      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-[#2F4C39] pb-2">
        {(['courses', 'notes', 'research', 'bibliography'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-t-lg transition-colors ${
              activeTab === tab 
                ? 'bg-[#3EB4A2] text-white' 
                : 'bg-[#2F4C39] text-[#8D8371] hover:bg-[#3F7249]'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>
      
      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {activeTab === 'courses' && courses.map(course => (
          <div key={course.id} className="bg-[#2F4C39] rounded-lg p-4">
            <h3 className="text-lg font-semibold text-[#D8B26A]">{course.title}</h3>
            <p className="text-sm text-[#8D8371] mb-3">{course.category}</p>
            <div className="w-full bg-[#1E1F22] rounded-full h-2 mb-2">
              <div 
                className="bg-[#3EB4A2] h-2 rounded-full" 
                style={{ width: `${course.progress}%` }}
              />
            </div>
            <p className="text-sm text-[#8D8371]">{course.progress}% complete</p>
          </div>
        ))}
        
        {activeTab === 'notes' && notes.map(note => (
          <div key={note.id} className="bg-[#2F4C39] rounded-lg p-4">
            <h3 className="text-lg font-semibold text-[#D8B26A]">{note.title}</h3>
            <div className="flex gap-2 mt-2">
              {note.tags.map(tag => (
                <span key={tag} className="px-2 py-1 bg-[#3EB4A2] text-xs rounded">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        ))}
        
        {activeTab === 'research' && research.map(project => (
          <div key={project.id} className="bg-[#2F4C39] rounded-lg p-4">
            <h3 className="text-lg font-semibold text-[#D8B26A]">{project.title}</h3>
            <p className={`text-sm ${
              project.status === 'active' ? 'text-[#3EB4A2]' : 
              project.status === 'paused' ? 'text-[#D8B26A]' : 'text-[#8D8371]'
            }`}>
              {project.status.toUpperCase()}
            </p>
            <div className="flex gap-4 mt-2 text-sm text-[#8D8371]">
              <span>{project.sources} sources</span>
              <span>{project.notes} notes</span>
            </div>
          </div>
        ))}
        
        {activeTab === 'bibliography' && (
          <div className="col-span-2 bg-[#2F4C39] rounded-lg p-4">
            <h3 className="text-lg font-semibold text-[#D8B26A] mb-4">Bibliography</h3>
            <p className="text-[#8D8371]">Manage your research sources and citations here.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScholarPage;


// ============================================================
// FILE 2: FinancePage.tsx
// ============================================================

/*
--- FILE: /pages/spaces/FinancePage.tsx
*/

import React, { useState } from 'react';

interface Transaction {
  id: string;
  description: string;
  amount: number;
  type: 'income' | 'expense';
  category: string;
  date: string;
}

interface Budget {
  id: string;
  category: string;
  allocated: number;
  spent: number;
}

interface Invoice {
  id: string;
  client: string;
  amount: number;
  status: 'paid' | 'pending' | 'overdue';
  dueDate: string;
}

const FinancePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'transactions' | 'budgets' | 'invoices'>('overview');
  
  const [transactions] = useState<Transaction[]>([
    { id: '1', description: 'Client Payment - Project Alpha', amount: 5000, type: 'income', category: 'Projects', date: '2025-12-11' },
    { id: '2', description: 'Software Subscription', amount: -99, type: 'expense', category: 'Tools', date: '2025-12-10' },
    { id: '3', description: 'Material Purchase', amount: -1200, type: 'expense', category: 'Materials', date: '2025-12-09' },
  ]);
  
  const [budgets] = useState<Budget[]>([
    { id: '1', category: 'Marketing', allocated: 5000, spent: 3200 },
    { id: '2', category: 'Operations', allocated: 10000, spent: 7500 },
    { id: '3', category: 'R&D', allocated: 8000, spent: 2000 },
  ]);
  
  const [invoices] = useState<Invoice[]>([
    { id: '1', client: 'Acme Corp', amount: 12000, status: 'paid', dueDate: '2025-12-01' },
    { id: '2', client: 'BuildRight Inc', amount: 8500, status: 'pending', dueDate: '2025-12-15' },
    { id: '3', client: 'GreenBuild LLC', amount: 3200, status: 'overdue', dueDate: '2025-12-05' },
  ]);
  
  const totalIncome = transactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
  const totalExpenses = Math.abs(transactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0));
  
  return (
    <div className="min-h-screen bg-[#1E1F22] text-[#E9E4D6] p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-4xl">💰</span>
          <h1 className="text-3xl font-bold text-[#D8B26A]">Finance</h1>
        </div>
        <p className="text-[#8D8371]">Gestion financière</p>
      </div>
      
      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-[#2F4C39] rounded-lg p-4">
          <p className="text-sm text-[#8D8371]">Total Income</p>
          <p className="text-2xl font-bold text-[#3EB4A2]">${totalIncome.toLocaleString()}</p>
        </div>
        <div className="bg-[#2F4C39] rounded-lg p-4">
          <p className="text-sm text-[#8D8371]">Total Expenses</p>
          <p className="text-2xl font-bold text-[#7A593A]">${totalExpenses.toLocaleString()}</p>
        </div>
        <div className="bg-[#2F4C39] rounded-lg p-4">
          <p className="text-sm text-[#8D8371]">Net Balance</p>
          <p className={`text-2xl font-bold ${totalIncome - totalExpenses >= 0 ? 'text-[#3EB4A2]' : 'text-red-500'}`}>
            ${(totalIncome - totalExpenses).toLocaleString()}
          </p>
        </div>
      </div>
      
      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-[#2F4C39] pb-2">
        {(['overview', 'transactions', 'budgets', 'invoices'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-t-lg transition-colors ${
              activeTab === tab 
                ? 'bg-[#3EB4A2] text-white' 
                : 'bg-[#2F4C39] text-[#8D8371] hover:bg-[#3F7249]'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>
      
      {/* Content */}
      {activeTab === 'transactions' && (
        <div className="bg-[#2F4C39] rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-[#1E1F22]">
              <tr>
                <th className="text-left p-3 text-[#8D8371]">Description</th>
                <th className="text-left p-3 text-[#8D8371]">Category</th>
                <th className="text-left p-3 text-[#8D8371]">Date</th>
                <th className="text-right p-3 text-[#8D8371]">Amount</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(tx => (
                <tr key={tx.id} className="border-t border-[#1E1F22]">
                  <td className="p-3">{tx.description}</td>
                  <td className="p-3 text-[#8D8371]">{tx.category}</td>
                  <td className="p-3 text-[#8D8371]">{tx.date}</td>
                  <td className={`p-3 text-right font-semibold ${tx.amount >= 0 ? 'text-[#3EB4A2]' : 'text-[#7A593A]'}`}>
                    {tx.amount >= 0 ? '+' : ''}${tx.amount.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {activeTab === 'budgets' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {budgets.map(budget => (
            <div key={budget.id} className="bg-[#2F4C39] rounded-lg p-4">
              <h3 className="text-lg font-semibold text-[#D8B26A]">{budget.category}</h3>
              <div className="flex justify-between text-sm text-[#8D8371] mt-2">
                <span>Spent: ${budget.spent.toLocaleString()}</span>
                <span>Budget: ${budget.allocated.toLocaleString()}</span>
              </div>
              <div className="w-full bg-[#1E1F22] rounded-full h-3 mt-2">
                <div 
                  className={`h-3 rounded-full ${budget.spent / budget.allocated > 0.9 ? 'bg-red-500' : 'bg-[#3EB4A2]'}`}
                  style={{ width: `${Math.min((budget.spent / budget.allocated) * 100, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
      
      {activeTab === 'invoices' && (
        <div className="grid grid-cols-1 gap-4">
          {invoices.map(invoice => (
            <div key={invoice.id} className="bg-[#2F4C39] rounded-lg p-4 flex justify-between items-center">
              <div>
                <h3 className="text-lg font-semibold text-[#D8B26A]">{invoice.client}</h3>
                <p className="text-sm text-[#8D8371]">Due: {invoice.dueDate}</p>
              </div>
              <div className="text-right">
                <p className="text-xl font-bold">${invoice.amount.toLocaleString()}</p>
                <span className={`px-2 py-1 text-xs rounded ${
                  invoice.status === 'paid' ? 'bg-[#3EB4A2]' :
                  invoice.status === 'pending' ? 'bg-[#D8B26A]' : 'bg-red-500'
                }`}>
                  {invoice.status.toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {activeTab === 'overview' && (
        <div className="text-center py-12 text-[#8D8371]">
          <p>Financial overview dashboard coming soon</p>
        </div>
      )}
    </div>
  );
};

export default FinancePage;


// ============================================================
// FILE 3: WellnessPage.tsx
// ============================================================

/*
--- FILE: /pages/spaces/WellnessPage.tsx
*/

import React, { useState } from 'react';

interface WellnessEntry {
  id: string;
  date: string;
  type: 'sleep' | 'exercise' | 'nutrition' | 'meditation';
  value: number;
  unit: string;
  notes?: string;
}

interface Goal {
  id: string;
  title: string;
  target: number;
  current: number;
  unit: string;
  period: 'daily' | 'weekly';
}

const WellnessPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'tracking' | 'goals' | 'meditation'>('dashboard');
  
  const [entries] = useState<WellnessEntry[]>([
    { id: '1', date: '2025-12-11', type: 'sleep', value: 7.5, unit: 'hours' },
    { id: '2', date: '2025-12-11', type: 'exercise', value: 45, unit: 'minutes' },
    { id: '3', date: '2025-12-11', type: 'meditation', value: 15, unit: 'minutes' },
    { id: '4', date: '2025-12-10', type: 'sleep', value: 6.5, unit: 'hours' },
  ]);
  
  const [goals] = useState<Goal[]>([
    { id: '1', title: 'Sleep', target: 8, current: 7.5, unit: 'hours', period: 'daily' },
    { id: '2', title: 'Exercise', target: 150, current: 120, unit: 'minutes', period: 'weekly' },
    { id: '3', title: 'Meditation', target: 30, current: 15, unit: 'minutes', period: 'daily' },
    { id: '4', title: 'Water', target: 8, current: 6, unit: 'glasses', period: 'daily' },
  ]);
  
  const getTypeEmoji = (type: WellnessEntry['type']) => {
    switch (type) {
      case 'sleep': return '😴';
      case 'exercise': return '🏃';
      case 'nutrition': return '🥗';
      case 'meditation': return '🧘';
      default: return '❓';
    }
  };
  
  return (
    <div className="min-h-screen bg-[#1E1F22] text-[#E9E4D6] p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-4xl">🌿</span>
          <h1 className="text-3xl font-bold text-[#D8B26A]">Wellness</h1>
        </div>
        <p className="text-[#8D8371]">Santé et bien-être — tracking supportif, jamais de diagnostic</p>
      </div>
      
      {/* Disclaimer */}
      <div className="bg-[#7A593A] bg-opacity-20 border border-[#7A593A] rounded-lg p-4 mb-6">
        <p className="text-sm text-[#D8B26A]">
          ⚠️ CHE·NU Wellness est un outil de suivi personnel. Il ne fournit pas de conseils médicaux.
          Consultez toujours un professionnel de santé pour des questions médicales.
        </p>
      </div>
      
      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-[#2F4C39] pb-2">
        {(['dashboard', 'tracking', 'goals', 'meditation'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-t-lg transition-colors ${
              activeTab === tab 
                ? 'bg-[#3EB4A2] text-white' 
                : 'bg-[#2F4C39] text-[#8D8371] hover:bg-[#3F7249]'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>
      
      {/* Content */}
      {activeTab === 'goals' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {goals.map(goal => (
            <div key={goal.id} className="bg-[#2F4C39] rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-lg font-semibold text-[#D8B26A]">{goal.title}</h3>
                <span className="text-xs text-[#8D8371]">{goal.period}</span>
              </div>
              <p className="text-sm text-[#8D8371] mb-2">
                {goal.current} / {goal.target} {goal.unit}
              </p>
              <div className="w-full bg-[#1E1F22] rounded-full h-3">
                <div 
                  className="bg-[#3EB4A2] h-3 rounded-full transition-all"
                  style={{ width: `${Math.min((goal.current / goal.target) * 100, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
      
      {activeTab === 'tracking' && (
        <div className="space-y-4">
          {entries.map(entry => (
            <div key={entry.id} className="bg-[#2F4C39] rounded-lg p-4 flex items-center gap-4">
              <span className="text-2xl">{getTypeEmoji(entry.type)}</span>
              <div className="flex-1">
                <p className="font-semibold capitalize">{entry.type}</p>
                <p className="text-sm text-[#8D8371]">{entry.date}</p>
              </div>
              <div className="text-right">
                <p className="text-xl font-bold text-[#3EB4A2]">{entry.value}</p>
                <p className="text-sm text-[#8D8371]">{entry.unit}</p>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {activeTab === 'meditation' && (
        <div className="text-center py-12">
          <span className="text-6xl">🧘</span>
          <h2 className="text-2xl font-bold text-[#D8B26A] mt-4">Meditation Timer</h2>
          <p className="text-[#8D8371] mt-2">Guided meditation sessions coming soon</p>
          <button className="mt-6 px-6 py-3 bg-[#3EB4A2] rounded-lg hover:bg-[#3F7249] transition-colors">
            Start Quick Session (5 min)
          </button>
        </div>
      )}
      
      {activeTab === 'dashboard' && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-[#2F4C39] rounded-lg p-4 text-center">
            <span className="text-3xl">😴</span>
            <p className="text-2xl font-bold text-[#D8B26A] mt-2">7.5h</p>
            <p className="text-sm text-[#8D8371]">Sleep today</p>
          </div>
          <div className="bg-[#2F4C39] rounded-lg p-4 text-center">
            <span className="text-3xl">🏃</span>
            <p className="text-2xl font-bold text-[#3EB4A2] mt-2">45min</p>
            <p className="text-sm text-[#8D8371]">Exercise today</p>
          </div>
          <div className="bg-[#2F4C39] rounded-lg p-4 text-center">
            <span className="text-3xl">🧘</span>
            <p className="text-2xl font-bold text-[#3EB4A2] mt-2">15min</p>
            <p className="text-sm text-[#8D8371]">Meditation today</p>
          </div>
          <div className="bg-[#2F4C39] rounded-lg p-4 text-center">
            <span className="text-3xl">💧</span>
            <p className="text-2xl font-bold text-[#7A593A] mt-2">6/8</p>
            <p className="text-sm text-[#8D8371]">Water glasses</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default WellnessPage;


// ============================================================
// FILE 4: SandboxPage.tsx
// ============================================================

/*
--- FILE: /pages/spaces/SandboxPage.tsx
*/

import React, { useState } from 'react';

interface Experiment {
  id: string;
  title: string;
  description: string;
  status: 'draft' | 'running' | 'completed' | 'failed';
  createdAt: string;
  tags: string[];
}

interface Prototype {
  id: string;
  name: string;
  type: 'component' | 'workflow' | 'integration' | 'agent';
  version: string;
  lastModified: string;
}

const SandboxPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'experiments' | 'prototypes' | 'playground' | 'logs'>('experiments');
  
  const [experiments] = useState<Experiment[]>([
    { 
      id: '1', 
      title: 'AI Agent Response Testing', 
      description: 'Testing new methodology agent responses',
      status: 'running',
      createdAt: '2025-12-11',
      tags: ['AI', 'Agents', 'Testing']
    },
    { 
      id: '2', 
      title: 'XR Navigation Prototype', 
      description: 'Experimenting with 3D navigation patterns',
      status: 'completed',
      createdAt: '2025-12-10',
      tags: ['XR', 'Navigation', 'UI']
    },
    { 
      id: '3', 
      title: 'Data Visualization Tests', 
      description: 'New chart types for financial data',
      status: 'draft',
      createdAt: '2025-12-09',
      tags: ['Charts', 'Finance', 'UI']
    },
  ]);
  
  const [prototypes] = useState<Prototype[]>([
    { id: '1', name: 'DecisionTreeViewer', type: 'component', version: '0.3.0', lastModified: '2025-12-11' },
    { id: '2', name: 'AutomatedReporting', type: 'workflow', version: '0.1.0', lastModified: '2025-12-10' },
    { id: '3', name: 'CustomAgentTemplate', type: 'agent', version: '0.2.0', lastModified: '2025-12-09' },
  ]);
  
  const getStatusColor = (status: Experiment['status']) => {
    switch (status) {
      case 'running': return 'bg-[#3EB4A2]';
      case 'completed': return 'bg-[#3F7249]';
      case 'failed': return 'bg-red-500';
      default: return 'bg-[#8D8371]';
    }
  };
  
  const getTypeIcon = (type: Prototype['type']) => {
    switch (type) {
      case 'component': return '🧩';
      case 'workflow': return '⚙️';
      case 'integration': return '🔗';
      case 'agent': return '🤖';
      default: return '📦';
    }
  };
  
  return (
    <div className="min-h-screen bg-[#1E1F22] text-[#E9E4D6] p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-4xl">🧪</span>
          <h1 className="text-3xl font-bold text-[#D8B26A]">Sandbox</h1>
        </div>
        <p className="text-[#8D8371]">Espace d'expérimentation sécurisé — aucune conséquence réelle</p>
      </div>
      
      {/* Safety Notice */}
      <div className="bg-[#3EB4A2] bg-opacity-20 border border-[#3EB4A2] rounded-lg p-4 mb-6">
        <p className="text-sm text-[#3EB4A2]">
          🔒 <strong>Mode Sandbox:</strong> Toutes les actions sont simulées. 
          Aucune donnée réelle n'est modifiée. Expérimentez librement!
        </p>
      </div>
      
      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-[#2F4C39] pb-2">
        {(['experiments', 'prototypes', 'playground', 'logs'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-t-lg transition-colors ${
              activeTab === tab 
                ? 'bg-[#3EB4A2] text-white' 
                : 'bg-[#2F4C39] text-[#8D8371] hover:bg-[#3F7249]'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>
      
      {/* Content */}
      {activeTab === 'experiments' && (
        <div className="space-y-4">
          <button className="w-full py-3 border-2 border-dashed border-[#3EB4A2] rounded-lg text-[#3EB4A2] hover:bg-[#3EB4A2] hover:text-white transition-colors">
            + New Experiment
          </button>
          {experiments.map(exp => (
            <div key={exp.id} className="bg-[#2F4C39] rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-[#D8B26A]">{exp.title}</h3>
                <span className={`px-2 py-1 text-xs rounded ${getStatusColor(exp.status)}`}>
                  {exp.status.toUpperCase()}
                </span>
              </div>
              <p className="text-sm text-[#8D8371] mb-3">{exp.description}</p>
              <div className="flex gap-2">
                {exp.tags.map(tag => (
                  <span key={tag} className="px-2 py-1 bg-[#1E1F22] text-xs rounded text-[#8D8371]">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      
      {activeTab === 'prototypes' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {prototypes.map(proto => (
            <div key={proto.id} className="bg-[#2F4C39] rounded-lg p-4">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">{getTypeIcon(proto.type)}</span>
                <div>
                  <h3 className="font-semibold text-[#D8B26A]">{proto.name}</h3>
                  <p className="text-xs text-[#8D8371]">v{proto.version}</p>
                </div>
              </div>
              <p className="text-sm text-[#8D8371]">
                Last modified: {proto.lastModified}
              </p>
              <div className="flex gap-2 mt-3">
                <button className="px-3 py-1 bg-[#3EB4A2] text-sm rounded">Edit</button>
                <button className="px-3 py-1 bg-[#1E1F22] text-sm rounded">Duplicate</button>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {activeTab === 'playground' && (
        <div className="bg-[#2F4C39] rounded-lg p-6">
          <h2 className="text-xl font-bold text-[#D8B26A] mb-4">Code Playground</h2>
          <div className="bg-[#1E1F22] rounded-lg p-4 font-mono text-sm">
            <pre className="text-[#3EB4A2]">
{`// Write your experimental code here
function testFeature() {
  console.log("Testing new feature...");
  return { success: true };
}

testFeature();`}
            </pre>
          </div>
          <div className="flex gap-2 mt-4">
            <button className="px-4 py-2 bg-[#3EB4A2] rounded">Run</button>
            <button className="px-4 py-2 bg-[#1E1F22] rounded">Clear</button>
            <button className="px-4 py-2 bg-[#1E1F22] rounded">Save as Prototype</button>
          </div>
        </div>
      )}
      
      {activeTab === 'logs' && (
        <div className="bg-[#2F4C39] rounded-lg p-4">
          <h2 className="text-lg font-bold text-[#D8B26A] mb-4">Experiment Logs</h2>
          <div className="space-y-2 font-mono text-sm">
            <p className="text-[#3EB4A2]">[12:34:56] Experiment #1 started</p>
            <p className="text-[#8D8371]">[12:34:57] Running test suite...</p>
            <p className="text-[#8D8371]">[12:35:02] 5 tests passed</p>
            <p className="text-[#D8B26A]">[12:35:03] 1 warning detected</p>
            <p className="text-[#3EB4A2]">[12:35:05] Experiment completed</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SandboxPage;


// ============================================================
// EXPORTS
// ============================================================

export { ScholarPage, FinancePage, WellnessPage, SandboxPage };
