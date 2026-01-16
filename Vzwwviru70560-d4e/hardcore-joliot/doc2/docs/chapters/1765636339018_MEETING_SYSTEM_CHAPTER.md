# MEETING SYSTEM — COMPLETE SPECIFICATION

## Chapter 71: Meeting System Overview

### Introduction

The CHE·NU Meeting System represents a fundamental reimagining of collaborative gatherings. In CHE·NU's philosophy, meetings are not mere video calls or calendar events—they are **knowledge events** that generate structured, actionable, and replayable artifacts. Every meeting becomes a permanent contribution to the organizational knowledge base, automatically producing notes, decisions, tasks, and DataSpace updates.

### Purpose and Vision

Traditional meeting tools focus on connection—bringing people together in real-time. CHE·NU's Meeting System focuses on **outcomes**—ensuring that every collaborative session produces tangible results that integrate seamlessly into ongoing workflows. The system operates on the principle that time spent in meetings should compound, not evaporate.

### Core Capabilities

The Meeting System supports multiple collaboration modalities:

**Real-Time Meetings**: Synchronous gatherings where participants engage simultaneously, whether in the same physical location, connected virtually, or immersed in XR environments.

**Asynchronous Meetings**: Structured collaborative sessions where participants contribute at different times, with AI agents maintaining continuity, synthesizing inputs, and driving toward decisions.

**Hybrid Meetings**: Combinations of real-time and asynchronous elements, allowing for initial synchronous discussion followed by offline deliberation and subsequent reconvening.

**Cross-Domain Collaboration**: Meetings that span multiple CHE·NU domains, with relevant specialist agents from each domain contributing expertise and ensuring domain-specific requirements are addressed.

**XR Spatial Meetings**: Immersive gatherings in extended reality environments where participants can manipulate 3D objects, explore spatial data, and collaborate in ways impossible in traditional formats.

### Meeting Outputs

Every CHE·NU meeting automatically generates:

- **Structured Notes**: Organized by topic, speaker, and chronology
- **Tasks**: Actionable items extracted from discussion with assignees and deadlines
- **Decisions**: Formally captured choices with context and rationale
- **Documents**: Meeting-generated artifacts filed appropriately
- **DataSpace Updates**: Automatic synchronization with relevant DataSpaces
- **Timeline Artifacts**: Chronological record for historical reference
- **Replayable Knowledge**: Indexed, searchable meeting content for future retrieval

---

## Chapter 72: Meeting as DataSpace

### Architectural Foundation

In CHE·NU's architecture, every meeting exists as a dedicated DataSpace. This architectural decision ensures that meeting content is not ephemeral but becomes a permanent, structured, and queryable part of the organizational knowledge graph.

### Meeting DataSpace Structure

```
Meeting DataSpace: [Meeting Title]
├── 📋 Agenda/
│   ├── planned_agenda.md
│   ├── actual_flow.md
│   └── time_allocations.json
├── 👥 Participants/
│   ├── attendees.json
│   ├── identity_contexts/
│   │   └── [participant_identity_snapshots]
│   ├── roles_assigned.json
│   └── contribution_log/
├── 🌐 Context/
│   ├── sphere_context.json
│   ├── domain_context.json
│   ├── project_linkage.json
│   ├── related_dataspaces/
│   └── previous_meetings/
├── 📝 Notes/
│   ├── raw_transcript.md
│   ├── structured_notes.md
│   ├── topic_summaries/
│   └── speaker_contributions/
├── ✅ Tasks/
│   ├── extracted_tasks.json
│   ├── assignments.json
│   ├── deadlines.json
│   └── task_status/
├── 🎯 Decisions/
│   ├── decisions_log.json
│   ├── decision_context/
│   ├── approvals/
│   └── rationale/
├── 📎 Attachments/
│   ├── shared_files/
│   ├── screen_captures/
│   ├── presented_documents/
│   └── generated_artifacts/
├── 🎬 Recordings/
│   ├── audio_recording.m4a
│   ├── video_recording.mp4
│   ├── transcript_timecoded.vtt
│   └── xr_session_capture/
├── 🥽 XR_Objects/
│   ├── spatial_annotations/
│   ├── 3d_models_used/
│   ├── scene_snapshots/
│   └── manipulation_log/
├── 🔄 Follow-Up/
│   ├── triggered_workflows/
│   ├── scheduled_followups/
│   ├── pending_actions/
│   └── completion_tracking/
├── 🤖 Agent_Contributions/
│   ├── context_provided/
│   ├── suggestions_made/
│   ├── analyses_performed/
│   └── action_log/
└── 🔐 Governance/
    ├── permissions.json
    ├── consent_records/
    ├── audit_trail/
    └── retention_policy.json
```

### DataSpace Governance

Meeting DataSpaces inherit CHE·NU's governance framework:

**Permission Inheritance**: Meeting permissions derive from the sphere/domain context but can be restricted further based on meeting sensitivity.

**Consent Management**: Recording requires explicit participant consent, tracked in the governance folder.

**Audit Trail**: Every action within the meeting DataSpace is logged for accountability.

**Retention Policies**: Meetings follow configurable retention rules based on organizational requirements.

---

## Chapter 73: Thread and Context Injection

### Context Continuity

Meetings don't exist in isolation—they are nodes in ongoing collaborative threads. CHE·NU's Thread Engine ensures that every meeting connects to its broader context, enabling participants to understand history and agents to provide relevant support.

### Thread Integration

Every meeting automatically:

**Links to Existing Threads**: When a meeting relates to an ongoing project or discussion, it connects to the relevant thread, inheriting context and contributing outputs back to the thread.

**Inherits Sphere and Domain**: The meeting adopts the sphere (Personal, Enterprise, Creative, etc.) and domain (Construction, Finance, Architecture, Immobilier, etc.) context, activating appropriate specialist agents.

**Syncs with Related DataSpaces**: Documents, decisions, and artifacts from related DataSpaces are accessible within the meeting, and meeting outputs flow back to those DataSpaces.

### Agent Context Capabilities

Before and during meetings, agents can:

**Fetch Relevant Context**: Automatically retrieve documents, previous decisions, and historical information related to the meeting agenda.

**Provide Summaries**: Generate pre-meeting briefings that bring participants up to speed on relevant history.

**Highlight Previous Decisions**: Surface past commitments that may affect current discussions.

**Validate Continuity**: Alert participants when proposed actions conflict with previous decisions or ongoing workflows.

### Pre-Meeting Preparation

When a meeting is scheduled, CHE·NU's Meeting Engine initiates preparation:

1. **Context Analysis**: Determines relevant sphere, domain, and project context
2. **Material Assembly**: Gathers related documents, previous meeting notes, and pending items
3. **Agent Briefing**: Prepares relevant agents with meeting context
4. **Participant Briefing**: Optionally generates pre-meeting summaries for participants
5. **Agenda Enhancement**: Suggests agenda items based on pending tasks and unresolved issues

---

## Chapter 74: Meeting Types

### A. Standard Meeting

The foundational meeting type for general collaboration.

**Characteristics**:
- Structured agenda with time allocations
- Real-time note capture
- Decision identification and documentation
- Task extraction and assignment
- Shared workspace for collaborative editing

**Output Package**:
- Meeting summary (executive and detailed)
- Decision log with rationale
- Task list with owners and deadlines
- Updated DataSpaces
- Follow-up schedule

### B. Stand-Up Meeting

Quick synchronization meetings for teams.

**Characteristics**:
- Time-boxed (typically 15 minutes)
- Structured around: Progress, Plans, Blockers
- Rapid round-robin format
- Automatic summary generation

**Output Package**:
- Team status snapshot
- Blocker registry with escalation routing
- Progress metrics update
- Auto-generated follow-up tasks

### C. Project Review Meeting

Comprehensive assessment of project status.

**Characteristics**:
- Milestone-centered discussion
- Dependency mapping
- Risk identification and assessment
- Deliverable evaluation
- Resource allocation review

**Output Package**:
- Project health dashboard update
- Risk registry updates
- Milestone status report
- Resource reallocation recommendations
- Dependency conflict alerts

### D. Multi-Domain Meeting

Cross-functional collaboration spanning multiple CHE·NU domains.

**Characteristics**:
- Multiple domain specialist agents active
- Cross-domain context injection
- Integrated workflow coordination
- Multi-perspective analysis

**Example**: A construction project meeting involving:
- **Construction Domain**: Project execution status
- **Architecture Domain**: Design compliance review
- **Finance Domain**: Budget and cash flow analysis
- **Immobilier Domain**: Property integration requirements

**Output Package**:
- Domain-specific action items
- Cross-domain dependency map
- Integrated timeline updates
- Multi-domain risk assessment

### E. XR Spatial Meeting

Immersive collaboration in extended reality environments.

**Characteristics**:
- 3D spatial environment
- Object manipulation and annotation
- Spatial audio for natural conversation
- Agent avatars for AI participation
- Mixed reality integration (2D participants can join)

**Use Cases**:
- Architecture design reviews
- Construction site walkthroughs
- Property renovations visualization
- Creative brainstorming sessions
- Training and education

**Output Package**:
- XR scene capture with annotations
- Spatial decision documentation
- 3D model evolution log
- Immersive session replay

### F. Asynchronous Meeting

Structured collaboration across time zones and schedules.

**Characteristics**:
- Defined contribution windows
- Agent-facilitated continuity
- Structured input templates
- Progressive synthesis
- Defined decision points

**Workflow**:
1. Meeting initiator sets agenda and parameters
2. Participants contribute within defined windows
3. Agents synthesize contributions and identify convergence/divergence
4. Decision points are surfaced for resolution
5. Final synthesis generates standard meeting outputs

**Output Package**:
- Contribution timeline
- Synthesis documents
- Decision record with attribution
- Async participation metrics

---

## Chapter 75: Meeting Engines and Subsystems

### A. Meeting Engine

The central orchestrator for all meeting operations.

**Responsibilities**:
- Meeting creation and configuration
- Permission management
- Participant coordination
- Agent selection and activation
- Output routing to DataSpaces
- Follow-up workflow triggering

**Capabilities**:
- Multi-format meeting support (real-time, async, hybrid, XR)
- Template management for recurring meeting types
- Integration with calendar systems
- Notification and reminder management

### B. Note Engine

Transforms raw meeting content into structured knowledge.

**Input Processing**:
- Speech-to-text transcription
- Text chat capture
- Screen activity logging
- XR interaction recording

**Output Generation**:
- Chronological transcript with timestamps
- Topic-organized notes
- Speaker-attributed contributions
- Action item extraction
- Decision highlighting

**Domain Adaptation**:
The Note Engine formats outputs according to domain conventions. Construction meeting notes emphasize milestones and safety items; Finance meeting notes highlight budget decisions and approvals.

### C. Decision Engine

Identifies, structures, and manages decisions made during meetings.

**Decision Detection**:
- Natural language patterns indicating commitment
- Explicit decision declarations
- Voting outcomes
- Approval statements

**Decision Documentation**:
- Decision text
- Context and rationale
- Participants involved
- Related agenda items
- Implementation requirements
- Approval chain if required

**Decision Workflow**:
- Confirmation prompts for ambiguous decisions
- Escalation routing for decisions requiring additional approval
- Integration with governance workflows
- Conflict detection with previous decisions

### D. Task Extraction Engine

Creates actionable tasks from meeting discussions.

**Task Detection**:
- Action verb recognition
- Assignment statements
- Commitment patterns
- Deadline mentions

**Task Structuring**:
- Task title and description
- Owner assignment
- Deadline extraction or suggestion
- Priority assessment
- Domain and DataSpace routing
- Dependency identification

**Task Integration**:
- Automatic routing to task management
- Project timeline integration
- Workload balancing alerts
- Progress tracking initialization

### E. Summary Engine

Generates multiple summary formats for different audiences and purposes.

**Summary Types**:

**Micro Summary** (1-2 sentences): Capture meeting essence for quick reference
**Executive Summary** (1 paragraph): Key outcomes for leadership review
**Technical Summary**: Detailed technical decisions and specifications
**Task Summary**: Focused list of action items with assignments
**Risk Summary**: Identified risks and mitigation decisions
**Decision Summary**: All decisions with context and rationale

**Adaptive Generation**:
Summaries adapt to domain context. A creative meeting summary emphasizes concepts and directions; a construction meeting summary emphasizes schedules and specifications.

### F. Replay Engine

Enables time-shifted meeting consumption and reference.

**Capabilities**:
- Time-coded transcript navigation
- Jump to decision points
- Speaker-filtered playback
- Topic-based navigation
- Search within meeting content
- Clip extraction for sharing

**Integration**:
- Connect transcript to decisions
- Link playback to DataSpace updates
- Surface key phrases and moments
- Enable context reconstruction for non-attendees

---

## Chapter 76: Meeting Workflow

### Complete Meeting Lifecycle

#### Phase 1: Initiation

1. **User Request**: User initiates meeting via voice command, interface, or calendar
2. **Context Determination**: CHE·NU analyzes request to determine:
   - Relevant sphere(s)
   - Applicable domain(s)
   - Related projects and DataSpaces
   - Required participants
3. **Agent Activation**: Relevant agents are activated and briefed
4. **DataSpace Creation**: Meeting DataSpace instantiated with initial structure

#### Phase 2: Preparation

5. **Material Assembly**: Context Agent gathers relevant documents, previous decisions, pending items
6. **Agenda Generation**: Draft agenda created from:
   - User-specified items
   - Pending tasks from related DataSpaces
   - Unresolved issues from previous meetings
   - Agent-suggested topics
7. **Participant Notification**: Invitations sent with pre-meeting briefing
8. **Environment Setup**: Virtual room, XR space, or hybrid environment prepared

#### Phase 3: Execution

9. **Meeting Launch**: Participants join, agents activate in appropriate roles
10. **Agenda Management**: Meeting Orchestrator Agent guides discussion flow
11. **Real-Time Processing**:
    - Note-Taking Agent captures and structures discussion
    - Decision Agent identifies and documents decisions
    - Task Extraction Agent captures action items
    - Context Agent provides relevant information on demand
12. **Document Handling**: Shared files and presentations tracked and stored
13. **XR Tracking** (if applicable): Spatial interactions and annotations captured

#### Phase 4: Conclusion

14. **Summary Generation**: Summary Engine produces multi-format summaries
15. **Confirmation Round**: Key decisions and tasks confirmed with participants
16. **Recording Finalization**: Audio/video processed and indexed

#### Phase 5: Integration

17. **Task Routing**: Extracted tasks routed to appropriate DataSpaces and owners
18. **Decision Integration**: Decisions logged in relevant DataSpaces
19. **Document Filing**: Meeting artifacts filed in appropriate locations
20. **Workflow Triggering**: Follow-up workflows initiated based on decisions
21. **Calendar Updates**: Follow-up meetings scheduled as needed

#### Phase 6: Follow-Up

22. **Progress Monitoring**: Task completion tracked
23. **Reminder Generation**: Deadline reminders sent
24. **Escalation Handling**: Overdue items escalated appropriately
25. **Historical Integration**: Meeting becomes queryable part of knowledge base

---

## Chapter 77: Meeting Agents

### A. Meeting Orchestrator Agent

**Role**: Ensures meeting structure and efficiency

**Responsibilities**:
- Maintains agenda discipline
- Manages time allocation
- Facilitates transitions between topics
- Requests clarifications when needed
- Ensures all agenda items are addressed
- Prompts for decisions when discussion reaches conclusion
- Manages participant engagement

**Personality**: Professional, diplomatic, time-conscious

**Interactions**:
- Gently redirects off-topic discussions
- Summarizes discussions before moving to next topic
- Alerts when time allocation is exceeded
- Prompts quiet participants for input when appropriate

### B. Note-Taking Agent

**Role**: Captures and structures meeting content

**Responsibilities**:
- Transcribes discussions accurately
- Organizes notes by topic
- Attributes statements to speakers
- Highlights key points
- Flags items requiring follow-up
- Maintains consistent formatting

**Capabilities**:
- Multi-language transcription
- Technical terminology recognition
- Cross-reference to existing documents
- Real-time note sharing

### C. Decision Agent

**Role**: Identifies and documents decisions

**Responsibilities**:
- Recognizes decision moments in discussion
- Clarifies ambiguous commitments
- Requests explicit confirmation
- Documents decision context
- Tracks approval requirements
- Identifies conflicts with previous decisions

**Intervention Triggers**:
- Commitment language detected
- Multiple options discussed with selection
- Explicit voting or consensus
- Deadline or resource allocation statements

### D. Task Extraction Agent

**Role**: Converts discussion into actionable tasks

**Responsibilities**:
- Identifies action items in discussion
- Assigns owners based on discussion
- Extracts or suggests deadlines
- Assesses priority and dependencies
- Routes tasks to appropriate systems
- Tracks task acknowledgment

**Task Validation**:
- Confirms task understanding with assignees
- Clarifies ambiguous assignments
- Identifies resource conflicts
- Suggests realistic timelines

### E. Context Agent

**Role**: Provides relevant information during meetings

**Responsibilities**:
- Monitors discussion for information needs
- Retrieves relevant documents on demand
- Surfaces previous decisions that relate to current discussion
- Highlights inconsistencies or conflicts
- Provides historical context
- Answers factual questions from knowledge base

**Proactive Support**:
- Pre-loads likely-needed documents
- Prepares briefing materials
- Identifies relevant precedents
- Tracks pending items from previous meetings

### F. Domain Specialist Agents

Depending on meeting context, relevant domain specialists participate:

**Construction Specialist**: Provides technical construction expertise, code compliance, safety considerations

**Finance Specialist**: Budget analysis, financial implications, approval requirements

**Architecture Specialist**: Design considerations, spatial analysis, regulatory compliance

**Immobilier Specialist**: Property-specific context, tenant considerations, regulatory requirements

**Creative Specialist**: Brand consistency, creative direction, asset management

Each specialist contributes domain-specific expertise while coordinating with other agents through the Meeting Orchestrator.

---

## Chapter 78: XR Meeting System

### Immersive Collaboration

CHE·NU's XR Meeting System extends collaboration into three-dimensional space, enabling interactions impossible in traditional formats.

### XR Environment Types

**Virtual Meeting Room**: Standard meeting environment with enhanced visualization capabilities

**Design Studio**: Optimized for creative and design work with manipulation tools

**Construction Site**: Virtual representation of physical locations for walkthroughs

**Data Visualization Space**: Immersive environment for exploring complex data

**Brainstorming Sphere**: Open creative space for ideation and mind mapping

### XR Capabilities

**Collaborative Object Manipulation**: Multiple participants can simultaneously interact with 3D objects, models, and diagrams

**Spatial Annotation**: Draw, write, and annotate in 3D space with persistent markers

**Room Generation**: Dynamically create meeting environments based on purpose

**XR Sticky Notes**: Place notes in 3D space attached to objects or locations

**XR Diagrams**: Create and manipulate diagrams in three dimensions

**Voice and Hand Interactions**: Natural interaction through speech and gesture

**Agent Avatars**: AI agents appear as visual presences in XR space

**Multi-User Spatial Audio**: Realistic audio positioning for natural conversation

**2D Participant Integration**: Traditional video participants can join and see XR content

### XR Meeting DataSpace Additions

XR meetings extend the standard Meeting DataSpace with:

**Objects**: 3D models used or created during the meeting

**Scene Snapshots**: Captured states of the XR environment

**Manipulations Log**: Chronological record of object interactions

**Spatial Annotations**: All 3D annotations with positions and authors

**Environment Configuration**: Room setup and customizations

### XR Workflow

1. **Environment Selection**: Choose or generate appropriate XR space
2. **Asset Loading**: Relevant 3D models and documents loaded into space
3. **Participant Onboarding**: Users join via XR headsets or 2D fallback
4. **Spatial Collaboration**: Interactive session with full manipulation capabilities
5. **Capture and Synthesis**: XR interactions captured and synthesized into standard outputs
6. **Export**: XR content exportable to standard formats for non-XR consumption

---

## Chapter 79: Meeting Governance

### Permission Framework

**Meeting Creation**: Who can initiate meetings and set parameters

**Participation**: Who can join meetings and in what capacity

**Recording**: Explicit consent required; granular options for audio, video, transcript

**Document Access**: What materials participants can view and edit

**Output Distribution**: Who receives meeting outputs and summaries

### Identity Integration

Meetings respect CHE·NU's Multi-Identity system:

- Participants join under appropriate identity (Personal, Business, etc.)
- Identity context affects agent behavior and access
- Cross-identity meetings require explicit permission
- Identity separation maintained in outputs

### Audit and Accountability

**Complete Audit Trail**: Every action logged with timestamp and actor

**Decision Attribution**: All decisions attributed to participants

**Agent Transparency**: Agent contributions clearly marked and explainable

**Reversible Actions**: Meeting modifications tracked with rollback capability

### Consent Management

**Recording Consent**: Explicit opt-in required for recording

**AI Participation Consent**: Participants informed of AI agent roles

**Data Retention Consent**: Clear policies on how long meeting data is retained

**External Sharing Consent**: Explicit approval required for sharing outside participants

---

## Chapter 80: Meeting System Integration

### Cross-System Integration

The Meeting System integrates with all CHE·NU components:

**DataSpace Engine**: Meeting DataSpaces managed through DataSpace Engine

**Thread Engine**: Meetings linked to conversation threads

**Workspace Engine**: Meeting outputs feed workspace documents and projects

**File Transformation Engine**: Meeting recordings transformed to various formats

**Finance Domain**: Budget decisions integrated with financial systems

**Construction Domain**: Project decisions integrated with construction workflows

**Architecture Domain**: Design decisions captured with visual context

**Immobilier Domain**: Property-related decisions linked to property DataSpaces

**XR Spatial Engine**: Full XR meeting environment support

### Calendar Integration

- Native integration with Google Calendar, Outlook, Apple Calendar
- Automatic time zone handling
- Conflict detection and resolution
- Recurring meeting support
- Availability-based scheduling suggestions

### Communication Integration

- Meeting links shared via email, messaging
- Pre-meeting briefings distributed automatically
- Post-meeting summaries distributed to participants
- Task assignments notified to owners

---

## Chapter 81: Meeting System Diagrams

### Diagram 1: Meeting Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHE·NU MEETING SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   MEETING   │    │   CONTEXT   │    │    XR       │         │
│  │   ENGINE    │◄───│   ENGINE    │◄───│   ENGINE    │         │
│  └──────┬──────┘    └─────────────┘    └─────────────┘         │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MEETING PROCESSING LAYER                   │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │  NOTE   │ │DECISION │ │  TASK   │ │ SUMMARY │       │   │
│  │  │ ENGINE  │ │ ENGINE  │ │ ENGINE  │ │ ENGINE  │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 MEETING DATASPACE                       │   │
│  │  [Notes] [Decisions] [Tasks] [Recordings] [XR Objects]  │   │
│  └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              OUTPUT DISTRIBUTION                        │   │
│  │  [DataSpaces] [Workflows] [Calendars] [Notifications]   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Diagram 2: Agent Orchestration in Meetings

```
                    ┌─────────────────────┐
                    │     MEETING         │
                    │   ORCHESTRATOR      │
                    │      AGENT          │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ NOTE-TAKING │     │  DECISION   │     │    TASK     │
    │    AGENT    │     │   AGENT     │     │   AGENT     │
    └─────────────┘     └─────────────┘     └─────────────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    CONTEXT AGENT    │
                    │  (Provides Info)    │
                    └─────────────────────┘
                               │
           ┌───────────────────┴───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ CONSTRUCTION│     │  FINANCE    │     │  IMMOBILIER │
    │  SPECIALIST │     │ SPECIALIST  │     │  SPECIALIST │
    └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Chapter 82: Meeting Glossary

**Knowledge Event**: CHE·NU's term for meetings, emphasizing their role in generating structured, reusable knowledge.

**Meeting DataSpace**: The dedicated data container created for each meeting containing all artifacts.

**Meeting Engine**: Central orchestrator managing meeting creation, execution, and output routing.

**Note Engine**: Subsystem that transforms raw meeting content into structured notes.

**Decision Engine**: Subsystem that identifies, documents, and manages decisions.

**Task Extraction Engine**: Subsystem that creates actionable tasks from discussion.

**Summary Engine**: Subsystem that generates multiple summary formats.

**Replay Engine**: Subsystem enabling time-shifted meeting consumption.

**Meeting Orchestrator Agent**: AI agent ensuring meeting structure and efficiency.

**Context Agent**: AI agent providing relevant information during meetings.

**XR Meeting**: Immersive meeting conducted in extended reality environment.

**Async Meeting**: Meeting where participants contribute at different times.

**Hybrid Meeting**: Meeting combining real-time and asynchronous elements.

---

*End of Meeting System Chapters*
