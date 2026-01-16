# 📋 CHE·NU™ v40 → v50 — 100 TÂCHES EN 10 SPRINTS

**Objectif:** Score 67/100 → 90/100  
**Durée estimée:** 10 sprints × 1 semaine = 10 semaines  
**Livrables:** Produit production-ready sur 3 plateformes  

---

## 📊 VUE D'ENSEMBLE

| Sprint | Focus | Tâches | Score Cible |
|--------|-------|--------|-------------|
| 1 | Tests Fondation | 1-10 | 70/100 |
| 2 | Tests Avancés | 11-20 | 73/100 |
| 3 | CI/CD & Qualité | 21-30 | 75/100 |
| 4 | Mobile Core | 31-40 | 78/100 |
| 5 | Mobile Complet | 41-50 | 80/100 |
| 6 | Desktop | 51-60 | 82/100 |
| 7 | Intégrations Core | 61-70 | 84/100 |
| 8 | UI/UX Design System | 71-80 | 86/100 |
| 9 | Features Avancées | 81-90 | 88/100 |
| 10 | Polish & Launch | 91-100 | 90/100 |

---

## 🏃 SPRINT 1: TESTS FONDATION
**Focus:** Infrastructure de tests + tests stores  
**Score:** 67 → 70

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 1 | Installer Vitest + Testing Library | package.json, vitest.config.ts | 🔴 | 1h |
| 2 | Créer setup.ts avec mocks globaux | frontend/src/tests/setup.ts | 🔴 | 2h |
| 3 | Test sphereStore.ts (10 tests) | stores/sphereStore.test.ts | 🔴 | 3h |
| 4 | Test governanceStore.ts (10 tests) | stores/governanceStore.test.ts | 🔴 | 3h |
| 5 | Test authStore.ts (8 tests) | stores/authStore.test.ts | 🔴 | 2h |
| 6 | Test agentStore.ts (8 tests) | stores/agentStore.test.ts | 🟠 | 2h |
| 7 | Test threadStore.ts (8 tests) | stores/threadStore.test.ts | 🟠 | 2h |
| 8 | Test meetingStore.ts (6 tests) | stores/meetingStore.test.ts | 🟠 | 2h |
| 9 | Configurer coverage report | vitest.config.ts | 🔴 | 1h |
| 10 | Documenter patterns de tests | docs/TESTING_GUIDE.md | 🟡 | 2h |

**Livrables Sprint 1:**
- [ ] 50+ tests stores
- [ ] Coverage > 25%
- [ ] Guide de tests

---

## 🏃 SPRINT 2: TESTS AVANCÉS
**Focus:** Tests hooks + utils + schemas  
**Score:** 70 → 73

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 11 | Test useAuth.ts (8 tests) | hooks/useAuth.test.ts | 🔴 | 2h |
| 12 | Test useNavigation.ts (8 tests) | hooks/useNavigation.test.ts | 🔴 | 2h |
| 13 | Test useAccessibility.ts (6 tests) | hooks/useAccessibility.test.ts | 🟠 | 2h |
| 14 | Test useGovernance.ts (8 tests) | hooks/useGovernance.test.ts | 🔴 | 2h |
| 15 | Test security.ts (10 tests) | utils/security.test.ts | 🔴 | 3h |
| 16 | Test validation.ts (10 tests) | utils/validation.test.ts | 🔴 | 3h |
| 17 | Test schemas/index.ts (15 tests) | schemas/index.test.ts | 🔴 | 3h |
| 18 | Test navMachine.ts (10 tests) | navigation/navMachine.test.ts | 🟠 | 3h |
| 19 | Test i18n.ts (8 tests) | i18n/i18n.test.ts | 🟡 | 2h |
| 20 | Intégrer tests dans pre-commit | .husky/pre-commit | 🔴 | 1h |

**Livrables Sprint 2:**
- [ ] 100+ tests total
- [ ] Coverage > 40%
- [ ] Pre-commit hooks

---

## 🏃 SPRINT 3: CI/CD & QUALITÉ
**Focus:** Pipeline + E2E + linting  
**Score:** 73 → 75

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 21 | Créer workflow GitHub Actions CI | .github/workflows/ci.yml | 🔴 | 2h |
| 22 | Ajouter job lint | .github/workflows/ci.yml | 🔴 | 1h |
| 23 | Ajouter job test + coverage | .github/workflows/ci.yml | 🔴 | 1h |
| 24 | Ajouter job build | .github/workflows/ci.yml | 🔴 | 1h |
| 25 | Configurer ESLint strict | .eslintrc.cjs | 🔴 | 2h |
| 26 | Configurer Prettier | .prettierrc | 🟠 | 1h |
| 27 | E2E test auth flow | e2e/auth.spec.ts | 🔴 | 3h |
| 28 | E2E test sphere navigation | e2e/spheres.spec.ts | 🔴 | 3h |
| 29 | E2E test bureau sections | e2e/bureau.spec.ts | 🟠 | 3h |
| 30 | Configurer branch protection | GitHub Settings | 🔴 | 1h |

**Livrables Sprint 3:**
- [ ] CI/CD fonctionnel
- [ ] 3 E2E tests
- [ ] Branch protection

---

## 🏃 SPRINT 4: MOBILE CORE
**Focus:** Architecture mobile + navigation  
**Score:** 75 → 78

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 31 | Migrer vers Expo Router | mobile/app/_layout.tsx | 🔴 | 3h |
| 32 | Créer RootNavigator | mobile/src/navigation/Root.tsx | 🔴 | 2h |
| 33 | Créer TabNavigator (9 sphères) | mobile/src/navigation/Tabs.tsx | 🔴 | 3h |
| 34 | Synchro sphereStore mobile | mobile/src/stores/sphereStore.ts | 🔴 | 3h |
| 35 | Synchro authStore mobile | mobile/src/stores/authStore.ts | 🔴 | 2h |
| 36 | Créer SphereCard component | mobile/src/components/SphereCard.tsx | 🟠 | 2h |
| 37 | Créer SphereSelector | mobile/src/components/SphereSelector.tsx | 🟠 | 2h |
| 38 | Créer SphereBureau | mobile/src/components/SphereBureau.tsx | 🔴 | 3h |
| 39 | Implémenter thème CHE·NU | mobile/src/theme/index.ts | 🟠 | 2h |
| 40 | Tester sur Android Emulator | - | 🔴 | 2h |

**Livrables Sprint 4:**
- [ ] Navigation mobile fonctionnelle
- [ ] 9 sphères accessibles
- [ ] Thème appliqué

---

## 🏃 SPRINT 5: MOBILE COMPLET
**Focus:** 6 sections bureau + auth  
**Score:** 78 → 80

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 41 | Créer QuickCapture section | mobile/src/components/bureau/QuickCapture.tsx | 🔴 | 2h |
| 42 | Créer ResumeWorkspace section | mobile/src/components/bureau/ResumeWorkspace.tsx | 🔴 | 2h |
| 43 | Créer Threads section | mobile/src/components/bureau/Threads.tsx | 🔴 | 3h |
| 44 | Créer DataFiles section | mobile/src/components/bureau/DataFiles.tsx | 🟠 | 2h |
| 45 | Créer ActiveAgents section | mobile/src/components/bureau/ActiveAgents.tsx | 🟠 | 2h |
| 46 | Créer Meetings section | mobile/src/components/bureau/Meetings.tsx | 🟠 | 2h |
| 47 | Implémenter auth flow | mobile/src/screens/Auth/ | 🔴 | 3h |
| 48 | Ajouter biometric auth | mobile/src/services/biometric.ts | 🟡 | 2h |
| 49 | Tester sur iOS Simulator | - | 🔴 | 2h |
| 50 | Créer 10 tests mobile | mobile/src/__tests__/ | 🟠 | 3h |

**Livrables Sprint 5:**
- [ ] 6 sections bureau mobile
- [ ] Auth complet
- [ ] Tests mobile

---

## 🏃 SPRINT 6: DESKTOP
**Focus:** Electron app complète  
**Score:** 80 → 82

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 51 | Compléter main.js features | desktop/src/main.js | 🔴 | 2h |
| 52 | Implémenter auto-updater | desktop/src/autoUpdate.ts | 🔴 | 3h |
| 53 | Créer system tray | desktop/src/tray.ts | 🟠 | 2h |
| 54 | Implémenter deep links | desktop/src/deepLinks.ts | 🟠 | 2h |
| 55 | Global keyboard shortcuts | desktop/src/shortcuts.ts | 🟠 | 2h |
| 56 | Native notifications | desktop/src/notifications.ts | 🟠 | 2h |
| 57 | File system access | desktop/src/fileSystem.ts | 🔴 | 3h |
| 58 | Build macOS | electron-builder | 🔴 | 2h |
| 59 | Build Windows | electron-builder | 🔴 | 2h |
| 60 | Code signing setup | - | 🟠 | 3h |

**Livrables Sprint 6:**
- [ ] Desktop app complète
- [ ] Builds Mac/Win
- [ ] Auto-update

---

## 🏃 SPRINT 7: INTÉGRATIONS CORE
**Focus:** Paiements + Storage + Calendar  
**Score:** 82 → 84

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 61 | Stripe SDK backend | backend/services/stripe/ | 🔴 | 3h |
| 62 | Stripe webhooks | backend/services/stripe/webhook.ts | 🔴 | 2h |
| 63 | Subscriptions logic | backend/services/stripe/subscription.ts | 🔴 | 3h |
| 64 | Checkout UI frontend | frontend/src/components/payment/ | 🔴 | 3h |
| 65 | AWS S3 integration | backend/services/storage/ | 🔴 | 3h |
| 66 | Presigned URLs | backend/services/storage/presign.ts | 🟠 | 2h |
| 67 | Google Calendar OAuth | backend/services/calendar/ | 🟠 | 3h |
| 68 | Calendar sync service | backend/services/calendar/sync.ts | 🟠 | 2h |
| 69 | SendGrid email | backend/services/email/ | 🟡 | 2h |
| 70 | Email templates | backend/services/email/templates/ | 🟡 | 2h |

**Livrables Sprint 7:**
- [ ] Paiements Stripe
- [ ] Storage S3
- [ ] Calendar sync

---

## 🏃 SPRINT 8: UI/UX DESIGN SYSTEM
**Focus:** Storybook + Composants  
**Score:** 84 → 86

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 71 | Setup Storybook 8 | .storybook/ | 🔴 | 2h |
| 72 | Button component + stories | components/ui/Button/ | 🔴 | 2h |
| 73 | Input component + stories | components/ui/Input/ | 🔴 | 2h |
| 74 | Select component + stories | components/ui/Select/ | 🔴 | 2h |
| 75 | Modal component + stories | components/ui/Modal/ | 🔴 | 2h |
| 76 | Card component + stories | components/ui/Card/ | 🟠 | 2h |
| 77 | Table component + stories | components/ui/Table/ | 🔴 | 3h |
| 78 | Form component + validation | components/ui/Form/ | 🔴 | 3h |
| 79 | Toast notification system | components/ui/Toast/ | 🟠 | 2h |
| 80 | Déployer Storybook (Chromatic) | - | 🟠 | 2h |

**Livrables Sprint 8:**
- [ ] 10+ composants UI
- [ ] Storybook déployé
- [ ] Design tokens

---

## 🏃 SPRINT 9: FEATURES AVANCÉES
**Focus:** Collaboration + WebSocket  
**Score:** 86 → 88

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 81 | WebSocket gateway | backend/services/realtime/gateway.ts | 🔴 | 3h |
| 82 | Presence service | backend/services/realtime/presence.ts | 🔴 | 2h |
| 83 | Cursor sync | backend/services/realtime/cursors.ts | 🟠 | 2h |
| 84 | Thread real-time | backend/services/realtime/threads.ts | 🔴 | 3h |
| 85 | Typing indicators | frontend/src/components/Typing.tsx | 🟡 | 2h |
| 86 | Slack integration | backend/services/slack/ | 🟠 | 3h |
| 87 | Webhook system | backend/services/webhooks/ | 🟠 | 2h |
| 88 | API rate limiting | backend/middleware/rateLimit.ts | 🔴 | 2h |
| 89 | Request logging | backend/middleware/logging.ts | 🟠 | 2h |
| 90 | Error tracking (Sentry) | frontend/src/services/sentry.ts | 🟠 | 2h |

**Livrables Sprint 9:**
- [ ] Collaboration temps-réel
- [ ] Slack integration
- [ ] Error tracking

---

## 🏃 SPRINT 10: POLISH & LAUNCH
**Focus:** Performance + Accessibilité + Documentation  
**Score:** 88 → 90

| # | Tâche | Fichier(s) | Priorité | Temps |
|---|-------|------------|----------|-------|
| 91 | Code splitting | vite.config.ts | 🔴 | 2h |
| 92 | Lazy loading routes | frontend/src/routes/ | 🔴 | 2h |
| 93 | Image optimization | frontend/src/utils/images.ts | 🟠 | 2h |
| 94 | Bundle analysis | - | 🟠 | 1h |
| 95 | WCAG 2.1 audit | - | 🔴 | 3h |
| 96 | Keyboard navigation | frontend/src/hooks/useKeyboard.ts | 🔴 | 2h |
| 97 | Screen reader support | - | 🟠 | 2h |
| 98 | SEO optimization | frontend/index.html | 🟡 | 2h |
| 99 | Documentation finale | docs/USER_GUIDE.md | 🔴 | 3h |
| 100 | Release v50.0.0 | CHANGELOG.md | 🔴 | 2h |

**Livrables Sprint 10:**
- [ ] Lighthouse > 90
- [ ] WCAG 2.1 AA
- [ ] v50 released

---

## 📊 TRACKING PROGRESSION

### Template de Suivi

```markdown
## Sprint [X] — Semaine du [DATE]

### Tâches Complétées ✅
- [ ] Tâche #XX: [Description]
- [ ] Tâche #XX: [Description]

### Tâches En Cours 🔄
- [ ] Tâche #XX: [Description] — [XX%]

### Blocages 🚫
- [Description du blocage]

### Décisions Prises 📝
- [Décision et justification]

### Score Atteint: [XX]/100
```

---

## 🎯 CRITÈRES DE SUCCÈS PAR SPRINT

| Sprint | Critère Principal | Validation |
|--------|-------------------|------------|
| 1 | 50 tests stores | `npm test` pass |
| 2 | 100 tests total | Coverage > 40% |
| 3 | CI/CD vert | GitHub Actions pass |
| 4 | Nav mobile | 9 sphères accessibles |
| 5 | Bureau mobile | 6 sections fonctionnelles |
| 6 | Desktop builds | Mac + Win executables |
| 7 | Paiements | Stripe test mode OK |
| 8 | Storybook | URL publique |
| 9 | Realtime | WebSocket connections |
| 10 | Launch | v50.0.0 tagged |

---

*Document créé le 20 décembre 2025*
*100 tâches — 10 sprints — Objectif: 90/100*
