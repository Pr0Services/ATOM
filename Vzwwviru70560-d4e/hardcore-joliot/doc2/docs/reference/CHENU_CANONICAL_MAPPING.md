# CHE·NU V1 — CANONICAL MAPPING
## Spheres → Places → UI Components

**Version:** V1 FREEZE (2D + XR-READY)  
**Date:** 16 décembre 2025  
**Authority:** Complete Place Architecture  
**Status:** PRODUCTION SPECIFICATION

---

## 🎯 FUNDAMENTAL PRINCIPLE

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  A Sphere is NOT a menu.                      ║
║  A Sphere is a GOVERNED PLACE.                ║
║                                               ║
║  Each Sphere is composed of:                  ║
║  - Places (rooms / zones)                     ║
║  - Each Place maps to UI components           ║
║  - XR is only a different RENDERING           ║
║    of the same structure                      ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

## 🏛️ GLOBAL PLACE TYPES (Shared by All Spheres)

Every sphere may contain these canonical places:

```
1. Entrance Hall
   - Welcome/context reminder
   - Navigation hub
   - Nova presence

2. Bureau / Dashboard
   - Overview of sphere contents
   - Thread list
   - Quick actions

3. Workspace / Atelier
   - Active editing area
   - Document/table/canvas

4. Archives
   - Historical threads
   - Past decisions
   - Version history

5. Meeting Room
   - Collaboration space
   - Meeting notes
   - Shared decisions

6. Agent Backstage (Hidden by Default)
   - Staging area
   - Agent work in progress
   - Observable but not directly accessible
```

**Note:** Not all places must be active in MVP.

---

## 📋 UI COMPONENT LEGEND

```typescript
// Global Components
<TopBar />
<NovaChat />
<NotificationPanel />

// Navigation Components
<SphereSelector />
<BureauDashboard />
<SearchBar />

// Content Components
<ThreadList />
<ThreadRoom />
<VersionHistoryPanel />

// Workspace Components
<Workspace />
<UserWorkspaceEditor />
<AgentWorkspaceView />
<ComparisonView />

// Governance Components
<ApprovalModal />
<ExecutionStatus />
<BudgetIndicator />

// External Components
<BrowserView />
```

---

## 🏠 SPHERE 1 — PERSONAL

### Purpose
Personal thinking, planning, reflection, private work.

### Default Theme
Natural (warm, organic, calm)

---

### PLACE 1.1: Entrance Hall

**Purpose:** Welcome, context setting, Nova greeting

**UI Components:**
```tsx
<TopBar identity="personal" sphere="personal" />
<NovaChat context="personal_welcome" />
<QuickStats type="personal" />
```

**XR Projection:**
- Cozy entryway
- Wooden door
- Warm lighting
- Plants

---

### PLACE 1.2: Personal Bureau

**Purpose:** Overview of notes, tasks, threads

**UI Components:**
```tsx
<BureauDashboard sphere="personal">
  <TabGroup>
    <Tab name="Dashboard" />
    <Tab name="Notes" />
    <Tab name="Tasks" />
    <Tab name="Threads" />
  </TabGroup>
  
  <ThreadList 
    sphere="personal" 
    scope="sphere"
    editable={true}
  />
  
  <SearchBar 
    scope="sphere" 
    sphereType="personal"
  />
</BureauDashboard>
```

**XR Projection:**
- Personal office
- Desk with papers (notes)
- Wall calendar (tasks)
- Bookshelf (threads)

---

### PLACE 1.3: Personal Workspace

**Purpose:** Writing, tables, planning

**UI Components:**
```tsx
<Workspace type="user" sphere="personal">
  <UserWorkspaceEditor 
    mode="document" 
    autoSave={false}
  />
  
  <VersionHistoryPanel workspaceId={id} />
  
  <ActionBar>
    <Button onClick={handleSave}>
      Save (creates new version)
    </Button>
    <Button onClick={handleClose}>
      Close without saving
    </Button>
  </ActionBar>
</Workspace>
```

**XR Projection:**
- Writing desk (natural theme)
- Floating holographic editor (futuristic theme)
- Open book (astral theme)
- Clean table (neutral theme)

---

### PLACE 1.4: Archives

**Purpose:** Past threads, decisions, history

**UI Components:**
```tsx
<ArchiveView sphere="personal">
  <ThreadList 
    filter="archived"
    sphere="personal"
    readOnly={false}
  />
  
  <SearchBar scope="sphere" />
  
  <VersionHistory filter="old" />
</ArchiveView>
```

**XR Projection:**
- Library room
- Old bookshelves
- Dust motes in sunlight
- Historical documents

---

### PLACE 1.5: Agent Backstage (Hidden)

**Purpose:** Personal analysis drafts, agent work

**UI Components:**
```tsx
<AgentBackstage sphere="personal">
  <AgentWorkspaceView 
    executionId={id}
    readOnly={true}
  />
  
  {agentComplete && (
    <ComparisonView
      userVersionId={userV}
      agentDraftId={agentV}
    />
  )}
</AgentBackstage>
```

**XR Projection:**
- Behind-the-scenes room
- Glass wall (can observe)
- Agent working (visible as entity)
- Cannot enter directly

---

## 💼 SPHERE 2 — BUSINESS

### Purpose
Structured work, projects, decisions, accountability.

### Default Theme
Futuristic (professional, innovative, tech-forward)

---

### PLACE 2.1: Entrance Hall

**Purpose:** Business identity reminder, governance context

**UI Components:**
```tsx
<TopBar identity="business" sphere="business" />
<NovaChat context="business_context" />
<BusinessContextBanner>
  <CompanyName />
  <ActiveProjects count={5} />
  <BudgetIndicator />
</BusinessContextBanner>
```

**XR Projection:**
- Corporate lobby
- Glass walls
- Blue ambient lighting
- Holographic displays

---

### PLACE 2.2: Business Bureau

**Purpose:** Projects, threads, decisions, accountability

**UI Components:**
```tsx
<BureauDashboard sphere="business">
  <TabGroup>
    <Tab name="Dashboard" />
    <Tab name="Projects" />
    <Tab name="Threads" />
    <Tab name="Decisions" />
    <Tab name="Budget & Governance" />
  </TabGroup>
  
  <ProjectBoard />
  <ThreadList sphere="business" />
  <DecisionLog />
  <SearchBar scope="sphere" sphereType="business" />
</BureauDashboard>
```

**XR Projection:**
- Open office space
- Project boards floating
- Conference table
- Data visualization walls

---

### PLACE 2.3: Business Workspace

**Purpose:** Documents, reports, tables, professional content

**UI Components:**
```tsx
<Workspace type="user" sphere="business">
  <UserWorkspaceEditor 
    mode="document"
    templates={businessTemplates}
  />
  
  <VersionHistoryPanel />
  <BudgetTracker />
  
  <ActionBar>
    <Button onClick={handleSave}>Save</Button>
    <Button onClick={handleClose}>Close</Button>
  </ActionBar>
</Workspace>
```

**XR Projection:**
- Executive desk (holographic interface)
- Floating screens
- Real-time data feeds
- Professional atmosphere

---

### PLACE 2.4: Meeting Room

**Purpose:** Meeting notes, outcomes, collaborative decisions

**UI Components:**
```tsx
<MeetingRoom sphere="business">
  <Workspace type="collaborative">
    <MeetingEditor />
    <AttendeeList />
    <DecisionCapture />
  </Workspace>
  
  <ApprovalModal 
    context="meeting_decision"
    requiresSignoff={true}
  />
</MeetingRoom>
```

**XR Projection:**
- Conference room
- Large table
- Multiple participants (post-MVP)
- Shared screens

---

### PLACE 2.5: Archives

**Purpose:** Decisions, closed projects, audit trail

**UI Components:**
```tsx
<ArchiveView sphere="business">
  <DecisionLog filter="archived" />
  <ProjectList status="closed" />
  <AuditTrail sphere="business" />
  <SearchBar scope="sphere" />
</ArchiveView>
```

**XR Projection:**
- Records room
- Filing cabinets (organized)
- Secure vault atmosphere
- Compliance indicators

---

### PLACE 2.6: Agent Backstage

**Purpose:** Draft reports, simulations, analysis

**UI Components:**
```tsx
<AgentBackstage sphere="business">
  <AgentWorkspaceView executionId={id} />
  <SimulationResults />
  
  {agentComplete && (
    <ComparisonView 
      userVersionId={userV}
      agentDraftId={agentV}
    />
  )}
</AgentBackstage>
```

**XR Projection:**
- Analysis lab
- Data processing visible
- Holographic simulations
- Glass observation deck

---

## 👥 SPHERE 3 — COMMUNITY (POST-MVP)

### Purpose
Shared discussions, public threads, community engagement.

### Default Theme
Natural (warm, welcoming, organic)

---

### PLACES

#### 3.1: Agora (Public Square)

**UI Components:**
```tsx
<Agora sphere="community">
  <PublicThreadList />
  <DiscussionBoard />
  <EventCalendar />
</Agora>
```

---

#### 3.2: Discussion Corners

**UI Components:**
```tsx
<DiscussionSpace>
  <ThreadRoom threadId={id} visibility="public" />
  <ParticipantsList />
</DiscussionSpace>
```

---

#### 3.3: Announcement Board

**UI Components:**
```tsx
<AnnouncementBoard>
  <NoticeList type="community" />
  <EventFeed />
</AnnouncementBoard>
```

**Note:** Read-only inter-sphere references allowed

---

## 📱 SPHERE 4 — SOCIAL & MEDIA (POST-MVP)

### Purpose
Posts, events, media content management.

### Default Theme
Futuristic or Neutral (depending on use case)

---

### PLACES

#### 4.1: Media Feed

**UI Components:**
```tsx
<MediaFeed sphere="social">
  <ContentStream />
  <MediaViewer />
</MediaFeed>
```

---

#### 4.2: Post Editor

**UI Components:**
```tsx
<Workspace type="user" sphere="social">
  <PostEditor />
  <MediaUploader />
  <ScheduleManager />
</Workspace>
```

---

#### 4.3: External Platform Browser

**UI Components:**
```tsx
<BrowserView sphere="social">
  <MultiAccountBrowser />
  <ManualExtractTool />
</BrowserView>
```

**Governance:** Manual extraction only, no auto-scraping

---

## 🧪 SPHERE 5 — IA LABS (POST-MVP)

### Purpose
Experimentation, tools, models, agent configuration.

### Default Theme
Futuristic (experimental, tech-forward)

---

### PLACES

#### 5.1: Lab Dashboard

**UI Components:**
```tsx
<LabDashboard sphere="ia_labs">
  <ExperimentList />
  <ModelRegistry />
  <ToolLibrary />
</LabDashboard>
```

---

#### 5.2: Experiment Workspace

**UI Components:**
```tsx
<Workspace type="experiment" sphere="ia_labs">
  <CodeEditor />
  <ParameterTuner />
  <ResultsViewer />
  
  <AgentWorkspaceView 
    context="experimentation"
  />
</Workspace>
```

---

## 🤝 SPHERE 6 — MY TEAM (POST-MVP)

### Purpose
Agents, skills, tools management.

### Default Theme
Neutral (professional, organized)

---

### PLACES

#### 6.1: Team Overview

**UI Components:**
```tsx
<TeamDashboard sphere="my_team">
  <AgentList />
  <SkillRegistry />
  <ToolInventory />
</TeamDashboard>
```

---

#### 6.2: Agent Configuration

**UI Components:**
```tsx
<AgentConfig>
  <AgentSelector />
  <SkillAssignment />
  <BudgetAllocation />
  
  <AgentProposalCard
    agentId={id}
    capabilities={skills}
  />
</AgentConfig>
```

---

#### 6.3: Skill Library

**UI Components:**
```tsx
<SkillLibrary>
  <SkillList />
  <SkillDetails />
  <InstallManager />
</SkillLibrary>
```

---

## 🌐 GLOBAL / CROSS-SPHERE PLACES

### PLACE: Global Search Hall

**Purpose:** Profile-wide search (read-only index)

**UI Components:**
```tsx
<GlobalSearchHall>
  <SearchBar scope="profile" />
  
  <ResultsList>
    {results.map(result => (
      <ResultItem 
        key={result.id}
        sphere={result.sphere}
        readOnly={result.sphere !== currentSphere}
      >
        <SphereBadge sphere={result.sphere} />
        <ResultContent />
        
        {result.sphere !== currentSphere && (
          <Actions>
            <Button onClick={openReadOnly}>
              View (Read-Only)
            </Button>
            <Button onClick={switchContext}>
              Switch to {result.sphere}
            </Button>
          </Actions>
        )}
      </ResultItem>
    ))}
  </ResultsList>
</GlobalSearchHall>
```

**XR Projection:**
- Map room
- Results as markers in space
- Color-coded by sphere
- Can teleport to sphere

---

### PLACE: Browser Place

**Purpose:** External platforms (Facebook, Google, etc.)

**UI Components:**
```tsx
<BrowserPlace>
  <BrowserView 
    multiProfile={true}
    autoIngestion={false}
  >
    <AccountSwitcher />
    <NavigationControls />
    <ManualExtractButton />
  </BrowserView>
  
  <ExtractedContentPanel>
    <ContentPreview />
    <SaveToCHENUButton />
  </ExtractedContentPanel>
</BrowserPlace>
```

**Governance Rules:**
- No auto-ingestion
- Manual extract only
- Creates draft in workspace
- User must save explicitly

**XR Projection:**
- Window to external world
- Extract creates object in hand
- Must place in workspace

---

## 🥽 XR PROJECTION RULES

### In XR Mode:

```yaml
Each PLACE becomes:
  - A room with spatial layout
  - Theme-appropriate materials
  - Interactive objects
  - Ambient effects

Each THREAD becomes:
  - A folder OR
  - A constellation (astral theme) OR
  - A woven tapestry (natural theme) OR
  - A holographic stream (futuristic theme)

Each WORKSPACE becomes:
  - A table or surface
  - Editing tools (3D or holographic)
  - Version history as shelf

Each AGENT becomes:
  - A visible entity OR
  - An ambient presence OR
  - A light source
  - Observable in backstage

Transitions between places:
  - Walk through doors OR
  - Teleport OR
  - Spatial fade
```

**CRITICAL:** No logic changes. No governance changes. Only rendering changes.

---

## 🔒 VALIDATION RULES

### A Place is Valid CHE·NU Place When:

```
✅ Scope is always visible
✅ Read-only state is explained
✅ Permissions are clear
✅ No auto-apply of changes
✅ Context never hidden
✅ Sphere boundaries enforced
```

### A Place is INVALID When:

```
❌ Hides scope
❌ Merges spheres
❌ Auto-applies changes
❌ Unclear permissions
❌ Silent context switches
❌ Bypasses governance
```

---

## 📊 COMPLETE MAPPING TABLE

```
Sphere          | Places                        | Key Components
─────────────────────────────────────────────────────────────────
Personal 🏠     | Entrance Hall                 | NovaChat, QuickStats
                | Personal Bureau               | ThreadList, SearchBar
                | Personal Workspace            | UserWorkspaceEditor
                | Archives                      | VersionHistory
                | Agent Backstage               | AgentWorkspaceView

Business 💼     | Entrance Hall                 | BusinessContextBanner
                | Business Bureau               | ProjectBoard, DecisionLog
                | Business Workspace            | UserWorkspaceEditor
                | Meeting Room                  | MeetingEditor, ApprovalModal
                | Archives                      | AuditTrail
                | Agent Backstage               | SimulationResults

Community 👥    | Agora                         | PublicThreadList
(POST-MVP)      | Discussion Corners            | ThreadRoom
                | Announcement Board            | NoticeList

Social 📱       | Media Feed                    | ContentStream
(POST-MVP)      | Post Editor                   | PostEditor
                | External Browser              | BrowserView

IA Labs 🧪      | Lab Dashboard                 | ExperimentList
(POST-MVP)      | Experiment Workspace          | CodeEditor, AgentWorkspaceView

My Team 🤝      | Team Overview                 | AgentList, SkillRegistry
(POST-MVP)      | Agent Configuration           | AgentProposalCard
                | Skill Library                 | SkillList

GLOBAL          | Search Hall                   | SearchBar (profile scope)
                | Browser Place                 | BrowserView
```

---

## 🎯 IMPLEMENTATION CHECKLIST

### MVP (Personal + Business)

- [ ] Personal Entrance Hall
- [ ] Personal Bureau
- [ ] Personal Workspace
- [ ] Personal Archives
- [ ] Business Entrance Hall
- [ ] Business Bureau
- [ ] Business Workspace
- [ ] Business Meeting Room
- [ ] Business Archives
- [ ] Agent Backstage (both spheres)
- [ ] Global Search Hall
- [ ] Browser Place

### Post-MVP (6 Additional Spheres)

- [ ] Community places
- [ ] Social & Media places
- [ ] IA Labs places
- [ ] My Team places
- [ ] Government places (to be designed)
- [ ] Entertainment places (to be designed)

---

## 🔒 FINAL GOLDEN RULE

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  If a place:                                  ║
║  - hides scope                                ║
║  - merges spheres                             ║
║  - auto-applies changes                       ║
║                                               ║
║  IT IS NOT A VALID CHE·NU PLACE.              ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

**🏛️ CANONICAL MAPPING COMPLETE! EVERY SPHERE → PLACE → COMPONENT! 🚀**
