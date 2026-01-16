# CHE·NU — FIRST MEETING UX

```
Version: 1.0.0
Status: FROZEN
Last Updated: 2025-01
```

---

## 🎯 PURPOSE

Introduce meetings as a governed collaborative workspace,
not as a video call with AI gimmicks.

> A meeting is a context — not an event.

---

## 🧱 CORE PRINCIPLE

> Meetings do not start with AI.
> They start with people and intent.

AI assistance is optional, scoped, budgeted, and explicit.

---

## WHEN A MEETING CAN BE CREATED

A meeting can be created only if **at least one** of these is true:

- User is working inside a project
- User is collaborating with others
- User explicitly chooses "Create meeting"
- Orchestrator is already activated

**No automatic meeting creation.**

---

## MEETING CREATION FLOW (MINIMAL)

1. User clicks "Create meeting"
2. Inline modal opens (no page change)
3. Required fields:
   - Meeting name
4. Optional fields:
   - Project (recommended)
   - Sphere (auto-filled from context)
   - Budget preset (inherits current preset)

- No agenda required
- No participants required at creation

---

## INITIAL MEETING STATE (VERY IMPORTANT)

When the meeting opens:
- Workspace is empty
- No agents are active
- No recording
- No transcription
- No voice
- No budget spent

### Nova Message (text only, one message)
```
"Meetings start empty.
Nothing is recorded or analyzed unless you choose to."
```

---

## MEETING LAYOUT (3 SURFACES PRESERVED)

### Surface A — Nova
- Governance messages
- Budget / scope explanations
- Consent confirmations

### Surface B — Context
- Participants
- Project link
- Sphere
- Meeting status (live / paused)

### Surface C — Meeting Workspace
- Shared notes
- Documents
- Decisions
- Action items

Video / audio (if enabled later) are secondary layers.

---

## AI IN MEETINGS (STRICT RULES)

**AI is OFF by default.**

AI can be enabled only if:
- User explicitly clicks "Enable assistance"
- Scope is selected
- Budget is visible
- Token estimation is shown

### Nova Explanation Before Activation
```
"Assistance in meetings uses shared context and tokens.
Nothing will happen without confirmation."
```

### Buttons
```
[ Enable assistance ]   [ Continue without AI ]
```

**Default focus: Continue without AI**

---

## SCOPE IN MEETINGS

Available scopes:
- Selection (recommended)
- Meeting workspace
- Explicitly selected documents

**Workspace-wide or historical scopes are LOCKED by default.**

Scope lock rules apply exactly as elsewhere.

---

## BUDGET IN MEETINGS

- Each meeting has a token budget
- Budget is visible at all times
- Live meter is shown once AI is enabled
- When budget is near limit:
  - Nova warns at ~70%
  - Nova warns strongly at ~90%
- At 100%:
  - AI assistance stops
  - Meeting continues normally

**No automatic budget increase.**

---

## WHAT AI CAN DO IN MEETINGS

If enabled and confirmed, AI can:
- ✅ Propose summaries
- ✅ Extract action items
- ✅ Structure notes
- ✅ Draft follow-ups
- ✅ Compare versions

**All results are proposals.**
**Nothing is committed automatically.**

---

## WHAT AI CANNOT DO IN MEETINGS

- ❌ Speak without being asked
- ❌ Record silently
- ❌ Transcribe by default
- ❌ Decide outcomes
- ❌ Send messages
- ❌ Assign tasks without confirmation

---

## MEETING END

When meeting ends:
- No automatic summary
- No automatic follow-up
- No automatic email

### Nova Asks Once
```
"Would you like to save a summary of this meeting?"
```

### Buttons
```
[ Prepare summary ]   [ No, close meeting ]
```

**Default: No**

---

## POST-MEETING STATE

If summary is prepared:
- It appears as a proposal
- Can be accepted, edited, or rejected
- Can be assigned to a project or left unassigned

Meeting data remains accessible.
AI remains off unless re-enabled.

---

## PRIVACY & TRUST GUARANTEES

- Meetings are private by default
- No data leaves the meeting without consent
- No cross-meeting learning
- No silent reuse of content

---

## UX CONSTRAINTS (NON-NEGOTIABLE)

- No popups during discussion
- No interruptions
- No forced flows
- No hidden automation

> Meetings must feel calm and professional.

---

## CANONICAL STATEMENT

```
"A CHE·NU meeting is a shared space.
AI assists only when invited.
Decisions remain human."
```

---

```
END OF SPECIFICATION
```
