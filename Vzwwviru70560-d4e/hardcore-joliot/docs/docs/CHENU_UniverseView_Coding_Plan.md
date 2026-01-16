# CHE·NU — UniverseView Implementation Plan
## Complete Coding Roadmap

**Version:** 1.0  
**Date:** December 2024  
**Scope:** Full UniverseView + Agents + Meetings System

---

## 📁 ARCHITECTURE DES FICHIERS

```
src/
├── core/                          # 🧠 Logic Layer (Pure TypeScript)
│   ├── config/
│   │   ├── chenu.config.json      # Main configuration
│   │   └── config.types.ts        # Config types
│   │
│   ├── theme/
│   │   ├── themeEngine.ts         # Theme management
│   │   ├── theme.types.ts         # Theme types
│   │   └── themes/
│   │       ├── tree_nature.ts     # Default theme
│   │       ├── deep_ocean.ts
│   │       └── sacred_gold.ts
│   │
│   ├── agents/
│   │   ├── agent.types.ts         # Agent types & interfaces
│   │   ├── agentRegistry.ts       # Agent database
│   │   ├── agentBehavior.ts       # Agent AI logic
│   │   └── agentPermissions.ts    # Permission system
│   │
│   ├── spheres/
│   │   ├── sphere.types.ts        # Sphere types
│   │   ├── sphereRegistry.ts      # Sphere database
│   │   └── sphereLogic.ts         # Sphere operations
│   │
│   ├── meetings/
│   │   ├── meeting.types.ts       # Meeting types
│   │   ├── meeting.logic.ts       # Meeting flow logic
│   │   └── meetingPhases.ts       # Phase management
│   │
│   └── laws/
│       ├── laws.types.ts          # Law definitions
│       └── lawEnforcer.ts         # Law validation
│
├── ui/                            # 🎨 Presentation Layer (React)
│   ├── spheres/
│   │   ├── SphereCluster.tsx      # 3D sphere cluster
│   │   ├── SphereCard.tsx         # Individual sphere card
│   │   ├── SphereFocusView.tsx    # Focused sphere detail
│   │   ├── sphereCard.types.ts    # Card prop types
│   │   ├── sphereCard.styles.ts   # Card styling
│   │   └── sphereCluster.utils.ts # Position calculations
│   │
│   ├── agents/
│   │   ├── AgentOrbit.tsx         # Agent orbit display
│   │   ├── AgentAvatar.tsx        # Agent visual
│   │   ├── AgentPanel.tsx         # Agent control panel
│   │   ├── AgentTooltip.tsx       # Agent info tooltip
│   │   └── agentOrbit.utils.ts    # Orbit calculations
│   │
│   ├── meetings/
│   │   ├── MeetingRoom.tsx        # Main meeting interface
│   │   ├── MeetingHeader.tsx      # Meeting controls
│   │   ├── MeetingAgentRing.tsx   # Spatial agent display
│   │   ├── MeetingSummary.tsx     # Summary panel
│   │   └── MeetingReplay.tsx      # Event replay
│   │
│   ├── views/
│   │   ├── UniverseView.tsx       # Main universe view
│   │   ├── DashboardView.tsx      # Dashboard
│   │   └── SettingsView.tsx       # Settings
│   │
│   └── shared/
│       ├── Button.tsx             # Shared button
│       ├── Card.tsx               # Shared card
│       ├── Modal.tsx              # Modal component
│       └── IconSet.tsx            # Icon library
│
├── hooks/                         # 🪝 Custom Hooks
│   ├── useTheme.ts                # Theme hook
│   ├── useAgents.ts               # Agent management
│   ├── useSpheres.ts              # Sphere management
│   ├── useMeeting.ts              # Meeting state
│   └── useKeyboard.ts             # Keyboard shortcuts
│
├── store/                         # 📦 State Management
│   ├── index.ts                   # Store setup
│   ├── sphereSlice.ts             # Sphere state
│   ├── agentSlice.ts              # Agent state
│   └── meetingSlice.ts            # Meeting state
│
└── App.tsx                        # Root component
```

---

## 🔢 ORDRE D'IMPLÉMENTATION

### PHASE 1: CORE FOUNDATION (Week 1)
> Types, configuration, base logic

| Priority | File | Dependencies | Effort |
|----------|------|--------------|--------|
| 1.1 | `core/config/config.types.ts` | None | 1h |
| 1.2 | `core/config/chenu.config.json` | config.types | 2h |
| 1.3 | `core/theme/theme.types.ts` | None | 1h |
| 1.4 | `core/theme/themeEngine.ts` | theme.types | 2h |
| 1.5 | `core/theme/themes/*.ts` | themeEngine | 2h |
| 1.6 | `core/laws/laws.types.ts` | None | 1h |
| 1.7 | `core/laws/lawEnforcer.ts` | laws.types | 2h |

**Deliverable:** Configuration system + Theme engine + Laws framework

---

### PHASE 2: SPHERE SYSTEM (Week 2)
> Sphere types, registry, UI components

| Priority | File | Dependencies | Effort |
|----------|------|--------------|--------|
| 2.1 | `core/spheres/sphere.types.ts` | config.types | 1h |
| 2.2 | `core/spheres/sphereRegistry.ts` | sphere.types | 2h |
| 2.3 | `core/spheres/sphereLogic.ts` | sphereRegistry | 2h |
| 2.4 | `ui/spheres/sphereCard.types.ts` | sphere.types | 1h |
| 2.5 | `ui/spheres/sphereCard.styles.ts` | theme.types | 1h |
| 2.6 | `ui/spheres/sphereCluster.utils.ts` | None | 2h |
| 2.7 | `ui/spheres/SphereCard.tsx` | 2.4, 2.5 | 2h |
| 2.8 | `ui/spheres/SphereCluster.tsx` | SphereCard, utils | 3h |
| 2.9 | `ui/spheres/SphereFocusView.tsx` | SphereCard | 3h |

**Deliverable:** Complete sphere visualization system

---

### PHASE 3: AGENT SYSTEM (Week 3)
> Agent types, registry, behavior, UI

| Priority | File | Dependencies | Effort |
|----------|------|--------------|--------|
| 3.1 | `core/agents/agent.types.ts` | laws.types | 2h |
| 3.2 | `core/agents/agentPermissions.ts` | agent.types, laws | 2h |
| 3.3 | `core/agents/agentRegistry.ts` | agent.types | 3h |
| 3.4 | `core/agents/agentBehavior.ts` | agentRegistry | 3h |
| 3.5 | `ui/agents/agentOrbit.utils.ts` | agent.types | 1h |
| 3.6 | `ui/agents/AgentAvatar.tsx` | agent.types, theme | 2h |
| 3.7 | `ui/agents/AgentTooltip.tsx` | agent.types | 1h |
| 3.8 | `ui/agents/AgentPanel.tsx` | AgentAvatar | 3h |
| 3.9 | `ui/agents/AgentOrbit.tsx` | AgentAvatar, utils | 2h |

**Deliverable:** Complete agent system with 168+ agents

---

### PHASE 4: MEETING SYSTEM (Week 4)
> Meeting types, logic, phases, UI

| Priority | File | Dependencies | Effort |
|----------|------|--------------|--------|
| 4.1 | `core/meetings/meeting.types.ts` | agent.types | 2h |
| 4.2 | `core/meetings/meetingPhases.ts` | meeting.types | 2h |
| 4.3 | `core/meetings/meeting.logic.ts` | meetingPhases | 3h |
| 4.4 | `ui/meetings/MeetingHeader.tsx` | meeting.types | 1h |
| 4.5 | `ui/meetings/MeetingAgentRing.tsx` | AgentAvatar | 2h |
| 4.6 | `ui/meetings/MeetingSummary.tsx` | meeting.logic | 2h |
| 4.7 | `ui/meetings/MeetingReplay.tsx` | meeting.types | 2h |
| 4.8 | `ui/meetings/MeetingRoom.tsx` | 4.4-4.7 | 4h |

**Deliverable:** Complete meeting system with phases

---

### PHASE 5: INTEGRATION (Week 5)
> Views, hooks, state, final assembly

| Priority | File | Dependencies | Effort |
|----------|------|--------------|--------|
| 5.1 | `hooks/useTheme.ts` | themeEngine | 1h |
| 5.2 | `hooks/useSpheres.ts` | sphereLogic | 1h |
| 5.3 | `hooks/useAgents.ts` | agentBehavior | 1h |
| 5.4 | `hooks/useMeeting.ts` | meeting.logic | 2h |
| 5.5 | `hooks/useKeyboard.ts` | None | 1h |
| 5.6 | `store/sphereSlice.ts` | sphere.types | 1h |
| 5.7 | `store/agentSlice.ts` | agent.types | 1h |
| 5.8 | `store/meetingSlice.ts` | meeting.types | 1h |
| 5.9 | `ui/views/UniverseView.tsx` | All components | 3h |
| 5.10 | `App.tsx` | UniverseView | 1h |

**Deliverable:** Fully integrated UniverseView

---

## 📋 FICHIERS DÉTAILLÉS À CRÉER

### 1. `core/config/config.types.ts`

```typescript
// CHE·NU Configuration Types

export interface ChenuConfig {
  version: string;
  trunk: TrunkConfig;
  spheres: SphereConfig[];
  agents: AgentConfig[];
  laws: LawConfig[];
  themes: ThemeRef[];
}

export interface TrunkConfig {
  name: string;
  laws: string[];
  memory: MemoryConfig;
  orchestrator: OrchestratorConfig;
}

export interface SphereConfig {
  id: string;
  name: string;
  icon: string;
  color: string;
  type: SphereType;
  agents: string[];
  tools: string[];
  permissions: string[];
}

export type SphereType = 
  | "personal" 
  | "business" 
  | "creative" 
  | "scholar" 
  | "social" 
  | "institutions" 
  | "methodology" 
  | "xr";

export interface MemoryConfig {
  shortTerm: { ttl: number };
  longTerm: { encrypted: boolean };
  audit: { retention: string };
}

export interface OrchestratorConfig {
  id: string;
  name: string;
  level: 0;
  capabilities: string[];
}

export interface AgentConfig {
  id: string;
  name: string;
  level: AgentLevel;
  sphere: string;
  role: string;
  permissions: string[];
}

export type AgentLevel = 0 | 1 | 2 | 3 | 4 | 5;

export interface LawConfig {
  id: string;
  category: LawCategory;
  text: string;
  enforcement: string;
}

export type LawCategory = 
  | "trunk" 
  | "sphere" 
  | "agent" 
  | "decision" 
  | "memory" 
  | "extension";

export interface ThemeRef {
  id: string;
  name: string;
  path: string;
}
```

---

### 2. `core/agents/agent.types.ts`

```typescript
// CHE·NU Agent Types

export interface Agent {
  id: string;
  name: string;
  level: AgentLevel;
  sphere: string;
  role: string;
  avatar: AgentAvatar;
  status: AgentStatus;
  capabilities: string[];
  permissions: AgentPermission[];
  influenceLevel: number; // 0-1
  currentTask?: AgentTask;
  memory: AgentMemory;
}

export type AgentLevel = 0 | 1 | 2 | 3 | 4 | 5;

export type AgentStatus = 
  | "idle" 
  | "thinking" 
  | "working" 
  | "waiting" 
  | "blocked" 
  | "error";

export interface AgentAvatar {
  style: AvatarStyle;
  icon: string;
  color: string;
  animation?: string;
}

export type AvatarStyle = 
  | "orb" 
  | "geometric" 
  | "humanoid" 
  | "iconic";

export interface AgentPermission {
  resource: string;
  actions: ("read" | "write" | "execute" | "delete")[];
  scope: "self" | "sphere" | "global";
  expires?: Date;
}

export interface AgentTask {
  id: string;
  type: string;
  status: "pending" | "running" | "completed" | "failed";
  progress: number;
  startedAt: Date;
  completedAt?: Date;
}

export interface AgentMemory {
  shortTerm: Record<string, any>;
  context: string[];
  lastInteraction?: Date;
}

// Agent hierarchy definitions
export const AGENT_LEVELS: Record<AgentLevel, AgentLevelMeta> = {
  0: { name: "Orchestrator", color: "#D8B26A", maxCount: 1 },
  1: { name: "Director", color: "#8B2942", maxCount: 4 },
  2: { name: "Manager", color: "#1E3A5F", maxCount: 11 },
  3: { name: "Analyst", color: "#2D5A3D", maxCount: 35 },
  4: { name: "Executor", color: "#5D3A6E", maxCount: 85 },
  5: { name: "Observer", color: "#2A7B7B", maxCount: 32 },
};

export interface AgentLevelMeta {
  name: string;
  color: string;
  maxCount: number;
}

// Agent actions for meetings
export interface AgentAction {
  type: "suggest" | "analyze" | "summarize" | "alert" | "query";
  payload: any;
  confidence: number;
  requiresValidation: boolean;
}
```

---

### 3. `core/meetings/meeting.types.ts`

```typescript
// CHE·NU Meeting Types

export interface Meeting {
  id: string;
  title: string;
  objective: string;
  type: MeetingType;
  phase: MeetingPhase;
  status: MeetingStatus;
  agents: MeetingAgent[];
  participants: Participant[];
  events: MeetingEvent[];
  decisions: Decision[];
  summary?: string;
  createdAt: Date;
  startedAt?: Date;
  endedAt?: Date;
}

export type MeetingType = 
  | "decision" 
  | "brainstorm" 
  | "review" 
  | "standup" 
  | "planning";

export type MeetingPhase = 
  | "setup" 
  | "opening" 
  | "discussion" 
  | "proposals" 
  | "voting" 
  | "decision" 
  | "closing" 
  | "completed";

export type MeetingStatus = 
  | "scheduled" 
  | "active" 
  | "paused" 
  | "completed" 
  | "cancelled";

export interface MeetingAgent {
  id: string;
  name: string;
  role: string;
  sphere: string;
  influenceLevel: number;
  status: "active" | "observing" | "muted";
  contributions: number;
  avatar: {
    style: string;
    icon: string;
    color: string;
  };
}

export interface Participant {
  id: string;
  name: string;
  role: "host" | "participant" | "observer";
  isHuman: boolean;
  joinedAt: Date;
}

export interface MeetingEvent {
  id: string;
  type: MeetingEventType;
  actorId: string;
  payload: any;
  phase: MeetingPhase;
  timestamp: Date;
}

export type MeetingEventType = 
  | "phase_change" 
  | "agent_suggestion" 
  | "human_decision" 
  | "vote_cast" 
  | "action_created" 
  | "summary_generated";

export interface Decision {
  id: string;
  question: string;
  options: DecisionOption[];
  selectedOption?: string;
  decidedBy: string;
  decidedAt?: Date;
  rationale?: string;
}

export interface DecisionOption {
  id: string;
  text: string;
  proposedBy: string;
  votes: number;
  confidence?: number;
}

// Context for agent behavior in meetings
export interface MeetingContext {
  phase: MeetingPhase;
  hasHumanDecisionMaker: boolean;
  isCriticalDecision: boolean;
  activeAgents: string[];
  pendingDecisions: number;
}
```

---

### 4. `core/meetings/meeting.logic.ts`

```typescript
// CHE·NU Meeting Logic

import { 
  Meeting, 
  MeetingPhase, 
  MeetingEvent, 
  MeetingEventType,
  Decision 
} from "./meeting.types";

const PHASE_ORDER: MeetingPhase[] = [
  "setup",
  "opening",
  "discussion",
  "proposals",
  "voting",
  "decision",
  "closing",
  "completed"
];

export function advanceMeetingPhase(meeting: Meeting): Meeting {
  const currentIndex = PHASE_ORDER.indexOf(meeting.phase);
  const nextIndex = Math.min(currentIndex + 1, PHASE_ORDER.length - 1);
  const nextPhase = PHASE_ORDER[nextIndex];
  
  return {
    ...meeting,
    phase: nextPhase,
    events: [
      ...meeting.events,
      createEvent("phase_change", "system", { 
        from: meeting.phase, 
        to: nextPhase 
      }, nextPhase)
    ]
  };
}

export function logMeetingEvent(
  meeting: Meeting, 
  event: Omit<MeetingEvent, "id" | "timestamp">
): Meeting {
  return {
    ...meeting,
    events: [
      ...meeting.events,
      {
        ...event,
        id: `evt_${Date.now()}`,
        timestamp: new Date()
      }
    ]
  };
}

export function createEvent(
  type: MeetingEventType,
  actorId: string,
  payload: any,
  phase: MeetingPhase
): MeetingEvent {
  return {
    id: `evt_${Date.now()}`,
    type,
    actorId,
    payload,
    phase,
    timestamp: new Date()
  };
}

export function buildMeetingSummary(meeting: Meeting): string {
  const lines: string[] = [
    `📋 MEETING: ${meeting.title}`,
    `🎯 Objective: ${meeting.objective}`,
    `📊 Phase: ${meeting.phase}`,
    `👥 Agents: ${meeting.agents.length}`,
    "",
    "📝 EVENTS:",
  ];
  
  meeting.events.slice(-10).forEach(event => {
    const time = event.timestamp.toLocaleTimeString();
    lines.push(`  [${time}] ${event.type} by ${event.actorId}`);
  });
  
  if (meeting.decisions.length > 0) {
    lines.push("", "✅ DECISIONS:");
    meeting.decisions.forEach(d => {
      const status = d.selectedOption ? "✓" : "○";
      lines.push(`  ${status} ${d.question}`);
    });
  }
  
  return lines.join("\n");
}

export function getAgentSuggestion(
  agentId: string, 
  meeting: Meeting
): string {
  // Simulate agent suggestion based on context
  const agent = meeting.agents.find(a => a.id === agentId);
  if (!agent) return "No agent found";
  
  const suggestions: Record<MeetingPhase, string> = {
    setup: `Je suis prêt pour la réunion "${meeting.title}"`,
    opening: "Je suggère de commencer par définir les objectifs clés",
    discussion: "Basé sur l'analyse, voici les points importants...",
    proposals: "Je propose la solution suivante...",
    voting: "Mon évaluation des options est...",
    decision: "Selon les données, la meilleure option est...",
    closing: "Actions à retenir de cette réunion...",
    completed: "Résumé final disponible"
  };
  
  return `[${agent.name}] ${suggestions[meeting.phase]}`;
}

export function createMeeting(
  title: string,
  objective: string,
  type: Meeting["type"],
  agents: Meeting["agents"]
): Meeting {
  return {
    id: `mtg_${Date.now()}`,
    title,
    objective,
    type,
    phase: "setup",
    status: "scheduled",
    agents,
    participants: [],
    events: [],
    decisions: [],
    createdAt: new Date()
  };
}
```

---

### 5. `ui/agents/AgentAvatar.tsx`

```tsx
// CHE·NU Agent Avatar Component

import React from "react";
import { Agent, AGENT_LEVELS } from "@/core/agents/agent.types";

interface AgentAvatarProps {
  agent: Agent;
  size?: "sm" | "md" | "lg";
  showStatus?: boolean;
  onClick?: () => void;
}

const SIZES = {
  sm: { width: 32, height: 32, fontSize: 14 },
  md: { width: 48, height: 48, fontSize: 20 },
  lg: { width: 64, height: 64, fontSize: 28 }
};

export const AgentAvatar: React.FC<AgentAvatarProps> = ({
  agent,
  size = "md",
  showStatus = true,
  onClick
}) => {
  const dimensions = SIZES[size];
  const levelMeta = AGENT_LEVELS[agent.level];
  
  const statusColors: Record<string, string> = {
    idle: "#666",
    thinking: "#ffd54f",
    working: "#4caf50",
    waiting: "#2196f3",
    blocked: "#f44336",
    error: "#f44336"
  };
  
  return (
    <div
      onClick={onClick}
      style={{
        position: "relative",
        width: dimensions.width,
        height: dimensions.height,
        borderRadius: agent.avatar.style === "orb" ? "50%" : "8px",
        background: agent.avatar.color || levelMeta.color,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        cursor: onClick ? "pointer" : "default",
        boxShadow: `0 2px 8px ${agent.avatar.color || levelMeta.color}40`,
        transition: "transform 0.2s ease, box-shadow 0.2s ease"
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "scale(1.1)";
        e.currentTarget.style.boxShadow = `0 4px 16px ${agent.avatar.color || levelMeta.color}60`;
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "scale(1)";
        e.currentTarget.style.boxShadow = `0 2px 8px ${agent.avatar.color || levelMeta.color}40`;
      }}
    >
      {/* Icon */}
      <span style={{ fontSize: dimensions.fontSize }}>
        {agent.avatar.icon}
      </span>
      
      {/* Status indicator */}
      {showStatus && (
        <div
          style={{
            position: "absolute",
            bottom: -2,
            right: -2,
            width: 10,
            height: 10,
            borderRadius: "50%",
            background: statusColors[agent.status],
            border: "2px solid #1a1a1a"
          }}
        />
      )}
      
      {/* Level badge */}
      <div
        style={{
          position: "absolute",
          top: -4,
          left: -4,
          width: 16,
          height: 16,
          borderRadius: "50%",
          background: levelMeta.color,
          border: "2px solid #1a1a1a",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 8,
          fontWeight: "bold",
          color: "#fff"
        }}
      >
        L{agent.level}
      </div>
    </div>
  );
};
```

---

### 6. `ui/agents/AgentPanel.tsx`

```tsx
// CHE·NU Agent Panel Component

import React, { useState } from "react";
import { Agent } from "@/core/agents/agent.types";
import { MeetingContext } from "@/core/meetings/meeting.types";
import { AgentAvatar } from "./AgentAvatar";

interface AgentPanelProps {
  agent: Agent;
  context: MeetingContext;
  onAskForSummary: (agentId: string) => void;
  onAskForSuggestion: (agentId: string) => void;
}

export const AgentPanel: React.FC<AgentPanelProps> = ({
  agent,
  context,
  onAskForSummary,
  onAskForSuggestion
}) => {
  const [expanded, setExpanded] = useState(false);
  
  const canAct = context.hasHumanDecisionMaker || !context.isCriticalDecision;
  
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.05)",
        borderRadius: 8,
        padding: 12,
        marginBottom: 8,
        border: expanded ? "1px solid rgba(255,255,255,0.2)" : "1px solid transparent",
        transition: "all 0.2s ease"
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          cursor: "pointer"
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <AgentAvatar agent={agent} size="sm" />
        
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: "bold", fontSize: 13 }}>
            {agent.name}
          </div>
          <div style={{ fontSize: 11, opacity: 0.6 }}>
            {agent.role} • {agent.sphere}
          </div>
        </div>
        
        <div style={{ fontSize: 11, opacity: 0.5 }}>
          {expanded ? "▼" : "▶"}
        </div>
      </div>
      
      {/* Expanded content */}
      {expanded && (
        <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid rgba(255,255,255,0.1)" }}>
          {/* Capabilities */}
          <div style={{ fontSize: 11, marginBottom: 8 }}>
            <strong>Capabilities:</strong>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginTop: 4 }}>
              {agent.capabilities.slice(0, 5).map((cap, i) => (
                <span
                  key={i}
                  style={{
                    background: "rgba(255,255,255,0.1)",
                    padding: "2px 6px",
                    borderRadius: 4,
                    fontSize: 10
                  }}
                >
                  {cap}
                </span>
              ))}
            </div>
          </div>
          
          {/* Actions */}
          <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
            <button
              onClick={() => onAskForSummary(agent.id)}
              disabled={!canAct}
              style={{
                flex: 1,
                padding: "6px 12px",
                background: canAct ? "#2D5A3D" : "#333",
                border: "none",
                borderRadius: 4,
                color: "#fff",
                fontSize: 11,
                cursor: canAct ? "pointer" : "not-allowed"
              }}
            >
              📋 Résumé
            </button>
            
            <button
              onClick={() => onAskForSuggestion(agent.id)}
              disabled={!canAct}
              style={{
                flex: 1,
                padding: "6px 12px",
                background: canAct ? "#1E3A5F" : "#333",
                border: "none",
                borderRadius: 4,
                color: "#fff",
                fontSize: 11,
                cursor: canAct ? "pointer" : "not-allowed"
              }}
            >
              💡 Suggestion
            </button>
          </div>
          
          {/* Status */}
          <div style={{ 
            marginTop: 8, 
            fontSize: 10, 
            opacity: 0.5,
            textAlign: "center" 
          }}>
            Status: {agent.status} • Influence: {(agent.influenceLevel * 100).toFixed(0)}%
          </div>
        </div>
      )}
    </div>
  );
};
```

---

### 7. `ui/spheres/sphereCluster.utils.ts`

```typescript
// CHE·NU Sphere Cluster Utilities

import { SphereData } from "./sphereCard.types";
import { ChenuConfig, SphereConfig } from "@/core/config/config.types";

export interface Position {
  x: number;
  y: number;
}

// Limit visible spheres to prevent overcrowding
export function limitSpheres(spheres: SphereData[], max: number = 8): SphereData[] {
  return spheres.slice(0, max);
}

// Compute orbital positions for spheres
export function computePositions(count: number, radius: number = 200): Position[] {
  const positions: Position[] = [];
  
  for (let i = 0; i < count; i++) {
    const angle = (Math.PI * 2 * i) / count - Math.PI / 2;
    positions.push({
      x: Math.cos(angle) * radius,
      y: Math.sin(angle) * radius
    });
  }
  
  return positions;
}

// Build root spheres from config
export function buildRootSpheres(config: ChenuConfig): SphereData[] {
  return config.spheres.map((sphere, index) => ({
    id: sphere.id,
    name: sphere.name,
    type: sphere.type,
    icon: sphere.icon,
    color: sphere.color,
    dimensionClass: getDimensionClass(index),
    normalizedDimension: (index + 1) / config.spheres.length,
    indicators: [
      { label: "Agents", value: sphere.agents.length.toString() },
      { label: "Tools", value: sphere.tools.length.toString() }
    ]
  }));
}

// Get dimension class based on index/importance
export function getDimensionClass(index: number): "XS" | "S" | "M" | "L" | "XL" {
  const classes: ("XS" | "S" | "M" | "L" | "XL")[] = ["XL", "L", "M", "S", "XS"];
  return classes[Math.min(index, classes.length - 1)];
}

// Compute agent position in orbit
export function computeAgentPosition(
  agent: { influenceLevel: number },
  index: number,
  total: number
): Position {
  const baseRadius = 280;
  const radius = baseRadius + agent.influenceLevel * 60;
  const angle = (Math.PI * 2 * index) / total;
  
  return {
    x: Math.cos(angle) * radius,
    y: Math.sin(angle) * radius
  };
}
```

---

### 8. `ui/spheres/sphereCard.styles.ts`

```typescript
// CHE·NU Sphere Card Styles

import { CSSProperties } from "react";

type DimensionClass = "XS" | "S" | "M" | "L" | "XL";

const DIMENSION_SIZES: Record<DimensionClass, { width: number; height: number; padding: number }> = {
  XS: { width: 80, height: 80, padding: 8 },
  S: { width: 100, height: 100, padding: 10 },
  M: { width: 130, height: 130, padding: 12 },
  L: { width: 160, height: 160, padding: 16 },
  XL: { width: 200, height: 200, padding: 20 }
};

export function getCardStyle(
  dimensionClass: DimensionClass,
  normalizedDimension: number
): CSSProperties {
  const size = DIMENSION_SIZES[dimensionClass];
  const opacity = 0.6 + normalizedDimension * 0.4;
  
  return {
    width: size.width,
    height: size.height,
    padding: size.padding,
    borderRadius: "50%",
    background: `rgba(30, 58, 95, ${opacity})`,
    border: "2px solid rgba(216, 178, 106, 0.4)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    transition: "all 0.3s ease",
    boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
    textAlign: "center",
    color: "#fff"
  };
}

export function getHoverStyle(): CSSProperties {
  return {
    transform: "scale(1.08)",
    boxShadow: "0 8px 32px rgba(216, 178, 106, 0.4)",
    borderColor: "rgba(216, 178, 106, 0.8)"
  };
}
```

---

### 9. `core/theme/themeEngine.ts`

```typescript
// CHE·NU Theme Engine

import { Theme, ThemeColors, ThemeTypography } from "./theme.types";

const themes: Record<string, Theme> = {
  tree_nature: {
    id: "tree_nature",
    name: "Tree Nature",
    colors: {
      background: "#0a0e14",
      surface: "#1a1f28",
      primary: "#D8B26A",
      secondary: "#2D5A3D",
      accent: "#8B2942",
      text: "#F5F0E8",
      textMuted: "#888888",
      border: "rgba(216, 178, 106, 0.2)",
      success: "#4caf50",
      warning: "#ffd54f",
      error: "#f44336"
    },
    typography: {
      fontFamily: "'Inter', -apple-system, sans-serif",
      fontSizeBase: 14,
      fontSizeSm: 12,
      fontSizeLg: 16,
      fontSizeXl: 20,
      fontWeightNormal: 400,
      fontWeightBold: 600
    },
    spacing: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32
    },
    borderRadius: {
      sm: 4,
      md: 8,
      lg: 16,
      full: 9999
    }
  },
  
  deep_ocean: {
    id: "deep_ocean",
    name: "Deep Ocean",
    colors: {
      background: "#0d1b2a",
      surface: "#1b263b",
      primary: "#00b4d8",
      secondary: "#0077b6",
      accent: "#90e0ef",
      text: "#caf0f8",
      textMuted: "#778da9",
      border: "rgba(0, 180, 216, 0.2)",
      success: "#4caf50",
      warning: "#ffd54f",
      error: "#f44336"
    },
    typography: {
      fontFamily: "'Inter', -apple-system, sans-serif",
      fontSizeBase: 14,
      fontSizeSm: 12,
      fontSizeLg: 16,
      fontSizeXl: 20,
      fontWeightNormal: 400,
      fontWeightBold: 600
    },
    spacing: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32
    },
    borderRadius: {
      sm: 4,
      md: 8,
      lg: 16,
      full: 9999
    }
  },
  
  sacred_gold: {
    id: "sacred_gold",
    name: "Sacred Gold",
    colors: {
      background: "#1a1a1a",
      surface: "#2a2a2a",
      primary: "#D8B26A",
      secondary: "#8B2942",
      accent: "#F5F0E8",
      text: "#F5F0E8",
      textMuted: "#888888",
      border: "rgba(216, 178, 106, 0.3)",
      success: "#4caf50",
      warning: "#ffd54f",
      error: "#f44336"
    },
    typography: {
      fontFamily: "'Inter', -apple-system, sans-serif",
      fontSizeBase: 14,
      fontSizeSm: 12,
      fontSizeLg: 16,
      fontSizeXl: 20,
      fontWeightNormal: 400,
      fontWeightBold: 600
    },
    spacing: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32
    },
    borderRadius: {
      sm: 4,
      md: 8,
      lg: 16,
      full: 9999
    }
  }
};

export function getTheme(themeId: string): Theme {
  return themes[themeId] || themes.tree_nature;
}

export function getAllThemes(): Theme[] {
  return Object.values(themes);
}

export function getThemeIds(): string[] {
  return Object.keys(themes);
}
```

---

## 📊 ESTIMATION TOTALE

| Phase | Durée | Fichiers | Effort |
|-------|-------|----------|--------|
| Phase 1: Core Foundation | Week 1 | 7 files | 11h |
| Phase 2: Sphere System | Week 2 | 9 files | 17h |
| Phase 3: Agent System | Week 3 | 9 files | 19h |
| Phase 4: Meeting System | Week 4 | 8 files | 18h |
| Phase 5: Integration | Week 5 | 10 files | 13h |
| **TOTAL** | **5 weeks** | **43 files** | **78h** |

---

## 🔗 DÉPENDANCES NPM

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "zustand": "^4.4.0",
    "framer-motion": "^10.16.0",
    "lucide-react": "^0.294.0",
    "@radix-ui/react-tooltip": "^1.0.7",
    "@radix-ui/react-dialog": "^1.0.5"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/react": "^18.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0"
  }
}
```

---

## ✅ PROCHAINE ÉTAPE

**Option A:** Générer tous les fichiers Phase 1 maintenant
**Option B:** Générer la structure complète des dossiers
**Option C:** Créer un repo starter avec tous les fichiers
**Option D:** Générer fichier par fichier selon tes priorités

---

*CHE·NU — Governed Intelligence Operating System*
*Version 1.0 — December 2024*
