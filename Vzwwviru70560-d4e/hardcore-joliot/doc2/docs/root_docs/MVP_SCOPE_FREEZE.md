# CHE·NU™ — MVP SCOPE FREEZE

> **VERSION:** V1 FREEZE  
> **STATUS:** LOCKED  
> **PURPOSE:** Define exactly what is included/excluded in MVP

---

## ⚠️ SCOPE LOCK NOTICE

This document **locks** the MVP scope.

- Features listed as INCLUDED → must be delivered
- Features listed as EXCLUDED → must NOT be developed
- No scope creep allowed
- Changes require formal approval process

---

## 1. MVP DEFINITION

### 1.1 What MVP Means for CHE·NU

The MVP (Minimum Viable Product) delivers:
- Core value proposition demonstrable
- Essential workflows functional
- Governance model operational
- Foundation for scaling

The MVP does NOT deliver:
- All planned features
- Enterprise customization
- Advanced AI capabilities
- Full XR experience

### 1.2 MVP Success Criteria

| Criterion | Metric | Target |
|-----------|--------|--------|
| Core navigation | 8 spheres accessible | 100% |
| Bureau structure | 10 sections per sphere | 100% |
| Thread creation | Create/manage threads | Functional |
| Token tracking | Budget visibility | Operational |
| Agent interaction | Nova responses | Working |
| Governance | Pipeline enforced | Active |

---

## 2. INCLUDED IN MVP ✅

### 2.1 Core System

| Feature | Status | Notes |
|---------|--------|-------|
| 8 Spheres navigation | ✅ INCLUDED | All 8 spheres accessible |
| 10 Bureau sections | ✅ INCLUDED | Full structure per sphere |
| 3 Hub layout | ✅ INCLUDED | Center/Left/Bottom |
| User authentication | ✅ INCLUDED | Login/Register/Logout |
| Session management | ✅ INCLUDED | Secure sessions |

### 2.2 Thread System

| Feature | Status | Notes |
|---------|--------|-------|
| Create thread | ✅ INCLUDED | In any sphere |
| Send messages | ✅ INCLUDED | User ↔ AI |
| Thread history | ✅ INCLUDED | Persistent |
| Thread status | ✅ INCLUDED | Active/Paused/Completed |
| Basic encoding | ✅ INCLUDED | Standard mode only |

### 2.3 Token System

| Feature | Status | Notes |
|---------|--------|-------|
| Token balance display | ✅ INCLUDED | Per user |
| Budget per sphere | ✅ INCLUDED | Configurable |
| Consumption tracking | ✅ INCLUDED | Per action |
| Transaction history | ✅ INCLUDED | Read-only |

### 2.4 Agent System

| Feature | Status | Notes |
|---------|--------|-------|
| Nova presence | ✅ INCLUDED | Always available |
| Nova basic responses | ✅ INCLUDED | Guidance/help |
| Agent status display | ✅ INCLUDED | Active/Idle |
| Single orchestrator | ✅ INCLUDED | Default assigned |

### 2.5 Governance

| Feature | Status | Notes |
|---------|--------|-------|
| Scope validation | ✅ INCLUDED | Per sphere |
| Budget validation | ✅ INCLUDED | Before execution |
| Basic audit log | ✅ INCLUDED | Action tracking |
| Governance pipeline | ✅ INCLUDED | 10-step flow |

### 2.6 UI/UX

| Feature | Status | Notes |
|---------|--------|-------|
| Desktop layout | ✅ INCLUDED | Primary target |
| Mobile responsive | ✅ INCLUDED | Basic support |
| Dark theme | ✅ INCLUDED | Default |
| Light theme | ✅ INCLUDED | Alternative |
| Brand colors | ✅ INCLUDED | CHE·NU palette |

### 2.7 Data

| Feature | Status | Notes |
|---------|--------|-------|
| User profile | ✅ INCLUDED | Basic fields |
| Thread storage | ✅ INCLUDED | PostgreSQL |
| Token records | ✅ INCLUDED | Full history |
| Activity logs | ✅ INCLUDED | 90 days |

---

## 3. EXCLUDED FROM MVP ❌

### 3.1 Deferred Features (Post-MVP)

| Feature | Status | Reason | Target |
|---------|--------|--------|--------|
| Multiple orchestrators | ❌ EXCLUDED | Complexity | V2 |
| Specialist agents marketplace | ❌ EXCLUDED | Infrastructure | V2 |
| Advanced encoding modes | ❌ EXCLUDED | R&D needed | V2 |
| XR/VR interface | ❌ EXCLUDED | Hardware dependency | V3 |
| Voice interaction | ❌ EXCLUDED | Integration complexity | V2 |
| Multi-language UI | ❌ EXCLUDED | Translation effort | V2 |
| Offline mode | ❌ EXCLUDED | Sync complexity | V3 |
| Native mobile apps | ❌ EXCLUDED | Dev resources | V2 |

### 3.2 Enterprise Features (Post-MVP)

| Feature | Status | Reason |
|---------|--------|--------|
| SSO/SAML integration | ❌ EXCLUDED | Enterprise scope |
| Custom branding | ❌ EXCLUDED | Enterprise scope |
| Admin console | ❌ EXCLUDED | Enterprise scope |
| Team management | ❌ EXCLUDED | Enterprise scope |
| API rate limiting | ❌ EXCLUDED | Scale concern |
| Custom data residency | ❌ EXCLUDED | Infrastructure |

### 3.3 Advanced AI (Post-MVP)

| Feature | Status | Reason |
|---------|--------|--------|
| Multi-agent coordination | ❌ EXCLUDED | Complexity |
| Autonomous workflows | ❌ EXCLUDED | Governance risk |
| Learning from user | ❌ EXCLUDED | Privacy concerns |
| Cross-sphere insights | ❌ EXCLUDED | Isolation model |
| Predictive suggestions | ❌ EXCLUDED | Data requirements |

### 3.4 Integrations (Post-MVP)

| Feature | Status | Reason |
|---------|--------|--------|
| Calendar sync | ❌ EXCLUDED | API dependency |
| Email integration | ❌ EXCLUDED | Security scope |
| File storage (Drive, etc) | ❌ EXCLUDED | OAuth complexity |
| Third-party agents | ❌ EXCLUDED | Marketplace needed |
| Webhook automation | ❌ EXCLUDED | Infrastructure |

---

## 4. MVP BOUNDARIES

### 4.1 Sphere Limitations

| Sphere | MVP Support |
|--------|-------------|
| Personal | Full bureau, basic features |
| Business | Full bureau, basic features |
| Government | Full bureau, basic features |
| Studio | Full bureau, basic features |
| Community | Full bureau, basic features |
| Social | Full bureau, basic features |
| Entertainment | Full bureau, basic features |
| Team | Full bureau, basic features |

**All 8 spheres have identical MVP functionality.**

### 4.2 Bureau Section Limitations

| Section | MVP Support |
|---------|-------------|
| Dashboard | Basic overview only |
| Notes | CRUD operations |
| Tasks | CRUD, no automation |
| Projects | CRUD, no dependencies |
| Threads | Full thread support |
| Meetings | CRUD, no sync |
| Data | Basic dataspace, no import |
| Agents | View only, no hiring |
| Reports | Basic activity log |
| Budget | View and basic allocation |

### 4.3 Technical Limitations

| Area | MVP Limit |
|------|-----------|
| Concurrent users | 1,000 |
| Threads per user | 100 |
| Messages per thread | 500 |
| Tokens per month | 50,000 (free tier) |
| File uploads | Not supported |
| API rate | 100 req/min |

---

## 5. NON-EXTENSION RULES

### 5.1 Scope Creep Prevention

```
┌─────────────────────────────────────────────┐
│  RULE: No feature additions during MVP      │
├─────────────────────────────────────────────┤
│  • New feature requests → backlog           │
│  • "Quick additions" → denied               │
│  • "Small enhancements" → post-MVP          │
│  • Only bug fixes allowed                   │
└─────────────────────────────────────────────┘
```

### 5.2 Exception Process

To add any feature to MVP scope:

1. **Document the request** - Written justification
2. **Impact assessment** - Timeline, resources, risk
3. **Remove equivalent scope** - Zero-sum rule
4. **Approval required** - Product + Engineering leads
5. **Update this document** - Formal amendment

### 5.3 Bug vs Feature

| Classification | Action | Example |
|---------------|--------|---------|
| **Bug** | Fix immediately | Thread doesn't save |
| **Enhancement** | Post-MVP | Better thread search |
| **New feature** | Post-MVP | Voice messages |
| **Missing spec** | Clarify, then decide | Edge case handling |

---

## 6. MVP EXIT CRITERIA

### 6.1 Required for Launch

| Criterion | Measurement | Required |
|-----------|-------------|----------|
| Core flows working | QA pass rate | > 95% |
| Performance | Page load | < 3s |
| Stability | Uptime | > 99% |
| Security | Vulnerability scan | 0 critical |
| Documentation | Coverage | 100% |

### 6.2 Launch Checklist

- [ ] All INCLUDED features functional
- [ ] All EXCLUDED features confirmed absent
- [ ] Governance pipeline operational
- [ ] Token tracking accurate
- [ ] Audit logging active
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] Documentation complete

### 6.3 Post-MVP Transition

After MVP launch:
1. Gather user feedback (30 days)
2. Prioritize V2 features
3. Update roadmap
4. Begin V2 development

---

## 7. FEATURE MATRIX SUMMARY

```
┌─────────────────────────────────────────────────────────────┐
│                    MVP FEATURE MATRIX                        │
├─────────────────────────────────────────────────────────────┤
│  ✅ INCLUDED                    │  ❌ EXCLUDED               │
├─────────────────────────────────┼───────────────────────────┤
│  8 Spheres                      │  9th Sphere               │
│  10 Bureau Sections             │  Custom Sections          │
│  Thread System                  │  Advanced Encoding        │
│  Token Tracking                 │  Token Trading            │
│  Nova Basic                     │  Multi-Agent              │
│  Governance Pipeline            │  Autonomous AI            │
│  Desktop + Mobile Web           │  Native Apps              │
│  Dark/Light Themes              │  Custom Themes            │
│  Basic Audit                    │  Advanced Analytics       │
│  User Auth                      │  SSO/SAML                 │
└─────────────────────────────────┴───────────────────────────┘
```

---

## 8. VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| V1 FREEZE | 2024 | Initial MVP scope lock |

---

**END OF MVP SCOPE FREEZE**

*This document defines the immutable MVP scope.*
