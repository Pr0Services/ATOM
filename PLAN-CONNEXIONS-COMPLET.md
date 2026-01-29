# PLAN DE MATCH COMPLET — AT·OM CONNEXIONS
## Version 2.0 — Refonte complète à partir de zéro

**Date:** 2026-01-27
**Statut:** En attente d'exécution

---

## VUE D'ENSEMBLE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AT·OM — ARCHITECTURE DE CONNEXIONS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    [DOMAINE]  ←─────────────────────────────────────────┐                   │
│    atom.eco / atom-arche.com (à configurer)             │                   │
│         │                                                │                   │
│         ▼                                                │                   │
│    ┌─────────────┐                                       │                   │
│    │   VERCEL    │ ◄─── Frontend React                   │                   │
│    │  (Frontend) │      Routes SPA                       │                   │
│    └──────┬──────┘                                       │                   │
│           │                                              │                   │
│           │ /api/* (proxy)                               │                   │
│           ▼                                              │                   │
│    ┌─────────────┐                                       │                   │
│    │ DIGITALOCEAN│ ◄─── Backend API                      │                   │
│    │  (Backend)  │      Node.js / Express                │                   │
│    └──────┬──────┘                                       │                   │
│           │                                              │                   │
│     ┌─────┴─────┐                                        │                   │
│     ▼           ▼                                        │                   │
│ ┌────────┐  ┌────────┐                                   │                   │
│ │SUPABASE│  │ HEDERA │ ◄─── Blockchain                   │                   │
│ │  (DB)  │  │(Token) │      ZAMA Token                   │                   │
│ └────────┘  └────────┘                                   │                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PARTIE 1: DOMAINE

### 1.1 Configuration DNS

**Domaine choisi:** `_________________` (à remplir)

| Type | Nom | Valeur | TTL | Statut |
|------|-----|--------|-----|--------|
| A | @ | 76.76.21.21 (Vercel) | 300 | ⬜ |
| CNAME | www | cname.vercel-dns.com | 300 | ⬜ |

### 1.2 Vercel Domain Setup

1. Aller dans **Vercel Dashboard** → **Project: atom-sovereign** → **Settings** → **Domains**
2. Cliquer **Add Domain**
3. Entrer le domaine
4. Suivre les instructions pour ajouter les enregistrements DNS
5. Attendre la propagation (jusqu'à 48h mais souvent quelques minutes)

**Checklist Domaine:**
- [ ] Domaine acheté/possédé
- [ ] DNS A record configuré vers Vercel
- [ ] DNS CNAME www configuré
- [ ] SSL/HTTPS actif (automatique avec Vercel)
- [ ] Domaine vérifié dans Vercel

---

## PARTIE 2: VERCEL (Frontend)

### 2.1 Informations de connexion

| Paramètre | Valeur |
|-----------|--------|
| **Projet** | atom-sovereign |
| **Repository** | ATOM (GitHub) |
| **Branch production** | main |
| **Build Command** | `cd ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app && npm install && npm run build` |
| **Output Directory** | `ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app/build` |
| **Region** | iad1 (Washington D.C.) |

### 2.2 Variables d'environnement Vercel

**Aller dans:** Vercel Dashboard → Project → Settings → Environment Variables

| Variable | Valeur | Type | Statut |
|----------|--------|------|--------|
| `REACT_APP_SUPABASE_URL` | `https://vzbrhovthpihrhdbbjud.supabase.co` | Plaintext | ⬜ Vérifier |
| `REACT_APP_SUPABASE_ANON_KEY` | `sb_publishable_XywZJyq_IlyStM5PljZv4w_iCsAxKMq` | Secret | ⬜ Vérifier |
| `REACT_APP_HEDERA_TOKEN_ID` | `0.0.7730446` | Plaintext | ⬜ Vérifier |
| `REACT_APP_HEDERA_NETWORK` | `testnet` | Plaintext | ⬜ Vérifier |
| `REACT_APP_ATOM_M` | `44.4` | Plaintext | ⬜ Vérifier |
| `REACT_APP_ATOM_P` | `161.8` | Plaintext | ⬜ Vérifier |
| `REACT_APP_ATOM_I` | `369` | Plaintext | ⬜ Vérifier |
| `REACT_APP_ATOM_PO` | `1728` | Plaintext | ⬜ Vérifier |

### 2.3 Routes (vercel.json)

| Route | Destination | Description |
|-------|-------------|-------------|
| `/api/*` | `https://sea-turtle-app-n4vsa.ondigitalocean.app/api/$1` | Proxy vers backend |
| `/static/*` | `/static/$1` | Fichiers statiques |
| `/*` | `/index.html` | SPA fallback |

### 2.4 Vérification Vercel

- [ ] Projet existe et est connecté au repo GitHub
- [ ] Auto-deploy sur push vers main est actif
- [ ] Variables d'environnement configurées
- [ ] vercel.json correct
- [ ] Build réussit sans erreur
- [ ] Site accessible via URL Vercel (*.vercel.app)

---

## PARTIE 3: SUPABASE (Base de données + Auth)

### 3.1 Informations de connexion

| Paramètre | Valeur |
|-----------|--------|
| **Project URL** | `https://vzbrhovthpihrhdbbjud.supabase.co` |
| **Project Ref** | vzbrhovthpihrhdbbjud |
| **Region** | (vérifier dans dashboard) |
| **Anon Key** | `sb_publishable_XywZJyq_IlyStM5PljZv4w_iCsAxKMq` |
| **Service Role Key** | `sb_secret_KTX-whnB-ScZ1sUotgzlGg_gUGHGi6B` |

### 3.2 Tables existantes à vérifier

**Aller dans:** Supabase Dashboard → Table Editor

| Table | Existe | RLS Activé | Colonnes clés |
|-------|--------|------------|---------------|
| `profiles` | ⬜ | ⬜ | id, full_name, avatar_url, role, frequency |
| `community_messages` | ⬜ | ⬜ | id, content, sender_id, room |
| `private_threads` | ⬜ | ⬜ | id, participant_ids, created_by |
| `thread_messages` | ⬜ | ⬜ | id, thread_id, content |

### 3.3 Tables à créer (Scripts SQL)

**IMPORTANT:** Exécuter dans cet ordre exact dans **SQL Editor**

#### Script 1: 01-fix-existing-policies.sql
**But:** Corriger les policies RLS pour les tables existantes

```
Fichier: services/database/01-fix-existing-policies.sql
```
- [ ] Copié dans SQL Editor
- [ ] Exécuté sans erreur
- [ ] Policies recréées pour private_threads et thread_messages

#### Script 2: founder-features.sql
**But:** Ajouter colonnes à profiles, créer underground_videos et activity_feed

```
Fichier: services/database/founder-features.sql
```
- [ ] Copié dans SQL Editor
- [ ] Exécuté sans erreur
- [ ] Nouvelles colonnes dans profiles (role, youtube_channel_url, facebook_url)
- [ ] Table community_messages mise à jour (room)
- [ ] Table underground_videos créée
- [ ] Table activity_feed créée

#### Script 3: agents-tables.sql
**But:** Créer le système d'agents IA

```
Fichier: services/database/agents-tables.sql
```
- [ ] Copié dans SQL Editor
- [ ] Exécuté sans erreur
- [ ] Table agents créée
- [ ] Table agent_instances créée
- [ ] Table agent_outputs créée
- [ ] Table agent_messages créée
- [ ] Table validated_memory créée
- [ ] 3 agents de base insérés (facilitator, synthesis, memory)

#### Script 4: founder-adaptive-agents.sql
**But:** Créer le système d'agents UX adaptatifs

```
Fichier: services/database/founder-adaptive-agents.sql
```
- [ ] Copié dans SQL Editor
- [ ] Exécuté sans erreur
- [ ] Table founder_ux_metrics créée
- [ ] Table founder_friction_signals créée
- [ ] Table founder_layout_proposals créée
- [ ] Table founder_periodic_analyses créée
- [ ] Table founder_maturity_tracking créée
- [ ] 4 agents adaptatifs insérés (ux_observer, feedback_analyst, structure_architect, coherence_guardian)

#### Script 5: grid-tables.sql
**But:** Créer les tables pour la grille planétaire

```
Fichier: services/database/grid-tables.sql
```
- [ ] Copié dans SQL Editor
- [ ] Exécuté sans erreur
- [ ] Table grid_nodes créée
- [ ] Table grid_connections créée
- [ ] Table grid_sectors créée
- [ ] 12 secteurs zodiacaux insérés

### 3.4 Vérification post-scripts

Exécuter dans SQL Editor:
```sql
-- Lister toutes les tables
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' ORDER BY table_name;

-- Vérifier les agents
SELECT agent_type, display_name FROM agents;

-- Vérifier les secteurs de grille
SELECT sector_name, sector_code FROM grid_sectors;

-- Vérifier les fonctions créées
SELECT routine_name FROM information_schema.routines
WHERE routine_schema = 'public' AND routine_type = 'FUNCTION';
```

**Tables attendues (total ~17):**
```
activity_feed
agent_instances
agent_messages
agent_outputs
agents
community_messages
founder_friction_signals
founder_layout_proposals
founder_maturity_tracking
founder_periodic_analyses
founder_ux_metrics
grid_connections
grid_nodes
grid_sectors
private_threads
profiles
thread_messages
underground_videos
validated_memory
```

### 3.5 Storage Buckets

**Aller dans:** Supabase Dashboard → Storage

| Bucket | Type | Max Size | Statut | Action |
|--------|------|----------|--------|--------|
| `zama-assets` | Public | - | ⬜ Vérifier | Vérifier existe |
| `underground-vault` | Private | 50MB | ⬜ À créer | Créer + RLS |

**Créer underground-vault:**
1. Storage → New Bucket
2. Name: `underground-vault`
3. Public: **NON** (décoché)
4. File size limit: `52428800` (50MB)

**RLS Policies pour underground-vault:**
```sql
-- Dans SQL Editor après création du bucket
CREATE POLICY "Founders can upload videos"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'underground-vault');

CREATE POLICY "Founders can view own videos"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'underground-vault');
```

### 3.6 Realtime

**Aller dans:** Supabase Dashboard → Database → Replication

Tables avec Realtime activé:
- [ ] profiles
- [ ] community_messages
- [ ] private_threads
- [ ] thread_messages
- [ ] activity_feed
- [ ] grid_nodes
- [ ] grid_connections
- [ ] founder_layout_proposals

### 3.7 Authentication

**Aller dans:** Supabase Dashboard → Authentication → Settings

- [ ] Email auth activé
- [ ] Confirm email: selon préférence
- [ ] Site URL configuré (domaine production)
- [ ] Redirect URLs configurés

---

## PARTIE 4: DIGITALOCEAN (Backend)

### 4.1 Informations de connexion

| Paramètre | Valeur |
|-----------|--------|
| **App URL** | `https://sea-turtle-app-n4vsa.ondigitalocean.app` |
| **Type** | App Platform |

### 4.2 Variables d'environnement DigitalOcean

**Aller dans:** DigitalOcean → Apps → atom-backend → Settings → Environment Variables

| Variable | Valeur | Statut |
|----------|--------|--------|
| `SUPABASE_URL` | `https://vzbrhovthpihrhdbbjud.supabase.co` | ⬜ |
| `SUPABASE_SERVICE_ROLE_KEY` | `sb_secret_KTX-whnB-ScZ1sUotgzlGg_gUGHGi6B` | ⬜ |
| `HEDERA_NETWORK` | `testnet` | ⬜ |
| `HEDERA_OPERATOR_ID` | `0.0.7702951` | ⬜ |
| `HEDERA_OPERATOR_KEY` | `0xc8cd39aae1182effd990971a1c8c012979e7a7bd6e8a0f152550e4ceb55ed806` | ⬜ |
| `JWT_SECRET_KEY` | `788517fc-1451-4cdf-bd37-9ca97d70bd6c` | ⬜ |

### 4.3 Vérification API

Tester ces endpoints:
```bash
# Health check
curl https://sea-turtle-app-n4vsa.ondigitalocean.app/api/health

# Ou via navigateur
```

- [ ] Backend accessible
- [ ] API répond correctement
- [ ] Connexion Supabase fonctionne
- [ ] Connexion Hedera fonctionne

---

## PARTIE 5: HEDERA (Blockchain)

### 5.1 Informations de connexion

| Paramètre | Valeur |
|-----------|--------|
| **Network** | Testnet |
| **Operator Account** | `0.0.7702951` |
| **Treasury Account** | `0.0.7727679` |
| **ZAMA Token ID** | `0.0.7730446` |
| **Key Type** | ED25519 |

### 5.2 Vérification Hedera

```bash
# Dans le dossier services/hedera/
npm run test-connection
```

- [ ] Connexion au testnet réussie
- [ ] Balance du compte operator visible
- [ ] Token ZAMA accessible

### 5.3 Explorer Hedera

Vérifier sur HashScan (testnet):
- [ ] https://hashscan.io/testnet/account/0.0.7702951
- [ ] https://hashscan.io/testnet/token/0.0.7730446

---

## PARTIE 6: CONNEXIONS ENTRE SERVICES

### 6.1 Frontend → Supabase

```
[React App] ---(supabase-js)--→ [Supabase]
```

**Fichier:** `src/lib/supabase.js`

```javascript
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
```

- [ ] Variables d'environnement définies
- [ ] Client Supabase se connecte
- [ ] Auth fonctionne (signup/signin)
- [ ] Queries fonctionnent
- [ ] Realtime fonctionne

### 6.2 Frontend → Backend (via Vercel proxy)

```
[React App] --(/api/*)--→ [Vercel Proxy] --→ [DigitalOcean]
```

**Fichier:** `vercel.json`

- [ ] Routes /api/* configurées
- [ ] CORS headers présents
- [ ] Proxy fonctionne

### 6.3 Backend → Supabase

```
[DigitalOcean Backend] ---(service_role_key)--→ [Supabase]
```

- [ ] Service role key configuré
- [ ] Accès admin aux tables

### 6.4 Backend → Hedera

```
[DigitalOcean Backend] ---(operator_key)--→ [Hedera Testnet]
```

- [ ] Operator credentials configurés
- [ ] Token operations fonctionnent

---

## PARTIE 7: TESTS DE BOUT EN BOUT

### 7.1 Test Authentication

1. Ouvrir l'app dans le navigateur
2. Créer un compte
3. Se connecter
4. Vérifier le profil dans Supabase

- [ ] Inscription fonctionne
- [ ] Connexion fonctionne
- [ ] Profil créé dans la table profiles

### 7.2 Test Chat Realtime

1. Ouvrir l'app dans 2 navigateurs/onglets
2. Se connecter avec 2 comptes différents
3. Envoyer un message depuis le premier
4. Vérifier qu'il apparaît dans le second sans refresh

- [ ] Messages s'envoient
- [ ] Realtime fonctionne

### 7.3 Test FounderPage

1. Aller sur `/founder`
2. Tester chaque onglet:
   - [ ] Vision: contenu affiché
   - [ ] Réseau: planète 3D + liste membres
   - [ ] Discussions: chat global fonctionne
   - [ ] Archives: section visible
   - [ ] Activité: flux d'activité

### 7.4 Test GridPage

1. Aller sur `/grid`
2. Vérifier la visualisation 3D

- [ ] Page charge sans erreur
- [ ] Données de grille affichées

---

## PARTIE 8: SÉCURITÉ

### 8.1 Clés à ne JAMAIS exposer publiquement

| Clé | Lieu sûr | Exposable dans frontend? |
|-----|----------|--------------------------|
| `SUPABASE_SERVICE_ROLE_KEY` | DigitalOcean env | **NON** |
| `HEDERA_OPERATOR_KEY` | DigitalOcean env | **NON** |
| `JWT_SECRET_KEY` | DigitalOcean env | **NON** |
| `SUPABASE_ANON_KEY` | Vercel env | Oui (limité par RLS) |

### 8.2 RLS (Row Level Security)

Toutes les tables doivent avoir RLS activé:
- [ ] Vérifier `ALTER TABLE xxx ENABLE ROW LEVEL SECURITY` sur chaque table
- [ ] Vérifier les policies sont en place

### 8.3 CORS

- [ ] Backend accepte uniquement les origines autorisées
- [ ] Headers CORS configurés dans vercel.json

---

## PARTIE 9: ORDRE D'EXÉCUTION

### Phase A: Vérification existante

```
1. ⬜ Se connecter à Vercel Dashboard
   - Vérifier le projet atom-sovereign existe
   - Vérifier les variables d'environnement

2. ⬜ Se connecter à Supabase Dashboard
   - Vérifier le projet vzbrhovthpihrhdbbjud
   - Vérifier les tables existantes
   - Vérifier que RLS est activé

3. ⬜ Se connecter à DigitalOcean Dashboard
   - Vérifier l'app sea-turtle-app-n4vsa
   - Vérifier les variables d'environnement
```

### Phase B: Configuration domaine

```
4. ⬜ Acheter/configurer le domaine
5. ⬜ Ajouter le domaine dans Vercel
6. ⬜ Configurer les DNS
7. ⬜ Attendre propagation + vérifier HTTPS
```

### Phase C: Base de données

```
8. ⬜ Exécuter 01-fix-existing-policies.sql
9. ⬜ Exécuter founder-features.sql
10. ⬜ Exécuter agents-tables.sql
11. ⬜ Exécuter founder-adaptive-agents.sql
12. ⬜ Exécuter grid-tables.sql
13. ⬜ Créer bucket underground-vault
14. ⬜ Vérifier Realtime activé sur les tables
```

### Phase D: Déploiement

```
15. ⬜ Merger la branche vers main:
    git checkout main
    git merge claude/deployment-error-handling-9Ismo
    git push origin main

16. ⬜ Vérifier le déploiement Vercel
17. ⬜ Tester l'URL de production
```

### Phase E: Tests

```
18. ⬜ Test authentication
19. ⬜ Test FounderPage (5 onglets)
20. ⬜ Test chat realtime
21. ⬜ Test GridPage
22. ⬜ Test avec le domaine personnalisé
```

---

## RÉSUMÉ RAPIDE

### URLs de services

| Service | URL Dashboard |
|---------|---------------|
| Vercel | https://vercel.com/dashboard |
| Supabase | https://supabase.com/dashboard |
| DigitalOcean | https://cloud.digitalocean.com |
| Hedera Explorer | https://hashscan.io/testnet |

### Identifiants clés

| Service | Identifiant |
|---------|-------------|
| Supabase Project | vzbrhovthpihrhdbbjud |
| DigitalOcean App | sea-turtle-app-n4vsa |
| Hedera Account | 0.0.7702951 |
| ZAMA Token | 0.0.7730446 |

### Fichiers de configuration

| Fichier | Chemin |
|---------|--------|
| Vercel config | `/vercel.json` |
| Env principal | `/.env` |
| Frontend env | `/ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app/.env` |
| Supabase client | `/services/database/supabaseClient.js` |
| Hedera config | `/services/hedera/config.js` |

---

## CHECKLIST FINALE

```
DOMAINE
⬜ DNS configuré
⬜ SSL actif
⬜ Domaine vérifié dans Vercel

VERCEL
⬜ Variables d'environnement OK
⬜ Build réussit
⬜ Déploiement OK

SUPABASE
⬜ 5 scripts SQL exécutés
⬜ ~17 tables créées
⬜ RLS activé partout
⬜ Bucket underground-vault créé
⬜ Realtime activé

DIGITALOCEAN
⬜ Variables d'environnement OK
⬜ API accessible

HEDERA
⬜ Connexion testnet OK
⬜ Token ZAMA accessible

TESTS
⬜ Auth fonctionne
⬜ FounderPage charge
⬜ Chat realtime OK
⬜ Site accessible via domaine
```

---

*Document créé le 2026-01-27*
*AT·OM — L'Arche des Résonances Universelles*
