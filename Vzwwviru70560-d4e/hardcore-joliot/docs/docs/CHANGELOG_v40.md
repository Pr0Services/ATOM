# CHE·NU™ CHANGELOG

All notable changes to CHE·NU™ are documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [40.0.0] - 2025-12-20 🔒 FROZEN RELEASE

### 🔒 Architecture Frozen
- **SPHERE_COUNT = 9** (final, no changes allowed)
- **BUREAU_SECTION_COUNT = 6** (hard limit)
- **AGENT_COUNT = 226** (confirmed and documented)
- **GOVERNANCE_LAW_COUNT = 10** (complete)

### Added
- Unified documentation (SYSTEM_MANUAL_v40, MASTER_REFERENCE_v40)
- Complete agent distribution table (226 agents across 9 spheres + system)
- Rate limiting middleware with token bucket algorithm
- Redis caching layer (L1 Memory + L2 Redis)
- Background jobs system with Celery/RQ
- Health check endpoints
- PWA manifest and service worker
- Mobile responsiveness (100% coverage)
- E2E tests with Playwright
- CI/CD pipeline

### Changed
- Documentation synchronized to v40 format
- All references updated: 9 spheres, 6 sections, 226 agents
- API response headers include rate limit info
- Caching strategy unified across all services

### Fixed
- Inconsistent sphere counts in documentation (was 8/10, now 9)
- Inconsistent bureau section counts (was 10, now 6)
- Agent count discrepancies (was 168/200, now 226)

### Security
- Rate limiting prevents abuse
- Token bucket algorithm for fair usage
- Request validation on all endpoints

---

## [39.0.0] - 2025-12-15

### Added
- **Scholar sphere** (📚) - 9th sphere for learning and research
- Governance Law L10: DELETION_COMPLETENESS
- Scholar-specific agents (25 total)
- Research assistant capabilities
- Citation management features
- Note-taking enhancements

### Changed
- Bureau sections reduced from 10 to 6
  - Merged Dashboard + Notes → QUICK_CAPTURE
  - Merged Tasks + Projects → RESUME_WORKSPACE
  - Merged Reports/History → THREADS
  - Elevated Budget/Governance → System-wide
- Updated all sphere navigation
- Refined agent hierarchy documentation

### Removed
- Separate Dashboard section
- Separate Notes section  
- Separate Tasks section
- Separate Projects section
- Separate Reports section
- Bureau-level Budget section (now system-wide)

### Migration Notes
```sql
-- Bureau section migration v38 → v39
UPDATE bureau_sections SET id = 'quick_capture' WHERE id IN ('dashboard', 'notes');
UPDATE bureau_sections SET id = 'resume_workspace' WHERE id IN ('tasks', 'projects');
UPDATE bureau_sections SET id = 'threads' WHERE id IN ('threads', 'reports');
DELETE FROM bureau_sections WHERE id IN ('budget', 'governance');
```

---

## [38.0.0] - 2025-11-28

### Added
- Complete 8-sphere architecture
- 10 bureau sections per sphere
- 9 governance laws (L1-L9)
- 168 agents initial deployment
- Governed Execution Pipeline (10 steps)
- Thread system (.chenu format)
- Token budget system
- Semantic encoding layer
- Agent Compatibility Matrix (ACM)

### Architecture
- Hub 1: Communication (Nova, Agents, Messaging, Email)
- Hub 2: Navigation (Spheres, DataSpaces, Data, External)
- Hub 3: Workspace (Documents, Editors, Browser, Projects)

### Spheres (v38)
1. Personal 🏠
2. Business 💼
3. Government & Institutions 🏛️
4. Studio de Création 🎨
5. Community 👥
6. Social & Media 📱
7. Entertainment 🎬
8. My Team 🤝

### Bureau Sections (v38 - 10 sections)
1. Dashboard
2. Notes
3. Tasks
4. Projects
5. Threads
6. Meetings
7. Data/Database
8. Agents
9. Reports/History
10. Budget/Governance

---

## [37.0.0] - 2025-11-15

### Added
- XR Mode toggle (VR/AR interface)
- Immersive meeting rooms
- Spatial navigation
- 3D DataSpace visualization

### Changed
- Improved Three.js integration
- Enhanced WebXR support

---

## [36.0.0] - 2025-11-01

### Added
- Multi-language support (7 languages)
- Accessibility improvements (WCAG 2.1 AA)
- Dark/Light theme toggle

### Languages
- English (en)
- French (fr)
- Spanish (es)
- German (de)
- Portuguese (pt)
- Italian (it)
- Japanese (ja)

---

## [35.0.0] - 2025-10-15

### Added
- Immobilier domain (cross-sphere property management)
- Quebec-specific compliance features
- Tenant management
- Rental operations

---

## Version History Summary

| Version | Date | Key Changes |
|---------|------|-------------|
| **v40** | Dec 20, 2025 | 🔒 FROZEN: 9 spheres, 6 sections, 226 agents |
| v39 | Dec 15, 2025 | Added Scholar, reduced to 6 sections |
| v38 | Nov 28, 2025 | 8 spheres, 10 sections, 168 agents |
| v37 | Nov 15, 2025 | XR Mode |
| v36 | Nov 01, 2025 | i18n, accessibility |
| v35 | Oct 15, 2025 | Immobilier domain |

---

## Upgrade Guides

### v39 → v40

No breaking changes. Documentation updates only.

```bash
# Update documentation references
find . -name "*.md" -exec sed -i 's/v39/v40/g' {} \;

# Verify constants
npm run verify:constants
```

### v38 → v39

Breaking changes in bureau sections.

```typescript
// Old (v38)
const sections = ['dashboard', 'notes', 'tasks', 'projects', ...];

// New (v39+)
const sections = [
  'quick_capture',      // Replaces dashboard, notes
  'resume_workspace',   // Replaces tasks, projects
  'threads',
  'data_files',
  'active_agents',
  'meetings',
];
```

```sql
-- Database migration
ALTER TABLE bureau_items 
  ADD COLUMN section_v40 VARCHAR(50);

UPDATE bureau_items SET section_v40 = 
  CASE 
    WHEN section IN ('dashboard', 'notes') THEN 'quick_capture'
    WHEN section IN ('tasks', 'projects') THEN 'resume_workspace'
    WHEN section = 'threads' THEN 'threads'
    WHEN section IN ('data', 'database', 'files') THEN 'data_files'
    WHEN section = 'agents' THEN 'active_agents'
    WHEN section = 'meetings' THEN 'meetings'
    ELSE 'quick_capture'
  END;

ALTER TABLE bureau_items DROP COLUMN section;
ALTER TABLE bureau_items RENAME COLUMN section_v40 TO section;
```

---

*CHE·NU™ Changelog*
*Maintained by: Development Team*
*Last Updated: December 20, 2025*
