# 📱 CHE·NU™ V71 — PARCOURS UTILISATEUR COMPLET

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    CARTOGRAPHIE COMPLÈTE DU USER JOURNEY                     ║
║                    Frontend A — Public SaaS (Mirror/Vitrine)                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Version:** V71 CANONICAL  
**Date:** Janvier 2026  
**Statut:** RÉFÉRENCE OFFICIELLE

---

## 🗺️ VUE D'ENSEMBLE DU PARCOURS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║  PHASE 1: DÉCOUVERTE (Public)                                        ║  │
│  ║                                                                       ║  │
│  ║    /  ──────► /services ──────► /demo ──────► /pricing               ║  │
│  ║    │              │                              │                    ║  │
│  ║    │              ▼                              ▼                    ║  │
│  ║    │         /investor                       /signup                  ║  │
│  ║    │                                             │                    ║  │
│  ║    └──────► /faq ◄──── /tutorials                │                    ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                    │                                        │
│                                    ▼                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║  PHASE 2: AUTHENTIFICATION                                           ║  │
│  ║                                                                       ║  │
│  ║    /signup ──────► /login ◄────► /forgot-password                    ║  │
│  ║        │              │                                               ║  │
│  ║        │              │ (existing user)                               ║  │
│  ║        │              ▼                                               ║  │
│  ║        │         Dashboard (si onboarding complété)                   ║  │
│  ║        │                                                              ║  │
│  ║        ▼ (new user)                                                   ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                    │                                        │
│                                    ▼                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║  PHASE 3: ONBOARDING (First-time users)                              ║  │
│  ║                                                                       ║  │
│  ║    /onboarding                                                        ║  │
│  ║        │                                                              ║  │
│  ║        ├── Step 1: Bienvenue                                         ║  │
│  ║        ├── Step 2: Profil                                            ║  │
│  ║        ├── Step 3: Sphères préférées                                 ║  │
│  ║        ├── Step 4: Rencontrer Nova                                   ║  │
│  ║        ├── Step 5: Configuration initiale                            ║  │
│  ║        └── /onboarding/complete ──────► Dashboard                    ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                    │                                        │
│                                    ▼                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║  PHASE 4: APPLICATION PRINCIPALE (Protected)                         ║  │
│  ║                                                                       ║  │
│  ║    ┌─────────────────────────────────────────────────────────────┐   ║  │
│  ║    │  /{sphere}/{section}                                        │   ║  │
│  ║    │                                                             │   ║  │
│  ║    │  9 SPHÈRES × 6 SECTIONS = 54 ROUTES                        │   ║  │
│  ║    └─────────────────────────────────────────────────────────────┘   ║  │
│  ║                                                                       ║  │
│  ║    + /nova (Assistant IA)                                            ║  │
│  ║    + /settings/* (Paramètres)                                        ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 PHASE 1: PAGES PUBLIQUES (Pré-Login)

### Routes Principales

| Route | Nom | Description | Priorité |
|-------|-----|-------------|----------|
| `/` | Landing Page | Page d'accueil, présentation CHE·NU | 🔴 Critique |
| `/services` | Services | Présentation des capacités et domaines | 🔴 Critique |
| `/demo` | Démo Narrative | Démo scriptée 5-15 min | 🟠 Haute |
| `/investor` | Investisseurs | Page pour investisseurs potentiels | 🟡 Moyenne |
| `/pricing` | Tarifs | Plans et tarification | 🔴 Critique |
| `/faq` | FAQ | Questions fréquentes | 🟠 Haute |
| `/tutorials` | Tutoriels | Guides d'utilisation | 🟡 Moyenne |

### Pages Légales

| Route | Nom | Description |
|-------|-----|-------------|
| `/privacy` | Confidentialité | Politique de confidentialité |
| `/terms` | Conditions | Conditions générales d'utilisation |
| `/security` | Sécurité | Pratiques de sécurité |

### Redirections (Alias)

| Route source | Redirige vers |
|--------------|---------------|
| `/features` | `/services` |
| `/fonctionnalites` | `/services` |
| `/investors` | `/investor` |
| `/invest` | `/investor` |
| `/help` | `/faq` |
| `/guides` | `/tutorials` |
| `/documentation` | `/tutorials` |
| `/tarifs` | `/pricing` |
| `/confidentialite` | `/privacy` |
| `/conditions` | `/terms` |
| `/cgu` | `/terms` |
| `/securite` | `/security` |

---

## 🔐 PHASE 2: AUTHENTIFICATION

### Routes Auth

| Route | Nom | Description |
|-------|-----|-------------|
| `/signup` | Inscription | Création de compte |
| `/login` | Connexion | Connexion utilisateur |
| `/forgot-password` | Mot de passe oublié | Récupération de compte |

### Redirections Auth

| Route source | Redirige vers |
|--------------|---------------|
| `/register` | `/signup` |
| `/join` | `/signup` |
| `/inscription` | `/signup` |
| `/signin` | `/login` |
| `/connexion` | `/login` |
| `/reset-password` | `/forgot-password` |

### Flow Auth

```
Nouvel utilisateur:
  /signup → Création compte → /onboarding

Utilisateur existant:
  /login → Vérification → /{sphere}/quickcapture

Mot de passe oublié:
  /login → /forgot-password → Email → /login
```

---

## 🎓 PHASE 3: ONBOARDING

### Flow Onboarding (5-8 étapes)

```
/onboarding
    │
    ├── Step 1: Bienvenue à CHE·NU
    │   └── Présentation du concept
    │
    ├── Step 2: Votre Profil
    │   └── Nom, avatar, préférences
    │
    ├── Step 3: Choisir vos Sphères
    │   └── Sélection des sphères prioritaires
    │
    ├── Step 4: Rencontrer Nova
    │   └── Introduction à l'assistant IA
    │
    ├── Step 5: Configuration Initiale
    │   └── Notifications, thème, langue
    │
    └── /onboarding/complete
        └── Félicitations → Redirection vers Dashboard
```

### Conditions d'accès

- Accessible UNIQUEMENT si `user.onboardingCompleted === false`
- Après complétion, redirection automatique vers sphère préférée
- Possibilité de skip (mais fortement déconseillé)

---

## 🏠 PHASE 4: APPLICATION PRINCIPALE

### Les 9 Sphères Canoniques

| ID | Nom FR | Nom EN | Icône | Couleur |
|----|--------|--------|-------|---------|
| `personal` | Personnel | Personal | 🏠 | #4ade80 |
| `business` | Entreprise | Business | 💼 | #f59e0b |
| `government` | Gouvernement | Government | 🏛️ | #3b82f6 |
| `studio` | Studio Créatif | Creative Studio | 🎨 | #ec4899 |
| `community` | Communauté | Community | 👥 | #8b5cf6 |
| `social` | Social & Médias | Social & Media | 📱 | #06b6d4 |
| `entertainment` | Divertissement | Entertainment | 🎬 | #f43f5e |
| `myteam` | Mon Équipe | My Team | 🤝 | #84cc16 |
| `scholar` | Académique | Scholar | 📚 | #a855f7 |

### Les 6 Sections Bureau

| ID | Nom FR | Nom EN | Icône | Description |
|----|--------|--------|-------|-------------|
| `quickcapture` | Capture Rapide | Quick Capture | ⚡ | Saisie rapide d'idées, notes, tâches |
| `resumeworkspace` | Espace de Travail | Resume Workspace | 📋 | Reprise du travail en cours |
| `threads` | Threads | Threads | 💬 | Conversations et fils de discussion |
| `datafiles` | Données & Fichiers | Data & Files | 📁 | Gestion des fichiers et données |
| `activeagents` | Agents Actifs | Active Agents | 🤖 | Agents IA en cours d'exécution |
| `meetings` | Réunions | Meetings | 📅 | Planification et gestion des réunions |

### Matrice des Routes (54 combinaisons)

```
/personal/quickcapture      /business/quickcapture      /government/quickcapture
/personal/resumeworkspace   /business/resumeworkspace   /government/resumeworkspace
/personal/threads           /business/threads           /government/threads
/personal/datafiles         /business/datafiles         /government/datafiles
/personal/activeagents      /business/activeagents      /government/activeagents
/personal/meetings          /business/meetings          /government/meetings

/studio/quickcapture        /community/quickcapture     /social/quickcapture
/studio/resumeworkspace     /community/resumeworkspace  /social/resumeworkspace
/studio/threads             /community/threads          /social/threads
/studio/datafiles           /community/datafiles        /social/datafiles
/studio/activeagents        /community/activeagents     /social/activeagents
/studio/meetings            /community/meetings         /social/meetings

/entertainment/quickcapture /myteam/quickcapture        /scholar/quickcapture
/entertainment/resumeworkspace /myteam/resumeworkspace  /scholar/resumeworkspace
/entertainment/threads      /myteam/threads             /scholar/threads
/entertainment/datafiles    /myteam/datafiles           /scholar/datafiles
/entertainment/activeagents /myteam/activeagents        /scholar/activeagents
/entertainment/meetings     /myteam/meetings            /scholar/meetings
```

### Routes Spéciales Protégées

| Route | Nom | Description |
|-------|-----|-------------|
| `/nova` | Nova AI | Assistant IA principal |
| `/settings` | Paramètres | Page principale des paramètres |
| `/settings/profile` | Profil | Modification du profil |
| `/settings/appearance` | Apparence | Thème, couleurs, disposition |
| `/settings/notifications` | Notifications | Gestion des notifications |
| `/settings/security` | Sécurité | Mot de passe, 2FA |
| `/settings/billing` | Facturation | Abonnement, factures |
| `/settings/integrations` | Intégrations | Services connectés |

---

## 🧭 NAVIGATION — Structure UI

### Layout Canonique (Post-Login)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ TOP BAR                                                                      │
│ [Breadcrumb: Sphère > Section]                   [🔍 Search] [🔔] [❓]      │
├───────────────┬──────────────────────────────────────────────────────────────┤
│               │                                                              │
│   SIDEBAR     │              MAIN CONTENT                                    │
│               │                                                              │
│   🏠 Personal │    ┌─────────────────────────────────────────────────────┐  │
│   💼 Business │    │  SECTION TABS                                       │  │
│   🏛️ Gov      │    │  [⚡ Quick] [📋 Resume] [💬 Threads] [📁 Data]      │  │
│   🎨 Studio   │    │  [🤖 Agents] [📅 Meetings]                         │  │
│   👥 Commun.  │    ├─────────────────────────────────────────────────────┤  │
│   📱 Social   │    │                                                     │  │
│   🎬 Enter.   │    │              SECTION CONTENT                        │  │
│   🤝 MyTeam   │    │                                                     │  │
│   📚 Scholar  │    │                                                     │  │
│   ───────────  │    │                                                     │  │
│   🤖 Nova     │    │                                                     │  │
│   ⚙️ Settings │    └─────────────────────────────────────────────────────┘  │
│               │                                                              │
│   ───────────  │                                                              │
│   [Avatar]    │                                                              │
│   User Name   │                                                              │
│   PRO         │                                                              │
├───────────────┴──────────────────────────────────────────────────────────────┤
│ BOTTOM BAR                                                                   │
│ [🤖 Nova Quick Access]                                    [● Connecté]      │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Comportement Sidebar

1. **Collapsed Mode**: Icônes uniquement (70px)
2. **Expanded Mode**: Icônes + Labels (260px)
3. **Mobile**: Drawer avec overlay

### Navigation Sphère

1. Click sur sphère → Expand sous-menu des 6 sections
2. Click sur section → Navigation vers `/{sphere}/{section}`
3. Si collapsed → Click navigue directement vers `/{sphere}/quickcapture`

---

## 🔄 REDIRECTIONS AUTOMATIQUES

### Redirections de Base

| Condition | Source | Destination |
|-----------|--------|-------------|
| Non-auth, route protégée | `/personal/*` | `/login` |
| Auth, route publique | `/`, `/login` | `/{preferredSphere}/quickcapture` |
| Auth, onboarding non fait | Toute route | `/onboarding` |
| Route invalide | `/*` | `/` (public) ou `/{sphere}/quickcapture` (auth) |
| Sphère sans section | `/{sphere}` | `/{sphere}/quickcapture` |

### État de la Route

```typescript
// Logic de redirection
if (!isAuthenticated) {
  if (isProtectedRoute) return redirect('/login');
  return renderPublicPage();
}

if (!user.onboardingCompleted && !isOnboardingRoute) {
  return redirect('/onboarding');
}

if (isPublicOnlyRoute) {
  return redirect(`/${user.preferredSphere}/quickcapture`);
}

return renderProtectedPage();
```

---

## 📱 RESPONSIVE DESIGN

### Breakpoints

| Breakpoint | Largeur | Sidebar | Layout |
|------------|---------|---------|--------|
| Mobile | < 768px | Drawer | Stack |
| Tablet | 768-1024px | Collapsed | Side-by-side |
| Desktop | > 1024px | Expanded | Full layout |

### Mobile Navigation

```
┌────────────────────────────────────────┐
│ ☰  CHE·NU  [🔍] [🔔]                  │
├────────────────────────────────────────┤
│                                        │
│  SECTION TABS (scrollable)             │
│  [⚡] [📋] [💬] [📁] [🤖] [📅]        │
│                                        │
├────────────────────────────────────────┤
│                                        │
│        MAIN CONTENT                    │
│                                        │
│                                        │
│                                        │
│                                        │
├────────────────────────────────────────┤
│  [🏠] [💼] [🤖 Nova] [⚙️] [👤]        │
│  Bottom Tab Bar (sphères rapides)      │
└────────────────────────────────────────┘
```

---

## ✅ CHECKLIST DE VALIDATION

### Pages Publiques
- [ ] Landing Page (`/`) — Fonctionnelle
- [ ] Services Page (`/services`) — Fonctionnelle
- [ ] Demo Page (`/demo`) — Fonctionnelle
- [ ] Investor Page (`/investor`) — Fonctionnelle
- [ ] Pricing Page (`/pricing`) — Fonctionnelle
- [ ] FAQ Page (`/faq`) — Fonctionnelle
- [ ] Tutorials Page (`/tutorials`) — Fonctionnelle
- [ ] Privacy Page (`/privacy`) — Fonctionnelle
- [ ] Terms Page (`/terms`) — Fonctionnelle
- [ ] Security Page (`/security`) — Fonctionnelle

### Authentication
- [ ] Signup (`/signup`) — Création compte
- [ ] Login (`/login`) — Connexion
- [ ] Forgot Password (`/forgot-password`) — Récupération
- [ ] Redirections alias — Toutes fonctionnelles

### Onboarding
- [ ] Flow complet 5 étapes
- [ ] Skip possible mais déconseillé
- [ ] Redirection post-completion
- [ ] Persist state `onboardingCompleted`

### Application Principale
- [ ] 54 routes sphère/section fonctionnelles
- [ ] Sidebar navigation avec expand/collapse
- [ ] Section tabs fonctionnels
- [ ] Nova page accessible
- [ ] Settings pages accessibles
- [ ] Logout fonctionnel

### Protection Routes
- [ ] Public routes accessibles sans auth
- [ ] Protected routes redirigent vers login
- [ ] Onboarding obligatoire pour nouveaux users
- [ ] Redirection post-login correcte

---

## 📁 FICHIERS DE RÉFÉRENCE

```
frontend/src/
├── AppComplete.tsx           ← NOUVEAU App complet avec routing
├── pages/
│   ├── public/
│   │   ├── LandingPage.tsx
│   │   ├── ServicesPage.tsx
│   │   ├── DemoPage.tsx
│   │   ├── InvestorPage.tsx
│   │   ├── FAQPage.tsx
│   │   ├── PricingPage.tsx
│   │   ├── TutorialsPage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── SignupPage.tsx
│   │   ├── ForgotPasswordPage.tsx
│   │   ├── PrivacyPage.tsx
│   │   ├── TermsPage.tsx
│   │   ├── SecurityPage.tsx
│   │   └── PublicRouter.tsx
│   ├── onboarding/
│   │   └── OnboardingFlow.tsx
│   ├── settings/
│   │   └── SettingsPage.tsx
│   ├── nova/
│   │   └── NovaPage.tsx
│   └── NotFoundPage.tsx
└── USER_JOURNEY.md           ← CE DOCUMENT
```

---

## 🚀 PROCHAINES ÉTAPES

1. **Remplacer App.tsx** par `AppComplete.tsx`
2. **Créer les section components** manquants pour chaque section
3. **Tester le flow complet** : Landing → Signup → Onboarding → Dashboard
4. **Responsive testing** sur mobile et tablet
5. **Intégrer avec backend** pour auth réelle

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    © 2026 CHE·NU™ — PARCOURS UTILISATEUR                    ║
║                    Document de Référence Officiel                            ║
║                    GOUVERNANCE > EXÉCUTION                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
