# 🎨 AGENT BETA — FRONTEND & USER EXPERIENCE

```
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                              ║
║                              AGENT BETA BRIEFING                                             ║
║                              CHE·NU™ V54 Development                                         ║
║                                                                                              ║
║                              Focus: Frontend, UI/UX, Integration                             ║
║                              Stack: React, TypeScript, Zustand                               ║
║                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 🎯 MISSION

Tu es Agent Beta, responsable du développement **frontend et expérience utilisateur** de CHE·NU V54.

Ton travail:
1. Créer l'**Identity UI** (sélection, switch, management)
2. Construire l'**Agent Marketplace** (catalogue, embauche, exécution)
3. Implémenter la **Governance UI** (checkpoints, approbations, audit)
4. Développer le **Token Economy UI** (budgets, consommation)
5. Créer le **1-Click Command Bar** (entrée commandes, workflows)
6. Clarifier le **DataSpace UI** (contexte, navigation)
7. Ajouter le **XR Mode Toggle** (basculement immersif)

---

## 📋 CONTEXTE CRITIQUE

### Problème identifié par l'audit:

Le frontend V53 est un **shell UI bien conçu** mais **déconnecté** des features core:

| Feature | UI Existe | Fonctionnel | Connecté Backend |
|---------|-----------|-------------|------------------|
| Identity System | ❌ | ❌ | ❌ |
| Agent Marketplace | ❌ | ❌ | ❌ |
| Governance Dashboard | ⚠️ Partiel | ⚠️ | ⚠️ |
| Token Display | ❌ | ❌ | ❌ |
| 1-Click Bar | ❌ | ❌ | ❌ |
| DataSpace Context | ⚠️ Flou | ⚠️ | ⚠️ |
| XR Toggle | ❌ | ❌ | ❌ |

**Ton rôle: Créer les interfaces et les connecter au backend (Agent Alpha).**

---

## 🎨 DESIGN SYSTEM CHE·NU

### Couleurs Brand
```typescript
const CHENU_COLORS = {
  sacredGold: '#D8B26A',
  ancientStone: '#8D8371',
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
};
```

### Principes UI
- **Clarté > Features**: Moins d'éléments visibles = plus de pouvoir cognitif
- **Context First**: Toujours montrer où l'utilisateur se trouve
- **Governance Visible**: Les checkpoints et approbations doivent être clairs
- **Progressive Disclosure**: Complexité révélée selon le besoin

---

## 🔧 SPRINTS ASSIGNÉS

### 🔴 SPRINT B1: Identity UI (CRITIQUE)

**Objectif**: Permettre aux utilisateurs de gérer leurs identités

#### B1.1 Identity Selector Component

```tsx
// frontend/src/components/identity/IdentitySelector.tsx

import React, { useState } from 'react';
import { useIdentityStore } from '@/stores/identityStore';

interface Identity {
  id: string;
  type: 'personal' | 'enterprise' | 'creative' | 'government';
  name: string;
  avatar?: string;
  color: string;
}

export const IdentitySelector: React.FC = () => {
  const { currentIdentity, identities, switchIdentity } = useIdentityStore();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="identity-selector">
      {/* Current Identity Badge */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="identity-badge"
        style={{ borderColor: currentIdentity?.color }}
      >
        <span className="identity-avatar">{currentIdentity?.avatar}</span>
        <span className="identity-name">{currentIdentity?.name}</span>
        <ChevronDown />
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="identity-dropdown">
          {identities.map(identity => (
            <IdentityCard 
              key={identity.id}
              identity={identity}
              isActive={identity.id === currentIdentity?.id}
              onSelect={() => {
                switchIdentity(identity.id);
                setIsOpen(false);
              }}
            />
          ))}
          <button className="create-identity-btn">
            + Nouvelle Identité
          </button>
        </div>
      )}
    </div>
  );
};
```

#### B1.2 Identity Store (Zustand)

```tsx
// frontend/src/stores/identityStore.ts

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { identityApi } from '@/services/api/identityApi';

interface IdentityState {
  currentIdentity: Identity | null;
  identities: Identity[];
  isLoading: boolean;
  
  // Actions
  fetchIdentities: () => Promise<void>;
  switchIdentity: (identityId: string) => Promise<void>;
  createIdentity: (data: CreateIdentityInput) => Promise<Identity>;
  deleteIdentity: (identityId: string) => Promise<void>;
}

export const useIdentityStore = create<IdentityState>()(
  persist(
    (set, get) => ({
      currentIdentity: null,
      identities: [],
      isLoading: false,

      fetchIdentities: async () => {
        set({ isLoading: true });
        const identities = await identityApi.list();
        set({ identities, isLoading: false });
      },

      switchIdentity: async (identityId: string) => {
        set({ isLoading: true });
        await identityApi.switch(identityId);
        const identity = get().identities.find(i => i.id === identityId);
        set({ currentIdentity: identity, isLoading: false });
        
        // IMPORTANT: Refresh all data with new identity context
        window.dispatchEvent(new CustomEvent('identity-changed'));
      },

      createIdentity: async (data) => {
        const identity = await identityApi.create(data);
        set(state => ({ identities: [...state.identities, identity] }));
        return identity;
      },

      deleteIdentity: async (identityId: string) => {
        await identityApi.delete(identityId);
        set(state => ({
          identities: state.identities.filter(i => i.id !== identityId)
        }));
      },
    }),
    { name: 'chenu-identity' }
  )
);
```

#### B1.3 Identity in Header

```tsx
// Modifier: frontend/src/components/layout/Header.tsx

export const Header: React.FC = () => {
  return (
    <header className="chenu-header">
      <div className="header-left">
        <Logo />
        <IdentitySelector /> {/* NOUVEAU */}
      </div>
      
      <div className="header-center">
        <OneClickCommandBar /> {/* NOUVEAU - Sprint B5 */}
      </div>
      
      <div className="header-right">
        <TokenBalance /> {/* NOUVEAU - Sprint B4 */}
        <NotificationBell />
        <UserMenu />
      </div>
    </header>
  );
};
```

---

### 🔴 SPRINT B2: Agent Marketplace UI (CRITIQUE)

**Objectif**: Permettre la découverte et l'embauche d'agents

#### B2.1 Agent Catalog

```tsx
// frontend/src/components/agents/AgentCatalog.tsx

interface AgentCatalogProps {
  sphere?: string;
  domain?: string;
}

export const AgentCatalog: React.FC<AgentCatalogProps> = ({ sphere, domain }) => {
  const [agents, setAgents] = useState<AgentDefinition[]>([]);
  const [filters, setFilters] = useState({ level: '', search: '' });

  return (
    <div className="agent-catalog">
      <div className="catalog-header">
        <h2>Agent Marketplace</h2>
        <AgentSearch onSearch={(q) => setFilters(f => ({ ...f, search: q }))} />
      </div>
      
      <div className="catalog-filters">
        <AgentFilters 
          currentFilters={filters}
          onFilterChange={setFilters}
        />
      </div>
      
      <div className="catalog-grid">
        {agents.map(agent => (
          <AgentCard 
            key={agent.id}
            agent={agent}
            onHire={() => openHireModal(agent)}
          />
        ))}
      </div>
    </div>
  );
};
```

#### B2.2 Agent Card

```tsx
// frontend/src/components/agents/AgentCard.tsx

interface AgentCardProps {
  agent: AgentDefinition;
  onHire: () => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onHire }) => {
  const levelColors = {
    L0: '#D8B26A', // Gold - Nova
    L1: '#3F7249', // Green - Chiefs
    L2: '#3EB4A2', // Turquoise - Specialists
    L3: '#8D8371', // Stone - Workers
  };

  return (
    <div className="agent-card">
      <div className="agent-header">
        <div 
          className="agent-level-badge"
          style={{ backgroundColor: levelColors[agent.level] }}
        >
          {agent.level}
        </div>
        <span className="agent-sphere">{agent.sphere}</span>
      </div>
      
      <div className="agent-avatar">
        {agent.icon || '🤖'}
      </div>
      
      <h3 className="agent-name">{agent.name}</h3>
      <p className="agent-description">{agent.shortDescription}</p>
      
      <div className="agent-capabilities">
        {agent.capabilities.slice(0, 3).map(cap => (
          <span key={cap} className="capability-tag">{cap}</span>
        ))}
      </div>
      
      <div className="agent-footer">
        <span className="agent-cost">
          ~{agent.avgTokensPerTask} tokens/tâche
        </span>
        <button className="hire-btn" onClick={onHire}>
          Embaucher
        </button>
      </div>
    </div>
  );
};
```

#### B2.3 Hire Agent Modal

```tsx
// frontend/src/components/agents/HireAgentModal.tsx

export const HireAgentModal: React.FC<{ agent: AgentDefinition }> = ({ agent }) => {
  const [scope, setScope] = useState<string[]>([]);
  const [budget, setBudget] = useState<number>(1000);
  
  const handleHire = async () => {
    await agentApi.hire(agent.id, {
      scope,
      tokenBudget: budget,
      dataspaceId: currentDataspace?.id,
    });
    
    toast.success(`${agent.name} embauché!`);
    closeModal();
  };

  return (
    <Modal title={`Embaucher ${agent.name}`}>
      <div className="hire-modal">
        <AgentDetails agent={agent} />
        
        <div className="hire-config">
          <h4>Définir le scope</h4>
          <AgentScopeSelector 
            value={scope}
            onChange={setScope}
          />
          
          <h4>Budget tokens</h4>
          <AgentBudgetSetter
            value={budget}
            onChange={setBudget}
            estimatedCost={agent.avgTokensPerTask * 10}
          />
        </div>
        
        <div className="hire-actions">
          <button onClick={closeModal}>Annuler</button>
          <button className="primary" onClick={handleHire}>
            Confirmer l'embauche
          </button>
        </div>
      </div>
    </Modal>
  );
};
```

#### B2.4 Active Agents Section (Bureau)

```tsx
// frontend/src/components/bureau/sections/ActiveAgentsSection.tsx

export const ActiveAgentsSection: React.FC = () => {
  const { activeAgents, executions } = useAgentStore();
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  return (
    <div className="active-agents-section">
      <div className="section-header">
        <h3>Agents Actifs</h3>
        <button onClick={() => openAgentCatalog()}>
          + Embaucher un agent
        </button>
      </div>
      
      {activeAgents.length === 0 ? (
        <EmptyState 
          icon="🤖"
          title="Aucun agent actif"
          description="Embauchez des agents pour automatiser vos tâches"
          action={<button>Explorer le catalogue</button>}
        />
      ) : (
        <div className="agents-list">
          {activeAgents.map(agent => (
            <ActiveAgentCard
              key={agent.id}
              agent={agent}
              execution={executions[agent.id]}
              onAssignTask={() => openTaskAssigner(agent)}
              onRelease={() => releaseAgent(agent.id)}
            />
          ))}
        </div>
      )}
      
      {/* Panel détails agent sélectionné */}
      {selectedAgent && (
        <AgentDetailPanel agentId={selectedAgent} />
      )}
    </div>
  );
};
```

---

### 🔴 SPRINT B3: Governance UI (CRITIQUE)

**Objectif**: Visualiser et interagir avec le pipeline de gouvernance

#### B3.1 Governance Dashboard

```tsx
// frontend/src/components/governance/GovernanceDashboard.tsx

export const GovernanceDashboard: React.FC = () => {
  const { pendingCheckpoints, recentApprovals } = useGovernanceStore();

  return (
    <div className="governance-dashboard">
      <div className="dashboard-header">
        <h2>Gouvernance</h2>
        <span className="pending-count">
          {pendingCheckpoints.length} approbations en attente
        </span>
      </div>
      
      {/* Pending Approvals */}
      <section className="pending-section">
        <h3>En attente d'approbation</h3>
        <div className="checkpoints-list">
          {pendingCheckpoints.map(checkpoint => (
            <CheckpointCard 
              key={checkpoint.id}
              checkpoint={checkpoint}
              onApprove={() => approveCheckpoint(checkpoint.id)}
              onReject={() => rejectCheckpoint(checkpoint.id)}
            />
          ))}
        </div>
      </section>
      
      {/* Recent Activity */}
      <section className="history-section">
        <h3>Historique récent</h3>
        <ApprovalHistory items={recentApprovals} />
      </section>
      
      {/* Stats */}
      <section className="stats-section">
        <GovernanceStats />
      </section>
    </div>
  );
};
```

#### B3.2 Checkpoint Card

```tsx
// frontend/src/components/governance/CheckpointCard.tsx

export const CheckpointCard: React.FC<{ checkpoint: Checkpoint }> = ({ checkpoint }) => {
  const urgencyColors = {
    low: '#3EB4A2',
    medium: '#D8B26A',
    high: '#E57373',
  };

  return (
    <div className="checkpoint-card">
      <div className="checkpoint-header">
        <span 
          className="urgency-indicator"
          style={{ backgroundColor: urgencyColors[checkpoint.urgency] }}
        />
        <span className="checkpoint-type">{checkpoint.type}</span>
        <span className="checkpoint-time">
          {formatRelativeTime(checkpoint.createdAt)}
        </span>
      </div>
      
      <div className="checkpoint-content">
        <h4>{checkpoint.title}</h4>
        <p>{checkpoint.description}</p>
        
        {/* Agent qui demande */}
        <div className="requesting-agent">
          <span>Demandé par:</span>
          <AgentBadge agent={checkpoint.agent} />
        </div>
        
        {/* Estimation de coût */}
        <CostEstimateDisplay estimate={checkpoint.costEstimate} />
        
        {/* Scope */}
        <ScopeDisplay scope={checkpoint.scope} />
      </div>
      
      <div className="checkpoint-actions">
        <button 
          className="reject-btn"
          onClick={() => onReject(checkpoint.id)}
        >
          Rejeter
        </button>
        <button 
          className="approve-btn"
          onClick={() => onApprove(checkpoint.id)}
        >
          Approuver
        </button>
      </div>
    </div>
  );
};
```

#### B3.3 Audit Trail

```tsx
// frontend/src/components/governance/AuditTrail.tsx

export const AuditTrail: React.FC<{ resourceId: string }> = ({ resourceId }) => {
  const { auditEntries, loadMore, hasMore } = useAuditTrail(resourceId);

  return (
    <div className="audit-trail">
      <h3>Journal d'audit</h3>
      
      <div className="audit-timeline">
        {auditEntries.map((entry, index) => (
          <AuditEntry 
            key={entry.id}
            entry={entry}
            isLast={index === auditEntries.length - 1}
          />
        ))}
      </div>
      
      {hasMore && (
        <button onClick={loadMore}>
          Charger plus
        </button>
      )}
    </div>
  );
};

const AuditEntry: React.FC<{ entry: AuditLogEntry }> = ({ entry }) => (
  <div className="audit-entry">
    <div className="audit-dot" />
    <div className="audit-content">
      <div className="audit-header">
        <span className="audit-actor">
          {entry.actorType === 'agent' ? '🤖' : '👤'} {entry.actorName}
        </span>
        <span className="audit-time">{formatTime(entry.timestamp)}</span>
      </div>
      <p className="audit-action">{entry.action}</p>
      {entry.details && (
        <pre className="audit-details">{JSON.stringify(entry.details, null, 2)}</pre>
      )}
    </div>
  </div>
);
```

---

### 🔴 SPRINT B4: Token Economy UI (CRITIQUE)

**Objectif**: Rendre visible la consommation de tokens

#### B4.1 Token Balance (Header)

```tsx
// frontend/src/components/tokens/TokenBalance.tsx

export const TokenBalance: React.FC = () => {
  const { balance, isLoading } = useTokenStore();
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="token-balance">
      <button 
        className="balance-display"
        onClick={() => setShowDetails(!showDetails)}
      >
        <TokenIcon />
        <span className="balance-amount">
          {formatNumber(balance.available)} tokens
        </span>
      </button>
      
      {showDetails && (
        <div className="balance-dropdown">
          <div className="balance-row">
            <span>Disponible</span>
            <span>{formatNumber(balance.available)}</span>
          </div>
          <div className="balance-row">
            <span>Utilisé ce mois</span>
            <span>{formatNumber(balance.usedThisMonth)}</span>
          </div>
          <div className="balance-row">
            <span>Budget mensuel</span>
            <span>{formatNumber(balance.monthlyBudget)}</span>
          </div>
          
          <TokenUsageChart data={balance.dailyUsage} />
          
          <button onClick={() => navigate('/settings/tokens')}>
            Gérer les tokens
          </button>
        </div>
      )}
    </div>
  );
};
```

#### B4.2 Thread Token Display

```tsx
// frontend/src/components/threads/ThreadBudgetDisplay.tsx

export const ThreadBudgetDisplay: React.FC<{ threadId: string }> = ({ threadId }) => {
  const { budget, used, remaining } = useThreadBudget(threadId);
  const percentage = (used / budget) * 100;
  
  const statusColor = 
    percentage > 90 ? '#E57373' :
    percentage > 70 ? '#D8B26A' :
    '#3EB4A2';

  return (
    <div className="thread-budget">
      <div className="budget-header">
        <span>Budget Thread</span>
        <span>{used} / {budget} tokens</span>
      </div>
      
      <div className="budget-bar">
        <div 
          className="budget-fill"
          style={{ 
            width: `${percentage}%`,
            backgroundColor: statusColor 
          }}
        />
      </div>
      
      {percentage > 80 && (
        <TokenAlert 
          type={percentage > 90 ? 'critical' : 'warning'}
          message={`${remaining} tokens restants`}
        />
      )}
    </div>
  );
};
```

---

### 🟠 SPRINT B5: 1-Click Command Bar (MEDIUM)

**Objectif**: Point d'entrée pour les commandes naturelles

#### B5.1 Command Bar (Cmd+K Style)

```tsx
// frontend/src/components/oneclick/OneClickCommandBar.tsx

export const OneClickCommandBar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [command, setCommand] = useState('');
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [workflow, setWorkflow] = useState<Workflow | null>(null);

  // Keyboard shortcut
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const handleSubmit = async () => {
    if (!command.trim()) return;
    
    // Interpret command
    const interpreted = await oneclickApi.interpret(command);
    
    // Show workflow preview
    const workflow = await oneclickApi.constructWorkflow(interpreted);
    setWorkflow(workflow);
  };

  return (
    <>
      {/* Trigger Button */}
      <button 
        className="oneclick-trigger"
        onClick={() => setIsOpen(true)}
      >
        <SearchIcon />
        <span>Cmd + K</span>
      </button>

      {/* Modal Command Bar */}
      {isOpen && (
        <div className="oneclick-modal">
          <div className="oneclick-backdrop" onClick={() => setIsOpen(false)} />
          
          <div className="oneclick-content">
            <input
              autoFocus
              type="text"
              placeholder="Que voulez-vous faire?"
              value={command}
              onChange={(e) => {
                setCommand(e.target.value);
                // Fetch suggestions
              }}
              onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
            />
            
            {/* Suggestions */}
            {suggestions.length > 0 && !workflow && (
              <OneClickSuggestions 
                suggestions={suggestions}
                onSelect={(s) => setCommand(s.command)}
              />
            )}
            
            {/* Workflow Preview */}
            {workflow && (
              <WorkflowPreview 
                workflow={workflow}
                onConfirm={() => executeWorkflow(workflow)}
                onCancel={() => setWorkflow(null)}
              />
            )}
          </div>
        </div>
      )}
    </>
  );
};
```

#### B5.2 Workflow Preview

```tsx
// frontend/src/components/oneclick/WorkflowPreview.tsx

export const WorkflowPreview: React.FC<{
  workflow: Workflow;
  onConfirm: () => void;
  onCancel: () => void;
}> = ({ workflow, onConfirm, onCancel }) => {
  return (
    <div className="workflow-preview">
      <div className="preview-header">
        <h3>Plan d'exécution</h3>
        <span className="step-count">{workflow.steps.length} étapes</span>
      </div>
      
      <div className="preview-steps">
        {workflow.steps.map((step, index) => (
          <div key={index} className="preview-step">
            <div className="step-number">{index + 1}</div>
            <div className="step-content">
              <span className="step-agent">
                <AgentBadge agent={step.agent} />
              </span>
              <span className="step-action">{step.action}</span>
            </div>
            {step.requiresApproval && (
              <span className="checkpoint-badge">Checkpoint</span>
            )}
          </div>
        ))}
      </div>
      
      <div className="preview-cost">
        <CostEstimateDisplay estimate={workflow.estimatedCost} />
      </div>
      
      <div className="preview-actions">
        <button onClick={onCancel}>Annuler</button>
        <button className="primary" onClick={onConfirm}>
          Exécuter
        </button>
      </div>
    </div>
  );
};
```

---

### 🟠 SPRINT B6: DataSpace UI Clarity

```tsx
// frontend/src/components/dataspace/DataSpaceIndicator.tsx

export const DataSpaceIndicator: React.FC = () => {
  const { currentDataspace } = useDataspaceStore();
  const [showSelector, setShowSelector] = useState(false);

  if (!currentDataspace) {
    return (
      <div className="dataspace-indicator empty">
        <span>Aucun DataSpace sélectionné</span>
        <button onClick={() => setShowSelector(true)}>
          Sélectionner
        </button>
      </div>
    );
  }

  return (
    <div className="dataspace-indicator">
      <div 
        className="dataspace-badge"
        style={{ borderColor: currentDataspace.color }}
        onClick={() => setShowSelector(true)}
      >
        <span className="dataspace-icon">{currentDataspace.icon}</span>
        <span className="dataspace-name">{currentDataspace.name}</span>
        <span className="dataspace-type">{currentDataspace.type}</span>
      </div>
      
      {showSelector && (
        <DataSpaceSelector onSelect={(ds) => {
          switchDataspace(ds.id);
          setShowSelector(false);
        }} />
      )}
    </div>
  );
};
```

---

### 🟠 SPRINT B7: XR Mode Toggle

```tsx
// frontend/src/components/xr/XRModeToggle.tsx

export const XRModeToggle: React.FC = () => {
  const { isXRSupported, isXRActive, toggleXR } = useXRStore();
  
  if (!isXRSupported) {
    return null; // Don't show if device doesn't support XR
  }

  return (
    <button 
      className={`xr-toggle ${isXRActive ? 'active' : ''}`}
      onClick={toggleXR}
      title={isXRActive ? 'Quitter le mode immersif' : 'Mode immersif'}
    >
      <VRIcon />
      {isXRActive && <span className="xr-active-dot" />}
    </button>
  );
};
```

---

## 📁 STRUCTURE DE FICHIERS À CRÉER

```
frontend/src/
├── components/
│   ├── identity/
│   │   ├── IdentitySelector.tsx
│   │   ├── IdentityCard.tsx
│   │   ├── IdentityBadge.tsx
│   │   ├── IdentitySwitcher.tsx
│   │   └── CreateIdentityModal.tsx
│   │
│   ├── agents/
│   │   ├── AgentCatalog.tsx
│   │   ├── AgentCard.tsx
│   │   ├── AgentDetails.tsx
│   │   ├── AgentFilters.tsx
│   │   ├── AgentSearch.tsx
│   │   ├── HireAgentModal.tsx
│   │   ├── AgentScopeSelector.tsx
│   │   ├── AgentBudgetSetter.tsx
│   │   ├── ActiveAgentCard.tsx
│   │   ├── AgentTaskAssigner.tsx
│   │   ├── AgentExecutionStatus.tsx
│   │   └── AgentOutputViewer.tsx
│   │
│   ├── governance/
│   │   ├── GovernanceDashboard.tsx
│   │   ├── PendingApprovals.tsx
│   │   ├── ApprovalHistory.tsx
│   │   ├── GovernanceStats.tsx
│   │   ├── CheckpointCard.tsx
│   │   ├── CheckpointDetails.tsx
│   │   ├── CostEstimateDisplay.tsx
│   │   ├── ScopeDisplay.tsx
│   │   ├── AuditTrail.tsx
│   │   └── AuditEntry.tsx
│   │
│   ├── tokens/
│   │   ├── TokenBalance.tsx
│   │   ├── TokenUsageChart.tsx
│   │   ├── TokenBudgetBar.tsx
│   │   ├── TokenAlert.tsx
│   │   ├── ThreadBudgetDisplay.tsx
│   │   └── ThreadBudgetSetter.tsx
│   │
│   ├── oneclick/
│   │   ├── OneClickCommandBar.tsx
│   │   ├── OneClickSuggestions.tsx
│   │   ├── OneClickHistory.tsx
│   │   ├── WorkflowPreview.tsx
│   │   ├── WorkflowSteps.tsx
│   │   └── WorkflowProgress.tsx
│   │
│   ├── dataspace/
│   │   ├── DataSpaceIndicator.tsx
│   │   ├── DataSpaceBreadcrumb.tsx
│   │   ├── DataSpaceSelector.tsx
│   │   ├── DataSpaceInfo.tsx
│   │   └── CreateDataSpaceModal.tsx
│   │
│   └── xr/
│       ├── XRModeToggle.tsx
│       ├── XRModeIndicator.tsx
│       ├── XRBureauView.tsx
│       └── XRFallback.tsx
│
├── pages/
│   ├── identity/
│   │   ├── IdentityListPage.tsx
│   │   ├── IdentityCreatePage.tsx
│   │   └── IdentitySettingsPage.tsx
│   │
│   └── governance/
│       └── GovernancePage.tsx
│
├── stores/
│   ├── identityStore.ts
│   ├── agentStore.ts
│   ├── governanceStore.ts
│   ├── tokenStore.ts
│   └── oneclickStore.ts
│
├── hooks/
│   ├── useIdentity.ts
│   ├── useAgentExecution.ts
│   ├── useGovernancePipeline.ts
│   ├── useTokenBudget.ts
│   ├── useOneClick.ts
│   ├── useAuditTrail.ts
│   └── useXR.ts
│
└── services/api/
    ├── identityApi.ts
    ├── agentApi.ts
    ├── governanceApi.ts
    ├── tokenApi.ts
    └── oneclickApi.ts
```

---

## ⚠️ RÈGLES CRITIQUES

1. **IDENTITY CONTEXT**: Toujours afficher l'identité courante
2. **GOVERNANCE VISIBLE**: Les checkpoints doivent être impossibles à manquer
3. **TOKEN AWARENESS**: L'utilisateur doit voir sa consommation
4. **KEYBOARD FIRST**: Cmd+K doit être le point d'entrée principal
5. **RESPONSIVE**: Tout doit fonctionner mobile et desktop
6. **ACCESSIBILITY**: ARIA labels, keyboard navigation

---

## 📦 DOCUMENTS DE RÉFÉRENCE INCLUS

- `LAYOUT_ENGINE_CHAPTER.md` — Design system et layout
- `WORKSPACE_ENGINE_CHAPTER.md` — Modes workspace
- `ONECLICK_ENGINE_CHAPTER.md` — 1-Click UX
- `MEETING_SYSTEM_CHAPTER.md` — Meeting UI
- Tous les composants V53 existants

---

## ✅ CRITÈRES DE SUCCÈS

| Critère | Validation |
|---------|------------|
| Identity UI | Création, switch, display fonctionnels |
| Agent Marketplace | Browse, hire, manage fonctionnels |
| Governance UI | Checkpoints, approvals, audit visibles |
| Token Display | Balance, usage, budgets visibles |
| 1-Click Bar | Cmd+K ouvre, suggestions, preview |
| DataSpace Clarity | Contexte toujours visible |
| XR Toggle | Basculement smooth |
| Tests | >80% coverage sur nouveaux composants |

---

**BON COURAGE AGENT BETA! 🎨**

*CLARTÉ > FEATURES*
