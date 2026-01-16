# CHE·NU™ - Guide de Déploiement Vercel

## 🚀 Déploiement en 5 Minutes

### 1. Créer un compte Vercel

1. Allez sur [vercel.com](https://vercel.com)
2. Inscrivez-vous avec GitHub, GitLab, ou email
3. Vérifiez votre compte

### 2. Obtenir un Token API

1. Connectez-vous à Vercel
2. Allez dans **Settings** → **Tokens**
3. Cliquez **Create Token**
4. Nom: `chenu-deployment`
5. Scope: **Full Account**
6. Cliquez **Create**
7. **COPIEZ LE TOKEN** (il ne sera plus visible après!)

### 3. Créer un Projet Vercel

#### Option A: Via l'interface CHE·NU

1. Lancez l'application CHE·NU
2. Allez dans **Settings** → **Déploiement**
3. Collez votre token Vercel
4. Cliquez **Connecter**

#### Option B: Via le CLI Vercel

```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Dans le dossier frontend
cd frontend
vercel

# Suivre les instructions
# - Projet existant ou nouveau? Nouveau
# - Nom du projet: chenu-frontend
# - Répertoire: ./
# - Override settings? Non
```

### 4. Variables d'Environnement

Configurez ces variables dans Vercel (Settings → Environment Variables):

| Variable | Description | Exemple |
|----------|-------------|---------|
| `VITE_API_URL` | URL de votre backend | `https://api.chenu.app` |
| `VITE_SUPABASE_URL` | URL Supabase | `https://xxx.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Clé anonyme Supabase | `eyJhbGciOiJI...` |
| `VITE_STRIPE_PUBLIC_KEY` | Clé publique Stripe | `pk_live_...` |
| `VITE_APP_ENV` | Environnement | `production` |

### 5. Déployer

#### Via l'interface CHE·NU

1. Settings → Déploiement
2. Onglet **Déployer**
3. Cliquez **Déployer en Production**

#### Via le CLI

```bash
cd frontend
vercel --prod
```

#### Via Git (Recommandé)

1. Connectez votre repo GitHub dans Vercel
2. Chaque push sur `main` déclenchera un déploiement automatique

---

## 📁 Structure du Projet

```
frontend/
├── vercel.json         # Configuration Vercel
├── src/
│   └── components/
│       └── settings/
│           └── deployment/
│               └── VercelDeploymentManager.tsx
├── dist/               # Build output (généré)
└── package.json
```

---

## ⚙️ Configuration vercel.json

```json
{
  "name": "chenu-frontend",
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "VITE_API_URL": "@api_url",
    "VITE_SUPABASE_URL": "@supabase_url"
  }
}
```

---

## 🔄 Déploiement Continu

### GitHub Actions (optionnel)

Créez `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./frontend
```

---

## 🌐 Domaine Personnalisé

1. Dans Vercel → Settings → Domains
2. Ajoutez votre domaine (ex: `app.chenu.io`)
3. Configurez le DNS:
   - Type: CNAME
   - Name: app
   - Value: cname.vercel-dns.com
4. Attendez la propagation DNS (5-30 min)
5. SSL automatique via Let's Encrypt

---

## 🔍 Debugging

### Logs de Build

```bash
vercel logs <deployment-url>
```

### Variables d'environnement

```bash
vercel env ls
vercel env pull .env.local
```

### Rollback

```bash
# Lister les déploiements
vercel ls

# Rollback
vercel rollback <deployment-id>
```

---

## 📊 Analytics & Monitoring

1. Activez **Vercel Analytics** dans le dashboard
2. Ajoutez le script dans votre app:

```tsx
// src/main.tsx
import { Analytics } from '@vercel/analytics/react';

// Dans votre App
<Analytics />
```

---

## 🛡️ Sécurité

- ✅ Les tokens sont encryptés côté serveur
- ✅ Variables sensibles en mode "Secret"
- ✅ Headers de sécurité configurés
- ✅ SSL/TLS automatique

---

## 📞 Support

- [Documentation Vercel](https://vercel.com/docs)
- [Status Vercel](https://vercel-status.com)
- [Discord CHE·NU](https://discord.gg/chenu)

---

*CHE·NU™ - Governed Intelligence Operating System*
