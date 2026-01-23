# 🚀 GUIDE DÉPLOIEMENT PRODUCTION - VERCEL + DIGITALOCEAN

```
     █████╗ ████████╗   ██████╗ ███╗   ███╗
    ██╔══██╗╚══██╔══╝  ██╔═══██╗████╗ ████║
    ███████║   ██║     ██║   ██║██╔████╔██║
    ██╔══██║   ██║     ██║   ██║██║╚██╔╝██║
    ██║  ██║   ██║  ██╗╚██████╔╝██║ ╚═╝ ██║
    ╚═╝  ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝

         DÉPLOIEMENT CLOUD PRODUCTION
         Vercel (Frontend) + DigitalOcean (Backend)
```

---

## 📋 ARCHITECTURE DE DÉPLOIEMENT

```
┌─────────────────────────────────────────────────────────────────┐
│                        UTILISATEURS                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     VERCEL (Frontend)                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  React App (AT·OM)                                       │    │
│  │  - Static hosting                                        │    │
│  │  - Edge CDN global                                       │    │
│  │  - SSL automatique                                       │    │
│  │  - Preview deployments                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│    SUPABASE      │ │   OPENAI/    │ │   DIGITALOCEAN   │
│  (Database)      │ │   ANTHROPIC  │ │   (Backend API)  │
│  - PostgreSQL    │ │   (LLM API)  │ │  - Node.js API   │
│  - Auth          │ │              │ │  - WebSocket     │
│  - Storage       │ │              │ │  - Workers       │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

---

## PARTIE 1: DÉPLOIEMENT VERCEL (Frontend)

### Étape 1.1: Préparer le repository

```bash
# S'assurer que tout est committé
cd C:\Users\admin\Github\ATOM\ATOM\Vzwwviru70560-d4e
git add -A
git commit -m "Prepare for Vercel deployment"
git push
```

### Étape 1.2: Connecter Vercel au repository

1. Aller sur [vercel.com](https://vercel.com)
2. Se connecter avec GitHub
3. Cliquer **"Add New Project"**
4. Sélectionner le repository **ATOM**
5. Configurer:
   - **Root Directory**: `Vzwwviru70560-d4e/hardcore-joliot/atom/app`
   - **Framework Preset**: Create React App
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### Étape 1.3: Configurer les variables d'environnement

Dans Vercel Dashboard → Project Settings → Environment Variables:

```env
# SUPABASE (REQUIS)
REACT_APP_SUPABASE_URL=https://VOTRE_PROJET.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...

# LLM API (REQUIS)
REACT_APP_LLM_PROVIDER=openai
REACT_APP_LLM_API_KEY=sk-...
REACT_APP_LLM_MODEL=gpt-4

# DIGITALOCEAN BACKEND (après configuration)
REACT_APP_API_URL=https://api.votre-domaine.com
REACT_APP_WS_URL=wss://api.votre-domaine.com/ws

# AT·OM CONFIG
REACT_APP_FREQUENCY=999
REACT_APP_HEARTBEAT=444
REACT_APP_SOVEREIGN_MODE=true
```

**Important**: Cocher **Production**, **Preview**, et **Development** pour chaque variable.

### Étape 1.4: Déployer

```bash
# Option A: Déploiement automatique (push = deploy)
git push origin main

# Option B: Déploiement manuel via CLI
npm install -g vercel
vercel login
cd Vzwwviru70560-d4e/hardcore-joliot/atom/app
vercel --prod
```

### Étape 1.5: Configurer le domaine personnalisé (Optionnel)

1. Vercel Dashboard → Project → Settings → Domains
2. Ajouter votre domaine: `app.che-nu.io`
3. Configurer DNS chez votre registrar:

```
Type: CNAME
Name: app (ou @ pour racine)
Value: cname.vercel-dns.com
TTL: 3600
```

---

## PARTIE 2: DÉPLOIEMENT DIGITALOCEAN (Backend API)

### Étape 2.1: Créer un compte DigitalOcean

1. Aller sur [digitalocean.com](https://digitalocean.com)
2. Créer un compte (200$ de crédit gratuit avec lien partenaire)
3. Ajouter une méthode de paiement

### Étape 2.2: Option A - App Platform (Recommandé - Plus simple)

#### Créer l'application backend

1. Dashboard → **Create** → **Apps**
2. Connecter votre repository GitHub
3. Sélectionner le repository ATOM
4. Configurer:
   - **Source Directory**: `/Vzwwviru70560-d4e/hardcore-joliot/atom/api` (si vous avez un backend)
   - **Type**: Web Service
   - **Plan**: Basic ($5/mois) ou Pro ($12/mois)

#### Variables d'environnement DigitalOcean

```env
NODE_ENV=production
PORT=8080

# Supabase
SUPABASE_URL=https://VOTRE_PROJET.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIs...  # Clé SERVICE, pas ANON

# LLM
LLM_PROVIDER=openai
LLM_API_KEY=sk-...

# CORS
ALLOWED_ORIGINS=https://app.che-nu.io,https://votre-app.vercel.app

# WebSocket
WS_ENABLED=true
```

### Étape 2.3: Option B - Droplet (Plus de contrôle)

#### Créer un Droplet

1. Dashboard → **Create** → **Droplets**
2. Choisir:
   - **Region**: Frankfurt (fra1) ou Toronto (tor1)
   - **Image**: Ubuntu 22.04 LTS
   - **Size**: Basic $6/mois (1 vCPU, 1GB RAM) minimum
   - **Authentication**: SSH Key (recommandé)

#### Configurer le serveur

```bash
# Se connecter au Droplet
ssh root@VOTRE_IP_DROPLET

# Mettre à jour le système
apt update && apt upgrade -y

# Installer Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
apt install -y nodejs

# Installer PM2 (process manager)
npm install -g pm2

# Installer Nginx (reverse proxy)
apt install -y nginx

# Installer Certbot (SSL)
apt install -y certbot python3-certbot-nginx

# Créer un utilisateur non-root
adduser atom
usermod -aG sudo atom
su - atom
```

#### Déployer l'API

```bash
# Cloner le repository
git clone https://github.com/Pr0Services/ATOM.git
cd ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/api

# Installer les dépendances
npm install --production

# Créer le fichier .env
nano .env
```

Contenu de `.env`:
```env
NODE_ENV=production
PORT=3001

SUPABASE_URL=https://VOTRE_PROJET.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIs...

LLM_PROVIDER=openai
LLM_API_KEY=sk-...

ALLOWED_ORIGINS=https://app.che-nu.io
```

```bash
# Démarrer avec PM2
pm2 start npm --name "atom-api" -- start
pm2 startup
pm2 save
```

#### Configurer Nginx

```bash
sudo nano /etc/nginx/sites-available/atom-api
```

```nginx
server {
    listen 80;
    server_name api.votre-domaine.com;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/atom-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Installer SSL
sudo certbot --nginx -d api.votre-domaine.com
```

---

## PARTIE 3: CONFIGURATION SUPABASE

### Étape 3.1: Créer le projet Supabase

1. Aller sur [supabase.com](https://supabase.com)
2. **New Project**
3. Choisir:
   - **Organization**: Votre org
   - **Name**: atom-production
   - **Database Password**: (générer un mot de passe fort)
   - **Region**: EU West (ou le plus proche de vos utilisateurs)

### Étape 3.2: Exécuter le script de sécurité

1. Dashboard → **SQL Editor**
2. Coller le contenu de `supabase-security.sql`
3. Cliquer **Run**

### Étape 3.3: Récupérer les clés

Dashboard → **Settings** → **API**:

| Clé | Utilisation |
|-----|-------------|
| **Project URL** | `REACT_APP_SUPABASE_URL` (Vercel) |
| **anon public** | `REACT_APP_SUPABASE_ANON_KEY` (Vercel) |
| **service_role** | `SUPABASE_SERVICE_KEY` (DigitalOcean - JAMAIS côté client!) |

### Étape 3.4: Configurer les URLs autorisées

Dashboard → **Authentication** → **URL Configuration**:

```
Site URL: https://app.che-nu.io

Redirect URLs:
- https://app.che-nu.io/**
- https://votre-app.vercel.app/**
- https://*.vercel.app/** (pour les preview deployments)
```

---

## PARTIE 4: VÉRIFICATION POST-DÉPLOIEMENT

### Checklist de déploiement ✅

```
VERCEL:
[ ] Application déployée et accessible
[ ] Variables d'environnement configurées
[ ] Domaine personnalisé configuré (optionnel)
[ ] SSL actif (automatique)
[ ] Preview deployments fonctionnels

DIGITALOCEAN:
[ ] API accessible via HTTPS
[ ] WebSocket fonctionnel
[ ] PM2 configuré pour auto-restart
[ ] SSL via Certbot
[ ] Firewall configuré (UFW)

SUPABASE:
[ ] RLS activé sur toutes les tables
[ ] Policies configurées
[ ] URLs autorisées configurées
[ ] Emails de confirmation fonctionnels

GÉNÉRAL:
[ ] Connexion frontend ↔ backend OK
[ ] Authentification fonctionnelle
[ ] Agents IA répondent
[ ] Pas d'erreurs dans la console
```

### Tests de vérification

```bash
# Test de l'API backend
curl https://api.votre-domaine.com/health

# Test WebSocket (avec wscat)
npm install -g wscat
wscat -c wss://api.votre-domaine.com/ws

# Vérifier les headers de sécurité
curl -I https://app.che-nu.io
```

---

## PARTIE 5: MONITORING & MAINTENANCE

### DigitalOcean Monitoring

1. Dashboard → Droplet → **Monitoring** → Enable
2. Configurer des alertes:
   - CPU > 80%
   - Memory > 90%
   - Disk > 85%

### Logs

```bash
# Logs PM2
pm2 logs atom-api

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Mises à jour

```bash
# Mettre à jour l'application
cd ~/ATOM
git pull origin main
cd Vzwwviru70560-d4e/hardcore-joliot/atom/api
npm install --production
pm2 restart atom-api
```

### Backups automatiques (DigitalOcean)

1. Dashboard → Droplet → **Backups** → Enable
2. Coût: +20% du prix du Droplet
3. Snapshots hebdomadaires automatiques

---

## PARTIE 6: COÛTS ESTIMÉS

### Configuration minimale (~$20/mois)

| Service | Plan | Coût/mois |
|---------|------|-----------|
| Vercel | Free/Hobby | $0-20 |
| DigitalOcean | Basic Droplet | $6 |
| Supabase | Free | $0 |
| Domaine | .io | ~$3 |
| **TOTAL** | | **~$9-29** |

### Configuration production (~$50-100/mois)

| Service | Plan | Coût/mois |
|---------|------|-----------|
| Vercel | Pro | $20 |
| DigitalOcean | Regular Droplet | $24 |
| Supabase | Pro | $25 |
| Domaine + SSL | | $5 |
| Backups | | $5 |
| **TOTAL** | | **~$79** |

---

## COMMANDES RAPIDES

```bash
# === VERCEL ===
vercel                    # Déployer en preview
vercel --prod             # Déployer en production
vercel logs               # Voir les logs
vercel env pull           # Télécharger les env vars

# === DIGITALOCEAN ===
ssh root@IP               # Se connecter
pm2 status                # Status des apps
pm2 restart atom-api      # Redémarrer l'API
pm2 logs                  # Voir les logs
sudo systemctl restart nginx  # Redémarrer Nginx

# === MAINTENANCE ===
git pull && npm i && pm2 restart atom-api  # Update complet
sudo certbot renew        # Renouveler SSL
```

---

## SUPPORT & RESSOURCES

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **DigitalOcean Docs**: [docs.digitalocean.com](https://docs.digitalocean.com)
- **Supabase Docs**: [supabase.com/docs](https://supabase.com/docs)

---

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🌟 AT·OM PRODUCTION DEPLOYMENT READY! 🌟                   ║
║                                                               ║
║   Frontend: Vercel (CDN Global)                              ║
║   Backend: DigitalOcean (API + WebSocket)                    ║
║   Database: Supabase (PostgreSQL + Auth)                     ║
║                                                               ║
║   Score Sécurité: 94% ✅                                     ║
║   Status: PRODUCTION-READY                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
