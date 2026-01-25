# 🔐 AT·OM — EMPLACEMENTS DES CLÉS

> **Document de référence pour la rotation des clés**
> Une fois que tu auras révoqué tes anciennes clés, copie-colle les nouvelles aux emplacements listés ci-dessous.

---

## 📍 FICHIER PRINCIPAL: `.env` (racine du projet)

**Chemin:** `C:\Users\admin\Github\ATOM\.env`

C'est le **SEUL** fichier où tu dois mettre tes clés. Tous les services lisent depuis ce fichier.

---

## 🔑 CLÉS À CONFIGURER

### 1. HEDERA HASHGRAPH
```
HEDERA_OPERATOR_ID=0.0.7727679          ← Ton Account ID (déjà configuré)
HEDERA_OPERATOR_KEY=xxxxxxxxxx          ← Ta Private Key Hedera
MY_PRIVATE_KEY=xxxxxxxxxx               ← Même clé (alias pour compatibilité)
```

**Où obtenir:** https://portal.hedera.com/

---

### 2. SUPABASE
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1...
```

**Où obtenir:** Supabase Dashboard > Settings > API

---

### 3. DATABASE (DigitalOcean)
```
DATABASE_URL=postgresql+asyncpg://Admin:MOT_DE_PASSE@...
```

**Où obtenir:** DigitalOcean > Databases > Connection Details

---

### 4. JWT (Généré automatiquement ou personnalisé)
```
JWT_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Générer une nouvelle clé:**
```bash
openssl rand -hex 32
```

---

## 🌐 PLATEFORMES DE DÉPLOIEMENT

### VERCEL (Frontend)
**Dashboard:** https://vercel.com/dashboard

**Variables à configurer dans Settings > Environment Variables:**
- `HEDERA_NETWORK` = testnet
- `HEDERA_OPERATOR_ID` = 0.0.7727679
- `HEDERA_OPERATOR_KEY` = [ta clé]
- `SUPABASE_URL` = [ton url]
- `SUPABASE_ANON_KEY` = [ta clé anon]

---

### DIGITALOCEAN (Backend)
**Dashboard:** https://cloud.digitalocean.com/apps

**Variables à configurer dans App > Settings > App-Level Environment Variables:**
- `DATABASE_URL` = [ta connexion postgres]
- `JWT_SECRET_KEY` = [ta clé jwt]
- `HEDERA_OPERATOR_ID` = 0.0.7727679
- `HEDERA_OPERATOR_KEY` = [ta clé]
- `SUPABASE_URL` = [ton url]
- `SUPABASE_SERVICE_ROLE_KEY` = [ta clé service]

---

## ✅ CHECKLIST DE ROTATION DES CLÉS

1. [ ] Générer nouvelles clés Hedera sur portal.hedera.com
2. [ ] Générer nouvelles clés Supabase (Settings > API > Regenerate)
3. [ ] Mettre à jour `.env` local
4. [ ] Mettre à jour Vercel Environment Variables
5. [ ] Mettre à jour DigitalOcean Environment Variables
6. [ ] Tester connexion Hedera: `npm run test-connection` dans `services/hedera/`
7. [ ] Tester connexion Supabase: `npm run test-connection` dans `services/database/`
8. [ ] Révoquer les anciennes clés

---

## 🛡️ SÉCURITÉ

- **JAMAIS** commit le fichier `.env` sur GitHub
- Le `.gitignore` est configuré pour exclure tous les fichiers `.env`
- Utiliser des variables d'environnement sur les plateformes de déploiement
- Rotation des clés recommandée tous les 90 jours

---

**Dernière mise à jour:** 2026-01-24
