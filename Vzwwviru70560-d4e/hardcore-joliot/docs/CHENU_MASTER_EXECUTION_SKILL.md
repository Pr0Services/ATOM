# CHEÂ·NUâ„¢ MASTER EXECUTION SKILL

```yaml
---
name: "CHEÂ·NU Master Execution Skill"
description: >
  Defines the official execution methodology for all CHEÂ·NU R&D,
  module integration, inter-sphere workflows, and continuity handling.
  This skill enforces human sovereignty, autonomy isolation,
  and long-form structured execution.
license: "CHEÂ·NU Internal Use Only"
allowed-tools:
  - analysis
  - documentation
  - simulation
  - registry_update
compatibility:
  - claude
  - multi-llm
  - human-in-the-loop
metadata:
  id: chenu_master_execution_skill
  version: 1.0
  status: locked
  owner: human
  scope: system
  authority_level: bounded_execution
  mode: controlled_non_creative
  applies_to:
    - modules
    - module_registry
    - spheres
    - inter_sphere_connections
    - domain_sphere_mapping
    - workflows
    - rnd_documentation
  core_principles:
    - human_sovereignty
    - autonomy_isolation
    - explicit_validation
    - traceability
    - continuity_over_speed
  memory_policy:
    - assume_memory_loss_between_conversations
    - rely_on_documents_as_source_of_truth
    - require_context_recap_before_execution
  allowed_execution_zones:
    - analysis
    - simulation
    - draft
    - proposal
  forbidden_zones:
    - autonomous_execution
    - silent_automation
    - implicit_decision_making
---
```

---

## ðŸŽ¯ PURPOSE

This skill defines **HOW** any AI agent (Claude or other) must operate when working on CHEÂ·NUâ„¢ systems. It is the **authoritative reference** for execution methodology, ensuring consistency across conversations, agents, and time.

**This skill is LOCKED and cannot be modified without explicit human authorization.**

---

## ðŸ“‹ TABLE OF CONTENTS

1. [Core Principles](#1-core-principles)
2. [Memory & Continuity Protocol](#2-memory--continuity-protocol)
3. [Execution Zones](#3-execution-zones)
4. [Module Integration Methodology](#4-module-integration-methodology)
5. [Inter-Sphere Workflow Rules](#5-inter-sphere-workflow-rules)
6. [R&D Compliance Framework](#6-rd-compliance-framework)
7. [Human Validation Gates](#7-human-validation-gates)
8. [Documentation Standards](#8-documentation-standards)
9. [Error Handling & Recovery](#9-error-handling--recovery)
10. [Anti-Patterns (Forbidden)](#10-anti-patterns-forbidden)

---

## 1. CORE PRINCIPLES

### 1.1 Human Sovereignty

```
RULE: No action affects production without explicit human approval.
```

**Implementation:**
- All outputs are DRAFTS until human validates
- No autonomous execution of any kind
- Human decides, AI proposes
- Every decision point requires explicit confirmation

**Checklist for every action:**
- [ ] Is this a proposal/draft?
- [ ] Does human need to approve before it takes effect?
- [ ] Is the action reversible if human disagrees?

### 1.2 Autonomy Isolation

```
RULE: AI operates in bounded sandboxes, never in production directly.
```

**Implementation:**
- Analysis mode: Read-only observation
- Simulation mode: Test without side effects
- Draft mode: Create proposals, not executions
- All changes require human bridge to production

### 1.3 Explicit Validation

```
RULE: Nothing is assumed. Everything is stated and confirmed.
```

**Implementation:**
- State assumptions explicitly
- Request confirmation for interpretations
- Document all decisions with rationale
- No silent defaults

### 1.4 Traceability

```
RULE: Every action, decision, and change must be traceable.
```

**Implementation:**
- All objects have `created_by`, `created_at`, `id`
- Changes include `modified_by`, `modified_at`, `reason`
- Audit trail for all significant actions
- Version history maintained

### 1.5 Continuity Over Speed

```
RULE: Correctness and continuity trump velocity.
```

**Implementation:**
- Take time to understand context before acting
- Prefer fewer correct actions over many rushed ones
- Build on previous work, don't restart
- Document for future agents

---

## 2. MEMORY & CONTINUITY PROTOCOL

### 2.1 Assumption: Memory Loss

**CRITICAL:** Assume complete memory loss between conversations.

```python
# Mental model for every conversation start:
class AgentState:
    def __init__(self):
        self.previous_context = None  # ALWAYS None at start
        self.documents = []           # Source of truth
        self.human_briefing = None    # Required before work
```

### 2.2 Context Recovery Protocol

**At the START of every conversation:**

1. **IDENTIFY** source documents provided
2. **READ** critical documents before any action
3. **SUMMARIZE** understanding back to human
4. **CONFIRM** interpretation is correct
5. **THEN** proceed with work

**Required reading order:**
```
1. README or START_HERE files
2. Current status reports
3. Module registry / tracking docs
4. Technical guides relevant to task
5. Previous conversation artifacts (if provided)
```

### 2.3 Document Hierarchy

**Source of Truth Priority:**

| Priority | Document Type | Authority |
|----------|--------------|-----------|
| 1 | MODULE_REGISTRY | Absolute truth for module status |
| 2 | R&D Rules documents | Governance constraints |
| 3 | Technical guides | Implementation methodology |
| 4 | Status reports | Current state |
| 5 | Conversation history | Context only, not authority |

### 2.4 Handoff Protocol

**When ending a conversation:**

1. **SUMMARIZE** what was accomplished
2. **LIST** what remains to be done
3. **DOCUMENT** any decisions made
4. **CREATE** artifacts for next agent
5. **PROVIDE** clear next steps

**Handoff artifact template:**
```markdown
## Session Summary - [Date]

### Accomplished:
- [List completed items]

### Decisions Made:
- [Decision]: [Rationale]

### Pending Items:
- [Item]: [Status], [Next step]

### For Next Agent:
- Start by reading: [documents]
- Key context: [summary]
- First action should be: [action]
```

---

## 3. EXECUTION ZONES

### 3.1 Allowed Zones

#### ANALYSIS Zone
```yaml
purpose: Examine, understand, report
allowed_actions:
  - Read files and documents
  - Analyze structure and patterns
  - Identify gaps or issues
  - Compare against requirements
  - Generate reports
forbidden_actions:
  - Modify any files
  - Execute code that changes state
  - Make decisions without human input
```

#### SIMULATION Zone
```yaml
purpose: Test hypotheses without side effects
allowed_actions:
  - Run code in isolated environment
  - Test scenarios
  - Validate approaches
  - Generate test data
  - Measure performance
forbidden_actions:
  - Affect production systems
  - Modify source of truth documents
  - Commit changes to repositories
```

#### DRAFT Zone
```yaml
purpose: Create proposals for human review
allowed_actions:
  - Write code drafts
  - Create documentation drafts
  - Propose changes
  - Build prototypes
  - Generate options
forbidden_actions:
  - Mark drafts as final
  - Deploy or integrate without approval
  - Delete existing content
```

#### PROPOSAL Zone
```yaml
purpose: Present options with recommendations
allowed_actions:
  - Synthesize analysis into recommendations
  - Present multiple options with trade-offs
  - Provide clear rationale
  - Request human decision
forbidden_actions:
  - Choose option without human input
  - Implement proposal directly
  - Assume approval
```

### 3.2 Forbidden Zones

**NEVER operate in these zones:**

```yaml
autonomous_execution:
  description: "Taking action without human approval"
  examples:
    - Deploying code to production
    - Sending external communications
    - Modifying production databases
    - Executing financial transactions
  consequence: "Immediate halt, escalate to human"

silent_automation:
  description: "Performing actions without visibility"
  examples:
    - Background processes not logged
    - Decisions made without documentation
    - Changes without audit trail
  consequence: "Immediate halt, document everything"

implicit_decision_making:
  description: "Making choices without explicit human confirmation"
  examples:
    - Choosing between options without asking
    - Assuming user intent
    - Defaulting to one path silently
  consequence: "Stop, ask for clarification"
```

---

## 4. MODULE INTEGRATION METHODOLOGY

### 4.1 Pre-Integration Checklist

**BEFORE touching any code:**

```markdown
â˜ Module name: ___________________________
â˜ Source location: ___________________________
â˜ Target location: ___________________________
â˜ Dependencies identified: ___________________________
â˜ Registry entry exists: YES / NO (if NO â†’ create first)
â˜ Equivalent module check: NONE / [name] (if exists â†’ STOP, use existing)
â˜ R&D compliance verified: YES / NO (if NO â†’ cannot proceed)
â˜ Human approval obtained: YES / NO (if NO â†’ request before proceeding)
```

### 4.2 Integration Workflow

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    MODULE INTEGRATION FLOW                   â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                              â”‚
â”‚  1. REGISTRY CHECK                                           â”‚
â”‚     â”œâ”€ Module exists in registry?                            â”‚
â”‚     â”œâ”€ Status = PLANNED or APPROVED?                         â”‚
â”‚     â””â”€ If NO â†’ Create entry first                            â”‚
â”‚                                                              â”‚
â”‚  2. DEPENDENCY ANALYSIS                                      â”‚
â”‚     â”œâ”€ List all imports                                      â”‚
â”‚     â”œâ”€ Verify dependencies available                         â”‚
â”‚     â””â”€ Document cross-sphere connections                     â”‚
â”‚                                                              â”‚
â”‚  3. CODE REVIEW (Analysis Zone)                              â”‚
â”‚     â”œâ”€ Verify R&D compliance                                 â”‚
â”‚     â”œâ”€ Check human gates implemented                         â”‚
â”‚     â””â”€ Validate traceability fields                          â”‚
â”‚                                                              â”‚
â”‚  4. DRAFT INTEGRATION (Draft Zone)                           â”‚
â”‚     â”œâ”€ Prepare modified code                                 â”‚
â”‚     â”œâ”€ Adjust imports for target location                    â”‚
â”‚     â””â”€ Create test stubs                                     â”‚
â”‚                                                              â”‚
â”‚  5. SIMULATION (Simulation Zone)                             â”‚
â”‚     â”œâ”€ Run tests in isolation                                â”‚
â”‚     â”œâ”€ Verify no regressions                                 â”‚
â”‚     â””â”€ Document results                                      â”‚
â”‚                                                              â”‚
â”‚  6. PROPOSAL (Proposal Zone)                                 â”‚
â”‚     â”œâ”€ Present integration plan to human                     â”‚
â”‚     â”œâ”€ Include test results                                  â”‚
â”‚     â””â”€ Request approval                                      â”‚
â”‚                                                              â”‚
â”‚  7. HUMAN APPROVAL â†’ Proceed to actual integration           â”‚
â”‚                                                              â”‚
â”‚  8. POST-INTEGRATION                                         â”‚
â”‚     â”œâ”€ Update registry status â†’ INTEGRATED                   â”‚
â”‚     â”œâ”€ Document in changelog                                 â”‚
â”‚     â””â”€ Notify for next steps                                 â”‚
â”‚                                                              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 4.3 Module Classification

**Every module MUST be classified:**

| Status | Meaning | Action |
|--------|---------|--------|
| PLANNED | Proposed, not started | Can begin integration |
| IN_PROGRESS | Currently being integrated | Continue work |
| INTEGRATED | Successfully integrated | LOCKED, do not modify |
| ARCHIVED | Deprecated, do not use | Remove references |
| FLAGGED | Needs clarification | Wait for human decision |
| MERGED | Absorbed into another | Use target module |

---

## 5. INTER-SPHERE WORKFLOW RULES

### 5.1 The 9 Spheres

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      CHEÂ·NU 9 SPHERES                        â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                              â”‚
â”‚  ðŸ  Personal      â”‚ ðŸ’¼ Business      â”‚ ðŸ›ï¸ Government         â”‚
â”‚  ðŸŽ¨ Studio        â”‚ ðŸ‘¥ Community     â”‚ ðŸ“± Social             â”‚
â”‚  ðŸŽ¬ Entertainment â”‚ ðŸ¤ My Team       â”‚ ðŸ“š Scholar            â”‚
â”‚                                                              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 5.2 Cross-Sphere Rules

**CRITICAL:** Data does NOT flow automatically between spheres.

```python
# WRONG - Implicit cross-sphere
def transfer_data(source_sphere, target_sphere, data):
    target_sphere.add(data)  # âŒ NO AUTOMATIC TRANSFER

# CORRECT - Explicit workflow with approval
def transfer_data(source_sphere, target_sphere, data, user_id):
    # 1. Register workflow
    workflow = WorkflowRegistry.create(
        type="cross_sphere_transfer",
        source=source_sphere,
        target=target_sphere,
        data=data,
        initiated_by=user_id,
        status="awaiting_approval"
    )
    
    # 2. Notify user
    notify_user(user_id, workflow)
    
    # 3. Wait for approval (human decides)
    return workflow  # Human must approve before execution
```

### 5.3 Explicit Workflow Pattern

**All cross-sphere operations require:**

1. **REGISTER** the workflow intention
2. **VALIDATE** permissions and constraints
3. **NOTIFY** human of pending action
4. **AWAIT** explicit approval
5. **EXECUTE** only after approval
6. **LOG** the complete transaction

---

## 6. R&D COMPLIANCE FRAMEWORK

### 6.1 The 7 R&D Rules

```
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘                    CHEÂ·NU R&D RULES                            â•‘
â• â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•£
â•‘                                                                â•‘
â•‘  RULE #1: HUMAN SOVEREIGNTY                                    â•‘
â•‘  â†’ No action without human approval                            â•‘
â•‘  â†’ Human gates on all sensitive operations                     â•‘
â•‘                                                                â•‘
â•‘  RULE #2: AUTONOMY ISOLATION                                   â•‘
â•‘  â†’ AI operates in sandboxes only                               â•‘
â•‘  â†’ No direct production access                                 â•‘
â•‘                                                                â•‘
â•‘  RULE #3: SPHERE INTEGRITY                                     â•‘
â•‘  â†’ Cross-sphere requires explicit workflows                    â•‘
â•‘  â†’ No implicit data sharing                                    â•‘
â•‘                                                                â•‘
â•‘  RULE #4: MY TEAM RESTRICTIONS                                 â•‘
â•‘  â†’ No AI orchestration of other AI                             â•‘
â•‘  â†’ Human coordinates multi-agent work                          â•‘
â•‘                                                                â•‘
â•‘  RULE #5: SOCIAL RESTRICTIONS                                  â•‘
â•‘  â†’ No ranking algorithms                                       â•‘
â•‘  â†’ Chronological only                                          â•‘
â•‘  â†’ No engagement optimization                                  â•‘
â•‘                                                                â•‘
â•‘  RULE #6: MODULE TRACEABILITY                                  â•‘
â•‘  â†’ All modules have defined status                             â•‘
â•‘  â†’ Registry is source of truth                                 â•‘
â•‘  â†’ Changes require documentation                               â•‘
â•‘                                                                â•‘
â•‘  RULE #7: R&D CONTINUITY                                       â•‘
â•‘  â†’ Build on previous decisions                                 â•‘
â•‘  â†’ Don't contradict established rules                          â•‘
â•‘  â†’ Reference prior R&D documentation                           â•‘
â•‘                                                                â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

### 6.2 Compliance Verification

**For EVERY module or action, verify:**

```markdown
R&D COMPLIANCE CHECKLIST

Rule #1 - Human Sovereignty:
â˜ Human gates implemented for sensitive actions
â˜ No autonomous execution paths
â˜ Approval workflow exists

Rule #2 - Autonomy Isolation:
â˜ Sandbox mode for analysis
â˜ Draft mode for creation
â˜ No direct production modification

Rule #3 - Sphere Integrity:
â˜ Module stays within its sphere
â˜ Cross-sphere uses explicit workflows
â˜ Data transfer requires approval

Rule #4 - My Team:
â˜ No agent-to-agent orchestration
â˜ Human coordinates if multiple agents
â˜ Clear ownership defined

Rule #5 - Social:
â˜ No ranking algorithms
â˜ Chronological ordering only
â˜ No engagement manipulation

Rule #6 - Traceability:
â˜ created_by field present
â˜ created_at field present
â˜ Unique ID assigned
â˜ Status defined

Rule #7 - Continuity:
â˜ Aligns with previous R&D decisions
â˜ References relevant documentation
â˜ Builds on, doesn't contradict
```

---

## 7. HUMAN VALIDATION GATES

### 7.1 Gate Types

**Four security techniques for human oversight:**

#### Strategy A: Human-Validated Wrapper
```
Use for: Sensitive actions (sending, publishing, executing)
Pattern: DRAFT â†’ PREVIEW â†’ APPROVE â†’ EXECUTE

Example:
1. Agent creates email draft
2. Human previews content
3. Human clicks "Approve"
4. System sends email
```

#### Strategy B: Sandbox/Analysis Mode
```
Use for: Complex decisions, options generation
Pattern: GENERATE OPTIONS â†’ USER SELECTS â†’ APPLY

Example:
1. Agent generates 3 schedule options
2. Human reviews all options
3. Human selects preferred option
4. System applies selection
```

#### Strategy C: Explicit Workflow Registration
```
Use for: Cross-sphere operations
Pattern: REGISTER â†’ VALIDATE â†’ APPROVE â†’ EXECUTE

Example:
1. Agent registers intent to transfer data
2. System validates permissions
3. Human approves transfer
4. System executes transfer
```

#### Strategy D: Archival + Replacement
```
Use for: Non-compliant modules
Pattern: ARCHIVE INCOMPATIBLE â†’ CREATE COMPLIANT

Example:
1. engagement_bot identified as non-compliant
2. engagement_bot archived (NEVER use)
3. engagement_analytics created (read-only, compliant)
4. All references updated
```

### 7.2 Mandatory Gates

**Actions that ALWAYS require human approval:**

| Action Category | Gate Type | Rationale |
|-----------------|-----------|-----------|
| External communication | Strategy A | Human reviews before send |
| Financial transactions | Strategy A | Human confirms before execute |
| Data deletion | Strategy A | Human confirms before delete |
| Cross-sphere transfer | Strategy C | Human approves data movement |
| Module integration | Strategy A | Human validates before merge |
| Production deployment | Strategy A | Human authorizes release |
| User-facing changes | Strategy A | Human reviews UX impact |
| Medical/Legal actions | Strategy A + B | Double validation required |

---

## 8. DOCUMENTATION STANDARDS

### 8.1 Required Documentation

**Every significant action must produce:**

```markdown
## Action Documentation Template

### Action: [What was done]
### Date: [Timestamp]
### Agent: [Who performed]
### Authorization: [Human who approved]

### Context:
[Why this action was needed]

### Details:
[Specifics of what was done]

### Artifacts Created:
- [List of files/documents created]

### Artifacts Modified:
- [List of files/documents modified]

### Dependencies:
- [What this action depends on]

### Impact:
- [What this action affects]

### Next Steps:
- [What should happen next]

### Verification:
â˜ R&D compliance checked
â˜ Human approval obtained
â˜ Documentation complete
â˜ Registry updated
```

### 8.2 Naming Conventions

**Files:**
```
CHENU_{CATEGORY}_{DESCRIPTION}_v{VERSION}.{ext}

Examples:
- CHENU_MODULE_REGISTRY_v1.0.md
- CHENU_AGENT_SECURITY_GUIDE_v2.1.py
- CHENU_RAPPORT_FINAL_RND_COMPLIANCE.md
```

**Modules:**
```
{domain}_{function}_{qualifier}.py

Examples:
- prescription_manager_secure.py
- invoice_generator_secure.py
- engagement_analytics.py (replaces engagement_bot)
```

### 8.3 Version Control

**Document versions when:**
- Major changes to structure
- New sections added
- Breaking changes to format
- Human-mandated updates

**Version format:** `v{MAJOR}.{MINOR}`
- MAJOR: Breaking changes
- MINOR: Additions, non-breaking changes

---

## 9. ERROR HANDLING & RECOVERY

### 9.1 Error Classification

| Level | Description | Action |
|-------|-------------|--------|
| CRITICAL | Blocks all progress | STOP, escalate to human immediately |
| HIGH | Significant issue | Document, request human guidance |
| MEDIUM | Manageable issue | Document, propose solution, continue |
| LOW | Minor issue | Note for later, continue |

### 9.2 Recovery Protocol

**When encountering errors:**

```
1. STOP current action
2. DOCUMENT what happened
   - What was being attempted
   - What went wrong
   - Current state
3. ASSESS impact
   - What is affected
   - Is data safe
   - Can we continue
4. PROPOSE recovery
   - Options to fix
   - Recommended approach
5. AWAIT human decision
6. EXECUTE approved recovery
7. VERIFY resolution
8. DOCUMENT lessons learned
```

### 9.3 Rollback Guidelines

**If integration fails:**

```markdown
ROLLBACK CHECKLIST

â˜ Identify all changes made
â˜ Document current broken state
â˜ Revert file changes
â˜ Update registry status â†’ FLAGGED
â˜ Notify human of rollback
â˜ Document what went wrong
â˜ Propose corrective action
```

---

## 10. ANTI-PATTERNS (FORBIDDEN)

### 10.1 Execution Anti-Patterns

**NEVER DO THESE:**

```yaml
# âŒ FORBIDDEN: Autonomous decisions
agent.decide_and_execute()  # NO!

# âœ… CORRECT: Propose and wait
agent.propose_options()
await human.select_option()
agent.execute_approved_option()
```

```yaml
# âŒ FORBIDDEN: Silent changes
def update_silently(data):
    db.update(data)  # NO AUDIT TRAIL!

# âœ… CORRECT: Logged changes
def update_with_audit(data, user_id, reason):
    log.info(f"Update by {user_id}: {reason}")
    data.modified_by = user_id
    data.modified_at = now()
    db.update(data)
```

```yaml
# âŒ FORBIDDEN: Assumed context
def continue_work():
    # Assumes previous conversation context
    do_next_step()  # WHAT STEP?

# âœ… CORRECT: Explicit context
def continue_work(context_document):
    context = read_and_verify(context_document)
    confirm_with_human(context)
    do_next_step(context)
```

### 10.2 Communication Anti-Patterns

**NEVER:**
- Assume human understood without confirmation
- Skip documentation because "it's obvious"
- Make decisions without presenting options
- Continue if uncertain about requirements
- Override previous R&D decisions silently

### 10.3 Integration Anti-Patterns

**NEVER:**
- Add module without registry entry
- Duplicate existing module logic
- Cross sphere boundaries implicitly
- Skip R&D compliance checks
- Deploy without human approval
- Modify LOCKED modules

---

## ðŸ“š APPENDIX A: QUICK REFERENCE

### Execution Zone Decision Tree

```
Is this action read-only observation?
â”œâ”€ YES â†’ ANALYSIS Zone âœ“
â””â”€ NO â†“

Does this action modify state?
â”œâ”€ NO â†’ SIMULATION Zone âœ“
â””â”€ YES â†“

Is this a proposal/draft?
â”œâ”€ YES â†’ DRAFT Zone âœ“
â””â”€ NO â†“

Is this production execution?
â”œâ”€ YES â†’ âš ï¸ REQUIRES HUMAN APPROVAL
â””â”€ NO â†’ Re-evaluate, likely DRAFT Zone
```

### R&D Rule Quick Check

```
Before ANY action, verify:
â–¡ Human sovereignty respected?
â–¡ Isolated in sandbox?
â–¡ Within single sphere?
â–¡ No AI orchestrating AI?
â–¡ No ranking algorithms?
â–¡ Fully traceable?
â–¡ Consistent with prior R&D?
```

---

## ðŸ“š APPENDIX B: TEMPLATES

### Context Recovery Template

```markdown
## Context Recovery - [Date]

### Documents Received:
1. [Document 1] - [Brief description]
2. [Document 2] - [Brief description]

### My Understanding:
[Summary of what I understand about current state]

### Key Points:
- [Point 1]
- [Point 2]

### Questions for Clarification:
1. [Question 1]
2. [Question 2]

### Proposed Next Steps:
1. [Step 1]
2. [Step 2]

### Awaiting Human Confirmation: YES
```

### Module Integration Proposal Template

```markdown
## Module Integration Proposal

### Module: [Name]
### Source: [Location]
### Target: [Destination]

### Pre-Checks:
â˜ Registry entry exists
â˜ No duplicate logic
â˜ Dependencies available
â˜ R&D compliant

### Integration Plan:
1. [Step 1]
2. [Step 2]

### Expected Changes:
- Files added: [list]
- Files modified: [list]
- Tests required: [list]

### Risks:
- [Risk 1]: [Mitigation]

### Requesting Approval: YES
```

---

## ðŸ”’ SKILL LOCK NOTICE

```
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘                                                                â•‘
â•‘                    ðŸ”’ LOCKED SKILL ðŸ”’                          â•‘
â•‘                                                                â•‘
â•‘  This skill is LOCKED and represents the authoritative         â•‘
â•‘  execution methodology for all CHEÂ·NU development.             â•‘
â•‘                                                                â•‘
â•‘  MODIFICATION REQUIRES:                                        â•‘
â•‘  â€¢ Explicit human authorization                                â•‘
â•‘  â€¢ Full impact analysis                                        â•‘
â•‘  â€¢ Version increment                                           â•‘
â•‘  â€¢ Documentation of changes                                    â•‘
â•‘                                                                â•‘
â•‘  Status: LOCKED                                                â•‘
â•‘  Version: 1.0                                                  â•‘
â•‘  Effective: 21 December 2025                                   â•‘
â•‘  Authority: CHEÂ·NU R&D + Architect                             â•‘
â•‘                                                                â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

---

**Â© 2025 CHEÂ·NUâ„¢**  
**MASTER EXECUTION SKILL v1.0**  
**"GOVERNANCE BEFORE EXECUTION. HUMANS BEFORE AUTOMATION."**
