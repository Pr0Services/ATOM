# 🚀 AT·OM — CHECKLIST DE LANCEMENT

## Phase I : Fondation (144 Fondateurs)

---

## 📋 VUE D'ENSEMBLE

```
┌─────────────────────────────────────────────────────────────────┐
│                    AT·OM LAUNCH CHECKLIST                       │
├─────────────────────────────────────────────────────────────────┤
│  Infrastructure    ████████░░  80%                              │
│  Base de données   ██████░░░░  60%                              │
│  Frontend          ████████░░  80%                              │
│  Intégrations      ████░░░░░░  40%                              │
│  Sécurité          ██████░░░░  60%                              │
│  Tests             ████░░░░░░  40%                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ INFRASTRUCTURE & HÉBERGEMENT

### Vercel (Frontend)
- [ ] Créer projet Vercel
- [ ] Connecter repo GitHub `Pr0Services/ATOM`
- [ ] Configurer domaine personnalisé (si applicable)
- [ ] Configurer variables d'environnement :
  ```
  REACT_APP_SUPABASE_URL=
  REACT_APP_SUPABASE_ANON_KEY=
  REACT_APP_HEDERA_NETWORK=testnet
  REACT_APP_HEDERA_OPERATOR_ID=
  ```
- [ ] Activer déploiement automatique sur `main`
- [ ] Tester preview deployments sur branches

### DigitalOcean (Backend/Services)
- [ ] Créer Droplet ou App Platform
- [ ] Configurer domaine API (api.atom.xxx)
- [ ] Installer Node.js 18+
- [ ] Configurer PM2 pour process management
- [ ] Configurer Nginx reverse proxy
- [ ] Activer SSL/HTTPS (Let's Encrypt)
- [ ] Configurer firewall (UFW)

### DNS & Domaines
- [ ] Acheter/configurer domaine principal
- [ ] Configurer DNS records :
  - [ ] A record → Vercel
  - [ ] CNAME api → DigitalOcean
  - [ ] TXT pour vérification

---

## 2️⃣ SUPABASE (Base de données)

### Configuration initiale
- [ ] Créer projet Supabase
- [ ] Noter les credentials :
  - [ ] Project URL
  - [ ] Anon Key (public)
  - [ ] Service Role Key (secret)
- [ ] Configurer région (proche des utilisateurs)

### Exécuter les scripts SQL (dans l'ordre)
```bash
# Ordre d'exécution dans Supabase SQL Editor
```

1. [ ] **schema.sql** — Structure de base
   ```
   services/database/schema.sql
   ```

2. [ ] **grid-tables.sql** — Tables de la grille
   ```
   services/database/grid-tables.sql
   ```

3. [ ] **founder-features.sql** — Fonctionnalités Founder
   ```
   services/database/founder-features.sql
   ```

4. [ ] **agents-tables.sql** — Système d'agents
   ```
   services/database/agents-tables.sql
   ```

5. [ ] **founder-adaptive-agents.sql** — Agents adaptatifs
   ```
   services/database/founder-adaptive-agents.sql
   ```

### Vérification des tables
```sql
-- Vérifier que toutes les tables existent
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

Tables attendues :
- [ ] `profiles`
- [ ] `community_messages`
- [ ] `private_threads`
- [ ] `thread_messages`
- [ ] `agents`
- [ ] `agent_instances`
- [ ] `agent_outputs`
- [ ] `agent_messages`
- [ ] `validated_memory`
- [ ] `underground_videos`
- [ ] `activity_feed`
- [ ] `founder_ux_metrics`
- [ ] `founder_friction_signals`
- [ ] `founder_layout_proposals`
- [ ] `founder_periodic_analyses`
- [ ] `founder_maturity_tracking`

### Storage Buckets
- [ ] Créer bucket `zama-assets` (public)
  - Avatars utilisateurs
  - Images publiques
- [ ] Créer bucket `underground-vault` (private)
  - Vidéos privées fondateurs
  - Limite : 50MB par fichier
- [ ] Configurer policies de storage

### Realtime
- [ ] Activer Realtime sur :
  - [ ] `community_messages`
  - [ ] `profiles`
  - [ ] `private_threads`
  - [ ] `thread_messages`
  - [ ] `agent_instances`
  - [ ] `agent_outputs`
  - [ ] `founder_layout_proposals`

### Row Level Security (RLS)
- [ ] Vérifier RLS activé sur toutes les tables
- [ ] Tester policies avec différents rôles

### Authentication
- [ ] Configurer Email Auth
- [ ] Configurer Magic Link (optionnel)
- [ ] Configurer OAuth providers (optionnel) :
  - [ ] Google
  - [ ] GitHub
- [ ] Personnaliser emails de confirmation
- [ ] Configurer redirect URLs

---

## 3️⃣ HEDERA (Blockchain)

### Compte Opérateur
- [ ] Créer compte Hedera (testnet d'abord)
- [ ] Noter credentials :
  - [ ] Operator ID (0.0.xxxxx)
  - [ ] Private Key
- [ ] Financer compte avec HBAR (testnet faucet)

### Configuration
- [ ] Configurer variables d'environnement :
  ```
  HEDERA_NETWORK=testnet
  HEDERA_OPERATOR_ID=0.0.xxxxx
  HEDERA_OPERATOR_KEY=302e...
  ```

### Tests Hedera
- [ ] Tester création de compte
- [ ] Tester transfert HBAR
- [ ] Tester création de token (si applicable)

### Migration vers Mainnet (après tests)
- [ ] Créer compte mainnet
- [ ] Financer avec vrais HBAR
- [ ] Mettre à jour `HEDERA_NETWORK=mainnet`

---

## 4️⃣ FRONTEND (React App)

### Configuration
- [ ] Vérifier `.env` local :
  ```
  REACT_APP_SUPABASE_URL=https://xxx.supabase.co
  REACT_APP_SUPABASE_ANON_KEY=eyJ...
  REACT_APP_HEDERA_NETWORK=testnet
  ```

### Build & Test Local
```bash
cd ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app
npm install
npm run build
npm start
```

- [ ] Build sans erreurs
- [ ] Toutes les pages chargent
- [ ] Pas d'erreurs console

### Pages à tester
- [ ] `/` — Page d'entrée (EntreePage)
- [ ] `/founder` — Page Founder
  - [ ] Onglet Vision
  - [ ] Onglet Réseau (planète + liste)
  - [ ] Onglet Discussions (chat + threads)
  - [ ] Onglet Archives
  - [ ] Onglet Activité
- [ ] `/tableau-de-bord` — Dashboard
- [ ] `/grid` — Grille planétaire

### Fonctionnalités à tester
- [ ] Inscription/Connexion
- [ ] Ancrage fondateur
- [ ] Envoi de messages (chat global)
- [ ] Création de threads privés
- [ ] Upload d'avatar
- [ ] Modification de profil
- [ ] Panneau UX/Structure (admin)

---

## 5️⃣ SERVICES BACKEND

### Services à déployer
- [ ] `HederaService.js` — Intégration blockchain
- [ ] `SupabaseService.js` — Wrapper base de données
- [ ] `FounderAdaptiveAgents.js` — Agents UX

### Cron Jobs / Scheduled Tasks
- [ ] Agent Architecte (analyse toutes les 4h)
  ```javascript
  // Configurer avec PM2 ou cron
  startPeriodicAnalysis();
  ```

### API Endpoints (si backend séparé)
- [ ] `POST /api/anchor` — Ancrage fondateur
- [ ] `GET /api/founders` — Liste fondateurs
- [ ] `POST /api/messages` — Envoi message
- [ ] `GET /api/proposals` — Propositions UX

---

## 6️⃣ SÉCURITÉ

### Checklist sécurité
- [ ] Variables sensibles en `.env` (jamais commitées)
- [ ] HTTPS partout
- [ ] CORS configuré correctement
- [ ] Rate limiting sur API
- [ ] Validation des inputs
- [ ] Sanitization des outputs
- [ ] CSP headers configurés

### Secrets à protéger
```
⚠️ NE JAMAIS COMMITER :
- SUPABASE_SERVICE_ROLE_KEY
- HEDERA_OPERATOR_KEY
- Tout fichier .env
```

### Audit
- [ ] Vérifier `.gitignore`
- [ ] Scanner pour secrets exposés
- [ ] Vérifier RLS Supabase
- [ ] Tester injections SQL
- [ ] Tester XSS

---

## 7️⃣ MONITORING & LOGS

### Supabase
- [ ] Activer logs détaillés
- [ ] Configurer alertes (usage, erreurs)

### Vercel
- [ ] Activer Analytics
- [ ] Configurer alertes de déploiement

### Application
- [ ] Configurer error tracking (Sentry optionnel)
- [ ] Logs structurés

---

## 8️⃣ TESTS PRÉ-LANCEMENT

### Tests fonctionnels
| Test | Statut |
|------|--------|
| Inscription nouvel utilisateur | ⬜ |
| Connexion utilisateur existant | ⬜ |
| Ancrage fondateur | ⬜ |
| Envoi message chat | ⬜ |
| Réception message realtime | ⬜ |
| Création thread privé | ⬜ |
| Upload avatar | ⬜ |
| Modification profil | ⬜ |
| Visualisation planète | ⬜ |
| Navigation onglets | ⬜ |
| Panneau UX admin | ⬜ |

### Tests de charge
- [ ] Simuler 10 utilisateurs simultanés
- [ ] Simuler 50 messages/minute
- [ ] Vérifier temps de réponse < 2s

### Tests mobile
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Responsive design OK

---

## 9️⃣ DOCUMENTATION

### Pour les développeurs
- [ ] README.md à jour
- [ ] Instructions de setup local
- [ ] Architecture documentée

### Pour les utilisateurs
- [ ] Guide de démarrage Founder
- [ ] FAQ
- [ ] Contact support

---

## 🔟 LANCEMENT

### J-7 (Une semaine avant)
- [ ] Freeze des features
- [ ] Tests intensifs
- [ ] Backup de la DB
- [ ] Préparer communication

### J-1 (Veille du lancement)
- [ ] Vérification finale infrastructure
- [ ] Vérification DNS propagation
- [ ] Préparer rollback plan
- [ ] Briefer l'équipe

### Jour J
- [ ] Déployer version finale
- [ ] Vérifier tous les services
- [ ] Monitoring actif
- [ ] Communiquer le lancement

### J+1 (Lendemain)
- [ ] Analyser premiers logs
- [ ] Corriger bugs critiques
- [ ] Collecter feedback

---

## 📊 MÉTRIQUES DE SUCCÈS

### Phase I (144 fondateurs)
| Métrique | Objectif |
|----------|----------|
| Fondateurs inscrits | 144 |
| Taux de rétention J+7 | > 50% |
| Messages/jour | > 100 |
| Bugs critiques | 0 |
| Uptime | > 99% |

---

## 🔗 CONNEXIONS & INTÉGRATIONS

### Diagramme des connexions
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vercel    │────▶│  Supabase   │────▶│   Hedera    │
│  (Frontend) │     │    (DB)     │     │ (Blockchain)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    React    │     │  Realtime   │     │   Tokens    │
│     App     │     │  WebSocket  │     │   HBAR      │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Flux de données
```
Utilisateur
    │
    ▼
[Frontend Vercel]
    │
    ├──▶ [Supabase Auth] ──▶ Authentification
    │
    ├──▶ [Supabase DB] ──▶ Données (profiles, messages)
    │
    ├──▶ [Supabase Storage] ──▶ Fichiers (avatars, vidéos)
    │
    ├──▶ [Supabase Realtime] ──▶ Updates temps réel
    │
    └──▶ [Hedera] ──▶ Transactions blockchain
```

---

## 📁 FICHIERS IMPORTANTS

### Configuration
```
/ATOM
├── .env.example              # Template variables
├── vercel.json               # Config Vercel
├── package.json              # Dépendances
└── /services
    └── /database
        ├── schema.sql
        ├── grid-tables.sql
        ├── founder-features.sql
        ├── agents-tables.sql
        └── founder-adaptive-agents.sql
```

### Code source principal
```
/ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app/src
├── /pages
│   ├── FounderPage.js        # Page principale Founder
│   ├── EntreePage.js         # Page d'entrée
│   ├── TableauDeBordPage.js  # Dashboard
│   └── GridPage.js           # Grille planétaire
├── /services
│   └── FounderAdaptiveAgents.js  # Agents UX
├── /contexts
│   └── AuthContext.js        # Contexte auth
└── /lib
    └── supabase.js           # Client Supabase
```

---

## ⚡ COMMANDES RAPIDES

### Développement local
```bash
# Installation
npm install

# Démarrage
npm start

# Build production
npm run build

# Tests
npm test
```

### Git
```bash
# Commit
git add .
git commit -m "feat: description"
git push origin main

# Déploiement (automatique via Vercel)
```

### Supabase CLI (optionnel)
```bash
# Login
supabase login

# Link project
supabase link --project-ref xxxxx

# Push migrations
supabase db push
```

---

## 🆘 CONTACTS & RESSOURCES

### Documentation
- Supabase: https://supabase.com/docs
- Hedera: https://docs.hedera.com
- Vercel: https://vercel.com/docs
- React: https://react.dev

### Support
- Supabase Discord
- Hedera Discord
- GitHub Issues

---

## ✅ VALIDATION FINALE

Avant de lancer, confirmez :

- [ ] Toute l'infrastructure est configurée
- [ ] Toutes les tables Supabase sont créées
- [ ] Les variables d'environnement sont configurées
- [ ] Le build passe sans erreur
- [ ] Les tests fonctionnels passent
- [ ] La sécurité a été vérifiée
- [ ] Le monitoring est en place
- [ ] L'équipe est prête

**Signature de validation :**

```
Date: _______________
Validé par: _______________
Version: _______________
```

---

*🔱 AT·OM — L'Arche des Résonances Universelles*
*Phase I : Fondation des 144*
