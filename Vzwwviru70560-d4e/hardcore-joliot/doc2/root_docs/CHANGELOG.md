# CHE·NU™ — CHANGELOG

> **FORMAT:** [Semantic Versioning](https://semver.org/)  
> **STYLE:** [Keep a Changelog](https://keepachangelog.com/)

---

## [Unreleased]

### Planned
- Agent marketplace integration
- Advanced encoding modes
- Multi-language support
- Native mobile applications

---

## [1.0.0] - 2024-XX-XX

### 🎉 Initial Release — MVP FREEZE

#### Added
- **8 Spheres System**
  - Personal (🏠)
  - Business (💼)
  - Government & Institutions (🏛️)
  - Studio de création (🎨)
  - Community (👥)
  - Social & Media (📱)
  - Entertainment (🎬)
  - My Team (🤝)

- **10 Bureau Sections** (per sphere)
  - Dashboard
  - Notes
  - Tasks
  - Projects
  - Threads (.chenu)
  - Meetings
  - Data / Database
  - Agents
  - Reports / History
  - Budget & Governance

- **Thread System**
  - Create/manage threads (.chenu)
  - Persistent conversation history
  - Token budgeting per thread
  - Basic encoding (standard mode)
  - Decision tracking
  - Audit logging

- **Token System**
  - Internal utility credits
  - Budget allocation per sphere
  - Consumption tracking
  - Transaction history
  - Governance rules

- **Agent System**
  - Nova (system intelligence) - always present
  - Default orchestrator
  - Agent status display
  - Scope-based permissions

- **Governance Pipeline**
  - 10-step execution flow
  - Intent classification
  - Scope validation
  - Budget verification
  - Audit logging

- **3 Hub Layout**
  - Center: Main workspace
  - Left: Navigation
  - Bottom/Right: Intelligence panel

- **User Authentication**
  - Registration
  - Login/Logout
  - Session management
  - JWT tokens

- **UI/UX**
  - Desktop-first design
  - Mobile responsive
  - Dark/Light themes
  - CHE·NU brand colors

- **Backend**
  - FastAPI REST API
  - SQLAlchemy ORM
  - PostgreSQL database
  - Redis caching
  - WebSocket real-time

- **Infrastructure**
  - Docker Compose setup
  - Kubernetes configs
  - CI/CD pipeline

- **Documentation**
  - Canonical memory (BIOS)
  - Governance policy
  - MVP scope freeze
  - System overview
  - API documentation
  - Deployment guide

#### Fixed
- N/A (initial release)

#### Changed
- N/A (initial release)

#### Deprecated
- N/A (initial release)

#### Removed
- N/A (initial release)

#### Security
- JWT-based authentication
- Password hashing (bcrypt)
- CORS configuration
- Rate limiting basics

---

## Version History Summary

| Version | Date | Milestone |
|---------|------|-----------|
| 1.0.0 | 2024-XX | MVP Release |
| 0.9.0 | 2024-XX | Beta Testing |
| 0.5.0 | 2024-XX | Alpha Release |
| 0.1.0 | 2024-XX | Initial Development |

---

## Architectural Decisions

### [ADR-001] 8 Spheres Frozen
- **Date:** 2024-XX
- **Status:** ACCEPTED
- **Decision:** Exactly 8 spheres, no additions/removals
- **Rationale:** Cognitive load optimization, clear context boundaries

### [ADR-002] 10 Bureau Sections Fixed
- **Date:** 2024-XX
- **Status:** ACCEPTED
- **Decision:** Same 10 sections for every sphere
- **Rationale:** Consistency, predictability, reduced learning curve

### [ADR-003] Tokens as Internal Utility
- **Date:** 2024-XX
- **Status:** ACCEPTED
- **Decision:** Tokens are NOT cryptocurrency
- **Rationale:** Regulatory clarity, simplicity, trust

### [ADR-004] Nova as System Agent
- **Date:** 2024-XX
- **Status:** ACCEPTED
- **Decision:** Nova is always present, cannot be hired/replaced
- **Rationale:** System integrity, governance enforcement

### [ADR-005] Governance Before Execution
- **Date:** 2024-XX
- **Status:** ACCEPTED
- **Decision:** All AI actions pass governance pipeline
- **Rationale:** Human control, cost visibility, audit trail

---

## Migration Notes

### Upgrading to 1.0.0
- Fresh installation recommended for MVP
- No migration path from pre-release versions
- Database schema finalized

---

## Contributors

- Core Team @ CHE·NU™
- Community Contributors (see CONTRIBUTORS.md)

---

## Links

- [CANONICAL_MEMORY.md](./CANONICAL_MEMORY.md) - Source of truth
- [GOVERNANCE_POLICY.md](./GOVERNANCE_POLICY.md) - Official policies
- [MVP_SCOPE_FREEZE.md](./MVP_SCOPE_FREEZE.md) - Scope definition
- [SYSTEM_OVERVIEW.md](./SYSTEM_OVERVIEW.md) - System introduction

---

**END OF CHANGELOG**
