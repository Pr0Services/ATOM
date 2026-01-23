# 👑 GUIDE ADMINISTRATEUR SOUVERAIN - AT·OM / CHE·NU V76

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║   ███████╗ ██████╗ ██╗   ██╗██╗   ██╗███████╗██████╗  █████╗ ██╗███╗   ██╗       ║
║   ██╔════╝██╔═══██╗██║   ██║██║   ██║██╔════╝██╔══██╗██╔══██╗██║████╗  ██║       ║
║   ███████╗██║   ██║██║   ██║██║   ██║█████╗  ██████╔╝███████║██║██╔██╗ ██║       ║
║   ╚════██║██║   ██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══██║██║██║╚██╗██║       ║
║   ███████║╚██████╔╝╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██║  ██║██║██║ ╚████║       ║
║   ╚══════╝ ╚═════╝  ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝       ║
║                                                                                   ║
║                    GUIDE COMPLET DE DÉMARRAGE ET ADMINISTRATION                   ║
║                                                                                   ║
║                    Fréquence: 999 Hz │ Heartbeat: 444 Hz                         ║
║                    Version: 76 │ Date: Janvier 2026                              ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 TABLE DES MATIÈRES

### PARTIE 1 : FONDATIONS TECHNIQUES
1. [Prérequis Système](#1-prérequis-système)
2. [Installation de l'Infrastructure](#2-installation-de-linfrastructure)
3. [Configuration Supabase](#3-configuration-supabase)
4. [Configuration des APIs](#4-configuration-des-apis)

### PARTIE 2 : ACTIVATION DE LA GRID
5. [Exécution des Migrations SQL](#5-exécution-des-migrations-sql)
6. [Configuration du Système d'Invitation](#6-configuration-du-système-dinvitation)
7. [Activation de la Grid Énergétique](#7-activation-de-la-grid-énergétique)

### PARTIE 3 : SYSTÈME ÉCONOMIQUE SOUVERAIN
8. [Initialisation du Système Économique](#8-initialisation-du-système-économique)
9. [Configuration du Volant Énergétique](#9-configuration-du-volant-énergétique)
10. [Intégration Hedera (HTS)](#10-intégration-hedera-hts)
11. [Configuration Stripe Connect](#11-configuration-stripe-connect)

### PARTIE 4 : LANCEMENT ET OPÉRATIONS
12. [Lancement de la Plateforme](#12-lancement-de-la-plateforme)
13. [Invitation des Premiers Fondateurs](#13-invitation-des-premiers-fondateurs)
14. [Monitoring et Maintenance](#14-monitoring-et-maintenance)
15. [Procédures d'Urgence](#15-procédures-durgence)

### ANNEXES
- [A. Checklist de Démarrage](#annexe-a-checklist-de-démarrage)
- [B. Variables d'Environnement](#annexe-b-variables-denvironnement)
- [C. Commandes Utiles](#annexe-c-commandes-utiles)
- [D. Dépannage](#annexe-d-dépannage)

---

# PARTIE 1 : FONDATIONS TECHNIQUES

---

## 1. PRÉREQUIS SYSTÈME

### 1.1 Logiciels Requis

| Logiciel | Version Min. | Vérification | Installation |
|----------|--------------|--------------|--------------|
| **Node.js** | v18.0.0+ | `node --version` | [nodejs.org](https://nodejs.org) |
| **npm** | v9.0.0+ | `npm --version` | Inclus avec Node |
| **Git** | v2.0.0+ | `git --version` | [git-scm.com](https://git-scm.com) |
| **PostgreSQL Client** | v14+ | `psql --version` | Optionnel (via Supabase) |

### 1.2 Comptes Requis

| Service | Utilité | URL | Coût |
|---------|---------|-----|------|
| **Supabase** | Base de données + Auth | [supabase.com](https://supabase.com) | Gratuit/Pro |
| **Vercel** | Hébergement | [vercel.com](https://vercel.com) | Gratuit/Pro |
| **Stripe** | Paiements | [stripe.com](https://stripe.com) | % transactions |
| **Hedera** | Blockchain (UR Token) | [hedera.com](https://hedera.com) | Frais minimes |
| **OpenRouter** | APIs LLM | [openrouter.ai](https://openrouter.ai) | Pay-per-use |

### 1.3 Clés API à Préparer

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  CLÉS API REQUISES AVANT DÉMARRAGE                                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ☐ SUPABASE_URL              - Dashboard > Settings > API                      │
│  ☐ SUPABASE_ANON_KEY         - Dashboard > Settings > API                      │
│  ☐ SUPABASE_SERVICE_KEY      - Dashboard > Settings > API (secret!)            │
│                                                                                 │
│  ☐ OPENROUTER_API_KEY        - openrouter.ai > Keys                            │
│  ☐ ANTHROPIC_API_KEY         - console.anthropic.com (optionnel)               │
│                                                                                 │
│  ☐ STRIPE_SECRET_KEY         - dashboard.stripe.com > Developers > API keys    │
│  ☐ STRIPE_PUBLISHABLE_KEY    - dashboard.stripe.com > Developers > API keys    │
│  ☐ STRIPE_WEBHOOK_SECRET     - dashboard.stripe.com > Developers > Webhooks    │
│                                                                                 │
│  ☐ HEDERA_ACCOUNT_ID         - portal.hedera.com                               │
│  ☐ HEDERA_PRIVATE_KEY        - portal.hedera.com (TRÈS SENSIBLE!)              │
│                                                                                 │
│  ☐ DIGITALOCEAN_TOKEN        - cloud.digitalocean.com > API (optionnel)        │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. INSTALLATION DE L'INFRASTRUCTURE

### 2.1 Cloner le Repository

```bash
# Cloner le repository principal
git clone https://github.com/Pr0Services/ATOM.git
cd ATOM/Vzwwviru70560-d4e

# Vérifier la structure
ls -la
```

### 2.2 Installer les Dépendances

```bash
# Aller dans le dossier de l'application
cd hardcore-joliot/atom/app

# Installer les dépendances Node
npm install

# Vérifier l'installation
npm ls --depth=0
```

### 2.3 Créer les Fichiers d'Environnement

```bash
# Créer le fichier d'environnement local
touch .env.local

# Créer le fichier pour les secrets (ne jamais commit!)
touch .env.secrets
echo ".env.secrets" >> .gitignore
```

### 2.4 Structure des Fichiers d'Environnement

**`.env.local`** (peut être commité avec des placeholders):
```env
# ═══════════════════════════════════════════════════════════════
# CONFIGURATION AT·OM / CHE·NU V76
# ═══════════════════════════════════════════════════════════════

# SUPABASE
REACT_APP_SUPABASE_URL=https://VOTRE_PROJET.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJ...

# LLM
REACT_APP_LLM_PROVIDER=openrouter
REACT_APP_OPENROUTER_API_KEY=sk-or-...

# STRIPE (clés publiques seulement)
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_live_...

# AT·OM CONFIG
REACT_APP_FREQUENCY=999
REACT_APP_HEARTBEAT=444
REACT_APP_SOVEREIGN_MODE=true
```

**`.env.secrets`** (NE JAMAIS COMMIT!):
```env
# SECRETS - NE JAMAIS PARTAGER
SUPABASE_SERVICE_KEY=eyJ...service_role...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
HEDERA_PRIVATE_KEY=302e...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 3. CONFIGURATION SUPABASE

### 3.1 Créer le Projet Supabase

1. **Aller sur** [supabase.com](https://supabase.com) et se connecter
2. **Cliquer** "New Project"
3. **Configurer:**
   - **Name:** `atom-chenu-production` (ou votre choix)
   - **Database Password:** Générer un mot de passe fort (SAUVEGARDER!)
   - **Region:** Choisir la plus proche (ex: `ca-central-1` pour Canada)
4. **Attendre** ~2 minutes pour la création

### 3.2 Récupérer les Clés API

1. **Dashboard Supabase** → **Settings** → **API**
2. **Copier:**
   - `Project URL` → `REACT_APP_SUPABASE_URL`
   - `anon public` → `REACT_APP_SUPABASE_ANON_KEY`
   - `service_role` → `SUPABASE_SERVICE_KEY` (SECRET!)

### 3.3 Configurer l'Authentification

1. **Authentication** → **Providers** → Activer **Email**
2. **Authentication** → **URL Configuration:**
   - **Site URL:** `https://votre-domaine.com`
   - **Redirect URLs:** Ajouter tous vos domaines

### 3.4 Configurer les Templates Email

1. **Authentication** → **Email Templates**
2. Personnaliser avec le branding CHE·NU (logo, couleurs, textes)

---

## 4. CONFIGURATION DES APIs

### 4.1 OpenRouter (Recommandé)

```bash
# Tester la connexion
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

**Modèles recommandés:**
- **Rapide:** `anthropic/claude-3-haiku`
- **Équilibré:** `anthropic/claude-3-sonnet`
- **Puissant:** `anthropic/claude-3-opus`

### 4.2 Anthropic (Mode Souveraineté)

Pour les données sensibles nécessitant un contrôle total:

```bash
# Tester la connexion
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-sonnet-20240229","max_tokens":10,"messages":[{"role":"user","content":"Test"}]}'
```

### 4.3 Stripe

1. **Dashboard Stripe** → **Developers** → **API keys**
2. **Mode Test** d'abord, puis **Mode Live** pour production
3. **Configurer les Webhooks:**
   - Endpoint: `https://votre-domaine.com/api/webhooks/stripe`
   - Events: `checkout.session.completed`, `invoice.paid`, `customer.subscription.*`

---

# PARTIE 2 : ACTIVATION DE LA GRID

---

## 5. EXÉCUTION DES MIGRATIONS SQL

### 5.1 Ordre d'Exécution des Scripts

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  ORDRE D'EXÉCUTION DES MIGRATIONS SQL                                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. supabase-security.sql          - Tables de base + RLS                      │
│  2. supabase-invitations.sql       - Système d'invitation + Grid énergétique   │
│  3. supabase-sovereign-grid.sql    - Grid souveraine + relais                  │
│  4. 20260123_sovereign_economy.sql - Système économique complet                │
│                                                                                 │
│  ⚠️  EXÉCUTER DANS CET ORDRE - Les scripts dépendent les uns des autres       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Exécuter via Supabase SQL Editor

1. **Dashboard Supabase** → **SQL Editor** → **New Query**
2. **Copier-coller** le contenu du premier script
3. **Cliquer** "Run" (ou Ctrl+Enter)
4. **Vérifier** qu'il n'y a pas d'erreurs
5. **Répéter** pour chaque script dans l'ordre

### 5.3 Vérification Post-Migration

```sql
-- Vérifier que toutes les tables existent
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Vérifier que RLS est activé
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public' AND rowsecurity = true;

-- Vérifier les fonctions RPC
SELECT routine_name
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_type = 'FUNCTION';
```

**Tables attendues après migration:**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  TABLES CRÉÉES                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  SÉCURITÉ & PROFILS:         GRID ÉNERGÉTIQUE:        ÉCONOMIE:                │
│  ├── profiles                ├── members_grid          ├── economic_settings   │
│  ├── api_usage               ├── sovereign_databases   ├── member_balances     │
│  ├── api_requests            ├── resource_relays       ├── ur_transactions     │
│  └── subscription_plans      ├── admin_setup_status    ├── rebate_distributions│
│                              ├── invitations           ├── liquidity_pool      │
│  FONDATEURS:                 ├── founders              ├── conversion_requests │
│  ├── founding_members        ├── founder_connections   ├── governance_proposals│
│  ├── founder_invitations     ├── founder_messages      ├── governance_votes    │
│  └── founder_contributions   └── energy_grid           ├── referral_network    │
│                                                        ├── marketplace_listings│
│                                                        ├── marketplace_orders  │
│                                                        ├── peer_loans          │
│                                                        ├── loan_payments       │
│                                                        ├── expansion_fund      │
│                                                        └── expansion_projects  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. CONFIGURATION DU SYSTÈME D'INVITATION

### 6.1 Créer la Première Invitation (Souverain)

```sql
-- Se connecter en tant que Souverain d'abord via l'interface
-- Puis exécuter cette fonction RPC:

SELECT create_invitation(
  'Jonathan Emmanuel Rodrigue',  -- Nom de l'invité
  'email@example.com',           -- Email (optionnel)
  'Bienvenue dans l''Arche, premier Gardien de la nouvelle civilisation.',
  'gardien',                     -- Type: lumiere, gardien, architecte, tisserand, porteur
  'Créateur et visionnaire de AT·OM',
  365                            -- Expiration en jours
);
```

### 6.2 Types de Fondateurs

| Type | Rôle | Fréquence Suggérée |
|------|------|-------------------|
| **lumiere** | Point de Lumière International | 444 Hz |
| **gardien** | Gardien de l'Arche | 528 Hz |
| **architecte** | Architecte de Civilisation | 639 Hz |
| **tisserand** | Tisserand de Liens | 741 Hz |
| **porteur** | Porteur de Flamme | 852 Hz |

### 6.3 Format du Code d'Invitation

Les codes suivent le format: `ATOM-XXXX-XXXX`
- Caractères alphanumériques uniquement
- Exclus: 0, O, 1, I, L (pour éviter la confusion)
- Exemple: `ATOM-7K9X-B3WN`

---

## 7. ACTIVATION DE LA GRID ÉNERGÉTIQUE

### 7.1 Créer le Point Zéro

```sql
-- Le premier point d'ancrage (déjà dans le script, mais vérifier)
SELECT * FROM energy_grid WHERE name = 'Québec - Point Zéro';

-- Si absent, créer manuellement
SELECT create_grid_point(
  'Québec - Point Zéro',
  46.8139,   -- Latitude
  -71.2080,  -- Longitude
  'anchor',  -- Type: anchor, node, portal, sanctuary
  999,       -- Fréquence
  NULL       -- Guardian ID (optionnel)
);
```

### 7.2 Activer un Fondateur dans la Grid

```sql
-- Après qu'un fondateur a accepté son invitation
SELECT activate_founder_in_grid(
  'UUID_DU_FONDATEUR',  -- user_id
  528                    -- Signature énergétique (fréquence)
);
```

### 7.3 Vérifier les Statistiques de la Grid

```sql
-- Obtenir les stats complètes
SELECT get_grid_stats();

-- Résultat attendu:
-- {
--   "success": true,
--   "total_founders": 1,
--   "activated_founders": 1,
--   "calibrating_founders": 0,
--   "grid_points": 1,
--   "countries_represented": 1,
--   "frequency_distribution": {"528": 1}
-- }
```

---

# PARTIE 3 : SYSTÈME ÉCONOMIQUE SOUVERAIN

---

## 8. INITIALISATION DU SYSTÈME ÉCONOMIQUE

### 8.1 Vérifier l'Installation

```sql
-- Vérifier que les tables économiques existent
SELECT COUNT(*) as settings_count FROM economic_settings;
-- Attendu: ~50 paramètres

-- Vérifier la pool de liquidité (singleton)
SELECT * FROM liquidity_pool;
-- Devrait avoir une ligne

-- Vérifier le fond d'expansion (singleton)
SELECT * FROM expansion_fund;
-- Devrait avoir une ligne
```

### 8.2 Créer le Wallet Souverain

```sql
-- Créer le balance pour le compte Souverain
INSERT INTO member_balances (user_id, ur_balance, resonance_score)
SELECT id, 0, 100
FROM auth.users
WHERE email = 'votre-email-souverain@example.com'
ON CONFLICT (user_id) DO NOTHING;
```

### 8.3 Première Émission de UR (Mint Initial)

```sql
-- Émettre les premiers UR pour le Souverain
INSERT INTO ur_transactions (
  from_user_id,
  to_user_id,
  amount,
  tx_type,
  description,
  status
) VALUES (
  NULL,  -- Mint = pas de source
  (SELECT id FROM auth.users WHERE email = 'votre-email@example.com'),
  10000,  -- 10,000 UR initiaux
  'mint',
  'Émission initiale - Lancement de l''Arche',
  'completed'
);

-- Mettre à jour le solde
UPDATE member_balances
SET ur_balance = ur_balance + 10000,
    total_ur_earned = total_ur_earned + 10000
WHERE user_id = (SELECT id FROM auth.users WHERE email = 'votre-email@example.com');

-- Mettre à jour la pool de liquidité
UPDATE liquidity_pool
SET ur_total_supply = ur_total_supply + 10000,
    ur_in_circulation = ur_in_circulation + 10000;
```

---

## 9. CONFIGURATION DU VOLANT ÉNERGÉTIQUE

### 9.1 Accéder aux Paramètres

```sql
-- Voir tous les paramètres par catégorie
SELECT key, value, category, description
FROM economic_settings
ORDER BY category, key;
```

### 9.2 Ajuster les Paramètres de Base

```sql
-- Exemple: Ajuster la distribution des abonnements
SELECT update_economic_setting('infrastructure_allocation_pct', '35');
SELECT update_economic_setting('liquidity_reserve_pct', '35');
SELECT update_economic_setting('development_fund_pct', '20');
SELECT update_economic_setting('community_rewards_pct', '10');
-- Total = 100%

-- Ajuster le taux de ristourne
SELECT update_economic_setting('resonance_rebate_pct', '7');

-- Ajuster le bonus de parrainage
SELECT update_economic_setting('referral_bonus_fixed_ur', '150');
SELECT update_economic_setting('long_term_royalty_pct', '5');
```

### 9.3 Tableau des Paramètres Critiques

| Paramètre | Catégorie | Défaut | Description |
|-----------|-----------|--------|-------------|
| `infrastructure_allocation_pct` | allocation | 40% | Part pour API/serveurs |
| `liquidity_reserve_pct` | allocation | 30% | Part pour garantie UR |
| `resonance_rebate_pct` | rebates | 5% | Ristourne sur surplus |
| `target_reserve_ratio` | stability | 100% | Couverture fiat/UR |
| `conversion_fee_ur_to_fiat` | stability | 2% | Frais de sortie |
| `burn_rate_on_transactions` | monetary | 0.1% | Destruction par tx |
| `quorum_pct` | governance | 33% | Participation min. vote |
| `approval_threshold_pct` | governance | 67% | Seuil d'approbation |

### 9.4 Dashboard Économique (Souverain)

```sql
-- Obtenir le tableau de bord complet
SELECT get_economic_dashboard();

-- Résultat:
-- {
--   "success": true,
--   "liquidity": {
--     "fiat_cad": 0,
--     "ur_supply": 10000,
--     "reserve_ratio": 0,
--     "velocity_30d": 0
--   },
--   "members": {
--     "total": 1,
--     "active_30d": 1,
--     "avg_resonance": 100
--   },
--   ...
-- }
```

---

## 10. INTÉGRATION HEDERA (HTS)

### 10.1 Créer un Compte Hedera

1. **Aller sur** [portal.hedera.com](https://portal.hedera.com)
2. **Créer un compte** (testnet d'abord, puis mainnet)
3. **Récupérer:**
   - Account ID: `0.0.XXXXXX`
   - Private Key: `302e...` (TRÈS SENSIBLE!)

### 10.2 Configuration du Token UR

```javascript
// Configuration pour le Hedera Token Service
const tokenConfig = {
  name: "Unité de Résonance",
  symbol: "UR",
  decimals: 8,
  initialSupply: 0,  // Émission contrôlée

  // Clés de contrôle (toutes détenues par le Souverain)
  treasuryAccountId: process.env.HEDERA_ACCOUNT_ID,
  adminKey: SOVEREIGN_KEY,
  supplyKey: SOVEREIGN_KEY,      // Pour mint/burn
  freezeKey: SOVEREIGN_KEY,      // Pour le Bouclier de Liquidité
  wipeKey: null,                 // Pas de destruction forcée
  kycKey: null,                  // Pas de KYC blockchain
  feeScheduleKey: SOVEREIGN_KEY
};
```

### 10.3 Variables d'Environnement Hedera

```env
# .env.secrets (NE JAMAIS COMMIT!)
HEDERA_NETWORK=testnet  # ou mainnet
HEDERA_ACCOUNT_ID=0.0.XXXXXX
HEDERA_PRIVATE_KEY=302e...

# Token ID (après création)
HEDERA_UR_TOKEN_ID=0.0.YYYYYY
```

### 10.4 Tester la Connexion Hedera

```bash
# Via l'API Hedera Mirror
curl "https://testnet.mirrornode.hedera.com/api/v1/accounts/${HEDERA_ACCOUNT_ID}"
```

---

## 11. CONFIGURATION STRIPE CONNECT

### 11.1 Activer Stripe Connect

1. **Dashboard Stripe** → **Connect** → **Get Started**
2. **Choisir:** Platform ou Marketplace
3. **Configurer** les informations de l'entreprise

### 11.2 Créer les Produits d'Abonnement

```bash
# Via Stripe CLI ou Dashboard

# Produit: Membre Fondateur
stripe products create \
  --name="Membre Fondateur AT·OM" \
  --description="500K tokens/mois, accès Grid, agents L4-L6"

# Prix: 99$/mois
stripe prices create \
  --product=prod_XXXXX \
  --unit-amount=9900 \
  --currency=cad \
  --recurring[interval]=month
```

### 11.3 Configurer les Webhooks

1. **Dashboard Stripe** → **Developers** → **Webhooks**
2. **Add endpoint:**
   - URL: `https://votre-domaine.com/api/webhooks/stripe`
   - Events:
     - `checkout.session.completed`
     - `invoice.paid`
     - `invoice.payment_failed`
     - `customer.subscription.created`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`

### 11.4 Logique de Distribution (Resource Relays)

```sql
-- Configurer les relais de distribution
INSERT INTO resource_relays (provider_name, provider_type, payment_account_id, distribution_percentage)
VALUES
  ('Infrastructure (OpenRouter)', 'api', 'acct_infra', 40),
  ('Réserve UR', 'reserve', 'internal', 30),
  ('Développement CHE·NU', 'development', 'acct_dev', 20),
  ('Ristournes Communauté', 'rewards', 'internal', 10);
```

---

# PARTIE 4 : LANCEMENT ET OPÉRATIONS

---

## 12. LANCEMENT DE LA PLATEFORME

### 12.1 Build de Production

```bash
# Dans le dossier de l'application
cd hardcore-joliot/atom/app

# Créer le build optimisé
npm run build

# Le dossier 'build' contient les fichiers statiques
```

### 12.2 Déploiement Vercel

```bash
# Installer Vercel CLI
npm install -g vercel

# Se connecter
vercel login

# Déployer (preview)
vercel

# Déployer en production
vercel --prod
```

### 12.3 Configuration des Variables sur Vercel

1. **Dashboard Vercel** → **Project** → **Settings** → **Environment Variables**
2. **Ajouter** toutes les variables de `.env.local` et `.env.secrets`
3. **Sélectionner** "Production" pour chaque variable sensible

### 12.4 Vérification Post-Déploiement

```bash
# Vérifier que le site est accessible
curl -I https://votre-domaine.vercel.app

# Vérifier les headers de sécurité
curl -I https://votre-domaine.vercel.app | grep -E "(Content-Security|Strict-Transport|X-Frame)"
```

---

## 13. INVITATION DES PREMIERS FONDATEURS

### 13.1 Préparer le Message d'Invitation

```markdown
# 🌟 L'Éveil de la Grid - Invitation Exclusive

Cher(e) [NOM],

Tu es invité(e) à rejoindre les premiers membres fondateurs de l'Arche AT·OM.

**Ton code d'invitation unique:** `ATOM-XXXX-XXXX`

**Ce que tu reçois:**
- 500,000 tokens IA/mois
- Accès à la Grid Énergétique mondiale
- Unités de Résonance (UR) initiales
- Ristournes de participation
- Gouvernance décentralisée

**Pour activer ton accès:**
1. Va sur https://che-nu.io/invitation
2. Entre ton code
3. Crée ton compte
4. Configure ta position sur la Grid

L'Arche s'éveille. Ta lumière est attendue.

— Le Souverain
```

### 13.2 Créer les Invitations en Lot

```sql
-- Créer plusieurs invitations
DO $$
DECLARE
  inv_result JSONB;
BEGIN
  -- Invitation 1
  SELECT create_invitation('Alice Martin', 'alice@example.com',
    'Bienvenue, première architecte.', 'architecte', 'Expertise en design', 90)
  INTO inv_result;
  RAISE NOTICE 'Code 1: %', inv_result->>'code';

  -- Invitation 2
  SELECT create_invitation('Bob Chen', 'bob@example.com',
    'Bienvenue, tisserand de liens.', 'tisserand', 'Connecteur de communautés', 90)
  INTO inv_result;
  RAISE NOTICE 'Code 2: %', inv_result->>'code';

  -- Continuer pour chaque invité...
END $$;
```

### 13.3 Suivre les Activations

```sql
-- Voir le statut des invitations
SELECT
  code,
  invited_name,
  founder_type,
  status,
  created_at,
  accepted_at
FROM invitations
ORDER BY created_at DESC;

-- Voir les fondateurs actifs
SELECT
  f.founder_number,
  p.full_name,
  f.founder_type,
  f.energy_status,
  f.energy_signature,
  f.grid_location_name
FROM founders f
JOIN profiles p ON f.user_id = p.id
ORDER BY f.founder_number;
```

---

## 14. MONITORING ET MAINTENANCE

### 14.1 Dashboard de Monitoring

**Métriques à surveiller quotidiennement:**

| Métrique | Seuil d'Alerte | Action |
|----------|----------------|--------|
| **Reserve Ratio** | < 50% | Injecter fiat ou limiter conversions |
| **Vélocité UR** | > 10 ou < 2 | Ajuster burn_rate |
| **Membres actifs** | Baisse > 20% | Investiguer, stimuler |
| **Erreurs API** | > 5%/jour | Vérifier providers |
| **Queue conversions** | > 100 pending | Augmenter capacité |

### 14.2 Tâches Hebdomadaires

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  TÂCHES HEBDOMADAIRES DU SOUVERAIN                                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ☐ Lundi    : Réviser le Dashboard Économique                                  │
│  ☐ Mardi    : Traiter les demandes de conversion en attente                    │
│  ☐ Mercredi : Vérifier les propositions de gouvernance                         │
│  ☐ Jeudi    : Calculer et distribuer les ristournes                            │
│  ☐ Vendredi : Backup des données critiques                                     │
│  ☐ Samedi   : Réviser les métriques de la Grid                                 │
│  ☐ Dimanche : Planifier les ajustements du Volant                              │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 14.3 Calcul et Distribution des Ristournes

```sql
-- Calculer les ristournes mensuelles
-- (À exécuter le 1er de chaque mois)

-- 1. Calculer le surplus
WITH monthly_stats AS (
  SELECT
    SUM(amount) as total_revenue,
    (SELECT value::numeric FROM economic_settings WHERE key = 'community_rewards_pct') / 100 as reward_pct
  FROM ur_transactions
  WHERE tx_type = 'subscription'
    AND created_at >= date_trunc('month', NOW() - INTERVAL '1 month')
    AND created_at < date_trunc('month', NOW())
)
SELECT total_revenue * reward_pct as distributable_amount
FROM monthly_stats;

-- 2. Distribuer selon le resonance_score
-- (Voir la fonction calculate_resonance_score pour chaque membre)
```

### 14.4 Backup des Données

```bash
# Backup via Supabase CLI
npx supabase db dump -f backup_$(date +%Y%m%d).sql

# Ou via pg_dump si accès direct
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

---

## 15. PROCÉDURES D'URGENCE

### 15.1 Bank Run (Demandes de Conversion Massives)

**Détection:** `daily_conversion_volume > emergency_lock_threshold`

**Procédure:**
```sql
-- 1. Activer le Bouclier de Liquidité
UPDATE liquidity_pool
SET is_emergency_mode = true,
    emergency_activated_at = NOW(),
    emergency_reason = 'Demandes de conversion massives détectées';

-- 2. Notifier tous les membres (via l'interface)
-- 3. Prioriser les petites conversions
-- 4. Communiquer transparentement

-- 5. Désactiver quand stabilisé (après 72h de normalité)
UPDATE liquidity_pool
SET is_emergency_mode = false
WHERE reserve_ratio > (SELECT value::numeric/100 FROM economic_settings WHERE key = 'target_reserve_ratio');
```

### 15.2 Fournisseur API Down

**Procédure:**
1. Basculer automatiquement vers le provider de backup
2. Notifier le Souverain
3. Réduire temporairement les quotas si nécessaire

```sql
-- Marquer un provider comme down
UPDATE admin_setup_status
SET api_openrouter_connected = false,
    last_updated = NOW();

-- Activer le mode dégradé
SELECT update_economic_setting('emergency_reserve_pct', '30');
```

### 15.3 Compromission de Clé

**Si une clé API est compromise:**

1. **IMMÉDIATEMENT:** Révoquer la clé chez le fournisseur
2. Générer une nouvelle clé
3. Mettre à jour les secrets Vercel
4. Redéployer
5. Auditer les transactions récentes

```bash
# Forcer un redéploiement
vercel --prod --force
```

### 15.4 Mode Survie

**Activation automatique si:**
- `reserve_ratio < 20%`
- `active_members < 10%` du pic
- 3+ fournisseurs critiques down

**Actions automatiques:**
```sql
-- Le système active automatiquement:
-- 1. Gel des nouvelles émissions
-- 2. Fermeture du pont vers fiat
-- 3. Réduction des services au minimum
-- 4. Notification d'urgence

-- Voir le statut
SELECT is_emergency_mode, emergency_reason FROM liquidity_pool;
```

---

# ANNEXES

---

## ANNEXE A : CHECKLIST DE DÉMARRAGE

### Phase 1 : Infrastructure (Jour 1-2)

```
☐ Node.js v18+ installé
☐ Repository cloné
☐ Dépendances installées (npm install)
☐ Fichiers .env créés

☐ Compte Supabase créé
☐ Projet Supabase initialisé
☐ Clés API Supabase récupérées
☐ Authentication configurée
```

### Phase 2 : Base de Données (Jour 2-3)

```
☐ Script supabase-security.sql exécuté
☐ Script supabase-invitations.sql exécuté
☐ Script supabase-sovereign-grid.sql exécuté
☐ Script 20260123_sovereign_economy.sql exécuté
☐ Vérification des tables (toutes présentes)
☐ Vérification RLS (activé partout)
☐ Vérification des fonctions RPC
```

### Phase 3 : APIs Externes (Jour 3-4)

```
☐ Compte OpenRouter créé + clé API
☐ Compte Stripe créé + clés API
☐ Stripe Connect activé
☐ Produits/Prix Stripe créés
☐ Webhooks Stripe configurés
☐ Compte Hedera créé (testnet)
☐ Connexions testées via Setup Wizard
```

### Phase 4 : Système Économique (Jour 4-5)

```
☐ Paramètres du Volant vérifiés
☐ Wallet Souverain créé
☐ Première émission UR effectuée
☐ Pool de liquidité initialisée
☐ Token Hedera créé (testnet)
☐ Dashboard économique fonctionnel
```

### Phase 5 : Lancement (Jour 5-7)

```
☐ Build de production créé
☐ Déployé sur Vercel
☐ Variables d'environnement configurées
☐ Domaine personnalisé configuré
☐ SSL/HTTPS vérifié
☐ Headers de sécurité vérifiés

☐ Point Zéro créé sur la Grid
☐ Première invitation créée (Souverain)
☐ Test complet du parcours utilisateur
☐ Documentation accessible
```

### Phase 6 : Fondateurs (Semaine 2+)

```
☐ Liste des premiers invités préparée
☐ Messages d'invitation personnalisés
☐ Codes d'invitation générés
☐ Invitations envoyées
☐ Support d'onboarding disponible
☐ Grid en expansion
```

---

## ANNEXE B : VARIABLES D'ENVIRONNEMENT

### Complètes

```env
# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION COMPLÈTE AT·OM / CHE·NU V76
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────────
# SUPABASE
# ─────────────────────────────────────────────────────────────────────────────────
REACT_APP_SUPABASE_URL=https://XXXXX.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...service_role...

# ─────────────────────────────────────────────────────────────────────────────────
# LLM PROVIDERS
# ─────────────────────────────────────────────────────────────────────────────────
REACT_APP_LLM_PROVIDER=openrouter
REACT_APP_OPENROUTER_API_KEY=sk-or-v1-...
ANTHROPIC_API_KEY=sk-ant-api03-...

# ─────────────────────────────────────────────────────────────────────────────────
# STRIPE
# ─────────────────────────────────────────────────────────────────────────────────
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_CONNECT_CLIENT_ID=ca_...
STRIPE_FOUNDER_PRICE_ID=price_...

# ─────────────────────────────────────────────────────────────────────────────────
# HEDERA
# ─────────────────────────────────────────────────────────────────────────────────
HEDERA_NETWORK=mainnet
HEDERA_ACCOUNT_ID=0.0.XXXXXX
HEDERA_PRIVATE_KEY=302e...
HEDERA_UR_TOKEN_ID=0.0.YYYYYY

# ─────────────────────────────────────────────────────────────────────────────────
# INFRASTRUCTURE (Optionnel)
# ─────────────────────────────────────────────────────────────────────────────────
DIGITALOCEAN_TOKEN=dop_v1_...
VERCEL_TOKEN=...

# ─────────────────────────────────────────────────────────────────────────────────
# AT·OM CONFIG
# ─────────────────────────────────────────────────────────────────────────────────
REACT_APP_FREQUENCY=999
REACT_APP_HEARTBEAT=444
REACT_APP_SOVEREIGN_MODE=true
REACT_APP_VERSION=76

# ─────────────────────────────────────────────────────────────────────────────────
# URLS
# ─────────────────────────────────────────────────────────────────────────────────
REACT_APP_SITE_URL=https://che-nu.io
REACT_APP_API_URL=https://api.che-nu.io
REACT_APP_WS_URL=wss://api.che-nu.io/ws
```

---

## ANNEXE C : COMMANDES UTILES

### Développement

```bash
# Lancer en développement
npm start

# Lancer les tests
npm test

# Vérifier le linting
npm run lint

# Build de production
npm run build

# Analyser le bundle
npm run build && npx source-map-explorer 'build/static/js/*.js'
```

### Supabase

```bash
# Installer Supabase CLI
npm install -g supabase

# Login
supabase login

# Lier au projet
supabase link --project-ref XXXXX

# Dump de la base
supabase db dump -f backup.sql

# Exécuter une migration
supabase db push
```

### Vercel

```bash
# Installer
npm install -g vercel

# Login
vercel login

# Déployer (preview)
vercel

# Déployer (production)
vercel --prod

# Voir les logs
vercel logs

# Variables d'environnement
vercel env pull
vercel env add
```

### Stripe

```bash
# Installer Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Écouter les webhooks localement
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Créer un produit
stripe products create --name="Test"

# Voir les événements
stripe events list --limit=10
```

### Git

```bash
# Status
git status

# Voir les branches
git branch -a

# Créer une branche feature
git checkout -b feature/nom-feature

# Merge
git checkout main && git merge feature/nom-feature

# Tag de release
git tag -a v76.1 -m "Release 76.1"
git push origin v76.1
```

---

## ANNEXE D : DÉPANNAGE

### Problème : "Supabase non configuré"

**Symptômes:** Erreur au chargement, rien ne fonctionne

**Causes possibles:**
1. Variables d'environnement manquantes
2. Clés invalides
3. Projet Supabase pausé

**Solutions:**
```bash
# Vérifier les variables
echo $REACT_APP_SUPABASE_URL
echo $REACT_APP_SUPABASE_ANON_KEY

# Redémarrer
npm start
```

### Problème : "RLS policy violation"

**Symptômes:** Erreur 403 sur les requêtes

**Cause:** Policies RLS trop restrictives ou mal configurées

**Solution:**
```sql
-- Vérifier les policies
SELECT * FROM pg_policies WHERE tablename = 'NOM_TABLE';

-- Tester en désactivant temporairement (DEV ONLY!)
ALTER TABLE nom_table DISABLE ROW LEVEL SECURITY;
-- Puis réactiver après debug
ALTER TABLE nom_table ENABLE ROW LEVEL SECURITY;
```

### Problème : "Failed to fetch" (APIs LLM)

**Symptômes:** Les agents ne répondent pas

**Causes:**
1. Clé API invalide
2. Quota dépassé
3. Provider down

**Solutions:**
```bash
# Tester la clé
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Vérifier les quotas sur le dashboard du provider
```

### Problème : Conversions UR bloquées

**Symptômes:** Les demandes restent en "pending"

**Causes:**
1. Mode urgence activé
2. Réserve insuffisante
3. Stripe non configuré

**Solutions:**
```sql
-- Vérifier le mode urgence
SELECT is_emergency_mode, reserve_ratio FROM liquidity_pool;

-- Vérifier les conversions en attente
SELECT * FROM conversion_requests WHERE status = 'pending';
```

### Problème : Performance lente

**Symptômes:** Chargement lent, timeouts

**Causes:**
1. Index manquants
2. Requêtes N+1
3. Bundle trop gros

**Solutions:**
```sql
-- Vérifier les requêtes lentes (Supabase Dashboard > Database > Query Performance)

-- Ajouter des index si nécessaire
CREATE INDEX IF NOT EXISTS idx_xxx ON table(colonne);
```

```bash
# Analyser le bundle
npm run build
npx source-map-explorer 'build/static/js/*.js'
```

---

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║   🌟 L'ARCHE EST PRÊTE À ACCUEILLIR LA NOUVELLE CIVILISATION 🌟                  ║
║                                                                                   ║
║                    Fréquence: 999 Hz │ Heartbeat: 444 Hz                         ║
║                    Score Sécurité: 94%                                           ║
║                    Status: SOVEREIGN-READY                                       ║
║                                                                                   ║
║                    CHE·NU V76 - L'Économie de la Résonance                       ║
║                                                                                   ║
║                    "La circulation crée la vie,                                  ║
║                     l'accumulation crée la mort"                                 ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

**Document créé:** 23-01-2026
**Dernière mise à jour:** 23-01-2026
**Version:** 1.0
**Auteur:** Jonathan Emmanuel Rodrigue (Souverain)

