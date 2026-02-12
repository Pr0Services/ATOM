# 🚀 AT·OM — CHECKLIST DE LANCEMENT

## Phase I : Fondation (144 Fondateurs)

---

## 📋 VUE D'ENSEMBLE

```
┌─────────────────────────────────────────────────────────────────┐
│                    AT·OM LAUNCH CHECKLIST                       │
├─────────────────────────────────────────────────────────────────┤
│  Infrastructure    ██████████  100% ✅ CONNECTÉ                 │
│  Base de données   ██████░░░░  60%  (nouveaux scripts SQL)      │
│  Frontend          ████████░░  80%  (nouvelles pages)           │
│  Intégrations      ██████████  100% ✅ CONNECTÉ                 │
│  Sécurité          ██████░░░░  60%                              │
│  Tests             ████░░░░░░  40%                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ SERVICES DÉJÀ CONNECTÉS

| Service | Statut | Notes |
|---------|--------|-------|
| Vercel | ✅ Connecté | Frontend déployé |
| Supabase | ✅ Connecté | DB active |
| Hedera | ✅ Connecté | Testnet configuré |
| DigitalOcean | ✅ Connecté | Backend prêt |

---

## 1️⃣ MISES À JOUR REQUISES

### A. Nouveaux Scripts SQL à exécuter dans Supabase

**⚠️ PRIORITÉ HAUTE — Exécuter dans l'ordre :**

```sql
-- 1. Aller dans Supabase Dashboard → SQL Editor
-- 2. Copier-coller chaque fichier et exécuter
```

| # | Fichier | Description | Statut |
|---|---------|-------------|--------|
| 1 | `services/database/grid-tables.sql` | Tables grille planétaire | ⬜ À faire |
| 2 | `services/database/founder-features.sql` | YouTube, Vault, Activity | ⬜ À faire |
| 3 | `services/database/agents-tables.sql` | Système d'agents IA | ⬜ À faire |
| 4 | `services/database/founder-adaptive-agents.sql` | Agents UX adaptatifs | ⬜ À faire |

### B. Nouvelles Pages/Composants à déployer

| Page | Route | Fichier | Statut |
|------|-------|---------|--------|
| FounderPage | `/founder` | `src/pages/FounderPage.js` | ⬜ À déployer |
| GridPage | `/grid` | `src/pages/GridPage.js` | ⬜ Vérifier |
| FounderAdaptiveAgents | (service) | `src/services/FounderAdaptiveAgents.js` | ⬜ À déployer |

### C. Storage Buckets Supabase

| Bucket | Type | Usage | Statut |
|--------|------|-------|--------|
| `zama-assets` | Public | Avatars, images | ⬜ Vérifier existe |
| `underground-vault` | Private | Vidéos fondateurs (50MB max) | ⬜ À créer |

---

## 2️⃣ SCRIPTS SQL À EXÉCUTER (DÉTAIL)

### Script 1: grid-tables.sql
```sql
-- Copier depuis: services/database/grid-tables.sql
-- Tables créées:
--   - grid_nodes
--   - grid_connections
--   - grid_sectors
```
- [ ] Exécuté dans Supabase SQL Editor
- [ ] Vérifié sans erreur

### Script 2: founder-features.sql
```sql
-- Copier depuis: services/database/founder-features.sql
-- Modifications:
--   - Ajoute youtube_channel_url à profiles
--   - Ajoute facebook_url à profiles
--   - Ajoute is_active_creator à profiles
--   - Ajoute room à community_messages
--   - Crée underground_videos
--   - Crée activity_feed
```
- [ ] Exécuté dans Supabase SQL Editor
- [ ] Vérifié sans erreur

### Script 3: agents-tables.sql
```sql
-- Copier depuis: services/database/agents-tables.sql
-- Tables créées:
--   - agents (facilitator, synthesis, memory)
--   - agent_instances
--   - agent_outputs
--   - agent_messages
--   - validated_memory
-- Fonctions:
--   - add_agent_to_context()
--   - remove_agent_from_context()
--   - validate_agent_output()
```
- [ ] Exécuté dans Supabase SQL Editor
- [ ] Vérifié sans erreur

### Script 4: founder-adaptive-agents.sql
```sql
-- Copier depuis: services/database/founder-adaptive-agents.sql
-- Tables créées:
--   - founder_ux_metrics
--   - founder_friction_signals
--   - founder_layout_proposals
--   - founder_periodic_analyses
--   - founder_maturity_tracking
-- Nouveaux agents:
--   - ux_observer
--   - feedback_analyst
--   - structure_architect
--   - coherence_guardian
-- Fonctions:
--   - record_ux_metric()
--   - detect_friction_signal()
--   - should_generate_proposal()
--   - create_layout_proposal()
--   - respond_to_proposal()
```
- [ ] Exécuté dans Supabase SQL Editor
- [ ] Vérifié sans erreur

### Vérification post-scripts
```sql
-- Exécuter pour vérifier
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' ORDER BY table_name;

-- Vérifier les agents
SELECT * FROM agents;

-- Vérifier les fonctions
SELECT routine_name FROM information_schema.routines
WHERE routine_schema = 'public';
```

---

## 3️⃣ STORAGE SUPABASE

### Créer bucket underground-vault
1. Aller dans **Supabase Dashboard** → **Storage**
2. Cliquer **New bucket**
3. Configuration:
   - Name: `underground-vault`
   - Public: **NON** (décoché)
   - File size limit: `52428800` (50MB)
4. Ajouter policy RLS:
```sql
-- Policy pour underground-vault
CREATE POLICY "Founders can upload videos"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'underground-vault');

CREATE POLICY "Founders can view own videos"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'underground-vault' AND auth.uid()::text = (storage.foldername(name))[1]);
```

- [ ] Bucket créé
- [ ] Policies configurées

---

## 4️⃣ DÉPLOIEMENT FRONTEND

### Option A: Déploiement automatique (recommandé)
```bash
# Merger la branche vers main pour déclencher Vercel
git checkout main
git merge claude/deployment-error-handling-9Ismo
git push origin main
```
- [ ] Merge effectué
- [ ] Vercel déploie automatiquement
- [ ] Vérifier le déploiement dans Vercel Dashboard

### Option B: Déploiement manuel
```bash
# Dans le dossier de l'app React
cd ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app
npm install
npm run build
# Vercel CLI
vercel --prod
```

### Fichiers à vérifier dans le déploiement

| Fichier | Chemin | Vérifié |
|---------|--------|---------|
| FounderPage.js | `src/pages/FounderPage.js` | ⬜ |
| FounderAdaptiveAgents.js | `src/services/FounderAdaptiveAgents.js` | ⬜ |
| GridPage.js | `src/pages/GridPage.js` | ⬜ |
| App.js (routes) | `src/App.js` | ⬜ |

---

## 5️⃣ TESTS POST-DÉPLOIEMENT

### Pages à tester en production

| Page | URL | Statut |
|------|-----|--------|
| Entrée | `/` | ⬜ |
| **Founder** | `/founder` | ⬜ |
| Dashboard | `/tableau-de-bord` | ⬜ |
| Grid | `/grid` | ⬜ |

### Tests FounderPage (NOUVEAU)

| Fonctionnalité | Test | Statut |
|----------------|------|--------|
| Onglet Vision | Affiche mission, progression | ⬜ |
| Onglet Réseau | Planète 3D + Liste membres | ⬜ |
| Onglet Discussions | Chat global fonctionne | ⬜ |
| Onglet Discussions | Threads privés visibles | ⬜ |
| Onglet Archives | Créateurs YouTube affichés | ⬜ |
| Onglet Activité | Flux d'activités | ⬜ |
| Panneau UX | Bouton 🏗️ visible (admin) | ⬜ |
| Panneau UX | Propositions chargent | ⬜ |
| Profil | Modal édition fonctionne | ⬜ |
| Profil | Upload avatar | ⬜ |
| Ancrage | Nouveau fondateur s'ajoute | ⬜ |

### Tests Realtime

| Test | Résultat |
|------|----------|
| Envoyer message → apparaît sans refresh | ⬜ |
| Nouveau fondateur → apparaît sur planète | ⬜ |
| Nouvelle activité → flux se met à jour | ⬜ |

---

## 6️⃣ AGENT ADAPTATIF (OPTIONNEL)

### Activer l'analyse périodique
L'Agent Architecte peut analyser l'usage toutes les 4h.

**Option 1: Via DigitalOcean (cron)**
```bash
# Ajouter au crontab
0 */4 * * * node /path/to/run-agent-analysis.js
```

**Option 2: Via Supabase Edge Functions**
```sql
-- Créer une fonction scheduled
SELECT cron.schedule(
  'agent-analysis',
  '0 */4 * * *',
  $$SELECT should_generate_proposal(4)$$
);
```

- [ ] Analyse périodique configurée (optionnel pour le lancement)

---

## 7️⃣ RÉSUMÉ DES ACTIONS

### Actions immédiates (dans l'ordre)

```
┌────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1: Exécuter les 4 scripts SQL dans Supabase            │
│           (grid-tables → founder-features → agents →           │
│            founder-adaptive-agents)                            │
├────────────────────────────────────────────────────────────────┤
│  ÉTAPE 2: Créer le bucket "underground-vault" dans Storage    │
├────────────────────────────────────────────────────────────────┤
│  ÉTAPE 3: Merger la branche vers main                         │
│           git checkout main                                    │
│           git merge claude/deployment-error-handling-9Ismo    │
│           git push origin main                                 │
├────────────────────────────────────────────────────────────────┤
│  ÉTAPE 4: Vérifier le déploiement Vercel                      │
├────────────────────────────────────────────────────────────────┤
│  ÉTAPE 5: Tester /founder en production                       │
└────────────────────────────────────────────────────────────────┘
```

### Checklist rapide

| # | Action | Commande/Lieu | Fait |
|---|--------|---------------|------|
| 1 | SQL grid-tables | Supabase SQL Editor | ⬜ |
| 2 | SQL founder-features | Supabase SQL Editor | ⬜ |
| 3 | SQL agents-tables | Supabase SQL Editor | ⬜ |
| 4 | SQL founder-adaptive-agents | Supabase SQL Editor | ⬜ |
| 5 | Créer bucket underground-vault | Supabase Storage | ⬜ |
| 6 | Merge vers main | `git merge` | ⬜ |
| 7 | Vérifier Vercel | Dashboard Vercel | ⬜ |
| 8 | Tester /founder | URL production | ⬜ |

---

## 📊 NOUVELLES FONCTIONNALITÉS AJOUTÉES

### FounderPage — Page Entreprise avec 5 onglets

| Onglet | Description | Sphère future |
|--------|-------------|---------------|
| **Vision** | Mission, Phase I, Progression (n/144) | - |
| **Réseau** | Planète 3D + Liste, profils membres | Identité |
| **Discussions** | Chat global + Threads privés | Communication |
| **Archives** | YouTube créateurs, Documents | Scholar |
| **Activité** | Flux d'activités, Stats | - |

### Système d'Agents Adaptatifs

| Agent | Rôle | Action |
|-------|------|--------|
| **Observateur UX** | Tracker temps/section, scroll | Silencieux |
| **Analyste Feedback** | Détecter friction dans messages | Signaux |
| **Architecte Structure** | Proposer ajustements layout | Propositions |
| **Gardien Cohérence** | Empêcher dérive complexité | Blocage |

**Cycle d'adaptation:**
```
USAGE → OBSERVATION → ANALYSE → PROPOSITION → VALIDATION HUMAINE → AJUSTEMENT
```

### Métadonnées de migration

Chaque donnée créée dans Founder inclut:
```javascript
{
  origin_context: 'founder',
  future_sphere: 'communication', // ou 'scholar', 'identity'
  migration_status: 'pending'
}
```

---

## 🔗 ARCHITECTURE ACTUELLE

```
┌─────────────────────────────────────────────────────────────────┐
│                         AT·OM STACK                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   VERCEL    │  │  SUPABASE   │  │   HEDERA    │             │
│  │  Frontend   │  │   Backend   │  │ Blockchain  │             │
│  │   React     │  │  PostgreSQL │  │   HBAR      │             │
│  │   ✅ OK     │  │    ✅ OK    │  │   ✅ OK     │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          │                                      │
│                    DigitalOcean                                 │
│                      ✅ OK                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Flux des données Founder

```
[Utilisateur]
     │
     ▼
[FounderPage.js]
     │
     ├──▶ Onglet Vision ──▶ Affichage statique
     │
     ├──▶ Onglet Réseau ──▶ profiles (Supabase)
     │                      └──▶ Realtime subscription
     │
     ├──▶ Onglet Discussions ──▶ community_messages (Supabase)
     │                          └──▶ Realtime subscription
     │
     ├──▶ Onglet Archives ──▶ profiles (YouTube links)
     │                       └──▶ underground_videos
     │
     └──▶ Onglet Activité ──▶ activity_feed (Supabase)

[Agents Adaptatifs]
     │
     ├──▶ UX Observer ──▶ founder_ux_metrics
     ├──▶ Feedback Analyst ──▶ founder_friction_signals
     ├──▶ Structure Architect ──▶ founder_layout_proposals
     └──▶ Coherence Guardian ──▶ (validation locale)
```

---

## 📁 FICHIERS MODIFIÉS/CRÉÉS

### Nouveaux fichiers SQL
```
services/database/
├── grid-tables.sql              # NOUVEAU
├── founder-features.sql         # NOUVEAU
├── agents-tables.sql            # NOUVEAU
└── founder-adaptive-agents.sql  # NOUVEAU
```

### Nouveaux fichiers React
```
ATOM/.../src/
├── pages/
│   └── FounderPage.js           # MODIFIÉ (refonte complète)
└── services/
    └── FounderAdaptiveAgents.js # NOUVEAU
```

---

## ✅ VALIDATION FINALE

### Checklist pré-lancement

| Catégorie | Item | Statut |
|-----------|------|--------|
| **Infra** | Vercel connecté | ✅ |
| **Infra** | Supabase connecté | ✅ |
| **Infra** | Hedera connecté | ✅ |
| **Infra** | DigitalOcean connecté | ✅ |
| **DB** | Scripts SQL exécutés | ⬜ |
| **DB** | Bucket underground-vault créé | ⬜ |
| **Deploy** | Branche mergée vers main | ⬜ |
| **Deploy** | Vercel déployé | ⬜ |
| **Test** | /founder fonctionne | ⬜ |
| **Test** | Chat realtime OK | ⬜ |
| **Test** | Panneau UX visible (admin) | ⬜ |

### Commande rapide pour merger

```bash
git checkout main
git merge claude/deployment-error-handling-9Ismo
git push origin main
```

---

*🔱 AT·OM — L'Arche des Résonances Universelles*
*Phase I : Fondation des 144*
*Dernière mise à jour : 2026-01-26*
