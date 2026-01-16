# CHE·NU™ V50 — Phase 3 Design Decisions Documentation

## 📋 OVERVIEW

This document captures the architectural and design decisions made during Phase 3 implementation
of the bureau components: ThreadEditor, MeetingEditor, and ResizablePanels.

**Date:** December 28, 2025
**Total Lines Created:** ~7,000 lines
**Components Delivered:** 3 major components + integrations

---

## 🧵 THREAD EDITOR (.chenu) — 2,252 lines

### Why Threads Are First-Class Objects

Threads in CHE·NU are not simple chat conversations. They are **persistent lines of thought** that:
1. Have an owner and scope (personal/shared/project)
2. Carry a token budget (intelligence energy)
3. Apply encoding rules (semantic compression)
4. Maintain an immutable audit trail
5. Can be linked to DataSpaces and Meetings

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| **5 tabs (General, Participants, Budget, Encoding, Governance)** | Separation of concerns - each tab addresses one aspect of the thread lifecycle |
| **Scope as cards, not dropdown** | Visual distinction between Personal/Shared/Project makes the choice more intentional |
| **Token presets + slider** | Quick selection for common budgets (500-25000) + fine control with slider |
| **4 encoding levels** | Minimal (0.5x), Standard (1x), Detailed (1.5x), Comprehensive (2x) - clear multipliers help users understand cost impact |
| **Audit level selector** | Users should choose their compliance level: Minimal (actions only), Standard (all + context), Comprehensive (everything) |
| **Linked Resources section** | Threads don't exist in isolation - they connect to DataSpaces and Meetings |
| **Nova always present** | As system intelligence, Nova participates in all threads for governance and assistance |

### Keyboard Shortcuts Added
- `Escape` → Close editor
- `Ctrl/Cmd + S` → Save thread

### Missing Features (Future Work)
- [ ] Drag & drop for participant ordering
- [ ] DataSpace/Meeting picker modals
- [ ] Thread forking (create child thread)
- [ ] Version history viewer

---

## 📅 MEETING EDITOR (Knowledge Events) — 2,490 lines

### Why Meetings Are Knowledge Events

In CHE·NU, meetings are not video calls - they are **knowledge events** that automatically produce:
- Structured notes (by topic, speaker, chronology)
- Tasks (extracted with assignees and deadlines)
- Decisions (captured with context and rationale)
- DataSpace updates (automatic synchronization)
- Replayable content (indexed, searchable)

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| **6 tabs (Details, Schedule, Participants, Agenda, XR, Governance)** | Meetings are complex - each aspect needs dedicated space |
| **4 meeting types (Sync, Async, Hybrid, XR Spatial)** | Cover all collaboration modalities supported by CHE·NU |
| **8 categories (Standup, Planning, Review, Decision, Brainstorm, Presentation, Workshop, Other)** | Pre-set defaults optimize setup (duration auto-adjusts) |
| **Structured agenda with types** | Each agenda item has a type (Discussion, Presentation, Decision, etc.) to help Nova generate appropriate artifacts |
| **Duration warning** | Visual alert when agenda total ≠ scheduled duration |
| **Recurrence support** | Daily, Weekly, Biweekly, Monthly patterns for recurring meetings |
| **XR as dedicated tab** | XR spatial meetings are a key differentiator - deserve first-class treatment |
| **4 auto-generate toggles** | Users control which artifacts Nova creates: Notes, Tasks, Decisions, Summary |

### Consent Management
The editor captures 3 types of consent per participant:
1. **Recording consent** - Required for capturing meeting content
2. **AI participation consent** - Acknowledgment of Nova's presence
3. **External sharing consent** - Controlled via governance settings

### Missing Features (Future Work)
- [ ] Calendar integration (Google, Outlook, Apple)
- [ ] Real drag & drop for agenda items
- [ ] Advanced recurrence (specific days, end date, occurrences)
- [ ] Thread picker modal for linking context

---

## 📐 RESIZABLE PANELS — 1,227 lines

### Why This Was Needed

CHE·NU's workspace needs flexible layouts for different workflows:
- **Bureau:** Sidebar (20%) | Main (80%)
- **Extended Bureau:** Sidebar (15%) | Main (55%) | Details (30%)
- **Split View:** Document 1 (50%) | Document 2 (50%)
- **Vertical:** Header | Content | Footer

Existing libraries either didn't match our design system or lacked key features.

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Context-based architecture** | ResizablePanelGroup provides context to children, enabling flexible composition |
| **Percentage-based sizing** | More predictable than pixels across different viewport sizes |
| **Auto-handle injection** | Handles automatically appear between panels - cleaner API |
| **Double-click to collapse** | Standard UX pattern for panel collapse |
| **Min/max constraints** | Prevent panels from becoming unusable |
| **Layout persistence (localStorage)** | Users shouldn't have to resize every session |
| **7-day expiry on saved layouts** | Prevents stale layouts from persisting forever |
| **Keyboard navigation** | Arrow keys for accessibility (2% step) |
| **Touch support** | Mobile-ready drag handling |

### API Design
```tsx
<ResizablePanelGroup direction="horizontal" autoSaveId="bureau-layout">
  <ResizablePanel id="sidebar" defaultSize={20} minSize={15} maxSize={30} collapsible>
    <Sidebar />
  </ResizablePanel>
  {/* Handle auto-injected */}
  <ResizablePanel id="main" defaultSize={80} minSize={40}>
    <MainContent />
  </ResizablePanel>
</ResizablePanelGroup>
```

### Preset Layouts Provided
- `bureau` - Standard sidebar + main
- `bureauExtended` - Sidebar + main + details
- `split` - Equal left/right
- `focus` - Collapsed sidebar, full main
- `verticalSplit` - Top/bottom split

### Missing Features (Future Work)
- [ ] Nested layouts (horizontal in vertical)
- [ ] Panel drag-to-reorder
- [ ] Panel minimize to tabs
- [ ] Animation customization

---

## 🔗 INTEGRATIONS

### ThreadsSection (495 lines)
- ✅ ThreadEditor modal rendering
- ✅ Create new thread
- ✅ Edit existing thread
- ✅ Delete thread with confirmation
- ✅ State management for editing

### MeetingsSection (529 lines)
- ✅ MeetingEditor modal rendering
- ✅ Schedule new meeting
- ✅ Edit existing meeting
- ✅ Delete meeting with confirmation
- ✅ Convert internal Meeting type to MeetingEditor type

---

## 🎨 DESIGN SYSTEM ALIGNMENT

All components use the CHE·NU design tokens:

```typescript
const CHENU_COLORS = {
  // Primary Brand
  sacredGold: '#D8B26A',
  
  // Nature Palette
  jungleEmerald: '#3F7249',
  cenoteTurquoise: '#3EB4A2',
  shadowMoss: '#2F4C39',
  earthEmber: '#7A593A',
  ancientStone: '#8D8371',
  
  // UI Colors
  uiSlate: '#1E1F22',
  softSand: '#E9E4D6',
  
  // Backgrounds
  bgPrimary: '#0a0d0b',
  bgSecondary: '#111113',
  bgTertiary: '#1a1a1c',
  
  // Semantic
  success: '#4ade80',
  warning: '#f59e0b',
  error: '#ef4444',
};
```

### Typography
- Headers: 18px, weight 600
- Labels: 12px, weight 600
- Body: 13-14px, weight 400
- Hints: 11px, weight 400, muted color

### Spacing
- Modal padding: 24px
- Section margin: 24px
- Form group margin: 16px
- Element gap: 12px (standard), 8px (tight)

### Border Radius
- Cards: 16px
- Buttons: 8px
- Pills/Tags: 16-20px
- Inputs: 8px

---

## 🏛️ GOVERNANCE ALIGNMENT

All components respect CHE·NU's core principle:

> **GOUVERNANCE > EXÉCUTION**

### How This Manifests

1. **ThreadEditor:**
   - Require approval for edit/share/delete operations
   - Control agent execution with token limits
   - Audit trail with hash chain integrity

2. **MeetingEditor:**
   - Consent management for recording and AI
   - Auto-generation controls for artifacts
   - Token budget limits for agent participation

3. **ResizablePanels:**
   - Layout persistence respects user preferences
   - No tracking or analytics on resize behavior

---

## 📊 METRICS

| Metric | Value |
|--------|-------|
| Total lines of code | 6,993 |
| ThreadEditor lines | 2,252 |
| MeetingEditor lines | 2,490 |
| ResizablePanels lines | 1,227 |
| Integration lines | 1,024 |
| TypeScript interfaces | ~50 |
| Design tokens used | 15+ |
| Keyboard shortcuts | 2 per editor |

---

## ✅ QUALITY CHECKLIST

- [x] TypeScript strict mode compatible
- [x] React hooks best practices
- [x] Memoization for performance
- [x] Accessibility (keyboard, ARIA)
- [x] Error handling (validation, dirty state)
- [x] CHE·NU design system alignment
- [x] Governance principles respected
- [x] Documentation complete

---

*Document created as part of CHE·NU V50 Phase 3 implementation*
*GOUVERNANCE > EXÉCUTION*
