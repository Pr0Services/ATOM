# 🚀 CHE·NU™ v40 — PLAN D'AMÉLIORATION DÉTAILLÉ

**Objectif:** Passer de **67/100** à **90/100** en 12 mois

---

## 📊 SCORE ACTUEL PAR CATÉGORIE

| Catégorie | Score Actuel | Cible 3 mois | Cible 6 mois | Cible 12 mois |
|-----------|--------------|--------------|--------------|---------------|
| Architecture | 82 | 85 | 88 | 92 |
| Fonctionnalités | 71 | 75 | 80 | 88 |
| UI/UX | 58 | 70 | 78 | 85 |
| Tests | 45 | 65 | 75 | 85 |
| Intégrations | 52 | 65 | 75 | 88 |
| Documentation | 85 | 88 | 90 | 95 |
| Multi-plateforme | 48 | 65 | 78 | 88 |
| **GLOBAL** | **67** | **75** | **82** | **90** |

---

## 🔴 PHASE 1: FONDATIONS (Semaines 1-12)

### Sprint 1-2: Tests & CI/CD

#### Tests Unitaires (Priorité: CRITIQUE)
```
Fichiers à créer:
├── frontend/src/__tests__/
│   ├── stores/
│   │   ├── sphereStore.test.ts
│   │   ├── governanceStore.test.ts
│   │   ├── agentStore.test.ts
│   │   └── authStore.test.ts
│   ├── hooks/
│   │   ├── useAuth.test.ts
│   │   ├── useAccessibility.test.ts
│   │   └── useNavigation.test.ts
│   ├── components/
│   │   ├── bureau/BureauSections.test.tsx
│   │   ├── sphere/SphereProvider.test.tsx
│   │   └── navigation/NavMachine.test.tsx
│   └── utils/
│       ├── security.test.ts
│       └── validation.test.ts
```

**Tâches:**
- [ ] Installer Vitest + Testing Library
- [ ] Créer setup.ts avec mocks globaux
- [ ] Écrire 50 tests stores
- [ ] Écrire 50 tests hooks
- [ ] Écrire 30 tests composants
- [ ] Écrire 20 tests utils
- [ ] Configurer coverage report (cible: 60%)

#### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run test:coverage
      - run: npm run build
```

**Tâches:**
- [ ] Créer workflow GitHub Actions
- [ ] Ajouter lint check
- [ ] Ajouter test check
- [ ] Ajouter build check
- [ ] Configurer branch protection

---

### Sprint 3-4: Mobile Refactor

#### Structure Cible Mobile
```
mobile/
├── src/
│   ├── app/                    # App entry + providers
│   │   ├── _layout.tsx
│   │   └── index.tsx
│   ├── components/
│   │   ├── bureau/             # 6 sections
│   │   │   ├── QuickCapture.tsx
│   │   │   ├── ResumeWorkspace.tsx
│   │   │   ├── Threads.tsx
│   │   │   ├── DataFiles.tsx
│   │   │   ├── ActiveAgents.tsx
│   │   │   └── Meetings.tsx
│   │   ├── sphere/             # 9 sphères
│   │   │   ├── SphereCard.tsx
│   │   │   ├── SphereSelector.tsx
│   │   │   └── SphereBureau.tsx
│   │   └── ui/                 # Composants réutilisables
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       └── Modal.tsx
│   ├── constants/
│   │   └── canonical.ts        # ✅ FAIT
│   ├── stores/
│   │   ├── sphereStore.ts      # Synced with web
│   │   ├── authStore.ts
│   │   └── index.ts
│   ├── navigation/
│   │   ├── RootNavigator.tsx
│   │   └── TabNavigator.tsx
│   └── types/
│       └── index.ts            # ✅ FAIT
```

**Tâches:**
- [ ] Migrer vers Expo Router
- [ ] Créer 6 composants bureau
- [ ] Créer 9 composants sphère
- [ ] Synchroniser stores avec web
- [ ] Implémenter navigation tabs
- [ ] Ajouter authentification
- [ ] Tester sur Android/iOS

---

### Sprint 5-6: Design System

#### Storybook Setup
```
frontend/
├── .storybook/
│   ├── main.ts
│   ├── preview.ts
│   └── theme.ts
├── src/
│   └── components/
│       └── ui/
│           ├── Button/
│           │   ├── Button.tsx
│           │   ├── Button.stories.tsx
│           │   └── Button.test.tsx
│           ├── Input/
│           ├── Card/
│           ├── Modal/
│           ├── Form/
│           ├── Table/
│           └── Chart/
```

#### Composants UI à Créer
| Composant | Variantes | Priorité |
|-----------|-----------|----------|
| Button | primary, secondary, ghost, danger | 🔴 |
| Input | text, password, email, search, textarea | 🔴 |
| Select | single, multi, searchable | 🔴 |
| Checkbox | single, group | 🟠 |
| Radio | single, group | 🟠 |
| Switch | default, with label | 🟠 |
| Modal | default, confirm, form | 🔴 |
| Dialog | alert, confirm, prompt | 🟠 |
| Toast | success, error, warning, info | 🔴 |
| Card | default, interactive, stats | 🟠 |
| Table | sortable, filterable, paginated | 🔴 |
| Form | with validation, multi-step | 🔴 |
| DatePicker | single, range | 🟠 |
| FileUpload | single, multiple, drag-drop | 🟠 |
| Avatar | image, initials, status | 🟡 |
| Badge | default, dot, count | 🟡 |
| Progress | bar, circular, steps | 🟡 |
| Skeleton | text, card, table | 🟡 |
| Tooltip | default, rich | 🟡 |
| Dropdown | menu, select | 🟠 |

**Tâches:**
- [ ] Installer Storybook 8
- [ ] Configurer avec Tailwind
- [ ] Créer 10 composants core
- [ ] Créer 10 composants form
- [ ] Créer 5 composants feedback
- [ ] Documenter tous les composants
- [ ] Déployer Storybook (Chromatic)

---

## 🟠 PHASE 2: FEATURES (Semaines 13-24)

### Sprint 7-8: Paiements (Stripe)

#### Structure
```
backend/services/payments/
├── src/
│   ├── stripe.service.ts
│   ├── webhook.handler.ts
│   ├── subscription.service.ts
│   └── invoice.service.ts
frontend/src/
├── components/payment/
│   ├── PricingTable.tsx
│   ├── CheckoutForm.tsx
│   ├── BillingPortal.tsx
│   └── UsageDisplay.tsx
```

**Tâches:**
- [ ] Créer compte Stripe
- [ ] Implémenter Stripe SDK backend
- [ ] Créer webhook handler
- [ ] Implémenter subscriptions
- [ ] Créer UI checkout
- [ ] Créer billing portal
- [ ] Tester sandbox complet

---

### Sprint 9-10: Collaboration Temps-Réel

#### Architecture WebSocket
```
backend/services/realtime/
├── src/
│   ├── socket.gateway.ts
│   ├── presence.service.ts
│   ├── sync.service.ts
│   └── events/
│       ├── thread.events.ts
│       ├── cursor.events.ts
│       └── edit.events.ts
```

**Features:**
- [ ] Presence (qui est en ligne)
- [ ] Curseurs collaboratifs
- [ ] Édition simultanée
- [ ] Sync threads temps-réel
- [ ] Notifications push
- [ ] Typing indicators

---

### Sprint 11-12: Intégrations

#### Calendrier
```
Intégrations à implémenter:
├── Google Calendar
├── Microsoft Outlook
├── Apple Calendar (CalDAV)
└── Cal.com / Calendly
```

#### Storage
```
Providers:
├── AWS S3
├── Google Cloud Storage
├── Cloudflare R2
└── Local (dev)
```

#### Communication
```
Intégrations:
├── Slack
├── Microsoft Teams
├── Discord
└── Email (SendGrid/Resend)
```

**Tâches:**
- [ ] OAuth2 Google Calendar
- [ ] OAuth2 Microsoft Graph
- [ ] S3 SDK + presigned URLs
- [ ] Slack App + webhooks
- [ ] Email templates + service

---

## 🟢 PHASE 3: SCALE (Semaines 25-52)

### Sprint 13-16: Desktop Complet

#### Electron Features
```
desktop/src/
├── main/
│   ├── main.ts
│   ├── preload.ts
│   ├── ipc/
│   │   ├── file.ipc.ts
│   │   ├── notification.ipc.ts
│   │   └── system.ipc.ts
│   └── menu/
│       └── app.menu.ts
├── features/
│   ├── tray.ts           # System tray
│   ├── autoUpdate.ts     # Auto-updater
│   ├── deepLinks.ts      # chenu:// protocol
│   └── shortcuts.ts      # Global shortcuts
```

**Tâches:**
- [ ] Auto-updater (electron-updater)
- [ ] System tray avec menu
- [ ] Deep links (chenu://)
- [ ] Notifications natives
- [ ] Global shortcuts
- [ ] File system access
- [ ] Build Mac/Win/Linux
- [ ] Code signing

---

### Sprint 17-20: API Marketplace

#### Architecture
```
backend/services/marketplace/
├── src/
│   ├── app.controller.ts
│   ├── app.service.ts
│   ├── integrations/
│   │   ├── registry.ts
│   │   ├── oauth.service.ts
│   │   └── webhook.service.ts
│   └── templates/
│       ├── notion.template.ts
│       ├── airtable.template.ts
│       └── zapier.template.ts
```

**Intégrations Marketplace:**
| App | Type | Priorité |
|-----|------|----------|
| Notion | Bidirectionnel | 🔴 |
| Airtable | Bidirectionnel | 🟠 |
| Zapier | Trigger/Action | 🔴 |
| Make | Trigger/Action | 🟠 |
| GitHub | Webhooks | 🟠 |
| Jira | Bidirectionnel | 🟡 |
| Linear | Bidirectionnel | 🟡 |
| Figma | Read | 🟡 |

---

### Sprint 21-24: Performance & Accessibility

#### Performance
```
Optimisations:
├── Code splitting
├── Lazy loading routes
├── Image optimization
├── Bundle analysis
├── Service Worker
├── Redis caching
└── Database indexing
```

#### Accessibility (WCAG 2.1 AA)
```
Checklist:
├── Keyboard navigation
├── Screen reader support
├── Color contrast (4.5:1)
├── Focus indicators
├── Alt text images
├── ARIA labels
├── Skip links
└── Reduced motion
```

---

## 📋 CHECKLIST RÉCAPITULATIVE

### Phase 1 (0-3 mois)
- [ ] 150 tests unitaires
- [ ] CI/CD GitHub Actions
- [ ] Mobile refactor complet
- [ ] Design System Storybook
- [ ] 25 composants UI

### Phase 2 (3-6 mois)
- [ ] Stripe integration
- [ ] WebSocket collaboration
- [ ] Google Calendar
- [ ] AWS S3 storage
- [ ] Slack integration

### Phase 3 (6-12 mois)
- [ ] Desktop complet
- [ ] API Marketplace
- [ ] Performance optimization
- [ ] WCAG 2.1 compliance
- [ ] 50 E2E tests

---

## 💰 ESTIMATION RESSOURCES

| Phase | Durée | Développeurs | Coût estimé |
|-------|-------|--------------|-------------|
| Phase 1 | 3 mois | 2 dev | $45,000 |
| Phase 2 | 3 mois | 3 dev | $67,500 |
| Phase 3 | 6 mois | 3 dev | $135,000 |
| **TOTAL** | **12 mois** | - | **$247,500** |

---

## 🎯 KPIs À SUIVRE

| Métrique | Actuel | Cible 3m | Cible 6m | Cible 12m |
|----------|--------|----------|----------|-----------|
| Test Coverage | 15% | 60% | 75% | 85% |
| Lighthouse Score | ? | 75 | 85 | 95 |
| Bundle Size | ? | <500kb | <400kb | <300kb |
| Time to First Byte | ? | <200ms | <150ms | <100ms |
| Mobile MAU | 0 | 100 | 1,000 | 10,000 |
| Desktop DAU | 0 | 50 | 500 | 5,000 |
| API Integrations | 2 | 5 | 15 | 30 |
| NPS Score | ? | 30 | 50 | 70 |

---

**Prochaine action:** Commencer Sprint 1 (Tests + CI/CD)

*Document créé le 20 décembre 2025*
