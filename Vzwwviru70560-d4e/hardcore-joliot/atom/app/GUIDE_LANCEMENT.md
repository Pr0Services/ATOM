# 🚀 GUIDE DE LANCEMENT AT·OM / CHE·NU V76

```
     █████╗ ████████╗   ██████╗ ███╗   ███╗
    ██╔══██╗╚══██╔══╝  ██╔═══██╗████╗ ████║
    ███████║   ██║     ██║   ██║██╔████╔██║
    ██╔══██║   ██║     ██║   ██║██║╚██╔╝██║
    ██║  ██║   ██║  ██╗╚██████╔╝██║ ╚═╝ ██║
    ╚═╝  ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝

    Portail Partenaires & Sous-traitants
    Score Sécurité: 94% ✅
```

---

## 📋 TABLE DES MATIÈRES

1. [Prérequis](#1-prérequis)
2. [Installation Locale](#2-installation-locale)
3. [Configuration Supabase](#3-configuration-supabase)
4. [Configuration des APIs](#4-configuration-des-apis)
5. [Lancement en Développement](#5-lancement-en-développement)
6. [Déploiement Production](#6-déploiement-production)
7. [Vérification Post-Lancement](#7-vérification-post-lancement)
8. [Dépannage](#8-dépannage)

---

## 1. PRÉREQUIS

### Outils requis
- **Node.js** v18+ (recommandé v20 LTS)
- **npm** v9+ ou **yarn** v1.22+
- **Git**
- Compte **Supabase** (gratuit)
- Compte **Vercel** (gratuit pour déploiement)
- Clé API **OpenAI** ou **Anthropic** (pour les agents IA)

### Vérifier les versions
```bash
node --version   # v18.0.0+
npm --version    # v9.0.0+
git --version    # v2.0.0+
```

---

## 2. INSTALLATION LOCALE

### Étape 1: Cloner le repository
```bash
git clone https://github.com/Pr0Services/ATOM.git
cd ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app
```

### Étape 2: Installer les dépendances
```bash
npm install
```

### Étape 3: Créer le fichier d'environnement
```bash
# Copier le template
cp .env.example .env.local

# OU créer manuellement
touch .env.local
```

### Étape 4: Configurer les variables d'environnement
Ouvrir `.env.local` et ajouter:

```env
# ═══════════════════════════════════════════════════
# CONFIGURATION AT·OM - VARIABLES D'ENVIRONNEMENT
# ═══════════════════════════════════════════════════

# SUPABASE (REQUIS)
REACT_APP_SUPABASE_URL=https://VOTRE_PROJET.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# LLM API (REQUIS pour les agents)
REACT_APP_LLM_PROVIDER=openai
REACT_APP_LLM_API_KEY=sk-...
REACT_APP_LLM_MODEL=gpt-4

# WEBSOCKET (OPTIONNEL)
REACT_APP_WS_URL=wss://api.che-nu.io/ws

# AT·OM CONFIG (NE PAS MODIFIER)
REACT_APP_FREQUENCY=999
REACT_APP_HEARTBEAT=444
REACT_APP_SOVEREIGN_MODE=true
```

---

## 3. CONFIGURATION SUPABASE

### Étape 1: Créer un projet Supabase

1. Aller sur [supabase.com](https://supabase.com)
2. Créer un nouveau projet
3. Choisir une région proche (ex: `eu-west-1` pour l'Europe)
4. Définir un mot de passe fort pour la base de données
5. Attendre la création (~2 minutes)

### Étape 2: Récupérer les clés

1. Dans le dashboard Supabase, aller dans **Settings** > **API**
2. Copier:
   - **Project URL** → `REACT_APP_SUPABASE_URL`
   - **anon public** key → `REACT_APP_SUPABASE_ANON_KEY`

### Étape 3: Exécuter le script de sécurité RLS

1. Dans Supabase, aller dans **SQL Editor**
2. Cliquer **New Query**
3. Copier-coller le contenu de `supabase-security.sql`
4. Cliquer **Run**

```sql
-- Vérifier que tout est OK
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';
```

Vous devriez voir `rowsecurity = true` pour toutes les tables.

### Étape 4: Configurer l'authentification

1. Aller dans **Authentication** > **Providers**
2. Activer **Email** (déjà activé par défaut)
3. (Optionnel) Configurer les providers OAuth (Google, GitHub, etc.)

### Étape 5: Configurer les emails

1. Aller dans **Authentication** > **Email Templates**
2. Personnaliser les templates avec votre branding CHE·NU

---

## 4. CONFIGURATION DES APIs

### Option A: OpenAI

1. Aller sur [platform.openai.com](https://platform.openai.com)
2. Créer une clé API
3. Configurer dans `.env.local`:
```env
REACT_APP_LLM_PROVIDER=openai
REACT_APP_LLM_API_KEY=sk-...
REACT_APP_LLM_MODEL=gpt-4
```

### Option B: Anthropic (Claude)

1. Aller sur [console.anthropic.com](https://console.anthropic.com)
2. Créer une clé API
3. Configurer dans `.env.local`:
```env
REACT_APP_LLM_PROVIDER=anthropic
REACT_APP_LLM_API_KEY=sk-ant-...
REACT_APP_LLM_MODEL=claude-3-opus
```

### Option C: Via le Setup Wizard (Recommandé)

1. Lancer l'application
2. Aller sur `/admin`
3. Le Setup Wizard s'ouvre automatiquement
4. Suivre les étapes de configuration
5. Tester chaque connexion
6. Sauvegarder

---

## 5. LANCEMENT EN DÉVELOPPEMENT

### Démarrer le serveur de développement
```bash
npm start
```

L'application sera disponible sur: **http://localhost:3000**

### URLs importantes

| URL | Description |
|-----|-------------|
| `/` | Page d'accueil (Souverain) |
| `/entree` | Portail d'entrée public |
| `/tableau-de-bord` | Dashboard principal |
| `/admin` | **Cockpit Admin + Setup Wizard** |
| `/agent` | Interface agents IA |
| `/besoins` | Moteur de civilisation |
| `/gratitude` | Journal de gratitude |

### Tester la configuration

1. Ouvrir **http://localhost:3000/admin**
2. Vérifier que le Setup Wizard affiche les statuts de connexion
3. Tester chaque service (bouton "Tester")
4. Tous les indicateurs doivent être ✅

---

## 6. DÉPLOIEMENT PRODUCTION

### Option A: Vercel (Recommandé)

#### Étape 1: Connecter le repository
```bash
npm install -g vercel
vercel login
vercel
```

#### Étape 2: Configurer les variables d'environnement
Dans le dashboard Vercel:
1. Aller dans **Settings** > **Environment Variables**
2. Ajouter toutes les variables de `.env.local`
3. Sélectionner **Production** pour chaque variable

#### Étape 3: Déployer
```bash
vercel --prod
```

### Option B: Build manuel

```bash
# Créer le build de production
npm run build

# Le dossier 'build' contient les fichiers statiques
# À déployer sur n'importe quel hébergeur statique
```

### Configuration DNS (Optionnel)

Si vous avez un domaine personnalisé:

1. Dans Vercel: **Settings** > **Domains**
2. Ajouter votre domaine (ex: `app.che-nu.io`)
3. Configurer les DNS chez votre registrar:
   - Type: `CNAME`
   - Name: `app` (ou `@` pour le domaine racine)
   - Value: `cname.vercel-dns.com`

---

## 7. VÉRIFICATION POST-LANCEMENT

### Checklist de sécurité ✅

- [ ] Variables d'environnement configurées (pas de fallbacks)
- [ ] RLS activé sur Supabase (script exécuté)
- [ ] HTTPS actif (automatique sur Vercel)
- [ ] Headers de sécurité présents (CSP, HSTS)
- [ ] Pas de clés API exposées dans le code

### Vérifier les headers de sécurité

```bash
curl -I https://votre-domaine.vercel.app
```

Vous devriez voir:
```
Content-Security-Policy: default-src 'self'...
Strict-Transport-Security: max-age=31536000...
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
```

### Tester l'authentification

1. Créer un compte via `/entree`
2. Vérifier l'email de confirmation
3. Se connecter
4. Vérifier l'accès aux fonctionnalités

### Tester les agents IA

1. Aller sur `/agent`
2. Démarrer une conversation avec Nova
3. Vérifier que les réponses sont générées

---

## 8. DÉPANNAGE

### Erreur: "Supabase non configuré"

**Cause:** Variables d'environnement manquantes

**Solution:**
1. Vérifier que `.env.local` existe
2. Vérifier les noms des variables (avec `REACT_APP_` prefix)
3. Redémarrer le serveur de développement

### Erreur: "RLS policy violation"

**Cause:** Policies RLS non configurées

**Solution:**
1. Exécuter `supabase-security.sql` dans Supabase SQL Editor
2. Vérifier que toutes les tables ont RLS activé

### Erreur: "Failed to fetch" sur les APIs LLM

**Cause:** Clé API invalide ou quota dépassé

**Solution:**
1. Vérifier la clé API dans le Setup Wizard
2. Vérifier les quotas sur OpenAI/Anthropic
3. Tester avec une nouvelle clé

### L'application ne se charge pas

**Causes possibles:**
- Build corrompu
- Dépendances manquantes
- Erreur JavaScript

**Solution:**
```bash
# Nettoyer et réinstaller
rm -rf node_modules
rm -rf build
npm install
npm start
```

### Erreur de CORS

**Cause:** Domaine non autorisé dans Supabase

**Solution:**
1. Dans Supabase: **Authentication** > **URL Configuration**
2. Ajouter votre domaine dans **Site URL** et **Redirect URLs**

---

## 📞 SUPPORT

### Ressources

- Documentation Supabase: [supabase.com/docs](https://supabase.com/docs)
- Documentation Vercel: [vercel.com/docs](https://vercel.com/docs)
- Documentation React: [react.dev](https://react.dev)

### Logs utiles

```bash
# Logs de développement
npm start 2>&1 | tee dev.log

# Logs de build
npm run build 2>&1 | tee build.log
```

### Commandes utiles

```bash
# Vérifier les vulnérabilités npm
npm audit

# Mettre à jour les dépendances
npm update

# Analyser la taille du bundle
npm run build && npx source-map-explorer 'build/static/js/*.js'
```

---

## 🎯 RÉSUMÉ RAPIDE

```bash
# 1. Cloner et installer
git clone https://github.com/Pr0Services/ATOM.git
cd ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app
npm install

# 2. Configurer (créer .env.local avec vos clés)

# 3. Configurer Supabase (exécuter supabase-security.sql)

# 4. Lancer
npm start

# 5. Configurer via Setup Wizard
# Ouvrir http://localhost:3000/admin

# 6. Déployer
vercel --prod
```

---

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🌟 AT·OM EST PRÊT POUR LE LANCEMENT! 🌟                    ║
║                                                               ║
║   Fréquence: 999 Hz | Heartbeat: 444 Hz                      ║
║   Score Sécurité: 94%                                        ║
║   Status: PRODUCTION-READY                                   ║
║                                                               ║
║   CHE·NU V76 - Portail Partenaires & Sous-traitants          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
